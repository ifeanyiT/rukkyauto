"""Scraper source registry. Add new sources by dropping a module with a
`scrape(limit) -> list[dict]` function and registering it here."""
from . import demo, tiktok_creative_center

SOURCES = {
    "demo": demo.scrape,
    "tiktok": tiktok_creative_center.scrape,
}
