# Tensor-power projection inequalities

## 2026-07-28 08:01:51 PDT — Scope and initial notation

This note develops, from first principles, exact formulas and inequalities for
\[
P_S=\bigotimes_{i\in S}P_d^{(i)}
\]
on vectors whose \(A:B\) coefficient matrix has rank at most two.  The target
operator at the endpoint is
\[
X_d^{\otimes n}
=\sum_{S\subseteq[n]}\left(-\frac d2\right)^{|S|}P_S.
\]
Only local symbolic or exact computation is used for discovery.  Every retained
mathematical claim will be accompanied by a proof.

## 2026-07-28 08:14:23 PDT — Exact contraction and replica formulas

Write \([d]=\{0,\ldots,d-1\}\).  If \(S\subseteq[n]\), define the paired
partial contraction
\[
(\operatorname{Tr}_S C)_{x_{S^c},y_{S^c}}
 :=\sum_{z_S\in[d]^S}C_{(z_S,x_{S^c}),(z_S,y_{S^c})}.
\]
This is the ordinary partial trace of the matrix \(C\), after canonically
identifying its row and column tensor factors.

**Lemma 1 (exact subset overlap).**  For every matrix \(C\),
\[
\boxed{\quad
\langle\psi_C|P_S|\psi_C\rangle
=d^{-|S|}\|\operatorname{Tr}_S C\|_F^2.
\quad}                                                     \tag{1}
\]
Consequently, for every real \(\alpha\),
\[
\boxed{\quad
\langle\psi_C|X_{\alpha,d}^{\otimes n}|\psi_C\rangle
=Q_{n,\alpha}(C):=
\sum_{S\subseteq[n]}\alpha^{|S|}
\|\operatorname{Tr}_S C\|_F^2.
\quad}                                                     \tag{2}
\]
In particular the endpoint is the dimension-free alternating contraction
form
\[
Q_n(C):=Q_{n,-1/2}(C)
=\sum_{S\subseteq[n]}\left(-\frac12\right)^{|S|}
\|\operatorname{Tr}_S C\|_F^2.                             \tag{3}
\]

*Proof.*  On the tensor factors in \(S\),
\[
P_S=d^{-|S|}\sum_{p_S,q_S}|p_S,p_S\rangle\langle q_S,q_S|.
\]
The identity acts on the remaining factors.  Direct substitution therefore
gives
\[
\begin{aligned}
\langle\psi_C|P_S|\psi_C\rangle
&=d^{-|S|}\sum_{x_{S^c},y_{S^c}}
 \sum_{p_S,q_S}
 \overline{C_{(p_S,x_{S^c}),(p_S,y_{S^c})}}
 C_{(q_S,x_{S^c}),(q_S,y_{S^c})}\\
&=d^{-|S|}\sum_{x_{S^c},y_{S^c}}
\left|\sum_{q_S}C_{(q_S,x_{S^c}),(q_S,y_{S^c})}\right|^2.
\end{aligned}
\]
This is (1).  Expanding \(X_{\alpha,d}^{\otimes n}\), the coefficient
\((\alpha d)^{|S|}\) cancels the factor \(d^{-|S|}\), proving (2) and
(3). \(\square\)

There is also a useful two-replica form.  Let \(F_i\) swap the \(i\)-th
local tensor factors between two copies of
\(\mathcal K=(\mathbb C^d)^{\otimes n}\), and put
\[
K=F_1\cdots F_n,\qquad
R_\alpha=\bigotimes_{i=1}^n(I+\alpha F_i).
\]

