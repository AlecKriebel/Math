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

The implementation uses the equivalent bridge-to-nearest-gap-of-at-least-equal-size formula. It was compared exactly with all gap permutations for 1,536 rational examples, including equal-size ties. Free-operator matrices recover [-2,2] for nine periods. Separate exact substitution-word matrix products verify 120 trace-recursion identities and their invariants. These validate finite routines, not the spectral conjecture.

### Why geometric convergence alone is inadequate

Let C be the middle-third Cantor set and, for N>=2, let

`K_N=union_(j=0)^N (j/N + N^(-2)*C)`.

These compact Cantor sets converge to [0,1] in Hausdorff distance. The first inter-cluster gap has length `1/N-1/N^2`; its left bridge has length at most `1/N^2` under every presentation. Thus

`tau(K_N)<=1/(N-1)->0`.

Hausdorff proximity to a filled interval therefore gives no lower control on thickness. This abstract construction is not a spectral counterexample. The finite calculation route requires a verified infinite-generation thickness enclosure or a monotonicity theorem uniform in period, neither of which was obtained.

## 6. Route 5: finite-gap perturbation and the uniformity barrier

### Conditional finite-gap lemma

Let I_t=[a(t),b(t)] and let a fixed finite set of gaps G_i(t)=(u_i(t),v_i(t)) have endpoints extending C1 to t=0. Suppose:

1. a(0)<b(0), and each gap collapses to a distinct interior point c_i;
2. each gap length g_i(t) satisfies g_i(0)=0 and g_i'(0)>0;
3. the gaps remain disjoint for sufficiently small positive t.

Then the finite-gap quantity

`Phi(I_t minus union_i G_i(t))`

is strictly decreasing on some interval (0,delta), where delta may depend on this finite gap collection.

**Proof.** Fix one of the finitely many gap orders and one endpoint. Its bridge length B(t) is C1 and B(0)>0 because the collapsed gap centers are distinct and interior. With g(t) the current gap length, the derivative of B/g has numerator `B'(t)g(t)-B(t)g'(t)`, which tends to `-B(0)g'(0)<0`. Every ratio is therefore decreasing on a sufficiently small interval. There are finitely many ratios and orders, so a common delta works. Finite minima and finite maxima of strictly decreasing functions are strictly decreasing. The definition of Phi completes the proof.

Filling all but finitely many bounded gaps of a Cantor set, while preserving its hull, cannot decrease thickness: restrict any original presentation to the retained gaps. Removing fewer earlier gaps only enlarges bridges, and taking the minimum over fewer endpoints only raises its lower bound. Taking the supremum over presentations yields the claim.

This suggests finite-gap upper comparisons, but does not prove the target. The lemma is conditional; no claim is made here that all its C1-at-zero hypotheses have been verified for the chosen Fibonacci endpoint families. More importantly, a delta valid for each fixed finite collection need not have a positive lower bound as the number or generation of gaps increases. Finite upper bounds alone also do not establish equality with infinite-spectrum thickness. Positive-coupling global monotonicity requires substantially more.

A sufficient, presently unproved, comparison would transport every gap presentation between two couplings and show every transported bridge/gap ratio is nonincreasing. Taking infima and suprema would then preserve the inequality. Existing bounded-distortion estimates provide magnitude comparisons, not this parameter-order property.

## 7. Disposition

**unsolved, 5/5.** The strongest model-specific conclusion retained is the already-published weak-coupling order law. The additional rigorous statements here are elementary general lemmas and countercontrols, with no novelty claim. No counterexample to Fibonacci spectral-thickness monotonicity was found. The exact remaining gap is a coupling comparison for the infimum over all spectral gap scales, or a certified pair of couplings reversing that comparison. Further independent review may test this packet, but it is not a sixth proof-search route.
