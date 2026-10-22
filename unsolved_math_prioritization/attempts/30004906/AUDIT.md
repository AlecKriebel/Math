# Public independent mathematical audit: target 30004906

This unrefereed review edition records an internal AI audit. It has not received human peer review or formal proof-assistant certification. It is not a computational reproduction package. The unrestricted target remains unresolved by this work. AI tools were used in research, drafting, and checking. No novelty or present-day openness certification is claimed.

This report preserves the complete independent mathematical review. Its authentication, source inspection, and test-execution statements describe the historical audit. The full independent proof supplement is reproduced verbatim in Part III of PROOF.md.

# Independent audit: nonsymmetric determinant rank boundary

Target: 30004906 / OWR-8415356-017.

## Verdict

**ACCEPT the claimed partial results, with the finite-encoding proof supplement supplied here. No claim-breaking mathematical error was found.** The supplement makes the polynomial-bit PSD optimization step explicit; it is not a correction to the reduction or approximation factor. The original unrestricted target remains unresolved in this work. This is an independent mathematical and exact-arithmetic audit, not human review, formal verification, a novelty determination, or a certification of current openness.

The accepted statements are:

1. For rational accretive L with rank L<=k+1, deterministic polynomial-bit approximation with ratio at most 2h k^k/k! in the rank-(k+1), h=rank((L+L^T)/2)>0 case. The rank-k case uses one Gram objective; rank<k and the stated skew zero branch are handled separately. In particular an absolute 2^O(k) ratio follows.
2. For each fixed integer radius rho>=1, an infinite rational, strictly accretive, genuinely nonsymmetric family has strict rho-local maxima with gap at least (4k/(17rho^2))^k along unbounded powers of two k. This is a limitation of arbitrary constant-radius local optima, not of all algorithms or of the cited initialization.
3. The direct second-compound PSD extension fails: the supplied strict-accretivity example has the claimed negative quadratic value -6. The single-Gram support obstruction and symmetric-part-only obstruction are also valid, with their stated limited scope.
4. The candidate's narrow repair of the 2022 sector-angle argument is valid and supplies the needed polynomial cut bound. External stability and local-to-global spectral theorems are not reproved here.

## Authentication and independence

The candidate MANIFEST.json is 8,944 bytes with SHA256

    d1c04857fc2729a93a1544a6fda95c9b2a25fc7e3c3f63b6d3015a16df8f2bd7.

Historical independent authentication checked all 39 listed members, sizes, hashes, exact file-set equality, safe relative paths, and absence of symlinks. Its output agrees in normal, -O, and -OO execution. The candidate was read only. No candidate program, source-author program, external optimizer, or own optimizer was executed or imported. The archived manifest digest identifies the reviewed input, not the public prose-edition manifest.

All six candidate source PDFs were independently re-extracted with pdftotext -layout into temporary files. Each extraction was byte-identical to its pinned text companion. Hashes identify the authenticated local source bytes; this is not a claim that a fresh remote download had the same hash. Primary landing pages and available PDFs were checked on the public web. The DOI redirect initially failed, and the official EMS PDF succeeded. The PMLR PDF text opened, but a web screenshot attempt failed; the authenticated local rendered page was viewed instead. No copied source document or source text is included in this audit deliverable.

## Matrix algebra and boundary analysis

### Nonnegativity and common support

The regularization proof of nonnegative determinants is correct: G+epsilon I is positive definite, its congruence-normalized skew part has paired imaginary eigenvalues, and the determinant product is positive. Continuity gives det(G+A)>=0; if the matrix is invertible the determinant is strictly positive. This holds for each principal compression.

For L=H+A and Lx=0, positivity of H gives Hx=0 from x^THx=0, then Ax=0. Consequently L^Tx=0, and applying the same argument to L^T proves equality of left and right kernels. This justifies equality of row and column ranges, an essential point that would fail for arbitrary nonsymmetric matrices.

For pivot-column U and P=(U^TU)^(-1)U^T, UP is the orthogonal projection onto the common range. Directly, U(PLP^T)U^T=(UP)L(UP)^T=L. C=PLP^T is invertible, accretive, rational, and det C>0. Also H=U Sym(C) U^T and Sym(C)=PHP^T, so their ranks agree. No assumption H>0 is used.

### Cofactors and weighted Gram objectives

The signed complementary vector q satisfies det([B;v^T])=q^Tv. Double Cauchy-Binet gives the cofactor coefficient matrix transpose of adj(C); a scalar quadratic form is unchanged by transposition. Hence

    det(BCB^T)=det(C) q^TC^(-1)q.

The identity

    Sym(C^(-1))=C^(-T) Sym(C) C^(-1)

