# Final PASS5 structural and exact-law acceptance

Independent mathematical audit, 14 October 2026, row1778 / problem30005770. The acceptance concerns the precise statements listed below. It is an independent AI mathematical review, not a novelty or human peer-review claim.

## Verdict and uniform-law boundary

The reviewed arguments establish exact state or skeleton encodings, restricted-class growth bounds, conditional concentration estimates, and explicit deterministic obstructions to specified counting shortcuts. None proves the general fixed-alpha diagonal permuton conjecture or the uniform1324 anti-diagonal limit. In particular:

- Canonical path counts retain every directed edge multiplicity and both exterior completion factors.
- Boolean cut profiles decide existence of forbidden occurrences; incoming history multiplicities still count distinct permutations.
- Raw rectangle allocation counts are upper bounds until the actual avoidance indicator is imposed.
- Explicit geometric witness families are not asserted to have positive asymptotic probability.
- The exact uniform denominator is a_n, with lambda^n/a_n=exp(o(n)); it is not replaced by a bounded constant.

The accepted earlier family extensions and the credited previously known family remain separate from these PASS5 partial results.

## 1. Arbitrary-length low-chain runs

Reviewed `pass5_pair_counts/LOW_CHAIN_RUN_THEOREM.md`, SHA-256
`cc9008beda1563339e9f308a2fb1987d38835c1af2c521fb87e7ebb5b7c715fa`.

**Accepted in full.**

For an Av(213) state written L,1,R around its minimum, every L value exceeds every R value. Otherwise l,1,r realizes 213. If its longest increasing subsequence has length at most two, R is decreasing. Recursing on L gives a skew sum of the skew-indecomposable blocks A_p=1 direct-sum J_(p-1), including p=1. Unique skew decomposition makes this an exact composition encoding, with 2^(c-1) states of size c.

The weighted transition estimate uses the actual kernel only through its legitimate binary-shuffle upper bound. With t=C(2z), the exact state sum is

    sum_(c>=1) 2^(c-1) binom(a+c,c)(zt)^c
      = (t^(a+1)-1)/2 <= (t/2)t^a.

For z<1/8 the multiplier t/2 is strictly less than one. The starting-state sum is (t-1)/2; dividing by 1-t/2 gives the displayed finite path bound (t-1)/(2-t). Arbitrarily many cells are included in this argument. Thus growth at most eight is justified, without an equality claim.

The marked-run encoding retains the full prefix path, full restricted middle path, full suffix path, and the two cut shuffle words. The prefix itself identifies the marked location. The middle path already records its number of cells. There is no missing extra factor for the number or positions of its cells. For boundary sizes l,r, the product of lost-edge bounds is at most binom(m+l,l)binom(m+r,r), and the negative-binomial convolution gives binom(2m+l+r+1,l+r). Summing p+q=n-m uses a_p a_q<=a_(n-m), valid by skew closure. This proves the finite count used by the exponential theorem. Its small-boundary condition is essential.

The exact dense-edge formula also checks. For p,q>=2, every upper ascent in A_p starts at its first point, and every lower ascent in S(A_q) ends at its last point. Greediness forces that lower maximum between the first and a later upper point. Any lower point before the first upper would complete a 1324 with this witness. Hence the allowed words are exactly those beginning and ending U. There are binom(p+q-2,q) of them. Each lower contributes a pair with the final upper, while its expected number of later middle uppers is (p-2)/2. The exact mean cross count is pq/2. The conditional uniformity statement is valid only because a fixed canonical state chain has a Cartesian product of its genuine edge-shuffle choices. It is not a uniformity assertion about the state chain itself.

## 2. Height-three exact rows and size-weight limitation

Reviewed `pass5_pair_counts/HEIGHT_THREE_SIZE_WEIGHT_BARRIER.md`, SHA-256
`4423d6d5870b46781004ee7642a26fde62e7b03d0c619fd74487cdd22abdbf59`.

**Accepted in full.**

The minimum decomposition gives F_h=1/(1-x F_(h-1)), and the stated F_3=(1-2x)/(1-3x+x^2) and positive partial fractions follow. Its coefficient bound s_c<=kappa^(c-1) is valid, including c=1. The same binary-shuffle majorant gives a strict weighted contraction t/kappa<=2/kappa<1 even at z=1/(4 kappa). This is an upper bound on total restricted-path growth, not a lower bound.

