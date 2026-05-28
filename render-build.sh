#!/usr/bin/env bash
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Ituro ang folder kung saan dapat i-save ang browser
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/src/.cache/ms-playwright

# 3. Install Chromium (Pati dependencies para sigurado)
python -m playwright install --with-deps chromium
