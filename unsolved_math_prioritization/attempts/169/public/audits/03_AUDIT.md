# Shared Stage 3 independent adversarial audit

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 3.

## Decision and exact scope

For each prime p, let k=floor(sqrt(p)), c=floor(100 sqrt(p)), and sample A uniformly among the k-subsets of G=Z/pZ. The unrestricted success event is that some T, chosen after inspecting all of A, satisfies |T|<=c and A+T=G. The affirmative target is convergence of its probability to one along all primes. A negative result needs a fixed positive failure probability along an unbounded prime subsequence. None of the accepted results below establishes either conclusion.

The strongest unrestricted sufficient bridge identified in this pass is weaker than positive-density residuals: a lower bound E R_c >= a c sqrt(k), for a fixed a>0 along unbounded primes, suffices for the negative contract. It is not proved and is not a necessary condition for a negative answer. The fixed-R localized hole statement also remains open. A growing-R replacement that forgets the actual peeled-centre budget is proved false on a high-probability event.

## 1. Collective resampling: valid identities, insufficient optimum conditions


### Exact exchange identity and its quantifiers

For fixed A,T of sizes k,m, put d_x=|(x-A) intersect T| and N_d=|{x:d_x=d}|. Delete a uniform q-subset of T and add an independent uniform q-subset of G\\T, where 0<=q<=min(m,p-m). The chance that a point with old multiplicity d becomes uncovered is exactly

(q)_d/(m)_d * binom(p-m-k+d,q)/binom(p-m,q),

with the term zero when d>q. Equivalently, multiplying the expected number of holes by binom(m,q)binom(p-m,q) gives

sum_d N_d binom(m-d,q-d)binom(p-m-k+d,q).

The first factor removes all d old covering centres; the second avoids its k-d potential new centres. Their independence is legitimate because the two samples are drawn separately from disjoint, fixed populations. There is no assumption that the coverage indicators of different target points are independent.

At a global minimum over m-centre sets, every outcome has at least N_0 holes. The all-q inequalities therefore hold. For q=1 and p-m-k+1>0 they give

N_1 >= mk N_0/(p-m-k+1).

The denominator condition holds eventually in the fixed-C sqrt(p) regime. These are necessary conditions, not a characterization of local or global optimality. If N_0=0 every inequality is automatically satisfied, so they cannot themselves exclude a cover.

### Exact fractional stationarity and an actual finite nonoptimum

The expected histogram of a uniform m-subset T is

n_d=p binom(k,d)binom(p-k,m-d)/binom(p,m).

Every q-exchange kernel is symmetric on m-subsets, so that uniform law is stationary. The above fractional histogram consequently satisfies every exchange equality exactly, with positive n_0 whenever m+k<=p. This is an exact obstruction to eliminating all positive-hole profiles using only the stated linear histogram constraints. It does not claim that an actual optimal T has this generally nonintegral histogram.

The Poisson limit follows correctly: for m/k->C and q/m->theta, the normalized expected holes at a Poisson(C) profile tend to e^(-C). The bounded first moment controls the tails in the termwise limit. This blocks a strictly positive leading-order contraction derived solely from that limiting profile, but does not preclude smaller-order improvements accumulated over many adaptive rounds.

The finite-check study supplies a stronger finite warning about sufficiency. At p=11, A={0,1,2}, T={0,1,4,8} has histogram (1,8,2,0). It is not globally optimal, but every averaged q-exchange inequality holds. The mean hole counts for q=1,2,3,4 are respectively 2,17/7,12/5,71/35, all larger than the current value one. Nevertheless six of the 126 two-exchanges yield covers. Thus an actual integer histogram can pass every averaged inequality while better configurations exist.

Both displayed plateau escapes in the constructive and exact reports are correct. Neither refutes a procedure allowing neutral moves or temporary coverage losses. Minimum-cover existence is not established by the connectedness of the fixed-cardinality swap graph.

### Variance cancellation under full random resampling

For fixed A and uniform m-subset T, let Q_s=binom(p-s,m)/binom(p,m), a=Q_k, and r_A(d)=|A intersect(A+d)|. The exact identity

Var U = p a(1-a)+p sum_(d!=0) [Q_(2k-r_A(d))-a^2]

