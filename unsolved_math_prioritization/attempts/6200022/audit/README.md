# Audit of Delzant diagonal convex cores

Read AUDIT.md for the acceptance decision, source scope and independent proofs. The unchanged author freeze is identified by its SHA-256 in PUBLIC_METADATA.json and is not embedded in this package.

Run with Python 3.10 or later, from any working directory:

    python /path/to/audit/verify.py
    python -O /path/to/audit/verify.py

The verifier checks the exact package allowlist and SHA-256 manifest, then independently replays the arithmetic. VERIFY_TESTS.json records the tested normal, optimized, relocated and adversarial runs. No original PDF or corpus is required for replay. Do not create output or Python cache directories inside the package.

These are computational integrity and auxiliary arithmetic checks, not formal verification of the geometric proof. AUDIT.md gives the mathematical audit. Trust the externally supplied archive digest to identify this exact artifact; the manifest is not a digital signature.

To repeat the mutation suite in temporary directories:

    python /path/to/audit/test_integrity.py

To include independent tests of the unchanged pinned author archive:

    python /path/to/audit/test_integrity.py --author-archive /path/to/KLEINIAN_BOUNDARY_6200022_AUTHOR_SAFE_FREEZE.zip

The latter command reproduces the complete VERIFY_TESTS.json receipt: four positive and 28 negative runs for each package.
