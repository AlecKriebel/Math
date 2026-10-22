# Finite Brauer compatibility criterion for a fixed Enriques K3 cover

## Audit outcome and scope

The fixed-cover conditional criterion is mathematically valid under its stated hypotheses. No fatal defect was found in the quotient, global character, local difference characters, support argument, or exact binary test. The expanded proof below makes the hypotheses and the distinction between full and algebraic Brauer orthogonality explicit.

This is a structural characterization after local liftability to a specified cover is known. It is not an unconditional lifting theorem, a computation of the necessary arithmetic data, or a novelty claim. In particular it does not overturn the negative lifting examples already reported in the original AIM question.

The target identifier is 20000440 / AIM-ALGEBRAIC_NUMBER_THEORY-0092. The reviewed argument section has 2,937 bytes and SHA256 6b262e024bb59c3e62bdf094b412835cee3828afa555a706b4b6b0e6312f2aad. Its identity was rechecked without changing the input. The complete expanded proof and its acceptance boundary are given below.

## Definitions and exact statement

Let K be a number field, let X/K be a smooth projective geometrically integral Enriques surface, and let

    p : Y → X

be a fixed finite étale morphism of degree two, with Y a smooth projective geometrically integral K3 surface. Write ι for its deck involution, defined over K. In characteristic zero this cover is a torsor under the constant group of order two. This statement concerns this particular K-form of the covering surface and map.

For a smooth variety Z, use the cohomological Brauer group Br(Z), and write

    Br₀(Z) = image[Br(K) → Br(Z)],
    Br₁(Z) = kernel[Br(Z) → Br(Z ×K K̄)].

The image notation is important: no injectivity of Br(K) → Br(Z) is being presumed.

Let m = (mᵥ) be an adelic point of X such that

    Σᵥ invᵥ β(mᵥ) = 0    for every β ∈ Br(X).

Assume, separately, that p⁻¹(mᵥ)(Kᵥ) is nonempty at every place v of K. Choose Pᵥ in this fiber. Let A be either Br(Y) or Br₁(Y), and set

    D = Br₀(Y) + (A ∩ image[p* : Br(X) → Br(Y)]),
    B = A/D,
    B∨ = Hom(B, Q/Z).

Then B is a finite abelian group. For b ∈ B, choose any representative α ∈ A and define

    c(b) = Σᵥ invᵥ α(Pᵥ),
    dᵥ(b) = invᵥ α(ιPᵥ) − invᵥ α(Pᵥ).

Both definitions are independent of α; c and dᵥ belong to B∨. There is a finite set S of places, containing the archimedean places, for which dᵥ = 0 whenever v is outside S. The global evaluation characters attained by all adelic lifts of m to Y are exactly

    C(m,p,A) = {c + Σᵥ∈S εᵥdᵥ : εᵥ ∈ {0,1}}.

Consequently,

    m ∈ p(Y(AK)^A)   if and only if   0 ∈ C(m,p,A).

Here Y(AK)^A denotes orthogonality to all classes in A. When A = Br₁(Y), this is algebraic Brauer orthogonality only. When A = Br(Y), it is full Brauer orthogonality.

## Proof

### The denominator is a subgroup of A

In both cases Br₀(Y) is contained in A. The intersection in the definition of D is an intersection of subgroups of Br(Y), so D is a subgroup of A and the quotient is defined.

In fact Br₀(Y) is already contained in p*Br(X): the structural morphism Y → Spec K factors through X, and pullback of the constant class on X associated to γ ∈ Br(K) is exactly its constant class on Y. Thus the displayed Br₀ summand is redundant but harmless. It is useful for exhibiting finiteness and reciprocity explicitly.

For the algebraic choice of A, one must retain the intersection with p*Br(X). The argument does not assume that every pullback from Br(X) is algebraic, nor replace that intersection without proof by p*Br₁(X). It also does not assume that p* is injective.

### Finiteness

