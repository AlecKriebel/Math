# Wild-knot quadrisecants: source-free research packet

Unsolved, 5/5 distinct mathematical approaches. Read REPORT.md, then LEDGER.json and STATUS.json. SOURCES.json records public source identities, inspection scope, and dataset hashes. Source PDFs, extracts, dataset contents, and private coordination are excluded.

This packet supplies elementary conditional lemmas and countercontrols. It is neither a full solution nor a claimed novel result. The finite checker does not certify the continuous arguments or the topology.

## Reproduction and trust boundary

The delivery contains this packet/ directory plus external FREEZE_MANIFEST.json, bootstrap.py, and BOOTSTRAP_PINS.json files in freeze/. Obtain the bootstrap and manifest digests from the separate trusted delivery receipt. A pins file bundled with an attacker-modified archive is not an independent trust anchor.

After verifying those pins, run from any working directory:

    python3 -I -B freeze/bootstrap.py packet
    python3 -I -B -O freeze/bootstrap.py packet
    python3 -I -B -OO freeze/bootstrap.py packet

Use Python 3.9 or later. Only the standard library is required. Isolated mode is important: it prevents untrusted neighboring modules or PYTHONPATH from being imported. Bootstrap also starts its verifier and finite-check subprocesses in isolated mode. Checks do not rely on assert statements, and the selected optimization level is propagated.

The manifest is outside the packet it authenticates, hashes every allowed packet file including the verifier, and rejects missing/extra files, directories, symlinks, nonregular files, invalid types and malformed JSON. The bootstrap pins both the manifest and the verifier before running code from the packet. The frozen artifact is made read-only and tested by a real non-root process. Only temporary mutation copies may be writable.

Threat model: fixed files during each verification run; trusted Python and standard library; externally trusted bootstrap/manifest pins. This is an integrity/reproducibility check, not a defense against concurrent malicious filesystem races, a compromised interpreter, or an attacker replacing all trust anchors.

The separate acceptance receipt records normal/optimized, non-root read-only, hostile-input, and relocated-archive tests. These are finite diagnostics and integrity tests, not formal mathematical certification or independent human peer review.
