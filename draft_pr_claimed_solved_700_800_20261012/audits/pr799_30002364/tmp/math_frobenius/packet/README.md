# Frobenius audit packet

Read REPORT.md for the disposition, PREEXPOSURE.md for the independent mechanism fixed before candidate exposure, SOURCES.json for exact source versions/passages, and EXPECTED.json for independently recomputed finite values.

The packet is flat and closed. Raw primary-source bodies and rendering caches remain outside it, in the excluded scratch directory. No author executable is imported or run.

Obtain the manifest and checker SHA256 values from an independent channel. Before executing verify_packet.py, hash its bytes using a trusted utility and compare the checker pin; reject symlink paths. Then run with absolute paths:

    python3 -I -S -B /absolute/packet/verify_packet.py /absolute/packet MANIFEST_SHA256 CHECKER_SHA256
    python3 -I -S -B -O /absolute/packet/verify_packet.py /absolute/packet MANIFEST_SHA256 CHECKER_SHA256

The verifier authenticates the manifest against its external pin, every payload hash, and the exact inventory before running the finite checker. The verifier itself is excluded from the manifest to avoid a self-hash cycle and is separately pinned. After successful authentication, run test_packet.py with the same arguments to replay the controls. Its code has then been authenticated as a manifest payload.

The integrity boundary assumes trusted pins, Python and its standard library, and no concurrent filesystem replacement. It is not a sandbox against a hostile interpreter, OS, or same-user race. Tests include arithmetic mutations with freshly recomputed manifests, so the mathematical controls are distinct from hash failures. None of this mechanizes the geometric proof.
