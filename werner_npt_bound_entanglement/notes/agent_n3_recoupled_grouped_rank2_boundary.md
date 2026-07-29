# The grouped Schmidt-rank-two recoupling: exact reduction and boundary Hessian

## Status

Let
\[
 {\cal B}=\widehat{\cal K}-L\widehat{\cal K}R
 \tag{1}
\]
be the four-species recoupled operator in
`agent_n3_local_s4_recoupling_nogo.md`.  This note investigates the
stronger proposed inequality
\[
 \langle a\otimes b,{\cal B}(a\otimes b)\rangle\geq0
 \tag{2}
\]
when the coefficient matrices of \(a\) across \(L_1:L_2\) and of
\(b\) across \(R_1:R_2\) both have rank at most two.

The global statement (2) is **not proved here**.  The exact results are:

1. undoing the right partial transpose gives a simple four-block norm
   formula;
2. rank at most four of the regrouped matrix is grossly insufficient:
   the corresponding relaxation is negative already at rank two;
3. the genuine Kronecker rank-two problem reduces exactly to one
   \(4\times4\) exterior Gram matrix tested only on a positive product
   vector;
4. the known rank-three negative family is positive at rank one,
   zero at rank two, and negative at rank three;
5. the complete constrained quadratic form at its rank-two zero is
   positive semidefinite.  It acts on a real tangent space of
   dimension \(416\), has rank \(354\) and nullity \(62\), and splits
   into two isospectral \(208\times208\) rational blocks.

Thus the canonical zero has no negative quadratic direction inside
the grouped rank-two variety.  Because the quadratic form has a
62-dimensional real kernel, this does not exclude a higher-order
negative branch tangent to that kernel, and it says nothing about a
distant negative point.

The dependency-free exact checker is
`verification/verify_n3_recoupled_rank2_boundary.py`.

## 1. The four projection blocks

Let
\[
 {\cal H}=(\mathbb C^3)^{\otimes3}
 \quad\hbox{and}\quad
 {\cal E}={\cal H}_L\otimes\overline{{\cal H}_R}.
 \tag{3}
\]
On \({\cal E}\), let
\[
 P=\Pi_2,\qquad Q=I-P,\qquad Y=2I-3P.
 \tag{4}
\]
Write \(A,B\in M_{27}\) for the coefficient matrices of \(a,b\).
After taking the full transpose on the right grouped factor and
regrouping the two complete replicas, the coefficient matrix is
\[
 M=A\otimes\overline B
 \tag{5}
\]
on \({\cal E}:{\cal E}\), up to the fixed interleaving of physical
sites.  Put
\[
 K=\frac{M-M^{\mathsf T}}2.
 \tag{6}
\]
The original replica swap becomes matrix transposition.  Since it
commutes with \(Y\otimes Y\),
\[
\begin{aligned}
 \langle a\otimes b,{\cal B}(a\otimes b)\rangle
 &=2\langle K,(Y\otimes Y)K\rangle\\
 &=8\|K_{QQ}\|_2^2
   -4\|K_{PQ}\|_2^2-4\|K_{QP}\|_2^2
   +2\|K_{PP}\|_2^2,
 \tag{7}
\end{aligned}
\]
where
\[
 K_{RS}=RKS^{\mathsf T},\qquad R,S\in\{P,Q\}.
 \tag{8}
\]
Because \(K^{\mathsf T}=-K\) and \(P^{\mathsf T}=P\),
\[
 \|K_{PQ}\|_2=\|K_{QP}\|_2.
 \tag{9}
\]
Therefore (2) is exactly
\[
 \boxed{\qquad
 4\|K_{QQ}\|_2^2+\|K_{PP}\|_2^2
 \geq4\|K_{PQ}\|_2^2.
 \qquad}
 \tag{10}
\]

This formula is useful computationally: it applies the three local
scalar/traceless projections directly to a \(3^{12}\)-entry tensor
and never constructs the ambient operator.

## 2. Why rank and Pfaffian relations alone cannot work

Suppose the Kronecker condition in (5) is discarded and only
\(\operatorname{rank}M\leq4\) is retained.  Choose real unit vectors
\[
 p\in\operatorname{Ran}P,\qquad q\in\operatorname{Ran}Q,
 \tag{11}
\]
and set
\[
 M=pq^{\mathsf T}-qp^{\mathsf T}.
 \tag{12}
\]
Then
\[
 \operatorname{rank}M=2,\qquad K=M,
 \tag{13}
\]
and the only nonzero blocks are
\[
 K_{PQ}=pq^{\mathsf T},\qquad
 K_{QP}=-qp^{\mathsf T}.
 \tag{14}
\]
The left side of (10) is zero and its right side is \(4\).
Equivalently, (7) has value \(-8\).

