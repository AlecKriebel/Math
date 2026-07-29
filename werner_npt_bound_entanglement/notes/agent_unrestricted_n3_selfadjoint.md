# The self-adjoint and normal three-copy endpoint

## Status

For arbitrary finite-dimensional local spaces
\[
 {\cal H}=H_1\otimes H_2\otimes H_3,
\]
the three-copy endpoint form obeys the sharp singular-value bound
\[
 Q_3(H)\geq\frac18\bigl(s_1(H)-s_2(H)\bigr)^2
 \tag{S1}
\]
on every self-adjoint operator of rank at most two.  The same bound
holds for every normal operator of rank at most two.  In particular,
both classes are endpoint-nonnegative.

The only input from the earlier three-copy work is the already proved
positive rank-two estimate
\[
 Q_3(K)\geq
 \frac18\left(2\operatorname{Tr}K^2-(\operatorname{Tr}K)^2\right)
 \qquad(K\succeq0,\ \operatorname{rank}K\leq2).
 \tag{1}
\]
The new ingredient is an upper bound on the polarized endpoint form
between two orthogonal pure states.  It has a particularly transparent
proof: the defect is exactly a sum of the all-locally-antisymmetric
replica mass and three complementary marginal overlaps.

## 1. Notation

For operators \(C,D\) on \({\cal H}\), let
\[
 {\cal B}_3(C,D)
 =
 \sum_{S\subseteq[3]}
 \left(-\frac12\right)^{|S|}
 \operatorname{Tr}\!\left[
   (\operatorname{Tr}_S C)^\dagger
   \operatorname{Tr}_S D
 \right].
 \tag{2}
\]
Thus \(Q_3(C)={\cal B}_3(C,C)\).

If \(w\in{\cal H}\) is a unit vector, write
\[
 P_w=|w\rangle\langle w|,
 \qquad
 \rho_T^w=\operatorname{Tr}_{\bar T}P_w.
 \tag{3}
\]

## 2. The orthogonal cross-term bound

### Lemma 2.1

If \(u,v\in{\cal H}\) are orthogonal unit vectors, then
\[
 \boxed{\qquad
 {\cal B}_3(P_u,P_v)\leq\frac18.
 \qquad}
 \tag{4}
\]
More precisely, if
\[
 x_i=\operatorname{Tr}(\rho_i^u\rho_i^v),\qquad
 y_i=\operatorname{Tr}(\rho_{\bar i}^u\rho_{\bar i}^v)
 \tag{5}
\]
and
\[
 c_{123}=\left\|
 \prod_{i=1}^3\frac{I-F_i}{2}(u\otimes v)
 \right\|^2,
 \tag{6}
\]
then
\[
 \boxed{\qquad
 \frac18-{\cal B}_3(P_u,P_v)
 =2c_{123}+\frac14\sum_i y_i.
 \qquad}
 \tag{7}
\]

### Proof

Changing variables from the traced set \(S\) in (2) to its complement
\(T=\bar S\), and using orthogonality, gives
\[
 {\cal B}_3(P_u,P_v)
 =
 -\frac18+\frac14\sum_i x_i
 -\frac12\sum_i y_i.
 \tag{8}
\]
On the other hand, expanding the three local antisymmetric projectors
in (6) gives
\[
 8c_{123}=1-\sum_i x_i+\sum_i y_i.
 \tag{9}
\]
Substitution of (9) into (8) gives the exact identity (7).
Every term on the right of (7) is nonnegative, proving (4).
\(\square\)

The equality statement is also exact:
\[
 {\cal B}_3(P_u,P_v)=\frac18
 \quad\Longleftrightarrow\quad
 c_{123}=0\ \text{ and }\ y_1=y_2=y_3=0.
 \tag{10}
\]

## 3. Every self-adjoint rank-two operator

### Theorem 3.1

If \(H=H^\dagger\) and \(\operatorname{rank}H\leq2\), then
\[
 \boxed{\qquad
 Q_3(H)\geq
 \frac18\bigl(s_1(H)-s_2(H)\bigr)^2\geq0.
 \qquad}
 \tag{11}
\]

### Proof

If \(H\) is positive or negative semidefinite, apply (1) to \(H\) or
\(-H\); the form is unchanged by a global sign.  If its two nonzero
eigenvalues have the same sign, the right side of (1) is the square of
their difference divided by eight.

