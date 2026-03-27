import pandas as pd
import random
from feature_extractor import extract_features

# Base domains and patterns
safe_domains = ['google.com', 'youtube.com', 'facebook.com', 'wikipedia.org', 'amazon.com', 'twitter.com', 'instagram.com', 'linkedin.com', 'apple.com', 'microsoft.com', 'github.com', 'stackoverflow.com', 'netflix.com']
safe_paths = ['', '/about', '/contact', '/privacy', '/terms', '/help', '/search?q=test', '/profile', '/settings']

malicious_templates = [
    "http://{ip}/{path}",
    "http://{subdomain}.{domain}/{path}",
    "https://{domain}-{keyword}.com/{path}",
    "http://{shortener}/{path}",
    "http://{domain}@{ip}/{path}"
]

suspicious_keywords = ['login', 'verify', 'free', 'update', 'bonus', 'secure', 'account']
shorteners = ['bit.ly', 'goo.gl', 'tinyurl.com']

def generate_ip():
    return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

def generate_safe_url():
    domain = random.choice(safe_domains)
    path = random.choice(safe_paths)
    prefix = "https://" if random.random() > 0.1 else "http://" # mostly https
    return f"{prefix}www.{domain}{path}"

def generate_malicious_url():
    template = random.choice(malicious_templates)
    ip = generate_ip()
    domain = random.choice(['bank', 'paypal', 'apple', 'amazon', 'microsoft'])
    subdomain = random.choice(suspicious_keywords)
    path = random.choice(suspicious_keywords) + ".php"
    keyword = random.choice(suspicious_keywords)
    shortener = random.choice(shorteners)
    
    url = template.format(ip=ip, domain=domain, subdomain=subdomain, path=path, keyword=keyword, shortener=shortener)
    return url

if __name__ == "__main__":
    print("Generating synthetic dataset...")
    
    data = []
    
    # Generate 2500 safe URLs
    for _ in range(2500):
        url = generate_safe_url()
        features = extract_features(url)
        features['label'] = 0 # 0 for Safe
        features['url'] = url
        data.append(features)
        
    # Generate 2500 malicious URLs
    for _ in range(2500):
        url = generate_malicious_url()
        # Force a lot of malicious URLs to be http to emphasize it as a feature
        if random.random() > 0.3: 
            url = url.replace("https://", "http://")
            
        features = extract_features(url)
        features['label'] = 1 # 1 for Malicious
        features['url'] = url
        data.append(features)
        
    # Shuffle dataset
    random.shuffle(data)
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    
    # Reorder columns to put URL first and label last
    feature_cols = [c for c in df.columns if c not in ['url', 'label']]
    df = df[['url'] + feature_cols + ['label']]
    
    df.to_csv("dataset.csv", index=False)
    print("Dataset generated successfully with 2000 records: dataset.csv")

