# Independent attack derivations

This document reconstructs the current claim, including all rates and moments. It uses the authenticated geometric statements listed in REPORT.md. It is not an independent proof of the deep intersection-number or surface-counting theorems.

## 1. Latent law, graph symmetries and height normalization

Fix n=3g−3. Expand a one-vertex graph into positive monomials indexed by positive j_1+⋯+j_k=n. Its graph symmetry is 2^k k!: independent flips and permutations of its k loops. For each monomial, an unrestricted positive integer height m contributes m^(−2j), so summing heights gives ζ(2j), not1 and notζ(2j−1). Integrating ∏x_i^(2j_i−1) over Σx_i=1 gives ∏(2j_i−1)!/(2n−1)!. Thus its integrated weight is proportional to

    A_(g,k)/(2^k k!) × ctilde_(g,k)(j) × ∏ ζ(2j_i)/(2j_i).

The conditional normalized-area kernel is exactly Dirichlet(2j_1,…,2j_k). No Gamma parameter is inferred from a heuristic dimension: the exponents explicitly give total parameter2n=6g−6. Counts treat each maximal cylinder once; heights are multiplicities and are not extra cylinders. Sorting areas and then forgetting their order cannot increase total variation.

Let D=A/2^k. Direct cancellation simplifies the manuscript's ratio further to

    D_(g,k+1)/D_(g,k)=6(g−k)/(6g−2k−5).

For k=O(logg), log of this ratio is O((k+1)/g). Summing k such errors gives D_k/D_1=1+O(log²g/g), uniformly. Combined with a coefficient bound sup|ctilde−1|=o(1), every positive latent composition weight on k≤k_g is changed by a uniformly vanishing relative factor. Normalizing positive weights changes the factor by at most another vanishing relative error. Applying the same Dirichlet kernel gives the conditional Radon–Nikodym comparison for every nonnegative common observable with finite expectation. This step would fail with merely averaged coefficient asymptotics; the cited estimate is genuinely uniform over compositions, including highly unbalanced ones.

## 2. Why rare surfaces cannot destroy moments

Use t=11/10, k_g=floor(.6 log(2n)). E t^K=O(n^.05) gives

    P(K>k_g)=O(n^(−eta)), eta=.6log1.1−.05≈.0071861>1/220.

For k≤k_g, the multivertex/single-vertex comparison contributes at most O(log²⁵g·g^(−1+.6log2)), also polynomially vanishing. This is within k≤logg/log(9/4). The same exponential generating function gives the model's pgf bound.

For every fixed r choose L=A logn with A sufficiently large. Summing k^r n^.05 t^(−k) for k>L is O(log^r n); below L use K^r≤L^r. Hence both laws have E K^r=O(log^r n). Cauchy–Schwarz then gives

    E[K^r;bad] ≤ (E K^(2r))^.5 P(bad)^.5 =o(1).

No geometric count moment is transferred using total variation alone. A proposed counterexample concentrating huge counts on an o(1)-probability bad set is excluded by precisely these global logarithmic moments and polynomial bad probability.

## 3. Conditioning and the unmarked limit

For a count vector c with Σjc_j=n its mass is ∏a_j^c_j/c_j! divided by h_n. Removing r_j components gives, by shifting each count c_j→c_j−r_j,

    E∏(C_j)_[r_j] = (h_(n−m)/h_n)∏a_j^r_j, m=Σjr_j≤n,

and zero if m>n. This accounts for the dependence between component sizes. It does not assume independent backward labels or independent components after conditioning.

The product H(z)=(1−z)^−1/2 B(z), with B analytic in |z|<4, has B(1)=sqrt2, since ∏_(m=2)^M(1−1/m²)=(M+1)/(2M). Coefficient convolution gives h_n~sqrt(2/π)n^−1/2; the two-sided bounds yield h_(n−r)/h_n≤C sqrt((n+1)/(n−r+1)). The ratio tends uniformly to1 for r=o(n). These are absolute bounds, not unsupported rare-event relative estimates.

