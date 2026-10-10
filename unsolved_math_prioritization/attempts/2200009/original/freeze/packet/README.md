# Source-free verification packet

Read REPORT.md for the credited prior solution, the independent normalization proof and the zero-output convention. The universal theorem is due to Leake and Ryder, not to this report. Independent review is pending.

The distribution has a bootstrap.py and AUTHOR_MANIFEST.json beside a packet/ directory. Before executing any file, compare the bootstrap SHA-256 and manifest SHA-256 against the separately supplied external trust record. Merely accepting hashes shipped inside an untrusted replacement package provides no authentication.

From any directory, run:

    python -I -S -B /path/to/freeze/bootstrap.py
    python -I -S -B -O /path/to/freeze/bootstrap.py
    python -I -S -B -OO /path/to/freeze/bootstrap.py

The bootstrap checks the fixed manifest pin, strict manifest schema, exact flat payload inventory, regular-file types, byte counts and hashes before running verify_math.py. Its exact output must match EXPECTED.json. It also checks the source-independent CLAIMS.json semantic contract.

After successful authentication, run:

    python -I -S -B /path/to/freeze/packet/run_controls.py

The controls use only temporary copies and require a nonroot account. They replay all three interpreter modes, verify relocated read-only files with failed write probes, and test integrity rejection, hostile code/imports, malformed metadata and exact-type semantic mutations. The original distribution is read-only during the final acceptance run. No Python assert statements are used for required checks. The verifier itself uses exact fractions and standard-library modules only.

No source document, copied source passage, dataset or private coordination file is included. SOURCES.json records historical retrieval and inspection metadata; replay does not claim to re-read or mathematically re-prove those sources. The source PDFs can be independently retrieved from the versioned URLs and compared to their byte counts and SHA-256 values. The old queue's open status was stale.

All tests are finite diagnostics, not a replacement for the cited theorem, an independent mathematical audit, a novelty certificate, or GitHub CI. No external state change is performed by the replay.
