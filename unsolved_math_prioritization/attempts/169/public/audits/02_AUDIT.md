# Shared Stage 2 independent adversarial audit

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 2.

## Decision

ACCEPT the partial theorems, counterexamples to specified proof routes, and exact diagnostics below with their stated scopes. DO NOT ACCEPT either an affirmative or negative resolution of the original random covering question.

The unchanged target is: for every prime p, sample a uniform k=floor(sqrt(p))-subset A of G=Z/pZ and ask whether Pr[there exists T with |T|<=c=floor(100 sqrt(p)) and A+T=G] tends to one. A negative answer needs a fixed positive failure probability along arbitrarily large primes. Exceptional deterministic A, failure of typical random T, and obstructions to particular proof methods do not supply either direction.

 No novelty assessment is made.

## 1. Constructive argument: protected translates and the optimal residual


### Protected-translate construction

The argument is valid. For D=G\(A-A), d=|D|, and current covered set S,

sum_{t in D}|(A+t)\S| >= dk-k|S|.

Averaging gives a new centre with gain at least k(1-|S|/d) when that expression is positive. When it is nonpositive, monotonicity suffices for the same recurrence. For the first k selections, d>=k ensures there are enough distinct allowed centres; at a zero-gain tie an unused centre may be selected. Hence the coverage s_i obeys

s_i >= d[1-(1-k/d)^i].

Every allowed translate avoids A. The already proved Stage 1 arbitrary-elementwise-map theorem, with phi(a)=-a, gives d>=p/(2e) with high probability in the exact uniform-k model. Since d<=p and k^2/p->1, the bound at i=k is at least p/(4e) eventually. The entire original A remains uncovered, and its centre zero has marginal gain k. Thus the maximum marginal exceeds the density prediction by at least k/(4e), much larger than sqrt(k log p).

This is a genuine counterexample to a pointwise mixing estimate quantified over every adaptive residual path. It is not a claim about the unrestricted greedy algorithm: the path is greedy only within D. Adding centre zero covers the protected copy of A, but is not shown to cover the rest of the group.

### The optimizer does not destroy Lipschitz continuity

Let R_m(A)=min_{|T|<=m}|G\(A+T)|. For each fixed T the residual is swap-Lipschitz with constant |T|<=m, as proved in Stage 1. Taking the minimum of a family of uniformly Lipschitz functions preserves that constant: compare using a minimizer at one input, then reverse the two inputs. The optimizing T may change arbitrarily without affecting this argument.

The manuscript uses the conservative constant 2m, so its bound

Pr[R_m<=E R_m-u] <= exp[-u^2/(8km^2)]

is valid. The sharper constant m would also be available, but is unnecessary. This concentration is already for the unrestricted optimum and needs no union bound over T.

Its consequences are correctly directed. A positive-density lower bound E R_c>=eta p would imply whp failure of every legal cover. Conversely, if Pr[R_c=0]>=delta>0, the same inequality forces E R_c=O_delta(p^(3/4)); if the covering probability tends to one, it forces E R_c=o(p^(3/4)). A fixed-T mean is not a lower bound for E min_T U(A,T), and no such expectation lower bound is proved.

### Exact excess accounting

For any adaptive ordered distinct centres, with q=1-k/p and excess e_i=g_i-(k/p)u_(i-1),

u_m=p q^m-sum_i q^(m-i)e_i.

The displayed identity follows directly from u_i=q u_(i-1)-e_i. Thus a cover with m<=c needs total positive excess at least (e^(-100)-o(1))p. The manuscript's proposed aggregate bound is explicitly unproved. Its exceptional-step sufficient condition also checks: gamma=e^(-100)/404, at most gamma k steps above gamma k, and e_i<=k imply total positive excess at most (101 gamma+o(1))p<e^(-100)p.

The protected translate supplies one order-k anomaly, which is o(p), so it does not contradict such an aggregate bound. A theorem only about one algorithm's excess would still not control every T.

## 2. Entropy argument: the stratified Good event and its exact limitations


The report defines one precise joint event Good: nonzero autocorrelations below 3 ceil(3 log p/log log p), Fourier magnitudes at most 1+4 sqrt(k log p), and energy at most 3k^2+k^(7/4). It proves Good with high probability both under the target uniform law P and under Q, the independent one-point-per-balanced-cell law. The latter is P conditioned on the stratified family H.

