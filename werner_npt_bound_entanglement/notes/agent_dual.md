# Dual-cone, symmetry, and induction notebook

Scope: independent first-principles attack on two-block positivity of
\[
X_d^{\otimes n},\qquad X_d=I-\frac d2P_d
=I-\frac12|\Phi_d\rangle\langle\Phi_d|,
\quad |\Phi_d\rangle=\sum_{j=0}^{d-1}|jj\rangle .
\]
No external sources or prior research artifacts are used.

## Research log

- **2026-07-28 08:02 PDT.** Began the dual-cone/induction approach. The first
  target is an exact coefficient-matrix contraction formula, followed by a
  search for a cone invariant stable under adding one tensor factor.
- **2026-07-28 08:34 PDT.** Derived the crossed-Gram formulation below. Every
  subset contribution is a positive semidefinite \(2\times2\) Gram matrix, but
  the endpoint functional is their alternating sum. This isolates the missing
  ingredient as a compatibility inequality among partial-contraction Gram
  matrices.
- **2026-07-28 08:56 PDT.** Found a general one-sided product-code
  tensorization theorem: tensor products of \(k\)-block-positive operators
  remain nonnegative on \(k\)-term vectors when the codewords on one side
  factor across copies; the other side may be arbitrarily entangled. Also
  found an exact obstruction to the obvious complete-induction upgrade:
  after peeling a site the boundary dimension can exceed two, and the
  one-site crossed kernel is already indefinite for three product terms.
- **2026-07-28 08:58 PDT.** Proved an exterior-square amplification lemma:
  any negative rank-two witness at \(n\) copies produces, at \(2n\) copies,
  a negative witness with two equal Schmidt coefficients. Thus equal Schmidt
  coefficients are rigorous without loss for the all-copy existence
  question, although not necessarily at a fixed copy number.
- **2026-07-28 09:31 PDT.** Completed a phase/conjugation audit of the
  exterior-square lemma and found a second, adjoint-mixed determinant
  construction. It remains negative and has equal singular values. A
  right-copy swap makes it skew-Hermitian (hence normal) of rank two, but
  that swap changes standard tensor pairing to crossed tensor pairing.
  An exact one-copy block-positive example shows that this operation can
  reverse the sign. I also derived an exact rank-two positive dilation
  formula that records the additional invariants needed to overcome this
  obstruction.
- **2026-07-28 09:39 PDT.** Ran independent exact checks of the stable-rank
  counterexample, the adjoint-mixed sign reversal, and the positive
  flag-dilation formula. Consolidated the proved reductions and their
  limitations. No all-copy conclusion follows from the present cone.

## 1. Coefficient-matrix formula

Fix the vectorization convention
\[
\operatorname{vec}(C)=\sum_{a,b}C_{ab}|a\rangle_A|b\rangle_B .
\]
For \(S\subseteq[n]\), let \(\operatorname{Tr}_S C\) denote the ordinary
operator partial trace over the tensor factors indexed by \(S\). Then
\[
\boxed{\quad
 Q_n(C):=\langle\operatorname{vec}(C)|X_d^{\otimes n}|
 \operatorname{vec}(C)\rangle
 =\sum_{S\subseteq[n]}\left(-\frac12\right)^{|S|}
 \|\operatorname{Tr}_S C\|_2^2 .
\quad} \tag{1}
\]

### Proof

Write \(q_d=|\Phi_d\rangle\langle\Phi_d|\), where
\(|\Phi_d\rangle=\sum_j|jj\rangle\), so that \(X_d=I-q_d/2\).
Contracting \(\operatorname{vec}(C)\) against
\(\langle\Phi_d|\) on exactly the pairs in \(S\) gives
\(\operatorname{vec}(\operatorname{Tr}_S C)\). Hence
\[
\langle\operatorname{vec}(C)|
\bigotimes_{i\in S}q_d^{(i)}
|\operatorname{vec}(C)\rangle
=\|\operatorname{Tr}_S C\|_2^2 .
\]
Expansion of the tensor product proves (1).

Equivalently, for the self-adjoint superoperator
\[
\mathcal L_d(A)=A-\frac12\operatorname{Tr}(A)I_d,
\]
one has
\[
Q_n(C)=\langle C,\mathcal L_d^{\otimes n}(C)\rangle_{\rm HS}.
\]
The local scalar direction has eigenvalue \(1-d/2\), while every traceless
direction has eigenvalue \(1\). Thus positivity cannot follow from positivity
of the superoperator.

## 2. Crossed \(2\times2\) compression

Put
\[
Y_d=I-\frac12F,\qquad X_d=Y_d^\Gamma.
\]
The eigenvalues of \(Y_d\) are \(1/2\) and \(3/2\), so
\[
Y_d^{\otimes n}\succeq 2^{-n}I. \tag{2}
\]

