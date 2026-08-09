# Rukky UGC Automation

Autonomous weekly pipeline: scrape trending UGC hooks → AI enrichment → Notion dashboard.
Built on **n8n Cloud** (orchestration) + a **self-hosted Selenium scraper** (on Render) + **OpenAI** + **Notion**.

See `Rukky_UGC_Automation_Architecture.md` for the original design.

```
scraper/   FastAPI + Selenium service n8n calls over HTTP  (deploy to Render)
n8n/       Importable workflow JSON + Notion setup guide
```

## Why the scraper is separate
n8n Cloud is sandboxed — it can't run local Python/Selenium (no Execute Command node).
So the scraper is a tiny web service; n8n Cloud calls its `/scrape` endpoint over HTTP.

## Build order
1. **Deploy the scraper** (`scraper/`) to Render — see below. Verify `/health` responds.
2. **Import the workflow** — n8n Cloud → Workflows → Import from File → `n8n/rukky-ugc-workflow.json`.
3. **Set up Notion** — follow `n8n/NOTION_SETUP.md`, attach the credential.
4. **Add credentials in n8n** — OpenAI API key, Notion secret.
5. **Point the HTTP node** at your Render URL, keep `source=demo` for the first test.
6. **Run once manually** in n8n → confirm rows land in Notion.
7. **Switch `source` to `tiktok`** and harden the live selectors together.

## Deploy the scraper to Render
1. Push this repo to GitHub.
2. Render → **New +** → **Blueprint** → select the repo (reads `scraper/render.yaml`).
3. Set `SCRAPER_API_KEY` to a long random string in the Render dashboard.
4. After deploy, test: `GET https://<your-app>.onrender.com/health`.

## Local run (optional)
```bash
cd scraper
cp .env.example .env          # set SCRAPER_API_KEY
pip install -r requirements.txt
uvicorn app:app --reload
# http://127.0.0.1:8000/scrape?source=demo  (header x-api-key: <your key>)
```

## Roadmap
- v1: demo source → live TikTok Creative Center scraper.
- v2: read `Performance Status` from Notion back into the LLM (context feedback loop).
