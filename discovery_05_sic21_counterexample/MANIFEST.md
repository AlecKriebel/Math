# Discovery 05 manifest

| File | Purpose |
|---|---|
| `README.md` | Entry point, verification commands, and warning |
| `NOTE.md` | Complete human-readable construction and proof |
| `sic21_counterexample.tex` | Typeset paper source |
| `output/pdf/sic21_counterexample.pdf` | Rendered paper |
| `PRIORITY_AUDIT.md` | Source-specific novelty audit and permitted language |
| `RESEARCH_LOG.md` | Chronological derivation, checks, and scope correction |
| `construction.py` | Exact construction from the 13-variable stable model |
| `verify_symbolic.py` | Primary exact symbolic verifier |
| `export_certificate.py` | Deterministic sparse-certificate exporter |
| `verify_exported_stdlib.py` | Dependency-free exact rational checker |
| `verify_exported_node.mjs` | Independent Node.js/BigInt exact checker |
| `output/sic21_sparse.json` | 72-term machine-readable witness and collision |
| `render_paper.py` | Reproducible PDF build |
| `requirements.txt` | Pinned SymPy dependency |

The construction imports the certified stable reduction in
`../discovery_03_small_vanishing_counterexample/`. That dependency is retained
in the same repository and is covered by its own exact checks.
