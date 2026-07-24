# A centered all-harmonic pair/triple barrier

## Status

This is an exact **relaxation barrier**, not a spherical code and not an
upper-bound proof.

There is a positive rational pair/triple pseudodistribution of cardinality
41 on the quarter grid
\[
E=\{-1,-3/4,-1/2,-1/4,0,1/4,1/2\}
\]
that simultaneously satisfies:

1. the exact fixed-cardinality masses and all pair/triple marginal
   identities;
2. the centered first moment
   \[
   1+\sum_{q\in E}\alpha_q q=0;
   \]
3. the two exact design kernels forced by centering;
4. every ordinary dimension-five Gegenbauer inequality, at every degree;
5. every full-radial Bachoc--Vallentin matrix inequality, at every harmonic
   degree;
6. the aggregate robust-depth pair consequences
   \(\alpha((-\infty,-1/300))>7\) and
   \(\alpha((1/300,\infty))>6\); and
7. all 18 corrected exact-stratum common-pair capacity rows and both
   pointwise weighted-capacity rows available on this grid; and
8. all 27 sharp low-harmonic rank inequalities used in the continuous
   rank-aware search.

Thus imposing centering on the complete two/three-point formulation recorded
in this project still does not exclude 41 points.  A successful centered-case
argument must retain a four-point/common-source condition or stronger
rank-five information.

The exact weights are in
[`../certificates/centered_quarter_bv_pseudodistribution.json`](../certificates/centered_quarter_bv_pseudodistribution.json).
The all-degree thresholds and source hash are in
[`../certificates/centered_quarter_bv_all_harmonics.json`](../certificates/centered_quarter_bv_all_harmonics.json).
The standard-library verifier is
[`../verifiers/verify_centered_quarter_bv_all_harmonics.py`](../verifiers/verify_centered_quarter_bv_all_harmonics.py).

## 1. Exact finite data

