# Shifted-\(W\) sign-rank audit

## Result

The tempting implication
\[
\begin{gathered}
M_{ii}=-4,\quad M_{ij}\geq0\ (i\ne j),\quad
n_+(M)\leq1\\
\Longrightarrow\quad
\operatorname{rank}M\geq\left\lceil\frac N2\right\rceil
\end{gathered}
\]
is false.  It remains false at \(N=41\), with
\(0\leq M_{ij}\leq9/4\), with rank at most twenty, and even with the
stronger domination \(M\preceq(6/5)J\).

The exact counterexample has rank seventeen.  It is then ruled out by a
short degree-two harmonic moment calculation, pinpointing the common-source
condition that a valid kissing-code argument still has to use.

## Exact construction

Let the first forty vertices be the projective points of
\(\mathbb F_3^4\).  Choose one representative of each one-dimensional
subspace and join distinct \(x,y\) when
\[
[x,y]=x_0y_1-x_1y_0+x_2y_3-x_3y_2=0
\quad\text{in }\mathbb F_3.
\]
The verifier enumerates the points and checks directly that the adjacency
matrix \(A\) satisfies
\[
A^2=8I-2A+4J,\qquad A{\bf1}=12{\bf1}.
\]
Thus this is the point graph of the symplectic generalized quadrangle
\(W(3,3)\), with strongly regular parameters \((40,12,2,4)\).  On
\({\bf1}^{\perp}\),
\[
(A-2I)(A+4I)=0.
\]
Using \(\operatorname{tr}A=0\), its exact spectrum is
\[
12^1,\qquad 2^{24},\qquad(-4)^{15}.
\]

Append one isolated vertex, let \(A'\) be the resulting \(41\)-by-\(41\)
adjacency matrix, and set
\[
W=2A',\qquad M=W-4I.
\]
Then \(W\) is symmetric, has zero diagonal, and has off-diagonal entries
only \(0\) and \(2\).  Exactly,
\[
\operatorname{Spec}(M)
=20^1,\quad0^{24},\quad(-12)^{15},\quad(-4)^1.
\]
In particular,
\[
n_+(M)=1,\qquad \operatorname{rank}M=17<21.
\]

This improves the rank of the existing 41-vertex Cayley principal
counterexample in `proofs/rank_kernel_barriers.md` from at most nineteen to
exactly seventeen.

## Even rank-one domination is insufficient

Put
\[
Q=\frac65J-M.
\]
On the sum-zero subspace of the first forty coordinates, \(Q=-M\) has
eigenvalues zero and twelve.  On vectors of the form
\((c{\bf1}_{40},z)\), its quadratic form is
\[
1120c^2+96cz+\frac{26}{5}z^2.
\]
The coefficient matrix has first leading minor \(1120\) and determinant
\[
1120\frac{26}{5}-48^2=3520>0.
\]
Therefore \(Q\succeq0\), and exact elimination gives
\(\operatorname{rank}Q=17\).  Equivalently,
\[
M\preceq\frac65J
\]
with a PSD remainder of rank at most nineteen.  The sign, interval, inertia,
rank, and rank-one-minus-PSD properties still do not imply the desired
rank bound.

## The common-source condition excludes the fake

For an actual spherical-code Gram matrix \(G=(g_{ij})\), the transform is
\[
W_{ij}=2(1-g_{ij}-2g_{ij}^2)\quad(i\ne j).
\]
Hence a pair with \(W_{ij}=2\) must have
\[
g_{ij}\in\{0,-1/2\},
\]
and a pair with \(W_{ij}=0\) must have
\[
g_{ij}\in\{1/2,-1\}.
\]

There are 240 edges and 580 nonedges in the 41-vertex construction.  Let
\(e\) be the number of edges assigned \(g=-1/2\), and let \(a\) be the
number of nonedges assigned \(g=-1\).  Unit vectors can have only one
antipode, so \(a\leq20\).

For
\[
H_2=\frac{5(G\circ G)-J}{4},
\]
the squared entry \(H_{2,ij}^2\) is \(1/16\) at \(g=0\), \(1/256\) at
\(g=\pm1/2\), and \(1\) at \(g=-1\).  It follows exactly that
\[
\begin{aligned}
\operatorname{tr}H_2^2
&=41+2\left(
\frac{240-e}{16}+\frac e{256}
+\frac{580-a}{256}+a\right)\\
&=\frac{2417}{32}-\frac{15e}{128}+\frac{255a}{128}\\
&\leq\frac{923}{8}.
\end{aligned}
\]
But a genuine degree-two harmonic Gram matrix in dimension five is PSD,
has rank at most fourteen, and has trace 41.  Cauchy--Schwarz forces
\[
\operatorname{tr}H_2^2\geq\frac{41^2}{14}
=\frac{1681}{14}.
\]
The bounds are incompatible:
\[
\frac{1681}{14}-\frac{923}{8}=\frac{263}{56}>0.
\]

Thus the fake is rejected by an exact low-degree Hadamard moment identity.
This is also a concrete warning: any viable rank proof must retain the
nonlinear relation \(H_2=(5G\circ G-J)/4\), rather than only the combined
matrix rank and inertia.

## Sharp semidefinite remnant

The half-rank bound *is* valid when the positive inertia is zero.  If a
symmetric Metzler matrix with strictly negative diagonal is negative
semidefinite, permute it into blocks corresponding to the connected
components of its positive off-diagonal graph.  Perron--Frobenius, applied
after a scalar diagonal shift, says that the largest eigenvalue of each
irreducible block is simple.  Therefore each block contributes at most one
zero eigenvalue.  A one-vertex block is strictly negative, so every zero
eigenvalue consumes at least two indices.  Hence
\[
\operatorname{nullity}M\leq\left\lfloor\frac N2\right\rfloor,
\qquad
\operatorname{rank}M\geq\left\lceil\frac N2\right\rceil.
\]
This is sharp for disjoint blocks
\(\left(\begin{smallmatrix}-4&4\\4&-4\end{smallmatrix}\right)\), plus one
\((-4)\) block when \(N\) is odd.  The \(W(3,3)\) construction proves that
allowing even one positive eigenvalue destroys the conclusion.

## Reproduction

```sh
python3 \
  experiments/w_shift_sign_rank_audit/verify_sign_rank_counterexample.py
python3 -m unittest discover \
  -s experiments/w_shift_sign_rank_audit \
  -p 'test_*.py' -v
```

Only the Python standard library is required.

SHA-256 values for the machine-checked core are

```text
cb88a10d2a8cfb16eaf521e36e728337a7ed3f714b8226db1855cfa8fefb56b4  sign_rank_counterexample.json
8d301f6149ebba2a98fe910a69f38a264f9fe0a5d72e95ca137c799b7146c37f  verify_sign_rank_counterexample.py
756552de077db287e4ef3cb009f60aa8b4258889f6132b84fd0689cb450ebe1a  test_sign_rank_counterexample.py
```
