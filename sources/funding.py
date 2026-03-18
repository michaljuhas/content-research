import logging
from ddgs import DDGS
from .base import Signal, SignalCollection, SourceCollector

logger = logging.getLogger(__name__)


class GeneralNewsCollector(SourceCollector):
    def collect(self, config: dict) -> SignalCollection:
        queries = config.get("signals", {}).get("general_news_searches", [])
        source_cfg = config.get("sources", {}).get("general_news", {})
        max_results = source_cfg.get("max_results", 10)
        time_range = source_cfg.get("time_range", "w")

        signals: list[Signal] = []
        errors: list[str] = []
        seen_urls: set[str] = set()

        for query in queries:
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
                            source_name="General AI News",
                            source_type="general_news",
                            published_at="",
                        ))
                        count += 1
                logger.info("GeneralNewsCollector: '%s' — %d result(s)", query, count)
            except Exception as e:
                msg = f"GeneralNewsCollector failed for query '{query}': {e}"
                logger.warning(msg)
                errors.append(msg)

        logger.info("GeneralNewsCollector: %d unique signals total", len(signals))
        return SignalCollection(signals=signals, errors=errors)
