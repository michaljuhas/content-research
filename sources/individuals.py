import logging
from ddgs import DDGS
from .base import Signal, SignalCollection, SourceCollector

logger = logging.getLogger(__name__)


class IndividualPostsCollector(SourceCollector):
    def collect(self, config: dict) -> SignalCollection:
        individuals = config.get("signals", {}).get("individuals", [])
        source_cfg = config.get("sources", {}).get("individuals", {})
        max_results = source_cfg.get("max_results_per_person", 3)
        time_range = source_cfg.get("time_range", "w")

        signals: list[Signal] = []
        errors: list[str] = []
        seen_urls: set[str] = set()

        for person in individuals:
            name = person.get("name", "")
            searches: list[tuple[str, str]] = []  # (query, source_type)

            if handle := person.get("threads"):
                searches.append((f"site:threads.net/@{handle}", "individual_threads"))
            if handle := person.get("twitter"):
                searches.append((f"site:x.com/{handle}", "individual_twitter"))
            if handle := person.get("linkedin"):
                searches.append((f"site:linkedin.com/in/{handle}", "individual_linkedin"))

            for query, source_type in searches:
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
                                source_name=name,
                                source_type=source_type,
                                published_at="",
                            ))
                            count += 1
                    logger.info("IndividualPostsCollector: %s (%s) — %d result(s)", name, source_type, count)
                except Exception as e:
                    msg = f"IndividualPostsCollector failed for '{name}' ({source_type}): {e}"
                    logger.warning(msg)
                    errors.append(msg)

        return SignalCollection(signals=signals, errors=errors)
