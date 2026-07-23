# Hadamard order-668 search manifest

## Human-readable artifacts

| File | Purpose |
|---|---|
| `README.md` | Search overview, scope, and verification commands |
| `RESUME.md` | Compact restart point, checkpoint hashes, and memory rules |
| `PRIORITY_AUDIT.md` | Provisional novelty and publication audit |
| `RESEARCH_LOG.md` | Chronological derivation and computational record |
| `local_obstructions_668.tex` | Narrow research manuscript |
| `output/pdf/local_obstructions_668.pdf` | Rendered manuscript |

## Exact verification

| File or directory | Purpose |
|---|---|
| `verify_seed.py` | Reconstructs the published seed and full modular array |
| `verify_fixed_q_obstruction.py` | Checks the fixed-`q` parity telescope and reduction to `TU(41)` |
| `verify_variable_q_seed_quad_radius.py` | Dependency-free margin-plus-quad dynamic program |
| `verify_variable_q_seed_frontier_artifacts.py` | Audits radius-16 and distance-17 frontier artifacts |
| `verify_variable_q_seed_shell18_artifacts.py` | Audits the layered distance-18 artifacts and decoded survivors |
| `proof_certificates/` | Four independently replayed representative DRAT leaves plus 12/12 pinned positive root witnesses; the 1,296-leaf UNSAT gate remains incomplete |
| `tu41_certificate/` | Completed independent `TU(41)` enumeration: 461/461 shards, 57,543,021 nodes, zero solutions |
| `render_paper.py` | Reproducible Tectonic build |

The fixed-`q` endpoint now has a modern independent exhaustive enumeration.
The paper nevertheless remains a research draft until the radius-18
certificate gate is complete, the inaccessible literature has been checked
through lawful public access, and independent expert review has occurred.
