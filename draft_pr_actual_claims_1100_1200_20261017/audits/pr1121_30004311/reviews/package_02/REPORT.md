# Package 02 — PASS

Fresh independent adversarial whole-package review of PR1121 / problem30004311 / OWR-17294-011, completed 17 October 2026 UTC. **No actionable repair identified.** This decision applies only to the six exact operative inputs below. It does not use previous whole-package PASS judgments as premises, and no other whole-package reviewer report was read.

The strongest verified result is the complete mathematical negative answer to Cedó's original Problem 9: an explicit nontrivial simple left brace of order 20,000, with metabelian multiplicative group and every multiplicative Sylow subgroup abelian, has no asymmetric presentation with two trivial factors. The statement concerns the exact original question and includes every possible isomorphic presentation. No minimum-order or historical-first classification is asserted.

## Frozen identity

| Operative file relative to publication/ | Bytes | SHA-256 |
| --- | ---: | --- |
| main.tex | 16058 | 0c1705438710c03f9f3bfba42fcda9b9c83b252394944a06fdfae032d3c1eacc |
| output/pdf/simple-brace-counterexample.pdf | 73549 | dc8205d726236da7d61870806ed713ba329dbf4cdfdf049e5570d967d6b7e35e |
| output/simple-brace-counterexample-source-and-verification.zip | 1116255 | 8cc6e65647ff267cb2bd57e5ba5dda4cfc05f72ac11e527517131d9422a8d93d |
| output/zenodo-upload-kit.zip | 1183637 | b357fa5222aa409ff0f2bd858ad2798fe44cc33031e250218bec3b6c452b457c |
| zenodo-metadata.json | 4103 | b9bb1fc7a23b0b6f42be10e3fc32f5dc262512d8d52a741323c82eec77b991f6 |
| zenodo-deposit.json | 4468 | bc24323b9c9127fdf14cfb5ca35a969e0168171aa709bf94fafdaf35bf623f77 |

The eight original PR input artifacts are unchanged. The original head provenance is f86b108ac1bc024302648eee9f47f74e26c810ec and the frozen original full proof is 14,213 bytes, SHA-256 68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75. Historical proof-only-edition distribution and acceptance statements are visibly historical; the current README and provenance explain the present enlarged verification package and superseding priority reviews.

## Mathematical adversarial outcome

`MATHEMATICAL_CHECK.md` supplies the complete fresh reconstruction, including edge cases and all redundant original claims. The original question was freshly retrieved from EMS and visually read at physical PDF page22 / printed3228. Its hypotheses and requested two-trivial-factor conclusion match the operative theorem.

The direct log/quadratic coordinate map proves the full group law on arbitrary inputs, rather than extrapolating from generator tests. The lambda blocks are additive invertible maps over F5 and F2, giving the full left-brace law. Every multiplicative Sylow is covered by explicit Sylows plus conjugacy. The derived group is C5^2 x C2^4 of order400, abelian. The ideal proof uses multiplicative normality legitimately for i*g in I, isolates arbitrary mixed seeds, and reaches all nine additive generators. No irreducibility, normal-Sylow or coordinate-ideal assumption is hidden.

The universal obstruction starts with an arbitrary admissible normalized symmetric cocycle. Lambda composition forces biadditivity. Primary values and vanishing mixed values identify the full additive p-part setwise without assuming its addition splits; the p=2 nonsplit C4 case is expressly valid. Abelian multiplicative Sylows kill the same-prime action and imply zero triple stars on that full primary subbrace. Isomorphisms preserve the invariant. The example has nonzero (x*x)*x=x3, excluding every two-trivial presentation. Zero factors, missing primes and arbitrary finite factor exponents introduce no exception.

The original redundant invariants also survive independent reconstruction: Fix order10, socle0, multiplicative center of order5 with explicit x2+3x4 witness, derived order400 and abelianization order50, plus the exact oriented derived-star witness. The auxiliary fixed-complement and centerlessness results for the simple two-trivial-factor class were proved afresh in the mathematical note. No broad claim that all simple braces are centerless is made.

**Remaining mathematical gap found:** none. These written arguments are checkable proofs, not proof-assistant certification.

## Programs, certificates and guards

All four unchanged programs were read and then run through the supplied `verification/verify_all.py` in ordinary and optimized modes: eight successful runs. `REPLAY.json` records the results and exact code hashes. The comparison retains all mathematical output and guard counts, with only the declared finite runtime fields removed. The historical symbolic wrapper selects the correct result for the requested mode and checks its checker hash and successful exit statuses. Both certificate files match supplied bytes by length and hash in each finite run.

The independently authored `check_seed_certificates.py` imports no published mathematical module. It uses unital-array polynomial convolution, explicit eta expansion and coordinate rotation; it regenerates all19,999 transcript commitments in order and consumes all259,858 inference records against ideal-membership operations. All five full sample transcripts agree with those commitments, and every seed reaches the nine generators. `SEED_CHECK.json` records these results. A fresh all20,000-pair central-witness check, the triple-star calculation and associativity-breaking raw-eta and missing-Q controls also pass.

Four certificate corruptions are rejected: changed arithmetic output, a future reference, a genuinely missing x3 endpoint and changed seed. The first proposed endpoint control merely removed a redundant x4 line and correctly remained valid; this review-harness mistake was corrected and recorded, not treated as a release defect. The final consumer tests substantive generator completeness.

