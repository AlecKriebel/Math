# Independent adversarial verification of the slow-tail normalization corollary

Completed: 2026-10-04. Audit status: **verified conditionally on the supplied renewal asymptotic**. No counterexample was found under the stated assumptions and renewal convention. The strongest verified result is that **every asymptotically tight deterministic normalization converges to zero in probability**.

This audit read no other task, review, proof, or agent-conclusion files. It uses no literature lookup. Consequently it does not establish novelty, priority, or bibliographic attribution for either the renewal asymptotic or the corollary. The only externally supplied mathematical premise is `U(t)r(t) -> 1`.

## Exact setup

Let `X_1, X_2, ...` be independent identically distributed random variables with `0 < X_1 < infinity` almost surely. Write

`S_0 = 0`, `S_n = X_1 + ... + X_n`,

`r(x) = P(X_1 > x)`, and `U(t) = sum_(n >= 0) P(S_n <= t)`.

Assume that `r` is eventually positive, is slowly varying at infinity (that is, `r(cx)/r(x) -> 1` for every fixed `c > 0`), tends to zero, and satisfies the supplied premise

`U(t)r(t) -> 1` as `t -> infinity`.                                      (P)

Use the zero-delay, half-open interval convention

`N_t = max{n >= 0 : S_n <= t}`, and `D_t = X_(N_t+1)`.

Thus `D_t` is the full length of the renewal interval `[S_(N_t), S_(N_t+1))` containing `t`. Equivalently, if `J_t = inf{n >= 1 : S_n > t}`, then `D_t = X_(J_t)`. A renewal exactly at `t` starts the new interval.

Let `phi(t)` be any deterministic number in `(0, infinity)` for each `t`. No monotonicity, continuity, or measurability in the time parameter is needed. All limits here concern the full family as `t -> infinity`.

## Well-definedness and finite renewal measure

There is an `epsilon > 0` for which `P(X_1 >= epsilon) > 0`, since the union of events `{X_1 >= 1/k}` has probability one. Independence implies that infinitely many of these increments occur almost surely, so `S_n -> infinity` almost surely. Consequently `N_t` is finite for each finite `t`.

For any `lambda > 0`, set `q = E[exp(-lambda X_1)]`. Strict positivity gives `q < 1`. Markov's inequality and independence give

`P(S_n <= t) <= exp(lambda t) q^n`.

Therefore `U(t) <= exp(lambda t)/(1-q) < infinity`. All subsequent uses of `U(t)` are well-defined. Neither lattice restrictions nor absence of atoms is used.

## Exact tail identity, including the endpoint

For every `t >= 0` and `x >= t`,

`P(D_t > x) = U(t)r(x)`.                                                (1)

Indeed, the disjoint decomposition over the interval containing `t` gives

`P(D_t > x) = sum_(n >= 0) P(S_n <= t < S_n+X_(n+1), X_(n+1) > x)`.

On `{S_n <= t, X_(n+1) > x}`, the inequality `x >= t` implies `S_n+X_(n+1) > t`. Hence the second condition in the summand is redundant. Independence of `S_n` and `X_(n+1)` then gives (1). The strict inequality in the survival function makes this argument valid at `x=t`, even if the increment law has atoms or `t` is a possible renewal epoch.

The definition of `D_t` matters for this exact identity. For example, the forward recurrence time `S_(N_t+1)-t` instead has tail `sum_n E[1_{S_n<=t} r(t+y-S_n)]` at `y>=0`. Formula (1) is about the full interval length.

## Escape relative to the observation time

For every fixed `c >= 1`, (1), (P), and slow variation give

`P(D_t/t > c) = U(t)r(ct) = [U(t)r(t)] [r(ct)/r(t)] -> 1`.

For `0 < c < 1`, this probability is at least `P(D_t > t) -> 1`. Thus

`D_t/t -> infinity` in probability.                                     (2)

## Tightness forces the scale above time, even if it oscillates

Write `Y_t = D_t/phi(t)`. Suppose this family is asymptotically tight: for every `eta > 0`, some finite `M > 0` satisfies `limsup_(t->infinity) P(Y_t > M) <= eta`.

If `phi(t)/t` does not tend to infinity, there are times `t_k -> infinity` and a finite constant `C > 0` with `phi(t_k)/t_k <= C`. For each fixed `M > 0`,

`P(Y_(t_k) > M) >= P(D_(t_k)/t_k > MC) -> 1`

by (2). This contradicts tightness, for instance with `eta=1/2`. Therefore

`phi(t)/t -> infinity`.                                                (3)

This subsequence argument covers every possible oscillation of the scale. A proper finite weak limit implies asymptotic tightness: choose a large positive continuity point of its distribution whose upper tail is smaller than a given tolerance, and use convergence of the distribution there. Thus (3) is necessary for such a limit as well.

