# Offline verification

Use a fresh private copy of the complete audit tree. Obtain the final MANIFEST.json SHA-256 from the separate parent message; computing a replacement digest from an untrusted tree does not establish the original seal. Keep private primary-source captures private.

Run the copied verifier with the copy as `--root` and the external digest as `--expect-manifest-sha256`, under Python 3 normally, with `-O`, and with `-OO`. `-B` may also be supplied. The verifier performs no provider, Git, network or filesystem-write operation. It disables bytecode output before loading the freshly authored checker.

The verifier checks closed public/private inventories, all byte sizes and hashes, strict JSON without duplicate keys or nonfinite values, symlink rejection, exact head/base scope, ten captured PR Git blobs, the PR-authored manifest and acceptance identities, source bindings, and 5,013 finite exact mathematical checks with ten deliberate mathematical countercontrols. This does not certify universal mathematics or originality; see REVIEW.md for proofs and imported theorem boundaries.

CONTROL_TESTS.json records the pre-final-seal verifier controls on fresh copies, including deeper resealed parser/scope/check-result faults. After those records were saved, a final manifest was generated and the immutable final tree was again verified on fresh copies in all three Python modes. The final digest and final pass outputs are reported separately to avoid a self-referential manifest.
