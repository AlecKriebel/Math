# Supplemental acceptance of the C1 corrected release

Date: 2026-10-04. Problem 30001721 / OWR-4800-012, rank 621.

## Decision and exact scope

**ACCEPTED. C1 is resolved. There are no outstanding required corrections from the original audit.** Mathematical status remains **unsolved**, with five substantive approaches, valid auxiliary results, and no proof or counterexample to the universal target.

This is a binding continuation of the original independent audit, not a new literature search or a relaxation of its limitations. Acceptance applies specifically to:

- Corrected release master manifest SHA-256: `1fbdf52823eca55c48ba8718a45a948d5df08cc1a2670e403c63fe9a2e99a67a`.
- Corrected author manifest SHA-256: `d0b38ae74653f2041d18bf5b2f300ff6b80a7ba079b2133c2e119ff5c474a3b2`.
- Original author manifest SHA-256: `407db7c0739ad6ec9fb9417fac74cb60f35924c1e04623f0938b772d7acab070`.
- Preserved original audit manifest SHA-256: `58b4d7bd87ec37c4d035d09ff172da781353a715977f19622585d3b3e0ab7f38`.

The frozen release and original audit were not edited. This separate supplemental packet records the completed review and supersedes the frozen release's historical “awaiting”/“pending” reviewer-binding statements for this exact manifest only. It also closes C1 without rewriting the original audit's request or original binding.

## Exact correction checked

The sole code change replaces `tested_basis_permutation_orbits` by `algebra_cases_evaluated` and adds `basis_permutation_quotient_used`. The corrected JSON reports cases evaluated as 32, 12, 1, 485 and quotient flags as false, false, false, true.

These are the intended meanings: the first three cases evaluate labelled supports; the fourth evaluates 485 basis-permutation representatives while counting all 8,748 labelled supports. The actual small-case orbit counts 8 and 6 have not been substituted for evaluation counts. Every other JSON datum is unchanged.

Only three files differ between original and corrected author packets: `verify_tree_controls.py`, `control_results.json`, and `SHA256SUMS`. All five author narrative/metadata files are byte-identical. The exact patch was independently regenerated and matches `changes/C1.patch` byte-for-byte. Every listed hash, file size, and changed-file record in the release ledger matches the actual files.

## Preservation, manifests and inventory

The release contains exactly 36 regular files, including its master manifest. The master lists exactly the other 35 files. All nested author and original-audit manifests verify. The entire original author packet and the complete original audit packet match their original directories byte-for-byte, including their manifests and bindings.

The inventory consists only of the corrected author artifacts, the preserved original author/audit artifacts, and the explicitly recorded release documentation, patch/ledgers and replay outputs. There are no symlinks, binary payloads, downloaded primary papers, source-corpus files, or additional unlisted artifacts. The release preserves provenance without distributing source fulltexts or unrelated private material.

## Fresh replay results

Fresh runs wrote all outputs outside the frozen release:

1. Corrected author full extended controls pass and produce JSON byte-identical to corrected `author/control_results.json` and the release's corrected-author replay output.
2. Preserved original author full extended controls pass and reproduce the original results byte-for-byte.
3. The independently implemented full labelled enumeration passes and produces JSON byte-identical to the preserved original independent results and the release's independent replay. It directly retests all 8,748 affine-D4 labelled supports, without an orbit cache.

Every endomorphism-dimension/trace-rank histogram matches. Counts remain Kronecker 32 supports / 8 indecomposable; D4 12 / 6; A2 1 / 0; affine D4 8,748 / 96. The explicit dual-number witness and its real-root reflection sequence also replay successfully. All mathematical acceptance and bounded-literature qualifications in the original audit continue to apply.

`verify_release_binding.py`, `binding_checks.json`, and `SUPPLEMENTAL_BINDING.json` provide the machine-checkable chain. `SHA256SUMS` binds this supplemental packet. The corrected release's master manifest was reverified after the replay checks; its bytes and inventory remain unchanged.

No remote writes or publication were performed. Acceptance of this corrected investigation is not a claim that the original mathematical problem is solved.
