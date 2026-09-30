# Fantappiè denominators: prior geometric characterization

The reduced denominator consists precisely of the affine factors associated with nonzero algebraic vertices. Thus the original vertex-product equality holds exactly when every nonzero mandatory triangulation vertex has a tangent cone that is not a signed sum of line-cones.

This characterization is credited to Akopyan–Bárány–Robins, *Advances in Mathematics* (2017), with the transform identities of Gravin–Pasechnik–Shapiro–Shapiro. It is not a new discovery.

- [Exact criterion, source match and pole argument](SOURCE_STATUS.md)
- [Source audit and qualifications](SOURCE_AUDIT.md)
- [Exact checker](check_denominators.py) and [284-assertion receipt](check_results.json)
- [Pinned statement](source_record.json), [source hashes](source_checksums.json), [readiness](readiness.json), [research log](RESEARCH_LOG.md)

Run python check_denominators.py with SymPy installed. The checker uses exact arithmetic and writes check_results.json beside itself. It verifies finite examples, not the general theorem.

Recommend already_solved with no new substantive attempts. [Separate adversarial review](review/REVIEW.md) passed, with 6,463 independent exact controls and no required correction. The origin factor, denominator reduction, unit density and original vertex convention are retained explicitly.
