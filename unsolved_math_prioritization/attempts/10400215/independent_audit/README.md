# Independent acceptance of 10400215

Decision: ACCEPT_UNCHANGED_AS_SCOPED_PARTIAL_RESULTS. The target remains unsolved by this attempt, 5/5 approaches. Start with `AUDIT.md` and `ACCEPTANCE.json`. Original author freeze bytes are not changed; no correction patch is required.

This packet contains only the authored independent mathematical audit, exact diagnostic code, acceptance/boundary replay results, and public verification metadata. It does not contain source PDFs, extracted source text, images, imported dataset records, or private coordination.

The external bootstrap authenticates the complete flat audit inventory before executing either audit script. It also authenticates all five original author external files listed in the acceptance, runs the independent exact controls, reruns the author's entire isolated positive/negative replay matrix through the independent harness, and compares each output byte-for-byte with the frozen result.

From a directory holding the external files, use:

    python -I -S -B SHADOW_NORM_10400215_INDEPENDENT_AUDIT_BOOTSTRAP.py SHADOW_NORM_10400215_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json audit-root author-input-directory

Repeat with `-O` before the bootstrap filename, and after relocating `audit-root` and the five author inputs. `audit-root` is a clean extraction of the independent audit ZIP. `author-input-directory` contains the original author ZIP, external manifest, bootstrap, freeze receipt, and validation receipt. No network or third-party package is needed; the full negative matrix uses POSIX symlinks and FIFOs.

The external validation receipt records the actual normal/optimized relocation acceptance checks and audit-boundary rejection tests. Finite algebra tests supplement the written proofs; they do not certify topology, literature completeness, historical novelty, or a solution to the universal conjecture. The frozen audit's statements about the earlier author review status are historical rather than silently overwritten.
