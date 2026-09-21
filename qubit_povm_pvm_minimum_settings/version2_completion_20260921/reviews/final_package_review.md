# Final independent package verification

Checkpoint: 2026-09-21T15:29:13.411760+00:00. Completion estimate: **100%**. No unresolved blocker found. This supplement leaves the earlier, package-bound `verifier_review.md` unchanged.

## Final result

The exact final source ZIP has SHA-256:

`b301f82654bbebfdc3d91c3b0c7569d7a83e9cff9ffd0eb2b420cf6e82b52104`

Its clean-extraction reproduction completed successfully with Lean run `20260921T150935Z-9ebb22fc`. I independently checked the actual files and receipts, without starting another Lean build. The wrapper receipt SHA-256 is `fc957c3a83bee4e50eabbec9d03a8f7dcd14b927edf6b27d5c2792ceb6b5b850`.

- The exact-artifact, preflight, Lean and PDF commands all exited successfully. All four wrapper log hashes and all **138 Lean-run command log hashes** match. The sole nonzero Lean-run command is the intentionally invalid proof control.
- All **104 protected proof/verifier inputs** match the workspace, frozen stage and final replay. All **68 production modules**, followed by `Bell`, were built. All **78 contract examples in seven files** were checked.
- I independently parsed the raw axiom log: all **826 public declarations**, from **837 total theorem/lemma declarations**, appear exactly and use only `propext`, `Classical.choice` and `Quot.sound`.
- The ZIP matches the frozen stage exactly, with **1,268 manifest-covered files** plus the root manifest. Exact membership, per-file hashes, ZIP CRC and safe regular entries pass. The consumed manifest hash matches the final reproduction receipt.
- The output binding and outer manifest hashes match every listed output. All **10 LaTeX archive members** match the shipped manuscript sources and license byte for byte. Snapshot and copied final receipt match their authoritative run-specific originals.
- I independently rerendered both shipped and rebuilt PDFs using Poppler at an 850-pixel longest dimension. All **37 publication pages and 37 review pages** match exactly in rendered PNG hashes. The rebuilt PDFs are **not byte-identical** to shipped PDFs; both byte hashes and the visual equality are recorded honestly in `BINDINGS.json` and the review evidence.

The certificate inside the immutable ZIP intentionally records the earlier successful run `20260921T145457Z-083d0c3b`. Its receipt is successful and has exactly the same protected input snapshot as the final replay. The final exact-ZIP replay is preserved outside the ZIP, avoiding self-referential archive hashes. The earlier failed run is historical evidence and is not substituted for either success.

## Scope and limitations

This is an independent AI-agent verifier/package review, not external human peer review. Compiler/runtime, hardware and separately provisioned compiled dependency artifacts remain disclosed trust assumptions; the project proofs were rebuilt, but Mathlib was not independently rebuilt. The certificate covers the principal results and stated model bridges, not every auxiliary manuscript proof. PDF comparison establishes equality of the actual rendered pages at the recorded resolution and does not assert byte equality.

Machine-readable evidence: `evidence/final_package_review.json`. Earlier adversarial regression evidence records the repaired missing-contract, attributed-declaration, required-endpoint, receipt, manifest, archive-binding and PDF-binding failure cases. Full verifier tests passed **50 cases**, with **10 additional source-inventory regressions**. Frozen stage, ZIP and proof inputs were not changed during this final review.
