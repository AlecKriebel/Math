# Independent review package for surface automorphism dimension

Start with MATHEMATICAL_AUDIT.md. ACCEPTANCE.md and ACCEPTANCE.json are the separate disposition. The accepted outcome is a prior counterexample to the universal genus-one statement, with no correction required and no novelty claim.

The original seven authored data files are preserved byte-for-byte in original/. The immutable author archive and its external manifest are in author_inputs/. Public bibliography, source inspection history, PDF hashes, and dataset verification metadata appear in SOURCE_CHECKS.json and CORPUS_VERIFICATION.json. No copied third-party PDF, extracted source text, source image, raw corpus, private source, personal data, coordination record, or private checker hash is included.

The reviewer-authored replay_author_integrity.py authenticates the original archive and external manifest against built-in public pins and checks exact directory and archive membership. It never executes author content and is not a mathematical verifier. Review or externally authenticate that reviewer script before running it. From this directory run:

    python -I -S -B replay_author_integrity.py author_inputs/SURFACE_VCD_30003902_AUTHOR_SAFE_FREEZE.zip author_inputs/SURFACE_VCD_30003902_AUTHOR_EXTERNAL_MANIFEST.json original

Repeat with -O to test optimized execution. INTEGRITY_RESULTS.json records identical normal/optimized results and 24 controls. The trusted boundary is the Python installation and authenticated reviewer code; no hostile concurrent filesystem writer is modeled.

MANIFEST.json binds every other file in this review package. The external audit manifest binds MANIFEST.json too and gives the exact archive digest and byte count. These are static integrity checks, not computer proofs.

The source classification remains an explicit imported theorem. The review does not claim an exact virtual cohomological dimension, all-subcase resolution, or a re-audit of the whole Nikulin classification. The author packet's historical pending-review status is preserved; consult the separate acceptance for the current review outcome. No repository publication was performed.
