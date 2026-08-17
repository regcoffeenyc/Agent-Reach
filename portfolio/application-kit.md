# Application kit — AI automation / content operations

Everything below is written to be used as-is. Replace the bracketed bits.

---

## 1. Upwork / Contra profile

**Headline** (this is the whole pitch — most people waste it):

> AI content pipelines with a QA gate — I ship automations that catch their own hallucinations

**Overview:**

> Most AI content work fails the same way: somewhere in the batch, a confident
> paragraph contains a statistic nobody can source, and the client finds it
> before you do.
>
> I build the layer that stops that. My pipelines draft with Claude or GPT, then
> run every output through automated checks before a human ever sees it — every
> number verified against the source document, house-style violations blocked,
> platform limits enforced, cross-channel copy-paste flagged. Failed drafts get
> rewritten automatically. Anything still failing is reported, not published.
>
> What that means for you: you get volume without the reputational risk, and a
> scorecard showing exactly what was checked.
>
> **What I build**
> - Content repurposing pipelines (one source → LinkedIn, newsletter, SEO, social)
> - Lead enrichment and CRM hygiene automations
> - Make.com / n8n / Zapier workflows with error handling that actually fires
> - Document → structured data extraction with validation
>
> **Stack:** Python, Claude API, Make.com, n8n, Google Workspace APIs, GitHub Actions
>
> I work fixed-scope for the first engagement so you can evaluate the work
> without committing to a retainer. Portfolio and a runnable code sample below —
> the sample includes its own test suite, which is unusual in this category and
> is the point.

**Skills to tag:** Python, API Integration, Automation, Content Strategy, Prompt Engineering, Make.com, Data Extraction, Quality Assurance

---

## 2. Cover letter — content automation roles

> Hi [name],
>
> You're looking for someone who can build content automations that produce
> client-ready output, not just technically functional output. That distinction
> is most of the job, so I'll be specific about how I handle it.
>
> I build pipelines where the model drafts and code decides whether it ships.
> Every generated piece runs through automated checks before review: numbers
> verified against the source document, banned phrases blocked, platform limits
> enforced, cross-channel duplication flagged. Drafts that fail get rewritten
> automatically with their own scorecard as input. Anything still failing exits
> non-zero — nothing reaches a client feed by default.
>
> I've put a working version on GitHub: [link]. It runs offline with `--dry-run`,
> has 20 tests, and the stub model deliberately fabricates a statistic so you can
> watch the gate catch it. Two minutes to clone and run.
>
> On your three channels — [blog-to-video / newsletter / blog], adjust — the part
> I'd want to get right first is [the specific thing from their posting]. Happy to
> walk through my approach on a call, or to do a small paid scoped piece so you
> can see the working style before committing.
>
> [name]

---

## 3. Cover letter — "AI content quality" roles

Use for anything framed as reviewing, editing, or QA-ing AI output.

> Hi [name],
>
> The role is reviewing AI-generated content before publication. I've been doing
> that, and I got tired enough of catching the same four errors by hand that I
> automated the catching.
>
> The recurring failures are predictable: fabricated statistics that read as
> plausible, stock phrasing that flags the content as machine-written, near-
> duplicate copy across channels, and drift from the client's actual voice into
> generic marketing register. Three of those four can be checked mechanically.
> The fourth — voice — is where human judgment earns its cost.
>
> So my approach is to automate the mechanical checks and spend the review time
> on what actually needs a person. Working code here: [link].
>
> I'd bring the same split to your process: reduce what you're checking by hand,
> document why each rejected piece failed so the feedback to the generator is
> concrete, and keep the human attention on judgment calls.
>
> [name]

---

## 4. Upwork proposal template

Short. Most proposals lose by being long.

> [First line: restate their actual problem in your own words. No greeting
> paragraph, no "I'm excited about this opportunity."]
>
> Example: "You've got a Make.com flow producing videos that are technically
> fine and off-brand, and polishing each one by hand is eating the time saving."
>
> I've built this shape of pipeline before — [one sentence, specific].
>
> How I'd approach yours:
> 1. [step]
> 2. [step]
> 3. [step]
>
> Working sample of my pipeline code, with tests: [link]. Runs offline in
> two minutes.
>
> [One genuine question about their setup — proves you read the posting and
> starts a conversation rather than ending one.]
>
> Fixed price for the first scope so you can evaluate without a retainer.

**Rules that matter more than the wording:**
- Apply within the first hour. Response rate collapses after that.
- Never send the same proposal twice — the specific line about *their* problem is
  the whole reason it works.
- The Loom walkthrough is not optional. Several postings require it outright, and
  where it's optional it roughly doubles your reply rate.

---

## 5. The two-minute Loom script

Multiple postings I found explicitly require a video walkthrough. Record once,
reuse:

- **0:00–0:15** — "I'm [name]. I build AI content pipelines. Here's one running."
- **0:15–0:45** — Terminal. Run `repurpose samples/source.md --profile
  profiles/example.yaml --dry-run`. Let the FAIL lines land on screen.
- **0:45–1:20** — "The model wrote a clean-looking paragraph claiming a 47%
  improvement. That number isn't in the source. The gate caught it and blocked
  the publish. This is the failure mode that loses clients."
- **1:20–1:45** — Open `scorecard.md`. "Every check, per channel, with the
  evidence. This is what I hand over with each batch."
- **1:45–2:00** — "Same pipeline adapts to your channels through a YAML file.
  Happy to walk through your setup."

Don't script it word for word. Do run it once before recording so the terminal
output is already warm.

---

## 6. Rates

Anchor on the value, not the hour. For non-US applicants the platform average is
a floor to beat, not a target to match.

| Engagement | Range | Notes |
| --- | --- | --- |
| Pipeline build (fixed scope) | $800–2,500 | First engagement — deliberately scoped small |
| Monthly retainer (run + maintain) | $600–1,800/mo | Where the actual money is |
| Hourly (avoid where possible) | $25–45/hr | Only for genuinely open-ended work |

Move to retainer by the second month. Fixed-scope work doesn't compound.

---

## 7. Two-week plan

**Week 1**
- Push `repurpose` to a public GitHub repo under your own account
- Record the Loom
- Write the Upwork profile from section 1
- Apply to 5 automation postings using the section 4 template — quality over volume

**Week 2**
- Apply to 5 more; iterate the proposal opener based on what got replies
- Adapt the pipeline to one real public source (a company blog post) and add
  the output as a second portfolio piece
- Register Wise and Payoneer if you haven't — several platforms pay through Deel,
  Tipalti, or Payoneer, and PayPal is restricted in a number of countries

**What to measure:** replies per 10 proposals. Below 1, the opener is wrong.
Above 3, raise your rate.
