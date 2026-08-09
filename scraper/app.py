"""FastAPI wrapper that n8n Cloud calls over HTTP to run the Selenium scraper.

Endpoints:
  GET  /health           -> liveness check (also used to warm Render cold starts)
  GET  /scrape           -> run a source, return JSON array of trends

Auth: every /scrape call must send  x-api-key: <SCRAPER_API_KEY>.
"""
from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Query

from scrapers import SOURCES
from scrapers.base import trend_threshold

load_dotenv()

app = FastAPI(title="Rukky UGC Scraper", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok", "sources": list(SOURCES.keys())}


@app.get("/scrape")
def scrape(
    source: str = Query("demo", description="Which source to scrape"),
    limit: int | None = Query(None, description="Max trends (defaults to TREND_THRESHOLD)"),
    x_api_key: str | None = Header(None),
):
    expected = os.getenv("SCRAPER_API_KEY")
    if not expected or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing x-api-key")

    if source not in SOURCES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown source '{source}'. Options: {list(SOURCES.keys())}",
        )

    cap = limit or trend_threshold()
    try:
        trends = SOURCES[source](cap)
    except Exception as e:  # surface scraper failures to n8n's error branch
        raise HTTPException(status_code=502, detail=f"Scrape failed: {e}")

    return {"source": source, "count": len(trends), "trends": trends}
