# Curved-arc closure of the singular DTH product corner

## Status

Let

\[
 \widehat D_z=(2\sqrt2)D_z,
 \qquad
 \Delta(z)=4\|z\|^2-\sum_{j=1}^4s_j(\widehat D_z)^2.
\tag{1}
\]

Thus the Ky--Fan-four form of DTH is exactly \(\Delta(z)\ge0\).  This
note closes the lower-rank singularity left open by the smooth
factor-equality Morse--Bott theorem.

### Product-corner theorem

There is a neighborhood of the local-unitary orbit of a product tensor
in which

\[
 \boxed{\Delta(z)\ge0.}
\tag{2}
\]

More precisely, equality in a sufficiently small neighborhood is possible
only on one of the exact deficient-support branches

\[
 z=a\otimes\xi,
 \qquad \operatorname{SchmidtRank}(\xi)\le2,
\tag{3}
\]

and their physical-site permutations.

The proof treats arbitrary complex real-analytic arcs and, more strongly,
arbitrary convergent sequences.  It includes local-unitary gauge terms,
normalization, all three choices of the active pair, multi-pair zero-Hessian
directions, and the sixfold tied cluster belonging to a scaled-unitary
single pair.

This is a local DTH theorem.  It does not prove DTH at full-local-rank
points, square-zero positivity, unrestricted three-copy positivity, or an
all-copy Werner theorem.

## 1. A local-unitary slice

Fix

\[
 z_0=|000\rangle.
\]

Relative to \(e_0\oplus e_0^\perp\) at every site, let \(W\) be the
twenty-dimensional complex space spanned by basis tensors of Hamming weight
two or three.  Every nonzero tensor sufficiently close to \(z_0\) is,
after local unitaries and multiplication by a nonzero scalar, uniquely of
the form

\[
 z=z_0+h,
 \qquad h\in W,
\tag{4}
\]

once the harmless stabilizer of \(e_0\) is left unfixed.

To prove this, use the standard unitary chart

\[
 U(x)e_0={e_0+x\over\sqrt{1+\|x\|^2}},
 \qquad x\in e_0^\perp,
\]

and complete its first column by Gram--Schmidt in the fixed order
\(e_1,e_2\).  Apply \(U(x_1)^\dagger\otimes U(x_2)^\dagger\otimes
U(x_3)^\dagger\) and ask that the six complex weight-one coefficients
vanish.  At \((x_1,x_2,x_3,z)=(0,0,0,z_0)\), the derivative of those six
equations with respect to \((x_1,x_2,x_3)\) is minus the identity.  Solving
successive homogeneous Taylor coefficients therefore gives a convergent
real-analytic solution: at degree \(r\) the same invertible linear part is
used, while the right side depends only on lower degrees.  The majorant is
the geometric series for the unitary chart, so the coefficient recursion
converges in a smaller ball.  Finally divide by the nonzero \(000\)
coefficient.  This proves (4), including for analytic arcs.

Hodge covariance preserves the singular values of \(D_z\), and
\(\Delta(cz)=|c|^2\Delta(z)\).  Hence neither the gauge nor the scalar
division changes the sign.  In particular, normalization never enters the
local argument.

## 2. The two blow-ups

For \(h=r\delta\), \(\|\delta\|=1\), the eight squared singular values of
\(\widehat D_{z_0+h}\) which converge to one have no first-order shift.
Their second effective matrix is the exact matrix \(H_\delta\) in
`agent_dth_product_corner_cluster.md`.  Put

\[
 q_2(\delta)=-\kappa_4(H_\delta)\ge0,
\tag{5}
\]

where \(\kappa_4\) is the sum of the four largest eigenvalues.  Then

\[
 \Delta(z_0+r\delta)=8r^2q_2(\delta)+O(r^3).
\tag{6}
\]

The precise factor in (6) is immaterial below; its positivity is not.
The complete zero cone of \(q_2\), modulo the local-unitary directions
already removed in (4), is:

1. one active pair with an arbitrary \(2\times2\) matrix \(Z\);
2. two active pairs, both scaled unitaries;
3. three active scaled unitaries satisfying the skew-holonomy equation.

This is the exact common-maximizer classification in
`agent_dth_product_zero_cone_quartic.md`.

The following lemma is the curved, rather than straight-ray, statement
needed here.

### Lemma 1 (complete second blow-up)

Let \(\delta\ne0\) belong to the zero cone and let

\[
 z(t)=z_0+t\delta+t^2\eta+o(t^2).
\tag{7}
\]

If the four-dimensional effective top cluster is isolated, then

\[
 \Delta(z(t))
 =t^4\left(q_4(\delta)+
       \eta_{\mathbb R}^{\mathsf T}G_\delta\eta_{\mathbb R}\right)
   +o(t^4),
\tag{8}
\]

with \(G_\delta\succeq0\).  Here realification turns the twenty complex
coordinates of \(W\) into forty real coordinates, and

\[
 q_4(\delta)=
 \begin{cases}
  8|\det Z|^2,&\text{one active pair},\\[2mm]
  8\displaystyle\sum_e\alpha_e^4
   +4\displaystyle\sum_{e<f}\alpha_e^2\alpha_f^2,
       &Z_e=\alpha_eU_e\text{ on two or three pairs}.
 \end{cases}
\tag{9}
\]

For a single active pair whose second-order cutoff is isolated, the
spectrum of \(G_\delta\) is

\[
 0^{(8)},\qquad2^{(24)},\qquad4^{(8)}.
\tag{10}
\]

If \(Z\) has rank one, its kernel consists exactly of the four complex
second-jet coefficients on that same pair.  For two or three active pairs
we need only \(G_\delta\succeq0\); no amplitude-independent multi-pair
spectrum is asserted.

If a single \(Z\) is a scaled unitary, the effective second-order cutoff is
sixfold and (8) need not be differentiable as a function of \(\eta\).
Nevertheless its lower second-blow-up value obeys

\[
 \boxed{
 \liminf_{t\to0}{\Delta(z(t))\over t^4}
 \ge8|\det Z|^2>0.}
\tag{12}
\]

#### Proof

Write

\[
 S(t)=\widehat D_{z(t)}^\dagger\widehat D_{z(t)}
      =S_0+tS_1+t^2S_2+t^3S_3+t^4S_4+o(t^4)
\]

and split the space into the eight-dimensional one-eigenspace \(P_0\) of
\(S_0\) and its complement.  Eliminating the complement gives

\[
\begin{aligned}
 H_2={}&a_2+b_1b_1^\dagger,\\
 H_3={}&a_3+b_1b_2^\dagger+b_2b_1^\dagger,\\
 H_{40}={}&a_4+b_2b_2^\dagger+b_1b_3^\dagger+b_3b_1^\dagger
             +b_1c_2b_1^\dagger,
\end{aligned}
\tag{13}
\]

where \(a_j=P_0S_jP_0\), \(b_j=P_0S_j(1-P_0)\), and
\(c_2=(1-P_0)S_2(1-P_0)\).  Let \(R\) be the four-dimensional top
projector of \(H_2\), \(L=P_0-R\), and let \(H_2^+\) be the inverse of
\(H_2|_R\), extended by zero.  Direct expansion of the cluster trace gives

\[
\begin{aligned}
 \operatorname{Tr}_4S(t)\big|_{t^4}
 ={}&\operatorname{Tr}R\bigl(H_{40}-H_2b_1b_1^\dagger\bigr)\\
 &+\operatorname{Tr}\bigl(H_2^+H_3LH_3R\bigr).
\end{aligned}
\tag{14}
\]

Subtracting (14) from the norm coefficient \(4\|\eta\|^2\) gives (8).
There is no linear term in \(\eta\).  This also proves that all possible
cubic cluster splittings have been retained; no choice of individual
eigenvalue branches has been made.

