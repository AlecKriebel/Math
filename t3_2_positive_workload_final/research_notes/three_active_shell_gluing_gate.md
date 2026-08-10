# The fixed-top shell quasipotential and the remaining three-active gluing gate

## 1. Result and status

Every affine-feasible all-active tier failure of a fixed residual support
pair has the same whole-top linkage support. This permits one
network-dependent, cone-independent constrained-entropy shell potential.
That potential has strictly negative physical-time drift on **all failed
all-active cones of the pair at once**.

For the rank-one deficiency-zero two-complex top shape, Propositions
5.2--5.4 go further: a rate-adjusted entropy handles 276 support pairs, and
an orientation/rate-dependent positive linear workload handles the 12
curvature-seam pairs. Thus all 288 pairs of this shape are closed at the
all-active physical-time generator level.

Propositions 5.5--5.6 close the 24 rank-two pairs and the 91 arbitrary
directed three-complex rank-one pairs, respectively. Hence all 403 pairs
are now closed at the all-active physical-time generator level. This does
not yet prove recurrence: lower active-coordinate interfaces remain. The
shell potential itself can have positive drift on a cone where the top
linkage is not flat. Sections 6--8 record exact counterexamples to several
tempting generic global glues; those counterexamples explain why the
shape-specific potentials below are needed.

The support and exponent claims are certified by
*src/three_active_gluing_gate.py*. Its local analytic flag records the
independently audited theorem proved here and is separated explicitly from
the false pair-level and global recurrence flags.

## 2. One fixed top support per pair

Let \(P=(L_0,L_1)\) be one of the 403 ordered support pairs having an
affine-feasible all-active failed descriptor. For every such descriptor,
Proposition 3.1 of *three_active_flat_phase_classification.md* gives a unique
whole-top linkage.

The exact enumeration proves the stronger pairwise statement:

> For a fixed \(P\), the side and support of the whole-top linkage are the
> same for every affine-feasible all-active failed descriptor of \(P\).

Call this fixed support \(T\), call the other support \(R\), and let
\(S_T\) be the stoichiometric span of \(T\). There are 403 pairs and 35
possible fixed supports. The rank of \(S_T\) is one or two.

Every failed descriptor supplies \(w>0\) with
\(S_T\subset w^\perp\). Hence \(S_T^\perp\) contains a strictly positive
vector, and every affine fiber parallel to \(S_T\) in the nonnegative
orthant is compact.

## 3. The constrained shell entropy

Put

\[
 V(z)=\sum_{i=1}^3 \bigl[z_i(\log z_i-1)+1\bigr],
\tag{3.1}
\]

with the continuous convention at zero. Choose a full-row-rank matrix \(B\)
whose row space is \(S_T^\perp\), and define

\[
 \Phi_T(q)=
 \min\{V(z):z\in\mathbb R_{\ge0}^3,\ Bz=q\},
 \qquad
 F_T(x)=\Phi_T(Bx).
\tag{3.2}
\]

Strict convexity gives a unique minimizer, denoted \(z(x)\). Whenever the
fiber contains a strictly positive point, this minimizer is interior: a
segment from a hypothetical boundary minimizer toward the positive point
has derivative \(-\infty\) in every newly positive coordinate and therefore
strictly decreases \(V\). The positive invariant in the row space of \(B\)
makes every feasible set compact. It
also makes \(F_T\) proper: if \(|x|\to\infty\), the positive invariant
level tends to infinity, so every point in the fiber has divergent total
mass and the minimum in (3.2) tends to infinity.

Every top reaction vector \(\nu\in S_T\) satisfies \(B\nu=0\). Therefore

\[
 F_T(x+\nu)=F_T(x)
 \quad\hbox{and}\quad
 \mathcal L_TF_T(x)=0
\tag{3.3}
\]

exactly, at every state and for every choice of top rates and orientation.

## 4. Center comparison on a flat top tier

### Lemma 4.1 (multiplicative center comparison)

Let \(x_n\) be an all-active sequence on which all monomials sourced in
\(T\) lie in one D-tier. Then

\[
 \log z(x_n)=\log x_n+O(1)
\tag{4.1}
\]

coordinatewise. In particular every coordinate of \(z(x_n)\) tends to
infinity.

#### Rank-one proof

Write \(S_T=\operatorname{span}\{s\}\). Coordinates with \(s_i=0\) are
unchanged along a fiber. On the other coordinates, top-tier flatness gives

\[
 s\cdot\log x_n=O(1).
\tag{4.2}
\]

The minimizer has the form \(z=x+t s\), and its interior first-order
condition is

\[
 s\cdot\log(x+t s)=0.
\tag{4.3}
\]

The left side is strictly increasing in \(t\), because its derivative is

\[
 \sum_i\frac{s_i^2}{x_i+t s_i}>0.
\tag{4.4}
\]

If \(t>0\), then every term

\[
 s_i\log\frac{x_i+t s_i}{x_i}
\tag{4.5}
\]

is nonnegative; if \(t<0\), every term is nonpositive. The sum of these
terms equals the bounded difference between (4.3) and (4.2). Thus each
term in (4.5) is bounded in absolute value, so every ratio
\((x_i+t s_i)/x_i\) is bounded above and away from zero. This proves
(4.1).

#### Rank-two proof

Now \(S_T^\perp=\operatorname{span}\{w\}\) for one \(w>0\). Flatness and
the fact that the reaction differences of \(T\) span \(w^\perp\) give

\[
 \log x_n=\lambda_n w+O(1).
\tag{4.6}
\]

The KKT equation for (3.2) gives
\(\log z(x_n)=\mu_n w\). The conserved value satisfies

