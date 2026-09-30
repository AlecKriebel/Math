# Independent review: nonboundary Radix Selection counterexample (30002720)

**Verdict: PASS_COMPLETE_NONBOUNDARY_COUNTEREXAMPLE. No mandatory correction.** The proof establishes failure of tightness at one explicitly specified fixed nonboundary rank, under square-root scaling and every deterministic centering. It gives a complete negative answer to universal fixed-rank convergence in the stated Markov-source model. It does not classify ranks, establish an almost-everywhere statement, or certify historical priority.

Reviewed `COUNTEREXAMPLE.md`, SHA256 `c72a38099e93b4d593be231e8f0c4ad726a399c3d61283da9f7b1f7e55801a5c`. This is an independent gpt-6-astra xhigh mathematical and source audit, not human peer review.

All **16,642** submitted exact controls replay byte-identically. A separate implementation passes **44,602** exact controls, including **6,732** adaptive selection cases. The asymptotic result rests on the written proof, not those finite controls.

## 1. Exact question, cost and prior obstruction

I read the full original Leckey contribution in [OWR 50/2014](https://ems.press/content/serial-article-files/46539), pp.2854–2856, and visually checked the last page. The second part asks about Radix Selection on independent strings from a binary Markov source. The displayed normalization subtracts the deterministic first-order profile times n and divides by sqrt(n). The concluding question asks for convergence of the marginals for Markov sources. Sorting, grand-average ranks and a functional tightness question are distinct topics in the contribution.

The earlier [2014 analysis](https://arxiv.org/abs/1404.3672), Section 3.1, Theorem 3.1, explicitly states its quantile mean formula outside the countable cylinder-boundary set. It separately discusses the boundary convention. Thus a nonboundary construction is meaningful even if one reads the original question as inheriting that restriction.

I also read the definitions and relevant Sections 2.1 and 2.4 in the complete [process paper](https://arxiv.org/abs/1605.02352v2) and the [author-hosted manuscript](https://www.math.uni-frankfurt.de/~neiningr/radix_journal.pdf). Equations (2)–(3) define exactly the singleton-truncated prefix-count cost used in the candidate. The hypotheses require positive initial and transition probabilities. The proposed matrix and stationary uniform initial distribution satisfy them, and the transition rows differ, so this is not a memoryless source.

There is a genuine source tension, correctly disclosed in the package. Proposition 2.9 already proves non-tightness of fixed marginals at dense boundary ranks. The paragraph immediately following Corollary 2.11 nevertheless describes one- or finite-dimensional marginal convergence as open. I checked both rendered pages, including the symbols and quantifiers. The candidate does not claim to discover Proposition 2.9; its single fixed rank lies outside the boundary set. The result is compatible with the random, sample-dependent centering in Proposition 2.8.

The [author publication list](https://www.math.uni-frankfurt.de/~neiningr/publist.html) and [publisher issue page](https://www.sciencedirect.com/journal/stochastic-processes-and-their-applications/vol/129/issue/2) corroborate the final citation, SPA 129 (2019), pp.507–538. The full proof/source wording audited here comes from the complete preprint and author manuscript. A final typeset-text comparison was not made. Current primary searches did not establish priority for the sparse nonboundary construction.

## 2. Quantile representation and continuity of the chosen rank

The recursive cylinder intervals have lengths equal to the Markov prefix probabilities and form an ordered partition at each depth. Their maximum lengths tend to zero, so a uniform point outside the countable endpoint set has one infinite code with exactly the prescribed source law. Independent uniforms give independent source strings. Order preservation gives the required identity between the selected string and the code of the uniform order statistic. The event excluding all sample/cylinder endpoint coincidences has probability one.

For q=3/4, the sum of all terms strictly after a common nonempty prefix w is bounded between zero and 3 pi(w). Thus the absolute difference of two mean-profile values is at most 3 pi(w), not twice that number: both tails lie in the same interval of length 3 pi(w).

The sparse word has infinitely many zeros and ones. After any fixed prefix it therefore has positive-probability cylinder strings on either side in lexicographic order. Its rank t is strictly inside every cylinder containing that prefix. Consequently t is no cylinder boundary, and nearby ranks share every specified prefix with it. The preceding tail bound proves continuity of the first-order profile at t. Also 0<t<1, so the binomial variance used later is strictly positive.

## 3. The uniform cost error is justified without a process limit

For any deterministic cylinder interval, its empirical count differs from n times its length by at most 2nD_n. The empirical distribution function controls all intervals at once; a separate union bound over infinitely many cylinders is unnecessary.

The grid proof gives P(D_n>d_n)≤4/n². Its Hoeffding bound follows from the stated Bernoulli moment-generating-function calculation, and interpolation between grid points adds at most 1/n². The arithmetic of the union bound is correct.

At depth H_n, the collision probability is at most choose(n,2) times the sum of squared cylinder probabilities. The sum of squares is at most the largest cylinder mass, (1/2)q^(H_n−1), and q^(H_n−1)≤n^(−5). This proves the displayed 1/(4n³) bound. On the collision-free event every deeper cylinder has at most one input and hence contributes zero to the actual stopping cost.

At each of the H_n remaining depths, singleton truncation differs from the raw count by at most one. The uncounted mean-profile tail is at most 2q^(H_n−1). Multiplication by n yields exactly the 2n^(−4) term. Combining these facts gives the candidate's explicit R_n, uniformly over every target string. No dependence between the order statistic and the counts is ignored: this uniform deterministic estimate is applied on its common high-probability event.

The bound is O(sqrt(n)(log n)^(3/2)). A sharper Gaussian-process theorem is not required. The expectation of the finite-n cost is finite, so expectation centering is included among the deterministic sequences in the final conclusion.

## 4. Sparse cylinders and the scale calculations

I reconstructed the digit counts and endpoint values independently.

The prefix before position j² has j²−2 transitions. Its j−2 isolated ones produce 2j−4 changes, leaving j²−2j+2 equal-digit transitions. This gives exactly P_j. The successive prefix probabilities satisfy

    P_(j+1)/P_j = (1/16) q^(2j−1).

Each one digit contributes the left-child mass qP_j to the lexicographic distribution function. Therefore the series for t and its partial sums tau_j are correct.

The two endpoint strings at tau_j have common-prefix contribution C_j. On the left, the remaining profile equals 2qP_j=3P_j/2; on the right it equals P_j/2. Their jump is P_j. These are exact geometric sums, not asymptotic estimates.

Between square positions j² and (j+1)² there are exactly 2j zeros. The right cylinder beginning at tau_j with that zero block has length P_j q^(2j)/12, and t lies strictly inside it. This proves both the sign and the strict upper bound on t−tau_j.

For K=floor(j/2), the endpoint cylinders of depth K have respective masses P_j q^K/4 and P_j q^K/12. The proposed width w_j=P_jq^j eventually fits in both. The common-prefix estimate gives the two profile errors bounded by P_j q^K, as stated.

Taking n_j=ceil(w_j^(−2)) gives sqrt(n_j)w_j→1 and sqrt(n_j)P_j≥q^(−j)→infinity. The elementary lower bound on P_j gives log(n_j)=O(j²). Thus

    R_(n_j)/(n_j P_j) = O(j³ q^j)+o(1) → 0.

These estimates are consistent: the windows shrink on the quantile-fluctuation scale, while the corresponding cost jump grows without bound on the square-root cost scale. The rank remains fixed throughout; only the observation subsequence changes.

## 5. CLT, bands and the quantifier over all centers

For k_n=floor(nt)+1, the event U_(k_n)≤x is exactly the event Bin(n,x)≥k_n. With x=t+z/sqrt(n), the Bernoulli success probabilities converge to t in (0,1), the variances grow linearly, and bounded summands satisfy Lindeberg's condition. The triangular binomial CLT therefore applies. Its threshold tends to −z/sqrt(t(1−t)); the integer rounding contributes only O(1/sqrt(n)). This independently verifies the claimed order-statistic CLT.

On the n_j subsequence, the three window endpoints, centered at t and multiplied by sqrt(n_j), tend to −1, 0 and 1. Normal continuity gives the same positive limiting probability rho to each window. The high-probability cost event may be intersected with either window by subtracting its vanishing complement probability; independence is not needed.

The profile errors and uniform cost errors are o(P_j). Hence both deterministic bands of radius n_jP_j/8 around n_jA_j and n_jB_j carry at least rho−o(1) probability. Their gap is 3n_jP_j/4. For any fixed M, this gap eventually exceeds 2M sqrt(n_j). Every interval of that latter length, whatever its center, misses at least one entire band. It follows uniformly in the center that its probability is at most 1−rho+o(1).

This is the precise step establishing **every deterministic centering**, not merely the centering at one of the two band locations. In particular, for every M and every deterministic sequence c_n, the liminf along this subsequence of the probability outside [c_(n_j)−M sqrt(n_j), c_(n_j)+M sqrt(n_j)] is at least rho. Choosing any positive epsilon below rho proves failure of tightness. A convergent real-valued weak limit would imply tightness, so weak convergence is impossible.

No conclusion about random/data-dependent centers follows or is claimed. No almost-everywhere or all-nonboundary-rank conclusion follows from one exceptional fixed rank.

## 6. Independent checks and publication recommendation

The submitted verifier was copied with its frozen proof dependency and rerun; its 16,642-assertion receipt is byte-identical.

The independent checker constructs ordered cylinder partitions by interval recursion, evaluates eventually constant profiles by backward affine reward recurrences, checks the sparse rank and subsequence identities, and compares two implementations of singleton-stopping selection on rational sample points with odd denominator. This includes repeated finite prefixes and adaptive stopping depths rather than treating all input prefixes as already distinct. It also checks exact binomial generating-function coefficients and their first two moments. All 44,602 assertions pass with the Python standard library.

Reproduce with `python independent_checks.py` from this directory and `python verify.py` from `author_replay/`. The finite controls do not verify the CLT or infer an asymptotic from a finite sample; Sections 2–5 above audit those arguments directly.

The complete counterexample passes with no required mathematical or source-scope correction. A **claimed_solved** classification is justified for the universal fixed-rank question, provided the already known boundary obstruction, the stronger nonboundary scope of this construction, the lack of a priority certification, and the absence of an almost-everywhere classification remain explicit. The artifact should retain its AI-reviewed and unrefereed qualification.
