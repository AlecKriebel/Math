# Working mathematical checkpoint, turn 1

Unreviewed and not yet sealed as a complete proof. Exact source: OWR 41/2024, Delecroix pp.2384–2387, Problem 2 p.2387. First N→∞ uniformly among square-tiled surfaces with at most N squares in the principal quadratic stratum Q(1^(4g−4)); then g→∞. One horizontal or vertical maximal-cylinder decomposition, each cylinder counted once. No primitive-cover restriction; heights unbounded. Not the separate diagonal N≈αg question, all directions, arbitrary strata, or a deterministic all-surfaces bound.

Candidate outcome: for every s_g→0 with g s_g→∞, the point process sum_i δ_(A_i/s_g) tends vaguely to PPP(dx/(2x)); all fixed interval-count moments converge. In particular the count in [1/√g,2/√g] tends to Poisson((log 2)/2), with expectation and variance tending to that mean. There is also an explicit total-variation asymptotic model for the entire normalized area multiset.

## Generative model and geometric reduction

Put n=3g−3 and a_j=ζ(2j)/(2j). On ordered positive compositions j_1+...+j_k=n, assign probability (1/(h_n k!)) product_i a_(j_i), where

 h_n=[z^n] exp(sum_j a_j z^j).

Equivalently this is the cycle-size multiset of the weighted Ewens permutation with weights θ_j=ζ(2j)/2. Given the composition, take independent Gamma(2j_i,1) variables Y_i, and set X_i=Y_i/sum Y_i. Thus conditional areas are Dirichlet(2j_1,...,2j_k).

Delecroix–Liu final JEMS 27(2025), DOI10.4171/JEMS/1469, full publisher PDF in sources/, Theorems1.4,3.2,4.1, Lemma6.4 and (6.1) supply exact area law and uniform correlator coefficients. On the event of a one-vertex stable graph and k≤(3/5)log(2n), its composition weights are, up to a factor depending only on g,

 [D_(g,k)/k!] ctilde_(g,k)(j) product a_j,
 D_(g,k)=(6g−5−2k)! 2^(2k−3) /
          ((g−k)!(3g−3−k)! 3^(g−k)).

This follows by integrating the monomials x_i^(2j_i−1): the 1/(2j_i)! in the polynomial becomes 1/(2j_i); the graph automorphism factor is 2^k k!. Conditional area law is the Dirichlet law above. Uniformly for k=O(log g), ctilde→1 and D_(g,k)/D_(g,1)→1, since

 D_(g,k+1)/D_(g,k)=12(g−k)(3g−3−k)/
                   ((6g−5−2k)(6g−6−2k)).

The total-variation model follows from this uniform density ratio and mass concentration on that event. Exact constants and final-edition formulas still need to be laid out in the full proof.

For moments, mere TV convergence is insufficient. Use DGZZ Inventiones230(2022) published Theorem1.12 at t=11/10<8/7 for polynomially small tails beyond (3/5)log(2n), and Theorem5.2 for separating contributions in that low-k range. The latter gives O((log g)^25 g^-1 2^k), which is polynomially small there. The same moment generating bound gives E[K_g^r]=O((log g)^r) for each fixed r. Thus bad-event contributions to fixed count moments vanish by Cauchy–Schwarz. Uniform density ratios transfer nonnegative good-event moments without multiplying their error by the maximum possible cylinder count.

## Mesoscopic proof route

Let q_n=n s_g→∞ with q_n=o(n). The generating function is

 H(z)=(1−z)^(-1/2) B(z),
 B(z)=product_(m≥2)(1−z/m²)^(-1/2),
 B analytic for |z|<4, B(1)=√2.

Hence h_n~√(2/π)n^-1/2, uniformly h_(n-r)/h_n→1 for r=o(n), and h_(n-r)/h_n≤C√((n+1)/(n-r+1)). Exact assembly factorial moments of cycle counts have the factor h_(n−sum j)/h_n times product a_j. For fixed-order counts in [a q_n,b q_n], sum j=o(n), and sum a_j→(1/2)log(b/a), giving independent Poisson limits on disjoint intervals.

Gamma smoothing does not require q_n≫log log n: do not use a union bound over every cycle. For compactly supported Lipschitz f, compare sum f(Y_i/(2q_n)) to sum f(j_i/q_n) in expectation. On j in [εq_n,Mq_n], E|Y/(2q_n)−j/q_n|=O(√j/q_n), whose a_j-weighted sum is O(q_n^-1/2). Below that range use the Gamma upper-tail Chernoff bound; above it use the lower-tail bound. For j>n/2 the coefficient-ratio factor is at most O(√n) and is overwhelmed by an exponential Gamma tail. This proves the marked point-process limit. Since total Y has Gamma(2n,1) law, total Y/(2n)→1, so normalizing preserves it.

For all fixed marked-count moments, use exact factorial sums with independent Gamma marks. If the total selected size is ≤n/2, the coefficient ratio is bounded and the weighted one-mark sums are uniformly bounded. If it exceeds n/2, one selected j≥n/(2r); the Gamma probability of falling into a q_n-scale interval is exponentially small in n, dominating polynomial coefficient bounds and logarithmic sums. Thus every fixed moment is uniformly bounded. Normalize by total Y using its exponentially concentrated Gamma law and K moments. Then moment convergence and the geometric bad-event bounds give the actual cylinder-count means as well as the laws.

Important source caution: OWR's microscopic statement uses 4g−4 while the exact published Dirichlet model has total parameter 6g−6. The mesoscopic dx/x result is insensitive to a fixed rescaling, but the proof must not silently substitute the microscopic normalizations. No microscopic normalization correction or new microscopic theorem is needed for this target.