### Autocorrelation and Fourier checks

The autocorrelation proof does not assume independent difference edges. A d-cycle with at least 3h selected edges contains an h-edge matching. The probability of its 2h vertices under either law is at most k^(-2h), giving the stated p^(-2+o(1)) union bound.

For the stratified Fourier sum, subtracting 1/L times the full nontrivial character sum leaves only the longer cells; the expectation's modulus is at most r/L<=1. Real/imaginary Hoeffding gives 4 exp(-u^2/(4k)), so the reported frequency union bound is correct. For P, conditioning iid uniform draws on all being distinct costs a factor less than two, since the union bound gives distinctness probability greater than one half. This is an explicit valid transfer, not an assumption that collisions are negligible.

### Energy variance: the important dependence calculation

The decomposition E(A)=2k^2-k+X_3+X_4 is exact in odd characteristic. There are 2p(p-1) ordered three-distinct solutions and at most p^3 four-distinct solutions, giving E X_3=O(k) and E X_4<=k^2+O(k).

For two four-distinct tuples with disjoint vertex sets, covariance is nonpositive under P by the falling-factorial inequality. Under Q, if their block supports are disjoint the indicators are independent; otherwise they demand two different points in the same block and their joint probability is zero. Individually impossible tuples have probability zero as well. Thus discarding these covariances in an upper variance bound is legitimate.

For overlapping tuples sharing j<4 vertices, the two coefficient vectors have different four-element supports and are not proportional. The two additive equations therefore have rank two over every odd prime field. With v=8-j distinct variables, each of finitely many identification patterns has at most p^(v-2) assignments. Actual v-distinct assignments have inclusion probability at most k^(-v), giving O(k^(4-j)). The j=4 case contributes O(p^3/k^4)=O(k^2). Hence Var X_4=O(k^3), and the k^(7/4) deviations used in Chebyshev and Markov do give the claimed high-probability energy bound. No false independence or rank assumption was found.

### First-moment exponents and limits

Every stratified A has maximum cyclic gap at most m=2 ceil(p/k)-1=2k+O(1), so the fixed interval T0 of length m covers it. The exact probability P(H) is at least exp(-k-2), and Q(Good)->1 transfers this lower bound to Good intersect H. The family has log|H|=k log k+O(1); it remains exponentially rare under P.

All c-sized supersets of T0 give a truncated first moment with exponent (98+o(1))k log k. Adding a fixed k-set R of energy at most 4k^2 forces both sumset and difference support of the resulting centre sets to have size at least p/5. Padding a core of size 3k+3 gives exponent (97+o(1))k log k. The subtraction for the rare stratified event is only O(k), so both exponents are correct.

These are exact lower bounds on the specified unweighted truncated witness counts, not lower bounds on typical coverage probability. The counted large-doubling witnesses are redundant extensions of a small interval core. A stronger whp event excluding all simple fixed-menu covers, already justified in Stage 1, removes the whole stratified family. The report explicitly retains this boundary. It does not establish a minimal-witness obstruction after also excluding simple covering cores.

## 3. Structure argument: Singer transfer, padding and spectrum


The construction is valid as a deterministic method-obstruction theorem on infinitely many primes. It is not a random-model result.

### Source and algebra checks

The supplied finite-field argument proves the necessary Singer property: a trace-zero plane in F_(q^3), modulo F_q^*, produces q+1 points in the cyclic group of order n=q^2+q+1, with each nonzero difference occurring once. Nondegeneracy of the trace pairing is correctly justified by the nonzero trace polynomial and invertible field multiplication.

I independently inspected [Baker--Harman--Pintz, Theorem 1](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/BakerHarmanPintz.pdf). It guarantees a prime in [x-x^0.525,x] for all sufficiently large x. Applying it to x=n+2n^0.525 puts the entire interval strictly above n eventually, giving p=n+h with 0<h<=2n^0.525. This avoids any assumption that infinitely many Singer moduli themselves are prime. Unbounded q forces unbounded p.

