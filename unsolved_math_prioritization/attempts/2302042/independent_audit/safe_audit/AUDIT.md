# Independent audit: Function Theory 2.42 recovery freeze

Date: 2026-10-05. Target: problem 2302042 / AMR-022-2042, queue rank 675.

## Verdict

**PASS WITH EXPLICIT LIMITATIONS.** The frozen reconstruction establishes the
positive-ratio example at its stated scope. The `already_solved` disposition is
supported **as an attributed literature-status correction**. It is not an
independent verification of Barsegyan's universal theorem, a novelty claim,
formal proof certificate, or journal-readiness finding. No blocking mathematical
gap was found in the positive construction.

This is a fresh audit of the new recovery freeze. No historical audit was
inherited. The author packet and its ZIP were not edited.

## Exact object and replay

- Author ZIP: `asymptotic_ratio_2302042_NEW_FREEZE_20261005.zip`
- ZIP bytes: 13,409; members: 8, with no duplicates or unexpected members
- ZIP SHA-256: `f55af0a7d0d909ec90a41158620f8e5304d74646032ef6e1465613f7518f0902`
- Author manifest SHA-256: `9a16d1058ebccac239eee2faf033b61437eeeffe83ae178409e2903ae6914320`
- Every ZIP member equals its corresponding frozen-folder file; CRC passes
- Author exact replay: 2,480 checks and 8 rejected scope mutants, under both
  ordinary Python and `python3 -O`; output exactly reproduces `CHECKS.json`
- Author strict-inventory replay: passes in both modes
- Independent manifest controls: altered content, unexpected file, missing
  file, and symlink are all rejected in both modes
- Independent additions: 9 scope/identity consistency checks and 2,000 exact
  angular-integral/radial-flux checks pass
- The independent replay driver itself produces identical results with and
  without `-O`

The frozen manifest excludes itself. Its independently pinned hash and the
pinned ZIP hash supply the external identity check. The test counts describe
finite algebraic and consistency tests; they do not formalize the analysis.

Replay with `python3 audit_replay.py /path/to/asymptotic_ratio_2302042_recovery`;
the argument must contain the author ZIP and `safe_output` folder. The optional
numerical diagnostics run as `python3 independent_numeric.py` and require
mpmath. Their output is already preserved in `NUMERIC_RESULTS.json`.

## Target fit

The public problem uses the ordinary, unintegrated number of points in the
closed disk, with the book's general multiplicity convention. Its numerator is
the count on the designated asymptotic path. The reconstruction uses exactly
these quantities, and also proves simplicity for every selected value, so no
reduced-versus-multiplicity ambiguity affects its result.

For each integer n >= 2 the construction provides 2n distinct listed value/path
pairs. Keeping any l of them with 2n >= l answers the finite-selection existence
question. This does not claim exactly l total asymptotic values for arbitrary
odd l, prescribed values or curves, arbitrary ratio vectors, or all orders.
These exclusions are appropriately visible in the freeze.

The mathematical statement was independently checked against the public
Hayman-Lingham problem. The mapping to the dataset ID/rank and the recorded
dataset hashes was checked for frozen-metadata consistency only. Original
dataset statement/report bytes and complete upstream corpora were not fetched
or rematched by this audit.

## Analytic review

1. **Entire function and covariance.** Removing the origin singularity and
   integrating the entire sine quotient yields the stated series. Every
   exponent is 1 modulo 2n, giving the claimed rotations. Radial integration
   gives the global growth upper bound.
2. **Positive asymptotic value.** The substitution u = x^n has exponent
   1/n - 2. Multiplication by sine is integrable at zero, while the tail is
   absolutely integrable for n >= 2. Successive absolute half-wave integrals
   are strictly decreasing. Pairing them proves A > 0. Rotation then gives
   2n distinct finite limits. The optional Gamma evaluation is consistent.
3. **Ray counts and multiplicity.** At x_j = (j*pi)^(1/n), the tail has sign
   (-1)^j. The derivative has a fixed, nonzero sign on each intervening open
   interval, hence exactly one simple A-point occurs there and no endpoint
   is an A-point. This proves r^n/pi + O(1) without integration of the count.
   Critical points are precisely rotations of positive x_j, j >= 1.
   Their positive radial critical values differ from A, excluding all the
   selected values from the critical-value set.
4. **Sector asymptotics.** On a compact angular subsector with Im(z^n) > 0,
   the decaying exponential contributes a bounded term. Integration by parts
   gives the growing primitive's leading factor (i/n) z^(1-2n). Multiplying
   by the coefficient of exp(-i z^n) in sine yields the negative coefficient
   -1/(2n) in the freeze. Uniform endpoint estimates bound the relative
   remainder by O(|z|^(-n)). Rotation/conjugation covers every sector between
   consecutive designated rays. This also supplies the order lower bound.
