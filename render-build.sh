#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. I-install ang Python packages
pip install -r requirements.txt

# 2. I-install ang Chromium Browser specifically sa folder na 'pw-browsers'
# Hindi na natin kailangan ang --with-deps dahil pre-installed na ang basic libs sa Render
python -m playwright install chromium
