# Independent audit of the analytic-tail implications

Timestamp: 2026-09-14 14:54 UTC. This is a second review of
`Analytic.lean` and `AnalyticTail.lean`, independent of their implementation.
I compared the actual definitions with Appendix A (A.20), (A.23),
(A.27), (A.30), (A.32), and (A.34), and checked the direction and domain of
each inequality linking the polynomial identities to the true phase margin.

The proof does more than certify discriminant coefficient lists. The sum
of squares identity for the actual `G_N(j)` is expanded by Lean's ring
normalizer, and each term is proved nonnegative for `N≥84`, `j≥0`, with a
strictly positive constant term. This includes the requested tail domain.

The rational lower bound `24N/(25N-24j)` is proved for the actual recursive
`t N j`, not postulated as a replacement variable. Its rank-one comparison
has cleared difference `2N(N-12)`. Its inductive comparison has residual
`2N²(25N-24j-276)`, nonnegative on `N≥288`, `1≤j≤N-1`.
The recurrence denominator, current and previous lower-bound denominators,
and all multipliers cleared in these comparisons are strictly positive on
that domain. The proof covers `j=N-1` and does not attempt an absent rank N.

For the debt comparison, write `E=3Nj+3N-8j-10`. Substituting the lower bound
in the actual beta term gives exactly

`25*j*(j+2)*(25N-24j)/(66*(N-2)*E)`.

The residual obtained by comparing this with `19/20` is exactly `2G_N(j)`:

`19*66*(N-2)*E - 500*j*(j+2)*(25N-24j) = 2G_N(j)`.

I independently expanded both sides. `E>0`, `N-2>0`, and the lower radial
bound is positive on `N≥288`, `1≤j≤N-2`. Consequently replacing the actual
`t` with its lower bound gives an upper bound on its reciprocal in the
correct direction. `betaTerm_lt_nineteen_twentieths` retains the actual
`betaTerm` definition, and `beta_lt_nineteen_twentieths` passes the strict
bound to the actual finite maximum over precisely those physical ranks.

For epsilon, the actual inequality is equivalent, after positive factors
are cleared, to `22N²-1066N+2555>0`. Its value at `N=46` is 71, and its
shifted form is `22(N-46)²+958(N-46)+71`, positive for all `N≥46`.
The checked proof includes `1-c_N>0`. Thus adding the two strict bounds
proves the actual `beta N + epsilon N < 1` for every integer `N≥288`.
There is no endpoint gap between the finite range ending at 287 and this
tail beginning at 288.

For the other barrier polynomial `P`, the shifted sum of squares proves
positivity for every rational `N≥25,k≥0`. The separate exact check at
`N=24` includes all physical bad ranks `2,...,23`, with minimum 24 at rank
15. Connecting `P` to the actual boundary rows remains a separate block
comparison obligation; a positive polynomial alone cannot discharge it.

No mismatch or missing implication was found in these analytic-tail files.
Their conclusion is the genuine all-order phase margin, not yet positivity
of the reduced scalar or its identification with the active-chain quadratic
form. Completion estimate for this bounded audit: 100%.