5. **Scaling and zeros.** For each fixed a, the scaled logarithms are
   subharmonic and locally uniformly upper bounded. Off finitely many rays
   they converge locally uniformly to U(z) = |Im(z^n)|. Standard subharmonic
   compactness cannot have a minus-infinity alternative on a subsequence,
   because it would contradict this convergence on an open sector. Any
   L1_loc subsequential limit equals U almost everywhere; the exceptional
   rays have planar measure zero. Thus the whole family converges in L1_loc.
6. **Riesz mass and the nonintegrated denominator.** The normal-derivative
   jump along each ray is 2n*t^(n-1). With the 1/(2*pi) normalization this
   gives density (n/pi)*t^(n-1) and unit-disk mass 1/pi on each ray. The
   origin contributes no atom. Independently, integrating the radial flux
   uses integral_0^(2*pi) |sin(n*theta)| dtheta = 4, yielding total mass
   2n/pi. Distributional convergence of the positive zero measures extends
   to compactly supported continuous tests. The unit circle has zero limit
   mass, so its closed disk is a continuity set. Consequently the ordinary
   count divided by r^n tends to 2n/pi, with no exceptional-radius sequence
   and no replacement by the integrated Nevanlinna counting function.
7. **Conclusion.** Dividing the two asymptotics gives 1/(2n) for each listed
   pair and sum 1 over all 2n pairs. The universal upper bound is not used in
   this construction or its proof.

The two explicitly stated standard subharmonic/zero-measure results remain
standard analytic inputs rather than formally derived lemmas. Their
hypotheses are met here.

## Independent numerical diagnostics

An independent hypergeometric representation was compared with radial
quadrature at 70 decimal digits. Diagnostics cover 192 critical-value/tail
inequalities, 36 sector-asymptotic estimates, 8 quadrature comparisons, and
9 twice-meshed winding computations (290 recorded checks in total).
The largest tested value of r^n times the sector relative error was about
2.05313, consistent with the stated remainder scale.

For n = 2, 3, 5 and r^n = 20.3, 40.7, 80.9, the approximate winding counts
were respectively (24, 49, 98), (34, 73, 146), and (52, 121, 244). The
largest-radius count/leading-prediction ratios were approximately 0.9514,
0.9449, and 0.9475. Initial coarse meshes sometimes had excessive phase
steps; adaptive refinement resolved those diagnostic failures, and the
full refinement history is retained. Up to 81,920 samples were needed.

These are corroborating finite floating-point calculations, **not certified
zero counts or proofs of asymptotic limits**. The analytic review above,
rather than these diagnostics, supports the theorem.

## Literature and attribution

- The [Gol'dberg-Eremenko article](https://www.math.purdue.edu/~eremenko/dvi/as-curves.pdf),
  Section 3, printed pp. 531-532, contains the credited construction and
  ratio and leaves the density-one question open at that time. Its
  [Math-Net record](https://www.mathnet.ru/eng/sm2401) confirms the 1980 English
  translation, volume 37(4), pp. 509-533, DOI 10.1070/SM1980v037n04ABEH001989.
- [Hayman-Lingham, 2018 draft v2](https://arxiv.org/abs/1809.07200v2), printed
  p.39, Update 2.42, attributes the complete answer and the bounds 1 for
  entire functions and 2 for meromorphic functions to Barsegyan. Applying
  the reported entire-function bound excludes simultaneous density one
  for two or more distinct values. The freeze correctly labels this an
  attributed conclusion, not a verified original proof.
- New independent bibliographic evidence: the
  [Pan-Armenian Digital Library catalog record](https://arar.sci.am/dlibra/publication/122584/edition/111436)
  identifies Barsegyan's article in the Mathematics proceedings/Izvestiya,
  1983, volume 18(2), pp.124-133. It supplies the English alternate title
  *On the arrangement of asymptotic paths and alpha-points of meromorphic
  functions*. This corroborates the freeze's venue-discrepancy warning
  against the draft's Doklady citation. The library marks article access
  as secured/unavailable to this account. No access restriction was bypassed.

The original Barsegyan proof and any hypotheses omitted by the draft remain
uninspected. The audit independently read public PDF text and bibliographic
metadata; it did not independently redownload/hash the source PDF files or
inherit the author's visual-inspection claim. Web screenshot attempts did not
yield inspectable image output. No source PDF, source-text dump, dataset
content, or private coordination record is in this audit package.

## Permitted use of this verdict

Use the packet as a credited positive-example reconstruction plus a clearly
attributed literature correction. Keep the source-proof and dataset-byte
limitations adjacent to any `already_solved` classification. Do not recast
this audit as verification of the full Barsegyan proof or as a novel solution.
The new catalog link may be added as separate public verification metadata
without altering the identity of this audited freeze.

This AI-assisted audit does not replace qualified expert review.
