# Core geodesics in the one-handle compression body: first attempt

Problem: 30001048, OWR-2089-004. Assessment date: 2026-10-10.

## Outcome

**Unresolved.** This note does not prove or disprove the conjecture. It gives an exact algebraic test for self-intersection of the homotopic geodesic, proves two families of collision witnesses impossible, and identifies the missing global step. Even embeddedness at one hyperbolic structure is not, by itself, a proof of the required isotopy.

**Publication edition:** Approach 1 of 5. This authored mathematical note and its accompanying audit are AI-assisted and unrefereed. No novelty claim is made. Read the note together with [INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md), especially §§2–3 for the rank-two cusp, full stabilizer, marking, accidentally parabolic generator, and explicit properness argument. Those extensions are supplied by the audit; they are not attributed to the loxodromic-only wording of Lackenby–Purcell Lemma 4.8.

## 1. Exact scope and source alignment

Let C be obtained from T² × [0,1] by attaching one 1-handle to T² × {1}. Its negative boundary is a torus and its positive boundary has genus two. The core tunnel τ is the handle core extended by two product arcs to the negative boundary, so C is a regular neighborhood of ∂₋C ∪ τ. The fundamental group has a marked decomposition

G = P * ⟨γ⟩, with P ≅ Z².

The question is whether τ is isotopic to a geodesic in **every geometrically finite complete hyperbolic structure** on the interior of C. Endpoints are understood to run out the rank-two cusp, or equivalently one truncates the cusp and permits endpoints to move on its boundary torus. It is not a statement about pointwise-fixed arbitrary finite endpoints.

The original report is Jessica Purcell's contribution to Topologie, Oberwolfach Report 43/2008, context on printed p. 2435 and Conjecture 2.1 on p. 2436 [S1]. Lackenby–Purcell [S2, Conjecture 1.1 and §2.1] confirms this interpretation. In particular:

- Homotopy to a unique cusp-to-cusp geodesic is already available. Isotopy is the missing requirement.
- “Geometrically finite” is the conjecture's quantifier. The minimally parabolic restriction belongs to several partial theorems, not to the original question.
- Ford duality is the stronger Conjecture 5.11 in [S2], not the definition of the requested conclusion.
- Burton–Purcell's self-intersecting tunnel construction uses at least two handles [S3, Theorem 1.1]. It is not a counterexample here.

## 2. A normalized formulation

Let ρ be a discrete faithful representation giving such a hyperbolic structure, and identify G with its image Γ. Normalize the fixed point of P to ∞ in the upper half-space model. Thus P consists of translations

T_λ = [[1, λ], [0, 1]],  λ ∈ Λ,

where Λ is a rank-two lattice in C. The stabilizer of ∞ is precisely P; here is a justification that does not silently assume maximality of the marked subgroup. Any element fixing ∞ acts on the boundary as z ↦ Az+B. If |A|≠1, conjugating a nontrivial element of P by suitable positive or negative powers produces nonidentity translations converging to the identity, contrary to discreteness. If |A|=1 and A≠1, the element is elliptic, contrary to discreteness and torsion-freeness. Hence A=1, and the element is a translation commuting with P. The free-product normal-form theorem gives C_G(P)=P: an element outside P contains a handle syllable, and conjugating any nonidentity element of P by it cannot reduce to an element of P. Faithfulness now places the original element in P, as required.

Choose a determinant-one lift of γ. Its lower-left entry c is nonzero because γ is not peripheral. If its entries are initially [[a,b],[c,d]], first conjugate by the translation z ↦ z + d/c and then by the complex dilation z ↦ cz. The resulting generator is

g = [[s, -1], [1, 0]],   s = a + d.

All matrices below have determinant one. Changing a matrix lift by sign leaves the product of its off-diagonal entries unchanged.

The vertical geodesic

L = { (0,t) : t > 0 }

