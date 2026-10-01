# Independent full review: 20003006 / AIM digital topological realization

**Verdict: PASS_COMPLETE_CONVENTION_QUALIFIED_REALIZATION.**

The unchanged TURN_1.md, SHA256 `83dd8c0557690c6ae91bdc52fc8e500e7b373a90286fa58c57251d813e3b792f`, proves its all-degree strong-grid theorem and supplies a complete convention-qualified answer to the AIM source's existential homotopy-realization request. A credited `already_solved`, 1/5 disposition is supported. No mathematical correction is required. This verdict does not certify a simultaneous realization of every incompatible theory ever called digital homotopy or digital homology, and does not certify novelty.

The frozen author manifest is `54a1040b28922b46662133a75541583c4aab21e94b7b8bce6b9e281f02e6c3d0`. I had no role in constructing the candidate. I read the full argument, independently checked the actual primary definitions and all-degree input, replayed the author's checker, and wrote separate controls without importing it.

## 1. Binding source-scope judgment

I read AIM Digital topology Problems 1.1–1.3 and independently fetched the current HTTP page; its bytes match the author's pinned page. Problem 1.3 explicitly presupposes a construction of higher digital groups. It neither fixes a competing all-degree definition nor specifies an exhaustive list of chain invariants. The preceding problem asks for such higher groups, with the six-vertex digital sphere as a test. The 2024 second-group paper explicitly comes from the same March 2023 workshop and fixes categorical product adjacency.

Accordingly the candidate is a legitimate constructive response: it supplies direct, finite combinatorial groups D_n in every degree, agrees with the two specified published groups, and gives one functor F realizing all these groups naturally. This is not the vacuous declaration D_n:=π_n(FX); D_n is defined independently by finite arrays and fixed-boundary homotopies and the comparison is proved. The octahedral clique complex of the source's six-vertex sphere is the usual triangulated S², so the required degree-two test follows from the theorem.

The qualification must remain visible in the result headline, PR and queue summary: **strong-grid homotopy realization in every degree, extending the published π₁ and π₂**. An assertion that all digital invariants, with no choice of convention, now agree would exceed both this proof and a coherent reading of the open-ended source. That is a scope limitation, not a remaining gap in the specified realization construction. The live page's unchanged “Open” label is not itself a proof that this constructive response fails.

## 2. Primary theorem and model identification

Grandis's arXiv author version §§2.1–2.8 defines the integer line, its categorical powers, the linked-set function complex, paths, delays, concatenation and caterpillar homotopies. Section 6.2 defines π_n as π₀Ωⁿ, with fixed-face integer nets as representatives and groups for n≥1, abelian for n≥2. Theorem 6.6 and its full proof on pp.39–40 give the natural realization isomorphism. I read these definitions and proof and visually checked the theorem page.

The quoted input genuinely has the needed product, not a box product. A linked set in the grid projects in every coordinate into one consecutive pair, so the entire unit cube is a linked set. The function-complex linkedness simultaneously checks all cross-time labels. The candidate uses pairwise adjacency only after taking the flag complex Cl(X); it does not falsely impose pairwise criteria on arbitrary nonflag complexes.

The geometric realization of that grid complex is not being identified with a Euclidean cube. Grandis extends vertex labels multi-affinely inside their common image simplex. This is exactly the interpolation needed; it is compatible on shared faces and is constant on the based boundary. The theorem's naturality includes noninjective simplicial maps, so edge-collapsing digital maps cause no problem.

The complete author manuscript is the accessed mathematical source for Grandis; I make no claim of reading a subscription typeset version. It is a substantial established input, properly credited, rather than a theorem supposedly established by the finite tests.

## 3. Finite-domain comparison

**Extension and equivalence.** If a strong-grid edge crosses from an old box to its exterior, its endpoint in the box lies on the boundary. Fixed boundary values therefore permit zero extension, including every time-diagonal edge. The common enlargement used in transitivity is legitimate. Concatenating two time homotopies at their shared time slice does not create a skipped-time edge.

**Delays.** I independently checked the coordinate statement behind the caterpillar: the union of δ_s and δ_(s+1) applied to any adjacent pair has diameter at most one. Applied in one selected coordinate, this puts all labels of a spatial/time unit cube in a single original cube. The proof consequently works in arbitrary dimension and for nonflag linked-set targets as stated. It is stronger than checking each vertex's time track alone.