Let a rank-at-most-two coefficient matrix have singular-value decomposition
\[
C=s_1|u_1\rangle\langle v_1|
  +s_2|u_2\rangle\langle v_2|,
\]
where each displayed family is orthonormal and \(s_1,s_2\ge0\). Define
\[
H_{rs}
=\langle u_r\otimes v_s|Y_d^{\otimes n}|
u_s\otimes v_r\rangle,\qquad r,s\in\{1,2\}. \tag{3}
\]
The partial-transpose matrix-element identity
\[
\langle a\otimes\overline b|Y^\Gamma|
c\otimes\overline e\rangle
=\langle a\otimes e|Y|c\otimes b\rangle
\]
gives
\[
\boxed{\quad Q_n(C)=\sum_{r,s=1}^2s_rs_sH_{rs}.\quad} \tag{4}
\]
The matrix \(H\) is Hermitian. Consequently, the endpoint problem is exactly
the assertion that \(H\succeq0\) for every pair of isometries
\(U=(u_1,u_2)\), \(V=(v_1,v_2)\).

Equation (2) immediately gives the useful diagonal estimate
\[
H_{rr}\ge 2^{-n}. \tag{5}
\]
This proves the stronger rank-one inequality
\[
Q_n(C)\ge2^{-n}\|C\|_2^2\qquad(\operatorname{rank}C=1). \tag{6}
\]

## 3. Every subset matrix is a positive Gram matrix

For \(S\subseteq[n]\), flatten \(u_r\) and \(v_r\) across
\(\mathcal H_S:\mathcal H_{S^c}\), writing the resulting matrices as
\(A_{r,S}\) and \(B_{r,S}\), with rows indexed by \(S\). Set
\[
M_{r,S}=A_{r,S}^\dagger B_{r,S}.
\]
The partial-swap identity gives
\[
\begin{aligned}
G^S_{rs}
&:=\langle u_r\otimes v_s|F_S|u_s\otimes v_r\rangle\\
&=\operatorname{Tr}\!\left(
 A_{s,S}A_{r,S}^\dagger B_{r,S}B_{s,S}^\dagger
\right)
=\operatorname{Tr}(M_{r,S}M_{s,S}^\dagger).
\end{aligned} \tag{7}
\]
Thus
\[
\boxed{\quad G^S\succeq0,\qquad
H=\sum_{S\subseteq[n]}\left(-\frac12\right)^{|S|}G^S.\quad} \tag{8}
\]
Orthogonality of both codeword families gives \(G^\varnothing=I_2\).

This is a useful exact reduction, but positivity of the individual \(G^S\)
does not control their alternating sum. Their compatibility as reductions of
the same two isometries is essential.

## 3.1 Exterior-square amplification: equal coefficients without loss

### Lemma 3.1

Let \(W\) be any block-positive Hermitian operator. If \(W\) has negative
expectation on a Schmidt-rank-at-most-two vector, then \(W\otimes W\) has
negative expectation on a Schmidt-rank-two vector whose two nonzero Schmidt
coefficients are equal.

### Proof

Write the coefficient matrix of a negative vector in singular form
\[
C=s_1C_1+s_2C_2,\qquad
C_r=|u_r\rangle\langle v_r|,
\]
with both displayed vector families orthonormal. Define the Hermitian
\(2\times2\) compression
\[
H_{rs}=\langle\operatorname{vec}(C_r)|W|
\operatorname{vec}(C_s)\rangle. \tag{E1}
\]
With the vectorization convention of Section 1,
\(\operatorname{vec}(C_r)=u_r\otimes\overline{v_r}\). Thus these are
product vectors across the physical bipartition, and block positivity
really does imply \(H_{rr}\ge0\). Hermiticity gives
\(H_{21}=\overline{H_{12}}\), with no reality assumption on \(H_{12}\).
Block positivity gives \(H_{11},H_{22}\ge0\). The assumed negative
combination says that \(H\) is not positive semidefinite. Since
\(\operatorname{Tr}H\ge0\), this forces
\[
\det H=H_{11}H_{22}-|H_{12}|^2<0. \tag{E2}
\]

On the doubled system set
\[
D=C_1\otimes C_2-C_2\otimes C_1. \tag{E3}
\]
Its left vectors \(u_1\otimes u_2,u_2\otimes u_1\) are orthonormal, as are
its right vectors \(v_1\otimes v_2,v_2\otimes v_1\). Hence \(D\) has exactly
two nonzero singular values, both equal to \(1\). Moreover
\(\operatorname{vec}(D)\) is antisymmetric under interchange of the two
whole \(W\)-replicas. After the canonical regrouping
\((A_1B_1)(A_2B_2)\cong(A_1A_2)(B_1B_2)\), tensor matrix elements factor.
In particular,
\[
\begin{aligned}
\langle C_1\otimes C_2|W\otimes W|C_2\otimes C_1\rangle
 &=H_{12}H_{21},\\
\langle C_2\otimes C_1|W\otimes W|C_1\otimes C_2\rangle
 &=H_{21}H_{12}.
\end{aligned}
\]
Here and below a coefficient matrix between bra-kets denotes its
vectorization. Therefore direct expansion gives
\[
\begin{aligned}
\langle\operatorname{vec}(D)|W\otimes W|
\operatorname{vec}(D)\rangle
&=2H_{11}H_{22}-2H_{12}H_{21}\\
&=2\det H<0.
\end{aligned} \tag{E4}
\]
This proves the lemma.

### Corollary 3.2

For every physical Werner parameter \(-1\le\alpha\le1\),
\[
X_{\alpha,d}^{\otimes n}
=\left((I+\alpha F)^{\otimes n}\right)^\Gamma
\]
is block-positive, because \(I+\alpha F\succeq0\). Apply Lemma 3.1 with
\(W=X_{\alpha,d}^{\otimes n}\). Therefore:

> There is a negative finite-copy Schmidt-rank-two Werner witness if and
> only if there is one, possibly at twice as many copies, with equal Schmidt
> coefficients.

In particular, proving nonnegativity for all equal-Schmidt-coefficient
rank-two vectors at every copy number is sufficient for an all-copy theorem.
This is a global reduction across copy number, not a claim that every
fixed-\(n\) minimizer has equal coefficients.

## 3.2 Adjoint-mixed determinant and the normality obstruction

The preceding determinant has a useful adjoint-mixed variant. It comes
within one copy swap of producing a normal negative witness, but the copy
swap does not preserve the tensor pairing.

Let
\[
W=X_d^{\otimes n},\qquad
\mathfrak B(A,B)=
\langle\operatorname{vec}(A)|W|\operatorname{vec}(B)\rangle.
\]
The coefficient-map formula (1) implies
\[
\mathfrak B(A^\dagger,B^\dagger)
=\mathfrak B(B,A)
=\overline{\mathfrak B(A,B)}. \tag{E5}
\]
For completeness, write
\(\mathfrak B(A,B)=\operatorname{Tr}(A^\dagger\mathcal
L_d^{\otimes n}(B))\). The map \(\mathcal L_d^{\otimes n}\) is
self-adjoint for the Hilbert--Schmidt inner product and preserves
adjoints. Cyclicity of trace then proves (E5).

Suppose now that an equal-coefficient partial isometry
\[
C=C_1+C_2,\qquad C_r=|u_r\rangle\langle v_r|,
\]
has negative expectation. Put
\[
a=\mathfrak B(C_1,C_1),\quad
b=\mathfrak B(C_2,C_2),\quad
h=\mathfrak B(C_1,C_2).
\]
Block positivity gives \(a,b\ge0\), while
\[
a+b+2\operatorname{Re}h<0. \tag{E6}
\]
Multiplying \(C_2\) by a scalar phase preserves its singular value and all
orthogonality relations. Choose that phase so that the new mixed entry is
\(h=-r\), \(r=|h|\). Equation (E6) then remains negative and gives
\[
r>\frac{a+b}{2}\ge\sqrt{ab}. \tag{E7}
\]

On two \(W\)-replicas define
\[
D_\times=C_1\otimes C_2^\dagger-C_2\otimes C_1^\dagger. \tag{E8}
\]
The left vectors of its two terms are
\[
u_1\otimes v_2,\quad u_2\otimes v_1,
\]
and the right vectors are
\[
v_1\otimes u_2,\quad v_2\otimes u_1.
\]
Both pairs are orthonormal, so \(D_\times\) again has exactly two equal
nonzero singular values. By (E5),
\[
\begin{aligned}
\mathfrak B^{\otimes2}(C_1\otimes C_2^\dagger,
                      C_1\otimes C_2^\dagger)&=ab,\\
\mathfrak B^{\otimes2}(C_1\otimes C_2^\dagger,
                      C_2\otimes C_1^\dagger)&=h^2=r^2.
\end{aligned}
\]
Consequently,
\[
\boxed{\quad
\mathfrak B^{\otimes2}(D_\times,D_\times)
=2(ab-r^2)<0.
\quad} \tag{E9}
\]
Thus an equal negative witness produces a second equal negative partial
isometry, now built symmetrically from \(C_r\) and \(C_r^\dagger\).

Let \(S\) swap the two whole \(n\)-copy factors in coefficient space, and
put
\[
z_1=u_1\otimes v_2,\qquad z_2=u_2\otimes v_1.
\]
Right multiplication by \(S\) gives
\[
N=D_\times S
=|z_1\rangle\langle z_2|-|z_2\rangle\langle z_1|. \tag{E10}
\]
Hence \(N^\dagger=-N\): it is a normal rank-two matrix with equal singular
values. This is the desired algebraic normal form, but its expectation is
not (E9). Since \(S\) is real and symmetric,
\[
\operatorname{vec}(D_\times S)
=(I_A\otimes S_B)\operatorname{vec}(D_\times),
\]
and therefore
\[
\mathfrak B^{\otimes2}(N,N)
=\langle D_\times|
S_B(W\otimes W)S_B|D_\times\rangle. \tag{E11}
\]
The conjugated operator pairs \(A_1\) with \(B_2\) and \(A_2\) with
\(B_1\). It is the crossed-pairing operator, not the standard
\(W_{A_1B_1}\otimes W_{A_2B_2}\). Relabeling the \(B\)-replicas restores
the standard operator but simultaneously changes \(N\) back to
\(D_\times\).

This sign loss is real, not merely a missing invariance argument. Take one
block
\[
W=I-|\Phi_d\rangle\langle\Phi_d|,\qquad d\ge2,
\]
which is block-positive because
\(|\operatorname{Tr}A|^2\le\|A\|_2^2\) for rank-one \(A\). With
\[
C_1=|0\rangle\langle0|,\qquad C_2=|1\rangle\langle1|,
\]
one has \(a=b=0,h=-1\), and hence
\[
\langle D_\times|W^{\otimes2}|D_\times\rangle=-2.
\]
But
\[
N=|01\rangle\langle10|-|10\rangle\langle01|.
\]
Both one-factor partial traces of \(N\), as well as its full trace, vanish.
The analogue of (1) with coefficient \(-1\) therefore gives
\[
\langle N|W^{\otimes2}|N\rangle=\|N\|_2^2=2. \tag{E12}
\]
Thus the normalizing right swap can reverse the sign exactly.
The deterministic exact check is
`discovery/agent_dual_adjoint_check.py`.

