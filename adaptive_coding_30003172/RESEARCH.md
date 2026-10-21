# Simultaneous adaptive source coding: scoped research checkpoint

Row 1842; catalogue ID 30003172; source tag OWR14741-004. Prepared 2026-10-21. This is not a resolution of the intended envelope-coding problem.

## Scope contract and recovery gate

Source recovery inspected Boucheron's contribution in Oberwolfach Report 33/2016, printed pages 1921–1925. The catalogue paraphrases a general motivating question, without specifying a collection of classes. The original defines exact adaptivity and also permits a larger, class-dependent factor. Consequently three statements must be kept separate:

1. A blanket assertion for every possible collection of source classes. This is false, even for non-singleton classes with positive bounded minimax redundancy; see Proposition 2 below.
2. Sufficient structural conditions for simultaneous adaptation. Countable aggregation supplies a simple positive theorem when each benchmark diverges; see Proposition 1.
3. Exact or fixed-factor adaptation to the uncountable collection of nonincreasing summable envelope classes, or its regularly varying subcollection. Neither Proposition 1 nor Proposition 2 resolves this substantially different question. The original report does not isolate a single new conjecture with this exact scope.

Throughout the authored arguments below logarithms are natural. Changing to bits scales divergences and benchmarks by 1/log 2 and changes none of the ratios. Write R_n(C)=inf_Q sup_{P in C} D(P^n||Q), and R_n(Q,C)=sup_{P in C} D(P^n||Q). A coding distribution may depend on n, but not on the unknown class parameter. No projective consistency of Q_n is assumed.

## Known imports (not new results)

Ben-Hamou, Boucheron and Gassiat, *Pattern Coding Meets Censoring: (almost) Adaptive Coding on Countable Alphabets*, arXiv:1608.08367v2, Theorems 5 and 6, supplies the relevant benchmark. For positive nonincreasing summable envelopes with total mass greater than one and counting-function regular-variation index in [0,1), the Pattern Censoring code attains a class-dependent O(log log n) redundancy ratio. This is not a fixed factor. The benchmark R_f(n)=(1/2) integral_1^n nu_f(1/t) dt/t is asymptotically exact at index zero; at indices strictly between zero and one, the displayed theorem gives comparison up to constants. Index one is outside the coding theorem. The AC-code result in *About adaptive coding on countable alphabets*, arXiv:1202.0258, establishes adaptation for the more restrictive finite nondecreasing-hazard-rate envelope setting. These imports are not authored improvements.

Public source links:
- https://arxiv.org/abs/1608.08367
- https://arxiv.org/abs/1202.0258
- https://ems.press/journals/owr/articles/14741 (original report; DOI https://doi.org/10.4171/OWR/2016/33).

The counting function nu_f uses the associated envelope distribution: F(k)=max(0,1-sum_{j>k} f(j)), and f_j=F(j)-F(j-1), with F(0)=0. Thus nu_f(x)=#{j:f_j>=x}; these probabilities differ from the raw upper-envelope values at only finitely many indices. Class members are not required to be monotone or regularly varying.

## Avenue 1: mixture oracle costs

### Proposition 1 (countable aggregation; proved here, standard argument)
Let C_1,C_2,... be classes with 0<R_n(C_j)<infinity eventually and R_n(C_j) tending to infinity for each fixed j. For every n,j choose a coding distribution Q_{j,n} satisfying R_n(Q_{j,n},C_j)<=R_n(C_j)+1. For arbitrary positive weights w_j summing to one, define Q_n=sum_j w_j Q_{j,n}. Then

R_n(Q_n,C_j)<=R_n(C_j)+1+log(1/w_j).

Indeed Q_n(x)>=w_j Q_{j,n}(x), hence log(P^n(x)/Q_n(x))<=log(P^n(x)/Q_{j,n}(x))+log(1/w_j). Integrate and take the supremum. Dividing by the divergent benchmark proves exact adaptation for every fixed j. Infima need not be attained because the +1 approximate optimizer suffices. Eventual finiteness implies finiteness at every earlier n by marginalization and monotonicity of minimax redundancy. Nothing is asserted about computational tractability or online consistency.

