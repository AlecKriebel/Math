# Stage 2: convolution moments and a heavy-point reduction for every cover

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 2. Exact model: A is a uniform k=floor(sqrt(p))-subset of Z/pZ, p prime; c=floor(100 sqrt(p)).

## Results

1. Untrimmed Poisson factorial-moment estimates cannot hold uniformly over translating sets, even when A itself is completely typical: the choice T=-A creates a spike of height k, forcing every fixed factorial moment of order at least three to diverge.
2. Every hypothetical cover admits a deterministic heavy-point peeling. With high probability over A, every such peeling leaves a linearly sized residual translating set. Its convolution with A has no spike as high as delta k, and it still must cover the holes left by a bounded union of translates of A-A.
3. This gives a valid structural reduction for unrestricted covers, together with a precise missing local statement. It does not provide enough control to establish the statement: a fixed-fraction spike cutoff is too weak for a fixed-order moment method, whereas a bounded cutoff can require order k peeled pieces.

## 1. The exact factorial-moment obstruction

For any T, let f_T(x)=(1_A*1_T)(x), let lambda=k|T|/p, and define

mu_j(A,T)=p^-1 sum_x (f_T(x))_j,

where (z)_j=z(z-1)...(z-j+1) and mu_0=1. One has mu_1=lambda exactly. A naive Poisson route would seek mu_j approximately lambda^j uniformly in admissible T, with enough orders to detect the zero mass.

This cannot hold. For every k-set A, take T=-A. Then f_T(0)=k and |T|=k<=c, so for fixed j>=3,

mu_j(A,-A)>=(k)_j/p=(1+o(1))k^(j-2) -> infinity.

But lambda=k^2/p tends to one. The contradiction is deterministic and applies on every possible high-probability typical-A event. Moreover T=-A has exactly the same individual energy, doubling and nontrivial Fourier magnitudes as A. Thus assumptions of random-like individual energy and spectrum do not prevent the high-order obstruction.

This is not a covering construction: A-A usually has holes in the present model. It shows why a uniform moment approximation needs to recognize and handle joint coherence between the two factors before it can be used to exclude covers. Restricting attention only to genuine covers would require a new cover-specific argument; it cannot be justified by a uniform theorem already falsified by T=-A.

## 2. What a sufficiently accurate moment estimate would imply

For every nonnegative integer f and odd m,

1_{f=0} >= sum_{j=0}^m (-1)^j (f)_j/j!.

For f>0 the sum is -binom(f-1,m), interpreted as zero if m>f-1; for f=0 it is one. Hence

|G\(A+T)|/p >= sum_{j=0}^m (-1)^j mu_j(A,T)/j!.                  (2.1)

For admissible T, 0<=lambda<=100 exactly. Choose m=399. Taylor's theorem gives

sum_{j=0}^{399}(-1)^j lambda^j/j!
 >= e^-lambda - 100^400/400!
 >= e^-100 - (e/4)^400
 > (3/4)e^-100.                                                 (2.2)

The last strict inequality follows from 400(1-log 4)<-154, while log((1/4)e^-100)>-102. Thus a bound

sum_{j=1}^{399}|mu_j(A,T)-lambda^j|/j! <= (1/4)e^-100             (2.3)

would imply at least (1/2)e^-100 p uncovered points. Equations (2.1)-(2.3) make the required precision and number of moments explicit, rather than calling an unspecified moment estimate Poisson-like.

The observation in Section 1 shows that (2.3) cannot hold uniformly over all T for any A. It remains conceivable that suitably localized or truncated observables distinguish every cover, but those observables and their uniform estimates must be supplied.

## 3. A deterministic peeling for arbitrary T

Fix C>0 and 0<delta<=1. For sufficiently large p, floor(C sqrt(p))<=(C+1)k. Put

R=ceil((C+1)/delta),  h=ceil(delta k).

Start with T^(0)=T, where |T|<=floor(C sqrt(p)). If there is a point x_i with

|(x_i-A) intersect T^(i-1)|>=h,

remove the whole block

B_i=(x_i-A) intersect T^(i-1),  T^(i)=T^(i-1)\B_i.

Repeat until there is no such point. The blocks are disjoint and each has at least h elements, so at most R steps occur. If X is the set of their points x_i and T0 is the final remainder, then

T=T0 disjoint-union B_1 disjoint-union ... disjoint-union B_l,
l<=R,
B_1 union ... union B_l subset X-A,
max_x(1_A*1_T0)(x)<delta k.                                     (3.1)

