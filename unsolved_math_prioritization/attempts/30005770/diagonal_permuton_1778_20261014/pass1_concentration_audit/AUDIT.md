# Independent concentration and entropy audit

Date: 14 October 2026. Target: uniform avoidance of the fixed pattern alpha skew-sum 1, for every fixed nonempty alpha. This audit evaluates weak convergence to the diagonal. It does not substitute total variation, uniform control over growing patterns, or a claim about every avoider.

## Current verdict

Accepted: the frozen minimum-insertion frontier theorem, its completion-weighted small-value extension, and all frozen entropy/cut reductions within their stated scope. Rejected as unsupported: any claim that these results prove or disprove the universal diagonal-permuton target. The accepted existing geometric source mechanism transfers the uniform law through particular bijections. The rare-region argument controls exponential growth rates, which do not by themselves control limiting mass. Exact candidate pins and verdicts appear in Sections 7-9.

## 1. What the existing geometric proof actually needs

Source: Kaitlyn Hohmeier and Erik Slivken, *Permuton limits for some permutations avoiding a single pattern*, arXiv:2502.19541v3, 24 February 2026, https://arxiv.org/pdf/2502.19541v3 . PDF SHA-256: cc23f169b852b0581492d4524c3b0e0857f5b8f7fe6655631ff867fb59bc2d5d; 394904 bytes.

The relevant pins go beyond the theorem statement:

- Section 2, pp.5-6: the shape-Wilf construction recolors a Young diagram, changes only its blue traversal, and leaves the white region fixed. Proposition 2.2 provides bijections for replacing an initial increasing block by a decreasing block before an unchanged suffix. Equality of enumeration sequences alone is not the property being used.
- Section 4, pp.8-10: the source class is uniform avoidance of I_(d+1). Its canonical d decreasing layers obey, with probability tending to one, macroscopic anti-diagonal localization, local density and regularity, bounded gaps, and separation between adjacent layers. Lemma 4.2 turns these conditions into an extension of each interior layer point to a full d-point increasing chain.
- Section 5, pp.10-11: a point in the layer indexed by k1+k2 has a suffix chain of the required length. That chain forces avoidance of J_k1 direct-sum I_k2 southwest of the layer. After reverse-complement, this supplies a region where the second bijection is frozen. The retained layer's density and location make this frozen region macroscopically large.
- Theorem 1.1 proof, pp.11-12: the full composite map is a bijection of the complete finite source and target classes. Consequently a uniform source has a uniform target, and the image of the high-probability good set has the same relative cardinality. Uniformity does not come from a heuristic random generator or from conditioning without accounting for the discarded set.

The missing hypothesis for importing this proof strategy is a replacement for that high-probability geometric transport for arbitrary alpha. A transfer-based replacement must establish a map with the correct finite uniform law and show that its image retains a one-sided macroscopic concentration estimate. A different proof strategy could bypass bijections entirely. Merely knowing a Wilf-equivalence, a finite growth constant, a principal avoidance condition, or sum-closure supplies none of those geometric properties. In particular, the local layer extension needed to identify the second frozen region has not been established for arbitrary alpha.

This is an audit of the proof mechanism and its limits, not an independent verification of every theorem invoked from the paper's references. The displayed target subfamily remains alpha = I_a skew-sum J_b, a >= 1 and b >= 0, as fixed in the construction contract. Section 6, p.12, does not establish the uncovered alpha=132 case.

## 2. A clean replacement for the one-sided analytic step

The following elementary estimate is valid for every permuton and avoids dependence on the source's total-variation wording or its logarithmic strip estimate.

Let (X,Y) have a permuton law mu and put Z=X-Y. Both marginals are uniform, so E Z=0. Therefore

    integral |x-y| dmu = 2 E[Z_+].

For 0<delta<1, if mu{Z>delta} <= delta, then

    E[Z_+] <= delta + mu{Z>delta} <= 2 delta,
    integral |x-y| dmu <= 4 delta.

