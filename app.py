import time
import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright

app = Flask(__name__)
CORS(app)

# Siguraduhin na ang path ay tugma sa Environment Variable
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/opt/render/project/src/.cache/ms-playwright"

def super_scraper(target_url):
    results = {}
    try:
        with sync_playwright() as pw:
            # Gagamit tayo ng simpleng launch dahil naka-set na ang PATH
            browser = pw.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
            )
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
            page = context.new_page()

            def handle_response(res):
                if ".m3u8" in res.url:
                    if "stream" not in results:
                        results["stream"] = res.url

            page.on("response", handle_response)
            
            page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(12) # Antay ng traffic
            
            browser.close()
    except Exception as e:
        results["error"] = str(e)
        results["traceback"] = traceback.format_exc()
    
    return results

@app.route('/')
def home():
    return "API is Online! Browsers are persistent.", 200

@app.route('/scrape')
def api_scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    
    data = super_scraper(url)
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
