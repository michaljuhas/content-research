#!/usr/bin/env python3
"""
Daily content research pipeline.
Monitors curated companies and individuals, collects their latest signals,
then synthesizes a live stream brief using Claude API.

Usage:
    python main.py
    python main.py --no-reddit        # skip Reddit source
    python main.py --no-general-news  # skip general AI news
    python main.py --no-individuals   # skip individual posts
    python main.py --config path/to/config.yaml
"""

import argparse
import logging
import os
import sys
import time
import yaml
from dotenv import load_dotenv

from sources.companies import CompanyNewsCollector
from sources.individuals import IndividualPostsCollector
from sources.funding import GeneralNewsCollector
from sources.reddit import RedditCollector
from sources.builds import BuildsCollector
from sources.base import SignalCollection
from synthesis import prompt_builder, claude_client
from output import brief_writer


def setup_logging(config: dict) -> None:
    logs_dir = config.get("output", {}).get("logs_dir", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(logs_dir, "run.log")),
            logging.StreamHandler(sys.stdout),
        ],
    )


def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def collect_all(config: dict, skip_sources: set[str]) -> SignalCollection:
    source_cfg = config.get("sources", {})
    logger = logging.getLogger(__name__)

    all_signals = []
    all_errors = []

    collectors = []
    if source_cfg.get("companies", {}).get("enabled", True) and "companies" not in skip_sources:
        collectors.append(("companies", CompanyNewsCollector()))
    if source_cfg.get("individuals", {}).get("enabled", True) and "individuals" not in skip_sources:
        collectors.append(("individuals", IndividualPostsCollector()))
    if source_cfg.get("general_news", {}).get("enabled", True) and "general_news" not in skip_sources:
        collectors.append(("general_news", GeneralNewsCollector()))
    if source_cfg.get("reddit", {}).get("enabled", True) and "reddit" not in skip_sources:
        collectors.append(("reddit", RedditCollector()))
    if source_cfg.get("builds", {}).get("enabled", True) and "builds" not in skip_sources:
        collectors.append(("builds", BuildsCollector()))

    for source_name, collector in collectors:
        logger.info("Collecting from: %s ...", source_name)
        try:
            result = collector.collect(config)
            logger.info("  %s: %d signal(s), %d error(s)", source_name, len(result.signals), len(result.errors))
            all_signals.extend(result.signals)
            all_errors.extend(result.errors)
        except Exception as e:
            msg = f"Unhandled exception in {source_name}: {e}"
            logger.error(msg)
            all_errors.append(msg)
        time.sleep(1)  # courtesy pause

    return SignalCollection(signals=all_signals, errors=all_errors)


def main():
    parser = argparse.ArgumentParser(description="Run the daily content research pipeline.")
    parser.add_argument("--no-reddit", action="store_true", help="Skip Reddit source")
    parser.add_argument("--no-general-news", action="store_true", help="Skip general AI news")
    parser.add_argument("--no-individuals", action="store_true", help="Skip individual posts")
    parser.add_argument("--no-builds", action="store_true", help="Skip AI builds & inspiration")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    load_dotenv()
    config = load_config(args.config)
    setup_logging(config)

    logger = logging.getLogger(__name__)
    logger.info("=== Content Research Pipeline starting ===")
    start = time.time()

    skip_sources: set[str] = set()
    if args.no_reddit:
        skip_sources.add("reddit")
    if args.no_general_news:
        skip_sources.add("general_news")
    if args.no_individuals:
        skip_sources.add("individuals")
    if args.no_builds:
        skip_sources.add("builds")

    # Step 1: Collect signals from all sources
    collection = collect_all(config, skip_sources)
    logger.info("Collection complete: %d signals, %d errors", len(collection.signals), len(collection.errors))

    # Step 2: Build synthesis prompt
    logger.info("Building prompt...")
    prompt = prompt_builder.build(collection, config)

    # Step 3: Generate brief with Claude
    logger.info("Calling Claude API to generate brief...")
    brief = claude_client.generate_brief(prompt, config)

    # Step 4: Write brief to disk
    filepath = brief_writer.write(brief, config)
    elapsed = time.time() - start

    logger.info("=== Pipeline complete in %.1fs — brief saved to %s ===", elapsed, filepath)
    print(f"\nBrief saved to: {filepath}\n")
    print(brief)


if __name__ == "__main__":
    main()
