# Whole-package adversarial audit, round 1 — PR1121 / problem 30004311

**Verdict: PASS. No actionable mathematical, reproduction, presentation, metadata or release-integrity defect was found in this frozen package.** The full negative answer to Cedó's original OWR 51/2019, Problem 9 survives this independent review. This verdict is not a historical-priority certificate, external human peer review or formal proof-assistant certification.

Audit date: 17 October 2026 UTC. Original PR head: `f86b108ac1bc024302648eee9f47f74e26c810ec`. Original full proof: 14,213 bytes, SHA-256 `68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75`. All eight original inputs were compared to their archive copies and remain identical. The queue or any earlier PASS verdict was not an authority for this audit.

## Scope and independent method

I read the complete original proof and mathematical audit, complete five-page TeX note, README, builder, portable runner, all four checker sources, their result/certificate structures, exact Zenodo metadata/deposit and package receipt. I read the current root priority documents, broad priority report and focused implication report/derivations, then independently rederived the principal mathematical deductions. I freshly retrieved nine primary PDFs, inspected the exact original question and relevant theorem/formula boundaries, and ran 20 new targeted search strings. The full source boundaries, current version histories and access failures are recorded separately; this report does not claim full-page inspection of every retrieved article.

All work was confined to `reviews/package_01/`. Both `sources/private/` and `tmp/` were ignored before any retrieval. No operative publication file, original input, PR, publication deposit, tracker, Git index/ref or remote was changed. No external individual or other shard agent was contacted. The only internal delivery is to the parent reviewer.

## Mathematical result

The exact source question was independently checked in the official OWR report, entire Cedó contribution printed 3226–3228, with visual inspection of printed 3228. It asks about a finite nontrivial simple **left** brace whose multiplicative group is metabelian with abelian Sylow subgroups, and asks for an asymmetric product of **two trivial** braces. The note preserves that full target.

My checkable deductions are in [MATHEMATICAL_REVIEW.md](MATHEMATICAL_REVIEW.md). The following are the central results of that audit:

- The full admissible normalized symmetric-cocycle definition matches the cited primary left-brace formulation. Lambda composition forces biadditivity. No initial bilinearity restriction is smuggled into the universal nonpresentation argument.
- The primary subset is identified by its group order and closure; the proof permits nonsplit twisted additive primary groups, including the order-four phenomenon at 2. Abelian multiplicative Sylows force the same-primary action to be trivial, and twisted subtraction then gives zero primary triple stars for every possible two-trivial-factor presentation. Arbitrary factors, prime powers and brace isomorphisms are covered.
- The degree-four logarithm/exponential identities are valid in characteristic five without division by five. The binary polarization, nondegeneracy and fixed-point-free cyclic action are correct. Psi gives an all-input isomorphism to the asserted direct product of semidirect groups, independently proving the circle group law.
- Every lambda map is an invertible additive map. The derived subgroup has order 400 and is abelian. Explicit Sylows have orders 625 and 32 and are abelian; conjugacy covers all Sylows without a normality assumption.
- Simplicity treats every nonzero ideal. The use of i*g in an ideal is justified by the quotient brace, not inferred merely from lambda invariance. The ring/binary cases and the two cross-action propagation steps reach all nine additive generators. Boundary cases of lowest degree four and zero binary vector are handled explicitly.
- On the 5-primary subbrace, `(x*x)*x=x^3` is nonzero. This simultaneously supplies the intrinsic contradiction with the universal lemma and proves nontriviality. It excludes every presentation, not only a familiar bilinear family or the displayed coordinates.
- The retained original fixed-set, center, derived-subgroup and explicit commutator witnesses are also correct. Fix has order 10, the center has order five, the derived subgroup has order 400 and the abelianization has order 50. The comparison statements about simple two-trivial-factor products were independently justified rather than assumed.

No hidden circularity, missing ideal-normality step, unsupported module irreducibility assumption, characteristic-two splitting assumption, finite-enumeration substitute for a universal claim, or weakened version of the original problem was found.

## Computation and adversarial certificate validation

