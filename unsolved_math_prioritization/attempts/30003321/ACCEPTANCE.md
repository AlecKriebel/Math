# Independent acceptance report

Problem 30003321. Review date: 10 October 2026.

## Review status of this edition

This is an AI-assisted mathematical proof accompanied by an independent internal AI mathematical and source audit. The authored documents are unrefereed. Acceptance records that audit's full affirmative verdict within the stated source theorems and NBG/global-choice setting. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or exhaustive-priority claim. The proof dependencies were checked against the authenticated author manuscript, not a byte-authenticated publisher PDF.

## Decision

**ACCEPT: complete affirmative proof for the full stated target. No required mathematical correction.**

Every discrete initial ordered additive subgroup of No has an order-group-isomorphic copy that is an initial subgroup of Oz. The review covers set-sized and proper-class groups in NBG with global choice, including the trivial group. Neither multiplicative closure nor preservation of the source simplicity order is assumed.

The reviewed manuscript is pinned by SHA-256 `5844d5646e90761d0760a94ea8cb975c4da6eaa36efefc8e7567553c988608aa`, byte count 10,925. This independent review is distinct from the author's self-review. It is not a formal-machine verification, journal referee acceptance, or priority certificate.

## Decisive checks

- The original [Kaplan–Ehrlich question](https://ems.press/content/serial-article-files/46663), PDF page 44, and [Question 9.1 in the later author manuscript](https://elliotakaplan.github.io/Number_systems_with_simplicity_hierarchies_II.pdf) match the target.
- The actual additive-group characterization was checked against its full primary-source context. All its canonical-Hahn-image, truncation, cross-section, exponent-initiality, coefficient-initiality, and right-predecessor hypotheses are used correctly.
- Discreteness forces the least positive element to be a single term and forces a genuine minimum exponent -alpha with coefficient group 2^(-n) Z.
- An independent inverse confirms injectivity of the exponent rotation. An ordered-concatenation proof verifies the full prefix identity and all cross-branch comparisons at arbitrary ordinals, including limits and their successors.
- No new right-predecessor relation is introduced. In particular, the normalized bottom coefficient group acquires no dyadic-divisibility obligation.
- Every individual reverse-well-ordered set support is preserved. The transport uses the source group itself rather than silently completing it to a full Hahn product.
- Every required unit monomial survives, including the separate bottom-monomial normalization. Coefficient groups are identified exactly, not merely included in larger groups.
- NBG class replacement and elementary comprehension suffice for the new explicit construction. No proper-class support or stronger class recursion is introduced.
- The image has nonnegative exponents and integral coefficient at zero, so the final containment in Oz is valid.

The detailed mathematical audit supplies the full transfinite verification and explains why no proof patch is required. The explicit inverse is an optional expository strengthening.

## Independent computational and integrity diagnostics

The independent sign-sequence checker uses Cantor-normal-form ordinals below omega^4 and run-length sign words. Its 15 minima include zero, finite ordinals, omega, limit successors, omega squared, and omega cubed + omega + 1. Each completed run checks:

- 6,960 sampled source nodes across the 15 minima
- 2,436,256 ordered pairs
- 140,596 sampled proper-prefix checks
- 750 finite-support coefficient-additivity checks
- Four adverse mathematical mutations, all rejected

The mutations omit the branch-sign deletion, leave the minimum nonzero, omit bottom-coefficient scaling, and append the plus instead of prepending it. These tests are diagnostic; they do not establish an all-ordinal or proper-class theorem. The written proof does.

Execution modes: ordinary, -O, and -OO Python. All three completed successfully and produced identical diagnostic results before the final inventory was sealed. The audit inventory verifier passed a positive fixture and rejected nine adverse fixtures in each Python mode: changed, missing, extra, or symbolic-link files; stale seal; duplicate path; wrong target; unsafe path; and altered release boundary. These are byte-integrity checks, not mathematical verification.

## Status and limitations

The reviewed manuscript was preserved unchanged. This edition contains the complete authored proof, mathematical audit, acceptance, and permitted public citation and verification metadata.

The mathematical verdict is unconditional within the stated source theorems and NBG/global-choice setting. The known discrete-subdomain theorem is not being substituted for the group problem. A bounded literature search found no later resolution, but novelty and current open-problem status are not certified. No claim is made about the adjacent dense-group set-model question.