**Lemma 2 (replica formula).**  One has
\[
\|\operatorname{Tr}_S C\|_F^2
=\operatorname{Tr}\!\left[(C^\dagger\otimes C)F_{S^c}\right]               \tag{4}
\]
and hence
\[
Q_{n,\alpha}(C)
=\operatorname{Tr}\!\left[(C^\dagger\otimes C)
  \bigotimes_{i=1}^n(F_i+\alpha I)\right]
=\operatorname{Tr}\!\left[(C^\dagger\otimes C)R_\alpha K\right].           \tag{5}
\]
If
\[
C=\sum_{a=1}^r z_a|u_a\rangle\langle v_a|,
\]
then
\[
\boxed{\quad
Q_{n,\alpha}(C)=z^\dagger Gz,\qquad
G_{ab}=
\langle u_a\otimes v_b|R_\alpha|u_b\otimes v_a\rangle .
\quad}                                                                    \tag{6}
\]

*Proof.*  In indices, inserting \(F_{S^c}\) contracts the two replicas
crosswise on \(S^c\) and separately on \(S\).  The resulting sum is
\[
\sum_{x_{S^c},y_{S^c}}\sum_{p_S,q_S}
\overline{C_{(p_S,x_{S^c}),(p_S,y_{S^c})}}
C_{(q_S,x_{S^c}),(q_S,y_{S^c})},
\]
which is the squared norm in (4).  Summing (4) with weights
\(\alpha^{|S|}\) gives the first expression in (5).  Since all swaps
commute and \(F_i^2=I\),
\[
\bigotimes_i(F_i+\alpha I)
=\left(\bigotimes_i(I+\alpha F_i)\right)K=R_\alpha K.
\]
Finally,
\[
C^\dagger\otimes C
=\sum_{a,b}\overline{z_a}z_b
 |v_a\rangle\langle u_a|\otimes|u_b\rangle\langle v_b|.
\]
In the corresponding trace, \(K\) sends
\(v_a\otimes u_b\) to \(u_b\otimes v_a\), which yields (6).
\(\square\)

At the endpoint,
\[
R_{-1/2}=\bigotimes_i\left(I-\frac12F_i\right)>0,                           \tag{7}
\]
because one local factor has eigenvalue \(1/2\) on the symmetric subspace
and \(3/2\) on the antisymmetric subspace.  Formula (6) isolates the entire
difficulty: although \(R_{-1/2}\) is positive, the indices in \(G_{ab}\)
are crossed.

**Corollary 3 (strict rank-one bound).**  If \(\operatorname{rank}C=1\),
then
\[
Q_n(C)\ge 2^{-n}\|C\|_F^2.                                                  \tag{8}
\]
More generally, for \(-1\le\alpha\le0\),
\[
Q_{n,\alpha}(C)\ge(1+\alpha)^n\|C\|_F^2.                                   \tag{9}
\]

*Proof.*  Write \(C=|u\rangle\langle v|\).  Formula (6) has one entry:
\[
Q_{n,\alpha}(C)
=\langle u\otimes v|R_\alpha|u\otimes v\rangle.
\]
For \(-1\le\alpha\le0\), the least eigenvalue of each factor
\(I+\alpha F_i\) is \(1+\alpha\).  Also
\(\|u\otimes v\|^2=\|C\|_F^2\). \(\square\)

## Sharp individual projection bounds

**Lemma 4 (rank-sensitive partial-trace bound).**  Let
\(C\) act on \(\mathbb C^m\otimes\mathbb C^k\), and suppose
\(\operatorname{rank}C\le r\).  Then
\[
\boxed{\quad
\|\operatorname{Tr}_{\mathbb C^m}C\|_F^2
\le \min\{r,m\}\|C\|_F^2 .
\quad}                                                                    \tag{10}
\]
Both constants are sharp.