The exact row formula uses additional genuine geometry. An Av(213) skew-indecomposable block must begin with its minimum; otherwise the part preceding that minimum is an earlier skew component. If the first block of C has size d and total size q, then C_1=q-d+1, so the maximum of S(C) occurs in position d. For upper A_p, the first letter is again forced to be U. With that condition, every possible cross1324 is excluded; greediness is exactly the requirement of some later U after the d-th lower. The nongreedy words are counted by binom(p+d-2,d-1). This proves the exact subtraction, including q=1 and d=1.

Decomposing C into its first block and skew suffix correctly produces the factor x F_3(x), the H_2 coefficient sequence, and the displayed half-sum [1+(1-2x)^(-p)]/2. For fixed 0<x<1/kappa the positive (1-kappa x)^(-p) term has strictly larger exponential base than all subtraction terms. If zt>=1/kappa, each row diverges since every C has at least one allowed shuffle with A_p. Otherwise the row norm along A_p grows with base 1/[t(1-kappa zt)]. For z>1/(4 kappa) this exceeds one for every positive t. The claimed obstruction is therefore genuinely about the actual kernel and exactly about pure exponential size weights. It gives no lower bound on restricted-path growth and does not rule out shape-dependent weights.

## 3. Exact occupied-to-empty rectangle reduction

Reviewed `pass5_pair_rectangles/RECTANGLE_DELETION_AND_ENTROPY.md`, SHA-256
`990442ebcdd9866c6df9f1ddd127bfa36a31a399c5ddd965a1020ebfdab7a373`.

**Accepted in full.**

The interior of an increasing-pair rectangle in a1324-avoider is increasing, since an interior descent would combine with its endpoints into1324. Deleting that interior leaves the full marked skeleton, and its open position/value interval counts are exactly p and q. Choosing m of the m+p position slots and m of the m+q value slots, then matching increasingly, reconstructs a unique candidate. Every surviving point remains outside at least one endpoint interval. Consequently the reconstruction has exactly the designated interior, without extra hidden points.

The exact identity properly sums the actual avoidance indicator over allocation records. The displayed 31524 to314625 example verifies that not all allocations preserve avoidance; the latter contains the subsequence1,4,2,5. Thus neither independent allocation sampling nor equality with the raw binomial product is justified, and the note does not claim either.

The uniform entropy tail sums at most (n+1)^3 statistic triples, retains the full skeleton count a_(n-m), and divides by a_n. All marking and location factors are polynomial. The contamination corollary uses concavity to bound E by m log(27/4), then the already established strict two-cell growth gap. This is a conditional rare-event theorem only: large interior alone does not imply its favorable score.

## 4. Actual canonical comb obstruction

Reviewed `pass5_pair_rectangles/COMB_RECTANGLE_OBSTRUCTION.md`, SHA-256
`cabf1788cc22562cc3ba8ffb3feaf81298c9fc1b89db99d76d321e4b8714cea3`.

**Accepted in full.**

Every descent in a comb starts at a high tooth with no later larger value, excluding213. Increasing pairs and subsequences can contain at most one tooth; the stated exact pair count and LIS follow by summing over the low anchors. The ascent bridge is a genuine directed kernel edge, so the mountain is realized by its exact canonical cells rather than an arbitrary gridding. For these combs, S(C)'s maximum is last, and the particularly simple bridge U L^b U^(a-1) applies.

For a same-cell pair, all interior points are low anchors. If the upper endpoint is a tooth, the last interior anchor may lack its whole following tooth block, but the complete tooth block after the first endpoint compensates. When that endpoint block could coincide with the upper endpoint's block, there are no interior anchors to charge. This handles the endpoint issue and proves the stronger same-cell contamination bound Lm.

For adjacent cells, normalize to a vertical upper comb and lower reflected comb. All upper interior points are southwest of the upper endpoint and are anchors. All but possibly the last have complete tooth blocks in the open position strip above that endpoint. Reflection gives the dual bound for the lower interiors in the open value strip. The two charged sets are in different cells. Rectangle locality excludes a third cell. Therefore p+q>=L(m-2)_+ is valid for every increasing pair, in either staircase orientation.

