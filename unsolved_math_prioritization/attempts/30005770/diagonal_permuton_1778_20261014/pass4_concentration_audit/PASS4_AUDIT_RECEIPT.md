# Shared PASS4: final independent concentration audit

14 October 2026. This is the analytic/probability review.

## Verdict

**Accept the eleven pinned proof notes with the restricted and conditional scopes below. The universal diagonal-permuton theorem remains unresolved.** In particular, the exact-uniform 1324 anti-diagonal limit remains unresolved, and no uniform-probability counterexample has been established.

The exact reviewed bytes and SHA-256 values are in `REVIEWED_INPUT_PINS.json`. Eight detailed acceptance reports accompany this receipt. `CROSS_REVIEW_PINS.json` verifies the complementary structural reviewer’s final nine-note packet and all its embedded pins. The increasing-pair criterion and internal-chain companion receive complete independent checks in this audit.

The probability law throughout is exact uniform sampling from the actual avoidance class. The target topology is weak convergence in probability of square-spread permutons, equivalently convergence in the contract’s bounded-Lipschitz metric. No uniformity in a growing forbidden pattern is asserted.

## 1. Quantitative fixed-window gaps

`QUANTITATIVE_GAP_ACCEPTANCE.md` accepts the one-ended minimax identity. For E(p,q)=(p+q)log(p+q)-p log p-q log q and eta>0, let y_0=0 and choose the positive increasing-branch solution

    eta*y_j-E(y_(j-1),y_j)=1.

The exact K-coordinate minimax value is kappa_K(eta)=1/sum_j y_j. The branch selection is essential: the function initially decreases when its predecessor is positive, but its positive-level sublevel set is the interval ending at the stated unique positive root. Monotonicity in the predecessor and homogeneity justify the induction proving the lower bound; the normalized y-vector attains equality.

The actual profile count is

    b_(n,K) <= A_eta*lambda*(n+1)^(K+1)*lambda^n*exp(-n*kappa_K(eta)).

It uses the accepted one-point rerooting injection, the exact missing-edge shuffle multiplicity, and an absolute first-cell bound uniform in cell size. For fixed K, continuity permits eta increasing to gamma=log C(1/lambda) after taking the growth limit. The finite inequality is also valid when K varies, but its profile factor and the subexponential normalization defect lambda^n/a_n must then remain visible.

`TWO_ENDED_GAP_ACCEPTANCE.md` accepts the outgoing-edge rerooting variant and the exact two-ended value

    kappa_K^pm(eta)=1/sum_(j=1)^K min(y_j,y_(K+1-j)).

The coefficient prefactor becomes 2*A_eta*lambda*(n+1)^(K+1). The outgoing construction recovers the cut edge from its stored shuffle and bridge location; it does not assume that reversing a canonical cell path preserves its law. Both certificates are summable in K: the one-ended scale is R^(-K), and the two-ended scale is R^(-K/2), for the specified R>2. These are lower bounds on the true gaps, so their summability proves no summability statement about the true gaps.

## 2. Adaptive windows and actual deterministic obstructions

`ADAPTIVE_ENTROPY_ACCEPTANCE.md` accepts the centered-window selection lemma and its exact-law transfer. For a normalized profile, the sum of all outward boundary entropies is at most 2 log 2. If a nonnegative lower bound d_K on the true logarithmic gap satisfies the stated divergent odd-subseries condition, some bounded centered window around every macroscopic cell has a fixed positive gap-minus-boundary-entropy margin.

The probabilistic transfer retains the full prefix, marked-window and suffix counts a_p*b_(m,K)*a_q. Only the two boundary shuffles are charged. The finite cap on window width is chosen before n; the limsup coefficient estimates are then uniform over that finite collection and all m at least epsilon*n. Division by the actual a_n leaves the correct exp(o(n)) defect. Under the unproved divergence hypothesis this gives exponential largest-cell tails and the desired 1324 anti-diagonal limit.

The same report and the two-ended acceptance verify exact canonical ratio-half mountains defeating the established one-ended and two-ended certificates in every window of any prescribed bounded width. This includes one-sided and end windows; increasing a fixed window cap does not rescue the certificate. The witnesses are actual avoiders. Their existence establishes a deterministic limitation of these estimates, not a positive probability under uniform sampling.

The small-width supplement remains valid even after replacing the certificates for K=1,2 by the actual true gaps. The bounds g_1=4, g_2=27/4 and lambda<=27/2 give delta_1<=log(27/8) and delta_2<=log 2; the mountain’s endpoint entropy exceeds the corresponding gap budget. This says nothing about the unknown optimal gaps for all widths.

## 3. Fixed-width calibration

`FIXED_WIDTH_ACCEPTANCE.md` accepts the constant-overhead guard transfer between unrestricted labeled domino paths and canonical paths for every fixed width. In particular, g_1=4 and g_2=27/4 are exact. Keeping the number k of source construction blocks fixed and scaling their sizes gives

    g_(3k) >= (81/8)*(27/4)^(-7/(36k)).