It remains to consider the indefinite case.  Write
\[
 H=\lambda P_u-\mu P_v,
 \qquad \lambda,\mu>0,\quad \langle u,v\rangle=0.
 \tag{12}
\]
Set
\[
 a=Q_3(P_u),\qquad b=Q_3(P_v),\qquad
 c={\cal B}_3(P_u,P_v).
 \tag{13}
\]
The rank-one specialization of (1) gives
\[
 a,b\geq\frac18,
 \tag{14}
\]
and Lemma 2.1 gives \(c\leq1/8\).  Therefore
\[
\begin{aligned}
 Q_3(H)
 &=\lambda^2a+\mu^2b-2\lambda\mu c\\
 &\geq\frac18(\lambda^2+\mu^2-2\lambda\mu)
 =\frac18(\lambda-\mu)^2\geq0.
\end{aligned}
\tag{15}
\]
Here \(\lambda,\mu\) are exactly the two nonzero singular values of
\(H\).  Together with the same-sign case from (1), this proves the
displayed singular-value bound in every signature.
This covers every self-adjoint operator of rank at most two.
\(\square\)

The indefinite estimate admits the exact nonnegative-defect
decomposition
\[
\begin{aligned}
 Q_3(\lambda P_u-\mu P_v)-\frac18(\lambda-\mu)^2
={}&\lambda^2\left(Q_3(P_u)-\frac18\right)
  +\mu^2\left(Q_3(P_v)-\frac18\right)\\
 &+2\lambda\mu\left(\frac18-{\cal B}_3(P_u,P_v)\right).
\end{aligned}
\tag{16}
\]
For a pure projector,
\[
 Q_3(P_w)=\frac18+\frac14\left(
 3-\sum_i\operatorname{Tr}[(\rho_i^w)^2]\right),
\tag{17}
\]
so equality in the rank-one bound holds precisely when \(w\) is fully
product.  Combining (7), (16), and (17) classifies the nonzero
indefinite zeroes.  They have \(\lambda=\mu\), and, up to a permutation
of the three parties and local phases,
\[
 u=a_1\otimes a_2\otimes a_3,\qquad
 v=b_1\otimes b_2\otimes a_3,
 \qquad
 \langle a_1,b_1\rangle=\langle a_2,b_2\rangle=0.
\tag{18}
\]
Indeed, for product \(u,v\), the conditions in (10) say that two local
overlaps vanish and the remaining local overlap has modulus one.

An immediate polarization consequence will be useful below.  For every
orthonormal pair \(u,v\), the real matrix
\[
 G(u,v)=
 \begin{pmatrix}
 Q_3(P_u)&{\cal B}_3(P_u,P_v)\\
 {\cal B}_3(P_u,P_v)&Q_3(P_v)
 \end{pmatrix}
 \tag{19}
\]
is positive semidefinite, because its quadratic form is
\(Q_3(xP_u+yP_v)\) for real \(x,y\).

## 4. Every normal rank-two operator

### Corollary 4.1

If \(C\) is normal and \(\operatorname{rank}C\leq2\), then
\[
 \boxed{\qquad
 Q_3(C)\geq\frac18\bigl(s_1(C)-s_2(C)\bigr)^2\geq0.
 \qquad}
 \tag{20}
\]

### Proof

By the spectral theorem,
\[
 C=z_1P_u+z_2P_v
 \tag{21}
\]
for orthogonal unit vectors \(u,v\) and complex scalars \(z_1,z_2\).
Write \(C=A+iB\), where
\[
 A=(\operatorname{Re}z_1)P_u+(\operatorname{Re}z_2)P_v,
 \qquad
 B=(\operatorname{Im}z_1)P_u+(\operatorname{Im}z_2)P_v.
\tag{22}
\]
Both \(A\) and \(B\) are self-adjoint of rank at most two.  Moreover,
\({\cal B}_3(A,B)\) is real, so
\[
 Q_3(C)=Q_3(A)+Q_3(B).
\tag{23}
\]
Theorem 3.1 gives
\[
\begin{aligned}
8Q_3(C)\geq{}&
\bigl(|\operatorname{Re}z_1|-|\operatorname{Re}z_2|\bigr)^2\\
&+\bigl(|\operatorname{Im}z_1|-|\operatorname{Im}z_2|\bigr)^2.
\end{aligned}
\tag{24}
\]
The right side is the squared Euclidean distance between
\((|\operatorname{Re}z_1|,|\operatorname{Im}z_1|)\) and
\((|\operatorname{Re}z_2|,|\operatorname{Im}z_2|)\).  The reverse
triangle inequality bounds it below by
\((|z_1|-|z_2|)^2\), proving (20).
\(\square\)

For mere nonnegativity there is a slightly larger solved locus.  If
there is a two-dimensional subspace \(W\subseteq{\cal H}\) such that
\[
 C=P_WCP_W,
\tag{25}
\]
then both Hermitian quadratures \(A=(C+C^\dagger)/2\) and
\(B=(C-C^\dagger)/(2i)\) have rank at most two.  Equation (23) and
Theorem 3.1 therefore give \(Q_3(C)\geq0\).  For rank-two \(C\),
condition (25) is equivalent to
\[
 \operatorname{ran}C=\operatorname{ran}C^\dagger.
\tag{26}
\]
This common-two-plane locus strictly contains the normal locus.

### Corollary 4.2: the two-plane PPT formulation

