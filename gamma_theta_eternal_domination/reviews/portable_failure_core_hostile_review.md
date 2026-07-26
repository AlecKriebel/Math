# Independent hostile review: portable failure cores

## Verdict

**ACCEPT** as of 2026-07-25.

No critical, high, or medium mathematical or certificate defect remains in
the frozen artifacts below.  The universal statements are sound in the
standard one-guard-moves model, the finite core and occurrence claims are
independently replayable, and the one-vertex unmarked-class measurement is
conservatively labelled `OBSERVED`.

This review was performed separately from the author implementation.  The
reviewer did not edit the six reviewed artifacts.

## Frozen artifact identities

| artifact | SHA-256 |
|---|---|
| `math/lemmas/portable_failure_core.md` | `131b88a889a39fa9dc5c9a5e024eb5d6f3fb6fd83e44da6b4eb4a473e4434115` |
| `src/search/portable_failure_core.py` | `f053efc7d2b19ad1d6238f0bd4cd882df1860162ddae3f0ccc2116304e035a9f` |
| `tests/test_portable_failure_core.py` | `63930bc666a1a45c6c64f09c1eb1baf7dfcc35adf4840cb8b41eba964503df48` |
| `certificates/portable_failure_cores.json` | `e6f1abaf9e77f9b0bc223f3c3e46551243ececb951f3c9e5c20a5ca08c53cd6f` |
| `results/portable_failure_core_measurement.json` | `210ad8e551ddbbdc1624c7338da7e317cafcae1bdf21d2d19742b46c6afa5b39` |
| `results/portable_failure_core_J_extensions.csv` | `71884fe0fca10c9f6d2a7a4157a62551a8a8e0eff7d26cb0c6c6dd02a3f57142` |

The certificate and result manifests reproduce the current runtime,
supporting-artifact, input, certificate, extension-table, and pinned
`labelg` hashes.

## Mathematical audit

The independent-set forcing proof is valid without a maximality or
\(\alpha(G)=k\) hypothesis.  Repeatedly attacking a vertex of
\(S-D\) is always an unoccupied attack.  Independence prevents a guard
already in \(S\) from responding, so exactly one guard moves from outside
\(S\) into \(S\) and \(|D\cap S|\) increases by one.

The induced-core lifting is sound.  All configurations, attacks, and moved
guards stay in the induced vertex set \(W\).  For \(D\subseteq W\) and
\(r\in W-D\),

\[
 D\cap N_G(r)=D\cap N_{G[W]}(r),
\]

so the response branches are identical.  A terminal witness in \(W\)
remains undominated, while a state that fails to dominate a vertex outside
\(W\) can be terminated earlier.  This preserves unoccupied attacks,
exactly one edge move, and exhaustive defender branching.

The ranked-DAG condition is sufficient: every internal state dominates, its
attack is unoccupied, the response list is exactly the sorted set of
adjacent occupied guards, each listed successor is the required one-guard
swap, and every nonterminal arc strictly lowers a positive integer rank.
Terminal witnesses are checked against the full closed-neighborhood
condition.  Hence every defensive path terminates.

The note correctly identifies the forcing statement as prior Claim C-010
and the parameter-level induced monotonicity as prior Claim C-005.  It does
not claim a new monotonicity theorem.  A draft ambiguity about merging the
same configuration at different horizons was corrected: the frozen note
now requires normalization by exact deletion rank before repeated
configurations are merged into the state-indexed DAG.

## Independent finite replay

A fresh standard-library replay imported no campaign module.  It decoded the
raw Graph6 bits into adjacency sets, enumerated subsets directly, recomputed
the online kernels with `frozenset` configurations, and replayed every
ranked-DAG response.  It obtained:

| core | \(\gamma\) | \(\alpha\) | three-guard kernel sizes | four-guard kernel sizes |
|---|---:|---:|---|---|
| `J@l|bfNuVK_` | 3 | 3 | `110,105,100,88,64,10,0` | `311,311` |
| `Kun_w{vRrblV` | 3 | 3 | `147,143,136,128,119,93,28,0` | `461,461` |

Thus the empty three-guard and nonempty stable four-guard kernels certify
\(\gamma^\infty=4\) for both cores.  The replay also confirmed all 8 attack
states and 9 distinct terminal states for \(J\), and all 9 attack states and
11 distinct terminal states for \(Q\).

The following explicit maps were checked on all 55 unordered pairs.  Each
map sends base vertices \(0,\ldots,10\) of \(J\) to the listed host vertices
after deleting the named host vertex.

| host Graph6 | delete | base-to-host map |
|---|---:|---|
| `K]?H[|]nj}\k` | 4 | `0,1,5,6,9,8,7,10,3,2,11` |
| `KoDbMyz}@}ju` | 3 | `0,4,5,6,2,10,1,11,9,8,7` |
| `KoYu~_VMyzLf` | 8 | `0,3,4,11,2,9,1,10,7,5,6` |
| `Kp]e~_VDyZlf` | 8 | `0,3,10,11,5,9,1,4,6,2,7` |
| ``Krqb}iw[W^`~`` | 10 | `4,5,3,9,8,2,1,7,0,11,6` |
| ``KrrDthx\_^`~`` | 10 | `4,5,2,3,8,7,6,9,11,1,0` |

The same fresh implementation reconstructed the fixed 526 distinct source
graphs, exhaustively tested deletion of each possible host vertex, and
recomputed the three-guard kernel rank for every induced-\(J\) occurrence.
It found exactly 37 host graphs, with earliest-rank histogram
`{3: 30, 5: 7}`.

## Executed checks and hostile mutations

From the campaign root:

```text
PYTHONPATH=src PYTHONWARNINGS=error \
python3 -m search.portable_failure_core audit
```

passed with certificate, CSV, and result hashes
`e6f1abaf...`, `71884fe0...`, and `210ad8e5...`.

```text
PYTHONPATH=src PYTHONWARNINGS=error \
python3 -m unittest tests.test_portable_failure_core -q
```

reported `Ran 8 tests ... OK`.

The tests reject a missing response branch, an occupied attack, an invalid
terminal witness, a nondecreasing rank, a wrong root rank, a changed
population summary, surplus CSV fields, noncanonical CSV bytes, and altered
result limitations.

During review, two low-level acceptance gaps were found and repaired before
this verdict:

1. surplus CSV fields were previously ignored by `csv.DictReader`; and
2. the result verifier previously did not compare the top-level limitations
   text with the deterministic payload.

The frozen checker rejects both mutations and requires exact canonical CSV
bytes.

## Classification boundary

`CERTIFIED-FINITE` is justified for the two core profiles, the ranked DAGs,
the six explicit embeddings, and the exact 37-of-526 occurrence statement.
The population claim is only about the fixed, hash-bound derived population.

The reported 623 one-vertex keys remain appropriately `OBSERVED`: the audit
covers all 2,047 nonempty labelled neighborhoods, verifies every
raw-to-key isomorphism and every recorded parameter, and pins `labelg`, but
does not independently prove that distinct canonical keys are
nonisomorphic.  No finite claim here resolves the \(\gamma\)-\(\theta\)
conjecture or raises the global exhaustive order bound.
