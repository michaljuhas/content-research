from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Signal:
    title: str
    url: str
    summary: str
    source_name: str      # "Anthropic", "Sam Altman", etc.
    source_type: str      # "company_blog" | "individual_threads" | "individual_linkedin" | "funding_news" | "reddit"
    published_at: str     # ISO date or empty string
    score: int = 0        # Reddit upvotes; 0 for all other sources


@dataclass
class SignalCollection:
    signals: list[Signal] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class SourceCollector(ABC):
    @abstractmethod
    def collect(self, config: dict) -> SignalCollection:
        """Collect signals. Must not raise — return errors inside SignalCollection instead."""
        ...
