# portfolio/

Personal work product. **Not part of Agent Reach** — nothing here is imported by
`agent_reach/`, nothing here changes its behaviour, and this directory should
never be included in an upstream pull request.

| Path | What it is |
| --- | --- |
| `repurpose/` | A standalone AI content pipeline with an automated quality gate. Own package, own `pyproject.toml`, own tests. |
| `application-kit.md` | Freelance application materials — profile copy, cover letters, proposal template, rates. |
| `case-study.html` | Portfolio case study page for `repurpose/`. |

## Running the sample project

It is a separate package with its own dependencies:

```bash
cd portfolio/repurpose
pip install -e ".[llm,dev]"
pytest -q                                     # 20 tests, no network
python -m repurpose.cli samples/source.md \
  --profile profiles/example.yaml --dry-run   # exits 1 by design
```

## Note on the repo's test suite

Agent Reach runs `pytest tests/ -v`, which is scoped to the top-level `tests/`
directory and does not collect anything under `portfolio/`. A bare `pytest` from
the repository root would collect both suites; run the scoped command instead.
