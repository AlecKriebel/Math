# Construction track: diffuse and mesoscopic candidates

Date: 2026-08-01 (America/Los_Angeles)

No literature search or external contact was used.  This report distinguishes
proved algebra, exact finite computations, formal asymptotics, numerical
reconnaissance, and open conclusions.

## 1. Outcome of this track

**OPEN.**  No asymptotically universal simultaneous amplifier was found.

**NEW CANDIDATE EXCLUSION, PARTLY RIGOROUS.**  The most natural surviving
locally diffuse family---a hub joining many growing clique satellites---has an
exactly lumpable chain.  Its rare-mutant first correction is dB-suppressing
for every fixed fitness and every spoke-weight constant.  The algebraic sign
is rigorous within the displayed two-type branching expansion.  Turning that
expansion into a theorem for fixation through order `1/L` still requires a
uniform branching-to-establishment and post-establishment estimate, so the
full family exclusion is not labelled proved here.

The other scanned families (two equitable classes, complete bipartite limits,
paired and subdivided fans, two-clique barbells, a clique with short weighted
tails, and unrestricted small complete supports) supplied no positive
candidate.  These computations are reconnaissance, not universal claims.

## 2. The growing-clique fan

Let `F_{M,L}(s)` have a hub `H` and `M` disjoint modules of `L` vertices.
Every module induces a unit-weight clique, and every hub--module edge has
weight `s>0`; there are no edges between distinct modules.  Thus

\[
 n=ML+1,\qquad d_{\rm leaf}=L-1+s,\qquad d_H=MLs.
\]

The graph is connected for every `s>0`.  Its automorphism group contains the
wreath product permuting vertices within modules and permuting modules.  If
`h` is the hub type and `c_k` is the number of modules containing exactly `k`
mutants, the orbit state is

\[
 (h,c_0,\ldots,c_L),\qquad h\in\{0,1\},\quad
 \sum_{k=0}^L c_k=M.
\]

There are `2 binom(M+L,L)` quotient states.  Write

\[
 X=\sum_k k c_k,qquad d=L-1+s,qquad
 F=n+(r-1)(h+X).
\]

### 2.1 [PROVED] Exact quotient transitions

For Bd, the changing transition rates are

\[
\begin{aligned}
 h:0\to1 &: \frac{rXs}{Fd},&
 h:1\to0 &: \frac{(ML-X)s}{Fd},\\
 k\to k+1 &:c_k(L-k)\left(\frac{rk}{Fd}+\frac{rh}{FML}\right),&
 k\to k-1 &:c_kk\left(\frac{L-k}{Fd}+\frac{1-h}{FML}\right).
\end{aligned}
\tag{1}
\]

For dB they are

\[
\begin{aligned}
 h:0\to1 &: \frac1n\frac{rX}{rX+ML-X},&
 h:1\to0 &: \frac1n\frac{ML-X}{rX+ML-X},\\
 k\to k+1 &:\frac{c_k(L-k)}n
 \frac{r(k+hs)}{r(k+hs)+L-k-1+(1-h)s},\\
 k\to k-1 &:\frac{c_kk}n
 \frac{L-k+(1-h)s}{r(k-1+hs)+L-k+(1-h)s}.
\end{aligned}
\tag{2}
\]

Every expression depends only on the orbit state.  Hence the orbit partition
is strongly lumpable: for any two configurations in one orbit, the total
probability entering every target orbit is the same.  The exact independent
verifier `verify_clique_fan_lumping.py` builds the full subset chain directly
with `Fraction` arithmetic and agrees with (1)--(2) for all states of the test
instances `(M,L)=(2,2),(2,3)`, for both update rules.

### 2.2 [PROVED] The family lies in the surviving diffuse corridor

With the convention `P_{ji}=w_{ij}/d_j`, a leaf and the hub have temperatures

\[
 t_{\rm leaf}=\frac{L-1}{L-1+s}+\frac1{ML},\qquad
 t_H=\frac{MLs}{L-1+s}.
\tag{3}
\]

If `s=Theta(1/M)` and `L\to\infty`, then the uniform-vertex mean of
`|t_i-1|` tends to zero: the leaf error is `O(1/L)` and the possibly nonunit
hub contributes only `O(1/(ML))` to the mean.  Moreover