The coupling (X,Y) with (X,X) has second marginal equal to the diagonal permuton mu_I. Every 1-Lipschitz test function thus satisfies

    d_BL(mu,mu_I) <= integral |x-y| dmu <= 4 delta.

The reflected anti-diagonal version uses Z=X+Y-1 and the coupling (X,Y) with (X,1-X). It has the same proof. Also

    mu{|x-y|>epsilon} <= 4 delta / epsilon.

Thus one-sided strip mass tending to zero at every fixed width is sufficient, with no logarithmic loss. All these inequalities are deterministic; applying them on events of probability tending to one is legitimate. They impose no relationship between the random permutations at different n.

## 3. Inversions really do characterize the weak target

For a permuton mu, let q(mu) be the probability that two independent mu-points induce the pattern 21. Coordinates have no ties. The map q is continuous for weak convergence of permutons: the discontinuity set of the indicator consists only of equal first or second coordinates, which has zero product measure under every permuton.

For the square-smoothed permuton of pi in S_n, an exact calculation gives

    q(mu_pi) = 2 inv(pi)/n^2 + 1/(2n).

Indeed, distinct selected squares contribute twice the inversion count divided by n^2. The two samples land in the same square with probability 1/n, and then their coordinate orders disagree with probability 1/2. This finite-n correction must not be silently discarded in an exact formula.

Write F_mu(x,y)=mu([0,x] x [0,y]). The same-coordinate events have zero mass, and conditioning on one point gives

    q(mu) = 2 integral (x-F_mu(x,y)) dmu(x,y).

Since F_mu(x,y)<=min(x,y), this implies

    q(mu) >= 2 integral (x-y)_+ dmu = integral |x-y| dmu
           >= d_BL(mu,mu_I).

Consequently, for any sequence of random permutations, not necessarily uniform,

    E inv(Pi_n)/n^2 -> 0

implies weak convergence in probability of mu_(Pi_n) to mu_I, by Markov's inequality and the displayed deterministic bound. Conversely, weak convergence in probability to mu_I implies q(mu_(Pi_n))->0 in probability by continuity. As 0<=q<=1, expectations tend to zero, giving E inv(Pi_n)/n^2->0. Thus this is an equivalence for the stated deterministic limit, not only a sufficient criterion. The original OWR p.282 already credits the sufficient criterion; this audit supplies the finite-n correction and the missing converse justification, without a novelty claim.

## 4. The exact gap in the rare-region convex-hull route

Sources:

- Neal Madras and Gokhan Yildirim, *Longest Monotone Subsequences and Rare Regions of Pattern-Avoiding Permutations*, Electron. J. Combin. 24(4) (2017), P4.13, https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i4p13/pdf/ . PDF SHA-256 ad7c42082cafc232e7283e2fa6465bc139b499ed232c746a55fd05514887e12c; 633734 bytes. Definition and Theorem 1: p.5. Theorem 17(a) and its proof: pp.25-26.
- Justin M. Troyka, joint with David Bevan, *Permuton Limits of Permutation Classes and Rare Regions*, in OWR 6/2024, printed pp.298-299, PDF pp.26-27, https://ems.press/content/serial-article-files/48646?nt=1 . PDF SHA-256 9827c40680236ec3eb02900db7d61f448bd4c0e2d41e8334ddc9c82757446931; 379479 bytes.

Let a_n=|Av_n(tau)| and L=lim a_n^(1/n). In the proof of Theorem 17(a), a direct-sum injection yields, schematically,

    |E_n| a_m <= |embedded event at size n+m|.

After taking (n+m)-th roots, |E_n|^(1/n) approaching L along a subsequence implies the same exponential growth at scaled locations. This proves propagation of non-exponential rarity. Before taking roots, however, the probability supplied by the injection contains

    P_n(E_n) a_n a_m / a_(n+m).

