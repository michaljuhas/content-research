import logging
from ddgs import DDGS
from .base import Signal, SignalCollection, SourceCollector

logger = logging.getLogger(__name__)


class BuildsCollector(SourceCollector):
    """Finds 'what people are building with AI' — project showcases, tutorials, and step-by-step
    guides published on developer blogs, newsletters, and indie maker communities."""

    def collect(self, config: dict) -> SignalCollection:
        source_cfg = config.get("sources", {}).get("builds", {})
        searches = config.get("signals", {}).get("builds_searches", [])
        max_results = source_cfg.get("max_results", 10)
        time_range = source_cfg.get("time_range", "w")

        signals: list[Signal] = []
        errors: list[str] = []
        seen_urls: set[str] = set()

        for query in searches:
            try:
                with DDGS() as ddgs:
                    results = ddgs.text(query, timelimit=time_range, max_results=max_results)
                    count = 0
                    for r in results or []:
                        url = r.get("href", "")
                        if not url or url in seen_urls:
                            continue
                        seen_urls.add(url)
                        signals.append(Signal(
                            title=r.get("title", ""),
                            url=url,
                            summary=r.get("body", ""),
                            source_name=query,
                            source_type="ai_build",
                            published_at="",
                        ))
                        count += 1
                logger.info("BuildsCollector: '%s' — %d result(s)", query, count)
            except Exception as e:
                msg = f"BuildsCollector failed for '{query}': {e}"
                logger.warning(msg)
                errors.append(msg)

        return SignalCollection(signals=signals, errors=errors)
