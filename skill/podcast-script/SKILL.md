---
name: podcast-script
description: Generate a podcast episode script from today's stream brief.
---

Generate a podcast episode script and a matching Substack post from today's brief.

## Inputs

- Today's brief: `briefs/YYYY-MM-DD.md` (read the ⭐ Stream Picks section)
- Existing episode examples: `podcasts/` folder (read 1–2 recent `-episode.md` files to match tone and format)

## Output files

Save two files to `podcasts/`:
- `podcasts/YYYY-MM-DD-episode.md` — the spoken podcast script
- `podcasts/YYYY-MM-DD-substack.md` — the written Substack newsletter post

---

## Episode script format (`-episode.md`)

```
# AI with Michal — Episode Script
**Date:** [Month Day, Year]
**Topic:** [3–5 word punchy topic line summarising the episode's through-line]

---

## INTRO

Hey everyone, welcome back to AI with Michal.

I'm Michal, and if you're new here — this podcast is for people who use AI in their actual work. Recruiting, marketing, sales, operations. Not theory. Not hype. Practical stuff.

[N] stories today. Let's go.

---

## SEGMENT [N] — [Story headline]
*Source: [URL]*

[Body — see segment writing rules below]

---

## OUTRO

OK, quick recap.

- [One-line summary per story]

That's it for today. If this was useful, share it with one person on your team who wants to use AI but doesn't know where to start.

One more thing — if you're a company that wants to actually implement this stuff, not just read about it, I work with teams as a fractional AI advisor. We look at your real workflows — recruiting, sales, marketing, operations — and build practical AI into them. I also run courses and workshops for teams who want to get hands-on. If any of that sounds interesting, visit aiwithmichal.com and let's talk.

See you next time.

---

*Episode length estimate: ~[X]–[Y] minutes at a natural pace*
*Sources: AI with Michal daily brief, [Month Day, Year]*
```

---

## Segment writing rules

Each segment body must be **800–900 characters** (not words — count characters). Structure it in three parts:

**Part 1 — What happened (~250–300 chars)**
State the news in plain, direct language. No jargon. One or two sentences max. Write as if you're telling a smart colleague over coffee, not presenting a slide deck.

**Part 2 — Why it matters (~250–300 chars)**
Explain the significance in 2–3 sentences. Connect it to a broader trend or shift. Give the listener the mental model, not just the fact.

**Part 3 — Implication + one specific use case (~250–300 chars)**
Start with the generic implication (what it means for builders, marketers, or recruiters in general). Then add one concrete use case example — pick the single most relevant audience out of:
- **Builders** (people building AI products or automating workflows)
- **Marketers** (people running content, campaigns, or growth with AI)
- **Recruiters** (people hiring or building recruiting pipelines with AI)

Choose the audience that fits the story best. Write the use case as a specific, actionable scenario — not a tip, but a real situation someone could apply tomorrow.

---

## Substack post format (`-substack.md`)

```
# [Episode topic as a punchy headline]

**AI with Michal · [Month Day, Year]**

---

The audio is above. Below is a written summary you can skim, share, or save for later.

---

[One-sentence framing of today's through-line — what connects all the stories.]

---

## [N]. [Story headline]

[Source as markdown link]

[2–3 paragraph written summary. Same structure as the episode segment but written prose, not spoken word. Include the implication and the specific use case example. No bullet points.]

---

## That's it for today

If this was useful, forward it to one person on your team [relevant closing hook matching the episode's theme].

---

*I work with companies as a fractional AI advisor — helping teams build practical AI into their real workflows across recruiting, sales, marketing, and operations. I also run courses and workshops. If you want to go deeper, visit [aiwithmichal.com](https://aiwithmichal.com).*
```

---

## Tone and voice

- Conversational but credible — like a smart friend who reads everything so you don't have to
- Short sentences, active voice, no filler phrases ("it's worth noting that…", "in today's landscape…")
- Practical: always land on what the listener should *do* or *think differently about*
- No em-dash overuse — use periods and line breaks instead when in doubt
- Audience assumes: non-technical but curious, aged 35–50, works in a company that uses or wants to use AI

## Casual register

Write as if you're catching up with someone who's roughly as informed as you — not presenting to a room. This means:

- **Assume shared context before dropping facts.** Don't open a segment with a cold declarative. Instead, briefly acknowledge what the listener might already know, then build from there.

  Bad: "Jason Lemkin, founder of SaaStr, posted his actual daily schedule this week."
  Good: "Jason Lemkin — founder of SaaStr, which you might have heard of — posted his actual daily schedule this week."

  Bad: "An AI built by researchers at UBC, Sakana AI, and the Vector Institute just had a paper published in Nature."
  Good: "You know about the Nature paper, right? An AI built by researchers from several institutions — UBC, Sakana AI, the Vector Institute — just got published there."

- **Use softeners and bridges naturally.** Phrases like "which you might have heard of", "you've probably seen this", "and here's the part that got me", "so here's what that actually means" make the listener feel like a peer, not an audience.

- **It's okay to editorialize briefly.** A short reaction ("That's not a demo. That's a real result." / "And honestly, that's the part nobody's talking about.") makes the script feel human. Don't overdo it — one per segment max.

- **Don't over-introduce people.** If the person is well known in AI circles, a brief parenthetical is enough. If they're less known, one sentence of context is fine, but don't write a bio.

## Sentence flow

Every sentence must connect naturally to the one before it. Read the segment out loud — if you'd need to pause and reorient yourself, the flow is broken.

**Common mistakes to avoid:**

- **Fragments that don't follow from the previous sentence.** Bad: "Make the review loop part of the contract before you ship. A 15-minute daily check-in on outputs, drift, and errors. Clients won't ask for it." — the second sentence is a fragment that doesn't grammatically or logically continue from the first. Fix: "Before you ship, make the review loop part of the contract — a 15-minute daily check-in on outputs, drift, and errors. Clients won't ask for it."
- **Abrupt topic hops.** Each sentence should either continue the previous thought or explicitly signal a shift ("Here's the part nobody talks about." / "That's the real story." / "So what does that mean for you?").
- **Stacked short sentences that don't build.** Three short sentences in a row can sound punchy or choppy depending on whether they escalate. "Healthcare. Legal. Finance." works because it's a deliberate list. "The agent degraded. He stopped watching. Nobody noticed." works because it's a narrative sequence. Avoid three disconnected fragments that just happen to be short.

**Test:** Read every segment out loud before finalising. If a sentence makes you stumble or mentally re-read, rewrite it.
