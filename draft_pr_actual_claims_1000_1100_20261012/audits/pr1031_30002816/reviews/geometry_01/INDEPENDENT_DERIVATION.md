# Independent geometric reconstruction

This is family A's reconstruction of the geometric bridge in PR #1031, head
`f6570e093267a7f910faf9cdd60dfbc1c12f5681`, prepared after reading only the submitted
proof and its pin inventory. The submitted acceptance assertions, historical
reports, and other families' conclusions were not read before this derivation.
The conclusions below concern the geometric reduction. They do not independently
certify the external theorem about semidefinite lifts of separable states, the
moment/SOS implication, novelty, or the full target theorem.

## Claim, conventions, and success criteria

Let V be R^12 with its ordered orthonormal basis e1,f1,...,e6,f6, and J(ej)=fj,
J(fj)=-ej. The real Euclidean space V is the underlying real space of C^6.
Let C be the convex hull of both orientations of unit simple real 4-vectors.
Let W = exterior^2_C(C^6), and Herm(W) be its real space of Hermitian operators.
The proposed claim is that the simultaneous affine section

    C intersect {Phi = 1, Q = 0}

is real-linearly isomorphic to the convex hull of complex product projectors on
C^3 tensor C^3. Here omega=sum ej* wedge fj*, Phi=omega^2/2, and
Q=(omega_U^2+omega_Z^2)/2 for the orthogonal coordinate 3+3 split.

Success requires a universal proof of all set equalities, orientation signs,
and positivity restrictions, together with a real-linear injective map and
checkable coordinate evidence. Finite examples alone cannot certify the set
equalities. Zero vectors, dependent factors, nonorthogonal factors, reversed
orientations, complex phases, higher-rank mixed tensors, and the ambient
hyperplanes outside C are relevant boundaries.

## 1. Supporting maximum and exact equality case

For a unit simple 4-vector p, choose its oriented real orthonormal frame and let
P be its plane. The compression S = projection_P J |_P is skew-adjoint and has
operator norm at most one. Orthogonal block diagonalization of a real 4 by 4
skew matrix gives two blocks [0,-lambda; lambda,0], with |lambda| <= 1. Depending
on the oriented basis its Pfaffian has a sign, but its absolute value is
|lambda1 lambda2|. Evaluating omega^2/2 on the frame equals this Pfaffian up to
the fixed equivalent skew-matrix convention; its absolute value is therefore
at most 1. Direct evaluation on ej,fj,ek,fk gives +1 and fixes the convention.

If Phi(p)=1, both singular values equal one. Thus S is an isometry on all of P.
For v in P the orthogonal decomposition Jv=S v + projection_(P perp) Jv has
||Jv||^2=||v||^2=||S v||^2. Its perpendicular component vanishes. Hence P is
J-invariant. A J-invariant real 4-plane has a complex-orthonormal basis a,b, and
the real frame a,Ja,b,Jb has Phi=1. Reversing its orientation gives Phi=-1.
Consequently the +1 equality set is exactly the complex 2-planes with complex
orientation, not both orientations.

Compactness is elementary: the Stiefel manifold of orthonormal real 4-frames is
compact, and the wedge map is continuous and surjective onto the generators.
Its convex hull in a finite-dimensional space is compact. Every point in that
hull is a finite convex combination. When Phi of a combination equals its
maximum 1, each positive-weight summand also has Phi=1; there is no possibility
that non-equality generators cancel. Therefore F=C intersect {Phi=1} is exactly
the hull of the positively oriented complex planes.

## 2. Real-linear complexification map

Put uj=(ej-i fj)/sqrt(2) and ujbar=(ej+i fj)/sqrt(2). Then J uj=i uj and
J ujbar=-i ujbar. These 12 vectors form a basis of V_C. In particular the
225 monomials ui wedge uj wedge urbar wedge usbar (i<j,r<s) are distinct basis
elements of the (2,2) component of exterior^4 V_C.

For H in Herm(W), define

    A(H)=sum_(I,J) H_IJ uI wedge uJbar.

Conjugation sends its I,J term to H_JI uIbar wedge uJ. Interchanging exterior
factors of degree two has sign (-1)^4=+1; relabeling I,J returns the same sum.
So A(H) lies in the real fixed space, and A is real-linear. Its complex-linear
extension from all 15 by 15 matrices is injective by the basis statement, hence
its restriction to the real 225-dimensional Hermitian space is injective.
The square-root factors combine to 1/4. On the usual real Hermitian basis
(diagonals, real symmetric off-diagonals, imaginary skew off-diagonals) every
real exterior coefficient lies in (1/4)Z. This gives rational coefficients and
does not make an invalid complex-linear claim about Herm(W).

For a=(a_j) in C^6, define ahat=sum a_j uj. If a is identified with the real
vector sum (Re a_j) ej + (Im a_j) fj, then

    a=(ahat+ahatbar)/sqrt(2), Ja=i(ahat-ahatbar)/sqrt(2),
    a wedge Ja=-i ahat wedge ahatbar.

For all a,b, including dependent or zero vectors, z=a wedge b therefore gives

    A(zz*)=ahat wedge bhat wedge ahatbar wedge bhatbar
          =a wedge Ja wedge b wedge Jb.

