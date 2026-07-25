# An exact rank-six countermodel to the code-base depth/common-pair shadows

## Result and scope

There is an explicit 41-point \(E_6\) root subset \(C_6\subset S^5\) with
the following properties:

1. every distinct inner product is at most \(1/2\);
2. in every unit direction \(e\in S^5\), at least seven points satisfy
   \(\langle e,x\rangle>1/300\) and at least seven satisfy
   \(\langle e,x\rangle<-1/300\);
3. it satisfies every numerical common-pair capacity whose two base axes
   are code points, including the positive contact-base cap seven;
4. it is an actual configuration, so all graph covariance identities and
   all local Gram-PSD conditions through four points hold; and
5. its Gram matrix has rank six.

Thus robust \(\pm1/300\) depth, the entire **code-base** common-pair
capacity hierarchy, and local four-point Gram consistency do not recover
the missing global rank-at-most-five condition.  Any successful synthesis
must use genuinely global rank-five compatibility or the stronger
continuum family in which the base axes need not belong to the code.

This is a barrier theorem, not a five-dimensional kissing construction and
not a counterexample to \(\tau(5)=40\).

The certificate and exact verifier are
`e6_rank6_shadow_countermodel.json` and
`verify_e6_rank6_shadow_countermodel.py` in this folder.

## 1. The explicit 41 roots

Use the standard normalized \(E_6\) model in \(\mathbb R^6\).  It consists
of the 40 roots
\[
 \frac{\pm e_i\pm e_j}{\sqrt2},
 \qquad 1\le i<j\le5,
\]
with sixth coordinate zero, and the 32 spin roots
\[
 \frac1{\sqrt8}
 \left(s_1,s_2,s_3,s_4,s_5,
       \sqrt3\prod_{i=1}^5s_i\right),
 \qquad s_i\in\{-1,1\}.                              \tag{1}
\]
Whenever root indices are used below, they refer to the verifier's
ordering: the 40 \(D_5\) roots in lexicographic pair/sign order followed
by the 32 spin roots in lexicographic sign order.

For compactness write a \(D\)-line representative
\([d_1d_2d_3d_4d_5]\) for
\((d_1,\ldots,d_5,0)/\sqrt2\), and a spin-line representative
\([s_1s_2s_3s_4s_5;p]\) for
\((s_1,\ldots,s_5,\sqrt3p)/\sqrt8\).  Take both signs of the
following 20 lines:
\[
\begin{split}
L_D=\{&
[-1,-1,0,0,0],[-1,0,-1,0,0],[-1,0,1,0,0],\\
&[-1,0,0,0,-1],[-1,0,0,0,1],[0,-1,1,0,0],\\
&[0,-1,0,-1,0],[0,-1,0,1,0],[0,-1,0,0,1],\\
&[0,0,-1,-1,0],[0,0,-1,1,0],[0,0,-1,0,-1],\\
&[0,0,0,-1,-1]\},
\end{split}                                           \tag{2}
\]
\[
\begin{split}
L_S=\{&
[-1,-1,-1,-1,-1;-1],[-1,-1,-1,1,-1;1],\\
&[-1,-1,-1,1,1;-1],[-1,-1,1,1,-1;-1],\\
&[-1,1,-1,-1,1;-1],[-1,1,-1,1,1;1],\\
&[-1,1,1,1,1;-1]\}.
\end{split}                                           \tag{3}
\]
In every spin row \(p=\prod_i s_i\), so these are roots in (1).
Finally add the unpaired root
\[
 [0,0,-1,0,1]=\frac{-e_3+e_5}{\sqrt2}.                \tag{4}
\]
This gives \(40+1=41\) distinct roots.

The verifier computes the selected pair distribution, indexed by twice the
inner product:
\[
\begin{array}{c|rrrr}
2\langle x,y\rangle&-2&-1&0&1\\ \hline
\#\{x,y\}&20&219&362&219.
\end{array}                                          \tag{5}
\]
Thus the kissing inequality, including its contact boundary, holds.
Exact rational elimination of the \(41\times41\) Gram matrix gives rank
six.

## 2. Exact robust slab depth

The first 40 selected roots form the 20 antipodal line pairs in
(2)--(3).  Choose the displayed representatives and call them
\[
v_1,\ldots,v_{20}.
\]

For every 14-element subset \(T\subset\{1,\ldots,20\}\), define its frame
operator
\[
 F_T=\sum_{i\in T}v_iv_i^{\mathsf T}.
\]
The exact finite certificate proves
\[
\boxed{F_T\succ\frac14 I_6\quad\text{for every }|T|=14.} \tag{6}
\]

