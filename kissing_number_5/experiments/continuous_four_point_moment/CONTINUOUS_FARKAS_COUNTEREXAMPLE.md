# Continuous rank-five counterexample to the pool Farkas atom sign

## 1. The two sides of the exact Farkas ray

For the joint \((H,\Gamma)\) moment extension in
[`FACTORIAL_HIERARCHY.md`](FACTORIAL_HIERARCHY.md), the three-multiplier
ray has two different column types.

For a proposed global representing state
\[
H\ge7,\qquad \Gamma\ge0,
\]
its coefficient is
\[
\Gamma\left(
-\frac5{39}
+\frac{2109}{\binom{39}{5}}\binom H4
\right).
\]
Since
\[
\frac{2109}{\binom{39}{5}}=\frac1{273},
\qquad
\frac5{39}=\frac{35}{273},
\]
this factors as
\[
\begin{aligned}
\frac{\Gamma}{273}\left(\binom H4-\binom74\right)
&=\frac{
\Gamma(H-7)(H+4)(H^2-3H+30)
}{6552}\\
&\ge0.                                               \tag{1}
\end{aligned}
\]
The factorization is universal: \(H-7\ge0\), \(H+4>0\), and the
quadratic has negative discriminant.

For an anchored local K7 flag, let

- \(h\) be the number of five sampled residual vertices in the
  negative-\((y+z)\) depth set;
- \(g\) be the number common to the two endpoint caps
  \(\langle x,y\rangle,\langle x,z\rangle\ge1/4\);
- \(n_{155}\) count those common vertices whose two incident colors are
  exactly \(1/4,1/4\), with base color \(-3/4\).

The corresponding atom coefficient is
\[
\Phi_{\rm atom}
=g-n_{155}-2109\binom h4g.                           \tag{2}
\]

Every atom in the 1,782-column discovery pool satisfies (2) with
equality.  So does the one added repair atom.  The question is whether
rank-five Gram PSD forces \(\Phi_{\rm atom}\ge0\) on the full continuous
domain.

It does not.

## 2. Exact Gram counterexample

In the order
\[
(y,z,w,x_1,x_2,x_3,x_4),
\]
consider
\[
G=\begin{pmatrix}
1&-\frac34&\frac14&-\frac14&-\frac14&-\frac14&-\frac14\\
-\frac34&1&\frac14&-\frac14&-\frac14&-\frac14&-\frac14\\
\frac14&\frac14&1&0&-\frac23&-\frac23&-\frac23\\
-\frac14&-\frac14&0&1&\frac13&\frac13&\frac13\\
-\frac14&-\frac14&-\frac23&\frac13&1&\frac13&\frac13\\
-\frac14&-\frac14&-\frac23&\frac13&\frac13&1&\frac13\\
-\frac14&-\frac14&-\frac23&\frac13&\frac13&\frac13&1
\end{pmatrix}.                                      \tag{3}
\]

Every off-diagonal entry is at most \(1/2\).

An explicit realization explains its rank.  Let \(u,v\) be orthonormal,
and let \(t_1,t_2,t_3,t_4\) be the vertices of a regular tetrahedron in a
three-dimensional space orthogonal to \(u,v\), normalized so that
\[
\langle t_i,t_j\rangle=-\frac13\quad(i\ne j).
\]
Set
\[
\begin{aligned}
y&=\frac1{2\sqrt2}u+\sqrt{\frac78}\,v,&
z&=\frac1{2\sqrt2}u-\sqrt{\frac78}\,v,\\
w&=\frac1{\sqrt2}(u+t_1),&
x_i&=\frac1{\sqrt2}(-u+t_i).
\end{aligned}                                       \tag{4}
\]
These seven unit vectors have Gram matrix (3), proving \(G\succeq0\)
and \(\operatorname{rank}G\le5\).  They span \(u,v\) and the tetrahedron
space, so the rank is exactly five.

The same fact is visible from a Schur complement.  The base block is
\[
A=\begin{pmatrix}1&-3/4\\-3/4&1\end{pmatrix}\succ0.
\]
The Schur complement of \(A\) in (3) is one half of the Gram matrix of
\[
(t_1,t_1,t_2,t_3,t_4).
\]
It is PSD of rank three.  Thus the full matrix is PSD of rank
\(2+3=5\).

## 3. Negative atom value

At the distinguished base \((y,z)\):

- all four \(x_i\) obey
  \[
  \langle x_i,y\rangle+\langle x_i,z\rangle=-\frac12<0,
  \]
  so \(h=4\);
- \(w\) has both endpoint inner products equal to \(1/4\), while none of
  the \(x_i\) is common, so \(g=1\);
- the unique common point has exact incident pair \((1/4,1/4)\), so
  \(n_{155}=1\).

Therefore
\[
\Phi_{\rm atom}
=1-1-2109\binom44
=-2109<0.                                           \tag{5}
\]

The base \(yz=-3/4\) is the only \(-3/4\) edge in (3), so the
unanchored sum has the same negative value.

## 4. What the factorization really used

The nonnegative state factor (1) follows only from the global integer
bound \(H\ge7\).  The zero atom coefficients in the discovery pool used
an additional support property:

\[
\text{no supported anchored K7 flag has }h\ge4
\text{ and }g\ge1.                                  \tag{6}
\]

That property is neither a rank-five identity nor a consequence of Gram
PSD.  Matrix (3) is an exact counterexample.  It also contains the
continuous inner products \(1/3\) and \(-2/3\), exposing why a pool built
from the quarter alphabet can silently enforce (6).

Hence the three-multiplier Farkas ray cannot be promoted to a
continuous-support upper-bound certificate.  A valid continuation would
need an additional invariant that excludes (3) for a reason applicable
inside a full 41-point code, or it must include such atoms in the local
moment cone.
