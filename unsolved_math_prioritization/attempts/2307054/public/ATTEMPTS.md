# Five substantive attempts

Problem: Rippon's universal unit coefficient bound for `F₀=-1`, `Fₙ₊₁=exp(tFₙ)-1`. Date: 2026-10-03. The following are distinct mathematical approaches, not claims of five independent proofs. The universal question remains unresolved.

## 1. Exact recurrence and a finite counterexample search

Differentiating `exp(tFₙ)` gives the triangular integer recurrence (1) in `proof.md`. This avoids rounding and proves that truncation does not contaminate low coefficients. The initial rational calculation checked degree 100 for 80 iterates. The final integer certificate checks all 40,200 pairs `1≤n≤200`, `0≤k≤200`, with a separate rational-power expansion cross-check through degree 24. No counterexample occurs. The greatest off-leading modulus in the final rectangle is `2663/4480`, at `(n,k)=(6,13)`.

Outcome: exact finite evidence and a valid all-iterate degree-200 conclusion using `ord(Fₙ)=n`; no control of the unbounded degree/iterate range.

## 2. Coefficientwise majorization and induction

Taking absolute values before each composition yields the positive-start recurrence `G₀=1`, `Gₙ₊₁=exp(tGₙ)-1`. The exponential's nonnegative coefficients make this a valid majorant. It cannot prove the desired bound: `[t⁶]G₃=25/24>1`, although `[t⁶]F₃=1/24`. More general coefficientwise induction would need extra structure to preserve the cancellations.

Outcome: a rigorously identified obstruction to the direct positive-majorant route; not a counterexample to Rippon's question.

## 3. Uniform analytic bounds on a small disc

For `0<r≤log 2`, put `q=eʳ−1≤1`. Convexity gives `e^(rx)−1≤qx` for `0≤x≤1`. Starting from `|F₀|=1`, induction gives `|Fₙ(t)|≤qⁿ` on `|t|≤r`; Cauchy's formula then gives `|aₙ,ₖ|≤qⁿr^(−k)`. But `q>r` and `r<1`, so this upper bound is strictly greater than 1 throughout `k≥n`. A unit-supremum argument on the whole unit disc also fails already at `F₁(−1)=e−1>1`.

Outcome: an explicit analytic estimate with a precise reason it does not reach the target. These failures do not disprove sharper analytic methods.

## 4. Normalized iterates and stable diagonal coefficients

The normalization `Hₙ=−Fₙ/tⁿ` gives `Hₙ₊₁−Hₙ∈tⁿ⁺¹Q[[t]]`. Thus offset `j` is stable from iterate `n=j` onward. Combining this exact stabilization with the finite computation proves the bound for `0≤k−n≤100` at every iterate. A formal coefficientwise limit exists.

Outcome: an infinite-family partial result. Stabilization alone provides no bound for every offset, and a bound for the limiting coefficients would still require treatment of the transient cases `n<j`.

## 5. Signed level profiles and rigorous tail closure

Expanding the iterated exponential as rooted trees gives formula (12) in `proof.md`, a signed Stirling-number sum over nondecreasing level sizes. A sign-reversing cancellation argument would be a possible route to the universal bound. A termwise bound cannot suffice: the single profile `(3,6,9,12)` contributes `2835/256>1` before cancellations. No uniform cancellation theorem was obtained.

Separately, Cauchy estimates on rational radii close the infinite degree tails of the first four iterates. For `n≤3`, the certificate uses radius `11/10` and cutoff 128. For `n=4`, an exact degree-200 polynomial plus a geometric Cauchy tail bounds the weighted absolute norm of `F₃` on radius `21/20` by less than 5; cutoff 136 then suffices for `F₄`. All remaining low-degree inequalities are checked exactly.

Outcome: the full bound for `n=1,2,3,4`, and a sharper description of what is still missing. No proof or counterexample is established for the remaining region `n≥5`, `k≥201`, `k−n≥101`.
