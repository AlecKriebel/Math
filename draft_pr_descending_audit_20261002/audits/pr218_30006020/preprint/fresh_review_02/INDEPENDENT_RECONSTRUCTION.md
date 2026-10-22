# Independent reconstruction before the earlier verdict

Review 02, 2026-10-15 UTC. This reconstruction was completed from the frozen manuscript and primary-source text before opening `fresh_review_01/REPORT.md` or `ROOT_M1_GLOBAL_REPAIR_ACCEPTANCE.json`. The task brief already disclosed a previous finite-conditioning precision finding, and the package's `PROVENANCE_CLARIFICATIONS.md` was incidentally read with its metadata. I did not treat that information as a clean verdict or a substitute for this reconstruction.

## Exact target and falsification criteria

The target is the principal holomorphic quadratic stratum Q(1^(4g-4)); uniform isomorphism classes of square-tiled surfaces with at most N squares; N tends to infinity at each fixed genus before genus tends to infinity; all positive cylinder heights; each maximal horizontal cylinder counted once; each cylinder area divided by whole surface area. The conclusion is vague convergence of the area multiset at any scale s_g tending to zero with g s_g tending to infinity to PPP(dx/(2x)), together with every fixed joint moment of counts in fixed compact windows. The specific original example is [g^(-1/2),2g^(-1/2)]. Neither a diagonal N(g) limit, arbitrary strata, simultaneous directions, rare-event relative errors nor endpoint scale theorems are part of the claim.

I sought failures in: source-ensemble identity; graph automorphisms and heights; positive-mixture normalization; uniformity as the vertex genus changes; exceptional count moments; arbitrarily slow intermediate rates; singular coefficient ratios near selected total n; Gamma dependence after normalization; unbounded moment transfer; priority attribution; and reproducibility/provenance.

## Geometry reconstructed

DL Theorem 1.4 gives the fixed-genus law of normalized areas, with m=infinity. Its Q_g notation includes holomorphic strata; DGZZ Section 2.1 immediately following equation (2.1) explains the negligible lower-dimensional nonprincipal contribution at fixed genus as the square cutoff increases. The principal limit is consequently the same law. OWR pp.2384-2387 specifies principal quadratic context, total-area normalization and iterated order, and its footnote states that automorphism weights do not change the limit.

DL equations (2.1)-(2.4), (3.1)-(3.3) and Theorem 3.2 give the positive stable-graph mixture. For the one-vertex graph with k loops the vertex genus is g-k and graph automorphism order is 2^k k!. Summing all height vectors over labeled edges, with that factor, equals the sum over weighted-graph isomorphism classes with their stabilizer orders (DL Remark 2.5). Thus heights do not create an omitted multiplicity factor.

Writing n=3g-3, the proof of DL Lemma 6.4 gives

F_(g,k)(x)=A_(g,k) sum_(j_i>=1, sum j_i=n) ctilde_(g,k)(j) product_i x_i^(2j_i-1)/(2j_i)!,

A_(g,k)=(6g-5-2k)! 2^(3k-3)/[(g-k)!(3g-3-k)!3^(g-k)].

The simplex integral of the monomial is product(2j_i-1)!/(2n-1)!. A height m_i contributes m_i^(-2j_i), and summing m_i>=1 contributes zeta(2j_i). The normalized kernel is Dirichlet(2j_1,...,2j_k). After graph division, integrated weights are proportional to

[D_(g,k)/k!] ctilde_(g,k)(j) product_i[zeta(2j_i)/(2j_i)], D_(g,k)=A_(g,k)/2^k.

No height conditioning or individual-area normalization remains. The Gamma total is exactly 2n=6g-6. Direct factorial cancellation gives D_(g,k+1)/D_(g,k)=12(g-k)(3g-3-k)/[(6g-5-2k)(6g-6-2k)]. For k=O(log g), the individual logarithmic discrepancy is O((k+1)/g), whose sum is O((log g)^2/g).

