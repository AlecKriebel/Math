# Full-conflict Hall theorem through union size three

Let \(R=D_5\) denote the 40 raw roots of squared norm \(2\), let \(S\) be
the fixed 12-root support, and let \(V=R\setminus S\).  For a scaled
extension point \(z=\sqrt2y\), define its **full conflict set**
\[
F(z)=\{v\in V:v\cdot z>1\}.
\tag{1}
\]
Because \(r\cdot z\le1\) for \(r\in S\), this is also the full set of
\(D_5\) roots whose normalized inner product with \(y\) is greater than
\(1/2\).

This file proves:

> **Small-union Hall theorem.** If \(A\) is a pairwise compatible family of
> extension points and
> \[
> T=\bigcup_{z\in A}F(z)
> \]
> has cardinality at most three, then \(|A|\le|T|\).

The distinction between the strict conflict threshold \(>1/2\) and the
closed kissing threshold \(\le1/2\) is essential.

## 1. One- and two-root removal rigidity

### Theorem

If \(T\subset R\) and \(1\le|T|\le2\), every vector \(z\) satisfying
\[
\|z\|^2=2,\qquad r\cdot z\le1\quad(r\in R\setminus T)
\tag{2}
\]
belongs to \(T\).

### Pair-orbit reduction

Signed coordinate permutations preserve the \(D_5\) root set.  An unordered
pair of distinct roots has one of five types:

| raw inner product | support intersection |
|---:|---:|
| \(-2\) | 2 |
| \(-1\) | 1 |
| \(0\) | 0 |
| \(0\) | 2 |
| \(1\) | 1 |

The exact finite verifier recomputes the respective orbit cardinalities
\(20,240,240,40,240\).  Send one removed root to
\[
v=(-1,-1,0,0,0).
\]
The five pair types have representatives
\[
\begin{aligned}
-v&=(1,1,0,0,0),\\
(1,0,-1,0,0),\quad
(0,0,-1,-1,0),\quad
(-1,1,0,0,0),\quad
(-1,0,-1,0,0).
\end{aligned}
\tag{3}
\]

### Same coordinate pair

First suppose the two removed roots use coordinates \(1,2\).  Every signed
root on a pair involving one of coordinates \(3,4,5\) remains.  Put
\[
t=\max(|z_3|,|z_4|,|z_5|).
\]
Then
\[
|z_1|,|z_2|\le1-t,
\]
and, among the last three magnitudes, the two other than the maximum are at
most \(\min(t,1-t)\).  Hence
\[
\|z\|^2\le
2(1-t)^2+t^2+2\min(t,1-t)^2.
\tag{4}
\]
For \(0\le t\le1/2\), the right side is
\(2-4t+5t^2\); for \(1/2\le t\le1\), it is
\(4(1-t)^2+t^2\).  Convexity on the two closed intervals shows that (4) is
at most \(2\), with equality only at \(t=0\).  Equality in (2) then requires
\(|z_1|=|z_2|=1\), and the signed inequalities that remain on the
\((1,2)\)-pair select exactly the two removed sign patterns.  This covers
the antipodal and same-support orthogonal types.

### One shared coordinate

Next suppose the removed roots use pairs \((1,2)\) and \((1,3)\).  The full
set of signed roots on \((2,3)\) remains.  Put
\[
t=\max(|z_4|,|z_5|).
\]
Now \(|z_1|,|z_2|,|z_3|\le1-t\) and
\(|z_2|+|z_3|\le1\).  If \(t\le1/2\), then
\[
z_2^2+z_3^2\le(1-t)^2+t^2;
\]
if \(t\ge1/2\), then
\[
z_2^2+z_3^2\le2(1-t)^2.
\]
Adding the bounds for \(z_1,z_4,z_5\) gives exactly the same two upper
expressions as in (4).  Thus equality again forces \(t=0\),
\(|z_1|=1\), and exactly one of \(|z_2|,|z_3|\) to equal \(1\).
The surviving signed inequalities select precisely the two removed roots.
This covers raw inner products \(-1\) and \(1\).

