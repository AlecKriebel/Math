# Exact scope, partial arguments, and remaining gap

## 1. Target and known component

Let alpha=(sqrt(5)-1)/2. On l2(Z), set

`(H_(lambda,omega) u)(n) = u(n+1)+u(n-1)+lambda*1_[1-alpha,1)(n*alpha+omega mod 1)*u(n)`.

Here lambda>0 and omega is a phase. Its phase-independent spectrum is denoted Sigma_lambda. The target is Newhouse thickness of this **one-dimensional diagonal discrete model**, not an off-diagonal model, a continuum operator, or thickness of a two-dimensional sum spectrum.

For a compact set K with hull I, a presentation is an ordering of its bounded complementary gaps. At a gap endpoint, remove that gap and all earlier gaps; divide the length of the adjacent surviving component by the gap length. Thickness is the supremum over presentations of the infimum of these ratios. For a finite union of nondegenerate closed intervals, we use the identical finite-gap definition and write Phi(K), distinguishing this diagnostic from thickness of an infinite Cantor spectrum.

The conjectural monotonicity assertion is

`0 < lambda_1 < lambda_2 => tau(Sigma_lambda_2) <= tau(Sigma_lambda_1)`.

Strict decrease would be stronger; even this weak inequality is not established here. The lambda=0 interval is a limiting case, not part of the positive-coupling assertion.

The original source is Embree's contribution on printed p.164 of the 2011 Oberwolfach report [S1]. Damanik--Gorodetski [S2, Theorem 1.2, preprint p.4] proves, for sufficiently small positive lambda,

`c/lambda <= tau(Sigma_lambda) <= C/lambda`, with fixed 0<c<=C.

This establishes the order `Theta(1/lambda)`. It does not state that `lambda*tau(Sigma_lambda)` has a limit or that this limit is one. Its distortion estimate [S2, Proposition 3.11] controls gap/bridge ratios by fixed multiplicative constants, not by a sign for their coupling derivative. These existing results are credited to their authors.

## 2. Route 1: asymptotic differentiation does not prove monotonicity

Even a genuine asymptotic equivalence is insufficient. For 0<t<1 define

`f(t)=1/t+sin(1/t^2)`.

It is positive and t*f(t)->1. However,

`f'(t)=-1/t^2-2*cos(1/t^2)/t^3`.

At `t_n=((2n+1)*pi)^(-1/2)`, this equals `(2-t_n)/t_n^3>0`. Thus f is not nonincreasing on any sufficiently small neighborhood of zero. This is an abstract inference counterexample, not a Fibonacci spectrum.

Consequently, differentiating an unquantified `Theta(1/lambda)` statement, or even a `~1/lambda` statement, is invalid. A derivative bound on the remainder is necessary for that route.

## 3. Route 2: operator order and endpoint motion

For lambda_2>lambda_1, `H_lambda_2-H_lambda_1` is a nonnegative multiplication operator. In finite periodic or antiperiodic matrices, ordered eigenvalues are nondecreasing. At a simple eigenvalue with normalized eigenvector u, the Hellmann--Feynman derivative is `sum(v_j*|u_j|^2)` with v_j in {0,1}; it lies in [0,1].

This does not control ratios of differences of eigenvalues. Explicitly, let

`A_t=diag(0,1+t,3,5)`, for 0<=t<=1/2.

Its derivative is positive semidefinite and all endpoint derivatives lie in [0,1]. Interpret its four ordered eigenvalues as the endpoints of

`K_t=[0,1+t] union [3,5]`.

There is one gap. Therefore

`Phi(K_t)=(1+t)/(2-t)`, with derivative `3/(2-t)^2>0`.

The ratio increases from 1/2 to 1. This does not realize K_t as a Fibonacci spectrum or as the spectrum of A_t; A_t's eigenvalues merely provide admissible ordered endpoint motions. It disproves the proposed deduction from endpoint ordering alone. The missing input is a model-specific inequality between bridge and gap derivatives.

## 4. Route 3: differentiated trace recursion

Use half traces with

`x_(-1)=1, x_0=E/2, x_1=(E-lambda)/2`,
`x_(n+1)=2*x_n*x_(n-1)-x_(n-2)`.

The invariant is `x_n^2+x_(n-1)^2+x_(n-2)^2-2*x_n*x_(n-1)*x_(n-2)=1+lambda^2/4`.

At fixed E, let d_n=partial_lambda x_n. Then

`d_(n+1)=2*(d_n*x_(n-1)+x_n*d_(n-1))-d_(n-2)`.

At E=0, lambda=1, the exact d_n for n=-1 through 6 are

`0, 0, -1/2, 0, 1, -3/2, -6, 23`.

Hence a uniform coordinatewise sign induction for raw traces fails. This energy is used only to disprove a global sign heuristic; it is not claimed to lie in Sigma_1. A cone argument restricted to the relevant invariant set is not ruled out, but no suitable cone controlling all bridge/gap derivatives was constructed. Fixed-energy trace derivatives also differ from derivatives along moving gap endpoints, another required step.

