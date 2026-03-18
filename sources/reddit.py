import logging
import os
import praw
from .base import Signal, SignalCollection, SourceCollector

logger = logging.getLogger(__name__)


def _make_reddit_client() -> praw.Reddit | None:
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    if not client_id or not client_secret:
        return None
    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=os.environ.get("REDDIT_USER_AGENT", "content-research/1.0"),
        # Read-only mode — no username/password needed
    )


class RedditCollector(SourceCollector):
    def __init__(self):
        self._reddit: praw.Reddit | None = None

    def _get_reddit(self) -> praw.Reddit | None:
        if self._reddit is None:
            self._reddit = _make_reddit_client()
        return self._reddit

    def collect(self, config: dict) -> SignalCollection:
        reddit = self._get_reddit()
        if reddit is None:
            logger.info("Reddit credentials not set — skipping Reddit collection")
            return SignalCollection()

        source_cfg = config.get("sources", {}).get("reddit", {})
        max_results = source_cfg.get("max_results_per_entity", 3)
        subreddits = source_cfg.get("subreddits", ["artificial"])
        sub = reddit.subreddit("+".join(subreddits))

        # Build entity names to search for from companies + individuals
        signals_cfg = config.get("signals", {})
        entities = (
            [c["name"] for c in signals_cfg.get("companies", []) if c.get("name")]
            + [p["name"] for p in signals_cfg.get("individuals", []) if p.get("name")]
        )

        signals: list[Signal] = []
        errors: list[str] = []
        seen_urls: set[str] = set()

        for entity in entities:
            try:
                results = sub.search(
                    f'"{entity}" AI',
                    sort="relevance",
                    time_filter="week",
                    limit=max_results,
                )
                count = 0
                for post in results:
                    url = f"https://reddit.com{post.permalink}"
                    if url in seen_urls:
                        continue
                    seen_urls.add(url)
                    body = post.selftext[:400].strip() if post.selftext else ""
                    if not body and not post.is_self:
                        body = f"Link post → {post.url}"
                    signals.append(Signal(
                        title=post.title,
                        url=url,
                        summary=body or "(no body text)",
                        source_name=entity,
                        source_type="reddit",
                        published_at="",
                        score=post.score,
                    ))
                    count += 1
                if count:
                    logger.info("RedditCollector: '%s' — %d post(s)", entity, count)
            except Exception as e:
                msg = f"RedditCollector failed for entity '{entity}': {e}"
                logger.warning(msg)
                errors.append(msg)

        return SignalCollection(signals=signals, errors=errors)
