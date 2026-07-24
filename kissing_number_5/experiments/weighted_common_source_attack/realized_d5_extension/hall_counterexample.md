# Exact counterexample to the \(3/4\)-cap Hall conjecture

Let scaled extension coordinates be
\[
z_\pm=
\left(
\pm\frac12,\,
-\frac{\sqrt3}{2},\,
0,\,
-\frac{\sqrt3}{2},\,
\pm\frac12
\right),
\qquad y_\pm=\frac{z_\pm}{\sqrt2}.
\tag{1}
\]
Then \(\|z_\pm\|^2=2\), so \(y_\pm\in S^4\).

Using the exact polar inequalities from `aggregate_identities.md`, with
\[
|z_1|=|z_5|=\frac12,\quad |z_3|=0,\quad
z_2=z_4=-\frac{\sqrt3}{2},
\]
we obtain
\[
\begin{aligned}
z_4+|z_1|&=(1-\sqrt3)/2\le1,\\
-z_2+|z_3|&=\sqrt3/2\le1,\\
z_2+|z_5|&=(1-\sqrt3)/2\le1,\\
-z_4+|z_3|&=\sqrt3/2\le1,\\
|z_1|+|z_5|&=1.
\end{aligned}
\]
Thus both points lie in the exact support polar region.

Their mutual inner product is
\[
\langle y_+,y_-\rangle
=\frac12\,z_+\cdot z_-
=\frac12\left(-\frac14+\frac34+\frac34-\frac14\right)
=\frac12.
\tag{2}
\]
Hence they are compatible, including the closed boundary.

Let
\[
v=\frac{(0,-1,0,-1,0)}{\sqrt2},
\]
one of the 28 omitted \(D_5\) roots.  For both signs,
\[
\langle v,y_\pm\rangle=\frac12(0,-1,0,-1,0)\cdot z_\pm
=\frac{\sqrt3}{2}>\frac34.
\tag{3}
\]
For every other omitted root \(w=r/\sqrt2\), exact inspection gives
\[
r\cdot z_\pm\le\frac{1+\sqrt3}{2}<\frac32,
\tag{4}
\]
because the only omitted root collecting both negative coordinates is
\((0,-1,0,-1,0)\).  Therefore
\[
\{w:\langle w,y_+\rangle\ge3/4\}
=\{v\}
=\{w:\langle w,y_-\rangle\ge3/4\}.
\tag{5}
\]

The two cap-neighborhood sets have a union of cardinality one, so they do
not admit distinct representatives.  This refutes the proposed Hall
strengthening already at subset size two.  The exact verifier
`verify_hall_counterexample.py` checks (1)--(5) in
\(\mathbb Q(\sqrt3)\), including the non-strict kissing boundary.

This does **not** refute Hall matching for the full strict conflict sets at
threshold \(1/2\).  In the deterministic ordering of `completion_roots()`,
exact calculation gives
\[
\begin{aligned}
F(y_+)&=\{2,9,12,17,25\},\\
F(y_-)&=\{0,8,12,16,24\}.
\end{aligned}
\tag{6}
\]
Thus both full conflict degrees are five, their intersection is the single
overloaded \(3/4\)-center \(12\), and their union has cardinality nine.
Any charging rule proposed for the \(3/4\)-cover must pass this pair, while a
full-conflict Hall rule has ample neighboring centers available here.
