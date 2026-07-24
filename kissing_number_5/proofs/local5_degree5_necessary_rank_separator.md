# An exact degree-five separator for the local five-node pair data

## Theorem and scope

Let
\[
S=\left\{-\frac{77}{100},-\frac7{10},-\frac{11}{25},
          -\frac9{100},\frac{499}{1000}\right\}.
\]

**Theorem.**  There is no 41-point spherical code in \(S^4\) whose
off-diagonal inner products lie in \(S\) and whose ordered multiplicities,
in the displayed order, are
\[
(170,6,262,652,550).                                  \tag{1}
\]

This is an exact fixed-support nonexistence theorem.  It does **not** say
that an arbitrary 41-point code must use this support or these
multiplicities, and therefore it does not prove \(\tau(5)\le40\).

The compact certificate is
[`../certificates/local5_degree5_necessary_rank_separator.json`](../certificates/local5_degree5_necessary_rank_separator.json).
The standard-library verifier
[`../verifiers/verify_local5_degree5_necessary_rank_separator.py`](../verifiers/verify_local5_degree5_necessary_rank_separator.py)
reconstructs the full exact rational dual from the small stored directions.
It does not invoke an LP or SDP solver.

## 1. Triangle variables

For a hypothetical code, let \(x_{abc}\) be the number of unordered
triangles whose sorted edge colors are \((a,b,c)\).  Exact
\(3\times3\) Gram positivity leaves the following 21 types:
\[
\begin{gathered}
004,014,023,024,033,034,114,123,124,133,134,\\
222,223,224,233,234,244,333,334,344,444.
\end{gathered}                                         \tag{2}
\]
Determinant-zero types are retained.  Thus no boundary case is lost.
The variables satisfy \(x_{abc}\ge0\) and the five exact incidence
equations
\[
\sum_{abc}\operatorname {mult}_q(abc)x_{abc}
=39E_q,\qquad
(E_0,\ldots,E_4)=(85,3,131,326,275).                  \tag{3}
\]
The proof relaxes integrality, so infeasibility is stronger than needed.

## 2. Necessary scalar and matrix constraints

Only necessary conditions for a genuine realization are used.

### Threshold and support-specific clique cuts

The exact common-center inequality at
\[
q=\frac{5777}{10000}
\]
gives the stored threshold upper row.  The support-specific clique lemma
from `local_hybrid_degree4_rank_color_clique_barrier.md` gives
\[
W_{01}+2W_{11}\le24.                                  \tag{4}
\]
Its proof uses exact \(3\times3\) determinants and the fact that six
vectors with mutual inner product \(499/1000\) have rank six.

### A necessary outer relaxation of C047

For the fixed pair data,
\[
\delta=\frac{29759}{820000},\qquad
T_{\rm center}=\frac{46559493}{1025000}.
\]
C047 says
\[
20(T-T_{\rm center})^2\le369\delta^3.                 \tag{5}
\]
The rational interval used here is an **outer**, hence necessary,
relaxation:
\[
\left|T-T_{\rm center}\right|\le\frac3{100},           \tag{6}
\]
because
\[
20\left(\frac3{100}\right)^2-369\delta^3
=\frac{4873380367689}{13448000000000000}>0.           \tag{7}
\]
This is the crucial distinction from the earlier \(29/1000\) inner-band
experiment.

### Two harmonic-kernel rank intervals

The centered-skew lemma proved in
`harmonic_combination_centered_skew.md` supplies two further necessary
linear intervals in the triangle counts:
\[
|D_{(H_0+5H_1)/6}|\le\frac72,\qquad
|D_{H_2}|\le\frac{157}{50}.                           \tag{8}
\]
Both are rational outer approximations to the sharper exact rank bounds.
After moving the pair-data constants to the right, their all-distinct
triple contributions lie respectively in
\[
\left[\frac{4614211}{3840},\frac{4641091}{3840}\right]
\]
and
\[
\left[
\frac{104986344211837}{1254400000000},
\frac{112863976211837}{1254400000000}
\right].                                               \tag{9}
\]

### Degree-five BV and colored-degree PSD

For total degree five, let \(B_k(x)\), \(0\le k\le5\), be the exact
fixed-\(41\) Bachoc--Vallentin blocks in the normalization used by
`verify_weighted_residual_barrier.py`.  Every genuine code satisfies
\[
B_k(x)\succeq0.                                       \tag{10}
\]
The centered covariance \(C(x)\) of the five colored degree columns also
satisfies
\[
C(x)\succeq0.                                         \tag{11}
\]

