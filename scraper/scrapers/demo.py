"""Demo source: realistic sample trends so the whole n8n -> OpenAI -> Notion
pipeline can be built and tested before live scraping is dialled in."""
from __future__ import annotations


def scrape(limit: int) -> list[dict]:
    samples = [
        {
            "topic": "Get Ready With Me — but it's my 5am founder routine",
            "hook": "POV: you wanted a soft life so you started a business at 5am",
            "engagement": "1.2M likes",
            "source": "TikTok Creative Center",
            "source_link": "https://ads.tiktok.com/business/creativecenter",
        },
        {
            "topic": "Unboxing skincare that actually cleared my skin",
            "hook": "3 products, 30 days, zero filter — here's the receipts",
            "engagement": "890K likes",
            "source": "TikTok Creative Center",
            "source_link": "https://ads.tiktok.com/business/creativecenter",
        },
        {
            "topic": "Tech gadgets under $50 you didn't know you needed",
            "hook": "Amazon finds that feel illegal to know for this cheap",
            "engagement": "2.1M likes",
            "source": "TikTok Creative Center",
            "source_link": "https://ads.tiktok.com/business/creativecenter",
        },
        {
            "topic": "Day in the life of a content strategist",
            "hook": "I get paid to scroll TikTok — here's what that actually looks like",
            "engagement": "640K likes",
            "source": "Marketing blog roundup",
            "source_link": "https://example.com/ugc-trends",
        },
        {
            "topic": "Small business restock ASMR",
            "hook": "Restocking my shop at 2am because sleep is for the funded",
            "engagement": "1.5M likes",
            "source": "TikTok Creative Center",
            "source_link": "https://ads.tiktok.com/business/creativecenter",
        },
    ]
    # Repeat/truncate to honour the requested limit so batching logic is testable.
    out: list[dict] = []
    while len(out) < limit:
        out.extend(samples)
    return out[:limit]
