# Slowly growing image inradius: qualified obstruction and remaining gap

2305005 / AMR-022-5005. Five mathematical approaches; the literal-limit formulation remains unresolved in this investigation.

The report gives a complete construction of polar-complement domains with image inradius tending to infinity arbitrarily slowly. Applying the domain theorem attributed to Fernández in the original problem collection refutes every divergent upper-envelope criterion for bounded Taylor coefficients. The actual image of the provided map is only contained in the constructed domain: convergence of its own inradius to infinity has not been established. The original 1984 article and proof remain unavailable; the historical input is explicitly qualified.

REPORT.md contains the mathematical work. CLAIMS.json gives scope and accounting. SOURCES.json contains public verification metadata and references, with no source text or dataset bodies. FIXTURES.json and verify.py provide exact finite controls and integrity verification, not a proof of the analytic existence theorem or the unresolved assertion.

Use Python 3.12 or later. Supply the externally recorded SHA-256 of MANIFEST.json, obtained separately from the packet:

    python -B verify.py --root . --manifest-sha256 TRUSTED_MANIFEST_SHA256
    python -B -O verify.py --root . --manifest-sha256 TRUSTED_MANIFEST_SHA256
    python -B -OO verify.py --root . --manifest-sha256 TRUSTED_MANIFEST_SHA256

To reproduce all baseline, adversarial, relocation, and nonroot read-only controls, run:

    python -B controls.py --root . --manifest-sha256 TRUSTED_MANIFEST_SHA256

Run this command as an ordinary nonroot POSIX user. It creates disposable copies in the system temporary directory and does not change the original packet. The read-only control explicitly checks that both new-file creation and appending to an existing file are denied.

The verifier is read-only and standard-library-only. It rejects an altered manifest before trusting its file list, rejects symlinks and nonexact JSON number types, checks the exact inventory and payload hashes, and recomputes the finite identities. Run it on a read-only copy as an ordinary nonroot user. Its output does not depend on optimization mode.

Optional local source rehashing uses --problems, --research, and --pdf, each followed by the local path of an already authorized source file. Source files are not included and are never executed. Whole-file hashes and selected-record hashes must match the published metadata.

No theorem-proving software, network request, package installation, remote write, or queue update is performed by the verifier. A separate adversarial acceptance review remains to be performed.