The source’s independent size parameters, encoding injectivity and constant guard overhead were inspected; the primary Theorem 9, pages 13–14 were read directly. The entropy arithmetic agrees with the displayed expression. The resulting true-gap upper bound has nonzero limiting constant log(4/3), so it neither proves nor disproves the divergence condition above. Source copies and extracts are excluded from this authored audit packet.

## 4. Incoming marks and their exact limitation

`TERMINAL_MARK_ACCEPTANCE.md` accepts the parity-dependent terminal-strip symmetry and three-point guard. The output first state is exactly P(A)=12 skew-sum A^(-1); the parity ambiguity costs at most two fibers. The coefficientwise conclusion is z*ell_A<=2*h_(P(A)). The state-dependent padding and inverse are retained.

There is a common incoming exponential mark for every 1<u<C(1/lambda) at every real z<rho=1/lambda. Joint endpoint marks are also valid when log u+log v<gamma. These follow from absolute coefficient estimates and finite Hölder bounds, with one lambda^n factor rather than an incorrectly multiplied lambda^(2n).

The direct attempt to multiply outgoing and incoming marks yields only the domain

    u*z < rho^2*C(rho)^2 = rho*(C(rho)-1) < rho.

For u>=1 this is weaker than the elementary subcritical domain. It gives no fixed bulk-cell exponential mark near rho. No independent or uniform residual law is introduced.

## 5. General fixed alpha

`GENERAL_ALPHA_ACCEPTANCE.md` accepts the strict growth gap and packing theorem for every fixed alpha of length m>=2. The growth rate mu of Av(alpha) exists because every principal avoidance class is closed under at least one of direct or skew sum. The accepted frontier bound gives

    mu <= lambda/C(1/lambda) < lambda.

Recording deletion positions, deletion values, the deleted pattern and the retained alpha-free pattern gives the exact upper count binom(n,h)^2*a_h*b_(n-h). Hence deleting at most delta*n entries to become alpha-free has rate bounded above by

    2H(delta)-(1-delta)*log(lambda/mu),

which is negative for sufficiently small fixed delta. The inequalities P<=D<=mP transfer this to exponentially likely linear disjoint-alpha packing. All constants may depend on alpha.

The perfect-packing constructions for each alpha also pass: they avoid alpha skew-sum 1, have minimal frontier and localized smallest o(n) values, yet maintain fixed positive weak deviation from the diagonal. The displayed lower bound 1/(2*sqrt(2)*m^2) respects the contract’s Euclidean bounded-Lipschitz convention. Crossing rectangles are alpha-free. These are deterministic obstructions to replacing spatial completion control by global packing; they are not counterexamples to the uniform theorem.

## 6. Exact pair target and internal-chain refinement

`POINT_PAIR_ACCEPTANCE.md` accepts

    d_BL(mu_pi,anti-diagonal) <= 2*Inc(pi)/n^2 + 1/n.

The converse uses continuity of two-point pattern density on permutons and bounded expectations. Thus E Inc(Pi_n)=o(n^2) is necessary and sufficient for the desired deterministic anti-diagonal limit.

The exact generating identity keeps both completion factors:

    I(z)=sum_A z^|A| ell_A h_A inc(A)
         +sum_(A,C) z^(|A|+|C|) ell_A h_C K_inc(A,C).

The edge kernel sums actual allowed-shuffle cross-increasing-pair counts. No unconditioned shuffle mean is substituted. The remaining coefficient target is [z^n]I(z)=o(n^2*a_n); it has not been proved.

`INTERNAL_CHAIN_ACCEPTANCE.md` accepts inc(A)<=|A|(LIS(A)-1) for each normalized Av(213) state and the comparison L_max<=LIS(pi)<=2L_max. A sublinear-LIS theorem would therefore handle within-cell pairs, but J_m direct-sum J_m has LIS 2 and m^2 cross-pairs. The adjacent-edge weighted term remains indispensable.

## 7. Corrections, finite diagnostics and preservation

Two requested clarifications are incorporated in the final pins: the quantitative-gap proof now cites the accepted one-point rerooting artifact rather than its provisional predecessor, and the direct product-domain comparison explicitly states u>=1. No outstanding mathematical correction remains in the accepted versions.

`FINAL_CHECKER_RECEIPT.json` verifies five normal/optimized/double-optimized report triples and their proof pins. Four triples are byte-identical. The general-alpha triple has identical mathematical records after omitting declared runtime/interpreter/optimization metadata. Its coverage includes 41965 exact small cases, 305110 crossing rectangles and 96 explicit constructions. The profile checks cover 1023 compositions and 81435 mountain windows, and the exact pair totals through n=7 are 0, 1, 9, 67, 481, 3452, 25036. The terminal map’s factor-two fiber occurs in the finite checks. These are regression checks only; the all-size verdicts rest on the arguments above. This reviewer compared the frozen outputs and does not claim to have rerun those author scripts.

All public artifacts in this reviewer’s PASS1, PASS2 and PASS3 manifests were rehashed and remain unchanged. The audit manifest excludes private source extracts.

The remaining issue is an actual completion-weighted spatial or pair estimate. Neither a finite coefficient table, a scalar-state abstraction, global packing, summable lower-gap certificates, nor separate endpoint marks supplies that estimate.