## Tightness actually forces convergence to zero

By (3), `phi(t) -> infinity`, and for every fixed `a,b > 0` both `a phi(t)` and `b phi(t)` eventually exceed `t`. Apply (1), and set `p_t(a)=P(Y_t>a)`. Then

`p_t(a)/p_t(b) = r(a phi(t))/r(b phi(t)) -> 1`.

These ratios are well-defined eventually because the survival is eventually positive. More directly, since `0 <= p_t(b) <= 1`,

`|p_t(a)-p_t(b)| <= |r(a phi(t))/r(b phi(t)) - 1| -> 0`.                 (4)

Fix `a > 0` and `eta > 0`. Tightness supplies a fixed `b > 0` with `limsup p_t(b) <= eta`. Equation (4) gives `limsup p_t(a) <= eta`. Since `eta` was arbitrary, `p_t(a) -> 0` for every `a > 0`. Nonnegativity now proves

`D_t/phi(t) -> 0` in probability.                                       (5)

Therefore every proper finite weak limit is `delta_0`, and no nondegenerate proper finite weak limit is possible. This excludes a finite mixed law having an atom at zero and positive mass elsewhere.

For a sharp equivalent criterion, under the present assumptions any deterministic positive scale satisfies

`Y_t is asymptotically tight` iff `Y_t -> 0 in probability`

`iff U(t)r(phi(t)) -> 0` iff `r(phi(t))/r(t) -> 0`.

The forward implication to `U(t)r(phi(t)) -> 0` follows from (3) and (1) at threshold one. Conversely, if `U(t)r(phi(t)) -> 0`, a bounded `phi(t_k)/t_k <= C` subsequence would give `U(t_k)r(phi(t_k)) >= U(t_k)r(Ct_k) -> 1`, a contradiction. Thus (3) holds, and slow variation in (1) implies (5). The last equivalence follows from (P).

## Atom at zero and properness

No tail convergence at threshold zero is asserted: `P(Y_t>0)=1` for every `t`, even when `Y_t` converges weakly to `delta_0`. Zero is a discontinuity point of that limiting distribution, and slow variation is applied only at positive multipliers.

Alternatively, if a proper weak limit `Y` were given initially, (4) would make its survival equal at every pair of positive continuity points. Properness forces that common value to be zero by taking continuity points to infinity. Nonnegativity then forces `Y=0` almost surely. This is a separate check on the weak-convergence argument and expressly allows an initial hypothesis of an atom at zero.

Proper finiteness is essential. A mixed limit with an atom at infinity on the compactified half-line is possible; it is outside the claim. An explicit example appears below.

## Verification of the proposed explicit law

Define `r(t)=1` for `0 <= t < 1`, and `r(t)=1/(1+log t)` for `t >= 1`. This is a valid continuous survival function with density

`f(x)=1/[x(1+log x)^2]` for `x > 1`.

The density integrates to one by `u=log x`, and is positive on `(1,infinity)`. The law is therefore nonlattice, strictly positive, and finite almost surely. Equivalently it is generated by `X=exp(1/V-1)` for `V` uniform on `(0,1)`.

For every fixed `c>0`, eventually

`r(ct)/r(t)=(1+log t)/(1+log t+log c) -> 1`.

The survival tends to zero. Its mean is infinite, since

`integral_1^infinity r(t) dt = integral_0^infinity exp(u)/(1+u) du = infinity`,

where `exp(u)>=1+u` makes the final integrand at least one. Hence it satisfies every distributional requirement supplied in the task. The renewal asymptotic (P) remains the accepted input for this law as for the general theorem.

Two further boundary checks use (1) and (P):

- For `phi(t)=t^c`, `c>1`, `P(D_t/phi(t)>a) -> 1/c` for every fixed `a>0`. The family is not tight. On `[0,infinity]` it has limit `(1-1/c)delta_0+(1/c)delta_infinity`; this does not contradict the proper finite limit conclusion.
- For `phi(t)=exp((log t)^2)`, `P(D_t/phi(t)>a) -> 0` for every fixed `a>0`, giving the allowed degenerate limit `delta_0`.

These calculations also show that merely requiring `phi(t)/t -> infinity` is insufficient for tightness.

## Final assessment and remaining gap

The corollary and the explicit law survive the independent falsification attempt. The exact identity, endpoints, oscillating scales, atoms, and properness have been checked directly. No central difficulty was transferred to a stronger unsupported claim: the only assumed result is precisely the supplied premise (P).

Remaining gap for an unconditional, fully sourced research result: independently establish or accurately cite (P) under the exact stated hypotheses. Remaining gap for a priority assertion: examine prior literature; this elementary audit establishes correctness conditional on (P), not novelty.
