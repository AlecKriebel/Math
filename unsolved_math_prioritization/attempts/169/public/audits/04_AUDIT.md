# Stage 4 independent final audit

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 4.

## Decision and scope

**The four mathematical reports are accepted as partial results. The original covering question remains unresolved.**

The model is unchanged: p tends to infinity through primes, k=floor(sqrt(p)), A is a uniform k-subset of G=Z/pZ, c=floor(100 sqrt(p)), and T may depend arbitrarily on all of A. Success is the existence of T with |T|<=c and A+T=G. An affirmative result must make this probability tend to one along all primes. A negative result needs a fixed positive failure probability along an unbounded prime subsequence. Neither has been established here.

The results use the original cyclic group and actual additive convolution. None substitutes an independent-edge covering model, a nonprime product group, a Bernoulli A without transfer, or a restricted choice rule for T. Statements at 49k and 33k are explicitly smaller-budget sufficient hypotheses; they are not silently identified with estimates at c. Every use of an asymptotic fixed-R statement keeps R independent of p.

The earlier residual concentration bound is retained with its audited, conservative constant:

Pr(R_m <= E R_m-u), Pr(R_m >= E R_m+u) <= exp[-u^2/(8km^2)],

where R_m(A)=min_{|T|<=m}|G\(A+T)|. Swapping one A-point changes every fixed-T residual by at most 2m, taking minima preserves this common Lipschitz bound, and the without-replacement exposure coupling gives the displayed Azuma bound. It requires no union bound over T. In particular,

Pr(R_c=0) <= exp[-(E R_c)^2/(8kc^2)].

Consequently E R_c>=a c sqrt(k), for fixed a>0 along unbounded primes, is a sufficient negative bridge. It is not a necessary condition for a negative answer and has not been proved. Its scale is p^(3/4), not p. The bound does not give a positive mean merely because each fixed candidate has many expected holes.

## 1. Collective amplification and exact probability bridges


### The deterministic inequality is fully adaptive

For optimizing centre sets at budgets m,n, write U,V for their hole sets. Adding a shift d of the second centre set leaves exactly U intersect (V+d) uncovered. The exact identity

sum_d |U intersect (V+d)|=|U||V|

therefore proves

R_(m+n) <= floor(R_m R_n/p).

The same A occurs in both near-covers. Independence of A or of the two optimizers is neither used nor created by this averaging. The shift and both optimizers may depend arbitrarily on A. Duplicated centres reduce the cost and cause no problem.

Induction gives R_(rm)<=floor(R_m^r/p^(r-1)). Adding one centre x-a_0 for each remaining hole x, for any fixed a_0 in the nonempty A, then gives the exact complete-cover construction

tau(A) <= rm+floor(R_m(A)^r/p^(r-1)).

This is an unrestricted deterministic repair statement, not merely a near-cover estimate.

### Integer slack and probability direction

Let b=c-rm>=0. Failure tau>c implies floor(R_m^r/p^(r-1))>=b+1, hence

R_m >= [(b+1)p^(r-1)]^(1/r).

Markov gives the report's exact bound by E R_m divided by this threshold, capped at one. The b+1 is necessary and correctly retained. In particular, 100k<=c, so:

- m=49k, r=2 leaves b>=2k and failure probability at most E R_(49k)/sqrt((2k+1)p). Thus E R_(49k)=o(p^(3/4)) would prove the affirmative target.
- m=33k, r=3 leaves b>=k and failure probability at most E R_(33k)/[(k+1)p^2]^(1/3). Thus E R_(33k)=o(p^(5/6)) would suffice.
- The stronger 33k hypothesis E R_(33k)=O(p^(3/4)) gives O(p^(-1/12)) by Markov. Its repair threshold is of order p^(5/6), so the earlier upper-tail concentration improves this conditional rate to exp[-Omega(p^(1/6))]. The exponent follows from B^2/(km^2) of order p^(1/6); no unconditional rate is claimed.
- For fixed r and rm<=(100-eta)k with fixed eta>0, the general sufficient mean scale is o(p^(1-1/(2r))). The margin is preserved rather than replacing the cap by an uncontrolled coefficient-100 asymptotic.

