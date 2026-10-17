# Final accepted-result synthesis: Green Problem 39

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


**Disposition: UNSOLVED after five shared substantive passes.** No complete proof or verified counterexample to the original statement was obtained. The program stops here; verification and packaging add no mathematical pass.

## The original question

For primes p, choose A uniformly among the k=floor(sqrt(p))-element subsets of Z/pZ. Does the probability that some A-dependent set T with |T|<=c=floor(100sqrt(p)) satisfies A+T=Z/pZ tend to one? A negative answer must give a fixed positive failure probability along arbitrarily large primes. A rare exceptional A, failure of a particular algorithm, or a near-cover with unbudgeted repair is insufficient.

This is the operational exact-rounding interpretation of [Ben Green, *100 Open Problems*, Problem 39](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf#page=20). The inspected primary still states the question. Related results in [Bollobas--Janson--Riordan](https://arxiv.org/pdf/0910.3815v2) concern fixed k, a near-linear group-size regime, or a logarithmic universal upper bound; those hypotheses do not settle k~sqrt(p). This source review is bounded and dated, not an exhaustive assertion about all literature.

## What the five passes establish

- Several tempting construction classes and proof shortcuts genuinely fail: fixed low-entropy menus, bounded-doubling envelopes, bounded elementwise-map constructions and specified sublinear-seed decoders cannot produce typical covers. Their exclusions do not cover every unrestricted adaptive T.
- The optimum residual R_m(A)=min_(|T|<=m)|G\(A+T)| is m-Lipschitz under an A-point swap. Its uniform-subset tails are bounded by exp[-u²/(2km²)], even though its optimizer may change arbitrarily.
- Near-covers can be combined without assuming independence: R_(m+n)<=floor(R_m R_n/p). Iteration and one-centre-per-hole repair give tau(A)<=rm+floor(R_m^r/p^(r-1)), with the original budget and integer slack preserved.
- Actual heavy-block peeling, bounded-pencil residual capacities and the fractional-completion calculation are valid. The final coordinate-conditioning theorem shows that a real uniform-centre moment law can satisfy all specified lifted cover/lightness constraints through a positive fraction of k coordinates while admitting no integer cover in a finite example.
- The final adaptive bounded-score exchange identity keeps an explicit reoptimization flux. Its sign is not supplied by stationarity. A sufficient one-sided flux bound would imply noncoverage, but that bound is unproved.
- Representation graphs retain the real sum equations. Exact Fourier and collision-partition counts, an exponential graph-sparsity theorem and a stronger cover-conditioned representation bound are proved. Canonical counting divides representation multiplicity exactly once. The available estimates still yield only the trivial success-probability bound one.

Exact finite enumerations, independent implementations, optimization-mode replays and corrupted-certificate tests validate the stated identities and examples. They do not establish the asymptotic probability. The coefficient-100 cap is already vacuous at the small diagnostic primes.

## The precise unresolved estimates

At the original cap, the established unrestricted range is still

0<=R_c(A)<=g_c=(exp(-100)+o(1))p,

where g_c is the verified rounded greedy bound. No positive lower bound of the required scale, and no sufficiently small upper bound at a smaller budget, was proved.

Any one of the following new inputs would suffice, but none is established:

1. A negative-route bound E R_c>=a c sqrt(k), for fixed a>0 along unbounded primes. It would force success probability at most exp(-a²/2)<1 there.
2. A positive-route bound E R_(33k)=o(p^(5/6)) or E R_(49k)=o(p^(3/4)). Exact amplification and repair would then give whp covers within c.
3. The final probability bridge: a 33k-centre near-cover leaving o(p^(5/6)) holes on an event of probability at least exp[-o(p^(1/6))]. This alone would amplify to exact-cap success with failure exp[-Omega(p^(1/6))]. No such initial event is constructed.
4. A sufficiently strong adaptive-score flux bound, a strict deficit in the correctly normalized canonical additive count, or a genuine integral-completion theorem retaining actual blocks and budget.

The core gap is control of the globally optimized, fully A-dependent translating set. Fixed-candidate statistics, exact reformulations and conditional theorems do not fill it. The accepted outcome is substantive partial progress with the original question unresolved.

