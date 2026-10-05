# 4400001: Hochman's first Pingree problem, prior negative resolution

**Disposition: already_solved. Research turns: 1/5. Independent AI audit: pass.**

The two-sided binary full shift and proper-three-coloring shift do not become topologically conjugate after all periodic points are removed. Ville Salo's published Theorem 1 extends a conjugacy between aperiodic parts of infinite transitive two-sided shifts of finite type to the full shifts. These two full shifts have respectively two and zero fixed points, a contradiction.

This is an attributed prior-literature resolution, not a new theorem, first-resolution claim, or formal verification. The exact target is Hochman's problem 1 on page 1 of the 2010 Pingree problem list. The source is Salo, *Conjugacy of transitive SFTs minus periodic points*, Proceedings of the London Mathematical Society 127 (2023), 1681–1692, [DOI 10.1112/plms.12567](https://doi.org/10.1112/plms.12567), Theorem 1, published page 1683.

## Reading guide

- [Complete deduction and hypothesis checks](author/PROOF.md)
- [Original investigation](author/APPROACH_LOG.md)
- [Independent adversarial audit and proof inspection](audit/AUDIT.md)
- [Audit disposition](audit/RESULT.json)
- [Independent source-access and inspection record](audit/PROVENANCE.json)

Both original nine-file packets and their frozen archives are preserved byte for byte. The author's audit-pending and publication-not-performed labels record its historical freeze; the completed audit is separate. No substantive correction was required.

## Reproduce the checks

From the repository root, run:

    python3 -B unsolved_math_prioritization/attempts/4400001/verify_publication.py

Only Python's standard library is needed, with no network or source files. The wrapper checks every published attempt file, both archives and all members, then replays the author and independent audit with exact binding. The author checks contain 275 assertions over 90,618 candidate words. The independent checks contain 20,532 assertions over 269,813 main candidate words plus 8,190 two-color control words. False comparison claims and integrity mutations are rejected. These finite checks do not certify the infinite-space extension theorem or continuity.

Archive fingerprints:

- Author: 13,292 bytes; SHA-256 `4b8fdb1f5a2115d73a5d7966671ee7488b1c2e03957261e1120a23ae0d9df724`
- Independent audit: 19,522 bytes; SHA-256 `1051ffc7ead78d94bcc99dca178c4ae3856d284d3389964a769455a62222addd`

## Scope and limits

The theorem's applicable proof and this application were inspected. The audit's fresh published-PDF retrieval returned HTTP 403; a retained published copy was independently hashed and visually inspected, alongside successful independent publisher-full-text and author-PDF reads. The current exact catalog detail page and selected full AI corpora remain uninspected. Catalog hashes and earlier repository-search metadata in the author packet are historical verification claims, not new independent audit checks. This is an independent AI review, not human peer review or a formal proof certificate.

The category is two-sided shift-equivariant homeomorphism with the product/subspace topology and all globally periodic points removed. It is not a conclusion about one-sided shifts or merely Borel maps.

## Repository change

The queue changes only this problem's Status to `already_solved`, Turns to `1/5`, and its formerly blank Findings cell to the credited prior negative resolution. Chat, DOI, every other row and byte, and the existing embedded stale header are preserved. No queue regeneration is used.

The attempt contains only authored mathematics, original code, and public verification metadata. Source PDFs, extracted source text, source images, dataset contents, and private coordination materials are excluded. Publication is as a draft PR; no merge, release, DOI creation, or outreach is part of this work.
