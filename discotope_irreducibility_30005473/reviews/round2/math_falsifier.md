# Independent mathematical falsification audit, round 2

**Checkpoint:** 2026-10-01 04:13:32 UTC (2026-09-30 21:13:32 PDT).  
**Completion estimate:** 100% of the assigned mathematical audit scope. This is a task-completion estimate, not a probability that the theorems are correct.  
**Object audited:** `paper.tex`, SHA-256 `3576dcc78bf1a9188ee8a8b5c56f5914357d90d437767e29dc42e3a85ceedab4`.  
**Independence:** I read the current manuscript and did not read earlier reviews, verdicts, or their check scripts. I did not edit the manuscript, commit, push, or contact anybody. Citation accuracy and source/package completeness are outside this mathematical subaudit.

## Verdict and exact scope

I found no counterexample or mathematical gap in the two stated theorems. The universal theorem follows from the stated lemmas and the exact characterization of singleton support faces. The generic theorem follows from the surjectivity of the simultaneous projection map for the collapsed summands. The nongeneric separator is correct.

The strongest result verified by deductive review is: for every finite sum of centered ellipsoidal balls of real ranks at least two, including dependent or repeated summands and lower-dimensional sums, the complex Zariski closure of the exposed-point set is irreducible. For a full-dimensional sum satisfying (GP), the generator of the purely nonlinear part is contained in the Euclidean closure of the exposed points, so the two complex Zariski closures agree.

The remaining limits are specific: this is an independent AI mathematical audit, not formal proof certification or human peer review; the finite computations do not establish the universal statements; the historical conjecture-identification claims depend on the primary-source audit being performed separately. No stronger claim about the complex critical locus, degrees, or necessity of (GP) follows from this argument.

## Universal theorem: attempted failure mechanisms

### Singleton faces and exact normal domain (lines 132–166)

For an injective map `A_i`, maximizing `u·A_i v` over the unit ball is precisely maximizing `(A_i^T u)·v`. If that projection is nonzero, Cauchy–Schwarz has exactly one equality vector, and the image is the point in equation (2). If the projection is zero, every vector in the ball maximizes, and injectivity makes the entire positive-dimensional disc a nonsingleton face.

There is no possible cancellation of nonsingleton summand faces. Fixing one point in every other face embeds the remaining face into the Minkowski-sum face by translation. This settles the most plausible hidden dependency error: even repeated, opposite-coordinate, or overlapping faces cannot sum to a singleton because the Minkowski sum permits independent choices. Hence the exceptional set is exactly the union of the kernels, rather than merely a sufficient exceptional set. Every point in `F(U)` is exposed by its defining nonzero normal, and every exposed point comes from a normal in `U`.

Lower dimensionality introduces a common kernel, but all individual kernels still have codimension `m_i`. Normals orthogonal to the entire sum expose the entire sum and therefore do not produce an extra exposed point. Excluding them is correct. The positive-dimensional hypothesis also excludes the exceptional singleton-body convention.

### Connectedness and analytic primeness (lines 93–130)

The broken-segment proof is valid: for each excluded codimension-two-or-more space `M_i`, both `M_i + R x` and `M_i + R y` remain proper spaces. A point outside their finite union produces two segments that do not hit any `M_i`. The proof covers the limiting ambient dimension `d=2`, where the kernels of rank-two summands are just the origin. Repeated kernels and a positive-dimensional common kernel do not change it.

I checked that the analytic argument proves complex primeness, rather than only real primeness. For complex-coefficient polynomials, composition with the real-analytic map is a complex-valued real-analytic function. At any point where `P∘F` is nonzero, continuity supplies an open neighborhood where it is nonzero. If `(PQ)∘F=0`, `Q∘F` vanishes on that neighborhood. Its real and imaginary parts both satisfy real-analytic uniqueness on the connected domain, so `Q` vanishes on the whole image. The nonempty image makes the ideal proper. The vanishing ideal is unchanged by complex Zariski closure, giving the usual equivalence between a prime vanishing ideal and an irreducible affine algebraic set.

