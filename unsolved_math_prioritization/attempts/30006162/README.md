# Exceptional-surface generic points: audited partial results

**Problem 30006162 / OWR-14299082-004, rank 829: unsolved, 5/5 substantive approaches.**

Neither the sphere nor the real-projective-plane identity-component homeomorphism group is proved to have or fail the generic point property. The [independent audit](audit/REVIEW.md) accepts the scoped partial results and requires no mathematical correction.

## Accepted scope

- Point stabilizers are both presyndetic and co-precompact, share GPP with the ambient group, and have nonmetrizable universal minimal flows.
- Any subgroup preserving a finite configuration with at least two points is not presyndetic; this obstruction does not require closedness.
- A closed presyndetic extremely amenable certificate would have exactly one fixed point and no other finite orbit. It would lie strictly inside that point stabilizer, be non-co-precompact and nonnormal in both it and the ambient group.
- Restriction of continuous homogeneous quasimorphisms to any presyndetic subgroup is injective.

Read the [proofs and precise hypotheses](author/MATHEMATICAL_REPORT.md), [five approaches and gaps](author/APPROACHES.json), and the audit together. Finite diagnostics support these arguments but do not prove infinite topological or Baire-category assertions.

## Important limits and attribution

Basso–Zucker v2 Theorem 7.7 uses existence of a first-countability point, despite the opposite abstract wording. Its minimal G-extremally-disconnected-flow hypothesis is essential. The known nonmetrizability of the two universal minimal flows does not exclude a comeagre orbit.

Böke's September 29, 2026 v2 preprint supplies the credited infinite-dimensional homogeneous-quasimorphism input for the projective-plane group, with continuity as documented in the inspected sources. The restriction lemma therefore gives infinitely many restrictions on every presyndetic subgroup. No applicable vanishing theorem for arbitrary topologically extremely amenable subgroups was established. This is not a negative GPP answer.

The thin-chain and circular-cover results from [adjacent ID 30006161, PR 158](https://github.com/AlecKriebel/Math/pull/158) are credited at exact commit [91ddfb046912817229202f5478487cf91fcb3e36](https://github.com/AlecKriebel/Math/tree/91ddfb046912817229202f5478487cf91fcb3e36/unsolved_math_prioritization/attempts/30006161). They are not new results of this report. Source versions, public URLs, PDF byte counts and hashes, and inspection limits are retained in author/SOURCES.json and audit/SOURCE_AUDIT.json. No copied source documents or extracts are included.

## Preserved artifacts and current acceptance

Both ZIP archives and all 24 extracted members are preserved byte-for-byte. In particular, author/STATUS.json's independent-audit-pending label is a historical freeze-stage snapshot. The current verdict is PASS_SCOPED_PARTIAL_RESULTS with no mandatory corrections. Other historical retrieval, inspection and mutation statements retain their original temporal meaning.

This is substantially AI-assisted mathematical work and a separate AI audit. No novelty, priority, complete-literature, human-peer-review or formal-proof certification claim is made. Both exact targets remain open within the bounded inspected-source assessment. Neither an affirmative certificate nor a negative compact counterflow was established.

## Reproduction

Python 3.10+ and its standard library are sufficient. Retain a trusted digest of PUBLICATION_MANIFEST.json outside this directory, inspect verify_publication.py, and verify the manifest bytes against that digest before execution. From this directory:

    python -I -B verify_publication.py TRUSTED_MANIFEST_SHA256 --full
    python -I -O -B verify_publication.py TRUSTED_MANIFEST_SHA256 --full

The verifier checks strict inventories, regular files, byte counts and hashes, exact ZIP/member equivalence, externally pinned inner manifests, and exact agreement with frozen expected diagnostic results. It executes hash-verified checker source in isolated interpreters. Full replay runs the author 2,108 diagnostics, independent 58,588 diagnostics, and the 28 author plus 36 independent integrity controls. Relocate the complete publication directory and repeat for a relocation replay. These checks cannot authenticate coordinated replacement without an independently retained manifest digest.

The publication contains authored mathematics, code, audit reports, test results and public verification metadata only. Dataset contents, PDFs, extracts and private coordination material are excluded. Draft publication does not merge, release, create a DOI or contact outside people.
