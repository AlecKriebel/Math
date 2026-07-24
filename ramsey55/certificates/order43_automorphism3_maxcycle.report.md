# Order-3 maximal-cycle branch at order 43

Evidence status: **EXACT ENCODING VERIFIED; CONSTRUCTIVE SEARCH FOUND NO
WITNESS; CLASS UNRESOLVED**

This branch concerns graphs admitting an automorphism with cycle structure
\(3^{14}1^1\). It does not cover arbitrary order-43 graphs.

## Exact orbit formula

The prescribed action partitions all 903 unordered vertex pairs into 301
edge orbits of size three. Exhaustively mapping all
\(\binom{43}{5}=962{,}598\) five-sets gives 320,593 distinct orbit-variable
signatures and 641,186 positive/negative Ramsey clauses.

The canonical DIMACS byte stream was hashed in memory rather than retained:

`2cb249c2d09d00bd199be27711fc344873785b9e9756dc1cafad8f756084a5e5`.

An independent checker reconstructed the edge partition algebraically from
the three group elements, regenerated every five-set signature, matched the
formula hash and signature histogram, and returned `valid: true`.

- independent formula audit SHA-256:
  `4cbf533e91341743c13392f69957917639e6d86bf8c0e62c41e50458b6ee38a1`
- search source SHA-256:
  `0d3167c2396db371d1d207013e5397bdf74002d994a56529f7233d10928b6dd0`
- independent audit source SHA-256:
  `569bd1e4e0d72613a6609b66a5a89e8cbbbd3ae3093b59a4ed1b20a48905106f`
- structural test source SHA-256:
  `2b3444d79df4f61a9763ee7888b7279c33bfba6f477f97ea9446caf17d1f2419`

All five structural tests pass.

## Complete fixed-vertex normalization

The fixed vertex has constant adjacency on each moved 3-cycle, so its degree
is divisible by three. The theorem-implied order-43 interval
\(18\le d(v)\le24\) leaves degrees 18, 21, and 24, corresponding to 6, 7,
and 8 neighboring cycles. Complementation exchanges the 6- and 8-cycle
cases and fixes the 7-cycle case. The \(S_{14}\) action permuting moved
cycles then normalizes the neighbors to the first \(t\) cycles.

Consequently, the exact cases \(t=6\) and \(t=7\) cover the entire
\(3^{14}1^1\) class up to complementation and relabeling.

## Side-gluing reduction

For a fixed \(t\), the neighbor side is \(K_4\)-free and \(I_5\)-free. The
nonneighbor side is \(K_5\)-free and \(I_4\)-free, so it can be represented
as the complement of another \(K_4\)-free, \(I_5\)-free side model.

The independently checked \(C_3\)-invariant side formulas are:

| Moved cycles | Vertices | Variables | \(K_4\) signatures | \(I_5\) signatures | Clauses |
|---:|---:|---:|---:|---:|---:|
| 6 | 18 | 51 | 990 | 2,841 | 3,831 |
| 7 | 21 | 70 | 1,953 | 6,762 | 8,715 |
| 8 | 24 | 92 | 3,486 | 14,140 | 17,626 |

Fixing the vertex incidence and both side models leaves only cross-cycle
variables:

| Case | Fixed variables | Free cross variables |
|---:|---:|---:|
| \(t=6\) | 157 | 144 |
| \(t=7\) | 154 | 147 |

Side pools were diversified both by fresh SAT models and by exact
normalizer relabelings: cycle permutations, independent phase shifts, and
the common generator inversion.

## Constructive portfolio

The proof-free, in-memory run used seed 20260727.

1. Raw exact formula: CaDiCaL 1.9.5, Glucose4, and MapleChrono each ran two
   phase-diversified attempts on both \(t\) cases, with 100,000 conflicts per
   cube. All 12 attempts exhausted their budgets.
2. Side gluing: pools of 64, 128, and 64 models for the 6-, 7-, and 8-cycle
   side formulas were used.
3. Three fresh-pair stages ran 256 pairs per \(t\) at 5,000 conflicts under
   CaDiCaL, 128 pairs per \(t\) at 20,000 conflicts under Glucose4, and 64
   pairs per \(t\) at 50,000 conflicts under MapleChrono.

This is 448 distinct pairs in each normalized case, 896 total. Of these, 94
returned solver UNSAT within their budgets and 802 exhausted the budget.
The raw and gluing stages used 15,655,882 conflicts in total. The retained
summary is 427,468 bytes and has SHA-256:

`2de0ceec127b1d66eed4b835ebe709cf7caa7c493a1adef8e421e938b6da7810`.

An independent result checker reconstructed the complete raw and gluing
schedules, verified all 896 pair identities were unique, checked the
fixed/free-variable counts and evidence labels, bound the run to the
independently audited formula, and confirmed that no candidate artifact was
emitted. It returned `valid: true`.

- result-check JSON SHA-256:
  `eeb15bf74ebcb1565bb64620272acf69537ce2f4036d58e8d900eb31bc361aef`
- result-check source SHA-256:
  `c58c40919451c761ba566c2bc874b6dc97cfe8804e767a77af6fb052cb76bb24`

## Claim boundary

No SAT model was found. None of the negative outcomes has a retained proof,
so none certifies nonexistence—not even for its individual cube. The
\(3^{14}1^1\) automorphism class remains unresolved, and this work does not
change the bound \(43\le R(5,5)\le46\).

No CNF, DRAT, or LRAT artifact was written. Any proof-producing follow-up
must first pass a separately frozen proof-size and free-space gate.