For L=5,m>=20, concavity/subadditivity of H gives E>=m H(9/2)>m log(27/2)>=m log(lambda). The strict comparison is exactly 11^11>3^24. This blocks the raw-allocation score simultaneously at every occupied rectangle above the fixed threshold, not just at one chosen window. The central state's positive LIS and increasing-pair mass verify that the witnesses themselves do not approach the anti-diagonal. They do not imply a positive probability under the uniform law. Exact allocation admissibility could still make the corresponding family exponentially negligible.

## 5. Complete coarse-grid branch coverage

Reviewed `pass5_pair_rectangles/COARSE_RECTANGLE_DICHOTOMY.md`, SHA-256
`489d88735bac14ca612105f8e34682dbdfabd7fc554d4251b213d6f31b4dda2b`.

**Accepted in full.**

After discarding pairs with position or value separation at most2n/Q, at least epsilon*n^2/2 remain. Same or adjacent half-open bins cannot contain a retained pair. Pigeonholing into at most Q^4 cell pairs gives the claimed product population. All pairs in the selected southwest/northeast cells are increasing.

The chosen half-open common core lies strictly inside every such pair's open rectangle, even if a point center is exactly on a grid line. Any interior point outside the core lies in one of the two endpoint columns or two endpoint rows. Each strip contains at most ceil(n/Q) points. The explicit Q>=8/theta and n>=8/theta imply 4ceil(n/Q)<=theta*n, proving both branches with their strict inequalities. This is a fixed finite family of regions, with constants chosen before n grows.

The occupied branch supplies no contamination bound. The sparse branch remains necessary: J_a direct-sum J_b has exactly ab increasing pairs, all with empty interiors. Thus the argument covers the geometry completely but does not silently infer probability suppression in either remaining branch.

## 6. General-alpha exact diagonal-cut states

Reviewed `pass5_general_cuts/EXACT_CUT_STATES_AND_CONTEXT_OBSTRUCTION.md`, SHA-256
`01040a02521559ea6015e1928db860c7d6921f288b23cb356b8948ac0afa4fbc`.

**Accepted in full.** The state theorem is the key structural dependency; the following checks are essential.

A closed-point descriptor retains the pattern and the row/value strip of each selected point, not merely strip totals. For any new forbidden occurrence, at least one point is outside the previously known tau-free configuration, so at most m old closed points are used. Row strips preserve their comparisons with B; value strips preserve their comparisons with D. All closed points precede D and future northeast points, and lie below B and future northeast points. Replacing the closed selection by an equal descriptor therefore preserves every comparison needed by the occurrence. Existence bits suffice for this avoidance test, although not for counting histories.

The five next-index cases are exhaustive. If the next row or value closes an old endpoint, it must be the least endpoint in its retained future order. Otherwise a new endpoint is inserted with one of the displayed ranks. When both next row and next value are unassigned, there are exactly the diagonal alternative or two new crossing points. These are not independent choices that might accidentally assign one coordinate twice. The cases and insertion ranks uniquely recover the full permutation once all endpoints close.

Closing an old boundary point is reclassification, not a newly exposed point; it alone cannot introduce a forbidden occurrence. At most two points become closed at one step. A closing B point has an old row cut and a value above all old closed values; a closing D point has the dual configuration. Old cuts only disappear and merge strips, while openings create exterior cuts. Thus the old profile determines every new descriptor, with no internal refinement requiring hidden coordinate data. The converse realization is also valid: combine any old witness with the chosen newly closed points. This validates the time-homogeneous quotient, including states reached by histories of different lengths.

Finite width gives finitely many endpoint orders and profiles. Exact transition multiplicities must be retained even when different choices reach one compressed state. The transfer correctly accepts every width-zero terminal profile, not only the initial profile. Therefore the rational generating function counts actual permutations exactly.