With D0=D\{d0}, k=floor(sqrt(p)) and u=k-q, the bound u=O(p^0.025) is correct. For c=d0-a0 avoiding +/-h,+/-2h modulo n, S=(-D) union(c-D) has size 2q+1. Every difference from D-D is in D0+S, so D0+S=Z/nZ. The explicit lift T=S union(S-n) union(S+n) modulo p covers Z/pZ. Padding D0 preserves coverage and makes |A|=k exactly. Its at-most 6k+3 centres have a wide margin below the operational cap.

### Energy and good padding

An integer difference interval of length less than 2p has at most two representatives per p-residue. Thus E_p(B)<=2 E_Z(B)<=2 E_n(B), and a union of r translates has energy at most r^4 E(D). Their composition yields the stated E(T)<=15552k^2; the constant is conservative but correct.

For the embedded D0, every nonzero p-difference has multiplicity at most two. Uniformly padding by u points outside D0 has all intersections with translates of D0 at most two except with probability O(p^-0.425). The three-point union bound has the correct sample universe and scale p q^3 u^3/p^3. Repeated nonzero differences in the padding cost O(u^4/p+u^3/p)=o(1), including the three-vertex arithmetic-progression case. Fixing one good padding gives r_A(d)<=2+1+2+2=7 and E(A)<=8k^2. Arbitrary padding is not assumed to preserve this property.

### Zero-mode leakage and set-union correction

The Fourier interpolation formula is correctly normalized. Its Dirichlet kernels have total absolute mass O(log n) uniformly in the target frequency. More importantly, the j=0 term is at most |B|h/n: at a nontrivial p-frequency the full p-root sum vanishes, so the first n-root sum is the negative of the remaining h roots. This bound is uniform even at frequencies nearest zero. It gives leakage O(p^0.025), as does trivial padding control, both well below sqrt(k) log p.

For S, the nonzero n-spectrum is at most 2sqrt(q)+1. The passage to the actual union T requires correcting multiplicities. The avoidance condition on c gives r_(S,p)(h)<=4 and r_(S,p)(2h)<=8. The three pair intersections therefore total at most 16, and the nonnegative overcount correction has total mass at most 16. Consequently |T_hat(r)|<=3|S_hat(r)|+16. No unproved cancellation or ignored repeated points are present.

The proven spectral level is O(sqrt(k) log p), weaker than O(sqrt(k log p)) by sqrt(log p). The report now states this explicitly. It must not be merged with the sharper Fourier threshold in the entropy argument's Good event.

### Why these examples do not defeat the stronger known typicality

The final explicit containment is useful and correct. With

X={-n,0,n,2n,c-n,c,c+n,c+2n} modulo p,

T is contained in X-D, hence in (X-A) union(X-d0). As A+T=G, at most 8k points can be missing from A+(X-A). Thus these A violate the already proved Stage 1 positive-density hole condition for every bounded affine envelope. The construction is excluded by a known whp event; it is not evidence that every useful typicality truncation fails.

Outside X the displayed convolution is at most 40: each of at most eight shifts contributes at most two D0-to-D representations and at most three padding-to-D representations. It is at least one everywhere by coverage. Therefore discarding only the finitely many high spikes does not by itself restore a hole in this exceptional example. This remains a deterministic counterexample, not a typical-A assertion.

The cap-sized padded-witness first moment has lower exponent 93 k log k after dividing by the probability denominator binom(p,k). Its scope is explicitly predicates that admit these exceptional A, along the constructed prime sequence; it says nothing about minimal-witness counts or positive-measure coverage.

## 4. Structure argument: moments and heavy-point peeling


For every A, T=-A has a convolution value k at zero. Thus its fixed factorial moments of order j>=3 are at least (k)_j/p~k^(j-2), contradicting a uniform untrimmed Poisson approximation. This is a deterministic obstruction to that approximation and is not a cover.

The odd-order Bonferroni inequality is exact. The choice 399 and error thresholds are valid: Taylor's remainder is at most 100^400/400!<e^(-100)/4, so the order-399 Poisson partial sum exceeds 3e^(-100)/4 for 0<=lambda<=100. A weighted factorial-moment error at most e^(-100)/4 would leave at least e^(-100)p/2 holes. No such uniform estimate is claimed.

