# 11000263: Bigelow's braid-algebra Question 6

**Outcome:** prior public result found and locally checked; no new discovery.
The printed definition is ill-typed. Argus AI Team's August 2026 construction
proves nonvanishing under both natural indexing repairs. We independently
recomputed its all-index argument and 1,590 exact checks.

- [Audit and complete algebraic check](AUDIT.md)
- [Exact verifier](verify.py) and [receipt](verification.json)
- [Source and search provenance](SOURCES.md)
- [Preliminary scalar route and its obstruction](SCALAR_SCOPE_CHECK.md)
- [Research log](RESEARCH_LOG.md), [turn ledger](turns.jsonl), [readiness](readiness.json)
- [Disposition](status.json)

Run from this folder:

```sh
python3 verify.py
```

Only Python's standard library is needed. The test is bounded; the proof for
arbitrary strand count is in the audit. Third-party PDFs and code are not
redistributed. No live queue or shared status file has been modified.

This work uses gpt-6-astra at xhigh reasoning, not the queue's hypothetical
ultra setting. The public construction is credited to its existing source.
An independent review of this audit must be distinguished from the initial
exact recomputation.
