#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Ito ang importante: install chromium pati dependencies
python -m playwright install --with-deps chromium
