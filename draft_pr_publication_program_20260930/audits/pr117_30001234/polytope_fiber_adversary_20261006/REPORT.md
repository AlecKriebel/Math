# PR117 independent augmented-polytope and fiber adversarial review

**Verdict: PASS for the complete augmented-LP counterexample and its required ideal hypotheses. No mandatory mathematical correction found in this family. Priority, historical openness, and publication readiness are not certified.**

Reviewed immutable PR117 head `8163ee0dc7a0f944570925984cef2dc0fb291ad8`. Candidate body: 10,573 bytes, SHA-256 `1409e8ad35d34f3cc4a9bb14f7e42318c1dd1e0446ecba525c655fad8c978cdf`. Source-record body: 4,949 bytes, SHA-256 `c815205b3bf1eeb3dd0d47ad93fcb1faedf360759d44bc605915ef4a66595ea5`.

The existing construction attempt remains 1/5. This is validation of the submitted construction, with zero new central proof-search turns. All work occurred in this family's dedicated directory; originals and other families' files were unchanged. No Git, index, ref, PR, publication, tracker, cache, or native-review action was taken.

## Independence and exact scope

I first read the full candidate and source record, then reconstructed the LP, wrote a different full-polytope proof, implemented an exact checker, and sealed `INDEPENDENCE_CHECKPOINT.json` before reading any original checker or review. Only afterwards did I inspect and reproduce the original author's checker and original review checker. I read no new parallel-family reports.

The mathematical target audited here is the source-record assertion

`exists z in F, for every z' in F with z' != z, A z' != A z`,

where the augmented matrix retains both exponent rows and `(I_3 I_3)`, the variables are nonnegative rational numbers, inequalities are nonstrict, and the objective sums all six coordinates. This family checked the formula supplied in the candidate/source record; it does not independently authenticate the primary PDF's typography, question numbering, or historical interpretation. That primary-source task belongs to the separate source family.

## Reconstruction from the actual generators

The three positive terms are `x1*y2`, `x2*y3`, and `x3*y1`; the respective negative terms are `x2*y1`, `x3*y2`, and `x1*y3`. With coordinates `(mu1,mu2,mu3,nu1,nu2,nu3)`, the six exponent rows and three augmentation rows are exactly

```
       mu1 mu2 mu3 nu1 nu2 nu3
x1      1   0   0   0   0   1
x2      0   1   0   1   0   0
x3      0   0   1   0   1   0
y1      0   0   1   1   0   0
y2      1   0   0   0   1   0
y3      0   1   0   0   0   1
f1      1   0   0   1   0   0
f2      0   1   0   0   1   0
f3      0   0   1   0   0   1.
```

Thus the nine inequalities are **all nine cross-part pair inequalities** `mu_i+nu_j<=1`. The objective is `sum(mu)+sum(nu)`. Each coordinate lies in `[0,1]`, so the associated real polytope is compact; its nonnegative rational points are the original feasible domain.

## Unrestricted proof of the entire polytope and optimal face

For an arbitrary real feasible point define `a=max_i mu_i` and `b=max_j nu_j`. Because every pair inequality is present, `a+b<=1`. If both are positive, then

`(mu,nu)=a*(mu/a,0)+b*(0,nu/b)+(1-a-b)*0`.

The normalized vectors lie in their respective three-dimensional unit cubes. If a maximum is zero, omit its zero-weight term. Conversely every point of either cube satisfies all nine inequalities, and so does every convex combination. Therefore the full real feasible polytope is

`conv(([0,1]^3 x {0}) union ({0} x [0,1]^3))`.

The fifteen distinct zero-one vertices of these cubes are exactly the vertices of this polytope: the common origin and seven nonzero points in each cube. Every such point is extreme because a zero-one point of `[0,1]^6` cannot be expressed as a nontrivial convex combination of different points in that box. No additional vertex can occur in the convex hull of these finite cube vertices. This is a complete written proof, independent of numerical or finite-grid tests.

For every feasible point,

`sum(mu)+sum(nu)<=3a+3b<=3`.

The endpoint `(1,1,1,0,0,0)` attains three. Equality requires `a+b=1` and every coordinate in each block to equal that block's maximum: a strict deficit in any coordinate would make the sum strictly smaller than `3a+3b`. Consequently the entire real optimal face is

`z(t)=(t,t,t,1-t,1-t,1-t)`, for `0<=t<=1`.

The entire rational optimal face is precisely the same expression with rational `t`. A rational optimizer has `t=mu1`, and every rational `t` produces rational coordinates. Each of the nine pair sums equals one, hence `Az(t)=1_9` everywhere on this face.

For any rational `t` in `[0,1]`, take `s=0` when `t!=0`, and `s=1` otherwise. Then `s` is rational and feasible, differs from `t`, and has the same augmented image. This proves the failure of the existential singleton-fiber condition at **every rational optimizer**, with no endpoint exception. The fact that the optimal image set is a singleton is the opposite of the asserted singleton-fiber property here: the fiber over that single image is the full nontrivial segment.

Moreover the objective equals the sum of the last three image coordinates. Any feasible point sharing an optimal image is therefore automatically optimal. Restricting the fiber to feasible points or to optimal points gives the same fiber for these images.

## Rank, kernel, and exact primal/dual certificate

