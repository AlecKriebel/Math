# PR95 exact reproduction

The tested runtime is CPython 3.12.14 with NumPy 2.3.5. Python 3.9+ syntax is intended; other runtimes need fresh execution. The two lattice programs need only the standard library. NumPy arrays in verify.py hold arbitrary-precision Python integers with object dtype; certificate arithmetic is exact.

From the clean extracted archive root:

    python3 -E -B verification/run_all.py --output-dir /a/new/empty/directory

Output must be absent/empty and outside the archive root. Every run is fresh. First the runner verifies every member in PAYLOAD_MANIFEST.json and rejects missing, changed or unsafe paths and every symlinked file or ancestor directory component beneath the package root. It runs all three programs normally and with -O, then arithmetic false-target copies in both modes. Each false target must raise an explicit exception, exit nonzero, emit no success stdout, and create no author success JSON.

Child flags are -E -B, plus -O for optimized runs. PYTHON* variables are removed and LC_ALL=C set. Complete records capture input snapshots, argv, actual PID, UTC start/end, Python/NumPy versions, exit and full streams. Inspect a fresh exit/status; included earlier results cannot establish a new pass.

## Mechanisms

1. verify.py: original full 126-label modular-word computation, repaired guards and artifact binding to pr95_note.tex. Exact coefficient targets are unchanged. It writes verification.json in the child's fresh output directory.
2. independent_checks.py: earlier distinct root-lattice route in Z[zeta10], explicit guards and corrected sine-product comment. Historical field exact_assertions=2005 counts finite explicit checks.
3. root_lattice_check.py: fresh independent reconstruction in Z[zeta50], 625 representatives and 120 Weyl permutations, q=1,2,3,4,6,7,-1,-2, exact orientation/inverse/periodicity/S3 controls. Floating fields are diagnostics only.

The lattice programs separately implement the same published theorem; they are not independent foundation proofs. The full modular-word route is a distinct finite mechanism. The manuscript table can be checked by hand.

SOURCE_PROVENANCE.json identifies authenticated original and repaired/public sources. recorded_results.json and recorded_processes/ preserve actual current V2 assembly executions as historical evidence. The final clean-extraction run is separately retained in private preparation evidence, leaving archive bytes fixed. Frozen V1 receipts remain in the preserved V1 sibling; their successes did not test the repaired ancestor-directory guard.

The payload manifest excludes itself to avoid recursive hashing. The external SHA256SUMS includes the ZIP: establish a trusted archive digest first. A mutable manifest alone cannot authenticate authorship or protect against simultaneous replacement of manifest and payload. Hashes identify bytes, not proof correctness, novelty, priority, peer review or release authority.

Ordinary full modular-category and RT/Hansen-Takata surgery results are imported inputs. No copyrighted source PDFs, extracted texts, source-page images, private source-audit receipts, raw retrieval headers or credentials are included.
