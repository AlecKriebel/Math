# Independent adversarial audit: 30004953

Date: 5 October 2026 UTC. Target: OWR-8415364-011, rank 785.

## Verdict and exact scope

**PASS for the stated mathematical partial results. The original all-dimensional, all-p <= -1 optimal-threshold problem remains UNRESOLVED after the recorded 5/5 approaches.** No fatal mathematical error or required repair was found in the frozen proof. This is an independent AI audit, not human peer review, a formal proof certificate, editorial acceptance, or a novelty determination.

The accepted principal conclusions are:

1. For even nonzero finite measures on the circle, every antipodal-pair mass ratio strictly below pi/(pi+2) guarantees an origin-symmetric solution at p = -1.
2. The constant is sharp. The orthogonal four-atom measure at equality has no solution, even if an origin-symmetry requirement on the unknown body is dropped.
3. In dimension n >= 2, at p = -1, the line-mass bound 1/(1+d_n), where d_n = 2 Gamma(n/2)/(sqrt(pi) Gamma((n-1)/2)), is sufficient if the even measure spans the ambient space. Sharpness in dimensions n >= 3 is not established.
4. The compactification, the one-way implication from a full-dimensional maximizer to a solution, the rank k > -p exclusion, the two-pair existence examples for p < -1, and the nonmaximizing-solution example are valid as scoped.

For a guarantee written with a non-strict concentration bound <= c in the plane, the admissible constants have supremum pi/(pi+2) and do not include that endpoint. The paper does not claim an attained largest such closed-inequality constant.

The author freeze was reviewed without alteration: 24,951 bytes, SHA-256 63b3aee3a0e44e17b4ed2fc3d01065708f87dd3dd7e5fee397e85683c1a300e1. Section references below refer to its PROOFS.md. The full file binding is in SOURCE_AUDIT.json.

## 1. Measure conventions and primary hypotheses

The argument consistently uses integral curvature as a measure on radial directions. At almost every normal direction there is a unique supporting point; pushing spherical surface measure forward to that point's radial direction gives J. Thus J has total mass omega, and J_p has positive density rho^p relative to J. Its dilation law is a^p.

The polarity in J_p(K,.) = n C-tilde_(p,0)(K*,.) is necessary and correct under the stated dual-measure convention. In particular, the p in this problem cannot silently be reassigned to the dual parameter q. The support-function PDE concerns the polar. The primary survey's Sections 8.0.3-8.0.4 corroborate these distinctions.

The original OWR theorem explicitly assumes an even, nonzero, finite Borel measure and concludes existence of an origin-symmetric body. The catalog's shortened statement omits evenness. Restoring it is a faithful restriction to the actual source theorem, not a proof of the unrestricted catalog wording. The numerical value 1/2 of the old planar p = -1 constant is correct.

The phrase “spans the ambient space” means that the measure is not entirely supported on any proper linear subspace. This assumption in the all-dimensional line criterion cannot be deleted: a non-atomic measure on a proper subsphere can have every line mass zero. In the plane the strict line condition already implies spanning. No balancing condition from the surface-area Minkowski problem has been imported into this different problem.

## 2. Compactness, degeneracy, and entropy

### Lemma 2.1

The circumradius-one class of nonzero origin-symmetric compact convex sets is compact in the Hausdorff topology. Circumradius is continuous, so the zero set cannot occur as a limit. A unit point v in K puts the entire segment [-v,v] in K, giving |v dot u| <= h_K(u) <= 1. The exceptional hyperplane where the lower bound vanishes has surface measure zero. Its logarithmic singularity is integrable.

The moving-segment argument with Scheffe's lemma is valid: along every subsequence with v_j converging, the nonnegative functions -log|v_j dot u| converge almost everywhere and have the same integral. Their L1 convergence implies uniform integrability, which also holds for the smaller functions -log h_Kj. Uniform convergence of support functions then gives convergence of entropy integrals.