*Proof.*  Let \(P\) and \(Q\) be the left and right support projections of
\(C\), so both have rank at most \(r\) and \(C=PCQ\).  For every matrix
\(A\),
\[
|\langle A,C\rangle_F|
=|\langle PAQ,C\rangle_F|
\le\|C\|_F\|PAQ\|_F.
\]
Moreover
\[
\|PAQ\|_F^2\le\|AQ\|_F^2
=\operatorname{Tr}(Q A^\dagger A)
\le\sum_{j=1}^r s_j(A)^2.                                                  \tag{11}
\]
For completeness, the last inequality follows by diagonalizing
\(A^\dagger A\): if its decreasing eigenvalues are \(\lambda_j\), then
\(\operatorname{Tr}(Q A^\dagger A)=\sum_j\lambda_jq_j\), where
\(0\le q_j\le1\) and \(\sum_jq_j\le r\).  Moving all available weight to
the largest \(\lambda_j\)'s can only increase this sum.

By Frobenius duality,
\[
\|\operatorname{Tr}_{\mathbb C^m}C\|_F
=\sup_{\|D\|_F=1}|\langle I_m\otimes D,C\rangle_F|.
\]
The singular values of \(I_m\otimes D\) are the singular values of \(D\),
each repeated \(m\) times.  Thus the sum of its largest \(r\) squared
singular values is at most \(r\|D\|_F^2=r\), and its total squared
Frobenius norm is \(m\|D\|_F^2=m\).  Applying (11) gives (10).

If \(r\le m\), choose orthonormal \(e_1,\ldots,e_r\in\mathbb C^m\) and
unit \(p,q\in\mathbb C^k\), and take
\[
C=\sum_{j=1}^r|e_j\otimes p\rangle\langle e_j\otimes q|.
\]
Then \(\|C\|_F^2=r\), while
\(\operatorname{Tr}_{\mathbb C^m}C=r|p\rangle\langle q|\), whose squared
norm is \(r^2\).  If \(m\le r\), the same construction with all \(m\)
basis vectors has rank \(m\) and ratio \(m\). \(\square\)

Combining Lemmas 1 and 4, for every nonempty \(S\) and every
\(\operatorname{rank}C\le2\) (with \(d\ge2\)),
\[
\langle\psi_C|P_S|\psi_C\rangle
\le\frac{2}{d^{|S|}}\|\psi_C\|^2,                                          \tag{12}
\]
and the constant is sharp.  This proves the optimal bound for each overlap
separately, but not their simultaneous feasible region.

## 2026-07-28 08:17:08 PDT — The exact crossed-Cauchy target

The replica formula gives a concise necessary-and-sufficient uniform
inequality.  Let \(u_1,u_2\) be orthonormal in \(\mathcal K\), and likewise
let \(v_1,v_2\) be orthonormal.  At the endpoint set
\[
\begin{aligned}
A&=\langle u_1\otimes v_1|R_{-1/2}|u_1\otimes v_1\rangle,\\
B&=\langle u_2\otimes v_2|R_{-1/2}|u_2\otimes v_2\rangle,\\
Z&=\langle u_1\otimes v_2|R_{-1/2}|u_2\otimes v_1\rangle.
\end{aligned}                                                              \tag{13}
\]

**Proposition 5 (equivalent crossed-Cauchy formulation).**  Endpoint
two-block positivity at copy number \(n\) is equivalent to
\[
\boxed{\qquad |Z|^2\le AB \qquad}                                           \tag{14}
\]
for every two orthonormal pairs as above.

*Proof.*  Every rank-at-most-two matrix has a singular-value decomposition
\[
C=z_1|u_1\rangle\langle v_1|
  +z_2|u_2\rangle\langle v_2|,
\]
where the two pairs are orthonormal; allowing arbitrary complex \(z_a\)
is equivalent to absorbing their phases into the singular vectors.  By
Lemma 2,
\[
Q_n(C)=
\begin{pmatrix}\overline z_1&\overline z_2\end{pmatrix}
\begin{pmatrix}A&Z\\\overline Z&B\end{pmatrix}
\begin{pmatrix}z_1\\z_2\end{pmatrix}.                                      \tag{15}
\]
Here \(A,B>0\) by (7).  This quadratic form is nonnegative for every
\(z_1,z_2\) exactly when its \(2\times2\) matrix is positive semidefinite,
which is exactly (14). \(\square\)

