"""Send digest messages via Telegram Bot API."""

import json
import urllib.request
from datetime import datetime, timezone, timedelta

BRT = timezone(timedelta(hours=-3))
MAX_MESSAGE_LENGTH = 4096
MIN_RELEVANCE_SCORE = 3


def send_digest(
    papers: list[dict],
    bot_name: str,
    emoji: str,
    token: str,
    chat_id: str,
) -> None:
    # Filter by relevance and sort by score descending
    relevant = [p for p in papers if p.get("score", 0) >= MIN_RELEVANCE_SCORE]
    relevant.sort(key=lambda p: p.get("score", 0), reverse=True)

    if not relevant:
        return

    header = (
        f"{emoji} *ArXiv Digest: {bot_name}*\n"
        f"\U0001F4C5 {_today()} | {len(relevant)} papers\n"
    )

    messages = _build_messages(header, relevant)
    for msg in messages:
        send_message(msg, token, chat_id)


def send_message(text: str, token: str, chat_id: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req)


def _build_messages(header: str, papers: list[dict]) -> list[str]:
    messages = []
    current = header

    for i, paper in enumerate(papers):
        if i == 0:
            entry = _format_highlight(paper)
        else:
            entry = _format_paper(i, paper)

        if len(current) + len(entry) > MAX_MESSAGE_LENGTH:
            messages.append(current)
            current = ""

        current += entry

    footer = (
        f"\n{'─' * 20}\n\n"
        "\U00002615 _Enjoying the digest? "
        "[Support my token expenses!]"
        "(https://wise.com/pay/me/pedrohenriquef557?utm_source=request_flow)_"
    )

    if current:
        if len(current) + len(footer) > MAX_MESSAGE_LENGTH:
            messages.append(current)
            messages.append(footer)
        else:
            current += footer
            messages.append(current)

    return messages


def _format_highlight(paper: dict) -> str:
    tag = paper.get("tag", "Unknown")
    return (
        f"\n\u2B50 *HIGHLIGHT*\n"
        f"[{tag}] *{_escape_markdown(paper['title'])}*\n"
        f"\U0001F465 {_escape_markdown(paper['authors'])}\n\n"
        f"{paper['summary']}\n\n"
        f"\U0001F517 [Read paper]({paper['url']})\n"
    )


def _format_paper(index: int, paper: dict) -> str:
    tag = paper.get("tag", "Unknown")
    return (
        f"\n{'─' * 20}\n\n"
        f"*{index}. [{tag}] {_escape_markdown(paper['title'])}*\n"
        f"\U0001F465 {_escape_markdown(paper['authors'])}\n\n"
        f"{paper['summary']}\n\n"
        f"\U0001F517 [Read paper]({paper['url']})\n"
    )


def _escape_markdown(text: str) -> str:
    for char in ["_", "*", "`", "["]:
        text = text.replace(char, f"\\{char}")
    return text


def _today() -> str:
    return datetime.now(BRT).strftime("%d/%m/%Y")