For the heavy-point reduction, each removed block contains at least h=ceil(delta k) centres in one set x-A. At most R=ceil((C+1)/delta) blocks can be removed. The remaining integer convolution is below ceil(delta k), hence strictly below delta k, including when delta k is integral. Every removed centre lies in X-A with |X|<=R.

The Stage 1 affine-envelope theorem applies simultaneously to every adaptive X of this bounded size. With high probability its hole set H_X=G\(A+(X-A)) has at least eta p points, eta=e^(-R)/2. If the original T covered, those holes must be covered by the residual T0, because the removed blocks cannot touch them. Therefore |T0|>=|H_X|/k>=eta k. This is a valid reduction for every hypothetical cover and every allowed peeling, not merely an excluded construction subclass.

Its missing conclusion is still substantial: rule out H_X subset A+S for every |X|<=R and every adaptive S of size at most c with max_x(1_A*1_S)(x)<delta k, on a positive-probability typical-A event. The remainder has exp(Theta(k log p)) possible descriptions and is tested against an A-dependent H_X. Its local mean need not equal the global mean. A constant-fraction cutoff still tends to infinity; lowering it to a fixed cutoff may require Theta(k) pieces and loses the bounded-envelope conclusion. None of these gaps is closed in Stage 2.

## 5. Private-point argument: uniform typical-A quantifiers


The exact-size codegree event is valid. A p-cycle matching union bound with r=ceil(4 log p/log log p) gives Pr[L(A)>=3r]<=p(e/r)^r=p^(-3+o(1)). It is not inferred from a Bernoulli model.

For fixed A and uniform m=floor(C sqrt(p))-set T conditional on t in T, the exact private mean is

nu=k binom(p-k,m-1)/binom(p-1,m-1).

There are k-1 forbidden other centres, which verifies the finite parameters. Exchanging another centre changes the number of private points by at most L(A): both increments relative to the common core lie in [0,L(A)]. The conditional martingale bound is therefore correct, and summing the probabilities over selected t gives the factor m, not p. For typical A, nu~e^(-C)k and the negative exponent is of order k/L(A)^2, which dominates log p. Thus every selected translate has linearly many private points for a proportion 1-o(1) of all T, uniformly over the stated typical-A event.

The hole count under random T separately has mean p binom(p-k,m)/binom(p,m)~e^(-C)p and swap bound k. Combining the two tails proves that a proportion 1-o(1) of all candidates are private-rich noncovers. Its logarithm is log binom(p,m)+o(1). This is a genuine typical-A entropy obstruction to using irredundancy alone. It does not say that inclusion-minimal covers, which additionally satisfy global coverage, have that cardinality.

The induced-matching interpretation is exact, but private points are selected after A and T are known. They cannot be counted as independent data. The report correctly distinguishes counting all certificates from counting candidate T.

The deterministic replacement lemma also passes: if every old translate has v private points, A+T is a subset of A+T', and at least one centre is deleted, each newly added centre covers at most L(A) private points of a removed translate. Therefore |T'\T|>=v/L(A). Mere nondecrease of covered cardinality is insufficient. The finite-check study supplies a counterexample to that stronger false interpretation. The theorem does not rule out nonmonotone or sufficiently collective repairs.

## 7. Combined frontier and final acceptance gate

The Stage 2 results are consistent with each other. They rule out several tempting shortcuts, while the following two genuinely unrestricted reductions remain open:

1. Prove a sufficiently large expectation for the global optimum residual R_c, or an equivalent sufficiently strong aggregate-excess obstruction.
2. After heavy-point peeling, establish a uniform hole statement for the adaptive light remainder on H_X, with typicality conditions that exclude the already understood simple covering cores.

Neither stratified nor Singer examples invalidate every such strengthened typical event. The former are removed by excluding simple interval covers; the latter explicitly fail bounded-affine-envelope typicality. Conversely, private-rich irredundant noncovers are abundant on a genuine typical-A class, so private witnesses alone cannot supply the missing cover-specific compression.

A later argument must still preserve the exact uniform k-subset law, allow all adaptive T, verify every dependence/conditioning step, and meet the cap with one-sided endpoint control. The heavy-point and optimum-residual reductions do not establish their unproved hypotheses. No probability limit or negation of the original target is accepted from this pass.

