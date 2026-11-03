# Powerset-cover threshold: Erdős 624 (ID 2218)

Status: UNSOLVED. Five approaches yield scoped partial results, not a proof or refutation of divergent excess and not a novelty claim. Official open status is indexed historical evidence, not live verification.

Read RESEARCH.md for the five approaches, RANDOM_BOUNDS.md for full finite upper-bound proofs, SMALL_CASES.md for the exact finite reductions, and INDEPENDENT_AUDIT.md for the original mathematical acceptance boundary. SOURCE_GATE.md and SOURCE_METADATA.json describe public sources and retrieval limitations. No source PDFs or extracted third-party text are included.

Accepted exact unrestricted values H_u(1),...,H_u(11): 0,1,2,3,3,3,4,4,4,4,4. Seven positive witnesses are included unchanged. The author checker searches two reduced patterns in 46 calls; the independently implemented checker searches all three patterns without edge symmetry fixing in 72 calls. All n=12 diagnostics are excluded as inconclusive.

## Reproduction

Use Python 3.10 or later, standard library only, from this directory:

    python3 -B verify_integrity.py
    python3 -B validate_package.py
    python3 -O -B validate_package.py

-B prevents bytecode caches, which deliberately fail the closed inventory. The scripts do not rewrite certificates. COMMAND_LOG.json consolidates exact commands, complete stdout, complete stderr, and exit codes for normal and optimized mathematical replay. Validation replays and compares every byte, checks full packaged AST provenance, exercises mathematical corruptions and fail-closed inventory controls. Temporary negative-control copies are removed automatically. Failure raises exceptions, not optimization-removable assertions.

The inventory permits only flat regular files. Consequently every nested directory, including any nested manifest, is rejected rather than recursively exempted; symlinks, unexpected entries, unsafe names, altered bytes, and missing files also fail. MANIFEST.json covers every file except itself. Its external hash is frozen separately, since a manifest cannot authenticate itself. Hash checking detects changes relative to the manifest, not authenticity, mathematical truth, or historical source availability.

The added validation harness and guard transformations are packaging work, not part of the original independent mathematical audit. They require separate review. Exact original AST provenance is retained for that review; public provenance normalizes one local directory string. The numerical-constant checks supplement the analytic proof, not a finite substitute for its universal quantifiers.