Skorobogatov–Zarhin, Theorem 1.2, applies to a K3 surface over any field finitely generated over Q. It proves finiteness of both the Galois-invariant geometric Brauer group and Br(Y)/Br₀(Y). The field K here is a number field, so its hypothesis holds. Neither a K-rational point on Y nor an unproved Tate conjecture is an additional hypothesis. See [SZ], physical and printed p.2.

The inclusion A ⊂ Br(Y) induces an injection

    A/Br₀(Y) → Br(Y)/Br₀(Y).

The left side is therefore finite. Since B is a quotient of it, B is finite in either case. Hence B∨ is finite as well. No finiteness assertion about the possibly infinite group Br₀(Y), or about Br(X)/Br₀(X), is used.

### Local choices form an adelic point

Because p is an étale cover of degree two, its fiber over mᵥ is a reduced degree-two finite Kᵥ-scheme. The assumed Kᵥ-point forces the fiber to split into two Kᵥ-points. They are precisely Pᵥ and ιPᵥ, and are distinct.

Every family of Kᵥ-points on the proper variety Y is an adelic point. To see the restricted-product condition directly, spread Y to a proper model over the integers of K with finitely many primes removed. At every remaining finite place, the valuative criterion of properness extends every Kᵥ-point to an Oᵥ-point of this model. Therefore P = (Pᵥ) is adelic, and so is any family obtained by switching any collection of its components, even infinitely many of them.

### The Brauer sums are defined

For every α ∈ Br(Y), there is a finite set of places outside which α evaluates to zero at every Kᵥ-point of Y. Indeed, enlarge the finite set used for a proper smooth integral model so that α extends to its Brauer group. A concrete justification for this spreading step is to choose an integer n annihilating α, lift α through the Kummer sequence to an étale H² class with coefficients μₙ, invert n, and spread the class over a sufficiently small open subset of Spec O_K.

At each remaining finite place, evaluation at an integral point lands in Br(Oᵥ). This group is zero for a henselian discrete valuation ring with finite residue field. Thus the local invariant is zero. Archimedean places can all be included in the exceptional set.

It follows that every sum in the definition of c, and every global evaluation sum for any other adelic lift, has only finitely many nonzero terms. This paragraph uses the usual spreading, properness, and unramified local Brauer facts; it makes no computational claim about locating an exceptional set.

### Descent of the global character

Let γ ∈ Br(K). Evaluation of its image in Br₀(Y) at Pᵥ is its restriction to Br(Kᵥ). Global reciprocity gives

    Σᵥ invᵥ γ|Kᵥ = 0.

If δ = p*β belongs to A, with β ∈ Br(X), functoriality of evaluation gives

    δ(Pᵥ) = β(p(Pᵥ)) = β(mᵥ).

The sum of the invariants is zero because m is orthogonal to Br(X). Therefore the global evaluation at P annihilates D. Additivity of evaluation and of the invariant maps gives a well-defined homomorphism c : B → Q/Z.

Exactly the same reasoning shows that the global evaluation at every adelic lift Q of m annihilates D. Thus it makes sense to compare all such evaluations as elements of the one fixed finite group B∨.

### Descent of the local difference characters

For a constant class, the evaluations at Pᵥ and ιPᵥ coincide, so their difference is zero. For δ = p*β in A, both evaluations equal β(mᵥ), because p ∘ ι = p. Thus dᵥ annihilates D at each place individually, and additivity gives dᵥ ∈ B∨.

This does not assert that the individual function b ↦ invᵥ α(Pᵥ) is well-defined on B. That individual evaluation can change when a representative is altered by a constant or pullback. Only the global sum and the difference between the two local lifts descend as asserted.

### One finite support set suffices

Choose elements b₁,…,bᵣ generating the finite group B and representatives α₁,…,αᵣ in A. Apply the preceding spreading argument simultaneously to this finite list. It supplies a finite set S such that, for every v outside S and every R ∈ Y(Kᵥ),

    invᵥ αⱼ(R) = 0    for all j.

