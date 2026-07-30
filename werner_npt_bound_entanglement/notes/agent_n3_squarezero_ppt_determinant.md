# The square-zero frontier is one crossed Gram determinant

## Status

This note does **not** prove the remaining determinant inequality.  It
gives a lossless reduction of the complete orthogonal-plane
square-zero problem to one scalar polynomial, with no singular values
or coefficient matrix left to optimize.

Let
\[
 {\cal H}=(\mathbb C^3)^{\otimes3},\qquad
 {\cal L}(A)=A-\frac12\operatorname{Tr}(A)I_3,
 \qquad
 {\cal B}_3(A,B)=\langle A,{\cal L}^{\otimes3}(B)\rangle .
\]
For isometries \(U=(u_0,u_1)\), \(W=(w_0,w_1)\) satisfying
\[
 U^\dagger W=0,                                           \tag{1}
\]
put
\[
 E_{ab}=|u_a\rangle\langle w_b|,\qquad
 H_{ab,cd}={\cal B}_3(E_{ab},E_{cd}).                    \tag{2}
\]
Indices \(ab\) and \(cd\) are ordered as \(00,01,10,11\).

The main exact reduction is
\[
\boxed{
 Q_3(UBW^\dagger)\geq0\quad\hbox{for every }B\in M_2
 \quad\Longleftrightarrow\quad
 \det H(U,W)\geq0.}                                      \tag{3}
\]
Thus general square-zero positivity is precisely one invariant
degree-sixteen crossed-Gram inequality on two orthogonal two-planes.

There are two additional structural facts.

1.  The logical partial transpose \(H^{\Gamma_2}\) is an ordinary
    positive Gram matrix.
2.  \(H\) is *strictly* block positive, with the sharp product margin
    \[
      \langle x\otimes y,H(x\otimes y)\rangle
      \geq\frac14\|x\|^2\|y\|^2.                         \tag{4}
    \]

These facts make the determinant criterion possible, but do not by
themselves prove its sign.  An explicit abstract \(4\times4\) matrix
at the end of the note satisfies both facts and has negative
determinant.  Hence the unresolved sign must use the common
three-qutrit origin of all sixteen entries of \(H\).

The same orthogonality gives an exact auxiliary-parity formula.  In
matched singular-value coordinates,
\[
\boxed{
 Q_3(C)
 =\frac14\|C\|_2^2
  +(p_{0,2}-p_{1,2})
  +3(p_{0,3}-p_{1,3}).}                                  \tag{5}
\]
and, separately for \(k=0,1\),
\[
 p_{k,0}+p_{k,2}=p_{k,1}+p_{k,3}.                        \tag{6}
\]
Equation (5) is the exact compensated inequality suggested by the
numerical boundary.  In particular it explains simultaneously the
canonical nilpotent equality, where the pair-trace term compensates a
one-trace excess, and the fully transverse spin-flip equality, where
the two- and three-skew terms compensate each other.

The dependency-free exact checker is
`verification/verify_n3_squarezero_ppt_determinant.py`.

## 1. Linearization on the logical \(2\times2\) space

Every matrix in this square-zero family is
\[
 C_B=UBW^\dagger=\sum_{a,b}B_{ab}E_{ab}.                 \tag{7}
\]
Condition (1) gives
\[
 C_B^2=UB(W^\dagger U)BW^\dagger=0,
 \qquad \operatorname{rank}C_B\leq2.                    \tag{8}
\]
Conversely, the initial and final singular planes of an operator
whose singular-value decomposition has the form \(U\Sigma W^\dagger\)
and whose square is zero are orthogonal, so (7) is exactly the
orthogonal-plane frontier.

Polarization of the endpoint form gives
\[
\boxed{
 Q_3(C_B)=\operatorname{vec}(B)^\dagger
 H(U,W)\operatorname{vec}(B).}                           \tag{9}
\]
Consequently the left side of (3) is equivalent to \(H\succeq0\).
The point of the next two sections is that, for this particular
\(4\times4\) Hermitian matrix, positive semidefiniteness is equivalent
to its single determinant.

## 2. The crossed positive Gram

On two replicas of one qutrit put
\[
 Y_i=I-\frac12F_i,\qquad
 Y=Y_1\otimes Y_2\otimes Y_3\succ0.                      \tag{10}
\]
Direct partial transposition of the coefficient-matrix contraction
gives, for arbitrary \(u,v,x,y\in{\cal H}\),
\[
 {\cal B}_3(|u\rangle\langle v|,|x\rangle\langle y|)
 =
 \langle u\otimes y,Y(x\otimes v)\rangle.                \tag{11}
\]
Apply (11) to (2):
\[
 H_{ab,cd}
 =\langle u_a\otimes w_d,Y(u_c\otimes w_b)\rangle.       \tag{12}
\]
Taking partial transpose in the second logical index yields
\[
\boxed{
 (H^{\Gamma_2})_{ab,cd}
 =H_{ad,cb}
 =\langle u_a\otimes w_b,
       Y(u_c\otimes w_d)\rangle.}                        \tag{13}
\]
Thus \(H^{\Gamma_2}\) is the Gram matrix of the four vectors
\[
 Y^{1/2}(u_a\otimes w_b),\qquad a,b\in\{0,1\},
\]
and hence
\[
\boxed{H^{\Gamma_2}\succeq0.}                            \tag{14}
\]
Equivalently, the desired matrix \(H\) is the partial transpose of a
positive two-qubit matrix.  The missing determinant says exactly that
this very special two-qubit Gram matrix is PPT.

