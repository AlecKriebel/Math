# 10600020: minimal virtual-knot realizations

**Original target unresolved, 2/5 approaches.** The nonzero homology case is
Dye's prior result. The null-homologous case cannot reach that criterion through
surface homeomorphisms. A conditional compression-circle test follows from
Gabai's solid-torus surgery theorem, but the required nonsplit circle has not
been produced for every minimal representative.

- [Proof of the conditional test and exact gap](OBSTRUCTION.md)
- [Source and current-literature audit](SOURCES.md)
- [Exact algebraic controls](verify_obstruction.py), [receipt](verification.json)
- [Research log](RESEARCH_LOG.md), [readiness](readiness.json), [status](status.json)

Run `python3 verify_obstruction.py`. The controls do not certify link splitting,
minimal genus, or the unresolved geometric existence step. The [separate adversarial AI review](review/REVIEW.md) passed the scoped
partial, with 724 independent exact diagnostics. This is not human peer review.
The proof is retained byte-for-byte as the reviewed snapshot; its pending-review
sentence records its pre-review freeze. No novelty claim is made.
