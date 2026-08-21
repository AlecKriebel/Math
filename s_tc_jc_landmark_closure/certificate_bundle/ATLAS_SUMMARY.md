# Finite atlas summary

The counts below are deterministic checksums of theorem-derived finite
universes, not assumptions used to prove exhaustiveness.

The cut theorem has a separate finite handoff.  The human run-order argument
reduces every arbitrary two-colour segment word to either a direct three-run
path obstruction or the five-word palette checked on primitive graphs.  The
standalone reduction certificate covers all 808,642 balanced four-through-
eight-port words; a separately implemented rooted-graph/switching replay
checks 379,742 valid reduced-palette presentations and finds no survivor.

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
| Four-outgoing direct quotient classes | 3 |
| Four-outgoing nonretaining quotient classes | 57 |
| Four-outgoing restoration states | 2,106 |
| One-port direct-anchor probes | 2,642 |
| Two-port direct-anchor probes | 18,224 |
| Three-outgoing compact probes | 101,148 |
| Four-outgoing compact probes | 168,582 |

Every strict relation is bound to an exact polynomial, flattening minor, or
Bernstein sign certificate regenerated from its graph.  Equality terminals
are accepted only after independent labelled mixed-graph canonicalization as
an isomorphism or ordinary triangle redirection.

`atlas/ATLAS_EVIDENCE_BINDINGS.jsonl.gz` has one authoritative row per
three-outgoing canonical directed relation and one row per four-outgoing
normalized survivor presentation.  In the three-outgoing universe,
`relation_id` is the canonical decorated-relation identifier.  In the
four-outgoing universe, `relation_id` identifies one of the 192 normalized
survivor presentations, while
`evidence.presentation.canonical_relation_sha256` records the further mixed-
relation quotient.  The 18 direct presentations form 3 direct canonical
classes; the 42 selected-incoming and 132 marginalized nonretaining
presentations form 57 nonretaining canonical classes.  Presentation
multiplicities and transports are retained and verified.

Every row binds the source and target decorated graphs, direction,
disposition, exact base evidence, and—when required—the raw-to-restoration
transport and exact closure evidence.  Three auxiliary content-addressed
streams make this binding transitive and inspectable:

- `COMPACT_PATH_CLOSURE_BINDINGS.jsonl.gz`: 276 path-bound equality
  terminals (144 three-outgoing and 132 four-outgoing), with every packed
  transport, witness, and polynomial reference;
- `RESTORATION_CLOSURE_BINDINGS.jsonl.gz`: 5,476 roots (5,344 and 132), with
  all 68,584 and 2,106 reachable restoration states and their terminal
  evidence; and
- `DIRECT_ANCHOR_CLOSURE_BINDINGS.jsonl.gz`: all 62 direct residual anchors,
  binding 2,642 one-port and 18,224 two-port relations, their graphs, and all
  witnesses.

The complete map and all three closure streams are regenerated from the
underlying graph and certificate records during every verification mode.

`atlas/ATLAS_INDEX.csv.gz` is a compact human-readable projection of those
records.  It is useful for navigation but is not a substitute for the exact
JSONL evidence map.  The verifier requires the CSV to be the exact projection
of the regenerated evidence records.
