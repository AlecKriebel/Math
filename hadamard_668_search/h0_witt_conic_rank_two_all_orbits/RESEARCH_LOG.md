# Research log

## 2026-07-25 PDT — scope correction

- An exact `18 x 24` linear-rank audit showed that the quadratic
  antipodal feature law is not invariant under the classification
  action.  Six classification classes acquire different physical
  feature dimensions in different gauges.
- Corrected the historical phrase “all-orbit” to mean all 18 frozen
  canonical representative gauges.  The five exhaustive v1 records cover
  five canonical gauges, not their full action orbits.  Across the full
  classification there are 360 distinct action images, of which 342 are
  outside the v1 and completed v2 canonical-gauge censuses.
- Preserved `verify_all_orbit_rank_two.py` and
  `all_orbit_rank_two_certificate.json` byte-for-byte, including source
  hash `2ce1dfa5...` and certificate hash `88eee219...`.
- Added `SCOPE_CORRECTION.json` to bind the exact legacy bytes, corrected
  interpretation, action evidence, and superseding complete
  canonical-gauge certificate.

## 2026-07-24 20:13--20:44 PDT

- Extended the arbitrary-quadratic antipodal conic family from certified
  `orbit-07` to all 18 exact dense-shell `h=0` profile representatives.
- Re-derived the 40-parameter feature map, first-layer solution, physical
  evaluation kernel, and quotient image for every profile.  All
  first-layer coefficient solution spaces have dimension 22.  Physical
  dimensions are distributed as one at 14, four at 16, six at 17, and
  seven at 18.
- Froze the exact per-profile denominators: `3^14=4,782,969`,
  `3^16=43,046,721`, `3^17=129,140,163`, or
  `3^18=387,420,489`, according to orbit.
- Applied the predeclared complete-pilot gate exactly.  Exhausted
  `orbit-05`, `orbit-07`, `orbit-09`, `orbit-14`, and `orbit-17`; did not
  enumerate any dimension-17 or dimension-18 image.
- Restricted all 18 second-digit quadrics symbolically before each
  enumeration and processed the resulting spaces in 32,768-point
  batches.  The five complete censuses cover 176,969,853 distinct physical
  placements.
- All five profiles have maximum score 17/18 and zero exact digit-two
  survivors.  Their counts at 17/18 are respectively 4, 5, 12, 15, and
  4, totaling 40.
- Because the exact digit-two survivor set is empty, there are zero
  physical two-consecutive-digit lifts and zero margin-compatible
  second-digit lifts.  The verifier nevertheless reconstructs the exact
  1,756-word catalog and contains full next-digit/margin replay logic for
  every survivor.
- The all-profile physical quotient denominator is 3,663,754,254.
  Exhaustive state coverage is 176,969,853 states, exactly `37/766`.
  Coefficient-law-weighted profile coverage is separately `5/18`.
- For the deferred profiles, froze exact batch counts and dense-quadratic
  work proxies.  Dimension 17 costs `867/256` and dimension 18 costs
  `729/64` times one dimension-16 sweep by this proxy.  The thirteen
  deferred profiles total about 100.055 dimension-16 work units, an
  empirical estimate near 3.3 additional CPU hours on the current
  machine.  No deferred enumeration was launched.
- The detached verifier reproduced the certificate in 578.53 wall
  seconds, 485.47 user seconds, and 56,492,032 bytes maximum RSS.
  Semantic hash:
  `a12dbd72d6e0546f6f6eadf911116b2d83ac349ac0965bba2082263865e5b346`.
- No top-level documentation was changed.  No external contact,
  stochastic search, commit, or push occurred.
