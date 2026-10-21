# Reproducibility

Python 3 with the SymPy version pinned in requirements.txt. Run from this directory:

    python -I -B verify_manifest.py
    python -I -B -O verify_manifest.py
    python -I -B run_checks.py
    python -I -B -O run_checks.py
    python -I -B test_corruption_controls.py
    python -I -B -O test_corruption_controls.py

run_checks.py itself executes all four mathematical programs both normally and under -O, in disposable directories. It compares every saved result byte-for-byte and stdout as complete JSON, including every enumerated block and every reported count. Original package references are never overwritten. It rejects any Python assert node in a package checker. The corruption suite likewise runs each control normally and under -O. Running the individual mathematical programs directly writes their local result JSON; prefer the isolated replay runner.

REPLAY_RESULTS.json records the full normal/-O replay. CORRUPTION_CONTROLS.json records the selected failure controls. MANIFEST.json excludes only itself; verify its externally reported SHA-256 separately for anchoring. It checks exact file inventory, lengths, SHA-256 and frozen provenance. Neither hashes nor these controls authenticate an untrusted distributor.

PROVENANCE.json records original source hashes and package hashes. Mathematical programs changed only by removing workspace-specific file prefixes. Guard conversions were performed by the primary authors before the freeze and reviewed in the authored independent audit; this package performs no further guard conversion. RESULTS.md only loses its coordination closing sentence. SOURCE_GATE.md has a sanitized distribution paragraph, and SOURCE_METADATA.json includes only public-URL artifacts rather than local extracted records or renders.
