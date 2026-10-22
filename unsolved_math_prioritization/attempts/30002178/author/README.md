# 30002178: lower bounds for sums of roots of unity

**Unresolved after five substantive approaches.** This package does not claim a proof, counterexample, verified complete prior resolution, historical novelty, or a proof of global openness.

- `PROOF.md`: exact target, full proofs of retained restricted results, and the precise gap in each of five routes
- `LITERATURE.md`: primary-source scope and quantifier checks
- `SOURCE_VERIFICATION.json`: public source hashes/sizes and inspection coverage
- `RESEARCH_LOG.md` and `STATUS.json`: approach records and final scope
- `verify_math.py` and `RESULTS.json`: reproducible exact cyclotomic tests and certified rational modulus enclosures
- `VERIFICATION.md`: why the computations certify what they claim
- `verify_manifest.py`, `test_manifest.py`, `MANIFEST.json`, and `MANIFEST_TESTS.json`: strict payload integrity and corruption controls

Run from this folder:

    python verify_manifest.py
    python test_manifest.py
    python verify_math.py --output /tmp/roots-unity-replay.json
    python -O verify_math.py --output /tmp/roots-unity-replay-optimized.json

Compare either result file byte-for-byte with `RESULTS.json`. Python 3 and SymPy are required; the recorded run used SymPy 1.14.0. No network access or private source file is needed to replay.

The tests cover 46,803 normalized multisets (m<=4 with 2<=N<=24; m=5 with 2<=N<=18), using exact cyclotomic reduction to distinguish zero from nonzero. They verify 21 exact counting identities, 12 sparse-polynomial controls, and eight semantic negative controls. No numerical cancellation is used as a zero test. These finite tests do not certify the infinite conjecture.

All source PDFs, source extracts, images, raw dataset contents, and private coordination/history material are excluded. The primary conjecture was inspected directly, but the problem website was inaccessible and the raw dataset/AI-report fields remain uninspected. A fresh independent mathematical audit and publication gate are still required. This investigation performed no remote writes.