Here is the integer verification behind (6).  Multiply
\(F_T-I/4\) by eight and write it as
\[
\begin{pmatrix}
A&\sqrt3\,b\\
\sqrt3\,b^{\mathsf T}&c
\end{pmatrix},
\]
where \(A,b,c\) are integral.  Congruence by
\(\operatorname{diag}(1,1,1,1,1,1/\sqrt3)\), followed by multiplication
by three, gives the integral symmetric matrix
\[
R_T=
\begin{pmatrix}
3A&3b\\
3b^{\mathsf T}&c
\end{pmatrix}.                                      \tag{7}
\]
The verifier checks all
\[
\binom{20}{14}=38760
\]
subsets using exact Bareiss determinants and Sylvester's criterion.  The
minimum leading principal determinants of orders \(1,\ldots,6\) are
\[
12,\ 684,\ 28944,\ 1533168,\ 17029440,\ 71243712,    \tag{8}
\]
all strictly positive.

Now fix a unit vector \(e\in\mathbb R^6\).  If at most six of the line
pairs obeyed
\[
|\langle e,v_i\rangle|>\frac1{300},
\]
then some 14-element set \(T\) would satisfy
\[
\langle e,F_Te\rangle
=\sum_{i\in T}\langle e,v_i\rangle^2
\le\frac{14}{300^2}
=\frac7{45000}
<\frac14,
\]
contradicting (6).  Hence at least seven line pairs have absolute height
strictly greater than \(1/300\).  Each antipodal pair contributes one point
to each strict side.  The extra point (4) can only increase a side count,
so \(C_6\) has the claimed robust depth in every direction.

This proves the full quantitative conclusion of the enlarged-cap theorem,
not merely open-hemisphere depth.

## 3. Every code-base common-pair capacity also holds

All off-diagonal \(E_6\) inner products belong to
\[
\{-1,-1/2,0,1/2\}.
\]
An exact enumeration of the full 72-root system gives:

\[
\begin{array}{c|c|c}
q&\text{number of full-system base pairs}&
\text{common contact neighbors}\\ \hline
-1&36&0\\
-1/2&720&1\\
0&1080&6.
\end{array}                                          \tag{9}
\]
Every base pair of the indicated inner product has the displayed common
count.  Passing to \(C_6\) reduces its maxima to \(0,1,5\), respectively.

For any common-pair threshold \(0<b\le1/2\), a qualifying incident inner
product in \(E_6\) must equal \(1/2\).  At \(q=-1\), the capacity is zero.
At \(q=-1/2\), the projected parameter is \(p=4b^2\); whenever the
five-dimensional theorem asserts a bound, its capacity is at least one,
so the single possible common contact neighbor passes.  At \(q=0\),
\(p=2b^2\le1/2\); the only asserted endpoint is \(b=1/2\), where the
capacity is six.  Hence every pointwise, cumulative, exact-stratum, or
weighted consequence of those per-base capacity numbers holds for
\(C_6\).

There is one additional code-base row at positive base inner product.
When \(\langle y,z\rangle=1/2\) and both incident inner products equal
\(1/2\), projection into
\(\operatorname{span}\{y,z\}^{\perp}\cong\mathbb R^3\) gives the standard
capacity \(A(3,1/4)=7\).  Exact enumeration finds that every such base in
\(C_6\) has at most seven common contacts.  Thus the positive contact-base
row passes as well.  No stronger positive-base threshold theorem is being
silently assumed here.

## 4. The strongest direct pair-conditioned consequence of depth

There is a useful exact bridge from robust depth to the two incident
inner products at every base pair, but it does not reach the common-pair
quadrant.  Let \(C\) be any 41-point code having the robust depth
conclusion, fix distinct \(y,z\in C\), put
\[
 q=\langle y,z\rangle,\qquad
 a=\langle x,y\rangle,\qquad b=\langle x,z\rangle,
\]
and set \(\delta=1/300\).

If \(q>-1\), apply depth to
\[
 e_+=\frac{y+z}{\sqrt{2+2q}}.
\]
The two base points have nonnegative \(e_+\)-height.  Consequently, among
the other 39 points there are at least five satisfying
\[
 a+b>\delta\sqrt{2+2q}                              \tag{10}
\]
and at least seven satisfying
\[
 a+b<-\delta\sqrt{2+2q}.                            \tag{11}
\]
Indeed, removing \(y,z\) can remove at most two points from the positive
side and none from the negative side.

