# Research log

## 2026-07-25

- Reconstructed the five exact shell-two profile representatives and all
  compatible row-margin corpora from frozen repository sources.
- Located the first placement-dependent margin digit: digits zero through
  two are automatic, while digit three gives six independent affine rows.
- Exhausted all 405 augmented systems.  Every target is consistent and
  leaves affine dimension 30.
- Proved and replayed the exact directed augmentation identity.  With an
  exact row margin, the origin coefficient is two lambda digits later than
  the twelve nonzero lag classes.
- Exhausted all 364 projective five-hyperplanes of the six structured
  correlation quadrics before and after the physical margin restriction.
  Two unrestricted profiles have a unique five-form retraction; none
  survives on a physical chart.
- Exhausted all 11,011 four-dimensional subspaces after the margin cut.
  The exact maximum retraction dimensions are `4,3,3,3,4`.
- Interpolated and directly replayed the six margin digit-four quadrics on
  every target.  Their individual ranks are 5--11, their joint radical is
  always zero, and no five-form margin retraction exists.
- Ran a six-million-point exact four-form scan on
  `h2-422220-3`/target 65.  It found two correlation digit-two points; the
  best has one bad margin digit-four row and is pinned by placement hash
  `941b2029c2d0df0935f91bb213bb53b3ee23117f21c7cee1f9fc245eaddb8abc`.
- Exhausted the pinned point's 2,187-member linearized margin-correction
  sheet.  No member preserves correlation digit two while also satisfying
  margin digit four; the minimum correlation defect is four.
- A 300-CPU-second digit-two manifold walk replayed five distinct points
  with no exact row margin.  A separate 120-CPU-second margin-quadratic
  biased walk replayed four and did not improve the pinned defect one.
- No correlation digit-three point, consecutive digit-three/digit-four
  lift, exact row-margin digit-two point, `LP(333)`, or `H(668)` was found.
- Peak resident memory stayed below 55 MB.  No external communication
  occurred.
