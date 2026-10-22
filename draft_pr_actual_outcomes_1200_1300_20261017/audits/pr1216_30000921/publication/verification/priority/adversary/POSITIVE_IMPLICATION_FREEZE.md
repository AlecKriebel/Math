# Frozen positive implication checkpoint

Freeze UTC: 2026-10-17T18:24:32.341602+00:00

Independence: I have not read priority/independent or the parent conclusions.

## Earlier theorem

Miika Nikula, *Frequent hypercyclicity of random entire functions for the differentiation operator*, arXiv:1209.6209v1 (posted 27 September 2012), Theorem 1 (PDF pp. 2–3): for IID complex coefficients X_n with full support in C and a mild tail bound, f(z)=sum X_n z^n/n! is almost surely entire and frequently hypercyclic for D. In particular standard circular complex Gaussian coefficients qualify. Local complete source was freshly retrieved from https://arxiv.org/pdf/1209.6209v1; read scope currently theorem, introduction and proof end, not full proof audit. Publisher version/date check remains pending.

## Checkable deterministic deduction

Use standard complex Gaussians of density pi^-1 exp(-|z|^2), so P(|X|<r)=1-exp(-r^2) <=r^2 and P(|X|>R)=exp(-R^2). Fix alpha=3/4. The sums of P(|X_n|<n^-alpha) and P(|X_n|>log(n+e)) converge. By first Borel–Cantelli, almost surely, eventually

    n^-3/4 <= |X_n| <= log(n+e).

Intersect this probability-one event with the probability-one FHC(D) event from Theorem 1. For ANY nonconstant p(z)=sum_{j=0}^d p_j z^j with p_d !=0 and n>=d,

    (p f)^(n)(0) = sum_{j=0}^d p_j (n)_j X_{n-j}.

The highest term has size >= |p_d|(n)_d (n-d)^-3/4. The sum of lower-degree terms is <= C_p n^(d-1) log(n+e). Therefore

    |(p f)^(n)(0)| >= c_p n^(d-3/4) - C_p n^(d-1)log(n+e) -> infinity.

The event was selected WITHOUT reference to p. Hence the conclusion holds simultaneously for EVERY nonconstant complex polynomial, without an uncountable intersection of probability-one sets. Finite initial derivative values cannot make an escaping tail dense in C. Thus no p f is HC(D). In particular p=z already settles the historical universal-preservation question negatively.

## Density deduction

The Gaussian series law has full support in H(C): any finite jet can approximate prescribed polynomial coefficients with positive probability; independent tail has positive probability of being uniformly small on a prescribed disk, using its finite expected norm and sufficiently late truncation. The probability-one set just constructed therefore meets every nonempty open set. Alternatively any polynomial addition preserves FHC(D) (all high derivatives vanish) and the eventual coefficient bounds, and translates of one such f by polynomials are dense in H(C). This latter argument is deterministic and suffices.

## Status

Positive earlier general implication FOUND. It is unsafe to describe either the basic negative answer or the simultaneous-all-nonconstant-polynomials strengthening as novel based on the current search. I have not found evidence that Nikula explicitly stated this polynomial-multiplier corollary. This checkpoint certifies an implication from an older theorem, not explicit priority for the exact wording. Earlier Gaussian invariant-measure literature may move the underpinning even earlier and is being checked.
