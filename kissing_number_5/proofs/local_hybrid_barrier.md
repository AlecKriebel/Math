# Exact Pfender/Local-Hybrid Inequalities and Their Present Barrier

This note proves several classification-free inequalities for a spherical
\((5,N,1/2)\)-code.  One of them separates the first exact mass-\(41\)
two-point pseudo-distribution in `two_point_lp_barrier.md`.  We then give a
second exact pseudo-distribution that survives all of the scalar inequalities
proved here.  Thus the note records both genuine progress and a precise
barrier; it is **not** an upper-bound proof for \(\tau(5)\).

Throughout, ordered pair counts exclude the diagonal.  For a code \(C\), its
normalized two-point measure is
\[
 \mu_C=\delta_1+\frac1N\sum_{\substack{x,y\in C\\x\ne y}}
 \delta_{\langle x,y\rangle}.
\tag{1}
\]

## 1. Source-audited Pfender inequality

Theorem 4.3 of Florian Pfender, *Improved Delsarte bounds for spherical
codes in small dimensions*, J. Combin. Theory Ser. A **114** (2007),
1133--1147, arXiv:math/0501493v2, defines, for \(z=\cos\alpha\),
\[
 f_\alpha(t)=
 \begin{cases}
 (z-t^2)/(1-z),&t<-\sqrt z,\\
 0,&-\sqrt z\le t\le z,\\
 (t-z)/(1-z),&t>z,
 \end{cases}
\tag{2}
\]
and proves the row inequality
\[
 \sum_{y\in C}f_\alpha(\langle x,y\rangle)\ge0.
\tag{3}
\]
For \(z=1/2\), (3) is exactly
\[
 \sum_{\substack{y\ne x\\\langle x,y\rangle<-1/\sqrt2}}
 \bigl(2\langle x,y\rangle^2-1\bigr)\le1.
\tag{4}
\]
The boundary \(t=-1/\sqrt2\) contributes zero.  Summing (3) over \(x\)
and dividing by \(N\) says precisely that
\(\int f_{\pi/3}\,d\mu_C\ge0\) under normalization (1).

For completeness, (4) also has a direct proof.  Write
\(p_i=-\langle x,y_i\rangle>1/\sqrt2\) for the selected neighbors and
\(v_i=y_i+p_i x\in x^\perp\).  Put \(Q=\sum p_i^2\) and
\(S=\sum p_i\).  Since the \(v_i\) form a positive-semidefinite Gram
system and \(\langle y_i,y_j\rangle\le1/2\),
\[
\begin{aligned}
0
&\le \left\|\sum_i p_i v_i\right\|^2\\
&\le \frac{Q+S^2}{2}-Q^2
\le \frac{(m+1)Q}{2}-Q^2.
\end{aligned}
\]
Hence \(2Q\le m+1\), which is (4).

Pfender's Lemma 3.4 also gives the generator
\[
g_{\pi/3}(t)=
\begin{cases}
-1,&t<-\sqrt3/2,\\
0,&-\sqrt3/2\le t\le1/2,\\
1,&t>1/2.
\end{cases}
\tag{5}
\]
All strict and weak inequalities in (2), (4), and (5) are retained here.

## 2. A dimension-five cap bound

Fix \(a>1/\sqrt2\), and join \(x\) to \(y\) when
\(\langle x,y\rangle\le-a\).  Then
\[
d_a(x)\le5.
\tag{6}
\]
Indeed, unless \(y=-x\), normalize the residual
\[
u_y=\frac{y-\langle x,y\rangle x}
{\sqrt{1-\langle x,y\rangle^2}}\in x^\perp\cong\mathbb R^4.
\]
For two such neighbors,
\[
\langle u_y,u_z\rangle
=\frac{\langle y,z\rangle-\langle x,y\rangle\langle x,z\rangle}
{\sqrt{1-\langle x,y\rangle^2}
 \sqrt{1-\langle x,z\rangle^2}}<0.
\]
A pairwise-negative set in \(\mathbb R^4\) has at most five members.
One quick proof is that every linear dependence among such vectors has
coefficients of only one sign: moving positive and negative parts to
opposite sides and taking their inner product would otherwise make a
squared norm negative.  Two independent dependencies would have a linear
combination with both signs, so the nullity is at most one.  Thus
\(m-1\le4\).  If \(y=-x\), it is the only neighbor because
\(\langle-y,z\rangle>1/2\) for every other selected \(z\).

The strict hypothesis \(a>1/\sqrt2\) matters: at equality the projected
inner products need only be nonpositive.

