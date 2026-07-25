# Low-harmonic rank/frame inequalities and an exact barrier

## Status

This note proves a rank-sensitive family of universal inequalities, then
checks exactly that the existing all-harmonic mass-\(41\)
pair/triple pseudodistribution satisfies every member that can be nontrivial
at \(N=41\).  It is a **relaxation barrier**, not a spherical code and not an
upper-bound proof.

## Universal rank/frame matrix inequality

Let \(C=\{x_1,\ldots,x_N\}\subset S^4\), let \(P_k=P_k^{(5)}\) be the
normalized dimension-five Gegenbauer polynomial, and put
\[
 H_k=(P_k(\langle x_i,x_j\rangle))_{i,j=1}^N.
\]
The spherical-harmonic addition formula gives
\[
 H_k\succeq0,\qquad
 \operatorname{rank}H_k\le h_k,\qquad
 h_k=\binom{k+4}{4}-\binom{k+2}{4}.
\tag{1}
\]
In particular,
\[
 (h_0,h_1,h_2,h_3)=(1,5,14,30).
\tag{2}
\]

Fix a nonempty finite set \(S\) of harmonic degrees and write
\(r_S=\sum_{k\in S}h_k\).  For arbitrary real coefficients \(a_k\),
\[
 K=\sum_{k\in S}a_kH_k
\quad\hbox{satisfies}\quad
\operatorname{rank}K\le r_S.
\]
The eigenvalue Cauchy--Schwarz inequality therefore gives
\[
 \operatorname{tr}(K^2)\ge
 \frac{\operatorname{tr}(K)^2}{r_S}.             \tag{3}
\]
Since \(P_k(1)=1\), \(\operatorname{tr}K=N\sum_ka_k\).  Expanding (3)
for all real coefficient vectors proves that
\[
 \boxed{\quad
 M_S-\frac N{r_S}{\bf1}{\bf1}^{\mathsf T}\succeq0,\qquad
 (M_S)_{k\ell}
 =\frac1N\sum_{i,j=1}^N
 P_k(g_{ij})P_\ell(g_{ij}).
 \quad}                                           \tag{4}
\]
Unlike ordinary Gegenbauer-moment nonnegativity, (4) uses the finite
dimension of the harmonic feature spaces.  It is nevertheless only a
two-point constraint.

For \(N=41\), a set \(S\) containing any degrees beyond \(3\) has
\(r_S\ge h_4=55\), and (3) cannot improve the elementary nonnegativity
of \(\operatorname{tr}(K^2)\).  Among degrees \(0,1,2,3\), precisely
eleven nonempty subsets have \(r_S<41\):
\[
\{0\},\{1\},\{0,1\},\{2\},\{0,2\},\{1,2\},\{0,1,2\},
\{3\},\{0,3\},\{1,3\},\{0,1,3\}.                 \tag{5}
\]

## Exact mass-\(41\) barrier

Use the seven-node pair measure \(\alpha\) stored in
[`../certificates/fixed41_bv_fullradial_k16_pseudodistribution.json`](../certificates/fixed41_bv_fullradial_k16_pseudodistribution.json).
It has total off-diagonal mass \(40\), so on this measure
\[
 (M_S)_{k\ell}
 =1+\sum_q\alpha_qP_k(q)P_\ell(q).                \tag{6}
\]
The independent all-harmonic verifier already proves that the same
pair/triple object satisfies every ordinary two-point moment and every
fixed-cardinality Bachoc--Vallentin radial block in every harmonic degree.

The new exact verifier forms (6) over \(\mathbb Q\) for all eleven sets
in (5), subtracts \(41{\bf1}{\bf1}^{\mathsf T}/r_S\), and checks every
principal minor.  All are nonnegative.  The sole forced zero is the
\(S=\{0\}\) inequality; every other checked principal minor is positive.
The least positive principal minor is
\[
\frac{7796592200083}{800000000000000}>0,
\tag{7}
\]
attained for \(S=\{1\}\).

Thus adjoining the complete family (4) to the all-degree two/three-point
relaxation still does not exclude mass \(41\).  A successful rank argument
must retain at least a higher trace such as
\(\operatorname{tr}(K^4)\), whose expansion contains genuine four-cycle
data, or another common-source invariant not determined by the pair
measure.

## Reproduction and dependencies

From the project directory run

```sh
python3 verifiers/verify_fixed41_bv_all_harmonics.py
python3 verifiers/verify_harmonic_rank_frame_barrier.py
python3 -m unittest tests.test_harmonic_rank_frame_barrier -v
```

The first command certifies the imported pseudo-object's all-degree
two/three-point properties.  The second verifier is deliberately smaller:
it uses only `fractions.Fraction`, the Gegenbauer recurrence, exact Gaussian
elimination, and exhaustive principal-minor checks.

No floating-point eigenvalue, solver status, finite inner-product
assumption about genuine codes, or rank-\(41\) Gram realization is claimed.
