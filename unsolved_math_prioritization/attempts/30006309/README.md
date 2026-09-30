# 30006309: combinatorial comparison of weight-polytope models

**Candidate in the cited smooth polarized toric regime; independent review pending.** The geometric equality is already known. This package proposes a direct comparison of its two combinatorial descriptions.

For Q of dimension n, projection of massive GKZ vectors on Q×Delta_(n−1) is evaluated by product-face volume sums. An alternating binomial identity cancels all terms below codimension one, leaving n·eta_n−eta_boundary. Equal-column heights, regular refinements and the standard GKZ normal-fan map supply the reverse polytope inclusion, without enumerating all product triangulations or invoking K-energy.

- [Complete candidate and proof-type boundary](CANDIDATE.md)
- [Original source, restored assumptions and prior work](SOURCES.md)
- [Exact product-vector checker](verify_product_vectors.py), [receipt](product_verification.json)
- [Pinned source record](source_record.json), [source hashes](source_manifest.json)
- [Readiness](readiness.json), [status](status.json), [research log](RESEARCH_LOG.md), [turn ledger](turns.jsonl)

Run `python3 verify_product_vectors.py`; only the standard library is needed. All1,227 exact assertions pass, including eight complete low-dimensional product examples and the finite-difference coefficients through dimension16. Nonunimodular cells, unused points and induced face-lattice normalization are included.

The checker does not prove the GKZ fan theorem or certify the full infinite family. Smoothness, complete lattice-point embeddings and the source's degree hypothesis are retained. No claim is made for arbitrary singular configurations, a foundation-free proof of GKZ theory, or historical priority.
