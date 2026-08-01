# Route C: an explicit high-circumradius band

**Scope:** first-principles continuation of the Jung-defect and
nearest-anchor argument in `route_c_structural_report.md`.  No literature or
web search was used.

## Result

The nonexplicit constant in Corollary 13 of the structural report can be
replaced by the rational number

\[
  \boxed{\varepsilon=\frac1{100000}}.
\]

More precisely, let \(K\subset\mathbb R^4\) be compact, let
\(D=\operatorname {diam}K>0\), and let \(R\) be the radius of its minimum
enclosing ball.  If

\[
 R^2>\left(\frac25-\frac1{100000}\right)D^2,               \tag{1}
\]

then five nearest-anchor parts have diameters at most \(\Gamma D<D\), where

\[
 \Gamma^2=
 \frac{504}{125}
 \left(
   \frac{12997}{15500}-\frac45\sqrt{\frac{377}{620}}
 \right)
 <1.                                                       \tag{2}
\]

Numerically, only for orientation, \(\Gamma^2\approx0.865623\) and
\(\Gamma\approx0.930389\).  Inequality (2) is proved below using integers,
not these decimal values.  Passing to the closure proves the same statement
for every bounded set.

The proof has two quantitative steps.  First the Jung defect makes all ten
squared anchor edges lie in \((999/1000,1]\).  Second, any simplex with this
edge control is the image of a regular simplex under a linear map whose
squared-norm distortion is below \(1/125\).  Pulling the nearest-anchor cells
back through this map gives an explicit enlargement of the regular-simplex
cell estimate.

## 1. The Jung defect supplies five quantitative anchors

Scale to \(D=1\).  Write

\[
 \delta=\frac25-R^2.
\]

Under (1), \(0\le\delta<1/100000\).  Choose a balanced contact
representation, padded to five terms if necessary,

\[
 \sum_{i=0}^4\lambda_i=1,\qquad
 \sum_{i=0}^4\lambda_i(a_i-c)=0,
\]

where every nonzero-weight \(a_i\) is a contact point of the minimum
enclosing ball.  The exact defect identity (6) of the structural report is

\[
 \delta=
 \frac12\sum_{i=0}^4\left(\lambda_i-\frac15\right)^2
 +\sum_{0\le i<j\le4}\lambda_i\lambda_j
       \left(1-\lVert a_i-a_j\rVert^2\right).              \tag{3}
\]

All summands are nonnegative.  Hence

\[
 \left|\lambda_i-\frac15\right|^2
 \le 2\delta<\frac1{50000}<\frac1{100},
\]

and therefore

\[
 \lambda_i>\frac1{10}\qquad(0\le i\le4).                 \tag{4}
\]

In particular no padded weight is zero, so there are five genuine contact
anchors.  For every pair, (3) and (4) give

\[
 0\le 1-\lVert a_i-a_j\rVert^2
 \le\frac{\delta}{\lambda_i\lambda_j}
 \le100\delta<\frac1{1000}.                               \tag{5}
\]

Thus, with

\[
 \eta=\max_{i<j}\left(1-\lVert a_i-a_j\rVert^2\right),
\]

we have \(0\le\eta<1/1000\).  Notice also that every \(x\in K\)
satisfies

\[
 \lVert x-a_j\rVert\le1\qquad(0\le j\le4),               \tag{6}
\]

because the anchors belong to \(K\) and \(K\) has diameter one.

## 2. Edge errors give an exact metric-distortion bound

Use the fixed regular unit-edge simplex

\[
 H=\left\{z\in\mathbb R^5:\sum_{j=0}^4z_j=0\right\},
 \qquad
 v_i=\frac1{\sqrt2}\left(e_i-\frac15\mathbf1\right).
                                                               \tag{7}
\]

Let \(g=\frac15\sum_i a_i\) and \(u_i=a_i-g\).  There is a unique
linear map \(A:H\to\mathbb R^4\) satisfying \(Av_i=u_i\): the only linear
relation among the five \(v_i\)'s is their zero sum, and the \(u_i\)'s have
the same relation.

**Lemma 1 (edge-to-metric Lipschitz bound).**  If

\[
 1-\eta\le\lVert a_i-a_j\rVert^2\le1\qquad(i\ne j),        \tag{8}
\]

then, for every \(z\in H\),

\[
 (1-8\eta)\lVert z\rVert^2
 \le\lVert Az\rVert^2
 \le(1+8\eta)\lVert z\rVert^2.                            \tag{9}
\]

