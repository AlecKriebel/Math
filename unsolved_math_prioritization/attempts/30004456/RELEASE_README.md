# Release layout and reproducibility

Outcome: **already_solved, 1/5**, exclusively for the normalized **nonzero** character target, by an existing 2026 preprint theorem. See ACCEPTANCE.md for all qualifications.

The original ten-file submission is unchanged under submission/. Its external FROZEN_MANIFEST.json is unchanged. The full separate independent audit, its script, source-hash ledger, decision, replay outputs and manifest are unchanged under independent-audit/. The additional files provide acceptance, the exact queue-cell change, and strict release verification.

## Commands

Run from this directory with Python 3.10 or newer:

- `python3 verify_release.py --self-test`
- `python3 verify_release.py --self-test --sources /path/to/source-pdfs`

The first command requires the exact complete release file set, checks all release/frozen/audit hashes and reruns the source-free producer controls. Its negative controls reject a missing internal manifest, altered proof, missing audit, altered audit, and an extra file.

The second command additionally checks four independently obtained source PDFs and reruns both the producer's source mode and the original independent auditor's complete mathematical controls. Source filenames and primary URLs are recorded in independent-audit/SOURCE_CHECKS.json. No downloads are automatic. Missing or changed PDFs cause this explicit source mode to fail. The wrapper copies sources only to an ephemeral verification directory; they are never added to this public layout.

The audit script itself can also be run in a separate working copy after placing the four source PDFs in independent-audit/private/. Do not add that private source directory to the public release. The strict wrapper deliberately rejects extra public files.

## Historical versus fresh results

Frozen submission/CHECK_RESULTS.json has `manifest_payload_files_checked: 0`; that historical capture occurred before its manifest existed. Its values are unchanged. The new final-layout replay returns 9 for that field, while the external frozen manifest binds 10 payload files including the internal manifest. Source-free replay checks zero PDF hashes; explicit source replay checks four. Neither mode is presented as the other.

FINAL_LAYOUT_CHECKS.json contains both fresh modes and the strict negative controls. RELEASE_MANIFEST.json hashes every other release file, including these outputs. The manifest itself is identified in the publication receipt/commit, avoiding a self-hash cycle. Finite computations and byte integrity are not proofs of the all-automorphism theorem or certificates of external peer review.