An alternative verification of the decisive uniform integrability is a uniform tail estimate. Near zero the absolute first-coordinate density is bounded, including n = 2. Consequently, for large M,

    integral_{-log h_K > M} (-log h_K) d(sigma/omega)
      <= C_n' (M+1) exp(-M),

uniformly in K and the chosen unit segment direction. This also rules out a hidden entropy loss at a rotating collapse.

For fixed u, a limit of points rho_Kj(u) u belongs to K. This proves radial upper semicontinuity, not radial convergence. Bounded reverse Fatou gives the correct inequality for I_s. At I_s(K) = 0 the logarithm tends to minus infinity while H remains finite. The claimed upper semicontinuity of F_s therefore holds at both finite and infinite values.

The rotating-ellipse warning is correct. With rotation epsilon and short semiaxis epsilon squared, the horizontal radial value is asymptotic to epsilon although the limit segment has horizontal radial value one. No later step incorrectly replaces upper semicontinuity by unrestricted pointwise convergence.

### Lemma 2.2 and Proposition 2.4

The segment entropy gives the uniform finite upper bound log C_n, and the unit ball has F_s = 0 for a probability measure. A finite maximum is attained. For the special outer approximation K+epsilon B, nestedness and intersection equal to K imply monotone convergence of each radial function; this is valid even for a degenerate K. Its scale normalization does not change F_s.

The recovery of the old constant handles equality correctly. Degenerate sets have F_s <= 0 under the old mass bound. If the maximum is positive, no maximizer is degenerate. If the maximum is zero, the full-dimensional ball itself is a maximizer. The argument does not falsely infer a contradiction from equality at a degenerate maximizer. It also does not require uniqueness of the maximizing body.

## 3. The first variation and measure equation

Lemma 2.3 is the central existence step and survives nonsmoothness. A full-dimensional origin-symmetric convex set contains zero in its interior. Its radial function is positive and continuous, so multiplying it by exp(tg) for continuous even g gives a compact generating set and a full-dimensional symmetric convex hull K_t for both signs of sufficiently small t.

The actual radial function of this hull is at least the prescribed radial data. Hence the auxiliary differentiable expression

    (1/s) log integral rho_K^s exp(stg) dmu - H(K_t)

is bounded above by F_s(K_t), and thus by F_s(K), with equality at zero. That auxiliary expression has a two-sided maximum at zero, even if the actual radial function of K_t is not differentiable in t.

Almost-everywhere differentiability of the support function ensures a unique exposed supporting point for almost every normal direction. The maximizer in the support-envelope formula at t = 0 is then unique in radial direction, and its logarithmic derivative is g evaluated at that direction. The exponential support bounds yield a uniform bound ||g|| on the difference quotients. Dominated convergence is applicable. Corners and facets do not invalidate this calculation: their exceptional nonunique normal directions are surface-null.

Differentiating the radial integral and entropy gives

    rho_K^s dmu / I_s(K) = dJ(K) / omega.

Equality is first tested against every continuous even function. Both measures are even, so this determines the full Borel measures. Multiplying by rho_K^(-s) is permitted because it is bounded and positive on the sphere. The scale a = (omega/I_s(K))^(1/s) has the correct sign and power and yields J_(-s)(aK)=mu. A further factor M^(-1/s) restores a total mass M after probability normalization.

Only “full-dimensional global maximizer implies solution” has been proved and used. No converse, strict convexity of the objective, or uniqueness of solutions enters the existence proof.

## 4. Join thickening and collapse dimensions

For a k-dimensional symmetric body L spanning E, zero lies in its relative interior; an inradius r > 0 in E therefore exists. For Q_t = conv(L union t B_(E-perp)), the gauge is g_L(x)+|y|/t and the support function is max(h_L(x),t|y|). These identities are exact and valid for nonsmooth L. Q_t is full dimensional and still has circumradius one when 0<t<1.

The entropy integrand can be nonzero only when the projection R=|P_E U| is below t/r. The spherical beta density is O(R^(k-1)) on that small interval. Its potentially unbounded factor near R=1 is irrelevant because the interval is eventually below 1/2. Integrating R^(k-1) log((t/r)/R) gives (t/r)^k/k^2. Thus the entropy cost O(t^k) holds for the particular fixed L; uniformity over all degenerate shapes is unnecessary.