DL (6.1) permits every fixed C log(vertex genus) marked-loop range. Here ctilde_(g,k)=c_(g-k,k)(j_i-1) and k<=floor(.6 log(2n)); g-k is asymptotic to g, so this range fits, for example, a larger fixed C. The estimate is uniform in all allowed positive compositions; no large-j restriction is needed.

Uniform positive weight ratios remain uniform after conditioning and normalization. Applying the common Dirichlet kernel preserves this likelihood-ratio bound. Forgetting latent j, heights, ordering or graph labels can only decrease total variation. This proves the claimed conditional comparison once the bad events are controlled.

## Exceptional events and unbounded transfer

DGZZ Theorems 1.7 and 1.12 concern the same maximal-cylinder count K (not the height-weighted count). For t=11/10, its moment generating function is O(n^.05). The chosen cutoff produces

P(K>floor(.6 log(2n)))=O(n^(-eta)), eta=.6 log(1.1)-.05 > 1/220.

DGZZ Theorem 5.2's first assertion is a per-k multivertex-to-one-vertex relative estimate O((log g)^25 g^(-1)2^k), for k<=log g/log(9/4). Since .6<1/log(9/4), the cutoff eventually lies inside it. Also .6 log2<1. Summing positive contributions up to this cutoff bounds the multivertex probability by a negative power (with logarithmic factors); adding the K tail gives polynomially small bad probability. This does not extend Theorem 5.2 to its unstated range.

The same generating-function bound gives E K^r=O((log n)^r). To check this without differentiating an asymptotic formula, split at A log n and use P(K>u)<=C n^.05 exp(-u log1.1) above it, choosing A large for the fixed r. In particular E[K^r;bad]<=sqrt(E K^(2r) P(bad))=o(1). This works for both geometry and model and is enough even though the conditional coefficient error has no quantitative rate.

For a nonnegative count moment f, the uniform conditional density ratio makes its good-event expectation (1+o(1)) times the model good-event expectation. The latter is bounded by the independent Gamma-moment argument below. Bad-event count moments are bounded by the preceding K estimate. No implication from total variation to expectations of arbitrary unbounded statistics is made.

## Assembly and coefficient algebra

Set a_j=zeta(2j)/(2j). The unordered component-count law is h_n^(-1) product a_j^(c_j)/c_j! on sum j c_j=n. This is exactly DGZZ (1.7)-(1.8), Lemma 3.6, with cycle weight theta_j=zeta(2j)/2. An independent uniformly random ordering gives the ordered composition weights product a_j/(h_n k!). The independent Poisson representation uses only Z_1,...,Z_n and has finite conditioning probability exp(-sum_(j<=n) a_j) h_n>0.

Expanding zeta gives H(z)=(1-z)^(-1/2)B(z), B(z)=product_(m>=2)(1-z/m^2)^(-1/2). Its logarithm is analytic for |z|<4 and B(1)=sqrt2, since product_(m=2)^M(1-1/m^2)=(M+1)/(2M). Analytic convolution gives h_n~sqrt(2/pi)n^(-1/2), two-sided bounds for all n>=0, ratio h_(n-r)/h_n<=C sqrt((n+1)/(n-r+1)), and uniform convergence of the ratio to one whenever r=o(n). The same argument works for H^t for fixed t>0. Hence E t^K=O(n^((t-1)/2)) in the model.

Removing selected components yields E product(C_j)_(r_j)=h_(n-sum j r_j)/h_n product a_j^(r_j), with zero beyond n. This is the real-positive-weight specialization of AT Lemma 5/(126), whose substitution proof uses only the positive weights, and can also be derived directly here. There is no claimed new factorial identity.

With q=ns_g tending to infinity and q=o(n), fixed selected tuples from windows [aq,bq] have total size O(q). Their coefficient ratios tend uniformly to one. The sum of weights in a window tends to (1/2)log(b/a): the zeta correction is exponentially summable in j while the harmonic sum has that limit. Thus all fixed joint factorial moments tend to independent Poisson factorial moments; moment determinacy and first-moment local tightness give the unmarked PPP.

