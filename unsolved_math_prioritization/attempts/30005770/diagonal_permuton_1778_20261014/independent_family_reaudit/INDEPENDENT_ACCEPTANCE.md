# Independent re-audit of the two permuton families

Date: 14 October 2026. Decision: **ACCEPT the three pinned proofs for their stated fixed-pattern scope.** No mathematical defect or unresolved proof obligation was found in that scope. This is a fresh mathematical QA review of completed PASS1–PASS2 results, with **zero additional research passes**. It is not a novelty assessment, literature-exhaustive openness claim, or human peer review.

## Exact accepted statement

For each fixed integer r ≥ 0 and either

- α = 132 skew-sum J_r, or
- α = 213 skew-sum J_r,

the exactly uniform permutation in Av_n(α skew-sum 1) has the diagonal square-spread permuton limit. For every fixed positive bounded-Lipschitz deviation, its probability is at most C exp(−cn) for suitable positive constants depending on the pattern and deviation, for all sufficiently large n. Here J_0 is empty. Equivalently, uniform avoiders of I_d direct-sum 231 have the anti-diagonal limit with the same kind of tails for every fixed d ≥ 1.

The universal fixed-α target remains **UNSOLVED**. In particular, this audit supplies no result for α = 312 / forbidden pattern 4231. There is no growing-pattern claim, uniform rate over the family, maximum-displacement conclusion, or almost-sure coupling assertion.

## Frozen inputs

All SHA-256 values were checked before testing and again when sealing this report:

- `pass1_uncovered_case/TWO_SUBCASE_THEOREM.md`: `3afd21739fdb296393c21cc232130d94315d035434d98f7cb6e07b670a9af7ce`
- `pass1_entropy/KERNEL_ENUMERATION_APPENDIX.md`: `a57401941f3ec1296e7880d791a495c4daec92d8c714e92435c1e73d443c5181`
- `pass2_protected_tail_extension/MERGE_TRANSFER_THEOREM.md`: `d8a88fb75f5f2c78509e0610420cb8701d5445de0ae1be856d2c0e0b9d919d34`

The target specification and proof statements fixed the question. Earlier acceptance assertions were not used as evidence of correctness.

## 1. Source convention and the exact labeled law