A delay above the upper support face is ineffective; one below the lower face gives a unit translate. Sweeping the threshold is finite, admits a common bounding box, and preserves every other fixed face. On anchored arrays the sweep stops at zero, so it never destroys the coordinate-zero basepoint face. Reversing that sweep proves equivalence of a right-translated array with its original. The direct one-step translation shortcut would fail and is correctly excluded.

**Uniform support.** Iterating the path functor imposes a uniform outer support. Only finitely many distinct slices occur between its outer bounds; by induction each slice has finite inner support. Taking their finite union gives one spatial box. In a path in Ωⁿ the same argument also includes both endpoint nets. Thus the comparison does not exchange pointwise and uniform finiteness or posit unsupported compactness.

**Surjectivity and injectivity.** Every integer-supported loop net can be translated into an anchored box after adding a basepoint collar. The caterpillar preserves its class. If two anchored nets are homotopic through negative coordinates, translate the entire uniformly supported homotopy by one sufficiently positive vector, restrict it to a larger anchored box, and remove the endpoint translations by the boundary-preserving sweeps. This is the essential injectivity argument; restricting the original homotopy directly to the positive orthant would indeed be wrong.

The published second-group definition allows a side length zero. Such an array is entirely boundary and constant, hence gives only the identity and extends to the positive-side-length boxes used in the candidate. This harmless convention does not change any equivalence class.

## 4. Group laws and the published low degrees

The map q sends the first-coordinate concatenation to an admissible Grandis concatenation with a basepoint pause. The pause is a delay and can be removed. Bijectivity was established before group structure is transported, so there is no circular appeal to the desired group law. Padded supports do not cause a naturality failure when a target map collapses some labels.

For degree one I read Lupton–Scoville Theorem 4.6 and its proof, including the subdivision-based equivalence and its map on loop vertices. The common edge group gives the claimed identification. It is not an unsupported assertion that subdivision and basepoint extension are literally identical definitions. Triangle insertions can be implemented after a repeated endpoint because the three labels form a clique; conversely a strong strip gives edge homotopy.

For degree two I read the published Definitions 2.1–2.3, 2.9 and 4.1, the extension lemma, and the product formula, and visually checked Figure 5/Definition 4.1 on PDF p.12. The product really places the second block at offset (m+1,n+1), not just in the first coordinate. The candidate's regional translation supplies precisely the missing second offset.

The patching argument survives all cross-interface edges: the only adjacent columns across the two slabs are the old right boundary and the new left boundary, both constantly basepoint throughout the homotopy. No interior point on one side is adjacent to an interior point on the other. The top and bottom faces remain based during each transverse caterpillar. Thus the final product equals the published diagonal product after harmless padding. I independently tested this using arrays whose labels cover all six vertices of the octahedral sphere, as well as reflected and delayed variants; it is not a test confined to maps into one clique.

## 5. Nearby results and exclusions

The face-group preprint's Theorem 8.1 and Section 9 are described accurately: the latter announces the digital application and defers its proof. Its bracketed reference-number mismatch must not be interpreted as a different digital group. The candidate supplies the finite-array comparison rather than treating the announced all-degree extension as an established theorem.

The loop-space paper's precise final realization statement is Corollary 8.4, obtained from Theorem 8.3 and Stone's result. The source checkpoint's shorthand attribution to Theorem 8.3 “relying on Stone” is harmless; this paper is background and is not used to bridge any gap in the candidate.

The current McCord paper's Example 2 indeed distinguishes closure-space homotopy from digital homotopy and states an all-higher-degree comparison as a conjecture. Theorem 24 alone cannot establish that comparison for an unspecified digital model. The candidate instead proves its own specified model comparison through Grandis. The separate cubical-nerve theorem applies to A-groups. The stated four-cycle box contraction is valid, while one required strong diagonal fails. No false identification with A-theory or blanket digital homology claim is made.

## 6. Integrity and controls

- All 13 author artifacts match the frozen manifest; all ten source inputs (one HTML and nine PDFs) match their hashes.
- The author's 752,681-assertion output replays byte-for-byte.
- The independent checker passes 6,228,582 exact assertions. Most are explicitly counted individual spatial/time edge checks across 16 nonconstant diagonal-product comparisons; the count is not a count of mathematical lemmas or independent proofs.
- Additional controls address nonflag linkedness, negative supports, the six-vertex clique sphere, degree-two chain boundary/ranks, and the box/strong distinction.

No finite enumeration proves the arbitrary-degree statement. The full written finite-support comparison and the credited Grandis theorem carry that conclusion. No mandatory revision is identified. Publication remains subject to the parent's gate, with the convention qualification and full prior-theorem credit retained.