\[
 w\cdot x_n
 \asymp \sum_i w_i e^{\lambda_nw_i}
 \quad\hbox{and}\quad
 w\cdot z(x_n)=\sum_i w_i e^{\mu_nw_i}.
\tag{4.7}
\]

The two conserved values are equal. Monotonicity of the final sum and
\(w_i>0\) imply \(\mu_n-\lambda_n=O(1)\), proving (4.1).
\(\square\)

### Lemma 4.2 (bounded-jump envelope expansion)

Suppose, more generally, that \(x_n\) and a bounded vector \(\nu\) satisfy

\[
 \inf_{0\le t\le1}\min_i z(x_n+t\nu)_i\longrightarrow\infty.
\tag{4.8}
\]

Then

\[
 F_T(x_n+\nu)-F_T(x_n)
 =\log z(x_n)\cdot\nu+o(1)
\tag{4.9}
\]

In particular this holds for every vector \(\nu\) in the finite
reaction-jump set along the sequences of Lemma 4.1.

#### Proof

Put \(q_n(t)=B(x_n+t\nu)\). At an interior minimizer, the KKT equation is
\(\log z=B^{\mathsf T}\lambda\), while the derivative of the value function
is \(\nabla\Phi_T(q)=\lambda\). The dual Jacobian is

\[
 B\,\operatorname{diag}(z)\,B^{\mathsf T}.
\tag{4.10}
\]

Its least eigenvalue is bounded below by a fixed positive constant times
\(\min_i z_i\). Assumption (4.8) therefore makes

\[
 D^2\Phi_T(q_n(t))
 =\bigl(B\operatorname{diag}(z(x_n+t\nu))B^{\mathsf T}\bigr)^{-1}
 =o(1)
\tag{4.11}
\]

uniformly for \(0\le t\le1\). The integral Taylor remainder proves (4.9).

For a flat sequence, (4.8) follows by contradiction. If it failed, choose
\(t_n\in[0,1]\) and a subsequence on which one center coordinate stayed
bounded. But
\(\log(x_n+t_n\nu)-\log x_n=o(1)\) uniformly in \(t_n\), so
\(x_n+t_n\nu\) is another all-active flat sequence. Lemma 4.1 makes its
center multiplicatively comparable to it, contradicting the bounded center
coordinate. \(\square\)

## 5. One shell potential closes every failed cone of a fixed pair

### Proposition 5.1 (fixed-top failed-cone drift)

Fix arbitrary strongly connected orientations and positive rates on
\(T\) and \(R\). For every all-active tier sequence \(x_n\) realizing a
failed descriptor of \(P\),

\[
 \mathcal L F_T(x_n)\longrightarrow-\infty.
\tag{5.1}
\]

Indeed, (3.3) deletes the top contribution exactly. Let \(M\) be the
highest D-tier of sources in \(R\), and normalize all source propensities
by one source in \(M\). Sources in \(M\) then have finite positive limiting
ratios and every lower source has ratio tending to zero.

