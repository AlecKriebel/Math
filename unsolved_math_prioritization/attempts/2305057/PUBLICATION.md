# Credited negative resolution: Baernstein's Plessner question

**2305057 / AMR-022-5057 — Research Problems in Function Theory, Problem 5.57**  
**Disposition:** already solved by an existing preprint; one substantive verification attempt.  
**Resolution credit:** Oleg Ivrii, [arXiv:2609.18785v1](https://arxiv.org/abs/2609.18785v1), 16 September 2026.

The proposed capacity-zero omitted-set dichotomy is false. Ivrii's random lacunary series has, almost surely, no angular limit at almost every boundary point, while every Stolz-angle image there has planar density zero at infinity. Such an image omits a compact set of positive logarithmic capacity.

This package records an **independent AI verification of an existing result**. The full fresh audit returned PASS and found no required mathematical amendments. It is not external peer review. No new-resolution credit, historical-priority claim for the proof variant, or journal acceptance is asserted.

## Read and reproduce

- [Author's overview](release/README.md)
- [Counterexample verification](release/COUNTEREXAMPLE_VERIFICATION.md)
- [Source and attribution checks](release/SOURCE_GATE.md)
- [Full independent AI audit](audit/INDEPENDENT_AUDIT.md)
- [Deterministic controls](audit/independent_checks.py) and [recorded results](audit/independent_results.json)
- [Frozen author-file manifest](AUTHOR_MANIFEST.json), [audit manifest](audit/AUDIT_MANIFEST.json), and [release manifest](RELEASE_MANIFEST.json)

From this directory, run:

    python3 audit/independent_checks.py

Python's standard library suffices. The script verifies the five frozen author files and checks two finite arithmetic controls through index 100,000. It writes its report to audit/independent_results.json. Those controls are regression checks; the analytic proofs establish the probability-one and infinite-parameter conclusions.

The five author files and the complete audit are preserved unchanged. The author manifest and research log describe the earlier pre-audit freeze; this publication note records the subsequent PASS. Full source PDFs, source-corpus records, and operational files are excluded.

Only the queue row for 2305057 is updated. Related Problem 5.20 is discussed for mathematical context; its catalogue row is unchanged. This package does not independently certify Ivrii's separate exact-range or Hausdorff-dimension theorems.
