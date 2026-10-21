# Pencil-integral differentials: exact construction and cover audit

20 October 2026. Authored mathematical analysis for the genuine Question 1 in Garcia-Fritz's OWR49/2016 contribution, printed p. 2841. All varieties and differentials below are over **C**. This is a sufficient family and an obstruction audit, not a general solution or a novelty claim.

## Findings

1. A rational pencil of plane curves provides a nonzero branch-integral 1-form with explicit twist. Its saturated form has **exactly** the pencil-fiber components as integral curves. Products give symmetric forms with completely determined integral curves.
2. The number of selected branch fibers does not increase the twist. However, increasing this number creates multiple intersections at the pencil basepoints. Branch degree alone therefore does not justify an anti-ample twist on a resolution.
3. There is a clean smooth, **generically finite** family over P²: resolve a Lefschetz pencil and base-change it by a high-genus curve. Its pulled-back pencil form saturates to a differential twisted by the inverse canonical bundle of the new base curve. This proves a complete genus-bounded classification in that family.
4. Already for a pencil of lines, every nontrivial connected **normal finite** cover of P² branched only along those lines is singular over the common center. Thus there is no smooth finite-cover version of that simplest pencil example. A proof is given below.

## 1. The plane pencil construction

Let P,Q be coprime homogeneous polynomials of the same degree d≥1. Set

    f=[P:Q]:P² ⇢ P¹,       ω=Q dP−P dQ.

The coefficients of ω are homogeneous of degree 2d−1, and contraction with the Euler vector field is zero. The Euler sequence consequently gives

    0 ≠ ω ∈ H⁰(P², Ω¹_P²(2d)).

Nonvanishing also follows from ω=Q²d(P/Q) away from Q=0 and the characteristic-zero fact that a nonconstant rational function has nonzero differential.

Let G be the homogeneous gcd of the three coefficients of ω, let s=deg G, and put

    ω̄=ω/G,       k=2d−s.

Then ω̄ is a nonzero section of Ω¹_P²(k), with no divisorial zero. This k is the twist of this **saturated pencil differential**. It is not asserted to minimize twist among every possible symmetric differential making a prescribed branch arrangement integral. In particular k≥2, because H⁰(P²,Ω¹(k))=0 for k≤1.

### Proposition 1: exact integral-curve classification

An irreducible reduced plane curve D is ω̄-integral if and only if D is an irreducible component of a fiber of f. Consequently every reduced divisor supported on any finite selection of pencil fibers is ω̄-integral component by component.

Here integrality means that pullback to the normalization of D, followed by the map to its cotangent line bundle, is zero. It does not mean that the coefficient vector vanishes on D.

**Proof.** Work at the generic point of D; the pencil is defined there because P and Q have no common curve component. If f varies on D, the restriction of df to its function field is nonzero. Therefore df has no common divisorial factor along D and the restriction of ω̄ is nonzero.

If f is constant, use a target coordinate in which its value is a finite number a and write

    f−a=u^m v,

where u is a local equation of D and v is a unit at its generic point. Then

    df=u^(m−1)(m v du+u dv).

The expression in parentheses has a nonzero normal coefficient along D, so the common vanishing order is exactly m−1. After removing it, the restriction to the tangent direction of D is zero. This also handles components of Q=0 after replacing f by 1/f. Thus saturation preserves integrality of every fiber component, including multiple components. ∎

The same proof identifies G up to a nonzero scalar: it is the product of H^(m_H−1), over the irreducible components H appearing with multiplicity m_H>1 in pencil fibers. There are finitely many such components because G is a polynomial. No extra curve becomes integral merely because the unsaturated coefficients vanished there.

The assertion is parametric completeness, not finiteness: a pencil has infinitely many integral curves. A large branch divisor does not imply that all these curves have low genus, or that their inverse images do.

### Proposition 2: products of pencils

For pencils [P_i:Q_i] of degrees d_i, let G_i be their coefficient gcds and let η_i=(Q_i dP_i−P_i dQ_i)/G_i. For r≥1, their symmetric product satisfies

    η=η_1⋯η_r ∈ H⁰(P², SymʳΩ¹_P²(k)),
    k=Σ_i(2d_i−deg G_i),        η≠0.

Its integral curves are exactly the irreducible curves that are fiber components of at least one of the r pencils.

**Proof.** On a curve normalization every η_i pulls back to a section of a line bundle. At the generic point their product is zero precisely when at least one factor is zero. Proposition 1 applies. The product has no divisorial zero: over the residue field of any prime divisor, the symmetric algebra of the cotangent fiber is a polynomial ring, hence a domain. The product of the nonzero reductions of primitive factors stays nonzero. ∎