follows by counting the union of the two forbidden centre sets. Uniformly for s<=2k and m<=C sqrt(p),

log Q_s = -ms/p - [m(m-1)s+ms^2]/(2p^2)+O_C(k^(-2)).

Subtracting the s=k expansion twice gives the claimed linear term (m/p)(r-k^2/p). The remaining logarithmic error is bounded by O_C((r+1)/k^2+r^2/k^3). Exponentiating is uniform even up to r=k, because the logarithmic ratio stays bounded in terms of C; its quadratic remainder is O_C((r^2+1)/k^2).

The exact identity sum_(d!=0)(r_A(d)-k^2/p)=-k+k^2/p<=0 is the required cancellation. The remaining error yields Var U=O_C(p+E(A)), hence O_(C,K)(p) when E(A)<=Kk^2. A maximum-codegree hypothesis is unnecessary. The mean p exp(-mk/p)+O_C(k), including the operational cap c, has the correct rounding error.

The restart outside an arbitrary current T_0 is also justified. Start with a uniform whole-group m-set B and replace its L=|B intersect T_0| forbidden elements by a uniform L-subset outside B union T_0. Permutation symmetry gives a uniform m-set B' outside T_0, provided 2m<=p. Since E L^2=O_C(1) and the hole counts differ by at most kL,