Let \(V:\mathbb C^2\to{\cal H}\) be an isometry.  Let
\[
 Y=\bigotimes_{i=1}^3\left(I-\frac12F_i\right)\succ0
\tag{27}
\]
on two physical replicas, and compress it to the two logical replicas:
\[
 K_3(V)=(V^\dagger\otimes V^\dagger)Y(V\otimes V).
\tag{28}
\]
Then
\[
 \boxed{\qquad K_3(V)^{\Gamma_2}\succeq0.\qquad}
\tag{29}
\]

Indeed, partial transposition on the second logical replica gives
\[
 K_3(V)^{\Gamma_2}
 =(V^\dagger\otimes V^T)X^{\otimes3}
   (V\otimes\overline V),
\tag{30}
\]
where \(X=I-\frac12|\Phi\rangle\langle\Phi|\) is the coefficient-matrix
operator for one endpoint copy.  Here and below,
\(\operatorname{Re}M=(M+M^\dagger)/2\) and
\(\operatorname{Im}M=(M-M^\dagger)/(2i)\) denote the Hermitian
quadratures.  For every \(M\in M_2\),
\[
\begin{aligned}
 \langle\operatorname{vec}M,K_3(V)^{\Gamma_2}
       \operatorname{vec}M\rangle
 &=Q_3(VMV^\dagger)\\
 &=Q_3(V\,\operatorname{Re}M\,V^\dagger)
   +Q_3(V\,\operatorname{Im}M\,V^\dagger)\geq0,
\end{aligned}
\tag{31}
\]
because the two displayed coefficient matrices are self-adjoint of
rank at most two.  Thus (29) is exactly the operator form of positivity
on every coefficient matrix supported by one physical two-plane.

For comparison, the earlier real matrix \(G(u,v)\) in (19) is positive
semidefinite.  It is therefore positive semidefinite also as a complex
Hermitian matrix.  Consequently
\[
 \begin{pmatrix}\overline z_1&\overline z_2\end{pmatrix}
 G(u,v)
 \begin{pmatrix}z_1\\z_2\end{pmatrix}\geq0,
\tag{32}
\]
which is the diagonal spectral subcompression of (29).

## 5. Exact description of the remaining locus

Let \(C\) have rank two and singular-value decomposition
\[
 C=s_1|u_1\rangle\langle v_1|
   +s_2|u_2\rangle\langle v_2|,
 \qquad s_1,s_2>0,
 \tag{33}
\]
where both \((u_1,u_2)\) and \((v_1,v_2)\) are orthonormal pairs.  Put
\[
\begin{aligned}
 a&=Q_3(|u_1\rangle\langle v_1|),\\
 b&=Q_3(|u_2\rangle\langle v_2|),\\
 z&={\cal B}_3(
   |u_1\rangle\langle v_1|,
   |u_2\rangle\langle v_2|).
\end{aligned}
\tag{34}
\]
Then
\[
 \boxed{\qquad
 Q_3(C)=s_1^2a+s_2^2b+2s_1s_2\operatorname{Re}z.
 \qquad}
 \tag{35}
\]
The rank-one theorem gives \(a,b\geq1/8\).  Thus the unrestricted
three-copy problem is exactly the following matched-two-plane
inequality:
\[
 \boxed{\qquad
 \operatorname{Re}z\geq-\sqrt{ab}
 \quad\text{for all two orthonormal pairs }(u_1,u_2),(v_1,v_2).
 \qquad}
 \tag{36}
\]
Indeed, (36) makes the real \(2\times2\) quadratic form in (35)
positive semidefinite for every \(s_1,s_2\geq0\); conversely, failure of
(36) gives a negative value after choosing
\(s_1:s_2=\sqrt b:\sqrt a\).

The conjectured sharp quantitative bound
\[
 Q_3(C)\geq\frac18(s_1-s_2)^2
\tag{37}
\]
is equivalently the stronger shifted copositivity inequality
\[
 \boxed{\qquad
 \operatorname{Re}z+\frac18
 \geq-\sqrt{\left(a-\frac18\right)
                   \left(b-\frac18\right)}.
 \qquad}
\tag{38}
\]
Thus (36), or more sharply (38), is the smallest scalar obstruction
after both singular flags have been fixed.

### 5.1 Coupled Hermitian-pair canonical form

