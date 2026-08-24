# Independent mathematical feedback audit

Audit date: 2026-08-23  
Scope: the new finite-size, proof-scale, mechanism, reciprocal-invasion, and weak-cut claims in `FEEDBACK_CLAIMS.md`  
Source changes: none

## Verdict

No mathematical blocker remains in v2.0.3.  The proof-scale and explanatory edits already made are valid.  The proposed concrete finite thresholds, reciprocal exponential strengthening, and polynomial weak-cut complexity claim should not be added.

## Findings

1. The sharpened early-establishment error $O(K/C)$ is valid.  Before the first hub change, the hub-changing rate is $O(i/C)$ and the ordinary-count changing rate is $\Theta(i)$, so the adverse hazard per embedded count change is $O(C^{-1})$.  The stopped biased walk makes $O(K)$ expected count changes.
2. The quoted $t\approx400$ and $t\approx1400$ values are heuristic comparisons of the limiting Bd bracket with a fitted $3/q$ deficit.  They do not give first or permanent positivity thresholds, do not control the exact diagonal, and omit the sawtooth floor term.
3. An independent finite separated-trace solver derived from the manuscript rate tables reproduces the claimed Bd scaled gains at $r=1.4$:
   $-0.000027,+0.07565,-0.04847,+0.02037$ at $t=11,12,13,14$.  This confirms the nonmonotonicity warning, not a theorem-level finite-size bound.
4. The mechanism identity $F_r(0)=r(2r-3)$ exactly recovers the $3/2$ singular response boundary; optimizing at positive $\sigma_*$ raises the tangency to $1.5028569\ldots$.
5. The deficit-odds remainder is already introduced as uniform in the hub and pendant coordinates.
6. The global-sweep clause has the correct direction: failure implies at least one center reversal, while a reversal may subsequently recover and therefore need not imply failure.
7. Numerically exponential reciprocal decay is not proved.  The manuscript should retain only the uniform $o(C^{-1})$ estimates it establishes and needs.
8. The proposed weak-cut scale is not even the correct uniform heuristic for the manuscript's diagonal.  Since the lower end of $I_t$ is $1+1/t$, the complete-graph baseline is of order $1/t$.  If a fixed-$t$ perturbation has absolute slope $c_t$, the displayed scaled uniform diagonal condition heuristically requires $\varepsilon_t\lesssim t^{-5}/c_t$, not $t^{-4}/c_t$.
9. Small-chain experiments do not prove polynomial growth of $c_t$.  If $c_t$ were polynomial, the dyadic exponent would in fact be logarithmic in the population scale, so saying $e_t$ is "large but only polynomial" would also be imprecise.

## Final disposition

Accept the current v2.0.3 proof and discussion edits.  Reject the proposed finite-threshold and weak-cut-rate additions.  No further mathematical edit is recommended.
