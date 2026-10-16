# PR789 whole-preprint audit round 01

REPORT.md and VERDICT.json accept the exact prepared version1.0 with zero required mathematical/package repairs and one low, nonblocking documentation note about the separate frozen wrapper-control harness on macOS /var TMPDIR. Priority remains unresolved.

Authenticate MANIFEST.json and verify_packet.py against the SHA-256 pins supplied outside this packet before executing code. The flat manifest includes every authored file except itself. Example, with both externally supplied pins and absolute ordinary paths:

    python3 -I -B verify_packet.py --packet-root /absolute/whole_preprint_round01 --expected-manifest-sha256 MANIFEST_PIN --expected-checker-sha256 CHECKER_PIN --replay

Add --preprint-root /absolute/exact/preprint to freshly authenticate all151source files,58original Git blobs and six distribution files. Without that option the checker verifies the sealed receipts and independent diagnostics and reports zero freshly hashed source/distribution/body files. It never requires or redistributes third-party bodies. Optional body-custody receipts separately record139hashed files; this is not a reading claim.

Run test_packet.py with --packet-root, both pin arguments, --scratch pointing to a new owned ordinary directory, and optional --other-python /absolute/python to reproduce positive normal/optimized relocation and negative custody/scope controls. Write its stdout outside the sealed packet. The recorded controls were run on a preseal snapshot; the final closed packet was then independently rechecked. No mathematical proof or novelty oracle is implemented.

The original source commands and their four runtime/mode receipts are preserved. run_reproductions.py reruns the source's ten-process --replay in each of four outer modes and writes receipts in this directory; use only in an unsealed working copy. run_controls.py uses sibling scratch and writes its receipt in this directory; likewise rerun only in an unsealed copy. prepare_notes.py regenerates reading metadata and is not an entrypoint for verifying a sealed packet.

For the separate historical test_publication.py harness, set TMPDIR to an owned absolute nonsymlinked path. Its default /var temporary ancestry is correctly rejected by the strict wrapper on this Mac; its unchanged24controls pass with the ordinary path. Core verify_source.py --replay passes without this adjustment. Preserve all58immutable originals and the exact reviewed v1package.

Full source reading and finite computations do not equal formal proof-assistant certification or human external peer review. No firstness, exhaustive absence or current worldwide-open certification is made. No individual was contacted, and this reviewer made no Git/PR/release/deposit/tracker/account changes. Primary full bodies/extracts/renders remain excluded sibling scratch. This authored audit is CC BY4.0; third-party materials retain their own rights.
