# Exact obstruction to pairwise allocation of the pair-sector budget

## Status

This note does **not** disprove the qutrit pair-sector inequality
\[
 \left\|\sum_{i=1}^3D_{\widehat i}V\right\|_2^2
 \leq
 2\sum_{i=1}^3\|B_{\widehat i}\|_2^2,
 \qquad
 D_{\widehat i}=I_i\otimes B_{\widehat i},
 \tag{1}
\]
where every \(B_{\widehat i}\) is doubly traceless and
\(V:\mathbb C^2\to(\mathbb C^3)^{\otimes3}\) is an isometry.
It gives an exact rational obstruction to the most natural cyclic
proof of (1).

If
\[
 d_i=2\|B_{\widehat i}\|_2^2-\|D_{\widehat i}V\|_2^2,
 \tag{2}
\]
then the deficit in (1) is
\[
 {\cal D}
 =
 \sum_i d_i
 -
 2\sum_{i<j}\operatorname{Re}
 \langle D_{\widehat i}V,D_{\widehat j}V\rangle.
 \tag{3}
\]
The symmetric half-budget allocation writes this exactly as
\[
 {\cal D}=\sum_{i<j}q_{ij},
 \qquad
 q_{ij}
 =
 \frac{d_i+d_j}{2}
 -
 2\operatorname{Re}
 \langle D_{\widehat i}V,D_{\widehat j}V\rangle.
 \tag{4}
\]
The example below has
\[
 \boxed{q_{13}=-3}
 \tag{5}
\]
even though the full deficit is
\[
 \boxed{{\cal D}=10}.
 \tag{6}
\]
Thus the three cyclic interactions cannot be proved independently
with this canonical allocation.  Positive compensation from the
third pair is essential even when only two pair components of \(D\)
are nonzero.

The dependency-free exact checker is
`verification/verify_n3_pair_sector_cyclic_budget_obstruction.py`.

## Construction

Let
\[
 E=|1\rangle\langle0|,
 \qquad
 Z=\operatorname{diag}(1,1,-2),
 \qquad
 T=\operatorname{diag}(4,-2,-2).
 \tag{7}
\]
All three matrices are traceless.  Define the two nonzero pair
components
\[
 \begin{aligned}
 B_{\widehat1}&=E^{(2)}\otimes Z^{(3)},&
 D_{\widehat1}&=I^{(1)}\otimes E^{(2)}\otimes Z^{(3)},\\
 B_{\widehat3}&=T^{(1)}\otimes E^{(2)},&
 D_{\widehat3}&=T^{(1)}\otimes E^{(2)}\otimes I^{(3)},
 \end{aligned}
 \tag{8}
\]
and put \(B_{\widehat2}=D_{\widehat2}=0\).  Both pair coefficients in
(8) are doubly traceless.

Take the right singular plane
\[
 V|0\rangle=|000\rangle,
 \qquad
 V|1\rangle=|001\rangle.
 \tag{9}
\]
The pair-coefficient norms are
\[
 \|B_{\widehat1}\|_2^2
 =\|E\|_2^2\|Z\|_2^2=6,
 \qquad
 \|B_{\widehat3}\|_2^2
 =\|T\|_2^2\|E\|_2^2=24.
 \tag{10}
\]
On each of the two columns of \(V\), \(D_{\widehat1}\) has amplitude
\(1\), while \(D_{\widehat3}\) has amplitude \(4\), and the output
basis vectors coincide.  Therefore
\[
 \begin{aligned}
 \|D_{\widehat1}V\|_2^2&=2,\\
 \|D_{\widehat3}V\|_2^2&=32,\\
 \langle D_{\widehat1}V,D_{\widehat3}V\rangle&=8.
 \end{aligned}
 \tag{11}
\]
Equations (2) and (11) give
\[
 d_1=12-2=10,\qquad d_2=0,\qquad d_3=48-32=16.
 \tag{12}
\]
Substitution in (4) yields
\[
 q_{13}=\frac{10+16}{2}-2(8)=-3,
 \tag{13}
\]
whereas
\[
 q_{12}=5,\qquad q_{23}=8.
 \tag{14}
\]
Their sum is the positive full deficit
\[
 {\cal D}=-3+5+8=10.
 \tag{15}
\]
Equivalently,
\[
 \|(D_{\widehat1}+D_{\widehat3})V\|_2^2
 =2(1+4)^2=50,
 \tag{16}
\]
while the right side of (1) is
\[
 2(6+24)=60.
 \tag{17}
\]

## Consequence

The obstruction is not caused by a full-support interior code: the
plane (9) has one-site support ranks \((1,1,2)\).  Nor is it caused by
complicated pair coefficients: both nonzero coefficients share the
same rank-one matrix unit on their overlapping site and use diagonal
traceless matrices on the other sites.

Any cyclic Gram proof must therefore route unused diagonal budget
between different pair interactions.  In particular, proving all
three \(q_{ij}\geq0\), or applying an independent two-component
contraction with half of each \(d_i\), is strictly stronger than the
desired theorem and is false.
