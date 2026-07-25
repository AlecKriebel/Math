# Continuous four-point moment relaxation at \(N=41\)

## 1. Measures and normalization

Let \(g_{ij}=\langle x_i,x_j\rangle\).  For a hypothetical
41-point code define the ordered distinct-tuple measures

\[
\begin{aligned}
\alpha&={1\over41}\sum_{i\ne j}\delta_{g_{ij}},\\
\nu&={1\over41}\sum_{i,j,k\ {\rm distinct}}
 \delta_{(g_{ij},g_{ik},g_{jk})},\\
\rho&={1\over41}\sum_{i,j,k,\ell\ {\rm distinct}}
 \delta_{(g_{ij},g_{ik},g_{jk},g_{i\ell},g_{j\ell},g_{k\ell})}.
\end{aligned}
\]

Their masses are respectively

\[
40,\qquad 40\cdot39=1560,\qquad
40\cdot39\cdot38=59280.
\]

Write the six coordinates of \(\rho\) as
\[
(q,a,b,c,d,e)
=(g_{ij},g_{ik},g_{jk},g_{i\ell},g_{j\ell},g_{k\ell}).
\]
Every edge coordinate lies in \(I=[-1,1/2]\).  Every three-vertex
face obeys
\[
\Delta_3(u,v,t)=1+2uvt-u^2-v^2-t^2\geq0,
\]
and the full \(4\)-by-\(4\) Gram determinant is nonnegative.  The
projection identities are
\[
\pi_{ij}\nu=39\alpha,\qquad \pi_{ijk}\rho=38\nu,
\]
with the other projections following from \(S_3\)- and
\(S_4\)-invariance.

## 2. Degree-four truncated moment system

For a moment sequence \(y\), let \(M_r(y)\) denote the moment matrix
indexed by monomials of total degree at most \(r\).  The basic continuous
relaxation uses moments through degree four:

- \(M_2(\alpha)\succeq0\), with order-one localizers for
  \(q+1\) and \(1/2-q\);
- \(M_2(\nu)\succeq0\), with the analogous edge localizers and the
  scalar localizer \(L_\nu(\Delta_3)\geq0\);
- \(M_2(\rho)\succeq0\), with all six edge localizers, the four scalar
  face-determinant localizers, and
  \(L_\rho(\det G_4)\geq0\).

All projection and permutation-symmetry equalities are imposed through
degree four.  This is a relaxation on the full interval.  Its variables
are moments, not weights on a prescribed alphabet.

The same formulation works at any higher order by enlarging the moment
and localizing matrices.  The exact counter-witness below is an atomic
measure, so it satisfies every order, not merely order two.

## 3. Edge-conditioned covariance blocks

For any polynomial feature column
\(\phi(q,a,b)\), a real code necessarily satisfies

\[
38\int\phi(q,a,b)\phi(q,a,b)^{\mathsf T}\,d\nu
-\int\phi(q,a,b)\phi(q,c,d)^{\mathsf T}\,d\rho
\succeq0.                                             \tag{1}
\]

Indeed, for a fixed ordered base \((i,j)\), put
\(v_k=\phi(g_{ij},g_{ik},g_{jk})\) for its 39 residual vertices.
The contribution of this base to (1) is

\[
39\sum_kv_kv_k^{\mathsf T}
-\left(\sum_kv_k\right)\left(\sum_kv_k\right)^{\mathsf T}
\succeq0.
\]

The implementation uses every monomial in \((q,a,b)\) through degree
two.  Multiplying (1) by a polynomial nonnegative on a base interval
gives further valid localized blocks whenever the required moments are
available.

## 4. A closed semialgebraic cap/product flag

The instantiated discovery row uses

\[
L=-\frac3{10},\quad U=-\frac6{25},\quad
b_0=\frac{49}{100},\quad \delta'=\frac1{301},\quad M=3.
\]

For \(q\in B=[L,U]\), define

\[
\begin{aligned}
H(q,a,b)&:\quad a+b\leq0,\quad
(a+b)^2-\delta'^2(2+2q)\geq0,\\
G(q,a,b)&:\quad a\geq b_0,\quad b\geq b_0.
\end{aligned}
\]

