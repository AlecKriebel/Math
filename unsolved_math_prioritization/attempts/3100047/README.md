# Pressing balance partial results

Row **1747**, database **3100047 / AMR-030-0047**. Research date: **12 October 2026 UTC**.

## Accepted result and unresolved target

For every symmetric binary matrix on at most eight vertices with more than one successful full-length pressing permutation, some distinct pair of vertices has precedence probability in the closed interval **[1/3,2/3]**, under the uniform distribution on successful permutations. At order eight, a proven isomorphism reduction covers all **68,719,476,736 labelled symmetric matrices**. There are **28,758,575,496** full-length pressable matrices, including **28,757,486,856** nonunique ones, and no counterexample.

This is an exact finite verification, supported by two independently authored exact algorithms that a separate auditor reran, an independent complete orbit-cover check, and independent Gaussian/direct checks at small orders. It is not an unrestricted proof. Nonsingularity is necessary for full-length success but does not itself guarantee a successful pressing word. Singular omitted-vertex conventions are outside the accepted formulation.

The complete structural proofs establish:

- The successful permutations partition exactly by label-indexed instructional Cholesky roots into disjoint linear-extension families. These are precisely the adjacent-swap components and successful one-letter-relocation components.
- Every recursively constructed V-poset with more than one extension has a balanced pair, by a complete uniform-shuffle proof. The autonomous pressing corollary uses the explicitly external Cooper–Gartland–Whitlatch characterization. That characterization is not claimed to have been fully independently audited.
- Reversal bijects the success families of A and its inverse. For successfully pressable self-inverse A, every distinct pair has precedence probability 1/2.
- Principal-nonsingular sets satisfy symmetric exchange, with a complete proof. Small explicit examples obstruct greedoid, single-poset and competing-first-pair shortcuts. None is a counterexample to pressing balance.
- A vertex-minimal counterexample would have a transitive strict >2/3 majority order, connected underlying graph, multiple possible first and last letters, and multiple instructional classes.

A separate, independently accepted supplement proves an exact Cartesian-product factorization along connected components of the variable-order graph, whose edges are pairs with precedence probability strictly between zero and one. The components occur in one fixed order; their associated Schur-complement pressing families have independent uniform distributions and preserve all within-component pair probabilities. Combining this theorem with the accepted finite verification proves balance for every nonunique full-length pressing family whose variable-order components all have size at most eight, even when its total order is larger. A vertex-minimal counterexample must be variable-order-connected and have order at least nine. The supplement and its audit remain separate from the original frozen reports.

The general full-length pressing-balance conjecture remains unresolved. No singular-convention disproof, general poset balance theorem, novelty claim, priority claim or literature-optimal search bound is made.

## Complete mathematical documents

- [Computational theorem and exact methods](COMPUTATIONAL_METHODS.md): all determinant, subset-path counting, direct-press, canonical generation, orbit-weighting and arithmetic arguments; exact finite aggregate counts; historical execution description.
- [Structural proofs](STRUCTURAL_PROOFS.md): the complete instructional-root, relocation, shuffle, inverse, exchange, obstruction and necessary-condition proofs.
- [Independent mathematical audit](MATHEMATICAL_AUDIT.md): the complete substantive audit, unchanged from its accepted frozen bytes, including independent coverage derivation, source qualifications, replay scopes and negative controls.
- [Variable-order factorization](VARIABLE_ORDER_FACTORIZATION.md): the complete separate block-factorization proof and its precise finite-verification implication.
- [Independent factorization audit](FACTORIZATION_AUDIT.md): the complete separate audit and the explicit combined order-eight corollary.
- [Acceptance](ACCEPTANCE.json): the exact bounded scope and review limitations.
- [Aggregate verification](VERIFICATION.json): all retained finite aggregate counts, algorithm and audit scopes, compiler/runtime metadata, and relevant byte/hash identities. These are aggregate records, not raw case data.
- [Public source metadata](SOURCE_METADATA.json): source titles and public URLs, public-source byte/hash identities, retrieval and inspection history, distinct version dates, and narrow source-text defects.
- [Original input identities](ORIGINAL_INPUT_PINS.json) and [editorial map](EDITORIAL_MAP.json): exact source-to-edition correspondence, with every locator/distribution edit identified and the original mathematical arguments preserved.
- [Closed manifest](MANIFEST.json): the complete public file set and each other file's size and SHA-256. The manifest excludes itself from its digest list to avoid circularity; preparation separately seals its identity.

## Source and review boundary

Cooper's author-maintained probability question is the direct target source. Its wording does not resolve how to compare vertices omitted from successful words of singular matrices. The accepted work uses nonsingular matrices admitting successful full-length permutations.

Cooper–Davis arXiv:1502.07450v5 supplies the inspected leading-minor and fixed-order coloring statements; older withdrawn stronger claims are not substituted for them. The historical version metadata distinguishes the 28 September 2015 v5 revision from its internal 6 July 2021 typeset date. The V-poset source's official v2 revision is 14 November 2018; its PDF displays 3 May 2019, and the separately pinned author-hosted snapshot displays 16 October 2018. These are distinct dates and byte streams. Failed DOI access is not evidence of a publication-status conclusion.

The V-poset paper has a narrowly identified Lemma 8 cardinality equality defect and an incomplete printed bowtie definition. Restricting the local equality to extensions beginning with the chosen vertex repairs that local step. The authored argument uses the recursive V-poset definition rather than either defective line. This does not claim a full independent repair or audit of the external autonomy characterization.

This is **AI-assisted, unrefereed work**. Acceptance means independent internal AI mathematical review within the precise stated scope. It does not mean external human peer review, journal acceptance, proof-assistant certification, or priority clearance.

## Public edition and reproducibility

The full authored proofs, all substantive audit reasoning and all mathematical algorithm descriptions are included. Unavailable compile/run locators have been replaced transparently by historical execution descriptions, not by deletion of mathematical arguments. Exact reversible editorial controls establish preservation against the original frozen reports.

The programs, raw graph representatives, full per-case result files and certificates are retained separately and are not distributed here. **There is no executable public replay package.** The aggregate records and prose explain what was checked and why the algorithms are exact; this edition alone does not execute those historical checks. No copied source PDF, source extraction, source image, external dataset content, private source, personal information or private coordination material is included.
