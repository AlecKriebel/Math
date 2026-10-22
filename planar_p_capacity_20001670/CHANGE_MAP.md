# Corrected-release change map

Problem 20001670 / AIM-GEOMETRY-0008. Prepared 3 October 2026.

## Scope

The original problem remains **UNRESOLVED after 5/5 substantive attempts**.
The local theorem concerns sufficiently thin triangles at each fixed p only;
it does not establish global segment minimality. These edits address the two
minor rigor clarifications in the included fresh adversarial audit. They are
corrections to existing proofs, not a sixth search or proof attempt.

The original ten-file snapshot at commit
`f6b6b1836b38d43c1e666b0ea1623d61edba7d9d` is preserved unchanged.
Its manifest SHA-256 is
`9f91143a5283e666038b1d256f7a209c4ba2e99dece5a30c86d9630b5c3f4215`.

## Proof changes

1. **ATTEMPT_3.md, section 1, after equation (1).** Replaced the argument based
   only on the interior of K with the Sobolev level-set argument. The potential
   equals one quasi-everywhere, hence almost everywhere, on K. Its gradient
   therefore vanishes almost everywhere on K. This justifies the enlargement
   integral for an arbitrary compact K, even with positive measure and empty
   interior. The inequality, coefficients, and subsequent triangle proofs are
   unchanged.
2. **ATTEMPT_5.md, after equation (1).** Expanded the envelope justification:
   uniform equivalence of transformed norms gives energy convergence; weak
   closedness and uniqueness identify the weak limit; the Radon--Riesz property
   of uniformly convex L^p upgrades weak convergence plus norm convergence to
   strong gradient convergence. Uniform integrability then justifies the
   parameter derivative limit. No unproved global inequality was promoted.

## Other files

- `FRESH_ADVERSARIAL_AUDIT.md`: the complete original audit, copied byte-for-byte.
  It reviewed the earlier snapshot, so its two requested clarifications refer
  to the pre-correction text. Its conclusion is a pass for partial results and
  a hold on any claim that the original conjecture is solved.
- `README.md`: describes the included audit, the two corrections, and pending
  narrow review.
- `RESEARCH_LOG.md`: records this correction-only checkpoint and unchanged
  five-turn count and unresolved status.
- `ATTEMPT_1.md`, `ATTEMPT_2.md`, `ATTEMPT_4.md`, `SOURCE_GATE.md`,
  `verify_constants.py`, and `checks.json`: byte-identical to the original
  snapshot.

## Portable verification

Run `python3 verify_constants.py` with a standard Python 3 installation. No
third-party dependencies, network access, or PDF files are required. Its output
must match `checks.json` exactly. The script certifies the stated rational
constant brackets and checks 6,145 rational Heron cases; the continuum argument
is in the proofs, and the gamma-function table remains illustrative only.

The proof changes affect functional-analytic justifications, not numerical
constants. The full audit and these changed passages are the scope of the
pending narrow review. No final remote write is authorized by this document.
