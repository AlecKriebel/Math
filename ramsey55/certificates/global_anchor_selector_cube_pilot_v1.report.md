# Proof-free selector-cube pilot for global degrees 18, 19, and 20

Date: 2026-07-23 (America/Los_Angeles)

## Outcome and evidence boundary

**FULL BOUNDED SCREEN COMPLETED; NO SOLVE CLAIM.** All 429 exact
anchor-matrix selector cubes (143 in each normalized root-degree branch 18,
19, and 20) were presented to MapleChrono with a 5,000-conflict budget per
cube. Every call returned `BUDGET_EXHAUSTED`. There was no SAT model, no
solver-reported UNSAT cube, and no proof trace.

Therefore this pilot finds no order-43 Ramsey graph, excludes no cube or
degree branch, and changes no Ramsey bound.

The engineering conclusion is nevertheless clear: fixing one canonical
4-by-4 anchor matrix does **not** reveal a population of individually trivial
cubes at this budget. In particular, the data do not support launching a
large proof bundle on the assumption that most of these 429 cubes will close
within 5,000 conflicts.

## Frozen design

The pilot used the three previously generated and independently checked lean
selector-union formulas. For cube index `i`, the only solve assumption was
the positive selector variable `65404+i`. The checked selector implication
then fixes exactly the 16 matrix literals belonging to the corresponding
historical cube record. The independent pilot checker reconstructed:

- all 35,714 feasible 4-by-4 matrices;
- their exact 143-orbit quotient under independent row and column
  permutations;
- every degree-branch, anchor, and matrix assumption;
- all 429 historical full-cube assumption hashes; and
- the exact mapping from cube index to selector variable.

One solver instance was persistent across the 143 calls in a degree branch,
so sound learned clauses were shared within that branch. A fresh solver was
loaded for each new degree. Thus the per-call conflict deltas are exact, but
later calls are not fresh-solver timing samples. This reuse favored finding
easy later cubes; none resolved.

The plan was frozen before launch at:

```text
results/benchmark_plans/global_anchor_selector_cube_pilot_v1.json
SHA-256 4e67e6708c5dfc255224feaf9ba0b4e67cd2182d895ebccef3e9dd829ce62c3d
```

The plan bound the exact union CNF, cover plan, plan check, materialized-CNF
check, worker, checker, test, solver version, C++ verifier, schedule hash,
budget, and resource gates. Proof logging was disabled.

## Results

| normalized root degree | cubes | budget exhausted | SAT | observed UNSAT, unproved | conflicts | solver CPU s |
|---:|---:|---:|---:|---:|---:|---:|
| 18 | 143 | 143 | 0 | 0 | 715,104 | 57.211 |
| 19 | 143 | 143 | 0 | 0 | 715,110 | 66.860 |
| 20 | 143 | 143 | 0 | 0 | 715,095 | 91.772 |
| **total** | **429** | **429** | **0** | **0** | **2,145,309** | **215.843** |

The small excess over exactly 5,000 conflicts in some calls (maximum 5,005)
is the solver's bounded-call accounting granularity. It did not change any
status.

The complete run took 281.920 wall-clock seconds, including input hashing,
three formula loads, garbage collection, and atomic progress records. Peak
resident memory was 836,354,048 bytes, below the frozen 3,000,000,000-byte
cap. The launch preflight observed 8,098,390,016 free bytes, above the
4,000,000,000-byte disk gate, and found no active `drat-trim` proof
conversion. No proof file was created.

For comparison, the earlier unsplit degree-19 and degree-20 union pilots both
exhausted 50,000 conflicts. The present result shows that tenfold smaller
per-cube calls also exhaust uniformly. This is evidence against a
low-conflict easy-cube explanation for the union behavior, not evidence of
UNSAT.

The full result is:

```text
results/global_exact/global_anchor_selector_cube_pilot_v1.json
SHA-256 3567a678597edf52a4a60adbac82c83ab89e765438401de6c230bf2ba3622c9a
```

## Independent result audit

The checker imported neither the pilot worker nor the anchor-cover
generators. It found:

```text
independent feasible matrix count: 35,714
independent canonical matrix count: 143
independent scheduled cube count: 429
input errors: 0
cover-plan errors: 0
union-check errors: 0
record errors: 0
aggregate errors: 0
valid: true
```

The checked result record is:

```text
results/verification/global_anchor_selector_cube_pilot_v1.check.json
SHA-256 60ad7f784b2a4b7eb2b9b9b1b234f7f4db0e4f896a6b568608b96dea3082f384
```

The exceptional SAT path, though unused, is fail-closed: it retains the
solver model, streams it through every exact union-CNF clause, decodes all
903 primary edge variables, counts all five-subsets independently in Python,
and invokes the separate C++ bitset verifier. The result checker independently
replays the retained model and graph again.

## Reproduction

Run the five focused tests:

```bash
PYTHONPATH=/private/tmp/ramsey55-pysat.4YSXId:src:verify \
  /opt/homebrew/opt/python@3.11/bin/python3.11 \
  tests/global_anchor_cube_pilot_tests.py -v
```

Run the frozen pilot from the repository root:

```bash
PYTHONPATH=/private/tmp/ramsey55-pysat.4YSXId:src \
  /opt/homebrew/opt/python@3.11/bin/python3.11 -u \
  src/global_anchor_cube_pilot.py \
  --plan results/benchmark_plans/global_anchor_selector_cube_pilot_v1.json \
  --result results/global_exact/global_anchor_selector_cube_pilot_v1.json
```

Independently audit coverage and results:

```bash
PYTHONPATH=src /opt/homebrew/opt/python@3.11/bin/python3.11 \
  verify/global_anchor_cube_pilot_check.py \
  --plan results/benchmark_plans/global_anchor_selector_cube_pilot_v1.json \
  --result results/global_exact/global_anchor_selector_cube_pilot_v1.json \
  --output \
    results/verification/global_anchor_selector_cube_pilot_v1.check.json
```
