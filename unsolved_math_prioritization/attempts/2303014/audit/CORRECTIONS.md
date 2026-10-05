# Precision notes for the reconstructed circle minimum proofs

Problem 2303014. The audited freeze is unchanged. These are two low-severity
clarifications; neither changes a stated extremal value or the scope of a claim.
There is no required substantive theorem correction.

## N1 Locate the ceiling on the closed disk

Location: `PROOFS.md`, Lemma 5.1, lines 161-163, and Corollary 5.3, lines 213-214.

The word 'there' in the lemma can be read as requiring u<=C on a neighborhood
of the closed R-disk. The corollary directly proves that ceiling only on the
closed disk. The proof of the lemma uses the ceiling only on that closed disk.

Suggested replacement opening:

"Suppose u is continuous and subharmonic on a neighborhood of the closed disk
of radius R, u<=C on that closed disk with C>0, and every centered circle of
radius 0<r<=R contains a point at which u<=0."

If the frozen stronger reading is retained, the corollary still follows by
using C_R+epsilon on a sufficiently small neighborhood, then letting epsilon
decrease to zero. Continuity on a compact neighborhood justifies that step.
The C_R=0 case remains the direct inequality u<=0.

Severity: minor scope wording. Mathematical verdict: no change.

## N2 Make simultaneous boundary contact explicit

Location: `PROOFS.md`, projection input lines 150-157 and Lemma 5.1 lines 169-178.

The source theorem is stated in harmonic-measure form. A boundary point in K
is counted as contact at the stopping time, including a simultaneous disk exit.
The packet's proof is correct with this convention, but the informal phrase
'hitting K before disk exit' could suggest a strictly earlier hit.

Suggested clarification:

"For compact K in the closed R-disk, use its harmonic measure in D_R minus K,
counting an exit point in K as contact. For a starting point outside K, let T_K
be the first hit of K and tau_R the disk exit. The probability of escaping
without contact is Pr(tau_R<T_K). In the optional-stopping bound, points of K
on the outer circle still have value at most zero."

The projected boundary endpoint R is a single point of harmonic measure zero,
so it contributes no extra escape term. Starting points in K are handled by
the immediate bound u(z)<=0, before invoking the projection comparison.

Severity: minor stopping-time convention. Mathematical verdict: no change.