makes Q=det(C)Sym(C^(-1)) PSD of rank h. A positive diagonal pivot exists in any nonzero PSD residual: a zero diagonal forces its entire row/column to vanish. Repeated symmetric Schur-complement elimination therefore produces exactly h positive rational rank-one terms Q=sum d_j v_jv_j^T. This includes singular PSD forms and requires no square roots or division by vanishing principal objective values.

For any nonzero coordinate p of v, the stated T_v spans v-perp and its cofactor vector is a sign times v/v_p. Cauchy-Binet gives det(BT_v)^2=(q^Tv)^2/v_p^2. Since U is injective on R^(k+1) and T_v has rank k, W=UT_v has rank k. Multiplying by d_jv_p^2 proves the exact positive sum of Gram determinants. There is no missing transpose, weight, sign, or full-rank condition.

If rank L=k, the ordinary determinant-product formula gives one positive-weight Gram determinant. If rank L<k, all target minors vanish. If rank L=k+1 and H=0, the reduced C is invertible skew, hence even-dimensional; k is odd, Q=0, and all k-principal minors vanish. Mixed odd k is correctly retained. k=1 can be solved exactly by the largest diagonal. The empty k=0 problem is outside the candidate's explicit domain 1<=k<=n.

### Approximation and bit complexity

At an original optimum, one of h nonnegative components contributes at least OPT/h. An alpha(k)-approximation for that component yields an original determinant at least OPT/[h alpha(k)]. The algorithm compares original determinants, not incomparable component values. The h=0 branch is taken before attempting this argument.

For the full-rank Gram problem, the candidate's with-replacement expectation, ordered-prefix conditional expectation coefficient, and deterministic greedy continuation are correct. In particular the factorial (k-t)! and coefficient degree k-t are necessary and are present. Dependence or repetition gives zero continuation, so positive initial expectation forces a distinct full-rank final k-set. Exhaustive component maximization in tiny tests verifies only the selection argument and is not represented as the polynomial-time optimizer.

The rational elimination and interpolation bit bounds are valid. The cited constant-tolerance D-optimal-design primitive is consistent with Nikolov's results. Because a reference to weak optimization can obscure conditioning and rational output size, Part III of PROOF.md reproduces the complete independent supplement and gives a replacement implementation proof: fixed rational vertex steps, an exact leverage stopping certificate, polynomially bounded objective gap, polynomial denominator growth, and exact conditional-expectation rounding. It obtains the same 2k^k/k! factor without an external optimizer. No optimizer was run in the audit. Finally h<=k+1<=2^k and k!>=(k/e)^k give the stated (4e)^k upper bound, including k=1.

## Local-search family

The symmetric-part Schur complement is positive because a>0 and ad-kt^2=delta+delta kt^2+delta^2>0. b-c=2epsilon>0 proves genuine nonsymmetry. These are exact inequalities for every permitted k and rho, not merely numerical observations.

After a size-s swap, the retained Hadamard columns have Gram matrix kI-D^TD. The block determinant is

    a^(k-s) det(dI-(bc/a)(kI-D^TD)).

Dividing by a^k supplies exactly the candidate's gamma=(ad-kbc)/a^2 and beta=bc/a^2. This remains valid at s=k, where the retained block is empty. beta>0 and gamma>0. The trace of D^TD is s^2, so AM-GM bounds the ratio by (gamma+beta s)^s.

The four contributions to ad-kbc are bounded by 1/16, 1/64, 1/256, and 1/16 respectively. Dividing by a^2>=1 does not worsen the bound, and beta s<=1/(4rho)<=1/4. Thus the 101/256 bound is conservative and correct. The last-block competitor has ratio (d/a)^k>=(4k/(17rho^2))^k. Fixed rho and unbounded powers of two make its base unbounded, proving the asymptotic obstruction. For small k the displayed competitor need not be better than the local maximum; the theorem only needs arbitrarily large k and correctly states that scope. Entry lengths are O(log k+log rho).

## Extension and support obstructions

For the 4-by-4 block example, Sym(C)=I, det C=25, and the second compound computed in order 12,13,14,23,24,34 has the displayed symmetric matrix after multiplication by 25. The vector (0,1,0,0,-1,0) has value -6. Its Plucker relation z12*z34-z13*z24+z14*z23 is 1, so it is not a decomposable bivector. This is exactly why the negative direction does not contradict nonnegative principal determinants. Orthogonal Hodge-sign permutations preserve inertia.

For J direct-sum J, the only positive two-element principal minors are 12 and 34. Any hypothetical Gram representation would require two independent pairs and dependent cross pairs, forcing a nonzero vector into two distinct one-dimensional spans. This is impossible. The claim concerns an exact single-Gram support representation only. The diag(2I_2, [[1,M],[-M,1]]) example also correctly gives the fixed-k unbounded failure of optimizing H alone.

