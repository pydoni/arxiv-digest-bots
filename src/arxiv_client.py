"""Fetch recent papers from ArXiv matching bot topics."""

import urllib.parse
from datetime import datetime, timedelta, timezone

import feedparser

ARXIV_API_URL = "http://export.arxiv.org/api/query"


def fetch_recent_papers(
    categories: list[str],
    keywords: list[str],
    max_papers: int,
) -> list[dict]:
    cat_query = " OR ".join(f"cat:{cat}" for cat in categories)
    url = f"{ARXIV_API_URL}?{urllib.parse.urlencode({
        'search_query': cat_query,
        'start': 0,
        'max_results': 200,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending',
    })}"

    feed = feedparser.parse(url)
    cutoff = datetime.now(timezone.utc) - timedelta(days=5)
    keywords_lower = [kw.lower() for kw in keywords]

    papers = []
    for entry in feed.entries:
        published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        if published < cutoff:
            continue

        title = entry.title.replace("\n", " ").strip()
        abstract = entry.summary.replace("\n", " ").strip()
        searchable = f"{title} {abstract}".lower()

        if not any(kw in searchable for kw in keywords_lower):
            continue

        papers.append({
            "title": title,
            "authors": _format_authors(entry.authors),
            "abstract": abstract,
            "url": entry.link,
            "categories": [tag.term for tag in entry.tags],
            "published": published.strftime("%Y-%m-%d"),
        })

        if len(papers) >= max_papers:
            break

    return papers


def _format_authors(authors: list) -> str:
    names = [a.get("name", "") for a in authors]
    if len(names) <= 2:
        return ", ".join(names)
    return f"{names[0]}, {names[1]} et al."