**Proof.**  Take the basis \(b_k=v_k-v_0\), \(1\le k\le4\).  Its Gram
matrix \(G_0\) has diagonal entries one and off-diagonal entries \(1/2\),
so

\[
 G_0=\frac12(I+J),\qquad
 c^{\mathsf T}G_0c\ge\frac12\sum_{k=1}^4c_k^2.             \tag{10}
\]

Put \(d_{ij}^2=\lVert a_i-a_j\rVert^2=1-\alpha_{ij}\), where
\(0\le\alpha_{ij}\le\eta\).  The Gram matrix \(G\) of
\(Ab_k=a_k-a_0\) has

\[
 G_{kk}=1-\alpha_{0k},\qquad
 G_{k\ell}=\frac12+
 \frac{-\alpha_{0k}-\alpha_{0\ell}+\alpha_{k\ell}}2.
                                                               \tag{11}
\]

Every entry of \(E=G-G_0\) consequently has absolute value at most
\(\eta\).  For \(z=\sum_kc_kb_k\),

\[
 \begin{aligned}
 \left|\lVert Az\rVert^2-\lVert z\rVert^2\right|
 &=|c^{\mathsf T}Ec|\\
 &\le\eta\left(\sum_k|c_k|\right)^2
 \le4\eta\sum_kc_k^2
 \le8\eta\lVert z\rVert^2.
 \end{aligned}
\]

This is (9). \(\square\)

In the application put

\[
 \tau=8\eta<\frac8{1000}=\frac1{125}.                     \tag{12}
\]

Since \(\tau<1\), (9) also proves that \(A\) is invertible.  Thus every
point \(x\in\mathbb R^4\) has a unique representation

\[
 x=g+Az,\qquad z\in H.                                    \tag{13}
\]

## 3. Quantitative stability of the five Voronoi cells

For an anchor \(a_i\), let

\[
 C_i=\left\{x\in K:
       \lVert x-a_i\rVert\le\lVert x-a_j\rVert
       \text{ for every }j\right\}.                       \tag{14}
\]

The cells cover \(K\); any deterministic tie rule turns them into a
partition.  We now bound each closed cell uniformly.

Set

\[
 Q(y)=\lVert Ay\rVert^2,\qquad
 a=\frac{\tau}{1-\tau},qquad
 B=3+5a.                                                   \tag{15}
\]

By (9),

\[
 |Q(y)-\lVert y\rVert^2|\le\tau\lVert y\rVert^2.           \tag{16}
\]

It is enough by symmetry of the model simplex to consider \(C_0\).  Let
\(x=g+Az\in C_0\), put

\[
 r^2=\lVert z\rVert^2,\qquad s=z_0.
\]

From (6),

\[
 Q(z-v_j)=\lVert x-a_j\rVert^2\le1.
\]

The lower half of (9) therefore gives

\[
 \lVert z-v_j\rVert^2\le\frac1{1-\tau}.                   \tag{17}
\]

Moreover, actual nearest-anchor membership says
\(Q(z-v_0)\le Q(z-v_j)\).  Combining this with (16) and (17) yields

\[
 \begin{aligned}
 \lVert z-v_0\rVert^2-\lVert z-v_j\rVert^2
 &\le \tau\left(
       \lVert z-v_0\rVert^2+\lVert z-v_j\rVert^2\right)\\
 &\le\frac{2\tau}{1-\tau}.                                \tag{18}
 \end{aligned}
\]

In model coordinates,

\[
 \lVert v_j\rVert^2=\frac25,qquad
 \langle z,v_j\rangle=\frac{z_j}{\sqrt2}.
\]

Thus (17) and (18), respectively, imply

\[
 z_j\ge
 \ell:=\frac{r^2-\frac35-a}{\sqrt2},
 \qquad
 z_j\le u:=s+\sqrt2a                                    \tag{19}
\]

for every \(j\).  Since \(\sum_jz_j=0\) and every \(z_j\le u\), one has
\(u\ge0\).  Now each coordinate lies in \([\ell,u]\), so

\[
 0\le\sum_{j=0}^4(u-z_j)(z_j-\ell)
   =-r^2-5u\ell.
\]

Consequently

\[
 r^2\le\frac{(3+5a)u}{\sqrt2+5u}
       =\frac{Bu}{\sqrt2+5u}.                              \tag{20}
\]

Take \(t=2/5\).  Since \(s=u-\sqrt2a\), equations (20) and (7) give

