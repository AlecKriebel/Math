# Unbounded abstract prefix recursion and pressing nonrealizability

This separate packet for problem 3100047 / AMR-030-0047 (row 1747) preserves the complete authored construction proof and its complete separate independent mathematical audit. The original mathematical verdict is ACCEPT. The general pressing 1/3–2/3 conjecture, including its general four-, five- and six-word cases, remains unresolved here.

## Result and exact boundaries

For every integer T>=3, the explicit two-label recursion constructs exactly T permutations on 2T-3 labels. Their union of prefix sets has exactly those complete singleton-addition paths. The identity is included, the inversion sets are pairwise disjoint, and the maximum minority probability is exactly 1/T. Thus every constructed family with T>=4 has no 1/3–2/3-balanced pair. Complete singleton-addition paths are required throughout; arbitrary maximal inclusion-poset chains are a different notion.

The construction has (T-1)^2+2 prefix states, T^2-T+1 singleton-addition edges, 2+2(T-3)(T-2) variable pairs, and 3T-8 fixed pairs. The audit independently proves the edge formula. Exact five-word and six-word examples occur on seven and nine labels, respectively. No minimum-dimension claim for six words is made.

These are abstract path-system countermodels. Every displayed T>=4 family is proved unrealizable as the complete successful language of any symmetric binary pressing matrix. A self-contained four-letter support-forcing argument excludes the four-word base, and a legal fixed-prefix Schur residual reduces every larger constructed family to that base. At T=3, the seed is balanced on its variable pairs and is pressing-realizable.

Consequently prefix completeness and inversion disjointness, even with the majority identity included, impose no finite cardinality bound and cannot by themselves rule out exactly five or six words. This does not resolve general pressing balance, classify every unbalanced abstract family, or establish any universal weighted-context coverage bound.

## Full proof and separate audit

The [complete construction proof](UNBOUNDED_PREFIX_COMPLETE_DISJOINT_INVERSION_FAMILIES.md) gives the exact extension lemma, every possible cross-type singleton-addition edge, the general formula, small authored examples, and the full matrix nonrealizability proof. The [complete independent audit](INDEPENDENT_AUDIT.md) retains all independent derivations and scope qualifications, including the n>=3 boundary counterexample, the precise identity-containing subfamily corollary, both four-letter residual matrices, the T=3 realization, and the distinction between complete paths and arbitrary maximal chains.

No mathematical content is removed or corrected. [EDITORIAL_MAP.json](EDITORIAL_MAP.json) gives every changed UTF-8 byte range, old and new slice hashes, replacement text and reason. Safe original wording is included; private provenance locators are represented by exact ranges and hashes. The separately sealed preparation verifies complete two-way reconstruction against the pinned originals. [PRESERVATION_INVENTORY.json](PRESERVATION_INVENTORY.json) records the retained sections and mathematical boundaries.

[ORIGINAL_INPUT_PINS.json](ORIGINAL_INPUT_PINS.json) identifies the original proof, audit, source manifests and seals, weighted-identity dependency, and curated verification evidence by hashes and byte counts. The self-contained local argument is credited to the authored [four-letter weighted identity](../sparse_weighted/FOUR_LETTER_WEIGHTED_IDENTITY.md). [ACCEPTANCE.json](ACCEPTANCE.json) records the original mathematical acceptance and its precise scope. Independent review of this exact public editorial edition is a separate required gate.

## Verification and interpretation

[VERIFICATION.json](VERIFICATION.json) gives aggregate counts and exact replay matches. The independent audit checks all constructed cardinalities T=3,...,48; direct full permutation scans in dimensions 3, 5, 7 and 9; all 1,024 symmetric binary four-label matrices; and all 32,768 symmetric binary five-label matrices, including every one of the 1,024 with successful identity. None realizes the four-word target. Independent output has been freshly reproduced byte-for-byte under normal Python, -O and -OO during preparation. The original closed audit inventory has also been reverified in all three modes. These are finite corroborations of the full written proofs.

This is AI-assisted, unrefereed work. Independent internal AI mathematical review is not external human peer review, journal acceptance or formal proof certification. No fresh literature survey, novelty, priority, optimality or current external publication-status claim is made.

## Closed distribution

[MANIFEST.json](MANIFEST.json) is the exact public inventory, pinning every other public member. The external preparation seal pins that manifest. The packet contains complete prose reports and curated verification metadata only. Programs, raw per-case results or certificates, copied third-party sources, private sources, personal information and private coordination material are excluded. Small authored mathematical word and matrix examples remain as proof content. No executable public replay package is distributed.

This edition is separate from the base packet and all earlier supplements. Preparation does not change those editions, the repository, queue or live pull-request body. Later integration into the existing draft PR requires independent public-edition review and a separate exact-future-head preservation check after the preceding count-obstructions supplement lands.