More generally an oracle error o(R_n(C_j)) suffices. With sample-size-dependent candidate index j_n, both oracle error and log(1/w_{j_n}) must be o(R_n(C)). Pointwise density of candidates does not establish either requirement uniformly over C. Countability alone also does not remove constant cost when R_n(C_j) stays bounded.

Outcome: a rigorous positive partial theorem, not an uncountable-envelope solution.

## Avenue 2: discretization and countable cofinality

A naive countable catalogue of dominating summable envelopes cannot cover all nonincreasing summable envelopes by containment.

### Proposition 3 (no countable coordinatewise-cofinal catalogue)
Let g_m, m>=1, be any countable list of nonnegative nonincreasing summable sequences. Set a_m=2^(-m). Since j g_m(j) tends to zero, choose strictly increasing integers j_m>=3 with j_m g_m(j_m)<a_m. Define h(j)=sum_m (a_m/j_m) 1_{j<=j_m}, and f(j)=min(1,1_{j<=2}+h(j)). Then f is positive, nonincreasing, bounded by one, summable, and sum_j f(j)>2. (Its sum is at most 2+sum a_m=3.) At j_m, f(j_m)=h(j_m)>=a_m/j_m>g_m(j_m); here h(j_m)<=sum a_k/j_k<=1/3. Thus no g_m dominates f.

For completeness, j g(j)->0 follows because (j-floor(j/2))g(j)<=sum_{i=floor(j/2)+1}^j g(i), and the tail sum tends to zero.

This only blocks literal coordinatewise domination by a countable list of summable envelopes. It does not rule out finite-sample approximation, risk-equivalent classes, direct codes, or a cofinal catalogue for a restricted regularly varying subcollection. An alleged impossibility theorem for all adaptive methods would be invalid.

Outcome: a precise obstruction to a common proof shortcut; no global impossibility established.

## Avenue 3: sharp benchmark and quantifier tests

For the reference power tail f(j) asymptotic to c j^(-s), s>1, inversion yields nu_f(1/t) asymptotic to (ct)^(1/s). Direct integration gives R_f(n) asymptotic to (s/2)c^(1/s)n^(1/s). Under the imported theorem this determines the minimax rate only up to multiplicative constants for positive index 1/s. An upper bound with the same order cannot establish exact adaptation without the sharp lower constant.

For an exponential envelope asymptotic to c exp(-b j), b>0, nu_f(1/t)=(log t)/b+O(1), so R_f(n)=(log n)^2/(4b)+O(log n). Its counting index is zero, where the imported equivalence identifies the leading minimax constant. These calculations expose the distinction between knowing a rate and proving a sharp adaptive ratio.

The all-envelope case includes very slow or irregular tails not governed by either calculation. Uniformity in the unknown envelope is not claimed: the question asks a separate asymptotic guarantee for each fixed class, with an envelope-dependent starting time.

Outcome: calibration of two special families; no new lower bound sharp enough to settle positive-index exact adaptation.

## Avenue 4: constructive special-family assembly

Apply Proposition 1 to any prescribed countable list of nondegenerate envelope classes for which finite, divergent minimax benchmarks are available. This gives a single existential coding sequence exactly adaptive to that list, whether or not the individual envelopes share a tail exponent. The list must be fixed independently of the unknown class, and selecting a countable list does not cover an arbitrary envelope by itself.

For example a fixed countable list of exponential envelopes can be aggregated using their approximate minimax coding distributions. This is genuinely an infinite-alphabet result, unlike mixing finite-alphabet KT codes, but it is still only a countable-family construction. The already established AC theorem handles a richer specialized collection; it is an import, not a consequence of discretizing arbitrary envelopes.

A proposed rational grid of power exponents is insufficient for sharp adaptation: replacing s by a fixed smaller exponent s' gives a heavier-tail rate n^(1/s'), whose ratio to n^(1/s) diverges. Taking s'=s'_n requires a quantitative n-dependent approximation and a controlled mixture-description cost; neither is proved here. This identifies a missing estimate rather than claiming approximation cannot work.

Outcome: constructive existential positive subcases and a quantified failure of the fixed-exponent-grid shortcut.

## Avenue 5: generic impossibility and coding-overhead barriers

### Proposition 2 (nondegenerate arbitrary-family obstruction)
On the binary alphabet let P_p be Bernoulli(p), and for p in (0,1/2) set C_p={P_p,P_(1-p)}. Then R_n(C_p) tends to log 2. No coding sequence is adaptive within any finite class-dependent asymptotic factor simultaneously for all these classes.

