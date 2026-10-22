# Independent audit: modern K3 Problem 4.122

Audit date: 2026-10-05. Target: UnsolvedMath ID 2998, rank 695.

## Verdict and exact object reviewed

**PASS for the stated partial mathematical results, with one nonblocking historical-verifier defect.** There is no complete solution of the fixed branching-surface problem here. The appropriate outcome is **unsolved, five approaches completed (5/5)**. No novelty or universal literature-openness conclusion is certified.

The reviewer was not involved in the authored packet. All nine frozen author files, including the manifest itself, were checked before and after review and remained byte-for-byte unchanged. No helpers were used and no remote writes were performed. Fresh public-source retrieval, local reading, original calculations, and temporary-copy integrity attacks were used.

The controlling author binding is:

- `AUTHOR_MANIFEST.json`: 1,619 bytes; SHA-256 `e67ac4e9f37d89fce822f00e4e166b20f21d1051c41e5e2acd595a5709cd95c1`.
- Eight payload files plus that manifest: nine bound files in total.
- `RESULTS.md`: 17,479 bytes; SHA-256 `7ed5752a731b163c34a44864a5ebf3ae07706bba8dedb3883e08f2f31a4e5bbf`.
- Canonical author-tree SHA-256: `9b4de33360ac75d984ac9dd3722570bf6094642d880902e75e5853f69bc02c8c`.

`AUDIT_BINDING.json` lists every bound path, size, and digest and defines the canonical tree encoding. `AUDIT_MANIFEST.json` binds this audit's own files. Those are distinct bindings: the original author manifest is not rewritten to claim a later review.

**Release gate:** `binding_checks.py`, together with the audit manifest check, supersedes the original author's `verify_manifest.py` for deciding whether the reviewed bytes are present. The latter remains untouched as a historical artifact and is not sufficient for release verification.

## 1. Target identity, category, and quantifiers

The April 2026 K3 author PDF was independently retrieved and its target pages were independently rendered. Printed pages 291–292 are PDF pages 291–292 (one-based). Problem 4.122 concerns one fixed branching surface in the four-sphere with all closed orientable four-manifolds among its branched-cover total spaces. The degree and monodromy may vary. The same item discusses the four-ball ribbon theorem and the signature obstruction to connectedness. This verifies the modern problem identity; 1997 Kirby numbering is not being substituted. [K3]

The live catalog detail URL was attempted independently and did not load in the web tool. An indexed catalog listing corroborates the modern label and question. The supplied ID/rank mapping is also consistent with the previously selected local public-catalog record. This audit does not independently refresh the repository queue, repeat repository-wide duplicate searches, or rehash the large upstream corpus. Those parts of `SOURCE_METADATA.json` remain the author's explicitly described provenance, not newly certified observations of this reviewer.

The short K3 question does not itself spell out every local-model convention. The originating PZ paper introduces the problem after the smooth representation theorem, describes smooth power-map-type branching, and treats the actual branch set as minimal. IP explicitly works with PL maps and locally flat PL surfaces. These support the packet's ordinary smooth/locally flat PL interpretation. [PZ, IP]

The packet appropriately fixes stronger explicit hypotheses for its conclusions:

1. A finite disjoint union of closed, embedded, locally flat surfaces, with smooth standard transverse power-map models in the smooth version.
2. The *exact* branch locus, so every downstairs component has nonidentity meridional monodromy in every cover under consideration.
3. Compatible orientations away from the locus, extended over the total manifold.
4. A connected total space for the obstruction test manifolds.

These hypotheses are essential to the audit. An embedded topological surface with cone points need not be locally flat. Immersed nodal surfaces, arbitrary two-complexes, wild embeddings, and general singular coverings do not become covered by calling them surfaces. GKS treats singular categories separately and includes additional signature terms. Neither this audit nor the packet transfers the locally flat formulas into those categories. If a broader interpretation of the abbreviated catalog target is intended, these results remain partials for the stated subcategory, not a resolution of the broader question. [GKS]

Likewise, allowing a fixed marked surface to contain inactive dummy components changes the exact-locus problem. The packet explicitly excludes that change. Ordinary unbranched sheets *over an active component* are allowed and are correctly counted.

## 2. Signature dependency and the denominator discrepancy

### Verified source distinction

All six cited source PDFs were freshly downloaded from their public URLs. Every new byte count and SHA-256 matches the author's recorded private PDF. This establishes source-byte provenance without placing any PDF, extracted text, or page image in the audit package. `SOURCE_RETRIEVAL_CHECKS.json` contains the public metadata.

