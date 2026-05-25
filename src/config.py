"""Bot configuration loader."""

import os
from dataclasses import dataclass
from pathlib import Path

import yaml

# Load .env if present (local development)
_env_path = Path(__file__).parent.parent / ".env"
if _env_path.exists():
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

BOTS_DIR = Path(__file__).parent.parent / "bots"


@dataclass
class BotConfig:
    name: str
    emoji: str
    description: str
    arxiv_categories: list[str]
    keywords: list[str]
    summary_prompt: str
    max_papers: int
    telegram_bot_token: str
    telegram_chat_id: str
    anthropic_api_key: str


def load_config(bot_name: str) -> BotConfig:
    yaml_path = BOTS_DIR / f"{bot_name}.yaml"
    if not yaml_path.exists():
        available = [f.stem for f in BOTS_DIR.glob("*.yaml")]
        raise FileNotFoundError(
            f"Bot config '{bot_name}' not found. Available: {available}"
        )

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    telegram_token = os.environ.get(data["telegram_token_env"], "")
    telegram_chat_id = os.environ.get(data["telegram_chat_id_env"], "")
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    if not telegram_token:
        raise ValueError(f"Missing env var: {data['telegram_token_env']}")
    if not telegram_chat_id:
        raise ValueError(f"Missing env var: {data['telegram_chat_id_env']}")
    if not anthropic_api_key:
        raise ValueError("Missing env var: ANTHROPIC_API_KEY")

    return BotConfig(
        name=data["name"],
        emoji=data["emoji"],
        description=data["description"],
        arxiv_categories=data["arxiv_categories"],
        keywords=data["keywords"],
        summary_prompt=data["summary_prompt"],
        max_papers=data["max_papers"],
        telegram_bot_token=telegram_token,
        telegram_chat_id=telegram_chat_id,
        anthropic_api_key=anthropic_api_key,
    )
