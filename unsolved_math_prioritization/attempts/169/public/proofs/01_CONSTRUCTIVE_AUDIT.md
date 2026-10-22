# Stage 1 constructive audit: random translates at square-root size

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 1. Target: uniform `k=floor(sqrt(p))` subset A of F_p and the exact cap `floor(100 sqrt(p))`.

## Result

No affirmative construction establishing the target was obtained. Two fully proved restrictions on construction classes survive the audit:

1. Adaptive selection from a predetermined subexponential-size family of small centre sets fails with high probability.
2. More substantially, a bounded number of arbitrary predetermined elementwise maps applied to A fail with high probability, even when the maps are selected adaptively from a predetermined subexponential-size family. This includes bounded unions of shifted/dilated copies of A, inverse-map constructions, and bounded-parameter nonlinear elementwise constructions.

Both restrictions leave a positive fraction of the group uncovered. They do not exclude unrestricted collective dependence of T on A. The exact problem remains unresolved by this argument.

## 1. Uniform-subset concentration lemma

Let A be a uniform k-subset of a finite set of size p. Suppose a real-valued function F of k-subsets satisfies

`|F(A)-F(A')| <= L`

whenever A' is obtained by removing one element of A and adding one other element. Then for u>0,

`Pr(F(A) <= E F(A)-u) <= exp(-u^2/(2 k L^2)).`

Proof. Expose the first k elements of a uniformly random ordering and use the Doob martingale for F of their unordered set. After a fixed prefix, compare two possible next elements x and y. Couple completions by the transposition exchanging x and y in the remaining population. The two final k-subsets are either identical or differ by one swap. Consequently the conditional expectations for the different next elements have range at most L; in particular the martingale increments have absolute value at most L. Azuma's inequality gives the displayed conservative bound. No independent-Bernoulli conditioning assertion is used here.

## 2. Adaptive selection among a small predetermined family

Fix C>0 and 0<epsilon<exp(-C). Let D_p be a deterministic family of subsets T of F_p such that

- `|T| <= floor(C sqrt(p))` for every member;
- `log |D_p| = o(sqrt(p))`.

Then, with probability tending to one, simultaneously for every T in D_p,

`|F_p \ (A+T)| >= (exp(-C)-epsilon) p`.

In particular, T may be chosen after the whole sampled A has been inspected, provided T belongs to the predetermined family.

Proof. For a fixed T of size m, put U_T(A)=p-|A+T|. Translation invariance and uniform sampling give the exact expectation

`E U_T(A) = p * binom(p-m,k)/binom(p,k)`.

The ratio is decreasing in m. Uniformly for `m<=C sqrt(p)`,

`binom(p-m,k)/binom(p,k) >= exp(-C-o(1))`.

Indeed its logarithm is `sum_{h<k} log(1-m/(p-h))`; the leading sum is `-mk/p`, and the total error is `O_C(p^(-1/2))`. Swapping one element of A changes the uncovered count by at most 2m, a safe bound. Applying Section 1 with `L=2C sqrt(p)` and a deviation of `epsilon p/2` gives, for all sufficiently large p,

`Pr(U_T < (exp(-C)-epsilon)p) <= exp(-epsilon^2 sqrt(p)/(32 C^2))`.

A union bound over the family completes the proof.

Examples covered by the theorem include all intervals and their dilates; all bounded unions of arithmetic progressions, with independently selectable steps and lengths; and all fixed-rank generalized arithmetic progressions of allowed size. Each such parameter family has polynomially many members. The theorem also allows larger families satisfying the displayed entropy bound. The parameters can all be chosen after seeing A.

The family of all allowable centre sets has logarithmic cardinality of order `sqrt(p) log(p)`, so this theorem cannot be union-bounded over unrestricted T.

## 3. Main surviving theorem: adaptive elementwise-map constructions fail

Fix a positive integer r and `0<epsilon<exp(-r)`. For each p let M_p be a deterministic family of r-tuples

`Phi=(phi_1,...,phi_r),  phi_j:F_p -> F_p`,

with `log |M_p|=o(sqrt(p))`. No injectivity, linearity, regularity, or computational restriction is imposed on any map. Define

`T_Phi(A) = union_{j=1}^r phi_j(A)`.

Then, with probability tending to one, simultaneously for every Phi in M_p,

`|F_p \ (A+T_Phi(A))| >= (exp(-r)-epsilon)p`.

Consequently the same lower bound holds for every subset of T_Phi(A), even if both the tuple and the subset are chosen after inspecting all of A.

