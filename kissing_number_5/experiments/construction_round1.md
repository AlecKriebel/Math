# Construction search round 1 — numerical evidence only

Date: 2026-07-23

## Status banner

Except for the fixed-\(D_5\) saturation lemma linked below, **every result in
this note is NUMERICAL EVIDENCE ONLY**. No configuration of 41, 42, 43, or
44 points with maximal inner product at most \(1/2\) was found. Solver
termination, printed decimal coordinates, and near-equality of constraints
are not certificates of feasibility or nonexistence.

The one proved result from this track is
[`d5_saturation.md`](../proofs/d5_saturation.md): keeping the 40 normalized
\(D_5\) roots fixed, every possible added unit vector has inner product at
least \(\sqrt{2/5}>1/2\) with one of them.

## Reproducibility environment

The soft-maximum and four-configuration surgery runs reported here used:

- macOS on arm64;
- Python 3.14.6;
- NumPy 2.5.1;
- SciPy 1.18.0;
- NetworkX 3.6.1, used only for contact-graph diagnostics.

The independently implemented hybrid search in `random_codes/` used Python
3.9.6, NumPy 1.24.3, and SciPy 1.10.1; its own README records that
environment separately. Floating-point last digits can depend on the BLAS
and optimizer versions.

A matching temporary environment can be created with:

```sh
python3 -m venv /tmp/kissing5-construction-venv
/tmp/kissing5-construction-venv/bin/pip install \
  numpy==2.5.1 scipy==1.18.0 networkx==3.6.1
```

Random generators were NumPy `default_rng` instances. Seed formulas and
individual winning indices are recorded below.

The executable construction-search package is documented in
[`random_codes/README.md`](random_codes/README.md), and its complete seed
ledger and replay commands are in
[`random_codes/RESULTS.md`](random_codes/RESULTS.md). The principal
user-facing analysis command is:

```sh
kissing_number_5/.venv/bin/python \
  kissing_number_5/experiments/random_codes/analyze_refine_coordinates.py \
  kissing_number_5/experiments/input/spherical_codes_5_41.txt \
  --refine direct-slsqp \
  --output-json kissing_number_5/experiments/output/n41_direct_slsqp.json
```

## Public numerical benchmarks

