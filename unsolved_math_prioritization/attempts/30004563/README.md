# 30004563 — five centers in a cube move

**Current status: complete counterexample passed separate adversarial AI review; claimed solved, awaiting human review.**

The proposed upper bound of three potential centers for alpha>1 is contradicted by an alpha=16 realization with at least five new centers. This claim includes an incoming center, six distinct fixed boundary vertices, noncollinear alternating triples, and the original crossing-allowed source setting.

- [Independent adversarial review](review/REVIEW.md): full PASS; 13,948 fresh exact checks
- [Candidate proof](CANDIDATE.md)
- [Exact verifier](certify_five_centers.py), using only standard-library integer/rational arithmetic
- [Full exact certificate](turn2_exact_certificate.json): 6,987 checks pass
- [Source audit](SOURCE_AUDIT.md), [source manifest](source_manifest.json), and [readiness](readiness.json)
- [Research log](RESEARCH_LOG.md) and [continuity](continuity.json): two recovered substantive turns; historical count remains unknown
- [Exploratory numerical search](search_general_roots.py) and [search receipt](turn2_numerical_search.json), retained for reproducibility but not used as proof

Run the proof checks with `python3 certify_five_centers.py`. No NumPy, SciPy, or floating-point package is required for certification. The exploratory search alone uses NumPy and does not certify any result.

The frozen candidate and metadata retain their original pre-review status labels for hash integrity; the later independent review above supplies the current disposition. The mathematical proof and exact author certificate are unchanged.

The certificate proves at least five centers. It does not claim that five is maximal, nor resolve the different proper-embedding question. This is AI-generated and unrefereed research; historical priority remains unconfirmed. No source PDF or render is included for redistribution.