There is a useful stronger parity check.  For every \(v\in W\), along the
straight pencil \(z_0+tv\),

\[
 b_1b_2^\dagger=b_2b_1^\dagger=0,
 \qquad H_3=0.
\tag{14a}
\]

Indeed, \(b_1\) has one Hodge occupancy change from the product sector,
whereas \(b_2\), being quadratic in a tensor with at least two excited
indices, has the complementary occupancy parity on at least one site.
Their intermediate basis supports are disjoint.  Equivalently, insert the
three epsilon factors: every summand contains at one site both
\(\varepsilon_{0ai}\) and \(\varepsilon_{pai}\) with exactly one of
\(p,a,i\) equal to zero, so it vanishes.  Thus the straight cluster has no
cubic term anywhere in the slice, including at a nonsmooth cutoff.

It remains only a finite epsilon contraction.  Singular-value coordinates
put a single pair into \(aE_{11}+bE_{22}\).  For multiple pairs, the
common-maximizer calculation puts two Bell matrices into the symmetric
form and, when present, the third into the antisymmetric form.  In these
coordinates, substitution into (13)--(14) gives

\[
 \begin{array}{c|c}
 \text{stratum}&q_4\\ \hline
 \text{one pair}&8a^2b^2\\
 \text{two or three pairs}&
 8\sum_e\alpha_e^4+4\sum_{e<f}\alpha_e^2\alpha_f^2.
 \end{array}
\tag{15}
\]

Because of (14a), the curved correction is the second directional form of
the globally nonnegative function \(q_2\).  It is therefore positive
semidefinite on every smooth zero-cone stratum.  For a single pair the
epsilon contraction gives the stronger explicit identity

\[
\begin{aligned}
 \eta_{\mathbb R}^{\mathsf T}G_Z\eta_{\mathbb R}
 ={}&2\bigl(\|\eta_{13}\|^2+\|\eta_{23}\|^2\bigr)\\
 &+2\sum_{i,k=1}^2|\eta_{iik}|^2
   +4\sum_{\substack{i,j,k=1\\ i\ne j}}^2|\eta_{ijk}|^2.
\end{aligned}
\tag{16}
\]

This proves (10), identifies its kernel, and is independent of the two
singular values of \(Z\).  For audit purposes, if the nonzero spectrum of
\(H_2\) on a smooth multi-pair chart is \(x,x,y,y\), then

\[
 R={H_2((x+y)I-H_2)\over xy},
 \qquad
 H_2^+={(x+y)R-H_2\over xy}.
\tag{16a}
\]

These rational projector formulas verify positivity without choosing
algebraic eigenvectors.  Only the strict value (15), not a universal
multi-pair Gram spectrum, is used below.

Here is an exact finite certificate for the amplitude independence in
(16).  By homogeneity and interchange of the two singular axes, take the
singular values to be \((a,1)\), away from the tied values \(a=\pm1\).
Then

\[
 x+y=2(a^2+1),
 \qquad xy=(a^2-1)^2=:\pi.
\]

In (16a), \(R\) has denominator \(\pi\) and degree-four numerator, while
\(H_2^+\) has denominator \(\pi^2\) and degree-six numerator.  Inspection
of (13)--(14) shows that, after multiplication by \(\pi^4\), the
difference between any entry of \(G_Z\) and the corresponding entry in
(16) is a polynomial in \(a\) of degree at most twenty.  The verifier
evaluates every one of the \(40^2\) differences at the twenty-one exact
values

\[
 a=0,2,3,\ldots,21.
\]

All vanish.  A degree-at-most-twenty polynomial with these twenty-one
distinct roots is zero: successively divide by \(a-a_j\); after twenty-one
divisions a nonzero remainder would have negative degree.  This proves
(16) for every nontied \(a\).  The tied value is handled independently by
(17a), and a zero second singular value follows either from \(a=0\) or by
interchanging the axes.  Thus no sampled-amplitude assumption remains.

