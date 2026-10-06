# PR107 / 30003997: independent reproduction and adversarial report

**Mathematical result: verified within the candidate's exact stated scope.
Computational package: correction required for Python optimization safety.**
The frozen proof at PR head `cc2ae01897135b35bee135917819e782a220f2c1`
has SHA-256 `2c219bf80ad4bbba75f8c70169b26b7e9b11b6f5e1742543f25d9cb0d0c5ebe8`.
No mathematical counterexample or proof gap was identified. Both original
checkers silently discard their validation gates under Python `-O`, yet report
`PASS` with unchanged assertion counters. This is a checker defect, independently
demonstrated on known-false controls; it does not refute the written reduction.
Historical novelty remains unestablished. This is verification of the completed
original turn-1/5 candidate, with zero additional central proof-search turns.

## Exact hypothesis and independent method

The hypothesis is that fixed-root spanning out-arborescence optimization with
a separate arc-cost vector for each nonroot **destination** is strongly NP-hard,
even for the candidate's four-layer, adjacent-layer, simple reachable DAG with
indegree at most three and dense binary cost vectors. The restricted threshold-
zero decision problem is NP-complete. Adding one to every vector entry preserves
hardness using costs in `{1,2}` and threshold `4n+3m`.

Before reading `verify.py`, archived verification, the original independent
checker, or the old review, I read `PROOF.md`, the frozen source record and the
retrieved original OWR text around Problem 2. I implemented and froze
`independent_initial.py`. `INITIAL_CONTROL_PIN.json` records the timestamp
`2026-10-06T04:08:38.426887+00:00` and its SHA-256
`cc4f781470177b980022b6dd49bea4b14ac8abd908c87e1926e868df3c0568c4`.
The old review was read only afterward.

The independent model builds the full dense destination-by-arc cost table,
enumerates **every** edge subset of size `|V|-1`, and checks root indegree,
nonroot indegrees and root reachability by a generic graph traversal. Only then
does it compute the paths and sum each destination's own table row along its
path. It does not choose trees using assignments or allowed parent products.
Generic controls include a disconnected directed cycle, an incoming-root arc,
a singleton root, and an arbitrary graph with three valid rooted trees. These
check that the graph recognizer does not assume the candidate's layers.

## Actual finite evidence

| Check | Cases / subsets / feasible trees | Result |
|---|---:|---|
| Independent initial generic enumeration | 645 / 583,319 / 8,988 | Pass in normal and `-O` modes; result JSON byte-identical |
| Original author checker | 449 / parent enumeration / 12,696 | Normal stdout reproduces frozen 946-byte JSON exactly; 57,135 enforced assertion checks |
| Original independent checker | 114 / 222,114 / 1,674 | Normal stdout reproduces frozen 1,190-byte JSON exactly; 14,397 enforced assertion checks |
| Larger constructed witnesses | 36, with `n=3,7,16,40`, `m=1,5,25` | Feasibility, actual cost and offset pass; not global optimum enumeration |
| Further preprocessing | 33 per-assignment checks and 2 empty-clause controls | Pass in normal and `-O` modes |

The 645 independent instances comprise all ordered lists of zero through three
clauses from the eight normalized one-/two-variable clauses (585 cases), ten
boundary/adversarial cases, and 50 reproducible seeded three-variable cases.
Cases cover contradictory units, the four-clause unsatisfiable two-variable
formula, whole-clause repetition, repeated literal occurrences, tautologies,
empty conjunctions, empty clauses, unused variables, and all cost offsets.
Every feasible enumerated tree has the claimed structure; no noncanonical
arborescence was found. Structural tree counts were subsequently checked against
`2**n * product(clause_lengths)` on all 645 cases, without using that formula
to select subsets or compute optima.

An explicit 16-variable unused-variable control verifies that all selector and
variable vertices remain spanned, and that the same root-to-false-selector arc
costs one for a clause destination but zero for the selector destination. This
guards the exact source objective against accidental common-cost substitution.

## Demonstrated false positives and minimal repair

`guard_probe.py` executes the unchanged original checker, computes the actual
optimum **one** for `(x) AND (NOT x)`, and submits the false condition that this
optimum is zero to that checker's gate. Both original normal executions reject
with exit 1. Both original `-O` executions accept with exit 0 and emit
`ACCEPTED_KNOWN_FALSE`. Their original suites also print the same `PASS` JSON
under `-O`, including assertion counters, although validation asserts have been
compiled away. Therefore byte-exact replay under `-O` is not evidence that the
reported checks executed.

`corrupt_cost_probe.py` makes a stronger false-model test: after loading an
unchanged original copy it erases the destination costs **in memory** only for
the contradictory-unit instance. The resulting computed optimum zero differs
from the correct optimum one. The original normal checkers reject this error;
the original `-O` checkers both accept it and emit `ACCEPTED_CORRUPT_MODEL`.
Frozen original files were never edited.

