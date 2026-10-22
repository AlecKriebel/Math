# A finite-image criterion and its mapping-class application

## 1. Conventions and statement

Let S_g be a closed connected oriented surface of genus g>=2. Write G=Mod_g for its orientation-preserving mapping class group and C_g for the ordinary complex of essential simple closed curves, with disjointness simplices. Set

    D_Z = H_(2g-2)(C_g; Z),       D = D_Z tensor_Z Q,
    d = 4g-5,                   q = 2g-1.

Reduced and unreduced homology agree here because 2g-2>0. Coefficient actions are the natural left actions. A tensor product of two left G-modules below always has the diagonal action. The dual of a vector space means its full algebraic dual, not a restricted dual.

**Theorem.** For every g>=2 and every torsion-free finite-index Gamma<=G, H^d(Gamma;D_Z) has infinite rational rank. In particular H^3(Gamma;H_2(C_2;Z)) is not finitely generated for every such subgroup of Mod_2.

This is a corollary of the established duality theorem and the finite-image quotient theorem explicitly credited below. It is not an assertion that the requested H^q has infinite rank for g>=3.

## 2. Exact imported results

**Input H (Harer/Bieri–Eckmann).** Gamma has a finite classifying-space model and is an integral duality group of dimension d with dualizing module D_Z. With the usual conversion of the dualizing right module to a left module by inversion, the duality formula is

    H^j(Gamma;A) = H_(d-j)(Gamma;D_Z tensor_Z A)

for every left ZGamma-module A; the action on the right is diagonal. In particular

    H^d(Gamma;D) = H_0(Gamma;D tensor_Q D).

A primary account of the general coefficient formula is Church–Farb–Putman, *The rational cohomology of the mapping class group vanishes in its virtual cohomological dimension*, §2, which credits Harer's theorem and Bieri–Eckmann. Its construction uses the contractible thick Teichmüller manifold with corners and compact quotient. Restricting to a torsion-free finite-index subgroup produces the finite classifying space. The action is orientation preserving: Teichmüller space is complex and G acts holomorphically. No additional orientation character is being discarded.

**Input FP (Fullarton–Putman).** For every g>=2 and every prime p, there is a G-equivariant surjection

    psi_p: D -> V_p = St^ns_(2g)(F_p)

where V_p is a finite-dimensional vector space OVER Q, not over F_p. The G-action factors through the finite group Sp_(2g)(F_p), and

    dim_Q V_p = |Sp_(2g)(F_p)| / [g (p^(2g)-1)]
              = (1/g) p^(g^2) product_(i=1 to g-1)(p^(2i)-1).

These are Proposition 3.10, Proposition 3.11, and the equivariance paragraph immediately before Proposition 3.10 in the inspected 29 November 2017 author version of *The high-dimensional cohomology of the moduli space of curves with level structures* (published JEMS 22 (2020), 1261–1287). In Proposition 3.10 take the level parameter ell=p. This does not impose Gamma<=Mod_g(p): the map is equivariant under the WHOLE G and may be restricted to any subgroup. V_p is the quotient of the special-linear building's rational Steinberg module by separated apartments. It is not the symplectic Steinberg representation. Neither its irreducibility nor the nonvanishing of a map to a symplectic Steinberg representation is assumed.

For fixed g, the displayed positive polynomial tends to infinity with p. There are arbitrarily large primes. Consequently dim_Q V_p is unbounded. The proof below uses only that conclusion and finite image, not the precise dimension formula.

## 3. Elementary finite-rank lemmas

For a bilinear form B on a Q-vector space M, define T_B:M->M* by T_B(x)(y)=B(x,y), and rank(B)=dim im(T_B). This rank is allowed to be infinite.

**Lemma 1.** If B_1,...,B_r have finite rank and a_1,...,a_r are rational numbers, then

    rank(sum_i a_i B_i) <= sum_i rank(B_i).

**Proof.** The image of the sum of the linear maps a_i T_(B_i) is contained in the sum of their images. A sum of finite-dimensional subspaces has dimension at most the sum of their dimensions. This proof does not require M to be finite-dimensional. QED.

**Lemma 2.** If a set of finite-rank bilinear forms has unbounded ranks, its linear span is infinite-dimensional.

**Proof.** If its span were finite-dimensional, choose a finite basis from that set. Lemma 1 bounds the rank of every member of the span by the sum of the finitely many basis ranks, contradicting unboundedness. Equivalently, greedily choose a next form with rank greater than the sum of all previous ranks; it cannot be a linear combination of the previous forms. This constructs arbitrarily long independent families. QED.