has endpoints 0 = g⁻¹∞ and ∞. Its projection to H³/Γ is the unique geodesic in the proper homotopy class of the core tunnel, with orientation reversed if necessary. This uses the marked double coset PγP, as in [S2, Lemma 4.8].

The setwise stabilizer of L in Γ is trivial. An element fixing its two endpoints individually lies in P and fixes 0, hence is the identity. An element interchanging the endpoints has order two in PSL(2,C), impossible in this torsion-free group.

## 3. Exact collision criterion

### Proposition 1

For a nonidentity element h = [[a,b],[c,d]] of Γ, the geodesics L and hL meet in H³ if and only if

bc ∈ (−1,0) ⊂ R.

Consequently, the projected core geodesic is embedded if and only if every h ∈ Γ avoids this interval.

### Proof

If one of a,b,c,d vanishes, the two geodesics either have a common endpoint at infinity, are distinct vertical lines, or would have the same endpoint pair. A common ideal endpoint does not give an interior intersection of distinct hyperbolic geodesics. The last possibility was excluded by the trivial stabilizer. Also, bc is then either 0 or −1, never strictly between them.

Otherwise, the endpoints of hL are u = a/c and v = b/d. The geodesic joining finite nonzero u and v is a Euclidean semicircle orthogonal to the boundary plane. It meets the vertical line above 0 precisely when u and v are on opposite rays from 0. Equivalently,

u/v = ad/(bc) ∈ (−∞,0).

Since ad − bc = 1, this quotient is 1 + 1/(bc), which is negative real exactly when bc is real and −1 < bc < 0. In that case the height of intersection is √(|u||v|), so the meeting really occurs in H³.

The projection is locally injective because the quotient map is a local isometry. A double point lifts to L ∩ hL for some nonidentity deck element h, and any such intersection gives a double point because the stabilizer of L is trivial. The projected geodesic is proper: both its ends eventually remain in embedded cusp neighborhoods, and its remaining portion is a compact interval. Thus injectivity is equivalent to being an embedded proper geodesic. ∎

The interval is open. Values bc = 0 and bc = −1 correspond to endpoint coincidences or degenerate endpoint configurations, and are not interior self-intersections.

## 4. The Shimizu–Leutbecher exclusion

We use the following standard discreteness consequence in precisely its needed form [S3, Lemma 4.3]: if T_λ ∈ Γ with λ ≠ 0 and k ∈ Γ has lower-left matrix entry c_k ≠ 0, then

|λ c_k| ≥ 1.

Indeed the isometric sphere radius 1/|c_k| is at most the shortest nonzero translation length of P, which is at most |λ|. No sufficiency for discreteness is asserted.

### Proposition 2

No element of the form T_λ g T_μ or T_λ g⁻¹ T_μ, with λ,μ ∈ Λ, witnesses a self-intersection of the core geodesic.

### Proof

For positive exponent,

T_λ g T_μ = [[s+λ, μ(s+λ)−1], [1, μ]].

The product bc is μ(s+λ)−1. A collision would require μ(s+λ) ∈ (0,1), in particular μ ≠ 0. Set k = T_λ g. Its square has lower-left entry s+λ. This entry cannot be zero: trace(k) = s+λ = 0 would imply k² = −I by Cayley–Hamilton, giving a nontrivial element of order two in PSL(2,C). Applying the displayed discreteness inequality to T_μ and k² gives |μ(s+λ)| ≥ 1, a contradiction.

For negative exponent,

T_λ g⁻¹ T_μ = [[−λ, 1+λs−λμ], [−1, s−μ]].

Here bc = λ(μ−s)−1, and a collision requires λ(μ−s) ∈ (0,1), so λ ≠ 0. Set k = g⁻¹ T_μ. The lower-left entry of k² is μ−s. It is nonzero for the same trace-zero/order-two reason. The discreteness inequality applied to T_λ and k² gives |λ(μ−s)| ≥ 1, again a contradiction. ∎

