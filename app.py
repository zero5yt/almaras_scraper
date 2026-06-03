import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright

app = Flask(__name__)
CORS(app)


def super_scraper(target_url):
    results = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=True, 
                args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--single-process"]
            )
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

            def handle_response(res):
                print(f"DEBUG: Catching -> {res.url}")
                if ".m3u8" in res.url.lower() or ".mpd" in res.url.lower():
                    if "stream" not in results:
                        results["stream"] = res.url
                        print(f"FOUND STREAM: {res.url}")

            page.on("response", handle_response)
            
            # DITO DAPAT ANG PAG-GOTO AT WAIT
            page.goto(target_url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(5000) 

            # Subukang mag-click
            try:
                page.mouse.click(500, 300)
            except:
                pass
                
            time.sleep(10) # Bawasan natin para hindi mag-timeout
            browser.close()
            
    except Exception as e:
        results["error"] = str(e)
        
    return results

@app.route('/scrape')
def api_scrape():
    url = request.args.get('url')
    if not url: return jsonify({"error": "No URL"}), 400
    data = super_scraper(url)
    return jsonify({"success": True, "data": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
