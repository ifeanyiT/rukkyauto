# Rukky's UGC Content Strategy Automation Architecture

## 🎯 Project Goal
To build an autonomous, zero-touch content pipeline that scrapes trending User-Generated Content (UGC) hooks, competitor ad campaigns, and industry insights, enriches them using AI, and delivers actionable content strategies directly to a structured database (Notion/Google Sheets). This workflow is designed as a birthday gift to empower Rukky, a content strategist, to focus entirely on high-value creation and execution rather than manual research.

## 🛠 Tech Stack
- **Orchestration:** n8n 
- **Scraping Engine:** Python, Selenium WebDriver (Windows environment)
- **AI Processing:** LLM integration (OpenAI / Anthropic nodes)
- **Destination Database:** Notion API or Google Sheets

## 🏗 Pipeline Architecture Breakdown

### 1. The Trigger (Time-Based Graph Entry)
- **Node:** n8n Schedule Trigger.
- **Config:** Runs weekly (e.g., Mondays at 8:00 AM) to ensure a fresh batch of trends is waiting for her at the start of the week.

### 2. The Scraping Engine (Data Extraction)
- **Node:** n8n Execute Command Node.
- **Action:** Executes a local Python/Selenium script.
- **Target:** Navigates marketing blogs, TikTok Creative Center, or ad libraries to extract top-performing video hooks, ad copy, and engagement metrics.
- **Output:** Outputs a structured JSON array back to the n8n graph.

### 3. AI Enrichment (Data Processing)
- **Node:** Advanced LLM Node / AI Agent.
- **Action:** Ingests the JSON payload and acts as an AI Content Strategist.
- **Prompt Directive:** "Analyze these trending topics. Generate three high-converting UGC video hooks and a brief campaign strategy for each."

### 4. Destination & Delivery (Storage)
- **Node:** Notion or Google Sheets Node.
- **Action:** Maps the processed AI outputs (Topic, Hooks, Strategy, Source Link) into a clean, readable dashboard for Rukky.

---

## 🤖 Instructions for Claude Code (Implementation Specs)

To successfully scaffold and build this pipeline, please adhere to the following looping architectures:

### 1. Graph Looping (n8n Node Iteration & Resilience)
When building the n8n JSON blueprint or the Python script, implement graph-level looping to handle pagination and retries:
- **Pagination Cycles:** If the target site has multiple pages of trends, the Python script must loop through the paginated DOM structure until a specific data threshold is reached (e.g., top 50 trends).
- **Error Handling (Retry Graph):** In n8n, implement an error-trigger node linked back to the `Execute Command` node. If the Selenium script times out, the graph should loop back for a maximum of 3 retries with exponential backoff before logging a failure.
- **Item Batching:** Use n8n's `Split in Batches` node before hitting the LLM API to prevent token overflow. Loop through batches of 5 trends per AI request.

### 2. Context Looping (State Management & Iterative Refinement)
Ensure the AI processing stage maintains contextual awareness:
- **Memory/State:** The LLM prompt should include context from previous iterations (e.g., "In the last batch, we focused on beauty UGC; this batch is tech UGC"). 
- **Feedback Loop Integration:** Add a specific column in the Notion database called `Performance Status` (e.g., "Tested", "Failed", "Viral"). In version 2.0 of this workflow, Claude should write a script to read this Notion context back into the LLM node, creating a continuous context loop where the AI learns which hooks Rukky actually uses and adjusts future hook generation accordingly.