Proof of benchmark: Q=(P_p^n+P_(1-p)^n)/2 gives redundancy at most log 2 for each of the two laws. Conversely, give the two laws equal prior probability and let Z be their label. For every Q, the average divergence equals I(Z;X^n)+D(M_n||Q)>=I(Z;X^n), where M_n is their mixture. A threshold test on the empirical mean identifies Z with error tending to zero because p<1/2. Binary entropy bounds H(Z|X^n) by the binary entropy of that error, so I tends to H(Z)=log 2. This proves the limit, with positive nonzero benchmark.

Proof of obstruction: For arbitrary Q_n define S_M={p in (0,1): limsup_n D(P_p^n||Q_n)<=M}, for M>=0. Pick any finite distinct p_1,...,p_K in S_M and disjoint small intervals about them. Let A_(i,n) be the event that the empirical mean falls in the ith interval. These events are disjoint and P_(p_i)^n(A_(i,n)) tends to one. Data processing of KL to the event indicator gives

D(P_(p_i)^n||Q_n)>=a_(i,n) log(1/Q_n(A_(i,n)))-h(a_(i,n)),

where a_(i,n)=P_(p_i)^n(A_(i,n)) and h is binary entropy. For every epsilon>0, eventually the divergence is at most M+epsilon, so liminf_n Q_n(A_(i,n))>=exp(-M-epsilon). Let epsilon decrease to zero. Since the events are disjoint, 1>=sum_i liminf_n Q_n(A_(i,n))>=K exp(-M). Consequently every finite subset of S_M has cardinality at most exp(M); S_M is finite. The set of p with finite limsup divergence is contained in the countable union of S_M over nonnegative integers M, so is at most countable.

A finite-factor guarantee on C_p, combined with R_n(C_p)<=log 2, would imply finite limsup D(P_p^n||Q_n). It therefore cannot hold for every p in the uncountable interval (0,1/2). This allows both the factor and the asymptotic starting time to depend on p. It avoids the misleading inference from growing union minimax redundancy alone.

Relevance limitation: the C_p are two-point classes, not envelope classes. This disproves a blanket affirmative answer for arbitrary unspecified collections, not exact adaptation to regularly varying envelopes. It is a scope diagnostic, not a defensible resolution of the source's intended research program.

A separate elementary barrier concerns integer labels. A prefix code with lengths l(j)<=log_2 j+C for all positive integers would violate Kraft, since sum_j 2^(-l(j))>=2^(-C)sum_j 1/j=infinity. Thus completely eliminating all unbounded individual-label overhead is impossible for a standalone integer code. This does NOT prove the log log n adaptive ratio is necessary: joint dictionary coding, source-weighted cancellations, and a different scheme might avoid that loss. No improvement to the PC bound is proved here.

## Audit checklist and disposition

- Generic collection is unspecified: do not assert the source posed an exact theorem for all regularly varying envelopes.
- No singleton zero-benchmark trick was used in Proposition 2.
- All bounds concern expected KL, not pointwise regret.
- Countable mixture cost is constant for a fixed index, not for an n-dependent approximation index.
- The no-cofinality result is for coordinatewise envelope domination, not all forms of adaptation.
- Known PC result is O_f(log log n), not fixed-factor or 1+o_f(1).
- Positive-index minimax comparison is not a sharp equivalent.
- No numerical experiment is evidence of asymptotic exactness; no numerics were required or run.

Recommended disposition: unresolved/scope-limited checkpoint. Five substantive avenues have been explored. Preserve the generic counterexample and countable-mixture theorem as authored partial results; do not publish a claim that the intended envelope adaptivity question is solved. The completed independent adversarial audit accepts these scope-limited partial results; see INDEPENDENT_AUDIT.md.

### Independent audit update

The independent adversarial audit inspected this report and reported that all three propositions, the exponent examples, the Kraft caveat, and the scope verdict pass. Its report is saved separately as `INDEPENDENT_AUDIT.md`. An early-n finiteness clarification was answered using marginalization monotonicity, now stated in Proposition 1. Acceptance of these partial results does not upgrade the envelope-coding problem to solved.
