# Weighted harmonic/Metzler shadow

For any rank-five Gram matrix \(G\), define the degree-two harmonic Gram
matrix
\[
H_2=\frac{5G\circ G-J}{4}.
\]
Then \(H_2\succeq0\) and \(\operatorname{rank}H_2\leq14\).  Put
\[
B=I+J-2G,\qquad W=B\circ(3J-B),\qquad M=W-4I.
\]
The exact entrywise identity is
\[
M=\frac65J-2G-\frac{16}{5}H_2.
\tag{1}
\]
For a kissing code, \(0\leq B_{ij}\leq3\) off the diagonal, hence
\[
W\geq0,\qquad W_{ii}=0,\qquad 0\leq W_{ij}\leq\frac94.
\tag{2}
\]
Equation (1) gives
\[
\operatorname{rank}M\leq1+5+14=20
\tag{3}
\]
and \(M\) is negative semidefinite on \({\bf1}^{\perp}\).

If weighted isotropy holds, then \(Gp=H_2p=0\), so
\[
\boxed{Mp=\frac65{\bf1}.}
\tag{4}
\]
In particular, every vector in \(\ker M\) is orthogonal to \({\bf1}\), and
\(M\) has exactly one positive eigenvalue.

An equivalent positive-semidefinite shadow is
\[
K=\frac{\frac65J-M}{26/5}
=\frac5{13}G+\frac8{13}H_2.
\tag{5}
\]
It satisfies
\[
K\succeq0,\quad \operatorname{rank}K\leq19,\quad
K_{ii}=1,\quad Kp=0.
\]
For \(g=G_{ij}\in[-1,1/2]\),
\[
K_{ij}=\frac{10g^2+5g-2}{13}
\in\left[-\frac{21}{104},\frac3{13}\right].
\tag{6}
\]
The lower endpoint occurs at \(g=-1/4\); both \(g=-1\) and \(g=1/2\)
map to the upper endpoint.

Thus the weighted branch has a 41-point centered spherical shadow in
dimension at most 19 with the narrow two-sided interval (6).  Proving that
no such shadow can also arise from the quadratic Veronese relation in (5)
would eliminate the branch.  Dropping that relation may be too weak.

`analyze_best_weighted_transform.py` shows how close the current
41-point near-minimizer is to this exact system.  It has:

- maximum original inner product about `0.5149946525`;
- full-support weighted design floor about `0.02175608`;
- numerical inertia of \(M\): one positive, 21 zero, 19 negative;
- shadow rank 19 and weighted centroid residual below floating tolerance.

The only sign failure is \(W_{ij}<0\) on the violating original pairs
\(G_{ij}>1/2\).  Therefore rank, inertia, equilibrium, and the harmonic
shadow have no visible numerical margin by themselves.
