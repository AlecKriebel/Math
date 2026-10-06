# Audit packet: 30006162

Read `REVIEW.md` for the mathematical acceptance and its limits. The frozen author report remains unchanged. Both exceptional-surface GPP questions are unresolved, with five approaches used.

Replay with an externally supplied audit manifest pin:

`python -I -B verify_audit.py --root <audit-directory> --manifest-sha256 <pin>`

Repeat with `-O`. Run `integrity_tests.py` with the same arguments to reproduce rejection controls and relocations. The manifest cannot authenticate itself; obtain the pin from the separate receipt. Exact inventory forbids additional files, subdirectories, symlinks and bytecode caches.

`AUTHOR_REPLAY.json` records the separately rechecked frozen author package. To replay that package, use its own verifier and the author manifest pin identified in `SUMMARY.json`. This audit archive does not include source PDFs, extracts, dataset contents or private material. `SOURCE_AUDIT.json` and `PROVENANCE_AUDIT.json` contain only public bibliographic and verification metadata.

Neither executable is a GPP decision procedure. The finite checks do not certify the infinite topological proofs or the cited source theorems. Substantial AI assistance; no claim of novelty or human peer review.