Thus the all-copy question is precisely a crossed Cauchy--Schwarz
inequality.  Ordinary Cauchy--Schwarz for the positive form induced by
\(R_{-1/2}\) instead gives
\[
|Z|^2\le
\langle u_1\otimes v_2|R_{-1/2}|u_1\otimes v_2\rangle
\langle u_2\otimes v_1|R_{-1/2}|u_2\otimes v_1\rangle,                       \tag{16}
\]
whose two diagonal factors are the wrong ones.  Bridging (16) to (14) is
not a formal consequence of positivity.

There is a useful compression interpretation.  If
\(U,V:\mathbb C^2\to\mathcal K\) are the isometries with columns \(u_a,v_b\),
then
\[
H=(U^\dagger\otimes V^\dagger)R_{-1/2}(U\otimes V)\ge0.
\]
The desired inequality (14) is the positivity of the principal minor
indexed by \(11,22\) after partial transposition in the second
\(\mathbb C^2\) index:
\[
(H^{\Gamma_2})_{\{11,22\}}
=\begin{pmatrix}H_{11,11}&H_{12,21}\\H_{21,12}&H_{22,22}\end{pmatrix}\ge0.   \tag{17}
\]
This pinpoints why positivity of \(R_{-1/2}\) alone is insufficient.

## A proved all-copy tensorization class

The crossed inequality does tensorize when the two rank-one summands
themselves factor across copies.

**Theorem 6 (two fully decomposable summands).**  Let
\[
C=z_1\bigotimes_{i=1}^n|u_{1i}\rangle\langle v_{1i}|
 +z_2\bigotimes_{i=1}^n|u_{2i}\rangle\langle v_{2i}|,                       \tag{18}
\]
with completely arbitrary local vectors (orthogonality and normalization
are not required).  Then, for every \(\alpha\ge-1/2\),
\[
Q_{n,\alpha}(C)\ge0.                                                        \tag{19}
\]
In particular no endpoint distillation witness can have a decomposition
of the form (18).

*Proof.*  For every \(i\), form the \(2\times2\) matrix
\[
G^{(i)}_{ab}
=\langle u_{ai}\otimes v_{bi}|(I+\alpha F_i)
 |u_{bi}\otimes v_{ai}\rangle.                                             \tag{20}
\]
For \(w=(w_1,w_2)\), Lemma 2 at one copy says
\[
w^\dagger G^{(i)}w
=\|D_i(w)\|_F^2+\alpha|\operatorname{Tr}D_i(w)|^2,\qquad
D_i(w)=\sum_{a=1}^2w_a|u_{ai}\rangle\langle v_{ai}|.                        \tag{21}
\]
The matrix \(D_i(w)\) has rank at most two.  Its singular values therefore
give
\[
|\operatorname{Tr}D_i(w)|
\le\|D_i(w)\|_*
\le\sqrt2\|D_i(w)\|_F.                                                      \tag{22}
\]
For \(-1/2\le\alpha<0\), equations (21)--(22) imply
\[
w^\dagger G^{(i)}w
\ge(1+2\alpha)\|D_i(w)\|_F^2\ge0;
\]
for \(\alpha\ge0\), (21) is manifestly nonnegative.  Hence every
\(G^{(i)}\) is positive semidefinite.

By the product form of the vectors in (18), Lemma 2 gives
\[
G_{ab}=\prod_{i=1}^nG^{(i)}_{ab};
\]
that is, \(G=G^{(1)}\circ\cdots\circ G^{(n)}\), the entrywise product.
For completeness, the entrywise product of two positive \(2\times2\)
matrices is positive: its diagonal entries are nonnegative and
\[
|A_{12}B_{12}|^2
\le A_{11}A_{22}B_{11}B_{22}.
\]
Induction proves positivity of the displayed \(n\)-fold product.  Finally,
\(Q_{n,\alpha}(C)=z^\dagger Gz\ge0\). \(\square\)

