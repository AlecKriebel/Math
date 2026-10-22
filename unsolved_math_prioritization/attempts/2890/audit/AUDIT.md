# Independent adversarial audit: universal corks

Date: 5 October 2026 UTC. Target: catalogue ID 2890, rank 693, modern K3 Problem 4.14. The original author manifest is bound by SHA-256 `579a41fb8e474f60df00a4ecfe5d40e221e885385d5b8ee12557a9d7d32bdc37`. All ten original files, including its checksum list, were hashed before review and rechecked after execution. None was changed.

## Verdict

**LIMITED PASS WITH CONTROLLING ADDENDUM; UNSOLVED, 5/5.** The elementary statements and conditional reductions are valid within their stated hypotheses. The one mathematical wording defect found is that Approach 4 assigns infinity when existence is unknown, rather than when no extension exists. `CONTROLLING_ADDENDUM.md` supplies the exact corrected definition and checks every downstream use. No downstream argument relies on that confusion.

Acceptance applies only to this unresolved investigation with that addendum. It does not certify a solution, a new theorem of research significance, the truth of every foundational result from first principles, human peer review, formal verification, or global present-day openness. The five approaches are genuinely distinct attempts and each stops before the missing geometric statement. Their count is a count of substantive approaches, not proof that five separate conversation turns occurred.

## 1. Target and source authentication