The reviewer checked Viro's definitions, the four-dimensional specialization, and original formulas (17)–(18), including a fresh rendering of the scan's final page. With an upstairs ramification component, the coefficient multiplying its embedded normal Euler number is `(k^2-1)/3`. With the corresponding downstairs immersion's normal Euler number, it is `(k^2-1)/(3k)`. The latter normal Euler number belongs to an immersion of the entire upstairs surface, so its multiplicity over a downstairs component must still be accounted for. [Viro]

GKS Theorem 1 has the upstairs coefficient with denominator 3. Its proof's final display has denominator `3k` while retaining the upstairs self-intersection notation. The reviewer verified this independently in both arXiv v3 and the publisher's live HTML. The mismatch is genuinely in the source, not an OCR artifact. The exact correction to that display is to replace both displayed `3k` denominators by 3 when the self-intersections remain upstairs. Alternatively, a downstairs immersion must replace the associated quantity if retaining `3k`. No official erratum is asserted. [GKS]

The frozen packet already discloses the discrepancy and uses the correct coefficient. **No packet correction is required.** Substituting the inconsistent proof display into its conversion would introduce an extra division by `k`; that would affect the quantitative signature formula and its simple-cover specialization. It is not an alternative convention compatible with the quantities the display names.

### Independent normal-bundle conversion

For a connected component `A` above `S_i`, let `m` be the degree of the surface covering `A -> S_i` and `k` its transverse degree. Pull back the downstairs normal disc bundle to `A`. The fibre power map has degree `k`, so its circle-bundle Euler obstruction is `k` times that of the upstairs normal bundle. Evaluation gives

`k e(A in W) = m e_i`.

For a nonorientable component this is an equality with the relevant orientation local systems before evaluation. The ambient orientation identifies tangent and normal orientation systems; pullback of the orientation system agrees with the one on `A`. Equivalently, the statement can be checked on orientation double covers and divided by the same degree on both sides. There is no extra factor of two. Compatibility of ambient orientations yields the positive sign in the equality.

For fixed `i,k`, the sum of the surface-covering degrees `m` is exactly the number `c_(i,k)` of points of transverse degree `k` over a typical point of `S_i`, equivalently the number of length-`k` meridian cycles. Therefore the aggregate upstairs Euler number is `c_(i,k) e_i/k`. Applying Viro or the stated GKS theorem yields

`sigma(W) = -sum_i e_i sum_k c_(i,k)(k^2-1)/(3k)`.

This proves the packet's conversion, conditional on the cited signature theorem. In particular a simple transposition contributes `e_i/2` to the unsigned correction; two disjoint transpositions contribute `e_i`. The independent controls detect both omission and duplication of the index divisor and a sign reversal.

The full Viro index-theoretic proof and GKS's supporting smoothing theorems were not reconstructed from first principles. Their applicable theorem statements are explicit dependencies, not computationally established facts. GKS's reduction, normal-Euler convention, smoothing/product step, and final computation were read; the denominator correction agrees with Viro's upstairs formulation. The smooth/PL partials do not require an unproved extension by this reviewer to a singular or wild category.

## 3. Independent proof checks of the deductions

### 3.1 Cycle data and Euler characteristic

For a meridian permutation on `d` sheets, the number of preimages of a point of `S_i` is the number of cycles `c_i`, including fixed points. Transport along the surface can conjugate or invert the meridian but cannot change cycle lengths. Its full inverse image is thus an unbranched `c_i`-sheeted surface cover. In the complement there are `d` sheets.

One can use compact exteriors and normal disc bundles: the common boundaries are closed three-manifolds with Euler characteristic zero; the normal bundles retract to the corresponding surfaces. Hence

`chi(W) = d(2-sum_i chi_i) + sum_i c_i chi_i`.

Writing `r_i=d-c_i` gives the author's formula. For an exact nonempty locus, `1 <= r_i <= d-1` and each signature weight is positive. The lower bound follows from the presence of at least one nontrivial cycle; the upper bound follows from the presence of at least one cycle. The computation neither assumes regularity nor excludes fixed points. **Proposition 2.1 passes.**

### 3.2 Opposite normal-Euler signs

If every `e_i` vanishes, the signature formula rules out either orientation of CP2. If all nonzero `e_i` have the same sign, strict positivity of all the corresponding weights prevents cancellation, ruling out S4. These two tests work even if the universality question does not prescribe a chosen orientation on each total manifold. Reversing the orientation of CP2 never changes a nonzero signature to zero.

For a closed orientable component in S4, its normal Euler number is its integral self-intersection; its homology class vanishes since `H_2(S4;Z)=0`. Thus the required opposite-sign components are both nonorientable. This is a necessity assertion only. The exact-locus assumption is necessary for the S4 cancellation argument; the author says so. **Theorem 3.1 passes.**

