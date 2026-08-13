# Research log: active-invariant orbit gap certificate

## 2026-08-12 16:21 PDT — atomic finite certificate

The inherited mixed-support input consists of 4,761 positive-shielded seeds
and 408 signed-shielded seeds.  Exactly 110 seeds carry the legacy
`common_active_invariant` label.  Closing those seeds under the six species
permutations and linkage reversal gives 714 ordered pairs.  Its intersection
with the orbit of the other 5,059 seeds has 282 pairs, so the exclusive gap
has exactly 432 pairs.

The finite replay scans the repository's 259 exact tier/cap descriptors.  It
retains only descriptors which are affine-feasible and fail the corrected
S-tier-superlevel cut.  There are 192 such rows on 72 pairs; 360 pairs have no
such row.  Every retained row is one-active, with 64 rows for each active
coordinate, and the literal support categories split as 180 B/F0 plus 12
B/B.  This is a support/tier/affine set identity only.  It makes no stochastic
or recurrence claim and enumerates no orientations, rates, populations, or
reaction histories.

## 2026-08-12 16:35 PDT — invariant-alignment derivative

The finite certificate was extended, still without any stochastic claim, to
pin the exact invariant geometry needed by the replacement analytic proof.
Every one of the 432 pairs has stoichiometric rank two.  Its primitive
invariant has exactly one zero coefficient and two positive coefficients;
each coordinate is the zero coordinate for 144 pairs.  On all 192 feasible
cut failures, the unique active coordinate is exactly the invariant-zero
coordinate (64 rows per coordinate).

The 24 failed pairs which are not deficiency zero are exactly the disjoint
union of two 12-pair species-permutation/linkage-reversal orbits represented
by

- `({A,AB},{2A,2C,AC})`, with invariant `A+C`; and
- `({A,AB},{C,2A,BC})`, with invariant `A+2C`.

Frozen files:

- `src/active_invariant_orbit_gap_432_certificate.py`
  SHA-256 `31fa24a20e18546e9c623d3aaf6d3b845c1708d5782f86333c02417fa366cd53`
- `tests/test_active_invariant_orbit_gap_432_certificate.py`
  SHA-256 `09c434fc162ff33f51e331e298ec2e35407a8e0501f1a3b8d771bf33c2fe708b`

Frozen content fingerprints:

- exclusive 432-pair manifest:
  `5516d6071b2b9d07b0e4e02613b9caee217ba3ebb0082e21f2bc664e6247ea36`
- category-free 192-row manifest:
  `cad3bdf8e900cbb6f978e11d30e28bba7a7a57de055d9b9787f7dd53fbc91615`
- category-annotated 192-row manifest:
  `57dcf4af1250ee72a0658bdf5ec930e01ab657b77d739ba211dc12ef6e4ddae8`
- 432-pair invariant manifest:
  `9dec8108276e9d439c18aacda1ec35d9bac08e097f8833e3446c50b40d8148ca`
- invariant-aligned 192-row manifest:
  `a9368dd934b7ac6135c3df4866e2322700d3a607dd58f8327aeb709065880ab2`
- non-deficiency-zero failed 24-pair manifest:
  `051a641f3987ec93b129ad044d96292a97e536e9ef3d2724234dc4af9bfdef69`

Verification: all nine dedicated tests pass.  The twenty-two-test combined
replay of the corrected S-tier-superlevel, exact affine-feasibility, and new
gap-certificate suites also passes.
