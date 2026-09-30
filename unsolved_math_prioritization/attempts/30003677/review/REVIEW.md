# Independent review: high-degree seeds in competing FPP (30003677)

**Verdict: PASS_COMPLETE_EXISTENTIAL_GROWING_SEED_RESULT. No mandatory correction.** The theorem proves that degree-only selection of a suitably slow threshold gives a vanishing-density, vanishing-half-edge-mass initial population which wins almost all vertices against any fixed faster rate and one uniformly selected fixed-degree competitor. The original source explicitly permits growing seed counts and asks an existential possibility question. Accordingly **claimed_solved, 2/5** is justified for that question, with the growing-seed qualification prominent.

Reviewed `CANDIDATE.md`, SHA256 `588cc7063ba7e44bddd7fefafac7369d467ad52e70effd304a69d3dca95ba783`. This is independent gpt-6-astra xhigh mathematical/source review, not human peer review or a certification of priority.

All **11,561** submitted controls reproduce byte-identically. A separate exact implementation passes **62,001** assertions on **9,999** finite competition instances, including **20,278** protected-path witnesses. The stochastic limit is proved analytically, not inferred from these controls.

## 1. Exact source scope supports the existence answer

I read the full Deijfen contribution in [OWR 57/2017](https://ems.press/content/serial-article-files/46721), printed pp.3442–3443, and visually inspected p.3442. Its last paragraph expressly discusses initial populations growing with n and selection based on degree, immediately before asking whether a weaker type can capture a positive fraction from high-degree vertices against a small-degree start. It imposes no fixed number of weak seeds or prescribed asymptotic budget in that question.

The same context and question occur in Section 5 of the full [Ahlberg–Deijfen–Janson preprint](https://arxiv.org/abs/1711.02902). Its introduction specifies independent type-specific exponential times on each edge of the configuration multigraph, irreversible occupation, and the parity repair by increasing one random degree. Assumptions (A1)–(A2) are finite limiting second moment, convergence of that moment, minimum degree two, and positive probability above two. These are exactly compatible with the candidate's iid unbounded law. Parallel edges are individual channels and loops do not infect a new vertex.

The primary [publisher metadata](https://doi.org/10.1002/rsa.20846) corroborates Random Structures & Algorithms 55 (2019), pp.545–559. This review uses the full stated preprint for the proof and concluding question, not a claimed line-by-line final-typeset comparison.

The candidate proves the result for every unbounded degree law satisfying the stated finite-second-moment and minimum-degree hypotheses. Even its explicit even-geometric law would suffice for the source's possibility question. The absence of bounded-support laws from a theorem requiring diverging seed degree is therefore not a gap in an existential answer.

A single hub, a fixed number of hubs, a prescribed polynomial budget, an optimal threshold and a competitor chosen adversarially after seeing the graph are distinct stronger questions. The candidate expressly excludes them. Its answer should always be described as the **existential growing-seed result**, rather than a fixed-hub result.

## 2. Deterministic path protection is sound

Any actual type-2 infection ancestry is a path from its starting vertex whose sum of type-2 edge times is its arrival time. Thus the actual type-2 set by T lies in the unopposed weighted ball B_2(T).

If a type-1 path has total type-1 weight at most T and avoids that entire ball, each of its vertices is unavailable to type 2 before T. Induction along the path shows that type 1 reaches each vertex no later than its cumulative path weight. Earlier type-1 infection only helps. This proof works on multigraphs; zero-weight diagnostics also satisfy it, although the stochastic model has strictly positive weights almost surely.

There is no use of an incorrect final-distance Voronoi description of two-type competition. The ball is an upper bound on the competitor, and avoiding it protects the entire witness path.

## 3. Degree limits, two-root coupling and nonexplosion

The iid empirical degree law and its first two moments converge in probability to the required limits. Finite second moment gives max_i D_i=o_P(sqrt(n)). The single parity correction changes the empirical second moment by at most (2 max_i D_i+1)/n, so it cannot disturb those limits. The count of degree-d_0 vertices is asymptotic to nP(D=d_0)>0, and the missing-root event is negligible.

The empirical size-biased probabilities converge pointwise to dP(D=d)/E[D]. Their total mass is one and the denominator converges, so discrete Scheffe convergence gives total variation convergence. Sampling partners without replacement changes only a bounded number of choices when exploration is stopped after at most M exposed half-edges. The probability of hitting exposed stubs or joining the two exposed regions is O(M²/n). Conditioning the second root to have degree d_0 is harmless: its class contains a positive asymptotic fraction of vertices, so encountering that root in a bounded exploration also has vanishing probability.

The fixed nonbacktracking path therefore has root degree D and independent subsequent total degrees D*. Minimum degree two ensures at least one forward half-edge at every new vertex of the limit tree. Auxiliary half-edge ordering does not inspect edge weights or alter the seed rule. Finite-graph cycles and collisions belong to the vanishing coupling-error event.

For the fast tree, an active half-edge has an Exp(lambda_2) lifetime and is replaced by D*−1 offspring. The offspring mean nu=E[D*−1] is finite. The expected active population is d_0 exp(lambda_2(nu−1)s), and the expected event count through fixed T is finite. One can justify this without assuming nonexplosion in advance by stopping at a fixed event count and applying the corresponding first-moment/Gronwall bound, then letting the cutoff grow. Finite expectation bounds exclude infinitely many events before T. Each revealed degree is finite almost surely, so the total incident half-edge exposure is finite almost surely as well.

This supplies the required cutoff argument: first choose M so the limiting path and time-ball explorations stay below it with probability at least 1−epsilon; then couple for n tending to infinity; finally let epsilon decrease to zero. The time-ball cutoff is a continuity event because edge weights have continuous laws. Consequently the full fixed path and the fast time ball are disjoint with probability tending to one.

The source's Section 2, especially pp.6–7, proves the same finite-time branching coupling mechanism. The candidate correctly checks the extra finite path and degree-conditioned root. It never substitutes growing R, k or T directly into a fixed-parameter local weak limit.

## 4. Fixed-threshold success estimate

For fixed k>d_0, each of the first R non-root path degrees has law D*. Unbounded support makes p_k=P(D*≥k)>0. The probability of no high-degree vertex on that path is exactly (1−p_k)^R in the limit. Ignoring a possible seed at the root is conservative.

The path is chosen without using type-1 weights. Their sum along its first R edges has mean R/lambda_1. Reversing the path does not change these undirected edge weights. Markov's inequality bounds failure to traverse it by T by R/(lambda_1 T).

Both conclusions can be intersected with the joint disjointness event by a union bound. No independence from the actual competition is assumed. Path protection then gives exactly the displayed limsup bound. It also handles the uniform test vertex equaling the competitor and the negligible missing-degree-class event through the coupling error.

## 5. The deterministic diagonal and the macroscopic conclusion

At level j, the proposed R_j and T_j make each of the two fixed-threshold error terms at most 1/j². The geometric bound (1−p)^R≤1/(1+Rp) is valid, including p=1 separately. Hence the limsup estimate yields a deterministic N_j after which the total failure probability is at most 3/j² for **every** n≥N_j.

Increasing N_j to satisfy strict monotonicity, N_j q_j≥4j² and log(N_j)≥jT_j preserves this probability statement. Every requirement is finite for each fixed j, and all choices depend only on the degree law, fixed degree and rates. They do not depend on a sampled graph, its degree list or weights.

For J(n)=max{j:N_j≤n}, we have J(n) tending to infinity. The selected thresholds and times diverge, and t_n/log(n)≤1/J(n) tends to zero. This holds across the whole sequence, not just at n=N_j. The lack of an explicit rate for N_j is allowed by the existence theorem.

Conditional on the completed infection process, an independent uniform test vertex is absent from type 1 with probability exactly 1−N_1(n,t_n)/n. Averaging and applying the diagonal estimate gives expectation at most 3/J(n)². Markov's inequality then proves that this absent fraction tends to zero in probability. There is no unsupported independence or concentration assumption for different vertex indicators.

## 6. Both initial resource fractions vanish

Before repair, the number of threshold seeds is binomial with mean nq_j. Its expected fraction tends to zero because k_n tends to infinity. Repair changes its count by at most one. Conversely nq_j≥4j², so Chebyshev's inequality shows that at least half this mean is present with failure probability at most 1/j². This proves divergence of the number of seeds while their fraction vanishes.

The original seed degree total has expected normalized value E[D 1_(D≥k_n)], which tends to zero by integrability. For the parity repair, the extra threshold degree mass is at most D_I+1, where I is the uniformly selected repair vertex. Although repair occurs on the odd-sum event, the required **unconditional** estimate is still

    E[1_(odd)(D_I+1)]
      = E[1_(odd)((1/n)Σ_i D_i+1)] ≤ E[D]+1.

Thus its normalized contribution vanishes. Since total degree is at least 2n, the fraction of seed incident half-edges tends to zero. This closes a potentially important loophole: a vanishing vertex fraction alone would not imply a vanishing half-edge fraction.

The even-geometric example is correct: with P(D=2m)=2^(−m), the mean is 4, the second moment is 24, and P(D*≥2j)=(j+1)/2^j. All degrees are even, so this example needs no parity correction and provides a concrete degree-two competitor.

## 7. Attribution and verification limits

The [Antunovic–Dekel–Mossel–Peres work](https://arxiv.org/abs/1109.2575), Theorem 2.6, already studies the effect of one fixed and one growing initial population on random regular graphs, including regimes where a speed disadvantage is overcome. Its [publication](https://doi.org/10.1002/rsa.20699) is Random Structures & Algorithms 50 (2017), pp.534–583. That phenomenon and the configuration-model branching machinery are properly credited. The candidate supplies its own degree-biased argument; it does not transfer the regular-graph theorem without proof.

The author verifier was copied with its frozen proof and its standard output matches the saved receipt byte for byte. The independent checker uses Floyd shortest-path matrices on induced subgraphs and a separate sorted-event competition implementation. It covers zero weights, ties resolved in favor of the faster type, loops, parallel edges and disconnected examples. It also checks parity-correction expectations and exact moment, geometric-tail and diagonal inequalities. All 62,001 assertions pass.

Run `python independent_checks.py` in this directory. To reproduce the submitted receipt, run `python verify.py` in `author_replay/` and compare its output with `verification.json`. These finite controls do not certify local weak convergence or the asymptotic diagonal; those arguments were independently reviewed above.

No mandatory correction remains. Recommend publication as an AI-reviewed complete affirmative answer to the original **existence** question in its explicitly permitted growing-seed regime, retaining the absence of a quantitative budget, single-hub result, adversarial-root result or historical-priority claim.
