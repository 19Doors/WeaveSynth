import hashlib
import re

def normalize_url(url: str) -> str:
    """
    Basic URL normalization to improve consistency before hashing.
    """
    # Convert to lowercase
    url = url.lower()
    # Remove scheme (http, https) for consistency if desired, though often kept
    # url = re.sub(r'^https?:\/\/', '', url)
    # Remove www.
    url = re.sub(r'^www\.', '', url)
    # Remove trailing slash
    if url.endswith('/'):
        url = url[:-1]
    # Remove common tracking parameters (add more as needed)
    url = re.sub(r'\?utm_.*$', '', url)
    url = re.sub(r'&utm_.*$', '', url)
    # Consider sorting query parameters if their order can vary but mean the same page
    # This is more complex and might require urlparse
    return url

def url_to_sha256_id(url: str) -> str:
    """Converts a URL to a SHA-256 hash string."""
    normalized = normalize_url(url)
    # Encode the string to bytes, then hash it
    hashed_url = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    return hashed_url
