# The intersection-one frontier as a two-vector Schur inequality

## Status

This note gives a lossless reduction of the three-vector inequality
\[
 \left|{\cal B}_3(P_w,|u\rangle\langle v|)\right|^2
 \leq Q_3(P_w)Q_3(|u\rangle\langle v|)
 \tag{1}
\]
to one rank-one Schur complement depending only on \(w,u\).  It also
proves (1), in arbitrary local dimensions and for every copy number,
when the anchor \(w\) is fully product.

The general two-vector Schur inequality remains unproved.  Unrestricted
complex searches in local dimensions two, three, and four found no
violation of (1); this numerical observation is not used as evidence.

The independent exact checker is
`verification/verify_n3_three_vector_schur_reduction.py`.

## 1. The two complementary endpoint operators

Let
\[
 {\cal H}=H_1\otimes H_2\otimes H_3
\]
with arbitrary finite local dimensions.  Define
\[
 L_i(X)=X-\frac12\operatorname{Tr}(X)I_i,\qquad
 M_i(X)=\operatorname{Tr}(X)I_i-\frac12X,
 \tag{2}
\]
and put
\[
 {\cal L}=L_1\otimes L_2\otimes L_3,\qquad
 {\cal K}=M_1\otimes M_2\otimes M_3.
 \tag{3}
\]
For a vector \(x\in{\cal H}\), set
\[
 A_x={\cal L}(P_x),\qquad K_x={\cal K}(P_x).
 \tag{4}
\]
If \(\rho_S^x=\operatorname{Tr}_{\bar S}P_x\), with identities
inserted on the complementary factors, then
\[
 \boxed{
 K_x=
 I-\frac12\sum_i\rho_i^x\otimes I_{\bar i}
 +\frac14\sum_{i<j}\rho_{ij}^x\otimes I_{\overline{ij}}
 -\frac18P_x.}
 \tag{5}
\]
The complementary formula is
\[
 \boxed{
 A_x=
 P_x-\frac12\sum_i I_i\otimes\rho_{\bar i}^x
 +\frac14\sum_{i<j}I_{ij}\otimes\rho_{\overline{ij}}^x
 -\frac18I.}
 \tag{6}
\]

The crossed-swap contraction gives, for all \(u,v,w\),
\[
\begin{aligned}
 Q_3(|u\rangle\langle v|)
   &=\langle v,K_uv\rangle,\\
 {\cal B}_3(P_w,|u\rangle\langle v|)
   &=\langle v,A_wu\rangle,\\
 Q_3(P_w)&=\langle w,A_ww\rangle.
\end{aligned}
\tag{7}
\]

Moreover,
\[
 \boxed{\qquad K_u\succeq\frac18\|u\|^2I.\qquad}
\tag{8}
\]
Indeed, on two replicas,
\[
 Y=\bigotimes_{i=1}^3\left(I-\frac12F_i\right)\succeq\frac18I,
\tag{9}
\]
and \(K_u\), up to the harmless conjugation dictated by the
vectorization convention, is the compression of \(Y\) against \(u\)
on one replica.  Compressing (9) gives (8).

## 2. Lossless elimination of the third vector

Put
\[
 a=Q_3(P_w)>0,\qquad x=A_wu.
\tag{10}
\]
For fixed unit \(w,u\), equation (1) for every \(v\) is
\[
 |\langle v,x\rangle|^2\leq a\langle v,K_uv\rangle
 \qquad(v\in{\cal H}).
\tag{11}
\]
Consequently:

### Theorem 2.1 (two-vector Schur reduction)

For fixed unit \(w,u\), the following are equivalent:

1. (1) holds for every \(v\);
2.
   \[
    \boxed{\qquad aK_u-|A_wu\rangle\langle A_wu|\succeq0;\qquad}
    \tag{12}
   \]
3.
   \[
    \boxed{\qquad
    \langle A_wu,K_u^{-1}A_wu\rangle\leq a.
    \qquad}
    \tag{13}
   \]

#### Proof

The equivalence of (1) and (12) is exactly (7) and (11).  By (8),
\(K_u\) is invertible for nonzero \(u\).  Congruence of (12) by
\(K_u^{-1/2}\) gives
\[
 aI-|K_u^{-1/2}A_wu\rangle
       \langle K_u^{-1/2}A_wu|\succeq0.
\tag{14}
\]
A rank-one subtraction from \(aI\) is positive precisely when the
squared norm of the subtracted vector is at most \(a\), which is
(13).  This proves all equivalences. \(\square\)

