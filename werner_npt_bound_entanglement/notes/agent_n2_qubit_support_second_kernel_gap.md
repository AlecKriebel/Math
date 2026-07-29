# A quantitative second-kernel gap on the two-qubit support boundary

## Status

Let \({\cal U}\) be a two-plane embedded in a \(2\times2\) local
support inside two qutrits, and let \(H_{\cal U}\) be the fixed-left
two-copy endpoint compression
\[
 \langle W,H_{\cal U}W\rangle=Q_2(UW^\dagger).
 \tag{1}
\]
The exact boundary classification says that \(H_{\cal U}\) has
nullity one when its minimal support is \(2\times2\); if
\({\cal U}\) has a fixed local factor, its nullity is three.

This note gives an explicit quantitative version.  Identify the two
local supports with \(\mathbb C^2\), identify their tensor product
with \(\mathbb C^4\), and let
\[
 L:\mathbb C^2\longrightarrow{\cal U}^{\perp}
 \tag{2}
\]
be any isometry onto the Hermitian orthogonal complement.  Put
\[
 \Lambda=\overline L,\qquad
 \epsilon=\begin{pmatrix}0&1\\-1&0\end{pmatrix},
 \qquad J=\epsilon\otimes\epsilon,
 \tag{3}
\]
and define the intrinsic symmetric matrix
\[
 M_{\cal U}=\Lambda^{\mathsf T}J\Lambda.
 \tag{4}
\]
Its Frobenius norm is independent of the chosen orthonormal frame
\(L\).  Then
\[
\boxed{\qquad
 \lambda_2(H_{\cal U})
 \geq\frac1{20}\|M_{\cal U}\|_2^2.
 \qquad}
 \tag{5}
\]
Here eigenvalues are ordered increasingly, so
\(\lambda_1(H_{\cal U})=0\).

Moreover,
\[
 M_{\cal U}=0
 \quad\Longleftrightarrow\quad
 {\cal U}=a\otimes\mathbb C^2
 \ \hbox{or}\
 {\cal U}=\mathbb C^2\otimes a.
 \tag{6}
\]
Thus (5) quantitatively measures exactly the rank jump from the
generic one-dimensional kernel to the three-dimensional
fixed-factor kernel.

Numerical discovery suggests that \(1/20\) can be replaced by the
sharp constant \(1/8\).  No such sharpening is claimed here.
The dependency-free checker
`verification/verify_n2_qubit_support_second_kernel_gap.py` verifies
the universal skew-map singular values and constant arithmetic used
in the proof.

## 1. Projection geometry of the compressed endpoint

Choose the two-dimensional local row supports \(E,F\subseteq
\mathbb C^3\).  On
\(\operatorname{Hom}(\mathbb C^3,E)\), the one-copy endpoint form is
represented by
\[
 Z_E=I_6-|e_E\rangle\langle e_E|,
 \qquad e_E=\frac{J_E}{\sqrt2},
 \tag{7}
\]
where \(J_E\) is the canonical identity map from the conjugate
two-dimensional column support to \(E\), extended by zero on its
one-dimensional orthogonal complement.  Thus \(Z_E\) is an
orthogonal projection; define \(Z_F\) identically.

On the row-supported two-copy operator space
\[
 {\cal A}
 =
 \operatorname{Hom}(\mathbb C^3\otimes\mathbb C^3,E\otimes F),
 \qquad\dim{\cal A}=36,
\]
the endpoint form is the orthogonal projection
\[
 Q=Z_E\otimes Z_F.                                      \tag{8}
\]
Put
\[
\begin{aligned}
 {\cal S}&=\{C\in{\cal A}:\operatorname{ran}C\subseteq{\cal U}\},
 &\dim{\cal S}&=18,\\
 {\cal N}&=\ker Q
 =\{J_E\otimes A+B\otimes J_F\},&
 \dim{\cal N}&=11,
\end{aligned}                                             \tag{9}
\]
where
\[
 A\in\operatorname{Hom}(\mathbb C^3,F),\qquad
 B\in\operatorname{Hom}(\mathbb C^3,E).
\]
The fixed-left operator is the compression
\[
 H_{\cal U}=P_{\cal S}QP_{\cal S}|_{\cal S}.
 \tag{10}
\]

Let \(T=P_{{\cal S}^{\perp}}|_{\cal N}\).  The squared singular
values of \(T\) and the eigenvalues of (10) agree, apart from the
seven additional eigenvalues \(1\) caused by
\(\dim{\cal S}-\dim{\cal N}=7\).  This is the elementary
principal-angle identity: the nonzero spectra of
\[
 P_{\cal S}P_{\cal N}P_{\cal S}
 \quad\hbox{and}\quad
 P_{\cal N}P_{\cal S}P_{\cal N}
 \tag{11}
\]
coincide, and subtracting them from the identity gives (10) and
\(T^\dagger T\), respectively.

