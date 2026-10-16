# Sealed first independent assessment

Target: PR166; problem 30002720; original claimed_solved1/5; requested exact head efc3f35a72543ad9ae76fd31a860116f1ffd4a32.

This assessment was made from the original COUNTEREXAMPLE.md and the neutral problem.json/source_manifest.json only. No author checker, review, gate/status/frozen verdict, root notes, sibling verdict, or operational review was consulted. The head string is the assigned provenance, not independently established through repository operations. Candidate bytes match the assigned SHA256 c72a38099e93b4d593be231e8f0c4ad726a399c3d61283da9f7b1f7e55801a5c and length 13938.

## Exact claim tested

For the stated stationary binary Markov source and exact cost charging a prefix count only while that count exceeds one, there is a fixed interior cylinder-nonboundary t such that (Y_n(floor(nt)+1)-c_n)/sqrt(n) is not tight for every deterministic real sequence c_n. This is a mathematical claim about a single fixed rank, not merely a process topology or data-dependent centering.

## Independent probability checks

1. The Bernoulli exponential estimate is valid uniformly in the grid parameter: the tilted centered cumulant has second derivative at most 1/4. At epsilon=sqrt(2 log(n)/n), each two-tail error is at most 2 n^(-4). There are n^2+1 points. Monotonic interpolation adds at most n^(-2), proving the stated 4 n^(-2) bound for n>=2.
2. Pair collision at depth H has probability at most binom(n,2) times the sum of squared depth-H cylinder masses. That sum is at most the maximum mass, (1/2)q^(H-1), since masses sum to one. The given H ensures q^(H-1)<=n^(-5). No independence between different pairs is assumed.
3. On no depth-H pair collision, all prefix counts beyond depth H are <=1. For any count L, L*1[L>1]-L equals -1 when L=1 and zero otherwise. Truncating at depths 0,...,H-1 therefore incurs at most H, not an unbounded singleton tail. The omitted deterministic mean tail is at most 2n q^(H-1). Endpoint avoidance is one measurable probability-one event over countably many endpoints. The bound is simultaneously valid for every path and hence for the sampled order statistic.
4. The claimed cylinder probabilities and endpoint mean values rederive correctly: P_j has 2j-4 digit changes in j^2-2 transitions; left/right endpoint continuation contributions are (3/2)P_j and (1/2)P_j. The length of W_j1 0^(2j) is P_j q^(2j)/12. Near the endpoints, prefix-tail bounds give the stated conservative errors P_j q^floor(j/2).
5. For w_j=P_j q^j, n_j=ceil(w_j^(-2)), sqrt(n_j)w_j tends to 1, sqrt(n_j)P_j>=q^(-j) tends to infinity, and log(n_j)=O(j^2). Thus the uniform error divided by n_j P_j tends to zero, since j^3 q^j tends to zero. The moving boundary displacement sqrt(n_j)(tau_j-t) tends to zero.
6. The triangular Bernoulli CLT is justified because endpoint parameters x_n=t+z/sqrt(n) tend to t in (0,1), variances grow linearly, and the bounded summands satisfy the Lyapunov condition. The integer rank differs from nt by at most one. Binomial/order-statistic duality then yields the stated normal order-statistic limit, including thresholds with standardized limits -1,0,1. Each side window has limiting probability rho>0.
7. Independence of side-window and uniform-cost events is unnecessary: P(E intersect G)>=P(E)-P(G complement). The two deterministic cost bands have relative width o(n_j P_j), and their gap divided by sqrt(n_j) diverges. A bounded sqrt(n_j)-scale window can intersect at most one band, for every center. Its missing band has probability at least rho-o(1), uniformly in the center. This proves non-tightness for every deterministic sequence of centers, with epsilon=rho/2 and arbitrarily large subsequence indices for every fixed radius.

## First verdict and exact remaining gap

No fatal probability/asymptotic gap is apparent. Provisional mathematical verdict: passes this mechanism, conditional only on the correctness of the cited exact algorithm/source definitions. The proof is analytic; finite tests can detect algebraic or coding errors but cannot prove its universal or asymptotic conclusions.

Still to do: record a complete independent derivation and diagnostic program; test integer/rational bounds, degenerate n, empirical-CDF interpolation, singleton stopping, moving-endpoint CLT, and negative mutations with explicit exceptions active under -O; inspect the supplied verify.py only after this seal; independently obtain primary source definitions if needed. No historical-priority/publication determination is within this review.

Checkpoint completion estimate: 45%. The estimate concerns this assigned probability/asymptotic adversarial review, not the research problem as a whole.

Assessment timestamp UTC: 2026-10-12T10:26:11.775219+00:00
