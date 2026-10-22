# Punctured homology spheres: five approaches to KP-4.26

## Result and scope

**The universal question remains unresolved in this investigation.** This note proves elementary reductions and surgery calculations, explains established positive examples, and identifies the missing smooth step. It claims neither a new solution nor a counterexample.

The exact question in *K3: A New Problem List in Low-Dimensional Topology*, Problem 4.26, printed p. 211, is:

> If Y is a homology three-sphere, does the punctured manifold Y₀ = Y ∖ Int(B³) smoothly embed in S⁴?

Here homology means integral homology, Y is closed, connected and oriented, and S⁴ has its standard smooth structure. Put F = Y₀ and G = π₁(Y). All manifolds and embeddings below are smooth, except where explicitly qualified. Corners of products and handle constructions are rounded. A compact puncture, rather than deletion of a point, is intended. The distinction matters at the boundary, and Zeeman's theorem supplies the compact version.

## 1. Doubling: an exact reduction, but no homology-cobordism obstruction

### Proposition 1

F embeds in S⁴ if and only if Y # (−Y) embeds in S⁴. For every Y, whether or not either embedding exists, Y # (−Y) bounds the smooth integral homology ball F × [−1,1]. Its fundamental group is G.

**Proof.** Removing a ball from an integral homology 3-sphere gives an acyclic connected 3-manifold F with boundary S². This follows from the Mayer–Vietoris sequence of Y = F ∪ B³: the connecting map H₃(Y) → H₂(S²) is an isomorphism by the relative fundamental class, so all reduced homology groups of F vanish. Van Kampen gives π₁(F) = G because B³ and S² are simply connected.

An embedding of F in oriented S⁴ has trivial oriented normal line bundle. The tubular-neighborhood construction, extended across a collar of ∂F and rounded at corners, gives a codimension-zero neighborhood diffeomorphic to F × [−1,1]. Its boundary is the oriented double of F, namely Y # (−Y), so the latter embeds.

Conversely, the double contains a smoothly embedded copy of F as a codimension-zero submanifold: take one copy of F and shorten its boundary collar if necessary. Restrict any embedding of the double to this copy. Finally, F × [−1,1] retracts onto F, proving the homology and fundamental-group assertions. ∎

If a closed integral homology sphere M embeds in a smooth integral homology 4-sphere X, the two complementary closures are smooth integral homology balls. Indeed, M separates: its mod-2 homology class in X is zero, and it is connected and two-sided. In the Mayer–Vietoris sequence, H₄(X) → H₃(M) is the orientation isomorphism, and the remaining positive-degree groups of M and X vanish. The sequence gives zero positive-degree homology for both closures.

Thus the usual necessary condition that M bound a homology ball is already automatic for M = Y # (−Y). Any invariant of oriented homology spheres that vanishes on boundaries of smooth integral homology balls vanishes on this double. In particular, a nonzero Rokhlin invariant of Y does not obstruct the punctured embedding by this argument. The closed Poincaré sphere and its puncture actually behave differently; see §4.

**Failed completion.** Filling Y # (−Y) by F × I is not enough to embed that filling in S⁴. In fact its identity double has fundamental group G: the inclusion π₁(∂(F × I)) = G * G → π₁(F × I) = G is the fold map, and the pushout of two identical fold maps is G. For nontrivial G this particular double is not S⁴. A different complementary manifold and gluing, with standard smooth total space, remain necessary.

The equivalence in Proposition 1 is standard; it is also explicitly recorded by Hillman in §2.9 of *Locally flat embeddings of 3-manifolds in S⁴*. The proof is included to expose exactly what does and does not follow.

## 2. Ordinary spinning: the fundamental group survives

### Proposition 2

For every Y there is a smooth integral homology 4-sphere Σ containing F, with π₁(Σ) ≅ G. The untwisted construction therefore supplies an embedding in the required standard S⁴ only when one additionally identifies its ambient smooth manifold with S⁴; for G ≠ 1 such an identification is impossible for this construction.

**Proof.** Start with P = S¹ × Y and remove S¹ × Int(B³). Attach D² × S² along the resulting boundary S¹ × S² using the product identification. Thus

Σ = (S¹ × F) ∪ (D² × S²).

The slice {θ} × F is an embedded copy of F. Van Kampen starts with π₁(S¹ × F) = ⟨t⟩ × G; attachment kills t and introduces no new fundamental group, so π₁(Σ) = G.

Since F is acyclic, S¹ × F has the homology of S¹. The H₁ map from the common boundary to this piece and the H₂ map to D² × S² are isomorphisms. The integral Mayer–Vietoris sequence therefore gives H₀(Σ) = H₄(Σ) = Z and H₁(Σ) = H₂(Σ) = H₃(Σ) = 0. ∎

