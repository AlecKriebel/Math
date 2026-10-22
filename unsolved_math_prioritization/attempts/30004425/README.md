# Tropical wall crossing: qualified prior-results correction

Problem 30004425 (OWR-17473-001), rank 750. **Unsolved, 1/5.**

The general piecewise-linear relation is a published Escobar–Harada result. The standard-monomial semigroup bijection requires a common Gröbner cone. The published example disproves universal additivity and universal agreement with either geometric map. No new theorem, counterexample, novelty, or universal resolution is claimed.

Read [the corrected report](author/corrected_safe_freeze/REPORT.md), [the explicit scope and conventions](author/corrected_safe_freeze/PUBLICATION_SCOPE.md), and [the controlling delta acceptance](delta_audit/DELTA_ACCEPTANCE.md). The corrected package passes. The original author freeze and initial audit are preserved unchanged; their pending/REVISE_REQUIRED wording describes historical snapshots. The delta acceptance closes exactly the finite/finitely-generated terminology correction and the stale queue-header interpretation correction.

The common rows, valuation order, and vertical lattice normalization remain explicit qualifications. Normality, saturation, additivity, and a direct algebraic map between special fibers are not inferred from convex-body maps. The stronger general semigroup classification is not supplied.

## Reproduce

From this directory, run `python3 verify_publication.py`. Python's standard library suffices. It checks the complete file allowlist and hashes, all four preserved archive memberships, both author manifests, both audits, exact output replay, and the four code mutations. The independent arithmetic also rejects eight false strengthenings. Run `python3 -O verify_publication.py` to check the delivery verifier does not depend on optimized-away assertions.

All scholarly source PDFs, extracted source text, raw dataset records, and private coordination files are excluded. Public metadata records retrieval and inspection scope; it does not assert a rehash of both complete upstream corpus files. Source review and mathematical arguments are not proof-assistant certification or exhaustive literature search.

This draft changes only this row's Status, Turns, and Findings in QUEUE.md. Its historical embedded header, every other row, Chat, and DOI are preserved byte-for-byte. No merge or release is part of this publication.
