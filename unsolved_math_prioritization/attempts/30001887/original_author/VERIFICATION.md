# Verification record

Author-side verification, 2026-10-05 UTC. An independent mathematical audit has not yet been performed.

Successful deterministic run of `python3 verify.py`:

- 48 exact balanced-splitting recurrences, with one-less-than-threshold controls
- 30,648 finite closed-interval minimal-cover cases
- 4,149 ordered congruent-interval cases across closed, open, and half-open boundaries
- 157,888 finite-type multiplicity/incidence cases and 15 pigeonhole boundary controls
- Exhaustive two- and three-color enumeration of hub constructions for s=2,3,4
- 352 exact rational geometric witness-incidence checks across those hub examples
- Four exact-rational strict union-bound thresholds
- 2,727 sample half-plane subsequence checks; the universal result is proved in the text

Negative controls reject an all-equal purported three-coloring, the missing strictness at the union-bound equality case, the one-below balancing threshold, and a deliberately colliding geometric encoding.

The first control run failed because the initially chosen malformed-spacing fixture happened not to produce incorrect incidences. This was a defect in the negative-control fixture, not a mathematical result. The fixture was replaced with two identical singleton edges at insufficient spacing; the test then detected the intended spurious incidence. The final report is from the complete successful rerun. No failed result was represented as a pass.

A relocated replay from a separate temporary directory produced byte-identical JSON. All mathematical universal claims retained here have written proofs; none relies on extending these finite enumerations beyond their stated bounds.
