# Supplemental binding acceptance

Problem 30002048 / OWR-11784-007, rank 622. Original independent auditor's continuation, 2026-10-04, 13:35-13:37 UTC.

## Decision

**ACCEPT_CORRECTED_SCOPED_RELEASE.** Both required corrections from the original audit are closed in the exact release snapshot identified below. This is a binding correction review, not a new theorem, expanded claim, or historical-priority determination.

Accepted release identifiers:

- Root MANIFEST.sha256: `15b87ed1e163d1f07d6d66dc8d32354b98aa3c62c6e218e8ee02790971099bb2`
- Corrected author/MANIFEST.sha256: `cba75811450e787073452b49549169d07316a5f4f5294de5524997236c017c63`
- Corrected author/PROOF.md: `697b031dfc8e7c65d83854d8dcf5bcbfc4f9000b6e8769166d6b38999f45f3f4`

The original audit remains bound to manifest `8673ca5bd15366eaa567d101f8ee18026957d202bd3b4eac53bf761e11ec40e9`; the original author freeze remains bound to manifest `4a4a0478c91311606382e2ae00aa891d93272992593724e976589ab9ef65cf6c`.

## Correction closure

**C1 closed.** ROUTES.md Route 2 now uses |B_j(f)|=1 for coprimality of f with x^j-1 modulo every rational prime, and explicitly gives the equivalent condition |A_m(f)|=1 for every divisor m of j. This is correct for the monic integer polynomials under discussion: the resultant is an integer, its reduction is nonzero exactly when the reductions are coprime, and an integer avoiding divisibility by every prime is +/-1. Multiplicativity supplies the all-divisors equivalence. The erroneous single-A_j assertion is gone from the corrected manuscript.

**C2 closed.** PROOF.md Section 5 now states f(x)=P(x)(x+a)+r(x), explicitly multiplication, with a integral and r in the finite residue set. This agrees with the degree-nine derivation and both original certificate implementations.

The corrected files are exactly the original files with these two audit-proposed replacements. There are no other content changes among the ten author content files. The author manifest differs only in its two corresponding hashes. APPLIED.patch is byte-identical to the original audit's proposed patch; DIFF.patch independently matches the actual two-file changes. This directly establishes the intended result without relying on the preparer's account of patch execution or fuzz settings.

## Inventory, preservation, and replay

- The root manifest covers all 38 other files in the release, with no omitted or extra file. No symlink was found.
- All nested manifests pass: corrected author, preserved original author, and preserved independent review each cover ten content files.
- All eleven original-author files, including its manifest, are byte-identical to the frozen original source directory.
- All eleven original-audit files, including its manifest, are byte-identical to the complete original audit directory.
- The correction ledger's before/after identities and unchanged-certificate hashes agree with the actual files.
- The original author verifier was rerun and reproduced results.json byte-for-byte.
- The author's SymPy cross-check was rerun and reproduced CROSSCHECK.txt byte-for-byte.
- The independent verifier was rerun against the corrected author's JSON and reproduced independent_results.json byte-for-byte.
- The root inventory and all five bound identity hashes were checked again after the replays. The release was not modified.

`VALIDATION.json` records the exact replay commands and output hashes. `verify_binding.py` repeats these read-only checks when this supplement is alongside the release, original author, and original audit directories. It does not apply patches or rewrite the reviewed snapshot.

## Scope and provenance retained

The accepted scoped assertions remain exactly e(7)=5, e(8)=7, e(9)=6 and the strict degree bound for every root of unity. The full all-degree source target retains **unsolved**, with five recorded substantive routes. The remaining mathematical gap is the non-root-of-unity case in every exact degree at least ten.

The corrected manuscript retains its nonzero-algebraic-integer convention, exact-degree interpretation, C. L. Stewart attribution, credit for the known lower-bound witnesses, and explicit non-claim of historical priority. SOURCES.md, STATUS.json, and all mathematical programs and output data are unchanged. The release README introduces no broader result, and clearly distinguishes the corrected manuscript from the historical original whose two lines are superseded.

The frozen release's statements that binding review is pending describe its preparation state. This separate, later acceptance supplies the outcome for the hashes above without changing that snapshot. Historical audit statements requiring C1 and C2 remain accurate about the preserved original; they do not contradict this correction closure.

No edits to the release, original author, or original audit were made. No new source acquisition, helper, remote write, publication, or redistribution occurred in this binding review. Acceptance of the scoped mathematical snapshot does not itself authorize publication and does not certify a solution of the global conjecture.