This proof exposes a concrete obstruction to extending the argument:
entangled \(u_a\) or \(v_a\) destroy the entrywise factorization of \(G\).

There is also a simpler multiplicativity statement useful for building
examples.  On disjoint sets of copies,
\[
Q_{n+m,\alpha}(C\otimes D)
=Q_{n,\alpha}(C)Q_{m,\alpha}(D),                                           \tag{23}
\]
which follows immediately by splitting every subset into its two parts in
(2).  Notice that
\(\operatorname{rank}(C\otimes D)=\operatorname{rank}C\,\operatorname{rank}D\);
therefore rank two permits at most one rank-two tensor factor.

## Exact endpoint equality family

Let \(x,y\in[d]^n\) be distinct product-basis strings, let
\[
D(x,y)=\{i:x_i\ne y_i\},\qquad k=|D(x,y)|,
\]
and take
\[
C=a|x\rangle\langle x|+b|y\rangle\langle y|.                               \tag{24}
\]
This has rank two when \(a,b\ne0\).  If \(D(x,y)\not\subseteq S\), the two
projectors remaining after tracing \(S\) are orthogonal, whereas if
\(D(x,y)\subseteq S\), they coincide.  Thus
\[
\|\operatorname{Tr}_S C\|_F^2
=\begin{cases}
|a|^2+|b|^2,&D(x,y)\not\subseteq S,\\
|a+b|^2,&D(x,y)\subseteq S.
\end{cases}                                                               \tag{25}
\]
Summing exactly,
\[
\boxed{\quad
Q_{n,\alpha}(C)
=(|a|^2+|b|^2)(1+\alpha)^n
+2\operatorname{Re}(a\overline b)\,
  \alpha^k(1+\alpha)^{n-k}.
\quad}                                                                    \tag{26}
\]
At the endpoint this becomes the square
\[
\boxed{\quad
Q_n(C)=2^{-n}|a+(-1)^k b|^2.
\quad}                                                                    \tag{27}
\]
Consequently there are nonzero rank-two equality vectors for every
\(n\): choose any two strings at Hamming distance \(k\ge1\) and take
\[
b=(-1)^{k+1}a.                                                             \tag{28}
\]
For \(-1/2\le\alpha<0\), formula (26) is nonnegative because
\(|\alpha|\le1+\alpha\) and
\(2|\operatorname{Re}(a\overline b)|\le|a|^2+|b|^2\).  Thus this exact
family also illustrates why \(\alpha=-1/2\) is the sharp boundary: the
two exponential terms have equal magnitude only there.

For reference, the one-copy inequality used above has a complete equality
description.  For rank-at-most-two \(D\),
\[
\|D\|_F^2-\frac12|\operatorname{Tr}D|^2\ge0.                               \tag{29}
\]
For nonzero \(D\), equality holds exactly when
\[
D=e^{i\theta}sP,                                                           \tag{30}
\]
where \(s>0\) and \(P\) is an orthogonal projection of rank two.  Indeed,
\[
|\operatorname{Tr}D|\le\|D\|_*\le\sqrt2\|D\|_F.
\]
Equality in the second inequality requires the two singular values to be
equal.  Equality in the first requires equality in every term of the trace
duality bound, so the polar factor of \(D\) is one common phase on its
two-dimensional support; this is precisely (30).  The converse is direct.

## 2026-07-28 08:59:35 PDT — Exact \(n=2\) reduction and proved subcases

For two copies, (3) is
\[
Q_2(C)=\|C\|_F^2-\frac12\left(
\|\operatorname{Tr}_1C\|_F^2+\|\operatorname{Tr}_2C\|_F^2\right)
+\frac14|\operatorname{Tr}C|^2.                                           \tag{31}
\]
Thus the desired two-copy statement is precisely
\[
\boxed{\quad
\|\operatorname{Tr}_1C\|_F^2+\|\operatorname{Tr}_2C\|_F^2
-\frac12|\operatorname{Tr}C|^2\le2\|C\|_F^2
\quad}                                                                    \tag{32}
\]
for \(\operatorname{rank}C\le2\).

