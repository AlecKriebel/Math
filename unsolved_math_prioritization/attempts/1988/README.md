# EP-197 / 1988: corrected bounded-deficit partial obstruction

The positive integers' partition into two sets, each with an omega enumeration avoiding increasing and decreasing three-term arithmetic progressions at arbitrary subsequence positions, remains unresolved by this work.

These AI-assisted authored documents and their independent internal AI audit are unrefereed. “Accepted” refers only to the corrected partial results in this edition. No external human peer review, journal acceptance, formal proof-assistant certification, novelty or exhaustive worldwide-status determination is claimed.

## Accepted after two corrections

PROOF.md is the exact corrected 16,759-byte proof (SHA256 670b73ed1e4c3a0fd52235a67f6ee9a67140bb8949e923798bb52c73f5e074bd). The original candidate is not accepted as written. Theorem 1 now counts positive integer interval starts; the affine extension distinguishes infinite and finite lattice intersections and uses positive inverse coordinates. CORRECTIONS.md explains both defects and their repairs in full. CORRECTIONS.patch is the exact 2,030-byte, two-hunk historical patch against the unchanged original authored/PROOF.md; the original is not distributed, and the patch is already applied here.

For a 3-permutable set S and each fixed C>=0, only finitely many positive integers n have the whole integer interval [n,2n-C] contained in S. Equivalently, deficits of full intervals with starts tending to infinity must tend to infinity. The finite-prefix bound is P>=k+2 for k distinct shifted C3 scales and two fixed anchors. This excludes bounded-additive-error dyadic-run partitions and any two-color partition with infinitely many monochromatic full intervals of bounded-above doubling deficit.

For every prescribed nondecreasing unbounded f:N->N, the proof also constructs one 3-permutable set of upper natural density at least 2/3 with infinitely many full intervals whose positive deficits are at most f of their starts. Their deficits still diverge. This constructs only one set, with no admissible complement claimed. Translation equates zero-based and positive-integer versions of the two-set existence question.

## Attribution and proof dependencies

Kasel’s finite C3 lemma (Theorem 22) is fully reproved through mirror propagation and four cases, then transplanted using fixed anchors and finite predecessor counts. The slow-allowance construction adapts Geneson’s Section 3, with a complete finite binary-order and cross-stage argument. No computational verdict is a dependency of either infinite proof. The correction to Kasel’s Remark 3 is separate from the finite lemma. No underlying mechanism is claimed novel.

## Reading guide

- PROOF.md: exact corrected proof and public citations
- AUDIT.md: complete substantive independent internal AI mathematical audit, including all four C3 cases, endpoint inequalities, quantifiers and limitations
- ACCEPTANCE.md: conditional verdict, applied-correction status and exact distributed review identities
- CORRECTIONS.md and CORRECTIONS.patch: complete correction explanation and exact historical patch
- STATUS.md: partial results and unresolved target
- SOURCE_AUDIT.md and SOURCE_METADATA.json: public source attribution, hashes, byte counts, retrieval/inspection history and stated status
- VALIDATION_SUMMARY.json: public verification boundaries and exact proof/correction identities
- MANIFEST.json: complete eleven-member inventory; it hashes the other ten members, while the proposed PR body separately pins the manifest

The historical finite certificate replay, negative controls, generator reproduction and exact arithmetic checks support finite instances and edge cases only. Code, certificates and detailed test outputs are omitted. This is a prose-only research edition, not an executable reproduction package. Mathematical truth is assessed by the written arguments, not by byte-integrity checks.

All source retrieval and inspection records are historical; no new scholarly-source retrieval or inspection was performed during edition preparation. The original candidate and audit remain unchanged. Copied third-party documents, extracts and images, raw datasets, private sources, private personal data and private coordination material are excluded. Only the eleven listed files are proposed as additions; QUEUE.md and unrelated paths remain unchanged.
