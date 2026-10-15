# Root examination of older-theorem implications

Checkpoint: 2026-10-12 UTC. Case completion estimate 35%; priority review estimate 70%. The submitted mathematical theorem and corrected model/source scope are accepted. Final priority disposition remains pending the complete independent family artifacts and the fresh branching-bridge adversary.

## Exact comparison

The accepted example has finite integer offspring with `P(xi >= m) = m^(-1/4)`, rate-one vertex recoveries, and rate-lambda ordered-edge arrows. Infection means existence of an ordinary finite graphical path from the initial root. The candidate proves positive probability of infinitely many vertices infected simultaneously at `tau = 1/(2 lambda)`, with lower bound `(7/30) exp(-3/(2 lambda))`. Its almost-every-tree statement allows a tree-dependent finite time and does not assert explosion with probability one.

The original OWR question is existential. A valid consequence of older general results that supplies one such offspring law answers that qualitative question even if the old paper does not print the contact-process corollary. This distinction must be explicit in the final priority decision. A quantitative bound not located in the inspected older results does not establish universal novelty of that bound or restore novelty of the qualitative existence mechanism.

## Recovery-free thinning and ADGO 2013

Root read actual ADGO PDF pages 1–9, including the independent-edge tree interpretation (page 2), plump definition and survival conditioning (page 6), and Theorem 1.3 and equivalence theorem (page 7). Theorem 1.3 was visually checked. The complete manuscript was independently read by the branching family; Root does not claim that complete read personally.

Fix any finite `H > 0`. Retain a vertex precisely when its recovery process has no mark in `[0,H]`; these independent indicators have probability `p = exp(-H)`. Condition on retaining the root. The retained root component is a Galton–Watson tree with offspring `eta = Bin(xi,p)`. Conditioning on a vertex being retained does not bias its independent offspring field or its children's retention indicators. The possibility `eta = 0` is allowed: ADGO conditions on survival, which has positive probability since `E eta = infinity`.

For integer `m`, put `k = ceil(2m/p)`. Monotonicity of binomial counts and a standard binomial lower-tail estimate give

`P(eta >= m) >= P(xi >= k) P(Bin(k,p) >= m) >= c m^(-1/4)`

for all sufficiently large `m`, for a fixed positive `c`. In particular, after increasing the threshold, `P(eta >= m^3) >= 1/m`: the retained law is plump. Its large upper quantiles grow at least cubically. For an exponential edge weight of rate `lambda`, the small quantile is `-log(1-u)/lambda <= 2u/lambda` for `u <= 1/2`. The reciprocal-quantile series in ADGO Theorem 1.3 converges, so independent exponential first-passage weights on this retained tree have a finite-length infinite ray with positive probability, and almost surely conditional on retained-tree survival.

The finite ray sum can be smaller than any prescribed positive `H` with positive probability. One self-contained justification is that otherwise every rooted descendant, of which there are only countably many, would almost surely have no exploding ray of sum below `H`. A finite-sum infinite ray has some descendant tail of sum below `H`, contradicting that assertion. Each descendant has the same unconditioned branching law. This is also covered by Komjathy 2016 Claim 2.3, whose statement and complete proof Root read on pages 11–12. The inference concerns the same fixed retained offspring law; it does not change `p` midway through the argument.

Couple these exponential weights to actual arrows recursively: for each parent-to-child edge, use the first arrow after the parent's recursively defined arrival. A parent's arrival uses only its ancestor edges. Its distinct outgoing Poisson processes remain independent, and their waits are independent rate-lambda exponentials. This construction defines each finite-path arrival even after the global infimum accumulation time; it does not require a Markov restart from an infinite infected configuration.

On the event that the root is retained and a retained ray has sum below `H`, infinitely many ray vertices are reached by time `H`. Each endpoint uses only finitely many arrows, with no recoveries on retained vertices through `H`. Therefore these endpoints are simultaneously infected at the deterministic time `H` in the accepted minimal graphical process. This elementary bridge supplies the qualitative existential answer from a published 2013 general theorem. It does not supply the candidate's explicit numerical lower bound, and it must not be attributed as an explicitly printed ADGO contact-process theorem.

## BKV growing-degree first-arrow proof

Root read complete actual published BKV pages 46–48, equations (100)–(107), and visually checked page 47. The printed proposition concludes global survival. It allows `alpha + mu < 1`; the candidate has `alpha = 1/4`, `mu = 0`. Restoring full degree instead of offspring count changes only positive constants in the displayed rate estimates.

The first eligible arrow is an allowed specialization of the child selection. On an existing successful stage, its total rate grows at least as `r_m = c lambda K^(delta s1^m)` for some `delta > 0`, `s1 > 1`. If `W_m` is the first eligible wait and `H_m` the independent first recovery wait, then

`E[W_m 1{W_m < H_m} | revealed prefix and eligible rates] = R_m/(R_m+1)^2 <= 1/r_m`.

Set the term to zero when the prefix fails. The sum of these successful-prefix terms weighted by `m+1` has finite expectation. On the positive-probability infinite successful ray, both the total arrival time and `sum_m (S_infinity - S_(m+1))` are finite. No unproved conditional expectation given eventual ray success is used.

The independent exponential race density factors the unobserved recovery residual after a winning outgoing arrow as `exp(-e) de`, independently of the winner and wait. Future ray choices consult fresh descendants and do not expose these residuals. Conditional on this selective skeleton, the residuals remain independent rate-one exponentials. Summable probabilities of recovering before `S_infinity` imply that all but finitely many ray vertices remain infected at the finite accumulation time. At a deterministic integer beyond that accumulation time, the probabilities of persistence have a common positive lower bound; conditional independence then gives infinitely many surviving endpoints. A countable union supplies a deterministic integer with positive probability. Every endpoint is supported by a finite path.

Root read the complete independent timing adversary's report, which checks these conditioning details, degree offsets, finite-path convention, and a separate hereditary quenched upgrade. The inference is valid as a short addendum to the older proof, rather than an already printed common-time-infection theorem. The author-version family's separate deterministic-interval adaptation remains to be checked at final integration.

## Direct 2024 discussion and exact remaining gap

Root read actual Cardona-Tobon–Ortgiese–Seiler–Sturm arXiv2406.12689v1 pages 15–16 and v2 page 16, and visually checked v1 page 15. The authors explicitly discuss finite-time explosion for power-law offspring mass exponent `b` in `(1,2)`, refer to BKV Proposition 6.2, and propose setting the penalisation exponent to zero. The candidate's offspring mass is asymptotic to `(1/4) n^(-5/4)`, so it belongs to that range. Their prose is qualified discussion and must not be promoted to a printed exact theorem or probability bound.

The cumulative evidence rules out a new qualitative mechanism or an unqualified first resolution/current-openness claim for this example. The candidate's self-contained deterministic time and explicit lower bound remain mathematically verified quantitative content. The final disposition must compare that content with the original existential target and follow the user's publication rule; this checkpoint does not authorize a preprint, DOI, tracker row, PR mutation, or merge. All underlying source and page hashes and Root's actual read scope are pinned in `ROOT_FULL_PRIMARY_READ_RECEIPT_02.json`.
