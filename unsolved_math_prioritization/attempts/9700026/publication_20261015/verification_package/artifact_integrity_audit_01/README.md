# PR880 artifact-integrity audit

Read REPORT.md and DECISION.json, then the independently written THREAT_SCOPE.md and STATIC_CODE_REVIEW.md. Raw metadata-only receipts are RESULTS_WITH_PROVENANCE.json and RESULTS_SOURCE_FREE.json.

Run from this folder with Python's standard library:

```sh
python3 -I -B audit_harness.py
python3 -I -B -O audit_harness.py
```

The default replay explicitly marks optional provenance NOT_RUN. `--provenance` additionally reads the existing complete unchanged local corpora and separately held primary PDFs; it creates only temporary verified ordinary-file hardlinks and removes them after use. Never replace the startup trust boundary with an untrusted script's self-hash. Inspect or externally authenticate this harness before execution.

The audit supplies artifact/reproduction evidence only, not a mathematical verdict, literature/priority finding or formal proof certificate. Original artifacts are unchanged. The public manifest includes only authored notes/code and metadata receipts; it excludes all primary PDFs, extracts, renders, corpora, canonical-pair payloads and disposable fixtures.
