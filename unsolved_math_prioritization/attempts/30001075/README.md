# Common tangent loci: reviewed proof candidate

The full proof is [CANDIDATE.md](CANDIDATE.md). A separate adversarial AI audit found no remaining mathematical gap in the exact source scope: see [review/REVIEW.md](review/REVIEW.md) and [review/review_summary.json](review/review_summary.json). The candidate file is preserved byte-for-byte at the reviewed hash; its pre-review header records the status when it was frozen.

The claim is OWR2008/44 Conjecture4: the union of common tangent lines to any three pairwise disjoint convex subsets of R3 is contained in a Lebesgue-null set. The stronger 2-manifold-cover conjecture is not addressed. Historical priority remains unconfirmed, and the independent AI audit is not external peer review.

Run `python verify.py` for exact local sanity checks, and `python review/independent_checks.py` for the independent diagnostics. These supplement rather than replace the proof. Source provenance and the limited novelty search are in LITERATURE.md, source_record.json, and source_checksums.json. Research chronology and the one substantive proof-attempt turn are preserved in RESEARCH_LOG.md and turns.jsonl.
