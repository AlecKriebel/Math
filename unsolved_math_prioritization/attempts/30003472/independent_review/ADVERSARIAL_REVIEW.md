# Independent final scoped review: random order-type gaps, 30003472

## Verdict and bound packet

**PASS_FULL_FIVE_TURN_SCOPED_PACKET. No mandatory mathematical revisions. Original unrestricted problem remains UNSOLVED, 5/5 substantive author turns.**

The special-class probability-gap theorems, the credited same-type reduction, and both conclusions of the final mixture theorem are sound. In particular the mixture with critical convex-position probability also has a proved large actual max/min gap. It is neither an original-question counterexample nor a remaining unresolved instance of that construction.

The reviewed author manifest is `FINAL_PACKET_MANIFEST.json`, SHA-256

`e21ce309aa21fcc8d354c9933893145792c518393304d16757f9723ac2491e43`.

All 38 bound files match their lengths and hashes; the complete packet contains 39 files including the manifest. The four historical manifests contribute 26 additional verified file entries. All five author outputs were reproduced byte-for-byte, totaling **1,334,627 exact assertions**. Four primary PDFs match their recorded hashes. A separate checker importing no author code passes **56,100 exact assertions**, including independent geometry, empirical-kernel, binary-trie and generating-series controls. These finite assertions supplement the analytic review below; they do not formally certify the infinite-measure arguments.

This is an independent AI-assisted audit, not human peer review, proof-assistant certification or novelty certification. It is not a sixth author search.

## Exact source and quantifiers

