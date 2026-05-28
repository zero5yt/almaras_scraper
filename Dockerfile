# Gamit ang official Playwright image (Kasama na lahat ng browsers at libs)
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# I-setup ang folder
WORKDIR /app

# I-copy ang requirements at i-install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# I-copy lahat ng files (app.py)
COPY . .

# Port para sa Render
EXPOSE 10000

# Command para patakbuhin ang Flask gamit ang Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