One can take, for example, \(p\) proportional to
\[
 E_{01}\otimes E_{01}\otimes I_3
 \tag{15}
\]
and \(q\) proportional to
\[
 E_{01}\otimes E_{01}\otimes E_{01}.
 \tag{16}
\]
They lie in exact degrees two and three, respectively.

Thus neither \(\operatorname{rank}M\leq4\), the vanishing of its
five-by-five minors, nor a Pfaffian bound on \(K\) can prove (10).
The factorization \(M=A\otimes\overline B\), together with the two
separate third-exterior-power identities, is indispensable.

## 3. Canonical Schmidt-two reduction

Take Schmidt decompositions
\[
\begin{aligned}
 a&=s_1x_1\otimes y_1+s_2x_2\otimes y_2,\\
 b&=t_1p_1\otimes q_1+t_2p_2\otimes q_2,
\end{aligned}
 \tag{17}
\]
where all four displayed pairs are orthonormal and
\[
 s_i,t_j\geq0.
 \tag{18}
\]
After the right conjugation in (5), define
\[
 e_{ij}=x_i\otimes\overline p_j,\qquad
 f_{ij}=y_i\otimes\overline q_j,
 \tag{19}
\]
and the normalized exterior vectors
\[
 z_{ij}=e_{ij}\wedge f_{ij}
 =\frac{e_{ij}\otimes f_{ij}-f_{ij}\otimes e_{ij}}{\sqrt2}.
 \tag{20}
\]
Let \(W\) be the \(4\times4\) Hermitian matrix, indexed by
\((i,j)\in\{1,2\}^2\), with
\[
 \boxed{\qquad
 W_{ij,kl}
 =\langle z_{ij},(Y\otimes Y)z_{kl}\rangle.
 \qquad}
 \tag{21}
\]
Expansion of the exterior product gives the intrinsic determinant
formula
\[
\boxed{
\begin{aligned}
 W_{ij,kl}
={}&
 \langle e_{ij},Ye_{kl}\rangle
 \langle f_{ij},Yf_{kl}\rangle\\
 &-
 \langle e_{ij},Yf_{kl}\rangle
 \langle f_{ij},Ye_{kl}\rangle.
\end{aligned}}
 \tag{22}
\]

Put
\[
 \lambda=(s_1t_1,s_1t_2,s_2t_1,s_2t_2)^{\mathsf T}.
 \tag{23}
\]
Using
\[
 P_-\operatorname{vec}M
 =\frac1{\sqrt2}\sum_{i,j}s_it_jz_{ij},
 \tag{24}
\]
equation (7) becomes
\[
 \boxed{\qquad
 \langle a\otimes b,{\cal B}(a\otimes b)\rangle
 =\lambda^\dagger W\lambda.
 \qquad}
 \tag{25}
\]

This is a strict reduction.  The remaining grouped-rank-two theorem
is the following positive-Segre copositivity statement:

> For every four orthonormal two-frames in (17), the matrix \(W\) in
> (21)--(22) is nonnegative on every vector
> \((s_1,s_2)\otimes(t_1,t_2)\) with nonnegative real entries.

It is not necessary that \(W\) itself be positive semidefinite.
The singular values in (17), rather than arbitrary four
coefficients, are exactly the surviving nonlinear Kronecker
constraint.

## 4. A basic rank-two exterior inequality

The rank threshold in the known example is governed by an elementary
matrix inequality which may be useful in a global proof.

### Lemma 1

Let \(u,v\) be bipartite vectors with coefficient matrices \(U,V\).
If \(\operatorname{rank}U\leq2\), then
\[
 \boxed{\quad
 |\langle u,v\rangle|^2
 \leq
 \operatorname{Tr}(\rho_u^L\rho_v^L)
 +\operatorname{Tr}(\rho_u^R\rho_v^R).
 \quad}
 \tag{26}
\]
No rank assumption on \(V\) is required.

#### Proof