The author's separate cycle assert is exercised by `cycle_guard_probe.py` on a
self-parent map. The original normal implementation raises immediately. Under
`-O`, it fails to reject before a bounded 0.1-second alarm (exit 2), showing that
the cycle guard was bypassed. This map is not a valid tree in the candidate's
DAG; it is a software guard test, not a mathematical counterexample.

The minimal suggested own-copy repairs replace each `assert` with an explicit
`if not ...: raise AssertionError(...)`. The author's cycle check uses an
explicit membership test and exception. Exact patches and pins are:

| Artifact | SHA-256 |
|---|---|
| `author_suggested_repair/verify.py` | `e97081e21df60b3e06af907788a03fc280d0506839c452d78dc50cdca59565da` |
| `independent_suggested_repair/independent_checks.py` | `e2ff01b552ff827eb94c3747fc73178150b63f1b6657d82daac5c06a90cb4c08` |
| `author_suggested_repair.diff` | `a80db3ce83a5e961aadf7f1f357d6d33efc13a4554d1a55f85606d5700892ca7` |
| `independent_suggested_repair.diff` | `446f1dd4e65b80a069657152806204823fd9f9e442ca7fa0fe8eab9653e342b4` |

Both repaired suites pass under normal Python and `-O`. All repaired known-false
and corrupted-cost controls reject under both modes; the repaired author cycle
control also rejects immediately in both modes. The independent initial checker
uses explicit `require` exceptions and likewise rejects its false and corrupted-
cost controls under both modes.

`REPAIRED_RESULT_COMPARISON.json` compares every original/repaired result. The
author's JSON differs **only** in the intentional `checker_sha256` value. The
old independent checker result remains byte-exact; it has no checker SHA field.
No mathematical test or expected count was weakened by either patch. An updated
package should regenerate the author's checker-SHA-bearing receipt and retain
the immutable original history, rather than relabel the old receipt as current.

## Arbitrary-size argument and scope

The general argument is deductive, not an extrapolation from small cases.
Every selector's unique incoming edge forces its root arc. Every variable
vertex's single incoming tree edge chooses one globally shared truth value.
Every clause's single parent identifies one literal. Since all edges advance
one layer, these are all possible spanning arborescences, and every such choice
is feasible. A clause destination's only nonzero path entry is its first edge;
it is one precisely when the chosen literal is false. Fixing an assignment makes
clause parents independent. Its minimum tree cost is therefore exactly its
number of unsatisfied clauses, proving

`min_T C(T) = min_assignment(number of unsatisfied clauses)`.

This supplies both directions of the SAT reduction for arbitrary formula size.
Deleting tautologies and duplicate literal occurrences preserves the formula's
semantics; whole-clause repetition is retained. An empty clause maps to the
fixed no instance `(x) AND (NOT x)`; an empty or all-tautological conjunction maps
to the fixed yes instance `(x)`. Both fixed graphs have all four layers and meet
the promised degree, reachability, simplicity and cost conditions.

The graph has `1+3n+m` vertices and at most `4n+3m` edges. Its dense table is
polynomial in formula length, with entries zero or one. A certificate is checked
by indegree/reachability tests and exact root-path summation, which is polynomial
also for rational binary input costs. The restricted problem is therefore in NP,
and SAT hardness uses bounded numbers, giving strong NP-hardness. Every tree's
sum of root-path lengths is `2n + 2n + 3m`; adding one to all dense entries adds
exactly `4n+3m` independently of the choices. This proves the positive-cost
threshold version. No unsupported translation to Wong's extended formulation
is needed.

The strongest verified theorem is the written binary-cost restricted
NP-completeness theorem and its positive-cost strong-hardness consequence for
the exact fixed-root destination-specific source Problem 2. This review does
not establish novelty, an approximation threshold, a result for source Problem 1,
or a separate result for duplicate record 30003998. The finite computations
support the mechanism and challenge implementation errors; they alone do not
prove NP-hardness.

## Reproduction and receipts

`FROZEN_REPLAY_COPY_MANIFEST.json` proves own replay copies are byte-identical to
archived inputs. `REPLAY_COMPARISON.json` records original stdout equality.
`actual_runs/*/started.json` and `receipt.json` preserve actual command argv, cwd,
child PID, UTC start/completion, exit code, and binary stdout/stderr byte counts,
line counts and SHA-256. All failing controls and outputs are retained. Run
indices group the replay, false-model and cycle experiments. The runtime is
standard-library `/opt/homebrew/bin/python3`; version details are in the verdict.
`MANIFEST.json` pins source inputs and final audit artifacts. Original frozen
bytes remain unchanged, and no Git, PR, queue, tracker, editor, Zenodo or external
outreach operation was performed by this subtask.
