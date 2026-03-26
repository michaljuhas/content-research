from datetime import date
from sources.base import SignalCollection


def build(collection: SignalCollection, config: dict) -> str:
    today = date.today().strftime("%A, %B %-d, %Y")
    lenses = config.get("content_lenses", [])
    lens_labels = [l["label"] for l in lenses]

    companies = config.get("signals", {}).get("companies", [])
    individuals = config.get("signals", {}).get("individuals", [])
    n_companies = len(companies)
    n_individuals = len(individuals)
    n_signals = len(collection.signals)

    # Group signals by source type
    company_signals = [s for s in collection.signals if s.source_type == "company_blog"]
    individual_signals = [s for s in collection.signals if s.source_type in (
        "individual_threads", "individual_twitter", "individual_linkedin"
    )]
    general_signals = [s for s in collection.signals if s.source_type == "general_news"]
    reddit_signals = [s for s in collection.signals if s.source_type == "reddit"]
    builds_signals = [s for s in collection.signals if s.source_type == "ai_build"]

    lines = [
        f"Today is {today}.",
        "",
        f"You are preparing a **live stream brief** for a content creator.",
        f"You have collected {n_signals} signals from {n_companies} companies/media sources "
        f"and {n_individuals} AI thought leaders.",
        "",
        "The creator will go live and share their screen on 5–6 items, reading/commenting on each "
        "for 2–3 minutes. Your job is to pick the best items and write a ready-to-use brief for each.",
        "",
        "YOUR TASKS:",
        "1. Review ALL signals below.",
        "2. Select the 6–7 most compelling items for a live stream audience interested in AI.",
        "   Priority order (highest to lowest):",
        "   - BREAKTHROUGH: new model release, major research paper, significant product launch",
        "   - THOUGHT LEADER: original opinion/post from a known AI figure",
        "   - INTERESTING: notable event, surprising finding, industry shift",
        "   - AI BUILD: step-by-step guide or showcase of something someone built with AI",
        "   - GENERAL NEWS: relevant AI news article",
        "3. For each pick, write a Stream Feature Card (see format below).",
        "4. After the picks, list ALL collected signals as a reference section.",
        "5. Keep everything factual — do not invent details not present in the raw data.",
        "6. Prefer items from the last 24–48 hours over older ones.",
        "7. Prefer original posts/announcements over articles summarising them.",
        "8. Prefer specific ('Claude adds X feature') over vague ('AI is changing everything').",
        "9. Prefer original content over curated summaries.",
        "",
        "Content lenses to use for Audience tags (apply whichever are relevant):",
    ]
    for label in lens_labels:
        lines.append(f"  - {label}")

    lines += [
        "",
        "=" * 60,
        "RAW SIGNAL DATA",
        "=" * 60,
    ]

    def format_signals(signals, label):
        if not signals:
            return [f"\n[{label}] No signals collected."]
        out = [f"\n[{label}] {len(signals)} signal(s):"]
        for i, s in enumerate(signals, 1):
            out.append(f"  {i}. [{s.source_name}] {s.title}")
            out.append(f"     URL: {s.url}")
            if s.score > 0:
                out.append(f"     Upvotes: {s.score}")
            if s.summary:
                out.append(f"     Excerpt: {s.summary[:350].replace(chr(10), ' ')}")
        return out

    lines += format_signals(company_signals, "COMPANY & MEDIA")
    lines += format_signals(individual_signals, "THOUGHT LEADER POSTS (Threads / X / LinkedIn)")
    lines += format_signals(builds_signals, "AI BUILDS & INSPIRATION")
    lines += format_signals(general_signals, "GENERAL AI NEWS")
    lines += format_signals(reddit_signals, "REDDIT COMMUNITY")

    if collection.errors:
        lines += ["", "[COLLECTION ERRORS]"]
        for err in collection.errors:
            lines.append(f"  - {err}")

    # Output format template
    lines += [
        "",
        "=" * 60,
        "OUTPUT FORMAT (produce exactly this Markdown structure):",
        "=" * 60,
        "",
        f"# Live Stream Brief — {today}",
        f"*Tracking: {n_companies} companies/media, {n_individuals} thought leaders "
        f"| {n_signals} signals collected*",
        "",
        "---",
        "",
        "## ⭐ Stream Picks",
        "",
        "### 1. [Headline — what happened in plain language]",
        "- **Hook:** 1–2 conversational sentences to open this segment on air.",
        "- **Why it matters:** 2–3 sentences explaining the significance.",
        "- **Implication:** What it means for the AI builders (people in their 40s who want to build AI products and automate with AI).",
        "- **Type:** Breakthrough / Interesting / Thought Leader / AI Build / General News",
        "- **URL:** [Direct link](url)",
        "",
        "### 2. [Headline]",
        "*(repeat card format)*",
        "",
        "*(5–6 picks total)*",
        "",
        "---",
        "",
        "## All Signals (reference)",
        "",
        "### Company & Media",
        "- **[Source]** [Title] — [URL]",
        "",
        "### Thought Leader Posts",
        "- **[Person, Platform]** [Summary] — [URL]",
        "",
        "### AI Builds & Inspiration",
        "- [Title] — [URL]",
        "",
        "### General AI News",
        "- [Title] — [URL]",
        "",
        "### Community (Reddit)",
        "- **[r/subreddit]** [Title] ↑[score] — [URL]",
        "",
        "---",
        "",
        "## Collection Notes",
        "- [List any errors, empty sources, or gaps. If all clean, write 'All sources returned data.']",
    ]

    return "\n".join(lines)