There are two nearby constructions worth recording.

First, for any rank-one tensor word \(A\), every matrix
\[
A+e^{i\theta}A^\dagger
\]
is phase-Hermitian, hence normal, and has rank at most two. Taking
\(A=C_1\otimes C_2^\dagger\) gives
\[
\mathfrak B^{\otimes2}(A+e^{i\theta}A^\dagger,
                       A+e^{i\theta}A^\dagger)
=2ab+2\operatorname{Re}\!\left(
e^{i\theta}
\mathfrak B(C_1,C_1^\dagger)
\mathfrak B(C_2^\dagger,C_2)\right). \tag{E13}
\]
The entries in the second term are not determined by \(a,b,h\). In the
class of two-term tensor-word constructions, this is the basic dilemma:
an adjoint pair gives normality but samples local adjoint-paired entries;
the determinant entry \(h^2\) is obtained only after permuting the
adjoint word, which produces the crossed pairing in (E11).

There is a universal but insufficient rank-four conclusion behind this
observation. For every coefficient matrix \(C\),
\[
Q_n(C+C^\dagger)+Q_n(C-C^\dagger)
=2Q_n(C)+2Q_n(C^\dagger)=4Q_n(C). \tag{E13a}
\]
Thus a negative rank-two \(C\) always yields either a negative Hermitian
matrix \(C+C^\dagger\) or a negative skew-Hermitian matrix
\(C-C^\dagger\). Both are normal, but their rank can be four. More
generally, \(C+e^{i\theta}C^\dagger\) is phase-Hermitian for every
\(\theta\), yet if the initial and final two-planes of a partial isometry
\(C\) are orthogonal then its restriction to their direct sum has an
invertible off-diagonal \(2+2\) block form, so its rank is four for every
phase.
Hence adjoint symmetrization solves normality exactly at the cost of
doubling the forbidden Schmidt rank.

Second, there is a canonical rank-two positive dilation. Let \(D\) be any
rank-two partial isometry with
\[
P_R=D^\dagger D,\qquad P_L=DD^\dagger,
\]
and add one \(d\)-dimensional flag copy, using only flag levels \(0,1\).
For \(p,q\ge0\), the block coefficient matrix
\[
E_{p,q}=
\begin{pmatrix}
pP_R&\sqrt{pq}\,D^\dagger\\
\sqrt{pq}\,D&qP_L
\end{pmatrix} \tag{E14}
\]
is positive semidefinite of rank two: if \(D r_i=l_i\), it is the sum of
the two projectors onto
\(\sqrt p\,|0\rangle r_i+\sqrt q\,|1\rangle l_i\).
Set
\[
A_R=Q_n(P_R),\quad A_L=Q_n(P_L),\quad
c=\mathfrak B(P_R,P_L),\quad q_D=Q_n(D).
\]
Applying the exact block recursion from Section 5 below gives
\[
\boxed{\quad
Q_{n+1}(E_{p,q})
=\frac{p^2}{2}A_R+\frac{q^2}{2}A_L
+2pq\,q_D-pq\,\operatorname{Re}c.
\quad} \tag{E15}
\]
The negative term \(q_D\) is now present in a phase-positive, normal
rank-two candidate, but its sign is not controlled without new inequalities
on the two support projections and their mixed matrix element. Formula
(E15) isolates precisely the extra information a successful positive
dilation argument would need.
The deterministic exact check is
`discovery/agent_dual_flag_check.py`.

## 4. A genuine tensor-stable cone: one-sided product codewords

### Theorem 4.1

Let \(k\ge1\), and let \(W_i\) be a \(k\)-block-positive Hermitian operator
on \(\mathcal A_i\otimes\mathcal B_i\), for \(i=1,\ldots,n\). Suppose a
vector has the form
\[
|\psi\rangle
=\sum_{r=1}^k c_r|u_r\rangle_{A_1\cdots A_n}
       \bigotimes_{i=1}^n|b_{ri}\rangle_{B_i}.
\tag{9}
\]
The \(A\)-side vectors \(u_r\) may be arbitrarily entangled across
copies, and no orthogonality or normalization assumptions are needed. Then
\[
\langle\psi|\bigotimes_{i=1}^nW_i|\psi\rangle\ge0. \tag{10}
\]
The same conclusion holds with the roles of \(A\) and \(B\) reversed.
In particular, for \(k=2\), one may take every
\(W_i=X_{\alpha,d}\), for any \(\alpha\ge-1/2\).

### Proof

For each site define a \(k\times k\) operator-block matrix
\(\mathcal K_i\) on \(\mathbb C^k\otimes\mathcal A_i\) by
\[
(\mathcal K_i)_{rs}
=(I\otimes\langle b_{ri}|)W_i
 (I\otimes|b_{si}\rangle). \tag{11}
\]
For arbitrary \(w_1,\ldots,w_k\in\mathcal A_i\),
\[
\left\langle\sum_{r=1}^k|r\rangle w_r
\middle|\mathcal K_i\middle|
\sum_{r=1}^k|r\rangle w_r\right\rangle
=\left\langle
\sum_{r=1}^kw_r\otimes b_{ri}
\middle|W_i\middle|
\sum_{r=1}^kw_r\otimes b_{ri}
\right\rangle\ge0. \tag{12}
\]
Indeed the vector in (12) has Schmidt rank at most \(k\), so every
\(\mathcal K_i\succeq0\).

