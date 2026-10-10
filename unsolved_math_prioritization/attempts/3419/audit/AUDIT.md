# Independent adversarial audit: OPG-37237

Date: 3 October 2026. Target: ID 3419, rank 539.

## Verdict

**Accept the frozen packet as an unresolved, five-attempt research report with valid partial results.** No blocking mathematical error was found. This is not acceptance of a solution to the open problem, a novelty claim, or a machine-checked topology proof.

The main new calculation in Proposition 5 survives the audit: the September 2026 group Γ₆ has nonzero second rational group homology, and the stated lower bound dim H₂(Γ₆;Q) ≥ 2 follows from the actual injective HNN constructions. It is therefore excluded as a smooth or locally flat PL sphere-knot group. A separate audit supplement obtains the stronger value 7 by keeping additional exact-sequence information; this improvement is not needed to validate the frozen packet.

The supplied SHA256SUMS digest is

    acc47454c1010668f2edce71c227d55e0202b14e317b1960052decc1c121b88a

It matches. All eight entries in that manifest verify. Running the frozen verifier afresh produced byte-for-byte identical output, including all 35,453 assertions. The frozen files were not edited.

## 1. Target and category

The [original Open Problem Garden question](https://www.openproblemgarden.org/op/unsolvability_of_word_problem_for_2_knot_complements) asks for a smooth/PL embedded S² in S⁴ whose complement group has an unsolvable word problem. The packet explicitly works in the conventional smooth or locally flat PL knot category. That convention agrees with the definition in González-Acuña–Gordon–Simon, §2. The bare OPG wording does not itself spell out local flatness; the packet transparently states its interpretation rather than silently proving a theorem about singular or wild embeddings.

The ambient sphere remains the standard sphere. No positive-genus surface, arbitrary 4-manifold, homotopy sphere, higher-dimensional knot, or embedded thickening is substituted. “Unresolved” is an account of this investigation's outcome, not an asserted theorem that the entire literature remains unresolved.

The fixed-group word problem is correctly distinguished from recognizing group classes and recognizing unknotted embeddings. An undecidable recognition problem over varying presentations does not by itself give a particular 2-knot group with undecidable word problem.

## 2. Necessary conditions and the realization barrier

Proposition 1 is correct. Compact exteriors have finite CW type. Alexander duality gives H₁(E)=Z and H₂(E)=0, and the Hopf exact sequence surjects H₂(E) onto H₂(π₁E). The normal-bundle and van Kampen argument establishes meridional normal generation. Passing from integral to rational H₂ introduces no issue.

I checked the complete relevant printed arguments in [González-Acuña–Gordon–Simon (2010)](https://ems.press/content/serial-article-files/44199), including Proposition 3.1, Theorem 3.3, Corollaries 3.4–3.5 and the comparison Theorem 3.6. The perfect-container theorem is an established cited input; its printed proof itself leaves some cancellation details implicit. The packet neither conceals that fact nor claims to have computer-certified the theorem. The higher-dimensional realization theorem is likewise an explicit cited input.

For the packet's subsequent HNN construction, the two edge maps are monomorphisms. The quotient onto the free group on s,t also proves that s,t freely generate their subgroup. The integral H₂ map is the stated invertible map (a,b) ↦ (a+b,−a), with inverse (x,y) ↦ (−y,x+y). The final H₁ difference map is −I. Killing u eliminates s,t and then both copies of P. Thus this construction has the necessary homology and weight and preserves the original subgroup. Its justified realization is in knot dimension at least three.

The complete definition, theorem and proof in [González-Acuña (1994), pp.222–224](https://ems.press/content/serial-article-files/37850) were checked, including the page images. The two closure groups must be free, the braid automorphism must satisfy its free-group conditions, and the connected banded surface must have genus zero. The capping argument produces a sphere in standard S⁴ under those hypotheses. The final surface generalization does not remove the genus restriction for a 2-knot.

Accordingly, the packet is right to reject the parenthetical shortcut in [K3, Problem 4.35, Remark (5)](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf). Arbitrary finite Wirtinger presentations describe a larger surface-complement class; they are not the full sphere-knot criterion. Combining the Kervaire conditions with that shortcut would erase the strict distinction already established in the original sources.

## 3. Other partial propositions

### Labelled trees

The tree-incidence proof correctly computes H₁ and the presentation complex's H₂; the latter surjects onto group H₂. Normal generation follows along the tree. The triangular-label induction is valid and does force the entire group to be infinite cyclic.

The relevant necessity and sufficiency arguments in [Yajima (1969), §3](https://ir.library.osaka-u.ac.jp/repo/ouka/all/10894/ojm06_02_14.pdf) were checked. For arbitrary word labels, subdivision into elementary generator-conjugation relations introduces one intermediate generator per additional step and preserves a deficiency-one tree. This supplies the conventional bridge to the source's elementary Wirtinger form. Abstract deficiency one alone would not suffice; the packet requires the specific Wirtinger presentation.

The [Nozaki 2026 proof of Proposition 1.3](https://arxiv.org/abs/2606.02978) does supply the stated ribbon control. The packet's separate BS(1,2) argument has the correct ascending-union orientation: t⁻ʲ⟨a⟩tʲ grows with j when tat⁻¹=a². Its kernel is Z[1/2], so finite generation of commutators is not a necessary condition for a 2-knot group.

### Fibred groups

The pair-scanning algorithm for H⋊Z is a genuine terminating word-problem algorithm, with negative exponents handled by the inverse automorphism. Its application uses a fixed compact 3-manifold fibre and fixed monodromy data; no uniform fibre-recognition step is smuggled in. The additional conditional hypotheses in the source's finiteness-to-fibering discussion are not asserted unconditionally.

### The non-residually-finite control

The specified satellite presentation and fibred-group discussion were checked in [Hillman, p.7](https://www.maths.usyd.edu.au/u/pubs/publist/preprints/2010/hillman-11.pdf). In the base C₃⋊Z, the multiplication and inverse formulas are correct. Both cyclic associated subgroups embed, so b has exact order three in the HNN extension.

Conjugacy of a and a² forces a to have odd order in any finite quotient. Its inversion action then kills b. This proves non-residual-finiteness, but the explicit edge-membership tests and Britton reductions still decide the word problem. Every pinch removes two stable letters; an unreduced nonempty stable-letter sequence cannot represent the identity. The implementation uses the same stable-letter directions as the presentation.

## 4. Main obstruction: six HNN stages

The complete construction and relevant subgroup proofs in [Kegel–Li–Ren (2026), §§2–3 and Appendix B](https://arxiv.org/abs/2609.10461) were read. Their earlier Borisov freeness and embedding results remain cited mathematical inputs. The audit did not run the authors' Lean formalization. The crucial issue is the actual subgroup structure, not merely the shape of displayed relators.

For a genuine HNN extension J with vertex V and edge W, exactness gives

    H₂(W;Q) → H₂(V;Q) → H₂(J;Q) → H₁(W;Q) → H₁(V;Q).

The edge maps are differences of the two induced inclusions. For identity-centralizing extensions both differences vanish. There is no extra quotient of H₂(V) coming from higher homology in that case. These facts justify each step below.

1. Γ₁ is the two-loop extension of F(d,e) along free rank-two subgroups. Its H₁ difference matrix has rank two, so b₂(Γ₁)=2 and b₁(Γ₁)=2.
2. The Γ₂ edge really is F₅. Its H₂ is zero; therefore the old H₂ injects. The kernel of a map Q⁵→Q² has dimension at least three, giving b₂(Γ₂)≥5.
3. In Γ₂, c,d are free by the source's Corollary 3.6. Centralizing them adds exactly two to b₂, giving b₂(Γ₃)≥7.
4. Γ₄ centralizes the actual subgroup Δ. The inclusion of H₂(Γ₃) is injective even if Δ is not free and even if H₂(Δ) is nonzero. This is a key safeguard, correctly used.
5. The Γ₅ edge A has exactly the source's Lemma 3.1 presentation. Its intermediate group S has b₂=0 and b₁=1, since diag(3,−3) is invertible over Q. Centralizing s adds one to b₂. In the resulting group, ⟨c,d⟩ is free: nonzero d powers cannot enter ⟨s⟩, by the stable-letter exponent map, and Britton reduction rules out a nontrivial relation. Centralizing this F₂ adds two more. Thus b₂(A)=3, and the Γ₅ step can remove at most three dimensions, leaving at least four.
6. The last edge is precisely F(c,d)×Z(t), not an assumed free group. Its b₂ is two by Künneth. It can remove at most two dimensions, leaving b₂(Γ₆)≥2.

The abelianization calculation is also valid: the eliminated generators have the same class as d, 2d=3d=0, s₂=−s₁, and the semigroup condition (c) eliminates s₁,s₂. The stable letter z remains unrestricted, so H₁(Γ₆)=Z. The cited normal-generation argument is compatible with this calculation.

None of these steps equates presentation deficiency with group deficiency, assumes Δ is free, or relies on a finite test to establish an infinite family of injections. The sphere-knot exclusion follows from H₂=0 for sphere-knot groups, not from the number of generators or relators.

## 5. Decision results and computational evidence

The complete relevant §§5C–D passage in [Blackwell–Kirby–Klug–Longo–Ruppik (2025)](https://msp.org/agt/2025/25-8/agt-v25-n8-p07-p.pdf) was checked. The packet uses its recognition discussion conservatively and does not turn it into a fixed-group word-problem result.

The frozen program was inspected and independently replayed. The exact output includes 1,442 labelled trees, 8,477 maximal-minor tests, 423 small permutation representations, and the announced total of 35,453 assertions. New audit controls also recompute the displayed ranks by determinant minors, rather than repeating the packet's Gaussian-elimination routine.

These computations are finite consistency tests. They do not prove undecidability, exhaust all finite quotients, establish all HNN subgroup injections, or certify a geometric realization. The unrestricted conclusions rely on the written arguments and identified source theorems.

All nine source PDF hashes in SOURCE_HASHES.json were independently checked against the inspected bytes; the K3 PDF was retrieved again from its listed public URL. No source PDFs or extracted source text are included in this audit.

## 6. Required changes and limits

No correction is required for the packet's stated unresolved verdict or its proved partial claims. The optional exact-H₂ calculation in HOMOLOGY_SUPPLEMENT.md may be used as additional mathematical evidence, but should not be described as solving OPG-37237 or as established novelty.

A future positive solution still needs a genuine smooth or locally flat PL 2-knot in standard S⁴ and an injective undecidability reduction. A negative solution still needs a word-problem algorithm for every such group. Neither is supplied by these five attempts.