The two factors -i initially give a minus sign, and moving ahatbar past bhat
gives the second minus sign. The result is positive. No orthogonality
assumption was used in this identity. With complex Gram-Schmidt, every nonzero
simple z is c a wedge b for orthonormal a,b; ||z||=|c|. For a unit z the unit
phase c can be absorbed into a. Thus A maps the projectors of all unit simple
complex bivectors exactly onto the generators of F. Linearity proves

    F=A(K), K=conv {zz*: z simple complex, ||z||=1}.

Unit complex phases do not change zz* or the real oriented 4-plane. A scales
zz* by |c|^2 when z scales by c. For nonorthogonal a,b, the norm of the resulting
real 4-vector is ||a wedge b||^2, agreeing with the trace of zz*, not generally
||a||^2||b||^2. This is an important normalization boundary.

In the real exterior basis, the coefficient on ei wedge fi wedge ej wedge fj
is H_(ij),(ij). No off-diagonal I,J can contribute because the four real
coordinates occupy exactly those two complex coordinate lines. Each diagonal
term contributes +1. Hence Phi(A(H))=trace H for every Hermitian H.

## 3. Positive face restriction and exact mixed tensors

Use the orthogonal complex decomposition E=U direct-sum Z, dim U=dim Z=3.
Then W splits orthogonally into exterior^2 U, B=U wedge Z, and exterior^2 Z.
Let D be the sum of the first and last spaces. For H=sum lambda_t z_t z_t* in K,

    trace(P_D H)=sum lambda_t ||P_D z_t||^2 >= 0.

When this is zero, every positive-weight z_t lies in B. This uses positivity
of the convex weights and squares. Merely asserting matrix support would be
weaker, though also true. In fact if H is PSD with trace(P_D H)=0, then writing
H=R R* shows P_D R=0, so H is supported on B.

Suppose a nonzero simple z=a wedge b lies in B. Writing a=a_U+a_Z and b=b_U+b_Z,
its pure components vanish, so the spans of a_U,b_U and of a_Z,b_Z have
dimension at most one. Neither span can be zero: that would put the whole
nonzero z in one pure exterior summand while z lies in the orthogonal mixed
summand. Choose nonzero x,y spanning the respective projected lines. Then

    a=alpha x+gamma y, b=beta x+delta y,
    z=(alpha delta-beta gamma) x wedge y.

The scalar is nonzero because z is nonzero, and can be absorbed into x.
Therefore z=x wedge y with x in U,y in Z. Conversely such a vector is simple
and mixed. Thus under the unitary map T(x tensor y)=x wedge y, the nonzero
simple mixed vectors are exactly rank-one complex tensors.

An equivalent coordinate obstruction is useful for adversarial checks: if
z=sum M_ir ui wedge zr in B, the coefficient of ui wedge uj wedge zr wedge zs
in z wedge z is -2(M_ir M_js-M_is M_jr). A rank-two mixed M has a nonzero minor
and cannot be a simple bivector. No cancellation or higher-rank exception is
possible. This is a secondary coordinate certificate, not a substitute for
the projection-line proof above.

Since U is perpendicular to Z, ||x wedge y||=||x|| ||y||. If z is unit, each
factor can be normalized separately without changing z: their norm product
is one. Thus unit simple mixed projectors correspond exactly to
xx* tensor yy* with ||x||=||y||=1. Taking positive convex hulls yields

    K intersect {trace(P_D H)=0} = T Sep(3,3) T*.

## 4. Ambient section and lift preservation

The same diagonal-coefficient argument gives Q(A(H))=trace(P_D H). It follows
from F=A(K) that the simultaneous section of C by Phi=1 and Q=0 is exactly the
image of the preceding separable-state set. Q is nonnegative on F, but not on
all of C: the negatively oriented pure-U plane has Q=-1. This does not break
the two-equation section argument, since Phi=1 is imposed at the same time.

Both hyperplanes alone do not force separability in the whole real ambient
space. For example a rank-one entangled H supported on B has trace H=1 and
trace(P_D H)=0; A(H) satisfies both equations but is outside C. Indeed if it
were in C it would be in F=A(K). A convex decomposition of a rank-one PSD H
into projectors forces every generating vector into its one-dimensional
range, which is impossible when that vector is a nonsimple mixed bivector.

A is injective and T is unitary, so the section is isomorphic as a real affine
convex set to Sep(3,3). The inverse is real-linear on its image; choosing a
real basis of the image and extending it to a basis of exterior^4 V extends
the inverse to a real-linear ambient map. No nonlinear inverse is necessary.

If C is the image pi(S) of a finite spectrahedron S, imposing the section's
affine equations on pi(s) imposes two affine equalities on S. This is again a
finite spectrahedron: if needed each equality can be encoded by opposite
scalar LMI blocks. Composing its projection with the extended inverse map
gives a finite lift of Sep(3,3). This elementary implication is unconditional.
The conclusion that C has no finite lift is conditional on the external
separable-state obstruction, which is outside this family's assignment.

## Current strongest result and exact remaining gap

The geometric set equality and preservation argument above are proved by
elementary finite-dimensional real/complex linear algebra and convexity.
No circular dependence on the target nonrepresentability theorem was used.
Coordinate verification and hostile numerical/algebraic controls are pending
at the time this initial reconstruction was written. No geometric gap or
counterexample has been identified. The external obstruction and moment/SOS
theory remain separate audit obligations, and priority remains unestablished.
