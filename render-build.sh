#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Sasabihin natin sa installer na dito ilagay ang browser files
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/src/.cache/ms-playwright
python -m playwright install --with-deps chromium