The manuscript's additional uniqueness argument is sufficient: the neighborhood-zero locus is relatively closed because all derivatives vanish at a limit point, and real analyticity supplies a convergent Taylor expansion there. No simply connected domain, complex analytic continuation, or global complex radical branch is needed.

As a stress test on the logical role of analyticity, mere connectedness or smoothness would be insufficient. A smooth map on the real line that equals `(exp(-1/t^2),0)` for positive `t`, `(0,exp(-1/t^2))` for negative `t`, and `(0,0)` at zero has reducible complex Zariski closure `XY=0`. The actual support map is real analytic on its entire stated domain; it does not have this defect.

### Proportional radicals, nonorthogonal ellipses, and embedded sums

I independently tested

`A = [[2,1],[0,3],[0,0],[0,0],[0,0]]`, `D_1=A B^2`, `D_2=2A B^2` in `R^5`.

This combines a nonorthogonal ellipse, exactly proportional quadratic radicals, coincident summand spans, repeated shape, and a three-dimensional common ambient kernel. Here `D=3A B^2` and the exposed image is the ellipse

`(3X-Y)^2 + 4Y^2 = 324`, `X_3=X_4=X_5=0`.

Seven exact rational unit vectors were checked with independently constructed normals satisfying `A^T u=v`. In each case the support sum is exactly `3A v` and satisfies the displayed conic. The conic is smooth and irreducible over `C`; this also supplies a directly identifiable algebraic answer in a highly degenerate example. The universal argument does not require independence of the radicals or injectivity of `F`.

## Generic theorem: simultaneous collapsed faces

### Deductive review (lines 177–234)

At a supporting normal `u`, every decomposition of a supported sum point has each support deficit zero, since the deficits are nonnegative and sum to zero. No uniqueness of the given decomposition is assumed or needed.

All collapsed spans lie in `u^perp`. Under (GP), their total dimension cannot reach `d`: that would force their sum to be all of `R^d`, contradicting the nonzero normal. Their dimension sum is therefore at most `d-1`, and (GP) says the concatenated map has that exact rank. Thus its columns are independent, its transpose is surjective, and all prescribed unit vectors `v_j` can be imposed simultaneously. The manuscript prescribes `A_j^T w=v_j`, which is the correct condition even for nonorthogonal matrices; prescribing the ambient points themselves or their Euclidean orthogonal projections would have been incorrect.

For positive epsilon the collapsed summand point is exactly fixed, since normalization cancels the positive epsilon. Every noncollapsed projection remains nonzero for sufficiently small epsilon, by continuity and finiteness of the index set. The resulting normals are genuinely in `U`. Taking their exposed support sums gives the desired limit, and complex algebraic sets are Euclidean closed. The `J` empty case is separately correct. Full-dimensional summands also cause no problem: their normal projections never collapse for a nonzero normal.

The simultaneous Vandermonde construction makes (GP) nonempty for every allowed collection of block sizes. Rank failure for a specified subset is algebraic in the entries, and there are finitely many subsets, so the stated real Zariski-open conclusion follows. If the total size is below the ambient dimension, the generic spans are a direct sum. In that case every sum of relative-boundary points is already exposed by a suitable simultaneous projection normal; this independently checks the lower-ambient-span reduction without relying on a potentially ambiguous ambient-boundary convention.

### Exact nonorthogonal test with two collapsed summands

In `R^6`, use columns `c(t)=(1,t,t^2,t^3,t^4,t^5)^T` for `t=1,…,6`, blocked as `(1,2)`, `(3,4)`, `(5,6)`. These are strongly nonorthogonal rank-two ellipses. Exact Gaussian elimination checked all 63 nonempty column subsets and found their maximal possible ranks.

