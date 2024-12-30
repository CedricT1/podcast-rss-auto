from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os
import configparser
from feedgen.feed import FeedGenerator
import re
from threading import Thread
import time
from urllib.parse import urljoin
import mimetypes
import email.utils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_CHANGES'] = False

db = SQLAlchemy(app)

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Configuration for podcasts
PODCAST_CONFIG = {
    'scan_directory': config.get('podcasts', 'podcast_directory', fallback='podcasts/'),
    'supported_formats': ['.mp3', '.m4a', '.wav'],
    'metadata_fields': ['title', 'author', 'duration', 'published_date'],
    'title': config.get('podcasts', 'podcast_title', fallback='Podcasts'),
    'description': config.get('podcasts', 'podcast_description', fallback='Liste des podcasts disponibles'),
    'base_url': config.get('podcasts', 'base_url', fallback='').rstrip('/'),
    'image_url': config.get('podcasts', 'image_url', fallback=''),
    'author': config.get('podcasts', 'author', fallback=''),
    'email': config.get('podcasts', 'email', fallback=''),
    'categories': config.get('podcasts', 'categories', fallback='Religion & Spirituality').split(','),
    'language': config.get('podcasts', 'language', fallback='fr')
}

def get_file_size(file_path):
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0

def get_mime_type(file_path):
    """Get MIME type of file"""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'

def format_rfc822_date(dt):
    """Format datetime as RFC 822 string"""
    return email.utils.format_datetime(dt)

def get_full_url(endpoint, **kwargs):
    """Generate full URL using base_url from config if available"""
    if PODCAST_CONFIG['base_url']:
        path = url_for(endpoint, _external=False, **kwargs)
        return urljoin(PODCAST_CONFIG['base_url'] + '/', path.lstrip('/'))
    return url_for(endpoint, _external=True, **kwargs)

# Function to parse date from filename
def parse_date_from_filename(filename):
    match = re.search(r'(\d{6})_(\d{4})', filename)
    if match:
        date_str, time_str = match.groups()
        try:
            dt = datetime.strptime(f"{date_str}_{time_str}", "%d%m%y_%H%M")
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return datetime.now(timezone.utc)
    return datetime.now(timezone.utc)

def format_date(date):
    """Format the date in French"""
    mois = {
        1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril',
        5: 'mai', 6: 'juin', 7: 'juillet', 8: 'août',
        9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
    }
    return f"{date.day} {mois[date.month]} {date.year} à {date.hour:02d}h{date.minute:02d}"

# Function to scan podcasts
def scan_podcasts():
    """
    Scan the configured podcast directory for audio files and extract metadata
    """
    podcast_files = []
    try:
        for root, dirs, files in os.walk(PODCAST_CONFIG['scan_directory']):
            for file in files:
                if any(file.endswith(ext) for ext in PODCAST_CONFIG['supported_formats']):
                    date = parse_date_from_filename(file)
                    podcast_title = os.path.splitext(file)[0].replace('-', ' ').title()
                    podcast_files.append({
                        'title': podcast_title,
                        'url': file,
                        'date': format_date(date)
                    })
        return sorted(podcast_files, key=lambda x: parse_date_from_filename(x['url']), reverse=True)
    except Exception as e:
        print(f"Error scanning podcasts: {str(e)}")
        return []

@app.route('/')
def index():
    podcast_files = scan_podcasts()
    return render_template('index.html', podcasts=podcast_files, now=datetime.now(), config=PODCAST_CONFIG, get_full_url=get_full_url)

@app.route('/download/<path:filename>')
def download_file(filename):
    directory = os.path.join(os.getcwd(), PODCAST_CONFIG['scan_directory'])
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/feed.xml')
def rss_feed():
    fg = FeedGenerator()
    fg.load_extension('podcast')
    
    # Configuration du podcast
    fg.title(PODCAST_CONFIG['title'])
    fg.description(PODCAST_CONFIG['description'])
    fg.link(href=get_full_url('rss_feed'))
    fg.language(PODCAST_CONFIG['language'])
    
    if PODCAST_CONFIG['image_url']:
        fg.image(PODCAST_CONFIG['image_url'])
        fg.podcast.itunes_image(PODCAST_CONFIG['image_url'])
    
    if PODCAST_CONFIG['author']:
        fg.author({'name': PODCAST_CONFIG['author'], 'email': PODCAST_CONFIG['email']})
        fg.podcast.itunes_author(PODCAST_CONFIG['author'])
    
    # Catégories iTunes
    for category in PODCAST_CONFIG['categories']:
        fg.podcast.itunes_category(category.strip())
    
    podcast_files = scan_podcasts()
    
    for podcast in podcast_files:
        fe = fg.add_entry()
        fe.title(podcast['title'])
        
        # URL du fichier audio
        file_url = get_full_url('download_file', filename=podcast['url'])
        fe.link(href=file_url)
        
        # Date de publication
        pub_date = parse_date_from_filename(podcast['url'])
        fe.published(pub_date)
        fe.pubDate(format_rfc822_date(pub_date))
        
        # Description
        description = f"Épisode diffusé le {format_date(pub_date)}"
        fe.description(description)
        fe.podcast.itunes_summary(description)
        
        # Fichier audio
        file_path = os.path.join(os.getcwd(), PODCAST_CONFIG['scan_directory'], podcast['url'])
        fe.enclosure(file_url, str(get_file_size(file_path)), get_mime_type(file_path))
        
        # GUID unique
        fe.guid(file_url)
        
    response = make_response(fg.rss_str(pretty=True))
    response.headers.set('Content-Type', 'application/rss+xml; charset=utf-8')
    return response

def background_scan():
    """
    Background thread to periodically scan for new podcasts
    """
    while True:
        print("Scanning for new podcasts...")
        scan_podcasts()
        # Get scan interval from config (in seconds)
        scan_interval = int(config.get('podcasts', 'scan_interval', fallback=3600))
        time.sleep(scan_interval)

if __name__ == '__main__':
    # Start background scanner
    scanner_thread = Thread(target=background_scan, daemon=True)
    scanner_thread.start()
    
    app.run(debug=True)