The radial function on E is unchanged. Outside E, its lower bound t/(1+t/r) is valid because |P_E u|<=1 and g_L(P_E u)<=1/r. Spanning gives strictly positive mass outside E. At a finite maximizer I_s(L)>0, so the logarithmic moment gain is bounded below by a positive multiple of t^s. This dominates O(t^k) precisely in the proved regime k>s.

For s=1 every collapse rank at least two is eliminated. For general s>=1 the proof leaves the ranks 1 through min(n-1,floor(s)), including the equality rank when s is an integer. This is a list of ranks not eliminated by this argument, not an assertion that every one occurs as a maximizing degeneration.

## 5. The line derivative, strict threshold, and equality

For L=[-v,v] the radial value off its endpoints is t/(t|u dot v|+sqrt(1-(u dot v)^2)). Dividing the off-line contribution by t gives increasing functions as t decreases to zero. Monotone convergence applies to arbitrary finite measures, including measures for which the limiting integral A_v is infinite. Separately, I_1(Q_t) tends to m=mu({v,-v}) by bounded convergence. If m=0, L cannot maximize because its functional value is minus infinity.

The distribution of T=|U dot v|/sqrt(1-(U dot v)^2) has density d_n(1+T^2)^(-n/2). Its normalization is 2/B(1/2,(n-1)/2). Integrating log(t/T) over T<t gives D_n(t)/t -> d_n. This recovers d_2=2/pi and d_3=1 with no missing factor of two or sphere-area normalization.

The resulting one-sided quotient is A_v/m-d_n, interpreted as positive infinity when A_v is infinite. This extended limit is justified because log(1+x)/x tends to one as the moment increment tends to zero. Since A_v>=1-m, the strict line bound makes the quotient positive. Every proposed line maximizer is excluded separately; a uniform positive margin over all directions is not needed.

At m=1/(1+d_n), the lower estimate A_v>=1-m gives only zero first order. For data entirely on the line and its perpendicular subsphere, the exact increment is log(1+d_n t)-D_n(t), whose leading nonzero term is -d_n^2 t^2/2. This verifies that the proof must not silently replace the strict inequality by a non-strict one. In dimensions above two this calculation alone is not a general nonexistence theorem.

The stronger directional condition A_v>d_n m is valid when imposed at every possible positive-mass line. For a single selected line it excludes that line only. The all-dimensional theorem itself states its assumptions unambiguously.

## 6. Finite-support rigidity and nonsymmetric endpoint exclusion

The positive bounded density rho^p makes J_p and J mutually absolutely continuous. If J_p is supported on finitely many radial directions, their boundary points must generate the entire body: otherwise strict separation creates an open set of normal directions where the support exceeds that of their hull. On almost every direction in that open set the unique supporting point is outside the finite set, contradicting concentration of J. This argument does not assume symmetry.

With four positive masses on the coordinate rays, the generating hull is exactly the quadrilateral (a,0),(0,b),(-c,0),(0,-d), with all lengths positive. Each point is an exposed vertex. Its right-hand exterior angle is atan(a/b)+atan(a/d), independent of the opposite length c. Thus opposite mass equality compares the same function of a and c.

For s>=1 the derivative numerator z/(1+z^2)-s atan z is strictly negative for every z>0. One direct proof is that atan z-z/(1+z^2) has derivative 2z^2/(1+z^2)^2>0 and starts at zero. Hence equal opposite masses force a=c and then b=d. This closes the possible nonsymmetric loophole in the endpoint obstruction.

For the resulting diamond, the two pair masses have ratio t^(-s) atan(t)/atan(1/t). At s=1 the strict range is (2/pi,pi/2). The manuscript's auxiliary function G has the stated derivative sign: its numerator is t(4pi-(pi^2-4)t), while its denominator is positive. G increases and then decreases to zero from above. Reciprocity supplies the other bound, and continuity plus endpoint limits supplies every intermediate value. Monotonicity of the ratio is not assumed or needed.

