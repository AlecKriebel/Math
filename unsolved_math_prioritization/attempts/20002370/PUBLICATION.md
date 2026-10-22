# Reviewed partial results for AIM-LOGIC-0146

**Overall status: unsolved, 5/5.** The exact variable-minimization questions are not resolved. No new solution or historical novelty is claimed.

## Mathematical scope

The fields are the real-algebraic rational-function field and the real rational-function field, in the pure ring language with the generator unnamed. Established results imply an exact minimum of one prenex block alternation. The smallest leading universal block in a two-block separator is bounded between two and three. At least two reusable variable symbols are necessary, but their exact minimum is unknown in this work.

The packet reconstructs the known separator with consistent factorial digits, proves that a proposed diagonal compression is vacuous, and records existential-guard and bounded-degree barriers. Primary sources retain full credit. A checked rational-offset discrepancy in one source is bypassed; no author-issued erratum is asserted.

## Reading order

1. [Research overview](public/README.md)
2. [Definitions and proofs](public/PROOF.md)
3. [Full independent mathematical audit](audit/AUDIT_REPORT.md)
4. [Sanitized-release verification](audit/SANITIZED_RELEASE_REVIEW.json)

## Reproduction and version boundaries

From this directory, run:

```sh
python public/check_exact.py
python audit/independent_controls.py
```

The first output matches `public/exact_results.json` byte for byte and contains 3,364 assertions. The second matches `audit/release_independent_results.json` and contains 72,112 assertions. Its mathematical output agrees with the earlier `audit/independent_results.json`; only the reviewed-document hashes and manifest hash differ after the explicitly approved editorial substitutions. The original audit report and its manifest remain unchanged as the record of the mathematical review. The narrow receipt binds that review to this release.

The frozen proof SHA256 is `263eb37b85a357b0245a607311daf2e5680452d7ed10dbc2fd0c35ad44bfdaaa`. The release manifest SHA256 is `819c2b03e24444f35551915240574733a745c23be20d60005aa27e48706153de`.

These finite controls audit arithmetic, logic transformations and integrity. They are not finite models of the function fields and do not replace the explicitly cited theorem inputs. This is an AI-assisted, unrefereed research packet, not human peer review or formal proof-assistant verification.

## Change scope

All mathematical and audit artifacts concern only this problem. The queue change is limited to its status and turn-count cells. Source PDFs, full source extracts and imported corpus records are not redistributed. No merge or release is part of this submission.
