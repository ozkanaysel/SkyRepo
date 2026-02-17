import os
import json
import zipfile

def sky_ultimate_maker():
    print("\n🚀 --- SKYSTREAM JS ULTIMATE: SERIES & MOVIE EDITION --- 🚀")
    
    github_user = "ozkanaysel"
    repo_name = "SkyRepo"
    
    # 1. GİRDİLER
    main_url = input("\n[1] Hedef Site URL: ").strip("/")
    plugin_name = input("[2] Eklenti İsmi: ")
    plugin_id = f"com.{github_user}.{plugin_name.lower().replace(' ', '')}"
    version = int(input("[3] Sürüm (Sayı): "))
    github_token = input("[4] GitHub Token: ")

    # 2. JS ENGINE İÇİN ŞABLON (Dizi ve Film Destekli)
    js_content = f"""
/**
 * SkyStream JS Provider: {plugin_name}
 * Features: Auto Season/Episode Detection & Recursive Iframe
 */

const mainUrl = "{main_url}";
const commonHeaders = {{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": mainUrl
}};

function getManifest() {{
    return {{ name: "{plugin_name}", id: "{plugin_id}", version: {version}, baseUrl: mainUrl }};
}}

function getHome(callback) {{
    http_get(mainUrl, commonHeaders, (status, html) => {{
        const regex = /<a href="([^"]+)"[^>]*title="([^"]+)"[^>]*>.*?<img[^>]*src="([^"]+)"/g;
        var movies = [];
        var matches;
        while ((matches = regex.exec(html)) !== null) {{
            movies.push({{
                title: matches[2],
                url: matches[1].startsWith('http') ? matches[1] : mainUrl + matches[1],
                posterUrl: matches[3].startsWith('http') ? matches[3] : mainUrl + matches[3]
            }});
        }}
        callback(JSON.stringify({{ "Trendler": movies.slice(0, 20) }}));
    }});
}}

function search(query, callback) {{
    const searchUrl = mainUrl + "/?s=" + encodeURIComponent(query);
    http_get(searchUrl, commonHeaders, (status, html) => {{
        const regex = /<a href="([^"]+)"[^>]*title="([^"]+)"[^>]*>.*?<img[^>]*src="([^"]+)"/g;
        var results = [];
        var matches;
        while ((matches = regex.exec(html)) !== null) {{
            results.push({{
                title: matches[2],
                url: matches[1].startsWith('http') ? matches[1] : mainUrl + matches[1],
                posterUrl: matches[3].startsWith('http') ? matches[3] : mainUrl + matches[3]
            }});
        }}
        callback(JSON.stringify(results));
    }});
}}

function load(url, callback) {{
    http_get(url, commonHeaders, (status, html) => {{
        const title = html.match(/<h1[^>]*>([^<]+)<\\/h1>/)?.[1] || "Bilinmiyor";
        
        // --- Dizi Bölümü Tarama Mantığı ---
        var episodes = [];
        const epRegex = /<a[^>]+href="([^"]+)"[^>]*>(?:Sezon\\s*(\\d+)\\s*)?Bölüm\\s*(\\d+)[^<]*<\\/a>/gi;
        var epMatch;
        while ((epMatch = epRegex.exec(html)) !== null) {{
            episodes.push({{
                name: "S" + (epMatch[2] || "1") + " E" + epMatch[3],
                url: epMatch[1].startsWith('http') ? epMatch[1] : mainUrl + epMatch[1],
                season: parseInt(epMatch[2] || "1"),
                episode: parseInt(epMatch[3])
            }});
        }}

        // Eğer bölüm bulunduysa dizi formatında, yoksa film formatında dön
        if (episodes.length > 0) {{
            callback(JSON.stringify({{
                url: url,
                title: title,
                episodes: episodes
            }}));
        }} else {{
            callback(JSON.stringify({{
                url: url,
                title: title,
                data: html // Film için HTML'i sakla
            }}));
        }}
    }});
}}

function loadStreams(url, callback) {{
    http_get(url, commonHeaders, (status, html) => {{
        const iframeRegex = /<iframe[^>]+src="([^"]+)"/;
        const match = html.match(iframeRegex);
        
        if (match) {{
            const iframeUrl = match[1].startsWith('//') ? "https:" + match[1] : match[1];
            http_get(iframeUrl, {{ ...commonHeaders, "Referer": url }}, (s, iframeHtml) => {{
                const videoRegex = /file:\\s*"([^"]+\\.(?:m3u8|mp4))"/i;
                const videoMatch = iframeHtml.match(videoRegex);
                
                if (videoMatch) {{
                    callback(JSON.stringify([{{
                        name: "SkyStream HD Server",
                        url: videoMatch[1],
                        headers: {{ ...commonHeaders, "Referer": iframeUrl }}
                    }}]));
                }} else {{ callback("[]"); }}
            }});
        }} else {{ callback("[]"); }}
    }});
}}
"""

    # 3. .SKY PAKETLEME
    sky_file = f"{plugin_name.replace(' ', '')}.sky"
    with zipfile.ZipFile(sky_file, 'w') as zip_f:
        zip_f.writestr("plugin.js", js_content)
    
    # 4. REPO VE PLUGINS JSON
    raw_url = f"https://raw.githubusercontent.com/{github_user}/{repo_name}/main"
    
    plugins_data = [{
        "name": plugin_name,
        "internalName": plugin_name.replace(" ", ""),
        "url": f"{raw_url}/{sky_file}",
        "version": version,
        "authors": [github_user],
        "language": "tr",
        "types": ["Movies", "TV"]
    }]
    
    repo_data = {
        "name": "SkyStream Universe Repo",
        "id": f"com.{github_user}.repo",
        "manifestVersion": 1,
        "pluginLists": [f"{raw_url}/plugins.json"]
    }

    with open("plugins.json", "w") as f: json.dump(plugins_data, f, indent=2)
    with open("repo.json", "w") as f: json.dump(repo_data, f, indent=2)

    # 5. GITHUB DEPLOY
    print("\n📤 GitHub Evrenine Aktarılıyor...")
    os.system("git init")
    os.system(f"git config user.email '{github_user}@example.com'")
    os.system(f"git config user.name '{github_user}'")
    os.system("git remote remove origin > /dev/null 2>&1")
    os.system(f"git remote add origin https://{github_token}@github.com/{github_user}/{repo_name}.git")
    os.system("git add .")
    os.system(f'git commit -m "Add Series & Movie Support to {plugin_name}"')
    os.system("git branch -M main")
    os.system("git push -u origin main -f")

    print(f"\n✨ BAŞARIYLA TAMAMLANDI!")
    print(f"📡 SkyStream Uygulama Linki: {raw_url}/repo.json")

if __name__ == "__main__":
    sky_ultimate_maker()