**Failed completion.** A homology 4-sphere need not be simply connected. Nor can the missing 3-ball in the slice be filled just because its boundary is a 2-sphere. If such a cap could be added disjointly to every slice in a smooth homology 4-sphere, every Y would bound a smooth integral homology ball, contradicting, for example, Rokhlin's obstruction for the Poincaré sphere.

The source's unqualified sentence about spinning closed Y must therefore not be interpreted as a universal *smooth closed-Y embedding* theorem. Proposition 2 is the precise punctured statement furnished by the indicated surgery. A topological interpretation of an unqualified embedding is a different assertion.

## 3. Diagonal-circle surgery: a precise weight-one criterion

### Proposition 3

Given g ∈ G, there is a smooth integral homology 4-sphere Σg containing F with

π₁(Σg) ≅ G / ⟨⟨ [g,x] : x ∈ G ⟩⟩.

Because G is perfect, this group is trivial if and only if g normally generates G. Consequently, weight one gives an embedding of F in a smooth homotopy 4-sphere. It does not by itself identify that sphere with standard S⁴.

**Proof.** Choose a smooth loop γ:S¹ → Y representing g, constant near a chosen parameter value θ₀. Its graph c(θ) = (θ,γ(θ)) is an embedded circle in P = S¹ × Y, even if γ itself has self-intersections. It meets the slice {θ₀} × Y transversely once. Its oriented rank-three normal bundle is trivial, so choose a framing and perform circle surgery: replace c × Int(D³) by D² × S². Choose the tubular neighborhood near the intersection to be a product; the remainder of the slice is F and survives the operation.

Let A be the exterior of c. Inclusion A → P induces a fundamental-group isomorphism. Surjectivity follows by making loops disjoint from a circle in a 4-manifold. For injectivity, a homotopy of loops is a two-dimensional map and can likewise be made disjoint from c, since 2 + 1 < 4. Passing from the complement to the exterior does not change homotopy type. The attaching boundary has fundamental group Z represented by c, which is (t,g) in Z × G. Van Kampen therefore gives

π₁(Σg) = (Z × G) / ⟨⟨tg⟩⟩.

Eliminate t = g⁻¹. The original relations saying that t commutes with every x ∈ G become exactly [g,x] = 1. This proves the displayed formula; choosing the reverse convention for g gives the same normal subgroup.

For the integral homology calculation, excision identifies Hᵢ(P,A) with Hᵢ(S¹ × D³,S¹ × S²), which is Z in degrees 3 and 4 and zero otherwise. The map H₄(P) → H₄(P,A) is the orientation isomorphism. The map H₃(P) → H₃(P,A) is also an isomorphism: its coefficient is the intersection of the slice Y with c, namely +1. Since P has the homology of S¹ × S³, the long exact sequence of the pair now gives Hᵢ(A) = Hᵢ(S¹) for every i. Moreover H₁(S¹ × S²) → H₁(A) is an isomorphism, because the framed longitude represents c, primitive in H₁(P). The H₂ map from this boundary to D² × S² is an isomorphism. Mayer–Vietoris proves that Σg is an integral homology 4-sphere, independently of the framing.

Write Cg = ⟨⟨[g,x] : x ∈ G⟩⟩ and Ng = ⟨⟨g⟩⟩. Since Cg ⊆ Ng, triviality of G/Cg implies Ng = G. Conversely, if Ng = G, the image of g normally generates G/Cg and is central there. Its normal closure is its cyclic subgroup, so G/Cg is cyclic. A quotient of a perfect group is perfect; a cyclic perfect group is trivial. Finally G is perfect because its abelianization is H₁(Y;Z) = 0. This proves the criterion.

A simply connected integral homology 4-sphere is a homotopy 4-sphere. One direct argument uses Hurewicz successively to get π₂ = π₃ = 0 and π₄ ≅ H₄ ≅ Z, represents a generator by S⁴ → Σg, and applies the homology version of Whitehead's theorem for simply connected CW complexes. ∎

**Two distinct missing steps.** This approach would need (i) a normal generator for every relevant G, and (ii) standardness of a corresponding smooth Σg. Neither is supplied here. In particular, solving the group-theoretic issue alone does not prove the desired smooth embedding theorem. The finite group checks accompanying this note verify the quotient calculation on examples, not either universal missing assertion.

## 4. Twist-spinning and surgery families: positive tests, no universal reduction

Zeeman's 1965 Main Theorem, part 2 (p. 486), and Corollary 4 (p. 487) imply that the compact puncture of every finite cyclic cover of S³ branched over a smooth knot embeds smoothly in standard S⁴. The theorem identifies it as the closure of a fiber of the twist-spun knot complement. This is an established theorem, not a new construction in this note; its full proof in §§5–7 was inspected.

This includes the Poincaré homology sphere: Zeeman explicitly identifies the punctured dodecahedral space as the fiber of the 5-twist spin of the trefoil. Hence its nonzero Rokhlin invariant cannot be a punctured-embedding obstruction. There is no inconsistency with the closed obstruction: the embedded boundary S² need not admit a smooth cap disjoint from that particular punctured hypersurface.

