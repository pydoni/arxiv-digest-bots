# ArXiv AI Digest

Daily curated ArXiv paper digests for data professionals, delivered via Telegram.

Each bot targets a specific role in the data field, with tailored topic filters and role-aware summarization powered by an LLM.

## How it works

```
GitHub Actions (cron, Mon-Fri 8am BRT)
  -> ArXiv API (fetch recent papers by category + keyword filtering)
    -> Anthropic Haiku (summarize, score relevance 1-5, classify paper type)
      -> Telegram Bot API (deliver formatted digest per role)
```

Papers are scored for relevance (1-5) and only those scoring 3+ are delivered. The highest-scored paper is featured as the **Highlight of the Day**. Each paper is tagged by type (`New Method`, `Survey`, `Benchmark`, `Application`, `Framework`, `Analysis`, `Dataset`, `Theory`).

## Professional Profiles

| Bot | Focus |
|-----|-------|
| **ML Engineer** | MLOps, model serving, distributed training, monitoring, drift detection, AutoML |
| **Data Scientist** | Causal inference, deep learning, experimental design, Bayesian methods, time series |
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
│   ├── summarizer.py            # Summarizes with LLM (score + tag + bullets)
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
| Language | Python 3.12 |
| LLM | Anthropic Haiku |
| Paper Source | ArXiv API (Atom feed via feedparser) |
| Delivery | Telegram Bot API (urllib, no SDK dependency) |
| Scheduling | GitHub Actions (cron, matrix strategy) |
| Config | YAML per bot role |

## Setup

### 1. Fork and clone

```bash
git clone https://github.com/<your-username>/arxiv-ai-digest.git
cd arxiv-ai-digest
```

### 2. Create Telegram Bots

Create a bot via [@BotFather](https://t.me/BotFather) on Telegram for each role you want. Save each token.

### 3. Create Telegram Channels

For each bot:
1. Create a public channel on Telegram (e.g. `@arxiv_ml_engineer_digest`)
2. Add the bot as an **administrator** with permission to **Post Messages**
3. Post any message in the channel
4. Visit `https://api.telegram.org/bot<TOKEN>/getUpdates` and copy the `chat.id` (negative number)

### 4. Configure GitHub Secrets

Go to your repo Settings > Secrets and variables > Actions, and add:

- `ANTHROPIC_API_KEY` - your Anthropic API key
- For each bot: `TELEGRAM_BOT_TOKEN_<NAME>` and `TELEGRAM_CHAT_ID_<NAME>`

Example for the ML Engineer bot:
- `TELEGRAM_BOT_TOKEN_ML_ENGINEER` = `123456:ABC...`
- `TELEGRAM_CHAT_ID_ML_ENGINEER` = `-100123456789`

### 5. Run

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

## Create Your Own Bot

You can easily create a custom bot for any field or role. Here's a step-by-step guide:

### Step 1: Create the YAML config

Create a new file in `bots/`, for example `bots/nlp_researcher.yaml`:

```yaml
name: "NLP Researcher"
emoji: "📝"
description: "Papers relevant to NLP researchers"
arxiv_categories:
  - cs.CL
  - cs.AI
keywords:
  - natural language processing
  - sentiment analysis
  - named entity recognition
  - machine translation
  - text classification
  - question answering
  - dialogue systems
  - parsing
  - morphology
  - syntax
summary_prompt: >
  Summarize this paper in 3 concise bullet points.
  Focus on the contribution to NLP research.
  Highlight: problem addressed, proposed method, and key results.
max_papers: 15
telegram_token_env: "TELEGRAM_BOT_TOKEN_NLP_RESEARCHER"
telegram_chat_id_env: "TELEGRAM_CHAT_ID_NLP_RESEARCHER"
```

**How to choose `arxiv_categories`:**

Browse the full list at [arxiv.org/category_taxonomy](https://arxiv.org/category_taxonomy). Common ones:

| Category | Field |
|----------|-------|
| `cs.LG` | Machine Learning |
| `cs.AI` | Artificial Intelligence |
| `cs.CL` | Computation and Language (NLP) |
| `cs.CV` | Computer Vision |
| `cs.DB` | Databases |
| `cs.DC` | Distributed Computing |
| `cs.IR` | Information Retrieval |
| `cs.SE` | Software Engineering |
| `stat.ML` | Machine Learning (Statistics) |
| `stat.AP` | Applications (Statistics) |
| `cs.RO` | Robotics |
| `cs.CR` | Cryptography and Security |
| `cs.NE` | Neural and Evolutionary Computing |
| `eess.SP` | Signal Processing |
| `q-bio.QM` | Quantitative Methods (Biology) |
| `q-fin.ST` | Statistical Finance |

**How to choose `keywords`:**

Keywords are matched against the paper title and abstract (case-insensitive). Tips:
- Use specific terms (e.g. `named entity recognition` instead of just `NLP`)
- Include abbreviations and full forms (e.g. both `rag` and `retrieval augmented generation`)
- Add method names (e.g. `transformer`, `attention`, `bert`)
- Start broad and narrow down based on the papers you receive

### Step 2: Create a Telegram bot and channel

1. Message [@BotFather](https://t.me/BotFather) on Telegram and send `/newbot`
2. Choose a name (e.g. `ArXiv NLP Researcher`) and username (e.g. `arxiv_nlp_researcher_bot`)
3. Save the bot token
4. Create a Telegram channel and add the bot as admin (Post Messages permission)
5. Post a message in the channel, then get the chat ID:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
   Look for `"chat": {"id": -100...}` in the response

### Step 3: Add to GitHub

1. Add two secrets to your repo (Settings > Secrets > Actions):
   - `TELEGRAM_BOT_TOKEN_NLP_RESEARCHER` = your bot token
   - `TELEGRAM_CHAT_ID_NLP_RESEARCHER` = the channel chat ID

2. Add your bot to the workflow matrix in `.github/workflows/daily-digest.yml`:

   ```yaml
   matrix:
     bot:
       - ml_engineer
       - data_scientist
       - genai_engineer
       - cv_engineer
       - data_engineer
       - nlp_researcher    # <-- add here
   ```

3. Add the env vars to the workflow's `env` section:

   ```yaml
   env:
     # ... existing vars ...
     TELEGRAM_BOT_TOKEN_NLP_RESEARCHER: ${{ secrets.TELEGRAM_BOT_TOKEN_NLP_RESEARCHER }}
     TELEGRAM_CHAT_ID_NLP_RESEARCHER: ${{ secrets.TELEGRAM_CHAT_ID_NLP_RESEARCHER }}
   ```

4. Push and your new bot will run with the next scheduled digest.

### Step 4: Test locally

```bash
# Add to your .env
TELEGRAM_BOT_TOKEN_NLP_RESEARCHER=your_token
TELEGRAM_CHAT_ID_NLP_RESEARCHER=your_chat_id

# Run
python -m src.main nlp_researcher
```
