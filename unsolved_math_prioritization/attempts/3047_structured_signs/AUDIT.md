# Independent audit of two structural partition-sign obstructions

## Decision and exact scope

Both mathematical claims pass independent review, subject to the exact final document pins recorded in the acceptance manifest.

1. If only finitely many unrestricted-partition factors are changed, and each changed factor has either a rational coefficient-sign series or a binary-digit multiplicative coefficient-sign series, the product retains radial logarithmic constant π²/6 and coefficient upper-growth constant π√(2/3). In particular, its coefficients are unbounded.
2. If every factor may independently use an arbitrary binary-digit multiplicative sign sequence, the sharp last feasible degree for coefficients in {−1,0,1} is 75. Every assignment violates the bound by degree 76.

The second statement allows infinitely many changed factors, but restricts the coefficient signs within each factor. Neither statement treats the full independently signed unrestricted product. Neither claims a new result in the literature or a resolution of the original problem. These claims are separate from the at-most-two-arbitrary-factor obstruction.

## A. Analytic proof audit

Let E(q)=∏_{m≥1}(1−q^m)⁻¹ and let S be the finite set of changed factors. The exact identity is

P(q)=E(q)∏_{m∈S}(1−q^m)f_m(q^m).

All factors have constant coefficient 1. Every coefficient of each f_m is ±1. The finite replacement identity is valid both formally and analytically in the open unit disk. A changed factor may have infinitely many changed coefficients; finiteness concerns the number of factors.

### Partition radial constant and coefficient upper bound

For t>0, nonnegative summation gives

log E(e⁻ᵗ)=∑_{ℓ≥1}1/[ℓ(e^{tℓ}−1)].

Multiplication by t bounds the ℓ-th summand by 1/ℓ². Dominated convergence therefore gives t log E(e⁻ᵗ)→C=π²/6, while the same comparison yields log E(e⁻ᵗ)≤C/t for every t>0.

Each coefficient a_n of P is the sum of one ±1 contribution for each partition of n, so |a_n|≤p(n). The elementary positive-coefficient estimate p(n)e⁻ⁿᵗ≤E(e⁻ᵗ), optimized at t=√(C/n), yields log max(1,|a_n|)≤2√(Cn). No asymptotic partition formula is required.

### Binary factors: zeros and the lower bound

For B(z)=∏_{j≥0}(1+σ_j z^{2^j}), unique binary expansion supplies exactly one signed contribution to each coefficient. Thus its coefficients are ±1. For fixed u>0, each factor at z=e⁻ᵘ is positive, and the deviations from 1 are summable. Consequently B(e⁻ᵘ)>0; positivity of individual factors alone would not have sufficed without the summability argument.

The least possible value on this radius is the all-negative product. Write a=log 2, L=log(1/u), J=⌈L/a⌉, with 0<u≤1. For j<J, the estimate 1−e^{−2^j u}≥2^j u/2 applies because 2^j u<1. For j≥J, 2^j u≥2^{j−J}≥1, and −log(1−x)≤x/(1−x) bounds the entire tail by the fixed constant e/(e−1)². The resulting bound is

log B(e⁻ᵘ)≥−L²/(2a)−3L/2−a−e/(e−1)².

The algebra involving the fractional part of J is correct, including dyadic endpoints and u=1. The trivial coefficient bound gives log B(e⁻ᵘ)≤L+log 2. These inequalities imply u log B(e⁻ᵘ)→0 uniformly in the digit-sign choices. They correctly handle the transition 2^j u≈1.

### Rational factors

A rational f with f(0)=1 is not identically zero. Near z=1 it can be written (1−z)^νg(z), with integer ν and g analytic and nonzero near 1. Hence log|f(e⁻ᵘ)|=ν log u+O(1). This is a local statement: rational signed series can have zeros in (0,1), so a global radial lower bound would be invalid. The reviewed proof uses only a sufficiently small positive u and is zero-safe.