The set \(M\) is proper. Otherwise \(R\), as well as \(T\), would be flat
in the descriptor workload, putting the full stoichiometric space in a
two-dimensional hyperplane; all enumerated incidences instead have full
rank three. Strong connectivity of \(R\) forces an edge \(y\to y'\) from
\(M\) to \(R\setminus M\). For that edge,

\[
 \log z(x_n)\cdot(y'-y)
 =\log x_n\cdot(y'-y)+O(1)\longrightarrow-\infty.
\tag{5.2}
\]

Edges within \(M\) have only \(O(1)\) increments, by (4.1). One must be
slightly more careful with a positive increment from a lower source, because
a vanishing propensity ratio need not dominate an unrelated logarithm.
Here the logarithm is not unrelated. If \(u\to v\) has a divergent positive
increment, put
\[
 g_n=\log z(x_n)\cdot(v-u)>0.
\]
Then \(g_n=\log(x_n^v/x_n^u)+O(1)\), and, after normalization by a source
\(y_0\in M\),
\[
 \frac{x_n^{\underline u}}{x_n^{\underline{y_0}}}\,g_n
 \le C\frac{x_n^v}{x_n^{y_0}}\,g_ne^{-g_n}
 \longrightarrow0.
\tag{5.3}
\]
The target \(v\) is itself a complex of \(R\), so its monomial is no larger
than a top-tier monomial. Positive bounded increments from lower tiers have
vanishing normalized source propensity directly. Thus every normalized
positive contribution is \(O(1)\), while the forced exit (5.2) tends to
minus infinity. Lemma 4.2 gives

\[
 \frac{\mathcal L_RF_T(x_n)}
      {x_n^{\underline{y_0}}}
 \longrightarrow-\infty
\tag{5.4}
\]

for any \(y_0\in M\). This proves (5.1).

This is a physical-time generator statement. It is uniform over the finite
choice of failed cones for a fixed pair and ignores every faster top jump
without tracing it.

### Proposition 5.2 (the rate-adjusted entropy branch)

Suppose the fixed top support has two complexes,
\(T=\{y,z\}\), and give its necessarily reversible orientation rates
\(\kappa_{yz},\kappa_{zy}>0\). Choose \(\theta>0\) so that

\[
 \kappa_{yz}\theta^y=\kappa_{zy}\theta^z
\tag{5.5}
\]

and define the proper rate-adjusted entropy

\[
 U_\theta(x)=
 \sum_i\left[x_i\left(\log\frac{x_i}{\theta_i}-1\right)+\theta_i\right].
\tag{5.6}
\]

Let \(d=z-y\), and let \(x_n\) realize a failed all-active flat-top
descriptor. Put

\[
 \alpha_n=x_n^y\asymp x_n^z,\qquad
 \beta_n=\max_{u\in R}x_n^u.
\tag{5.7}
\]

For every changed coordinate \(i\), select either endpoint \(e\in\{y,z\}\)
with \(e_i>0\). The associated **curvature cofactor** is \(e-\mathbf e_i\).
If every such cofactor lies at or below the maximal \(R\)-source D-tier,
then

\[
 \mathcal L U_\theta(x_n)\longrightarrow-\infty.
\tag{5.8}
\]

To prove this, bounded-jump Taylor expansion and all-active
falling-factorial comparison give, uniformly on the flat tier,

\[
\begin{aligned}
 \mathcal L_TU_\theta(x_n)
 &=
 (a_n-b_n)\log\frac{b_n}{a_n}
 O\left(\alpha_n\sum_{i:d_i\ne0}\frac1{x_{n,i}}\right)\\
 &\le
 C\alpha_n\sum_{i:d_i\ne0}\frac1{x_{n,i}},
\end{aligned}
\tag{5.9}
\]

where \(a_n=\kappa_{yz}x_n^y\) and
\(b_n=\kappa_{zy}x_n^z\). Replacing monomials by falling factorials only
changes the displayed remainder: flatness makes
\(\log(b_n/a_n)=O(1)\). For a changed coordinate \(i\),
\(\alpha_n/x_{n,i}\) is comparable to the monomial of one curvature
cofactor. The hypothesis therefore makes (5.9) \(O(\beta_n)\).

The lower linkage has a proper maximal tier and a forced strong-orientation
exit from it. The proof of Proposition 5.1, now with
\(\log(x_n/\theta)=\log x_n+O(1)\), gives

\[
 \frac{\mathcal L_RU_\theta(x_n)}{\beta_n}
 \longrightarrow-\infty.
\tag{5.10}
\]

Equations (5.9)--(5.10) prove (5.8). On an all-active descriptor satisfying
the ordinary descending-source condition, the fixed linear adjustment in
(5.6) does not alter its strict logarithmic descent. Consequently one
single \(U_\theta\) handles every all-active cone of any support pair for
which all failed descriptors obey the cofactor condition.

The exact certificate applies this condition to all 966 failed incidences
whose fixed top is a rank-one deficiency-zero two-complex support. It
certifies:

- 950 incidences satisfy the condition;
- 16 incidences fail it;
- 276 of the 288 support pairs satisfy it on every failed descriptor;
- the remaining 12 pairs have 44 safe failed incidences and 16 genuinely
  curvature-obstructed incidences.

Thus the two-complex all-active problem is reduced exactly to those 16
incidences on 12 pairs. This is not yet a full T3-2 branch because lower
active-coordinate interfaces still need their own physical-time theorem.

### Proposition 5.3 (exact linear descent on the 16 curvature seams)

The 16 incidences excluded by Proposition 5.2 nevertheless have a much
simpler local potential. For the eight \(B\)-side incidences, put

\[
 H_B(x)=2A+B+3C,
\tag{5.11}
\]

and for their eight \(B/C\)-swaps put

\[
 H_C(x)=2A+3B+C.
\tag{5.12}
\]

Both top complexes \(2A\) and \(B+C\) have value four under either
applicable workload, so

\[
 \mathcal L_TH_B=0
 \quad\hbox{or}\quad
 \mathcal L_TH_C=0
\tag{5.13}
\]

exactly. On the \(B\)-side lower menu
\(\{0,A,B,2B,A+B\}\), the \(H_B\)-values are respectively

\[
 0,\ 2,\ 1,\ 2,\ 3.
\tag{5.14}
\]

If \(A+B\) is present, it is both the unique \(H_B\)-maximal complex and
the unique maximal lower D-tier in every associated curvature obstruction.
Every strong orientation has an edge leaving it, and that edge has strictly
negative \(H_B\)-increment. Every positive \(H_B\)-edge has a strictly
lower source D-tier, so

\[
 \mathcal L_RH_B(x_n)\longrightarrow-\infty.
\tag{5.15}
\]

The only obstruction support without \(A+B\) is
\(\{0,A,B,2B\}\). Its \(H_B\)-maximal set is \(\{A,2B\}\).
Strong connectivity forces an edge from this set to \(\{0,B\}\).
In all three obstruction descriptors on this support, both \(A\) and \(2B\)
strictly dominate both \(0\) and \(B\) in D-order. Thus whichever maximal
vertex supplies the forced exit, its negative propensity dominates every
positive cross-cut propensity, proving (5.15) again. The \(C\)-side proof
is the exact coordinate swap.

The certificate checks the cut and every strict D-comparison separately for
all 16 incidences and all 12 support pairs. This closes the **local**
curvature seam for arbitrary strong orientations and positive rates. It
does not by itself glue \(H_B\) or \(H_C\) to \(U_\theta\) on the other
all-active cones; that remains the global interface problem.

There are exactly two exceptions where no glue is needed. For

\[
 \{2A,B+C\}\ \&\ \{0,A,B,A+B\}
\tag{5.16}
\]

and its \(B/C\)-swap, \(A+B\) (respectively \(A+C\)) is both the unique
linear-workload maximum and, on every all-active sequence, strictly above
all unary and zero source monomials. Every strong orientation therefore
has a strictly negative workload edge sourced at the unique quadratic
maximum, and all positive edges have lower-order sources. Thus \(H_B\)
(respectively \(H_C\)) is a global all-active Foster workload for these two
support pairs.

No other seam pair has this property. At the affine-feasible descriptor
\(w=(1,1,1)\), each of the remaining ten pairs admits an explicit directed
Hamiltonian cycle whose earliest nonzero workload tier contains a positive
edge. For example,

\[
 0\to A\to2B\to A+B\to0
\tag{5.17}
\]

has the positive quadratic edge \(2B\to A+B\). Taking its rate sufficiently
large relative to the other fixed positive cycle rates makes the leading
\(H_B\)-drift positive. The certificate records one such exact
counterorientation for every remaining pair. Consequently the global
linear branch removes two pairs and two obstruction incidences; ten pairs
and fourteen obstruction incidences still need an interface theorem.

### Proposition 5.4 (rate-dependent linear closure of all 12 seam pairs)

The final sentence of Proposition 5.3 is true only for the fixed displayed
workloads. Allowing the workload to depend on the actual orientation and
rates removes the remaining seam. On the \(B\)-side define

\[
 H_b(x)=2A+bB+(4-b)C,\qquad 0<b<4.
\tag{5.18}
\]

Both \(2A\) and \(B+C\) have \(H_b\)-value four, so
\(\mathcal L_TH_b=0\) exactly. The \(C\)-side uses the swapped family
\(2A+(4-b)B+bC\).

For a \(B\)-side lower support, let

\[
 \Gamma_y(b)=
 \sum_{y\to v}\kappa_{yv}\{H_b(v)-H_b(y)\}.
\tag{5.19}
\]

The lower generator is the exact polynomial

\[
 \mathcal L_RH_b
 =\Gamma_0+\Gamma_A A+\Gamma_BB
  +\Gamma_{2B}B(B-1)+\Gamma_{A+B}AB,
\tag{5.20}
\]

with absent-source terms omitted.

First suppose \(A+B\) and \(2B\) are both present. At \(b=2\), \(H_b\)
is twice total molecularity. Hence

\[
 \Gamma_{A+B}(2)\le0,\qquad \Gamma_{2B}(2)\le0.
\tag{5.21}
\]

If the first inequality is strict, take \(b=2\). If it is equality, every
outgoing \(A+B\)-edge must target the only other quadratic complex \(2B\).
Strong connectivity then forces a lower-degree exit from \(2B\), so
\(\Gamma_{2B}(2)<0\). Since an \(A+B\to2B\) edge has increment \(b-2\),
choosing \(b<2\) sufficiently close to two makes

\[
 \Gamma_{A+B}(b)<0,\qquad \Gamma_{2B}(b)<0.
\tag{5.22}
\]

The negative \(AB\)-term dominates every unary term because
\(AB/A=B\to\infty\) and \(AB/B=A\to\infty\), while the nonpositive
\(B(B-1)\)-coefficient prevents a competing positive quadratic term.
Thus (5.20) tends to minus infinity on every all-active sequence. If
\(A+B\) is the only quadratic lower complex, its strong outgoing edge is
lower-degree, so \(\Gamma_{A+B}(2)<0\) directly.

It remains to treat the only double-only support
\(\{0,A,B,2B\}\). Aggregate the outgoing rates as

\[
\begin{array}{lll}
 a_0:A\to0, &a_1:A\to B, &a_2:A\to2B,\\
 d_0:2B\to0,&d_A:2B\to A,&d_1:2B\to B.
\end{array}
\tag{5.23}
\]

Then

\[
\begin{aligned}
 \Gamma_A(b)
   &=-2a_0+(b-2)a_1+(2b-2)a_2,\\
 \Gamma_{2B}(b)
   &=2d_A-b(2d_0+2d_A+d_1).
\end{aligned}
\tag{5.24}
\]

The first affine function is negative below its root

\[
 r_A=\frac{2(a_0+a_1+a_2)}{a_1+2a_2}\ge1
\tag{5.25}
\]

when the denominator is nonzero, and is negative for every \(b\) otherwise.
The second is negative above

\[
 r_2=\frac{2d_A}{2d_0+2d_A+d_1}\le1.
\tag{5.26}
\]

Equality \(r_A=r_2=1\) would say that every \(A\)-edge goes to \(2B\)
and every \(2B\)-edge goes to \(A\), making \(\{A,2B\}\) a closed set.
Strong connectivity forbids this. Therefore \(r_2<r_A\), with the evident
infinite-root convention, and one may choose

\[
 0<b<4,\qquad r_2<b<r_A.
\tag{5.27}
\]

Then both coefficients in (5.24) are strictly negative. The negative
\(B(B-1)\)-term dominates the possibly positive linear \(B\)-term, and
the negative \(A\)-term handles every hierarchy with \(A\) dominant.
Again \(\mathcal L_RH_b\to-\infty\).

The exact support certificate partitions the 12 seam pairs into eight
double-and-mixed supports, two mixed-only supports, and two double-only
supports. Equations (5.21)--(5.27), plus the \(B/C\) swap, prove:

> For every one of the 12 seam support pairs, every strong orientation,
> and every fixed positive rate vector, there is one \(b=b(\kappa)\in(0,4)\)
> such that the proper linear workload \(H_b\) has physical-time generator
> tending to minus infinity along every all-active divergent sequence.

Combining this with Proposition 5.2 closes the all-active interface for all
288 rank-one deficiency-zero two-complex-top pairs: 276 use
\(U_\theta\), and the 12 curvature-seam pairs use \(H_b\). This statement
still does not cover two-active, one-active, or boundary sequences.

### Proposition 5.5 (the 24 rank-two tops have an exact linear workload)

The rank-two branch has no gluing problem. In all 24 failed incidences the
other linkage is exactly

\[
 R=\{0,C\}
\tag{5.28}
\]

in the fixed coordinate convention. Let \(w>0\) be the descriptor workload.
Every complex of the whole-top support \(T\) has the same \(w\)-value, so

\[
 H_w(x)=w\cdot x,
 \qquad \mathcal L_TH_w=0
\tag{5.29}
\]

for every orientation and every rate vector on \(T\). Strong connectivity
of the two-vertex linkage \(R\) supplies both directed reactions. Therefore
the full generator is exactly

\[
 \mathcal LH_w(x)
 =w_C\{\kappa_{0C}-\kappa_{C0}C\}
 \longrightarrow-\infty
 \qquad(C\to\infty).
\tag{5.30}
\]

The workload is proper because every entry of \(w\) is positive. The finite
certificate freezes the top-size histogram \(17,6,1\) for sizes \(4,5,6\),
and the workload histogram: 22 incidences use \((1,1,1)\), one uses
\((2,1,1)\), and one uses \((1,2,1)\). Thus one exact physical-time linear
Foster workload handles every all-active sequence for each of these 24
pairs, not only its failed cone.

### Proposition 5.6 (the 91 directed triple tops have one factorial-linear potential)

After permuting coordinates, every remaining rank-one top support is

\[
 T=\{2A,A+B,2B\}.
\tag{5.31}
\]

Give its three-vertex reaction graph an arbitrary strongly connected
orientation and arbitrary positive rates. Lemma 4.1 of
*certified_exact_shielded_seam.md* constructs a rate-dependent constant
\(d\in\mathbb R\) such that

\[
 V_d(x)=\log(A!)+\log(B!)+\log(C!)+dA
\tag{5.32}
\]

is proper and obeys the global discrete estimate

\[
 \mathcal L_TV_d(x)\le K(1+A+B).
\tag{5.33}
\]

This estimate uses only the endpoint signs forced by strong connectivity;
it does not assume reversibility or complex balance.

Consider first a failed all-active exact-tier sequence \(x_n\). Flatness of
\(T\) gives \(A_n\asymp B_n\); write \(N_n=A_n+B_n\). Let \(M\) be the
maximal source tier of the other linkage \(R\), and let

\[
 \beta_n=\max_{y\in R}x_n^{\underline y}.
\tag{5.34}
\]

The set \(M\) is proper, since otherwise both linkage stoichiometric spaces
would lie in the failed workload hyperplane, contradicting the certified
full rank of the pair. Strong connectivity forces an edge from \(M\) to its
complement. The exact factorial increment on that edge tends to minus
infinity. Edges inside \(M\) have bounded increments. If a lower-tier edge
has a positive divergent increment \(g_n\), its normalized contribution is
bounded by \(C g_ne^{-g_n}\to0\), exactly as in (5.3). Consequently

\[
 \frac{\mathcal L_RV_d(x_n)}{\beta_n}\longrightarrow-\infty.
\tag{5.35}
\]

The lower linkage necessarily contains a source involving \(A\) or \(B\):
otherwise its difference space, together with the rank-one top space, would
have rank at most two. Since every vertex of a strongly connected graph is
a source and \(A_n\asymp B_n\asymp N_n\), this gives

\[
 \beta_n\ge cN_n.
\tag{5.36}
\]

Equations (5.33)--(5.36) imply

\[
 \mathcal LV_d(x_n)\longrightarrow-\infty
\tag{5.37}
\]

on every failed all-active cone.

On every passing all-active descriptor, the ordinary descending-source
argument applies directly to the same \(V_d\). The correction \(dA\) has a
bounded increment on every reaction, whereas the forced factorial-entropy
exit has a logarithmically divergent negative increment; lower positive
terms are again controlled by \(g e^{-g}\). Thus the fixed correction does
not change the Anderson--Kim tier conclusion. One \(V_d\), chosen from the
actual top orientation and rates, therefore handles every all-active cone
of the pair.

The exact certificate counts 279 failed incidences on 91 pairs, with top
support histogram 270 for \(\{2A,2B,A+B\}\), six for its \(A,C\) version,
and three for its \(B,C\) version. It also verifies in every incidence the
full-rank condition and the presence of a lower source involving a top
species. This is an all-active physical-time generator theorem only; it
does not close any lower-dimensional active-coordinate interface.

## 6. The shell potential is not a global Foster function

Consider

\[
 T=\{2A,B+C\},\qquad
 R=\{0,A,B,2C\},
\tag{6.1}
\]

and the all-active integer sequence

\[
 x_N=(A,B,C)=(N^3,N,N).
\tag{6.2}
\]

This is an affine-feasible **passing** descriptor with weight \((3,1,1)\):
\(2A\) is a proper top source in \(T\). The \(T\)-fiber is

\[
 (N^3-2t,N+t,N+t).
\tag{6.3}
\]

The constrained entropy center solves
\(z_A^2=z_Bz_C\); by symmetry all three coordinates are equal, and

\[
 z_A=z_B=z_C=\frac{N^3+2N}{3}.
\tag{6.4}
\]

Give \(R\) unit rates on the directed cycle

\[
 A\longrightarrow2C\longrightarrow B\longrightarrow0\longrightarrow A.
\tag{6.5}
\]

It is strongly connected. The envelope calculation from Lemma 4.2 applies
directly here because (6.4) has all coordinates tending to infinity. The
first edge has

\[
 F_T(x_N+2C-A)-F_T(x_N)
 =\log z(x_N)\cdot(2C-A)+o(1)
 =3\log N+O(1).
\tag{6.6}
\]

Its source rate is \(\Theta(N^3)\); all other sources in (6.5) have rates
at most \(O(N^2)\). Thus

\[
 \mathcal L_RF_T(x_N)
 =3N^3\log N+O(N^3)>0.
\tag{6.7}
\]

The top linkage contributes zero by (3.3). Hence \(F_T\) is not a global
Foster function, even though ordinary entropy has a strict top-linkage
descent on this sequence.

## 7. Why a finite linear polyhedral selector does not perform the glue

For the same top support, take instead

\[
 P_0=\{2A,B+C\}\ \&\ \{0,A,B,2C\}.
\tag{7.1}
\]

The five canonical primitive representatives of its failed all-active tier
types are

\[
 (2,3,1),\ (3,4,2),\ (3,5,1),\ (4,5,3),\ (7,10,4).
\tag{7.2}
\]

Every corresponding exponential realization has the same population
dominance

\[
 B\gg A\gg C.
\tag{7.3}
\]

Let \(\ell_j(x)=q_j\cdot x+c_j\) be any finite family of affine linear
functions. Along every sequence in (7.2), a minimum selects
lexicographically by

\[
 (q_{j,B},q_{j,A},q_{j,C},c_j),
\tag{7.4}
\]

and a maximum selects by the reverse lexicographic order. Thus the active
slope set is the same on all five sequences. A fixed-temperature
log-sum-exp has the same asymptotic active slopes as the maximum, and a
soft minimum has those of the minimum.

Consequently a finite min/max/log-sum-exp of the five local descriptor
workloads cannot select \(H_w\) according to these five tier cones. This is
a limitation of the proposed construction, not a proof that no common
network-dependent slope or nonlinear monomial-sensitive gate can work.

## 8. A fixed phase-entropy coefficient also fails

The first 966 incidences in the shape table have reversible two-node
rank-one top supports. It is tempting to add a fixed amount of the
within-shell detailed-balance entropy gap

\[
 G_T(x)=V(x)-F_T(x)\ge0.
\tag{8.1}
\]

There are two obstructions.

First, no nonconstant function \(D\) on a finite irreducible top shell can
satisfy \(Q_TD\le0\) pointwise. If \(\pi\) is the shell stationary law,

\[
 \sum_x\pi(x)Q_TD(x)=0.
\tag{8.2}
\]

Pointwise nonpositivity would force equality everywhere, and irreducibility
then forces \(D\) to be constant. Detailed-balance relative entropy is
therefore not generator-superharmonic at every state; near its minimum its
stochastic curvature is positive.

Second, this curvature can be faster than the lower-linkage descent. Take

\[
 T=\{2A,B+C\},\qquad
 R=\{0,A,2B,A+B\},
\tag{8.3}
\]

unit rates on the reversible top pair, and

\[
 x_N=(N^3,N,N^5).
\tag{8.4}
\]

This is a failed flat descriptor of weight \((3,1,5)\), and
\(A^2=BC=N^6\), so \(x_N\) is exactly its constrained entropy center and
\(G_T(x_N)=0\). For either top jump \(\nu\),

\[
 G_T(x_N+\nu)-G_T(x_N)
 =\frac12\sum_i\frac{\nu_i^2}{x_{N,i}}
 +O(N^{-2})
 =\Theta(N^{-1}).
\tag{8.5}
\]

Both top propensities are \(\Theta(N^6)\). Hence

\[
 \mathcal L_TG_T(x_N)=\Theta(N^5)>0.
\tag{8.6}
\]

The largest lower source is \(A+B\), with propensity \(\Theta(N^4)\), and
every bounded-jump entropy increment is \(O(\log N)\). Therefore

\[
 |\mathcal L_R(F_T+\varepsilon G_T)(x_N)|
 =O(N^4\log N)
\tag{8.7}
\]

for each fixed \(\varepsilon\). Equations (8.6)--(8.7) show that

\[
 \mathcal L(F_T+\varepsilon G_T)(x_N)>0
\tag{8.8}
\]

eventually for every fixed \(\varepsilon>0\).

The exact exponent certificate finds 16 such failed incidences on 12 pairs,
all with top support \(\{2A,B+C\}\). The top-curvature exponent exceeds the
maximal lower-source exponent by one in 12 incidences and by two in four.

### 8.1 A single polynomial shell coefficient also fails

One might let the phase coefficient decay with a proper top invariant. The
same pair (8.3) rules out the simplest such repair. Give \(R\) the strong
cycle

\[
 2B\longrightarrow A+B\longrightarrow A\longrightarrow0
 \longrightarrow2B
\tag{8.9}
\]

and put \(M(x)=1+A+B+C\). Both top complexes have molecularity two, so
\(M\) is exactly invariant under \(T\). Consider

\[
 W_p(x)=F_T(x)+M(x)^{-p}G_T(x).
\tag{8.10}
\]

At the failed center (8.4), \(M=\Theta(N^5)\). Equations (8.6)--(8.7)
show that suppressing the positive top curvature requires

\[
 p\ge\frac15.
\tag{8.11}
\]

Now take the passing sequence

\[
 \widehat x_N=(N^6,N^{10},N^{11}),
\tag{8.12}
\]

of weight \((6,10,11)\). Write the point on its top fiber as

\[
 z=(N^6+2r,N^{10}-r,N^{11}-r).
\tag{8.13}
\]

The entropy-center equation \(z_A^2=z_Bz_C\) gives
\[
 N^{10}-r=\Theta(N^9),
\]
so the exact center exponents are

\[
 (\log_Nz_A,\log_Nz_B,\log_Nz_C)\longrightarrow(10,9,11).
\tag{8.14}
\]

The leading lower edge \(2B\to A+B\) in (8.9) therefore has positive
\(F_T\)-increment

\[
 \log z_A-\log z_B=\log N+O(1)
\tag{8.15}
\]

and propensity \(\Theta(N^{20})\). Thus its positive contribution is
\(\Theta(N^{20}\log N)\). The top reverse reaction \(B+C\to2A\) has
propensity \(\Theta(N^{21})\) and entropy decrement
\(-9\log N+O(1)\). Since \(M(\widehat x_N)=\Theta(N^{11})\), making the
scaled top descent dominate (8.15) requires

\[
 p<\frac1{11}.
\tag{8.16}
\]

The leading lower edge \(2B\to A+B\) preserves \(M\), so no coefficient
seam term alters (8.15). At the failed center \(G_T=0\), so coefficient
increments do not alter the leading curvature comparison there either.
The incompatible conditions (8.11) and (8.16) prove that no single power
\(M^{-p}\) glues these two regimes, even for this reversible two-node top
phase.

### 8.2 A fixed entropy-gap-per-shell hinge also fails

A continuous hinge does not repair the same example if its switching level
is a fixed fraction of a positive top invariant. Let \(m_q(x)=q\cdot x\),
where \(q>0\) is any linear invariant of \(T=\{2A,B+C\}\). Necessarily

\[
 2q_A=q_B+q_C,
\tag{8.17}
\]

so on the passing sequence (8.12),

\[
 m_q(\widehat x_N)=\Theta(N^{11}).
\tag{8.18}
\]

The center in (8.13)--(8.14) has

\[
 z_A=\Theta(N^{10}),\qquad
 z_B=\Theta(N^9),\qquad
 z_C=N^{11}-\Theta(N^{10}).
\tag{8.19}
\]

Because \(x-z\in S_T\) and \(\log z\in S_T^\perp\), the entropy gap is the
Bregman divergence

\[
 G_T(x)=\sum_i\left[x_i\log\frac{x_i}{z_i}-x_i+z_i\right].
\tag{8.20}
\]

At \(x=\widehat x_N\), the \(B\)-summand is
\(N^{10}\log N+O(N^{10})\), the \(A\)-summand is
\(\Theta(N^{10})\), and the \(C\)-summand is \(O(N^9)\). Hence

\[
 G_T(\widehat x_N)=N^{10}\log N+O(N^{10}),
 \qquad
 \frac{G_T(\widehat x_N)}{m_q(\widehat x_N)}\longrightarrow0.
\tag{8.21}
\]

Consider the seam-matched candidate

\[
 W_c=F_T+\bigl(G_T-cm_q\bigr)_+,
 \qquad c>0.
\tag{8.22}
\]

Equation (8.21) puts \(\widehat x_N\), and every one-jump neighbor of it,
strictly inside the \(F_T\) branch for all sufficiently large \(N\): the
distance to the seam is \(\Theta(N^{11})\), whereas a bounded jump changes
\(G_T-cm_q\) by \(O(\log N)\). Therefore

\[
 \mathcal L W_c(\widehat x_N)
 =\mathcal L F_T(\widehat x_N)
 =\Theta(N^{20}\log N)>0
\tag{8.23}
\]

by the leading edge \(2B\to A+B\) from (8.9) and (8.15). If \(c=0\), then
\(W_0=V\); equations (8.4)--(8.8) show positive drift at the failed
curvature center. Thus no fixed \(c\ge0\) in (8.22) glues these two
regimes. The obstruction is that the spectator \(C\)-mass dominates every
strictly positive shell invariant while the top-phase entropy gap is only
of order \(N^{10}\log N\).

### 8.3 The canonical shell-Poisson gauge can reverse the averaged sign

For \(T:2A\rightleftarrows B+C\), write the top invariants as

\[
 Q_1=A+2B,\qquad Q_2=A+2C.
\tag{8.24}
\]

On a fixed shell, parameterize states by \(a=A\), with
\(b=(Q_1-a)/2\) and \(c=(Q_2-a)/2\). For unit top rates the stationary
birth--death law satisfies

\[
 \frac{\pi(a+2)}{\pi(a)}
 =\frac{bc}{(a+2)(a+1)}.
\tag{8.25}
\]

Let \(g=\mathcal L_RF_T\), let
\(\bar g=\sum_a\pi(a)g(a)\), and solve

\[
 Q_T\chi=\bar g-g.
\tag{8.26}
\]

If \(\pi(\chi)=0\) is imposed separately on every shell, this natural
canonical gauge is not globally usable. Take unit rates and

\[
 R:\quad0\longrightarrow A+B\longrightarrow A
 \longrightarrow2B\longrightarrow0.
\tag{8.27}
\]

Use shells whose kinetic centers are \((N^3,N,N^5)\), and evaluate at

\[
 \widetilde x_N=
 \left(N,\frac{N^3+N}{2},
 N^5+\frac{N^3-N}{2}\right).
\tag{8.28}
\]

The exact conductance recurrence gives

\[
\begin{aligned}
 \bar g_N&=-(1+o(1))N^4\log N,\\
 \mathcal L_R\chi(\widetilde x_N)
   &=\left(\frac54+o(1)\right)N^4\log N,
\end{aligned}
\tag{8.29}
\]

and therefore

\[
 \bar g_N+\mathcal L_R\chi(\widetilde x_N)
 =\left(\frac14+o(1)\right)N^4\log N>0.
\tag{8.30}
\]

The top-to-lower total propensity ratio is nevertheless
\((2+o(1))N^2\). At \(N=4\), the deterministic high-precision certificate
finds

\[
 \bar g=-455.777293518\ldots,\qquad
 \mathcal L_R\chi=472.748697241\ldots,
\]

so the corrected drift is \(16.971403723\ldots>0\), with Poisson-equation
residual below \(2.7\times10^{-85}\).

This is a gauge obstruction, not an obstruction to the Poisson strategy
itself. Adding a shell function \(c(Q_1,Q_2)\) to \(\chi\) changes
\(\mathcal L_R\chi\). In this same family, normalizing \(\chi\) to vanish
at the left fiber endpoint (which is also its minimum for the tested
\(N\ge3\)) makes the corrected drift negative. A boundary/minimum-gauge
theorem therefore remains a plausible route, but it still needs uniform
cross-shell gradient and properness estimates for every orientation and
rate choice.

There is also an essential interior qualification. Stationary averaging
has negative asymptotic drift when the kinetic center has all three
coordinates divergent. Large shell mass alone is insufficient: a
degenerate shell can be a singleton on the boundary and have positive
\(\bar g\). Such shells must be routed to the lower-active atlas rather than
absorbed into an interior shell theorem.

### 8.4 Divergent top flux before the first lower reaction need not flatten

The same passing sequence (8.12) rules out one further shortcut. Use the
cycle (8.9), and let \(\tau_R\) be the first lower-linkage reaction. At
\(\widehat x_N=(N^6,N^{10},N^{11})\), the dominant top and lower rates are

\[
 \lambda_T(\widehat x_N)
 =(1+o(1))N^{21},\qquad
 \lambda_R(\widehat x_N)
 =(1+o(1))N^{20}.
\tag{8.31}
\]

Thus the number of top jumps before \(\tau_R\) diverges, but is only
\(\Theta_{\mathbb P}(N)\). Top equilibration on this shell requires
\(\Theta(N^{10})\) moves, since \(B\) must fall from \(N^{10}\) to its
center scale \(\Theta(N^9)\). With probability \(1-o(1)\), the first lower
reaction is therefore \(2B\to A+B\) while the state still has the same
passing descriptor. By (8.15),

\[
 \mathbb E_{\widehat x_N}
 \left[F_T(X_{\tau_R})-F_T(\widehat x_N)\right]
 =\log N+O(1)>0.
\tag{8.32}
\]

Consequently

\[
 \lambda_T/\lambda_R\to\infty
 \quad\hbox{and}\quad
 N_T(\tau_R)\to\infty
\tag{8.33}
\]

do not imply a flat killed occupation or a negative first-\(R\) shell
episode. The normalized top trace can be a moving one-directional segment;
its endpoint displacement is of the same order as its jump count. A valid
killed-Green split must retain ordinary-entropy descent during that directed
transport and invoke the shell potential only after reaching a flat central
tube.

## 9. Exact all-active conclusion and remaining interface

The original 403 all-active failed support pairs now split disjointly as

\[
 288+91+24=403.
\tag{9.1}
\]

The two-complex rank-one group is covered by Propositions 5.2--5.4, the
three-complex rank-one group by Proposition 5.6, and the rank-two group by
Proposition 5.5. Each branch supplies one proper, network-dependent
physical-time generator potential that also handles the passing all-active
cones of the same pair. There is therefore no remaining **all-active** shell
gluing gate among these 403 pairs.

This conclusion is deliberately dimension-local. It does not turn a
descriptor workload episode into factorial-entropy descent, control a
moving bounded coordinate, or compose different potentials across
two-active, one-active, and boundary interfaces. Those are the remaining
global obligations before any recurrence theorem can be claimed.

The rank-one overlap has an exact common-top identity. The finite
certificate compares the 403 all-active pairs with the 310 pairs having a
two-active closed rank-one top phase. Their intersection has exactly 298
pairs, and in every one the two-active whole-top mask is the same fixed mask
as the all-active whole-top linkage. Of these, 207 have a two-node
reversible top and 91 have the arbitrary directed triple. A fixed physical
orientation/rate vector therefore selects the same *available*
detailed-balance or factorial-linear correction in both regimes.

This is a finite compatibility fact only. Exactly 286 overlap pairs use
that corrected-factorial potential in the all-active proof (195 two-node
pairs and all 91 triples). The other 12 are the \(H_b\) curvature seams:
their top mask is the same, but their all-active proof switches to a linear
workload because rate-adjusted entropy has excessive top curvature. Those
12 still need a separate common-potential interface, and the two-active
corrected-entropy endpoint theorem must be proved independently.

### Independent audit status

An independent proof replay checked all three disjoint branches in (9.1).
For the 288 two-node cases it verified the rate-adjusted entropy calculation,
the strict coefficient interval for every one of the twelve linear seams,
and every missing-edge convention. For the 91 directed-triple cases it
verified both regimes: on a failed flat cone the lower maximal rate is at
least order (N), while on a passing cone either the ordinary
descending-source criterion applies or the same lower drift dominates the
top (O(N)) remainder of the fixed (V_d). For the 24 rank-two cases it
verified the exact positive invariant and the lower support
\(\{0,C\}\), giving drift
\(w_C(\kappa_{0C}-\kappa_{C0}C)\).

The audit found no orientation/rate counterexample or load-bearing gap at
this **dimension-local all-active generator** scope. It expressly did not
certify positive recurrence of any support pair: compatibility with the
two-active endpoint theorem, the one-active interface, and the final common
proper-potential composition remain separate obligations.

The counterexamples in Sections 6--8 remain useful: they disprove generic
attempts to use \(F_T\), a fixed shell correction, or the canonical
mean-zero Poisson gauge. The successful closure is instead shape-specific:
rate-adjusted entropy or a positive linear workload for two-node tops, the
arbitrary-directed factorial-linear correction for triple tops, and the
exact positive invariant for rank-two tops.

## 10. Reproduction

Run

    PYTHONPATH=src python3 src/three_active_gluing_gate.py
    PYTHONPATH=src python3 -m unittest tests/test_three_active_gluing_gate.py -v
    PYTHONPATH=src python3 src/shell_poisson_counterexample.py
    PYTHONPATH=src python3 -m unittest tests/test_shell_poisson_counterexample.py -v

The deterministic gluing-geometry certificate hash is

    77c4853ce916f224fe23132f17e2236a81d319632c6e2f3892cf516ae76f4b5e

The deterministic finite shell-Poisson certificate hash is

    cede254774e6ae78bb3712c5d48ace13f95c7474a008fbc7e2cbe5aba605f89d
