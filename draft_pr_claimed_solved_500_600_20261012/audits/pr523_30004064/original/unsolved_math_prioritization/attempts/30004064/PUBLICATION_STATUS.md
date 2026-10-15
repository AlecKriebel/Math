# Problem 30004064: exact-dual recovery

Status as of 2026-10-04: **independently audited negative answer to the literal exact-minimizer formulation**. This package is for draft review; it is not a peer-reviewed publication.

The exact dual objective has unique minimizer zero for every noiseless binary datum. A full-row-rank 3-by-3 row/column tomography example has exactly two binary solutions and five common pixels, but the prescribed sign recovery loses all five. Both recovery clauses in the exact formula fail.

The source paper already acknowledges the scalar zero-minimizer obstruction. No novelty or historical-priority claim is made. Finite-iterate algorithms, smoothing procedures, and reconstructions using an additional primal variable are outside this conclusion.

## Read the result and its review

- [Complete proof and interpretation limits](public/PROOF.md)
- [Source and prior-work gate](public/SOURCE_GATE.md)
- [Substantive attempt log: 1/5](public/ATTEMPT_LOG.md)
- [Complete independent adversarial audit](audit/AUDIT.md)
- [Frozen candidate manifest](public/FROZEN_MANIFEST.json)
- [Audit manifest](audit/AUDIT_MANIFEST.json)
- [Publication-file manifest](PUBLICATION_MANIFEST.json)

The independent audit passes without requiring changes to the frozen candidate. Publication review accepts the same restricted scope. Statements in the preserved frozen README about awaiting review record its earlier freeze state; the full audit and this dated status record the completed review.

## Reproduce the exact checks

Run from this directory:

```sh
python3 public/verify.py
python3 audit/audit_verify.py
```

Both use only the Python standard library and exact integer/rational arithmetic. The original verification checks 1,044 binary images, 1,458 objective identities, 729 projected-objective cases, and eight scalar approximation identities. The independent audit adds 528 enumerated binary images, 1,400 exact box-feasible objective identities, and larger line-sum-family checks. These checks supplement the universal proof rather than replace it.

Only authored proof, audit, verification files, and integrity metadata are included. No paper copies, extracted source text, catalogue dumps, or copied implementation code are included. Queue changes are restricted to this problem's status, turn count, and previously blank findings cell.
