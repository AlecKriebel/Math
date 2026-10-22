# Author packet: 30000962 / OWR-1967-011

Start with RESULT.md, then PROOF.md. TURN_LEDGER.md records exactly five mathematical approaches. The unrestricted target remains unresolved. Independent review is pending.

## Replay

Python 3.10+ with the standard library is sufficient.

    python -I -S -B check_math.py
    python -I -S -B -O check_math.py

Both commands should print exactly CHECK_RESULTS.json: 4,043 bounded exact diagnostic checks. These are arithmetic and algebraic controls, not a formal proof or a q-holonomicity computation for a knot.

Authenticate MANIFEST.json against the SHA-256 in the separate freeze receipt before trusting this snapshot. The integrity command requires that external pin:

    python -I -S -B verify_packet.py --manifest-sha256 THE_EXTERNAL_PIN

It verifies the closed flat inventory and every listed byte count/hash, and replays the diagnostics in a clean temporary directory. It does not prove the mathematical claims. The manifest is an inventory, not a self-authenticating signature. Verify the checker against its separately supplied hash before executing code from an untrusted copy.

The packet contains authored mathematics, diagnostics, results, and public source/provenance metadata. It excludes original source PDFs/text, raw corpus records, and private coordination. SOURCE_AUDIT.md explicitly records failed source-PDF download and screenshot attempts; the metadata contains no unverified PDF hashes.
