# Checkpoint 3A — Computational Adversarial Review

**Date:** 2026-07-28  
**Reviewer role:** independent artifact and numerical adversary  
**Final verdict:** PASS

## Initial NO-GO findings

The numerical core reproduced, but the first publication review rejected six
semantic weaknesses:

1. several JSON norm labels did not name their metrics;
2. checks performed on the leading 25 pairs were described too broadly;
3. one realized stochastic event was mislabeled as coverage;
4. floating-point support enumeration was described as an exact or certified
   minimum-enclosing-ball computation;
5. an effect-calibrated synthetic stochastic illustration was described too
   much like a prospective predeclared study; and
6. script, requirements, run-command, and path-independent provenance were
   incomplete.

A second review found one narrative mismatch: the prose said target-free
quantities were computed before solving the reset target, while the
implementation's helper solved both together. It also noted that, for two
routes, the radius crossing is equivalent to half the pair crossing rather
than independent evidence.

## Repairs

- Named Euclidean and retained-Hessian norms in every relevant field.
- Directly checked the analytic cell formula on all 97,461 pairs.
- Scoped top-25 and 1,000-sample checks in their machine-readable names.
- Replaced the coverage label with a realized lower-bound consistency label.
- Made half the diameter the operative target-free bound and called the
  support search exhaustive floating-point enumeration.
- Marked stochastic noise and bandwidth as deliberately effect-calibrated
  before random-number generation.
- Added a working-directory-independent output path, exact run command, and
  SHA-256 script and requirements hashes.
- Separated retained-system construction from the validation-target solve so
  certificates are computed first.
- Replaced “independently” with “equivalently” for the two-route radius rule.

## Independent final verification

The reviewer reran the final artifact byte-for-byte and confirmed:

- JSON SHA-256
  `89c39c6c4bb7928646d1f7e3b0cc3fecaa33363af90f7f014f92414dcdd1f1b0`;
- recorded script SHA-256
  `46308edd7ac99430885241f1cc10e50fea9a70cec500b8dcb82f0f5ba2d0b7e0`;
- matching pinned-requirements hash;
- all twelve accurately scoped checks pass;
- every pair formula is directly evaluated;
- pair and triple certificates precede target solving;
- MEB, stochastic, and narrative semantics agree with the code.

The final verdict was **PASS with no remaining blocker**.