If \(C=\sum_{k=1}^2|X_k\rangle\langle Y_k|\), where the matrices
\(X_1,X_2\in M_d\) are Frobenius-orthonormal (orthonormalize the left
factor in any rank factorization), then
\[
\|C\|_F^2=\sum_k\|Y_k\|_F^2,
\]
and, up to harmless transposes determined by vectorization convention,
\[
\operatorname{Tr}_1 C=\sum_kX_k^\dagger Y_k,\qquad
\operatorname{Tr}_2 C=\sum_kY_kX_k^\dagger,\qquad
\operatorname{Tr}C=\sum_k\langle X_k,Y_k\rangle_F.
\]
Therefore (32) is equivalent to the following frame inequality:
\[
\boxed{\quad
\left\|\sum_kX_k^\dagger Y_k\right\|_F^2
+\left\|\sum_kY_kX_k^\dagger\right\|_F^2
-\frac12\left|\sum_k\langle X_k,Y_k\rangle_F\right|^2
\le2\sum_k\|Y_k\|_F^2.
\quad}                                                                    \tag{33}
\]

For \(d=3\), Frobenius duality gives a particularly concrete equivalent
bottleneck.  It is enough, and is in fact equivalent, to prove that for
all traceless \(A,B\in M_3\) and all \(z\in\mathbb C\),
\[
\boxed{\quad
s_1(D)^2+s_2(D)^2
\le2\bigl(\|A\|_F^2+\|B\|_F^2+|z|^2\bigr),
\quad
D=I_3\otimes A+B\otimes I_3+\frac z{\sqrt6}I_9.
\quad}                                                                    \tag{34}
\]
Indeed, the left side is the squared operator norm of
\((A,B,z)\mapsto(DX_1,DX_2)\), maximized over orthonormal \(X_1,X_2\);
the adjoint sends \(Y_1,Y_2\) to
\[
\left(
\Pi_0\sum_kX_k^\dagger Y_k,
\Pi_0\sum_kY_kX_k^\dagger,
\frac1{\sqrt6}\sum_k\langle X_k,Y_k\rangle
\right),
\]
where \(\Pi_0(M)=M-\operatorname{Tr}(M)I_3/3\).  The squared norm of this
triple is exactly the left side of (33), because the two traceless
projections subtract \(2|\operatorname{Tr}C|^2/3\), while the scalar
coordinate restores \(|\operatorname{Tr}C|^2/6\), leaving
\(-|\operatorname{Tr}C|^2/2\).

The following subcases of (34) admit short exact proofs.

**Lemma 7 (one arbitrary nonnormal summand).**  If \(B=0\), then (34)
holds; likewise if \(A=0\).

*Proof.*  The singular values of \(I_3\otimes A+cI_9\), with
\(c=z/\sqrt6\), are those of \(A+cI_3\), each repeated three times.
It is therefore enough to prove
\[
\|A+cI_3\|_{\mathrm{op}}^2\le\|A\|_F^2+|z|^2.                              \tag{35}
\]
For unit \(x,y\), put \(r=|\langle y,x\rangle|\).  The functional
\(A\mapsto\langle y,Ax\rangle\), restricted to traceless matrices, has
Frobenius representing vector
\[
yx^\dagger-\frac{\operatorname{Tr}(yx^\dagger)}3I_3
\]
and hence squared norm \(1-r^2/3\).  Its scalar coefficient as a
functional of \(z\) has squared modulus \(r^2/6\).  Cauchy--Schwarz in
the parameter space \(M_3^0\oplus\mathbb C\) gives
\[
|\langle y,(A+cI)x\rangle|^2
\le\left(1-\frac{r^2}{3}+\frac{r^2}{6}\right)
   (\|A\|_F^2+|z|^2)
\le\|A\|_F^2+|z|^2.
\]
Taking the supremum over \(x,y\) proves (35), and the repeated singular
value proves (34). \(\square\)

