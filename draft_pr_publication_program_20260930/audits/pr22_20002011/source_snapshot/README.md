# Conformal-primitive statement: known negative answer

The literal AIM 2003 claim is false by a six-dimensional obstruction published by Branson in 2005. This package corrects the source status and gives a direct closed-torus verification of that known obstruction. **It does not claim a new discovery or resolve the repaired formally self-adjoint conjecture.**

Records **20002011 / AIM-GEOMETRY-0349** and **20002052 / AIM-GEOMETRY-0390** are exact duplicates of Conjecture 1 and its reprint as Problem 30. This is one research target and one PR.

- [Source-status correction and direct verification](SOURCE_STATUS.md)
- [Independent PASS review](independent_review/REVIEW.md)
- [Review summary](independent_review/review_summary.json)
- [Prior-report and duplicate audit](PRIOR_AUDIT.md)
- [Research log](RESEARCH_LOG.md) and [provenance](provenance.json)

The frozen source-status document retains its pre-review header. Its current status is **independent AI review passed**, with no required mathematical changes: 25 author assertions and 21 independent geometric-jet assertions passed. This is not external peer review or formal verification.

Reviewed SHA-256: `b6d39596acb84613b15c43c5a9f6d2382bbd4826348638398d793fab4cbc7463`.

From this directory, run:

```sh
python3 check_jets.py
python3 independent_review/independent_checks.py
```

Both scripts require SymPy, tested at version 1.14.0. The calculations are exact and small; the written argument separately establishes the closed-manifold and variational claims.