Split each local column space as its active two-dimensional
conjugate support plus its one-dimensional complement.  Then
\[
 {\cal N}={\cal N}_{00}\mathbin{\widehat\oplus}
          {\cal N}_{01}\mathbin{\widehat\oplus}{\cal N}_{10},
 \qquad
 \dim({\cal N}_{00},{\cal N}_{01},{\cal N}_{10})=(7,2,2).
 \tag{11a}
\]
The core \({\cal N}_{00}\) is supported on the active
\(2\times2\) column block.  The other two summands contain,
respectively, the outside-column part of \(A\) and of \(B\).
They occupy orthogonal column sectors.  Since
\(P_{{\cal S}^{\perp}}\) acts as \(P_{{\cal U}^{\perp}}\) on every
column, \(T\) respects this orthogonal decomposition.  We bound the
core in Sections 2--3 and the two outside-column sectors in
Section 4.

## 2. Skew-plus-scalar parametrization

On the active block, right multiplication by the unitary symmetric
matrix \(J\) maps \({\cal N}_{00}\) onto
\[
 \{S+cJ:S^{\mathsf T}=-S,\ c\in\mathbb C\}.
 \tag{12}
\]
For completeness, the identities
\[
\begin{aligned}
 (I\otimes A)J+\bigl((I\otimes A)J\bigr)^{\mathsf T}
  &=\operatorname{Tr}(A)J,\\
 (B\otimes I)J+\bigl((B\otimes I)J\bigr)^{\mathsf T}
  &=\operatorname{Tr}(B)J
\end{aligned}
\tag{12a}
\]
show that the image is contained in the displayed space; equality
follows because both spaces have dimension seven.  The
representation is unique.  The skew and symmetric summands are
orthogonal, and \(\|J\|_2^2=4\), so
\[
 \|C\|_2^2=\|S\|_2^2+4|c|^2
 \quad\hbox{when}\quad
 CJ=S+cJ.
 \tag{13}
\]

The columns of \(\Lambda=\overline L\) are bilinear annihilators of
\({\cal U}\), because
\[
 \Lambda^{\mathsf T}U=L^\dagger U=0.
 \tag{14}
\]
Consequently
\[
 \operatorname{dist}(C,{\cal S})
 =
 \|L^\dagger C\|_2
 =
 \|\Lambda^{\mathsf T}(S+cJ)\|_2.
 \tag{15}
\]
Set
\[
 R=\Lambda^{\mathsf T}(S+cJ).
 \tag{16}
\]

The restriction of \(R\) back to the annihilator plane satisfies
\[
 R\Lambda+(R\Lambda)^{\mathsf T}
 =
 2c\,\Lambda^{\mathsf T}J\Lambda
 =
 2cM_{\cal U}.
 \tag{17}
\]
Therefore
\[
 \boxed{\qquad
 \|R\|_2\geq |c|\,\|M_{\cal U}\|_2.
 \qquad}
 \tag{18}
\]

## 3. The universal skew gap

Consider first the map on skew matrices
\[
 S\longmapsto\Lambda^{\mathsf T}S.
 \tag{19}
\]
Extend \(\Lambda\) to a unitary basis of \(\mathbb C^4\) and apply the
corresponding unitary congruence to \(S\).  The map then takes the
first two rows of a \(4\times4\) skew matrix.  Its kernel is the
one-dimensional lower-right skew block.  On the orthogonal complement
of that kernel,
\[
\boxed{\qquad
 \|\Lambda^{\mathsf T}S\|_2^2
 \geq\frac12\|S\|_2^2.
 \qquad}
 \tag{20}
\]
Indeed, the \(12\)-entry occurs twice in the first two rows, while
each of the four cross-block entries occurs once; every skew entry
occurs twice in \(\|S\|_2^2\).

Also
\[
 \|\Lambda^{\mathsf T}J\|_2=\sqrt2.
 \tag{21}
\]
Hence, if \(S\) is orthogonal to the kernel line in (20),
\[
 \|R\|_2
 \geq\frac{\|S\|_2-2|c|}{\sqrt2}.
 \tag{22}
\]

Put
\[
 x=\|S\|_2,\qquad y=2|c|,\qquad
 \mu=\|M_{\cal U}\|_2.
 \tag{23}
\]
Equations (18), (22) give
\[
 \|R\|_2\geq
 \max\left\{\frac{\mu y}{2},\frac{x-y}{\sqrt2}\right\},
 \tag{24}
\]
where the second term may simply be discarded when it is negative.
Since
\[
 0\leq\mu\leq\sqrt2,
 \tag{25}
\]
an elementary two-case estimate yields
\[
\boxed{\qquad
 \|R\|_2^2
 \geq\frac{\mu^2}{20}(x^2+y^2).
 \qquad}
 \tag{26}
\]
For clarity, if \(x\leq y\), the first term in (24) gives
\[
 \frac{\|R\|_2}{\sqrt{x^2+y^2}}
 \geq\frac{\mu}{2\sqrt2}
 \geq\frac{\mu}{\sqrt{20}}.
 \]