\[
 \frac1n\sum_{i,j}P_{ji}^2=O(1/L).
\tag{4}
\]

The support degrees are `L` at leaves and `ML` at the hub.  Thus, when
`L\to\infty`, this family has diverging support degree, is locally diffuse,
and is asymptotically isothermal in the uniform-vertex sense.  It is not
removed by the inherited fixed-class unequal-degree obstruction.

The exactly weighted-regular spoke value is

\[
 s_{\rm reg}=\frac{L-1}{ML-1}.
\tag{5}
\]

At (5), Bd ties the complete graph exactly for every `r`, as follows directly
from equality of all weighted degrees.

## 3. Rare-mutant first correction

Fix `M`, `r>1`, and a spoke constant `s=\sigma>0`, then let `L\to\infty`.
Poissonize so every vertex dies at rate one for dB.  Up to first order in
`1/L`, a leaf mutant has death rate one, produces leaf mutants at rate

\[
 b=\frac{(L-1)r}{L+r-2+\sigma}
   =r-\frac{r(r-1+\sigma)}L+O(L^{-2}),
\tag{6}
\]

and produces a hub mutant at rate

\[
 a=\frac r{ML+r-1}=\frac r{ML}+O(L^{-2}).
\tag{7}
\]

A hub mutant dies at leading rate one and produces leaf mutants at leading
rate

\[
 \beta=Mr\sigma.
\tag{8}
\]

For the associated two-type branching process, let `u` and `v` be survival
probabilities from a leaf and the hub.  Direct first-event equations give

\[
 u=(1-u)(bu+av),\qquad v=(1-v)\beta u.
\tag{9}
\]

Put `q=1-1/r`.  Solving (9) through first order gives

\[
 u=q+\frac1L\left[
 -q-\frac\sigma r+
 \frac{\sigma}{1+M\sigma(r-1)}
 \right]+O(L^{-2}),
\tag{10}
\]

while

\[
 v=\frac{M\sigma(r-1)}{1+M\sigma(r-1)}+O(L^{-1}).
\tag{11}
\]

The uniformly chosen initial vertex is the hub with probability
`1/(ML+1)`.  Including that initial condition and subtracting

\[
 \rho_{\rm dB}(K_{ML+1},r)
 =q-\frac{q}{ML}+O(r^{-ML})
\tag{12}
\]

yields the formal coefficient

\[
 \boxed{
 D_{\rm dB}(r,\sigma,M)
 =-\frac{r-1}{r}-\frac\sigma r
  +\frac{\sigma r}{1+M\sigma(r-1)}.}
\tag{13}
\]

That is, the branching calculation predicts

\[
 \rho_{\rm dB}(F_{M,L}(\sigma),r)
 -\rho_{\rm dB}(K_{ML+1},r)
 =\frac{D_{\rm dB}(r,\sigma,M)}L+o(L^{-1}).
\tag{14}
\]

### 3.1 [PROVED ALGEBRA] The predicted coefficient is always negative

Let `x=M\sigma`.  Multiplication of (13) by the positive denominator shows
that its sign is the sign of

\[
 f(x)=-x^2+\big[(r+1)-M(r-1)\big]x-M.
\tag{15}
\]

For `M>1` and `r>1`,

\[
 (r+1)-M(r-1)<2<2\sqrt M.
\]

Therefore the concave quadratic (15) has negative maximum and

\[
 \boxed{D_{\rm dB}(r,\sigma,M)<0}
 \quad(M>1,r>1,\sigma>0).
\tag{16}
\]

For `M=1`, (15) is `-(x-1)^2`, with equality only at the complete graph.

At the regular limit `\sigma=1/M`, (13) simplifies to

\[
 D_{\rm dB}(r,1/M,M)
 =-\left(1-\frac1r\right)\left(1-\frac1M\right).
\tag{17}
\]

For Bd, the analogous two-type calculation has leaf birth rates
`r(L-1)/(L-1+\sigma)` and `r\sigma/(L-1+\sigma)`, leaf loss rate
`(L-1)/(L-1+\sigma)+1/(ML)`, hub leaf-birth rate `r`, and hub loss rate
`M\sigma+O(1/L)`.  After uniform initial averaging, its entire `1/L`
comparison coefficient cancels identically for every `\sigma`; the Bd sign
lives at order `1/L^2`.  This scale separation is exactly what the finite
quotient computations display.

