# Exact free-group computation supporting Kourovka21.127 research

**Outcome: `scl_F(a,c)(acacAcACCC)=1/2`, with a small exact primal/dual certificate.** This is an auxiliary free-group calculation, not a resolution of21.127 or a claim of a new free-group scl theorem. Uppercase denotes inverse. All turn indices below are zero based, with turn i immediately after letter i.

## Input and normalization

The word is

`h = a c a c A c A C C C`.

It has length10, exponent sums zero, and is cyclically reduced. We use `[x,y]=xyx^{-1}y^{-1}`. The turn graph has an edge `i→j` precisely when `h[i]^{-1}=h[(j+1) mod10]`; its dual edge is `(j+1)→(i−1)`, with indices modulo10.

Brady–Clay–Forester, Lemma3, gives

`scl(h) = inf (10/4 − D/(2n))`,

where a taut admissible surface has total positive boundary degree n and D disk pieces, whose boundaries follow embedded directed turn circuits. Each turn occurs n times across those circuits. Conversely, nonnegative integer circuit multiplicities satisfying equality of every dual pair of edge counts give an admissible surface (Proposition6).

Primary reference: N.Brady, M.Clay, M.Forester, *Turn graphs and extremal surfaces in free groups*, Contemp.Math.560(2011),171–178, [arXiv1104.5221v1](https://arxiv.org/abs/1104.5221v1), especially Sections4–5, Lemma3, Lemma5 and Proposition6. The objective here is taken directly from equation(3), not from the inconsistent plus sign displayed in the final proof's A(u) formula in the cached preprint.

## Upper certificate

Take one copy of each of the four directed circuits

- `(0,3,7)`;
- `(1,6)`;
- `(2,5,8)`;
- `(4,9)`.

They visit each turn exactly once, so n=1. Their edges pair under duality as follows; all other edge counts are zero:

| Edge | Dual edge |
|---|---|
| `0→3` | `4→9` |
| `3→7` | `8→2` |
| `7→0` | `1→6` |
| `6→1` | `2→5` |
| `5→8` | `9→4` |

There are four disk pieces and five bands; hence χ=4−5=−1, giving scl≤1/2. The disk adjacency graph is connected, and the total boundary degree1 means there is one boundary component. Thus this is a once-punctured torus.

There is also a direct algebraic upper certificate:

`h = [acacA,cACA]`.

Free reduction of the right side yields the displayed ten-letter word. This identity independently realizes a once-punctured torus bounding h.

## Lower certificate

Let `K={0,1,2,4}`. After deleting these four turn vertices, the only edges left are

`3→6`, `3→7`, `3→8`, `5→6`, `5→7`, `5→8`, `6→9`.

This is a directed acyclic graph; `(3,5,6,7,8,9)` is a topological order. Consequently **every directed turn circuit meets K**. For any taut admissible surface, each disk piece consumes at least one occurrence of a turn in K. There are exactly4n such turn occurrences, so D≤4n. Therefore

`scl(h) ≥ 10/4 − 4n/(2n) = 1/2`.

Together with the upper certificate this proves the exact value. This lower argument does not require enumerating the circuits or trusting an LP solver.

## Rational LP artifact and reproducibility

For completeness, `compute_certificate.py` reconstructs all133 embedded directed circuits,26 directed edges and13 dual edge pairs. The primal LP maximizes `sum u_j` with all10 turn-visit sums1, all13 dual edge balances0, and nonnegative u. The certificate has four nonzero primal coordinates, all1. The dual has vertex weights1 on K and0 elsewhere, and all dual-edge-balance weights0. Every dual column inequality is at least1, and both objective values equal4.

Run from any working directory:

`python3 /absolute/path/to/free_scl_certificate/compute_certificate.py`

Verification uses only Python's standard library, exact integers and `fractions.Fraction`. It reconstructs the matrix rather than trusting `model.json`, verifies all primal equalities and nonnegativity, checks all133 dual inequalities and objective equality, checks the acyclic cut complement, and free-reduces the explicit commutator identity. `VERIFICATION.json` records the successful run.

The optional `--solve` mode uses SymPy1.14.0's exact rational simplex to regenerate the certificate. SymPy is not required to check it. One separate dual solve with split unrestricted variables encountered SymPy's oscillation exception; no result relies on that failed attempt. The simultaneous primal/dual output from the exact primal simplex passed independent Fraction checks. No third-party software is vendored in this folder.

## Scope for the parent research

If a group homomorphism maps two boundary conjugacy classes to h, monotonicity supplies a lower bound from the corresponding free-group chain. Since that image chain is `h+h=2h`, its scl is **1**, by homogeneity. The single-word value1/2 therefore does not establish a lower bound2 for the two-boundary chain, nor prove sharpness of a degree-one surface giving upper bound2. Any such stronger claim needs additional information from the original group.

Completion estimate: **100% of this exact auxiliary computation; 21.127 remains unresolved by this package.** No publication or priority claim is made.
