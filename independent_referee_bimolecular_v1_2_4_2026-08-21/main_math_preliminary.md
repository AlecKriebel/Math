# Main referee mathematical pass — preliminary and blind

Timestamp: 2026-08-21 22:34 PDT. This assessment was written after reading the
complete 16-page journal PDF and the exact TeX source, but before inspecting
the verifier, committed reports, author audits, preservation records, or
validation summaries. It is deliberately provisional.

## Exact claim audited

Let the species set and the set of labelled reaction channels be finite. A
complex is a vector in `N_0^d`, every complex appearing in the graph has total
molecularity at most two, every rate constant is strictly positive, the
reaction graph has one undirected linkage class, and it is weakly reversible
(hence the whole complex graph is strongly connected). Propensities are
`lambda_r(x)=kappa_r (x)_{y_r}` with multivariate falling factorials. For every
initial population `x_0`, the state space under consideration is the reachable
set `Gamma(x_0)={z:x_0 ->* z}`. The theorem says this set is itself one closed
communicating class. If it has a population-changing jump, its minimal
population CTMC is nonexplosive and has finite expected positive physical
return time to every state; if it is an absorbing singleton, its stationary
law is its point mass. Consequently each reachable class has one stationary
probability law.

## Load-bearing audit

| # | Preliminary result | Independent check |
|---|---|---|
| 1 | Pass | If `x=rho+y -> rho+y'`, weak reversibility gives `y' ->* y`; adding the same nonnegative `rho` enables every reverse-path source. Reversing such lifted paths makes accessibility symmetric, and reachability is closed by definition. This covers `0`, faces, labelled parallel edges, lattice restrictions, and the empty return for a self-channel (TeX 249–291). |
| 2 | Pass | A mark is the actual fired channel's target, so the transition kernel depends only on the current population and the new target is enabled. Every population state in a nonabsorbing irreducible class is the endpoint of a positive-length channel path, giving surjective projection. A witnessed predecessor of any desired marked state plus population irreducibility proves augmented irreducibility (332–370). Equal displacements do not identify channels. |
| 3 | Pass | With `rho=x-t`, `V=sum_i log((x_i-t_i)!)` is proper because a sublevel bounds every residual coordinate and the target set is finite. After `s->u`, the new residual is `x-s`, so exponentiating the increment gives `prod_i (x_i-s_i)!/(x_i-t_i)!=(x)_t/(x)_s`; a source equal to the carried target has exactly zero increment (369–378, 453–470). |
| 4 | Pass | Along a designated path `t=y_0->...->y_m=c`, the population is exactly `rho+y_k`. Every deviation is included in the phase drift `delta` and ends the episode. Continuation has the exact labelled-channel probability `q_k p_k`, and its immediate increment is zero, yielding `J_m=delta(rho+c,c)` and `J_k=delta(rho+y_k,y_k)+q_k p_k J_{k+1}`. The `c=t` case is one final jump (520–566). |
| 5 | Pass | Maximizing `log p+C_0+q p M` over `0<p<=1` gives the stated two branches: the endpoint `p=1` for `M>=-1/q`, and `p=(-qM)^{-1}` otherwise. The supremum is monotone in `M`, and its lower branch tends to `-infinity`; finite backward composition therefore transports terminal negative drift through arbitrarily separated positive rates (571–616). |
| 6 | Pass | A diagonal subsequence makes each residual coordinate fixed or divergent. Normalizing the logs gives nonnegative weights summing to one. A divergent coordinate may have weight zero but stays in the divergent support `I`. Enabled falling factorials have log asymptotic `R_n w.y+o(R_n)`; fixed-coordinate factors are `O(1)`, including repeated species (630–684). |
| 7 | Pass | The binary trichotomy is exhaustive. If all complexes are top, `w.X` is invariant but diverges. If a top complex has two `I`-particles, bimolecularity makes it available from the residual over every lower complex. Otherwise every top has one `I`-particle. For the represented set `J`, top is equivalent to `q_J=1`; a unary top is available, a bounded companion present in a lower complex makes its paired top available, and if no lower has any companion then `sum_J x_i-sum_D x_D` is exactly zero on every complex and is a signed invariant whose negative coordinates stay fixed while its positive part diverges (694–787). This explicitly retains zero-weight divergent coordinates in `I`. |
| 8 | Pass | If `K` were infinite, properness selects a sequence with `V->infinity`; the trichotomy either contradicts a class invariant or supplies a fixed lower terminal whose episode drift tends to `-infinity`, contradicting membership in `K`. A global minimizer of proper `V` exists, and every episode endpoint has no lower potential, so every episode drift there is nonnegative; hence `K` is nonempty (814–840). |
| 9 | Pass | The selected episode has 1 to `|C|` jumps and drift at most `-1`. Each coordinate can rise by at most `2|C|` per episode, so every fixed-time stopped potential is integrable. Thus `V(Y_{n∧sigma})+n∧sigma` is a nonnegative supermartingale, bounded-time expectation followed by monotone convergence gives `E sigma_K<=V(z)`. No unbounded optional-stopping theorem is silently invoked (892–940). |
| 10 | Pass | From finite `K`, one jump followed by the established hitting bound gives finite mean positive return to `K`. Its trace is finite and irreducible; a uniform finite-path/minimum-probability argument gives finite mean trace return. Conditional excursion lengths are uniformly bounded in expectation, and Tonelli plus the trace return tail sum converts this to finite original-jump return. Projection can only make the first population return earlier and has the ordinary population kernel (946–1000). |
| 11 | Pass, cited standard theorem still to source-check | A positive recurrent irreducible jump chain visits a reference state infinitely often. The independent exponential holding-time subsequence at those visits has fixed finite rate and divergent total, excluding explosion. Moreover `inf_Gamma Lambda>=min_r kappa_r>0`, since every nonabsorbing state enables a genuine channel and every positive falling factorial is an integer; hence expected physical return is at most expected jump return divided by this lower bound. The regenerative occupation measure is finite, normalized by Tonelli, stationary by the regenerative theorem, and unique by irreducibility (1003–1071). |
| 12 | Pass | A state with no enabled population-changing channel is a closed absorbing singleton by lifted reversibility; its point mass is the unique law on that class. Every other reachable class is irreducible, and uniqueness follows after the recurrence construction (285–315, 1071–1073). |