### 3.3 Positive Euler mass and component count

For `chi_i>0`, multiplying `r_i <= d-1` by the negative coefficient `-chi_i` gives a lower bound for the Euler contribution. For `chi_i<=0`, the corresponding contribution is nonnegative and may be dropped. Thus

`chi(W) >= 2d-(d-1)P`, where `P=sum_i max(chi_i,0)`.

If `P<=2`, the right side is positive, excluding S1 x S3. The empty locus cannot be universal either; even a degree-one case has Euler characteristic 2 and the same exclusion. Hence `P>=3` is necessary.

A connected closed nonorientable surface has Euler characteristic at most one. If there were just two components, the opposite-sign requirement forces both to be nonorientable, and then `P<=2`. Zero or one component already fails the signature tests. Therefore at least three components are necessary. This uses the classification of closed surfaces only for their possible positive Euler characteristics; it makes no geometric existence claim about candidates with three components.

For `W_g=#^g(S1 x S3)`, connected-sum additivity gives `chi(W_g)=2-2g`. Substitution and division by positive `P-2` gives exactly

`d >= ceil(1+2g/(P-2))`.

The ceiling and direction are correct. **Proposition 4.1 and Corollaries 4.2–4.4 pass.**

### 3.4 Unbounded degree and the simple-only obstruction

A compact smooth or locally flat PL exterior has finitely generated fundamental group. If it has `g` generators, at most `(d!)^g` homomorphisms to the finite group `Sym(d)` exist. Requiring relations, transitivity, and peripheral compatibility only reduces this finite list. Ordinary covers are determined up to equivalence by monodromy; in the standard branched category the completion is determined by that ordinary cover. IP explicitly uses this uniqueness in the PL category, and PZ uses its smooth analogue. GKS also states the ordinary-cover extension in its topological setup. [IP, PZ, GKS]

The finiteness assertion is consequently valid in the stated category and for the corresponding equivalence of total spaces. It should not be inflated into a count of arbitrary maps with nonstandard singular smooth structures. A bounded finite set of degrees still gives only finitely many total-space types. The `W_g` have distinct first Betti numbers, so they already require unbounded degree. The explicit Euler growth bound supplies a second route to that conclusion once `P>2` is known.

For simple covers, each active meridian is one transposition: `r_i=1` and `a_i=1/2`. Therefore `chi(W)=2d-chi(S)` and `sigma(W)=-e(S)/2`. Degree at least two bounds the former below while the `W_g` Euler characteristics tend to negative infinity; the latter cannot include both zero and nonzero signatures. These are independent valid obstructions.

Having all *local* ramification indices at most two does not imply simplicity: multiple transpositions over the same component are allowed. The packet and controls preserve that distinction. **Propositions 5.1–5.2 pass.**

### 3.5 Complement-group largeness

For a cover with total space `W_2=#^2(S1 x S3)`, the preimage `A=f^-1(S)` is a disjoint union of closed locally flat codimension-two submanifolds, including the unbranched preimage components. Removing these from connected `W_2` does not disconnect it. In the smooth category this follows from path general position; the locally flat statement follows by local path adjustments in product charts.

The connected ordinary complement cover therefore identifies `pi_1(W_2-A)` with an index-`d` subgroup of the downstairs complement group. Inclusion into `W_2` is surjective on fundamental groups. In addition to general position, this can be seen without smooth transversality by restoring the normal disc bundles: each boundary circle bundle maps surjectively to the fundamental group of its base surface, so van Kampen creates no new generators. It may kill meridians. The completed group is `pi_1(W_2)=F_2`.

Thus an index-`d` subgroup surjects onto `F_2`, precisely the stated definition of largeness. Finite groups cannot have such a quotient. If the original group is virtually solvable, so are its subgroups and quotients; `F_2` is not virtually solvable, since every finite-index subgroup has free rank at least two. This excludes the claimed group classes.

The converse is not proved: a chosen free quotient need not be the quotient obtained by the particular meridians filled in a branched completion, and a group alone does not classify smooth four-manifolds. **Theorem 6.1 passes.**

### 3.6 Doubling and missing relative data

Doubling a proper orientable surface along its boundary gives a closed orientable surface. For the PZ three-component type, the annulus doubles to a torus and each disc doubles to a sphere. Every such component has normal Euler number zero in S4. Consequently every ordinary branched cover with that doubled branch locus has signature zero, independent of degree and simplicity. It cannot cover all closed orientable four-manifolds.

