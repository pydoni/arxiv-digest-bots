"""ArXiv AI Digest - main entrypoint."""

import sys

from src.config import load_config
from src.arxiv_client import fetch_recent_papers
from src.summarizer import summarize_papers
from src.telegram_notifier import send_digest, MIN_RELEVANCE_SCORE


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <bot_name>")
        print("Example: python -m src.main ml_engineer")
        sys.exit(1)

    bot_name = sys.argv[1]
    config = load_config(bot_name)

    print(f"[{config.emoji} {config.name}] Fetching papers...")
    papers = fetch_recent_papers(
        categories=config.arxiv_categories,
        keywords=config.keywords,
        max_papers=config.max_papers,
    )
    print(f"  Found {len(papers)} papers")

    if papers:
        print(f"  Summarizing with Haiku...")
        papers = summarize_papers(
            papers=papers,
            summary_prompt=config.summary_prompt,
            api_key=config.anthropic_api_key,
        )
        relevant = [p for p in papers if p.get("score", 0) >= MIN_RELEVANCE_SCORE]
        print(f"  {len(relevant)}/{len(papers)} papers passed relevance filter (score >= {MIN_RELEVANCE_SCORE})")

    print(f"  Sending digest via Telegram...")
    send_digest(
        papers=papers,
        bot_name=config.name,
        emoji=config.emoji,
        token=config.telegram_bot_token,
        chat_id=config.telegram_chat_id,
    )
    print(f"  Done!")


if __name__ == "__main__":
    main()
