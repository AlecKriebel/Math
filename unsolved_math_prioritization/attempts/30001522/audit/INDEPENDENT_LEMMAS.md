# Independent mathematical cross-checks

These are audit-authored arguments. They supplement the original proof without changing its frozen bytes. They are not additional claims of novelty.

## A. Recovering the tangent characteristic number

Write W = SU(3)/SO(3), with the usual real-matrix inclusion. The homogeneous tangent representation is the action of SO(3) on the five-dimensional space of real symmetric traceless three-by-three matrices, by conjugation. Indeed the Lie algebra decomposition is su(3) = so(3) direct sum i Sym_0(R^3).

For rotations of an oriented coordinate two-plane, this real representation splits into a trivial real line and two oriented two-planes of circle weights one and two. The weight-one plane is spanned by the mixed quadratic terms with the perpendicular coordinate; the weight-two plane is spanned by the traceless quadratic terms within the rotating plane. A generator loop in SO(3) therefore maps into SO(5) with class 1 + 2 = 1 modulo two. The tangent isotropy homomorphism induces the nonzero map on fundamental groups.

The boundary map pi_2(W) -> pi_1(SO(3)) of the principal bundle is an isomorphism Z/2 -> Z/2. Pulling the tangent bundle back along a sphere representing the nonzero element of pi_2(W) thus gives the nontrivial clutching class in pi_1(SO(5)). Its w_2 is nonzero. Hence w_2(W) is the unique nonzero x in H^2(W;F_2).

The integral homology groups of W are Z in degrees zero and five, Z/2 in degree two, and zero otherwise. In the coefficient sequence 0 -> Z/2 -> Z/4 -> Z/2 -> 0, the reduction map H^2(W;Z/4) -> H^2(W;Z/2) is zero. By the universal coefficient theorem these groups are Hom(Z/2,Z/4) and Hom(Z/2,Z/2), and the reduction sends the value two to zero. Exactness makes the connecting homomorphism nonzero on x. This connecting homomorphism is Sq^1. Thus Sq^1(x) is the unique nonzero y in H^3(W;F_2).

Since W is oriented, the standard identity Sq^1(w_2) = w_1 w_2 + w_3 yields w_3(W) = y. Mod-two Poincare duality pairs the one-dimensional H^2 and H^3 nondegenerately, so xy is the nonzero top class and evaluates to one on [W]. This independently recovers the exact tangent characteristic number used by the obstruction and agrees with Debray-Yu's Corollary 4.44 and Proposition 4.45.

## B. Why nonsmooth free involutions cannot escape

If a homeomorphism h of order two has no fixed points, choose U around each point with U intersect h(U) empty. The quotient identifies U homeomorphically with an open chart and makes q:W -> W/<h> a genuine covering. Let N denote the quotient. The two local sheets identify the pullback of N's tangent microbundle with W's tangent microbundle. The Thom-class definition of mod-two Stiefel-Whitney classes is natural, so w_2(W)w_3(W) = q^*(w_2(N)w_3(N)).

The fundamental-class transfer formula q_*[W] = 2[N] = 0 over F_2 contradicts the nonzero pairing. This does not invoke a smooth quotient or require any orientation assumption about N. It is therefore an obstruction to continuous free involutions, and its restriction argument obstructs continuous free actions of every positive-rank torus.

A geometric corroboration is that a double cover supplies an associated real line bundle over N whose disk bundle has boundary W. This explains the nonbounding formulation used in Kuhn-Lloyd, Example 2.25. The direct characteristic-class proof avoids importing the admissibility hypothesis of their surrounding chromatic fixed-point result.

## C. Why a single transgression cannot kill rank-two polynomial cohomology

For an odd prime p and E = (Z/p)^2, H^*(BE;F_p) is a polynomial algebra on two degree-two generators tensored with an exterior algebra on two degree-one generators. A mod-p homology five-sphere has only two nonzero fiber-cohomology rows. Trivial E-action on those rows follows because a p-group has no nontrivial map into F_p^*.

The only possible differential is d_6, and its bottom image is the principal ideal of one degree-six element f. Killing the exterior generators leaves a quotient by zero or by one homogeneous binary cubic. In degree m >= 3, multiplication by a nonzero cubic injects the (m-3)-degree polynomial space, of dimension m-2, into the m-degree space, of dimension m+1. The quotient has dimension three. It therefore has nonzero elements in unbounded degrees even when f has a nontrivial exterior part or a zero polynomial part.

For a free finite action the Borel construction is homotopy equivalent to the quotient topological five-manifold, whose cohomology vanishes above five. This contradiction is independent of a triangulation or a finite CW structure on the quotient. Consequently no rank-two elementary abelian odd-primary group acts freely on W.

## D. Quantifiers and exceptional-prime test

The space W and the circle embedding z -> diag(z,z,z^(-2)) are fixed. For all z simultaneously, a fixed coset implies z in {1,-1}. Consequently each odd finite subgroup acts freely, and this establishes the infinitely-many-primes statement without interchanging a prime-dependent choice of spaces with a fixed-space quantifier. The prime two remains an obstruction to every free torus, even though it is the sole torsion prime in W's homology. Passing to large odd primes cannot remove that integral obstruction from the definition of a free torus action.