If a particular cover is doubled, its total space is the oriented double `M union_boundary (-M)`. Its signature is also zero by additivity, or by the orientation-reversing involution. This verifies the direct-doubling obstruction independently of the geometry of the PZ diagram. A general cap is not a double, so this does not rule out every fixed-cap construction.

The packet correctly identifies missing data for an alternative gluing strategy: equal degrees, boundary monodromy agreement under one sheet identification, an actual lift with the desired gluing diffeomorphism, and preservation of a fixed embedded branch surface with exact active components. The existence of arbitrary boundary link covers does not provide these simultaneous conditions. Orientable halves that glue to an orientable closed surface are already excluded. **Proposition 7.1 and the stated gluing gap pass.**

## 4. Source theorem hypotheses versus a solution

- **IP:** Closed connected orientable PL four-manifolds admit simple degree-five coverings with locally flat PL branch surfaces. The surface is allowed to vary with the manifold. The theorem does not assert one fixed surface. The definitions and theorem were read; the full node-elimination diagrams were not independently reconstructed. [IP]
- **PZ:** The fixed orientable ribbon surface represents compact orientable four-dimensional handlebodies with one zero-handle and handles of indices one and two. Its concluding section states the reduction to an annulus and two discs and separately discusses an index-two-only modification. This is a proper four-ball theorem, not an arbitrary closed-manifold extension theorem. Definitions, introductory theorem, and concluding statements were checked; the full diagrammatic construction was not certified. [PZ]
- **BPZ 2026:** Theorem A assumes closed connected oriented PL `M,N`, no one- or three-handles in `N`, and degree `d>=4`. It compares a scaled intersection lattice with that of `M`. Its embedded locally flat surface refinement requires `d>=5`; the degree-four refinement permits transverse double points. The branch set is variable. This distinction prevents the later result from being mistaken for a fixed embedded-surface solution. Introduction, theorem and corollaries were read; its full proof was not audited. [BPZ]
- **Viro/GKS:** The precise local-flatness, orientation and normal-Euler hypotheses are handled in Sections 1–2 above. The singular dihedral theorem is not substituted for the ordinary locally flat theorem. [Viro, GKS]

Targeted public searches found the posed K3 problem and the cited representation work, not a primary fixed-locus resolution. This is a bounded search observation. It is neither a proof that no resolution exists nor an assertion that all the packet's deductions are new.

## 5. Computation and negative controls

The author's control script was run only in a separate temporary directory. Its regenerated JSON was byte-identical to the frozen output, SHA-256 `901afdc58d473a66ca58fa03f511e59a844299199b6b8e50dd473c64da4b0e3e`. The author's 257,996 counted cases reproduce: 1,596 partition profiles; 162,000 Euler inequalities; 6,540 same-sign pairs; 58,860 two-nonorientable bounds; and 29,000 degree-growth checks.

The independent implementation imports no author code. It computes actual permutation cycle decompositions, evaluates weights as `(d-sum(1/k))/3`, evaluates Euler characteristic by the stratified expression, and uses a generating-function partition count. Its ranges and exact results are in `INDEPENDENT_CONTROL_RESULTS.json`:

- All 46,233 permutations of degrees 1–8, producing 66 degree-labelled cycle types; cycle-type multiplicities checked against the factorial formula.
- Nine partition-count comparisons, including the author's full degree-1–18 count.
- 437,400 Euler-bound cases: degrees 2–10, three Euler entries in `{-3,-2,-1,0,1,2}`, and all nontrivial orbit counts.
- 23,820 same-sign tests and 38,906 two-nonorientable Euler tests using independently obtained cycle types.
- 1,833 integer-compatible normal-Euler conversion tests.
- 90,000 exact degree-bound equivalences; three normalization cases; 99 all-orientable signature cases.

These counts are different kinds of checks; their sum is not a count of distinct covers or mathematical examples.

Ten mathematical negative controls reject: omitting the downstairs index divisor; dividing by it twice; reversing the signature sign; forgetting fixed points; equating index-two-only with simple; dropping exact-locus positivity; promoting scalar restrictions to global nonexistence; forgetting the connected-sum Euler correction; inferring transitivity from nontrivial meridians; and treating all index-two covers as having the same signature weight.

The degree-three scalar profile with Euler data `(1,1,2)`, normal Euler data `(2,-2,0)`, and meridian cycle types `(2,1),(2,1),(3)` does give formal `chi=0` and `sigma=0`. This only disproves a claim that these scalar tests leave no formal possibilities. **It neither establishes nor refutes a geometric realization**, much less identifies a resulting manifold or solves universality. Similarly the transitivity negative test checks a permutation action, not a complement representation for a particular embedded surface.

