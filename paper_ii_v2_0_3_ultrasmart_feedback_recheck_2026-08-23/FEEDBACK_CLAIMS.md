# External-AI feedback claims to audit (2026-08-23)

This file is a faithful structured transcription of the actionable claims in the user's message. It is evidence to test, not an accepted result.

## Claimed reproductions

- Exact algebra: sextic signs and Sturm counts; `R_hyb`, `sigma_*`, `lambda_*`; `L<U iff F_r(sigma)<0`; minimizer/minimum; derivative and pair-term factorizations; gate ratios; tangency; rational margins and `R_Q`.
- Independent labelled and lumped finite chains agree to `1e-15` for the 9-vertex audit graph and others. Connected fixation for `epsilon=10^-2,...,10^-6` allegedly converges linearly to the separated trace for `C<=10`, three `sigma` values, `r in {1.2,1.5,1.7}`, both rules.
- Along the actual sequence for `t=2,...,14`, dB allegedly matches its response quickly. Bd allegedly has an `O(1/q)` scaled deficit approximately `-(1/(rp)+1)/q` plus `-lambda(m/C)/(r^2p^2)`, compatible with the proof's `o(q/C)` remainder after unscaling.
- References/build/tag allegedly check; the reviewer could not verify three Zenodo DOIs.

## Issues/suggestions

1. **Finite-size sentence.** Suggested concrete separated-trace estimates: Bd-positive at `r=1.4` from roughly `t=12–14` (`n≈2e4–4e4`); at `r=1.5` the bracket is `0.0071` against an alleged deficit `≈3/q`, giving `t_0≈400` (`n≈3e10`); at `r=1.502`, `t_0≈1400`. Suggested as a sentence pre-empting finite-size questions.
2. **Floor non-monotonicity.** Since `m_t=floor(lambda_* t)` under-supplies leaves and Bd needs `lambda>L`, alleged separated scaled Bd gains at `r=1.4` are about `-0.00003, +0.076, -0.048, +0.020` for `t=11,12,13,14`. Suggested round-to-nearest or at least a remark. The theorem's eventual statement is acknowledged unaffected.
3. **Mechanism sentence.** Since `F_r(0)=r(2r-3)`, `sigma→0` recovers the earlier `3/2` endpoint; the positive-sigma pair gate allegedly buys the `≈0.0029` improvement.
4. **Proof-level prose.** (a) Lemma 7/earlier numbering allegedly states `O(K^2/C)` though a hazard ratio `O(1/C)` per ordinary change might yield `O(K/C)`; say which. (b) Equation `deficit-odds` should say its `{1-o(1)}` is uniform in `h,ell`. (c) In the gate proposition, say the union bound on any reversal dominates `1-P_U^H` because reversal is not extinction. (d) Reciprocal quantities appear numerically exponential, but the proved `o(C^-1)` is accepted.
5. **Weak-cut scale.** Small graphs allegedly show `|rho(epsilon)-rho_0|≈c epsilon`, suggesting `epsilon_t≲t^-4/c_t`, with `c_t` polynomial in `C`, so `e_t` is allegedly large but only polynomial. Reviewer says this is consistent with discussion.

## Cosmetic suggestions

- Figure 1's five-vertex “unit clique” allegedly omits chords `c_1c_4` and `c_2c_3`; the `C_t/sigma_*` label allegedly collides with dashed edges.
- Since `5069/6439=37/47`, optionally rewrite `R_Q` with reduced rational part.
- Abstract phrase “supremum of the fitness intervals `(1,R)`” could become “supremum of `R` such that ...”.
- MSC `60J10` allegedly denotes discrete-time chains; consider adding `60J27` for continuous-time Markov chains.
- Confirm CPython 3.14.6 is the actual pin.
