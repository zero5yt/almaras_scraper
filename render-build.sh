#!/usr/bin/env bash
set -o errexit

# 1. Install python packages
pip install -r requirements.txt

# 2. Ituro ang folder (Persistent Cache)
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/src/.cache/ms-playwright

# 3. I-install ang Chromium binary LANG (Wag na yung dependencies)
python -m playwright install chromium
