# Independent audit of the Artin–Tate compact generator obstruction

## Verdict and exact scope

**ACCEPT the stated structural partial result.** The reviewed proof establishes that each of the following presentable stable categories has a countable compact generating set and no finite compact generating set:

- A = Mod_{SH(R)^AT}(1₂)[a⁻¹], with the BHS i2 convention;
- D = A₂^∧, where derived 2-completion is performed after forming A, exactly as defined in the proof.

Consequently neither is equivalent, even as an unstructured presentable stable category, to Mod_R for an E₁-ring spectrum R. The finite-object spectral-category exclusion and the stated affine spectral-scheme exclusion follow as well. The separate compact quotient correction is also accepted, with its explicit compact tensor-ideal interpretation.

This is not a solution of the recognizable intrinsic-model problem. The filtered coefficient algebra, its deformation data, the comparison functors, and the geometric interpretation remain unidentified by this argument. Retain **partial progress, one proof turn out of five**. No novelty certification is made: the obstruction is a short deduction from credited BHS inputs. This audit does not identify D with a different order of completion and localization.

## Distributed proofs and acceptance scope

The review applies to these exact UTF-8 files in this edition:

- [PROOF.md](PROOF.md): 11,390 bytes; SHA-256 `6bd064035b553aca0c5ec754d8713cfd3b3ffc4a9b043ace43bf688ea69889db`.
- [QUOTIENT_CORRECTION.md](QUOTIENT_CORRECTION.md): 6,072 bytes; SHA-256 `2e913157670bb7c541b21087ef9eec8bea4aca9b9c11f0a8bae6f604400289f4`.

Any mathematical change requires renewed review. Both arguments were independently read in full. The compact tensor ideal lies inside C^ω and permits only compact tensor factors. The proof includes the degree-zero cobar explanation needed for π₀B = F₂. This edition retains all accepted mathematical arguments and source qualifications, while presenting the quotient correction as a standalone note. The audit is AI-assisted and unrefereed; it does not represent external human peer review, journal acceptance or formal proof-assistant certification.

## Primary sources and inspection scope

