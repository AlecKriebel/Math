# Independent derivation sealed before inherited-review access

Frozen submission: PR 218 head `dc457c741c779fbf90fbfdcdc73f750b3716f561`, attempt 30006020, CANDIDATE.md. This derivation uses only that submission and fresh calculations. It does not certify the external geometric inputs or novelty.

## Claim audited and assumptions separated

Analytic claim: for the exponential assembly with `a_j = zeta(2j)/(2j)`, conditioned on total size n, independently Gamma(2j,1)-marked parts divided by their sum have, at every q -> infinity with q/n -> 0, a rescaled local PPP limit of intensity dx/(2x), with convergence of every fixed joint compact-window count moment.

Geometric transfer is conditional on: (G1) the exact positive one-vertex latent mixture in (5)-(7), including the Dirichlet shapes and its normalization; (G2) a uniform relative error ctilde = 1+o(1) on k <= floor(.6 log(2n)); (G3) the actual K generating bound at t=1.1; (G4) the actual low-k multivertex excess bound in (13); and (G5) the exact fixed-genus area-law/surface correspondence. These are credited hypotheses here, not deductions from assembly analysis.

## 1. Assembly and prefactor algebra

Writing C_j for multiplicities, all ordered compositions representing C have k!/prod C_j! orderings. Dividing their weight by k! gives `prod a_j^C_j/C_j!`; summing is [z^n] exp(sum a_j z^j)=h_n. In particular no extra repeated-size factor is missing. For n>0 the k=0 term contributes zero.

For selected counts r_j, multiplying by prod (C_j)_(r_j), replacing C_j by C_j-r_j and summing proves (19) exactly. When the residual size is zero, h_0=1 is essential and present. When selected size exceeds n the expectation is zero.

From (5), its Dirichlet integral gives prod [(2j-1)!/(2j)!]=prod 1/(2j). The height sums give prod zeta(2j). Division by the loop automorphism factor 2^k k! leaves A_(g,k)/2^k times prod a_j divided by k!: thus the stated D is algebraically correct conditional on (5).

Direct factorial cancellation yields D_(g,k+1)/D_(g,k) = 12(g-k)(3g-3-k)/[(6g-5-2k)(6g-6-2k)]. For k=O(log g), numerator and denominator are positive, their relative difference is O((k+1)/g), and summing logarithms from k=1 gives O(k^2/g)=o(1). No comparison with an inadmissible k=0 graph is needed.

A positive uniform weight comparison survives conditional normalization: if every latent unnormalized weight ratio belongs to [1-d,1+d], the normalized density ratio belongs to [(1-d)/(1+d),(1+d)/(1-d)]. Consequently the relative comparison holds for every nonnegative integrable f, without an f-dependent error. Unbounded nonnegative count powers are therefore admissible after proving their integrability. Signed f would require an additive bound by E|f|; the submission does not use a multiplicative signed claim.

## 2. Product, branches, and coefficients

For |z|<1, absolute summability permits interchanging the m and j sums in sum zeta(2j) z^j/(2j), giving -1/2 sum_(m>=1) log(1-z/m^2). The canonical log at zero defines B(z)=exp(-1/2 sum_(m>=2) log(1-z/m^2)) throughout |z|<4. The log series converges normally on compact subdisks because sum m^-2 is finite. This constructs a single analytic, nonvanishing B and therefore also its analytic power B^t via the same logarithm. There is no unaddressed fractional-power branch choice for t=1.1.

The finite telescoping product prod_(m=2)^M (1-1/m^2)=(M+1)/(2M) tends to 1/2. The canonical value B(1) is positive, hence sqrt(2).

For fixed t>0 put alpha=t/2 and c_m(alpha)=[z^m](1-z)^(-alpha)=Gamma(m+alpha)/(Gamma(alpha)Gamma(m+1)). The coefficients d_k=[z^k]B^t decay geometrically, and c_m(alpha)~m^(alpha-1)/Gamma(alpha). For k<=sqrt(n), c_(n-k)/c_n -> 1 uniformly. The complementary convolution is negligible relative to c_n, because |d_k|<=C R^-k (any fixed 1<R<4) and c_m is polynomially bounded for 0<=m<=n. Thus [z^n]H^t~B(1)^t n^(t/2-1)/Gamma(t/2), including t=1.1. Coefficients are positive for t>0, since H^t is the exponential of a positive-coefficient series.

The t=1 estimate and positivity, with finitely many small indices absorbed, give c/sqrt(m+1)<=h_m<=C/sqrt(m+1). Division gives (18) uniformly for the entire 0<=r<=n, including r=n. If r<=u_n=o(n), then n-r -> infinity uniformly and h_(n-r)/h_n=(1+o(1))*sqrt(n/(n-r)) -> 1 uniformly. No uniformity close to r=n is claimed or needed.

## 3. Counts before marking

For q -> infinity, the sum of a_j over aq<=j<=bq tends to .5 log(b/a): the zeta correction is exponentially small in q; the harmonic sum has its usual integral limit, with endpoint roundings O(1/q). Fixed factorial orders select total size at most r b q=o(n), so the residual coefficient ratio tends to one uniformly across every tuple, including repeated selected sizes. Exact factorial moments therefore tend to those of independent Poisson window counts.

