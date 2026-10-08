# Author packet: 30003536

Disposition: unsolved, 5/5 genuine mathematical approaches. Start with REPORT.md and APPROACH_LEDGER.json.

The report proves partial estimates and strategy obstructions. In particular, its smooth positive local-maximum construction is not a global counterexample. CLAIMS.json preserves that distinction. SOURCES.md records credited earlier results and bounded current-search limitations. DUPLICATE_GATE.md and CORPUS_GATE.json give a bounded no-predecessor check, not an exhaustive certification.

Python 3, standard library only. Run:

    python -I -B check_math.py
    python -I -B verify_packet.py --expected-manifest-sha256 <externally supplied pin>
    python -I -B run_controls.py --expected-manifest-sha256 <externally supplied pin>

The verifier requires the actual externally supplied manifest SHA-256 from the delivery receipt; do not substitute an untrusted replacement manifest's hash. Paths resolve relative to the scripts, so replay works from another current directory and in a read-only relocation. Both scripts use explicit exceptions rather than assertion statements, including under -O and -OO. The normal mathematical output is CHECKS.expected.json.

The 12,371 checks cover exact finite algebra and scope declarations. They are regression evidence, not proofs of the analytic theorems, current global literature status, or absence of all prior work. Separate validation runs include normal, optimized, doubly optimized, wrong-claim, malformed-input, tampered-inventory and read-only relocation controls. Their external receipt is not part of the pinned author payload, so it can record results without a self-hash cycle.

There are no copied source files, source-text extracts, dataset contents, private coordination notes, or remote changes in this packet. SOURCE_METADATA.json contains only public PDF retrieval metadata. A separate independent mathematical audit is still required; no such audit is claimed here.