## 3. Two-anchor wedge and common-center inequalities

Let \(D_a\) be the graph just defined, let
\[
b=2a^2-1,
\]
and let \(Q_b\) be the number of ordered pairs with inner product at least
\(b\).  Every wedge \(y-x-z\) in \(D_a\) has
\[
4a^2\le\langle x,y+z\rangle^2\le\|y+z\|^2
=2+2\langle y,z\rangle,
\]
so its endpoint pair is counted by \(Q_b\).

Suppose a fixed endpoint pair \(y,z\) has \(m\) common \(D_a\)-neighbors.
Writing \(r=\langle y,z\rangle\le1/2\) and
\[
u=-\frac{y+z}{\sqrt{2+2r}},
\]
each common neighbor \(x_i\) satisfies
\[
\langle u,x_i\rangle\ge
\frac{2a}{\sqrt{2+2r}}\ge\frac{2a}{\sqrt3}=:c.
\]
If \(a>\sqrt{3/8}\), then \(c>1/\sqrt2\).  The dimension-five cap
argument gives \(m\le5\).  Also,
\[
m^2c^2\le\left\|\sum_i x_i\right\|^2
\le m+\frac{m(m-1)}2,
\]
and hence
\[
m\le L(a):=\min\left(5,
\left\lfloor\frac3{8a^2-3}\right\rfloor\right).
\tag{7}
\]
In particular, \(L(3/4)=2\), while \(L(a)=1\) for \(a>3/4\).
This explicitly handles the endpoint where two common centers can occur.

Let \(D\) denote the ordered edge count of \(D_a\), and put
\[
W=\sum_x\binom{d_a(x)}2.
\]
If \(P=Q_b/2\) is the unordered high-inner-product pair count, (7) gives
\[
W\le L(a)P.
\tag{8}
\]
For integers \(d,k\ge0\),
\[
\binom d2\ge kd-\binom{k+1}2
\tag{9}
\]
because the difference is \((d-k)(d-k-1)/2\).  Equivalently, if
\(D=qN+r\), \(0\le r<N\), then
\[
W\ge F_N(D):=(N-r)\binom q2+r\binom{q+1}2.
\tag{10}
\]
Combining (8)--(10) yields the exact two-point cut
\[
L(a)Q_b\ge2F_N(D).
\tag{11}
\]

At \(a=77/100\), \(b=929/5000\) and \(L(a)=1\).  The pseudo-measure in
`two_point_lp_barrier.md` has \(D=176\), \(Q_b=550\), and
\[
2F_{41}(176)=588.
\]
Thus (11) separates that pseudo-measure exactly.

## 4. A rank-deficit refinement

There is a further dimension-five inequality.  Assume
\[
\frac34<a<\sqrt{\frac35},\qquad
\beta=3-5a^2>0,\qquad b=2a^2-1.
\]
Define
\[
\begin{aligned}
D&=\#\{(x,y):x\ne y,\ \langle x,y\rangle\le-a\},\\
S&=\sum_{\langle x,y\rangle\le-a}(-\langle x,y\rangle-a),\\
T&=\sum_{\langle y,z\rangle\ge b}(1/2-\langle y,z\rangle),
\end{aligned}
\tag{12}
\]
where all three sums use ordered pairs.  Then
\[
\boxed{\ \beta(D-4N)\le10S+T.\ }
\tag{13}
\]

To prove (13), fix a vertex \(x\) of \(D_a\)-degree five and write
\(p_i=-\langle x,y_i\rangle\ge a\).  The five residual vectors
\[
v_i=y_i+p_i x
\]
lie in the four-dimensional space \(x^\perp\).  Their Gram matrix \(R\)
is therefore positive semidefinite and singular, with
\[
R_{ii}=1-p_i^2,\qquad
R_{ij}=\langle y_i,y_j\rangle-p_ip_j.
\]
Let \(B\) have diagonal \(1-a^2\) and off-diagonal \(1/2-a^2\).  Thus
\[
B=\frac12I+(1/2-a^2)J\succeq\beta I.
\]
The entrywise difference \(E=B-R\) is nonnegative.  Choose
\(0\ne w\in\ker R\).  There is no sign reversal:
\[
\beta\|w\|^2
\le w^\mathsf TBw=w^\mathsf TEw
\le\sum_{i,j}E_{ij}|w_iw_j|
\le\left(\sum_{i,j}E_{ij}\right)\|w\|^2.
\]
Consequently \(\sum E_{ij}\ge\beta\).  If
\(\Delta=\sum_{i<j}(1/2-\langle y_i,y_j\rangle)\), direct expansion gives
\[
\sum_{i,j}E_{ij}
=\left(\sum_i p_i\right)^2-25a^2+2\Delta
\le10\sum_i(p_i-a)+2\Delta.
\tag{14}
\]
The last inequality uses \(\sum p_i+5a\le10\).