If \(x\geq y\), write \(t=x/y\).  For
\(1\leq t\leq1+\mu/\sqrt2\), the first term gives
\[
 \frac{\|R\|_2}{\sqrt{x^2+y^2}}
 \geq\frac{\mu}{2\sqrt5}
 =\frac{\mu}{\sqrt{20}},
 \]
because \(t\leq2\).  For \(t\geq1+\mu/\sqrt2\), use the second term;
its quotient is increasing in \(t\) and has at the left endpoint the
same lower bound.

If \(\mu>0\), equation (17) shows that the kernel of the core
restriction \(T|_{{\cal N}_{00}}\) has \(c=0\); equation (20) then
makes it exactly the one skew line already removed.  Thus (26) and
(13) bound every positive squared singular value of the core by
\(\mu^2/20\).

## 4. The two outside-column sectors

It remains to check that the four directions in
\({\cal N}_{01}\oplus{\cal N}_{10}\), which are present in the full
qutrit fixed-left operator, cannot create a smaller second
eigenvalue.

Let \(P_L=P_{{\cal U}^{\perp}}\) on \(E\otimes F\), and put
\[
 \rho_E^L=\operatorname{Tr}_F P_L,\qquad
 \rho_F^L=\operatorname{Tr}_E P_L.
 \tag{26a}
\]
An element of \({\cal N}_{01}\) is parametrized by \(a\in F\).
Its squared norm is \(2\|a\|^2\), while its squared distance from
\({\cal S}\) is
\[
 \sum_{j=1}^2
 \|P_L(e_j\otimes a)\|^2
 =\langle a,\rho_F^L a\rangle.
 \tag{26b}
\]
Consequently
\[
 \lambda_{\min}\left(
 T^\dagger T|_{{\cal N}_{01}}\right)
 =\frac12\lambda_{\min}(\rho_F^L).
 \tag{26c}
\]
The other sector gives
\[
 \lambda_{\min}\left(
 T^\dagger T|_{{\cal N}_{10}}\right)
 =\frac12\lambda_{\min}(\rho_E^L).
 \tag{26d}
\]

Both marginal deficits control \(M_{\cal U}\) explicitly:
\[
\boxed{\qquad
 \|M_{\cal U}\|_2^2
 \leq4\lambda_{\min}(\rho_E^L),\qquad
 \|M_{\cal U}\|_2^2
 \leq4\lambda_{\min}(\rho_F^L).
 \qquad}
 \tag{26e}
\]
To prove the second inequality, put
\(\widetilde\rho_F^L=\operatorname{Tr}_E(\overline{P_L})
=\overline{\rho_F^L}\).  It has the same eigenvalues as
\(\rho_F^L\).  Fix a unit \(b\in F\), choose a unit
\(b_\perp\perp b\), and write the two columns of \(\Lambda\) as
\[
 \Lambda_r=x_r\otimes b_\perp+y_r\otimes b
 \qquad(r=1,2).
 \tag{26f}
\]
Let \(X=(x_1,x_2)\), \(Y=(y_1,y_2)\).  Since \(\Lambda\) is an
isometry,
\[
 X^\dagger X+Y^\dagger Y=I_2,
 \qquad
 \|X\|_{\rm op}\leq1,
 \qquad
 \|Y\|_2^2=\langle b,\widetilde\rho_F^L b\rangle.
 \tag{26g}
\]
Up to an irrelevant unit scalar coming from the basis
\((b_\perp,b)\),
\[
 M_{\cal U}=X^{\mathsf T}\epsilon Y+
            (X^{\mathsf T}\epsilon Y)^{\mathsf T}.
 \tag{26h}
\]
Hence
\[
 \|M_{\cal U}\|_2
 \leq2\|X^{\mathsf T}\epsilon Y\|_2
 \leq2\|Y\|_2.
 \tag{26i}
\]
Minimizing over \(b\) proves the second inequality in (26e); swapping
the two local factors proves the first.

Equations (26c)--(26e) show that every outside-column squared
singular value is at least \(\mu^2/8\).  The core has one zero
singular value and all its others are at least \(\mu^2/20\).
Together with the principal-angle identity this proves (5) when
\(\mu>0\).  If \(\mu=0\), the right side of (5) is zero and the
inequality is immediate.

Finally, \(M_{\cal U}=0\) says that the annihilator plane is totally
isotropic for \(J\).  Reshaping its vectors as \(2\times2\) matrices,
the identity
\[
 \xi^{\mathsf T}J\xi=2\det\xi
 \tag{27}
\]
shows that every member has rank at most one.  The elementary
upper-rank-one classification then gives a common row or column
factor.  Taking the annihilator interchanges the corresponding
ruling and proves (6).