The factor a_n a_m/a_(n+m) need not stay bounded away from zero. Even Catalan counts, a_j ~ 4^j/(sqrt(pi) j^(3/2)), give a factor of order N^(-3/2) when n and m are both proportional to N=n+m. Equal exponential growth permits polynomial or exp(-sqrt(N)) probability loss. It does not imply positive limiting mass, let alone samplewise support propagation.

Hence a valid general support proof still needs a quantitative mass-propagation theorem, or another argument excluding off-diagonal mass in every subsequential limit. It must also handle possible random subsequential limits. Positive area in the support of an expected/barycenter measure is not a contradiction to almost surely thin supports of random individual limits.

The relevant endpoints are (0,0) and (1,1); the ambient space is [0,1]^2. The OWR neighboring misprints do not disprove the intended conjecture.

## 5. Correct form of the OWR small-point-probability criterion

Here is a safe version that needs no assumption that the entire sequence already has a limit. Fix an open U in the square. Suppose there is a sequence b_n=o(1/n) such that

    P(Pi_n(i)=j) <= b_n

for every lattice corner (i/n,j/n) in U. For a continuous nonnegative f whose support is compactly contained in U, all cells meeting its support have their upper-right corners in U once n is large. Therefore

    E integral f dmu_(Pi_n) <= ||f||_infinity n b_n -> 0.

For any random weak subsequential limit M, the bounded continuous functional mu -> integral f dmu has expectation zero under M. A countable exhaustion by such functions shows M(U)=0 almost surely. This is the justified support conclusion.

The displayed o(n) on OWR p.299 cannot be used: it is vacuous for probabilities, and the surrounding intended scale is o(1/n). Pointwise estimates with constants depending on moving lattice locations do not give the required uniform estimate. Continuity sets or compactly supported continuous test functions are needed; weak convergence never means convergence on every measurable set. The criterion is sufficient and can be stronger than necessary because a bounded number of atypical points contributes only O(1/n) permuton mass.

## 6. Enumeration and sampling checks that every candidate must pass

1. Denominators must be the cardinality of the complete Av_n(alpha skew-sum 1), or a proven asymptotically equivalent count. A uniform law on a chosen subclass, a tree encoding without multiplicity correction, or an image with unknown fiber sizes is insufficient.
2. To obtain exponential rarity from a counting ratio, the bad-count exponential growth must be strictly smaller than the full growth. Equal nth-root growth leaves all subexponential probability behavior unresolved.
3. A successful weak-limit proof only needs bad mass probability to vanish. It does not need exponential suppression of every far-away point or of maximum displacement. A claimed exponential maximum-displacement bound is a strictly stronger assertion and must be audited separately.
4. Deleting the smallest entries of a uniform avoider does preserve avoidance. It does not automatically preserve the uniform distribution. The induced probability of a smaller avoider is proportional to its number of allowed completions.
5. Fixed-pattern quantifiers are essential. Constants and thresholds may depend on the fixed alpha and on the fixed positive error parameter. No conclusion for growing patterns or a rate uniform in alpha is inferred.

## 7. Frozen minimum-insertion candidate: accepted restricted theorem

Reviewed artifact: *Minimum-insertion frontiers in principal ends-in-one classes*, ACTIVE_FRONTIER_PROOF.md. SHA-256: 6058827dafd2c16dc53c66452c4da6cc010619d80508b07a08eaaaaffdc6957b.

Let L(sigma) be the first prefix endpoint containing alpha, with sentinel n+1 if alpha is absent. For m=|alpha|>=2, write lambda=lim a_n^(1/n), C(z)=(1-sqrt(1-4z))/(2z), and gamma=log C(1/lambda). The complete proof establishes 4<=lambda<infinity and accepts the following:

