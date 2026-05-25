# ArXiv AI Digest

Daily curated ArXiv paper digests for data professionals, delivered via Telegram.

Each bot targets a specific role in the data field, with tailored topic filters and role-aware summarization powered by Claude Haiku.

## How it works

```
GitHub Actions (cron, Mon-Fri 8am BRT)
  → ArXiv API (fetch recent papers by category + keyword filtering)
    → Claude Haiku (summarize, score relevance 1-5, classify paper type)
      → Telegram Bot API (deliver formatted digest per role)
```

Papers are scored for relevance (1-5) and only those scoring 3+ are delivered. The highest-scored paper is featured as the **Highlight of the Day**. Each paper is tagged by type (`New Method`, `Survey`, `Benchmark`, `Application`, `Framework`, `Analysis`, `Dataset`, `Theory`).

## Professional Profiles

| Bot | Focus |
|-----|-------|
| **ML Engineer** | MLOps, model serving, distributed training, monitoring, drift detection, AutoML |
| **Data Scientist** | Causal inference, experimental design, Bayesian methods, time series, uplift modeling |
| **AI/GenAI Engineer** | LLMs, RAG, AI agents, prompting, fine-tuning, guardrails, embeddings |
| **CV Engineer** | Object detection, segmentation, 3D vision, edge CV, diffusion models, OCR |
| **Data Engineer** | Data pipelines, streaming, lakehouse, data quality, orchestration, query optimization |

Each bot has its own YAML config (`bots/*.yaml`) defining ArXiv categories, keyword filters, and a role-specific summarization prompt.

## Digest Format

```
🤖 ArXiv Digest: AI/GenAI Engineer
📅 24/05/2026 | 8 papers

⭐ HIGHLIGHT
[New Method] Title of Top Paper
👥 Author1, Author2 et al.

• Bullet 1
• Bullet 2
• Bullet 3

🔗 Read paper

────────────────────

1. [Framework] Another Paper Title
👥 Author1, Author2 et al.

• Bullet 1
• Bullet 2
• Bullet 3

🔗 Read paper
```

## Architecture

```
arxiv-ai-digest/
├── bots/                        # Role configs (YAML)
│   ├── ml_engineer.yaml
│   ├── data_scientist.yaml
│   ├── genai_engineer.yaml
│   ├── cv_engineer.yaml
│   └── data_engineer.yaml
├── src/
│   ├── config.py                # Loads YAML config + env vars
│   ├── arxiv_client.py          # Fetches papers from ArXiv API
│   ├── summarizer.py            # Summarizes via Claude Haiku (score + tag + bullets)
│   ├── telegram_notifier.py     # Sends formatted digest via Telegram
│   └── main.py                  # Orchestrator (CLI: python -m src.main <bot_name>)
├── .github/workflows/
│   └── daily-digest.yml         # GitHub Actions cron with matrix strategy
├── pyproject.toml
└── .env.example
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11+ |
| LLM | Claude Haiku (Anthropic) |
| Paper Source | ArXiv API (Atom feed via feedparser) |
| Delivery | Telegram Bot API (urllib, no SDK dependency) |
| Scheduling | GitHub Actions (cron, matrix strategy) |
| Config | YAML per bot role |

## Setup

### 1. Create Telegram Bots

Create 5 bots via [@BotFather](https://t.me/BotFather) on Telegram. Save each token.

### 2. Get Chat IDs

For each bot:
1. Send `/start` to the bot
2. Visit `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Copy the `chat.id` from the response

### 3. Configure GitHub Secrets

Add these secrets to your GitHub repo (Settings > Secrets > Actions):

- `ANTHROPIC_API_KEY`
- `TELEGRAM_BOT_TOKEN_ML_ENGINEER` / `TELEGRAM_CHAT_ID_ML_ENGINEER`
- `TELEGRAM_BOT_TOKEN_DATA_SCIENTIST` / `TELEGRAM_CHAT_ID_DATA_SCIENTIST`
- `TELEGRAM_BOT_TOKEN_GENAI_ENGINEER` / `TELEGRAM_CHAT_ID_GENAI_ENGINEER`
- `TELEGRAM_BOT_TOKEN_CV_ENGINEER` / `TELEGRAM_CHAT_ID_CV_ENGINEER`
- `TELEGRAM_BOT_TOKEN_DATA_ENGINEER` / `TELEGRAM_CHAT_ID_DATA_ENGINEER`

### 4. Run

The workflow runs automatically Mon-Fri at 8am BRT. To trigger manually:
- Go to Actions > Daily ArXiv Digest > Run workflow

### Local Testing

```bash
cp .env.example .env
# Fill in your keys

pip install -e .
python -m src.main ml_engineer
```

## Cost

- **GitHub Actions**: ~55 min/month (free tier: 2000 min)
- **Anthropic Haiku**: ~$1.50/month
- **Telegram**: Free

## Adding a New Role

1. Create a new YAML in `bots/` (copy an existing one as template)
2. Define ArXiv categories, keywords, and a role-specific summarization prompt
3. Create a Telegram bot via @BotFather
4. Add the token and chat ID as GitHub Secrets
5. Add the bot name to the matrix in `.github/workflows/daily-digest.yml`
