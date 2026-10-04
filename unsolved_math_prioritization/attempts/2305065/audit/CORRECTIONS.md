# Corrections and clarifications

## Blocking corrections

None for the exact already-solved existence claim. No frozen author file was changed.

## Nonblocking helper-domain defect

`check_controls.py` defines `approximation_parameters(epsilon, eta)` without enforcing the geometric lemma's n≥2 condition for all positive epsilon. The independent input epsilon=100 and eta=1 returns:

    n = 1
    arc_bound = 1/2
    norm_bound = 88/7

This satisfies its norm inequality but does not satisfy the lemma's allowed n range. Every existing test uses epsilon≤1/2, so none of the recorded 48 controls is invalidated. No analytic argument or existence claim depends on the untested helper input.

Optional hardening for a future separately frozen revision:

    n = max(2, x.numerator // x.denominator + 1)

Add a control with epsilon=100, eta=1, requiring n≥2. The prose choice in FULL_PROOF.md can similarly say "choose an integer n≥2 with 4π/n<epsilon." Arbitrarily large n are available, so this is not a mathematical obstruction.

## Source caveats already handled or irrelevant to the target

- The unrestricted openness step at constants is false. The packet's use of the nonconstant open subspace is the correct repair. No additional correction is required for the target proof.
- Lemma 3.2(d) uses closures of open arcs; the closure bars are visible in the scan and often lost in OCR. The packet's description as closed contact arcs is correct.
- The source's very terse gauge definition omits an explicit right-continuity/vanishing-at-zero assumption customarily included in a Hausdorff gauge. For instance, h(r)=1 for r>0 and h(0)=0 would invalidate a sweeping nonconstant conclusion. The packet uses the conventional term "Hausdorff gauge" and actually applies only h(t)=t, so no such ambiguity affects its argument. Do not extend the claim to discontinuous counting gauges.
- To reconstruct the doorway geometry literally, choose the slit-gap parameter sufficiently small, for example below 1/n as well as below the required measure tolerance divided by n. The source's printed auxiliary bound is not by itself a sufficient small-gap condition for all n. The cited lemma allows arbitrary further shrinking, and the packet already calls for a sufficiently small parameter.
- The harmonic-measure limit and the boundary extension remain imported analytical facts; they were inspected but not formally or fully source-freely reproved. Keep the packet's existing disclosure.

## Freeze discipline

Do not silently amend the audited files. If the optional helper correction is applied, prepare a new manifest and identify the changed hash. The present acceptance refers only to author manifest SHA-256 22542408192501b6ff6f2c1cd3491cc529463fb0549283fa8164334dfb83012e.