For a scaled-unitary single pair \(Z=aI_2\), \(H_2\) has eigenvalues
\(4a^2,4a^2,0,\ldots,0\).  The variational definition

\[
 \sum_{j=1}^4\lambda_j(S)
 =\max_{P^2=P=P^\dagger,\ \operatorname{Tr}P=4}\operatorname{Tr}(PS)
\tag{17}
\]

keeps the positive two-plane and optimizes over an arbitrary two-plane in
the tied six-space.  Let \(R_+\) project onto the positive two-plane and
\(L_0=I-R_+\).  Exact contraction gives

\[
 L_0H_{40}L_0=0,
 \qquad
 \operatorname{Tr}R_+
  \bigl(H_{40}-H_2b_1b_1^\dagger\bigr)=-8a^4.
\tag{17a}
\]

Thus every possible extra two-plane in the tied space gives the same
straight deficit coefficient \(8a^4\).  For an arbitrary approaching
sequence, choose maximizing four-projectors in (17) and take a convergent
subsequence.  Its limit contains \(R_+\); the leading deficit
\(8q_2\) is nonnegative, the cubic operator vanishes by (14a), and (17a)
is independent of the remaining tied two-plane.  This proves (12) without
a tangent-cone assumption or a differentiability claim. \(\square\)

The dependency-free verifier

```text
python3 verification/verify_dth_product_arc_closure.py
```

reconstructs (13)--(17a) over \(\mathbb Q(i)\), checks the universal
single-pair formula at rank one and unequal full rank, audits equal and
unequal representative multi-pair charts, identifies the rank-one kernel
coordinate by coordinate, and verifies that all two-planes in the tied
six-space have the same fourth coefficient.  The proof does not use a
sampled multi-pair spectrum.

## 3. A finite blow-up lemma

We record the elementary compactness step used to pass from (8) to curved
arcs and arbitrary sequences.

### Lemma 2 (strict quartic strata are stable)

Let \(h_n=r_n\delta_n\in W\), where \(r_n\downarrow0\),
\(\|\delta_n\|=1\), and \(\delta_n\to\delta\).  If either

\[
 q_2(\delta)>0
\tag{18}
\]

or

\[
 q_2(\delta)=0,\qquad q_4(\delta)>0,
\tag{19}
\]

then \(\Delta(z_0+h_n)>0\) for all sufficiently large \(n\).

#### Proof

The first case follows immediately from the isolated eight-cluster
expansion (6), uniformly on a compact neighborhood of \(\delta\).

For the second case, no metric error bound for the zero cone is needed.
The uniform cluster reduction and (14a) have the form

\[
 S_{\rm eff}(r,v)=I+r^2H(v)+r^4K(v)+O(r^5),
\tag{20}
\]

for \(v\) in a compact part of the unit sphere of \(W\).  Both \(H\) and
\(K\) are continuous Hermitian matrix functions.  Choose a rank-four
projector \(P_n\) attaining the variational maximum for
\(S_{\rm eff}(r_n,\delta_n)\), and pass to a subsequence
\(P_n\to P\).  The order-two variational problem implies that \(P\)
maximizes \(\operatorname{Tr}(PH(\delta))\).

Subtracting the nonnegative leading deficit gives

\[
 {\Delta(z_0+h_n)\over r_n^4}
 ={8q_2(\delta_n)\over r_n^2}+J(\delta_n,P_n)+o(1),
\tag{20a}
\]

where \(J\) is the continuous fourth deficit obtained from (13)--(14).
The first term on the right is nonnegative.  At every zero-cone point
other than a scaled-unitary single pair, the maximizing four-space is the
isolated space used in Lemma 1, so

\[
 J(\delta,P)=q_4(\delta).
\]

At the scaled-unitary tie, every maximizing projector contains \(R_+\),
and (17a) gives the same identity for every choice of its other two
directions.  Consequently