The [official OWR 19/2017 report](https://ems.press/content/serial-article-files/46683), printed p. 1198, item 6, was independently opened and visually inspected. It prints c>0 and the exponential c^n but does not explicitly quantify the size n or specify its lower range. The imported c>1 interpretation is a substantive nontriviality clarification, not a literal transcription. The packet appropriately declines to call the literal small-c loophole a solution and separates absolute versus measure-dependent size thresholds.

The intended measures are Borel probabilities charging no line; this implies nonatomicity and almost-sure simple iid samples. The [primary order-type definition](https://arxiv.org/abs/1811.02236) uses orientation-preserving bijections, with labels forgotten. The packet follows that convention throughout, including its n! gains and labeled-to-unlabeled counting inequality.

All affirmative class results have their measure-dependent parameters and thresholds stated. A missing k-type gives a missing n-type for every n≥k; this observation by itself gives a measure-dependent threshold, not an absolute bound on the first missing size. The final packet does not claim that it solves the stronger uniform-threshold interpretation.

The [2024 same-type theorem](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v31i2p60) was independently read and its displayed Theorem 1 visually inspected. For d=2 its lower fraction is exactly 2^(-400)n^(-4); its upper bound is 4n^(-2). The external theorem, rather than a new result here, supplies those constants. The [Goaoc–Welzl counting discussion](https://arxiv.org/abs/2003.08456), Section 1.3.1, gives labeled n^(4n+O(n)) counts and the required factorial relation for the unlabeled scale.

The local primary text of *Limits of Order Types*, Lemma 3.16, does pass from absolute continuity to continuity of a Radon–Nikodym density without an intervening justification in that presentation. The candidate correctly identifies this narrow unfilled inference rather than refuting the lemma's conclusion or alleging that no repair exists. Its Turn 2 proof supplies the stated area-component conclusion independently. The final seed construction uses Lemma 3.15 and Proposition 17, not that regularity argument.

## Turn 1: counting and the area-domination class

### Generic joining-line arrangement

The realization space of a simple labeled type is open. Generic perturbation within it can avoid the finitely many extra parallelism and concurrency polynomial conditions. For three selected joining lines, any non-star three-edge graph either has an endpoint that can be moved to break concurrence or is a triangle, whose three side lines are already nonconcurrent in general position. Thus no extra incidence is forced. Coinciding ordinary intersections are excluded by the same conditions.

The line arrangement has binomial(j,2) lines, j original vertices of multiplicity j−1, and three ordinary vertices per four-set. The standard region increment formula therefore gives

    R_j=1+binomial(j,2)+j(j−2)+3binomial(j,4).

Each open sign cell provides a distinct labeled extension; differing base types stay different upon restriction. Thus L_(j+1)≥R_j L_j is justified, rather than inferred from finite counts. The displayed polynomial establishes 128R_j>(j+1)^4 for j≥2. Dividing the accumulated labeled bound by at most n! labelings gives exactly

    T_n≥1024(n!)³/128^n.

The automorphism group need not be trivial; the inequality direction handles it correctly.

### Curved strips and probabilities

The strips are inside the square and have area 1/(16n³). The determinant expansion is exact. With the stated minimum horizontal gaps and vertical errors its lower bound is strictly positive for every triple. Consequently the entire transversal forms a convex chain and all selected points are hull vertices. The n! assignments to separated strips are disjoint events, giving the claimed probability lower bound.

Area domination ensures positive mass in the small stable neighborhoods of every rescaled finite simple realization, hence positivity of every type. The factorial/counting constants multiply to the stated ratio. The inequality e<3 yields the deliberately crude explicit threshold. This is a measure-dependent class theorem; no arbitrary singular measure is covered by the area hypothesis.

## Turn 2: nonzero absolutely continuous component

The truncation selects a bounded integrable density h below the original measure, not a conditional density obtained by discarding an uncontrolled component. The singular part can remain everywhere. The vertical change of variables (x,t)↦(x,x²+t) preserves the relevant Lebesgue integrals. Sectionwise differentiation plus Fubini gives almost-everywhere convergence for almost every single t; the uniform bound h≤M makes it L1 convergence on [0,1]. Positive total mass guarantees a t for which both convergence and a positive trace level set hold. This t and its beta,m constants are fixed before n varies.

The good-interval counts are valid without a convergence rate. E-light cells carry at most m/2 mass; at least mN/2 cells are E-heavy. Each heavy cell failing the strip-average threshold consumes more than beta m/(4N) of the L1 error. The stated error budget leaves at least mN/4 good cells and one parity class of at least mN/8 separated cells. N=ceil(8n/m) both supplies n cells and obeys N≤9n/m. The strip mass is consequently at least beta m^4/(5832n³), with constants independent of n.

The determinant margin remains positive at the resulting spacing and width. Full finite-type support follows separately from a planar density point of a positive-area level set: one sufficiently small enclosing ball leaves less missing area than half of each finitely many stable disks. This proof does not assume an open set where the original density has a pointwise lower bound.

Thus the extension to every line-null measure with a nonzero absolutely continuous component passes. It does not give uniform thresholds over that class or a smoothing argument for purely singular measures.

## Turn 3: singular product components

The interval Frostman upper bound makes nu nonatomic. Continuous quantiles on a compact supporting interval can be chosen in increasing order even if its distribution function has flat portions. Each full intervening quantile interval has mass 1/M and therefore length at least (CM)^(-1/d); this is a lower bound on the geometric gap between the selected odd intervals. The width ell_n²/4 gives the stated determinant margin. The probability and counting estimates have the exponent 3−2s/d and the reported constants.

The heavy-interval lemma works for arbitrary eta, including atoms: the two closed halves cover the parent, so at least one has half its mass. Nested intervals have a unique common point and length within a factor two of any requested radius. This proves the uniform local lower-mass bound at that point. It does not impose a global lower regularity condition on eta.

For line-nullness, vertical lines require one nu-null x value; for a nonvertical line, conditioning on t leaves at most two x solutions of a quadratic. Fubini then applies even to atomic eta. The full-support singular example is also valid: a countable positive mixture of Cantor measures can be singular with full real-line support, and the parabolic shear preserves the stated product support while Fubini shows area-null concentration. Stable open neighborhoods inside the strip give every finite type positive probability.

The actual dominated product hypothesis is indispensable and is retained. Disintegration of an arbitrary singular measure is not silently replaced by a fixed independent product.

## Turn 4: universal same-type transfer and its limitation

The colored-set theorem applies to the n small perturbed copies because their union is in general position and all triples of distinct underlying original points preserve orientation. If projected subsets in two colors share two distinct points p,q, a third color has a point r outside them. The two corresponding colorful triples have opposite orientations, contradicting the common transversal type. Hence any two projected subsets overlap in at most one point.

Removing shared points costs at most n−1 per color. The resulting disjoint sets preserve the common type when projected, and their disjointness legitimizes the n! label assignments. The assumption gamma_n M>n supplies the third point and positive final set sizes. It is attainable because n is fixed before M grows.

The empirical expectation identity is correct: only distinct pool-index tuples contribute, yielding (M)_n/M^n times the population probability. Disjoint pairs of pool-index tuples have zero covariance. At most n²/M of the pairs share an index by a union bound, giving the stated variance estimate. Chebyshev and the finite number of n-types supply deterministic general-position pools with simultaneous convergence. Passing a finite maximum through this limit is legitimate. No continuum homogeneous-region theorem is presumed.

The result is the universal bound n!(2^(-400)n^(-4))^n. Combining it with the counting lower bound has an exponentially unfavorable constant and therefore does not prove a gap. The conditional improvement criterion p<4, or gamma_n n^4 tending to infinity, follows algebraically. The cited exponent four is a limitation of this method, not a proven optimal exponent or an impossibility theorem for the original question. The failure of six-point block amplification without fiber comparisons is likewise correctly left as a proof-route gap.

## Turn 5: seed, infinite mixture and the simultaneous large gap

### Seed and compressed binary trees

The chosen a=1/4,b=1/16 satisfies the exact hypothesis b≤a(1−2a)(1−2b) of the credited seed lemma. Its nested binary coding is injective and nonatomic. The source's prefix-length orientation rule gives a nonzero sign for every triple of distinct support points, so a line contains at most two such points and has measure zero. The covering by 2^j rectangles of diameter O(4^(-j)) gives an area-null support of dimension at most 1/2.

The Gaussian-type convex-probability upper bound follows from the credited Proposition 17 after reducing the quadratic coefficient and enlarging D to handle finitely many small m. It does not depend on Lemma 3.16.

For lexicographically sorted sampled leaves, the two relevant lowest common ancestors are comparable ancestors of the middle leaf. In a binary tree they have distinct depths. Suppressing unary vertices preserves which is deeper, hence every orientation sign. An ordered full binary tree with n leaves thus determines the sampled type. Catalan(n−1)≤4^(n−1) gives the support-complexity bound; injectivity from trees to types is unnecessary. The independent checker tests this invariance after inserting different unary-chain lengths in every small tree.

### Explicit neighborhoods and full support

For x_j=2^(-j), the separating functional has value −x_i²/16 at its own center. Its gradient norm is below 2. For any other center, the ratio computation (1−z)²−z²/16 has the stated minima on z≤1/2 and z≥2. Perturbations in the chosen radii cost at most x_j²/64, so separation stays strict. Every finite transversal is therefore in strictly convex position, and all balls lie in the unit disk.

The positive mixture weights are summable because alpha=beta+1>1. Odd components provide the separated neighborhoods; even components in a countable basis provide full disk support. Countable unions preserve area-null concentration and line-nullness. Positive support on every open ball gives all finite simple types positive probability after a positive affine rescaling. The latent component labels are legitimate even where component supports overlap.

### Lower probability bound

Selecting n specified odd components with indices below 4n gives weights at least Z_alpha^(-1)(4n)^(-alpha). The n! disjoint latent-label assignments are all convex by separation. The factorial bound yields the exponent −(alpha−1)n log n with a fixed constant. It is not an n-dependent choice of the underlying measure.

### Infinite positive generating series

Convexity of the complete sample implies convexity of every component subsample. Conditional independence of those subsamples gives the product occupancy upper bound. All coefficients are nonnegative. F(t)≤exp(t) for t≥0 implies the infinite product is finite, bounded by exp(z), and monotone limits of the finite products justify its coefficients and the occupancy sum via Tonelli.

The translated Gaussian sum after completing the square is bounded uniformly in its real center. Thus log F(t)≤C1(1+log t)² for t≥1, with a constant fixed by the seed. At smaller t the bound log F(t)≤t is valid.

The split at H=(z/Z_alpha)^(1/alpha) is correct. The head summand is a decreasing function of its index, so its sum is bounded by the integral from zero to H. That improper integral is finite and equals H(1+2alpha+2alpha²). For the tail, integration from floor(H)≥H/2 gives 2^(alpha−1)H/(alpha−1). Hence log G(z)≤Bz^(1/alpha), with B independent of n.

Positivity gives the coefficient estimate a_n≤G(z)/z^n. Choosing z=(alpha n/B)^alpha is the optimizer of this upper bound and eventually lies in the valid large-z regime. Using n!≤n^n gives the matching exponent −(alpha−1)n log n. Together with the lower bound this proves n^(−beta n)exp(O_beta(n)) for every fixed beta>0. No conditional convergence, unquantified exchange of limits or n-dependent constant is hidden in this step.

### The same measures have a large actual gap

A fixed positive-weight seed component yields max p_mu≥w_1^n/4^(n−1). Multiplication by the universal type-counting lower bound gives exactly

    max p_mu/min p_mu ≥4096(n!)³(w_1/512)^n
                      ≥4096[w_1 n³/(512e³)]^n.

Thus every constructed mixture satisfies the intended eventual exponential gap. At beta=3 its convex statistic happens to have the counting scale, so it defeats only a method demanding a nonzero n log n separation for that particular statistic. Finer convex-probability constants are not ruled out, and the actual heavy type is eventually nonconvex. Both simultaneous conclusions are correctly retained in the final packet.

## Final remaining scope

The arbitrary line-null measure question remains unresolved under either documented asymptotic interpretation. The nonzero-area-component, specified parabolic-product and low-type-complexity-component cases are genuine sufficient classes. The universal same-type transfer is rigorous but quantitatively inconclusive. The final singular full-support mixture illustrates the limitation of a convex-only method while being affirmatively resolved by another statistic.

No mandatory revision is required for publication with **unsolved, 5/5** and these explicit qualifications. The original source ambiguity and all measure-dependent thresholds should remain visible. This review approves neither a universal result nor a counterexample that the packet does not supply.
