import re
import urllib.parse
import math
from collections import Counter

def calculate_entropy(text):
    if not text:
        return 0
    entropy = 0
    for x in Counter(text).values():
        p_x = float(x) / len(text)
        entropy -= p_x * math.log(p_x, 2)
    return entropy

def extract_features(url):
    """
    Extracts features from a given URL to be used for machine learning.
    Returns a dictionary of features.
    """
    features = {}
    
    # 1. Length of URL
    features['url_length'] = len(url)
    
    # 2. Protocol Check
    features['has_https'] = 1 if url.startswith("https://") else 0
    features['is_http'] = 1 if url.startswith("http://") else 0
    
    # 3. "@" Symbol
    features['has_at_symbol'] = 1 if "@" in url else 0
    
    # Parse URL to get the domain
    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc
        path = parsed_url.path
    except Exception:
        domain = ""
        path = ""
        
    # Domain specific features
    features['domain_length'] = len(domain)
    features['path_length'] = len(path)
    
    # 4. IP Address in URL
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    features['has_ip'] = 1 if ip_pattern.match(domain) else 0
    
    # 5. Number of Dots in domain
    features['num_dots'] = domain.count('.')
    
    # 6. Hyphen in Domain
    features['num_hyphens'] = domain.count('-')
    
    # 7. Suspicious Keywords
    suspicious_words = ['login', 'verify', 'free', 'update', 'bonus', 'secure', 'account', 'banking', 'admin', 'pay', 'bank', 'confirm']
    lower_url = url.lower()
    has_suspicious = any(word in lower_url for word in suspicious_words)
    features['has_suspicious_words'] = 1 if has_suspicious else 0
    
    # 8. URL Shorteners
    shorteners = ['bit.ly', 'goo.gl', 'tinyurl.com', 'is.gd', 'cli.gs', 't.co', 'ow.ly', 't.ly']
    has_shortener = any(shortener in domain for shortener in shorteners)
    features['is_shortened'] = 1 if has_shortener else 0
    
    # 9. Entropy (High entropy indicates random characters common in DGA/malicious domains)
    features['entropy'] = calculate_entropy(url)
    
    return features

if __name__ == "__main__":
    # Test
    print(extract_features("https://www.google.com"))
    print(extract_features("http://192.168.1.1/login-update-free-bonus.com"))