Let
\[
J:\mathbb C^k\longrightarrow(\mathbb C^k)^{\otimes n},
\qquad J|r\rangle=|r\rangle^{\otimes n},
\]
and, after regrouping all \(A\)-systems, define
\[
\mathcal K
=(J^\dagger\otimes I)\left(\bigotimes_{i=1}^n\mathcal K_i\right)
 (J\otimes I). \tag{13}
\]
This is a compression of a positive operator, so \(\mathcal K\succeq0\);
its \((r,s)\) operator block is
\[
\mathcal K_{rs}=\bigotimes_{i=1}^n(\mathcal K_i)_{rs}.
\]
For
\[
|\zeta\rangle=\sum_{r=1}^kc_r|r\rangle|u_r\rangle
\]
one now has, by direct tensor contraction,
\[
\langle\psi|\bigotimes_iW_i|\psi\rangle
=\langle\zeta|\mathcal K|\zeta\rangle\ge0.
\]
This proves (10). Interchanging the two sides proves the reversed statement.

For the Werner application, one-copy two-block positivity follows from
\[
\|C\|_2^2+\alpha|\operatorname{Tr}C|^2
\ge\min\{1,1+2\alpha\}\|C\|_2^2\ge0
\quad(\operatorname{rank}C\le2), \tag{14}
\]
because
\[
|\operatorname{Tr}C|\le\|C\|_1
\le\sqrt2\,\|C\|_2.
\]

Thus throughout the entire unresolved interval, any distillation witness
must use genuine intraparty entanglement across copies on **both** sides:
neither pair of side-codewords may consist entirely of product vectors.

### Corollary 4.2: a tensor-rank obstruction at general \(\alpha\)

Let \(\alpha<0\), and let \(m\le d\) satisfy
\(\alpha\ge-1/m\). If a vector admits an expansion
\[
|\psi\rangle
=\sum_{r=1}^m |u_r\rangle_{A_1\cdots A_n}
 \bigotimes_{i=1}^n|b_{ri}\rangle_{B_i}. \tag{15a}
\]
then
\[
\langle\psi|X_{\alpha,d}^{\otimes n}|\psi\rangle\ge0.
\]
Indeed, for every coefficient matrix of rank at most \(m\),
\[
\|C\|_2^2+\alpha|\operatorname{Tr}C|^2
\ge(1+m\alpha)\|C\|_2^2\ge0,
\]
so \(X_{\alpha,d}\) is \(m\)-block-positive and Theorem 4.1 applies.
The threshold is exact at one copy: if \(m\le d\), the rank-\(m\)
projection \(P_m\) has expectation \(m+\alpha m^2\).

For a Schmidt-rank-two vector, (15a) applies whenever the two codewords on
one side, taken together, have an expansion using at most \(m\) fully product
terms. Hence a witness at parameter \(\alpha\) must have one-sided product
tensor rank greater than every \(m\) with \(\alpha\ge-1/m\), on both sides.
At the endpoint \(\alpha=-1/2\), this reduces to the two-product-term
obstruction in Theorem 4.1.

### Corollary 4.3: tensor-factorized coefficient matrices

If \(C=C_1\otimes\cdots\otimes C_n\) and
\(\operatorname{rank}C\le2\), then
\[
Q_n(C)\ge2^{-n}(s_1(C)-s_2(C))^2\ge0. \tag{15b}
\]

To prove this, note that ranks multiply, so at most one factor has rank two
and all others have rank one. Formula (1) factorizes:
\[
Q_n(C)=\prod_iQ_1(C_i).
\]
For a rank-one factor,
\[
Q_1(C_i)\ge\frac12\|C_i\|_2^2,
\]
and for a rank-two factor with singular values \(t_1,t_2\),
\[
Q_1(C_i)\ge\frac12(t_1-t_2)^2.
\]
Multiplication gives (15b).

## 5. Why the obvious bond-two induction does not close

Write \(C\) as a \(d\times d\) block matrix \(C=(C_{ij})\) with respect to
the last tensor factor. Formula (1) gives the exact recursion
\[
Q_n(C)=\sum_{i,j=1}^d Q_{n-1}(C_{ij})
-\frac12Q_{n-1}\!\left(\sum_{i=1}^dC_{ii}\right). \tag{16}
\]
If \(\operatorname{rank}C\le2\), then every block \(C_{ij}\) has rank at most
two, but the diagonal contraction \(\sum_iC_{ii}\) can have rank as large as
\(2d\). Thus rank-two positivity at level \(n-1\) supplies no sign for the
second term in (16).

The corresponding crossed-kernel obstruction is already exact at one site.
For \(m\) product terms define
\[
\mathsf K_{rs}
=\langle a_r\otimes b_r|X_d|a_s\otimes b_s\rangle .
\tag{17}
\]
This matrix is positive for \(m\le2\), which is precisely one-copy
two-block positivity. It is not positive for \(m=3\): take
\[
a_r=b_r=e_r,\qquad r=1,2,3.
\]
Then
\[
\mathsf K=I_3-\frac12J_3, \tag{18}
\]
whose all-ones eigenvector has eigenvalue \(-1/2\).