The certificate selects nine rational quadratic forms from (10)--(11):
three from \(B_2\), two from \(B_3\), one each from \(B_1,B_4\), and two
from \(C\).  Their rational direction vectors are recorded explicitly in
the JSON.  No eigenvalue rounding is used in verification.

## 3. The exact finite dual

Introduce a free common-margin variable \(z\).  Each selected BV
quadratic form is imposed as
\[
q^\mathsf TB_k(x)q\ge z,                              \tag{12}
\]
while the two covariance forms are imposed with right side zero.
A genuine realization makes this finite system feasible with \(z=0\).

Write the resulting system as
\[
Ax\le b,\qquad Ex=f,\qquad x\ge0,                     \tag{13}
\]
with \(z\) included as a free final variable, and minimize \(-z\).
There are 21 triangle variables.  The certificate stores 14 active
inequalities and the following 18 basic triangle indices:
\[
0,1,2,3,4,5,8,9,11,12,13,14,15,16,17,18,19,20.       \tag{14}
\]
Together with the free \(z\) column, these give a square \(19\times19\)
system for 14 nonnegative inequality multipliers and five free incidence
multipliers.

The verifier solves that system by exact Gauss--Jordan elimination.  It
then checks:

1. every one of the 14 inequality multipliers is strictly positive;
2. the combined coefficient is exactly \(-1\) on \(z\);
3. it is exactly zero on the 18 basic triangle columns;
4. it is strictly negative on the three remaining columns
   \(114,123,134\); and
5. the exact dual lower bound for \(-z\) is
\[
\varepsilon=
\frac{
111155751914162088181574110470285369293569260826340758682583706463708549791398364559254338577405495351961219368572100654108903740563092663957474470438305931382264916165533798539605398101345764395608460453825085463308286800584091288924369310530923581936736919473115445181968049090443318473051890360685380106098720268443212093166489199
}{
386620944208815127045307777453913146490885262282444837240483166411027439269726353884496456148121273736188712256105813443033913929722435921764848155144001831808519499640579890842967662007563756468186837653368450735689619418213927319544213092151552859835732356712061652451723436093059349433704325750771713212251080240377120000000000000000
}>0.                                                    \tag{15}
\]
Numerically, only for scale,
\[
\varepsilon=0.000287505769098\ldots.
\]

For completeness, the dual implication is elementary.  If
\(\lambda\ge0\) and \(\mu\) are the reconstructed multipliers, the checked
column inequalities say
\[
-A^\mathsf T\lambda+E^\mathsf T\mu\le c,
\]
with equality on the free \(z\) column, where \(c\) is the objective
vector for \(-z\).  Therefore every feasible point obeys
\[
-z=c^\mathsf T(x,z)
\ge-\lambda^\mathsf Tb+\mu^\mathsf Tf
=\varepsilon>0.                                      \tag{16}
\]
Hence \(z<0\), contradicting the feasible choice \(z=0\) supplied by
(10)--(11).  This proves the theorem.

## 4. Boundary and numerical rigor

- The kissing inequality is non-strict, and all reductions use
  \(\langle x_i,x_j\rangle\le1/2\).
- Triangle types with determinant zero would be included by (2).
- Triangle counts are allowed to be arbitrary nonnegative rationals in
  the relaxation.
- The C047 band \(3/100\) and both harmonic-rank bands are wider than their
  exact algebraic feasible intervals; they cannot discard a realization.
- Every certificate coefficient is rational.  PSD is used only through
  explicitly listed rational quadratic forms.
- The exploratory LP and its floating eigenvectors are not trusted.  The
  stored vectors are rational, and the verifier rebuilds all rows and the
  dual from scratch.
- Strictness occurs only in the final exact positive rational
  \(\varepsilon\); all geometric inequalities remain non-strict.

## 5. Reproduction and proof dependency

Run

```bash
PYTHONPATH=. /usr/bin/python3 \
  verifiers/verify_harmonic_combination_centered_skew.py

PYTHONPATH=. /usr/bin/python3 \
  verifiers/verify_local5_degree5_necessary_rank_separator.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  tests.test_harmonic_combination_centered_skew \
  tests.test_local5_degree5_necessary_rank_separator -v
```

The human-readable dependency chain is
\[
\begin{gathered}
\text{fixed support and pair counts}\\
\Downarrow\\
\text{triangle incidences, threshold/clique, C047, harmonic-rank,
BV, and covariance constraints}\\
\Downarrow\\
\text{finite rational linear system with }z=0.
\end{gathered}
\]
The computer-certified step is only
\[
\text{compact rational active basis}
\Longrightarrow
\text{exact dual }\varepsilon>0.
\]
The verifier is substantially smaller than the cutting-plane discovery
program and does not read solver output.