Seven integrity negative controls reject a size-changing payload mutation, a same-length payload mutation, a missing file, an unlisted nested manifest, a matching-byte payload symlink, a matching-byte manifest symlink, and an altered manifest. They operate solely on temporary copies and verify that the actual frozen author tree remains unchanged.

No computation certifies the imported signature theorem, a surface embedding, global peripheral compatibility, a branched completion, smooth structure, or a universal construction.

## 6. Historical verifier defect and exact remedy

In `author/verify_manifest.py`, the file-set enumeration omits a path whenever its *basename* is `AUTHOR_MANIFEST.json`. It therefore ignores not only the intended root manifest but any unexpected nested file with that name.

Confirmed negative case: in a temporary copy, add `unlisted/AUTHOR_MANIFEST.json` containing the 19 UTF-8 bytes `{"unlisted": true}` followed by a newline. The frozen historical verifier exits successfully even though this extra file is not listed by the manifest. `VERIFIER_HARDENING_CHECK.json` records the exact added-file hash, bytes, result and controlling replacement.

The actual reviewed tree has no such file, so this is not a provenance mismatch or a mathematical error. The strict `binding_checks.py` rejects that exact case because it includes every file, excludes no path by basename, verifies the supplied root-manifest hash, rejects symlinks, and compares all listed sizes and hashes. **This strict check is the controlling release verification.** It supersedes the historical verifier's path acceptance without modifying the frozen historical code. A future author revision could instead exclude only the exact root manifest path, but that would require a new freeze and binding.

Affected dependency: trust in the historical file-set checker alone. Unaffected: the byte-exact binding established here, the mathematics, source retrieval matches, and arithmetic outputs. No substantive mathematical correction was found.

## 7. Five-approach disposition and release limits

The approach record contains five meaningfully different attempted routes, each with work, a result, and an unresolved step:

1. Fixed-degree representation and monodromy: bounded-degree finiteness and simple-only failure; no surface-preserving universalization.
2. Signature and normal bundles: required opposite signs; mixed signs remain.
3. Euler characteristic and small surfaces: positive mass and component/degree bounds; surviving scalar profiles remain.
4. Complement groups: largeness is required; meridional quotient and manifold realization remain.
5. Relative ribbon construction and gluing: doubling fails; a fixed compatible nonorientable cap system remains unconstructed.

There is overlap in dependencies between routes 1–3, but distinct mechanisms and stopping points justify five recorded approaches. This is not evidence of five solved problems or of an exhaustive classification. Recommended disposition: **unsolved 5/5, useful partial results retained**.

This audit authorizes no expansion of the claim. Any changed author byte, unstated singular-category extension, sufficiency statement, novelty claim, global-openness assertion, or full-solution label lies outside this approval. Publication should preserve the source limitations and identify imported theorems as dependencies.

## References and public verification links

[K3] R. Inanc Baykur, Robion C. Kirby and Daniel Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, April 2026 author version, Problem 4.122, pp. 291–292. https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf

[PZ] Riccardo Piergallini and Daniele Zuddas, *A universal ribbon surface in B^4*, Proc. London Math. Soc. 90 (2005), 763–782; inspected arXiv v1, 2003. https://arxiv.org/abs/math/0308222 ; https://doi.org/10.1112/S0024611504015072

[IP] Massimiliano Iori and Riccardo Piergallini, *4-manifolds as covers of the 4-sphere branched over non-singular surfaces*, Geometry & Topology 6 (2002), 393–401. https://arxiv.org/abs/math/0203087 ; https://doi.org/10.2140/gt.2002.6.393

[Viro] O. Ya. Viro, *Signature of a branched covering*, Mathematical Notes 36 (1984), 772–776, formulas (17)–(18). https://www.maths.ed.ac.uk/~v1ranick/papers/viro3.pdf ; https://doi.org/10.1007/BF01156467

[GKS] Christian Geske, Alexandra Kjuchukova and Julius L. Shaneson, *Signatures of topological branched covers*, IMRN 2021, 4605–4624; arXiv v3, 2020. https://arxiv.org/abs/1901.05858 ; https://academic.oup.com/imrn/article/2021/6/4605/5880468

[BPZ] Valentina Bais, Riccardo Piergallini and Daniele Zuddas, *Branched coverings of simply connected 4-manifolds*, arXiv:2605.26337v2, July 2, 2026, Theorem A. https://arxiv.org/abs/2605.26337

Catalog detail attempted: https://www.unsolvedmath.com/problems/2998 . Indexed corroboration: https://www.unsolvedmath.com/problems?category=7&difficulty=3&page=7 . Neither the full corpus nor a selected dataset record is distributed with this audit.