### Disjoint supports

Finally suppose the removed roots use disjoint coordinate pairs
\((1,2)\) and \((3,4)\).  Put
\[
A=\max(|z_1|,|z_2|),\quad
B=\max(|z_3|,|z_4|),\quad
c=|z_5|.
\]
All cross-pair signed roots remain, so
\[
A+B\le1,\qquad A+c\le1,\qquad B+c\le1.
\tag{5}
\]
The compact polytope in (5) has vertices
\[
0,\ (1,0,0),\ (0,1,0),\ (0,0,1),\ (1/2,1/2,1/2).
\]
The convex quadratic \(2A^2+2B^2+c^2\) is at most \(2\) at these vertices
and hence throughout the polytope.  Equality is possible only at
\((A,B,c)=(1,0,0)\) or \((0,1,0)\).  Equality in the original norm then
forces both coordinates in the corresponding pair to have magnitude one,
and the remaining signed inequalities select the removed root.

This proves the theorem for two removed roots.  The one-root statement
follows either from its first case directly or by intersecting the
two-root conclusions obtained after adding two different auxiliary removed
roots.

### Conflict-degree consequence

For \(v\in V\), the point \(z=v\) has \(F(z)=\{v\}\).  Conversely, the
removal theorem implies
\[
\boxed{z\notin V\quad\Longrightarrow\quad |F(z)|\ge3.}
\tag{6}
\]
It also proves the small-union Hall theorem whenever \(|T|\le2\).

## 2. Classification of conflict triples

Let \(a_i=|z_i|\).  If \(a_i+a_j>1\) and both magnitudes are nonzero, exactly
one signed root on the coordinate pair \(\{i,j\}\) conflicts with \(z\).
The signs are the signs of the two coordinates.  If one magnitude vanishes
and the other exceeds one, two signed roots conflict.  Such a coordinate of
magnitude greater than one creates at least four conflicts, one on every
other coordinate pair.  Therefore a non-root point with exactly three
conflicts has \(a_i\le1\) for every \(i\), and its three conflicts are the
edges of the threshold graph
\[
\{ij:a_i+a_j>1\}.
\tag{7}
\]

Order \(a_1\ge a_2\ge\cdots\ge a_5\).  A threshold graph with exactly three
edges is of one of two forms:

- the triangle \(12,13,23\), when \(a_2+a_3>1\);
- the star \(12,13,14\), when \(a_2+a_3\le1<a_1+a_4\).

The star is impossible on \(\|z\|^2=2\).  Indeed,
\[
a_2+a_3\le1,\qquad a_1+a_5\le1,
\]
and \(a_4\le a_3\), so
\[
a_1^2+a_5^2\le1,\qquad
a_2^2+a_3^2+a_4^2
\le (1-a_3)^2+2a_3^2\le1
\]
for \(0\le a_3\le1/2\).  Equality in both bounds yields magnitudes
\((1,1,0,0,0)\), whose threshold graph has only one edge, not a star.

Thus the three coordinate supports form a triangle and the three
corresponding roots have raw pairwise inner product \(1\).  Among the 28
omitted roots there are exactly 18 such coordinate-cycle triples.  The
stabilizer of the fixed 12-root support inside the signed permutation group
has order 16 and splits the 18 triples into four orbits of sizes
\[
4,\ 8,\ 4,\ 2.
\tag{8}
\]
`verify_small_union_hall.py` recomputes the group, all 18 triples, and all
four orbits exactly.

## 3. Occupancy one in a non-root triangle patch

All coordinate-cycle triangles are equivalent under a signed coordinate
permutation, so use the three raw roots
\[
t_1=(1,1,0,0,0),\quad
t_2=(1,0,0,-1,0),\quad
t_3=(0,1,0,-1,0).
\tag{9}
\]
A non-root point with conflict set exactly this triangle has the same signs
on coordinates \(1,2,4\).  Write their magnitudes as \(a,b,c\), and write
the other two magnitudes as \(p,q\).  Then
\[
\begin{gathered}
0<a,b,c\le1,\qquad
a+b>1,\quad a+c>1,\quad b+c>1,\\
p,q\le1-\max(a,b,c),\qquad
a^2+b^2+c^2+p^2+q^2=2.
\tag{10}
\end{gathered}
\]
We prove an exact Lorentz inequality for the closure of (10).

