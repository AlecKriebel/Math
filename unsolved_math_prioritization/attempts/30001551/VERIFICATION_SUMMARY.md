# Verification summary and acceptance boundary

Problem 30001551 / OWR-4425-006 remains unresolved by this work. The accepted result is the attributed partial theorem in `PROOF.md`, reviewed in `AUDIT.md` and bounded by `ACCEPTANCE.json`. The original candidate's verification note preceded this separate audit; this summary records the combined verification history without treating earlier verification as external peer review.

## Written mathematical review

The audit read the complete submitted proof and relevant primary articles. It checked the balanced reduction, indexed two-letter injectivity including equal and empty images, the nonperiodic erasing profiles, two-deletion block cancellation, coordinate-axis kernel cases, the commutation-subsystem proposition, and both erasing-witness restrictions. It retained nontriviality and the common nonperiodic hypothesis. The distinction between nonperiodicity and linear rank is explicit. These are mathematical arguments, not deductions from finite samples.

The accepted two-line terminology patch was applied to an isolated copy using strict Git patch checks. The distributed proof is exactly 8,762 bytes, SHA-256 `789e66432d69e98b18230efdf629a7cf55238fd54a040fa2e9195a34692af50f`. Neither original sealed package was altered.

## Recorded computational verification

The candidate's independent verifier used a different equation generator, exact base-3 evaluation, and set differences rather than the original searcher's bit operations. The audit independently reconstructed both complete finite families in C++ with exact length-delimited binary integer evaluation, without the original pair-pruning step. Python comparisons checked combinatorial counts, every signature bit, direct evaluation of every representative, and all distinct-signature triples.

- Maximum side length 8; binary witness image lengths 1–2: 157,800 equations, 216 morphisms, 5 signatures, 10 signature triples, zero independent triples on the pool.
- Maximum side length 7; binary witness image lengths 1–3: 28,216 equations, 2,744 morphisms, 15 signatures, 455 signature triples, zero independent triples on the pool.

The common solution for each searched equation is `[a,b,epsilon]`. Repeated signatures cannot supply all three deletion witnesses. Exact equality uses no floating-point or randomized comparison.

The candidate rejected six deliberate search-output mutations and checked positive independent pairs, separate/common-solution confusion, reused or reversed witnesses, periodic impostors, single-projection insufficiency, and unbalanced-periodic behavior. The audit's nine corrupt-result controls and seven additional logical controls passed in normal Python, `-O`, and `-OO`. Sanity rechecks reproduced 98,441 two-erasure tests, 57,798 erasing-profile tests, and 1,617,840 commuting-slice tests. An adverse control shows why the injectivity argument cannot be applied to periodic morphisms. The pairwise-commutation triple demonstrates necessity of the common nonperiodic hypothesis.

Address and undefined-behavior sanitizer runs of the audit reconstruction matched. Leak checking could not run under the execution environment's tracing mechanism and is not claimed. These computations and logical controls corroborate the written proof, not universal nonexistence. Preparing this edition did not rerun the mathematical searches or extend their scopes.

## Source verification

The original Karhumäki contribution and the complete relevant Nowotka–Saarela (2022), Saarela (2024), and Holub–Žemlička (2015) texts were inspected during the recorded research/audit. Decisive pages were visually checked. Exact scopes, public URLs, PDF hashes, and byte counts are retained in the two source metadata files. The original workshop's unrelated contributions were not treated as dependencies.

The original 36-member candidate inventory and the 44-member audit inventory were verified against externally supplied SHA-256 digests. The recorded source-gate inventory had 23 verified members. Edition preparation rechecked the unchanged candidate and audit inventories and the externally pinned validation receipts. The original integrity verifiers passed again in normal Python, `-O`, and `-OO`; all ten audit integrity adverse controls were rejected in each mode. Integrity checks authenticate recorded bytes, not mathematical truth.

The candidate inventory digest is `6a149dd5ea848857f600d5819b424427e5b2b6b4fdf6b57900205ad01783ca21`; the audit inventory digest is `68c3def3d73eac6204e65d3096700712689fc2d80fddecf9fab2af1740b321a2`; the audit validation-receipt digest is `185b396aa015c2418d736d846cbe3f4158c559be203c484b687e9753dcd1fa5f`. These are verification metadata, not copies of the underlying inventories or source content.

## Explicit exclusions

No independent triple was constructed and no complete nonexistence proof was obtained. There is no conclusion about arbitrary witness lengths or alphabets at the searched equation lengths, no exclusion of common erasing nonperiodic solutions, no new general bound below 17, no novelty certification, and no exhaustive later-literature claim.

The edition is an unrefereed AI-assisted exposition and independent internal AI audit. No external human peer review, journal acceptance of these authored documents, formal proof-assistant certification, or fresh source inspection during edition preparation is claimed. Executable code, copied sources, and raw computational data are outside this edition.