The robust-depth theorem with gap \(1/300\) implies
\(H_e\geq7\): using the smaller \(\delta'\) only enlarges the closed
tail.  The two sets are disjoint.  Moreover

\[
\frac{2b_0^2}{1+q}\geq
\frac{2b_0^2}{1+U}
=\frac{2401}{3800}
=\frac58+\frac{13}{1900}>\frac58,
\]
so the proved projected-cap bound gives \(\Gamma_e\leq3\).
Consequently

\[
H_e\Gamma_e\leq3H_e+7\Gamma_e-21.                   \tag{2}
\]

Introduce positive component moment sequences supported on the base
band and on the closed sign conditions defining \(H\), its complement,
\(G\), and its complement.  Their sums are the global moments, and the
row and column projections of the four-point components are respectively
38 times the corresponding \(H\)- and \(G\)-triple components.  Boundary
atoms may be assigned to either adjacent closed component; this weakens
the relaxation but never deletes a real code.

In the ordered-measure normalization, (2) becomes

\[
\rho(B,H,G)\leq
3\nu(B,H)+7\nu(B,G)-21\alpha(B).                    \tag{3}
\]

The separate depth and cap rows are

\[
\nu(B,H)\geq7\alpha(B),\qquad
\nu(B,G)\leq3\alpha(B).                              \tag{4}
\]

No discretization is used to derive (3) or (4).

## 5. Rank-five harmonic trace cuts

For
\[
\kappa(t)=\sum_k c_kP_k^{(5)}(t),
\qquad
r=\sum_{c_k\ne0}\dim\mathcal H_k(\mathbb R^5),
\]
let \(K_{ij}=\kappa(g_{ij})\), and set

\[
\begin{aligned}
V&=\operatorname{tr}K^2-\frac{(\operatorname{tr}K)^2}{r},\\
D&=\operatorname{tr}K^3
-\frac{3\operatorname{tr}K\,\operatorname{tr}K^2}{r}
+\frac{2(\operatorname{tr}K)^3}{r^2}.
\end{aligned}
\]

The exact rank-\(r\) trace inequality is

\[
r(r-1)D^2\leq(r-2)^2V^3.                            \tag{5}
\]

Here

\[
\begin{aligned}
\operatorname{tr}K&=41\kappa(1),\\
\operatorname{tr}K^2
 &=41\left(\kappa(1)^2+\int\kappa(q)^2\,d\alpha(q)\right),\\
\operatorname{tr}K^3
 &=41\left(\kappa(1)^3
 +3\kappa(1)\int\kappa(q)^2\,d\alpha(q)
 +\int\kappa(u)\kappa(v)\kappa(t)\,d\nu\right).
\end{aligned}
\]

The 27 degree-at-most-three kernel combinations of harmonic rank below
41 are imposed.  For convex numerical discovery one may replace (5) by
a globally valid rational secant outer cut \(|D|\leq sV\), after proving
an upper bound \(V\leq U\) and choosing
\[
s^2r(r-1)\geq(r-2)^2U.
\]
The counter-witness satisfies the sharper nonlinear inequalities (5),
so it also satisfies every such valid outer cut.

## 6. Exact six-point counter-witness and its scaling

The file
`../four_point_depth_projection/k6_product_audit/productpool_extension.json`
is a positive rational mixture of 74 exact rank-five \(K_6\) Gram
matrices.  Let \(\alpha_6,\nu_6,\rho_6\) be the measures obtained by
summing, in each atom, over all ordered distinct pairs, triples, and
quadruples.  Define

\[
\boxed{\quad
\alpha=\frac43\alpha_6,\qquad
\nu=13\nu_6,\qquad
\rho=\frac{494}{3}\rho_6.
\quad}                                               \tag{6}
\]

The masses then are \(40,1560,59280\).  Also
\(\pi\nu_6=4\alpha_6\) and \(\pi\rho_6=3\nu_6\), so (6) gives exactly
\(\pi\nu=39\alpha\) and \(\pi\rho=38\nu\).

Every atom is a genuine Gram-PSD rank-five six-point configuration.
Therefore all moment and support-localizer matrices, including every
higher-order version, have explicit positive atomic Gram
decompositions.

The covariance block (1) also has an atomwise SOS decomposition.  A
sampled base has four residual feature vectors \(v_1,\ldots,v_4\), and
(6) transforms its contribution into

\[
\frac{494}{3}\left(
4\sum_{h=1}^4v_hv_h^{\mathsf T}
-ss^{\mathsf T}\right)
=\frac{494}{3}\sum_{h<k}
(v_h-v_k)(v_h-v_k)^{\mathsf T},\qquad
s=\sum_hv_h.                                         \tag{7}
\]

Thus no choice of polynomial degree in a block of the form (1) can
separate this witness.

For the cap/product flag, the exact induced masses are

\[
\begin{aligned}
\alpha(B)&=\frac{125532493886399}{56250000000000},\\
\nu(B,H)&=\frac{974897098487491}{25000000000000},\\
\nu(B,G)&=\frac{656862349021}{100000000000},\\
\rho(B,H,G)&=\frac{8707691389928497}{75000000000000}.
\end{aligned}
\]

They satisfy the depth and cap inequalities strictly:

\[
\nu(B,H)-7\alpha(B)
=\frac{5259164057568247}{225000000000000}>0,
\]

\[
3\alpha(B)-\nu(B,G)
=\frac{4741606889923}{37500000000000}>0,
\]

while the product row (3) is an exact equality.

Finally, the same pair/triple marginal satisfies all 27 sharp trace cuts
(5) strictly.  The least exact residual is attained by \(H_0+5H_1\) and
equals

\[
\frac{
55167524940721706879162142630825892057376871095010136958418083
}{
145896583472409513607299072000000000000000000000000000000000000
}>0.
\]

Hence this continuous four-point/edge-conditioned relaxation is
feasible at \(N=41\).  Weak SDP duality rules out a valid dual objective
strictly below 41 for this formulation.

## 7. Exact bottleneck of this baseline system

The failure is not caused by insufficient polynomial degree on one
\(K_4\) or one base edge.  The witness is supported on genuine
rank-five \(K_6\) Gram matrices and therefore survives all such local
SOS refinements.  What it does not encode is consistency between
overlapping six-subsets of one 41-point Gram matrix or the higher
falling-factorial consequences of an integer cap bound.

A separating mechanism must therefore add information not determined by
one symmetric \(K_6\) marginal, for example:

- higher factorial moments of the integer depth and cap counts;
- overlapping-\(K_6\) consistency (at least a seven-vertex flag);
- a global rank-five identity coupling different base edges;
- or a new nonlinear count inequality that the repaired \(K_6\) mixture
  itself violates.

Adding more univariate/triple harmonic cuts or raising the polynomial
degree inside the same edge-conditioned covariance template cannot
remove the counter-witness.

The first item does separate the witness.  The follow-up exact
calculation is recorded in
[`FACTORIAL_HIERARCHY.md`](FACTORIAL_HIERARCHY.md).
