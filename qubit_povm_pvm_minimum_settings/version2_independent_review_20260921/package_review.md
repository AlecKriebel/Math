# Independent package and evidence review

Checkpoint: 2026-09-22T00:50:23.901384+00:00. Completion estimate: **100% of the bounded byte-integrity and verifier-source review**. Fresh complete reproduction is separate parent work. No production source, output archive, or retained receipt was changed by this review.

## Result

**No concrete packaging or evidence-binding blocker found in the exact final local ZIP.** This finding is based on independently read ZIP bytes, recomputed hashes, direct log parsing, and source inspection, not earlier review conclusions. It is not a new full Lean rerun or a mathematical statement-correspondence audit.

The reviewed ZIP is `version2_completion_20260921/output/qubit-povm-pvm-v2.0.0.zip`: **11,427,095 bytes**, SHA-256 **b301f82654bbebfdc3d91c3b0c7569d7a83e9cff9ffd0eb2b420cf6e82b52104**.

## Independently verified artifact facts

- All **1,269 ZIP members** have safe paths, are unique, and pass CRC; no symlinks, `.lake`, `.venv`, `.git` or Python-cache paths occur.
- The root manifest has **1,268 entries** and the Lean manifest **1,002 entries**. Exact membership and every SHA-256 match their respective archive contents; no missing, surplus or duplicated entries.
- The final `staging/candidate2/qubit-povm-pvm-v2.0.0` directory matches every ZIP member byte-for-byte. The older first-stage directory is obsolete and should not be used as the release source.
- All **104 protected proof/verifier inputs** in the packaged successful run match both the ZIP and the current repository. All current manuscript `.tex`, `.bib`, `.sty` and `.sh` source files match their archived copies.
- All ten standalone LaTeX TAR members equal the corresponding archived manuscript files (the license matches the project license). All files referenced by output `BINDINGS.json` have matching hashes.
- Packaged run **20260921T145457Z-083d0c3b** has 138 command records whose actual logs all match recorded hashes. The only nonzero command is the labelled deliberately invalid proof control. Its aliases identify that same run.
- Final-extraction run **20260921T150935Z-9ebb22fc** also has 138 valid command-log hashes. The outer reproduction receipt binds the exact ZIP shipment-manifest hash, the run-specific kernel-report hash and the identical embedded kernel report. All four outer reproduction command logs match their hashes.
- Independently counted **68 individual mathematical module build commands**, **78 `example` statements in seven contracts**, and parsed **826 distinct theorem dependency reports** from the final authenticated `119-axioms.log`. Parsed results exactly equal the supplied audit JSON; no axiom beyond `propext`, `Classical.choice`, and `Quot.sound` occurs.

Machine-readable results: [package_hash_audit.json](package_hash_audit.json). Historical receipts and the external second-reproduction receipt have distinct purposes; placing that second receipt outside the frozen ZIP correctly avoids self-reference.

## Reproduction helper and fail-closed checks

Read `reproduce.py`, `scripts/run_lean.py`, `scripts/check_axioms.py`, `scripts/preflight_checks.py`, the package builder and PDF builder directly. The wrapper verifies exact shipment membership before executing the four stages, stops on nonzero subprocess status, reads run-specific kernel and axiom receipts, requires matching run IDs and proof/contract success flags, and saves failure status on an exception. The Lean runner checks fixed compiler identity and dependency commits, rejects dirty tracked dependency sources, performs valid/invalid compiler controls, moves aside local project build outputs, rebuilds every project module, compiles all required contracts, parses all public theorem dependency reports, and verifies protected-input stability. Required historical baseline archives are present in the hashed package. The PDF builder requires Tectonic and rejects detected layout/reference warnings.

Fresh isolated manifest tests accepted a valid fixture and rejected modified, missing, extra, duplicate, empty, symlinked and traversal-path cases. Results: [manifest_negative_controls.json](manifest_negative_controls.json). These are actual helper calls on temporary fixtures, not proof evidence.

The documented prerequisites are Python and the two requirement files, Git/Bash, pinned Lean/Lake, Tectonic, and either separately provisioned dependency checkouts/cache or bootstrap network access. The archive correctly does not advertise standalone offline proof execution. Compiled external dependency objects and the compiler/runtime remain trusted; inspecting dependency Git sources does not authenticate those compiled objects. No independent Mathlib rebuild is claimed.

## Limits and optional hardening

The high-level reproduction wrapper relies on its verified runner to write a fresh successful receipt; it does not independently require the returned run ID to differ from the pre-run pointer. The real runner unconditionally initializes a new run and writes its final pointer, and authenticated logs show this happened. Adding an explicit old-ID/new-ID check would be harmless defense in depth, but absence of it is not a concrete failure of the shipped verified path.

The high-level wrapper binds the shipment manifest before execution; the lower runner protects proof/verifier inputs during its work. General non-proof presentation files are not frozen after every step because reports and PDFs intentionally change. The retained external bindings and final PDF/source checks are therefore appropriate release evidence.

This reviewer did not independently rerender the PDF pages or reacquire all dependencies via `--bootstrap`; those claims are not upgraded by this report. Parent reproduction should operate on a new extraction of the exact reviewed ZIP, retain its run-specific reports, and preserve the same cache/compiler trust qualification.
