"""Live scraper for TikTok Creative Center trending hashtags.

NOTE: TikTok's Creative Center is a JS-heavy SPA with anti-bot measures and a
layout that changes often. Treat the selectors below as a STARTING POINT — we
will verify and adjust them against the live DOM together. The pagination loop
(spec: keep loading until TREND_THRESHOLD trends are collected) is the durable
part; the selectors are the fragile part.
"""
from __future__ import annotations

import time

from .base import headless_driver

TRENDS_URL = (
    "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en"
)


def scrape(limit: int) -> list[dict]:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    results: list[dict] = []
    with headless_driver() as driver:
        driver.get(TRENDS_URL)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(5)  # let the SPA hydrate

        max_clicks = 20  # safety cap on the pagination loop
        clicks = 0
        while len(_extract_cards(driver)) < limit and clicks < max_clicks:
            if not _click_view_more(driver):
                break
            clicks += 1
            time.sleep(3)

        for card in _extract_cards(driver)[:limit]:
            results.append(card)

    return results


def _extract_cards(driver) -> list[dict]:
    """Pull hashtag cards from the current DOM. Selectors are best-effort."""
    from selenium.webdriver.common.by import By

    cards = driver.find_elements(By.CSS_SELECTOR, "[class*='CardPc_container']")
    out: list[dict] = []
    for c in cards:
        try:
            name = c.find_element(
                By.CSS_SELECTOR, "[class*='titleText'], span, h3"
            ).text.strip()
        except Exception:
            name = c.text.strip().split("\n")[0] if c.text else ""
        if not name:
            continue
        out.append(
            {
                "topic": name,
                "hook": "",  # filled by the LLM stage
                "engagement": _safe_text(c, "[class*='number'], [class*='posts']"),
                "source": "TikTok Creative Center",
                "source_link": TRENDS_URL,
            }
        )
    return out


def _click_view_more(driver) -> bool:
    from selenium.webdriver.common.by import By

    for text in ("View More", "Load More", "See more"):
        try:
            btn = driver.find_element(
                By.XPATH, f"//*[contains(text(), '{text}')]"
            )
            driver.execute_script("arguments[0].click();", btn)
            return True
        except Exception:
            continue
    return False


def _safe_text(el, css: str) -> str:
    from selenium.webdriver.common.by import By

    try:
        return el.find_element(By.CSS_SELECTOR, css).text.strip()
    except Exception:
        return ""