\[
 \liminf {\Delta(z_0+h_n)\over r_n^4}
 \ge q_4(\delta)>0.
\]

This proves the claim uniformly across all tied intersections and all
rates at which \(\delta_n\) approaches the zero cone. \(\square\)

## 4. The sole zero quartic chart

By (9), the only nonzero \(\delta\in\mathcal Z\) not covered by Lemma 2 is
a rank-one matrix on one pair.  Site permutations and the local
\(U(2)^3\) stabilizer reduce it to

\[
 \delta=|110\rangle.
\tag{21}
\]

Let \(L_{12}\subset W\) be the same-pair space spanned by
\(|ij0\rangle\), \(i,j\in\{1,2\}\), and write

\[
 h=x+y,
 \qquad x\in L_{12},\quad y\perp L_{12}.
\tag{22}
\]

### Lemma 3 (conical transverse stability)

There are \(c,\epsilon>0\) such that, whenever

\[
 0<\|x\|<\epsilon,
 \qquad
 \left\|{x\over\|x\|}-|110\rangle\right\|<\epsilon,
 \qquad
 \|y\|<\epsilon\|x\|,
\]

one has

\[
 \boxed{
 \Delta(z_0+x+y)\ge\Delta(z_0+x)+c\|y\|^2.}
\tag{23}
\]

#### Proof

First, the derivative in \(y\) at \(y=0\) vanishes exactly.  Indeed,
\(z_0+x\) has third-site factor \(e_0\), while every term of \(y\) has
third index in \(e_0^\perp\).  The unitary

\[
 \operatorname{diag}(1,e^{i\theta},e^{i\theta})
\]

on the third site fixes \(z_0+x\) and multiplies \(y\) by
\(e^{i\theta}\).  Invariance of \(\Delta\) kills every term linear in
\(y\).

Put \(r=\|x\|\), write \(u=\|y\|\), and put \(Z=x/r\).  Because \(Z\) stays close to a
rank-one single-pair matrix, it stays a fixed distance from the
scaled-unitary tie and from every multi-pair zero-cone branch.  The explicit
zero-cone classification makes this quantitative: in a closed sufficiently
small neighborhood of \(|110\rangle\), a zero of \(q_2(Z+w)\) with
\(w\in L_{12}^\perp\) would have two active pairs, which would force the
same-pair matrix \(Z\) to be a scaled unitary.  This is impossible in that
neighborhood, so the only zero is \(w=0\).  Moreover (14a) and (16) give
the uniform Taylor formula

\[
 8q_2(Z+w)=w_{\mathbb R}^{\mathsf T}G_Zw_{\mathbb R}
            +O(\|w\|^3),
 \qquad G_Z\big|_{L_{12}^\perp}\succeq2I.
\]

The coefficients and the remainder are continuous on the closed
single-pair neighborhood.  Shrinking it until the remainder is at most
\(\|w\|^2\) gives constants
\(c_0,C_0>0\) such that

\[
 8q_2(Z+w)\ge c_0\|w\|^2
 \quad(w\in L_{12}^\perp,\ \|w\|<\epsilon),
 \qquad
 0\le\Delta(z_0+x)\le C_0r^4.
\tag{23a}
\]

We now cover three explicit regimes.

1. **Outer regime, \(u\ge Mr^2\).**  The uniform cluster expansion (20),
   with \(w=y/r\), and (23a) give

   \[
    \Delta(z_0+x+y)-\Delta(z_0+x)
    \ge c_0u^2-C_1r^4.
   \]

   Choose \(M^2\ge2C_1/c_0\).  The right side is then at least
   \((c_0/2)u^2\).  This covers the entire range
   \(Mr^2\le u<\epsilon r\); no assertion based only on an unbounded
   quotient is being used.

