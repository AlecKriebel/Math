# Residual exact-completion and core-radius certificates

Date: 2026-07-23

## Scope

These are local, fixed-structure conclusions.  They do **not** prove that a
\((5,5;43)\)-graph does not exist and do not change the bound on \(R(5,5)\).

The pinned solving chain is:

1. Python 3.11.8 and `python-sat` 1.9.dev7 `Glucose3`;
2. an explicit ASCII DRAT trace;
3. `drat-trim` commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`,
   which also emits LRAT;
4. the separately compiled `lrat-check`.

The workflow reports `SAT`, `CERTIFIED_UNSAT`, or `TIMEOUT` distinctly.
Candidate assumptions are materialized as sorted unit clauses in a new CNF,
so proof checking never depends on opaque solver assumptions.

## Constructive-candidate exact completion

The read-only candidate
`results/best_candidates/incident_lns_seed_20260726.g6` has two forbidden
five-sets and preserves all 666 edges outside the 237-variable incident
boundary.  Its two violated clauses involve nine variables.  Fixing the
other 228 candidate values leaves those nine free.

The resulting formula is UNSAT by input unit propagation.  `drat-trim`
accepted the empty DRAT trace (the augmented input already propagates to a
conflict), emitted LRAT, and `lrat-check` accepted that LRAT.  The independent
completion checker also:

- reconstructed all base clauses and 228 unit clauses exactly;
- independently checked the fixed boundary;
- reran both proof checkers;
- returned `valid=true`.

This certificate applies only to that nine-variable completion neighborhood.

## Full 237-variable fixed boundary

**CERTIFIED:** the independently reconstructed 237-variable formula
`residual_lns_incident_six.cnf` is UNSAT.  Every edge incident to one of
`{3,4,7,38,41,42}` is free; the other 666 edges equal the base graph.

Glucose3 solved it in 0.283349 seconds internal time:

- 10,035 conflicts;
- 14,400 decisions;
- 189,745 propagations;
- 13,828 DRAT records.

The 1,070,726-byte DRAT trace was accepted by `drat-trim`: 6,335 input
clauses and 5,810 of 10,036 lemmas were in the core, with 185,659 resolution
steps and zero RAT lemmas.  The generated 1,891,741-byte LRAT was accepted by
`lrat-check`.

## Aggregate core Hamming radius six

**CERTIFIED:** no satisfying assignment exists when:

- all 237 incident-boundary edges remain unrestricted; and
- at most six of the other 666 edge values differ from the base graph.

The aggregate formula has:

- 903 primary edge variables;
- 1,925,196 direct Ramsey clauses;
- 4,641 sequential-counter auxiliaries;
- 9,276 counter clauses;
- 5,544 variables and 1,934,472 clauses total.

The 88,318,842-byte generated CNF has SHA-256
`34183fc806ec83136001f49c3373b770484168d70f846ba9b08de5fbe2bfea7d`.
It was generated in `/tmp` and is deterministic, so it is not retained or
duplicated in the repository. The independent checker reconstructed every
clause in 4.03 seconds and returned `valid=true`.
The hardened generator and checker fail closed on a mismatched base graph,
order, file hash, noncanonical/duplicate edges, or any set other than the
exact 237-edge incident boundary.

Glucose3 returned UNSAT with 436,104 conflicts.  The raw DRAT trace was
347,262,937 bytes with SHA-256
`1bfc9fc9f8df0b042a3df72e0c422b84c914eb46cc216811b6c9abc147c67e26`.
`drat-trim` accepted it with:

- 33,548 of 1,934,472 input clauses in the core;
- 221,705 of 436,105 lemmas in the core;
- 169,233,890 resolution steps;
- zero RAT lemmas.

The resulting 1,424,628,404-byte LRAT, SHA-256
`638e5deb58354931725ef00f8bf670f47eb3cc656fde8b6b4c036cb1bbc8b2f6`,
was accepted by `lrat-check`.

To stay below repository file limits, only the Zstandard-compressed DRAT is
retained.  It is 68,702,255 bytes with SHA-256
`0fbd59057b014662a8aa1030c18616836ccfa98734a36bcd11a9195c4042b418`.
`zstd -t` passed, and its decompressed stream reproduced the raw DRAT hash.
The checked LRAT is deterministically regenerated from that proof.

## Reproduction

```text
python3 src/core_radius_cnf.py \
  --base-graph results/best_candidates/exoo_seed_20260724.g6 \
  --boundary-metadata certificates/residual_lns_incident_six.metadata.json \
  --radius 6 \
  --output /tmp/ramsey55_core_radius6.cnf \
  --metadata certificates/core_radius6.metadata.json