### Interpolation restrictions are substantive

Uniform-size coupling yields 0<=mu(a,m)-mu(a+s,m)<=sm; deleting s centres yields 0<=mu(a,m)-mu(a,m+s)<=sa. These are valid with arbitrary optimizer changes, but changing the budget by Theta(k) costs O(p), too much for a p^(3/4) bridge.

Taking expectations of amplification yields E[R_m R_n]/p, not (E R_m)(E R_n)/p. The finite p=11 diagnostic has E R_4=2/3 and E R_4^2=2/3>(2/3)^2. This refutes product replacement in that argument; it does not refute mean submultiplicativity as a separately proved possibility.

The p=7 optimized-coverage values 4,5,5,7 for {0,1}, {0,1,3}, {0,1,5}, {0,1,3,5} verify failure of pointwise submodularity. Finite residual profiles also contain genuine failures of pointwise budget convexity. Neither refutes an averaged inequality not derived from these pointwise premises. The exact finite mean searches below found no counterexample to several averaged properties and correctly make no theorem from that absence.

The unconditional target-budget estimate remains only

0<=R_c(A)<=floor[p binom(p-k,c)/binom(p,c)]=(exp(-100)+o(1))p

for all sufficiently large p. It follows by averaging over uniform c-centre sets for each fixed A. Fixed-number amplification of a constant-density-hole bound still leaves a constant-density-hole bound. The positive and negative mean hypotheses above remain unproved.

## 2. Fixed-R budgeted residual capacity and the fractional optimum


### Uniform sparse-graph zero probability

The graph lemma is correct for simple graphs with p+O(1) vertices, bounded maximum degree, rp+O(1) edges, and a uniform k+O(1) vertex sample, for fixed r and all uniform constants. The jth factorial moment of occupied edges has disjoint-edge contribution r^j+o(1). A union of overlapping edges with v vertices and a components has O_j(p^a) realizations and sampling probability O_j(p^(-v/2)). At least one component then has at least three vertices, so a-v/2<=-1/2. Thus the overlapping contribution tends uniformly to zero.

Fixed-order Bonferroni bounds, followed by taking their truncation order to infinity, give zero-edge probability e^(-r)+o(1). This uses the actual fixed-size sample. It does not assume independent edge indicators or a uniform approximation when r grows.

### The endpoint Lipschitz argument avoids a genuine extension pitfall

The difference and sum codegrees are simultaneously O(log p/log log p) on a shared Good event with failure p^(-9+o(1)). For a nonzero difference the graph is a p-cycle; 3m occupied edges contain an m-edge matching. For a sum, unordered off-diagonal pairs are already a matching and there is at most one diagonal contribution. The matching union bounds give (e/m)^m per parameter and the stated shared failure probability with m=ceil(10log p/log log p).

For F_Z(A)=#{a in A:a-z notin A-A for all z in Z}, the condition A intersect Z nonempty forces F_Z=0. On the slice avoiding Z, compare any two Good endpoint sets A,A' directly. A changed witness a+d=b+z uses a removed or inserted endpoint y. If b=y, the sum codegree bounds the number of candidates; if d=y, the difference codegree applies because z-y is nonzero. Adding the contribution of noncommon candidates proves