Thus the whole intersection-one stratum is reduced from three
independent vectors to the two-vector inequality (13).  The crude
replacement \(K_u\succeq I/8\) would require
\(\|A_w\|_{\rm op}^2\leq a/8\), which is false for entangled anchors;
the state-dependent metric \(K_u^{-1}\) is essential.

The variational form
\[
 \langle x,K_u^{-1}x\rangle
 =
 \sup_y\left(2\operatorname{Re}\langle y,x\rangle
             -\langle y,K_uy\rangle\right)
\tag{15}
\]
is sometimes convenient: it displays (13) as one concave quadratic
optimization with no remaining rank constraint.

## 3. A sharp all-copy theorem for product anchors

The same reduction works for any copy number \(n\).  Write
\[
 {\cal L}_n=\bigotimes_{i=1}^nL_i,\qquad
 {\cal K}_n=\bigotimes_{i=1}^nM_i,
\tag{16}
\]
and define \(A_w,K_u\) as in (4).  The replica spectrum gives
\[
 K_u\succeq2^{-n}\|u\|^2I.
\tag{17}
\]

### Theorem 3.1 (product-anchor inequality)

Let
\[
 w=w_1\otimes\cdots\otimes w_n
\]
be a unit product vector, in arbitrary finite local dimensions.  Then
for every \(u,v\),
\[
 \boxed{
 \left|{\cal B}_n(P_w,|u\rangle\langle v|)\right|^2
 \leq Q_n(P_w)Q_n(|u\rangle\langle v|).}
\tag{18}
\]
The constant is sharp.

#### Proof

For each site,
\[
 L_i(P_{w_i})=P_{w_i}-\frac12I_i
             =\frac12U_i,
\qquad U_i=2P_{w_i}-I_i,
\tag{19}
\]
and \(U_i\) is a self-adjoint unitary.  Therefore
\[
 A_w=2^{-n}U,\qquad
 U=\bigotimes_iU_i,\qquad
 Q_n(P_w)=2^{-n}.
\tag{20}
\]
For unit \(u\), (17) implies \(K_u^{-1}\preceq2^nI\), and hence
\[
\begin{aligned}
 \langle A_wu,K_u^{-1}A_wu\rangle
 &\leq2^n\|A_wu\|^2\\
 &=2^n\,2^{-2n}\|Uu\|^2
 =2^{-n}
 =Q_n(P_w).
\end{aligned}
\tag{21}
\]
The \(n\)-copy version of Theorem 2.1 now proves (18).

For sharpness, choose a product \(u=v\) whose local factors are each
either \(w_i\) or orthogonal to \(w_i\).  Then \(Uu=\pm u\),
\(Q_n(P_u)=2^{-n}\), and
\[
 |\langle u,A_wu\rangle|^2=2^{-2n}
 =Q_n(P_w)Q_n(P_u).
\tag{22}
\]
\(\square\)

## 4. The smallest remaining inequality

There is a second exact boundary theorem which follows from the Schur
form and is stronger than requiring the third vector \(v\) to have
qubit support.

### Theorem 4.1 (one-sided common-qubit compression)

Suppose that for every site \(i\) there is a subspace
\(E_i\subseteq H_i\), of dimension at most two, such that
\[
 w,u\in E:=E_1\otimes\cdots\otimes E_n.
\tag{23}
\]
Then (18) holds for every \(v\in{\cal H}\), without any support
restriction on \(v\).

#### Proof

Pad one-dimensional \(E_i\)'s to dimension two when necessary and
let \(P_E\) be the projection onto \(E\).  Every reduced density
operator of \(w\) or \(u\) is supported on the corresponding tensor
product of the \(E_i\)'s.  Formulas (5)--(6), and their \(n\)-copy
versions, therefore show that \(A_w\) and \(K_u\) commute with \(P_E\).
Moreover their compressions are exactly the operators obtained by
regarding \(w,u\) as \(n\)-qubit vectors:
\[
 P_EA_wP_E=A_w^{(E)},\qquad
 P_EK_uP_E=K_u^{(E)}.
\tag{24}
\]
Indeed, compression of an identity \(I_{H_i}\) gives \(I_{E_i}\),
while all reduced operators and their traces are unchanged.