The source ZIP was extracted into this review's ignored temporary folder. Running its unchanged portable runner produced [EXTRACTED_VERIFICATION.json](EXTRACTED_VERIFICATION.json): **four controls, eight successful runs**, ordinary and optimized Python. Exact mathematical expected JSON matched in every case. Only the declared finite runtime fields—start/completion times, Python version and per-stage seconds—are excluded. Checker/proof hashes, guard counts, witnesses, cases and other mathematical content remain compared. Both deterministic finite certificate files matched their pinned lengths and SHA-256.

I inspected how the symbolic receipt wrapper is consumed: its code hash and successful historical exit codes are checked, and the correct ordinary/optimized nested expected result is selected. The source checker programs use explicit failures and contain no removable Python assertions. All six authored Python files in the release also parse under Python 3.10 grammar.

To test that the 19,999 certificates were not tautological metadata, I wrote an additional [independent consumer](check_seed_certificates_independently.py). The frozen finite checker supplies candidate transcripts only. My consumer recomputes ring arithmetic, log coefficient, rotation, direct circle, additive operations and every inference without using the supplier's arithmetic. It verifies exact nonzero-seed coverage, every stored transcript commitment, valid prior-node references, every operation, and all nine final generators. Results are in [INDEPENDENT_SEED_RESULTS.json](INDEPENDENT_SEED_RESULTS.json): **19,999 seeds and 259,858 derivation steps independently checked**. Three deliberate corruptions—future reference, false output and changed actor—were rejected.

The bundled mathematical mutation and cocycle boundary controls also reproduced. They distinguish nonassociativity from a legitimate brace that loses simplicity, allow nonzero star squares with zero triples, reject a nonbiadditive cocycle that fails brace admissibility, exercise the p=2 additive twist, and show a nonzero triple when abelian Sylows are deliberately removed. These are falsification controls and finite certificates; the all-ideal and universal no-presentation conclusions rest on the written proofs. No claim to enumerate all 20,000 cubed triples is made.

## Exact package reconstruction and PDF inspection

All six supplied first-freeze pins matched before review and again at finalization:

| File in `publication/` | Bytes | SHA-256 |
|---|---:|---|
| `main.tex` | 16058 | `0c1705438710c03f9f3bfba42fcda9b9c83b252394944a06fdfae032d3c1eacc` |
| `output/pdf/simple-brace-counterexample.pdf` | 73549 | `dc8205d726236da7d61870806ed713ba329dbf4cdfdf049e5570d967d6b7e35e` |
| `output/simple-brace-counterexample-source-and-verification.zip` | 1116255 | `8cc6e65647ff267cb2bd57e5ba5dda4cfc05f72ac11e527517131d9422a8d93d` |
| `output/zenodo-upload-kit.zip` | 1183637 | `b357fa5222aa409ff0f2bd858ad2798fe44cc33031e250218bec3b6c452b457c` |
| `zenodo-metadata.json` | 4103 | `b9bb1fc7a23b0b6f42be10e3fc32f5dc262512d8d52a741323c82eec77b991f6` |
| `zenodo-deposit.json` | 4468 | `bc24323b9c9127fdf14cfb5ca35a969e0168171aa709bf94fafdaf35bf623f77` |

The source archive has exactly 79 unique safe members, including a manifest covering its other 78 members; all fingerprints matched. The upload kit has exactly five members. ZIP CRC tests passed and neither archive has symlinks. Third-party bodies, extracts, source images, raw responses and private paths are absent from the member inventory; the only PDF is the authored operative note. Priority metadata screens contain titles, bibliography and authored inspection boundaries, not copied abstracts. All eight original PR inputs are preserved byte-for-byte. See [OPERATIVE_PINS_AND_INVENTORY.json](OPERATIVE_PINS_AND_INVENTORY.json) and [ZIP_AND_INPUT_INTEGRITY.json](ZIP_AND_INPUT_INTEGRITY.json).

I ran the included builder **only inside the extracted source**, never against the live publication. Both ZIP files, every ZIP member, all six frozen release files and the complete generated package receipt were byte-identical to the originals. This is recorded in [EXACT_REBUILD_COMPARISON.json](EXACT_REBUILD_COMPARISON.json); the builder stdout is [EXTRACTED_BUILD_STDOUT.json](EXTRACTED_BUILD_STDOUT.json). This establishes exact reproduction in the current local Python/zlib environment. It does not assert that other compression runtimes must produce identical ZIP bytes. The frozen PDF is deliberately an input, so this is not a new TeX-compilation reproducibility claim.

