# Reproducibility and its limits

Use Python 3.9 or newer; no third-party packages or network access are required.

    python -I -B verify_manifest.py
    python -I -B -O verify_manifest.py
    python -I -B run_checks.py
    python -I -B test_corruption_controls.py

The verifier checks exact inventory, rejects symlinks, validates SHA-256 and byte counts, checks frozen report versions and provenance, and preserves UNSOLVED/five-avenue scope. The replay runner tests normal and optimized modes with assertion-independent checks. Corruption controls operate on disposable copies and exercise equal-size manuscript corruption, deletion, injection, symlinks, acceptance-version mismatch, and provenance mismatch. In the latter cases manifests are recomputed to ensure the semantic metadata checks themselves reject the change.

These are integrity/replay controls, not a formal proof checker. No numerical or toy-chain experiment is substituted for the motivic geometry, adjunction, orientation, primary theorem imports, or audit. No external source/dataset bytes are bundled or re-downloaded by replay. Their hashes attest the recorded inspection inputs, not independent source authentication. The historical audit covers its original manuscript hash; the normalization audit covers the packaged derivative. Self-contained hashes detect selected accidental tampering but do not authenticate against an adversary able to rewrite all reports and checkers. Trust the separately recorded manifest digest and mathematical audit provenance.

Running the commands produces stdout only inside the package; temporary disposable copies are outside it. Saved receipt JSON files document the packaging run. They are not promises of future external source availability.