The final strict inequality follows because the integer convolution values are less than ceil(delta k). This construction is valid for every A and T, and every choice of eligible points at each step. It does not assume T independent of A.

## 4. The random-A consequence: the residual cannot be small

The already proved Stage 1 affine-envelope theorem states that, for every fixed R and epsilon>0, with probability tending to one,

|G\(A+(X-A))| >= (e^-R-epsilon)p

simultaneously for every X subset G with |X|<=R. Its parameters may depend arbitrarily on A. The proof is the polynomial-menu argument for a fixed number of translates of -A; see ../proofs/01_CONSTRUCTIVE_AUDIT.md and its independent audit in ../audits/01_AUDIT.md.

Take epsilon=e^-R/2 and work on this event. If T in Section 3 is a cover, define the canonical residual

H_X(A)=G\(A+(X-A)).

Then |H_X(A)|>=eta p, eta=e^-R/2. All peeled blocks lie in X-A, so they cover no points of H_X(A). Since A+T=G, necessarily

H_X(A) subset A+T0.                                             (4.1)

Since each centre t in T0 supplies a set A+t of exactly k points, |A+T0|<=k|T0| and (4.1) gives

|T0|>=|H_X(A)|/k>=eta p/k>=eta k.                               (4.2)

Consequently the following assertion is proved:

**Heavy-point residual theorem.** For every fixed C>0 and 0<delta<=1, with high probability every cover T of size at most floor(C sqrt(p)), and every greedy peeling as above, leaves a residual T0 of size at least eta k, where eta=(1/2)exp[-ceil((C+1)/delta)]. It satisfies max_x(1_A*1_T0)(x)<delta k and covers H_X(A) for some |X|<=R.

This is a reduction applying to all hypothetical covers, not just a theorem ruling out one more predetermined family. It says a bounded collection of strongly coherent pieces cannot account for an entire cover: a linear-size remainder is required. The constants are extremely small at C=100 and are purely asymptotic.

## 5. Exactly what remains

For fixed C=100 and a chosen fixed delta, it would suffice for a negative answer to prove, with probability bounded away from zero along infinitely many primes, the following statement:

For every X subset G with |X|<=R and every S subset G with |S|<=c and max_x(1_A*1_S)(x)<delta k, the set H_X(A) is not contained in A+S.                 (5.1)

Indeed, (5.1) contradicts the remainder produced from any putative cover. The family of X has polynomially many descriptions because R is fixed. However S still has exp(Theta(k log p)) possibilities, can depend on all of A, and is tested against an A-dependent residual. Neither the concentration nor the inverse results from Stage 1 establish (5.1).

The maximum in (5.1) is only bounded by delta k, which still tends to infinity. Fixed-order factorial moments can remain dominated by a small number of points at this scale. Peeling to a fixed maximum M would remove blocks of at least M centres and could take Theta(k) steps, so the bounded-envelope theorem would no longer provide a fixed positive-density residual or a polynomial parameter count. This gap is quantitative and substantial, not a rounding issue.

A localized version of (2.1), averaging only over H_X(A), is valid algebraically. Its factorial moments depend jointly on A, X and S, and its mean need not equal k|S|/p. Therefore global Poisson moments cannot simply be substituted. A useful future theorem would need either a uniform localized hole estimate in (5.1), or an inverse theorem showing that a violation forces substantially more compressibility than the present peeling provides.

## 6. Connection with the Singer counterexamples

The companion [Singer construction](02_SINGER_PRIME_COUNTEREXAMPLES.md) proves that even simultaneous low energy and small spectrum of both factors permit exact efficient covers on infinitely many prime groups. Those examples retain finite coherent shifted-copy structure and are exceptional under the uniform-random law. Together with the deterministic T=-A spike, they show that individual pseudorandom statistics are insufficient proxies for the joint structure a successful moment or inverse argument would have to detect.

No assertion is made that every efficient cover has a short decoder, that every low-energy T has Poisson occupancy, or that the residual theorem itself settles (5.1). The unrestricted contract remains unresolved.

## Independent checks

The proof audit checked the peeling bound, strict integer cutoff, positive-density remainder implication, and order-399 Bonferroni constants. Direct finite-set tests checked 502 peeling cases across 52 small-prime affine orbits, using minimum and maximal inclusion-minimal covers and all thresholds from 1 through k+1. These tests checked the deterministic containments and cardinality inequalities; they do not prove concentration for adaptive choices. These are historical finite diagnostics; see the reproducibility guide for the public replay scope.