Since \(u\in E\), one has \(A_wu\in E\).  Block diagonality gives
\[
 \langle A_wu,K_u^{-1}A_wu\rangle
 =
 \langle A_w^{(E)}u,(K_u^{(E)})^{-1}A_w^{(E)}u\rangle.
\tag{25}
\]
On qubits the anchored map has the exact completely positive
certificate
\[
 a{\cal K}_n^{(E)}(V)-A_w^{(E)}VA_w^{(E)}\succeq0
 \qquad(V\succeq0).
\tag{26}
\]
For completeness, its Choi matrix is
\[
 a\Pi-|\operatorname{vec}A_w^{(E)}\rangle
       \langle\operatorname{vec}A_w^{(E)}|,
\qquad
 \Pi=\left(I-\frac12|\Phi_2\rangle\langle\Phi_2|\right)^{\otimes n}.
\tag{27}
\]
Here \(\Pi\) is an orthogonal projection,
\(\operatorname{vec}A_w^{(E)}\in\operatorname{ran}\Pi\), and its
squared norm is \(a\); hence (27) is positive.  Taking \(V=P_u\), or
equivalently applying the Schur complement, proves that (25) is at
most \(a\).  Theorem 2.1 then proves (18) for arbitrary \(v\).
\(\square\)

Thus a counterexample to the three-vector inequality cannot be
generated by a pair \(w,u\) which fits into common local qubit
supports, even if the optimizing third vector uses the full ambient
local dimensions.

For three copies, the exact two-copy theorem improves "every site" to
"one site."

### Theorem 4.2 (one-site Schur boundary)

Assume the established two-copy endpoint theorem
\[
 Q_2(C)\geq0\qquad(\operatorname{rank}C\leq2).
\tag{28}
\]
If, for some site \(i\), the union of the local supports of \(w\) and
\(u\) has dimension at most two, then the three-copy Schur inequality
(13) holds.  Consequently (1) holds for every \(v\).

#### Proof

Let \(E_i\) contain both local supports and put
\(P=P_{E_i}\otimes I_{\bar i}\).  Formulas (5)--(6) show
\[
 [K_u,P]=[A_w,P]=0,\qquad Pu=u,\qquad PA_wu=A_wu.
\tag{29}
\]
Thus the vector which maximizes the quotient in (11),
\[
 v_*=K_u^{-1}A_wu,
\tag{30}
\]
also obeys \(Pv_*=v_*\).

If (13) failed, the \(2\times2\) scalar Gram matrix of
\(P_w\) and \(|u\rangle\langle v_*|\) would have a negative
eigenvalue.  Hence some
\[
 C=\gamma P_w+\delta|u\rangle\langle v_*|
\tag{31}
\]
would satisfy \(Q_3(C)<0\).  This \(C\) has rank at most two.  At site
\(i\), both its row support (generated by \(w,u\)) and its column
support (generated by \(w,v_*\)) lie in \(E_i\).

Compress the local endpoint form to \(E_i\).  In vectorized local
matrix space it is
\[
 I_4-\frac12
 (|00\rangle+|11\rangle)(\langle00|+\langle11|),
\tag{32}
\]
with a harmless one-dimensional deletion when \(\dim E_i=1\).  It has
the separable decomposition
\[
\begin{aligned}
 {}&\frac12\sum_{\theta\in\{0,\pi/2,\pi,3\pi/2\}}
 |p_\theta\rangle\langle p_\theta|
 +\frac12|01\rangle\langle01|
 +\frac12|10\rangle\langle10|,\\
 &p_\theta=\frac12
 (|0\rangle+e^{i\theta}|1\rangle)
 \otimes(|0\rangle-e^{-i\theta}|1\rangle).
\end{aligned}
\tag{33}
\]
Contracting \(C\) at site \(i\) against each product vector in (33)
produces a two-copy coefficient matrix of rank at most two.  Therefore
\[
 Q_3(C)=\sum_\mu\lambda_\mu Q_2(C_\mu)\geq0
\tag{34}
\]
by (28), contradicting (31).  Hence (13) holds.
\(\square\)

In particular, a violating pair \(w,u\) must have genuinely
three-dimensional combined local support at **every** one of the
three physical sites.  This statement concerns only the two vectors
remaining after the lossless Schur elimination; no condition on an
independently chosen \(v\) is needed.

## 5. The smallest remaining inequality

The unresolved intersection-one theorem is now exactly
\[
 \boxed{
 \left\|K_u^{-1/2}A_wu\right\|^2
 \leq\langle w,A_ww\rangle
 \qquad\text{for every unit }w,u.}
\tag{35}
\]
It is important that the same \(u\) occurs both in the vector
\(A_wu\) and in the nonlinear positive metric \(K_u\).  Separating
these two occurrences recovers the already disproved operator-norm
relaxation.