Peripheral elements themselves have bc = 0 and cannot witness a collision.

## 5. A cyclic-word exclusion

Define polynomials P₀(x)=1, P₁(x)=x and Pₘ₊₁(x)=xPₘ(x)−Pₘ₋₁(x). Thus Pₘ(x)=Uₘ(x/2), in terms of the Chebyshev polynomials of the second kind.

### Lemma 3

For m ≥ 1 and r ∈ (−1,1), every complex solution of Pₘ(z)=r is real and belongs to (−2,2).

### Proof

For j=0,…,m put θⱼ=(j+1/2)π/(m+1) and xⱼ=2cos θⱼ. The xⱼ are distinct real numbers in (−2,2), in decreasing order. The identity

Pₘ(2cos θ)=sin((m+1)θ)/sin θ

follows directly from the defining recurrence. Hence

Pₘ(xⱼ)= (−1)ʲ/sin θⱼ.

These values have alternating signs and absolute value at least one. Subtracting r ∈ (−1,1) preserves their signs. The intermediate value theorem gives a real root of Pₘ−r in each of the m intervals between consecutive xⱼ. Since its degree is m, these are all its complex roots, counted with multiplicity. ∎

### Proposition 4

No nonzero power of T_λ g, for any λ ∈ Λ, witnesses a self-intersection of the core geodesic. In particular, no nonzero power of g does.

### Proof

The matrix k = T_λ g is again [[t,−1],[1,0]], where t=s+λ. It sends 0 to ∞, so the relevant geodesic L has not changed. For n ≥ 1, the recurrence or Cayley–Hamilton gives the off-diagonal entries of kⁿ as −Pₙ₋₁(t) and Pₙ₋₁(t). Their product is −Pₙ₋₁(t)².

For n=1 the product is −1, so there is no collision. For n≥2, a product in (−1,0) would imply that Pₙ₋₁(t) is real and lies in (−1,1). Lemma 3 then forces t ∈ (−2,2). A determinant-one matrix with real trace strictly between −2 and 2 represents a nonidentity elliptic isometry. This is impossible in a discrete torsion-free Kleinian group: finite-order elliptics violate torsion-freeness and infinite-order elliptics violate discreteness. Thus no positive power causes a collision. The off-diagonal product is unchanged by taking the inverse, which treats negative powers. ∎

These exclusions use discreteness and torsion-freeness, not an unverified numerical test.

## 6. Where the attempted proof stops

Propositions 2 and 4 do **not** exhaust G=P*⟨γ⟩. Arbitrary reduced mixed words with several handle passages and intervening peripheral factors remain. There is no established induction from the proved word families to all such words: the product bc of a matrix product contains cross terms and does not inherit an interval-avoidance property from its factors.

It is also false that “h is loxodromic” alone excludes the forbidden interval. For example,

h₀ = [[2i, 1/2], [−1, −i/4]]

has determinant one, trace 7i/4, and bc=−1/2. It is loxodromic, and h₀L joins −2i to 2i, meeting L at height 2. This is only an algebraic example. It is **not** a counterexample to the conjecture: no discrete faithful one-handle compression-body group containing h₀ with the required marked generator and cusp is supplied.

The unsolved embeddedness step is therefore the following universal statement:

For every geometrically finite discrete faithful uniformization of P*⟨γ⟩, in the normalization of §2, every group element h satisfies bc ∉ (−1,0).

Even proving that statement at one structure would show only that its homotopic core geodesic is embedded. One must still establish its isotopy class. The familiar local-knot phenomenon explains why arbitrary homotopic proper embedded arcs in a 3-manifold need not be isotopic; it cannot be dismissed by the free-product presentation. Conversely, an arbitrarily knotted representative of the generator is not automatically a core tunnel, so it cannot furnish a counterexample either.

## 7. The path route and its exact missing hypothesis

