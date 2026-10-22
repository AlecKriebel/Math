# 30002278 / OWR-12331-002: variable acoustic PML energy

**Broad target unresolved after two approaches.** This package rules out the
specific δ,F Lyapunov family displayed in the source for a smooth monotone face
damping profile, using compatible layer-supported initial data with zero
auxiliary fields. It does not rule out different or further augmented functionals
and does not establish PDE instability.

The profile-gradient mechanism is already identified in the original report and
in later literature. The exact ansatz obstruction and its initial-data limitation
are proved explicitly; no novelty is claimed.

- [Proof and exact unresolved gap](OBSTRUCTION.md)
- [Source equations, conventions and current-literature audit](SOURCES.md)
- [Exact checker](verify_obstruction.py), [receipt](verification.json)
- [Research log](RESEARCH_LOG.md), [status](status.json), [readiness](readiness.json)

Run `python3 verify_obstruction.py`. The 9,539 exact rational controls verify
energy identities and the positive witness integral, not an instability theorem.
The [separate adversarial AI review](review/REVIEW.md) passed this scoped
obstruction, with 21 independent symbolic controls. This is not human peer review.
The proof is preserved byte-for-byte as the reviewed snapshot; its pending-review
sentence records its pre-review freeze. The physical-region-only initial-data
class and the general coercive monotone-functional request remain unresolved.
