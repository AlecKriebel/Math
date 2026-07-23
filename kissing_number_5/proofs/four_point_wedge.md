# Four-Point Wedge Inequalities and an Exact Barrier

This note proves a family of local inequalities for a spherical
\((5,N,1/2)\)-code.  It then gives an exact \(N=41\) pseudo-incidence
structure showing that these inequalities, Pfender's row inequality, and all
ordinary two-point Gegenbauer inequalities still do not by themselves imply
nonexistence.  The pseudo-incidence structure is **not** a spherical code or a
full three-point feasible point.

## 1. The strict \(a>3/4\) inequality

For \(0<a\leq1\), let
\[
 D_a=\#\{(x,y):x\ne y,\ \langle x,y\rangle\leq-a\},\qquad
 d_a(x)=\#\{y\ne x:\langle x,y\rangle\leq-a\}.
\]
For \(b\in[-1,1]\), let
\[
 Q_b=\#\{(y,z):y\ne z,\ \langle y,z\rangle\geq b\}.
\]
All pair counts in these definitions are ordered.

If \(y,z\) are distinct \(a\)-deep neighbors of \(x\), write
\[
 y=-s x+\sqrt{1-s^2}\,u,\qquad
 z=-t x+\sqrt{1-t^2}\,v
\]
with \(s,t\geq a\) and \(u,v\in x^\perp\) unit.  Then
\[
 \langle y,z\rangle
 \geq st-\sqrt{(1-s^2)(1-t^2)}
 \geq 2a^2-1.                                      \tag{1}
\]
The last expression is increasing separately in \(s,t\geq0\).

Now fix an unordered pair \(\{y,z\}\), put \(r=\langle y,z\rangle\leq
1/2\), and suppose that both \(x\) and \(w\) are common \(a\)-deep
neighbors.  With
\[
 e=-\frac{y+z}{\|y+z\|},
\]
both \(\langle x,e\rangle\) and \(\langle w,e\rangle\) are at least
\[
 c=\frac{\sqrt2a}{\sqrt{1+r}}.
\]
Consequently
\[
 \langle x,w\rangle\geq 2c^2-1
 \geq \frac{8a^2}{3}-1.
\]
For \(a>3/4\), this is strictly greater than \(1/2\).  Thus an endpoint
pair has at most one common \(a\)-deep center.  Counting centered unordered
wedges and then orienting their endpoint pairs proves
\[
 \boxed{\quad Q_{2a^2-1}\geq
        2\sum_x {d_a(x)\choose2}\quad}\qquad(a>3/4).       \tag{2}
\]

There is no orientation or factor-of-two slack in (2): its right side first
counts an unordered endpoint pair once per center and then counts its two
orientations.

## 2. Integer envelope

If \(D=\sum_xd_x=Nq+r\), where \(q=\lfloor D/N\rfloor\) and
\(0\leq r<N\), discrete convexity gives
\[
 \sum_xd_x(d_x-1)\geq
 F_N(D):=Nq(q-1)+2qr.                               \tag{3}
\]
Indeed, moving one unit from a degree at least two larger to a smaller degree
strictly decreases the sum.  Hence the minimum has \(r\) entries \(q+1\)
and \(N-r\) entries \(q\).  This is the exact integer convex envelope when
only \(N,D\) are retained.  Its tangent at degrees four and five is
\[
 F_N(D)\geq8D-20N,
\]
because \(d(d-1)-8d+20=(d-4)(d-5)\geq0\) for integral \(d\).
Thus (2) implies the proposed inequality
\[
 Q_{2a^2-1}\geq8D_a-20N.
\]

## 3. The endpoint \(a=3/4\) and common-center bounds

Strictness in \(a>3/4\) is necessary.  For orthonormal \(e_0,e_1,e_2\),
put
\[
\begin{aligned}
y&=(\sqrt3/2)e_0+(1/2)e_1,&
z&=(\sqrt3/2)e_0-(1/2)e_1,\\
x&=-(\sqrt3/2)e_0+(1/2)e_2,&
w&=-(\sqrt3/2)e_0-(1/2)e_2.
\end{aligned}
\]
The two inner products \(\langle y,z\rangle,\langle x,w\rangle\) equal
\(1/2\), and the four cross inner products equal \(-3/4\).  At \(a=3/4\),
all four vertices have deep degree two.  Therefore
\[
 Q_{1/8}=4,\qquad 2\sum_v{d_{3/4}(v)\choose2}=8.
\]
This refutes (2) at the weak endpoint.  Every high endpoint pair here has
exactly two deep centers.

More generally, suppose \(\{y,z\}\) has \(m\) common \(a\)-deep centers
\(x_1,\ldots,x_m\), and put \(X=\sum_i x_i\).  Since
\(\|y+z\|^2\leq3\),
\[
 4a^2m^2
 \leq\|X\|^2\|y+z\|^2
 \leq\frac{3m(m+1)}2.
\]
For \(a>\sqrt{3/8}\), this proves
\[
 m\leq\left\lfloor\frac3{8a^2-3}\right\rfloor.       \tag{4}
\]
Projection perpendicular to \(y+z\) places the residual directions in
\(\mathbb R^4\) with pairwise negative inner products, so also \(m\leq5\).
Thus one may take
\[
 m(a)=\min\left(5,\left\lfloor\frac3{8a^2-3}\right\rfloor\right)
 \quad\left(\sqrt{3/8}<a\leq3/4\right),              \tag{5}
\]
and \(m(a)=1\) for \(a>3/4\).  In particular \(m(3/4)=2\).

