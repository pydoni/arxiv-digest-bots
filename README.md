# ArXiv AI Digest

Daily ArXiv paper digests for data professionals, delivered via Telegram. Powered by Claude Haiku.

## How it works

1. **GitHub Actions** triggers a cron job every weekday at 8am BRT
2. For each of the 6 professional profiles, the bot:
   - Fetches recent papers from ArXiv matching the profile's topics
   - Summarizes each abstract in 3 bullet points using Claude Haiku
   - Sends a formatted digest to the profile's Telegram bot
3. Each profile has a curated set of keywords and a custom summarization prompt

## Professional Profiles

| Bot | Focus |
|-----|-------|
| ML Engineer | MLOps, model serving, distributed training, monitoring |
| Data Scientist | Causal inference, experimental design, Bayesian methods, time series |
| AI/GenAI Engineer | LLMs, RAG, agents, prompting, fine-tuning |
| CV Engineer | Object detection, segmentation, 3D vision, edge deployment |
| Data Engineer | Pipelines, streaming, lakehouse, data quality, orchestration |
| Analytics Engineer | Metrics, experimentation platforms, causal discovery, forecasting |

## Setup

### 1. Create Telegram Bots

Create 6 bots via [@BotFather](https://t.me/BotFather) on Telegram. Save each token.

### 2. Get Chat IDs

For each bot:
1. Send `/start` to the bot
2. Visit `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Copy the `chat.id` from the response

### 3. Configure Secrets

Add these secrets to your GitHub repo (Settings > Secrets > Actions):

- `ANTHROPIC_API_KEY`
- `TELEGRAM_BOT_TOKEN_ML_ENGINEER` / `TELEGRAM_CHAT_ID_ML_ENGINEER`
- (repeat for each bot)

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

- **GitHub Actions**: ~66 min/month (free tier: 2000 min)
- **Anthropic Haiku**: ~$1.50/month
- **Telegram**: Free

## Tech Stack

- Python 3.11+
- Claude Haiku (paper summarization)
- ArXiv API (paper fetching)
- Telegram Bot API (delivery)
- GitHub Actions (scheduling)