Var U(B') <= 2 Var U(B)+2k^2 E L^2.

The current T_0 may depend arbitrarily on A because this calculation conditions on fixed A,T_0 before fresh resampling. It does not justify treating partial adaptive exchanges as independent full restarts. The O(p) variance and positive-order-p mean do not determine the extreme lower tail among exp(Theta(k log p)) candidates.

## 2. Entropy: valid stronger typicality and exact normalization


### The specified typical event is legal

The report's H_p is a fixed finite intersection of already proved simultaneous properties: the precise Stage 2 Good event; exclusion of a fixed number of arithmetic-progression components; small doubling with K_p=(log log p)^(1/8); a fixed-size affine-envelope hole condition; and a specified exp(o(k)) family of sublinear-seed decoders. The quantitative check K_p^4 log^2(K_p+2)=o(log log p) is correct. Their intersection has probability 1-o(1).

The interval-covered stratified examples are removed by the progression condition. The Singer examples are removed by the affine-hole condition when its fixed envelope parameter is at least eight. They therefore do not disprove a theorem genuinely conditioned on this stronger H_p.

The quantifier warning is essential and correct: one cannot intersect the failure events for every conceivable low-entropy menu at once. Every singleton {T} is such a menu; taking all of them would simply assert failure of every cover. A decoder selected after seeing A must have its identity paid for in a family fixed before sampling A.

### Genuine minimal witnesses and normalized counting

If M_c(A) is the family of inclusion-minimal covers of size at most c, and m_c(A)=|M_c(A)|, the sum of 1[T in M_c(A)]/m_c(A) over T is exactly the success indicator, with zero convention when no cover exists. The report's H_p-restricted expectation identity is consequently exact. Canonical selection is another exact disjoint partition of the same event, not a probability estimate.

Prime-group translation symmetry forces at least p minimal witnesses whenever one exists. This saves only log p in the entropy. The verified p=19 Sidon examples have exactly one translation orbit of minimum-cardinality covers. They disprove a blanket finite claim of more minimum-cover orbits from low codegree; they do not bound the total number of inclusion-minimal witnesses of all sizes, and do not refute a typical asymptotic multiplicity theorem.

The unresolved factor is the inverse multiplicity under the correct cover-conditioned and H_p-conditioned law. It cannot be replaced by an unconditioned inverse expectation or by an independent private-point calculation. Normalization removes padding overcounting without supplying the missing numerical estimate.

### Weighted seed/advice compression criterion

For fixed decoders F_j with weights w_j>=0 and sum w_j<=1, let

Z(A)=sum_j w_j sum_(B subset A, |B|<=s_p) 1[A+F_j(B)=G],

where s_p=o(k) and every output has size at most c. Conditional on a fixed B subset A, the residual sample is uniform among (k-|B|)-subsets of G\\B. At least p-|B|c points are not covered by B, each with the stated exact hypergeometric miss probability. The exchange-Lipschitz constant is c. Thus the finite exponent

D_s=[(p-sc) binom(p-s-c,k-s)/binom(p-s,k-s)]^2/[2(k-s)c^2]

is valid, and uniformly for s<=s_p it equals (gamma_100+o(1))k, where gamma_100=e^(-200)/(2*100^2). All denominator and positivity conditions hold eventually because s_p=o(k).

Summing seeds contributes sum_(s<=s_p)binom(k,s)=exp(o(k)); summing the countable weighted decoder family costs at most one by nonnegativity. Therefore E Z<=exp[-(gamma_100+o(1))k]. If every hypothetical successful A in H_p admitted such a seed and decoder weight at least exp(-o(k)), Markov would give whp noncoverage. This is a proved implication with an unproved additive compression premise. Hardcoding arbitrary T does not meet the advice bound.

### Abstract incidence countermodel: what it does and does not prove

The orbit assignment is valid. For every A-orbit the p forbidden lists exclude at most p f_p T-orbits. Distinct assignments are possible when binom(p,c)>binom(p,k)+p^2 f_p, which holds for f_p=exp(o(k log k)). Each A receives exactly p minimal cap witnesses, each fixed used T succeeds on exactly p inputs, and independent translation invariance holds. Sublinear-seed decoder families still fail by their output-range bound.

The forbidden-list qualification is correctly restricted to specified outputs or cap subsets of bounded envelopes. It does not include all cap supersets of an arbitrary small core without accounting for their potentially much larger number. Declaring smaller sets unsuccessful in the abstract relation is not a proof about actual additive cores.

This construction legitimately refutes a counting-only implication from the enumerated properties to low-description covers. It is not additive and does not satisfy all residual, Lipschitz, intersection, or fixed-interval identities of the real problem. It cannot refute a theorem that uses those additional sumset-specific equations.

## 3. Localized peeling: a real growing-R failure and a surviving budget constraint


### Exact typical inputs and growing-R patch

For nonzero d, absence of d from A-A is independence of A in the d-cycle. The exact number p/(p-k)*binom(p-k,k) and resulting q_p=e^(-1)+O(1/k) are correct. A 4k swap bound gives the claimed density error O(k^(-1/4)) with failure exp(-Omega(sqrt(k))). This explicit rate, rather than an unspecified o(1), permits multiplication by log k.

The maximum-autocorrelation proof correctly extracts a matching of m edges from at least 3m occupied cycle edges. Its endpoint probability is at most (k/p)^(2m); the union bound gives the displayed p^(-2+o(1)) failure rate. No independent-edge model is used.

For R=ceil(log(p/k))+2 independent shifts of D=A-A, the expected complement is at most (e^(-2)+o(1))k. Therefore some X of size at most R has |H_X|<=k. Given any such residual H and an A with nonzero autocorrelations at most L, independently choosing one a_x in A for each x in H makes S={x-a_x:x in H} cover H. Its actual convolution is at most the indexed Bernoulli sum, because duplicate centres must be deduplicated. The mean is at most L+1, and exponential Markov plus a union over target points gives max A*S=O(log p).

This is a genuine high-probability counterexample to uniform noncoverage of H_X by all light S when R is about log k. Empty H is permitted and already falsifies that universal statement. It is not a cap-sized covering construction: X-A may use order k log k centres. No budget-feasible subset B of that envelope covering the rest of G was found. The fixed-R statement is neither proved nor disproved by this construction.

### Quantitative affine-hole concentration

For y outside X, the forbidden graph has no loops and degree at most 2|X|. Sequential sampling gives the product lower bound used in the report. Summing its linear and quadratic logarithmic errors yields exactly

a_p(R)=Rk(k-1)/(p-k+1)+2R^2(k-1)k(2k-1)/[3(p-k+1)^2].

With B_p(R)=(p-R)exp(-a_p(R)), a 4Rk swap constant and a lower deviation B_p(R)/2 give exponent B_p(R)^2/(128R^2k^3). The (R+1)p^R menu factor is valid. At R=floor((1/2)log k-3log log k), the negative exponent has order (log k)^4, beating the O((log k)^2) menu entropy. The simultaneous residual size bound is proved in this range; its density tends to zero and must not be called a fixed positive proportion.

Peeling with h=ceil(c/R) removes at most R blocks and leaves max convolution below h. The surviving centre count is at least B_p(R)/(2k), of order sqrt(k)(log k)^3 at the stated R. This is a quantified reduction, not a proof of a remaining hole.

### Uniform light moments fail, even at the exact cap

The full-budget pencil construction checks. Choose b=floor(h/2) anchors B subset A and S_0=z-B. Pad to c centres uniformly outside S_0. Each target's padding contribution has mean at most 101 and tail at Q_p=ceil(4log p/log log p) at most (101e/Q_p)^Q_p. The union bound is p^(-3+o(1)). If h>=2Q_p+2, some padding has max convolution below h and multiplicity at z at least b.

At h of order k/log k, every fixed factorial moment of order j>=3 is at least (b)_j/p, which diverges. This construction works for every A. Under the typical autocorrelation bound, on any H containing z with |H|>=k, the local mean is at most L_p+Q_p+1, yet the same lower moment grows faster than its j-th power. The failure persists when the correct local mean is used; it is not an artifact of substituting the global mean 100.

The audit independently supplied the simpler subthreshold-pencil version before padding. Neither version is claimed to cover H. A cover-conditioned moment theorem remains logically possible, whereas uniform untrimmed moment matching on the light class is false.

The degree-201 certificate below reduces the older order-399 requirement, but does not fix this scale conflict. A spike obstruction for order201 is already relevant at h of order k^(2/201); the budget-only number of allowed blocks can then be order k^(199/201), far beyond the logarithmic envelope range. This is not a proof that every actual cover requires that many blocks.

### Budget-preserving clipping and its limits

For all T simultaneously on an autocorrelation event r_A(d)<=L,

sum_y f_T(y)^2=kt+sum_(d!=0)r_A(d)r_T(d)<=kt+Lt(t-1)<=10100Lp.

At an even threshold M of order L^2, the fraction of sites above M is O(L^(-3)) and their total first-moment mass divided by p is O(L^(-1)). Clipping preserves the zero set and the centre budget. This is a useful uniform fact, but does not prove a positive zero mass or bound high polynomial moments. On a localized residual, the estimates must be divided by its relative size; a growing-R small residual cannot be treated as fixed-density without checking this loss.

A universal clipped Poisson law is still false. For T=A, all counts are even except possibly on the k diagonal sums 2A, and an even clipping threshold preserves that fact. The odd probability of a Poisson mean tending to one stays positive. The exact-cap strengthening also checks on L=o(k): take 100 distinct fixed translates of A. Their multiset union has deficit at most binom(100,2)L from its ordinary union. Correcting those duplicate centres and adding at most binom(100,2)L+99 centres to reach c affects only O(kL)=o(p) target sites. The indexed convolution is even outside at most 100k diagonal sites, so the clipped odd mass remains o(1), while the global cap mean tends to100. Thus a one-sided bounded certificate, rather than a universal Poisson-law approximation, would need genuinely new justification.

### What budget-aware localization retains

The actual data are disjoint blocks B_i subset x_i-A, each at least the peeling threshold, a disjoint light remainder S, and sum_i|B_i|+|S|<=c. With B their union, a violation of H_B not subset A+S is exactly a cap-sized cover. Every cover admits these data by peeling. Therefore the budget-aware universal noncoverage statement is an exact reformulation of the original deterministic event, with potentially useful structure, rather than an already easier theorem.

Replacing H_B by the smaller H_X forgets the interaction between the actual block sizes, centre budget, and the rest of the cover. The growing-R counterexample identifies the cost of that relaxation. Counting possible B inside X-A is insufficient without handling its A-dependence and the unrestricted remainder S.

## 4. Moment certificates: a precise lower-degree barrier and a valid degree201 bridge


### Zero-free matching through degree99

For n=100 and lambda>=sqrt(9900), the finite correction

q_j=e^(-lambda)[lambda^j/j!-(-1)^j binom(100,j)] for 0<=j<=100

with unchanged Poisson tail has q_0=0. Odd corrections add mass. For even j>=2, (100)_j<=[100*99]^(j/2)<=lambda^j proves positivity. The 100th finite-difference identity annihilates every polynomial of degree below100, giving exactly the first99 factorial moments of Poisson(lambda). The actual cap mean lambda_p=kc/p eventually meets the threshold.

The fixed-support strengthening is sound. At lambda=100 the masses on1,...,100 are strictly positive. Truncate a sufficiently long tail, restore its first100 moment equations using the invertible matrix ((j)_r) with rows0,...,99 and columns1,...,100, and use continuity to preserve positivity. The same finite support works in a neighborhood of100. Consequently no degree<=99 polynomial with the minorant sign conditions on1,...,k can have positive Poisson(lambda_p) expectation for large p, even when its coefficients depend on p.

Rounding this finite law to p sites and moving a bounded number between100 and101 gives an everywhere-positive integer profile with exactly kc total and O(1/p) error in each of these fixed moments. The restoration proof is an existence argument, not a numerically extracted degree99 finite-support certificate. Most importantly, none of these profiles is proved to factor as 1_A*1_T.

### Charlier certificate and the missing hypothesis

The generating function exp(t)(1-t/M)^x proves the stated orthogonality, and coefficient comparison proves the three-term recurrence. With a_j=M^j/j!, the vector q_j(1)=sqrt(a_j)(1-j/M), j<M, has eigenvalue1 in the principal Jacobi block because q_M(1)=0. Extending by b=sqrt(a_(M-1))/(2M-1) changes the quadratic form of I-J by

2sqrt(a_(M-1))b-(2M-1)b^2=a_(M-1)/(2M-1).

The value at zero telescopes to 2M a_(M-1)/(2M-1). Therefore the rational polynomial

P_M(x)=(1-x)[Q_M(x)/Q_M(0)]^2

has P_M(0)=1, is nonpositive at every positive integer, and has positive Poisson(M) expectation (2M-1)/(4M^2 a_(M-1)). At M=100 its degree is201 and its exact margin is

199*99!/(40000*100^99).

The pointwise zero-indicator minorant and every-cover inequality are correct. Continuity handles lambda_p->100; global padding to exactly c is legitimate for a putative cover. The weighted moment-error condition is sufficient for a positive proportion of holes, but is not established for arbitrary or cover-conditioned T.

The blanket uniform version is deterministically false: a cap set containing -A has f(0)=k, and the negative leading term of P_100 makes its empirical average tend to minus infinity. The light exact-cap construction above shows why merely lowering the peak by a diverging cutoff does not restore a uniform high-degree approximation. No assertion is made that degree201 is optimal, or that the certificate alone excludes a cover.

## 6. Final unrestricted acceptance gate

Let R_c(A)=min_(|T|<=c)|G\\(A+T)| and mu_p=E R_c(A). The already audited uniform-k concentration, with its conservative constant, gives

Pr[R_c=0]<=exp[-mu_p^2/(8kc^2)].

Thus a fixed a>0 and an unbounded prime subsequence p_j satisfying mu_(p_j)>=a c_(p_j) sqrt(k_(p_j)) would imply

limsup_j Pr[success at p_j]<=exp(-a^2/8)<1.

This is exactly sufficient to negate convergence to one. It does not bound the global limsup over all primes from a subsequence hypothesis, and it is not necessary for a negative answer. Divergence of the normalized expectation along all primes would imply whp noncoverage; small normalized expectation alone does not imply that the integer residual is zero. No requisite expectation lower bound was proved.

The other surviving bridges also require new input: a budget-aware localized hole theorem, a genuinely cover-conditioned entropy/compression estimate, a bounded one-sided certificate with controlled adaptive expectation, or an affirmative collective mechanism that reaches zero within the exact cap. Fixed-T probabilities, full-restart variance, canonical normalization, abstract moment feasibility, and the degree201 minorant do not supply these missing estimates.

All probability-model transfers in the accepted work preserve the exact uniform k-set law or explicitly condition on fixed A before auxiliary sampling. All adaptive union bounds count predetermined families or retain their stated restricted scope. No equality between the caps c and100k is assumed. The unrestricted question remains unresolved after this shared pass.

