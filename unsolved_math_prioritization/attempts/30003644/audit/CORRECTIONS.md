# Corrections disposition

No substantive mathematical or computational correction is required. Preserve the frozen originals and retain the disposition **unsolved, five approaches used**.

Optional editorial improvements for a separately versioned future revision:

1. In `verify_controls.py`, change the comment “sign/denominator mutants” to “sign mutants,” or add actual denominator-mutant checks. The existing loop flips three signs; the README already describes that accurately. This audit supplies three actual denominator mutants in its own tests.
2. When reusing numerical certificate outputs, export hexadecimal dyadics or raw mpmath tuples, not `str(iv)` as if it were an outward enclosure. The frozen verifier does not make this error. Negative-control JSON floats are round-trip renderings of binary values, rather than literal exact-rational endpoint strings; both interpretations still contain the negative-control root, independently checked here.

Neither item changes a proved statement, the finite-height certificate, the Rouché disk, or the mathematical disposition. Do not extrapolate `|t|<=10000` to all height, reclassify the off-line zero as a counterexample, treat torus density as an exact orbit intersection, or omit the Schanuel premise.
