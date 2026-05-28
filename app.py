import time
import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright

app = Flask(__name__)
CORS(app)

# Dito hahanapin ng Playwright ang browser
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "pw-browsers"

def super_scraper(target_url):
    results = {}
    # Ginamit ang 'with' para automatic mag-close ang Playwright
    try:
        with sync_playwright() as pw:
            # Hahayaan natin si Playwright na humanap ng executable kusa
            browser = pw.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu"]
            )
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )

            # Listener para sa m3u8
            def handle_response(res):
                if ".m3u8" in res.url:
                    if "stream" not in results:
                        results["stream"] = res.url
                        print(f"FOUND: {res.url}")

            page.on("response", handle_response)
            
            # Buksan ang site
            page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(12) # Antay ng traffic
            
            browser.close()
    except Exception as e:
        results["error"] = str(e)
        results["debug"] = traceback.format_exc()
    
    return results

@app.route('/')
def home():
    return "API is Online and Browser path is set!", 200

@app.route('/scrape')
def api_scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"success": False, "error": "Missing URL"}), 400
    
    data = super_scraper(url)
    return jsonify({"success": True, "data": data})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
