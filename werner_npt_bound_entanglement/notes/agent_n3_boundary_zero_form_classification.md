# Classification forced by equality in the Haar boundary filter

## Status

This note strengthens the exact Haar-filter ceiling by recovering the
nonlinear equality information discarded by sector averaging.  It
does **not** prove unrestricted three-copy positivity.

The main algebraic lemma is independent of the Werner problem:

> If a Hermitian quadratic form on \(M_3\) is nonnegative on every
> singular matrix and vanishes on every rank-two orthogonal
> projection, then it is a nonnegative multiple of the one-copy
> endpoint form
> \[
> Q_1(A)=\|A\|_2^2-\frac12|\operatorname{Tr}A|^2.
> \]

Consequently, equality in the Haar-filter pair ceiling forces each of
the three complete local-filter forms of one common rank-two matrix
to be exactly isotropic:
\[
 \boxed{\qquad
 Q_3(A^{(i)}C)
 =\gamma\,Q_1(A)
 \quad(A\in M_3,\ i=1,2,3),
 \qquad
 \gamma=-\frac23Q_3(C)\geq0.
 \qquad}                                                     \tag{1}
\]
Thus the formal negative sector point cannot be realized merely by
choosing six abstract contraction maps with the correct norms: a
physical realization at Haar equality must satisfy the full
sesquilinear identities obtained by polarizing (1) at all three
sites.

The dependency-free exact checker is
`verification/verify_n3_boundary_zero_form_classification.py`.

## 1. A quadratic-form classification

Let \(h\) be a Hermitian sesquilinear form on \(M_3\), with associated
self-adjoint linear operator \({\cal H}\):
\[
 h(A,B)=\langle A,{\cal H}(B)\rangle_{\rm HS}.
                                                               \tag{2}
\]
Assume
\[
 h(A,A)\geq0\quad\text{if }\det A=0                         \tag{3}
\]
and
\[
 h(I-|z\rangle\langle z|,I-|z\rangle\langle z|)=0
 \quad\text{for every unit }z.                              \tag{4}
\]

### Theorem

There is a number \(\gamma\geq0\) such that
\[
 \boxed{\qquad
 {\cal H}(A)
 =\gamma\left(A-\frac12\operatorname{Tr}(A)I\right)
 \quad\text{for every }A\in M_3.
 \qquad}                                                     \tag{5}
\]

### Proof

