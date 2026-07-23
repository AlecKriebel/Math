# An improved exact frame lower bound from a projected cap

## Status

This note strengthens the frame-conditioning lemma in
`max_volume_semialgebraic_reduction.md`.  It proves that the frame operator
of any hypothetical 41-point code is strictly larger than
\((15059/40000)I\).  It does not prove nonexistence of the code.

## An exact \(S^3\) polynomial

Let \(P_k=P_k^{(4)}\) be the normalized Gegenbauer polynomials for \(S^3\):
\[
P_0=1,\quad P_1=t,\quad
(k+2)P_{k+1}=2(k+1)tP_k-kP_{k-1}.
\]
Put
\[
s=\frac{7123}{12877},
\]
\[
q(t)=t^4+\frac{329}{200}t^3+\frac{1729}{2000}t^2
       +\frac{157}{1000}t+\frac{11}{2000},
\]
\[
r(t)=t^2-\frac{4013}{2000}t+\frac{2119}{2000},
\qquad
f(t)=(t-s)q(t)^2r(t).
\]
The exact Gegenbauer coefficients of \(f=\sum_{k=0}^{11}f_kP_k\) are
\[
\begin{array}{c|c}
k&f_k\\ \hline
0&67952343786393/6593024000000000\\
1&15765983073661/412064000000000\\
2&431885251860417/6593024000000000\\
3&33671464919107/412064000000000\\
4&80729136030847/1318604800000000\\
5&2888971220163/82412800000000\\
6&263043203507/1648256000000000\\
7&2629177469/82412800000000\\
8&5763898791/263720960000000\\
9&54981833/4120640000\\
10&206901849/26372096000\\
11&3/512.
\end{array}
\]
Every coefficient is strictly positive.  Moreover,
\[
\operatorname{disc}(r)
=-\frac{847831}{4000000}<0.
\]
Since \(r\) is monic, \(r(t)>0\) for every real \(t\).  Therefore
\[
f(t)\leq0\qquad(-1\leq t\leq s),
\]
including the boundary \(t=s\).  The Delsarte argument gives
\[
A(4,s)\leq\frac{f(1)}{f_0}
=\frac{701778046943232}{22650781262131}
=31-\frac{396172182829}{22650781262131}<31.
\]
Cardinality is integral, so
\[
\boxed{A(4,7123/12877)\leq30.}                    \tag{1}
\]

## Projection and the strict frame bound

Suppose \(x_1,\ldots,x_{41}\in S^4\) have pairwise inner products at most
\(1/2\), and let
\[
S=\sum_{i=1}^{41}x_ix_i^{\mathsf T}.
\]
Fix a unit vector \(v\), set \(z_i=v\mathbin{\cdot}x_i\), and retain the
indices with
\[
|z_i|\leq c,\qquad c=\frac{37}{200}.
\]
Project and normalize them into \(v^\perp\cong\mathbb R^4\):
\[
y_i=\frac{x_i-z_iv}{\sqrt{1-z_i^2}}\in S^3.
\]
For two retained indices,
\[
y_i\mathbin{\cdot}y_j
\leq\frac{\frac12+c^2}{1-c^2}
=\frac{7123}{12877}=s.                            \tag{2}
\]
Here is the sign-safe justification.  If the numerator
\(x_i\mathbin{\cdot}x_j-z_iz_j\) is nonpositive, the left side is at most
zero and (2) is immediate.  If it is positive, use
\(-z_iz_j\leq c^2\) and
\(\sqrt{(1-z_i^2)(1-z_j^2)}\geq1-c^2\) to obtain (2).  Thus all signs and
slab-boundary cases are covered.  Equality of two projected unit vectors
would give their inner product \(1>s\), hence the projected code has no
collisions.

By (1), at most 30 indices lie in the closed slab.  At least 11 therefore
satisfy the strict inequality \(|z_i|>c\).  Consequently
\[
v^{\mathsf T}Sv=\sum_i z_i^2>11c^2
=\frac{15059}{40000}.
\]
As this holds for every unit \(v\),
\[
\boxed{S\succ\frac{15059}{40000}I_5.}             \tag{3}
\]

This improves the previous lower bound \(9/25=14400/40000\).

## Consequence for centered spectral moments

Let \(m=41/5\), let \(\lambda_i\) be the five frame eigenvalues, and put
\(z_i=\lambda_i-m\), \(V=\sum z_i^2\), \(D=\sum z_i^3\).  With
\[
\ell=\frac{15059}{40000},\qquad h=m-\ell
=\frac{312941}{40000},
\]
equation (3) makes the localizing moment matrix for
\((\lambda-\ell)(a+bz)^2\) positive definite:
\[
\begin{pmatrix}
5h&V\\
V&hV+D
\end{pmatrix}\succcurlyeq0.
\]
In particular,
\[
5h(hV+D)\geq V^2.                                \tag{4}
\]
This is exact rank-aware information, but it does not strengthen the
small-variance witnesses currently closest to the tight-frame spectrum.
For example, the abstract completion
\((z_i)=(a,-a,a,-a,0)\) has \(D=0\) and satisfies (4) whenever
\(|a|<h\).  Thus (3) improves semialgebraic conditioning and the
large-variance moment cone, but does not close the 41-point obstruction.

## Reproduction

Run

```sh
python3 verifiers/verify_improved_frame_cap_bound.py
python3 -m unittest tests.test_improved_frame_cap_bound -v
```

The verifier expands the polynomial from its factors and reconstructs all
Gegenbauer coefficients using exact rational arithmetic.