**Lemma 8 (both summands normal).**  If \(A\) and \(B\) are normal, then
(34) holds.

*Proof.*  Independent unitary similarities on the two tensor factors
reduce \(A\) and \(B\) to diagonal matrices with diagonal vectors
\(a,b\in\mathbb C^3\) satisfying \(\sum_j a_j=\sum_i b_i=0\).  The nine
singular values of \(D\) are the moduli of
\[
\ell_{ij}(a,b,z)=a_j+b_i+\frac z{\sqrt6}.                                  \tag{36}
\]
In the parameter Hilbert space
\[
\{a:\sum a_j=0\}\oplus\{b:\sum b_i=0\}\oplus\mathbb C,
\]
the representing vector of each \(\ell_{ij}\) has squared norm
\[
\frac23+\frac23+\frac16=\frac32.                                          \tag{37}
\]
For two distinct grid positions \((i,j)\ne(i',j')\), the inner product of
the two representing vectors equals \(1/2\) if exactly one coordinate
agrees, and \(-1/2\) if neither agrees.  Hence the \(2\times2\) Gram
matrix of any two distinct evaluation functionals is
\[
\begin{pmatrix}3/2&\pm1/2\\ \pm1/2&3/2\end{pmatrix},
\]
whose largest eigenvalue is \(2\).  The sum of the squared moduli of any
two entries in (36) is consequently at most twice the squared parameter
norm.  Choosing the two largest proves (34). \(\square\)

**Lemma 9 (sharp nilpotent family at \(z=0\)).**  Let
\[
A=a|p\rangle\langle q|,\qquad
B=b|r\rangle\langle s|,
\qquad p\perp q,\quad r\perp s.
\]
Then equality holds in (34) with \(z=0\).

*Proof.*  Local unitaries reduce the matrices to
\(A=aE_{01}\), \(B=bE_{01}\).  Directly partitioning the product basis
shows that the squared singular values of
\[
I_3\otimes aE_{01}+bE_{01}\otimes I_3
\]
are
\[
|a|^2+|b|^2,\quad |a|^2+|b|^2,\quad |a|^2,\quad |b|^2,
\]
with the remaining five zero.  The top-two sum is
\(2(|a|^2+|b|^2)\). \(\square\)

For \(z=0\), (34) can be sharpened to one exact Cauchy--Schwarz target.
For Frobenius-orthonormal \(X_1,X_2\), define
\[
\begin{aligned}
\delta_A&=2\|A\|_F^2-\sum_{k=1}^2\|X_kA\|_F^2,\\
\delta_B&=2\|B\|_F^2-\sum_{k=1}^2\|BX_k\|_F^2,\\
\chi&=\sum_{k=1}^2\langle BX_k,X_kA\rangle_F .
\end{aligned}                                                             \tag{38}
\]
The quantities \(\delta_A,\delta_B\) are nonnegative because
\(\sum_kX_k^\dagger X_k\le2I\) and
\(\sum_kX_kX_k^\dagger\le2I\).  Allowing independent rescaling and a
relative phase of \(A,B\) shows that the \(z=0\) case is equivalent to
\[
\boxed{\qquad |\chi|^2\le\delta_A\delta_B
\quad\text{for traceless }A,B. \qquad}                                    \tag{39}
\]
Equality holds in (39) for the singular frame in Lemma 9.  A proof of
(39) for arbitrary nonnormal \(A,B\) remains the precise \(n=2\)
bottleneck in this note.

## Failed invariants and exact obstructions