Likewise apply depth to
\[
 e_-=\frac{y-z}{\sqrt{2-2q}}.
\]
Here \(y\) lies on the positive side and \(z\) on the negative side.
After removing the bases, at least six third points satisfy each of
\[
 a-b>\delta\sqrt{2-2q},\qquad
 a-b<-\delta\sqrt{2-2q}.                            \tag{12}
\]
These statements remain valid at \(q=-1\), where only the \(e_-\) row is
defined.  They may be summed over any exactly specified collection of
base pairs, so they give rigorous triple-distribution inequalities with
no symmetry assumption.

The gap is geometric: (10)--(12) control half-planes whose boundaries pass
near the origin, whereas common-pair projection controls the quadrant
\(a,b\ge b_0>0\).  Neither region contains the other.  For example,
\((a,b)\) may have one coordinate near \(1/2\) and the other near
\(-1/2\), making \(a-b\) large without being a common neighbor.  The
countermodel above satisfies both sets of constraints, so combining them
only by nonnegative summation cannot be a universal separator.

## 5. Why four-point local consistency does not repair the gap

The configuration is genuine, so every edge-conditioned covariance matrix
is PSD and every graph-incidence identity holds automatically.  Moreover,
every four selected vectors have a Gram matrix of rank at most four.  That
Gram matrix is therefore realizable already in \(\mathbb R^4\), so no test
that sees only one four-point Gram matrix can detect that the full
configuration needs dimension six.

The dimension-five common-pair theorem contains more than raw \(K_4\)
positivity because it projects all common neighbors into a common
three-dimensional residual space.  Nevertheless, the \(E_6\) code-base
counts in (9) satisfy all of its numerical conclusions.

The restriction “code-base” is essential.  The selected roots with
canonical indices
\[
4,\ 13,\ 43,\ 49,\ 33
\]
form a five-clique: every mutual inner product is \(1/2\).  Let \(s\) be
their normalized sum and let \(t\) be a unit vector orthogonal to their
five-dimensional span.  For
\[
 u=\sqrt{\frac5{12}}\,s+\sqrt{\frac7{12}}\,t,\qquad
 v=\sqrt{\frac5{12}}\,s-\sqrt{\frac7{12}}\,t,
\]
one has
\[
\langle u,v\rangle=-\frac16,\qquad
\langle x,u\rangle=\langle x,v\rangle=\frac12
\quad\text{for all five clique points}.
\]
The projected parameter is \(p=3/5\), whose dimension-five residual
capacity is four.  Thus this rank-six configuration fails the stronger
continuum family in which \(u,v\) may be arbitrary auxiliary axes.  That
family is not encoded by pair/triple marginals with base points in \(C\).

A second transparent dimension-five rejection is the quadratic harmonic
sum.  From (5),
\[
\operatorname{tr}G^2=300,\qquad
\sum_{x,y\in C_6}\frac{5\langle x,y\rangle^2-1}{4}
=-\frac{181}{4}<0.                                  \tag{13}
\]
The nonnegativity of this sum on \(S^4\) therefore excludes \(C_6\).
Both rejections use dimension information absent from the audited shadows.

The decisive global failure is
\[
\operatorname{rank}G(C_6)=6>5.                       \tag{14}
\]
Thus a universal proof may still combine robust depth and common-pair
geometry successfully, but only if it couples them through a rank-five
invariant, such as (13), a global stress or a six-dimensional minor, or
else exploits the arbitrary-axis continuum family above.

## 6. Reproduction and boundary audit

Run from the repository root:

```bash
PYTHONPATH=. /usr/bin/python3 \
  experiments/four_point_depth_projection/verify_e6_rank6_shadow_countermodel.py

PYTHONPATH=. /usr/bin/python3 \
  experiments/four_point_depth_projection/audit_e6_rank6_shadow_countermodel.py
```

Both programs use only exact integers and `Fraction`.  The second is an
independent implementation using rational \(LDL^{\mathsf T}\), rather than
the first verifier's Bareiss/Sylvester path.  They check:

- all 41 roots are distinct and have exact norm one;
- all pair inner products and the exact Gram rank;
- every one of the 38,760 shifted-frame matrices in (6);
- all full-\(E_6\) and selected-subset common-contact counts; and
- the strict comparison \(7/45000<1/4\).

Contacts at \(1/2\) are retained.  The slab inequalities are strict because
the contradiction assumes the complementary non-strict bounds
\(|\langle e,v_i\rangle|\le1/300\).  No sampled direction, floating
eigenvalue, or solver status enters the certificate.