Formula (13) is also a compact exterior target:
\[
 \det H
 =
 \det\!\left[
  \langle u_a\otimes w_d,Y(u_c\otimes w_b)\rangle
 \right]_{ab,cd}.                                        \tag{15}
\]
All sixteen entries come from the same four orthonormal physical
vectors.  Treating them as an arbitrary positive-Gram partial
transpose loses the essential constraint.

## 3. A sharp strict product margin

The rank-one endpoint margin improves from \(1/8\) to \(1/4\) when
the two physical vectors are orthogonal.

### Lemma 3.1

If \(u\perp w\), then
\[
\boxed{
 Q_3(|u\rangle\langle w|)
 \geq\frac14\|u\|^2\|w\|^2.}                             \tag{16}
\]
The constant is sharp.

### Proof

The three swaps in (10) commute.  On their simultaneous sector having
exactly \(r\) minus signs, \(Y\) has eigenvalue \(3^r/8\), while
\(F_1F_2F_3\) has eigenvalue \((-1)^r\).  Therefore
\[
\boxed{
 Y-\frac14I+\frac18F_1F_2F_3
 =\Pi_{r=2}+3\Pi_{r=3}\succeq0,}                         \tag{17}
\]
where \(\Pi_{r=j}\) is the projector onto the sector with \(j\)
minus signs.

For a product of the two replicas,
\[
 \langle u\otimes w,F_1F_2F_3(u\otimes w)\rangle
 =|\langle u,w\rangle|^2=0.                              \tag{18}
\]
Taking the expectation of (17) proves (16).

Equality holds, for example, when \(u,w\) are computational strings
which differ at exactly one site.  Hence \(1/4\) is sharp.
\(\square\)

For logical product vectors, (7) becomes a rank-one physical
transition between a vector in \(\operatorname{ran}U\) and a vector
in \(\operatorname{ran}W\).  The two are orthogonal by (1), so Lemma
3.1 gives
\[
 \boxed{
 \langle x\otimes y,H(x\otimes y)\rangle
 \geq\frac14\|x\|^2\|y\|^2.}                             \tag{19}
\]
This proves the strict block positivity asserted in (4).

## 4. Why one determinant is lossless

We need one elementary two-qubit fact.

### Lemma 4.1

Every complex two-dimensional subspace of
\(\mathbb C^2\otimes\mathbb C^2\) contains a nonzero product vector.

### Proof

Identify a two-qubit vector with a \(2\times2\) matrix.  For a basis
\(A,B\) of the subspace, the homogeneous quadratic
\[
 (s,t)\longmapsto\det(sA+tB)
\]
has a nontrivial zero over \(\mathbb C\).  At that zero the
corresponding matrix has rank at most one and therefore represents a
product vector.  This also covers the case in which the polynomial
vanishes identically.
\(\square\)

Let \({\cal N}\) be the spectral subspace of \(H\) for its nonpositive
eigenvalues.  If \(\dim{\cal N}\geq2\), Lemma 4.1 supplies a product
vector in \({\cal N}\), whose \(H\)-expectation is nonpositive.  This
contradicts (19).  Hence
\[
 \dim{\cal N}\leq1.                                      \tag{20}
\]
In particular:

* \(H\) has at most one negative eigenvalue;
* if it has a negative eigenvalue, it has no zero eigenvalue;
* a negative \(H\) therefore has exactly one negative and three
  positive eigenvalues, so \(\det H<0\).

The converse is immediate: if \(\det H\geq0\), the preceding
alternative excludes a negative eigenvalue.  Therefore
\[
 H\succeq0\quad\Longleftrightarrow\quad\det H\geq0,       \tag{21}
\]
which, together with (9), proves (3).

The equality information is already useful.  If \(\det H=0\), then
\(H\succeq0\), and every nonzero kernel vector is entangled in the
logical \(2\otimes2\) space by the strict product margin.  Thus any
square-zero endpoint zero has rank exactly two and both singular
values nonzero.

## 5. Exact auxiliary-parity compensation