If `(u,v)` lies in the homogeneous kernel, the nine equations are `u_i+v_j=0` for every `i,j`. Fixing one index in the second block forces every `u_i` equal; then all `v_j` are their negative. Thus the kernel is exactly the rational/real span of `(1,1,1,-1,-1,-1)` and the rank is five. The exact row-reduction checker independently obtains the opposite-sign generator, which spans the same kernel.

The feasible primal endpoint has value three. The dual vector `(0,0,0,0,0,0,1,1,1)` is nonnegative, its transpose image is the six-coordinate all-one objective vector, and its value is three. Weak duality suffices to certify the optimum; no floating-point computation, strict-feasibility assumption, or unproved optimizer existence is used.

## Algebraic hypotheses and permitted changes

At the point with all six variables equal to one, each generator vanishes but every nonzero scalar multiple of a monomial is nonzero. Evaluation is a ring homomorphism, so the polynomial ideal contains no monomial. All coefficients are one and all exponent vectors are nonzero, integral, and nonnegative.

The six degree-two monomials are pairwise distinct, so the three displayed binomials are linearly independent over any characteristic-zero field. The ideal is homogeneous and generated in degree two. Its degree-two part therefore has dimension three; all higher-degree elements are in the homogeneous maximal ideal times the ideal. The quotient by that multiple has dimension three, so fewer than three generators are impossible, including after localization at the homogeneous maximal ideal. This rules out a redundant-generator counterexample.

The candidate's optional primeness argument is also logically valid: the monomial parameterization `x_i -> s*z_i`, `y_i -> t*z_i` identifies precisely the monomials with equal column totals and equal total x-degree. An excess x-allocation at one index and a deficit at another ensures the first monomial contains the required `x_j*y_i` factor. Exchanging it for `x_i*y_j` is one of the three minor relations and reduces the allocation distance by two. The finite nonnegative integer distance gives termination for arbitrary degrees. Grouping a kernel polynomial by distinct target monomials then shows each group is a sum of these monomial differences, since its coefficients sum to zero. The quotient is a subring of the target domain. Primeness is unnecessary for the LP counterexample.

Reordering generators, exchanging their two terms, and permuting ring variables give invertible coordinate/row permutations. They preserve the objective and all fiber cardinalities. The checker verifies all 48 generator-order/orientation cases and all 720 variable-order cases. Nonzero generator scalar multiples do not change exponents. Invertible diagonal variable rescalings preserve the ideal's hypotheses and exponent matrix; the induced coefficient ratios satisfy cyclic product one. Arbitrary unrelated binomial coefficients are not covered: a cyclic product other than one makes the full six-variable product belong to the ideal. The explicit coefficient control detects this hypothesis failure.

## Reproduction and adversarial controls

The independently written standard-library checker passed **1,729 explicit exception guards in each normal and optimized (`-O`) execution**, PIDs 59080 and 59082, both reaped with exit zero and empty stderr. The mathematical JSON outputs agree exactly after removing the intentionally different optimization flag. Exact rational enumeration considers all **5,005** six-row active-basis choices; **1,792** are nonsingular, and the resulting **15** vertices have precisely the two expected optimal endpoints. The convex-decomposition proof above provides independent completeness, rather than inferring the entire face from sampling.

Meaningful controls include:

- Five altered-source-matrix mutations are rejected: missing augmentation, one missing augmentation row, omitted lower-right identity, a changed exponent, and paired-column ordering without coordinate relabeling. Some omissions happen to preserve this example's optimal face; rejection authenticates the exact target matrix and does not falsely claim each omission must destroy the mathematical phenomenon.
- Keeping only the first two genuine generators gives a rank-four injective augmented map with optimum two and two distinct optimal vertices. The source condition then holds despite optimizer nonuniqueness. This prevents conflating a nonunique optimizer with a non-singleton image fiber.
- Both actual endpoints and rational points very near them have explicit distinct rational partners. The universal partner argument proves every rational case, rather than relying on these diagnostic instances.
- Replacing nonstrict inequalities by strict inequalities excludes the optimal endpoints. In that altered problem, the three bottom inequalities force objective strictly below three, while scaled segment points approach three; there is a supremum but no maximizer. Thus the actual nonstrict convention is essential to the claimed attained optimum.
- Adding a duplicate fourth binomial gives degree-two rank three with four displayed generators, detecting loss of minimality.
- For compatible variable rescalings, a nonzero evaluation point still annihilates all three binomials. For incompatible coefficients `(2,1,1)`, the polynomial identity checked exactly expresses the negative full six-variable product as a combination of the three modified generators, detecting loss of the monomial-free hypothesis.

After sealing the independent construction, I read the original author/review code and full review. I reproduced both on private copies in this family's folder, without writes to the originals. Their result bodies reproduce **byte for byte**: original author 3,045 assertions, PID 60289; original review 5,368 assertions, PID 60292. Both were reaped normally with empty stderr. Both original codes use Python `assert`, so this comparison certifies their normal-mode runs only; it makes no claim that their guards remain active under `-O`. The new independent code uses explicit exceptions and was actually tested in both modes.

## Findings and remaining boundaries

Mandatory findings in this family's mathematical scope: **none**. The augmented matrix, complete optimal face, rank/kernel, universal rational fiber failure, and required ideal hypotheses check out. Original and independent results agree.

Historical priority and whether the numbered question remained genuinely open are not established by this report. I did not audit later literature claims, threshold values, or publication metadata. The mathematical verdict must not be promoted to a novelty verdict or human peer review. A future verification package can use the new explicit-guard checker alongside the original historical normal-mode receipts.
