# Independent audit of the robust block coupling gate

Artifact: `pass3_audit/ROBUST_BLOCK_COUPLING_GATE.md`

SHA-256: `34e2f7b56db469b60f19cb9740bd070ac2c6e59fb69d0018d609e9aede5d9268`

Verdict: accepted as a conditional theorem. No controller satisfying its full hypotheses is constructed by the audited document or by this audit. In particular, acceptance of the concentration implication does not imply that bounded-band short-threat tracking is possible.

## Independence check

Fix an announcement history and its chosen target time t. The index of the last completed block before t is then fixed. The designated D_i is still unrevealed at announcement time. The anchor a_(S_i) is determined before D_i is drawn; adaptedness prevents that anchor from encoding D_i. The next displacement D_(i+1) is drawn independently of all earlier inputs, including both the anchor and D_i. Therefore the pair consisting of the anchor and D_(i+1), not merely its individual components, is independent of D_i under the earlier conditioning. Applying the fixed function F_(i+1) preserves this independence.

This argument requires the stated joint fresh-draw/adaptedness hypotheses. Independence of D_i from each of two quantities separately would not in general suffice, but the chronological construction here supplies their joint independence.

## Tracking and concentration check

Local resetting gives exactly

    a_t=a_(S_i)+D_i+F_(i+1)(prefix,D_(i+1))+e_i+e_prefix.

On the good event the error norm is at most rho_i+rho_(i+1). At a block boundary the prefix error vanishes. Thus the hit-and-good event is contained in the event that an independent uniform D_i plus the displayed remainder enters a square with at most [2(rho_i+rho_(i+1))+1]² cells.

The correction need not be independent and is not treated as an independent convolution. The proof correctly bounds P(hit AND G | earlier actual history), rather than conditioning on G. No conditioning bias from future success is omitted.

## Safety and restart check

The sufficient theorem explicitly requires conditional short-bomb safety, tracking, and post-endpoint invariant closure from every admissible complete history. Its closure includes the Devil announcement after the endpoint move. These are substantive assumptions, not consequences of spread. The first-failure argument gives the sum of epsilon_j bounds, and the separate union bound handles every long-announcement collision on G. These two categories account for all possible lethal announcements under the stated classification.

The controller and the fresh draws must remain defined on the stipulated hypothetical extension after a collision; the audited statement expressly requires this. Actual play still stops at its first collision. State or memory used for the short/long distinction must retain the necessary announcement-history information, as permitted by the complete-history formulation.

The resulting strictly positive survival probability against every adaptive Devil supports finite-horizon determinacy and the already accepted finite-Angel-action extraction. This is a valid conditional route to a deterministic strategy.

## Adversarial boundary

The independently derived endpoint-recovery attack in `ENDPOINT_RECOVERY_OBSTRUCTION.md` prevents certain linearly interpolated reference blocks from satisfying the required bounded-tracking controller guarantee. That attack does not contradict the spread lemma: it defeats the existence hypothesis of the controller, not the conditional bounded-preimage implication.
