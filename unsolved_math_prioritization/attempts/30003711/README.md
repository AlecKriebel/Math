# Flex-point cover: ordinary section genus eight

Problem **30003711 / OWR-15987-022**, rank 870. The candidate proves ordinary unnormalized section-based Schwarz genus **8**, equivalently normalized sectional category **7**, for the nine-flex cover over the smooth cubic coefficient space CP^9 minus the cubic discriminant. This resolves the curated Chen–Wan 8-versus-9 section-genus target, relative to the cited lower bound and classical theorem inputs.

**The literal OWR requirement of connected domains with simultaneous trivialization of all nine sheets is not resolved by this result.** One selected sheet suffices for a section. The element C has flex monodromy of cycle type 1^3 3^2: three fixed flexes and two nontrivial three-cycles. The orbit construction therefore supplies a section without trivializing the whole cover, and the eight color domains need not be connected.

## Proof and reviews

- [Unchanged author proof](author/PROOF.md), [one-approach ledger](author/APPROACHES.md), and [original status](author/STATUS.json)
- [First independent mathematical audit](independent_audit/INDEPENDENT_MATHEMATICAL_AUDIT.md) and [acceptance with exact scope](independent_audit/ACCEPTANCE_AND_SCOPE.md)
- [Second independent adversarial audit](second_review/MATHEMATICAL_AUDIT.md) and [separate acceptance](second_review/ACCEPTANCE.json)
- [Publication acceptance](PUBLICATION_ACCEPTANCE.json), [static package test results](PUBLICATION_TEST_RESULTS.json), and [complete package manifest](PUBLICATION_MANIFEST.json)
- [Public source-inspection addendum](independent_audit/SOURCE_INSPECTION_ADDENDUM.json)

Both independent AI reviews accepted the explicitly scoped theorem without a mathematical correction. These reviews are not conventional human peer review. No formal proof-assistant verification, novelty or priority, exhaustive literature search, or exact algorithmic branching-complexity result is claimed.

The upper bound uses the projective Hessian spectral lemma, common fixed flexes for cyclic circle stabilizers, sections near complete orbits, a dimension-seven coarse orbit space, eight-color refinement, and the actual covering pullback. Chen–Wan supplies the matching lower bound. Finite-group diagnostics supplement the written argument; they are not a topological proof certificate.

## Frozen provenance and limitations

The three ZIP archives and their external manifests are preserved byte-for-byte in `archives/`. The first audit archive also contains all five original author files unchanged. The sixteen distinct authored proof/review/metadata files are unpacked for reading.

Historical statements that independent review or publication had not occurred describe the corresponding freeze time and are preserved unchanged. Similarly, the author and second reviewer did not retrieve Illman's full text; the first audit's later source-inspection addendum records successful recovery and inspection of the original article. Only its public citation, retrieval record, hash and size are included. No copied PDF, OCR, extract or image is redistributed. The Chen–Wan journal full text was not retrieved; the exact arXiv v2 is the inspected theorem source.

Static byte, inventory, scope-binding and corruption-rejection checks passed in normal Python and with optimization enabled. They do not establish mathematical validity. This data-only package has no executable proof verifier or private checker fingerprint, and makes no CI-pass claim.

The queue is updated only in this problem's Status, Turns and Findings cells to `claimed_solved`, `1/5`, with the invariant qualification in the same row. No additional proof-search approach was used for publication. The existing unrelated queue content and chat links are preserved.