The plain-text coordinate files were retrieved from the
[Spherical Codes table](https://www.spherical-codes.org/) at
`https://www.spherical-codes.org/data/5/N`. Each whitespace-delimited row is
a point, with its five coordinates separated by commas.

| \(N\) | Maximum inner product recomputed in binary64 | Active pairs within \(10^{-7}\) of the maximum | SHA-256 of raw download |
|---:|---:|---:|---|
| 41 | 0.5149946525121659 | 153 | `c54b38d8216bf76a79c57119fc46245811188e1de05c840c68a33cec9b7fe1b0` |
| 42 | 0.5182411558622615 | 169 | `f941a50369a6a26ab4785216a9c5d544a861b7bd9546f0ac1e246d848281f865` |
| 43 | 0.5247096018290188 | 169 | `bf6414a336bf9205c3ec0115f6f289ac2e40b57f9fac5d7f4223083665e9a768` |
| 44 | 0.5274577123235276 | 190 | `d7ac84e95fa5d34b358da80920922f52ead9d932fec19250ac176d277f8999c2` |

The largest observed squared-norm error in these files was
\(4.45\cdot10^{-16}\). This is a floating-point diagnostic, not an exact
normalization proof.

The hashes can be reproduced without storing the files:

```sh
for n in 41 42 43 44; do
  curl -fsSL "https://www.spherical-codes.org/data/5/$n" |
    shasum -a 256
done
```

The maxima and contact counts can be recomputed using only the Python
standard library:

```sh
python3 - <<'PY'
import urllib.request

for n in range(41, 45):
    raw = urllib.request.urlopen(
        f"https://www.spherical-codes.org/data/5/{n}"
    ).read().decode()
    x = [[float(t) for t in row.split(",")] for row in raw.split()]
    values = [
        (sum(a*b for a, b in zip(x[i], x[j])), i, j)
        for i in range(n) for j in range(i+1, n)
    ]
    mu = max(value for value, _, _ in values)
    edges = [(i, j) for value, i, j in values if value > mu-1e-7]
    print(n, repr(mu), len(edges))
PY
```

### Contact and Gram diagnostics

For \(N=41\), the 153-pair threshold graph consists of a connected
35-vertex core and six isolated points. Its degree multiset is

\[
0^6,\quad 8^{18},\quad 9^{10},\quad 10^6,\quad 12^1.
\]

Thus the six points are numerical “rattlers” relative to the maximum-contact
graph; this observation does not show that they can be moved so as to
improve the objective.

The five nonzero Gram eigenvalues, equivalently the eigenvalues of
\(X^{\mathsf T}X\), were:

| \(N\) | Nonzero Gram eigenvalues |
|---:|---|
| 41 | 7.89209914, 7.97875519, 7.97875519, 8.18617329, 8.96421719 |
| 42 | 7.89872347, 8.01212937, 8.49118704, 8.68033850, 8.91762161 |
| 43 | 8.39791854, 8.41114832, 8.41211367, 8.41211367, 9.36670580 |
| 44 | 8.59143245, 8.63764921, 8.63764921, 9.05949682, 9.07377231 |

These are ordinary floating-point eigensolver outputs. In particular, they
are not interval enclosures or rank certificates.

## Independent asymmetric soft-maximum sweep

For normalized rows \(x_i\), the discovery objective was

\[
F_\beta(X)=\frac1\beta
\log\sum_{i<j}\exp\!\bigl(\beta\langle x_i,x_j\rangle\bigr).
\]

Rows were renormalized inside the objective, its analytic gradient was
passed to L-BFGS-B, and \(\beta\) was increased by continuation. Direct
high-\(\beta\) starts were included to avoid forcing every run into the same
low-\(\beta\) energy basin.

The base seed was `202607232000`; start \(k\) for size \(N\) used

```text
seed = 202607232000 + 10000*N + k.
```

There were 500 starts for \(N=41\) and 150 starts for each of
\(N=42,43,44\). According to `k % 6`, the initial beta schedule was one of

```text
[100]
[300]
[1000]
[100, 300]
[300, 1000]
[1000, 3000]
```

and every schedule was followed by `[3000, 10000, 30000]`. Each continuation
stage used SciPy L-BFGS-B with at most 1500 iterations, analytic gradients,
`ftol=2e-14`, `gtol=1e-9`, `maxls=50`, and `maxcor=20`.

| \(N\) | Best fresh-run maximum | Winning \(k\) | Public benchmark beaten? |
|---:|---:|---:|:---:|
| 41 | 0.5155878486743447 | 139 | no |
| 42 | 0.5201135512636789 | 90 | no |
| 43 | 0.5262791664210132 | 135 | no |
| 44 | 0.5274907221444453 | 125 | no |

An independent hybrid search using nonsmooth hinge penalties, insertion/deletion
cascades, and epigraph SLSQP obtained, before importing the public files,

```text
N=41  0.515557051615
N=42  0.518241352984
N=43  0.525896549470
N=44  0.527471192536
```

The independent \(N=42\) run nearly rediscovered the public benchmark.
None of these decimals proves a lower bound on the optimal maximal inner
product.

## Epigraph refinement and benchmark perturbations

Local minimax refinement used the nonconvex epigraph formulation

\[
\begin{aligned}
\text{minimize}\quad &t,\\
\text{subject to}\quad
&\lVert x_i\rVert^2=1 &&(1\leq i\leq N),\\
&t-\langle x_i,x_j\rangle\geq0 &&(i<j),
\end{aligned}
\]

with analytic constraint Jacobians and SciPy SLSQP. Direct refinement of the
public files returned the tabulated objectives to the displayed precision.

For \(N=41\), 96 tangent/core/rattler continuation perturbations and 32
direct SLSQP perturbations at scales from \(10^{-8}\) through \(0.02\) all
returned to a maximum of approximately `0.514994652512`. Thirty-two analogous
local perturbations at each of \(N=42,43,44\) also returned to the public
benchmark basin. This establishes only numerical local persistence.

## Surgery around exact 40-point configurations

Four exact 40-point inputs were used: \(D_5\), Leech's \(L_5\), Szöllősi's
\(Q_5\), and Cohn–Rajagopal's \(R_5\). Their rational unnormalized
coordinates were independently enumerated from Table 2.2 of
[Cohn–Rajagopal, *Variations on five-dimensional sphere packings*,
arXiv:2412.00937v3](https://arxiv.org/abs/2412.00937). A direct numerical
pair count reproduced 240 pairs with normalized inner product \(1/2\) for
each input. The exact validity of these four inputs comes from their listed
rational coordinates, not from that floating-point diagnostic.

One random point was appended, all 41 points were optionally perturbed, and
the epigraph problem above was locally minimized. The NumPy generator seeds
were `2026072344` for \(D_5,L_5,Q_5\) and `2026072401` for \(R_5\), with
noise scales selected from

```text
0, 1e-4, 0.003, 0.03, 0.1, 0.3.
```

The best maxima observed in these small targeted sweeps were:

| Starting configuration | Best local maximum | Active pairs within \(10^{-6}\), when recorded |
|:---|---:|---:|
| \(D_5\) plus one | 0.52206926099694 | 190 |
| \(L_5\) plus one | 0.52139894574727 | not recorded |
| \(Q_5\) plus one | 0.52085614418627 | 190 |
| \(R_5\) plus one | 0.52085614418625 | 190 |

A limited \(D_5\) deletion/replacement experiment removed \(k\) roots,
inserted \(k+1\) random points, and optimized all 41 points. For
\(k=0,1,2,3\), the best maxima were approximately

```text
0.52206926, 0.51796033, 0.52543856, 0.52218359.
```

This deletion sweep was deliberately stopped after the first few values of
\(k\), because direct asymmetric searches and the public benchmark were
already better. It is not an exhaustive surgery result.

## Fixed-code hole search

For each exact 40-point input \(C\), 1000 SLSQP starts numerically minimized

\[
h_C(y)=\max_{x\in C}\langle x,y\rangle
\quad\text{subject to}\quad \lVert y\rVert=1.
\]

The generator seed was `2026072355` for the sequential \(D_5,L_5,Q_5\)
runs and `2026072399` for \(R_5\). All four returned

\[
\min h_C(y)\approx0.6324555320336759=\sqrt{\frac25}.
\]

For \(D_5\), this value and global optimality are proved exactly in
[`d5_saturation.md`](../proofs/d5_saturation.md). For \(L_5,Q_5,R_5\), the
same value is **NUMERICAL EVIDENCE ONLY** in this round. A floating-point
convex-hull calculation found supporting-facet distances consistent with
the value, but no exact facet-completeness certificate was produced.

## Exact verification commands

The proved \(D_5\) result is checked independently of NumPy and SciPy:

```sh
python3 kissing_number_5/verifiers/verify_d5_saturation.py
python3 -m unittest discover \
  -s kissing_number_5/tests -p 'test_d5_saturation.py'
```

The verifier uses integer root coordinates and `fractions.Fraction`; it does
not read solver output.

## Construction conclusion

No run produced even an approximate 41–44 point code with maximum inner
product at most \(1/2\). The nearest 41-point numerical input examined was
the public `N=41` file with maximum approximately `0.5149946525121659`, a
gap of about `0.0149946525121659` above the kissing threshold.

This search failure is not an upper bound. Its appropriate claim status is
**NUMERICAL EVIDENCE ONLY**.