PYTHONPATH=verify python3 verify/core_radius_cnf_check.py \
  --cnf /tmp/ramsey55_core_radius6.cnf \
  --graph results/best_candidates/exoo_seed_20260724.g6 \
  --boundary-metadata certificates/residual_lns_incident_six.metadata.json \
  --generation-metadata certificates/core_radius6.metadata.json \
  --radius 6

zstd -dc certificates/core_radius6_glucose3.drat.zst \
  > /tmp/core_radius6_glucose3.drat

/tmp/ramsey55-drat-trim.x3nb3p/src/drat-trim \
  /tmp/ramsey55_core_radius6.cnf \
  /tmp/core_radius6_glucose3.drat -I -L /tmp/core_radius6_glucose3.lrat

/tmp/ramsey55-drat-trim.x3nb3p/src/lrat-check \
  /tmp/ramsey55_core_radius6.cnf /tmp/core_radius6_glucose3.lrat
```

Focused tests:

```text
python3 tests/residual_completion_tests.py -v
python3 tests/core_radius_cnf_tests.py -v
```

All seven residual-completion tests and all four core-radius tests passed.
They include SAT, proof-checked UNSAT, strict subprocess timeout, rejected
tampered proof, exhaustive small counter semantics, exact production counts,
and adversarial boundary metadata.

## Source and retained-artifact SHA-256

| File | SHA-256 |
|---|---|
| `src/residual_completion.py` | `b8117443d48a2d51c528fe126166455ed4f62e0caf2efd6d9dc86dbc6a75c2db` |
| `src/residual_completion_glucose.py` | `d8ce8f16146069ba438130f48e2e21babdd7bdc7a6c963e74114ae9c54029006` |
| `src/certify_cnf_glucose.py` | `4adfcbfe33c99813ef67f4746b507e06d7d74ff64788de7e9838295ebc48eaba` |
| `verify/residual_completion_check.py` | `d7c1215d57a65e84ba0ab790c41ffe98c3d12da725320556a1f018a53300dea0` |
| `tests/residual_completion_tests.py` | `dbebf6b3dc54dc74fdd6839e722c9e0331d28fa57f7831b636afa5246409aed1` |
| `src/core_radius_cnf.py` | `4900f6fd0b9adcb3558ef9c8b161637608ce33e6fefcd528d5be96583a6a0a22` |
| `verify/core_radius_cnf_check.py` | `cbaf55f63595de2e3b4f9252e7a490bb397364e0c70429dd5ab0c53988c1144d` |
| `tests/core_radius_cnf_tests.py` | `52eeaad128a773445b94508b0bbb619adf8a63c245036158360c11f5f1e2f3fb` |
| `certificates/residual_lns_incident_six_glucose3.drat` | `e7c8da6188c304e79ca2ca9bc077d261ed7536b3e4b3ec1181bebb006547c654` |
| `certificates/residual_lns_incident_six_glucose3.lrat` | `592d2ce4df932c6332af5b2523b4fbaaf6d394d14aa639c74b303f1bf1195209` |
| `certificates/core_radius6_glucose3.drat.zst` | `0fbd59057b014662a8aa1030c18616836ccfa98734a36bcd11a9195c4042b418` |
