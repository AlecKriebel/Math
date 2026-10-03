# Frozen PR375 probability audit verdict

Frozen head: `36c29bb039471f132889d577c9322d78925b62dd`. Scope: literal model, lower bound, zero-one structure, bounded-support stabilization, and probability/moment claims across later turns. This verdict is sealed before historical review or its independent checker is consulted. The source-first proof/control seal preceded all candidate access.

Disposition: accept the mathematical claims in this probability scope as partial results, with the declared unresolved quantitative status. No mandatory candidate correction has been identified. This is not a novelty certification, a full audit of every external proof, or a claim that the underlying open problem has been resolved.

## 1. Literal question and credited source input

LITERAL_COROLLARY.md is correct. The supremum over all x is infinite almost surely; each fixed r_A(x) is finite. Its proof needs only increasing M(D) and divergence in probability, not independence between different D. The candidate correctly distinguishes an unbounded collection of finite values from a finite attained maximum, and separates this credited corollary from the finite-prefix growth target.

SOURCE_SCOPE.md correctly names independent Bernoulli probability 1/i, finite subsets, the surely selected element 1, and the empty subset. It labels log M(D)/log log D as a precise interpretation rather than pretending the OWR source mandates this exact normalization. FGK Lemma 2.1 and its remark already address prefix growth in probability; the candidate credits that precedent. Its eta input remains an external published threshold theorem, not a numerical test or independently reconstructed full FGK proof.

## 2. Turn 1: lower bound, amplification, tail law, cutoff

The annuli are disjoint because of the explicit half-open convention. At their lower endpoint, the possible difference from the source closed interval is selected with probability at most D^{-c}; this vanishes for fixed positive c. The supremum beta_k need not be attained: downward closure gives every fixed 0<c<beta_k. Positivity is the credited input. The preliminary beta_k<=2/3 union bound is valid: each valid signed assignment determines its largest entry, and its support entries are distinct before independence is used.

The rate-free strong law using square subsequences is sound. Var S_n<=n/4 implies summable Chebyshev probabilities at n=m^2; the Cesaro mean tends to one, and monotonicity fills the gaps. It proves the almost sure lower exponent on all prefixes after monotone interpolation; it does not infer almost sure eventual success from arbitrary probability-to-one statements. My independent proof used Hoeffding on the same deterministic independent annuli and reached the same bound before candidate exposure.

The claimed identity zeta_*=zeta_+ is valid. For fixed r, split a large annulus into r annuli with parameter c<beta_k, take a finite union bound, and tensor their equal-sum families. This gives beta_{k^r}>=beta_k^r after c increases to beta_k. Each fixed-k ratio recurs as a lower bound along k^r, so its supremum equals the large-k limsup. No estimate uniform in r or k growing with D is inserted. This identity identifies variational expressions and does not evaluate them.

The finite-modification comparison is correct and makes each normalized liminf/sup a tail random variable. Kolmogorov makes each individually deterministic, allowing infinity; it does not establish convergence, equality, or finiteness. The element-prefix/sum-prefix comparisons use positivity and a deterministic D(D+1)/2 bound. Their slow log-log normalization yields the stated common liminf/sup and finite in-probability limits; lower-order distributions are not equated.

## 3. Turn 2: signed relations and fixed cardinalities

The relation must first cancel common elements. Its largest and second-largest entries obey n>=m/(ell-1), and the second-largest entry is determined uniquely by the other entries and signs. The bound (4) has the right m^{-2} saving and factorial denominator. The dyadic fixed-length tail constant is allowed to depend on ell; it is not silently made uniform.

The separate growing-length calculation retains the factorial. With L=floor(c log(2D)), u=1+log(2D), the bound has logarithmic rate -1+c log(2e/c). The root condition is sufficient rather than optimal. Since the resulting probabilities are summable on dyadic scales, Borel-Cantelli I applies without relation-event independence. c=1/4 is certified by (1+3log2)/4<1. This controls the maximum differing support entry, not a common element adjoined to an old relation.

The finite collision core proves the candidate's at-most-h conclusion. A bounded nondecreasing integer sequence eventually stabilizes. The same reasoning applies to exactly-h maxima: they too are bounded nondecreasing integers. My independent derivation additionally identifies their eventual value as max_{0<=j<=h} M_j(C), where C is a finite collision core, using infinitely many outside elements to complete core families. Thus the broader wording "fixed-cardinality" in RESULT/state files causes no unsupported extension. No bound for unrestricted cardinalities follows.

## 4. Cross-boundary Turn 3/4 probability logic

I read the full later-turn proofs to check whether they invalidate or overstate earlier probability conclusions. The diagonal flag counting claims are internally consistent on the inspected steps. Decreasing exposure supplies the support condition, including rounded threshold ties. Residual assignments are counted modulo the diagonal; assignments inside one diagonal coset give the same residual sum. Recorded vectors independent modulo the diagonal imply unique reconstruction. The exact deletion ratio is product 1/(K_j-1), applied only to distinct recorded entries absent from the residual realization. Summing residual Bernoulli probabilities bounds the mass without asserting that deletion preserves the residual law.

Turn 4's cube/quotient count uses at most 2^{j+1} cube points and saves one for 0 and 1 in the same coset. The summation-by-parts error is (u+2)h_t, avoiding an incorrect extra factor t. The coefficient increments after the first are bounded by log(7/3)<1; their negative signs give the correct maximizing choice c_j>=c. Its q=c log D-R guard controls the geometric sum explicitly. The growing k and u in Turn 4 satisfy t_0 R=o(log D), b=o(log D), and q->infinity. The bound is summable on dyadic D and the count law applies along D^{c(D)}->infinity. It yields the stated upper normalization C_*=(log3-1)(log2)^2 in (0.047,0.048), which does not bound log M(D)/log log D by a finite constant.

