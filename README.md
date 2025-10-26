# NTS Tracklist Extractor

A clean, minimalist web application that extracts tracklists from NTS Radio episodes and formats them in a copyable "Song - Artist" format.

## 🎵 Live Demo

**https://nts-extractor.vercel.app**

## ✨ Features

### Core Functionality
- **Instant Extraction**: Paste any NTS Radio episode URL and get the full tracklist instantly
- **Clean Formatting**: Outputs tracks in "Song - Artist" format for easy sharing
- **Smart Filtering**: Automatically excludes unreleased tracks (ID - ID, TBC, Unreleased, etc.)
- **Copy to Clipboard**: One-click copying of the entire tracklist
- **CSV Export**: Download tracklists as CSV files for spreadsheet use

### Design
- **Minimalist Black & White**: Clean, high-contrast interface inspired by NTS Radio's aesthetic
- **Monospace Output**: Courier New font for the tracklist output
- **Responsive**: Works on desktop, tablet, and mobile
- **No Rounded Corners**: Sharp, brutalist design language

## 🚀 How It Works

### Frontend (JavaScript)
1. User pastes an NTS episode URL
2. JavaScript sends POST request to `/api/extract` endpoint
3. Displays formatted tracklist in textarea
4. Provides copy and download functionality

### Backend (Python/Flask)
1. Receives NTS URL from frontend
2. Fetches the episode page HTML
3. Parses embedded JSON tracklist data from the page
4. Filters out unreleased tracks
5. Formats tracks as "Song - Artist"
6. Returns JSON response with:
   - Show name
   - Track count
   - Formatted tracklist
   - Individual track objects

### Key Components

**HTML Parsing** (`api/index.py:18-61`)
```python
def extract_tracklist_from_html(html: str)
```
- Finds the `"tracklist":[{` pattern in the HTML
- Extracts the JSON array using bracket counting
- Handles escaped characters and nested objects

**Track Filtering** (`api/index.py:64-80`)
```python
def is_unreleased_track(title: str) -> bool
```
- Detects keywords: "unreleased", "forthcoming", "tbc", "tba", "unknown", "id - id"
- Returns `True` if track should be excluded

**API Endpoints**
- `GET /` - Serves the main HTML page
- `POST /api/extract` - Extracts tracklist from URL
- `POST /api/download_csv` - Generates CSV file

## 📦 Project Structure

```
nts-extractor/
├── api/
│   └── index.py            # Main Flask application (serverless)
├── templates/
│   └── index_vercel.html   # Frontend HTML/CSS/JS
├── vercel.json             # Vercel deployment config
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🛠️ Local Development

### Prerequisites
- Python 3.12+
- pip or uv

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/nts-extractor.git
cd nts-extractor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or use uv (recommended)
uv venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
# Or with uv
uv pip install -r requirements.txt
```

### Running Locally

```bash
# For local testing, you can use the development script:
# (Note: The main app runs from api/index.py on Vercel)
python api/index.py

# App will be available at:
# http://localhost:5000
```

### Testing

Try these NTS URLs:
- `https://www.nts.live/shows/rap-vacation/episodes/rap-vacation-29th-august-2025`
- `https://www.nts.live/shows/soup-to-nuts-w-anu/episodes/soup-to-nuts-w-anu-16th-march-2024`

## 🌐 Deployment to Vercel

### Option 1: Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

### Option 2: GitHub Integration

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "Add New..." → "Project"
4. Import your GitHub repository
5. Vercel auto-detects the configuration
6. Click "Deploy"

### Environment Setup

No environment variables needed! The app works out of the box.

## 📋 Example Output

### Input
```
https://www.nts.live/shows/rap-vacation/episodes/rap-vacation-29th-august-2025
```

### Output
```
We Need We - Manchild
Vinca Rosea - MF DOOM
Chrome Dreams - Madlib
Birds Of Paradise - Yussef Dayes
DBZ - Your Old Droog, Method Man, Denzel Curry
...

Successfully extracted 36 tracks (unreleased excluded)
```

## 🔧 Technical Details

### Dependencies
- **Flask 3.0.0**: Web framework for Python
- **requests 2.31.0**: HTTP library for fetching NTS pages

### Why These Choices?

**Flask**: Lightweight, perfect for serverless functions, easy to deploy on Vercel

**No Database**: Stateless design means no database needed, making deployment simple

**Server-side Rendering**: HTML parsing happens on the backend to avoid CORS issues

**Monospace Font**: Makes tracklists look cleaner and more professional when copying

## 🎨 Design Philosophy

### Color Scheme
- `#000000` - Pure black background
- `#ffffff` - Pure white text and borders
- `#0a0a0a` - Slightly lighter black for cards
- `#1a1a1a` - Dark gray for hover states

### Typography
- **Headers**: Helvetica Neue, bold, uppercase, tight letter-spacing
- **Body**: Helvetica Neue, regular weight
- **Tracklist**: Courier New monospace for clean alignment

### Aesthetic Goals
- **Brutalist**: No rounded corners, sharp edges
- **High Contrast**: Black and white only
- **Minimal**: No unnecessary elements
- **Functional**: Every element serves a purpose

## 🤝 Contributing

Found a bug or want to add a feature? Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [NTS Radio](https://www.nts.live) - For the amazing music and inspiration
- [Vercel](https://vercel.com) - For the excellent serverless deployment platform
- [Flask](https://flask.palletsprojects.com) - For the simple and elegant web framework

## 📧 Contact

Have questions or suggestions? Open an issue on GitHub!

---

Built with ❤️ for music lovers