- Frontier tail: for fixed epsilon in (0,1], limsup n^(-1) log P(L(Pi_n)>=ceil(epsilon n)) <= -epsilon gamma.
- Small-value tail: the same bound holds with L(Pi_n) replaced by the largest position of the smallest k_n values for every sequence 1<=k_n=o(n).
- Corner bound: if k_n/n->delta in (0,1) and a in (delta,1], the largest position of those k_n values exceeds ceil(a n) with logarithmic rate at most H(delta)-(a-delta)gamma.

The audit checked these exact steps:

1. Active gaps are precisely k=0,...,L-1, with k counting old entries to the left of the new minimum. A new forbidden tau uses the inserted minimum as its last entry, so the initial old k entries must contain alpha for the insertion to fail.
2. If r is the position of alpha's minimum, a new alpha occurrence is impossible for k<r-1; otherwise its endpoint is at least k+m-r+1. Old alpha occurrences move no earlier than L+1, and the old first occurrence (or absent-occurrence sentinel) also gives the upper bound L(child)<=L+1. Consequently the sorted L child labels satisfy b_j>=j+1. Empty parents and missing occurrences obey the same indexing.
3. The actual tree therefore contains the comparison succession with children 2,...,L+1. Its depth-t count is B(L,t)=L/(L+2t) binom(L+2t,t). The recurrence and C(z)^L generating function agree. Deleting the t smallest values uniquely recovers the ancestor and path, so comparison branches and different parent descendant sets cannot collide.
4. The finite inequality A_n(ell) B(ell,t)<=a_(n+t) has the complete uniform denominator a_n. For ell/n->epsilon and t/n->s>0, Stirling plus log a_n=n log lambda+o(n) gives the claimed rate. For lambda>4 the stationary point is s=epsilon(sqrt(lambda/(lambda-4))-1)/2. For lambda=4, taking the infimum over separately fixed finite s yields the limit epsilon log 2; no illegal interchange with s growing with n is used.
5. Deletion bias is handled rather than ignored. For an ancestor sigma of size n-k, all inserted small values lie in the first L(sigma)+k-1 positions. Each ancestor has at most binom(n,k)a_k completions. Thus the exact comparison is

       P_n(M_k>=q) <= binom(n,k) [a_k a_(n-k)/a_n]
                          P_(n-k)(L>=q-k+1).

   Sum-closure bounds the bracket by 1. For k=o(n), log binom(n,k)=o(n), so this really does extend the tail to every sublinear sequence k_n. For k/n->delta>0, the entropy cost H(delta) is retained. Omitting this factor would invalidate a bulk inference.
6. The candidate's direct sum of repeated 132 blocks and a final decreasing block is a valid deterministic 2431-avoiding nonimplication example. Its linear-size decreasing part prevents diagonal geometry despite its bounded frontier and well-positioned first o(n) values. Its sampling law is not uniform, and the candidate correctly does not call it a target counterexample.

Independent finite indexing checks passed for all alpha of length 2 and 3 through parent size 6, and all alpha of length 4 through parent size 5: 7,958 parents, 49,486 tested slots and 41,965 valid children. These checks support the indexing audit; the all-n conclusions rest on the proof above and in the pinned candidate.

The case m=1 is separate and immediate, since avoidance of 21 gives only the increasing permutation. Constants throughout depend on the fixed alpha. Global-minimum macroscopic localization is also a corollary of the existing rare-region geometry after reverse-complement; no novelty is claimed for it or for the new presentation.

## 8. Frozen entropy candidate: accepted barriers and exact reductions

Reviewed artifact: *Entropy and counterexample audit for the diagonal permuton conjecture*, ENTROPY_OBSTRUCTIONS.md. Final SHA-256: a78e8464508487e2f5135dfd9d6cbef36f0ce6b3e8de508c5b74999a4b75477e; 13304 bytes.

All six sections are accepted within their expressly limited scope. In particular:

