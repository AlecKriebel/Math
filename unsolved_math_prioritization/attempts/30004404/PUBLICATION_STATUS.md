# Audited negative answer to the literal universal OWR question

Problem 30004404 / OWR-17471-010. Accepted mathematical disposition: **claimed_solved, 1/5**.

The figure-eight knot is hyperbolic and has no finite nonmeridional surgery. Its zero filling is a torus bundle, whose fundamental group is metabelian. Thus every rank-two free subgroup of the knot group has a nontrivial second-derived word killed by zero filling. This refutes the literal universal assertion in Motegi's OWR 8/2020 question, printed p.493.

The complete [proof](package/PROOF.md), [source and quantifier analysis](package/STATEMENT_AND_SCOPE.md), and [independent audit](audit-independent/AUDIT.md) are preserved byte-for-byte. The audit concludes PASS with no required mathematical corrections. Historical “independent audit pending” wording in the frozen author package records its earlier state; this file and the complete audit record the accepted disposition.

The printed Question 7.1 in the April 2026 preprint is also formally phrased with an arbitrary hyperbolic knot. Do not relabel that wording as existential. The separately meaningful existence question, whether at least one hyperbolic knot admits a persistent rank-two free subgroup, remains unresolved by this counterexample. No first-solution or novelty claim is made; the ingredients are classical and the priority search is bounded.

## Verification

Run `python3 verify_release.py --self-test` from this directory. It checks the safe-only release inventory and hashes, both frozen manifests, byte-identical original and independent outputs, and rejection of four altered-package controls. The author checks include 30,625 exact parameter pairs; the independent implementation checks 10,125 matrix parameter pairs and a non-metabelian negative control. Neither replaces the universal proof or the credited topological classification.

This is extensively AI-assisted research and independent AI review, not formal proof-assistant certification or human peer review. The package includes only authored mathematical materials, source identity metadata and complete portable review materials. Source PDFs, screenshots, full imported texts and corpora are excluded. The proposed repository change is a draft PR; no merge, release, DOI or outside outreach is part of it.
