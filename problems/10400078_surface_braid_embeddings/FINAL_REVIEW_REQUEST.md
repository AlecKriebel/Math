# Full independent review request

Proposed disposition: original unresolved5/5, with scoped mathematical candidates. Please audit all five proofs, exact target identifications, and the source interpretations. Preserve frozen bytes; any correction should be additive or versioned. No final status or PR is authorized by this review request alone.

Source priorities:
- Ohtsuki Section3.10 printed443–444; printed444.png was visually inspected. The source fixes a closed oriented surface and asks a rational pure-braid injection, without explicitly adding completion, graded-isomorphism or strandwise normalization in Problem3.28.
- González–Meneses–Paris Section1.4 pp3–4: chord generators/relations, completed crossed product and bead action; Proposition2.2 and Theorem1.2 for kernel filtration and separation. Distinguish chord-only A_n in that paper from its crossed product and from Ohtsuki notation.
- Bellingeri–Funar published2004 paper, Theorem2.1 handle commutator relation and Theorem1.1/Definition2.2. Its theorem is stated for full B(Σ,n), while later Brochier2013 prose cites a pure-group obstruction. Do not conflate bare injection, proper graded injection, graded isomorphism onto the prescribed target, linear-functional factorization, or tangle functoriality. No claim of correcting that paper is made here.
- Boyer–Rolfsen–Wiest Theorem1.4 for surface bi-orderability; Bowden2011 printed2213–2214 for the tangent Euler central extension/fiber homology. Lurie's Lecture36 Lemma1 was read as a primary PDF through the web tool; local download returned404. Its complete axis argument is summarized in the proof.

Proof priorities:
1. Torus difference-coordinate homeomorphism; exact two-strand free chord algebra; diagonal bead centralization; classical Magnus coefficient argument. Uncompleted unit obstruction must use actual domains and bi-orders, not a general unit conjecture.
2. Check the signs in the semidirect action and upward/downward edge labels. Verify no vertical-word cancellation for every reduced free word, degree-zero normalization, and the meridian difference symbol.
3. Check the grid spanning tree, infinite but finitely invertible free-basis change, augmentation tensor algebra, pure/full restriction of the kernel filtration, section-cocycle leading terms, strictness/separation and the proper graded image. This is a particularly important place to check the meaning of 'universal'.
4. Check the UΣ→Conf₂Σ map and its fiber, centrality and surjective base projection; Fadell–Neuwirth injectivity of the punctured-surface meridian; the actual pure commutator relation; invariant finite-support monomials and scalar quotient. Normalization is essential.
5. Check arbitrary degree-zero unit decomposition, nonzero Euler relation forcing every G→Π to kill c, and the finite-index normal-core orbit argument when one projected image is nonabelian. Confirm the cyclic/trivial-image cases really remain unresolved.

Sources are local-only in sources/, with initial and additive hash manifests. Do not publish PDFs, screenshots or imported records. Exact source paths: ohtsuki2002.pdf, printed444.png, gonzalez-paris2004.pdf, bellingeri-funar-published2004.pdf, ara-dicks2006.pdf, boyer-rolfsen-wiest2005.pdf, bowden2011.pdf. Source URLs and precise unavailable-download limitations are recorded in the proofs and source additions.

Run python turn1/check_magnus.py, turn2/check_lattice_embedding.py, turn3/check_filtered_image.py, turn4/check_invariant_terms.py, turn5/check_euler_boundary.py. Stdout must byte-match each turn's verification.json. Total new declared assertions28,038; imported old controls not doublecounted. Finite tests do not replace the topological/infinite-group proofs. Report a scoped PASS or precise required corrections, not a full original solved claim.