**Lemma 3.** Let pi:M->V be a surjective linear map onto a finite-dimensional Q-vector space with a nondegenerate bilinear form b. The pullback B(x,y)=b(pi(x),pi(y)) has rank dim(V).

**Proof.** In terms of linear maps, T_B=pi* circ T_b circ pi. The map pi* is injective, since a functional on V vanishing on the surjective image of pi is zero; T_b is an isomorphism by nondegeneracy; and pi is surjective. Thus im(T_B)=pi*(V*) has dimension dim(V). QED.

**Lemma 4.** Every finite-dimensional rational representation V of a finite group F admits an F-invariant nondegenerate symmetric bilinear form over Q.

**Proof.** Choose a rational basis and its dot product b_0. Define

    b(v,w) = sum_(f in F) b_0(fv,fw).

The matrices of the action and b have rational entries. Right multiplication by any fixed element of F permutes the terms, proving invariance. Embed Q into R. If v is a nonzero rational vector, every summand b_0(fv,fv) is positive, so b(v,v)>0. In particular, no nonzero rational vector lies in the radical. Hence b is nondegenerate. The same expression is positive definite after real extension. No division by |F| or irreducible decomposition is required. QED.

## 4. Finite-image quotient criterion

**Proposition.** Suppose a QG-module M has finite-dimensional, finite-image G-module quotients pi_i:M->V_i of unbounded rational dimensions. Then for EVERY subgroup L<=G,

    (M tensor_Q M)_L

is infinite-dimensional.

**Proof.** For each i choose the form b_i supplied by Lemma 4 for the finite image of G on V_i, and pull it back to B_i on M. Lemma 3 gives rank(B_i)=dim(V_i). Equivariance of pi_i and invariance of b_i imply

    B_i(gx,gy)=B_i(x,y)  for all g in G.

Thus the functional on M tensor M induced by B_i annihilates every relation gx tensor gy - x tensor y. It descends to a linear functional on the G-coinvariants and on the L-coinvariants. The ranks are unbounded, so Lemma 2 makes the B_i span an infinite-dimensional space of forms. The map from functionals on (M tensor M)_L to bilinear forms on M is injective: elementary tensors span the tensor product, whose quotient map is surjective. Therefore the dual of (M tensor M)_L is infinite-dimensional. The dual of a finite-dimensional vector space is finite-dimensional, so (M tensor M)_L itself is infinite-dimensional. QED.

An explicit finite witness is available for each desired lower bound N: choose i_1,...,i_N greedily with dim(V_(i_j)) greater than the sum of the previous dimensions. The N resulting functionals are independent. If the coinvariants had dimension smaller than N, they could not have N independent linear functionals. This argument establishes arbitrary finite lower bounds without identifying a basis of an infinite-dimensional dual.

## 5. Mapping-class application and integral conclusion

Apply the proposition to M=D using Input FP and L=Gamma. Input H identifies the resulting infinite-dimensional coinvariant vector space with H^d(Gamma;D).

It remains to connect this with the integral cohomology asked about. Let X be a finite CW classifying space for Gamma and let P_* be the finite-rank free ZGamma cellular resolution supplied by its contractible universal cover. For every j,

    Hom_(ZGamma)(P_j,D_Z) tensor_Z Q
      = Hom_(ZGamma)(P_j,D_Z tensor_Z Q),

because P_j is finite-rank free. These identifications commute with differentials. Tensoring with Q is exact, so taking cohomology gives

    H^j(Gamma;D_Z) tensor_Z Q = H^j(Gamma;D).

The rational vector space in degree d is infinite-dimensional. A finitely generated abelian group has finite-dimensional rationalization, so H^d(Gamma;D_Z) is not finitely generated. In fact its rational rank is infinite. This completes the theorem.

Finally d-q=(4g-5)-(2g-1)=2g-4. It is zero precisely when g=2 in the range g>=2. Thus the theorem answers the original degree in genus two, and only that genus. For g>=3, Input H instead identifies the target rational group with H_(2g-4)(Gamma;D tensor D). Section 4 proves a result about H_0, not about this positive homological degree. The distinction is essential; an explicit countermodel to that inference appears in Approach 3.

## 6. Dependence and status

The proof's deep inputs are published, pre-existing theorems. Fullarton–Putman's quotient construction and dimension calculation are not reproved here. The bilinear-form argument is elementary and may be standard or implicit in earlier work; no novelty claim is made. The result is an authored corollary, not an assertion that Fullarton–Putman explicitly states this exact genus-two answer. Nothing in this proof uses the unrefereed Avramidi small-model argument or a positive-genus conclusion imported from a finite computation.
