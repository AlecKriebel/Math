# Narrow release review, version 1

Date: 2026-10-03 UTC.

Publication copy: one description of removed nonmathematical metadata is generalized; all findings, conditions and checks are unchanged.

## Verdict

**PASS for faithful mathematical projection, subject to the exact documentation repair below before publication.** The supplied release snapshot has one reproducibility-wording defect; an unqualified release PASS is conditional on correcting it and refreshing its integrity metadata. The mathematical PASS from the full review remains unchanged. No new mathematical attempt or source search was performed.

Reviewed release-manifest SHA-256:
`9ff57fd17fb01241018a81699b3287e75b18050bbf95e54ea98f3afc4d5f245f`.

Reviewed publication-audit SHA-256:
`278992214da8f68ae7f4223a31ed6dd6f69507c1a965112240c77b69054a0144`.

## Verified

1. The release contains exactly 22 files: the 14 byte-identical frozen author files and the eight declared additions. No original author file was changed or deleted.
2. Every release-manifest payload matches its declared byte length, SHA-256, and Git blob SHA-1. The manifest itself matches the supplied hash. Its inventory is complete apart from the intentional self-exclusion.
3. Reapplying precisely the four text substitutions in the supplied projection map to the original audit produces the publication audit byte-for-byte. There are no undeclared text changes. The sanitized audit retains all mathematical findings, qualifications, source limitations, and the unsolved 5/5 disposition.
4. The publication audit JSON removes only nonmathematical identifying and coordination metadata, adds the two declared neutral publication fields, and recomputes the report hash. All other common fields, including all mathematical findings, are identical.
5. The measurable-weight clarification correctly identifies one fixed exceptional x-set, essential uniformity, incidence-Fubini identification for almost every normal, and ordinary every-normal equality for the actual continuous geometric weights. It does not strengthen the principal theorem.
6. The midpoint clarification correctly states nonincrease for every normal, strict decrease for some normals and in mean, without asserting strict decrease for all normals. Its reference to Attempt 2 retains that attempt's positive C¹ radial-function assumptions.
7. The publication overview and status retain original UNSOLVED 5/5, local C² partial-result scope, and the no-global-resolution, no-novelty, no-human-peer-review, and no-formal-verification qualifications.
8. The portable checker uses paths relative to its own file or an explicit root, requires no source downloads, and passes here. Its output matches RELEASE_CHECKS.json. All 228 finite exact controls replay successfully.

## Required small reproducibility clarification

`verify_release.py` uses `assert replay == expected`. Both dictionaries contain `sympy_version`, and the frozen expected value is `1.14.0`. Therefore an otherwise identical successful run on a different SymPy version fails this assertion. The stated requirement in PUBLICATION.md, "Python 3 and SymPy are required," omits this exact version dependency.

Required documentation-only change in PUBLICATION.md, under Reproduction:

- Replace exactly: `Python 3 and SymPy are required.`
- With exactly: `Python 3 and SymPy 1.14.0 are required.`

This explicitly documents the dependency already imposed by the checker's exact-output comparison. No change to verify_release.py, the frozen author packet, the audit's mathematical findings, or the proof is needed. Refresh PUBLICATION.md's byte length and content hashes in RELEASE_MANIFEST.json, recompute the release-manifest hash, and update any release receipt that records that hash. The original reviewed hash above identifies the pre-repair snapshot; it must not be presented as the repaired snapshot's hash.

This is a reproducibility/documentation issue, not a defect in the theorem, its proof, the projection, or the 228 controls. It does not require a new full mathematical audit. Applying this exact documentation correction and verifying the refreshed manifest is sufficient; no additional mathematical review is required.

No release files or remote state were modified during this review. The remote identity/diff and authorization gate remains separate.