A sufficient conditional route is as follows. Suppose a smooth path of hyperbolic structures is equipped with a smooth identification of their cusp-truncated manifolds, and their homotopic core geodesics truncate to a smooth family of properly embedded arcs with endpoints on the cusp torus. If the first arc is isotopic to τ, the isotopy-extension theorem transports that isotopy class to the final arc. The point is that the **entire** family must consist of embeddings, including all intermediate parameters; continuity of geodesic representatives alone does not give this.

Lackenby–Purcell implement this route using visible Ford faces [S2, Lemma 5.9]. Their Theorem 5.10 supplies sufficient hypotheses: a real-analytic path of minimally parabolic geometrically finite uniformizations starts at a one-face Ford spine, and at every later parameter a properly embedded compression disk avoids every face of the Ford spine. The resulting core is geodesic and Ford-dual.

Neither mere path connectedness of the deformation space nor the topological existence of some compression disk verifies that avoidance hypothesis. A disk may intersect the Ford faces. Face visibility is open along such paths, but openness does not make it persist to an arbitrary endpoint. [S2, §5.3] explicitly discusses internal changes of Ford-domain combinatorics; avoiding those changes is posed as Question 5.12.

The original conjecture also permits geometrically finite structures with rank-one parabolics. A proof restricted to the minimally parabolic deformation space would require a further justified boundary argument. Limits of embedded arcs can have double points, so approximation alone is insufficient. No such extension is proved in this attempt.

## 8. Why the known multi-handle counterexample does not settle this case

In [S3, Theorem 3.3], the construction replaces independent handle generators by words δₖ=γₖ⁻¹γₙ for k<n, keeping δₙ=γₙ. This requires n≥2. When n=1, there is no index k<n and the claimed number n−1 of self-intersecting tunnels is zero. Replacing the extra independent handle by a peripheral element changes the construction's topology and algebra; it is not an allowed specialization. The one-handle source cannot be relabeled as a multi-handle source without changing the problem.

## 9. Next proof obligations, not claimed results

1. Prove interval avoidance for all remaining reduced mixed words, or construct one violating word together with a rigorous certificate that the representation is discrete, faithful, geometrically finite, and gives the specified compression body.
2. If using a deformation argument, control embeddings over the entire path and identify the core isotopy class at its starting point.
3. Address geometrically finite structures with accidental rank-one parabolics if the argument initially handles only minimally parabolic structures.

Passing finitely many word tests, observing an almost-intersection numerically, or checking necessary discreteness inequalities would not finish any of these obligations.

## References

[S1] Jessica Purcell, “The geometry of unknotting tunnels” (joint work with Marc Lackenby), in Topologie, Oberwolfach Report 43/2008, printed pp. 2435–2436; Conjecture 2.1. Report DOI: https://doi.org/10.4171/OWR/2008/43 . Official report PDF: https://ems.press/content/serial-article-files/46190?nt=1 .

[S2] Marc Lackenby and Jessica S. Purcell, “Geodesics and compression bodies,” Experimental Mathematics 23 (2014), 218–240. arXiv:1302.3652v2, 12 February 2014. https://arxiv.org/abs/1302.3652 . DOI: https://doi.org/10.1080/10586458.2013.870503 . Relevant preprint locations: §2.1, Lemma 4.8, Lemmas 5.1 and 5.9, Theorem 5.10, Conjecture 5.11, Question 5.12.

[S3] Stephan D. Burton and Jessica S. Purcell, “Geodesic systems of tunnels in hyperbolic 3-manifolds,” Algebraic & Geometric Topology 14 (2014), 925–952. arXiv:1302.5469v2, 11 September 2013. https://arxiv.org/abs/1302.5469 . Published PDF: https://msp.org/agt/2014/14-2/agt-v14-n2-p11-s.pdf . Relevant preprint locations: Theorems 1.1 and 3.3; Lemma 4.3.
