
import re
import base64
import cloudscraper
from bs4 import BeautifulSoup

class selcuk:
    def __init__(self):
        self.base_url = "https://selcukflix.net"
        self.scraper = cloudscraper.create_scraper()
        self.resolver_patterns = {"Mixdrop": "mixdrop\\.co/e/([a-z0-9]+)", "Streamtape": "streamtape\\.com/e/([a-z0-9]+)", "Fembed": "fembed\\.com/v/([a-z0-9]+)", "M3U8-Direct": "https?://[^\\s/$.?#].[^\\s]*\\.m3u8"}

    def search(self, query):
        results = []
        try:
            url = f"{self.base_url}/?s={query.replace(' ', '+')}"
            res = self.scraper.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            for article in soup.find_all(['article', 'div', 'li'], class_=re.compile(r'(item|post|film|movie)')):
                a_tag = article.find('a', href=True)
                img_tag = article.find('img')
                if a_tag and len(a_tag.text.strip()) > 2:
                    title = a_tag.get('title') or a_tag.text.strip()
                    link = a_tag['href']
                    poster = ""
                    if img_tag:
                        poster = img_tag.get('data-src') or img_tag.get('src') or ""
                    results.append({"title": title, "url": link, "poster": poster})
        except: pass
        return results

    def get_sources(self, page_url):
        sources = []
        try:
            res = self.scraper.get(page_url)
            content = res.text
            base64_links = re.findall(r'base64,([A-Za-z0-9+/=]+)', content)
            for b_link in base64_links:
                try:
                    decoded = base64.b64decode(b_link).decode('utf-8')
                    if "http" in decoded: sources.append({"name": "Decoded", "url": decoded})
                except: pass
            for name, pattern in self.resolver_patterns.items():
                matches = re.findall(pattern, content)
                for m in matches:
                    l = m if m.startswith('http') else f"https://{name.lower()}.com/e/{m}"
                    sources.append({"name": name, "url": l})
        except: pass
        return sources
