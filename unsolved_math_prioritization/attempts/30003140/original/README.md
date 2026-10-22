# 30003140: bounded arithmetic partials, unresolved

The full target is the modularity association of the two specified antisymmetric weight-two Borcherds products at levels 713 and 893. Both associations remain unproved here after five approach families.

Read RESULT.md for complete proofs of the partial claims and the exact unresolved gaps. APPROACH_LEDGER.md records the chronology. certificate.json contains computed surface-side data; it does not contain an independent automorphic match. SOURCES.json and PROVENANCE.json contain public verification metadata only.

## Replay

Requirements: Python 3.10+ and SymPy 1.14.0 (the version used). No network, source corpus, source PDF, private file, Sage, database, or optimizer is needed. Standard semistable-Jacobian, Galois and cited modularity theorems remain mathematical inputs to the written proofs.

Obtain the MANIFEST.json SHA-256 from the separate frozen receipt. Then run:

    python -B verify.py --manifest-sha SHA256_FROM_RECEIPT
    python -B -O verify.py --manifest-sha SHA256_FROM_RECEIPT
    python -B -OO verify.py --manifest-sha SHA256_FROM_RECEIPT
    python -B test_negative_controls.py --manifest-sha SHA256_FROM_RECEIPT

The negative-control program runs all three interpreter modes, with three relocated positive replays, 21 repinned mathematical mutations and 15 integrity mutations. A hash check alone cannot catch a deliberately repinned wrong arithmetic certificate; the arithmetic layer must reject those cases.

## Exact boundaries

- Twenty good-prime surface factors, four bad-prime factors and three theta parameterizations are checked.
- The source's Borcherds holomorphy/cuspidality is imported; these computations do not prove it.
- Hecke-eigenform identification, matching Hecke data and the global Galois comparison remain absent.
- Corpus/source hashes are historical retrieval evidence. Offline replay reports external sources as not replayed; it does not reauthenticate papers or repeat the literature search.
- No original source text, PDF, dataset contents, private correspondence or coordination is included.
- MANIFEST.json excludes itself and is pinned externally. ZIP and receipt also live outside the manifested directory. Bytecode caches and all other unlisted files are rejected.
- No new resolution, novelty, independent review, formal verification, publication, release or merge is claimed.