All five operative PDF pages were independently rendered at 110 dpi and visually inspected. All mathematical symbols, equations, headings, page numbers and bibliography are legible, without clipping, overlap or placeholder citations. The source's mathematical content agrees with the PDF. PDF metadata matches the title, author and subject; all fonts are embedded; no JavaScript, encryption or forms are present. The 13 external annotations have the intended ORCID/bibliographic targets and all internal destination annotations resolve. [PDF_AND_LINK_INSPECTION.json](PDF_AND_LINK_INSPECTION.json) records this inspection. Some publisher web opens are access-restricted; that is not a malformed PDF link or proof of a dead DOI.

Zenodo metadata and deposit metadata are equal. The repository deposit uses the correct two local release paths; the portable kit uses their basenames and contains the same PDF, source ZIP, metadata and README. Title, author, ORCID, version, date, license, preprint/unrefereed status, AI disclosure and bounded priority caveats agree across the paper, metadata and README. Registry/primary metadata support the cited identities, with one rate-limited bibliographic lookup explicitly recorded rather than counted as successful.

## Fresh priority and implication audit

This is a separate bounded finding: **no prior full answer or verified published full implication was identified**, not a claim that no earlier answer exists. The package's prominent caveats about the inaccessible full Rump 2020/2022 bodies and incomplete final-journal comparisons, including CO 2025, are accurate and remain material. No exclusion is inferred from an abstract, failed request, low citation count or lack of a search hit.

[QUERY_LEDGER.json](QUERY_LEDGER.json) records the 20 exact fresh queries, including poor/irrelevant discovery results. [PRIMARY_FETCH_RECEIPTS.json](PRIMARY_FETCH_RECEIPTS.json), [REFERENCE_METADATA_CHECK.json](REFERENCE_METADATA_CHECK.json) and [SOURCE_INSPECTION_LEDGER.md](SOURCE_INSPECTION_LEDGER.md) record actual retrievals, current versions, source boundaries and access failures. The earlier search and citation counts were checked against their distributed ledgers; they are not presented as a fresh replay of those historical searches or as exhaustive coverage.

The serious recent candidates were checked from actual primary formulas: 2608.01884v2, 2609.20401v1 and 2609.24640v1. Their official current histories match the versions cited. The group-action lemma, CO nontrivial-factor elimination, iterated two-trivial-factor flattening and arbitrary-seed kernel-wreath elimination were independently rederived in MATHEMATICAL_REVIEW.md. They are **new audit deductions**, not published theorems falsely credited to those papers. The generic matched-product mechanism does recover the submitted brace structure, so the note correctly disclaims novelty of that formalism. Its all-ideal propagation proof and universal intrinsic obstruction remain separately necessary to the full conclusion.

These deductions exclude the inspected routes under their stated hypotheses, not every imaginable consequence of the entire literature. The existing disclosure is appropriately bounded. Closing the remaining source-access or historical-priority gaps could improve confidence but is not represented as accomplished here. No outreach was prepared or initiated.

## Reproduction and artifact map

The review's additional certificate check can be reproduced by extracting the frozen source ZIP into `package_01/tmp/extracted/` and running `python3 -B -O check_seed_certificates_independently.py` from this review directory. The unchanged package runner and builder can then be run from that extracted directory. The additional script expects this directory layout and does not modify operative files.

`ARTIFACT_MANIFEST.json` fingerprints every authored deliverable in this review, including this report, excluding the manifest itself and ignored private/temporary material. It also repeats and rechecks the operative release pins. `RESEARCH_LOG.md` records timestamped checkpoints and completion estimates for this audit deliverable. Final estimated completion: **100% of this bounded whole-package review**. This percentage is not a probability of mathematical truth or historical novelty.

**Final disposition: PASS on the unchanged first freeze. No repair requested.** Honest priority limits remain explicitly separate from mathematical correctness and release integrity.