For \(\sqrt3/4\leq a\leq\sqrt{3/8}\), projection along \(y+z\) instead
gives a code in \(S^3\) with maximum inner product at most \(1/3\).  The
exact bound \(A(4,1/3)\leq15\), proved in `local_link_geometry.md`, yields
the convenient bound \(m(a)\leq15\).  The trivial bound \(m(a)\leq N-2\)
is always available.

It follows from the same incidence count that
\[
 m(a)Q_{2a^2-1}\geq2\sum_x{d_a(x)\choose2}.           \tag{6}
\]

## 4. Mixed thresholds

Let \(a\geq c>0\), and define
\[
 \beta(a,c)=ac-\sqrt{(1-a^2)(1-c^2)}.
\]
At a center \(x\), the number of unordered pairs of \(c\)-deep neighbors
with at least one \(a\)-deep member is exactly
\[
 W_{a,c}(x)
 ={d_c(x)\choose2}-{d_c(x)-d_a(x)\choose2}.          \tag{7}
\]
Equation (1), with unequal depths, puts every such endpoint pair above
\(\beta(a,c)\).  An endpoint pair has at most \(m(c)\) common \(c\)-deep
centers.  Therefore the degree-sequence-strength mixed family is
\[
 \boxed{\quad
 m(c)Q_{\beta(a,c)}
 \geq2\sum_xW_{a,c}(x).
 \quad}                                               \tag{8}
\]
This includes (2) and (6).  Notice that separately applying several
threshold inequalities is valid, but summing them without assigning
disjoint wedge incidences would double count.

For comparison, the link of a fixed center gives the independent local
degree bound
\[
 d_a(x)\leq
 \min\left(5,\left\lfloor\frac1{2a^2-1}\right\rfloor\right)
 \qquad(a>1/\sqrt2).                                  \tag{9}
\]
Indeed the normalized residuals lie in \(\mathbb R^4\) and have mutual
inner product at most
\[
 \frac{1/2-a^2}{1-a^2}<0.
\]
The simplex sum inequality and the dimension bound for a strictly obtuse
set give (9).  In particular, for \(N=41\), ordered-pair parity gives
\(D_a\leq204\) on \(1/\sqrt2<a\leq\sqrt3/2\), while
\(D_a\leq40\) for \(a>\sqrt3/2\).

## 5. Exact \(N=41\) pseudo-incidence barrier

Consider the six rational inner-product labels
\[
 \left(-\frac{157}{200},-\frac{39}{50},-\frac9{20},
       -\frac1{10},-\frac{19}{200},\frac{99}{200}\right)
\]
with ordered multiplicities
\[
 (32,132,264,130,522,560).                            \tag{10}
\]
They sum to \(41\cdot40\), and every entry is even.

The verifier contains a labeled complete graph realizing exactly these
multiplicities as unordered edge counts
\[
 (16,66,132,65,261,280).
\]
Its two deepest classes form a 4-regular graph \(L\) of girth at least five.
The deepest 16 edges form a matching.  The high graph contains all 246
distance-two pairs of \(L\), plus 34 more edges, and has degree multiset
\(14^{27},13^{14}\).  The \(-9/20\) edges are chosen within the classes of
an explicit proper 3-coloring of \(L\).  These facts imply all mixed wedge
incidences; the verifier also checks them directly by exact \(3\times3\)
determinants.  Among all centered triples whose two incident labels are
negative, the minimum determinant is
\[
 \frac{161}{1600}>0.                                  \tag{11}
\]
At depth \(9/20\), the maximum number of common centers is eight, below the
bound fifteen.

Pfender's row inequality
\[
 \sum_{y:\langle x,y\rangle<-1/\sqrt2}
 \left(2\langle x,y\rangle^2-1\right)\leq1
\]
also holds vertex by vertex.  The only row values are
\[
 \frac{542}{625},\qquad \frac{17657}{20000},
\]
both strictly below one.

Finally, (10) satisfies every dimension-five Gegenbauer moment inequality.
For degrees \(1\) through \(103\), exact recurrence evaluation gives
\[
 \min_k\left(41+\sum_i c_iP_k(t_i)\right)
 =\frac{30261}{16000}
\]
at \(k=2\).  For every atom, \(1-t_i^2\geq15351/40000\), and
\[
 (1-t_i^2)^{-3/2}<17/4.
\]
Using the analytic bound from `two_point_lp_barrier.md`, the normalized
off-diagonal tail is less than
\[
 \frac{1054}{k^{3/2}}<1\qquad(k\geq104),
\]
where \(1054^2<104^3\).  Hence every higher moment is strictly positive.

## 6. Exact scope boundary

The object above is not a full three-point pseudo-distribution.  It has 244
negative \(3\times3\) minors.  For example, vertices \(0,1,2\) have labels
\[
 \left(\frac{99}{200},\frac{99}{200},-\frac{157}{200}\right)
\]
and determinant
\[
 -\frac{1963857}{4000000}<0.                          \tag{12}
\]
Thus the certificate proves only that two-point positivity, all
negative-centered wedge inequalities (including mixed thresholds), local
deep-degree bounds, and Pfender's row generator remain jointly
insufficient.  General three-point positivity detects it immediately.

## Reproduction

Run

```sh
python3 verifiers/verify_four_point_wedge.py
python3 -m unittest tests.test_four_point_wedge -v
```