2. **Feshbach annulus, \(mr^2\le u\le Mr^2\).**  Write
   \(y=r^2\eta\).  Here \(m\le\|\eta\|\le M\).  Subtract the same-pair
   value before applying (8).  Formula (16) has no row or column coupling
   \(L_{12}\) to \(L_{12}^\perp\), and its least transverse eigenvalue is
   two.  Uniformity on the compact \((Z,\eta)\)-annulus gives

   \[
    \Delta(z_0+x+y)-\Delta(z_0+x)\ge u^2
   \]

   after reducing \(\epsilon\).

3. **Inner regime, \(u<mr^2\).**  At \(z_0+x\), the top-four cluster is
   isolated from the remaining cluster by at least \(c_2r^2\).  The
   variational resolvent expansion therefore gives a transverse Hessian
   bounded below by one and a third-order Taylor remainder bounded by

   \[
    C_2{u^3\over r^2}.
   \]

   This estimate follows directly by differentiating the finite resolvent
   in (13).  The internal reduced resolvents have norm at most
   \((c_2r^2)^{-1}\); the slice-parity identity kills the bare internal
   linear block, so every use of such a resolvent is accompanied by a
   factor \(r\).  Even the crude bound obtained by allowing two resolvents
   is \(C_2u^3/r^2\).  Choose
   \(m\le(2C_2)^{-1}\).  The remainder is at most \(u^2/2\), so the
   difference is at least \(u^2/2\).

Taking \(c=\min(c_0/2,1/2)\) proves (23) in all three regimes.

This argument also explains why the eight zero directions in (10) cause no
loss: they are exactly \(L_{12}\), already assigned to \(x\), and there is
no mixed row or column between them and \(L_{12}^\perp\). \(\square\)

The base term in (23) is globally nonnegative, not merely perturbatively
nonnegative.  Namely

\[
 z_0+x=X\otimes e_0
\]

for a \(3\times3\) coefficient matrix \(X\), so the established
deficient-support theorem gives

\[
 \Delta(z_0+x)\ge0.
\tag{24}
\]

Equality in (24) means \(\operatorname{rank}X\le2\).

## 5. Proof of the product-corner theorem

Suppose, to the contrary, that a sequence with negative deficit converges
to the product orbit.  Put it in the slice (4), write

\[
 h_n=r_n\delta_n,
 \qquad \|\delta_n\|=1,
\]

and pass to a convergent subsequence \(\delta_n\to\delta\).

If \(q_2(\delta)>0\), Lemma 2 gives a contradiction.  If
\(q_2(\delta)=0\) but \(q_4(\delta)>0\), the same lemma gives a
contradiction, including the scaled-unitary tied cluster by (12).

The only remaining case is a rank-one single pair.  Reduce it to (21), and
split every \(h_n=x_n+y_n\) as in (22).  Then
\(y_n=o(\|x_n\|)\), so Lemma 3 and (24) give

\[
 \Delta(z_0+h_n)
 \ge\Delta(z_0+x_n)+c\|y_n\|^2\ge0,
\]

again a contradiction.  This proves (2).  The equality assertion follows
from the strict alternatives in Lemmas 2--3 and the equality statement in
(24).

Every complex analytic arc is a special case of this sequence argument.
Weight-one jets, arbitrary physical sites and pairs, and unit-norm
corrections have already been absorbed by Sections 1 and (1).  Hence no
unexamined valuation or nonsmooth singular-value branch remains at the
product corner.

## 6. Exact scope

What is now proved:

1. the product orbit is a genuine local nonnegative set for DTH;
2. all curved arcs through it are nonnegative, not only straight rays;
3. all multi-pair zero-Hessian directions are quartically repelled;
4. the unique quartic kernel is absorbed by the exact deficient-support
   branch;
5. the scaled-unitary sixfold cutoff cannot produce a hidden negative
   branch.

What remains:

1. DTH at full-local-rank points separated from the factor equality set;
2. the implication from DTH to square-zero positivity, if DTH is proved;
3. the compatible common-plane/square-zero cross inequality;
4. unrestricted three-copy and all-copy Werner positivity.
