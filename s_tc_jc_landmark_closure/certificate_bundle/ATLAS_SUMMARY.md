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

`atlas/ATLAS_INDEX.csv.gz` has one row per canonical relation. Its separate
base and closure fields make the restoration/probe dependency explicit:
direct strict/equality rows terminate at the base certificate, while pending
rows name both their raw-to-restoration transport and the exact closure
certificate/verifier.