For r=100, these centre sets have size at most `100 floor(sqrt(p))`, which is within the operational cap. The result says that this large class of legal adaptive constructions fails; it says nothing about all legal adaptive constructions.

### 3.1 Bernoulli expectation bound, including repeated constraints and loops

First let B include each field element independently with probability q. Fix Phi and x. The condition

`x not in B + T_Phi(B)`

is the intersection, over all indexed pairs (j,b), of the event that b and `x-phi_j(b)` are not both in B. If these two elements are distinct, this decreasing event has probability `1-q^2`. If they agree, its probability is `1-q`.

Let

`L_x = #{(j,b): b+phi_j(b)=x}`.

There are rp indexed constraints, and `sum_x L_x=rp`. Some constraints may repeat. Repeated application of the product-measure correlation inequality for decreasing events still applies to them, and gives

`Pr(x uncovered) >= (1-q^2)^(rp-L_x) (1-q)^L_x`

`                       = (1-q^2)^(rp) (1+q)^(-L_x)`.

For completeness, the correlation inequality follows by induction on the number of independent Boolean coordinates: condition on the last coordinate, apply the induction hypothesis to the conditional covariance, and observe that the two conditional expectations move in the same direction. Induction on the number of events then gives the product bound. Repetitions do not invalidate it.

The function `z -> (1+q)^(-z)` is convex. Jensen's inequality and the exact average `p^(-1)sum_x L_x=r` imply the uniform expectation lower bound

`E |F_p \ (B+T_Phi(B))| >= p(1-q^2)^(rp)(1+q)^(-r)`.

This argument handles arbitrary maps, including constant maps and maps producing many diagonal loops at a particular x. There is no hidden bound on graph degree.

### 3.2 Explicit transfer to the exact uniform-k model

Put `q=(k+k^(2/3))/p`. Generate a uniformly random ordering of F_p and independently let N have distribution Bin(p,q). Let B consist of the first N points and A of the first k points. B has exactly the independent Bernoulli-q law and A has exactly the required uniform-k law.

The function

`U_Phi(S)=p-|S+union_j phi_j(S)|`

is decreasing under inclusion of S. On the event N>=k, it follows that `U_Phi(A)>=U_Phi(B)`. Since the function always lies in [0,p],

`E U_Phi(A) >= E U_Phi(B) - p Pr(N<k)`.

The binomial lower-tail bound gives `Pr(N<k)<=exp(-Omega(k^(1/3)))=o(1)`. Also `rp q^2=r+o(1)` and `r log(1+q)=o(1)`. Thus, uniformly over all choices of the maps,

`E U_Phi(A) >= (exp(-r)-o(1))p`.

The Bernoulli model is used only to obtain this expectation estimate; high-probability concentration is then proved directly in the exact uniform-k model.

### 3.3 Concentration and the adaptive choice of maps

If A and A' differ by the swap a->a', any sum lost from

`union_j {u+phi_j(v):u,v in A}`

has a representation in which u=a or v=a. There are at most 2rk such indexed representations. Likewise at most 2rk values can be newly gained. Therefore `|U_Phi(A)-U_Phi(A')|<=4rk` is a valid uniform bound.

By Section 1 and the preceding expectation bound, for all sufficiently large p,

`Pr(U_Phi(A)<(exp(-r)-epsilon)p)`

` <= exp(-epsilon^2 p^2/(128 r^2 k^3))`

` <= exp(-epsilon^2 sqrt(p)/(128 r^2))`.

Multiplication by |M_p| proves the simultaneous assertion. The final map tuple may therefore depend arbitrarily on A within the specified predetermined menu. A smaller centre subset can only increase the uncovered set.

### 3.4 Concrete consequences and exact limitations

For every fixed r, all tuples of affine maps `phi_j(a)=s_j+lambda_j a` form a family of at most `p^(2r)` choices. Hence the theorem simultaneously excludes, even with adaptively chosen coefficients:

- T=A, T=-A, T=lambda A, or a shifted version;
- T=-A+S for any |S|<=r;
- any union of at most r shifted/dilated copies of A;
- any subset of one of these full envelopes.

More generally, any predetermined polynomial-size family of arbitrary maps is covered. This includes fixed-degree polynomial-map families, fixed inverse maps (with any specified value at zero), and predetermined polynomial-size menus of permutations. It does not include the family of all p! permutations. The maps need not be bijections.