## 5. Route 4: periodic numerical approximants

With F_0=F_1=1, let q=F_k, p=F_(k-1), and

`v_n=lambda*(floor((n+1)*p/q)-floor(n*p/q))`, n=1,...,q.

We construct the real symmetric periodic and antiperiodic Jacobi matrices with these diagonal entries, nearest-neighbor entries 1, and corner entries +1 or -1. Sorting all 2q eigenvalues and pairing successive values produces the q spectral bands. Consecutive periods are merged to form the finite cover `A_(k,lambda)=sigma_(k,lambda) union sigma_(k+1,lambda)` [S3, Section 7.1].

The computation covers k=6,8,10,11 and lambda in {0.05,0.1,0.2,0.5,1,2,4,8,16}. No sampled increase of Phi(A_(k,lambda)) occurred for any fixed k. For example, at k=11 the scores for lambda=0.1,1,4 are approximately 20.701154, 1.445453 and 0.138878. These are **finite-approximation floating-point diagnostics**, not proven values or error bars for tau(Sigma_lambda). A tolerance of 1e-12 is used when merging bands. No continuum in coupling is certified.

### Finite-gap ordering lemma

For finitely many gaps, a nonincreasing-length presentation maximizes the minimum bridge/gap ratio. To prove it, exchange two adjacent removals whose lengths g<h are in the wrong order. If they lie in separate surviving components, nothing changes. Otherwise suppose the smaller gap lies left of the larger, and write the component as lengths A,g,M,h,C in spatial order. The old minimum is at most A/g, M/h, C/h. After exchanging the removals the four affected ratios are `(A+g+M)/h`, `C/h`, `A/g`, `M/g`; each is at least the old minimum because h>g. The reversed spatial order is identical. Repeated exchanges prove the assertion; equal-length ties do not change the optimal minimum.

### Blocker formula, including ties

The following formula applies both to a compact Cantor set with a nondegenerate bounded hull and to a finite union of nondegenerate intervals. For each bounded gap G of length g and each side, take the distance M from that endpoint to the nearest gap on that side whose length is at least g; if there is no such gap, use the hull boundary instead. Let S be the infimum of all M/g. Then the relevant thickness quantity equals S.

For the upper bound, fix any presentation and any candidate. A hull-boundary candidate bounds the corresponding bridge from above. Otherwise let H be the candidate's blocking gap, with length h>=g. If G is removed after H, G's bridge toward H has length at most M and denominator g. If H is removed after G, H's bridge toward G has length at most M and denominator h>=g. Thus some ratio in the presentation is at most M/g in either case. Its infimum is at most every candidate, hence at most S. Taking the supremum over presentations preserves this upper bound.

For the lower bound, enumerate gaps by nonincreasing length. Such an enumeration exists in a bounded hull because only finitely many disjoint gaps can have length at least any fixed positive number. Every gap already removed has length at least that of the current one. Consequently its bridges extend at least to the nearest qualifying blockers, so every presentation ratio is at least S. This proves equality.

At equal lengths, a tied blocker removed later can make an individual bridge longer than the formula's distance. The upper-bound argument uses the gap removed later to witness the candidate. Thus the formula describes the global infimum, not necessarily each individual bridge in a fixed tie order. In the adjacent-exchange proof above, when g=h both affected minima equal min(A,M,C)/g; ties preserve the optimum.

The implementation uses this blocker formula. It was compared exactly with all gap permutations for 1,536 rational examples, including equal-size ties. Free-operator matrices recover [-2,2] for nine periods in floating-point arithmetic; those nine checks are not exact or interval-certified. Separate exact substitution-word matrix products verify 120 trace-recursion identities and their invariants. These validate finite routines, not the spectral conjecture.

### Why geometric convergence alone is inadequate

Let C be the middle-third Cantor set and, for N>=2, let

`K_N=union_(j=0)^N (j/N + N^(-2)*C)`.

These compact Cantor sets converge to [0,1] in Hausdorff distance. The first inter-cluster gap has length `1/N-1/N^2`; its left bridge has length at most `1/N^2` under every presentation. Thus

`tau(K_N)<=1/(N-1)->0`.

Hausdorff proximity to a filled interval therefore gives no lower control on thickness. This abstract construction is not a spectral counterexample. The finite calculation route requires a verified infinite-generation thickness enclosure or a monotonicity theorem uniform in period, neither of which was obtained.

## 6. Route 5: finite-gap perturbation and the uniformity barrier

### Conditional finite-gap lemma

Let m>=1 be finite. Require all functions a,b,u_i,v_i, for 1<=i<=m, to be C1 on a one-sided neighborhood [0,epsilon) of zero. Write

`I_t=[a(t),b(t)]`, `G_i(t)=(u_i(t),v_i(t))`, and `g_i(t)=v_i(t)-u_i(t)`.

Assume:

1. a(0)<b(0), and u_i(0)=v_i(0)=c_i, where the c_i are pairwise distinct and strictly inside (a(0),b(0));
2. g_i'(0)>0 for every i;
3. for sufficiently small positive t the gaps lie inside I_t and are pairwise disjoint.

Then the finite-gap quantity

`Phi(I_t minus union_(i=1)^m G_i(t))`

is strictly decreasing on some interval (0,delta), where delta may depend on the full finite collection. Both hull endpoints are explicitly included in the C1 requirement. Nonemptiness is necessary: with no gaps, Phi(I_t)=infinity is constant.

**Proof.** The distinct collapsed centers fix the spatial order for sufficiently small t. For a fixed gap presentation and endpoint, the bridge length B(t) is a difference of two of the specified C1 endpoint functions, and B(0)>0. The positive initial derivative of its gap length g(t) ensures g(t)>0 for small positive t. The derivative of B/g has numerator B'g-Bg', which converges to -B(0)g'(0)<0. All 2m*m! endpoint/order ratios therefore strictly decrease on one common sufficiently small interval. A finite minimum of strictly decreasing functions strictly decreases: use a minimizer at the earlier argument. A finite maximum strictly decreases by using a maximizer at the later argument. Apply the minimum over endpoints and then the maximum over presentations to obtain the result.

Filling all but finitely many bounded gaps of a Cantor set, while preserving its hull, cannot decrease thickness: restrict any original presentation to the retained gaps. Removing fewer earlier gaps only enlarges bridges, and taking the minimum over fewer endpoints only raises its lower bound. Taking the supremum over presentations yields the claim.

### Exact exhaustion by true gaps

Let K be a compact Cantor set with its exact hull I. Let F_N be an increasing sequence of finite subsets of its actual bounded gaps, exhausting every such gap. Define

`K_N=I minus union_(G in F_N) G`.

Then `Phi(K_N)` is nonincreasing in N and converges to `tau(K)`.

**Proof.** The filling-gap comparison above gives Phi(K_N)>=tau(K) and monotonicity in N. Consider any candidate M/g in the blocker formula for K. Once its gap G and its blocking gap H, if there is one, have both entered F_N, this same candidate occurs for K_N. No gap of K_N can be a closer qualifying blocker, since all its gaps are gaps of K and H was chosen nearest there. A hull-boundary candidate likewise persists after G enters because the hull is unchanged. Therefore the limit of Phi(K_N) is at most each candidate M/g. Taking their infimum gives the upper bound tau(K), proving equality.

This is an elementary fixed-set identity, not an identification of the numerical periodic covers A_(k,lambda) with true-gap fillers. Their exact endpoints, hulls and removed gaps have not been shown to satisfy these hypotheses. It supplies no certified numerical error bound or coupling comparison.

### Uniformity remains missing

The finite-gap perturbation lemma is conditional; this investigation has not verified its complete C1-at-zero assumptions for the intended spectral endpoints and hull. Even if every finite collection satisfied them, its interval of decrease could shrink with the gap collection. For an explicit general control, the symmetric one-gap set in [-1,1] with gap length

`g_n(t)=t/(1+n^2*t^2)`, n>=3,

satisfies the corrected endpoint hypotheses, but its quantity is `1/t+n^2*t-1/2`. The derivative is negative for t<1/n and positive for t>1/n. Thus these qualitative hypotheses provide no common interval for the family. These are different one-gap sets, not truncations of one spectral Cantor family.

If exact true-gap truncations were all nonincreasing on one common coupling interval and exhausted the true gaps at each coupling, the identity above would pass nonincrease to their pointwise limit. No such common-interval comparison is established here. Strict decrease also need not survive an infinite limit. Global positive-coupling monotonicity needs still more than a local comparison at zero.

### Sufficient comparison with full presentation coverage

Fix 0<lambda_1<lambda_2. Suppose a bijection between their bounded spectral gaps, with a consistent correspondence of endpoints, induces a bijection between all gap presentations by transporting the ordered labels. Assume that for every presentation P at lambda_1 and every gap endpoint, its corresponding bridge/gap ratio in the transported presentation at lambda_2 is no larger.

Taking infima over corresponding endpoints yields a comparison for each presentation. Taking suprema, using surjectivity of the induced map onto all presentations at lambda_2, yields

`tau(Sigma_lambda_2)<=tau(Sigma_lambda_1)`.

This is a sufficient conditional criterion only; the required model-specific inequalities remain unproved. A transport that misses presentations at the second coupling would not suffice. Existing bounded-distortion magnitude estimates do not establish the assumed parameter-order property.

## 7. Disposition

**unsolved, 5/5.** The strongest model-specific conclusion retained is the already-published weak-coupling order law. The additional rigorous statements here are elementary general lemmas and countercontrols, with no novelty claim. No counterexample to Fibonacci spectral-thickness monotonicity was found. The exact remaining gap is a coupling comparison for the infimum over all spectral gap scales, or a certified pair of couplings reversing that comparison. Further independent review may test this packet, but it is not a sixth proof-search route.