Six isolated runner corruptions are rejected (`RUNNER_GUARDS.json`): changed checker, original proof or expected-receipt bytes; an inserted assert with a resealed checker hash; false expected mathematics with a resealed expected hash; and a failed historical symbolic exit status. The supplied mathematical mutations and order25/order4/order36/nonbilinear/nonabelian-Sylow boundary cases were also inspected, not accepted merely because their output says PASS.

These tests supplement the all-input proof. Neither the paper nor this review claims enumeration of all20,000^3 triples or a finite certification of the universal cocycle theorem.

## Archives, privacy and exact reconstruction

`check_package.py` and `PACKAGE_CHECK.json` verify the following independently:

- The source ZIP has79 unique safe members, no absolute/traversal/backslash paths or symlink members. Its manifest covers exactly the other78 members and every member hash/size agrees with the live package receipt.
- The five upload-kit members are exactly the PDF, source ZIP, identical metadata, portable deposit manifest and identical README. Its PDF and source ZIP match operative bytes. The portable manifest paths resolve at the kit root; live deposit paths resolve under publication/.
- All eight original inputs match their audit copies exactly, and source provenance pins the stated head and proof.
- Public members contain authored analysis, code, certificates, search/version/fetch metadata and the operative paper. Full third-party article bodies, extracted texts, screenshots, raw API response caches and private coordination contents are absent. Only the operative paper is a PDF member. Known private/temp/cache paths and source-body file types are absent; content and credential-pattern inspection found no secret or private-person communication leak.
- The ignore rules for this review's `sources/private/` and `tmp/` were created **before** fresh retrieval. Its downloaded third-party bodies and renders stay in those ignored directories.

The builder was run **only in the extracted copy**. It reproduced the two archive bytes, all six operative pins and the **entire PACKAGE_RECEIPT.json byte for byte** in the current environment. The operative PDF remains a frozen input. `REBUILD.json` and `PACKAGE_CHECK.json` preserve this evidence. No live builder or operative edit occurred. As the README says, another zlib/Python compression environment may alter archive bytes while preserving contents; no universal cross-runtime byte identity is asserted.

## PDF, citations, metadata and licensing

I independently rendered and viewed all five operative pages. All are legible, with coherent pagination, visible references, consistent margins and no clipping, overlap, missing glyph boxes or placeholders. The visible mathematics agrees with the source and frozen proof. `PDF_QA.json` records the five visual checks.

`PDF_LINKS.json` enumerates41 annotations and34 named destinations. All28 internal GoTo/destination links resolve; this includes destinations nested under `/A` as `/S /GoTo`, as well as direct `/Dest` entries. All13 external URI targets are the intended author/bibliographic targets. All12 bibliography entries were inspected for their titles, identities, version labels and relevant target scope. Target resolution is not confused with full publisher-body access.

The note, README, exact metadata and deposit agree on title, author/ORCID, version1.0.0, date17 October2026, preprint/open status, extensive AI assistance, unrefereed status and CC BY4.0 for original authored materials. Third-party rights are reserved. The exact metadata description and both deposit copies contain the correct decoded author name Okniński: the apparent escape in serialized output was disproved by actual JSON decoding. No double-escaped Unicode defect exists in any copy. No external human review, journal acceptance or formal certification is claimed. The metadata expresses bounded priority limits rather than historical-first status.

## Bounded priority disposition

`PRIORITY_CHECK.md` and `SOURCE_LEDGER.json` give the source-led deductions, exact inspection boundaries and remaining gaps. Nineteen fresh searches were performed; twelve version-specific primary PDFs were retrieved (including historical/current cyclic versions), with raw copies ignored. The original question, full cocycle definition, matched-product formulas and serious recent candidates were inspected directly. Current arXiv histories match the cited versions. The archived query/citation/screen counts also match their literal README accounting.

The following new audit deductions were independently checked from actual formulas: the finite metabelian A-group action lemma; nontrivial-second-factor elimination for2401.12904v2 Theorem4.5; flattening of the iterated1705.08493v1 simple-extension route; and arbitrary-seed kernel–wreath elimination for2609.20401v1, including its T=C2 boundary. These are clearly labeled new audit deductions, not old published theorems. The general matched-product theorem recovers brace existence, while its cited simple-factor theorem cannot certify these nonsimple primary factors. The local-algebra/invariant-homomorphism work is credited; its advertised proper-ideal p-group examples do not supply the target. Nonzero inverse-Baer outputs have nonabelian addition, and their displayed undeformed seeds have nonabelian multiplicative Sylows. The current cyclic-Sylow classification has stronger hypotheses than this target.

**Strongest verified priority finding:** no identified prior full answer or verified published full implication within this bounded scope. **Exact remaining priority gaps:** Rump2020/2022 full bodies, several final journal comparisons including2025JPAA, and incomplete global literature/citation coverage. Successful DOI redirects did not yield those bodies. These material limits remain visible in the paper, README and deposit; inaccessible sources are not excluded by abstracts. They are separate from mathematical correctness. No human was contacted, and no outreach was prepared.

## Review boundary and receipt

All persistent authored work for this review stayed under `reviews/package_02/`; unchanged verification programs also used their self-cleaning temporary mirrors. No Git refs/index/remote, PR, tracker, publication or release mutation was performed. Communications were internal to root only. `RESEARCH_LOG.md` timestamps checkpoints and completion estimates. `ARTIFACT_MANIFEST.json` hashes every authored public file except itself, excludes `sources/private/` and `tmp/`, and repeats all six operative pins. A final live recheck confirms that this PASS still refers to the unchanged frozen package.