|F_Z(A)-F_Z(A')|<=(1+4|Z|L_p)|A\A'|.

The proof does not assume that a shortest swap path remains Good. This direct all-endpoint bound is sufficient for the clipped McShane extension to the entire avoiding-Z slice.

### Conditional means, exceptions, and the single shared Good event

Conditional on a belonging to A and A avoiding Z, the forbidden differences a-z are nonzero and distinct up to sign except for O_R(1) candidates satisfying 2a=z_i+z_j. For a nonexceptional a, the forbidden graph is simple 2r-regular. Its r additional neighbours 2a-Z must be excluded; that costs only 1-O_R(k/p). After this exclusion, the remaining uniform k-1 sample lives on p-2r-1 vertices and the graph retains rp-O_R(1) edges. The graph lemma yields the uniform conditional mean (e^(-r)+o(1))k. The exceptional candidates contribute only O_R(k/p).

The extension is D_p=1+4RL_p Lipschitz and lies in [0,k]. Its mean differs from the original mean by at most 2k p^(-9+o(1)). The without-replacement tail at t=k^(3/4) has exponent of order sqrt(k)/L_p^2. This beats the log of the O_R(p^R) menu for every fixed R. The extension tails are union-bounded, while the one shared Good-complement probability is added only once. Multiplying the latter by p^R would not justify arbitrary fixed R and is correctly avoided.

Changing variables Z=X-s now proves, simultaneously over |X|=r<=R and all s,

|(A+s) intersect H_X| = 0 for s in X-A,
|(A+s) intersect H_X| = (e^(-r)+o(1))k otherwise,

where H_X=G\(X+A-A). Since e^(-R)k diverges, the asserted bounded-envelope inverse-containment corollary follows. It does not apply to unrestricted large envelopes.

### Residual size and actual budget

The analogous forbidden graph for a target y has the same e^(-r) limit outside O_R(1) exceptional y. A swap changes X+A-A at at most 4rk positions. The tail at t=p k^(-1/4) has exponent of order sqrt(k), which again beats R log p. Thus |H_X|=(e^(-r)+o(1))p uniformly for fixed R.

Every centre inside X-A contributes zero to H_X. Summing the individual capacities of s centres outside this envelope bounds their union from above in the valid direction. Therefore a full cover, or any o(p)-hole cover, requires at least (1-o(1))p/k=(1-o(1))k such outside centres. In particular, spending at least (99+eta)k centres inside a bounded pencil envelope leaves a positive-density hole set at cap c, for fixed eta>0 and all sufficiently large p. This counts actual centres and does not replace retained blocks by free full pencils.

### Sharp fractional limitation, including lightness

For any A and actual retained B, weights w_t=1/k on G\B and zero on B have convolution

sum_t w_t 1_A(y-t)=1-(1/k)(1_A*1_B)(y).

It lies in [0,1] everywhere and equals one on H_B=G\(A+B). Thus it satisfies the box bounds and every stated global lightness constraint with integer threshold h>=2. Its exact cost is (p-|B|)/k.

If B subset X-A with fixed |X|<=R and |B|<=c, then H_X subset H_B. Summing the fractional cover constraint over H_X and applying the capacity upper bound forces cost at least (1-o(1))p/k. Combined with the explicit upper bound this gives the claimed first-order optimum (1+o(1))k, uniformly over the actual B. Adding the retained cost stays within c whenever

|B| <= (kc-p)/(k-1)=99k+O(1).

This is a true obstruction to proving a larger cost from that fractional relaxation. It neither supplies an integral cover nor a rounding procedure. Candidates with several k-scale blocks outside every bounded pencil union remain uncontrolled. The fixed-R theorem does not establish the full-budget mean lower bound.

## 3. Bounded certificate, compound-Poisson scope, and clipping


### The bounded score preserves the actual candidate domain

For 0<q<=1/2, g_q(n)=(1-n)q^n equals one at zero and lies in [-q^2,0] at positive integers. The successive ratio of (n-1)q^n is nq/(n-1)<=1 for n>=2. Therefore the pointwise sandwich and its minimization over the same at-most-c domain are valid:

R_c-q^2p <= B_q <= R_c,
B_q=min_{|T|<=c} sum_x g_q((1_A*1_T)(x)).

The observable need not be monotone when centres are added. The at-most-c minimum is not identified with the exactly-c score minimum. Cover existence implies B_q<=0, and when q^2p<1 the converse follows from integer-valued R_c. These facts concern the original convolution rather than an assumed realizable clipped profile.

The increment range [-1,q^2] gives fixed-T exchange bound |T|(1+q^2), and taking minima preserves c(1+q^2). The stated Azuma inequality, with denominator 2kc^2(1+q^2)^2, follows. A positive expectation of order c sqrt(k) would therefore provide the required negative subsequence conclusion. This expectation has not been established.

The smoothing error is at most q^2p. Choosing q=o(p^(-1/8)) makes it o(c sqrt(k)); the example q=p^(-1/6) is correct. At that scale the new mean problem is quantitatively equivalent to the old one to the precision relevant here. A fixed q has order-p comparison error and cannot transfer a merely p^(3/4) residual lower bound by this sandwich alone.

### Fixed-candidate and clustered-law means are not adaptive theorems

The hypergeometric size-bias identity gives exactly

E_A G_q(A,T)=p[H(p,k,m;q)-(km/p)q H(p-1,k-1,m-1;q)]

for every fixed m-set T. It also holds with A fixed and T uniformly sampled. Its fixed-q Poisson limit is exp[-C(1-q)](1-Cq) after division by p when m/sqrt(p)->C. It is not a lower bound on E min_T G_q.

For a drift-free compound-Poisson law with jump intensities beta_j and sum j beta_j<=100, the generating function gives

E g_q(Y)=F(q)[1-sum_j j beta_j q^j] >= (1-100q)e^(-100)>0

when 0<q<1/100. This includes parity and other clustered laws, and mixtures whose conditional means obey the same bound. Deterministic positive drift destroys the conclusion; an arbitrary mixture with only an unconditional mean bound is not covered. No claim is made that every adaptive additive convolution satisfies this law or a sufficient one-sided approximation to it.

### Literal clipping fails the mass-divisibility test

On the exact-size high-probability codegree event, start with the pencil -A and pad outside it to exactly c centres. The hypergeometric tail and union bound give a padding for which f(0)=k and every nonzero value is at most M_p=4ceil(4log p/log log p)<k. The padding avoids all centres covering zero, so the value there is exactly k.

Clipping f at M_p changes only this value. Its total becomes kc-k+M_p, not divisible by k. Every convolution 1_A*1_S, even with nonnegative integral centre multiplicities, has total divisible by k. Thus literal clipping need not remain feasible for any centre set. The construction is at the exact cap but is not asserted to be a cover. Applying a bounded observable to f itself remains valid.

### Support-preserving pencil deletion has a different obstruction

For nonzero d, r_A(d)=1 means exactly one occupied edge in its p-cycle. Selecting that edge and excluding its two external neighbours leaves a path on p-4 vertices. Choosing k-2 independent vertices there gives precisely

Pr(r_A(d)=1)=p binom(p-k-1,k-2)/binom(p,k).

For k~sqrt(p), the unique-difference mean is (e^(-1)+o(1))p. Its 4k exchange bound gives the stated exponentially small lower tail at p/(2e). Every unique difference is private to its representing pencil centre; each centre owns at most k such targets. A subfamily of -A preserving all of A-A must therefore retain at least k/(2e) centres, all covering zero. It cannot reduce the maximum convolution to o(k).

This only rules out support-preserving subfamily deletion. New replacement centres, changed covered sets, redistribution, and other integral constructions remain possible. Neither clipping obstruction is a counterexample to the original random-covering assertion.

## 4. Actual-additive partition functions and normalized cycle counting


### Full additive hierarchy and exact-size Laplace bound

For fixed A, expansion over subsets of the actual hole set proves the polynomial identity

sum_{|T|=t} z^(U(A,T)) = sum_{X subset G}(z-1)^|X| binom(p-|X-A|,t).

It holds for complex z, with the stated zero convention on binomial coefficients. Its z=0 specialization and factorial-moment identity are exact. High-order cancellation cannot be replaced by absolute-value bounds without loss. Annealed commutativity of F_t and F_k is legitimate; corresponding symmetry for optimum means or expected log partition functions is not implied.

For Bernoulli centres of density rho, every coordinate belongs to exactly k hole windows. The relative-entropy chain-rule inequality kD(Q||mu)>=sum_x D(Q_(x-A)||mu_(x-A)), combined with the finite variational identity, gives

E exp(-beta U) <= [1-u+u exp(-beta k)]^(p/k), u=(1-rho)^k.

This is a read-k bound, not independence of holes. Conditioning at rho=t/p costs exactly 1/b_t, where b_t is the binomial probability of exactly t centres. The transfer is rigorous and uniform in A.

At t=c, the maximum log suppression from this bound is only b_100 k+O(log k), while log binom(p,c)=(100+o(1))k log k. The exact min-versus-partition inequalities have the signs stated in the report and therefore supply only the trivial residual lower bound from this estimate. A sufficiently stronger expected log-partition bound would imply the negative mean bridge, but is not proved. The present estimate also does not produce either smaller-budget positive mean bound.

### The graph retains actual target equations

Every representation selection of a genuine cover yields a simple bipartite p-edge subgraph of K_(k,t) with a bijection from edges to target labels in G. An edge is an actual equation a_i+t_j=ell(i,j). Conversely, distinct-coordinate solutions of a bijectively labelled graph are covers with one representation choice per target.

If v=k+t and h counts all components, including isolated vertices, the coefficient rank is v-h. Negating right variables gives the incidence matrix of the graph. A spanning forest determines variables from h roots, while the p-v+h nonforest edges impose independent cycle-label equations. A fixed labelling therefore has either zero solutions or p^h solutions before distinctness and typicality restrictions. These label constraints cannot be discarded as though low variable rank made them automatic.

For inclusion-minimal T, each centre has a private target, so every representation selection uses every right vertex. Every component then contains a left vertex, and p<=sum_i a_i b_i<=(k-h+1)t gives h<=k+1-ceil(p/t). This does not apply without minimality. It leaves order-k roots at the cap, with graph and label advice still unpaid, and is not the missing sublinear-advice compression theorem.

### Representation multiplicity and canonicality are normalized once

The true autocorrelation identity gives E_x f(x)^2<=[kt+L t(t-1)]/p. For a cover with lambda=kt/p>1, applying Paley-Zygmund to f-1 and using E(f-1)^2<=E f^2 gives the report's lower bound

log product_x f(x) >= p (lambda-1)^2 log((lambda+1)/2) / [4(lambda+L t(t-1)/p)].

At the cap this is Omega(p/L) under the proved codegree condition. It counts representation selections of each fixed cover, not different centre sets. Its general t-dependent form is correctly kept because a canonical minimum cover need not have cap size.

For a canonical minimum selector K(A), the report's weighted sum over t,J,ell and ordered solutions is exactly the H_p-restricted success probability after dividing by binom(p,k)k! and by t! in each t summand, with each solution weighted by 1/product_x f(x). For each successful unordered A there is one unordered K(A), k!t! orderings, and product_x f(x) representation selections per ordering. These factors cancel once. No additional cover-count division is permitted after canonical selection. If all minimal covers were counted instead, that different multiplicity would need its own normalization.

H_p is the specified prior finite intersection of proved typicality and predetermined decoder-family exclusions. It is not an intersection over all possible singleton codebooks. H_p and canonicality remain inside the exact count; dropping them in an upper estimate can reintroduce known exceptional cores.

The elementary cycle-consistent bound is only p^v per graph, and there are at most binom(kt,p) graphs. At t~100k the graph entropy has positive order p, while the representation lower bound removes only order p/L in this loose estimate. Thus it does not control the normalized success probability. No unproved permutation-label rarity, canonical counting bound, or adaptive expectation estimate is treated as established.

## 6. Accepted frontier and unresolved work

The following conclusions are accepted:

1. Same-A translation amplification and exact-budget repair give genuine unrestricted conditional positive bridges at 49k and 33k.
2. Fixed-R canonical residuals have uniform first-order size and per-centre capacity; every near-cover needs roughly k centres outside any bounded pencil union.
3. The actual retained-B fractional relaxation has sharp cost roughly k, including the stated lightness constraints, and cannot itself yield a stronger integral obstruction.
4. A bounded one-sided convolution certificate has a valid adaptive concentration bridge and drift-free clustered-law positivity, with the requisite mean estimate still missing.
5. Typical-A literal clipping and support-preserving pencil deletion have precise factorization or indispensability obstructions; they do not rule out all replacement schemes.
6. Actual additive partition identities, cycle consistency, representation multiplicity, and canonical normalization are exact, but their unrestricted enumeration is uncontrolled.

The central alternatives remain: prove E R_c>=a c sqrt(k) along unbounded primes; prove a sufficient smaller-budget upper mean and apply amplification; prove an adequate adaptive bounded-observable estimate; or establish a new normalized actual-additive counting or integral-completion theorem. None is supplied by this audit. There is no resolution claim and no automatic promotion of the problem's status.

