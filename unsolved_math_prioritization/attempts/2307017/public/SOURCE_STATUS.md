# Source and status reconciliation: 2307017

Checked 2026-10-04. Recommended classification: **already_solved**, under the classical distinct-positive-integer convention. Independent audit pending. No new discovery is claimed.

## Primary evidence

Hayman–Lingham, arXiv:1809.07200v2, printed p. 165, contains Problem 7.17 immediately followed by an update crediting its proof to Korevaar and Zeinstra. The cited 1985 paper is bibliographic item [489]; the additional 1992 paper is [812]. The exact page was rendered and inspected. https://arxiv.org/abs/1809.07200

Zeinstra's 1992 paper was inspected in the Göttingen digitization: p. 2 defines finite complex Borel measures and the curve condition; pp. 11–12 give Theorem 4 and its proof. The type equality is explicitly written with upper limits, and the sampling points have a linear separation hypothesis. A straight ray satisfies the curve condition, and increasing integers give the required sample separation. This corroborates the literature mechanism, but the theorem's finite-measure Laplace-transform class is not silently identified with all bounded holomorphic functions. The complete half-plane proof in PROOF.md avoids that issue. https://doi.org/10.1515/crll.1992.424.1

Working digitization: https://gdz.sub.uni-goettingen.de/id/PPN243919689_0424?tify=%7B%22pages%22:%5B15%5D%7D (physical page 15 is printed p. 11). The obsolete DigiZeitschriften PDF URL now returns 404. The digitization was recovered through the EUDML-linked institutional resolver and its official IIIF manifest, rather than treating cached search OCR as the final mathematical source. The bars in the upper-limit notation were visually checked.

The 1985 full text was not recovered. Its bibliographic identity and attribution are verified from the problem source and Korevaar's publication list; its proof was not independently read.

## Catalogue and prior report

The exact catalogue URL, https://www.unsolvedmath.com/problems/2307017, was attempted first but was inaccessible to the web reader; a direct request returned HTTP 403. The pinned UnsolvedMath import provides the full statement. Its research report says that the problem was open as of the 2018 edition and that no resolution was located. This conflicts directly with the update on the very source page. That report is source triage, not a proof attempt or proof certificate.

Dataset revision: 37e53eabe540fb458758e198be61634bd02ee008.

- problems.json SHA-256: 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf
- research_results.json SHA-256: 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b
- Selected review hash: bec6dd51007601dd5df1737d6548a0bf9056e10a3f19c08273277caa3350c730
- Selected statement hash: 96bdbc5b53b58f4bb2d68b1ba023f64854326f0d48057abb88d34ff4634841c5

The cached source files were hashed and matched the live repository's manifest. Only the selected records were extracted; no corpus or source scans belong in the publishable packet.

## Scope caveats

1. Distinctness matters. The printed source does not explicitly require distinct or increasing samples. The intended distinct/increasing interpretation is corroborated by the separated-sampling theorem cited above. If arbitrary repetitions are permitted, the literal statement is false: PROOF.md Section 6 gives a counterexample even when the repeated sequence tends to infinity.
2. “Type” means a signed limsup. Sparse zeros prevent replacing it by an ordinary limit.
3. Neither alpha=pi/2 nor alpha=-pi/2 is in the domain assumed by the problem.
4. The identically zero function is covered by the -infinity convention.
5. No novel proof method or priority claim is established by this reconstruction.

## Duplicate and repository checks

Read-only checks of AlecKriebel/Math on 2026-10-04 found:

- main at 6a112842592930803e459f013484062787ce7772;
- rank 591 row still queued, 0/5;
- no 2307017 entry in state.json;
- no attempts/2307017 directory (contents endpoint returned 404);
- no matching PRs for the numeric ID or Function Theory 7.17, no matching branch, and no code-search matches for the ID or AMR code;
- no selected ID in review_v2/related_target_groups.json;
- the full pinned statement corpus has one exact 7.17 target. Nearby Korevaar problems concern other claims and were not relabeled.

These checks are bounded searches, not a proof of absence of every possible duplicate. No remote file, queue cell, branch, issue, PR, or status was changed during this attempt.
