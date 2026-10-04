# Function Theory 4.9: a previously resolved diameter conjecture

Numeric catalogue ID: **2304009**. Code: **AMR-022-4009**. Queue rank at review: **574**.

**Recommended disposition: already_solved, 1/5.** The original degree-independent component bound is false. This package verifies a known resolution; it makes no new-discovery claim.

For every real `0 < d < 4` and every positive integer `N`, some monic complex polynomial has at least `N` distinct connected components of its closed unit sublevel set, each of diameter greater than `d`. Taking `d = 2` disproves the original assertion at `c = 1`, where `1 + c^2 = 2`.

- [PROOF.md](PROOF.md): full reconstruction with explicit separated segments and careful monic normalization
- [SOURCE_GATE.md](SOURCE_GATE.md): exact scope, historical resolution, prior-report correction, and source-access limits
- [ATTEMPT_LOG.md](ATTEMPT_LOG.md): one substantive verification response and its audit targets
- [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json): bibliographic provenance and retrieved-byte hashes
- [verify.py](verify.py), [CHECKS.json](CHECKS.json): exact rational geometric and normalization controls
- [verify_manifest.py](verify_manifest.py), [SHA256SUMS.json](SHA256SUMS.json): artifact integrity
- [STATUS.json](STATUS.json): scope and classification

Run `python3 verify.py` and `python3 verify_manifest.py` from this directory. The controls check the finite algebra and geometry appearing in the proof; they do not replace Hilbert's lemniscate theorem or certify the mathematical proof by themselves.

The asymptotic questions in the source's update, concerning sublinear or subpolynomial growth with degree, are separate. No such estimate is established here. The construction does not produce an explicit degree bound or coefficient list.

This is AI-assisted research verification, not human peer review. At author freeze the independent audit is pending. Source PDFs, source extracts, catalogue/report corpora, and private working records are intentionally excluded.
