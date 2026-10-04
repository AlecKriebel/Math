# Function Theory Problem 1.39: corrected scoped investigation

**Unsolved, 5/5.** Neither sharp constant is determined. No positive-index admissible example or improved unrestricted bound is established.

**Mandatory correction:** read [REVIEWER_CORRECTION.md](audit/REVIEWER_CORRECTION.md) together with [the frozen proof](public/PROOF.md). Proposition 4's displayed estimate needs the origin-cancellation term `(k-p) log(1/r)`. The correction gives an explicit counterexample to the original display and a complete corrected proof; the theorem conclusions survive. The author has independently checked and accepted this correction.

The [complete independent audit](audit/AUDIT.md) passes only the corrected scoped bundle. It is an independent AI review, not human peer review or formal verification. The frozen author files remain byte-for-byte unchanged, so the original status file's pending-audit field records the freeze-time state; [AUDIT_STATUS.json](audit/AUDIT_STATUS.json) gives the review disposition.

- [Author packet and source limitations](public/README.md)
- [Five substantive approaches and exact remaining gap](public/RESEARCH_LOG.md)
- [Modular construction obstruction](public/MODULAR_OBSTRUCTION.md)
- [Author SHA-256 manifest](public/SHA256SUMS)
- [Audit SHA-256 manifest](audit/AUDIT_SHA256SUMS)

The 131 author controls and 324 correction controls reproduce their stored outputs exactly. They are finite algebraic and inequality checks; the analytic arguments are reviewed separately. The historical bounds 2 and 7 remain attributed background because the original Shea-Sons proof was unavailable. No novelty or priority certification is claimed.

Run the scripts in their respective directories with Python 3 and SymPy, and run `sha256sum -c SHA256SUMS` in `public` and `sha256sum -c AUDIT_SHA256SUMS` in `audit`.

Author manifest SHA-256: `27fa158bea7288368c1e1b5b275f72b4e78ca7166bfda923c9ab90e77da41eae`.

Audit manifest SHA-256: `c400c9e9be35b47997dd69cb40eda8a0ed5b984d2040f1ec411ccaea03f17557`.
