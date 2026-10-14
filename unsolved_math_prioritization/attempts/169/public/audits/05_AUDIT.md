# Stage 5 final independent adversarial audit

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 5.

## Decision and exact acceptance gate

**UNSOLVED after five shared substantive passes.** The accepted results below are partial theorems, exact identities, conditional bridges, and counterexamples to specified proof mechanisms. No affirmative proof or negative counterexample meeting the original probability contract was found or survives this audit. A conditional bridge is not promoted to a solution.

For each prime p, put k=floor(sqrt(p)) and c=floor(100 sqrt(p)); choose A uniformly among all k-element subsets of G=Z/pZ. The question is whether

Pr[there exists T subset G with |T|<=c and A+T=G] -> 1

as p tends to infinity through all primes. T may depend arbitrarily on the complete A. A negative answer requires a fixed positive failure probability along an unbounded prime subsequence. An exceptional deterministic set, a rare family of sets, a particular unsuccessful algorithm, or finite tests cannot supply that conclusion. The operational cap is not silently replaced by 100k, although 100k<=c<=100k+99 is used in the favorable direction.

## 1. Primary-source scope and cumulative accepted results

The source remains [Green, *100 Open Problems*, Problem 39, PDF page 20](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf#page=20). I independently reread that page in the previously retrieved complete PDF and verified its hash against the source manifest. It states the square-root random-set covering question and comments on the constant 1.01; it does not determine the answer's direction. The exact uniform law and floor conventions are the operational contract's explicit interpretation of the source's implicit rounding, not precision quoted from the original.

I also independently reread [Bollobas--Janson--Riordan, *On covering by translates of a set*, v2, Theorem 4.7 and Corollary 7.3](https://arxiv.org/pdf/0910.3815v2). The former's n<=k^(1+delta/7), for fixed 0<delta<1, fails when n=p~k^2; the latter fixes k before n tends to infinity. Neither can be applied on the square-root diagonal. The previously checked general bound tau(A)<=(p/k)H_k has a growing logarithmic coefficient, not the required fixed 100. The prior source-scope audit also checked the Rodgers--Sahay and Alon--Pham papers and found no matching theorem. This is a dated, bounded source assessment; it is not an exhaustive literature claim or proof that no other result exists.

The earlier accepted rounds establish the following useful but insufficient facts:

- Predetermined subexponential menus, fixed bounded-doubling envelopes, fixed numbers of arbitrary predetermined elementwise maps, and specified sublinear-seed decoders cannot furnish typical covers at a fixed square-root budget. Their quantifiers do not cover arbitrary descriptions chosen after A is seen.
- Rare interval-covered and Singer-derived sets expose failures of naive first moments and coarse pseudorandomness tests. The stronger explicitly predetermined typical events already exclude those examples. None has the probability mass needed for a negative answer.
- Private-rich noncovers are abundant for typical A. Inclusion-minimality, private witnesses, fixed-candidate means, and full-restart variance do not control the unrestricted optimum.
- Uniform residual concentration survives arbitrary changes of optimizer. Heavy-point peeling is valid when actual retained blocks and their costs are kept. For fixed pencil count, the residual has asymptotic density exp(-r), and every outside translate has capacity (exp(-r)+o(1))k. This forces about k outside centres, not more than the whole c budget.
- Ordinary fractional covering and the budgeted residual fractional completion both have about-k optimum. The stronger Stage 5 coordinate-conditioned obstruction is reviewed below.
- Polynomial and bounded one-sided score certificates are valid. Untrimmed moments, universal Poisson matching, and literal clipping do not acquire the missing adaptive estimate. The degree-201 certificate and the degree-99 moment barrier are statements about their precise certificate classes, not solutions.
- Same-A shift amplification, exact repair, additive partition identities, cycle consistency, and canonical normalization are valid. Their required quantitative optimizer or weighted-counting estimates remain unproved.

These conclusions are mutually consistent. The new final-pass theorems sharpen the surviving frontier rather than overturning the exact target.

## 2. Collective construction: probability amplification and its missing input


### Sharper optimum concentration

For A=B union {a} and A'=B union {a'}, each fixed-T sumset is B+T plus at most |T| new points. Therefore the difference of their cardinalities, as opposed to their symmetric difference, is at most |T|. Taking minima over the common family gives the sharper bound

|R_m(A)-R_m(A')|<=m,
R_m(A)=min_(|T|<=m)|G\(A+T)|.

The random-order coupling of completions differs by at most one swap; the conditional expectation range is at most m. Azuma therefore gives each tail exp[-u^2/(2km^2)]. This strengthens the previous conservative denominator 8km^2 and does not require stability of the optimizing T or a union bound over T.

If alpha=Pr(R_m<=v)>0, the lower tail yields

E R_m<=v+m sqrt(2k log(1/alpha)).

When the mean is already at most v the inequality is immediate; alpha=1 presents no exception. If rm<=c, b=c-rm, and B=[(b+1)p^(r-1)]^(1/r), the previously proved deterministic amplification and repair imply

failure at cap c => R_m>=B.

The integer b+1 is necessary. Combining the upper tail gives the valid finite bound

Pr(failure)<=exp[-(B-v-m sqrt(2k log(1/alpha)))_+^2/(2km^2)].

The repeated near-covers use the same A; auxiliary shift averaging creates no independence assumption. Duplicated centres only reduce the cost.

At m=33k,r=3, the exact cap leaves b=k+O(1), so B~p^(5/6). Thus an event R_(33k)<=o(p^(5/6)) of probability at least exp[-o(p^(1/6))] would imply failure probability exp[-Omega(p^(1/6))]. In particular, a fixed positive probability of a 33k-centre cover would suffice. **No such initial event is proved.** The known stratified complete covers have only an exp[-k+O(log k)] proved probability, far below the required scale. This is a comparison of available lower bounds, not an upper bound on the true success probability.

### Other collective improvements retain their scope

The nonuniform-budget amplification product is valid by induction. Substitution of the available constant-density residual estimates still gives a constant-density bound; this does not prove that better alignments are impossible.

The integer greedy recurrence g_(i+1)=g_i-ceil(kg_i/(p-i)), g_0=p, is sound: selected centres touch no remaining hole, while each hole has k available centres. Its integer update is monotone for i<=p-k. The bounds pQ_i-i<g_i<=pQ_i, Q_i=binom(p-k,i)/binom(p,i), follow from summing rounding errors below one. At any fixed Ck budget this remains (exp(-C)+o(1))p. A tiny constant exp(-100) cannot be converted into a vanishing power of p.

Random restriction of a fixed parent S and its fully adaptive T(S) has exact expected holes sum_x binom(|S|-d_x,k)/binom(|S|,k). Its discrete convexity and positive-density lower bound for fixed-ratio thinning are valid for the retained parent T. They are not lower bounds on the reoptimized child residual.

The pairwise collective-exchange formula keeps actual old and outside neighbourhood unions, including x=y. Direct deletion and addition probabilities yield the stated second moment. For a globally optimal T, the exchange residual H lies in [u,u+qk]; hence Var(H)<=delta(qk-delta), delta=E H-u. The stronger descent test is valid, but neither its adaptive variance nor its adaptive mean drift is controlled sufficiently to force improvement. The finite plateau illustrates this distinction; it is not a convergence theorem.

## 3. Actual-additive graph counting and correct canonical normalization


For a p-edge bipartite graph J on k+t labelled vertices, the plus-incidence matrix B has rank r=k+t-h, including isolated components. A consistent bijective edge labelling has exactly p^h coordinate preimages. The Fourier orthogonality formula

N_J=p!p^(-(p-r)) sum_(xi in ker B^T) C_p(xi)

is exact with the declared permutation-Fourier normalization and sign. The collision-partition formula is exact Mobius inversion over equal edge labels, with every rank taken in characteristic p. These formulas neither discard cycle constraints nor make them independent.

The affine action on complete permutation labellings is free, so N_J is zero or divisible by p(p-1). At t<=c the Fourier zero-mode count is exp[-p+O(k log p)], below one eventually. Any feasible graph therefore needs an exponentially large total nonzero-mode correction relative to the zero mode. This invalidates a graphwise independent-cycle approximation on feasible graphs. It does not invalidate an averaged theorem asserting most graphs are infeasible.

For distinct-coordinate tuples, sum_J Q_J=sum_z product_x f_z(x). Each feasible J has at least p^2(p-1) such tuples under common nonzero dilation and independent translations of the two vertex parts. AM-GM then proves

|G_real|<=(p)_k(p)_t (kt/p)^p/[p^2(p-1)].

For lambda=kt/p in a fixed compact subinterval of (1,infinity), division by binom(kt,p) gives exp[-d_lambda p+O(k log p)], d_lambda=-(lambda-1)log(1-1/lambda). At the cap d_lambda->-99log(99/100). This is a real sparsity theorem for representation graphs, not the probability of a random A. The endpoint lambda=1 is not smuggled into the stated uniform entropy expansion.

The improved representation lower bound is also valid. On an actual cover, Y=f-1>=0 has mean mu=lambda-1 and second moment nu<=V=L t(t-1)/p-lambda+1. Necessarily V>=nu>=mu^2>0. Under size bias by Y, the function phi(y)=log(1+y)/y is decreasing and convex, as follows from its integral representation. Jensen and nu<=V give

log product_x f(x)>=p(mu^2/V)log(1+V/mu).

At the cap and the proved typical codegree bound this yields Omega(p log L/L), still o(p). No arbitrary occupancy law is claimed to factor additively. The optional private-target upper bound is applied only to genuinely inclusion-minimal pairs.

The report deliberately defines K_c(A) as one cap-sized canonical cover. Padding establishes the event equivalence; it does not make K_c minimal. For its graph weights W_J, the identity

Pr(H_p and success)=sum_J W_J/[(p)_k c!]

is correctly normalized. Each successful unordered A has one unordered K_c, k!c! orderings, and product_x f(x) representation selections per ordering. The inverse representation weight cancels that last factor exactly once. No extra p!, cover-count divisor, or minimum-cover component bound belongs here. H_p is the previously justified event with specified predetermined parameters, not an intersection over all conceivable singleton menus.

Combining graph sparsity with the representation bound and the crude coordinate count leaves an upper expression with logarithm p(log100-o(1))+O(k log p). After clipping at one it gives no probability gain. Counting the rare compatible graphs and their inverse weights jointly, with canonicality and H_p retained, remains the missing theorem. Exact identities and separate marginal estimates do not prove that joint bound.

## 4. Actual-budget integer completion and coordinate conditioning


The peeling reduction retains disjoint actual B_i, their union B, the remaining budget m=c-|B|, and H_B=G\(A+B). It does not give full pencils free of charge. For every y in H_B, its available neighbourhood inside V=G\B still has exactly k elements. Thus the displayed binary cover/lightness system is an exact original-event reformulation after allowing the actual peeling data; it is not already a relaxed solution.

For uniform m-subsets S of an n-set V, conditional on P subset S and Q disjoint from S, the occupancy mean of a k-neighbourhood is exactly

u+(m-a)(k-u-v)/(n-a-b),

with a=|P|,b=|Q|,u=|P intersect N|,v=|Q intersect N|. Under the stated k<=m and degree restrictions, every cylinder of degree at most r has mean at least m(k-r)/(n-r). A direct concave quadratic gives this lower bound, attained by excluding r neighbours. If n>=m+k, the convex quadratic gives the sharp upper bound r+(m-r)(k-r)/(n-r), attained by including r neighbours.

Consequently the genuine uniform-subset moments satisfy every cylinder-multiplied covering inequality when (m-1)r<=mk-n; they also satisfy lifted lightness when the stated upper bound is at most h-1. The budget, Boolean and box constraints hold pointwise. Multipliers have degree at most r and constraint products use moments through r+1; no ambiguous hierarchy-level label is used.

At B empty, covering constraints admit r=(0.99+o(1))k. With |B|/k->beta<99 and h~delta k, both cover and lightness constraints admit any fixed fraction alpha<min(1-1/(100-beta),delta) of k coordinates. This is uniform in the actual adaptive B. Exact-cardinality moment feasibility does not assert that a light integral completion can be padded while retaining lightness.

The bounded-coordinate corollary is legitimate: a nonnegative test of at most r coordinates is a nonnegative combination of cylinders, and an adaptive depth-r coordinate-query tree has cylinder leaves. Choosing the tested target from the same leaf preserves the expectation bound. Conditioning on all of S or on global coverage is outside this statement.

These moments need not be supported on any feasible covers. The finite p=19, A={0,1,2,4}, m=6, r=1 diagnostic has minimum residual one while every degree-one lifted cover inequality passes. This is an actual prime-group separation for that six-centre system, not a counterexample at coefficient100. General nonlinear multipliers, a stronger cover-conditioned argument, or other proof systems are not excluded.

## 5. Adaptive bounded-score flux: the omitted term is now explicit


For an arbitrary deterministic exactly-m selector T(A), use H_q=p^(-1)sum_x q^f and the one-A-point exchange A to A'. The flux

D=E[H_q(A',T(A'))-H_q(A',T(A))]

compares both selectors on the same new A'. Stationarity cancels D against the frozen-selector drift; it does not set D to zero. Conditional on multiplicity n, the exact birth and death probabilities are (k-n)(m-n)/[k(p-k)] and n(p-k-m+n)/[k(p-k)]. Their substitution gives the correct identity and sign:

(1-q)M2+[p-(1-q)(k+m)]M-qkmF=-qk(p-k)D/(1-q).

Here F=E q^Z, M=E Zq^Z, M2=E Z^2q^Z for the real adaptive convolution at a uniform target. The resulting score identity retains all finite-population terms.

Since E Z=lambda=km/p exactly, decreasing covariance gives M<=lambda F and Jensen gives F>=q^lambda. The finite correction has the declared nonnegative sign and upper bound. At m=c and fixed q<1/100, a sufficiently small negative scaled flux, in particular liminf kD>=0 for a canonical score minimizer, would force a positive linear-p expected score and hence whp noncoverage by concentration. **No required flux bound is proved.** The unconditional lower bound D>=-(1-q)/k leaves a negative order-one normalized-score term and is far too weak.

The score minimizer here is exactly-c. A cover at at most c can be padded to an exactly-c cover with nonpositive score; this proves event inclusion without asserting score monotonicity. The sandwich R_c-q^2p<=B_q^=<=R_c follows by taking both minima over exactly-c sets, since the residual minimum can be padded. Its c(1+q^2) exchange constant is valid.

The finite negative-flux example is correct: at p=5,k=2,m=3,q=1/2 the canonical score minimizer has F=9/20,M=1/2,M2=3/5,D=-1/30 and normalized score -1/20. Thus discarding or reversing D is not harmless. This finite example does not refute the proposed asymptotic premise.

The weak-limit interpretation is correctly qualified. Bounded q^n,nq^n,n^2q^n permit passage to the limit, and the mean of a limit is at most C. Drift-free compound-Poisson limits have nonnegative scaled flux; zero-free limits have strictly negative scaled flux for q<1/C. No theorem says all adaptive additive profiles have either prescribed law. A zero-free random-site limit can still conceal p^(3/4) holes, so zero density is not exact covering or a sufficient negative estimate at the concentration scale.

## 7. Final original gap, without promoting sufficient conditions

Put mu_m=E R_m. The strongest unrestricted lower bound obtained at c remains zero. The universal integer greedy upper bound is

0<=R_c(A)<=g_c=(exp(-100)+o(1))p.

This interval leaves both answers possible. The following are precise sufficient missing statements:

1. **Negative route:** mu_c>=a c sqrt(k) for fixed a>0 along unbounded primes. The sharpened tail would imply success probability at most exp(-a^2/2)<1 on that subsequence. This is sufficient, not necessary for a negative answer.
2. **Positive mean routes:** mu_(33k)=o(p^(5/6)) or mu_(49k)=o(p^(3/4)). Either would combine with exact-budget amplification and repair to prove the original affirmative limit. No estimate at c is automatically transferable to these smaller budgets.
3. **Positive probability route:** a 33k-centre near-cover with o(p^(5/6)) holes on an event of probability exp[-o(p^(1/6))]. The new theorem would amplify it to an exact-cap whp cover; the requisite event is not constructed.
4. **Adaptive score route:** a sufficient one-sided bound on the canonical selector's exchange flux or on its expected bounded score. Fixed-candidate hypergeometric laws and drift-free clustered-law positivity do not establish that bound.
5. **Actual-additive counting or completion route:** a strict deficit in the normalized canonical weighted graph count on a legitimate typical event, or a real infeasibility/construction theorem for the actual-budget residual integer system. Exact normalization and the coordinate-conditioned relaxation do not prove either.

The first three are concrete sufficient estimates, not equivalent reformulations of each other or of the yes/no problem. The canonical count and actual integral system are exact formulations whose unproved quantitative content remains the original global dependence problem. No union over families chosen after A, no untransferred Bernoulli model, no independent-edge substitution, and no rounding error is accepted as a way around it.

**Final disposition: accept the scoped partial results and exact diagnostics; retain UNSOLVED after exactly five shared substantive passes. No sixth pass is authorized or performed.**

