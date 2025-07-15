# HealthChainSys Agent 🚑🤖

**HealthChainSys Agent** is an AI-powered healthcare data pipeline designed to extract, validate, and push insights from EHR systems (like Cerner CommunityWorks) to real-time execution dashboards and analytics tools like Tableau and Notion.

---

### 🔧 Core Features

- 🧠 **IRIS Agent** — Autonomous desktop assistant that navigates Cerner Discern Analytics and retrieves clinical + financial reports
- 📤 **Ingestors** — Structured parsing of exports (claims, implants, OR logs, etc.)
- ✅ **Validation Engine** — Rule-based system to flag data integrity or reimbursement risks
- 📊 **Execution Pushers** — Automatically push insights into Notion Execution Planner and Tableau
- 🧬 Modular AI agents for business strategy, growth, R&D, market intel, and automation

---

### 🗂️ Repo Structure

```bash
📁 core/
  ├── agents/
  │   └── discern/
  │        ├── iris_autonomous.py  # Main IRIS desktop automation
  │        ├── discern_ingestor.py
  │        └── ...
  ├── validator/
  ├── utils/
  └── ...
📁 data/
📁 logs/
📁 assets/
main.py