Set q=ns_g. For a fixed factorial order r in bounded j/q windows, all removed sizes sum toO(rq)=o(n). The ratio is consequently uniformly1+o(1). Also Σ_(aq≤j≤bq)ζ(2j)/(2j)→log(b/a)/2. The resulting joint factorial moments are those of independent Poisson window counts. Higher orders bound moments and first orders give local tightness. Poisson moment determinacy gives the unmarked point-process limit. A secondary ABT route has the same scope: for Poisson a_i, iP(Z_i=1)−1/2=O(1/i), while iP(Z_i=l)≤i^−1 C^l/l! for l≥2. Thus ULC holds with e(i)=1/i and summable factorial tail constants. No extra lower bound on the speed q→∞ enters either route.

## 4. Arbitrarily slow Gamma marking

For compactly supported Lipschitz f on [a,b], linearity and the single selected-component identity bound the expected discrepancy by

    Σ_j a_j h_(n−j)/h_n E|f(Y_j/(2q))−f(j/q)|.

For aq/2≤j≤2bq, the ratio is bounded, Σa_j=O(1), and E|Y_j−2j|/(2q)≤sqrt(2j)/(2q)=O(q^−1/2). For j<aq/2, only the marked term survives, and exponential Markov with Gamma mgf at1/2 gives P(Y_j≥2aq)≤exp[−a(1−log2)q]. Summing these weights costs O(log(q+2)), not O(logn).

For j>2bq, Markov with exp(−Y/2) gives P(Y_j≤2bq)≤exp[bq−2jlog(3/2)]≤exp[−c j], c=2log(3/2)−1/2>0. Up to n/2 the coefficient ratio is bounded. Above n/2 its sqrt(n) loss is absorbed by exp(−c n/2), regardless of how slowly q diverges. Every term tends0 even for q=logloglogn on a sufficiently large domain. An attempted union bound over all K cylinders would create an artificial rate restriction; the paper does not use one.

The marked measures therefore have the same limiting Laplace functionals. Since every composition has total Gamma shape2n, T/(2n)→1 in probability. Joint convergence with this constant needs no independence. The dilation map (measure,c)→Σδ_(c x) is continuous for c>0 in the vague topology, which gives the normalized model limit.

## 5. All fixed marked and normalized count moments

Let p_j=P(Y_j/(2q)∈[a,b]). The same three ranges show Σa_jp_j≤C_(a,b). For a fixed factorial order r, independent marks and the removal identity give

    E(M)_[r] = Σ_(j_1+⋯+j_r≤n) [h_(n−Σj_i)/h_n]∏a_(j_i)p_(j_i).

When selected total≤n/2 this is bounded by a constant times (Σa_jp_j)^r. Otherwise some j_i≥n/(2r). Since q=o(n), that mark has lower-tail probability≤exp(−c_r n) for all sufficiently large n. Bound all other probabilities by1, all remaining weight sums byO(logn), and the coefficient ratio byC sqrt(n). The entire remainder is O(sqrt(n) log^r n exp(−c_r n))=o(1).

Thus every marked compact-window moment is uniformly bounded. On T/(2n)∈[1/2,2], the normalized [a,b] count is bounded by the marked [a/2,2b] count. The complementary event costs at most n^r exp(−cn), since K≤n. A bound at a higher order gives uniform integrability for any fixed moment. Use the count in a union of windows to bound mixed powers. Vague convergence plus non-atomic limiting endpoints gives joint count convergence and hence all joint moments. The latent density ratio and bad-moment estimate in section2 then transfer the full original assertion to geometry, for arbitrary permitted s_g.

## 6. Sampling order and real endpoint obstructions

At fixed g the finite cylinder count is bounded by3g−3. Each mixture component with at least two cylinders has continuous simplex marginals; the only one-cylinder atom is X=1. Eventually every fixed rescaled compact window is strictly below1, so the fixed-genus N→∞ limit transfers count distributions and their fixed moments before g is sent to∞. No uniformity in N as a function of g has been established or used.

The excluded regimes have concrete obstructions. At s=1 a window [.6,.9] contains at most one normalized area, whereas a positive-mean Poisson law assigns positive probability to2. At q=1 the independent infinite marked assembly gives mean≈.41403449 in Y/(2q)∈[1,2], differing from log2/2≈.34657359. Primitive-only heights change that microscopic mean further to≈.30332328. These finite/high-precision diagnostics expose normalization mistakes; they do not prove a universal limit or a counterexample within the claimed intermediate regime.