This diagonal-only argument does not depend on a classification of every rational subflag or on Mao-Song's claimed weak/strict threshold equality. It is not licensed to recover a sharp prefix exponent merely from exact fixed-k thresholds. My family audit is not a standalone novelty claim for the upper argument; its mechanisms are explicitly credited to FGK.

## 5. Turn 5: annealed moments, rare tails, logarithmic moments

The tilt dQ_lambda/dP=lambda^N/Z_lambda is valid on the support of the original distribution, including the deterministic first coordinate. The tilted Bernoulli probabilities are lambda/(i+lambda-1). The pigeonhole bound M>=2^N/(S+1), the convex inverse-power Jensen step, and E_Q S<=lambda D all have the claimed directions. Z_4(n)=(n+1)(n+2)(n+3)/6 gives the stated lower constant 1/96 after dividing the squared denominator and taking n->infinity. It is a lower constant, not the true moment constant.

The raw exponent 2^q-1-q is positive for all q>1 and need not be positive for all q>0. Polynomial raw moments coexist with almost sure subpolynomial maxima because there are rare heavy tails. Under a fixed tilt lambda>(1+gamma)/log2, the high-probability N band and the S<=4lambda n bound intersect with probability at least 1/2; lambda^{-N} is bounded below by using the upper N band. This yields the lower probability rate in the stated direction. The parameters remain fixed in each limit, and the real-D argument uses gamma'>gamma before flooring. A polynomially small lower tail does not imply a positive limiting tail probability or contradict almost sure typical growth.

For the larger logarithmic normalization, almost sure bounded limsup alone would not bound moments. The candidate instead splits off the explicitly controlled annular bad event, uses Bernoulli fixed-moment estimates and Cauchy-Schwarz, and obtains a negligible exceptional expectation. The good-event bound converges in every fixed L^r. Thus its all-fixed-logarithmic-moment upper claim is supported without claiming convergence on the unresolved log-log normalization.

## 6. Independent controls and scope of replay

- Before candidate access: 17,932 exact assertions in `independent_controls.py`, including exhaustive A subset [10], finite collision-core maxima, coefficient convolution, disjoint tensor products, ordered harmonic-composition identities, and explicit counterexamples to unjustified probability-mode/exponent inferences.
- After candidate access: a separately written exact probability/tilt control enumerates all Bernoulli prefixes [n] through n=10 and verifies the full tilted moment identity as well as its lower bound. Disjoint equal-sum side pairs through maximum 12 independently verify the second-largest first-moment bound. Exact atanh intervals enclose C_*. `{1}` and `{2,3}` falsify a multiplicative upper bound, since component maxima are one and the union maximum is two.
- All five frozen candidate checkers were copied into ignored own `tmp/candidate`, run there, and matched their exact JSON receipts: 57,418 + 41,951 + 26,536 + 8,202 + 16,818 = 150,925 assertions. Full stdout/stderr streams and hashes are saved. No source absence is reported as source revalidation.

Controls verify finite identities and evidence continuity. Infinite strong laws, Borel-Cantelli conclusions, and zero-one statements are justified by the written arguments, not by assertion totals.

## 7. Fresh recent-source boundaries

Fresh direct downloads confirm Mao-Song [v2](https://arxiv.org/pdf/2609.22296v2) is 81 pages, dated 27 September 2026, and claims fixed-k alpha/beta and weak/strict entropy equalities. I inspected the introduction and statements to establish this boundary, not the entire long proof. These are recent preprint claims; none has been promoted here to a verified prefix theorem. Its reported local corrections motivate scrutiny of general residual-support/subflag arguments; the candidate's diagonal-only argument explicitly supplies its own support condition and exact weights.

Fresh de la Breteche-Tenenbaum [author PDF](https://tenenb.perso.math.cnrs.fr/PPP/Delta%28n%5Er%29.pdf) is 13 pages with a printed 8 September 2026 timestamp. Its introduction gives an ordinary-divisor normal-order gap and results for powers/polynomial values. Neither is automatically a statement about M(D). No divisor-to-prefix transfer has been assumed.

The fresh OWR and both FGK PDF hashes match the frozen source manifest, as do both recent PDFs. All raw PDFs and extracts remain ignored private files. There was no external communication, remote/service mutation, branch change, or Git/index mutation.

## 8. Mandatory fixes, promotion limits, remaining gap

Mandatory mathematical fixes within this probability scope: none. A useful nonmandatory note is the visible reversed beta monotonicity typo in both FGK Corollary 1 proofs; the candidate's reasoning uses the correct direction and is unaffected.

Strongest scoped result: valid almost sure lower exponent at zeta_+>=eta, deterministic extended liminf/sup, finite stabilized fixed-cardinality maxima, and correctly separated later upper/moment probability modes. Exact gap: no finite/equal leading liminf/sup, no identified sharp exponent, no in-probability convergence of log M(D)/log log D, no finer limiting law, and no new certified eta improvement. Keep `unsolved` and `complete_quantitative_resolution=false`, preserve source credit and recent-preprint qualifications, and do not create a paper/DOI for this audit.

Checkpoint: 2026-10-03 06:59 UTC (exact seal time in JSON). Audit completion estimate: 85%. This verdict precedes consultation of the historical review and checker; that material may only corroborate the independently reached disposition.
