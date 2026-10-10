# Shy-coupling rigidity: corrected restricted results

Problem 9500007 / AMR-094-0007 remains **unresolved, exhausted 5/5**. Read `REPORT_CORRECTED.md`, `AUDIT.md`, and `ACCEPTANCE.md` for the accepted mathematics and exact remaining gap.

This is a fresh public-only corrected derivative, not the original complete bundle. The full superseded report is omitted. The contextual patch labels removed hunks rejected/superseded, and the corrected report is authoritative. Original frozen inputs remain privately unchanged. The report's Section 9 reference to `replay_controls.py` describes historical verification; that old full-bundle driver is not distributed here. `math_controls.py` is the new derivative driver. `PUBLIC_SCOPE.json` states every omitted-input stage as NOT_RUN.

`verify.py`, `independent_verify.py`, and `CERTIFICATE.json` are byte-identical finite mathematical inputs. `MATH_REPLAY_REFERENCE.json` and its empty stderr counterpart retain every fresh positive and negative child output. The report's analytic proofs require mathematical review; code checks finite algebra only. `SOURCE_METADATA.json` and `SOURCE_REHASH_HISTORICAL.json` retain public bibliographic and byte-identification history, without source bodies or fresh publication-time source claims.

## Authenticate before execution

Obtain the exact BOOTSTRAP.py SHA-256 from the independently reviewed PR description or publication receipt. Check it without running packet code. Do not treat a self-reported hash inside an untrusted packet as an external trust anchor.

Prepare a separate copy of this complete directory with mode 0555, each file mode 0444, and a copy of the exact changed repository QUEUE.md with mode 0444. Run as genuine UID=EUID=1000, using Python 3.10 or later:

    python3 -I -S -B /trusted/BOOTSTRAP.py /absolute/readonly/packet /absolute/readonly/QUEUE.md

Repeat with `-O` and `-OO`. The trusted bootstrap must be byte-identical to the packet bootstrap. It authenticates the manifest and verifier before executing the verifier. The manifest covers all remaining delivered files and the exact external queue; the externally checked bootstrap closes the trust chain. Full fresh stdout/stderr is compared byte-for-byte and recursively by exact JSON types to the authenticated reference, with no normalization.

To rerun the publication trust-boundary controls after independently authenticating the complete packet:

    python3 -I -S -B mutation_tests.py --root /absolute/readonly/packet --queue /absolute/readonly/QUEUE.md --bootstrap-sha256 EXTERNAL_SHA256

Repeat with `-O` and `-OO`. Negative copies are disposable and may be writable; accepted input copies remain read-only. The controls reject missing/extra files or directories, symlinks, special files, malformed manifests, substituted verification code, altered acceptance and receipts, and reanchored content. Hostile current-directory modules and Python environment variables must not execute. Tests do not retrieve sources or prove the full Euclidean conjecture.
