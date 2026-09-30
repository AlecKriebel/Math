# 30006576: local curvature moments and odd rotational fans

**Original target unresolved; one substantive approach.** The local criterion and rotational-fan example are described in [PARTIAL.md](PARTIAL.md). [SOURCE_AUDIT.md](SOURCE_AUDIT.md) distinguishes the July2026 authors' sufficient theorem from the broader mesh characterization, and records the exact lifting and elementwise-curvature conventions.

The result is a necessary-and-sufficient leading-moment criterion on a fixed shrinking graph patch, a pair-free odd-fan realization for even polynomial degrees, an exact odd-degree diagnostic, and a conditional weighted global estimate. No full nonpaired global mesh family or complete surface Stokes result is claimed. Historical priority is unconfirmed.

Run `python verify.py` from this directory with SymPy installed. The verifier uses exact rational, polynomial and cyclotomic arithmetic; its receipt is [verification.json](verification.json). It does not use floating-point evidence to establish the result. The separate [adversarial AI review](review/REVIEW.md) passed with no correction. It independently recomputed full fan moments over cyclotomic fields: 3,745 submitted controls reproduce byte-for-byte and 4,971 independent controls pass. This is not human peer review. The historical pending-review header in the frozen mathematical snapshot is superseded by this review.
