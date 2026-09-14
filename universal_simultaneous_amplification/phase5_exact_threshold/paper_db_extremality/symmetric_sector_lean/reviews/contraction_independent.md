# Independent audit of the completed-excursion contraction

Timestamp: 2026-09-14 14:54 UTC. I reviewed `Contraction.lean` independently
of its author against Appendix A (A.26)–(A.27), after independently checking
the six concrete block actions it uses.

At physical bad rank `k=i+2`, `phaseHhat` is exactly
`k/(N-2) * gᵃ_(k-1)`. Its predecessor ratio is
`(k-1)(k-2)/[(N-2)(N-k+1)]`, multiplied by `gᵃ_(k-1)`.
Its formal successor ratio is `(k+1)(N-k)/[(N-2)(k-1)]`.
The former is exact, including the zero bottom neighbor. The latter is an
upper bound at the true top boundary because the actual missing successor
is zero and the formal expression is positive. Multiplying it by the
nonnegative Q successor coefficient increases the upper bound on `Q Hhat`
and therefore lowers the bound on `(I-Q)Hhat` in the correct direction.

The resulting lower residual is exactly

`(N²-k+1)/[N(N-2)(N-k+1)] * gᵃ_(k-1)`.

This is the genuine `D v` upper bound obtained by substituting the proved
`t_(k-1) ≤ (N²-k+1)/[(N-2)(N-k+1)]`. The theorem
`phaseV_eq_radialVector` identifies v with the actual good inverse response;
the proof does not rename an arbitrary vector as the desired response.

At physical good rank k with `1≤k≤N-2`, the two C contributions simplify
independently to `k/[2N(N-2)]` and `(k-1)/[2N(N-2)]`, times `gᵃ_k`.
Their sum is `(2k-1)/[2N(N-2)]`, maximized at `k=N-2`, giving exactly
`c_N=(2N-5)/[2N(N-2)]`. At the final good rank `k=N-1`, the first
contribution is absent, so the true ratio is `1/(2N)`. Its comparison with
c_N is equivalent to `N≥3`. This proves the exact stated boundary allowance,
including N=3 where the interior and top ratios tie.

For N=3 the single bad coordinate has both neighbors absent. The proof
retains those zero extensions, rather than asserting two incompatible
separate endpoint equalities. Its lower residual is still valid. No
overlapping-boundary error from the printed intermediate formulas is imported.

Finally, `bad_inverse_D_phaseV_le` applies the actual proved nonnegative
inverse of `I-Q`, and `phaseA_phaseV_le` applies the nonnegative C action
and the actual inverse of `I-S`. Matrix associativity yields exactly
`A v ≤ c_N v` for `A=R_S C R_Q D`. All inverses used for cancellation
have proved unit determinants. No desired contraction inequality is
assumed, and no positive scalar is substituted for the actual excursion
operator.

No mathematical, indexing, sign, or boundary gap was found. Completion
estimate for this bounded independent review: 100%. The theorem does not
by itself prove the first-phase lower bound, left occupation bound, bad
debt comparison, or physical Hessian identification.
