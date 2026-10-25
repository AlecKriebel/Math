# Active non-four anchor-universe derivation

This directory derives the designated model-independent starting-universe
rows for the K3P probe argument.  It derives the tree, cycle, and theta2
anchor seeds without reading the frozen 176-row contract, the frozen theta2
closure, or the frozen cycle anchor list.

Run, from the project root:

```sh
.venv/bin/python -B anchor_universe/generate_non_four_anchor_universe.py
.venv/bin/python -B anchor_universe/verify_non_four_anchor_universe.py
.venv/bin/python -B anchor_universe/test_non_four_anchor_mutations.py
.venv/bin/python -B anchor_universe/verify_marginalized_theta_one_port_reconciliation.py
.venv/bin/python -B anchor_universe/verify_complete_anchor_crosswalk.py
```

The producer uses the active K3P atlas only for graph construction and exact
mixed-graph operations.  It does not compile or evaluate a model map.  The
verifier is a separate literal implementation and imports neither the
producer nor either submitted atlas.  The final crosswalk reads the legacy
theta/cycle files only to expand their opaque locator IDs after the independent
133-row universe is fixed.  It then joins that universe to the already active
four-port verification.  The crosswalk now also replays the literal graph
grammar over all 144 equality rows in the exhaustive four-port ledger and
transports every fixed-full restoration request into the active one- and
two-port ledgers.  The frozen contract's 43 four-port rows are designated
serialization rows (26 direct generators and 17 physical descendants), not
an assertion that there are only 43 rooted equality presentations.  The
crosswalk finally checks the complete 176-row contract.

Expected non-four census:

| origin | isomorphic | triangle | total |
|---|---:|---:|---:|
| three-port tree | 1 | 0 | 1 |
| three-port cycle | 8 | 16 | 24 |
| restored cycle | 12 | 0 | 12 |
| theta2 five-port | 24 | 0 | 24 |
| theta2 six-port | 40 | 0 | 40 |
| theta2 seven-port | 32 | 0 | 32 |
| **non-four** | **117** | **16** | **133** |

The active four-port route contributes 26 isomorphisms and 17 triangles, so
the complete census is 176 = 143 + 33.

The independent four-port descendant crosswalk has the following exact
graph-only census:

The 144 raw rows occupy 93 active map classes (24 isomorphic and 69
ordinary-triangle); forgetting map-rank data and quotienting the ordered
source/target presentations by exact labelled semi-directed graph-pair
isomorphism leaves nine parent classes.

| layer | raw requests | existing ledger rows | equality outcomes |
|---|---:|---:|---:|
| four-port equality parents | 144 | 9 ordered graph-pair classes represented by the 26 direct rows | 30 isomorphic + 114 triangle |
| first restoration | 1,260 | 161 one-port rows | 15 isomorphic + 24 triangle |
| second restoration from 12 continuations | 96 | 64 two-port rows | 0 |

The first layer has 27 fully physical five-port equality terminals.  Nineteen
are presentations of the 11 ordered graph-pair classes represented by the 17
restored contract rows.  The other eight presentations form four additional
triangle pair classes, but all eight are already one-port descendants of
`four:raw154873` (four one-port rows, each reached twice).  The remaining 12
equality children each have one dummy role; all 96 second restorations are
non-equalities already classified by the two-port ledger.  Thus all 1,356
restoration requests are mapped and none is an uncovered seed obligation.
The 16-case anchor mutation gate preserves the twelve non-four/runtime attacks
and adds four coherently rebound semantic attacks: raw equality-parent
omission, used one-port equality corruption, used two-port status corruption,
and extra-terminal identity corruption.  It also retains the earlier nested
raw-ledger binding attack.

This is a seed-universe statement, not the claim that no other raw rooted
presentation can become graph-isomorphic after arbitrary port insertion.  In
particular, 176 theta2 comparisons (44 per source) become abstractly
isomorphic only after deleting a marginalized incoming role.  They are
excluded by the incoming-selected fixed-full-parent convention.  Exhaustive
restoration produces 424 fully physical paths (56/176/192 at depths one/two/
three).  The independent verifier gives a per-path root-movement certificate:
after removing the restored incoming label, every path restricts to exactly
one canonical theta seed class and a valid transported one-port attachment
site.  The counts are 56/176/192 into the five-/six-/seven-port seed families,
with zero unmatched cases.  The terminal reconciliation additionally maps
these transports bijectively onto 66 existing `isomorphic` one-port ledger
rows and 66 stored relation classes.  Thus these are downstream one-port
presentations, not missing seed obligations.
