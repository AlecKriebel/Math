# Root priority model comparison (provisional)

Timestamp: 2026-10-15T14:23:56.732966+00:00. PR885 remains under priority review; original effort 5/5. This is an analytical priority check, not a candidate revision or a new central proof-search turn. No publication decision is made here.

## Primary source inspected

Basdevant–Gouéré–Théret, *First-order behavior of the time constant in Bernoulli first-passage percolation*, arXiv:2106.12266v1 (23 June 2021), published Annals of Applied Probability 32(6), 4535–4567 (2022), DOI 10.1214/22-AAP1795. Actual PDF 967612 bytes, SHA256 9d78c8dd86aaa62dbaa7bfcaf40195c901c3cc9dee025bffd4a6e29af64339ba. Parent has read all relevant definitions, §§2.2–2.5 and §§3.1–3.4, including (19), Lemma19 and the evaluated sequence sum (33). Theorem1 and Proposition3 have the matching coefficient for a distinct undirected first-passage model. The direct theorem substitution is invalid; stronger published bounds require inspection.

## Exact finite distinction

For a simple path from (0,0) to (N,N), let b count backward steps, k_f count marked forward traversals and k_b count marked backward traversals. In a common confined box,

    target cost = 2N+b-k_f;
    ordinary symmetric Bernoulli FPP cost = 2N+2b-k_f-k_b.

Their difference is b-k_b >=0, and their defects are respectively k_f-b and k_f+k_b-2b. Consequently the matching ordinary-FPP deficit cannot by this pointwise comparison give the needed target upper bound. The whole-lattice versus confined-box distinction also requires care.

The independent root checker exhausts all twelve simple corner paths in Q_2 for four marked forward edges: (0,0)→(1,0), (1,0)→(1,1), (0,1)→(0,2), (0,2)→(1,2). Target minimum cost is 1; ordinary confined minimum is 2. This is an exact finite counterexample to model identity, not a counterexample to equal leading constants or a proof against every possible prior corollary.

## Stronger old-input corollary to be checked

Both initial priority families independently identified a potentially complete stronger route after inspecting the old counting proof. A new adversarial disposition family is checking it without their current reports.

Extend outgoing mark coordinates independently beyond Q_N, and set Y_x=1 when at least one of x's outgoing E/N edges is marked. These are iid Bernoulli r=2q-q² across x. Let S_r(M,M) be the old strictly coordinate-increasing open-site score, with nonnegative starts and each selected site strictly below the terminal corner.

A strict Y-open chain below (N,N) can choose one marked outgoing edge at each site and visit those edges monotonically inside Q_N: strict integer gaps absorb each one-step edge displacement. Hence D_N >= S_r(N,N).

For an optimal simple target path, use the old monotone subsequence construction on its visited open sites, excluding its terminal vertex, and append terminal (M,M), M=N+1. Every actual path vertex is strictly below this terminal. Let a be the number of extracted monotone gaps and l_j the numbers of intervening open sites. The total number p of listed open sites, excluding the origin, is a-1+sum l_j. The initial origin reward contributes I_0 to both bounds:

    k_f <= p+I_0;
    S_r(M,M) >= a-1+I_0;
    D_N-S_r(M,M) <= sum l_j-b.

For a nonlast selected strictly NE pair, a monotone comparison can use a marked outgoing edge at its start whenever that start is Y-open. The segment's marked forward count is at most l_j plus that initial indicator. Its cost is the L1 displacement plus b_j minus this count. Minimality therefore gives b_j <= l_j (the weaker l_j+1 also suffices). A full optimal nonnegative-cost path has optimal subpaths; replacing and erasing any loops is admissible. The last block satisfies the relevant coordinate-overshoot constraint directly because its visited vertices lie strictly below (M,M). Thus the old Lemma19 Items1–4, with d1=2, d2=0 and m=0, hold.

The old geometric quantity C (the distinguished coordinate's internal absolute variation plus the other coordinate's negative-variation term, summed over blocks) is at most 2b. Therefore an excess D_N>S_r(M,M)+eta M sqrt(r) forces

    C < 2 sum l_j - 2 eta M sqrt(r),

which is stronger than old Lemma19 Item5 with m=0 and old eta'=2eta, including its harmless +1. For a fixed valid list of distinct Y-sites the probability is exactly r^p. Requiring zero doubly-open sites is unnecessary: the m=0 slice imposes no double-open requirements, rather than imposing their absence. It appears to be a subset of the already evaluated nonnegative union/Chernoff sum (33), with parameter r. If that event inclusion is correct in every boundary case, the published bound tends to zero at fixed sufficiently small r as N→infinity.

Since 0<=D_N<=2N and S_r>=0, the event estimate would imply

    sigma_r/2 <= g(q) <= sigma_r/2 + eta sqrt(r)/2,

where sigma_r=lim E S_r(N,N)/N and M/N→1. Old site Lemmas10 and13 and the classical planar Poisson-chain constant give sigma_r/sqrt(r)→2. Sending q→0 then eta→0 proves g(q)/sqrt(2q)→1. This would be a complete old-input deduction with an explicit deterministic model-event comparison, rather than an identity with their standard-FPP time constant.

## Priority limits

The finite mismatch alone was insufficient to close the priority audit. Conversely, a newly written complete corollary from an old universal estimate does not establish that the precise Aldous flow result was stated or recognized in earlier literature. Its significance and the original-open-status premise require an explicit disposition after independent falsification. Any acceptable account must credit the full strength of the earlier estimates and cannot present this as a new Poisson or BK principle. The earlier candidate proof can remain mathematically valid despite a changed priority assessment.

No QUEUE reclassification, paper preparation, merge, closure, DOI deposit or tracker change has occurred.