When an arbitrary two-dimensional code is peeled across one physical site,
its remaining boundary labels are pairs \((r,i)\), so the boundary size
grows from \(2\) to as much as \(2d\). Any induction that upgrades the
\(2\times2\) crossed kernel to complete positivity on that enlarged boundary
therefore asks for the false assertion contradicted by (18). A viable
induction must retain additional Gram/isometry constraints rather than only
positivity of the boundary matrix.

The rank growth asserted above is attainable. Suppose the untraced space has
dimension at least \(2d\), choose orthonormal vectors \(e_1,\ldots,e_{2d}\)
there, and set
\[
u_1=d^{-1/2}\sum_{i=1}^d |i\rangle|e_i\rangle,\qquad
u_2=d^{-1/2}\sum_{i=1}^d |i\rangle|e_{d+i}\rangle .
\]
For the rank-two positive matrix
\[
C=|u_1\rangle\langle u_1|+|u_2\rangle\langle u_2|,
\]
tracing the first factor gives
\[
\operatorname{Tr}_1C
=d^{-1}\sum_{i=1}^{2d}|e_i\rangle\langle e_i|,
\]
which has rank \(2d\).

## 6. CP/co-CP splitting and its obstruction

Under the Choi correspondence, \(X_d\) represents
\[
\Phi(A)=\operatorname{Tr}(A)I-\frac12A. \tag{19}
\]
Let
\[
\mathcal D(A)=\operatorname{Tr}(A)I,\qquad
\mathcal R(A)=\operatorname{Tr}(A)I-A.
\]
Then
\[
\Phi=\frac12(\mathcal D+\mathcal R). \tag{20}
\]
The reduction term is co-completely-positive. Indeed, with
\[
K_{ij}=|i\rangle\langle j|-|j\rangle\langle i|,\qquad i<j,
\]
direct entrywise calculation gives the completely positive map
\[
\Psi(A)=\sum_{i<j}K_{ij}AK_{ij}^\dagger
=\operatorname{Tr}(A)I-A^T, \tag{21}
\]
and \(\mathcal R=\Psi\circ T\).

Although (20) is an exact positive/co-CP decomposition, its tensor expansion
does not give termwise two-positivity. Already at one copy, for a rank-two
projection \(P_2\),
\[
\langle\operatorname{vec}(P_2)|
(I-|\Phi_d\rangle\langle\Phi_d|)
|\operatorname{vec}(P_2)\rangle
=\|P_2\|_2^2-|\operatorname{Tr}P_2|^2
=2-4=-2. \tag{22}
\]
Thus the \(\mathcal R\) summand itself is negative on Schmidt rank two;
the depolarizing summand is quantitatively essential. Tensor-level proofs
must track cancellation between the \(2^n\) CP/co-CP patterns.

## 7. A strengthened conjecture suggested by exact extremizers

The following inequality is consistent with the exact one-copy bound,
Corollary 4.2, product-code equality families, and floating-point searches:
\[
\boxed{\qquad
Q_n(C)\stackrel{?}{\ge}
2^{-n}\bigl(s_1(C)-s_2(C)\bigr)^2
\quad(\operatorname{rank}C\le2).
\qquad} \tag{23}
\]
It would settle endpoint two-block positivity and describe a large part of
the equality boundary. It is **not proved** here.

Two tempting proofs of (23) fail:

1. Bounding the crossed term in (3) by \(H_{12}\ge-2^{-n}\) is false.
   At \(n=2\), choose orthonormal \(a_1,a_2\), put
   \(u_r=a_r\otimes x\), \(v_r=a_r\otimes y\), and choose \(x\perp y\).
   Then
   \[
   H_{11}=H_{22}=\frac12,\qquad H_{12}=-\frac12,
   \]
   whereas \(-2^{-n}=-1/4\). The larger diagonal entries exactly compensate.

2. Applying ordinary Cauchy--Schwarz in the positive metric \(Y_d^{\otimes n}\)
   gives
   \[
   |H_{12}|^2
   \le K(u_1,v_2)K(u_2,v_1),\qquad
   K(a,b)=\langle a\otimes b|Y_d^{\otimes n}|a\otimes b\rangle.
   \]
   The desired replacement of mismatched by matched diagonals is false even
   at one copy: for \(u_r=v_r=e_r\),
   \[
   K(u_1,v_2)K(u_2,v_1)=1,\qquad
   K(u_1,v_1)K(u_2,v_2)=\frac14.
   \]
   The actual crossed matrix element contains phase/cancellation information
   discarded by this Cauchy--Schwarz step.

## 8. Symmetry reduction and why marginal overlap bounds are insufficient

For each copy let \(P_i=|\Omega_d\rangle\langle\Omega_d|\). The commuting
spectral projections generated by the \(P_i\)'s give an ordinary probability
distribution after independently twirling a Schmidt-number-at-most-two
state under \(U_i\otimes\overline U_i\). Twirling is legitimate in the dual
formulation: it is a convex mixture of local unitaries and therefore
preserves Schmidt number at most two.