The mathematical reference is R. Burklund, J. Hahn, A. Senger, *Galois reconstruction of Artin–Tate R-motivic spectra*, [arXiv:2010.10325v2](https://arxiv.org/abs/2010.10325v2), published in [Geometry & Topology 30 (2026), 1625–1717](https://doi.org/10.2140/gt.2026.30.1625).

The retained arXiv PDF is 1,323,629 bytes with SHA-256 `f74a6f89b5774c5e022750ddd46cbc8cb77abd6fddb9485746171d52586e2ef8`. The retained publisher PDF is 1,072,734 bytes with SHA-256 `7077369ab7bbc89b23bc71159d7dda616de19390837fe48a22e2185c4978b8de`. The independent audit extracted both PDFs and checked the relevant source statements. It also visually inspected the retained arXiv page images 16, 53 and 62 and the publisher PDF page images 20, 65 and 76. These contain the category convention, the special-fiber formula, and the precise vanishing region. The latter journal pages are 1643, 1688 and 1699. The arXiv and journal statements used here agree.

Additional source checks cover arXiv pages 5–6 (compact trigraded spheres and their coordinates), 14 (Question 1.31), 17 (complex base change of ta), 30 (the Cta-module comparison), 54 (the filtered model and comparison map), and 60–61 (the odd-prime splitting). The live arXiv metadata was checked and records v2 dated 30 June 2022 and the 2026 publication. Some live page requests failed; the original AIM statement and the relevant Borel-deformation passage were inspected in the retained source copies instead. No failed request is represented as successful retrieval.

The source problem is [AIM Equivariant Techniques, Problem 3.2](http://aimpl.org/equivstable/3/). It asks about inversion of a. The retained AIM HTML has SHA-256 `a8b9969c825a3bd05926db77d0779a627f399a67590e166e182e3e7285ed6146`. The retained *A deformation of Borel equivariant homotopy* PDF, arXiv:2308.01873, has SHA-256 `2d504ca5820a439afd117272356370df7925fe12c7ed320dbdef1fa710119a4c`; its page 6 distinguishes the remaining a-local problem from the a-complete construction. This targeted inspection is not an exhaustive literature or novelty search.

## Check 1 Category conventions and compactness

Let C₀ = SH(R)^AT and C = Mod_{C₀}(1₂). BHS distinguishes this module category from the full subcategory of complete objects. The distinction matters: a completed unit need not be compact in the full completion, whereas the free rank-one module is compact in C.

More directly, the free/forgetful adjunction identifies maps out of a free sphere module with maps out of the underlying compact sphere in C₀. The forgetful functor preserves filtered colimits. Consequently the free sphere modules are compact. Their joint detection of zero objects also follows through this adjunction. This verifies the proof's use of compact generators without assuming compactness of 1₂ as an object of C₀.

The a-local objects are those for which the natural action of a is an equivalence. Tensoring by the invertible source of a preserves colimits, so a-local objects are closed under colimits in C. The fully faithful local inclusion therefore preserves filtered colimits. The localization adjunction carries the compact sphere generators to compact generators of A.

The q-shift becomes trivial because a has degree (0,−1,0). Thus the integer-indexed twists T_w suffice, with ordinary suspensions understood. Compact objects are in the ordinary thick closure of these generators. Every finite thick construction uses only a finite subset of weights. Retracts do not change this finite-subset statement. No tensor-ideal closure is used in this step.

## Check 2 Exact test object and grading

The object B is the a-inverted cofiber of ta, not the cofiber of a. BHS's commutative-algebra construction supplies its ring structure. Corollary 7.1 supplies the homotopy computation. Its degree-zero term is F₂: in internal degree zero the normalized BP cobar terms of positive cohomological degree vanish, and the polynomial geometric-fixed-point factor contributes only its constant term to total degree zero. In particular B is nonzero.

Theorem 10.1(8) explicitly applies after a-inversion and gives zero homotopy at every negative weight, uniformly in both remaining coordinates. This avoids an unproved interchange of a-localization with an infinite limit. The journal counterpart is Theorem 10.1(viii).

For B(N) = T_N ⊗ B, invertibility of T_N implies B(N) ≠ 0. Moving the target twist to the source gives

π_k Map_A(T_w, B(N)) = π_{k,0,w−N}B.

The sign is w−N. Choosing N strictly larger than all weights used in a compact P therefore makes every homotopy group of each relevant mapping spectrum vanish. This is full mapping-spectrum orthogonality, not just vanishing of degree-zero maps. The ordinary mapping spectra specified in the proof avoid any ambiguity with BHS's C₂-enriched notation.

The class of sources right-orthogonal to B(N) is thick. Hence Map_A(P,B(N)) is zero. A generator cannot have such a nonzero right-orthogonal object. A finite collection of compact generators would have a compact direct sum, so it too is excluded. The existing countable generating set proves that the minimum cardinality is exactly ℵ₀. The optional observation that B(N) itself is compact in A is valid: B is a cofiber of compact objects, and invertible twists preserve compactness.

## Check 3 The derived completion extension

This extension is accepted on its own definition of D. It does not reuse compactness of the completed sphere and does not commute the two localizations.

To justify the completion formalism explicitly, the 2-invertible objects of A form the localizing subcategory generated by T_w[1/2]. Their right orthogonal is an accessible reflective stable subcategory. The cofiber of a completion unit X → L₂X belongs to that 2-invertible subcategory. This also establishes the asserted mod-2 equivalence. That subcategory is a tensor ideal, so the described completed tensor product is legitimate.

For H_w = cofib(2:T_w→T_w), the uniform assertion is 4·id = 0, rather than an unjustified 2·id = 0. In the cofiber triangle, 2·id_{H_w} factors through the connecting morphism δ because its restriction to T_w is zero. A second multiplication by 2 then vanishes, because (Σ2)δ = 0. This argument works in the homotopy category of any stable category.

If Z is 2-invertible, multiplication by 2 on Map(Z,H_w) is invertible through its source, while multiplication by 4 is null through its target. Thus this mapping spectrum is zero and H_w is complete. Maps from H_w also vanish into a 2-invertible target: apply Map(−,Z) to the defining Moore cofiber triangle. Applied to the cofiber of X→L₂X, this proves

Map_A(H_w,X) ≃ Map_A(H_w,L₂X).

The author's equivalent finite-Moore-duality argument is sound. Combined with compactness of H_w in A, this identity proves compactness in D despite the fact that colimits in D must be completed. If a complete Y receives no maps from any suspension of any H_w, multiplication by 2 is an equivalence on all Map_A(T_w,Y), hence on Y. An object that is both complete and 2-invertible is zero. Therefore the H_w compactly generate D.

There is no unjustified inference from additive characteristic alone in the next step. The element 2 times the unit is null in Map_A(T₀,B), and B is a unital algebra. Multiplication sends this null unit element to the actual endomorphism 2·id_B. Therefore that endomorphism is null. The same holds on each B(N), so every B(N) is already complete and stays nonzero in the full subcategory D.

Finally, negative-weight orthogonality from T_w to B(N) implies orthogonality from H_w by the cofiber mapping sequence. Every compact object of D uses only finitely many H_w. The same finite-weight argument therefore excludes a finite compact generating set in D, while the countable one is established above.

## Check 4 Morita and geometric consequences

For any E₁-ring spectrum R, its free module R is a compact generator of Mod_R. Under an equivalence of presentable stable categories, compactness and generation are invariant. The obstruction therefore needs no compatibility with the unit, ta, weight twists or tensor products. This is stronger than merely observing that a distinguished parameter has nonzero cofiber.

For a spectral category with finitely many objects, the finite sum of the representables is a compact generator; that model is likewise excluded. For an affine spectral scheme, quasi-coherent modules have the form Mod_R. The proof makes no claim ruling out all non-affine schemes, stacks, filtered algebras or countably many-object spectral categories.

## Check 5 The compact quotient correction

The kernel of a-inversion is generated as a localizing subcategory by all compact objects Ca⊗S₂^{r,q,w}. The compactly generated localization theorem gives the idempotent-completed quotient of C^ω by their ordinary thick closure. Since C^ω itself is thickly generated by sphere twists, this denominator equals the thick tensor ideal of Ca inside C^ω. A single unqualified ordinary thick(Ca) is insufficient.

The reviewed strictness witness is valid. Set E = Ca⊗Cta and extend scalars to E-modules. Complex base change identifies Ca with the finite étale orbit algebra, gives Ca⊗Ca ≃ Ca⊕Ca, and carries ta to τ. Thus the scalar-extension images of Ca and its weight-one twist are E⊕E and E(1)⊕E(1), respectively.

The E-module E(1) is nonzero: under the complex comparison it is an invertible module twist of nonzero Cτ, whose degree-zero Ext class is nonzero. Its mapping spectrum from E has homotopy π^C_{k,−1}Cτ. Equivalently, apply BHS Theorem 10.1(5) to E at real weight −1: the necessary interval −1 ≤ p+q ≤ −2 is empty. Every one of these homotopy groups therefore vanishes.

If E(1) belonged to thick(E), its orthogonality to E would extend to all sources in thick(E), including E(1), forcing its identity to be zero. This contradicts nonzeroness. Since E(1) is a retract of E(1)⊕E(1), scalar extension proves

Ca⊗S₂^{0,0,1} ∉ ordinary thick(Ca).

The same twist belongs to the tensor ideal and is killed by a-localization. This proves actual strictness, not merely the possibility that tensor-ideal notation matters. The correction distinguishes the two interpretations explicitly: a tensor-ideal denominator is correct, while an ordinary-thick denominator is false.

## Check 6 Known models and residual scope

The filtered-module presentation is already given in the proof of BHS Proposition 7.6. It is a valid, nonempty mathematical presentation by an explicitly constructed filtered coefficient ring, but repackaging that known presentation does not supply the requested intrinsic recognition. The order of levelwise geometric fixed points and infinite totalization cannot be silently interchanged; BHS gives comparison maps, not the claimed equivalence such an interchange would require.

The retained odd-prime consequence follows from the central-idempotent split, the vanishing of a on the η-complete factor, and its invertibility on the real-realization factor. The two complex factors need not form a componentwise monoidal product. This is credited known/formal background and does not solve the two-primary residual.

The new obstruction does not identify a deformation solely by its generic and special fibers, does not establish an integral arithmetic-gluing statement, and does not transfer an a-complete result to the a-inverted problem.

## Verification and limitations

The mathematical acceptance rests on the categorical arguments and the exact cited primary-source inputs. Public-source hashes, PDF extraction and source-page inspection establish source identity and inspection scope only. They are not a computation of motivic homotopy groups, a formal proof-assistant certification, a full reconstruction of BHS, or a proof of novelty.

The proof and quotient correction are accepted at the distributed hashes above with no outstanding mathematical correction required for their stated scope.
