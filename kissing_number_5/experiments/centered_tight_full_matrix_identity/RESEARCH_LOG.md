# Research log

## 2026-07-23

- Proved that a symmetric entrywise-nonnegative solution of the complete
  weighted strongly-regular identity automatically has row sum 42 and
  yields a positive-semidefinite rank-five Gram matrix.  Thus an exact
  full-equation matrix countermodel inside the interval would itself solve
  the centered/tight construction problem.
- Derived the four type-conditional moment equations forced by each
  off-diagonal matrix entry.
- Found a strictly positive numerical 246-orbit measure satisfying all
  type-conditional equations.
- Added all 48 exact-stratum common-pair capacity rows and both weighted
  capacity rows; strict feasibility remained.
- Added full-radial BV blocks through harmonic degree eight.  Clarabel
  found positive complementary-block margin about `0.00723`.  This is
  numerical evidence only pending exact rationalization and all-degree
  verification.
- Constructed and independently verified an exact sparse 46-orbit
  type-conditional witness satisfying every corrected capacity row.  It
  fails the \(k=0\) BV node block by a strict negative order-two minor, so
  it is not a common-source three-point certificate.
- Found the nonnegative low-rank transform
  \(W=B\circ(3J-B)\).  It is regular of degree \(266/5\) and has eigenvalue
  four with multiplicity at least 21.  The resulting exact spectral lower
  bound on \(\operatorname{tr}W^2\) remains below the sharp elementary
  row-moment upper bound and therefore does not prove a contradiction.
- A degree-eight BV numerical witness rationalizes but fails degree nine.
  Reoptimization through degree nine is numerically feasible; higher-degree
  solver statuses are unstable and have no certified interpretation.
- Reoptimized through degree twelve and converted the result into an exact
  rational reconstruction.  The independent standard-library verifier
  proves positivity of all 246 weights, all 45 conditional equations, all
  50 capacity rows, and every full-radial BV block through degree twelve.
  The degree-zero, one, and two kernels are checked exactly and completed by
  positive-definite principal blocks.
- Located a strict exact negative \(3\)-by-\(3\) principal minor in the
  degree-thirteen block of that same witness (node indices
  \(\{2,7,10\}\)).  This sharply limits the certificate to degree twelve;
  it is not an infeasibility result for the degree-thirteen relaxation.
- Stabilized the degree-thirteen search by removing the three forced
  low-degree kernels and maximizing a common reduced-block margin.
  Numerically, all BV blocks through degree thirteen remain feasible
  without the stratified capacities, and degree thirteen alone remains
  feasible with them.  The negative cutoff uses compatibility between the
  full stack of degrees and the stratified capacity rows.
- Rationalized the degree-thirteen dual into 18 exact rational Gram
  factors, six nonzero capacity multipliers, and 40 rational equality
  multipliers.  The standard-library verifier proves a strictly positive
  orbit slack and a strictly negative dual objective, so the fixed
  eleven-node pair table has no triple measure satisfying the combined
  relaxation through degree thirteen.
- Recorded the essential limitation explicitly: the eleven nodes and pair
  multiplicities are assumptions of this pseudomodel, not consequences of
  centered tightness.  The exact dual is therefore a fixed-atomic
  obstruction, not a universal centered-code contradiction.