## Re-derived displayed calculations

- For `0 -> A+B -> B -> 0` at `((n,0),0)`, the first designated jump is
  forced. The second is chosen with probability
  `kappa_1(n+1)/(kappa_0+kappa_2+kappa_1(n+1))`. At `((n,1),B)`, only source
  `A+B` has nonzero potential increment, namely `-log n`, so the expected
  increment is exactly `-[kappa_1 n/(kappa_0+kappa_2+kappa_1 n)] log n`.
- In Remark 3.1, direct source-by-source calculation reproduces all three
  phase drifts and continuation probabilities. The only order-`log n`
  terminal term is `-log(n-1)`, multiplied asymptotically by
  `[kappa_1/(kappa_1+kappa_2)] [2kappa_2/(kappa_1+2kappa_2)]
  [kappa_3/(kappa_1+kappa_2+kappa_3)]`, exactly the displayed positive
  coefficient.
- In Remark 6.2, direct calculation gives
  `D_0=a_m+p_m(b_m+q_m c_m)`. For fixed positive rates its leading term is
  `-[kappa_2/(kappa_1+kappa_2)] log m`; for fixed `m` and
  `kappa_2 downarrow 0`, `b_m->a_m` and `q_m c_m->0`, giving
  `a_m(1+p_m)>0`. The claimed lack of a rate-uniform location for `K` follows.

## Boundary attempts

- `0 <-> 2A`: even/odd lattice classes remain closed; the death propensity is
  quadratic and the proof's repeated-species branch is enabled eventually.
- `A <-> B` at population zero: both channels are disabled and the class is
  the correctly separated absorbing singleton; positive shells are finite.
- Absent species: its coordinate is exactly invariant; it cannot supply a
  divergent sequence within one class.
- Equal population displacements from distinct sources: the population kernel
  may combine endpoints, but the proof samples and marks labelled channels, so
  the potential recursion does not infer a source or target from displacement.
- Zero-length target path: the episode is precisely the terminal ordinary
  jump and the recursion has only `J_m=delta`.
- Arbitrarily small positive terminal rates: the scalar envelope preserves
  eventual negativity but provides no uniform exceptional-set scale, matching
  Remark 6.2.

No exact mathematical counterexample emerged in this pass. The internal proof
interfaces are provisionally complete. This is not yet a final validity
conclusion: the static verifier audit, independent computations/mutations,
artifact rebuilds, primary-source checks, and comparison with barred records
remain outstanding.

