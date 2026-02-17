import os
import json
import zipfile

def final_fixer():
    print("\n🛠️ --- SKYSTREAM YÜKLEME HATASI GİDERİCİ --- 🛠️")
    
    github_user = "ozkanaysel"
    repo_name = "SkyRepo"
    
    plugin_name = "slc"
    version = 3
    github_token = input("[!] GitHub Token: ")

    # JS içeriği (Önceki altyazı destekli kodun aynısı)
    # Değişkeni burada tanımladığınızdan emin olun
    js_content = """... (Paylaştığın plugin.js kodu buraya gelecek) ..."""

    # 1. PAKETLEME (Klasörsüz Saf Yapı)
    sky_file = "slc.sky"
    with zipfile.ZipFile(sky_file, 'w', zipfile.ZIP_DEFLATED) as sky_zip:
        # arcname="plugin.js" diyerek dosyanın klasörsüz en üstte olmasını sağlıyoruz
        sky_zip.writestr("plugin.js", js_content)
    
    # 2. JSON YAPILANDIRMASI (RAW Link Zorlaması)
    raw_url = f"https://raw.githubusercontent.com/{github_user}/{repo_name}/main"
    
    plugins_data = [{
        "name": "slc",
        "internalName": "slc",
        "url": f"{raw_url}/slc.sky", # Doğrudan RAW indirme linki
        "version": version,
        "authors": [github_user],
        "language": "tr",
        "types": ["Movies", "TV"]
    }]
    
    repo_json = {
        "name": "SkyStream Universe",
        "id": f"com.{github_user}.repo",
        "manifestVersion": 1,
        "pluginLists": [f"{raw_url}/plugins.json"]
    }

    with open("plugins.json", "w") as f: json.dump(plugins_data, f, indent=2)
    with open("repo.json", "w") as f: json.dump(repo_json, f, indent=2)

    # 3. GITHUB PUSH
    os.system("git init")
    os.system(f"git remote add origin https://{github_token}@github.com/{github_user}/{repo_name}.git > /dev/null 2>&1")
    os.system("git add .")
    os.system('git commit -m "Fix: Package structure and raw links"')
    os.system("git branch -M main")
    os.system("git push -u origin main -f")

    print(f"\n✅ İşlem Tamam! Uygulamayı kapatıp açın ve tekrar yüklemeyi deneyin.")

if __name__ == "__main__":
    final_fixer()

