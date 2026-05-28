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
            browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
            page = context.new_page()

            def handle_response(res):
                # Mas malawak na paghahanap sa m3u8
                if ".m3u8" in res.url.lower():
                    if "stream" not in results:
                        results["stream"] = res.url
                        print(f"CAPTURED: {res.url}")

            page.on("response", handle_response)
            
            # Buksan ang site
            page.goto(target_url, wait_until="load", timeout=60000)
            time.sleep(5) # Antay mag-load ang player

            # --- ITO ANG DAGDAG: AUTO-CLICK PARA SA VIDSRC ---
            try:
                # Susubukan nating hanapin at i-click ang play button kung meron
                # Kadalasan ang vidsrc ay may overlay na play icon
                page.mouse.click(500, 300) # Click sa gitna ng screen (default player size)
                print("[*] Clicked center of the screen to trigger video...")
            except:
                pass

            time.sleep(10) # Antay lumabas ang m3u8 pagkatapos i-click
            
            browser.close()
    except Exception as e:
        results["error"] = str(e)
        results["debug"] = traceback.format_exc()
    
    return results

@app.route('/')
def home():
    return "Vidsrc Scraper is Active!", 200

@app.route('/scrape')
def api_scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL"}), 400
    data = super_scraper(url)
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