In particular dᵥ(bⱼ) = 0 for every generator. Because dᵥ is a homomorphism, dᵥ = 0 on all of B.

The support set is uniform for these representatives and all local points. It need not make every representative of every class of B evaluate to zero outside S: one may add global constant Brauer classes with ramification at other places. Such constants nevertheless cancel in dᵥ and in the global sum, which is precisely why the quotient argument works.

### Exactness of the binary test

Let Q be any adelic lift of m. At every place, the two-point fiber description provides εᵥ ∈ {0,1} such that Qᵥ = ι^εᵥPᵥ. For every α ∈ A,

    Σᵥ invᵥ α(Qᵥ)
      = Σᵥ invᵥ α(Pᵥ)
        + Σᵥ [invᵥ α(Qᵥ) − invᵥ α(Pᵥ)]
      = c([α]) + Σᵥ∈S εᵥdᵥ([α]).

The sums are justified by the previous finite-support arguments. Hence every attainable character lies in the displayed set C(m,p,A).

Conversely, given any binary vector (εᵥ) for v in S, define Qᵥ = ι^εᵥPᵥ on S and Qᵥ = Pᵥ elsewhere. This is an adelic point of Y and lifts m. Its global evaluation character is the specified element of C(m,p,A). Thus no additional compatibility condition among the binary choices is missing.

An adelic lift is orthogonal to A exactly when its descended character vanishes on B: it already annihilates D, and B = A/D. This proves the stated equivalence.

### Invariance under the choices

Changing representatives of b₁,…,bᵣ does not change c or dᵥ, by their established descent. Changing the generating set changes only a presentation of the same characters. Enlarging S adds only zero dᵥ terms and does not change the attainable set.

For the base lifts, suppose first that Pᵥ is switched at one place w. Then

    c′ = c + d_w,
    d′_w = −d_w,
    d′_v = d_v  for v ≠ w.

The terms at w become c + d_w − ε_wd_w, which correspond to the old choices with coefficient 1 − ε_w. Hence the attainable set is unchanged.

More generally, let P′ be any other system of base lifts, with switching indicators ηᵥ ∈ {0,1}. The common support construction works for all local points, so it also works for P′. Then

    c′ = c + Σᵥ∈S ηᵥdᵥ,
    d′_v = (−1)^ηᵥdᵥ.

For each v, ηᵥ + (−1)^ηᵥεᵥ is either εᵥ or 1 − εᵥ. Thus these formulas simply permute the binary choices, even if the original systems differ at infinitely many places. The criterion is intrinsic to m, p, and A. This completes the proof.

## Consequences and limits

If B = 0, every adelic lift already known to exist is A-orthogonal. If A = Br₁(Y), this statement must not be strengthened to full Brauer orthogonality without controlling the remaining classes.

The attainable set is generally a translated binary subset-sum set. Replacing it by a subgroup generated by the dᵥ loses information. For example, in a group identified with Z/3, take c = 1 and a single d = 1. The attainable values are {1,2}, whereas c + ⟨d⟩ is the whole group and contains zero. This is an abstract algebraic illustration, not a claim that the data arise from a specified surface. If all dᵥ have order dividing two, the binary sum set does equal their generated subgroup, but that extra condition was not assumed.

The criterion becomes a finite computation once a presentation of B, a certified finite support set S, and the exact values of c and dᵥ on generators are supplied. It gives neither an algorithm for producing all those inputs nor an algorithm for an arbitrary adelic point represented without effective local data.

Local liftability is an independent hypothesis of this fixed-cover theorem. A quadratic twist changes the K-form of the cover. To obtain a lift of the same m to a global twist, its one global twisting class must have the required localization at every place; arbitrary independent local twists are not a single global object. Binary switching within a split fiber never repairs a nonsplit fiber of the fixed cover.

## An additional transfer consistency check

The standard Brauer corestriction for the finite étale double cover satisfies

    p* cor_p(α) = α + ι*α.

