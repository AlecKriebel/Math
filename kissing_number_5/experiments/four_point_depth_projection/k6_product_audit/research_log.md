# Research log

## 2026-07-23 21:55 PDT

- Parsed the 51-atom exact direct K6 certificate and its independent
  verifier.
- Inspected the 137,296-column discovery catalog.  Confirmed that it is an
  incomplete discovery catalog and that its floating LP report is labeled
  `NUMERICAL EVIDENCE ONLY`.
- Derived the induced symmetric K5 marginal: sample a K6 atom with its exact
  weight, symmetrize over \(S_6\), then give each of its six deleted faces
  mass \(1/6\).  No automorphism or orbit-size multiplier is required.
- Exact canonicalization merged 306 deleted faces into 266 positive
  unlabeled K5 orbits.
- Verified induced edge marginal \(\alpha/4\) and triangle marginal
  \(\nu/156\).
- Derived the independent direct-K6 product normalization
  \[
  494c+39i\le39Mh+39rg-4rM
  \]
  from 4-of-39 sampling.
- Checked atom by atom that summing the 3-of-39 K5 form over all six deleted
  faces equals the direct K6 form.
- Audited all 560 exact continuum states.  Found 41 violations, all for
  \((q,b,M)=(-1/4,1/2,3)\), and 62 zero rows, all from the trivial \(M=0\)
  family.
- Identified the strongest violation as the rational direction
  \(-\!(y+z)\), with exact right-minus-left slack
  \[
  -34774569534004858111024638332474125643044200329/
  2136111269073896339143576173079200000000000000.
  \]
- Added an exact verifier and two regression tests, including source-tamper
  rejection.

## Status

**COMPUTATIONALLY CERTIFIED:** the stored direct K6 extension fails the
depth/common-capacity product constraints.

**Unresolved:** whether a different symmetric rank-five K6 extension of the
same pair/triple marginal can satisfy all product rows.

## 2026-07-23 22:03 PDT

- Reoptimized over the authenticated 137,296-column rank-five K6 discovery
  pool with all 560 product rows.
- Exactly reconstructed the positive 74-atom certificate
  `productpool_extension.json`.
- Two standard-library verifiers independently checked positive weights,
  all exact triangle and edge marginals, every local Gram atom as PSD of
  rank exactly five, pool provenance, and every product row.
- The replacement has 113 equality rows and minimum strictly positive
  twice-symmetrized slack \(4741606889923/12500000000000\).
- The negative-sum row that refuted the original distribution is saturated
  exactly.

**COMPUTATIONALLY CERTIFIED:** a symmetric local rank-exact-five K6
distribution with the centered pair/triple marginals satisfies every
current depth/common-capacity product row.  This is not a global code or a
six-point Lasserre certificate.

## 2026-07-23 22:05 PDT

- Independently rechecked the 74-atom replacement through the deleted-K5
  implementation rather than its direct-K6 verifier.
- All \(74\cdot560=41{,}440\) atomwise identities between the direct K6
  form and the sum over six deleted K5 faces held exactly.
- The induced K5 marginal has zero negative rows and 113 equality rows.
- Its smallest positive induced-K5 slack is
  \(4741606889923/75000000000000\), exactly one sixth of the direct-K6
  slack recorded by the replacement verifier.

## 2026-07-23 22:10 PDT

- Expanded the 64-orbit exact K5 product witness to all 6,270 labeled
  supported K5s.
- Grouped them by their common labeled K4: 3,888 keys and 14,874 ordered
  compatible face pairs.
- Exhausted all 104,118 joins after trying the seven colors of the one
  missing K6 edge. Exactly zero colored K6s have all six K5 faces in the
  64-orbit support. This is a complete support obstruction and does not
  assume Gram positivity or rank.
- Directly scanned the authenticated 137,296-row available K6 pool. Its
  supported-face-count histogram is
  \(0:136359,1:897,2:38,3:1,4:1\); no pool atom has five or six supported
  faces.
- Added a standard-library verifier and regression test. Therefore the
  particular 64-atom K5 product distribution has no K6 lift, although the
  separate 74-atom K6 replacement induces a different product-valid K5
  marginal.