Let \(\alpha_q>0\) be the normalized off-diagonal pair masses and let
\(\nu_{uvw}>0\) be the unordered triple-orbit masses in the certificate.
All 51 unordered triples on \(E\) whose \(3\)-by-\(3\) Gram determinant is
nonnegative occur with positive mass.  Exact rational arithmetic verifies
\[
\sum_q\alpha_q=40,\qquad
\sum_{u,v,w}\nu_{uvw}=40\cdot39,
\]
and, for every \(q\in E\),
\[
\sum_{u,v,w}\frac{\#\{q\text{ in }(u,v,w)\}}3\,\nu_{uvw}
=39\alpha_q.
\]
It also verifies
\[
1+\sum_q\alpha_q q=0.                                  \tag{1}
\]
Equation (1) is the pair-distribution shadow of \(G{\bf1}=0\).

The exact robust pair masses are
\[
\sum_{q<-1/300}\alpha_q
=\frac{1653481733059617708857}{115151400000000000000}>7,
\]
\[
\sum_{q>1/300}\alpha_q
=\frac{1474966314278593738993}{115151400000000000000}>6.
\]
These are necessary aggregate consequences of the exact enlarged-cap
theorem at a code vertex.

The verifier also enumerates the corrected common-pair projection
inequalities directly from the 51 triple types.  All 18 contiguous
nonpositive base-stratum rows and both pointwise weighted rows hold exactly.
The minimum stratum slack is zero only in the vacuous \(-1\)-base,
capacity-zero row; the weighted rows have strict rational slack.

## 2. The two forced centered kernels

Let \(W_k\) denote the full-radial Bachoc--Vallentin coefficient matrix in
the normalization of
[`fixed41_three_point_formulation.md`](fixed41_three_point_formulation.md).
At \(k=0\), the usual fixed-cardinality kernel is
\[
\kappa=(-1/40,\ldots,-1/40,1).
\]
Centering supplies the independent radial kernel
\[
c=(-1,-3/4,-1/2,-1/4,0,1/4,1/2,1).
\]
The verifier reconstructs \(W_0\) directly from the stored weights and
checks
\[
W_0\kappa=W_0c=0.                                     \tag{2}
\]
A complementary \(6\)-by-\(6\) principal submatrix has six positive exact
\(LDL^{\mathsf T}\) pivots.  Hence
\[
W_0\succeq0,\qquad \operatorname{rank}W_0=6.           \tag{3}
\]

For \(k=1\), the endpoint rows vanish and the active \(6\)-by-\(6\) block
has the exact constant-radial kernel:
\[
W_1{\bf1}=0.                                           \tag{4}
\]
Its leading \(5\)-by-\(5\) principal submatrix has five positive exact
pivots, so
\[
W_1\succeq0,\qquad \operatorname{rank}W_1=5.           \tag{5}
\]
The rationalization program was constrained to preserve (2) and (4)
exactly.  The verifier reconstructs them independently and does not trust
the floating discovery output.

## 3. Every higher harmonic degree

For \(k>0\), both endpoint rows \(u=-1\) and \(u=1\) vanish.  On the six
active nodes, divide row and column \(u\) by
\((1-u^2)^{\lfloor k/2\rfloor}\).  This is a positive diagonal congruence.
For an ordered support triple, set
\[
A=(1-u^2)(1-v^2),\qquad w=t-uv,\qquad \Delta=A-w^2.
\]
The normalized even and odd transverse kernels are rational and obey
\[
R_{k+2}=\frac{(k+1)(4w^2/A-2)R_k-(k-1)R_{k-2}}{k+3}.
\]
The verifier uses this recurrence with `Fraction` arithmetic.

For every \(2\le k\le552\), all six exact
\(LDL^{\mathsf T}\) pivots are positive.  The smallest finite pivot occurs
at \(k=3\), and is still strictly positive.

For the infinite tail, separate determinant-zero atoms from atoms with
\(\Delta>0\).  The even and odd boundary-limit matrices \(L_0,L_1\) are
positive definite by exact \(LDL^{\mathsf T}\).  The standard
\(S^3\) identity
\[
P_k^{(4)}(\cos\theta)
=\frac{\sin((k+1)\theta)}{(k+1)\sin\theta}
\]
gives an entrywise \(1/(k+1)\) bound for the interior remainder.  Exact
inversion and rational square-root majorants give
\[
C_0=
\frac{66053135204248927472034833389609}
     {119580986212604966280137284552}<553,
\]
\[
C_1=
\frac{697150454786030978563662596848}
     {1495891333869514210542202953}<553.
\]
Therefore
\(\|L_p^{-1}(W_k-L_p)\|_\infty<1\) for every \(k\ge553\), proving
\[
\boxed{W_k\succeq0\quad\text{for every }k\ge0.}        \tag{6}
\]
The only singular degrees are the exactly explained design degrees zero and
one.

## 4. Every ordinary two-point degree

The verifier checks exactly that
\[
1+\sum_q\alpha_qP_k^{(5)}(q)>0
\]
for \(2\le k\le121\), while degree one is exactly zero by (1).  The smallest
positive finite moment occurs at degree three.

For the six interior nodes, rational upper bounds for
\((1-q^2)^{-3/2}\) are
\[
4,\ 8/5,\ 6/5,\ 1,\ 6/5,\ 8/5.
\]
Using the normalized Gegenbauer integral estimate
\[
|P_k^{(5)}(q)|
<\frac{31}{5[k(1-q^2)]^{3/2}},
\]
the verifier computes an exact normalized tail constant \(C\) satisfying
\[
C^2<122^3.
\]
The endpoint contribution at \(-1\) then dominates the entire interior
tail for every \(k\ge122\), for both parities.  Thus every ordinary
two-point moment is nonnegative, with equality only at the forced centered
degree one.

## 5. Sharp harmonic-rank audit

For each of the 27 stored linear combinations of \(H_0,H_1,H_2,H_3\), the
verifier reconstructs the centered trace variance \(V\), centered third
trace \(D\), and the appropriate harmonic rank \(r\).  It proves exactly
\[
(r-2)^2V^3-r(r-1)D^2>0.                               \tag{7}
\]
The smallest residual occurs for \((H_0+5H_1)/6\) and equals
\[
\frac{
55167524940721706879162142630825892057376871095010136958418083
}{
145896583472409513607299072000000000000000000000000000000000000
}>0.
\]
Consequently the witness survives the sharp nonlinear rank cuts that reject
the older all-harmonic pseudodistribution.

## 6. Local Gram-PSD four- and five-point extensions

The same triangle marginal has an exact symmetric extension to individual
four-point Gram matrices.  Enumerate the six edge labels of a \(K_4\) from
the seven-node grid.  Exact principal-minor tests leave 25,808 labeled
Gram-PSD patterns and 1,375 distinct multisets of four triangular face
types.

The certificate
[`../certificates/centered_quarter_k4_extension.json`](../certificates/centered_quarter_k4_extension.json)
stores 51 of those face-count types with positive rational weights.  Their
weights sum to one, their uniform triangular-face marginal is exactly
\(\nu/1560\), and their uniform edge marginal is exactly \(\alpha/40\).
Every stored \(4\)-by-\(4\) Gram matrix is checked by all principal minors.
The independent verifier also re-enumerates all 25,808 feasible labeled
patterns, so the finite support is not trusted blindly.

Separately, the same pair/triple witness admits a local extension one level
further.  The certificate
[`../certificates/centered_quarter_k5_extension.json`](../certificates/centered_quarter_k5_extension.json)
stores 51 positive rational atoms, each representing an \(S_5\)-orbit of a
quarter-grid edge labeling of \(K_5\).  Averaging each representative
uniformly over all vertex permutations gives a genuinely symmetric
distribution.  Its weights sum to one, its uniform triangular-face marginal
is exactly \(\nu/1560\), and its uniform edge marginal is exactly
\(\alpha/40\).  For each atom the verifier checks every principal minor of
orders one through five, so each stored matrix is a genuine PSD Gram matrix
of five unit vectors with all off-diagonal entries at most \(1/2\).
The \(K_4\)-face marginal induced by this \(K_5\) mixture is itself a valid
local \(K_4\) extension, but it is not the particular 51-atom \(K_4\)
mixture stored in the preceding certificate.

The discovery enumerator found 12,087,822 labeled locally PSD \(K_5\)
patterns and 105,930 triangle-count vectors, then a floating LP selected the
51 stored atoms.  None of those enumeration or solver claims is needed for
the exact existence assertion: the standard-library verifier checks the
stored atoms, positive rational weights, and all marginal equations directly.

These extensions prove that the centered witness is not rejected merely by
demanding a symmetric distribution of locally realizable Gram matrices on
every subset of at most five vertices.  They are **not** second- or
higher-level Lasserre certificates: they do not verify the larger
positive-semidefinite moment matrices that couple overlapping subsets
through a common global source.  Six vertices are the first purely local
level at which the ambient rank is restrictive, since every genuine
\(6\)-by-\(6\) Gram matrix in \(\mathbb R^5\) must have determinant zero.

That first rank-sensitive level also remains feasible after changing the
intermediate \(K_5\) marginal.  The certificate
[`../experiments/centered_quarter_k6_rank/direct_k6_triangle_extension.json`](../experiments/centered_quarter_k6_rank/direct_k6_triangle_extension.json)
stores 51 positive rational \(K_6\) atoms.  Every principal minor is
nonnegative, every full determinant is zero, and every atom has a positive
principal minor of order five.  Hence every atom is PSD of rank exactly
five.  Uniform \(S_6\)-averaging gives edge marginal \(\alpha/40\) and
triangle marginal \(\nu/1560\) exactly.

There is an instructive support warning.  The particular sparse \(K_5\)
mixture above does not itself extend to \(K_6\): an exhaustive exact
48,594-case gluing leaves four face-count columns, and the one-coordinate
Farkas vector \(-e_1\) separates their cone from its exact \(K_5\) target.
This does not contradict the direct \(K_6\) certificate, whose induced
\(K_5\) marginal is different.  The proof and both independent verifiers are
in
[`../experiments/centered_quarter_k6_rank/`](../experiments/centered_quarter_k6_rank/).

The same phenomenon repeats at seven vertices.  The frozen 51-orbit \(K_6\)
distribution has no \(K_7\) lift with that exact \(K_6\)-face marginal:
complete exact gluing checks 277,410 last-edge cases and finds no supported
pattern.  However, the direct certificate in
[`../experiments/centered_quarter_k6_rank/k7/`](../experiments/centered_quarter_k6_rank/k7/)
stores a different positive 51-atom \(K_7\) mixture.  Every atom is PSD of
rank exactly five, and its uniform edge and triangle marginals are again
\(\alpha/40\) and \(\nu/1560\).  Thus the support-specific obstruction does
not survive reoptimization of the intermediate \(K_6\) marginal.

## 7. What this does and does not prove

The certificate proves exact feasibility of a centered, fixed-cardinality
pair/triple relaxation.  It does **not** supply 41 vectors, a PSD
\(41\)-by-\(41\) Gram matrix, or rank five.  It does not supply a consistent
eight-point distribution or any unstated row-by-row realization condition.
The local \(K_6\) and \(K_7\) rank claims mean only that each atom separately
has rank five; they supply no compatibility between overlapping subsets.

In particular, this result refutes the route

> centering + every ordinary two-point inequality + every full-radial
> three-point inequality + the recorded low-harmonic sharp rank cuts
> immediately contradict cardinality 41.

It does not refute a proof using four-point common-source consistency,
all-distinct cycle traces, or a genuinely complete rank-five realization
condition.

## 8. Reproduction and dependency map

From the project root:

```sh
python3 verifiers/verify_centered_quarter_bv_all_harmonics.py
python3 verifiers/verify_centered_quarter_k4_extension.py
python3 verifiers/verify_centered_quarter_k5_extension.py
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/verify_fixed_support_obstruction.py
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/verify_direct_k6_triangle_extension.py
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k7/verify_fixed_support_obstruction.py
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k7/verify_direct_k7_triangle_extension.py
python3 -m unittest \
  tests.test_centered_quarter_bv_all_harmonics \
  tests.test_centered_quarter_k4_extension \
  tests.test_centered_quarter_k5_extension -v
```

The proof dependencies are

```text
exact rational pair/triple masses
        |
        +--> fixed-size marginals + centered moment
        |          |
        |          +--> exact W0 and W1 design kernels
        |
        +--> finite exact LDL checks through k=552
        |          |
        |          +--> rational even/odd tail bounds
        |                         |
        |                         v
        |                  W_k PSD for all k
        |
        +--> finite pair moments through k=121
        |          |
        |          +--> analytic Gegenbauer tail
        |
        +--> 27 exact centered-skew rank residuals
        |
        +--> exact 51-atom locally Gram-PSD K4 extension
        |
        +--> exact 51-atom locally Gram-PSD K5 extension
        |
        +--> exact 51-atom rank-five local K6 extension
        |
        +--> exact 51-atom rank-five local K7 extension
```