Rationality is equivalent here to eventual periodicity. Rationality gives an eventual, deterministic, finite-order linear recurrence. Its state tuples take values in a finite alphabet, so an eventual repeated tuple forces periodicity. Conversely, the generating function of a periodic tail is rational. The argument does not require the recurrence coefficients to be integers.

Substitution u=mt for each fixed m, followed by a finite sum, proves t log|P(e⁻ᵗ)|→C. This step could not be applied without further uniform control to an infinite active set.

### Absolute-value Laplace step

For A≥0,

lim_{t↓0} t log ∑_{n≥0}exp(A√n−tn)=A²/4.

For the upper bound, split tn=(1−δ)tn+δtn, complete the square in √n, sum the geometric factor exp(−δtn), and let δ↓0 after taking the upper limit. For A>0 the single term n=⌊A²/(4t²)⌋ gives the lower bound; A=0 is the geometric-series case. The order of these limits is valid.

If the coefficient limsup were less than 2√C, choose A between the two values and absorb the finite exceptional prefix in a constant K. Then |a_n|≤Kexp(A√n) for all n, and the triangle inequality gives a radial upper limit at most A²/4<C, contradicting the radial result. Thus the limsup equals 2√C=π√(2/3). This does not assert a lower bound for every coefficient and does not misuse a positive-coefficient Tauberian theorem.

The use of log max(1,|a_n|) avoids undefined logarithms at zero. With log 0=−∞, the corresponding ordinary logarithmic limsup is the same because the established constant is positive.

The final necessary-condition discussion for arbitrary finite active sets is also valid: bounded output coefficients would force ∏_{m∈S}|f_m(e^{−mt})|≤exp(−c/t) for every 0<c<C and sufficiently small t. Some factor is exponentially small at each t, but that factor can depend on t. This gives no claimed lower bound for arbitrary signed series and does not settle that broader case.

## B. Exact all-binary reduction

A binomial is indexed by a pair (m,j), m≥1 and j≥0, and has exponent n=m2^j. For fixed n the complete set of such pairs is

(n,0), (n/2,1), …, (n/2^{v₂(n)},v₂(n)).

There are d_n=v₂(n)+1 pairs. Grouping their binomials gives

H_n(q)=(1+q^n)^{k_n}(1−q^n)^{d_n−k_n},  0≤k_n≤d_n,

where k_n is their number of positive signs. The count is exact, including n odd and powers of two. Every pair belongs to exactly one group. Every sequence of legal counts lifts to labelled signs by choosing any k_n of the d_n labels in each group to be positive. Such independent choices are allowed within and between every original factor.

Different labelled assignments with the same counts yield exactly the same full product, not merely the same coefficient prefix. Thus the grouping loses no feasible product. It need not preserve how many labelled assignments produce a product, which is irrelevant to existence.

The formal rearrangement is legal: only finitely many pairs satisfy m2^j≤N for each fixed N, indeed ∑_{j≥0}⌊N/2^j⌋. Factors of greater exponent cannot affect coefficients through N. This also proves that any degree-75 assignment can be extended by arbitrary later signs without changing its verified prefix.

## C. Exhaustive recurrence and independent checks

At degree n, retain the complete count string (k_1,…,k_{n−1}), not a truncated signature or a numerical score. Let A_n be the degree-n coefficient of ∏_{m<n}H_m(q). The degree-n coefficient after adding the next group is exactly

A_n+2k_n−d_n.

All lower coefficients are unchanged; the next nonconstant term of H_n has degree at least 2n. Therefore testing every integer k_n from 0 to d_n and keeping precisely the children with absolute value at most 1 is both necessary and sufficient. Induction proves that the frontier contains every feasible grouped assignment. There is no beam cutoff, heuristic pruning, randomized step, or identification of distinct count strings.

The independent producer multiplied the binomials by ordinary integer convolution. Before inspecting the author's implementation, it reproduced the claimed first empty degree. A separately written verifier used the logarithmic derivative instead. For G=∏_{m<n}H_m and s_r=[q^r]qG′/G,