At \(d=3\), if \(K\) is the number of outcomes \(P_i\), then
\[
\langle X_3^{\otimes n}\rangle=\mathbb E[(-1/2)^K]. \tag{24}
\]
For a normalized rank-two coefficient matrix, the elementary bound
\[
\|\operatorname{Tr}_S C\|_2
\le \|\operatorname{Tr}_S C\|_1
\le \|C\|_1
\le\sqrt2\,\|C\|_2 \tag{25}
\]
implies
\[
\Pr(P_i=1\text{ for every }i\in S)\le \frac2{d^{|S|}}. \tag{26}
\]
For completeness, the middle inequality in (25) follows by taking a singular
decomposition \(C=\sum_rs_r|u_r\rangle\langle v_r|\), flattening \(u_r,v_r\)
across \(S:S^c\), and using
\[
\|\operatorname{Tr}_S|u_r\rangle\langle v_r|\|_1
\le\|A_r\|_2\|B_r\|_2=1.
\]

The intersection bounds (26), even for every subset, do not imply the sign
in (24). For every \(n\ge2\), the abstract distribution concentrated on
\(K=1\) obeys (26) after permutation symmetrization whenever
\(1/n\le2/3\), but has
\[
\mathbb E[(-1/2)^K]=-\frac12.
\]
Such a distribution need not be realizable by a Schmidt-rank-two vector;
the example proves that a dual-cone proof based only on the separate overlap
bounds loses indispensable compatibility information.

## 9. Two further exact obstructions to simple dual certificates

### 9.1 Positive sums of global isotropic witnesses do not suffice

For nonempty \(S\subseteq[n]\), let
\[
Z_S=I-\frac12\bigotimes_{i\in S}|\Phi_d\rangle\langle\Phi_d|.
\]
Each \(Z_S\) is two-block-positive by the global trace inequality
\(|\operatorname{Tr}C|\le\sqrt2\|C\|_2\) after grouping the factors in
\(S\) into one system. One might hope to write \(X_3^{\otimes n}\) as a
positive sum of the \(Z_S\)'s plus a positive operator.

This is already impossible at \(n=2\), even allowing an arbitrary invariant
positive residual. In the joint spectral sector \(T=\{1\}\),
\(X_3^{\otimes2}\) has eigenvalue \(-1/2\). Among the \(Z_S\), only \(Z_{\{1\}}\)
is negative there, with eigenvalue \(-1/2\); every other \(Z_S\) has
eigenvalue \(1\). Therefore a nonnegative-coefficient decomposition forces
the coefficient of \(Z_{\{1\}}\) to be at least \(1\). The sector
\(T=\{2\}\) similarly forces the coefficient of \(Z_{\{2\}}\) to be at
least \(1\). But in the sector \(T=\varnothing\), all \(Z_S\) have eigenvalue
\(1\), while \(X_3^{\otimes2}\) has eigenvalue \(1\). The two forced
coefficients already sum to \(2\), so the residual cannot be positive.

### 9.2 No linear sum-of-squares identity in \(C\)

There cannot be an identity on the rank-at-most-two variety of the form
\[
Q_n(C)=\sum_j|\ell_j(C)|^2, \tag{27}
\]
with linear functionals \(\ell_j\). Indeed both sides are Hermitian quadratic
forms. Their difference would vanish in particular on every rank-one matrix,
equivalently on every product vector. Repeated polarization in the two
tensor factors implies that a Hermitian operator whose quadratic form
vanishes on all product vectors is the zero operator. Hence (27) would hold
for every \(C\), making \(X_d^{\otimes n}\) positive semidefinite. This is
false already for \(n=1,d\ge3\), since its eigenvalue on
\(|\Phi_d\rangle\) is \(1-d/2<0\).

Therefore any sum-of-squares proof must use nonlinear rank-two
factor variables, denominators, or additional inequalities; a quadratic
SOS directly in the entries of \(C\) cannot exist.

### 9.3 Exact failure of a compression stable-rank bound

A plausible strengthening for
\[
R_n=(I-F/2)^{\otimes n}
\]
was that every compression
\[
K=(P_U\otimes P_V)R_n(P_U\otimes P_V),
\qquad \dim U=\dim V=2,
\]
satisfies
\[
2\|K\|_{\mathrm{op}}\le\operatorname{Tr}K. \tag{28}
\]
This is sharp at one copy, but false already for \(d=3,n=2\).

Use only levels \(0,1\), set
\[
j=\frac{|01\rangle-|10\rangle}{\sqrt2},\qquad
U=\operatorname{span}\{j,|11\rangle\},\qquad
V=\operatorname{span}\{j,|00\rangle\}.
\]
In the ordered product basis
\[
(j\otimes j,\ j\otimes|00\rangle,\ |11\rangle\otimes j,\
 |11\rangle\otimes|00\rangle),
\]
direct exact contraction gives
\[
K=
\begin{pmatrix}
3/4&0&0&1/2\\
0&1/2&0&0\\
0&0&1/2&0\\
1/2&0&0&1
\end{pmatrix}. \tag{29}
\]
Its characteristic polynomial is
\[
(\lambda-\tfrac12)^2
\left(\lambda^2-\frac74\lambda+\frac12\right),
\]
so its spectrum is
\[
\left\{\frac12,\frac12,\frac{7-\sqrt{17}}8,
\frac{7+\sqrt{17}}8\right\}.
\]
Since \(\operatorname{Tr}K=11/4\),
\[
\frac{2\|K\|_{\mathrm{op}}}{\operatorname{Tr}K}
=\frac{7+\sqrt{17}}{11}>1.
\]
The deterministic symbolic check is
`discovery/agent_dual_compression_counter.py`. Thus any argument that
deduces the endpoint from (28) is too strong.