The common rank-two origin of the Hermitian quadratures can be retained
without referring to the ambient dimension.  Let
\[
 U=(u_1,u_2),\qquad V=(v_1,v_2),\qquad
 S=\operatorname{diag}(s_1,s_2),
\tag{39}
\]
so \(C=USV^\dagger\), and put
\[
 K=V^\dagger U,\qquad R=(I-K^\dagger K)^{1/2}.
\tag{40}
\]
The matrix \(K\) is a contraction.  Choose the partial isometry \(W\)
in the polar decomposition of \((I-VV^\dagger)U\), with initial
space \(\operatorname{supp}R\) and final space contained in
\((\operatorname{ran}V)^\perp\).  Then
\[
 U=VK+WR.
\tag{41}
\]
When the orthogonal complement has dimension at least two, \(W\) may
be extended harmlessly to an isometry on all of \(\mathbb C^2\).
Otherwise the zero directions of \(R\) are simply omitted.
Relative to \(\operatorname{ran}V\oplus\operatorname{ran}W\), all of
\(C\) is therefore contained in the four-dimensional block
\[
 \boxed{\qquad
 C=
 \begin{pmatrix}
 KS&0\\
 RS&0
 \end{pmatrix}.
 \qquad}
\tag{42}
\]
Zero rows and columns may be deleted when \(R\) is singular.  Conversely,
every positive diagonal \(S\), every \(2\times2\) contraction \(K\), and
\(R=(I-K^\dagger K)^{1/2}\) in (42) produce a rank-at-most-two matrix.
Thus (42) is an exact canonical parametrization of the coupled
Hermitian pair, not a relaxation.

Writing \(C=A+iB\), it gives
\[
\boxed{
\begin{aligned}
2A&=
\begin{pmatrix}
 KS+SK^\dagger&SR\\
 RS&0
\end{pmatrix},\\[1mm]
2B&=
\begin{pmatrix}
 -i(KS-SK^\dagger)&iSR\\
 -iRS&0
\end{pmatrix}.
\end{aligned}}
\tag{43}
\]
The solved common-two-plane case is exactly \(R=0\), equivalently
\(K\) unitary.  If \(\operatorname{rank}R=1\), the unsolved pair acts
on only three dimensions.  If \(R\) is invertible, every Hermitian
quadrature
\[
 H_\theta=e^{-i\theta}C+e^{i\theta}C^\dagger
\tag{44}
\]
has inertia \((2,2)\): its lower-right block is zero and its off-diagonal
block \(e^{-i\theta}RS\) is invertible.  This explains why separate
rank-two Hermitian positivity does not settle the transverse case.

More generally, whether or not \(R\) is invertible, every \(H_\theta\)
has at most two positive and at most two negative eigenvalues.  Indeed,
if its positive spectral subspace had dimension at least three, it
would meet \(\ker C\), which has codimension at most two.  A nonzero
vector in the intersection would have both
\(\langle x,H_\theta x\rangle>0\) and
\(\langle x,H_\theta x\rangle
=2\operatorname{Re}(e^{-i\theta}\langle x,Cx\rangle)=0\),
a contradiction.  The negative case is identical.

On the fully transverse stratum, the rank-two coupling has an even
smaller intrinsic form.  Fix a phase and put
\[
 A=\operatorname{Re}C,\qquad B=\operatorname{Im}C.
\tag{45}
\]
Here \(A\) is invertible on the four-dimensional space
\(\operatorname{ran}C+\operatorname{ran}C^\dagger\).  Define
\[
 J=A^{-1}B.
\tag{46}
\]
Since \(B\) is Hermitian,
\[
 J^\dagger A=AJ.
\tag{47}
\]
Moreover,
\[
 C=A(I+iJ),\qquad C^\dagger=A(I-iJ).
\tag{48}
\]
Both \(C\) and \(C^\dagger\) have two-dimensional kernels.  Thus \(J\)
has a two-dimensional \(+i\) eigenspace and a two-dimensional \(-i\)
eigenspace.  These eigenspaces span the four-dimensional support, so
\[
 \boxed{\qquad J^2=-I,\qquad B=AJ,\qquad
 B A^{-1}B=-A.\qquad}
\tag{49}
\]
Conversely, if \(A\) is invertible Hermitian and \(J\) obeys
\(J^\dagger A=AJ\) and \(J^2=-I\), then \(A\) has inertia \((2,2)\)
and \(A(I+iJ)\) has rank two.  Indeed the \(\pm i\) eigenspaces are
two complementary \(A\)-isotropic spaces.  Nondegeneracy of \(A\)
forces the pairing between them to be nondegenerate, so they have the
same dimension, namely two.  In bases adapted to them, \(A\) has the
form
\(\left(\begin{smallmatrix}0&G\\G^\dagger&0\end{smallmatrix}\right)\)
with \(G\) invertible, which has inertia \((2,2)\); also \(I+iJ\)
vanishes exactly on the \(+i\) plane.

Consequently the entire fully transverse three-copy problem is the
following explicit coupled-complex-structure inequality:
\[
 \boxed{\qquad
 Q_3(A)+Q_3(AJ)\geq0
 \quad\text{whenever}\quad
 A=A^\dagger,\ J^\dagger A=AJ,\ J^2=-I.
 \qquad}
\tag{50}
\]
Unlike positivity for arbitrary inertia \((2,2)\), (50) retains exactly
the nonlinear rank-two equation.  It is strictly smaller than (36):
the singular flags have been replaced by one Hermitian form and one
pseudo-Hermitian complex structure on a four-dimensional support.