### Proposition 4

If F₁ = (Y₁)₀ and F₂ = (Y₂)₀ each embed in S⁴, then (Y₁ # Y₂)₀ embeds in S⁴. Conversely, an embedding of (Y₁ # Y₂)₀ restricts to an embedding of each Fi.

**Proof.** Move each compact embedded Fi into a small ball in R⁴ = S⁴ ∖ {point}, by an ambient chart followed by a translation and dilation, and choose disjoint balls. At a small disk on each ∂Fi, choose a local exterior collar directed toward the complement. The complement of each Fi is connected: Alexander duality gives reduced H₀(S⁴ ∖ Fi) ≅ H³(Fi) = 0, and the complement is locally path connected. Join the exterior collars by an embedded arc with interior disjoint from both Fi. A sufficiently thin D²-bundle along the arc is a 3-dimensional 1-handle attached along the chosen boundary disks; choose its framing to preserve orientation and smooth the corners. The resulting boundary connected sum is diffeomorphic to (Y₁ # Y₂)₀. Conversely, in the boundary-connected-sum model each Fi, with a slightly shortened collar, is a submanifold, and restriction gives the embeddings. ∎

Thus positive cyclic-cover examples extend to their finite connected sums. However, an arbitrary Y has not been represented by such examples here, nor has a more general construction been reduced to them.

The K3 remarks separately credit Larson's thesis with the punctured embedding for 1/n-surgery on an arbitrary knot. The thesis file could not be retrieved, so this note does not count that statement as primary-proof-verified or use it in any proposition. The accessible article *Surgery on tori in the 4-sphere* does not substitute for that exact assertion: its Corollary 5.5 has S² × S² or the twisted S²-bundle as ambient manifold; Theorem 5.6 obtains closed S⁴ embeddings under ribbon/slice hypotheses. The knot hypotheses and the ambient smooth manifold cannot be dropped.

**Failed completion.** Neither special families nor their connected sums constitute a universal classification. General branched-cover presentations need not be cyclic covers of a single knot. No transfer from a noncyclic presentation, or reduction of all homology spheres to the inspected classes, has been proved.

## 5. Killing more generators: the second-homology cost

### Proposition 5

Let X be a closed connected oriented smooth 4-manifold with H₁(X;Z) = 0. Surgery on an embedded circle produces X′ with H₁(X′;Z) = 0 and

rank H₂(X′;Z) = rank H₂(X;Z) + 2.

In particular, starting from the homology sphere of Proposition 2 and killing a finite normal generating set by r circle surgeries produces a simply connected manifold with b₂ = 2r. For r > 0 it is not S⁴.

**Proof.** The same general-position and van Kampen arguments as in Proposition 3 show that circle surgery quotients π₁(X) by the normal closure of the represented element. Its abelianization is a quotient of H₁(X), hence zero. Poincaré duality gives b₃(X) = b₁(X) = 0 and the same for X′.

The surgery removes S¹ × D³, of Euler characteristic 0, and adds D² × S², of Euler characteristic 2. Their common boundary S¹ × S² has Euler characteristic 0. Thus χ(X′) = χ(X) + 2. Both connected closed oriented 4-manifolds have χ = 2 + b₂ because b₁ = b₃ = 0. This proves the rank increase. The integral H₂ groups are free: by Poincaré duality and the universal coefficient theorem, their torsion is determined by the torsion in H₁, which is zero.

A compact manifold has finitely generated fundamental group. Choose finitely many loops representing generators, make them embedded and pairwise disjoint by general position, and perform the surgeries. Their normal closures kill π₁, and iteration gives the asserted rank. ∎

**Failed completion.** This route cannot end at S⁴ merely by killing fundamental group. It creates 2r independent second-homology classes. Removing those classes while preserving an embedded copy of F would require additional smooth geometric operations and proofs of their effect. Algebraic cancellation of ranks is not a geometric handle cancellation. Even preservation of F during arbitrarily chosen additional surgeries is an extra requirement; Proposition 5 is an ambient calculation and makes no such preservation claim. No suitable relative cancellations have been constructed here.

## Exact remaining question

For an arbitrary integral homology 3-sphere Y, construct a smooth embedding of its compact puncture in *standard* S⁴, or produce an obstruction that applies to that puncture. The direct ordinary spin retains G; a normal-generator modification gives only a homotopy 4-sphere; further loop surgeries incur nonzero b₂; established twist-spun families do not cover arbitrary Y. The homology-ball condition on Y # (−Y) is automatic and so does not decide the issue.

The accompanying exact computations are diagnostics for the algebra used above. They do not establish smooth standardness, certify a 4-dimensional handle cancellation, or decide the universal problem.