Apply left and right unitaries so that
\[
 U=\operatorname{diag}(\sigma_1,\sigma_2,0,\ldots).
 \tag{27}
\]
In the transformed coordinates,
\[
 \langle u,v\rangle
 =\sigma_1V_{11}+\sigma_2V_{22}.
 \tag{28}
\]
The two reduced overlaps on the right side of (26) are
\[
\begin{aligned}
 \operatorname{Tr}(UU^\dagger VV^\dagger)
 &=\sum_{i=1}^2\sigma_i^2\sum_j|V_{ij}|^2,\\
 \operatorname{Tr}(U^\dagger U V^\dagger V)
 &=\sum_{i=1}^2\sigma_i^2\sum_j|V_{ji}|^2.
\end{aligned}
 \tag{29}
\]
Together they contain
\[
 2\sum_{i=1}^2\sigma_i^2|V_{ii}|^2.
 \tag{30}
\]
Finally,
\[
 |\sigma_1V_{11}+\sigma_2V_{22}|^2
 \leq2\sum_{i=1}^2\sigma_i^2|V_{ii}|^2,
 \tag{31}
\]
which proves the claim. \(\square\)

For equal rank-two Schmidt coefficients and aligned frames, equality
holds in (26).  For equal rank-three coefficients, it fails by the
factor \(3/2\).

## 5. The exact \(\Phi_r\) threshold

Let
\[
 \Phi_r=\frac1{\sqrt r}\sum_{j=0}^{r-1}|j,j\rangle,
 \qquad r=1,2,3.
 \tag{32}
\]
Use the site-product vectors
\[
\begin{array}{c|ccc}
 &1&2&3\\ \hline
 a_i&|0,1\rangle&|0,0\rangle&\Phi_r\\
 b_i&|0,1\rangle&|1,1\rangle&\Phi_r .
\end{array}
 \tag{33}
\]
The first two sites reduce (7) to
\[
 \frac13\left(
 \operatorname{Tr}(\rho_a^{L_1}\rho_b^{R_1})
 +\operatorname{Tr}(\rho_a^{L_2}\rho_b^{R_2})
 -|\langle a_3,b_3\rangle|^2
 \right).
 \tag{34}
\]
At the third site the two reduced overlaps are \(1/r\), while the
global overlap is one.  Hence
\[
 \boxed{\qquad
 \langle a\otimes b,{\cal B}(a\otimes b)\rangle
 =\frac13\left(\frac2r-1\right).
 \qquad}
 \tag{35}
\]
Thus the values at grouped Schmidt ranks \(1,2,3\) are exactly
\[
 \frac13,\qquad0,\qquad-\frac19.
 \tag{36}
\]
Lemma 1 proves the nonnegativity of the more general third-site
version of (34) whenever either third-site coefficient matrix has
rank at most two.

## 6. Complete constrained Hessian at the rank-two zero

Put
\[
\begin{aligned}
 A_0&=\frac1{\sqrt2}
 E_{01}\otimes E_{00}\otimes
 \operatorname{diag}(1,1,0),\\
 B_0&=\frac1{\sqrt2}
 E_{01}\otimes E_{11}\otimes
 \operatorname{diag}(1,1,0).
\end{aligned}
 \tag{37}
\]
Both matrices have Hilbert--Schmidt norm one and rank two.  They are
the \(r=2\) point in (33).

Let \({\cal O}=(I-F)(Y\otimes Y)\), so the recoupled value is
\[
 \langle\operatorname{vec}M,{\cal O}\operatorname{vec}M\rangle,
 \qquad M=A\otimes\overline B.
 \tag{38}
\]
At (37), not only is the expectation zero, but
\[
 M_0=A_0\otimes\overline{B_0}
\tag{39}
\]
is a constrained critical point:
\[
 \boxed{\qquad
 \operatorname{Re}\langle M_1,{\cal O}M_0\rangle=0
 \quad\hbox{for every rank-two tangent }M_1.
 \qquad}
 \tag{40}
\]
Importantly,
\[
 {\cal O}M_0\ne0.
 \tag{41}
\]
It is a normal vector, rather than zero.  Consequently the second
fundamental form of the determinantal variety must be included in the
true constrained Hessian.

The complex tangent space of the rank-two determinantal variety at a
\(27\times27\) rank-two matrix has dimension
\[
 2(27+27-2)=104.
 \tag{42}
\]
Use \(C=\overline B\) as the second complex matrix coordinate, and
let \(X,Y_1\) be tangent matrices at \(A_0,C_0=B_0\).  The first
variation of \(M=A\otimes C\) is
\[
 M_1=X\otimes C_0+A_0\otimes Y_1.
 \tag{43}
\]