1. **Individual subset caps cannot determine the sign.**  For \(d=3\),
   consider the formal joint spectral distribution of the two commuting
   projections \(P_1,P_2\) given by
   \[
   \mu_{\{1\}}=\mu_{\{2\}}=\frac12,\qquad
   \mu_\varnothing=\mu_{\{1,2\}}=0.
   \]
   It obeys all ordinary probability constraints and the sharp
   Schmidt-rank-two caps
   \[
   \langle P_i\rangle=\frac12\le\frac23,\qquad
   \langle P_1P_2\rangle=0\le\frac29.
   \]
   Nevertheless, since the eigenvalue of \(I-\frac32P_i\) on
   \(\operatorname{ran}P_i\) is \(-1/2\), this distribution gives formal
   expectation \(-1/2\).  Thus even the full classical joint distribution
   constraints plus all individual bounds (12) omit an essential
   low-matrix-rank compatibility condition.

2. **Rank is not preserved by contraction.**  Let
   \(u=d^{-1/2}\sum_{j=1}^d e_j\otimes f_j\), and set
   \(C=|u\rangle\langle u|\).  Then \(\operatorname{rank}C=1\), but
   \[
   \operatorname{Tr}_{\mathbb C^d}C=\frac1d I_d
   \]
   has rank \(d\).  Therefore an induction that applies an \(n\)-copy
   rank-two hypothesis directly to \(\operatorname{Tr}_i C\) is invalid.

3. **The wrong-diagonal Cauchy bridge is false exactly.**  For one local
   factor take
   \(u_1=v_1=e_1\), \(u_2=v_2=e_2\), with \(e_1\perp e_2\), and put
   \(R=I-F/2\).  Then
   \[
   \begin{aligned}
   \langle u_1\otimes v_1|R|u_1\otimes v_1\rangle
   &=\langle u_2\otimes v_2|R|u_2\otimes v_2\rangle=\frac12,\\
   \langle u_1\otimes v_2|R|u_1\otimes v_2\rangle
   &=\langle u_2\otimes v_1|R|u_2\otimes v_1\rangle=1.
   \end{aligned}
   \]
   Hence the tempting log-supermodular comparison of the two products
   would assert \(1\le1/4\).  Ordinary Cauchy--Schwarz (16) can therefore
   be exponentially looser than the crossed inequality actually needed.

4. **A tempting trace/nuclear-norm strengthening is false even at rank
   one.**  The inequality
   \[
   \|\operatorname{Tr}_1C\|_F^2+\|\operatorname{Tr}_2C\|_F^2
   \stackrel{?}{\le}\|C\|_*^2+\frac12|\operatorname{Tr}C|^2
   \]
   fails for
   \[
   C=|0,0\rangle\langle 0,+|,\qquad
   |+\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2}.
   \]
   The left side is \(1+1/2=3/2\), while the right side is
   \(1+(1/2)(1/2)=5/4\).  Thus a proof of (32) cannot come from this
   stronger-looking nuclear-norm estimate.

5. **Copywise factorization is the exact limit of the Schur-product
   proof.**  In Theorem 6 the \(2\times2\) Gram matrix factors entrywise.
   General singular vectors entangled across copies do not admit that
   factorization.  Replacing them by product approximations is not
   legitimate: the equality family (27) already lies on the boundary, so
   there is no uniform positive gap with which to absorb approximation
   error.

## Current status of this line

The all-\(n\) problem has been reduced exactly to (14).  The sharp
individual projection inequalities (12), the strict rank-one theorem
(8), the fully decomposable two-summand theorem (19), and the equality
family (27) are proved uniformly in \(n\).  For \(n=2,d=3\), the remaining
problem is exactly the nonnormal dual inequality (34), or, at \(z=0\), the
cross-defect inequality (39).  Lemmas 7--9 settle substantial boundary
classes but do not settle arbitrary simultaneous nonnormal \(A,B\), and
no all-copy conclusion follows from the present results.