Let `v_1=(3/5,4/5)`, `v_2=(5/13,12/13)`. Independently solving the six projection equations produced

`u=(14,-941/30,25,-217/24,3/2,-11/120)`,

`w=(-6102/455,406477/13650,-17219/780,2685/364,-6187/5460,253/3900)`.

Their projection tuples are respectively `(0,0,0,0,3,4)` and `(3/5,4/5,5/13,12/13,1/7,-2/7)`. Consequently `J={1,2}`, both collapsed support points stay exactly fixed for `u+epsilon w`, and the third projection is `(3+epsilon/7,4-2epsilon/7)`. It never vanishes for real epsilon. Four rational positive epsilons were checked exactly.

There is also a reproducible error bound, with no floating-point inference. For `q=(3,4)` and `r=(1/7,-2/7)`, triangle and reverse-triangle inequalities give

`||(q+epsilon r)/||q+epsilon r|| - q/||q|||| <= 2 epsilon ||r||/||q||`.

Multiplying by the third matrix and bounding its operator norm by its Frobenius norm yields squared support-sum error at most `(289465228/245) epsilon^2`. This tends to zero and explicitly verifies the noncollapsed limit in the tested construction.

## Nongeneric separation and rank-one boundaries

The nongeneric construction in lines 245–258 is correct. Each vector in `e_1+(-e_1)+e_3` lies on its summand's relative boundary. The `e_3` support face is exactly `2B^2_xy+e_3`, so the sum point is on the boundary. For a regular normal, writing `a=2u_1/r`, `b=u_1/s` gives both `a^2+Y^2=4` and `b^2+Z^2=1`, and therefore the stated quartic is zero. This algebraic identity proves vanishing on all exposed points and hence on their Zariski closure. Four independent Pythagorean normals were evaluated exactly:

| Normal | Exposed point | Separator |
|---|---|---:|
| `(3,4,0)` | `(11/5,8/5,0)` | 0 |
| `(0,3,4)` | `(0,2,1)` | 0 |
| `(12,5,9)` | `(172/65,10/13,3/5)` | 0 |
| `(20,21,15)` | `(316/145,42/29,3/5)` | 0 |

At `e_3` the separator is exactly 16. This establishes strict separation of `S` and `E`; it does not depend on whether a selected real normal fails to expose the point. The repeated `xy` spans violate (GP), as required.

The rank-one examples are also correct. For a nonzero segment the kernel is a hyperplane, its complement disconnects, and the support image splits. For the stadium, a positive horizontal normal component selects the right endpoint of the segment and a negative component selects the left endpoint. A zero horizontal component produces a horizontal segment face, so the top and bottom endpoints of those arcs are not exposed. Each open semicircle is Zariski dense in its translated smooth complex circle. The two circles are distinct for positive `a`, and their union is reducible. Six exact branch points for three positive segment lengths satisfied their own circle and failed the other circle.

## Check artifacts and reproducibility

The public independent check script is [math_falsifier_exact_checks.py](math_falsifier_exact_checks.py); its captured output is [math_falsifier_exact_results.json](math_falsifier_exact_results.json). It uses only Python's standard library and exact rational arithmetic. Run it from the project folder with `python3 reviews/round2/math_falsifier_exact_checks.py`. It prints the audited manuscript hash and all check totals. All checks passed. The public copy differs from the original scratch script only in the manuscript-path locator needed for its new folder depth. These evidence artifacts do not replace the manuscript's universal deductive arguments.

**Portability checkpoint:** 2026-10-01 04:17:40 UTC; completion estimate 100%. The public script was copied to `tmp/round2/extracted/reviews/round2/` with an equivalent project-root `paper.tex`, run there, and its new scratch JSON compared byte-for-byte with the public captured JSON. They are identical. The original scratch script and result remain preserved.

No canonical changes are recommended by this audit. No unsupported route was promoted, and no unresolved mathematical gap was found within the stated scope.