The one-dimensional-intersection stratum has a parallel cubic normal
form.  Here
\[
 \dim(\operatorname{ran}C+\operatorname{ran}C^\dagger)=3.
\]
If no Hermitian quadrature is invertible, both quadratures at any fixed
phase have rank at most two and Theorem 3.1 already proves positivity.
Otherwise choose a phase for which \(A=\operatorname{Re}C\) is
invertible on this three-dimensional support and again put
\(J=A^{-1}B\).  The kernels of
\(C=A(I+iJ)\) and \(C^\dagger=A(I-iJ)\) show that \(+i\) and \(-i\)
are simple eigenvalues of \(J\).  Since
\(J^\dagger=AJA^{-1}\), the spectrum of \(J\) is invariant under
complex conjugation; its third eigenvalue \(r\) is therefore real.

Replace \(C\) by \(e^{-i\phi}C\), where \(\tan\phi=r\).  The new
quadrature ratio is
\[
 J_\phi=(\cos\phi\,I+\sin\phi\,J)^{-1}
        (\cos\phi\,J-\sin\phi\,I).
\tag{50a}
\]
This Möbius transform fixes \(+i\) and \(-i\) and sends \(r\) to zero.
The first factor in (50a) is invertible.  Hence, after this canonical
phase choice,
\[
 \boxed{\qquad
 J_\phi^\dagger A_\phi=A_\phi J_\phi,\qquad
 J_\phi(J_\phi^2+I)=0,\qquad
 \operatorname{rank}(A_\phi J_\phi)=2.
 \qquad}
\tag{50b}
\]
Thus the intersection-one problem reduces to
\[
 Q_3(A)+Q_3(AJ)\geq0
\quad\text{under}\quad
 A=A^\dagger\text{ invertible on }\mathbb C^3,\quad
 J^\dagger A=AJ,\ J(J^2+I)=0.
\tag{50c}
\]
The second quadrature \(AJ\) is self-adjoint of rank two and is
therefore controlled by Theorem 3.1.  Only its coupled compensation
with the rank-three first quadrature remains.  Together, (25), (50),
and (50c) split the problem exactly by support dimensions \(2,4,3\),
respectively.

### 5.2 Rank-one plus Hermitian rank-one: the exact three-dimensional
normal form

The cubic normal form above admits a sharper and more geometric
description.  It removes \(J\) completely and reduces the
intersection-one stratum to one Gram determinant involving only three
vectors.

#### Proposition 5.1

Let \(C\) have rank two and
\[
 \dim(\operatorname{ran}C+\operatorname{ran}C^\dagger)=3.
\tag{50d}
\]
After multiplication of \(C\) by a scalar phase, there are rank-one
operators \(R,D\) such that
\[
 \boxed{\qquad C=R+D,\qquad R=R^\dagger,\qquad
 \operatorname{rank}R=\operatorname{rank}D=1.\qquad}
\tag{50e}
\]
More intrinsically, in the canonical phase of (50b), let
\[
 A=\operatorname{Re}C,\qquad B=\operatorname{Im}C,\qquad
 J=A^{-1}B,
\tag{50f}
\]
and let \(k\) be a unit vector spanning \(\ker B=\ker J\).  Then
\[
 \alpha=\langle k,Ak\rangle\ne0,\qquad
 R=\frac{|Ak\rangle\langle Ak|}{\alpha},\qquad
 D=C-R
\tag{50g}
\]
give the decomposition (50e).  Both \(D\) and \(D^\dagger\) annihilate
\(k\).

#### Proof

The three eigenspaces of \(J\), with eigenvalues \(0,+i,-i\), span the
support because the polynomial \(t(t^2+1)\) has distinct roots.  Use
the nondegenerate Hermitian form
\[
 [x,y]_A=\langle x,Ay\rangle.
\tag{50h}
\]
The relation \(J^\dagger A=AJ\) implies that if \(Jx=\lambda x\) and
\(Jy=\mu y\), then
\[
 (\overline\lambda-\mu)[x,y]_A=0.
\tag{50i}
\]
Thus the zero eigenspace is \(A\)-orthogonal to both the \(+i\) and
the \(-i\) eigenspaces.  If also \([k,k]_A=0\), then \(k\) would be
\(A\)-orthogonal to all three eigenspaces and hence to the whole
support.  This would give \(Ak=0\), contradicting the invertibility of
\(A\).  Therefore \(\alpha\ne0\).

