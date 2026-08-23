# Theorem-to-certificate crosswalk

**FINAL OUTCOME A — PROVED.**  Active manuscript: *Strong Tree-Childness Is
a Sharp Generic-Identifiability Boundary for Level-2 Jukes--Cantor Networks*.

Release gates: `V111`, `V112`, `V113`, `V114`, `V115`.

Status: **v1.1.7 certificate bundle prepared; Zenodo DOI
`10.5281/zenodo.22064121`**

The authoritative computer-assisted proof object is
`stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz`. All paths below are
relative to its extracted root. The broad development snapshot and historical
audit reports are provenance only and are not theorem dependencies.

| Article claim | Minimal exact evidence | Replay |
|---|---|---|
| Fixed mixed-graph convention, primitive supports, cut recovery, and full incidence-scaling bridge fibre | `primary/certificates/{core_universe,support_universe}.json`, `reviews/root_probe/`, `independent/bridge_cut/` | `bash verify.sh full` |
| Theorem 6.3, including every three-/four-outgoing relation and its restoration/probe closure | `atlas/ATLAS_EVIDENCE_BINDINGS.jsonl.gz` binds every theorem row to `atlas/{RESTORATION,DIRECT_ANCHOR}_CLOSURE_BINDINGS.jsonl.gz`; restoration terminals in turn bind to `atlas/COMPACT_PATH_CLOSURE_BINDINGS.jsonl.gz`, whose records name every packed path, transport, witness, and polynomial used | `bash verify.sh full` and `bash verify.sh regenerate-all` |
| Deterministic graph-to-certificate regeneration | primitive inputs and compilers under `primary/`; frozen streams under `primary/certificates/` | `verifiers/regenerate_load_bearing.py`, invoked twice by `regenerate-all` |
| Ordinary triangle common germ | `primary/certificates/jc_triangle_redirection_active.json`, `reviews/triangle_redirection_cleanroom/` | `bash verify.sh full` |
| Omega and Theta sharpness families | `sharpness/omega/` and `sharpness/theta/` in the extracted certificate bundle | `bash verify.sh full` |
| Bundle integrity, relation and closure totality, and mutation sensitivity | `ACTIVE_MANIFEST.json`, `SHA256SUMS`, all four `atlas/*BINDINGS.jsonl.gz` streams, `expected_outputs/`, `verifiers/package_mutation_tests.py` | all three modes |

The authoritative evidence map has 10,466 three-outgoing records and 192
four-outgoing survivor records.  Every record binds its decorated graphs,
direction, certificate, transport when applicable, and verifier.  The CSV is
a checked human-readable projection.  The archive excludes referee prose,
research logs, superseded claims, manuscripts, and release-engineering
workspaces.

## Explicit exclusions

No active theorem uses a reciprocal-only bridge chart, a hidden cleanup-fibre
rooting convention, a weak-class gadget as a move in the strong class,
target-only counts, equality of complete stochastic images under ordinary
triangle redirection, physical bridge-parameter recovery, or K2P/K3P claims.
