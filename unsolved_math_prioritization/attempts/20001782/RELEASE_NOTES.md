# Audited partial-results release

The [independent audit](INDEPENDENT_AUDIT.md) passes the package as correctly
scoped partial results. The original problem remains unresolved after five
attempts. No mandatory mathematical repair was found and no novelty claim
is made.

The ten reviewed mathematical files are unchanged from commit
`a3a0c79d408ae120614dabedd7a8f8e60565949d`. The audit supplies additional
verification of full span at radius 2R, the exact groups of the paired-layer
and irrational two-coset examples, and the meaning of the restriction image.
Those details verify the existing attempts and do not start a sixth search.

The 633 controls are finite parameter cases with the limitations explained
in the audit. Reproduce them with `python verify_examples.py`; the output
must match `checks.json`. The audit-result JSON gives the digest of the
public audit report.