Take a matched singular-value representation
\[
 C=s_0|u_0\rangle\langle w_0|
   +s_1|u_1\rangle\langle w_1|,
 \qquad s_0,s_1\geq0,                                    \tag{22}
\]
with the four vectors orthonormal.  Define
\[
\begin{aligned}
 |{\cal A}\rangle
 &=\sum_a\sqrt{s_a}|a\rangle_K|u_a\rangle,\\
 |{\cal B}\rangle
 &=\sum_a\sqrt{s_a}|a\rangle_K|w_a\rangle.
\end{aligned}                                             \tag{23}
\]
For \(k\in\{0,1\}\) and \(r\in\{0,1,2,3\}\), let \(p_{k,r}\)
be the squared norm of the component of
\({\cal A}\otimes{\cal B}\) having auxiliary swap parity
\((-1)^k\) and exactly \(r\) physically antisymmetric replica
pairs.

Condition (1) is stronger than scalar orthogonality:
\[
 \operatorname{Tr}_{123}
 |{\cal A}\rangle\langle{\cal B}|
 =
 \operatorname{diag}(\sqrt{s_a})\,
 U^\dagger W\,
 \operatorname{diag}(\sqrt{s_a})
 =0.                                                      \tag{24}
\]
The swap trick therefore gives both
\[
\begin{aligned}
 0&=\sum_{k,r}(-1)^r p_{k,r},\\
 0&=\sum_{k,r}(-1)^{k+r}p_{k,r}.                         \tag{25}
\end{aligned}
\]
Adding and subtracting (25) gives the two separate parity balances
\[
\boxed{
 \sum_r(-1)^rp_{k,r}=0\quad(k=0,1),}                     \tag{26}
\]
which is (6).

Let \(t_k=\sum_rp_{k,r}\).  The auxiliary swap expectation is
\[
 t_0-t_1
 =\operatorname{Tr}(\rho_K^{\cal A}\rho_K^{\cal B})
 =s_0^2+s_1^2
 =\|C\|_2^2.                                             \tag{27}
\]
Finally,
\[
 Q_3(C)
 =\frac18\sum_{k,r}(-1)^k3^r p_{k,r}.                   \tag{28}
\]
For each fixed \(k\), (26) gives
\[
 \sum_r3^rp_{k,r}
 =2t_k+8p_{k,2}+24p_{k,3}.                              \tag{29}
\]
Substitution of (27)--(29) proves (5).

For rank one, \(t_1=0\), so (5) immediately recovers the stronger
bound (16).  For rank two, the only possible negativity is the
coherent imbalance between the \(k=0\) and \(k=1\) two- and
three-skew sectors displayed in (5).  Bounding either difference
independently is incompatible with the known transverse zero.

## 6. Sharp physical equality and an abstract obstruction

Choose
\[
\begin{aligned}
 u_0&=|000\rangle,&u_1&=|100\rangle,\\
 w_0&=|010\rangle,&w_1&=|110\rangle.
\end{aligned}                                             \tag{30}
\]
Then \(U^\dagger W=0\), and exact contraction gives
\[
 H=
 \begin{pmatrix}
 1/4&0&0&-1/4\\
 0&1/2&0&0\\
 0&0&1/2&0\\
 -1/4&0&0&1/4
 \end{pmatrix}.                                          \tag{31}
\]
Its kernel is spanned by \(\operatorname{vec}I_2\), and
\[
 C=UI_2W^\dagger
 =P_{\operatorname{span}\{0,1\}}\otimes
 |0\rangle\langle1|\otimes|0\rangle\langle0|
\]
is the canonical square-zero endpoint equality.

The partial transpose is
\[
 H^{\Gamma_2}=
 \begin{pmatrix}
 1/4&0&0&0\\
 0&1/2&-1/4&0\\
 0&-1/4&1/2&0\\
 0&0&0&1/4
 \end{pmatrix}\succeq0.                                  \tag{32}
\]

It is important that (14) and (19) alone do not prove the missing
determinant.  Let
\[
 |\Phi_2\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2},
 \qquad
 H_{\rm abs}=I_4-\frac32|\Phi_2\rangle\langle\Phi_2|.     \tag{33}
\]
Then
\[
\begin{aligned}
 \langle x\otimes y,H_{\rm abs}(x\otimes y)\rangle
 &\geq\frac14\|x\|^2\|y\|^2,\\
 H_{\rm abs}^{\Gamma_2}
 &=I_4-\frac34F\succeq0,
\end{aligned}                                             \tag{34}
\]
but
\[
 \operatorname{spec}H_{\rm abs}=(-1/2,1,1,1),
 \qquad
 \det H_{\rm abs}=-\frac12.                              \tag{35}
\]
Thus a completion must prove that the abstract obstruction (33)
cannot arise from the common crossed Gram (12) with four physical
orthonormal vectors.  This is the exact remaining square-zero lemma:
\[
\boxed{
 \det\!\left[
  \langle u_a\otimes w_d,
   Y(u_c\otimes w_b)\rangle
 \right]_{ab,cd}\geq0
 \quad
 \text{whenever }(u_0,u_1,w_0,w_1)\text{ is orthonormal}.} \tag{36}
\]

Unlike the original optimization over \(B\), (36) is one explicitly
defined, basis-covariant real polynomial inequality on the complex
Stiefel manifold \(\mathrm{St}(4,27)\).
