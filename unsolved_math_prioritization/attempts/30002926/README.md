# Condensation profiles: a physical-clock obstruction

**30002926 / OWR-13856-002. Original Gamma-profile existence question unresolved; 1/5 approaches. Separate review pending.**

The [proof](CLOCK_OBSTRUCTION.md) establishes a necessary clock constraint using the actual branching model. A nonzero deterministic Gamma profile on t(1−fitness) must have rate 1−beta. An explicit positive-mutation strict-condensation example therefore contradicts the source's displayed rate-one formula in its stated physical clock.

This does not establish the existence or shape parameter of a clock-corrected profile. The source-normalization caveat is part of the result, and no novelty claim is made.

- [Sources](SOURCES.md)
- [Readiness and scope](readiness.json)
- [Research log](RESEARCH_LOG.md)
- [Exact checker](verify.py) and [receipt](verification.json)

Run `python3 verify.py` in this directory. Finite controls verify algebra; Sections 3–5 of the proof contain the branching, mutation and random-normalization arguments. No simulation or fitted profile is used.
