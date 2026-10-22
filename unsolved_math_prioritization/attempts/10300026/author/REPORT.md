# Question 8.3: audited scope and elementary partial results

## Disposition

Problem 10300026 / AMR-102-0026 is **not solved by this report**. No new counterexample or general existence theorem is established. The exact original question's current status was not established by this bounded investigation. A June 2026 primary manuscript still poses the co-orientable version. Earlier material contains contrary-looking announcements, whose compatibility with that convention has not been resolved here. This is a source-grounded status correction and a collection of elementary reductions, not a novel partial-solution claim.

## Exact target and definitions

The target of Calegari, *Problems in foliations and laminations of 3-manifolds*, Question 8.3, printed page 16, can be written in authored logical notation as follows: for every atoroidal 3-manifold M, nonemptiness of the collection of taut foliations on M should imply nonemptiness of the collection of R-covered foliations on M.

In Definitions 1.1–1.2, tautness is expressed using a transverse circle meeting every leaf; R-covered means that the lifted foliation's leaf space in the universal cover is homeomorphic to the real line. Atoroidality excludes essential embedded tori. The question itself does not add co-orientability. See [C].

The quantifiers concern the manifold: given at least one taut foliation, does there exist some R-covered foliation, possibly entirely different? Constructing a branching foliation on a particular manifold only disproves an assertion about that foliation. It does not rule out another R-covered one. A negative answer needs both tautness and an obstruction applying to every candidate on the same atoroidal manifold. A classification of all candidates is not requested and would be stronger than necessary.

The elementary arguments below assume connected closed manifolds and nonsingular codimension-one foliations. The bundle argument assumes a connected closed surface. The virtual-fibering application is restricted to closed hyperbolic manifolds. These are explicit hypotheses of the partial statements, not silent additions to the original problem.

## 1. Covering invariance and the missing descent condition

**Lemma 1.** Let p:N→M be a connected covering and F a foliation on M. The leaf spaces of the universal lifts of F and p*F are naturally identical. In particular, F is R-covered if and only if p*F is R-covered.

**Proof.** Let q:U→N be the universal covering. The composite p∘q:U→M is a covering with simply connected domain, so it is a universal covering of M. Pullbacks compose: q*(p*F)=(p∘q)*F. Thus the two lifted foliations are literally the same partition of U into leaves. Their quotient spaces, including the quotient topologies, coincide. ∎

This proves invariance for the pullback of a specified downstairs foliation. It says nothing about an unrelated foliation constructed upstairs.

**Lemma 2.** Let p:N→M be a finite regular covering with deck group D. A foliation G on N descends to a foliation on M with pullback G if and only if each d∈D preserves G. If G is R-covered, the descended foliation is R-covered.

**Proof.** Necessity follows from p∘d=p. Conversely, choose an evenly covered neighborhood of a downstairs point and a small foliation box in one sheet. Transport its plaques to the other sheets by deck transformations. D-invariance makes the resulting local plaque structure independent of the choice of sheet. These descended boxes form a compatible foliated atlas. Their pullback is G. The last assertion is Lemma 1. ∎

Preservation here means preservation of the entire foliation, not pointwise preservation of each leaf. Co-orientation descends only if the deck transformations also preserve that chosen co-orientation. Tautness descends in the usual leafwise closed-transversal sense: a transverse closed curve upstairs projects to a transverse closed curve meeting the corresponding downstairs leaf. No averaging of foliations or automatic deck invariance is supplied by a covering theorem.

**Lemma 3.** The fiber foliation of a bundle M→S¹ with connected closed surface fiber Σ is co-orientable, taut, and R-covered.

**Proof.** Write M as the mapping torus of a homeomorphism f:Σ→Σ. Its infinite cyclic cover is Σ×R, and its universal cover is the product of the universal cover of Σ with R. The lifted leaves are exactly the horizontal slices. Projection to R identifies the quotient leaf space with R, with the quotient topology. The base-circle direction supplies a co-orientation. Choose x∈Σ and a path in Σ from x to f⁻¹(x). Its graph over [0,1] closes in the mapping torus, is transverse to each fiber, and meets every fiber. In the smooth category the path can be chosen stationary near its endpoints, giving a smooth closed transversal. ∎

Agol's virtual-fibering theorem, Theorem 9.2 of [A], implies that every closed hyperbolic 3-manifold has a finite cover satisfying Lemma 3, even without initially assuming a taut foliation downstairs. A further finite regular cover can be obtained by taking the normal core of the covering subgroup; the pulled-back foliation remains R-covered by Lemma 1. Its invariance under the full deck group over the original manifold is still unproved. Thus virtual fibering settles the finite-cover variant, not the question on M itself.

## 2. The exact line-action obstruction

**Lemma 4.** If M has an R-covered taut foliation F, its fundamental group acts on R without a global fixed point. If F is co-orientable, this action preserves orientation.

**Proof.** Deck transformations preserve the lifted foliation and therefore act by homeomorphisms on its leaf space L≅R. Suppose a point of L were fixed by every deck transformation, and let λ be the corresponding lifted leaf. Choose a transverse closed curve through a point of the projected leaf and lift it starting at x∈λ. Its endpoint is g(x) for some deck transformation g, hence lies in g(λ)=λ. Along the lifted transverse curve, the map to the oriented line L is locally strictly monotone. Its local direction cannot change on the connected parameter interval without losing transversality. It is therefore strictly monotone on that interval. The starting and ending points cannot project to the same point of L, a contradiction. Finally a downstairs co-orientation lifts to a deck-invariant orientation of L. ∎

