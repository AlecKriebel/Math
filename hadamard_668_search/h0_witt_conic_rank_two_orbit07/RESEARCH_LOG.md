# Research log

## 2026-07-25 PDT — scope correction

- Relabeled the result explicitly as a census on the frozen
  `orbit-07` canonical representative gauge.
- The classification orbit has 12 distinct action images.  This
  certificate covers the canonical image only; the other 11 were not
  enumerated.  Although all 12 have physical feature dimension 14,
  equality of dimensions alone does not prove covariance of the feature
  spaces.
- Preserved the verifier and certificate byte-for-byte.  The exact
  result on the chosen gauge remains valid; only any implicit
  whole-action-orbit interpretation is withdrawn.

## 2026-07-24 20:03--20:12 PDT

- Started from the proved local identity
  `(q-t)^2=p(s)-1`, with the lossless active-fiber conversion `t=-p*u`.
- Replaced the shared-shape rank-one correction by independent arbitrary
  quadratic corrections `Q_A,Q_B`, while retaining arbitrary quadratic
  base laws `P_A,P_B`.  This is exactly the full rank-at-most-two
  `2 x 10` opposite-correction coefficient family within the quadratic
  antipodal feature space.
- Audited all 18 final profiles before selecting the pilot.  Chose
  `orbit-07` (`0x86b13a0388d98a5e`) because it is tied for the maximum 96
  compatible margin rows, has the second-largest raw margin mass, and its
  rank-two physical image collapses to dimension 14, the smallest of the
  18.
- Derived the exact quotient before enumeration.  The 40-parameter
  feature map has rank 32; the first-layer system has rank 18; its
  coefficient solution space has dimension 22; and the evaluation kernel
  has dimension eight.  Therefore all `3^22` valid coefficient laws map
  uniformly, `3^8` at a time, to exactly `3^14=4,782,969` distinct
  physical placements.
- Restricted all 18 second-digit quadrics symbolically to the canonical
  14-dimensional affine quotient.  The complete state space fits easily
  within the resource gate: batches of 32,768 points, no coefficient or
  ambient-space materialization, and a final verification maximum RSS of
  only 61,308,928 bytes.
- Exhausted all 4,782,969 placements.  No exact second-digit survivor
  exists.  The maximum score is 17/18, attained by exactly five points.
  The five missing physical rows are 2, 3, 4, 10, and 16, once each.
  None of the five near misses belongs to the exact 1,756-word row-margin
  catalog.
- Hence the family contains zero two-consecutive-digit survivors and zero
  margin-compatible second-digit lifts.  This conclusion is complete for
  the delimited family but makes no claim about degree-three,
  non-antipodal, or unrestricted 36-dimensional center laws.
- Froze the complete histogram, quotient hashes, stream hashes, direct
  physical replays, and near-miss data in
  `rank_two_orbit07_certificate.json`.  The detached replay passed in
  11.61 wall seconds with semantic hash
  `cc272f74521b7cf58216b1971f8a2659b1eb1068a295b6c7552cb3c15c778dc8`.
  No stochastic search, external contact, commit, or push occurred.