Thus the four-atom measure is realizable exactly when 2/(pi+2)<m<pi/(pi+2), and no nonsymmetric body can change that conclusion. At the upper endpoint the other pair has mass 2/(pi+2), so the maximal line mass is exactly the stated threshold. This is the required sharpness example against both a larger strict constant and an endpoint-allowing closed constant.

## 7. Negative parameters below -1 and critical-point limitations

For s>1, the pair ratio tends to infinity at zero aspect ratio and to zero at infinite aspect ratio. Continuity suffices to realize each positive pair-mass ratio. Dilation adjusts total mass. The oblique-pair exterior angle is also correct: computing cross and dot products of the incident edges gives atan2(2t sin(alpha),1-t^2), in (0,pi). Its complementary angle and its two endpoint asymptotics give the same existence conclusion.

These examples can carry line mass arbitrarily close to one. They show that the sufficient bounds are not necessary conditions on individual solutions. They do not prove a universal guarantee near one.

For line/perpendicular data the join's moment gain is order t^s but its entropy cost is order t. For every fixed positive m and s>1, the objective decreases for sufficiently small t. This establishes failure of that variation to exclude a collapse, without proving that the collapse is globally maximizing or that a solution does not exist.

In the equal-data planar aspect family, direct normal-fan differentiation gives H'(x)=(2/pi)atan(exp x) and F_s''(0)=s/4-1/pi. When s>4/pi the diamond is a strict local minimum along that family, yet its four exact curvature masses match the data after dilation. Hence it cannot be a global maximum. This is a sufficient counterexample to the invalid converse; no assertion of a local minimum in all shape directions is made.

For 1<s<4/pi, the ratio's positive derivative at unit aspect and its opposite endpoint limits provide two additional crossings of level one, besides the central crossing. The rotated outer solutions are distinct as fixed-coordinate subsets. No uniqueness theorem is presumed.

## 8. Independent controls and their limits

The author verifier and mathematical controls reproduced normally and under Python -O after extraction into a separate directory. Corruption controls cover changed proof bytes, a missing file, an added file, and changed saved numerical results. The input ZIP and author files remain byte-identical.

The separate independent_checks.py imports no author code. It performs 100 finite high-precision controls using angular beta integrals, direct consecutive-edge turning angles, direct integration over polygon normal fans, two-sided vertex perturbations, explicit measure/dilation checks on a nonsmooth hexagon, oblique quadrilaterals, boundary second-order terms, and the p<-1 barriers. Both normal and optimized Python runs reproduce its saved JSON.

These controls are regression evidence only. They are not a discretization proof of arbitrary-measure existence, an interval certificate, a search over all convex bodies, or a substitute for Sections 2-7 of this deductive audit.

## 9. Required corrections, interpretation limits, and remaining gap

No required mathematical correction was identified. CORRECTIONS.md records optional clarifications. The author freeze should remain immutable; a current audit wrapper should supersede its historically correct “independent review pending” labels without rewriting them.

The full original target remains unresolved for every p<-1 parameter range claimed as unsolved by the author, and higher-dimensional p=-1 sharpness remains unproved. The lower-rank variational obstacles have not been replaced by a degree, minimax, or other existence/nonexistence argument for general measures. A good partial theorem does not justify relabeling the full record solved.

The audit's mathematical acceptance is separate from its literature assessment. The 2026 Feng-Hu-Li-Lv abstract reports endpoint nonexistence and negative-parameter nonuniqueness, but its complete text was not accessible in the checked official route. The previously unverified Yang-Hu planar-paper lead has now been authenticated through its official journal issue and abstract; its full text was blocked by a slider-guard page. SOURCE_UPDATE.md gives the exact bibliographic update. Neither unavailable full text was bypassed. No priority or originality conclusion follows from the present source search. SOURCE_AUDIT.json records the bounded source and repository checks.