Put
\[
x=1-a,\quad y=1-b,\quad z=1-c,
\]
order these deficits as \(0\le d\le e\le f\), and set
\[
X=d+e+f,\qquad \rho^2=p^2+q^2.
\]
The pair inequalities give \(e+f\le1\), while the cross-pair inequalities
give
\[
\rho^2\le2d^2.
\tag{11}
\]
The norm identity is
\[
\rho^2=2X-(d^2+e^2+f^2)-1.
\tag{12}
\]

Let \(u=e+f\).  Since \(d\le e\le f\), we have
\[
d^2+e^2+f^2\le2d^2+(u-d)^2.
\]
Combining this with (11)--(12) yields
\[
g(u):=u^2-2(d+1)u+5d^2-2d+1\ge0.
\tag{13}
\]
On \(2d\le u\le1\), the quadratic is decreasing up to its smaller root, so
\[
u\le1+d-2\sqrt{d(1-d)}.
\tag{14}
\]
Because \(u\ge2d\), (14) first gives \(d\le1/5\).  On this interval,
\[
\sqrt{d(1-d)}\ge d+d^2
\]
(after squaring, this is
\(1-2d-2d^2-d^3\ge0\)).  Hence (14) gives the purely rational conclusion
\[
\boxed{X\le1-2d^2.}
\tag{15}
\]

Set
\[
L=\frac{a+b+c}{2}=\frac{3-X}{2}.
\]
Equations (11), (12), and (15) imply
\[
\begin{aligned}
4(L^2-\rho^2-1)
&=(1-X)(5-X)-4\rho^2\\
&\ge (2d^2)(4)-8d^2=0.
\end{aligned}
\tag{16}
\]
Equality in (16) forces \(d=0,\rho=0,X=1\), and then (12) forces the
deficits to be a permutation of \((0,0,1)\).  Thus equality occurs exactly
at one of the three removed roots.  Every non-root point has
\[
L^2-\rho^2>1.
\tag{17}
\]

The signed main-coordinate vector is a nonnegative combination
\[
(a,b,c)=\lambda_1(1,1,0)+\lambda_2(1,0,1)
            +\lambda_3(0,1,1),
\]
because \(a,b,c\le1\) and their pair sums are at least one.  Moreover
\(\lambda_1+\lambda_2+\lambda_3=L\).  For two points with coefficients
\(\lambda,\mu\) and transverse norms \(\rho,\rho'\), their raw dot product
is bounded below by
\[
z\cdot z'
\ge LL'+\lambda\cdot\mu-\rho\rho'
\ge LL'-\rho\rho'.
\tag{18}
\]
The reverse Cauchy identity
\[
(LL'-\rho\rho')^2
-(L^2-\rho^2)(L'^2-\rho'^2)
=(L\rho'-L'\rho)^2
\]
and (16) show \(z\cdot z'\ge1\).  If either point is a non-root, (17) makes
the inequality strict:
\[
\boxed{z,z'\text{ non-roots in the same patch}
\quad\Longrightarrow\quad z\cdot z'>1.}
\tag{19}
\]
Thus a kissing code contains at most one non-root point with this exact
conflict triple.

## 4. Hall conclusion

Let \(|T|=3\).  By (6), every point whose conflict set is contained in \(T\)
is either a root in \(T\), or a non-root with conflict set exactly \(T\).
The three roots are mutually compatible.  A non-root conflicts with every
root in \(T\), and (19) prevents two non-roots from coexisting.  Hence a
compatible family with conflict union \(T\) has at most three points.

Together with the one- and two-root removal theorem, this proves the stated
small-union Hall theorem.