ABT Theorem 3.1 already implies the stronger unmarked count-vector approximation up to b_n=o(n). Its conditioning relation truncates at n even when an infinite comparison sequence is introduced. For a_j=O(1/j), jP(Z_j=1)=1/2+O(1/j), and for l>=2, jP(Z_j=l)<=C^l/(j l!); e(j)=1/j and factorial tail constants satisfy the uniform logarithmic condition. Attribution in the manuscript is therefore appropriate.

## Gamma marking, all rates, and moments

Conditional on a composition, choose independent Gamma(2j, rate 1) marks. Their mean and variance are 2j; T has Gamma(2n,1) law for every composition. Mark Y/(2q) before dividing by T.

For a compactly supported Lipschitz f with support [a,b], the first-moment selected-component identity bounds the expected difference of marked and unmarked integrals by sum a_j[h_(n-j)/h_n] E|f(Y/(2q))-f(j/q)|. In aq/2<=j<=2bq, the coefficient ratio is bounded and the variance bound gives O(q^(-1/2)) after summing a_j. For j<aq/2, the unmarked term is zero and P(Y>=2aq)<=exp(-aq)2^(2j)<=exp(-a(1-log2)q), producing O(log(q+2)e^(-c q)). For j>2bq, P(Y<=2bq)<=exp(bq)(3/2)^(-2j)<=exp(-c j), where c=2log(3/2)-1/2>0. Below n/2 the ratio is bounded; above n/2 its worst C sqrt n growth is killed by the exponential tail. None of these bounds needs q/log n to diverge. In particular arbitrarily slow q tending to infinity is covered.

Laplace-function comparison gives marked vague convergence. T/(2n) tends in probability to one, and dilation is continuous on locally finite measures on (0,infinity); Slutsky does not require independence from the marked process. Thus normalization by T is harmless for weak convergence. The scale factors are consistent: (Y/T)/s_g=[Y/(2q)](2n/T). No factor 2, 3 or 6 is left in dx/(2x).

For marked-window probability p_(n,j), the same tails give sum a_j p_(n,j)<=C_(a,b). Removing r independently marked components gives exactly the manuscript's r-fold sum with coefficient ratio evaluated at the selected total. If that total is <=n/2 the ratio is bounded. Otherwise some selected j>=n/(2r); because q=o(n), its lower-tail probability is <=exp(-c_r n). The worst ratio C sqrt n and remaining O((log n)^(r-1)) weight sums are then negligible. Every marked count moment is bounded uniformly in n.

On 1/2<=T/(2n)<=2, a normalized [a,b] count is bounded by the marked [a/2,2b] count. On its complement, use K<=n and the Gamma tail O(e^(-cn)). Higher moment bounds imply uniform integrability of every fixed moment. Counts on a finite union dominate mixed powers; the diffuse limiting intensity removes endpoint problems. Combining this with the geometric bad-event and density-ratio bounds completes all joint moment transfer.

## Boundaries, example and status

At fixed genus, normalized area laws with at least two cylinders have continuous simplex densities; the only one-cylinder atom is at one. For sufficiently large g the moving windows avoid it. Since K<=3g-3, fixed-genus convergence of counts and all their moments follows before taking genus to infinity. This verifies the stipulated iterated order.

For s_g=g^(-1/2), q=(3g-3)/sqrt g tends to infinity and q/n tends to zero. The [1,2] limit has lambda=(log2)/2. Its mean and variance are lambda and zero-count probability exp(-lambda)=2^(-1/2). No microscopic q=O(1) or macroscopic q proportional to n statement is smuggled into this calculation. The original OWR4g-4 microscopic multiplier is visibly different from 2n=6g-6 and is unused.

No mathematical counterexample or unsupported central step was found in this independent reconstruction. Remaining work at this checkpoint is package/current-history validation, source/visual receipts, and only then comparison against the earlier report and the global repair acceptance. This is an AI adversarial reconstruction dependent on published geometry, not external human peer review or a universal-priority certificate.