- If alpha does not start with its maximum, the injection (sigma,eta,rho) -> sigma direct-sum (1 skew-sum eta) direct-sum rho places value j at position i for every i<=j. Its three block sizes are i-1, j-i, n-j and sum to n-1. Sum-indecomposability of tau and the nonmaximum first entry establish avoidance. Fixed-block recovery proves injectivity. The uniform all-size lower bound for a_k makes the resulting full-exponential-growth claim uniform over the entire upper triangle.
- The corner identity P(Pi_n(1)=n)=a_(n-1)/a_n is exact under the same additional hypothesis. Madras-Yildirim Theorem 15, p.20, applies because tau ends in 1, giving limiting probability 1/lambda. Thus maximum-displacement convergence can fail altogether, even when the weak diagonal theorem is known. A single square still has mass 1/n. This is not a target counterexample.
- Fixed-size direct-sum blocks prove full exponential growth inside every fixed diagonal neighborhood. The shrinking-neighborhood extension is valid when n epsilon_n->infinity, using k_n->infinity, k_n=o(n), and k_n/n<epsilon_n. The separable class comparison is sum-closed, exponentially bounded, and complement-invariant, but it is a different avoidance class. Complement symmetry yields E integral|x-y|>=1/4 and the stated uniform positive-probability d_BL separation. It validly refutes only the structural inference from full growth near the diagonal to concentration.
- For cut masses c_mu(t)=mu([0,t] x (t,1]), equality of opposite crossings, the 1-Lipschitz bound, D=2 integral c_mu, and 2M^2<=D<=2M are correct. Together with D/sqrt(2)<=d_BL<=D they give the exact finite-mesh reduction. At a lattice cut, the square-smoothed measure equals the crossing-entry count divided by n exactly.
- The four binomial allocation factors in the quadrant bound correctly specify left and right position sets and high and low value sets. Internal patterns provide an injective encoding of every actual permutation, while permitting extra incompatible allocations only enlarges the upper bound. At i=j approximately n/2 and northwest size approximately cn, the exponent is log lambda+2h(2c)-c log(lambda/lambda_alpha). The entropy term defeats every fixed finite growth ratio at sufficiently small fixed c. This establishes failure of that particular upper bound to give a gap, not failure of every possible speed-n mass-concentration estimate.

The only clarification requested during this review was to justify existence of lambda_alpha explicitly. The final artifact includes it: a pattern is either direct-sum indecomposable or skew-sum indecomposable, so its avoidance class is closed under at least one of the corresponding operations; Fekete and Marcus-Tardos apply. No other mathematical correction was required.

## 9. Final accepted and rejected scope

Accepted mathematical scope:

1. The elementary analytic implications in Sections 2, 3 and 5, with the exact square-spreading correction, ordinary weak topology and random subsequential-limit qualifications.
2. The complete restricted frontier, sublinear small-value and entropy-paid corner theorems in the frozen concentration candidate.
3. The full upper-point growth and extreme-point barrier, full-growth diagonal-neighborhood construction, non-target structural counterexample, finite-cut equivalence, and quadrant-bound obstruction in the frozen entropy candidate.
4. The precisely identified gap between exponential-rarity geometry and positive limiting support/mass in the existing route.

Rejected as not established by this packet:

- A universal diagonal-permuton theorem for all fixed nonempty alpha.
- A fixed target alpha with a positive-probability weak-distance departure along an unbounded subsequence.
- Any bulk concentration claim obtained by treating deletion ancestors as uniform or suppressing their completion weights.
- Any inference from equal exponential growth or Wilf counts alone to the limiting uniform shape.
- Any total-variation or maximum-displacement substitute for the intended weak convergence.
- A novelty claim, literature-exhaustive openness claim, or a full independent audit of all source theorems.

The unresolved quantity for these two lanes is a positive fraction of crossing entries at fixed macroscopic cuts under the exact uniform law. These results do not settle it. No additional pattern family is declared solved by these two candidates.

