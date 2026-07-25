# Research log

## 2026-07-25 PDT

- Recast the next binary support digit as
  `D^2+D=83(I+J) (mod 4)`, equivalently the conference-core equation
  modulo 16.
- Implemented the full rank-four unitary graph chart over
  `F_(2^36)`, exact CRT reconstruction for either quotient parity type,
  and direct coefficientwise carry evaluation.
- Proved and checked that a Hermitian diagonal entry with even
  augmentation reconstructs with zero displacement-zero coefficient.
  Thus the graph loop condition is automatic throughout this rank-four
  characteristic-two chart.
- At eight deterministic samples per parity type, the 720 coordinate
  finite differences of the targeted carry-plus-margin/trace syndrome have
  rank 720 and the base syndrome raises the rank to 721.  This is a sampled
  local diagnostic, not a global obstruction.
- A 3,000-point sampled affine audit has targeted difference rank 1,493
  for each parity type; zero belongs to both sampled affine hulls.  The
  frozen verifier makes no separate raw-carry rank claim.
- Built an exact fixed-quotient CP-SAT model with 1,494 membership bits,
  418,293 shared products, 1,503 modulo-four equations, exact margins,
  the `6/3` trace law, and a complete `37^8` fiber-shift gauge.
- Independently audited the two exact characteristic-two support
  witnesses.  Type 1 has 722 nonzero independent carry coefficients and
  type 2 has 764, out of 1,503.  Both pass the lower digit and fail the
  displayed next digit.
- A 200,000-move exact phase walk retained every lower-layer condition and
  improved type 1 only to `672/1503` carry defects.  Adjacent exact audits
  found no valid ordinary four-cycle switch and no exact-margin member of
  the smallest semiregular transvection family, so no further unstructured
  carry search is recommended.
- A 90-second hinted type-1 modulo-four run ended `UNKNOWN`; peak resident
  memory was approximately 2.7 GB.  No feasibility or infeasibility claim
  is made from that run.
- No external communication was made.
