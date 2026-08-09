"""Shared Selenium plumbing for all scrapers."""
from __future__ import annotations

import os
from contextlib import contextmanager


@contextmanager
def headless_driver():
    """Yield a headless Chrome driver, always cleaned up.

    Uses Selenium Manager (Selenium 4.6+) to resolve the driver, so no
    chromedriver path juggling is needed inside the Docker image.

    Selenium is imported lazily so demo mode runs without it installed.
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    # Light stealth so JS-heavy sites don't immediately flag the session.
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    )
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])

    binary = os.getenv("CHROME_BINARY")
    if binary:
        opts.binary_location = binary

    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(60)
    try:
        yield driver
    finally:
        driver.quit()


def trend_threshold() -> int:
    return int(os.getenv("TREND_THRESHOLD", "50"))
