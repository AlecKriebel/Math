# Route B: eliminate a universal diameter edge

**Scope:** first-principles diameter-graph reduction.  No literature or web
search was used.

## Result

Let \(S\subset\mathbb R^4\) be bounded and have positive diameter \(D\).  If
two points \(a,b\in S\) are at distance \(D\) from one another and from every
other point, then \(S\) has a five-partition whose parts have diameter
strictly below \(D\).  In particular, a finite six-chromatic diameter graph
in \(\mathbb R^4\) has no universal \(K_2\).

The earlier four-cycle determinant after a universal \(K_2\) is therefore a
special case of a stronger fact: the entire residual diameter graph is
three-colorable.  The key spherical statement works for every positive inner
product threshold, not only the value \(1/3\) arising here.

## 1. An acute spherical diameter graph in three dimensions

**Lemma 1.**  Let \(X\) be a compact set of unit vectors in \(\mathbb R^3\),
and suppose that

\[
 \langle x,y\rangle\ge c\qquad(x,y\in X),                 \tag{1}
\]

where \(0<c<1\).  Then \(X\) has a three-partition such that, within each
part, all inner products have a uniform lower bound strictly above \(c\).

**Proof.**  Let \(C=\operatorname{conv}X\), and let \(p\in C\) minimize
\(\lVert p\rVert\).  Condition (1) implies \(p\ne0\): for every convex
combination \(q=\sum_i\lambda_i x_i\),

\[
 \lVert q\rVert^2
 =\sum_{i,j}\lambda_i\lambda_j\langle x_i,x_j\rangle
 \ge c>0.                                                  \tag{2}
\]

The closest-point inequality gives

\[
 \langle p,x\rangle\ge\lVert p\rVert^2
 \qquad(x\in X).                                          \tag{3}
\]

Indeed, the right derivative at zero of
\(\lVert p+t(x-p)\rVert^2\) is nonnegative.

The exposed face

\[
 F=C\cap\{z:\langle p,z\rangle=\lVert p\rVert^2\}
\]

contains \(p\) and lies in an affine plane.  Hence \(p\) is a convex
combination of at most three points \(x_1,\ldots,x_m\) of \(X\), with
\(m\le3\).  If their weights are \(\lambda_i\), then

\[
\begin{aligned}
 \lVert p\rVert^2
 &\ge \sum_i\lambda_i^2
       +c\sum_{i\ne j}\lambda_i\lambda_j\\
 &=c+(1-c)\sum_i\lambda_i^2\\
 &\ge c+\frac{1-c}{3}=\frac{1+2c}{3}.                    \tag{4}
\end{aligned}
\]

Put \(n=p/\lVert p\rVert\) and

\[
 k=\sqrt{\frac{1+2c}{3}},\qquad \rho=\arccos k.
\]

Equations (3) and (4) place every point of \(X\) in the spherical cap

\[
 \langle n,x\rangle\ge k.                                \tag{5}
\]

Choose polar coordinates about \(n\):

\[
 x=(\sin r\cos\theta,\sin r\sin\theta,\cos r),
 \qquad 0\le r\le\rho.
\]