By (6), the number \(n_5\) of degree-five vertices is at least
\(D-4N\).  By (7), because \(a>3/4\), a pair is the endpoint pair of at
most one \(D_a\)-wedge.  Summing (14) over the degree-five vertices
therefore counts each ordered deep-edge excess within \(S\), and twice
each unordered endpoint deficit within the ordered sum \(T\).  Hence
\(\beta n_5\le10S+T\), which proves (13).

## 5. An exact witness surviving all scalar cuts above

Define
\[
\begin{aligned}
\mu_*={}&\delta_1+
\frac{170}{41}\delta_{-77/100}
+\frac6{41}\delta_{-7/10}
+\frac{262}{41}\delta_{-11/25}\\
&+\frac{652}{41}\delta_{-9/100}
+\frac{550}{41}\delta_{499/1000}.
\end{aligned}
\tag{15}
\]
The ordered counts are positive even integers summing to
\(41\cdot40\), so \(\mu_*\) has mass \(41\).

For the normalized dimension-five Gegenbauer recurrence
\[
(k+2)P_k=(2k+1)tP_{k-1}-(k-1)P_{k-2},
\]
exact evaluation through degree \(53\) gives
\[
\min_{1\le k\le53}\int P_k\,d\mu_*
=\int P_2\,d\mu_*=\frac{29759}{656000}>\frac1{23}.
\tag{16}
\]
The integral estimate proved in `two_point_lp_barrier.md` gives
\[
|P_k(t)|\le
\frac{\pi^2\sqrt{2\pi}}{4[k(1-t^2)]^{3/2}}.
\]
For the five atoms in (15), exact rational upper bounds for
\((1-t^2)^{-3/2}\) are
\[
4,\quad3,\quad\frac75,\quad\frac{51}{50},\quad\frac{31}{20}.
\]
Their weighted sum is \(129117/2050\).  Using the already proved
\(\pi^2\sqrt{2\pi}/4<31/5\), the off-diagonal contribution is less than
\[
\frac{4002627}{10250\,k^{3/2}}
<\frac{391}{k^{3/2}}<1\qquad(k\ge54),
\]
where \(391^2<54^3\).  Thus every Gegenbauer moment of (15) is positive.

The summed Pfender cost is
\[
\frac{170}{41}\left(2(77/100)^2-1\right)
=\frac{15793}{20500}<1,
\tag{17}
\]
and (15) has no atom below \(-\sqrt3/2\).

It also passes every cut (11).  It is enough to put \(q=a^2\); all
support, floor, and boundary events are rational.  The only tight regime is
\[
\frac9{16}<q\le\frac{5929}{10000},
\qquad L=1,\quad D=170,\quad Q_b=550,
\]
where \(2F_{41}(170)=540\).  The exact verifier checks every event and
every intervening cell, including \(q=1/2\), \(q=9/16\), and all support
boundaries.  It also checks (6): for \(q>1/2\), \(D\le170<205\).

Finally, throughout \(3/4<a\le77/100\), (13) reduces to
\[
6(3-5a^2)\le1700(77/100-a)+\frac{11}{20}.
\]
The right-minus-left derivative is \(-1700+60a<0\), so the worst point
is \(a=77/100\), where the two sides are respectively
\[
\frac{213}{1000}<\frac{11}{20}
\]
with margin \(337/1000\).  For \(a>77/100\), \(D=0\) and (13) is
automatic.

## 6. Exact scope of the barrier

The witness (15) proves feasibility only for the relaxation generated by:

- all ordinary two-point Gegenbauer inequalities, at every degree;
- the summed Pfender generators (2) and (5);
- the scalar cap bounds (6);
- all common-center/integer-envelope cuts (11); and
- the rank-deficit family (13).

It does **not** supply rowwise realizability, a triple distribution, a
rank-five Gram matrix, or a spherical code.  It does not defeat arbitrary
Bachoc--Vallentin constraints, full two-anchor conditional distributions, or
four-point information.  Any of those may still separate \(N=41\).

## Reproduction

Run:

```sh
python3 verifiers/verify_local_hybrid_barrier.py
python3 -m unittest tests.test_local_hybrid_barrier -v
```
