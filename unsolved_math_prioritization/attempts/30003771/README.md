# Nonabelian torsors: corrected unresolved partial audit

Problem 30003771 / OWR-16158-014, rank 871. Two approaches out of five.

**Status: unsolved.** This unrefereed, AI-assisted packet verifies the scope of a known local obstruction and two elementary algebraic arguments. It is neither a full solution nor a proper-base global counterexample, and makes no novelty claim.

## Read first

- [Corrected mathematical audit](corrected/MATHEMATICAL_AUDIT.md)
- [Independent mathematical audit](audit/INDEPENDENT_MATHEMATICAL_AUDIT.md)
- [Explicit acceptance and its limits](audit/ACCEPTANCE.md)
- [Actual author correction patch](audit/AUTHOR_CORRECTIONS.patch)
- [Approach ledger](corrected/APPROACHES.md)
- [Primary-source citations](corrected/CITATIONS.md) and [source inspection record](audit/SOURCE_INSPECTION.md)

The final manuscript uses the sum of coordinate-step images for joint weights, correcting the earlier report's diagonal-step convention. Maps into the generally nonalgebraic Nori gerbe are required to be faithful; representability is used only after passage to a finite algebraic stage. These qualifications are carried by the actual correction patch.

The elementary faithful-flatness/Frobenius obstruction arguments pass the independent review. Rydh's already-published local torsor-rigidity counterexamples do not disprove the original proper-base existence criterion with variable structure group. The same split groups have a canonical good induced torsor locally. Existing nonabelian root-stack uniformization does not by itself provide the required local Kummer form.

## Exact artifacts and provenance

The original author freeze is preserved unchanged under original/ and in NONABELIAN_TORSORS_30003771_AUTHOR_SAFE_FREEZE.zip. The corrected and audit ZIP files and their external manifests bind every member's bytes and SHA-256. Applying audit/AUTHOR_CORRECTIONS.patch to original/ exactly reproduces corrected/.

Historical statements such as “publication_performed: false” and “No publication was performed” describe the author and audit freezes at creation. They have deliberately not been rewritten in this publication packet. This draft PR is the separate publication step.

There is no executable mathematical proof checker. The static packaging checks, CRC/hash checks, and patch replay establish artifact identity only. Independent AI review is not expert peer review; source inspection is bounded and does not certify exhaustive literature coverage.

Only authored notes, correction patches, audits, acceptance reports, and public verification metadata are included. Source PDFs, extracted third-party text, dataset contents, and private material are excluded. The queue change is confined to this target's Status and Turns cells; Findings and every other byte are preserved.