Decompose the support as \(k^\perp\oplus\mathbb Ck\).  Since \(Bk=0\)
and \(B=B^\dagger\), the two quadratures have block forms
\[
 A=\begin{pmatrix}A_0&a\\a^\dagger&\alpha\end{pmatrix},
 \qquad
 B=\begin{pmatrix}B_0&0\\0&0\end{pmatrix}.
\tag{50j}
\]
The operator in (50g) and its complement in \(A\) are
\[
 R=
 \begin{pmatrix}
  aa^\dagger/\alpha&a\\a^\dagger&\alpha
 \end{pmatrix},
 \qquad
 H:=A-R=
 \begin{pmatrix}
  A_0-aa^\dagger/\alpha&0\\0&0
 \end{pmatrix}.
\tag{50k}
\]
In particular, \(R\) is Hermitian of rank one, and
\[
 D=C-R=H+iB
 =
 \begin{pmatrix}
  A_0-aa^\dagger/\alpha+iB_0&0\\0&0
 \end{pmatrix}.
\tag{50l}
\]
Taking the Schur complement of the lower-right entry in
\(C=A+iB\) gives
\[
 0=\det C
 =\alpha\det\!\left(
 A_0-aa^\dagger/\alpha+iB_0\right).
\tag{50m}
\]
Hence the displayed \(2\times2\) block in \(D\) has rank at most one.
It cannot vanish: its Hermitian and skew-Hermitian parts would then
both vanish, forcing \(B=0\), contrary to the \(\pm i\) eigenvalues of
\(J\).  Thus \(D\) has rank exactly one.  Equation (50l) also proves
the two kernel assertions.
\(\square\)

Conversely, a sum
\[
 C=\gamma |w\rangle\langle w|+\delta|u\rangle\langle v|,
 \qquad \gamma\in\mathbb R,\quad\delta\in\mathbb C,
\tag{50n}
\]
always has rank at most two.  When all coefficients are nonzero and
\(w,u,v\) are linearly independent, it has rank two and the union of
the ranges of \(C\) and \(C^\dagger\) is their three-dimensional span.
The linearly dependent and zero-coefficient cases lie in the already
solved support-at-most-two or rank-one strata, and are also limits of
the independent case.

It follows that the whole intersection-one problem is equivalent to
one explicit rank-one Gram inequality.  For unit vectors \(w,u,v\),
put
\[
 a=Q_3(P_w),\qquad b=Q_3(|u\rangle\langle v|),\qquad
 z={\cal B}_3(P_w,|u\rangle\langle v|).
\tag{50o}
\]
Then
\[
 \boxed{\qquad
 \text{intersection-one positivity}
 \quad\Longleftrightarrow\quad
 |z|^2\leq ab\quad\text{for every }w,u,v.
 \qquad}
\tag{50p}
\]
Indeed, the quadratic form of (50n) is
\[
 Q_3(C)=\gamma^2a+|\delta|^2b+
 2\gamma\operatorname{Re}(\delta z).
\tag{50q}
\]
It is nonnegative for all real \(\gamma\) and complex \(\delta\) if
and only if the \(2\times2\) Gram determinant \(ab-|z|^2\) is
nonnegative.  Proposition 5.1 proves sufficiency for every
intersection-one matrix.  Conversely, independent triples in (50n)
are physical rank-two matrices in that stratum, and they are dense
among all triples, proving necessity including the boundary cases.

The replica form makes the remaining issue especially compact:
\[
 z=
 \left\langle w\otimes v\left|
 \bigotimes_{i=1}^3\left(I-\frac12F_i\right)
 \right|u\otimes w\right\rangle.
\tag{50r}
\]
Thus (50p) is a three-vector four-point, or reflection-positivity,
inequality for one fixed positive replica filter.  Ordinary
Cauchy--Schwarz gives the wrong two diagonal terms,
\[
 |z|^2\leq
 Q_3(|w\rangle\langle v|)
 Q_3(|u\rangle\langle w|),
\tag{50s}
\]
so it does not prove (50p).

There is also an exact reason that Theorem 3.1 by itself cannot yield
(50p) merely by quadrature polarization.  Put
\[
 D=|u\rangle\langle v|,\qquad
 X_\theta=\operatorname{Re}(e^{-i\theta}D).
\tag{50t}
\]
The self-adjoint theorem applied to all \(X_\theta\) controls
\({\cal B}_3(D,D^\dagger)\), but the desired number
\({\cal B}_3(P_w,D)\) occurs only in mixed matrices
\(sP_w+tX_\theta\).  For an orthonormal triple
\((u,v,w)\), the matrix of this Hermitian operator on their span is
\[
 \begin{pmatrix}
 0&te^{-i\theta}/2&0\\
 te^{i\theta}/2&0&0\\
 0&0&s
 \end{pmatrix},
 \qquad
 \det(sP_w+tX_\theta)=-\frac14st^2.
\tag{50u}
\]
It has rank three whenever \(st\ne0\).  Hence the rank-at-most-two
self-adjoint theorem never tests a mixed point in this direct
quadrature family and therefore gives no constraint on \(z\) by this
polarization.  This is a geometric obstruction to the direct route,
not merely a loss in a numerical estimate; a new three-vector
inequality is genuinely required.

### 5.3 A rigorous phase-quadrature lower bound

