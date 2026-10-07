# Exact theorem ledger

## Target T1 (proved as a consequence; full package review pending)
For every real s>2, the ordered-pair unit-square minimal-energy limit
C_(s,2)=lim_(N→∞) N^(-1-s/2) min_(x_1,...,x_N∈[0,1]^2) Σ_(i≠j)|x_i-x_j|^(-s)
is ζ_Λ(s)=Σ_(v∈Λ\{0})|v|^(-s), with Λ=(√3/2)^(-1/2){(j+k/2,k√3/2): j,k∈Z}, covolume one.

## Target T2 (proved as a consequence; full package review pending)
For each compact smooth embedded two-dimensional surface M⊂R^p, with positive area A=H²(M), and every real s>2, the minimal ordered-pair ambient Euclidean-distance energy is asymptotic to ζ_Λ(s) A^(-s/2) N^(1+s/2). Smooth boundary is allowed: finite bi-Lipschitz chart pieces satisfy Hardin–Saff definition (19), Theorem 2.4 for s>d, including its addendum as used inside a compact regular thickening. The unit sphere coefficient is ζ_Λ(s)/(4π)^(s/2).

## Input U (analytic dependency audits pass; no reproduced full Lean build)
For every locally finite C⊂R² with # (C∩B_R)/(πR²)→1, and nonnegative smooth completely monotone g on (0,∞),
liminf_(R→∞) [#(C∩B_R)]^(-1) Σ_(x≠y∈C∩B_R) g(|x-y|²) ≥ Σ_(v∈Λ\{0})g(|v|²),
with equality for Λ, values in [0,∞]. Closed centered disks, ordered pairs, and liminf are exact.

## Excluded conclusions
No microscopic crystallization, uniqueness of finite minimizers, s≤2 result, second-order surface term, or full follow-on formalization is asserted.

## Success criteria
Validate U or repair it rigorously; prove finite transfer with all tails/limits; verify classical surface theorem scope/corrections; independently audit attribution/priority; pass complete package reviews; only then publish and update tracker. Material upstream gaps block unconditional target claims.

## Validation disposition
Both pivotal upstream manuscripts passed distinct analytic adversarial audits and their finite certificates reproduced. The finite bridge and lattice upper bound were independently derived. The corrected surface theorem hypotheses and original pair/covolume constants were inspected from primary texts. The result is a newly available explicit corollary of OpenAI plus known reductions; no independent base breakthrough or firstness claim is made. Full publication candidate reviews remain required before deposit.
