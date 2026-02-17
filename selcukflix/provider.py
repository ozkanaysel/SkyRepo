
import re
import cloudscraper
from bs4 import BeautifulSoup

class selcukflix:
    def __init__(self):
        self.name = "selcukflix"
        self.base_url = "https://selcukflix.net"
        self.scraper = cloudscraper.create_scraper()

    def detect_info(self, text):
        t = text.lower()
        info = []
        if "dublaj" in t or "tr-du" in t: info.append("TR-DUBLAJ")
        if "altyazı" in t or "sub" in t: info.append("ALT-YAZI")
        if "1080" in t: info.append("1080p")
        return " | ".join(info) if info else "HD"

    def search(self, query):
        results = []
        try:
            search_url = f"{self.base_url}/?s={query.replace(' ', '+')}"
            res = self.scraper.get(search_url)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            for item in soup.select('div.result-item, article, .post, .ml-item'):
                a = item.find('a', href=True)
                img = item.find('img')
                if a:
                    raw_title = a.text.strip() or a.get('title', '')
                    meta = self.detect_info(raw_title)
                    results.append({
                        "title": f"[{meta}] {raw_title}",
                        "url": a['href'] if a['href'].startswith('http') else self.base_url + a['href'],
                        "poster": img.get('data-src') or img.get('src') if img else ""
                    })
        except: pass
        return results

    def get_sources(self, url):
        sources = []
        try:
            res = self.scraper.get(url)
            content = res.text
            # Video hostlarını tara (Mixdrop, Streamtape, Fembed vb.)
            patterns = [
                r'src=["'](https?://[^"']+\.(?:m3u8|mp4))["']',
                r'src=["'](https?://(?:mixdrop|streamtape|fembed)[^"']+)["']'
            ]
            for p in patterns:
                links = re.findall(p, content)
                for link in links:
                    sources.append({"name": "Server", "url": link})
        except: pass
        return sources
