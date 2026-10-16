# Optional L1 growth and target-response addendum: adversarial verdict

**Verdict: verified optional enhancement, not a mandatory repair.** Under the exact frozen PR 248 example, the baseline objective has local L^1(0,1;H)-squared growth at the unique zero optimizer. Every perturbed global optimizer has L^1 norm O(ε) and L^2 norm O(√ε), where ε is the H-distance of its target from πe. The finalized original failure of L^2-squared growth remains correct and unchanged.

The new hypothesis survives the sign/domain check. Write A=∥u∥_1, x=(e,y_u(1)), and b=A/π+R A^5. The actual uniform nonlinear wave remainder gives x≤b. Exact expansion and nonnegative discarded terms give the gap at least q_A(x)=A−πx+x²/2. Since q_A decreases on (−∞,π], a local radius keeping b≤π/2 justifies q_A(x)≥q_A(b), even if x is negative. Separate substitution into the squared term would not be valid; substitution into the composite function is.

For a sufficiently small explicit δ>0, the exact expansion gives

\[
q_A(b)=\frac{A^2}{2\pi^2}-\pi R A^5+\frac R\pi A^6+\frac{R^2}{2}A^{10}
\ge\frac{A^2}{4\pi^2}\quad(0\le A\le\delta).
\]

`DERIVATION.md` gives a checkable radius that covers R=0, maintains b<π, and absorbs the negative error term. No change to the frozen cap ρ is needed. This growth bound holds for feasible controls in the L^1 neighborhood, with constants independent of ν≥0.

For any target perturbation w∈H, ε=∥w∥_H, perturbed optimality yields the exact inequality

\[
J_{\pi e,\nu}(u_w)-J_{\pi e,\nu}(0)
\le(w,y_{u_w}(1))\le E\epsilon A_w.
\]

The existing global cubic estimate first gives A_w≤√(12ρ²Eε), uniformly over every global optimizer. Thus all optimizers enter the local L^1 neighborhood for one fixed ε-neighborhood. Applying the new growth bound gives A_w≤4π²Eε. The pointwise cap then gives

\[
\|u_w\|_{L^2H}\le2\pi\sqrt{\rho E}\,\epsilon^{1/2}.
\]

These upper constants and their perturbation neighborhood are uniform for all finite ν≥0. Global optimizer existence is inherited from the already independently verified direct method. The estimates require no selected branch and hold for arbitrary H target perturbations near πe.

They are estimates relative to the fixed zero base optimizer. They establish neither pairwise Lipschitz continuity between arbitrary targets, uniqueness of perturbed optimizers, nor L^∞ convergence of the perturbed optimizers. No such enhancement should be advertised.

For the radial perturbation w=εe, the original negative trial comparison and g_ε bound also prove

\[
c\epsilon^{3/4}\le\|u_\epsilon\|_{L^2H}
\le C\epsilon^{1/2}
\]

for every global optimizer and sufficiently small ε, for each fixed ν≥0. A checkable choice is c=1/(8C_g), C_g=2^{1/4}π^{-5/4}. Substituting a hypothetical r≤cε^{3/4} into the existing lower objective bound produces −ε²/8−O(ε^{15/4}), which contradicts the negative comparison ≤−ε²/4. The powers are compatible and imply r/ε≥cε^{-1/4}→∞. Neither rate is asserted sharp.

There is a genuine uniformity distinction: the lower bound's c may be chosen independently of ν, but its ε-neighborhood is established only for fixed ν or bounded ν ranges. The existing pulse comparison has a νO(ε^{10}) velocity cost, and therefore does not supply a uniform negative improvement threshold across all unbounded ν≥0. The local L^1 growth and upper estimates do not use that trial comparison and remain uniform in ν. No counterexample to stronger lower uniformity is claimed; it is simply unproved by the supplied mechanism.

The artifact package includes the full independent derivation, exact algebra controls and receipts, original-artifact preservation pins, a timestamped research log, and a separate final manifest. All original finalized authored files and original manifest bytes remain unchanged. No priority investigation, source-content redistribution, external communication, Git/PR/publication, or spreadsheet action occurred.
