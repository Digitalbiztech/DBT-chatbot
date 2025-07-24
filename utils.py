import base64
import re
from urllib.parse import urlparse

# --- Helper Functions ---
def safe_filename_from_url(url):
    parsed = urlparse(url if url.startswith('http') else 'http://' + url)
    domain = parsed.netloc or parsed.path.split('/')[0]
    path = parsed.path.strip('/').replace('/', '_')
    if not path:
        path = 'index'
    return f"{domain}_{path}.pdf"

def url_to_safe_filename(url):
    # URL-safe base64 encoding, strip trailing '=' for shorter filenames
    encoded = base64.urlsafe_b64encode(url.encode('utf-8')).decode('ascii').rstrip('=')
    return encoded

def safe_filename_to_url(filename):
    # Add padding back for base64 decoding
    padding = '=' * (-len(filename) % 4)
    return base64.urlsafe_b64decode(filename + padding).decode('utf-8')

def extract_keywords(text, num_keywords=10):
    # List of target tags/keywords/phrases (add more as needed)
    TAGS = [
        "salesforce", "sap", "n8n", "ai automation", "data engineering", "vs code",
        "python", "machine learning", "cloud", "database", "etl", "api", "automation",
        "devops", "docker", "kubernetes", "sql", "big data", "analytics", "chatbot"
    ]
    text_lower = text.lower()
    found = []
    for tag in TAGS:
        # For multi-word tags, check as phrase; for single words, check as word boundary
        if " " in tag:
            if tag in text_lower:
                found.append(tag)
        else:
            if re.search(r'\b' + re.escape(tag) + r'\b', text_lower):
                found.append(tag)
        if len(found) >= num_keywords:
            break
    return found 