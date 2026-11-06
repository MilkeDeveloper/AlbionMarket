# AlbionMarket — Albion Online Market API

A Python backend built with **FastAPI** to search for Albion Online items and retrieve market prices by city, item tier, and quality. This personal project provides data for a separate frontend application: [AlbionMKTfront](https://github.com/MilkeDeveloper/AlbionMKTfront).

## Features

- Search items by partial name using local item metadata (Portuguese/Brazilian names).
- Query market prices from the [Albion Online Data Project](https://www.albion-online-data.com/).
- Filter prices by item tier, quality, or city.
- Organize prices by city and include item names, tiers, quality, prices, and item-image URLs where available.
- Allow local frontend requests via configured CORS origins.

## Tech stack

- Python
- FastAPI
- httpx (asynchronous HTTP requests)
- Uvicorn
- JSON item metadata

## API endpoints

### Search items

```http
GET /search?q=espada
```

Searches item names in `metadata/items.json` and returns matching item names and IDs. The search defaults to the `PT-BR` locale.

### Get market prices

```http
GET /market/price/{item_id}
```

Optional query parameters:

| Parameter | Type | Purpose |
| --- | --- | --- |
| `tier` | integer | Filter by tier |
| `quality` | integer | Filter by item quality |
| `city` | string | Filter by market city |

Example:

```http
GET /market/price/T4_MAIN_SWORD?tier=4&city=Martlock
```

The price route uses the local item catalog to match the supplied item ID/name and then requests external market data. Empty or unmatched searches may return an error or an empty-price response.

## Getting started

Requirements: Python 3.10+ recommended and pip.

```bash
git clone --branch master https://github.com/MilkeDeveloper/AlbionMarket.git
cd AlbionMarket
python -m venv .venv
# On Linux/macOS:
source .venv/bin/activate
# On Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:server --reload --host 127.0.0.1 --port 8000
```

Open the API documentation at http://127.0.0.1:8000/docs.

> Start the server from the repository root. The application reads `metadata/items.json` using a relative path.

## Data sources and integration

- Item metadata: `metadata/items.json`
- External prices: Albion Online Data Project, using the West region endpoint in the current code.
- Item images: Albion Online rendering service.
- Companion frontend: [AlbionMKTfront](https://github.com/MilkeDeveloper/AlbionMKTfront)

Market data comes from a community-powered service, so availability, freshness, and accuracy depend on that upstream source.

## Repository layout

```text
main.py                 # FastAPI routes and CORS configuration
metadata/items.json     # Local item catalog
services/
  search_service.py     # Item name search
  api_service.py        # Price lookup/filter orchestration
  general_search.py     # Multi-tier/multi-city prices
  search_by_city.py
  search_by_filter.py
  search_by_quality.py
requirements.txt
```

## Status and limitations

Personal project / prototype. The current implementation includes some hardcoded settings, simplified error handling, and separate filtering paths that could be consolidated. It has not been verified here as a production deployment.

## Author

[MilkeDeveloper](https://github.com/MilkeDeveloper)