## Source repair and attribution

The [2022 PMLR paper](https://proceedings.mlr.press/v178/anari22a.html) is accurately characterized: its nPSD condition is L+L^T>=0; its result is k^O(k), using positive-support initialization, bounded multiplicative local improvements, and a polynomial exchange loss raised to O(k). Its arithmetic runtime is not itself a rational-bit or floating-point analysis. The candidate's exact marginal interpolation supplies a valid alternative initialization, including zero support.

The visually inspected PDF page 18 indeed places the root with argument pi/q in Gamma_alpha after assuming only q>1/alpha. That membership is false in general, while membership in Gamma_(2alpha) is correct. The candidate's repaired contour chooses theta strictly between pi/q and alpha*pi. Writing eta=q theta-pi gives pi/(2r)<=eta<=pi/2 for alpha=1/r, q>=r+1. The ray inequality, endpoint coefficient bound, and inner/outer arc dominance are valid. The bounded annular-sector contour avoids the origin and lies in the zero-free region. Rouche then forces a contradiction if the middle coefficient sum is too small.

The graph translation is also valid for loop-free weights: a crossing q-set contributes at least q-1 cut weight and at most q(q-1) to either volume. Positive-volume cuts with an endpoint weight zero necessarily have crossing weight. Thus the stated sigma/[q(1+sigma)] and zero-endpoint 1/q bounds follow. This repairs the precise coefficient/cut step; it neither reproves all external spectral inputs nor improves the approximation exponent.

The [2020/2021 Anari-Vuong paper](https://arxiv.org/abs/2004.13018), Remark 9, already provides the Hadamard fixed-radius local-search barrier. The candidate correctly describes its strictly nonsymmetric variant without novelty claims. The [Nikolov manuscript](https://arxiv.org/abs/1412.0036) supports the full-rank PSD rounding factor and deterministic derandomization. The [coreset manuscript](https://arxiv.org/abs/2211.00289) concerns Gram/strongly-Rayleigh settings; the [EMNLP paper](https://aclanthology.org/2025.emnlp-main.1376/) states a conditioning-dependent log-determinant guarantee. Neither inspected statement resolves the unrestricted target. This audit did not independently verify the coreset paper's author-page venue listing or audit those later papers' full proofs.

## Exact tests and negative controls

The newly written stdlib-only Fraction suite reports 20,759 successful explicit checks with identical results under normal, -O, and -OO:

- 22 accretive matrices, ranks 2 through 6; 624 rank-(k+1) principal subsets; 624 exact positive sum identities; 5,200 identities covering every nonzero hyperplane pivot in the generated cases
- 585 rank-k identities and 352 rank-below-k zero tests; three pure-skew zero branches; singular symmetric parts, duplicate/zero rows, and rational nonorthogonal changes of coordinates
- 19 exhaustive small-instance component-selection checks
- 5,111 neighbors for ten (k,rho) pairs; 407 directly evaluated full principal determinants; all other neighbor ratios computed through the independently derived exact Schur matrices
- 98 prefix expectations independently compared with full draw-tuple enumeration; four deterministic rounding instances; 94 marginal coefficient identities and 64 successor sums
- Exact second-compound -6 value, nondecomposability, support obstruction, and symmetric-only gap examples
- Entirely zero matrices through n=5, a rank-one case, 670 rational sector-angle margin pairs, and 27 exact ray-inequality algebra checks

The local-neighbor enumeration reaches k=8 and rho=3, with all radii through 4 at k=4. It is not an asymptotic computation. The infinite families, sector lemma, polynomial-time bound, and approximation theorem rest on written arguments. The optimizer step tests only check an exact determinant-increase formula and constants, not a complete optimization run.

Mutation controls reject indefinite and nonsymmetric PSD inputs, an incorrect inverse form, a cofactor sign change, and a missing rounding factorial. Separate subprocess controls deliberately fail an explicit guard and a wrong manifest pin in normal/-O/-OO. Full-copy tamper probes reject same-size byte mutation, missing/extra members, a member symlink, and an altered manifest. The control harness itself was run in all three modes. Explicit exceptions, not Python assert, enforce checks. Authentication was repeated after the audit.

## Residual scope

The candidate's three main results and narrow source repair are accepted at their stated scope. General rank>=k+2 remains outside this reduction, aside from separate trivial regimes such as k=1. Rank k+2 is a failure point for this specific PSD cofactor technique, not a proved complexity threshold. No solver deployment, practical runtime benchmark, priority search certification, or human/formal acceptance is claimed. All reported exact checks and source inspections are historical; none was rerun to prepare this edition.
