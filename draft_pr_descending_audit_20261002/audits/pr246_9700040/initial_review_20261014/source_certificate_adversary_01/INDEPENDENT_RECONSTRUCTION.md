# Independent source and claim reconstruction

Written 2026-10-15, before opening any inherited review verdict or historical manifest. Inputs read at this stage: submitted `PROOF.md`, `SOURCES.md`, `stationary_law.py`, the live primary problem page, primary 1993 notes pp. 36–40, 1999 article sections 2.1/5.2, and Okounkov–Reshetikhin v3 section 2.2.4. The author's claims are hypotheses, not evidence of correctness.

## Exact question and success criterion

The authoritative live page is David Aldous, *A one-dimensional drift-jump particle process*, https://www.stat.berkeley.edu/~aldous/Research/OP/left_Hamm.html. Its finite system has `0<X_1<...<X_k`, deterministic velocity `dX_i/dt=X_i`, and intensity-one space–time Poisson events moving the nearest particle strictly to their right when such a particle exists. Events to the right of `X_k` do nothing. It says the laws are consistent in `k`, that a unique stationary law exists by soft arguments, and asks: “Give some (fairly explicit) description of the stationary distribution.” The page dates its posting February 2018. My current reading is not a 2018 snapshot.

Thus the mathematical target is a reasonably explicit probability law on all simultaneous ordered coordinates, compatible with every finite projection. A formula for one marginal, an existence proof, a sample-generation description alone, or asymptotics alone would leave an exact gap. The source does not require an elementary density, a polynomial-time algorithm, or transition/multi-time probabilities. Whether a fully specified convergent determinant series qualifies as “fairly explicit” is a descriptive assessment; acceptance by the proposer cannot be inferred.

The 1993 notes, dated July 8, 1993, already contain the exact finite process in section 4.1, the Poisson-arrival/random-rank limiting representation (42), synchronous uniqueness Lemma 33, and the low-index distribution (45)–(48) in section 4.2. They include unfinished placeholders and warn that a section-4.2 result was inconsistent. Their existence and low-index material should receive credit, and a stationary formula must not inherit their rough coordinate transformation without verification. The 1999 article section 5.2 mentions the finite-pile process and constants; its RSK/LIS discussion is a primary route to finite counting, not a publication announcing an answer to the 2018 question. Imported dataset “open” or “no published description” labels are not authoritative historical conclusions.

## Independently reconstructed mechanism

Let a unit Poisson field occupy the positive `(u,v)` quadrant. Let `L(x,t)` be the maximum cardinality of a strictly increasing chain in `(0,x]×(0,t]`, and let `Z_r(t)=inf{x:L(x,t)>=r}`. Finite-rectangle patience sorting identifies the `Z_r` as the pile tops and shows `#{r:Z_r(t)<=x}=L(x,t)`. For each finite `r,t>0`, `Z_r(t)` is finite almost surely: construct an increasing chain successively in ordered disjoint positive-height strips. Local finiteness follows because `L(x,t)` is bounded by the finite rectangle count. Distinct Poisson `u` coordinates give strict order.

Set `Y_r(s)=e^s Z_r(e^s)`. At an underlying event `(u,v)`, the transformed event is `(x,s)=(uv,log v)` and the absolute Jacobian is one: `u=xe^{-s}, v=e^s`. Between events `Y` has velocity `Y`. Finite first-coordinate projections are autonomous because an event above the kth coordinate cannot change those coordinates. Scaling `(u,v)` by `(c u,v/c)` preserves area and shifts the time parametrization, so this is stationary for every real `s`. This establishes a shared simultaneous law for all `k`. The source's uniqueness or the independently checkable synchronous coupling then identifies this law with the question's unique stationary law.

Fix increasing thresholds `0<x_1<...<x_m`, arbitrary positive indices `r_j`, `b_j=r_j-1`, and `d_j=|lambda^j|-|lambda^{j-1}|`. Conditional on the counts in the vertical strips, the relative vertical ranks in horizontal order give a uniform permutation on `n=sum d_j` letters. RSK records all prefix shapes. For a fixed shape chain, the final insertion tableau has `f^(lambda^m)` choices; the recording tableau has `product_j f^(lambda^j/lambda^{j-1})` choices because each consecutive label block must fill its skew shape increasingly. Divide by `n!`, then multiply by `e^{-x_m} product_j (x_j-x_{j-1})^{d_j}/d_j!`. With `D_t(lambda/mu)=t^{|lambda|-|mu|}f^(lambda/mu)/(|lambda|-|mu|)!`, this is precisely the submitted positive determinant-chain weight. The event is `L(x_j,1)<=b_j` for every `j`. Summing all unconstrained chains of size `n` gives `x_m^n/n!`.

The complete-symmetric specialization `h_q=t^q/q!` and skew Jacobi–Trudi identify `D_t` with the stated factorial determinant. Okounkov–Reshetikhin v3 eqs. (7)–(8) directly support the determinant and containment. The exponential/tableau identification will be independently checked against the remaining primary source and finite skew-tableau recurrence. No unknown joint random-rank law remains in this representation.

## Does the stated event class determine the required law?

Yes, conditional on the preceding identification and formula: any finite list of events `X_r>x` can be sorted by threshold without sorting the indices. Repeated thresholds reduce to the smallest associated index because coordinates are increasing; thresholds at most zero impose no constraint. An empty conjunction has probability one. Repeated indices at different thresholds also cause no problem (the strongest threshold renders some conditions redundant). Joint CDFs follow by finite inclusion–exclusion of the complements `{X_r>t}`. No differentiation, density assumption, or efficiency promise is needed. A shared Poisson construction supplies consistency when unused coordinates are marginalized or `k` is enlarged.

The theorem is about the simultaneous stationary law. `s` in `Y_r(s)` is process time, while the series parameters `x_j` are simultaneous spatial thresholds. Confusing those two roles would invent a requirement absent from the original question.

## Initial falsifiable checks

1. Re-derive the rational truncation interval using both an unknown exponential tail and an unknown constrained tail; do not normalize by the truncated exponential without accounting for both.
2. Compare raw coefficients against direct permutation/LIS counting with arbitrary index order and rational strip widths, including normalization and logically redundant constraints.
3. Check determinant padding and transpose against a skew-tableau counting recurrence independent of determinants.
4. Separate exact rational endpoints from non-outward-rounded decimal displays; identify actual API/CLI limits.
5. Only after these notes are saved, inspect inherited manifests/reviews and compare every original/native input hash, source pin, and recorded result. A bounded search for old mechanisms will not establish novelty or historical closure.
