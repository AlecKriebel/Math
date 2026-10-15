# Independent slow-tail corollary adversarial audit

Scope: this directory only. No other task/review/proof files are read. No Git mutation, outside contact, or publication. The stated classical theorem `U(t) r(t) -> 1` may be used conditionally, but all further steps will be independently checked.

## 2026-10-04 14:52:03 UTC — Initial checkpoint

Estimated completion: 5%.

Target claim: for a zero-delay renewal process with i.i.d. almost surely finite strictly positive interarrivals, survival `r(t)` slowly varying with `r(t) -> 0`, and `U(t)r(t) -> 1`, the interarrival length `D_t` covering time `t` has no proper finite nondegenerate weak limit under any deterministic finite positive scale `phi(t)`.

Adversarial focus: the exact tail identity and renewal conventions; finiteness of `U(t)`; arbitrary nonmonotone scales; implication from tightness to `phi(t)/t -> infinity`; continuity-point and atom-at-zero subtleties; validity of the proposed explicit tail.

Definition ambiguity identified: the stated identity can hold for the full interarrival length covering `t`, but is not the same identity for forward recurrence time or next renewal epoch. Asked the parent to confirm the intended definition. The audit proceeds with the full interval-length definition made explicit.

## 2026-10-04 14:54:12 UTC — Proof checkpoint

Estimated completion: 70%.

No mathematical counterexample found under the explicit interval-length convention. Independent deductions:

- The exact identity follows by a disjoint sum and increment independence for every `x >= t`, including `x = t`, using survival `P(X > x)` and intervals `[S_n, S_(n+1))`.
- `U(t)` is finite because a Laplace-Markov bound gives `P(S_n <= t) <= exp(lambda t) (E exp(-lambda X))^n` with the expectation strictly less than 1.
- `D_t/t -> infinity` in probability follows from `U(t)r(t) -> 1` and slow variation, including thresholds less than `t` by monotonicity.
- If `phi(t)/t` fails to tend to infinity, a subsequence on which it is bounded makes `D_t/phi(t)` diverge to infinity, which contradicts asymptotic tightness. No monotonicity or regularity of `phi` is needed.
- Once tightness forces `phi(t)/t -> infinity`, survival differences at every pair of strictly positive fixed thresholds tend to zero. Tightness alone then forces `D_t/phi(t) -> 0` in probability, a stronger statement than the proposed weak-limit assertion.

Boundary caveats retained: `D_t` must be the full covering interval length for the exact identity; zero is not an admissible multiplicative threshold for the slow-variation comparison; an extended limit with an atom at infinity can exist and is not a proper finite limit.

The proposed tail is an absolutely continuous law on `(1, infinity)`, with density `1/[x(1+log x)^2]`, and is positive, finite almost surely, nonlattice, slowly varying, and of infinite mean. A direct sampling construction is `X = exp(1/V - 1)` for uniform `V` in `(0,1)`.

## 2026-10-04 14:57:41 UTC — Final verification checkpoint

Estimated completion: 100% of this conditional adversarial audit.

The parent confirmed that the intended `D_t` is the full covering interval length, with `inf{n:S_n>t}` indexing; this matches the explicit convention in the report. No other mathematical conclusions were read.

Completed `report.md`, then reread the entire report against the original task. Checked both the direct tightness proof and the separate continuity-point proof for zero-atom limits. The sharper criterion is `D_t/phi(t)` tight if and only if `r(phi(t))/r(t) -> 0`; it is proved without assuming monotonicity of the scale. Verified the explicit law's density, normalization, support, slow variation, and infinite mean analytically. No numerical computation is needed to support these deductions.

The final conclusion is conditional correctness, not a priority determination. The exact remaining mathematical premise is `U(t)r(t) -> 1`; it was explicitly permitted as an input and has not been independently sourced or proved. Bibliographic priority remains outside this audit. The compactified mixed zero/infinity limit is a boundary case outside proper finite limits and is explicitly documented.

Final evidence: `report.md` and this log will be recorded in `SHA256SUMS`, checksums verified, and all three files marked read-only. No Git mutation, publication, outside contact, or reading of other task files occurred.