s_r=∑_{m|r, m<n}m·{2k_m−d_m if r/m is odd; −d_m if r/m is even}.

Starting with b_0=1, it recomputed coefficients by

r b_r=∑_{j=1}^r s_j b_{r−j}.

Integer divisibility was checked at every step. The verifier compared the full generated child set against every recorded frontier, and checked root, level coverage, state lengths, legal integer counts, uniqueness, counts, parent feasibility, and terminal exclusions. It did not accept counts or hashes as substitutes for complete-set comparisons.

Results:

- First empty degree: 76
- Last nonempty degree: 75, with exactly two grouped states
- Total nonempty grouped states, including the root: 3,903
- Largest frontier: 228, at degree 39
- For each final state: A_76=6 and d_76=3
- Every possible degree-76 coefficient: 3, 5, 7, or 9

The two final states are interchanged by q↦−q. This symmetry was observed after enumeration and was not used to reduce the search.

The complete frontier sizes for degrees 0 through 76 are:

1,2,2,4,8,12,24,32,32,26,26,16,30,36,64,40,78,82,136,74,140,74,68,78,150,74,70,36,36,36,32,22,42,50,44,64,104,144,180,228,154,166,100,106,142,62,42,24,34,30,24,20,38,50,86,44,80,30,26,14,26,20,16,22,22,14,14,8,14,18,14,8,16,16,4,2,0.

An additional exhaustive control enumerated all 32,768 labelled assignments to the 15 binomials of exponent at most 8. Exactly 1,132 labelled assignments were feasible, projecting onto the same 32 grouped states. For each state, the number of labelled preimages equalled ∏_{n=1}^8 binom(d_n,k_n). This directly tests that multiplicity reduction retains the correct collisions.

Both degree-75 witnesses were additionally lifted back to labelled digit signs. Each original factor was reconstructed coefficient by coefficient from binary expansions, and those original factors were convolved directly. This independently recovered both complete degree-75 prefixes and, for all four degree-76 choices, the coefficients 3, 5, 7, and 9.

Ten deliberate negative controls were all rejected: deleting a feasible state; adding an infeasible state with legal count alphabet; duplicating a state; deleting the root; omitting the terminal level; changing a terminal residual; changing a frontier count; changing the target bound; removing one copy from every grouped multiplicity; and reversing the even-multiple sign in the logarithmic derivative.

Normal Python, optimization level 1, and optimization level 2 returned identical substantive results. Verification uses explicit conditional failures, not removable assertions. Programs and complete raw certificates remain private; only mathematical statements, audit results, and permitted verification metadata are intended for publication.

## D. Source review and limitations

The [Open Problem Garden statement](https://www.openproblemgarden.org/op/dividing_up_the_unrestricted_partitions), independently inspected on 12 October 2026, concerns independently chosen signs in every unrestricted-partition factor. Its historical finite-search discussion does not concern only the binary-digit subclass.

[Andrews and Newman, *Binary Representations and Theta Function*, Integers 18 (2018), A34](https://math.colgate.edu/~integers/s34/s34.pdf), has a printed publication date of 13 April 2018. Its binary identities use specified sets of dilates, including odd dilates. Their success does not license omitting other factors from the full unrestricted product. The official PDF and its introduction and displayed product scopes were independently inspected; no third-party program was executed.

This audit establishes the mathematical claims within their stated classes. It does not certify exhaustive novelty, current literature status of the unrestricted problem, or a theorem for arbitrary independently signed coefficient arrays.

## E. Separately pinned late source caveat

The separately pinned RADIAL_SCOPE_SUPPLEMENT.md verifies the application of Güntürk’s published exponential-approximation theorem. It also proves the elementary harmonic amplification consequence for finitely many unrestricted active factors. This supplement sharpens the limitation of a purely radial approach and does not change either frozen structural proof. The cited theorem’s proof is not independently certified here.