The cross-term lemma also gives a useful theorem beyond rank two.
If \(H=H^\dagger\) has at most two positive and at most two negative
eigenvalues, write \(H=H_+-H_-\).  The two parts are positive
rank-at-most-two operators with orthogonal ranges.  Lemma 2.1 applied
to every positive/negative eigenvector pair gives
\[
 {\cal B}_3(H_+,H_-)
 \leq\frac18\operatorname{Tr}H_+\operatorname{Tr}H_-.
\tag{51}
\]
Applying (1) separately to \(H_+\) and \(H_-\) therefore yields
\[
 \boxed{\qquad
 Q_3(H)\geq
 \frac18\left(2\|H\|_2^2-\|H\|_1^2\right).
 \qquad}
\tag{52}
\]

For every phase put
\[
 A_\theta=\operatorname{Re}(e^{-i\theta}C),\qquad
 B_\theta=\operatorname{Im}(e^{-i\theta}C).
\tag{53}
\]
The two matrices obey the inertia hypothesis above, and
\[
 Q_3(C)=Q_3(A_\theta)+Q_3(B_\theta),\qquad
 \|C\|_2^2=\|A_\theta\|_2^2+\|B_\theta\|_2^2.
\tag{54}
\]
Consequently
\[
\boxed{\qquad
 Q_3(C)\geq\frac18\left[
 2\|C\|_2^2-\|A_\theta\|_1^2-\|B_\theta\|_1^2
 \right]\quad(\text{every }\theta).
\qquad}
\tag{55}
\]
This reduces the remaining nonnormal locus to the explicit sufficient
condition
\[
 \inf_{\theta\in\mathbb R}
 \left(\|A_\theta\|_1^2+\|B_\theta\|_1^2\right)
 \leq2\|C\|_2^2.
\tag{56}
\]
Condition (56) is genuinely smaller than the original tensor
inequality, but it is not automatic from rank two.  For the transverse
partial isometry
\[
 C=|e_3\rangle\langle e_1|+|e_4\rangle\langle e_2|,
\tag{57}
\]
the two quadratures have spectra
\(\{1/2,1/2,-1/2,-1/2\}\) for every phase.  Hence the left side of
(56) is \(8\), while \(2\|C\|_2^2=4\).  The rank-two coupling needed
after (55) must therefore use more than the separate inertia of the
two quadratures.

There is also a small exact obstruction to strengthening (52) to
positivity for every inertia-\((2,2)\) Hermitian matrix.  On three
qutrits put
\[
\begin{aligned}
p_1&=|022\rangle,&p_2&=|101\rangle,\\
n_1&=|120\rangle,&n_2&=|202\rangle,
\end{aligned}
\tag{58}
\]
and
\[
 H=\frac12(P_{p_1}+P_{p_2}-P_{n_1}-P_{n_2}).
\tag{59}
\]
In the order
\[
S=\varnothing,\ 1,\ 2,\ 12,\ 3,\ 13,\ 23,\ 123,
\]
the exact squared norms of its partial traces are
\[
 1,\ 1,\ 1,\ \frac12,\ 1,\ 0,\ \frac12,\ 0.
\tag{60}
\]
Therefore
\[
 \boxed{\qquad Q_3(H)=-\frac14.\qquad}
\tag{61}
\]
So inertia alone is decisively insufficient.

The same example also displays the missing quadrature compensation.
For any \(U=(U_{rs})\in U(2)\), define
\[
 B_U=\frac12\sum_{r,s=1}^2
 \left(U_{rs}|p_r\rangle\langle n_s|
 +\overline{U_{rs}}|n_s\rangle\langle p_r|\right).
\tag{62}
\]
Relative to the positive and negative eigenspaces of \(H\),
\[
 H+iB_U
 =\frac12
 \begin{pmatrix}I&iU\\ iU^\dagger&-I\end{pmatrix},
\qquad
 (H+iB_U)^2=0.
\tag{63}
\]
Its rank is exactly two.  Nevertheless,
\[
 Q_3(B_U)=\frac12,\qquad
 Q_3(H+iB_U)=\frac14
\tag{64}
\]
for every \(U\).  To check the first identity, note that
\(\|B_U\|_2^2=1\), every two-site partial trace vanishes, and the sum
of the three one-site-traced squared norms is
\(\frac12\sum_{r,s}|U_{rs}|^2=1\).  Thus the rank-two equation coupling
the two quadratures overcompensates this extremal negative Hermitian
direction by the fixed amount \(1/2\).

The normal locus is the diagonal sublocus in which the left and right
singular planes and matched singular lines can be chosen equal.  The
larger common-two-plane locus is \(R=0\).  The unresolved locus consists
of \(R\ne0\), with the ordered matched singular lines retained when
\(s_1\ne s_2\); the two planes alone do not determine (34).

### 5.4 Elimination of the singular-value optimization

