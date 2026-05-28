import time
import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright

app = Flask(__name__)
CORS(app)

def super_scraper(target_url):
    results = {}
    try:
        with sync_playwright() as pw:
            # Simple launch, Docker na ang bahala sa path
            browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
            page = context.new_page()

            def handle_response(res):
                if ".m3u8" in res.url.lower():
                    if "stream" not in results:
                        results["stream"] = res.url

            page.on("response", handle_response)
            
            # Buksan ang site
            page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
            
            # Auto-click para sa mga players
            try:
                page.mouse.click(500, 300)
            except:
                pass

            time.sleep(12) 
            browser.close()
    except Exception as e:
        results["error"] = str(e)
    
    return results

@app.route('/')
def home():
    return "Movie Scraper is LIVE (Docker Mode)", 200

@app.route('/scrape')
def api_scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"success": False, "error": "No URL"}), 400
    
    data = super_scraper(url)
    return jsonify({"success": True, "data": data})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
