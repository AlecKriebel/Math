# Exact audit of the centered quarter-grid spectral endpoint

## Scope and result

This note proves the following restricted theorem.

> **Theorem.** There is no centered 41-point spherical code in
> \(\mathbb R^5\) whose off-diagonal inner products lie in
> \[
> \{-1,-3/4,-1/2,-1/4,0,1/4,1/2\}
> \]
> and whose integer color-square sum
> \(Q=\sum_{i<j}(4\langle x_i,x_j\rangle)^2\) is \(2362\).
> In particular, there is no such code whose unordered edge-count vector,
> in the displayed grid order, is
> \[
> E=(0,100,55,207,173,35,250).
> \]

The theorem eliminates the exact integer endpoint found in
`result_degree_lift_exact_spectral_d0.json`.  It does **not** eliminate
noncentered codes, off-grid codes, or other centered quarter-grid edge
distributions, so it is not an upper bound for the unrestricted
five-dimensional kissing problem.

The only imported geometric result is the established four-dimensional
kissing theorem
\[
\tau(4)=24.
\]
A primary reference is O. R. Musin, *The kissing number in four
dimensions*, Annals of Mathematics **168** (2008), 1--32,
<https://doi.org/10.4007/annals.2008.168.1>.

## 1. Exact trace normalization

Let \(G\) be the \(41\)-by-\(41\) Gram matrix and put
\[
a_{ij}=4G_{ij}.
\]
Thus \(a_{ii}=4\), while the off-diagonal entries are the seven integers
\(-4,-3,\ldots,2\).  Let
\[
Q=\sum_{i<j}a_{ij}^2,\qquad
P=\sum_{i<j<k}a_{ij}a_{ik}a_{jk}.
\]
The displayed edge counts give, by direct integer arithmetic,
\[
\sum E_k=820,\qquad
\sum kE_k=-82,\qquad
Q=\sum k^2E_k=2362.
\]
The middle equality is consistent with centering: every off-diagonal row
sum of \(A=4G\) is \(-4\).

Pad the nonzero eigenvalues of \(G\) with zeros to obtain five
nonnegative numbers \(\lambda_1,\ldots,\lambda_5\).  This is legitimate
because \(\operatorname{rank}G\leq5\), and
\(\sum\lambda_i=\operatorname{tr}G=41\).  Define
\[
\begin{aligned}
V&=\sum_{r=1}^5(\lambda_r-41/5)^2
   =\operatorname{tr}(G^2)-1681/5,\\
D&=\sum_{r=1}^5(\lambda_r-41/5)^3\\
 &=\operatorname{tr}(G^3)
   -\frac{123}{5}\operatorname{tr}(G^2)
   +\frac{137842}{25}.
\end{aligned}
\]
Counting the terms in the two traces gives
\[
\operatorname{tr}(G^2)=41+\frac Q8,
\qquad
\operatorname{tr}(G^3)=41+\frac{3Q}{8}+\frac{3P}{32}.
\]
Consequently the scaled quantities
\[
X=40V,\qquad Y=800D
\]
are the integers
\[
X=5Q-11808,\qquad
Y=3636864-2160Q+75P.
\]
Under the theorem's hypothesis \(Q=2362\), this becomes
\[
X=2,\qquad Y\equiv-6\pmod {75}.
\]

## 2. The sharp five-eigenvalue inequality

We use the exact inequality
\[
20D^2\leq9V^3. \tag{1}
\]
For completeness, let \(\delta_r=\lambda_r-41/5\), so
\(\sum\delta_r=0\), \(V=\sum\delta_r^2\), and
\(D=\sum\delta_r^3\).  If \(V=0\), (1) is immediate.  Otherwise normalize
to \(V=1\) and maximize or minimize \(D\) on the compact intersection
\[
\sum\delta_r=0,\qquad\sum\delta_r^2=1.
\]
The two constraint gradients are independent.  Lagrange multipliers show
that every \(\delta_r\) solves one common quadratic equation, so an
extremizer has at most two distinct coordinates.  If one value has
multiplicity \(m\) and the other multiplicity \(5-m\), direct substitution
gives
\[
\frac{D^2}{V^3}
=\frac{(5-2m)^2}{5m(5-m)}
\leq\frac9{20}.
\]
Equality holds exactly for multiplicities \(1\) and \(4\).

In terms of \(X,Y\), inequality (1) is
\[
2Y^2\leq9X^3.
\]
Since \(X=2\), it gives \(|Y|\leq6\).  The congruence
\(Y\equiv-6\pmod {75}\) therefore forces
\[
Y=-6,\qquad V=\frac1{20},\qquad D=-\frac3{400}.
\]
Equality holds in (1).  The sign of \(D\), the trace, and the equality
case above now determine the five eigenvalues exactly:
\[
\{\lambda_1,\ldots,\lambda_5\}
=\left\{8,\frac{33}{4},\frac{33}{4},
             \frac{33}{4},\frac{33}{4}\right\}. \tag{2}
\]
In particular, the hypothetical Gram matrix has rank exactly five; no
rank-deficient boundary case was discarded.

## 3. The full matrix identity and the height vector

Choose a rank-five Gram factorization
\[
G=X^{\mathsf T}X
\]
whose columns \(x_i\) are the code points.  The frame operator
\(XX^{\mathsf T}\) has the positive spectrum (2).  Choose a unit
\(8\)-eigenvector \(u\), and define
\[
z=X^{\mathsf T}u,\qquad z_i=\langle u,x_i\rangle.
\]
Then
\[
\|z\|^2=8,\qquad Gz=8z,\qquad \sum_i z_i=0,
\]
where the last equality uses the assumed centering \(X{\bf1}=0\).
The spectral projector onto the \(8\)-eigenspace is \(zz^{\mathsf T}/8\).
Applying (2) on the two positive eigenspaces and on the kernel gives the
exact matrix identity
\[
G^2=\frac{33}{4}G-\frac14zz^{\mathsf T}. \tag{3}
\]