### 3.2 Scope of the derivation

Equations (6)--(13) are an exact algebraic expansion of the displayed
two-type rare-mutant process.  Equation (16) is an exact sign certificate for
that coefficient.  The missing theorem step is a proof that fixation in the
finite clique fan differs from the two-type survival calculation by
`o(1/L)`, uniformly through establishment and the post-establishment path.
Without that estimate, (14) remains a **FORMAL ASYMPTOTIC**, not a proved
fixation formula.

## 4. [NUMERICALLY OBSERVED] Exact quotient data

Sparse solutions of the exact quotient (1)--(2), with residuals below
`2e-9`, give the following dB deficits at the regular value (5), for `M=2`:

| `L` | `r` | graph minus complete | prediction `-q(1-1/M)/L` |
|---:|---:|---:|---:|
| 20 | 1.1 | `-7.50e-4` | `-2.27e-3` |
| 40 | 1.1 | `-7.73e-4` | `-1.14e-3` |
| 80 | 1.1 | `-5.08e-4` | `-5.68e-4` |
| 20 | 2 | `-1.12e-2` | `-1.25e-2` |
| 40 | 2 | `-5.93e-3` | `-6.25e-3` |
| 80 | 2 | `-3.05e-3` | `-3.13e-3` |
| 20 | 10 | `-2.07e-2` | `-2.25e-2` |
| 40 | 10 | `-1.08e-2` | `-1.13e-2` |
| 80 | 10 | `-5.51e-3` | `-5.63e-3` |

The slower convergence near `r=1` is expected because the establishment
scale diverges as selection weakens.  These values are evidence for (14), not
a proof of it.

Perturbing `s` below (5) can make the finite dB comparison positive extremely
near neutrality, but the Bd comparison then has the opposite sign.  Above
(5), Bd becomes positive and dB becomes more negative.  As `L` grows, the
temporary dB-positive window disappears in accordance with (16).

## 5. Other construction searches

The following are **NUMERICALLY OBSERVED FALSIFICATIONS OF ANSATZE**, not
theorems about all graphs.

1. Dense two-equitable-class graphs with vanishing or mesoscopic first class:
   broad power-law and random weight scans found no parameter positive for
   both rules over a fixed fitness grid.  dB was negative whenever Bd was
   positive.
2. Complete bipartite graphs `K_{a,b}`: Bd is positive away from equal parts,
   while dB is negative in every tested case.
3. Paired clique fans, subdivided stars, and the generic two-vertex module fan
   with two independently weighted spokes: the Bd and dB zero surfaces meet
   in the wrong order; no overlap was found.
4. Two equal cliques joined by one weighted bridge and a large clique with a
   short weighted tail: no simultaneous sign was found.
5. Unrestricted positive weights on `K_5` and `K_6`: differential-evolution
   reconnaissance collapsed to the uniform graph rather than a strict
   simultaneous amplifier.

A neutral-pair implementation independently reproduced the inherited exact
weak coefficients of the weighted path `(5,1,1,5)`.  Enumeration of every
connected unweighted graph through six vertices found no strict simultaneous
weak amplifier.  Random positive-weight scans consistently satisfied
`N_Bd+N_dB<=2n`, but this is only evidence; no such universal inequality is
claimed here.

## 6. Files and reproducibility

- `scan_clique_fan.py`: exact quotient builder and sparse absorbing solve;
- `verify_clique_fan_lumping.py`: independent exact full-chain verifier;
- `verify_clique_fan_asymptotic.py`: exact symbolic checks of (9)--(17);
- `equitable_solver.py`: general finite equitable-class quotient solver;
- `scan_dense.py`: dense two-class reconnaissance;
- `scan_subdivided_fan.py`, `scan_two_vertex_fan.py`: rooted-module fans;
- `scan_small_graphs.py`: unrestricted small complete-support search;
- `weak_coefficients.py`: neutral-pair weak-selection calculation.

All floating-point solvers check the absorbing-system residual.  Their output
is not used as a positivity certificate.