\[
 \begin{aligned}
 \left\lVert z-tv_0\right\rVert^2
 &=r^2-\sqrt2ts+\frac25t^2\\
 &\le
 \frac{Bu}{\sqrt2+5u}-\sqrt2tu
 +2ta+\frac25t^2.                                         \tag{21}
 \end{aligned}
\]

For completeness, the maximum over \(u\ge0\) of the first two terms is

\[
 \max_{u\ge0}
 \left(\frac{Bu}{\sqrt2+5u}-\sqrt2tu\right)
 =\frac{B+2t-2\sqrt{2Bt}}5.                               \tag{22}
\]

Indeed, the derivative vanishes only at

\[
 u=\frac{\sqrt{B/t}-\sqrt2}{5}>0,
\]

and the expression tends to \(-\infty\) as \(u\to\infty\).  Substitution
gives (22).  Therefore every pulled-back point of \(C_0\) lies in the ball
of squared radius

\[
 \rho^2(\tau)=
 \frac{B+\frac45-2\sqrt{\frac45B}}5
 +\frac45a+\frac8{125}                                   \tag{23}
\]

centered at \((2/5)v_0\).  The same conclusion holds for every \(i\).
Mapping this ball forward using (9) shows that

\[
 C_i\subset
 \overline B\left(g+\frac25(a_i-g),
                   \sqrt{1+\tau}\,\rho(\tau)\right),
\]

and hence

\[
 \operatorname {diam}(C_i)^2
 \le4(1+\tau)\rho^2(\tau).                                \tag{24}
\]

This is the promised explicit replacement for the compactness-only robust
anchor lemma.

## 4. The endpoint calculation is exact

The right side of (23) is increasing in \(\tau\in[0,1/125]\).  Indeed,
\(a=\tau/(1-\tau)\) and \(B=3+5a\) increase, while

\[
 B+\frac45-2\sqrt{\frac45B}
 =\left(\sqrt B-\sqrt{\frac45}\right)^2
\]

increases for \(B\ge3\).  At \(\tau_0=1/125\),

\[
 a_0=\frac1{124},\qquad B_0=\frac{377}{124},
\]

and direct common-denominator arithmetic in (23) gives

\[
 \rho^2(\tau_0)=
 \frac{12997}{15500}-\frac45\sqrt{\frac{377}{620}}.       \tag{25}
\]

It remains to check this is below \(125/504\).  Moving the radical to the
right gives the positive rational number

\[
 \frac{12997}{15500}-\frac{125}{504}
 =\frac{1153247}{1953000}>0.
\]

Both sides are positive, and their squared difference is

\[
 \left(\frac45\sqrt{\frac{377}{620}}\right)^2
 -\left(\frac{1153247}{1953000}\right)^2
 =\frac{154363852991}{3814209000000}>0.                   \tag{26}
\]

Thus

\[
 \rho^2(\tau_0)<\frac{125}{504},
\]

and (24), (12), and monotonicity imply

\[
 \operatorname {diam}(C_i)^2
 \le4(1+\tau)\rho^2(\tau)
 <4\left(1+\frac1{125}\right)\frac{125}{504}=1.           \tag{27}
\]

This proves the stated five-partition and the explicit value
\(\varepsilon=1/100000\).  Formula (2) is the slightly stronger bound
obtained by retaining (25) rather than replacing it by \(125/504\).

## 5. Dependency and strictness audit

The strict inequalities have the following exact sources.

1. The radius hypothesis makes \(\delta<1/100000\).
2. The nonnegative defect identity makes all weights positive and gives the
   strict edge estimate \(\eta<1/1000\).
3. The Gram estimate makes \(\tau=8\eta<1/125\).
4. Even at the weak metric threshold \(\tau=1/125\), the integer comparison
   (26) leaves a strict cell-diameter margin.

No generic-position assumption is used.  Voronoi ties are harmless because
every closed cell separately satisfies (27).  No continuity or limiting
argument is used after the five balanced contact anchors are chosen.

There is also no hidden affine-independence hypothesis.  The map \(A\) is
well-defined before independence is known and is permitted at that stage to
be singular.  Inequality (9), together with \(8\eta<1\), then proves that it
is injective.  Thus the high-radius hypothesis itself forces the five
contacts to be an affinely independent four-simplex.

Finally, if \(S\) is merely bounded, its closure \(K=\overline S\) is
compact and has the same diameter and circumradius: pairwise distance is
continuous, and a closed ball contains \(S\) exactly when it contains
\(\overline S\).  Apply the construction to \(K\) and restrict its five
parts to \(S\).  The common constant \(\Gamma<1\) in (2) preserves strictness
even when a part of \(S\) does not attain its diameter.