This formula includes repeated pencils. The symmetric order is r, not the number of selected branch fibers. It does not classify arbitrary low-genus curves until an upstairs degree or other argument makes those curves integral.

## 2. What happens at simple basepoints

Assume the pencil has d² distinct transverse basepoints p₁,…,p_(d²). Let

    β:S=Bl_{p₁,…,p_(d²)}P² → P²,
    f:S→P¹,
    H=β*O_P²(1),       F=dH−ΣE_i.

Then every E_i is a section of f and F=f*O_P¹(1). Every pencil member is reduced: a repeated component would meet Q=0, and at such a basepoint the two generators could not meet transversely. In particular G=1.

Near a basepoint, after trivializing O(d), use local coordinates P=u,Q=v. In a blowup chart u=s,v=st,

    β*(v du−u dv)=−s²dt.

Thus the differential vanishes to **order two**, not merely order one, along each exceptional section. More globally, the divisor-saturated pullback is the differential of f:

    η_S ∈ H⁰(S, Ω¹_S ⊗ O_S(2F)),
    β*ω=(canonical section of O_S(2ΣE_i)) · η_S.

Because every fiber is reduced, df has no divisorial zero; its zeros at isolated critical points are not a divisor to subtract. The exact divisorial zero of β*ω is 2ΣE_i.

If B is the union of N distinct smooth pencil members, then deg B=Nd, but its strict transform is

    B'=NF.

