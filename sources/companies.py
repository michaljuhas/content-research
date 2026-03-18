import logging
from ddgs import DDGS
from .base import Signal, SignalCollection, SourceCollector

logger = logging.getLogger(__name__)


class CompanyNewsCollector(SourceCollector):
    def collect(self, config: dict) -> SignalCollection:
        companies = config.get("signals", {}).get("companies", [])
        source_cfg = config.get("sources", {}).get("companies", {})
        max_results = source_cfg.get("max_results_per_company", 3)
        time_range = source_cfg.get("time_range", "w")

        signals: list[Signal] = []
        errors: list[str] = []
        seen_urls: set[str] = set()

        for company in companies:
            name = company.get("name", "")
            domain = company.get("domain", "")
            if not domain:
                continue
            keywords = company.get("keywords", "")
            query = f"site:{domain} {keywords}".strip() if keywords else f"site:{domain}"
            try:
                with DDGS() as ddgs:
                    results = ddgs.text(query, timelimit=time_range, max_results=max_results)
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
                            source_type="company_blog",
                            published_at="",
                        ))
                logger.info("CompanyNewsCollector: %s — %d result(s)", name, sum(1 for s in signals if s.source_name == name))
            except Exception as e:
                msg = f"CompanyNewsCollector failed for '{name}': {e}"
                logger.warning(msg)
                errors.append(msg)

        return SignalCollection(signals=signals, errors=errors)
