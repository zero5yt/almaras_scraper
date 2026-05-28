import time
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright

app = Flask(__name__)
CORS(app)

def super_scraper(target_url):
    results = {}
    # Gagamit tayo ng 'with' para siguradong mag-cl-close ang browser
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        def handle_response(res):
            if ".m3u8" in res.url and ("playlist" in res.url or "master" in res.url or "index" in res.url):
                if "stream" not in results:
                    results["stream"] = res.url

        page.on("response", handle_response)

        try:
            page.goto(target_url, wait_until="networkidle", timeout=60000)
            time.sleep(10) # Bigyan ng oras ang player
        except Exception as e:
            results["error"] = str(e)
        
        browser.close()
    return results

@app.route('/')
def home():
    return "Playwright Scraper is LIVE on Render!", 200

@app.route('/scrape')
def api_scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing url"}), 400
    data = super_scraper(url)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))