Every entry of \(G^2\) lies in \(\frac1{16}\mathbb Z\).  Therefore the
off-diagonal part of (3), and in fact the same formula on the diagonal,
gives
\[
z_i z_j=33G_{ij}-4(G^2)_{ij}\in\frac14\mathbb Z. \tag{4}
\]
Since \(u\) and every \(x_i\) are unit vectors, \(|z_i|\leq1\).  Taking
\(i=j\) in (4) yields
\[
z_i^2\in\{0,1/4,1/2,3/4,1\}. \tag{5}
\]

If \(z_i,z_j\ne0\), then
\[
\frac{z_i}{z_j}=\frac{z_i z_j}{z_j^2}\in\mathbb Q.
\]
Thus all nonzero \(z_i^2\) have the same class in
\(\mathbb Q^\times/(\mathbb Q^\times)^2\).  Among the four nonzero
possibilities in (5), the square classes are
\[
\{1/4,1\},\qquad\{1/2\},\qquad\{3/4\}. \tag{6}
\]

## 4. Centered row parity

For a fixed row, write
\[
q_i=\sum_{j\ne i}a_{ij}^2.
\]
The diagonal of (3), multiplied by \(16\), gives
\[
q_i=116-4z_i^2. \tag{7}
\]
Centering gives \(\sum_{j\ne i}a_{ij}=-4\).  Since \(n^2\equiv n\pmod2\)
for every integer \(n\),
\[
q_i\equiv\sum_{j\ne i}a_{ij}\equiv0\pmod2. \tag{8}
\]
Equations (7)--(8) exclude \(z_i^2=1/4\) and \(z_i^2=3/4\).
Combining this with the square-class restriction (6) and
\(\sum z_i^2=8\) leaves exactly two alternatives:
\[
\begin{array}{c|ccc}
&\#\{z_i^2=0\}&\#\{z_i^2=1/2\}&\#\{z_i^2=1\}\\ \hline
\text{I}&33&0&8\\
\text{II}&25&16&0.
\end{array} \tag{9}
\]

## 5. Four-dimensional obstruction

In either row of (9), at least 25 code points have \(z_i=0\).  Those
points are unit vectors in the four-dimensional space \(u^\perp\), and
their pairwise inner products remain at most \(1/2\), including all
boundary contacts.  They would therefore form a kissing configuration of
at least 25 points in \(\mathbb R^4\), contradicting \(\tau(4)=24\).
This proves the theorem.

## What the finite artifacts show

The discovery output stored one particular edge vector, triple-count vector,
and mixture of integer row degrees.  The proof above eliminates every
centered quarter-grid edge vector with \(Q=2362\), not merely the stored
edge vector.  The stored row mixture is already incompatible with (7):
its exact value of
\[
\sum_iq_i^2
\]
is \(555192\), whereas alternatives I and II force respectively
\[
8(112)^2+33(116)^2=544400
\]
and
\[
16(114)^2+25(116)^2=544336.
\]
This scalar check by itself rejects that particular triple/row witness,
but not the edge vector.

To check that no hidden strength is being attributed to this observation,
`endpoint_row_marginal_shadows.json` contains two exact countermodels to
the weaker marginal argument.  One for each row of (9), it satisfies:

- the fixed edge counts;
- nonnegative integer counts of all feasible quarter-grid triangle types;
- the forced cubic product \(P=19534\), hence \(Y=-6\);
- exact edge--triangle incidence;
- exact first and second integer row-degree marginals;
- the centered row equation, robust depth conditions, contact-degree
  bound, and the \(-3/4\)-neighbour bound;
- the pointwise energy equation (7).

The two shadows are not labeled matrices.  They do not assign row copies
to common vertices, assign signs to their \(z\)-values, or satisfy (3)
entry by entry.  Their survival proves that aggregate row marginals are
not the mechanism eliminating the endpoint.  The decisive additional
information is the geometric common-source fact that all zero-height rows
belong to one \(S^3\).

Run the standard-library exact checker with

```sh
python3 \
  experiments/centered_global_count_milp/spectral_endpoint_audit/verify_endpoint.py
```

The checker uses no solver and no floating-point arithmetic.  It rebuilds
the 51 closed-domain triangle types, verifies both shadows, checks the
source discovery file by SHA-256, and repeats all endpoint trace
arithmetic.  It does not attempt to re-prove the imported theorem
\(\tau(4)=24\).

## Dependency map

1. The centered quarter-grid hypothesis and \(Q=2362\) fix \(X\) and the
   residue class of \(Y\).
2. The five-eigenvalue inequality plus integer cubic congruence forces
   \(X=2,Y=-6\).
3. Its equality case gives the spectrum (2).
4. The spectrum gives the common height vector and matrix identity (3).
5. Quarter-grid arithmetic, square classes, and centered row parity give
   the two alternatives (9).
6. The established theorem \(\tau(4)=24\) eliminates both alternatives.

No step assumes rigidity, antipodality, a contact graph, rational
coordinates, or uniqueness of a 40-point code.  The quarter-grid and
centering hypotheses are explicit restrictions of this theorem, not
consequences asserted for a general extremizer.
