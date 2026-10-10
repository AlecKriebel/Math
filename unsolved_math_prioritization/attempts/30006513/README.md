# Permutation modules: prior counterexample and source-scope repair

Read ACCEPTANCE.md and the complete authored audit and source repair in accepted/. This releases the binary prior-proof-availability hold for the broadened catalogue. It does not solve the original finite-relational homogeneous OWR question. Credit Bojańczyk–Fijalkow–Klin–Moerman, TheoretiCS 2024, Theorem 4.16 and Appendix B; zero new proof-search turns.

## Public reproduction with independent trust

Obtain the fixed BOOTSTRAP.py SHA-256 from the reviewed PR description, authenticate it before execution, and copy that authenticated file outside this packet. Do not choose a new trust anchor from the download being verified. Set all packet files to 0444 and directories to 0555; run as actual UID=EUID=1000:

    python -I -S -B /trusted/BOOTSTRAP.py --controls /path/to/packet
    python -I -S -B -O /trusted/BOOTSTRAP.py --controls /path/to/packet
    python -I -S -B -OO /trusted/BOOTSTRAP.py --controls /path/to/packet

Without --controls, the same authenticated bootstrap performs positive verification only. The bootstrap binds the verifier, manifest and mutation harness. The manifest binds every other delivered byte, including accepted historical files, current verification code, declarations, pre-seal receipts and raw stdout/stderr references. Only the manifest and bootstrap are excluded from their own manifest; their hashes are bound outward. Final receipts remain outside the inventory and are pinned externally in the reviewed PR description.

Current output must match complete raw mode-specific stdout/stderr and recursive exact JSON types, values, identities and counts. Empty, malformed, altered, skipped, expected-failure and wrong-mode success outputs are rejected for fixed reasons. Physical create, append-open and unlink denials are exercised under UID/EUID1000, with before/after whole-packet hashes. Hostile current-directory and Python environment imports must match the full clean baseline. The interpreter and standard library remain trusted; modes provide an accidental-write barrier, not protection against root or deliberate owner chmod.

Only current code has explicit optimization-safe guards. The retained historical checker uses assert and writes an adjacent result file; historical execution is NOT_RUN. The fresh checker neither imports nor runs it. Finite algebra tests support small cases only, and do not certify the infinite proof, original OWR question, positive LICS theorem proofs, or excluded historical sources. All seven accepted input files remain byte-identical. No source bodies, datasets, private sources, private personal or coordination material, or identifying metadata for excluded private material are included. No QUEUE change.