## 10. Equality information for the proved cone

At one copy and \(\alpha=-1/2\),
\[
Q_1(C)=0,\quad 0<\operatorname{rank}C\le2,
\]
holds exactly when
\[
C=e^{i\theta}sP,\qquad s>0,
\]
with \(P\) an orthogonal rank-two projection. Indeed equality is required in
both
\[
|\operatorname{Tr}C|\le\|C\|_1
\quad\text{and}\quad
\|C\|_1\le\sqrt2\|C\|_2.
\]
The second equality forces two equal nonzero singular values. In the polar
decomposition \(C=U|C|\), equality in the first forces \(U\) to be a common
phase on the support of \(|C|\), giving the claimed form. The converse is
immediate.

Consequently, for a nonzero tensor-factorized matrix
\[
C=C_1\otimes\cdots\otimes C_n,\qquad\operatorname{rank}C\le2,
\]
one has \(Q_n(C)=0\) exactly when the unique possible rank-two factor is
\(e^{i\theta}sP_2\) as above; all other factors may be arbitrary nonzero
rank-one matrices. If every factor has rank one, (6) makes the inequality
strict.

Equality in the strengthened bound (15b) has a slightly narrower
factor-by-factor description. Every rank-one factor must be a phase times a
positive rank-one operator, and the possible rank-two factor must be a phase
times a positive semidefinite rank-two operator (its two eigenvalues need
not agree).

For the general one-sided product-code theorem, the proof gives an exact,
if implicit, criterion: equality holds precisely when
\[
|\zeta\rangle=\sum_rc_r|r\rangle|u_r\rangle
\in\ker\mathcal K,
\]
where \(\mathcal K\) is the positive diagonal compression in (13). Thus the
only equality mechanisms inside this cone come from kernels of the local
\(k\)-block compressions and their tensor product; there is no hidden
negative cancellation.

## 11. Precise status and limitations

### What is proved here

1. Formula (1) and the crossed-Gram formulas (3)--(8) are exact for every
   \(d,n\). They reduce the endpoint problem to compatibility of a family
   of \(2\times2\) partial-contraction Gram matrices.
2. Lemma 3.1 is dimension-independent: any finite-copy negative
   Schmidt-rank-two witness for a block-positive \(W\) yields, on two
   replicas, a negative witness with equal Schmidt coefficients. Its
   phase and conjugation conventions have been audited explicitly.
3. The adjoint-mixed determinant (E8) is also exactly negative and has
   equal singular values. The one-sided copy swap (E10) makes it normal
   of rank two, but (E11)--(E12) prove that this operation does not
   preserve the relevant tensor-paired expectation.
4. Theorem 4.1 gives a genuinely tensor-stable cone: endpoint
   nonnegativity holds whenever either side's two codewords factor across
   all copies, even if the other side is arbitrarily entangled.
5. The block recursion, boundary-rank construction, three-label kernel,
   CP/co-CP split, invariant-decomposition obstruction, and stable-rank
   compression counterexample are exact no-go results for several natural
   induction or dual-decomposition strategies.
6. The positive flag dilation (E14)--(E15) is an exact normal rank-two
   reduction. It would become a closure argument only after proving an
   additional inequality involving \(Q_n(P_R)\), \(Q_n(P_L)\), and
   \(\mathfrak B(P_R,P_L)\).

### Exact verification layer

The following deterministic scripts use only exact rational and radical
arithmetic.

- `discovery/agent_dual_compression_counter.py` verifies the matrix (29),
  its exact characteristic polynomial, and
  \((7+\sqrt{17})/11>1\).
- `discovery/agent_dual_adjoint_check.py` verifies rank two, skew
  Hermiticity after the normalizing swap, and the exact sign change
  \(-2\mapsto+2\).
- `discovery/agent_dual_flag_check.py` constructs an exact positive
  rank-two dilation and verifies both sides of (E15), obtaining \(30\).

All three checks passed on 2026-07-28. The floating-point search scripts
are discovery-only and are not used as evidence for any statement above.

### What remains unresolved

This notebook does **not** prove endpoint two-block positivity, construct
an endpoint negative witness, or establish either all-copy Alternative A
or eventual-distillability Alternative B. The central missing statement
can be expressed in any of three equivalent-looking ways:

- a compatibility inequality making the alternating Gram sum (8)
  positive;
- the conjectural singular-value bound (23);
- a support-projection inequality strong enough to control (E15).

The exact counterexamples show why weaker substitutes do not suffice:
individual subset-overlap bounds ignore compatibility, complete boundary
positivity is false once the boundary has three labels, global isotropic
decomposition is too rigid, and normalizing a negative partial isometry by
a one-sided swap changes the operator pairing.

No hardware limitation affected these conclusions. Larger numerical
searches could generate further conjectures, but they would not by
themselves address the missing uniform-in-\(n\) theorem.
