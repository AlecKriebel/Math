# Turn 5: a locally connected example with an explicit positive tensor witness

Substantive author turn **5/5**, for the explicitly infinite-spectrum variant. This turn constructs a MASA whose spectrum is the **Hawaiian earring**, the union of countably many circles of radii1/n tangent at a common point. Its tensor product fails to be maximal abelian for every tensor norm above an explicit threshold. The spectrum is compact, metrizable, path connected and locally connected.

The construction modifies Wassermann's nuclear-ideal/kernel mechanism. A three-involution free-product group gives an explicit algebraic norm gap and a positive kernel witness with detected norm **3−2sqrt(2)>0**. A quotient-constant loop algebra collapses the infinity circle of turn3's mapping torus to one point. An explicit unitary path makes this collapse compatible with the ambient noncommutative quotient; simply collapsing a diagonal subset without that compatibility would not prove the result.

The interval announcement in the source remains credited and unreconstructed. No arbitrary infinite compact realization theorem is obtained. This is the final author turn, not a full classification.

## 1. A free-product seed with a directly proved norm gap

Let G=Z2*Z2*Z2, with involutive generators a,b,c. Its elements are reduced finite words in these three letters with no equal adjacent letters; multiplication cancels adjacent equal letters. Let B=C*_r(G), represented by the left regular unitaries λ_g on H=l²(G), and let ρ_gδ_h=δ_(hg^(−1)) be the commuting right regular representation. The right representation is unitarily equivalent to the left by the inversion unitary, so it is a representation of B.

Put T=λ_a+λ_b+λ_c. The Cayley graph is the3-regular tree. A direct weighted Schur bound gives

                              ||T||<=2sqrt(2).                   (1)

Indeed assign the positive weight w(g)=2^(−|g|/2). At every nonidentity word, one neighboring word has length one less and two have length one more, so the sum of neighboring weights divided by w(g) is sqrt(2)+2/sqrt(2)=2sqrt(2). At the identity it is3/sqrt(2)<=2sqrt(2). The weighted Schur test follows, for finitely supported vectors, from the symmetric inequality

 2|ξ_g ξ_h| <= (w(h)/w(g))|ξ_g|²+(w(g)/w(h))|ξ_h|²

summed over unoriented edges. Density proves (1). Only this upper bound is needed.

In B⊙B consider the self-adjoint element

                       z=λ_a⊗λ_a+λ_b⊗λ_b+λ_c⊗λ_c.

For the faithful spatial representation on l²(G×G), the unitary δ_g⊗δ_h↦δ_g⊗δ_(g^(−1)h) conjugates simultaneous left translation to translation on the first coordinate. Thus

                              ||z||_min=||T||<=2sqrt(2).          (2)

The commuting left/right representation Π_B of the maximal tensor product satisfies Π_B(z)δ_e=3δ_e and ||Π_B(z)||<=3, so ||Π_B(z)||=3. Consequently Π_B is not minimal-norm continuous; if it were, its induced *-representation would be contractive, contradicting (2). This argument proves the required nonminimality directly, instead of importing a free-group nonamenability criterion.

## 2. The compact-ideal MASA and an explicit unitary path

Define A_0=B+K(H) and D_0=c0(G)+C1, represented as diagonal operators. The intersection B∩K(H) is zero. To check this, distinct right translations ρ_(g_n) converge weakly to zero on l²(G), by approximation with finitely supported vectors. If k in B were compact, its commutation with all right translations would give

 ||kδ_e||=||kρ_(g_n)δ_e||→0.

Thus kδ_e=0, and commutation with the right representation gives k=0 on the entire canonical basis. The quotient map q:A_0→B therefore has kernel K(H) and splits by the original inclusion of B. The sum A_0 is closed, since its image in the Calkin algebra is the closed faithful image of B.

The diagonal compression of each nonidentity λ_g is zero, while that of1 is1; by norm continuity diagonal compression sends B to the scalars. It sends compact operators to c0(G). An operator in A_0 commuting with all rank-one coordinate projections must be diagonal, so this proves D_0'∩A_0=D_0. Thus D_0 is a MASA with spectrum S=G∪{infinity}, the one-point compactification of the countable discrete set G. These arguments are the credited source pattern, with its analytic nonminimality input replaced by §1's explicit tree estimate.

