# Maximum finite CP-plus-rank: accepted partial result

Problem 30003650. Edition dated 10 October 2026.

Project author: Alec Kriebel, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).

## Accepted theorem and remaining question

For every n >= 1, the maximum finite strictly-positive-factor rank equals the maximum ordinary completely-positive rank:

    p_n^+ = p_n.

The proof includes singular matrices and gives the attained equality P_(n,r)^+ = P_(n,r) on every exact ordinary-matrix-rank stratum 1 <= r <= n. Here A=BB^T uses an n by p factor; positive means every factor entry is strictly positive.

The two-question target is accepted only as partial because its maximum gap g_n = max(cp^+(A)-cp(A)) remains undetermined in general. This edition does not determine explicit ordinary maxima p_n in all orders or assert pointwise equality cp^+(A)=cp(A). No novelty is claimed.

The complete proof uses two invertible congruences. Positive congruence sends a minimal nonnegative factor to a strictly positive one; closedness of bounded-CP-rank sets prevents a decrease for small parameters. Negative congruence preserves a given positive factor for an explicit interval, while its strictly positive inverse pulls any minimal nonnegative factor back to a strictly positive factor. Both operations preserve ordinary rank. No ambient-interior theorem is extended to singular boundary points.

The retained gap statements are g_1=g_2=g_3=0, 0<=g_4<=1, and 1<=g_n<=p_n-3 for n>=5, with the stated low-order and gap-one facts attributed to Bomze–Dickinson–Still. The rank-r bound is P_(n,r)-r. The positive-definite bound p_n-n is not asserted for all singular matrices. The maximum gap is nondecreasing in n by row duplication; this does not determine its value.

## Documents

- [Complete proof](PROOF.md), preserved byte for byte.
- [Substantive mathematical audit](MATHEMATICAL_AUDIT.md), preserved byte for byte.
- [Acceptance report](ACCEPTANCE_REPORT.md) and [machine-readable acceptance](ACCEPTANCE.json).
- [Correction disposition and safeguards](CORRECTIONS.md), preserved byte for byte; no mathematical correction is required.
- [Candidate source metadata](CANDIDATE_SOURCE_METADATA.json) and [independent audit source metadata](SOURCE_METADATA.json), both preserved byte for byte.
- [Verification summary](VERIFICATION_SUMMARY.md) and [public manifest](MANIFEST.json).

## Review and source limits

This is an AI-assisted mathematical exposition with an independent internal AI mathematical/source audit. These authored documents are unrefereed. Acceptance is not external human peer review, journal acceptance of these documents, or formal proof-assistant certification. The argument is mathematically accepted within that internal review; worldwide priority and exhaustive current-literature status are uncertified.

The sources distinguish the original Oberwolfach report, a complete Bomze–Dickinson–Still author manuscript dated November 4, 2014 corresponding to a 2015 journal article, and the published Lai–Yoshise 2022 paper. The inspected BDS manuscript is not labeled the journal PDF. Its interior theorem is used only within its stated domain; its all-order p_n^+=p_n question being open there does not certify current novelty. Lai–Yoshise's optimization results are not a factor-nonexistence certificate.

PDF hashes, sizes, retrieval/inspection history, precise theorem locators and bounded primary-web checks remain in the source records. The independent audit used authenticated candidate source copies and did not independently redownload them. Publication preparation adds no source retrieval, inspection or later-publication-status claim.

This edition distributes ten files of authored mathematical prose, acceptance, and public source/verification metadata. It includes no copied source documents, extracted source text or images, datasets, executable code, proof certificates, generated test cases, raw outputs, private sources, private personal data, or coordination records.
