# Supplemental structural review of the final two-ended certificate

Shared PASS4, 14 October 2026. Reviewed `pass4_window_gaps/TWO_ENDED_WINDOW_GAPS.md`, 9099 bytes, SHA-256 `45ff7bb650efb0d579cd9a8cb9c7093b78c4cf2224aef2c18e369a2af0245286`.

## Verdict

**Accepted.** The outgoing-edge rerooting map, its inverse count, deterministic profile selection, two-ended minimax formula, and final geometric-profile diagnostic are valid. This supplements the six-note acceptance receipt without changing it.

## Outgoing cut and exact recovery

For a nonterminal marked state A_i, cutting A_i -> A_(i+1) is the previously accepted rotation at index i+1. The original terminal state alone is inflated, so the marked state A_i becomes last with its size unchanged. The exact homogeneous kernel supplies every retained edge, the lifted incoming edge when present, and the deterministic bridge. No symmetry reversing a canonical chain is assumed.

Given an output and a proposed bridge edge, the state before the bridge is the inflated old terminal state. Deflation, inverse lifting and rotation recover all old states and the marked index. The only discarded datum is the old cut shuffle. In the boundary case i=r-1, the inflated state is first and its incoming edge was cut, so no inverse lift is needed. The missing edge uses the original, deflated sizes p,q and has at most binom(p+q,p) choices. Thus the n+1 possible bridge indices yield exactly the asserted finite fiber upper bound.

For each complete cell-size profile, choosing one maximizing cell and direction is deterministic. A zero coordinate cannot win because the maximum is positive. Already-first and already-last cases use their corresponding endpoint count directly. The profile union therefore needs no further location or direction factor beyond the stated bound.

## Two-ended minimax and scope

Applying the one-ended root recurrence from the left and right bounds each coordinate by d times the smaller of the two corresponding y values. The symmetric vector v_j=min(y_j,y_(K+1-j)) attains the bound: the neighbor toward a nearest endpoint is y_(s-1), and the other neighbor is no smaller. Monotonicity of entropy makes the maximum directional penalty exactly one before normalization. This verifies the exact displayed reciprocal-sum formula, including K=1 and the even central plateau.

The already proved exponential estimates for y_j give a summable certificate of order R^(-K/2) with R>2. That does not establish summability of the true gaps or fulfill the separate divergence hypothesis. Growing-K use still requires retaining the profile factor and the counting-series defect.

## Final geometric diagnostic

For a centered ratio-half window, its boundary-to-mass ratio is H(1/2)*s/(3-s), where s=2^(-l)+2^(-r). Balancing l,r minimizes s at fixed width, and the ratio increases with s. The finite symmetric ratio-two test profile has only endpoint-positive directional penalties. Its total weights are exactly 2(2^h-1) in even width and 3*2^h-2 in odd width. Comparing the resulting upper bound on the certificate with the balanced boundary ratios leaves the strict factor 2H(1/2)>eta, including width one.

Finite canonical mountains of sufficient depth realize these fixed centered-window ratios exactly, as verified in the main PASS4 review. The diagnostic is deterministic, concerns this particular lower certificate, and makes no assertion about the unknown true gaps or uniform probability of the mountain family.
