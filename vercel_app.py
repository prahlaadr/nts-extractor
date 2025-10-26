#!/usr/bin/env python3
"""
NTS Tracklist Extractor - Vercel Serverless Version
Outputs in "Song - Artist" format, excludes unreleased tracks
"""

from flask import Flask, render_template, request, send_file, jsonify
import requests
import json
import csv
import io
from datetime import datetime
import re

app = Flask(__name__)


def extract_tracklist_from_html(html: str):
    """Extract tracklist JSON from NTS episode HTML"""
    tracklist_start = html.find('"tracklist":[{')
    
    if tracklist_start == -1:
        return None
    
    json_start = html.find('[', tracklist_start)
    bracket_count = 0
    in_string = False
    escape_next = False
    
    for i in range(json_start, min(json_start + 500000, len(html))):
        char = html[i]
        
        if escape_next:
            escape_next = False
            continue
            
        if char == '\\':
            escape_next = True
            continue
            
        if char == '"' and not escape_next:
            in_string = not in_string
            continue
            
        if not in_string:
            if char == '[' or char == '{':
                bracket_count += 1
            elif char == ']' or char == '}':
                bracket_count -= 1
                
            if bracket_count == 0 and char == ']':
                json_end = i + 1
                json_str = html[json_start:json_end]
                
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    return None
                break
    
    return None


def is_unreleased_track(title: str) -> bool:
    """Check if track is unreleased"""
    if not title:
        return True
    
    title_lower = title.lower()
    unreleased_keywords = [
        'unreleased',
        'forthcoming',
        'tbc',
        'tba',
        'to be announced',
        'id - id',
        'unknown'
    ]
    
    return any(keyword in title_lower for keyword in unreleased_keywords)


def fetch_nts_tracklist(url: str):
    """Fetch and parse NTS episode tracklist"""
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    })
    response.raise_for_status()
    
    tracklist = extract_tracklist_from_html(response.text)
    
    if not tracklist:
        return None
    
    # Extract show name from URL
    show_name_match = re.search(r'/shows/([^/]+)/', url)
    show_name = show_name_match.group(1).replace('-', ' ').title() if show_name_match else "NTS Show"
    
    formatted_tracks = []
    for track in tracklist:
        title = track.get('title', '').strip()
        
        # Skip unreleased tracks
        if is_unreleased_track(title):
            continue
        
        # Get artists
        main_artists = [a['name'] for a in track.get('mainArtists', [])]
        featuring = [a['name'] for a in track.get('featuringArtists', [])]
        remix = [a['name'] for a in track.get('remixArtists', [])]
        
        if not main_artists:
            continue
        
        artist_str = ', '.join(main_artists)
        if featuring:
            artist_str += f" ft. {', '.join(featuring)}"
        
        # Add remix info to title
        if remix:
            title += f" ({', '.join(remix)} Remix)"
        
        # Format as "Song - Artist"
        formatted_line = f"{title} - {artist_str}"
        
        formatted_tracks.append({
            "formatted_line": formatted_line,
            "title": title,
            "artist": artist_str
        })
    
    return {
        "show_name": show_name,
        "url": url,
        "track_count": len(formatted_tracks),
        "tracks": formatted_tracks
    }


def create_text_output(data):
    """Create plain text output in Song - Artist format"""
    lines = []
    for track in data['tracks']:
        lines.append(track['formatted_line'])
    return '\n'.join(lines)


def create_csv(data):
    """Create CSV file from tracklist data"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Song', 'Artist'])
    
    # Write tracks
    for track in data['tracks']:
        writer.writerow([
            track['title'],
            track['artist']
        ])
    
    output.seek(0)
    return output


@app.route('/')
def index():
    """Main page"""
    return render_template('index_vercel.html')


@app.route('/api/extract', methods=['POST'])
def extract():
    """Extract tracklist from URL"""
    url = request.json.get('url', '').strip()
    
    if not url:
        return jsonify({"error": "Please provide a URL"}), 400
    
    if 'nts.live' not in url:
        return jsonify({"error": "Please provide a valid NTS.live URL"}), 400
    
    try:
        data = fetch_nts_tracklist(url)
        
        if not data:
            return jsonify({"error": "No tracklist found on this page"}), 404
        
        # Add text output
        data['text_output'] = create_text_output(data)
        
        return jsonify(data)
    
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch URL: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route('/api/download_csv', methods=['POST'])
def download_csv():
    """Download tracklist as CSV"""
    data = request.json
    
    if not data or 'tracks' not in data:
        return jsonify({"error": "No tracklist data provided"}), 400
    
    # Create CSV
    csv_file = create_csv(data)
    
    # Create filename
    show_name = data.get('show_name', 'nts_show').replace(' ', '_')
    timestamp = datetime.now().strftime('%Y%m%d')
    filename = f"{show_name}_{timestamp}.csv"
    
    # Convert to bytes
    csv_bytes = io.BytesIO(csv_file.getvalue().encode('utf-8'))
    
    return send_file(
        csv_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )


# Vercel serverless function handler
def handler(request):
    """Vercel serverless handler"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
