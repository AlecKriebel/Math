# Degree Bounds for Degenerate Herman Rings

**Unsolved for the intended unrestricted periodic target. Five approaches completed.**

This release preserves the exact frozen author packet in `submission/` and its complete independent audit in `audit/`. Read [RELEASE_ADDENDUM.md](RELEASE_ADDENDUM.md) first: it records the citation correction and the audit-approved proof and scope clarifications without rewriting historical files.

The independently reviewed restricted result is **N <= d-1 for individually invariant Jordan curves** of a degree-d rational map, assuming each curve lies in the Julia set, carries dynamics topologically conjugate to an irrational rotation, and is not a boundary component of a periodic rotation domain. The periodic spherical-circle subcase has at most one circle. These conclusions are not a bound for arbitrary-period degenerate curves or cycles.

For periods dividing L, the corresponding restricted estimate is d^L-1. Its dependence on L is essential to what was proved. The intended unrestricted periodic problem remains unresolved. The source's literal Siegel-disk omission is documented as a definition-scope warning, not an intended-problem resolution. No novelty or sharpness claim is made.

## Read and replay

- [Audit report](audit/AUDIT_REPORT.md)
- [Exact audit corrections](audit/EXACT_CORRECTIONS.md)
- [Frozen restricted proofs](submission/PARTIAL_PROOF.md)
- [Five approaches and remaining gaps](submission/APPROACH_LOG.md)
- [Source gate](submission/SOURCE_GATE.md)

From this directory, with Python 3.10 or later:

    python verify_release.py
    python -O verify_release.py
    python negative_controls.py

The release verifier checks the exact payload, both original manifest bindings, and replays the author and independent finite controls. Negative controls mutate isolated temporary copies. These are reproducibility checks, not formal proofs or novelty certificates.
