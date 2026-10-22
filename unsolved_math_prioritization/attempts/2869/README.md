# 2869 / KP-3.71: integral-to-mod-2 homology cobordism

**Unsolved after two approaches.** The required boundary must bound a smooth
mod-2 homology ball while bounding no smooth integral homology ball.

The package includes full proofs of the standard filling-homology constraints,
the odd-torsion and three-handle requirements, and a geometric negative control:
punctured spun lens spaces have the right odd-torsion pattern but boundary S³.
Thus a chosen nonintegral filling does not establish a nonzero boundary class.

- [Deductions and exact unresolved gaps](OBSTRUCTION.md)
- [Primary-source and prior-attempt audit](SOURCES.md)
- [Exact algebraic checker](verify_torsion.py), [receipt](verification.json)
- [Research log](RESEARCH_LOG.md), [status](status.json), [readiness](readiness.json)

Run `python3 verify_torsion.py` from this folder. Standard library only.
The free chain complexes are bounded diagnostics, not manifold or kernel
certificates. The actual spun-manifold computation is in the proof artifact.

The [independent adversarial review](review/REVIEW.md) passes this explicitly
unresolved package. All 312 author assertions and 118,054 independent exact
controls pass. This is AI review, not human peer review. No novelty, nonzero
kernel element, or injectivity result is claimed.

Reproduce the independent receipt with `python3 review/independent_checks.py`.
The review includes its exact frozen author snapshot and replay dependencies.
