# Quadratic Gram Kernels: Exact Constraints and Exact Barriers

## Scope

This note records a useful rank-aware reformulation and two exact
counterexamples to overstrong versions of it.  It does **not** prove an upper
bound for the five-dimensional kissing number.

## The dimension-five quadratic kernel

Let \(G=(g_{ij})\) be the Gram matrix of \(N\) unit vectors in
\(\mathbb R^5\), with \(g_{ij}\leq1/2\) for \(i\ne j\).  Define
\[
p(t)=(t+1)(t-\tfrac12)=t^2+\tfrac12t-\tfrac12
\]
and \(K=p[G]\), where the polynomial is applied entrywise.  Then
\[
K_{ii}=1,\qquad K_{ij}\leq0\quad(i\ne j).
\tag{1}
\]

For \(S^4\), the normalized degree-two zonal polynomial is
\[
P_2(t)=\frac{5t^2-1}{4}.
\]
Consequently, with
\[
H_2=P_2[G]=\frac{5(G\circ G)-J}{4},
\]
we have
\[
K=\frac45H_2+\frac12G-\frac3{10}J.
\tag{2}
\]
Both \(G\) and \(H_2\) are positive semidefinite Gram matrices: \(G\) is the
linear-feature Gram matrix, while \(H_2\) is the degree-two harmonic-feature
Gram matrix.  Therefore
\[
\operatorname{rank}G\leq5,\qquad
\operatorname{rank}H_2\leq14,
\]
and (2) yields
\[
\operatorname{rank}K\leq20,\qquad n_-(K)\leq1.
\tag{3}
\]
A hypothetical 41-point code would thus produce a \(41\times41\) matrix
satisfying (1)--(3).

The sign, rank, and inertia statements alone are not enough.

## A 49-vertex finite-field counterexample

Let \(V=\mathbb F_7^2\).  Define a Cayley graph \(L\) on \(V\) by joining two
distinct points when they have equal first coordinate, equal second
coordinate, or equal coordinate sum.  Its connection set is
\[
\{(t,0),(0,t),(t,-t):t\in\mathbb F_7^\times\}.
\]

For a character
\[
\chi_{a,b}(x,y)=\zeta^{ax+by},
\]
the adjacency eigenvalue of \(L\) is
\[
s(a)+s(b)+s(a-b),\qquad
s(c)=
\begin{cases}
6,&c=0,\\
-1,&c\ne0.
\end{cases}
\]
For nonzero \((a,b)\), at most one of \(a=0,b=0,a=b\) holds.  Exactly
\(3(7-1)=18\) nonzero pairs satisfy one of them.  Hence
\[
\operatorname{Spec}(L)=18^1,\ 4^{18},\ (-3)^{30}.
\]

Let \(A=J-I-L\) be the complement adjacency matrix and put
\[
M=I-\frac12A.
\]
On constants, \(A\) has eigenvalue \(30\).  On the orthogonal complement of
constants, complementation changes a nontrivial \(L\)-eigenvalue \(\lambda\)
to \(-1-\lambda\).  Thus
\[
\operatorname{Spec}(A)=30^1,\ 2^{30},\ (-5)^{18}
\]
and
\[
\operatorname{Spec}(M)=(-14)^1,\ 0^{30},\
\left(\frac72\right)^{18}.
\tag{4}
\]
In particular, \(M\) has order 49, rank 19, diagonal one, off-diagonal
entries \(0\) or \(-1/2\), and exactly one negative eigenvalue.

There is also a 41-by-41 principal example with exactly one negative
eigenvalue.  Retain
\[
Q=\{(0,0),(1,1),(2,4),(3,2)\}
\]
while deleting
\[
(0,1),\ldots,(0,6),(1,0),(1,2).
\]
The first coordinates, second coordinates, and coordinate sums of the four
points in \(Q\) are separately all distinct, so \(Q\) is a clique of \(A\).
The vector equal to one on \(Q\) and zero elsewhere has quadratic form
\[
4+12(-1/2)=-2
\]
under the retained principal submatrix of \(M\).  Thus that submatrix has at
least one negative eigenvalue.  Restriction of a quadratic form cannot
increase its negative index, so it has exactly one, and its rank is at most
19.