Both choices of A are stable under ι*. Consequently this sum lies in D for α ∈ A, and ι* acts by −1 on B. Evaluate the identity along P and use the Brauer orthogonality of m. It gives

    Σᵥ invᵥ α(ιPᵥ) = −Σᵥ invᵥ α(Pᵥ),
    Σᵥ∈S dᵥ = −2c   in B∨.

Thus complementing every binary choice negates its attainable character. This is a useful necessary consistency check for proposed arithmetic input data; it is not needed to prove the criterion. The Z/3 illustration above satisfies it, since 1 = −2 modulo 3.

## Relation to the established negative examples

AIM Question 8 asks for lifting assumptions and already contains a 25 September 2004 update reporting failure of unconditional Brauer-compatible lifting. The present conditional criterion does not assert that zero must belong to the finite attainable set. See [AIM], p.48.

Harari–Skorobogatov Proposition 1.6 concerns a union over global twists; for a universal torsor its terms use Br₁. Their Example 3 constructs an extension of Z/2 by a torus, without generally asserting a split extension. These statements cannot be replaced by a single fixed-cover, full-Brauer identity. See [HS], pp.8–10.

Their explicit example also illustrates how the finite test can fail despite existing local lifts. For the parameters a = 5, b = 13, c = 2, their class α = (y,5) is algebraic, invariant under the covering involution, and has nonzero global evaluation on the chosen adelic lift. In the present notation every dᵥ([α]) is zero while c([α]) is nonzero. No binary switch can remove that obstruction. This is their established example, not a new construction. See [HS], Proposition 2.6(ii), Theorem 2.10, and p.22.

## Acceptance boundary

Accepted: the exact finite-character criterion, with both choices of A, finite support, both directions of the existence equivalence, and invariance under arbitrary changes of base lifts.

No substantive correction to the frozen mathematical statement is required. The expansions above are recommended for a standalone version: spell out the image in the denominator, the hypotheses of the finiteness theorem, the role of properness, the distinction between local evaluations and descended differences, and the algebraic versus full meaning of compatibility.

Not established: universal existence of a compatible lift; automatic local liftability to the selected cover; a uniform effective algorithm; identification of fixed-cover lifting with a union over twists; a general semidirect-product assertion; or a new solution of the broader original AIM question. The original lead and the cited literature receive no novelty claim here.

## Public sources and version pins

[AIM] American Institute of Mathematics, Rational and integral points on higher dimensional varieties, version 22 November 2004, Question 8 and its dated update, physical and printed p.48. Public PDF: https://aimath.org/WWN/qptsurface2/qptsurface2.pdf . Inspected PDF: 502,057 bytes; SHA256 8b64d2f6b91f791c35afae10b2ef79c15a927a94c2142a56386f80c8b8a596e6.

[SZ] Alexei N. Skorobogatov and Yuri G. Zarhin, A finiteness theorem for the Brauer group of abelian varieties and K3 surfaces, arXiv:math/0605351v4, 5 November 2007, Theorem 1.2 and Remark 1.3, physical and printed p.2. Version page: https://arxiv.org/abs/math/0605351v4 . Captured PDF endpoint: https://arxiv.org/pdf/math/0605351 . Inspected PDF: 272,701 bytes; SHA256 631be3a8139ac7e392795073a513085845739a755f71528a4732e9b143181ecd.

[HS] David Harari and Alexei Skorobogatov, Non-abelian descent and the arithmetic of Enriques surfaces, author-hosted paper, Example 3, Proposition 1.6, Proposition 2.6(ii), Theorems 2.9–2.10, Proposition 2.11 and the alternative argument on p.22. Public PDF: https://www.ma.imperial.ac.uk/~anskor/HS.PDF . Inspected PDF: 188,257 bytes; SHA256 ecae938d433cde7eb9c6c0d7725bc5a2f57d8dbdfa4b3f919c6292f1d4099966.