For N≥3, B is not an SNC divisor on P²: N branches meet at every basepoint. On S these chosen fibers are disjoint and smooth, but

    (B'/m)−2F=(N/m−2)F,        F²=0,

is never ample. Therefore neither the plane branch-degree calculation nor simply blowing up the arrangement verifies the ample-divisor hypothesis of Garcia-Fritz–Urzúa Theorem 5.1. This is a genuine missing hypothesis, not a harmless technicality.

## 3. A smooth generically finite sufficient family

Assume additionally that f is a Lefschetz pencil with irreducible fibers: every singular fiber has precisely one ordinary node and no other singularity. Such pencils exist for degree d≥3. General plane pencils have this property; reducible degree-d curves form a locus of codimension at least d−1≥2, so a general pencil avoids them. General Lefschetz-pencil existence can also be obtained from the standard Veronese-embedding construction.

Choose a smooth connected projective curve C and a finite morphism

    h:C→P¹

of degree n, with all branch values outside the finite set of critical values of f. Let q=g(C), and define

    X=S×_{P¹}C,       a:X→S,       f_X:X→C,
    π=β∘a:X→P².

### Smoothness and branch locus

The fiber product is smooth. Above branch values of h, f is smooth, and smoothness survives base change. Above singular fibers of f, h is étale, so the base change is locally étale over the smooth total surface S. The surface is connected and projective; the connectedness of the fibers of f gives connectedness after this base change.

The morphism π is dominant, generically finite of degree n, but **not finite**. Each E_i' = a*E_i is a section isomorphic to C and is contracted by π to p_i. Its self-intersection is −n. The divisorial branch locus downstairs is precisely the union of the pencil members at branch values of h. The exceptional sections have point images and are not additional plane branch components.

### Exact differential and twist

Let R_h=Σ_c(e_c−1)c be the ordinary ramification divisor of h. Then

    div₀(π*ω)=2ΣE_i' + f_X*R_h.

This is an equality of divisorial zeros, not an assertion about isolated zeros. Locally at a ramification point, a base parameter t=h(z) gives dt=h'(z)dz, with order e_c−1. At exceptional sections the previous s² calculation persists. At nodes of the pencil, h is étale and no new divisorial zero occurs.

The exact saturated twist is therefore

    N = π*O_P²(2d) ⊗ O_X(−2ΣE_i'−f_X*R_h)
      = f_X*(h*O_P¹(2) ⊗ O_C(−R_h))
      = f_X*K_C^(−1),

using Riemann–Hurwitz. The resulting nonzero section

    η_X ∈ H⁰(X, Ω¹_X ⊗ f_X*K_C^(−1))

is the cotangent map f_X*K_C→Ω¹_X. It is integral exactly on fiber components of f_X. In particular the contracted E_i' are **not** integral for this saturated form: they map isomorphically to C. They were integral for the unsaturated pullback because their image in P² is a point. This is why the usual implication after division is one-way, and why exceptional curves must not be silently identified with the primitive integral locus.

### Theorem 3: genus-bounded completeness

Fix an integer g≥0. If q>g, every irreducible curve D⊂X of geometric genus at most g is a fiber component of f_X. These are the only possible low-genus curves.

**Proof by the differential degree test.** If D is horizontal, its normalization D̃ maps to C with some degree δ≥1. The pulled-back differential has target line bundle of degree

    deg(N|D̃)+deg K_D̃
      = −δ(2q−2)+2g(D)−2
      ≤ 2(g−q) < 0.

Here q≥1, so replacing δ by 1 gives the upper bound. The differential must vanish. But its pullback is the derivative of the nonconstant morphism D̃→C, which is nonzero in characteristic zero. Contradiction. Vertical curves are already known to be integral. ∎

The same argument is precisely Riemann–Hurwitz for a horizontal curve; this family is a transparent application of an established mechanism, not an assertion of a new general theorem.

The arithmetic genus of a degree-d plane curve is p_a=(d−1)(d−2)/2. The smooth fibers have genus p_a and the irreducible nodal fibers have geometric genus p_a−1. Thus:

    if q>g and (d−1)(d−2)/2−1>g,
    then X has no irreducible curves of geometric genus ≤g.

All exceptional sections have genus q>g, so they do not invalidate this assertion. If the second inequality is absent, the theorem still classifies the possible low-genus curves as the explicitly known fiber curves; the classification is not automatically an empty or finite set.

### Concrete cyclic choices

Choose N distinct noncritical values λ_j and an integer n≥2 dividing N. Normalize and compactify

    y^n=∏_{j=1}^N(t−λ_j).

This gives a connected cyclic h:C→P¹ with full ramification at the N finite values and no ramification at infinity. Its genus is

    q=(n−1)(N−2)/2.

For every fixed g, taking n=2 and N=2g+4 gives q=g+1. Select d≥3 with p_a−1>g. The resulting X is smooth and has no curves of geometric genus ≤g, while its plane branch divisor has degree Nd and ω has twist 2d.

The finite normal model is the normalization of the cyclic plane cover

    w^n=∏_{j=1}^N(P−λ_jQ),

where w is a fiber coordinate for O_P²(Nd/n). The smooth X above resolves this model over the pencil basepoints. Calling that normal finite model smooth would be incorrect.

For example, a general quartic Lefschetz pencil, n=2, N=6, and q=2 gives a smooth generically double surface X→P² with no rational or elliptic curves. The branch divisor is six smooth quartics of total degree 24, and ω has twist 8. The sixteen exceptional sections are genus-two curves of self-intersection −2. The exact saturated twist is

    N ≅ π*O_P²(−4) ⊗ O_X(ΣE_i'),

not π*O_P²(−4). Equivalently it is f_X*K_C^(−1), whose square is zero.

## 4. The exceptional correction cannot be dropped

In the cyclic construction, put R=Σ_j F_j', where F_j' is the reduced fiber of f_X over the ramification point above λ_j. Since each selected plane member contains every simple basepoint once,

    π*B=nR+NΣE_i'.

Ramification along the noncontracted branch curves removes (n−1)R, not (1−1/n)π*B. After also removing the exactly known exceptional zeros 2ΣE_i', the twist is

    π*O_P²(2d−Nd(1−1/n))
      ⊗ O_X((N(1−1/n)−2)ΣE_i').

The exceptional correction in the second line is essential. It restores the correct degree zero on every fiber. In particular the large positive plane coefficient Nd(1−1/n)−2d does not produce an anti-ample saturated twist on X.

For d=1 this can be checked without any singular pencil fibers. Then X is a P¹-bundle over C. A negative multiple of π*O(1), without the exceptional correction, has negative degree on a general rational fiber. Since Ω¹_X restricted to such a fiber is O⊕O(−2), no nonzero twisted 1-form with that incorrect twist could exist: it would vanish as a vector section on every fiber, hence globally. The actual twist f_X*K_C^(−1) has degree zero on those fibers.

## 5. Obstruction to a smooth finite concurrent-line cover

### Proposition 4

Let Z be a connected normal complex projective surface and ρ:Z→P² a finite surjective morphism of degree n. Suppose its branch locus is supported on finitely many lines through one point p. If n>1, then Z is singular above p. In particular a connected smooth finite cover with this branch support has degree one.

**Proof.** Choose a nonempty finite supporting collection of lines, enlarging it by an arbitrary line through p if the branch locus is empty. Let T⊂P¹ be its set of directions and U=P¹\T. Projection from p identifies

    W=P²\(union of those lines)

with the restriction to U of the line bundle O_P¹(1). Its complex fibers are contractible, and the zero section is a deformation retract. Hence every connected finite topological cover of W is pulled back from a connected finite cover of U. Riemann existence upgrades this to finite étale algebraic covers. Apply this to ρ over W and compactify the resulting cover to a finite morphism h:C→P¹ of degree n.

Let S=Bl_pP² and Y=S×_{P¹}C. This is a smooth P¹-bundle over C. The composite Y→P² is finite away from its distinguished section E≅C. The section has E²=−n and maps to p. Its Stein factor is a normal finite cover of P² with the same function field as Z, and therefore is Z by uniqueness of normalization. Thus Y→Z is a resolution, is an isomorphism away from E, and contracts the single curve E.

Suppose Z were smooth at that image point. The relative canonical divisor of the birational morphism between smooth surfaces is a positive integral multiple aE, with a≥1 (the Jacobian vanishes on a contracted divisor). Since a pulled-back Cartier divisor has intersection zero with E, adjunction gives

    2g(C)−2=(K_Y+E)·E=(a+1)E²=−(a+1)n.

The left side is at least −2, whereas the right side is at most −4 when n>1. Contradiction. ∎

This argument permits non-Galois covers; it is stronger than observing a singularity in a particular cyclic equation. It is limited to a pencil of **lines**. It is not a general nonexistence theorem for branch components contained in an arbitrary higher-degree pencil or in several different pencils.

The Riemann-existence input is the standard equivalence between finite étale covers and finite topological covers of a nonsingular complex variety. An author-hosted statement is J.S. Milne, *Lectures on Étale Cohomology*, v2.10, Theorem 21.3, printed p. 125: https://www.jmilne.org/math/CourseNotes/LEC210.pdf . The remaining steps above are the stated direct geometric argument; no source was found claiming this exact proposition as a new result.

## 6. Boundary against the cited literature and target

Garcia-Fritz's thesis already supplies the normalization-based integrality definition, ramification vanishing along divisors mapping to curves, and the negative-degree genus test (Proposition 3.42, Theorems 3.35 and 3.87, Proposition 3.88). The exceptional calculation here is separate: Theorem 3.87 expressly assumes the image is a curve and therefore does not justify an assigned vanishing order on a divisor contracted to a point.

Garcia-Fritz–Urzúa, *Families of explicit quasi-hyperbolic and hyperbolic surfaces*, inspected arXiv:1804.07671v1, Theorem 5.1, handles a different SNC cyclic-tower setting and its quotient-singularity corrections. Its hypotheses must not be imported into the non-SNC concurrent-pencil arrangement without verification. In the simple-basepoint pencil blowup, the natural positivity divisor is a multiple of the fiber class and is not ample. The exact fibration calculation above works instead, with a different, weaker positivity mechanism sufficient to exclude horizontal low-genus curves.

The construction gives verifiable conditions on a smooth X and a morphism π:X→P², with an explicit low-twist branch-integral differential and an exhaustive genus-bounded conclusion for the stated family. It does **not**:

- characterize existence or the optimal twist for arbitrary branch divisors;
- supply a smooth finite cover in this pencil base-change family;
- classify every low-genus curve merely from its plane integrality;
- prove that products of pencil forms yield positivity after arbitrary cover resolutions;
- resolve the general, open-ended OWR question or supersede the existing ramification and degree arguments.

Public primary sources inspected or used for standard inputs:

- Garcia-Fritz, OWR contribution, Question 1, printed p. 2841: https://ems.press/content/serial-article-files/46652 .
- Garcia-Fritz, 2015 thesis: https://qspace.library.queensu.ca/bitstreams/007eb1de-ecf4-4747-a756-f7cac789ba56/download .
- Garcia-Fritz–Urzúa, inspected manuscript: https://arxiv.org/abs/1804.07671 .
- Milne, *Lectures on Étale Cohomology*, Riemann-existence and Lefschetz-pencil treatments: https://www.jmilne.org/math/CourseNotes/LEC210.pdf .
- Milne, *Algebraic Geometry*, Lefschetz-pencil outline, Theorems 17.2–17.3 and Remark 17.4: https://www.jmilne.org/math/CourseNotes/AG500.pdf .

All source formulations in this note are paraphrases. The algebraic constructions, displayed calculations, and proofs are authored analysis; raw third-party text is not incorporated.