## 5. A quantitative two-slice/one-site bridge

The second-kernel gap immediately gives a form adapted to the
three-copy slice pencil.

### Corollary 5.1 (two independent approximate kernel slices)

Let
\[
 A:\mathbb C^2\longrightarrow E\otimes F
 \subseteq\mathbb C^3\otimes\mathbb C^3
\]
have rank two, let \(G=A^\dagger A\), and assume
\[
 G\succeq\kappa^2I_2.                                    \tag{28}
\]
Let
\(Y_1,Y_2:\mathbb C^2\to\mathbb C^3\otimes\mathbb C^3\)
obey
\[
 \left(\langle Y_p,Y_q\rangle_{\rm HS}\right)_{p,q=1}^2
 \succeq mI_2.                                           \tag{29}
\]
If
\[
 \left|
 {\cal B}_2(AY_p^\dagger,AY_q^\dagger)
 \right|\leq B
 \qquad(p,q=1,2),                                        \tag{30}
\]
then, for \({\cal U}=\operatorname{ran}A\),
\[
\boxed{\qquad
 \|M_{\cal U}\|_2^2
 \leq\frac{40B}{\kappa^2m}.
 \qquad}                                                  \tag{31}
\]
Equivalently, every vector \(\Lambda z\) in the normalized
annihilator pencil satisfies the explicit minor bound
\[
\boxed{\qquad
 \left|\det\operatorname{mat}(\Lambda z)\right|^2
 \leq\frac{10B}{\kappa^2m}\|z\|^4.
 \qquad}                                                  \tag{32}
\]

#### Proof

Take the polar factorization
\[
 A=UG^{1/2},\qquad U^\dagger U=I_2,
 \tag{33}
\]
and put
\[
 W_p=Y_pG^{1/2}\qquad(p=1,2).
 \tag{34}
\]
Then \(AY_p^\dagger=UW_p^\dagger\), so the matrix in (30) is
\[
 K=\bigl(\langle W_p,H_{\cal U}W_q\rangle\bigr)_{p,q=1}^2.
 \tag{35}
\]
It is positive semidefinite.  Its four entries have modulus at most
\(B\), whence
\[
 \|K\|_{\rm op}\leq\|K\|_2\leq2B.                        \tag{36}
\]

For every \(z\in\mathbb C^2\), assumptions (28) and (29) give
\[
\begin{aligned}
 \left\|\sum_pz_pW_p\right\|_2^2
 &=\operatorname{Tr}\left(
 G\left(\sum_pz_pY_p\right)^\dagger
       \left(\sum_qz_qY_q\right)\right)\\
 &\geq\kappa^2m\|z\|^2.
\end{aligned}                                             \tag{37}
\]
Thus the span of \(W_1,W_2\) is two-dimensional and every Rayleigh
quotient of \(H_{\cal U}\) on it is at most
\[
 \frac{\|K\|_{\rm op}}{\kappa^2m}
 \leq\frac{2B}{\kappa^2m}.
 \tag{38}
\]
The min--max principle and (5) prove (31).

Finally, (27) and (4) give
\[
 2\det\operatorname{mat}(\Lambda z)
 =z^{\mathsf T}M_{\cal U}z.                              \tag{39}
\]
Combining
\[
 |z^{\mathsf T}M_{\cal U}z|
 \leq\|M_{\cal U}\|_2\|z\|^2
\]
with (31) proves (32). \(\square\)

Thus two quantitatively independent approximate two-copy kernel
directions force the entire annihilator pencil quantitatively close,
in determinant, to the upper-rank-one locus.  This is the exact
two-slice/one-site bridge needed in the three-copy stability
argument.  Notice that no individual bound on the two slice
directions is used: their common \(2\times2\) Gram floor is essential.

## 6. Role in the three-copy stability problem

The complete quantitative route now has three distinct pieces.

1. The local quantitative-isotropy theorem converts a small Haar
   bracket into a small rank-one block-Gram defect.
2. A full-support fixed-left determinant gap would force each
   near-kernel slice plane close to a common \(2\times2\) support.
3. The present theorem converts two quantitatively independent
   near-kernel vectors on that boundary into small
   \(\|M_{\cal U}\|_2\), hence proximity to a fixed-factor plane.

The negative-minimizer marginal floor supplies the quantitative
independence needed in step 3 and excludes an actual factor-plane
pencil.  What remains is to control the perturbation from a nearly
\(2\times2\)-supported plane to its boundary compression and to make
the factor-side pencil argument quantitative.  Thus (5) closes the
second-nullity part of the stability chain but not the full
three-copy sign problem.
