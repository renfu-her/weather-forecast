# Weather Forecast Flask App

A simple Flask application that displays Taiwan's 36-hour weather forecast using the Central Weather Administration (CWA) Open Data API.

## Features

- Responsive UI (Bootstrap 5) for mobile, tablet, and desktop
- Select from 22 Taiwan counties/cities
- In-memory cache (5-minute TTL) to reduce API calls
- Clean forecast cards with icons for quick scanning

## Setup

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Configure API key

Copy `.env.example` to `.env` and provide your CWA API key:

```bash
cp .env.example .env
```

Edit `.env`:
```
CWA_API_KEY=your_api_key_here
```

### 3) Get a CWA API key

1. Visit the CWA Open Data Portal: https://opendata.cwa.gov.tw/
2. Sign up and request an API key
3. Put the key into your `.env`

### 4) Run the app

Using Flask CLI:

```bash
flask --app app run -h 0.0.0.0 -p 5000 --debug
```

Or run directly:

```bash
python app.py
```

### 5) Open in browser

Navigate to `http://localhost:5000`.

## How to use

1. Select a county/city on the homepage
2. Click "Search Weather"
3. View 36-hour forecasts including:
   - Weather condition and icon
   - Probability of precipitation (PoP)
   - Temperature range (Min–Max)
   - Comfort index (CI)

## Tech stack

- Backend: Flask 2.3.3
- Frontend: Bootstrap 5.3.0 + Font Awesome 6
- API: CWA dataset `F-C0032-001`
- Cache: In-memory with 5-minute TTL

## Data source

This app uses the Central Weather Administration Open Data 36-hour forecast dataset (F-C0032-001).

## License

For learning and personal use. Please follow the CWA Open Data usage terms.
