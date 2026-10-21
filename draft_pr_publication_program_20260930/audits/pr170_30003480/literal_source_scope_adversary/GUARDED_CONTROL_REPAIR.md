# Narrow guarded-control repair

UTC: 2026-10-12T12:13:47.458404+00:00

The scientific verdict remains PASS. All first assessment/input identities/seals, source bodies, historical receipts, REVIEW.md and DERIVATION.md are preserved byte-for-byte and remain 0444. This repair changes computational controls and inventory metadata only. Audit completion estimate:100%.

The original EXACT_CHECKS.py and its result remain historical artifacts with their original bytes. Their explicit Python assertion statements are removable under python -O. Consequently that original checker must not be treated as an optimization-safe validator: a reported successful optimized run of it alone does not certify that those assertions executed. This limitation also applies to its byte-identical retained private-scratch original. The earlier ordinary-mode result is retained as historical finite arithmetic evidence.

The active controls are GUARDED_EXACT_CHECKS.py, GUARDED_CHECKS_DRIVER.py and GUARDED_CHECKS_RECEIPT.json. The guarded checker raises VerificationFailure explicitly on invalid conditions; the driver raises DriverFailure explicitly on inconsistent outcomes. Both were statically checked to contain zero Python Assert AST nodes. They use only the Python standard library and neither borrows another reviewer's verifier.

Reproduce all controls with python3 GUARDED_CHECKS_DRIVER.py from this directory. The driver calls the checker both ordinarily and with -O. Each driver execution has two successful baseline runs plus ten rejected false-control runs. Both baseline stdout bodies are exactly identical, SHA256 776da94bf0e1bc1311ab68f4f1bab646ee00f46405cecddac5829ffd05c02da2. Each false variant is rejected with explicit status and exit code 2 in both modes, with byte-identical error diagnostics. The driver itself was also run ordinarily and with -O; these two complete receipts were identical.

| False variant | Changed mathematical input | Required explicit rejection |
| --- | --- | --- |
| q2_coefficient | Q2 prefactor 1/2 becomes 1/4 | Exact full-product Q2 changes |
| witness_roots | First root 49/100 becomes 48/100 | Roots no longer square to the coordinates |
| witness_coordinates | Positive fourth determinant becomes zero | All-positive strict cube requirement fails |
| parity_weights | Shift 1/100 from w0 to w1 on the triangle-boundary realization | Normalization and positivity remain valid, but the requested second/third marginals change |
| ghz_discrepancy | Secondary printed relation <= is replaced by>= | The purported printed union now includes the feasible GHZ tuple, so the claimed literal discrepancy is not reproduced |

The checker also confirms the exact witness products, polygon thresholds, representative parity-support boundary cases and strict H3 patch examples. **Finite controls do not prove the all-polynomial nonexistence theorem.** The unchanged written derivation supplies that universal argument.

New guarded checker identity: c5405c926d62e8dba4dea35be8d30f4bae91d8ac183a823e2722430d29b832b4. New driver identity: 511b1bc06f90ee94a51b86e1cf01aad46f9b80e0d43bf9b8162dcda0173783dd. New receipt identity: 0d6eafd59b0c2b4279547bf4d882307a99be5705382de8b27ea9c7a99e88a6eb.

The superseded current manifest had SHA256 c619559e090ea48e3ef3851ce5e366153907e872a05be73ebbfbd8f1f75d6fe6. No additional manifest snapshot or sidecar is created by this repair, so the earlier historical manifest/receipt pair remains a fixed historical record without an expanding snapshot chain. The newly completed manifest includes every retained file, including that receipt, and excludes only itself. Its hash is returned directly to ROOT.

RESULT.json explicitly whitelists the guarded checker, driver, receipt and this note as public own outputs. Full source bodies/extractions/metadata, private source renders and private scratch remain outside the public whitelist. No other scientific reviewer conclusions, historical-priority reassessment, Git/ref/remote actions or outside communications occurred.

## Direct scientific-runtime provenance

Finalized UTC: 2026-10-12T12:20:26.081632+00:00

RUNTIME_PROVENANCE.json records Python 3.14.6, its actual resolved executable bytes/hash/mode, and the directly invoked pdftotext, pdftoppm and pdfinfo binaries, each reporting Poppler 26.08.0. The updated guarded receipt also records the actual interpreter version and executable identity. The final external-input list now contains four documentary inputs and these four directly invoked scientific executables.

The older historical receipt and ROOT authentication of four declared documentary inputs did not authenticate interpreter or Poppler executable identities. That limited historical coverage is preserved accurately. The newly included runtime records are observed executable identities, not a claim that the prior documentary-only inventory was hermetic.

A nonessential otool linked-library metadata inspection encountered an unaccepted Xcode license. No license was accepted or host policy changed. Per ROOT's specified provenance scope, no transitive native-library audit was performed. Opaque tool-service internals, general OS/shell transport and transitive native libraries are not claimed to be fully inventoried. The requested direct scientific executable identities are included explicitly.

No additional historical-manifest snapshot or hash sidecar was created during runtime metadata finalization. All first seals, source bodies, historical receipts, REVIEW.md and DERIVATION.md remain byte-for-byte unchanged.