Consequently, an atoroidal tautly foliated manifold for which every action of π₁(M) on R has a global fixed point would be a counterexample. But no such manifold is verified here. Excluding only actions in Homeo⁺(R) is insufficient to exclude a non-co-orientable R-covered foliation. Faithfulness is neither needed nor asserted in Lemma 4. The universal-circle action attached to a foliation is a different action and does not, merely by existing, provide an obstruction to every possible line action.

## 3. One-sided branching does not finish the obstruction

Zhao's Theorem 1.1 in [Z1] states that a connected, closed, orientable, irreducible 3-manifold carrying a co-orientable taut foliation with one-sided branching has left-orderable fundamental group. It does not construct an R-covered foliation or prove that none exists.

Thus one-sided branching is not itself the manifold-level negative certificate sought above. Even a successful proof of left-orderability would not reverse Lemma 4: an arbitrary action on a line need not be realized as the leaf-space action of a foliation on the prescribed manifold. Establishing such realization would be additional mathematics.

## 4. Exact scope of the modern positive family

Zhao's June 2026 manuscript [Z2] globally assumes orientable 3-manifolds and co-orientable taut foliations; Question 2 reposes the problem. Its Theorem 1.4 has specific hypotheses: Σ is compact orientable with nonempty boundary and negative Euler characteristic; φ is orientation-preserving pseudo-Anosov; its stable foliation is co-orientable and φ reverses that co-orientation. In the paper's canonical peripheral coordinates, write the degeneracy locus on boundary torus Tᵢ as (pᵢ;qᵢ), and let cᵢ be the orbit length of a boundary component of Σ in Tᵢ. Let Jᵢ be the open interval of the projective slope circle with endpoints pᵢ/(qᵢ+cᵢ) and pᵢ/(qᵢ−cᵢ) avoiding pᵢ/qᵢ. For rational slopes sᵢ∈Jᵢ, including infinity when in Jᵢ, an appropriate admissible arc system produces an R-covered foliation on the filling. This is a genuine positive family. The theorem does not cover arbitrary atoroidal tautly foliated M. It also cannot silently settle the unqualified original question's non-co-orientable cases.

## Historical evidence that must remain visible

Calegari's Remark (2) following Question 8.3 contains an assertion about tautly foliated hyperbolic manifolds with no fixed-point-free line actions, citing Roberts–Shareshian–Stein. Read literally, that would interact directly with Lemma 4. This report does not certify the assertion or silently change its wording. [C]

Rachel Roberts's July 2004 conference abstract announces hyperbolic manifolds with taut foliations but no R-covered foliation. The short abstract supplies neither the examples nor a proof, and does not resolve the co-orientation convention. It is an important lead, not a verified counterexample certificate. [R]

Brittenham's paper establishes graph-manifold counterexamples; its examples contain incompressible tori, so they do not meet the atoroidal hypothesis. It also poses the hyperbolic variant in Question 6. [B]

The announced historical examples and the modern co-orientable question must be reconciled before upgrading the original problem to solved or declaring its exact unqualified status definitively open. No conclusion about novelty follows from an unsuccessful bounded search.

## Stopping condition and acceptance boundary

Four substantive routes were examined: covering/descent, universal line-action obstruction, one-sided branching, and the specified Dehn-filling construction. None gives a full answer. The first two yield complete elementary lemmas above; the latter two are audited uses of existing work. Further work would need either a verified historical counterexample with all hypotheses, a genuinely new obstruction for all candidate foliations, or a realization/descent theorem not proved here.

The package's program checks metadata and preservation of this unresolved disposition. It is not a theorem prover, a proof checker for foliation theory, or evidence of a new mathematical result. Independent mathematical and privacy review is required before publication.

## Public primary sources

[C] Danny Calegari, *Problems in foliations and laminations of 3-manifolds*, arXiv:math/0209081v1, Definitions 1.1–1.2 and Question 8.3 with remarks. https://arxiv.org/abs/math/0209081v1

[Z1] Bojun Zhao, *Left orderability and taut foliations with one-sided branching*, arXiv:2209.04752v2, Theorem 1.1. https://arxiv.org/abs/2209.04752v2

[Z2] Bojun Zhao, *Left-orderability in Dehn fillings of pseudo-Anosov mapping tori*, arXiv:2604.04629v2, Question 2, Conventions 1.1–1.2, Theorems 1.3–1.4. https://arxiv.org/abs/2604.04629v2

[A] Ian Agol, with an appendix by Ian Agol, Daniel Groves and Jason Manning, *The virtual Haken conjecture*, Theorem 9.2. https://arxiv.org/abs/1204.2810

[B] Mark Brittenham, *Tautly foliated 3-manifolds with no R-covered foliations*, Introduction and Question 6. https://arxiv.org/abs/math/0011130

[R] Rachel Roberts, *Foliated hyperbolic 3-manifolds containing no R-covered foliation*, abstract in *Knots in Vancouver*, July 19–23, 2004, page 5. https://media.pims.math.ca/pdf/science/2004/KT3Mwksp/knotabs.pdf
