# Reconstruction before reading earlier audit conclusions

Recorded 2026-10-04 04:18:57 UTC. No earlier ESTEROV_SPECIALIZATION, DERIVATION, REPORT, VERDICT, or disposition read yet. Completion estimate: 45% of adversarial verification.

Let n≥1, Q a full-dimensional Delzant lattice polytope, A=Q∩Z^n, and the degree of its complete very ample toric embedding exceed one. Let I(F) be Esterov's Minkowski integral of Γ_F=conv{(e_a,a):a∈A∩F}, projected to the coefficient coordinates R^A. Its integration measure is (dim F+1)! times lattice Lebesgue measure. Use lower support s_K(w)=min_{z∈K}<w,z> throughout.

## The Hurwitz side without a tied-coefficient substitution

Take n universal independent equations F_i=sum_a t_{ia}x^a. The coefficient parameters t_{ia} are all independent. Their Newton polytopes are Γ_i=conv{(e_{ia},a)}. For every selected nonempty face polynomial in any row i, differentiation with respect to one parameter t_{ia} gives the nonzero torus monomial x^a. Different rows have disjoint parameter sets. Thus all selected row Jacobians are independent; Esterov Definition 5.5's general-position condition holds, including its smaller family of compatible faces with injective base projection. Pairwise differences of A generate the full lattice: at any Delzant vertex the primitive directions of its n edges form a lattice basis and the first lattice point along each edge belongs to A. Consequently the lattice divisor in Theorem 5.10 is one.

Project coefficient coordinates by L(e_{ia})=e_a, without substituting or evaluating the discriminant polynomial. All LΓ_i=Γ_Q. Mixed fiber polytopes commute with L: the diagonal case follows by applying L to every integrated section, or by equality of every lower support function; polarization yields the mixed case. This also commutes with signed Minkowski expressions because their support functions add and subtract. Set k=n,l=n−1 in Theorem 5.10. Faces of dimension j<n−1 cannot contribute because n positive exponents cannot sum to j+1. For j=n−1 there is one composition, all exponents one; for j=n there are n compositions, one exponent two. Smooth signed Euler obstruction is (-1)^(n−j). Hence the projected Newton polytope of the reduced universal complete-intersection discriminant is the actual convex polytope

    K_H = n I(Q) − sum_{facets F} I(F).                         (H)

The minus sign is a Minkowski difference justified by Theorem 5.10; it must not be interpreted as arbitrary convex-set subtraction. Identifying this universal reduced complete-intersection discriminant with the Stiefel pullback of Hu_X still needs the standard algebraic meaning of these forms and a boundary-codimension check. This identification must be examined before declaring the source request answered.

## The product discriminant side

For B=A×Vert(Δ_(n−1)), use universal independent coefficient parameters u_{ia}. The ordinary hypersurface-discriminant case l=0 of Theorem 5.10 or Theorem 4.10 gives a signed face-integral expression for its Newton polytope. The coefficient projection L has Γ_(F×E) projecting to Γ_F×E. A j-face F and an l-face E of the standard simplex give the exact factor

    L I_B(F×E) = [(j+l+1)! / ((j+1)! l!)] I(F)
                = binom(j+l+1,j+1) I(F).                      (P)

This follows either by integration over E or by lower support; the base lattice is a product and the lattice volume of E is 1/l!. There are binom(n,l+1) such E. Smoothness gives signed obstruction (-1)^(2n−1−j−l). Therefore the coefficient of the sum of I(F) over j-faces is

    c_(n,j)=sum_(l=0)^(n−1) (-1)^(2n−1−j−l)
                            binom(n,l+1)binom(j+l+1,j+1).

The n-th finite difference of binom(j+r,j+1), evaluated at r=0, yields c_(n,j)=0 for j<n−1, −1 for j=n−1, and n for j=n. This gives K_D=K_H by a finite combinatorial calculation, independently of identifying the two polynomials by Cayley trick.

## Conversion to the candidate's actual combinatorial models

For generic w inducing a lower regular triangulation T, the minimizing section of Γ_F over each simplex in T|F consists of its barycentric coefficients. Integration of λ_a over a j-simplex of normalized volume V gives V at coordinate a after multiplication by (j+1)!. Thus the gradient of s_I(F) at w is the face's GKZ vector; summing all j-faces gives the candidate's η_(T,j). The gradient of the actual support function (H) is ξ_T=nη_(T,n)−η_(T,n−1). It is the actual minimizing vertex, since an actual polytope's differentiable lower support has that unique minimizer. This is stronger than merely subtracting independently chosen GKZ vertices. Conversely all vertices of K_H occur for some generic w, so K_H=conv{ξ_T:T regular}. The same reasoning on B gives D(P)=conv{sum_k(-1)^(2n−1−k)η_(U,k):U regular}. Accordingly the formula deduction proves the exact candidate polytope equality after the remaining name/identification checks.

## Preliminary adversarial assessment

No genericity or normalization obstruction has emerged when the proof uses independent coefficient parameters and projects polytopes only afterward. Naively applying Theorem 5.10 to F_i=sum_a t_a x^a with identical rows is invalid: for n≥2 the repeated rows force dependent Jacobians, while arbitrary-specialization Part 2 supplies only containment. The cleaned route above avoids that error entirely. Whether to call (H)/(P) an earlier 'pure combinatorial proof' rather than a new deduction from older algebraic-combinatorial machinery requires a separate proof-type and priority qualification. In particular, Theorem 5.10's own proof uses Cayley trick; merely citing it does not amount to a Cayley-free foundational derivation.