The conclusion is unchanged if an arbitrary adaptively chosen set of `o(sqrt(p))` additional centres is appended: these extra translates cover at most `o(sqrt(p))*k=o(p)` points. In particular, the at-most-99-centre difference between the two 100 rounding conventions cannot repair the positive-density residual. This does not exclude repair with a further fixed positive multiple of sqrt(p) centres.

The theorem does not allow the formula for each phi_j to depend without restriction on the whole A. An arbitrary adaptive T can be encoded by a map tailored to that A, and the collection of all those maps is far larger than the menu allowed here. Nor does the fixed-r theorem allow r to grow without checking both its expectation and entropy error terms. These are substantive boundaries, not merely technical caveats.

## 4. Why the natural nibble route has not supplied a construction

The translate hypergraph has p vertices and p edges A+t. Its uniformity and degree both equal k. Vertex codegrees are autocorrelations `|A intersection (A+d)|`, of expected order one in the target model. This is suggestive but insufficient.

The small-relative-codegree matching principle normally invoked here has fixed uniformity. Uniformity cannot simply be allowed to grow to the degree: a finite projective plane of order q gives a `(q+1)`-regular, `(q+1)`-uniform hypergraph on `q^2+q+1` vertices, codegree one, with any two edges intersecting. Its maximum matching has size one. It does possess a small cover, so this example refutes the unrestricted matching implication, not the target covering conclusion.

A verified growing-uniformity source is Alon, Bollobas, Kim and Vu, *Economical covers with geometric applications*, author PDF, Theorem 1.2 (PDF p. 2): its k>4 conclusion requires `exp(2k) C=o(D/log D)`, where C is maximum codegree. At D=k≈sqrt(p), that condition fails even with C=1. The paper's fixed-uniformity statements also explicitly retain that hypothesis. Its general counterexamples are not random cyclic translate families and are not counterexamples to this target.

Primary source: https://web.math.princeton.edu/~nalon/PDFS/abkv4.pdf
Journal DOI: https://doi.org/10.1112/S0024611502013886

Splitting translates into much smaller pieces changes the cost scale: a construction using pieces of size O(log k) needs at least p/O(log k) pieces to cover p vertices. Unless many pieces can be charged to the same original translate through an additional argument, this cannot produce a fixed multiple of sqrt(p) original translates. Such a charging argument was not established.

## 5. Greedy, reservoir, and absorption accounting

The deterministic averaging step for an uncovered set U is

`max_t |(A+t) intersection U| >= k|U|/p`.

Thus ordinary greedy selection guarantees only `|U_s|<=p(1-k/p)^s`. Taking s=C sqrt(p) makes this *upper bound* about exp(-C)p, which is still much larger than sqrt(p) asymptotically. This is a limitation of that guarantee, not a proof that fully adaptive greedy must fail. Singleton repair after this guarantee returns the familiar logarithmic overhead.

A fresh-reservoir exposure can analyze a diagonal union `union_i (A_i+T_i)` when T_i is chosen before A_i is exposed. It does not analyze the actual final sumset `(union_i A_i)+(union_i T_i)`. The cross terms `A_j+T_i`, including j<i, permit T_i to exploit previously revealed samples. A diagonal-union no-go argument must not be relabelled as a full reservoir-construction obstruction. No such relabelling is made here.

Absorption would need a genuine theorem controlling the final residual and the net translate cost. For example, an adaptive first-stage set T_0 and residual U satisfying the exact inequality `|T_0|+|U|<=floor(100 sqrt(p))` would allow singleton repair. A bound `|T_0|+|U|<=(100-eta)sqrt(p)` for a fixed eta>0 is a simpler rounding-robust sufficient condition. The currently justified constant-round/random-round estimates leave a positive-density residual rather than a square-root-size one. A full-A-dependent repair mechanism bridging those scales was not established.

## 6. Acceptance status and next precise gap

The two proved restrictions are valid in the exact uniform floor-size model and imply a large residual, so they cannot be repaired by an additional `o(sqrt(p))` translates, even if those additional centres are chosen without restriction. They do not prove a lower bound on the optimal covering number, and they do not meet either global acceptance direction.

The surviving construction gap is unrestricted collective dependence: an efficient T, if it exists, must evade both a small predetermined menu of centre sets and the bounded-elementwise-map model. Nibble needs an additional property beyond degree and small codegree, while absorption needs a proved residual-repair theorem with total cost strictly within the fixed 100 cap. No such lemma was proved in this pass.