For the strict gap, the extra width-(K+1) sum-indecomposable blocks are valid: I_(K+1) skew-sum I_(K+1) has one descent, while tau has at least two for nonincreasing alpha; taking a subsequence cannot increase the number of descents because each selected descent charges a disjoint interval containing an original descent. For increasing alpha of length at least two, the displayed decreasing block avoids tau's ascent. Both have exactly width K+1 and are sum-indecomposable. Adjoining this block to the unique direct-sum decomposition is an injective subclass count. Rationality and the positive pole imply the strict radius improvement. Exhaustion by arbitrary fixed-size blocks gives sup lambda_K=lambda; no rate follows.

The width-one context example also checks. The final1 makes tau-avoidance equivalent to alpha-avoidance of the preceding part. Its leading maximum cannot occur in alpha=2143. The remaining parts are respectively12 direct-sum sigma and21 direct-sum sigma. Their completion classes are exactly Av(2143) and the singleton increasing permutation. Skew sums of increasing blocks give the asserted exponential positive completion ratio. This is a genuine loss of information when the profile is omitted, not a uniform-law counterexample.

## 7. Folding collisions

Reviewed `pass5_collective_windows/FOLDING_ENTROPY_OBSTRUCTION.md`, final corrected SHA-256
`0241b9c09b2a20390289479200a33fedadd2037e3751c0cb0ac03c90d798430c`.

**Accepted in full at this corrected pin.** The earlier version needed a distinction between source coordinates and folded-output markings; the final derivative makes it explicit and supplies the appropriate source-record count.

Reverse-complement maps a vertical D(A,C) domino to D(C^{-1},A^{-1}), with the word reversed and colors exchanged. The inverse normalization is necessary. Source active levels are nonadjacent, so every edge has at most one extra singleton. ULLU and the two possible single-letter appendings are genuine K edges with the required lower-maximum witness. The state identity (12 skew-sum1) skew-sum12 = 12 skew-sum(12 skew-sum1)^{-1} is exact. On either incident edge the extra switches color under reflection, so moving it from the up piece to the down piece leaves w X bar(w) unchanged.

Within-color skew order prevents new ascents spanning the concatenated pieces. Therefore the folded words give valid unrestricted D edges. The reflected piece need not itself be greedy, which is why the subsequent accepted D-to-K guard is retained. Shared turns are duplicated once per additional use: R upper turns and R-1 interior lower turns, each of size two, produce exactly4R-2 extra points. The state guard adds2W more. All2^(Ra) source bit choices remain distinct canonical paths of the same size and have one common folded output.

The full fiber statement remains exact with the specified folded-output markings. Original source coordinates are not identical in general. If all original turnaround coordinates are also retained, the2R+1 source turn cells are pairwise nonadjacent and each has pattern12; their induced pattern is fixed in skew order. Thus choosing their4R+2 positions and values gives at most binom(n,4R+2)^2 records. Pigeonholing proves the weaker displayed fiber bound with these records included. Its entropy subtraction is2h(4/(4W-4+a)), tending to zero as W grows, so the stated limiting positive rate log2/9 survives. This repairs the metadata issue without a claim about every possible folding map or the probability of the source family.

## 8. Independent finite diagnostics and source boundary

The independent scripts in this audit folder test the exact bulk edge formula and reconstruct the actual comb paths, independently peel their greedy cells, and inspect every increasing-pair rectangle. The bulk check covers28 endpoint pairs and1920 binary words. The comb check covers L=2,5 and s=1,...,5, including n=552 with53716 increasing pairs and24243 interiors of size at least20. These finite checks support indexing and regression only; the all-size proofs above carry the mathematical conclusions.

The primary numerical inputs used by these notes are the previously inspected Bevan--Brignall--Elvey Price--Pantone staircase bounds and exact domino calibration. Their public primary source is https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf. The retained primary PDF has SHA-256 `1264749e17f01005277e8acf1a7782e6c4e448fe1733ac6fbb29ec8bd125f26d`,627368 bytes. Its Theorems8,9,16 and the earlier fixed-width calibration are used only for their stated rigorous bounds. No guessed latest bound or conjectured growth constant is used. No third-party source text is reproduced in this audit.

## Closing scope

The unrestricted exact uniform problem remains open in this pass. Small fixed crossing width is exponentially atypical, but this says nothing decisive about width/n. Low-chain runs with small boundaries and low-contamination occupied rectangles are exponentially rare, but their complementary events are not controlled. The explicit comb and folding families diagnose particular lost information; they are not probability counterexamples. 