Let U=λ_a λ_b. Its permutation of G, g↦abg, has only infinite orbits, because ab has infinite order. Unlike a single generator of the torsion-free source group, U has an explicit path to1 inside B. For s=a,b let P_s=(1−λ_s)/2, a projection, and define

             v_t=exp(iπtP_a)exp(iπtP_b),  0<=t<=1.               (3)

This is norm continuous, v_0=1 and v_1=U. No stable-rank theorem, K-theory vanishing argument or stabilization is required.

## 3. A quotient-constant twisted loop algebra

Let θ=Ad(U) and define A to consist of the functions F in C([0,1],A_0) such that

 F(1)=U F(0) U*,
 q(F(t))=v_t b v_t* for one fixed b in B and all t.                (4)

The first condition is closed; the second asks that the continuous quotient-valued function belong to the isometric image of the *-homomorphism b↦(v_t b v_t*)_t. Thus A is a closed unital C*-algebra. The map Q:A→B taking F to b=q(F(0)) is a surjective unital *-homomorphism with the *-homomorphic splitting

                           j(b)(t)=v_t b v_t*.                   (5)

Its kernel I is the twisted continuous K(H)-valued loop algebra. Conjugation F(t)↦v_t*F(t)v_t untwists the endpoint condition, giving

                            I≅C(S1,K(H)).                       (6)

In particular I is nuclear, by the nuclearity of K(H) and of the commutative circle algebra. These are classical C*-tensor facts already used in the source mechanism.

Let

                       D=A∩C([0,1],D_0).                        (7)

For a D_0-valued section, q(F(t)) is scalar. Condition(4), at t=0 and then at every t, says precisely that this scalar is constant. Hence D consists of the twisted diagonal loops whose infinity value is constant along the interval. It is abelian and unital, and

                               D⊂I+C1.                          (8)

To verify maximality, suppose H in A commutes with D. For any interior t and any rank-one diagonal projection e_g, choose a scalar bump supported inside(0,1), equal to1 at t. The section bump times e_g lies in D and in I. Thus H(t) commutes with every e_g and is diagonal. Since H(t) lies in A_0, §2 gives H(t) in D_0. Continuity handles both endpoints, proving H in D. The smaller ideal in (6) is nuclear; we are not claiming that it contains a localized copy of the nonnuclear source tensor product from turn3.

## 4. The positive tensor witness and all larger norms

In A⊙A form

 Z=j(λ_a)⊗j(λ_a)+j(λ_b)⊗j(λ_b)+j(λ_c)⊗j(λ_c).

The split inclusion j preserves the minimal tensor norm, so ||Z||_min<=2sqrt(2). The representation Π=Π_B∘(Q⊙Q) of A⊙A extends to its maximal completion and satisfies Π(Z)δ_e=3δ_e. Since Z is a sum of three self-adjoint unitaries, ||Z||_max<=3.

Use continuous functional calculus in the maximal completion to define

                           X=(Z−2sqrt(2)1)_+.                    (9)

The canonical minimal quotient sends X to zero by (2). On the other hand

                       Π(X)δ_e=(3−2sqrt(2))δ_e.                 (10)

Therefore X is a nonzero positive element, and in fact ||X||_max=3−2sqrt(2): the upper bound follows from the maximal spectral bound3, and (10) gives the matching lower bound. This is an explicit functional-calculus certificate; a finite matrix simulation cannot replace it.

We now check its commutation, rather than assume that a tensor-norm gap suffices. The maximal-to-minimal quotient is isometric on I⊗_max A and A⊗_max I. Indeed ideals embed isometrically in maximal tensor products by turn3's representation-extension proof, and I is nuclear by (6), so these restricted maximal norms are the corresponding minimal norms. Multiplying an element of the minimal kernel on either side by i⊗1 or1⊗i lies in those ideal completions. Its image is zero, so isometry forces the product to be zero. Thus X annihilates I on both tensor legs. By (8), X commutes with D⊗1 and1⊗D, hence with D⊗D.