I inspected the primary [Bóna preprint, math/9702223v1](https://arxiv.org/pdf/math/9702223): the decomposition definition, Definition 1, Lemma 2, normalization definitions/propositions, Theorem 1 and Corollary 2. The relevant decomposition is skew decomposition. The source's child-before-parent traversal is postorder in standard terminology, although it calls it preorder. The shape is constructed from the normalization retaining both positions and values of left-to-right minima. The root-sum rule, zero leaves, vertex size, and singleton convention agree with the audited proofs.

The exact bijection, not a Wilf-count identity, is the credited external input. Its shape preservation provides the geometry; its bijectivity supplies the uniform labeled law. Arbitrary ordered sequences of proper trees correspond to skew components. The induced shape probabilities count all admissible labelings, rather than giving equal probability to unlabeled shapes.

As a separate regression, the new checker reconstructs the forward reachability-label map with the specified root-sum rule. Through n = 8 it checks validity and injectivity of every indecomposable image, matches its image count to an independently enumerated set of admissible labeled trees, and matches every ordered forest shape's permutation multiplicity to the product of its components' labeling counts. At n = 8 this includes all 15,485 avoiders, all 1,430 forest shapes, and 9,152 distinct indecomposable labeled images. These are substantially stronger checks than matching total Wilf counts, but are still finite checks rather than a replacement proof of the credited bijection.

The old preprint's displayed indexed counting formula and full-series denominator conflict with its own conventions/formulas. The independent kernel appendix removes their role as enumerative assumptions. This audit makes **no assertion that the publisher's final version contains those errors**; the full mathematical source inspected here is the pinned preprint.

## 2. Catalytic enumeration and analytic branch

The proper/relaxed distinction is correct. A proper root has one label after choosing its ordered relaxed children, giving T = z/(1−B(z,1)). A relaxed singleton has only label zero; a nonempty child sequence with total root-label sum S permits precisely 0 through S+1 at its parent. This gives the stated polynomial catalytic equation without an illicit substitution at u = 1.

The appendix's formal kernel construction is valid: coefficient polynomials allow composition at U(z) with U(0)=1; the formal implicit function theorem applies because the u derivative at the base point is −1. Differentiating the catalytic identity and evaluating at the kernel gives P = P_b = P_u = 0. Direct symbolic verification confirms the elimination identities. The factor discarded in the elimination has constant term one, and cancellation of the nonzero series β takes place in an integral domain. The correct branch has β(0)=0. Consequently the derived T, vertex indexing, coefficient formula, critical value T(1/8)=5/32, and asymptotic constant 3/(16√π) are correct.

For b(z)=B(z,3/2), the displayed algebraic solution is the branch with b(0)=0. Its positive-real discriminant is nonzero before 1/8. The proof correctly first obtains a positive radius by the analytic implicit function theorem, then uses nonnegative coefficients and Pringsheim to exclude any smaller radius. Thus the evaluation is justified for every 0 ≤ z < 1/8, rather than merely assumed from a formal expression. Monotone convergence gives b(1/8)=1/4, and positive coefficients imply strict inequality below the endpoint.

Independent symbolic expansion, with t=(1−8z)^(1/4), gives

- b = 1/4 − (√6/4)t³ + (3/8)t⁴ + O(t⁵);
- M = 1 − (2√6/3)t³ + O(t⁵).

These verify, and are consistent with, the slightly weaker remainder estimates used in the proof. No competing algebraic branch is being selected at the critical endpoint.

## 3. Marked depth, forest height, and weak geometry

The marked-depth estimate correctly retains all labels. For an internal vertex, summing its allowed u-weights is bounded by u^(S+2)/(u−1). After distinguishing a child, the sequences on its two sides give the factor (1−B)^−2. Hence W_(h+1) ≤ M W_h at u=3/2. Each W_h is finite at subcritical z because its coefficients are bounded by those of z∂_z B. This avoids circularly assuming the marked series converges.

A proper tree is an injectively included relaxed tree with the same labels, and its root weight is at least one. The resulting count bound does not identify the two random laws. Since M has defect of order (1−8z)^(3/4), for every ε>0 one can choose a *fixed* z<ρ with log(ρ/z)+ε log M(z)<0. The negative fractional-power term dominates the positive linear term. Coefficient extraction and the exact t_n asymptotic therefore give an exponential linear-height tail after absorbing n^(5/2).

For forests, marking one component gives A(z)^2 W_h(z,3/2); the unmarked components remain proper trees. A(z) is finite subcritically, and the exact uniform-forest denominator satisfies a_n≥t_n. The height argument therefore transfers without an assertion about giant components, conditional independence, or uniform Catalan shapes.

The leaf identity i+q_i=k+1−depth follows from the specified child intervals and postorder recursion. Preserved minima imply the one-sided component envelope, and skew shifts align it globally as i+p_i≥n+1−H. The square-spread correction is exactly the stated extra 1/n. Uniform marginals give zero mean for X+Y−1, so the one-sided bound yields E|X+Y−1|≤2(H+1)/n. The coupling to (X,1−X) then proves the bounded-Lipschitz bound. No individual-point two-sided bound is needed. Reversal and inversion are exact finite-class bijections and the indicated square isometries.

## 4. Merge transfer and starts-with-1 restriction

I inspected [Bóna, math/0403502v2](https://arxiv.org/pdf/math/0403502v2), Proposition 5.1, Lemma 5.3, Theorems 5.2 and 5.4, and the preceding growth construction. Theorem 5.4 inherits precisely the starts-with-1 hypothesis stated by the audited proof. The matching growth equality is a credited enumerative input, not a geometric theorem.

For such q, skew-closure and supermultiplicativity justify a_k≤λ^k at every size. Deleting left-to-right minima gives the stated avoidance equivalence: the first entry of a surviving q occurrence is its minimum, so an earlier smaller entry extends it to 1 direct-sum q. Conversely, a q portion within a 1 direct-sum q occurrence has no global minimum entries. Position set, value set, and standardized remainder reconstruct the permutation uniquely.

The proof uses independent subsets only in the unconditioned ambient triple model. The actual class is injected into it. Its total count is at most (1+√λ)^(2n), while the actual class has that same exponential growth rate. Thus the eventual denominator comparison costs only exp(o(n)); no invalid conditioned-independence assertion is made.

The deterministic merge bound is correct, including the 1/n center correction and the k=0,n endpoints. The complementary subset has the same prefix discrepancy. The two groups' weighted center errors sum to 2(E(P)+E(V))/n+1/n. The bounded-Lipschitz/transport comparison uses the correctly normalized 1-Lipschitz test function |x+y−1|/√2.

The sampling-without-replacement Doob increment is (n−k)/(n−r) times the centered next draw; its absolute value is at most one. Azuma and the two union bounds yield the claimed uniform discrepancy tail, including deterministic endpoints. On good allocations, a bad merge requires k>εn/2 and a fixed positive deviation of its remainder. Counting bad ambient encodings, then dividing by the *actual* avoidance count with a chosen smaller exponential loss, proves the transfer. Small k need no asymptotic concentration assumption.

The starts-with-1 restriction is substantive: for q=21, the permutation 3412 avoids 132=1 direct-sum q while its non-minimum remainder is 21. The independently checked counterexample illustrates why the audited argument correctly excludes that extrapolation. Iteration applies to each fixed I_d direct-sum 231. The stated reversals/inverses give exactly the two accepted target families; no seed for α=312 is supplied.

## 5. Reproducible checks and boundaries

`check_family_proofs.py` is newly written for this audit and imports no author or prior-review checker. Its explicit failure checks remain active under optimization. All three runs passed:

- `python check_family_proofs.py`
- `python -O check_family_proofs.py`
- `python -OO check_family_proofs.py`

The matching result files are `CHECK_OPTIMIZATION_0.json`, `CHECK_OPTIMIZATION_1.json`, and `CHECK_OPTIMIZATION_2.json`. Coverage includes:

- every 1342 avoider through n=8: exact labeled/forest-shape law and geometric envelopes;
- independent plane-shape tree enumeration through n=9, closed-form coefficients through n=30, exact symbolic kernel/branch identities, and 80 exact marked-depth coefficient inequalities;
- minima deletion and reconstruction for all permutations through n=7 and all nine starts-with-1 patterns of lengths 2–4: 53,217 permutation/pattern pairs;
- the merge inequality for every ambient triple through n=7, with arbitrary remainder permutation, including both endpoint cases: 146,047 triples.

The asymptotic acceptance rests on the preceding mathematical audit, not on these finite computations. Source PDFs/text have not been copied into this deliverable or republished. Only public source metadata is recorded in `SOURCE_PINS.json`. No frozen proof correction is required by this review.
