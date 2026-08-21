# Finite atlas summary

The counts below are deterministic checksums of theorem-derived finite
universes, not assumptions used to prove exhaustiveness.

| Family | Exact count |
|---|---:|
| Raw three-outgoing decorated presentations | 10,826 |
| Canonical three-outgoing directed relations | 10,466 |
| Strict three-outgoing relations | 5,284 |
| Raw three-outgoing restoration roots | 5,344 |
| Three-outgoing restoration states | 68,584 |
| Three-outgoing isomorphism / ordinary-T terminals | 120 / 24 |
| Direct residual anchors | 62 |
| Four-outgoing completion records | 6,138 |
| Four-outgoing raw survivors | 192 |
| Four-outgoing direct / rooting-duplicate / restoration-root survivors | 18 / 42 / 132 |
| Four-outgoing restoration states | 2,106 |
| One-port direct-anchor probes | 2,642 |
| Two-port direct-anchor probes | 18,224 |
| Three-outgoing compact probes | 101,148 |
| Four-outgoing compact probes | 168,582 |

Every strict relation is bound to an exact polynomial, flattening minor, or
Bernstein sign certificate regenerated from its graph.  Equality terminals
are accepted only after independent labelled mixed-graph canonicalization as
an isomorphism or ordinary triangle redirection.

`atlas/ATLAS_EVIDENCE_BINDINGS.jsonl.gz` has one authoritative record per
canonical relation.  Each record binds the source and target decorated
graphs, direction, disposition, exact base evidence, and—when required—the
raw-to-restoration transport and exact closure evidence.  The complete map is
regenerated from the frozen graph and certificate streams during every
verification mode.

`atlas/ATLAS_INDEX.csv.gz` is a compact human-readable projection of those
records.  It is useful for navigation but is not a substitute for the exact
JSONL evidence map.  The verifier requires the CSV to be the exact projection
of the regenerated evidence records.
