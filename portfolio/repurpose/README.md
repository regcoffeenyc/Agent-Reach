# repurpose

Turn one source document into multi-channel content that has already passed an
automated quality gate.

The model drafts. Code that cannot hallucinate decides whether it ships.

```
$ repurpose samples/source.md --profile profiles/example.yaml --dry-run

[FAIL] linkedin_post              436 chars, 2 attempt(s)
        [FAIL] claims_grounded: '47%' does not appear in the source material
        [FAIL] banned_phrases: contains banned phrase 'it's important to note'
        [FAIL] required: missing required element 'northwind.example/report'
[WARN] cross-channel: shares 8+ words verbatim with 'linkedin_post'

Review failed — nothing here is ready to publish.
$ echo $?
1
```

## Why the gate is the product

Anyone can prompt a model into a LinkedIn post. The reason clients stop paying
for AI-assisted content is that somewhere in the batch a confident paragraph
contains a statistic nobody can source, or the tenth post that month opens with
the same three sentences as the ninth.

This pipeline treats those as build failures. Non-zero exit, no publish.

| Check | Severity | What it catches |
| --- | --- | --- |
| `claims_grounded` | fail | Any number in the draft that isn't in the source — the fabricated-statistic failure |
| `banned_phrases` | fail | House-style violations and stock AI register |
| `length` | fail | Platform limits and minimums |
| `required` | fail | Missing CTA, link, disclosure, or legal line |
| `readability` | warn | Drift above the audience's reading level |
| `duplication` | warn | Verbatim runs shared across channels |

Failures block. Warnings inform. A draft that fails is fed its own scorecard and
rewritten once before the pipeline gives up — so most runs self-correct, and the
ones that don't are flagged rather than shipped.

## Install

```bash
pip install -e ".[llm,dev]"
```

`--dry-run` needs neither an API key nor the `llm` extra: it swaps in a stub
model that deliberately fabricates a statistic and reuses source sentences, so
you can watch the gate work offline. That stub is also what the test suite runs
against.

## Use

```bash
export ANTHROPIC_API_KEY=...        # or: ant auth login
repurpose article.md --profile profiles/acme.yaml --out dist/
```

Outputs one Markdown file per channel plus `scorecard.md` in `--out`.

| Flag | Default | Purpose |
| --- | --- | --- |
| `--profile` | required | Client profile YAML |
| `--out` | `dist` | Output directory |
| `--dry-run` | off | Offline stub model, no API key |
| `--max-attempts` | 2 | Rewrite attempts per channel before giving up |
| `--effort` | `medium` | Model effort: `low`…`max` |

## Client profiles

One YAML file per client defines voice, audience, channels, and the rules the
gate enforces. Adding a client is a new file, not a code change.

```yaml
client: Northwind Logistics
voice: >
  Plain, concrete, faintly dry. Short sentences. No exclamation marks.
audience: >
  Warehouse and fleet operations managers at mid-size distributors.

banned_phrases: [revolutionize, seamless]   # extends the built-in list

channels:
  linkedin_post:
    brief: >
      A single LinkedIn post. Open with the concrete finding, not a hook
      question. One idea only. End with the link.
    rules:
      min_chars: 400
      max_chars: 1300
      max_reading_grade: 9
      required: [northwind.example/report]
```

A profile's `banned_phrases` extends the built-in defaults rather than replacing
them — adding one client-specific phrase can't silently switch off every other
check.

## Layout

```
repurpose/
  qa.py         the gate — pure functions, no API calls, no I/O
  pipeline.py   draft → review → repair → draft
  config.py     profile loading
  llm.py        Claude client + offline stub
  cli.py        argument parsing and the scorecard writer
tests/          20 tests, no network
```

`qa.py` has no dependency on the model layer, which is what makes the rules
testable: every check is a pure function over `(draft, source, rules)`.

## Tests

```bash
pytest -q      # 20 passed
```

The suite covers number normalisation (`$1,200,000` vs `1200000`), list markers
that look like claims, the repair loop firing exactly once on a failed draft,
giving up after `--max-attempts`, and the CLI's non-zero exit on failure.

## Extending

- **New check**: add a `check_*` function in `qa.py` returning `list[Finding]`,
  call it from `review()`. `fail` blocks, `warn` reports.
- **New channel**: add an entry under `channels:` in the profile.
- **New client**: new profile file.

## Licence

MIT.
