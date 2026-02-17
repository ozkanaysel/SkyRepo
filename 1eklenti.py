import os
import requests
import cloudscraper
import json
import re
import base64
from bs4 import BeautifulSoup

# --- AYARLAR VE DESENLER ---
RESOLVER_PATTERNS = {
    "Mixdrop": r"mixdrop\.co/e/([a-z0-9]+)",
    "Streamtape": r"streamtape\.com/e/([a-z0-9]+)",
    "Fembed": r"fembed\.com/v/([a-z0-9]+)",
    "M3U8-Direct": r"https?://[^\s/$.?#].[^\s]*\.m3u8"
}

def final_plugin_creator():
    print("\n🚀 --- SKYSTREAM ULTIMATE DEVELOPER KIT (Full Version) ---")
    
    github_user = "ozkanaysel"
    repo_name = "SkyRepo"
    
    # 1. BİLGİ ALMA
    target_url = input("\n[1] Hedef Site URL (Örn: https://siteadi.com): ").strip("/")
    plugin_display_name = input("[2] Eklenti İsmi: ")
    plugin_version = input("[3] Sürüm (Örn: 1.0.0): ")
    github_token = input("[4] GitHub Token (ghp_...): ")

    folder_name = plugin_display_name.replace(" ", "")
    scraper = cloudscraper.create_scraper()

    # 2. DOSYA HAZIRLIĞI
    print(f"\n📂 '{folder_name}' klasörü oluşturuluyor...")
    os.makedirs(folder_name, exist_ok=True)
    
    # provider.py oluşturma
    provider_code = f"""
import re
import base64
import cloudscraper
from bs4 import BeautifulSoup

class {folder_name}:
    def __init__(self):
        self.base_url = "{target_url}"
        self.scraper = cloudscraper.create_scraper()
        self.resolver_patterns = {json.dumps(RESOLVER_PATTERNS)}

    def search(self, query):
        results = []
        try:
            url = f"{{self.base_url}}/?s={{query.replace(' ', '+')}}"
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
                    results.append({{"title": title, "url": link, "poster": poster}})
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
                    if "http" in decoded: sources.append({{"name": "Decoded", "url": decoded}})
                except: pass
            for name, pattern in self.resolver_patterns.items():
                matches = re.findall(pattern, content)
                for m in matches:
                    l = m if m.startswith('http') else f"https://{{name.lower()}}.com/e/{{m}}"
                    sources.append({{"name": name, "url": l}})
        except: pass
        return sources
"""
    with open(f"{folder_name}/provider.py", "w", encoding="utf-8") as f:
        f.write(provider_code)

    # manifest.json
    manifest_data = {
        "id": f"com.{github_user}.{folder_name.lower()}",
        "name": plugin_display_name,
        "version": plugin_version,
        "main": "provider.py",
        "author": github_user,
        "type": "TV_SHOWS_AND_MOVIES"
    }
    with open(f"{folder_name}/manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=4)

    # repository.json (Mağaza dizini) güncelleme
    repo_file = "repository.json"
    p_list = []
    if os.path.exists(repo_file):
        try:
            with open(repo_file, "r") as f: p_list = json.load(f)
        except: p_list = []
    
    entry = {"id": manifest_data["id"], "name": plugin_display_name, "version": plugin_version, 
             "url": f"https://raw.githubusercontent.com/{github_user}/{repo_name}/main/{folder_name}/manifest.json"}
    
    p_list = [p for p in p_list if p.get("id") != entry["id"]]
    p_list.append(entry)
    with open(repo_file, "w") as f: json.dump(p_list, f, indent=4)

    # 3. GITHUB GÜNCELLEME SÜRECİ
    print(f"\n📤 GitHub: {repo_name} güncelleniyor...")
    
    # Komut listesi
    git_commands = [
        "git config --global init.defaultBranch main",
        "git init",
        f"git config user.email '{github_user}@example.com'",
        f"git config user.name '{github_user}'",
        "git remote remove origin",
        f"git remote add origin https://{github_token}@github.com/{github_user}/{repo_name}.git",
        "git add .",
        f'git commit -m "Deployment of {plugin_display_name} v{plugin_version}"',
        "git branch -M main",
        "git push -u origin main -f"
    ]

    for cmd in git_commands:
        print(f"DEBUG: {cmd}") # Hangi adımda olduğumuzu görmek için
        os.system(cmd + " 2>&1") # Hataları da ekrana basar

    print(f"\n✨ İŞLEM TAMAMLANDI!")
    print(f"🔗 Repo: https://github.com/{github_user}/{repo_name}")
    print(f"📜 Uygulamaya eklenecek Raw linki için repository.json dosyasını kullanın.")

if __name__ == "__main__":
    final_plugin_creator()