To retain rank two exactly, split rows and columns into the two
support coordinates and their complements.  In this chart,
\[
\begin{pmatrix}
 A_{11}&A_{12}\\ A_{21}&A_{22}
\end{pmatrix},
\qquad
 A_{22}=A_{21}A_{11}^{-1}A_{12},
 \tag{44}
\]
and similarly for \(C\).  Since the base support block is
\(D=I_2/\sqrt2\), a real one-parameter direction has
\[
\begin{aligned}
 A(t)&=A_0+tX+t^2Z_A+O(t^3),&
 (Z_A)_{22}&=X_{21}D^{-1}X_{12},\\
 C(t)&=C_0+tY_1+t^2Z_C+O(t^3),&
 (Z_C)_{22}&=(Y_1)_{21}D^{-1}(Y_1)_{12}.
 \end{aligned}
 \tag{45}
\]
Thus
\[
 M_2=Z_A\otimes C_0+A_0\otimes Z_C+X\otimes Y_1
 \tag{46}
\]
and the true quadratic coefficient is
\[
 \boxed{\quad
 [t^2]\langle M(t),{\cal O}M(t)\rangle
 =
 \langle M_1,{\cal O}M_1\rangle
 +2\operatorname{Re}\langle M_2,{\cal O}M_0\rangle.
 \quad}
 \tag{47}
\]
The second term in (47) is essential.

Choose the standard matrix-unit tangent bases.  In the computational
ordering used in the verifier, the row and column supports are
\[
\begin{array}{c|cc}
 &\text{rows}&\text{columns}\\ \hline
 A_0&\{0,1\}&\{9,10\}\\
 B_0&\{3,4\}&\{12,13\}.
\end{array}
 \tag{48}
\]
A matrix unit is tangent exactly when its row belongs to the listed
row support or its column belongs to the listed column support.
This gives \(104+104=208\) complex coordinates.

All base data are real.  Write a complex tangent vector as its real
and imaginary parts.  The quadratic form (47) has no real--imaginary
cross term and splits into two \(208\times208\) real symmetric
blocks
\[
 H_+=G+N,\qquad H_-=G-N,
 \tag{49}
\]
where \(G\) is the tangent-linear term
\(\langle M_1,{\cal O}M_1\rangle\), and \(N\) is the normal/second-
fundamental-form term in (47).  The exact checker reconstructs both
blocks over \(\mathbb Q\).  They are isospectral, \(18H_\pm\) are
integer matrices, and each nonzero graph has
\[
 64\text{ blocks of size }1,\quad
 40\text{ of size }2,\quad
 14\text{ of size }4,\quad
 1\text{ of size }8.
 \tag{50}
\]
Exact rational elimination on those blocks gives, for each of
\(H_+\) and \(H_-\), the spectrum
\[
\begin{array}{c|rrrrrrrrr}
\lambda&
0&1/9&1/6&1/3&5/9&2/3&7/9&5/6&1\\ \hline
\text{mult.}&
31&1&4&15&1&23&8&16&6
\end{array}
\tag{51}
\]
and
\[
\begin{array}{c|rrrrrrrrrr}
\lambda&
7/6&11/9&4/3&3/2&14/9&5/3&11/6&2&7/3&3\\ \hline
\text{mult.}&
24&3&8&16&5&32&4&1&6&4.
\end{array}
\tag{52}
\]
In particular,
\[
 \boxed{\quad
 H_+\succeq0,\quad H_-\succeq0,\quad
 \operatorname{rank}_{\mathbb R}H_{\rm full}=354,\quad
 \dim_{\mathbb R}\ker H_{\rm full}=62.
 \quad}
 \tag{53}
\]

This rules out a negative branch having a nonzero quadratic
component transverse to the Hessian kernel.  It does not control the
quartic term along a Hessian-flat direction, so (53) is a local
obstruction, not a proof of (2).

## 7. Remaining exact lemma

The rank-only relaxation is false by (11)--(16), while the canonical
rank-two boundary has no quadratic instability by (53).  The exact
unresolved assertion is now (25):
\[
 \bigl((s_1,s_2)\otimes(t_1,t_2)\bigr)^\dagger
 W
 \bigl((s_1,s_2)\otimes(t_1,t_2)\bigr)\geq0
 \tag{54}
\]
for all nonnegative Schmidt coefficients and all four physical
two-frames.

Numerical projected-gradient searches using the four-block formula
(7), including unrestricted complex rank-two matrices, converged to
zero and found no negative value.  Exhaustive choices were not made,
and this is discovery evidence only.  At rank three, initialization
near (33) converges back to the exact negative value \(-1/9\), so the
same search detects the known negative basin.

The most direct positive proof would be a sum-of-squares certificate
for (54) modulo
\[
 \bigwedge\nolimits^3A=0,\qquad
 \bigwedge\nolimits^3B=0.
 \tag{55}
\]
The counterexample (12) proves that a certificate using only
\(\operatorname{rank}M\leq4\) cannot exist.