This example even preserves the forgotten PSD-minus-rank-one shape:
\[
M+\frac3{10}J\succeq0,\qquad
\operatorname{rank}\left(M+\frac3{10}J\right)=19.
\tag{5}
\]
Indeed, (4) shows that adding \(3J/10\) changes the constant eigenvalue from
\(-14\) to \(7/10\) and leaves the other eigenspaces unchanged.  Its diagonal
is \(13/10\), exactly as in the dimension-five matrix below.

Therefore no argument using only (1), (3), the interval
\(p([-1,1/2])=[-9/16,0]\), or even (5) can rule out order 41.

## An actual polynomial-kernel counterexample in dimension six

The failure is not confined to abstract sign matrices.  Let \(G\) be the Gram
matrix of the normalized \(D_d\) roots, of cardinality
\(N=2d(d-1)\), and put
\[
B=G\circ G,\qquad K=B+\frac12G-\frac12J=p[G].
\]

The nonzero eigenvalues of \(B\) can be read from quadratic feature space:

- \(2(d-1)\) on the constants;
- \(d-2\), with multiplicity \(d-1\), on traceless diagonal quadratics;
- \(2\), with multiplicity \(d(d-1)/2\), on off-diagonal symmetric tensors.

The linear features are orthogonal to the quadratic features by antipodality,
and \(G\) has eigenvalue \(2(d-1)\) there, with multiplicity \(d\).  The
constant vector has \(G\)-eigenvalue zero.  It follows that \(K\) has spectrum
\[
\begin{array}{c|c}
\text{eigenvalue}&\text{multiplicity}\\ \hline
-(d-1)(d-2)&1\\
d-2&d-1\\
2&d(d-1)/2\\
d-1&d\\
0&2d(d-1)-d(d+3)/2.
\end{array}
\tag{6}
\]
For \(d=6\), this becomes
\[
-20^1,\quad4^5,\quad2^{15},\quad5^6,\quad0^{33}.
\]
Thus the exact 60-point \(D_6\) code produces an actual entrywise polynomial
kernel of rank \(27<60/2\) with the sign pattern (1) and exactly one negative
eigenvalue.  Any dimension-free rank-versus-sign shortcut is false.

## Information that survives the counterexamples

In dimension five, set
\[
R=K+\frac3{10}J=\frac45H_2+\frac12G.
\tag{7}
\]
Then
\[
R\succeq0,\quad \operatorname{rank}R\leq19,\quad R_{ii}=\frac{13}{10},
\]
but, crucially, its two summands in (7) come from one common \(G\) and remain
separately constrained:
\[
\frac12G\preceq R,\qquad \frac45H_2\preceq R.
\]
If the eigenvalues of \(R\) are in decreasing order, the Ky Fan variational
principle gives
\[
\sum_{i=1}^5\lambda_i(R)\geq\frac N2,\qquad
\sum_{i=1}^{14}\lambda_i(R)\geq\frac{4N}{5}.
\tag{8}
\]
For example, choose the rank-five projector onto the range of \(G\).  Its
trace against \(R-G/2\succeq0\) is nonnegative, so its trace against \(R\)
is at least \(\operatorname{tr}(G/2)=N/2\); maximizing over rank-five
projectors proves the first inequality.  The second is identical with
\((4/5)H_2\).

The finite-field matrix fails (8): the largest eigenvalue of the full PSD
matrix in (5) is \(7/2\), and no principal restriction has a larger one.
Hence the top-five sum of a 41-point restriction is at most \(35/2<41/2\).
This precisely demonstrates why the separate harmonic factors matter.

Other exact surviving constraints include
\[
\operatorname{tr}(G^2)\geq\frac{N^2}{5},\qquad
\operatorname{tr}(H_2^2)\geq\frac{N^2}{14},
\]
by fixed trace and rank, together with the nonlinear common-source identity
\[
R_{ij}=g_{ij}^2+\frac12g_{ij}-\frac15.
\tag{9}
\]

A viable rank proof must use (8), (9), or equivalent common-source
information.  The combined sign, rank, inertia, entry range, diagonal, and
PSD-minus-rank-one decomposition are rigorously insufficient.
