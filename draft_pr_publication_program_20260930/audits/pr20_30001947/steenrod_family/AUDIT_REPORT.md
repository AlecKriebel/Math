# PR20 / 30001947: Steenrod/Wu family audit

Candidate head: 7914dfa8c2ddf0efb784a29accc8a05b5a24a690. All ten frozen files were independently hashed and matched snapshot_manifest.json. This audit made no Git or PR changes and no external communication. Foreign source full text and page renders remain under this family's ignored tmp directory.

**Verdict: qualified acceptance at the published-theorem level.** The negative answer for every j>=0 is supported by Goresky-Pardon's exact number-valued odd-square corollary, together with explicit adapters. The displayed universal cochain lift in its printed proof has an unresolved premise; this family does not certify that proof at chain level. The published conclusion was not falsified. The distinction matters for describing the audit, rather than automatically overturning the already-solved literature disposition.

## Independent artifacts and chronology

FIRST_PASS_CRITERION.md was sealed before any historical review or root/sibling conclusion. FIRST_PASS_RECONSTRUCTION.md was sealed at 2026-10-01 18:18:48 UTC with SHA-256 4eae22d1d96fcfd5bec47c8d69baa4dc960fc2a38d17afbd892b0aae3f781a2c. It remains unchanged after reconciliation. Its derivation contains the exact perversities, all-vector pairing adapter, local orientation argument, normalization preservation, j=0 case, and elementary symplectic decomposition.

PROOF_QUALIFICATION.md gives the corrected exact maps and equation on printed pp.339-340, identifies the integral lift premise, and checks a six-dimensional target-class countercontrol X=(Sigma RP^3) x S^2. CORRECTION_SUPPLEMENT.md records that the integral D_a target is t, correcting the first-pass transcription without changing either seal. This space has a hyperbolic middle F2 form; it falsifies an automatic integral middle-cochain lifting assumption, not the target conclusion.

## Findings by falsification test

| Test | Finding and exact remaining gap |
| --- | --- |
| Integral orientation -> orientable links | Pass. Cancel the oriented R^s and radial interval in the regular local product. Each link fiber is orientable. |
| Nonorientable singular stratum / link monodromy | Pass. Simultaneous sign reversal of stratum and link fiber can preserve the ambient orientation; no coherent global link-bundle orientation is needed. |
| Definition of F2-Witt | Pass. The primary definition uses the same lower-middle vanishing for links of odd-codimension strata. |
| Ordinary cohomology substitution | Excluded. The diagonal is the square of a middle intersection cohomology class; arbitrary middle vectors need not come from ordinary cohomology. |
| Degenerate versus nonsingular pairing | Pass. Complementary-perversity mod-two duality and the Witt comparison give a nonsingular form on all middle IH, not only an image pairing from a manifold-with-boundary. |
| Normal connected convention | Pass with explicit adapter. Normalization preserves traditional IH chain complexes, link Witt vanishing and regular orientation; middle intersections avoid singular strata and preserve counts. Components give an orthogonal sum. |
| All j>=0 and j=0 | Pass at theorem level. The odd number-valued corollary includes degree one; normalization reduces dimension two to oriented surfaces. |
| Stronger locally-square-free hypothesis | Unneeded for the published number-valued corollary. General middle Sq^1 assertions are excluded. |
| Nonsingular alternating -> Witt zero | Independently checked elementary induction. No quadratic-refinement or Arf claim is involved. |
| Printed proof's universal middle operation types and integral lift | Qualified. The literal mod-two J_a/lemma m-to-m types are broader than earlier definitions. Integral D_a correctly has target t; the integral IC_m input reduction/lift is not automatic. Exact target-degree countercontrol and gap are preserved separately. |

## New checkable algebra supplement

check_forms.py exhaustively checked every alternating matrix over F2 in dimensions 0,2,4,6. It verified explicit symplectic bases and half-dimensional isotropic subspaces for all nonsingular cases: respectively 1,1,28,13888 matrices. Countercontrols checked the nonsingular nonalternating one-dimensional identity and an alternating singular three-dimensional form. Arithmetic is exact. These probes validate the algebra adapter and have no role as a replacement for the universal geometric source theorem.

## Reconciliation and acceptance level

After sealing, the prior review was read. Its orientation and theorem-scope conclusions agree with the independently reconstructed adapter. It did not discuss the cochain type/lift concern. Friedman's May 11, 2015 manuscript §5.2.1, full footnote 14 on p.28, and adjacent locally orientable discussion were independently retrieved and read. They explicitly recognize the previously unresolved oriented 4k+2 bordism computation as already present in Goresky-Pardon. They corroborate the literature classification, but do not resolve the detailed p.340 lift mechanics.

The candidate's statement that it read the proof is consistent with the evidence and is not a claim of a new proof. Any broader phrase such as “independently verified the complete chain-level proof” should be avoided. A precise description is: source theorem and exact-target adapters checked; printed proof read, with a middle-perversity integral-lift qualification recorded. If the publication gate requires a universal chain-level reconstruction as opposed to literature status verification, that subroute is blocked until a materially new source or mechanism supplies it. The strongest verified result in this family is the exact-target implication from the published corollary plus independent elementary/geometric adapters.

Audit completion estimate: 100% of this assigned family's source audit. This is not a claim of a new discovery or completion of the unresolved reconstruction of the printed cochain proof.