Set

                     ||w||_α=max{||w||_min,||Π(w)||}.             (11)

It is a C*-crossnorm for the same reason as the earlier thresholds. For every β>=α, let X_β be the image of X in A⊗_β A. Representation Π factors through that completion, so (10) guarantees X_β≠0. Its minimal image is zero and it commutes with D⊗D. The minimal quotient is faithful on the abelian tensor algebra D⊗D, so X_β lies outside it. This proves the source pathology for every β>=α, including max. The detected lower bound3−2sqrt(2) survives every such quotient.

## 5. The exact spectrum is the Hawaiian earring

Let σ(g)=abg on G and σ(infinity)=infinity. Without the constant-infinity condition, the diagonal mapping-torus spectrum would be

 Y=(S×[0,1])/((s,1)~(σ^(−1)(s),0)),

as in turn3. The extra condition in (4)–(7) restricts to functions constant on the infinity circle. Therefore the spectrum of D is the compact Hausdorff quotient Y' obtained by collapsing that entire closed circle to one point o.

The open complement Y'\{o} is the topological disjoint union of the suspensions of the σ-orbits in G. Each orbit is indexed by Z, so each such suspension is a copy of R. There are countably infinitely many orbits. For an explicit infinite family of different orbits, use g_n=(ca)^n, n>=1. If (ab)^k g_n=g_m and k≠0, the reduced word on the left starts in a or b, with no cancellation at the following c, while g_m starts in c. Hence k=0 and then n=m. Countability follows from countability of G.

Consequently Y' is the one-point compactification of a countable disjoint union of real lines. This identifies it with the Hawaiian earring

 H=union_(n>=1){(x,y):(x−1/n)²+y²=1/n²} ⊂ R².                  (12)

For completeness, H is compact: the circles shrink to the common point(0,0), so every sequence on circles of unbounded index converges to that point, while the remaining subsequences lie in a finite union of compact circles. Removing that point leaves a topological disjoint union of countably many open circle-arcs, each homeomorphic to R. Each component is open in the complement; away from the common point only finitely many circles can approach a given small neighborhood. Thus H is also the one-point compactification of that same locally compact disjoint union. Uniqueness of one-point compactification gives Y'≅H.

Every circle meets the common point, so H is path connected. At a noncommon point it has small interval neighborhoods. At the common point, intersection with a sufficiently small Euclidean ball consists of whole small circles and arcs through the common point from the remaining circles; this intersection is connected and path connected. These ball intersections give a neighborhood basis, proving local connectedness there as well. Thus the result adds a locally connected compact metrizable example, unlike simply asserting extra regularity of turn3's mapping torus.

By the cone construction of turn4, the cone over H is also a realized spectrum. Its explicit radial contraction makes it contractible. It is locally connected: away from the apex use local products of locally connected spaces, and at the apex use the connected truncated-cone neighborhoods. This supplies a locally connected, contractible realized compact space, without identifying it with a ball or interval.

## 6. Final scope and remaining obstruction

The five turns establish the literal finite-space negative answer and several positive infinite families, culminating in (12) with the explicit norm-gap certificate. They do not classify all infinite compact Hausdorff spaces. In particular the general transfer from a continuous image, quotient or closed retract of a realized spectrum to that prescribed spectrum is unproved; turn4 explains why an unrestricted version is false. The primary report's interval realization is an attributed announcement, not a newly proved theorem here.

The quotient-constant condition in (4) works because the twisting unitary has the explicit path (3). It preserves a noncommutative split quotient and a nuclear ideal while collapsing exactly the diagonal infinity circle. This verified construction must not be extrapolated to arbitrary identifications of the spectrum or arbitrary spaces. No counterexample among infinite compact Hausdorff spaces has been obtained.

Final proposed substantive disposition: **infinite-spectrum variant unresolved5/5**, with the literal finite obstruction displayed separately. The source, classical ingredients and Wassermann's mechanism retain credit; no novelty certification is asserted. This completes the author budget. Full independent review, not a sixth research turn, is the next step.
