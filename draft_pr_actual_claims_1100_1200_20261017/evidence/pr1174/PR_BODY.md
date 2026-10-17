## Accepted prior partial bounds; sublinearity remains unresolved

This bounded independent audit accepts the two principal bounds in the five-page version 1 manuscript by Paratelligent Research Agent and Jeff Pickhardt:

- liminf f(n)/sqrt(n) >= 4/sqrt(3)
- f(n) <= ceil(n/2)+floor(n/(2R))+R(R-1)/2 for every positive integer R
- consequently f(n) <= n/2+((3/2)2^(-2/3)+o(1))n^(2/3)

Here f(n) is the largest length of a strictly increasing sequence of positive integers at most n whose nonempty indexed consecutive block sums are all different. Singleton blocks, overlapping blocks and collisions across lengths are included. The residual f(n)=o(n) question is not established. Neither the order of growth of f nor f(n)~n/2 is claimed.

## Complete mathematical reconstruction and review limits

AUDIT.md preserves the complete elementary reconstruction of the mod-3 construction, fixed-c passage to all n, layer packing with the exact floor(V)-floor(U) count, and finite upper bound for every R. No external theorem is required by these proofs, and no mathematical correction is needed in Theorem 2.1, Corollary 2.2, Lemma 3.1, Theorem 3.2 or their combined Theorem 1.1.

The accepted original audit is 13,724 bytes, SHA-256 2ae73a98dc3113340a4e2d7370b9d10f4a5af76224313aecf8fc1d0701dfbbad. Public-edition changes are limited to edition/review framing and historical-check references; all mathematical arguments and qualifications are retained. These are credited prior partial results, with no new-bound or priority claim.

These AI-assisted authored documents and their independent internal AI audit are unrefereed. Acceptance means only the bounded mathematical assessment. No external human peer review, journal acceptance, formal proof-assistant certification, comprehensive priority search, novelty or priority certification is claimed.

## Source and hypothesis qualifications

[New Bounds for Sequences with Distinct Consecutive Sums in Erdős Problem 357](https://paratelligent.com/research/papers/new-bounds-for-sequences-with-distinct-consecutive-sums-in-erds-1hwQTOM4) has a PDF dated 14 July 2026 and landing-page publication timestamp 31 August 2026, 03:34:29 UTC. The PDF byline names Paratelligent Research Agent and Jeff Pickhardt; the landing structured author field names Jeff Pickhardt. Its five-page PDF has 61,836 bytes and SHA-256 632302d4350145aa1b3970bd37b35f01cabc733ddafda191af959a5f5f43e411. All pages were text-read and visually inspected in the bounded audit. No journal peer-review status was verified.

The inspected [Coppersmith–Phillips 1996 publisher abstract](https://epubs.siam.org/doi/10.1137/S0895480193244139) assumes increasing order and supports its stated bound for f. The manuscript's further attribution to arbitrary-order g remains unverified, not disproved. The full CP96 proof was not inspected; sorting is not a valid general reduction. This bibliographic qualification is not a defect in the self-contained main proofs.

Weakly increasing valid sequences are automatically strictly increasing, because uniqueness of singleton blocks forbids repeated terms. Dropping order genuinely changes the class. The exact finite target was checked on printed page 58 of [Erdős and Graham's 1980 book](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf). Related infinite-sequence and EP356 questions are distinguished in the audit.

Source metadata states precise historical inspection limits. Direct EP357 tracker access returned HTTP 403, so no freshly verified tracker status is claimed. Edition preparation added no scholarly-source retrieval or inspection.

## Historical verification and distribution boundary

The recorded exact-arithmetic checks passed in normal Python, -O and -OO, with all three outputs byte-identical: 7,049 bytes each, SHA-256 aea72257d458d534c9d19563dad88128163f675e3c677466cb5c99575b04a43f. Edition preparation rechecks these historical identities without rerunning mathematical programs.

Checks cover 1,800 construction sequences, 18,960 neighboring residue-layer pairs, 45,150 quadratic identities, exhaustive valid subsets through n=22, independent enumerator agreement through n=10, 6,082,589 finite-upper-bound instances, 1,643,662 layer-packing instances, and 414 top-interval admissibility instances. Negative controls detect repeated singletons and sorting-induced collisions. Finite checks corroborate the arguments; the infinite statements rest on the complete written proofs.

Exactly eight authored audit, acceptance and public citation/verification metadata files are proposed as additions. No programs, raw datasets, detailed output or witness files, certificate contents, copied third-party source documents or source text, private sources, private personal data or private coordination material are included. The prose-only edition enables mathematical inspection and reconstruction, not execution of the original checks from the distributed files alone. QUEUE.md and all existing paths remain unchanged. This is a draft only, with no release or DOI.

## Exact public-file identities

- `ACCEPTANCE.json`: 2,851 bytes; SHA-256 `f917988c3d183fd939a8f1912baa1bf7d1cd96f212c75f5727da2fcc8bb030df`.
- `ACCEPTANCE.md`: 3,491 bytes; SHA-256 `10567e942904492402d81cf27413c1c3c147867b9ce5f29694ba4692291b63ff`.
- `AUDIT.md`: 14,879 bytes; SHA-256 `8d5aa41ef9a33093a0de2c813d2a4d5af199307944fa94cbcb693335feda0495`.
- `MANIFEST.json`: 1,619 bytes; SHA-256 `70768b0f7797aa60fb4d2df25f91c691ab62e8c2de09a79ecd79b38ac18f41ba`.
- `README.md`: 3,203 bytes; SHA-256 `09571e452f33105fa54e392b04bb318040793df8a4e44f0c3437d9842f6a0d1d`.
- `SOURCE_METADATA.json`: 6,115 bytes; SHA-256 `84c1a361f14266a42e503a22d6bfefdd5d2d4dc9fc107d562238f3072e087046`.
- `VALIDATION_SUMMARY.json`: 1,660 bytes; SHA-256 `724a2d135b91c03ff50046bd4d36e34a13a085231c896f91bdeaaeb0b5568a8a`.
- `VERIFICATION.md`: 3,797 bytes; SHA-256 `e8450380e5e3448712c128af6d7466a65a2a76c304c445d574d222307ba85fdd`.

MANIFEST.json lists all eight members and hashes the other seven; its own digest is pinned separately above.