A complete method-of-moments justification is available: factorial identities give uniform bounds for every fixed higher moment of the finite vector, which ensure tightness and moment uniform integrability. Every subsequential limit has the independent Poisson mixed moments. These mixed moments determine a distribution, for example since its total count has the moment-determinate Poisson law and thus an exponential moment; expanding its multivariate moment generating function locally recovers independence. Disjoint bounded intervals away from zero form a determining class for locally finite point measures, and their total-count expectations give local tightness. Thus the count limits imply vague point-process convergence.

## 4. Marking without a hidden rate assumption

Let f be nonnegative compactly supported Lipschitz in [a,b]. On aq/2<=j<=2bq the residual coefficient ratio is bounded for all sufficiently large n since q=o(n). The expected displacement is sqrt(2j)/(2q). The weighted sum is O(q^-1/2).

For j<aq/2, the upper Gamma Chernoff bound using exponent 1/2 is exp(-aq)2^(2j)<=exp(-a(1-log 2)q). The residual ratio is bounded here, and sum_(j<=aq/2) a_j=O(log(q+2)), which gives a vanishing bound for every q -> infinity, including q growing slower than every iterated fixed logarithm.

For j>2bq, the lower Gamma Chernoff bound using exponent -1/2 is exp(bq)(3/2)^(-2j)<=exp(-(2log(3/2)-1/2)j). The positive constant is approximately .31093. For j<=n/2 the residual coefficient ratio is bounded. For j>n/2 it is at most C sqrt(n), still dominated by the exponential sum. Hence E|<f,Z_n>-<f,U_n>| -> 0.

For nonnegative f, |exp(-<f,Z>)-exp(-<f,U>)|<=|<f,Z>-<f,U>|. Nonnegative compactly supported Lipschitz tests are convergence determining for the Laplace functionals of point measures (general continuous compactly supported tests can be approximated using local mass tightness). This proves the same PPP limit for Z_n.

T is exactly Gamma(2n,1) conditional on every composition, so T/(2n)->1 in probability. Positive dilation is continuous on the space of locally finite point measures with the vague topology. Joint convergence with a scalar tending to a constant needs no independence. This validates the normalization step.

## 5. Marked moment bounds

Put w_j=a_j P(Gamma(2j)/(2q) in [a,b]). The same three ranges show sum_(j<=n) w_j<=C uniformly for sufficiently large n. Applying the exact factorial identity to independent marking yields the ordered tuple sum (23); repeated j values correctly correspond to distinct selected parts and require no correction.

For fixed factorial order r, tuples with sum j_i<=n/2 contribute at most C(sum w_j)^r. If sum j_i>n/2, one index j_i>=n/(2r). For sufficiently large n, bq<=j_i/2; its marking probability is at most exp(-c j_i)<=exp(-c n/(2r)). The coefficient ratio is at most C sqrt(n), there are r choices of the large coordinate, and sum a_j=O(log n). Thus this remainder is bounded by C_r sqrt(n) exp(-c n/(2r))(log n)^r=o(1). Dependence of the threshold and constants on the fixed r is harmless; the theorem does not assert uniformity in moment order.

On 1/2<=T/(2n)<=2, normalized-window counts are bounded by the unnormalized count on [a/2,2b]. The complement has probability <=C exp(-c n), and K<=n in the ideal assembly. Its contribution to a fixed r-th moment is <=C n^r exp(-c n). Hence every normalized compact-window moment has a uniform higher-moment bound, giving moment convergence from the count law. A finite union has the same proof, so all fixed joint ordinary moments converge.

## 6. K tails and transfer

For t=1.1, beta=(t-1)/2=.05 and alpha=log(1.1). The model generating function is [z^n]H^t/h_n=O(n^beta). Conditional on (G3), the actual generating function has the same upper bound. For k_cut=floor(.6 log(2n)), Markov gives P(K>k_cut)<=C n^(beta-.6 alpha)=O(n^-eta), eta=.6 log(1.1)-.05>1/220. Rounding changes only a fixed factor. More precisely eta is approximately .0071861079.

For every fixed p, split the tail integral for E K^p at L log n with L>beta/alpha. The first part is O((log n)^p); the Chernoff tail contributes O(n^(beta-alpha L)(log n)^(p-1)). Thus all fixed K moments are O((log n)^p). This holds even though using just E[t^K] as an upper bound for K^p without splitting would give a weaker polynomial bound.

Under (G4), 2^k<=C n^(.6 log 2), so the low-k multivertex excess is O((log n)^25 n^(-1+.6 log2)), polynomially small since 1-.6log2 approximately .58411. Averaging a conditional bound cannot worsen its uniform maximum. Combining it with the K tail gives a polynomially small bad probability.

For f a nonnegative r-th count power, C<=K and Cauchy-Schwarz give E[f;bad]<= (E K^(2r))^(1/2)P(bad)^(1/2)=O((log n)^r n^(-c/2))=o(1). The identical argument removes the model K tail. The normalized latent density comparison on good then gives the actual fixed moment the model limit. The o(1) density error multiplies a uniformly bounded model conditional count moment, not an uncontrolled power of log n. This distinction is correctly maintained in the submission.

## Independent conclusion

No counterexample or algebraic/probabilistic defect was found in the audited analytic assembly, coefficient, mesoscopic marking, moment, or conditional transfer arguments. Strongest independently checked result: the entire ideal-model analytic theorem and the transfer implication under G1-G5. Exact remaining audit gap: whether all G1-G5 are indeed provided by the cited final-edition primary sources in the precise stated principal-stratum scope. No novelty or priority conclusion is drawn.
