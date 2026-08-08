# Research log: entropy and conductance certificates at dB fitness two

## 2026-08-02 10:18 PDT -- initialization

- Target: close the exact `rho_G-rho_K = L-V` sign, or at least prove the
  universal stationary-dual density ceiling `E|A|/n <= 1/2`, for every
  connected undirected weighted graph at dB fitness `r=2`.
- Routes under examination: stationary entropy production, conductance
  reversibility, global level flux, and coverage/submodularity.
- Explicitly excluded as already closed elsewhere: per-level residual signs,
  `L<=0`, statewise complete-Poisson domination, pairwise crossing bounds,
  and linear state potentials.
- No literature search is used.  Every candidate identity will be derived
  from the geometric-union generator and exactified before being recorded as
  a result.

## 2026-08-02 10:40 PDT -- fair-geometric resolvent channel delegated

- Delegated an independent order-two information attack to
  `chi_square_channel/`.
- The exact midpoint resolvent
  `2 nu_v = (sigma_v + nu_v) A_v` was proved, together with the posterior
  effective-event identity `sum_{v notin B} e_v(B)=|B|`.
- Two apparently natural contractions were killed exactly:
  fixed-`Pi` quadratic contraction expands by `2/3` on the unweighted
  three-vertex path, and revealing the effective/null flag exceeds the
  desired order-two bound by `168/20165` on the weighted triangle `(7,1,1)`.
- The aggregate target inequality `I_2(V;B)<=2` survived exhaustive directed
  uniform-row tests through four vertices and random/optimized tests through
  six vertices, but remains open.

## 2026-08-02 11:05 PDT -- Shannon entropy reflection isolated

- For the stationary random-target experiment, proved
  `tau_v(B)=(1+e_v(B))/n` on the holes and
  `Pr(effective|B)=|B|/n`.
- Derived the exact reflection identity

  `M-I(V;B) = E[(k/n) log((n-k)/k) - D(tau_B || Unif(B^c))]`,

  where `M=E h_2(k/n)=H(C|B)`.
- Proved that `M>=I(V;B)` implies the half-density ceiling: if
  `x=E k/n`, then `I>=-log(1-x)` and `M<=h_2(x)`, forcing `x<=1/2`.
- Complete graphs attain equality by exact pairing of levels `k` and `n-k`.
  The integrand itself changes sign; on a size-three state of `K_4` it is
  `(3/4)log(1/3)<0`.  A pointwise entropy proof is therefore impossible.
- Reversible and directed optimizations through five vertices found no
  negative aggregate gap.  This is numerical evidence only.

## 2026-08-02 11:48 PDT -- active entropy split and exact counterexample

- Proved the exact decomposition

  `M-I(V;B) = I(C;V|B) + (1/n) sum_v p_v [H(N_v)-H(S_v)]`,

  with `S_v` the deleted active source and `N_v` its effective output.
- The conditional-information term is nonnegative, but the separate active
  entropy expansion is false.  On regular weighted `K_4`, with cycle edges
  weight `4` and diagonals weight `1`, every `p_v=168/395` and

  `H(N_v)-H(S_v) = (1/336) log(2^158 3^9 7^84/(5^10 37^74)) < 0`.

  This is an exact rational/prime-log certificate, not a floating-point
  observation.  The full reflection gap on the same graph is positive, so
  the failure demonstrates essential compensation by `I(C;V|B)`.
- Added `ENTROPY_REFLECTION_REDUCTION.md` and the standalone exact verifier
  `verify_entropy_reflection.py`.  No universal sign has been proved or
  refuted; the output of this branch is a sharp new equivalent/sufficient
  gap plus exact closures of the most direct entropy-production routes.

## 2026-08-02 11:52 PDT -- exact reversal and comparison-route boundary

- Independent follow-up constructed the normalized Bayesian reverse channel
  forced by the Cayley identity and checked 400 labelled paths exactly.
  Forward and reverse path probabilities coincide, so the natural
  path-space entropy production is zero rather than the reflection gap.
- Blackwell dominance is impossible already on the unweighted three-path:
  membership-row total variation is `7/9`, while output-row total variation
  is `5/6`.
- Even scalar convex ordering of the membership and output likelihood ratios
  is false.  On the `(7,1,1)` triangle, the stop-loss gap at `t=3/2` is
  `-8/327`.
- These results are recorded in `chi_square_channel/SHANNON_REFLECTION.md`
  and checked by `verify_shannon_routes.py`.  Any surviving proof must use
  the specific `x log x` integral, stationary rank transport, and the
  null/effective compensation simultaneously.