First suppose that \(\lVert p\rVert>k\).  Use the smaller cap radius
\(\rho'=\arccos\lVert p\rVert<\rho\).  Divide the longitude circle into three
half-open sectors of width \(2\pi/3\), and color a point by its sector.  Points
on the polar axis may be given any color.  If two nonpolar points have the
same color, their longitude difference satisfies
\(|\Delta|<2\pi/3\).  Therefore

\[
\begin{aligned}
 \langle x,y\rangle
 &=\cos r\cos s+\sin r\sin s\cos\Delta\\
 &>\cos r\cos s-\frac12\sin r\sin s\\
 &\ge \cos^2\rho'-\frac12\sin^2\rho'\\
 &=\frac32\lVert p\rVert^2-\frac12>c.                    \tag{6}
\end{aligned}
\]

For the middle inequality, the displayed expression is decreasing in each
of \(r,s\in[0,\rho']\), so its minimum occurs at
\(r=s=\rho'\).  A polar point has inner product at least
\(\lVert p\rVert>c\) with every point in the cap.  This case has an explicit
uniform margin.

It remains to handle the sharp case \(\lVert p\rVert=k\).  Equality in both
steps of (4) is rigid: exactly three active points occur, their weights are all
\(1/3\), and all three mutual inner products equal \(c\).  Each active point
has polar cosine \(k\).  Their three longitudes therefore have pairwise cosine

\[
 \frac{c-k^2}{1-k^2}=-\frac12,
\]

so, after rotating longitude, they are \(0,2\pi/3,4\pi/3\).

Center the three half-open sectors at those longitudes.  If one color class
failed to have a uniform margin, compactness would give a limiting pair in
the closure of that sector with inner product \(c\).  Equality in the two
inequalities leading to (6) forces both polar radii to equal \(\rho\) and the
longitude difference to equal \(2\pi/3\).  The two longitudes must therefore
be the boundary rays of the sector.  Every boundary ray is opposite one of
the three active longitudes.  An outer-cap point on such a ray would have
inner product

\[
 \cos(2\rho)=2k^2-1=\frac{4c-1}{3}<c                    \tag{7}
\]

with that active point, contradicting (1).  Hence limiting equality cannot
occur.  Compactness now supplies a uniform strict margin for each of the
three color classes.  This proves the lemma. \(\square\)

The half-open convention assigns every nonpolar point exactly once.  The
additional equality analysis is what prevents sequences on opposite sector
boundaries from losing strictness in the compact case.

## 2. Apply the lemma after a universal diameter edge

First assume that \(S\) is compact.  Its residual set is compact as well:
every residual point is at distance \(D\) from each of \(a,b\), so those two
points are isolated from it.  Scale \(D=1\), place the midpoint of \(a,b\) at
the origin, and write

\[
 a=-\frac12e,\qquad b=\frac12e
\]

for a unit vector \(e\).  For any residual point
\(x\in S\setminus\{a,b\}\), the two universal-edge equations give

\[
 \lVert x-a\rVert^2=\lVert x-b\rVert^2=1.
\]

Subtracting them and then using either one yields

\[
 \langle x,e\rangle=0,\qquad \lVert x\rVert^2=\frac34.  \tag{8}
\]

Thus

\[
 y_x=\frac2{\sqrt3}x
\]

is a unit vector in the three-dimensional space \(e^\perp\).  For two
residual points, the global diameter bound is equivalent to

\[
 1\ge\lVert x-z\rVert^2
 =\frac34\lVert y_x-y_z\rVert^2
 =\frac32\bigl(1-\langle y_x,y_z\rangle\bigr),
\]

so

\[
 \langle y_x,y_z\rangle\ge\frac13.                       \tag{9}
\]

Equality in (9) holds exactly when \(x,z\) are a diameter pair.  Lemma 1 with
\(c=1/3\) partitions the residual compact set into three sets whose original
diameters are uniformly below one.  Give \(a\) and \(b\) two new singleton
parts.  This is the required five-partition.

For an arbitrary bounded, nonclosed \(S\), pass first to its closure.  The
diameter is unchanged, and continuity preserves all universal-edge
equalities.  Apply the compact result and intersect its five parts with
\(S\).

## 3. Exact constants and consequences

At \(c=1/3\), the cap calculation is

\[
 k^2=\frac59,qquad
 \cos^2\rho-\frac12\sin^2\rho
 =\frac59-\frac12\frac49=\frac13.                        \tag{10}
\]

No approximation enters the proof.  In particular, every finite
counterexample candidate must satisfy all of the following increasingly
strong pruning conditions already established in this program:

1. it is \(K_5\)-free;
2. it contains no \(K_6-e\) diameter subgraph;
3. it contains no universal diameter \(K_2\); and
4. it contains no pair of completely cross-joined blocks each carrying two
   diameter edges.

The equality-rigidity paragraph in Lemma 1 supplies the closure analysis, so
the theorem is a genuine positive partial result for arbitrary bounded sets,
not only a finite diameter-graph obstruction.