There is an exact determinant formulation of the remaining problem.
It packages all choices of the two singular values and of bases in the
two singular planes into one scalar polynomial.

Let \(U,V:\mathbb C^2\to{\cal H}\) be arbitrary isometries and set
\[
 Y=\bigotimes_{i=1}^3\left(I-\frac12F_i\right),\qquad
 K(U,V)=(U^\dagger\otimes V^\dagger)Y(U\otimes V).
 \tag{65}
\]
Thus \(K(U,V)\) is a strictly positive operator on
\(\mathbb C^2\otimes\mathbb C^2\).  Directly from the crossed-swap
formula, for every \(M\in M_2\),
\[
 Q_3(UMV^\dagger)
 =
 \left\langle\operatorname{vec}M,\,
 K(U,V)^{\Gamma_2}\operatorname{vec}M\right\rangle.
 \tag{66}
\]
Consequently the full unrestricted theorem is equivalent to
\[
 K(U,V)^{\Gamma_2}\succeq0
 \qquad\text{for every pair of isometries }U,V.
 \tag{67}
\]

For these \(4\times4\) matrices, (67) is in turn equivalent to the
single determinant inequality
\[
 \boxed{\qquad
 \det K(U,V)^{\Gamma_2}\geq0.
 \qquad}
 \tag{68}
\]
Here is a self-contained proof of the nontrivial implication.  Partial
transpose of a positive operator is block-positive:
\[
 \langle x\otimes y,K^{\Gamma_2}x\otimes y\rangle
 =
 \langle x\otimes\overline y,Kx\otimes\overline y\rangle>0
 \tag{69}
\]
for nonzero \(x,y\), where strictness follows from \(K\succ0\).
Every two-dimensional subspace of
\(\mathbb C^2\otimes\mathbb C^2\) contains a product vector.  Indeed,
after identifying vectors with \(2\times2\) matrices, a projective line
\([s:t]\mapsto sA+tB\) meets the determinantal quadric because the
homogeneous quadratic \(\det(sA+tB)\) has a projective zero over
\(\mathbb C\).

It follows that a block-positive Hermitian operator on two qubits has
at most one negative eigenvalue.  In the strictly block-positive case,
it cannot have both a negative and a zero eigenvalue: the span of
corresponding eigenvectors contains a product vector, and that product
vector has nonpositive expectation (negative unless it lies entirely
in the zero eigenspace).  Either possibility contradicts strict block
positivity.  Therefore, if
\(K^{\Gamma_2}\) is not positive semidefinite, it has exactly one
negative eigenvalue, no zero eigenvalues, and hence negative
determinant.  This proves (68).

For fixed left and right singular planes, (68) has no residual vector
optimization: it is one explicit degree-four polynomial in the entries
of the compressed positive Gram matrix \(K(U,V)\).  Changing logical
bases conjugates \(K^{\Gamma_2}\) and leaves its determinant unchanged.
The common-plane theorem (29) proves (68) when
\(\operatorname{ran}U=\operatorname{ran}V\).  Thus the determinant still
to be controlled lies precisely on the intersection-one and transverse
strata described by (50c) and (50).

## Research log

- **2026-07-28 21:22 PDT.** Proved the exact antisymmetric-sector
  identity (7), completed the sharp self-adjoint and normal rank-two
  bounds, and extracted the common-two-plane PPT theorem (29).
- **2026-07-28 21:22 PDT.** Reduced the remaining nonnormal locus to the
  canonical contraction data \((S,K)\) in (42), the scalar matched-flag
  inequalities (36)/(38), the complex-structure equation (50), and the
  phase-quadrature estimate (55).  The exact example (59)--(64) refutes
  positivity for arbitrary Hermitian inertia \((2,2)\) and exhibits its
  compulsory rank-two quadrature compensation, so the common origin
  (43) of the two quadratures is essential.
- **2026-07-28 21:42 PDT.** Eliminated all singular-value and logical-basis
  optimization at fixed left/right planes: unrestricted positivity is
  exactly the determinant inequality (68).  The proof uses strict
  block positivity and the elementary fact that every projective line
  in \(M_2\) meets the rank-one quadric.
- **2026-07-28 21:42 PDT.** Reduced the entire intersection-one stratum
  to the exact normal form \(C=R+D\), with \(R\) Hermitian rank one and
  \(D\) arbitrary rank one.  Positivity on this stratum is now exactly
  the three-vector Gram inequality (50p).  Equation (50u) proves that
  the rank-two self-adjoint theorem cannot reach its mixed cross term
  by direct quadrature polarization.
- **2026-07-28 21:55 PDT.** Adversarially audited the determinant
  equivalence (65)--(69) and all support-stratified canonical forms.
  The determinant argument is sound.  Corrected the zero-eigenvector
  branch in its strict-block-positivity proof, made the polar factor in
  (41) a partial isometry on \(\operatorname{supp}R\), and supplied the
  missing equal-multiplicity argument in the converse to (49).