The relevant source is the 2026 preliminary author copy of [K3: A New Problem List in Low-Dimensional Topology](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed pp. 201–202. The target is a single compact contractible smooth C and a single nonextendable boundary map f, with embeddings allowed to depend on the closed simply connected exotic pair. It is not the old 1997 Problem 4.14, fixed-embedding universality, or the permission to choose a new map or power for every pair. The displayed question omits orientation; the surrounding discussion distinguishes the two orientations. The author's explicitly oriented deductions therefore have the necessary scope qualification.

Independent read-only GitHub retrieval at commit `2669042ac964d5710972af552df141f7934588af` returned catalogue blob `bd5c23e4e6c7e1901717a7e596477a7f6dc72425`. Independently hashing locally available catalogue bytes gave that Git blob hash, byte count 21,735,099, and SHA-256 `891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566`. The selected record matched the record supplied for this investigation. The pinned queue independently associates rank 693 and ID 2890 with KP-4.14. These are identity and provenance checks, not evidence that the upstream open-status label is current. See the [pinned catalogue](https://github.com/AlecKriebel/Math/blob/2669042ac964d5710972af552df141f7934588af/unsolved_math_prioritization/catalog.json) and [pinned queue](https://github.com/AlecKriebel/Math/blob/2669042ac964d5710972af552df141f7934588af/unsolved_math_prioritization/QUEUE.md).

All eight primary PDFs listed by the author were downloaded anew. Their byte counts and SHA-256 values independently matched the author metadata. Relevant statements and arguments were read; delicate typography was visually checked for the target, the two orientation classes in Ladu, and Yasui's signed genus formula. Full scholarly PDFs, rendered pages, and extracted text are excluded from this deliverable. `INDEPENDENT_SOURCES.json` records the exact versions, locations, and inspection limits. The full raw research corpus was not downloaded or rehashed. Prior duplicate searches, dataset-manifest hashes, and publication-page observations remain author-reported except for the specific independent checks listed here.

## 2. Claim-by-claim elementary mathematics

### Lemma 0.1: boundary, complement, forms, and fundamental group

**Pass.** Contractibility plus Poincaré–Lefschetz duality computes the relative homology; the exact sequence of the pair gives a connected integral homology sphere as boundary. The exterior is connected: its connected boundary collar meets every exterior component adjacent to C, and a component disjoint from that collar would be separated from C and hence from the connected ambient manifold.

The Mayer–Vietoris map from H₂(E) to H₂(X) is an isomorphism because H₂(C), H₂(Y), and H₁(Y) vanish. Repeating for the twisted gluing yields the identification through the same E. Integral two-dimensional classes have oriented surface representatives; general position and local oriented resolution remove double points without changing the class. Representatives and their perturbations can be placed in the interior using a collar. Thus squares and pairings are computed in E and are unchanged under an orientation-preserving reglue. A general ambient manifold can have torsion, so the pairing there is interpreted in the usual homological sense; the stated torsion-free and unimodular conclusion is reserved for the closed simply connected case.

Van Kampen gives a quotient of π₁(E) by the normal closure of the full boundary image. Precomposition by any boundary automorphism is surjective on π₁(Y), so it changes neither this image nor its normal closure. Basepoint choices affect representatives by conjugacy, which does not affect the conclusion. The proof does not require π₁(E)=1. Ordinary invariants consequently supply no distinction here; identifying intersection forms alone is not a smooth classification theorem. The author expressly does not infer diffeomorphism or give a standalone homeomorphism proof.

### Proposition 1.1 and Corollary 1.2: exterior genus bounds

**Pass.** Positive b₂ is specified so the maximum is nonempty. An integral rational basis in E remains such a basis in every gluing. Its fixed embedded representatives bound the new minimal genera from above, and their squares stay fixed. Taking the maximum then the infimum gives exactly the stated inequality. The extended value −∞ is harmless for an upper bound. A nonempty subset of integers bounded below attains its minimum, so the author's conditional comparison with a minimum is justified.

The corollary uses upper-unbounded target J-values. Any particular finite collection of exteriors supplies a finite collection of surface-basis bounds, whose maximum is finite. Hence it cannot realize that sequence, even if all boundary maps are allowed at each of those finitely many embeddings. The argument does not supply a bound uniform over all embeddings of the abstract C. Nor is mere infinitude of a family a substitute for unbounded J-values. A negative signed value is possible already at genus zero and square one; the author's avoidance of unjustified nonnegativity is important.

### Lemmas 2.1 and 2.2: orientation and evaluations

**Pass.** Oriented universality of C applied to the simultaneously reversed pair, followed by reversing the whole decomposition, proves oriented universality of −C with the same underlying map. Reversing both domain and codomain preserves the relevant map's orientation-preserving property. This is not an identification of C and −C inside a fixed oriented ambient manifold.

For a nonzero vector δ over F₂, choosing one linear functional μ with μ(δ)=1 and taking bᵢμ realizes any finite prescribed list of evaluations. The result is valid even in dimension one. The gluing identity is linear algebra; it does not establish that these functionals occur as complement maps. Constraints involving gradings, Spin^c structures, and geometric realization are still indispensable. The zero-difference implication is an external theorem rather than a consequence of finite-dimensionality alone. The necessary nonvanishing condition in both orientations is confined to the involutive setting to which that theorem was applied.

### Lemma 3.1: parity

**Pass.** The algebraic intersection matrix is the identity. Writing each entry as positive minus negative points makes its geometric count equal to the Kronecker delta plus twice its negative count. Subtracting the number of handle pairs yields a nonnegative even integer. The empty decomposition also has complexity zero. This argument concerns excess intersections, not the number of handle pairs or the stabilization distance.

### Proposition 3.2: relative-cobordism transfer

**Pass as a conditional theorem.** The hypothesis must provide the relative h-cobordism, its product side marking, and a normal decomposition. The proof does not establish that such a cobordism exists for every arbitrary-order f. Glue along collared inclusions; the map of the incoming-end diagram to the cobordism diagram consists of homotopy equivalences on C, its side boundary, and the product exterior. Homotopy invariance of these cofibrant pushouts gives an h-cobordism after gluing. The same holds at the outgoing end. This argument does not need a simply connected exterior.

The chosen Morse function extends over the product with no new critical points, so the given spheres and all of their geometric intersections remain available. Minimization can only lower the resulting complexity. Reversing a relative cobordism interchanges its index-two and index-three data and inverts its side marking; the geometric count and handle-pair number are unchanged. Orientation and the product boundary identification must accompany this reversal, as in the proof's conventions. The surrounding simply connected normal-handle setting is essential to the definition of c_pair used here.

The selected/minimum distinction is decisive: the product has zero complexity for an identical endpoint pair, regardless of another chosen inertial cobordism's complexity. A lower bound for one induced isometry cannot be asserted for the minimum over all isometries and all h-cobordisms.

### Lemma 3.3: capping

**Pass.** Compatible boundary restrictions glue a relative diffeomorphism to the identity of the cap. Product collars permit smoothing the union. In the opposite direction, a diffeomorphism of the closed manifolds need not preserve the designated cap or its marking. The author asserts only the insufficiency of an unmarked closed diffeomorphism, not a fabricated specific smooth counterexample. For the needed closed upgrade, recoverability of the relative data is an additional theorem, not a formal property of attaching a cap.

### Proposition 4.1 and Corollary 4.2: stabilization

**Pass with the controlling definition correction.** Given an extension F at level n, the author's map is identity on E and F⁻¹ on the stabilized C. On the seam, the target relation sends f⁻¹(c) to j(f(f⁻¹(c)))=j(c), exactly the source seam relation. This checks the inverse convention for maps of arbitrary order; replacing F⁻¹ by F would fail generally. Collar straightening makes the gluing smooth. The passage from a least height m≤n to level n uses the small-ball isotopy and identity-extension observation supplied explicitly in the addendum.

The universal-candidate corollary applies this one fixed n to every embedding. A finite menu gives the maximum of finitely many finite heights, provided one member suffices in one twist. It does not cover unrestricted sequences of twists by that menu with a uniform bound. Reversal changes C#nH to (−C)#n(−H); a reflection of one sphere factor is orientation-reversing on H=S²×S² and supplies the needed oriented identification with (−C)#nH. Applying reversal twice proves equality of the two heights. The reverse implication from a uniform stabilization bound to a universal cork has not been proved and is not used.

### Proposition 5.1 and Corollary 5.2: gluing normalization

**Pass.** Restriction of an orientation-preserving diffeomorphism of either piece gives a group homomorphism on boundary mapping classes; conjugating the exterior restriction by the orientation-reversing marking still yields an orientation-preserving boundary map. Thus A and B really are subgroups of Γ. Restricting a piece-preserving diffeomorphism gives αg=hβ, hence h=αgβ⁻¹ and [h]∈A[g]B.

Conversely, the mapping-class relation supplies extendable representatives. A residual boundary isotopy can be realized in a collar (using a parameter function constant near its ends), so the boundary compatibility can be made exact. Collar straightening then glues the maps. This is a complete proof for piece-preserving diffeomorphisms; exchanging or moving the pieces lies outside the criterion. The convention includes labelled E and C and does not allow them to be swapped.

Taking g to be the identity proves that f extending over E can make the gluing ineffective despite its failure to extend over C. Isotopic boundary representatives have equivalent extension status because collar isotopy extends, so using [f] rather than f introduces no defect. The finite subgroup examples do not claim geometric realization as exterior extension groups.

## 3. External theorem and dependency audit

The paragraphs below are hypothesis checks of credited inputs. They are not new proofs of Floer theory, four-dimensional classification, stable smoothing, or cork decomposition.

1. **Yasui.** Theorem 1.3 fixes the embedded submanifold. Theorem 1.11 permits varying embeddings but its numerical hypothesis excludes a contractible W with homology-sphere boundary. Definition 2.2 and Proposition 3.2 supply the relevant genus mechanism. The author's extended-infimum formulation avoids using nonnegativity outside justified cases. [Inspected primary version](https://arxiv.org/pdf/1610.04033v3).

2. **Ladu nonuniversality.** The conventions require orientation-preserving involutions. Proposition 3.2 places the difference in reduced degree −1 and provides mod-2 invariant preservation under an isometry for closed oriented simply connected pairs with b₂⁺≥2. Corollary 1.3 covers the named family and reversals. Definitions 4.1–4.2 distinguish cork, cobordism, and endpoint-pair minima; Lemma 4.6 is the product-exterior transfer. Theorem 4.7 and Proposition 4.8 use recoverable boundary data from the invertible-cobordism construction. The article's deeper inputs are not rederived. [Inspected v3](https://arxiv.org/pdf/2311.17028v3).

3. **The orientation discrepancy remains quarantined.** The two orientation classes in the older Ladu manuscript were visually distinguished. Its stronger-looking statement is not silently reconciled with the different K3 remark. Separate preservation laws do not automatically obstruct mixed sequences. No claim resolving the orientation-flexible version is certified. The final publisher article's full text was not independently obtained, and no identity of its entire contents with the preprint is asserted. [Publisher record](https://doi.org/10.1007/s00029-025-01061-6).

4. **Ladu complexity.** Theorem 1.2 and Section 6 construct large-complexity cobordisms. The proof of Theorem 6.3 follows specified reflected isometries Rₘ and the resulting cobordisms Cₘ. It does not lower-bound every unmarked-endpoint cobordism. The distinction from handle-count stabilization complexity is explicit. Neither the Floer computation nor its dependencies are re-proved in this audit. [Inspected v2](https://arxiv.org/pdf/2501.08750v2).

5. **Stable extension.** The author uses the finite-extension statement attributed to Wall in K3 Remark 4 as an external input, and proves the embedding-independent consequence directly. Original Wall/Gompf proofs and all category refinements were not independently reconstructed. The formal conclusion remains valid whenever the specified oriented extension exists, so this dependency cannot conceal an unconditional solution.

6. **Kang and Guth–Kang.** Kang's Theorem 1.1 is relative and Corollary 1.2 is an absolute boundary example; Question 1 identifies the closed step. Guth–Kang's Theorem 1.8 remains a boundary-manifold result after one stabilization, not unbounded closed-pair distance. Its accepted v2 also explains that Kang's proof relies on results from this splitting paper, so these are related inputs rather than two fully independent verifications. [Kang v3](https://arxiv.org/pdf/2210.07510v3); [Guth–Kang v2](https://arxiv.org/pdf/2404.06618v2).

7. **Pair-dependent and finite-family corks.** Melvin–Schwartz's relative theorem uses simply connected manifolds with homology-sphere boundaries. Its finite theorem depends on the selected finite family and uses powers of a boundary map. The proof routes through consolidation and prior handlebody results. Those foundations are external here. The v2 history expressly removes erroneous infinite-order results from v1; none is used in the packet. [Final author v2](https://arxiv.org/pdf/1902.02840v2); [version notice](https://arxiv.org/abs/1902.02840).

8. **Strong corks.** Mukohara's definitions and main statements concern nonextension over specified classes of fillings. They are not universality theorems about all closed ambient exotic pairs and do not close a missing step in this packet. This is a scope check only. [Inspected v3](https://arxiv.org/pdf/2601.02230v3).

The elementary algebraic-topology inputs are Poincaré–Lefschetz duality, exact sequences, van Kampen, surface general position, and collar/isotopy facts. Deep existence and classification inputs include the source papers' cited work of Freedman, Wall/Gompf, Curtis–Freedman–Hsiang–Stong, Matveyev, Morgan–Szabó, Akbulut–Ruberman, and Floer/geography foundations. Their original proofs were not all separately audited. No conclusion in this report upgrades a cited input into a formally checked theorem.

## 4. Why five approaches justify only unresolved 5/5

1. **Adjunction:** the authored bound is genuinely proved, but varies with the exterior. Missing: a uniform geometric bound across all embeddings of the fixed abstract C, or another embedding-independent obstruction applicable to every candidate.
2. **Floer:** zero difference is a scoped obstruction; dimension alone is defeated by the evaluation lemma. Missing: a restriction on realizable complement maps strong enough to obstruct every possible fixed cork, with arbitrary-order and orientation hypotheses handled.
3. **Cobordism complexity:** a fixed relative model gives an upper bound. Missing: an unbounded sequence of minimum complexities of closed unmarked pairs, together with the appropriate finite relative models. Chosen cobordisms and arbitrary caps do not fill this gap.
4. **Stabilization:** a fixed finite height bounds all its twists. Missing: unbounded stabilization distance among the required closed simply connected pairs. Boundary examples and stabilized diffeomorphism phenomena do not establish it.
5. **Construction:** the double-coset criterion is exact only after both pieces are fixed. Missing: one compact C, one f, and compatible embeddings for all exotic pairs. Finite-family constructions and piece-preserving classifications do not supply that uniform model.

Each attempt has a mathematical mechanism, a proved deduction or checked external input, an adversarial failure test, and an explicit missing step. None supplies the witness or universal obstruction demanded by the target. Recording unsolved 5/5 accurately describes this investigation; it does not assert that the entire field lacks a later solution.

## 5. Computation and deliberate-negative controls

The author checker was inspected before execution. It uses Python's standard library and exact arithmetic, has no source-paper dependencies, and writes only standard output. Its 226,926 assertions replayed byte-for-byte. The independent checker uses a dihedral presentation rather than the author's permutation-group implementation and coordinate tuples rather than its bit encoding. It passes 22,339 checks, including 13 named negative controls.

Independent groups cover direct double-coset compatibility over all ten subgroups of the order-eight dihedral group; normal-closure invariance under boundary-group automorphisms; signed genus inequalities; parity including the empty decomposition; arbitrary-order inverse gluing; F₂ evaluations; the inapplicable Yasui inequality; and finite logical models of the embedding quantifiers. The negative controls expose wrong factor order, nonextension/effectiveness conflation, use of F instead of F⁻¹, involution overreach, handle/intersection conflation, selected/minimum conflation, unjustified nonnegativity, unsupported uniform embedding bounds, the dimension shortcut, mixed-sequence overreach, pairwise/global stabilization confusion, finite-family quantifier reversal, and the knowledge/existence confusion.

Some negative controls are deliberately finite countermodels to logical implications. They are labelled as such and are not claimed to arise from smooth manifolds. The epistemic control records the logical countermodel explicitly; it is not a computation deciding extension existence. Passing many assertions is not a proof of the geometric hypotheses, and the count has no statistical or probabilistic meaning.

The read-only verifier checks the supplied freeze against every file, the original manifest entries, the original checksum list, both saved outputs, and all original hashes again after execution. Six additional integrity mutation tests reject changed author proof, changed manifest, an unexpected file, a missing file, changed author results, and changed independent results. Positive baselines pass before and after these temporary-copy mutations. Literature retrieval is documented separately and is not silently rerun by that verifier. Re-running the tests does not access datasets or papers.

## 6. Publication and use limits

The public-safe audit contains only authored review and code plus public source titles, URLs, hashes, sizes, bounded inspection descriptions, and status metadata. It contains no source PDFs, extracts, images, corpus records, credentials, private personal data, or private coordination records. No remote modification or publication was performed by the auditor.

Before any publication, preserve the original freeze and include the controlling addendum prominently. The original author status says the audit is pending because it predates this separate review; this audit supplies the later verdict without rewriting history. If any author file is changed, this exact-freeze verdict no longer binds the changed packet without revalidation. No novelty, priority, global-openness, formal-proof, human-review, or complete-literature claim is authorized by this result.