Fix a unit \(z\), put \(P_z=|z\rangle\langle z|\), and
\(A_z=I-P_z\).  The rank-two determinantal variety is smooth at
\(A_z\).  Its complex tangent hyperplane is
\[
 {\cal T}_z=\{B:z^\dagger Bz=0\}.                           \tag{6}
\]
Here is a direct verification.  In a basis with \(z=e_3\), the
derivative of the determinant at
\(\operatorname{diag}(1,1,0)\) is \(B\mapsto B_{33}\).
If \(B_{33}=0\), then
\[
 A(t)=A_z+tB+s(t)E_{33},\qquad
 s(t)=-
 \frac{\det(A_z+tB)}
      {\operatorname{cof}_{33}(A_z+tB)}
                                                               \tag{7}
\]
has determinant zero for all sufficiently small \(t\).
The denominator is \(1+O(t)\), while the numerator is \(O(t^2)\);
hence \(A'(0)=B\).  Conjugating the construction proves (6) for every
\(z\).

By (3)--(4), \(A_z\) is a minimum of \(h(A,A)\) along every such
curve.  Applying the same statement to tangents \(B\) and \(iB\)
gives
\[
 h(B,A_z)=0\qquad(B\in{\cal T}_z).                         \tag{8}
\]
The Hilbert--Schmidt orthogonal complement of \({\cal T}_z\) is the
line \(\mathbb CP_z\).  Therefore
\[
 {\cal H}(A_z)=\lambda_zP_z                                \tag{9}
\]
for some scalar \(\lambda_z\).

Put \(K={\cal H}(I)\).  Equation (9) says
\[
 {\cal H}(P_z)=K-\lambda_zP_z.                             \tag{10}
\]
For every orthonormal basis \((z_1,z_2,z_3)\), sum (10) and use
\(\sum_jP_{z_j}=I\):
\[
 2K=\sum_{j=1}^3\lambda_{z_j}P_{z_j}.                     \tag{11}
\]
Thus \(K\) is diagonal in every orthonormal basis.  It follows
directly that \(K=\kappa I\): any two unit vectors can be included
in orthonormal bases after first rotating inside their span, and
(11) forces all off-diagonal matrix entries and then all diagonal
differences to vanish.  Equation (11) then gives
\(\lambda_z=2\kappa\) for every \(z\).

Hence
\[
 {\cal H}(P_z)=\kappa(I-2P_z).                             \tag{12}
\]
Rank-one orthogonal projections linearly span \(M_3\), so
\[
 {\cal H}(A)=\kappa(\operatorname{Tr}(A)I-2A).             \tag{13}
\]
Self-adjointness makes \(\kappa\) real.  Applying (3) to a rank-one
projection gives \(-\kappa\geq0\).  Setting
\(\gamma=-2\kappa\geq0\) turns (13) into (5). \(\square\)

## 2. Application to a three-copy Haar equality

Let \(C\) have rank at most two.  For each physical site define
\[
 h_i(A,B)
 =
 \left\langle A^{(i)}C,\,
 {\cal L}^{\otimes3}(B^{(i)}C)\right\rangle_{\rm HS}.
                                                               \tag{14}
\]
If \(A\) is singular, \(A^{(i)}C\) has deficient local left support.
The established boundary theorem gives
\[
 h_i(A,A)=Q_3(A^{(i)}C)\geq0.                              \tag{15}
\]

Suppose equality holds in the grouped Haar-filter inequality
\[
 \frac14w_1-w_2+3w_3=0.                                   \tag{16}
\]
Its three sitewise summands are averages of the continuous
nonnegative functions
\[
 z\longmapsto
 Q_3\bigl((I-P_z)^{(i)}C\bigr).
\]
Their sum can vanish only if every function vanishes identically.
The theorem applied to \(h_i\) yields
\[
 h_i(A,B)
 =
 \gamma_i\left(
 \langle A,B\rangle_{\rm HS}
 -\frac12\overline{\operatorname{Tr}A}\operatorname{Tr}B
 \right).
                                                               \tag{17}
\]
Putting \(A=B=I\) gives
\[
 Q_3(C)=\gamma_iQ_1(I)=-\frac32\gamma_i.                  \tag{18}
\]
Thus all three constants coincide and
\[
 \gamma_i=-\frac23Q_3(C),
\]
which proves (1).

In particular, if a physical matrix realized the formal equality
distribution
\[
 (w_0,w_1,w_2,w_3)
 =\left(\frac19,0,\frac23,\frac29\right),
\]
then \(Q_3(C)=-1/8\), \(\gamma=1/12\), and all three polarized local
forms would have to satisfy the explicit \(9\times9\) identities
\[
 h_i=\frac1{12}{\cal L}.                                  \tag{19}
\]
This is a strictly stronger, common-\(C\) realizability condition
than the scalar sector and six separate Gram-norm constraints.  The
remaining equality problem is to exclude (19) using the mixed
two-site commutation/Pluecker identities, or to realize it by an
exact rank-two matrix.

## 3. A critical negative equality is locally maximally mixed

There is a further exact consequence at a stationary point of the
normalized endpoint functional.  Normalize \(\|C\|_2=1\) and put
\[
 q=Q_3(C).
\]
For a left local filter at site \(i\), define
\[
 n_i^L(A,I)
 =\langle A^{(i)}C,C\rangle_{\rm HS}
 =\overline{\operatorname{Tr}(A\rho_i^L)},
\qquad
 \rho_i^L=\operatorname{Tr}_{\widehat i}(CC^\dagger).
                                                               \tag{20}
\]
Stationarity of
\(Q_3(C)/\|C\|_2^2\) along
\(C(t)=(I+tA^{(i)})C\), first for \(A\) and then for \(iA\), gives
the polarized identity
\[
 h_i(A,I)=q\,n_i^L(A,I)
 \quad\text{for every }A.                                  \tag{21}
\]

At a negative Haar equality, (17)--(18) give
\[
 q=-\frac32\gamma,\qquad
 h_i(A,I)=-\frac\gamma2\,\overline{\operatorname{Tr}A}.
                                                               \tag{22}
\]
Substitution in (21), and \(\gamma>0\), imply
\[
 \operatorname{Tr}(A\rho_i^L)=\frac13\operatorname{Tr}A
 \quad\text{for every }A.
\]
Therefore
\[
 \rho_i^L=\frac13I_3.                                      \tag{23}
\]
Applying the same argument to right local filters gives
\[
 \boxed{\qquad
 \rho_i^L=\rho_i^R=\frac13I_3
 \quad(i=1,2,3)
 \qquad}                                                    \tag{24}
\]
at every stationary negative Haar equality.

Consequently, a global negative minimizer realizing the formal
Haar-saturating point would have to satisfy simultaneously:

1. the three exact local form identities \(h_i={\cal L}/12\);
2. all six weighted one-site densities equal to \(I_3/3\);
3. the rank-two singular-plane and mixed-site compatibility
   identities.

This is a finite exact critical-point system.  Its consistency is not
settled here, but it is strictly smaller than the unrestricted
rank-two search and exactly matches the marginal data of the formal
norm-only obstruction.
