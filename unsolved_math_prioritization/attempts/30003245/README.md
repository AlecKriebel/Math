# Bounded-house finiteness: audited partial results

Problem **30003245 / OWR-15170-007**, queue rank 866. Full target **unsolved** after **5/5 substantive approaches**. The independent audit adds no new proof-search turn. These are unrefereed authored proofs and checks; no human peer review, proof-assistant certification, or novelty is claimed.

## Accepted mathematical scope

- Every house bound for d = 1 or 2.
- House at most 2 for every fixed positive integer d, with an explicit finite cyclotomic containing set.
- The maximal abelian subfield case for arbitrary d, credited to Bombieri–Zannier.
- A totally real S3 splitting-field example for T^3 - 4T + 1, discriminant 229, disproving an all-primes inertia-fixed-field valuation-divisibility step.

The remaining target is finiteness in the **full ring of integers** of Q^(d) intersect Q_tr for d >= 3 and arbitrary house bounds above 2. The local example is a proof-step obstruction, not a counterexample to this finiteness problem.

Read [the corrected mathematical report](corrected/MATHEMATICAL_REPORT.md), [the independent audit](audit/INDEPENDENT_AUDIT.md), [the actual correction patch](audit/CORRECTION.patch), and [the finite acceptance results](audit/ACCEPTANCE.json).

## Execution correction and preserved history

The original assertion-only checker falsely reports success under Python -O after its discriminant equality is changed to a false value. Its exact original archive is preserved in audit/ as historical evidence. The corrected verifier uses explicit fail-closed checks and exact loop-coverage guards. The patch also expands decomposition-group and valuation-normalization details without changing the accepted mathematical conclusion.

Publication-stage replay reproduced the exact canonical acceptance bytes under isolated normal and optimized Python, after relocation into a path containing spaces and with hostile Python environment variables and shadow modules. Each 36-process acceptance matrix includes 16 corrected-mutant failures, 10 external-pin rejections, and exact patch reconstruction of all eight corrected files. Four additional outer archive/manifest corruption controls reject before execution. See [PUBLICATION_ACCEPTANCE.json](PUBLICATION_ACCEPTANCE.json).

To replay from this directory, first inspect the bootstrap and its pinned inputs, then run:

    python -I -S BOUNDED_HOUSE_30003245_INDEPENDENT_AUDIT_BOOTSTRAP.py BOUNDED_HOUSE_30003245_INDEPENDENT_AUDIT_SAFE.zip BOUNDED_HOUSE_30003245_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json

Repeat with -O after -S. The bootstrap verifies the outer archive, manifest, exact member set, sizes, and hashes before executing the nested acceptance harness. Finite arithmetic checks support the report; they do not mechanically certify its universal field-theoretic arguments.

Frozen reports and receipts retain their prepublication `publication_performed: false` fields and historical review state. They have not been silently rewritten. This README describes the draft-publication package.

## Source limits

As checked on 6 October 2026, [Castillo's claimed full theorem](https://arxiv.org/abs/2605.27232v2) is withdrawn; the [Man–Technau–Widmer–Yatsyna preprint](https://arxiv.org/abs/2608.11904) establishes a component-generated-ring result without the full integral-closure transfer needed here. Public-reader inspections and exact theorem-scope cautions are recorded in [source metadata](audit/INDEPENDENT_SOURCE_METADATA.json).

The earlier denied source-PDF download was honored. No source PDF bytes, hashes, or byte counts are available, and no rendered-page verification is claimed. Only authored mathematical reports, code, audits, correction patches, acceptance reports, and public verification metadata are included.

The accompanying queue edit changes only this problem's Status and Turns cells to `unsolved` and `5/5`; every other byte, including Findings and existing links, is preserved.
