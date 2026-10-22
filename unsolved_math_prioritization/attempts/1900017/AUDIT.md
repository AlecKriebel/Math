# Row 1699: target audit and disposition

## Result

Aggarwal–Andritsch, *Generalised Gauss–Kuzmin Distribution for Klein sails in R³*, arXiv:2608.05853v1, Theorem 1.9, explicitly claims the finite sum required for the dimension-three case of Karpenkov's Problem 17. This is a preprint submitted 6 August 2026, with no journal reference visible in the inspected arXiv record. No new solution or result in dimension at least four is claimed.

Locating the prior theorem and giving a short reduction did not by itself constitute a completed proof audit. The original argument has literal errors, including a global chart coverage claim that misses an open set and a cross-section invocation whose closed-orbit hypothesis does not hold.

This audit supplies a repaired target-proof reconstruction. After independently reconstructing the geometric reduction and the summable upper-measure estimate, no specialized unproved intermediate lemma remains in that reconstruction. The exact established external input is G. K. White's 1964 Theorem 2, with its original publisher statement and hypotheses checked. White's full proof was not independently re-proved. Ordinary Haar measure and finite-volume unimodular-lattice facts are also used explicitly.

Accordingly:

- Source status: prior preprint theorem claim, not journal-certified here.
- Original printed proof: not accepted verbatim as a complete independently audited argument.
- Authored target reconstruction: checked relative to the explicit established White theorem and standard Haar facts.
- Whole 50-page manuscript: not fully audited; the unrelated lower bounds, all-lattice pointwise statements, generic ergodic and periodic-sail conclusions are outside acceptance.
- No counterexample to the dimension-three finiteness claim was found.

## What the reconstruction establishes

The detailed geometric audit is [REDUCTION_AUDIT.md](REDUCTION_AUDIT.md); the technical estimate is [MEASURE_AUDIT.md](MEASURE_AUDIT.md).

1. The historical question concerns integer-linear face types and retains position relative to the origin. This is checked against Karpenkov's cited 2007 primary paper, not inferred merely from the 2017 paper's general affine-congruence definition. Passing between GL₃(Z) and SL₃(Z) changes indexing by at most two, and between an arrangement and its chosen chamber by a fixed finite covering; neither changes finiteness.
2. The required face-adapted positive-height chart covers almost every cone with a fixed bounded face in z=k. The globally asserted chart does not cover mixed-height cones. Correcting the chart and the positive-cone stabilizer yields a single face-independent measure normalization factor.
3. A direct finite-candidate first-contact argument supplies local flow boxes for the full cross-section. The closed-orthant definition of the first minimum handles boundary lattice points correctly. This avoids the invalid closed-orbit invocation.
4. The affine-lattice first-contact description follows by an explicit group isomorphism and slice calculation. Right Haar measure uses ordinary translation area, not area divided by the lattice covolume.
5. Face stabilizers have order at most six. The countable image sets for distinct integer-linear types are disjoint. Thus, for a normalization constant B independent of the face,

   sum_[f] rel([f]) <= 6 B mu_C(C).

6. The reconstructed planar estimate, after compatible normalization, is

   I_1(L) <= 3√3,
   I_k(L) <= 1080√3 H_(k−1)/(k(k−1)) for k>=2,

   for almost every unimodular planar lattice L, where I_k is the radial integral of admissible translation area. This almost-everywhere scope is sufficient for total measure; the stronger source statement for every lattice is not certified.
7. Tonelli gives the exact elementary identity

   sum_(k>=2) H_(k−1)/(k(k−1)) = sum_(j>=1) 1/j².

   Indeed, interchange the positive sums and use sum_(k>=j+1) 1/(k(k−1))=1/j. Hence the total affine-lattice measure is bounded by 3√3+1080√3 sum_(j>=1)1/j². Its finiteness proves the required cross-section input. No lower estimate or prior normalization as a probability is used to establish this.

## Main repairs to the source

Exact locations and corrected statements are in the two detailed reports. The important mathematical changes are:

- Replace global Lemma 4.2 by the face-adapted local chart, retaining normalization and the finite ray-order covering factor.
- Replace the closed-orbit invocation in the first part of Theorem 3.3 with a direct local finite-contact proof.
- Correct the level denominator to exclude zero heights.
- Work in the positive component of P when identifying the supporting plane and its stabilizer.
- Prove the reduced-minima basis property and replace Lemma 9.5's Case 4 by a direct integer-coefficient argument.
- Add the first-contact exclusions to the witness parameter sets before using inclusion (11.6).
- Normalize witness translations consistently and correct the right/left Farey denominators.
- Recompute the radial inclusion-exclusion integral with unordered pairs, and restore the missing factor two in the harmonic sum. A stronger elementary support estimate yields the displayed uniform bound despite that correction.

These are authored repairs to proof steps. They are not public allegations of an invalid final theorem and do not claim originality for the underlying result.

## Verification and limits

All frozen audit inputs match their supplied byte counts and SHA-256 pins. The complete closed audit and reference inventories were rechecked during packet preparation. The public source metadata and aggregate verification results record the relevant identities and check scope. The independently written finite-check scripts perform exact algebra, residue checks, support-geometry sanity checks and numerical integral cross-checks. Finite checks support the reconstruction; they do not replace its universal proofs or amount to formal verification.

No source-author code was executed. Source PDFs, source-text extractions and rendered source pages are excluded from this packet. It contains authored mathematical reports and public verification metadata. The mathematical review was AI-assisted, with no independent human referee review or proof-assistant formal verification.
