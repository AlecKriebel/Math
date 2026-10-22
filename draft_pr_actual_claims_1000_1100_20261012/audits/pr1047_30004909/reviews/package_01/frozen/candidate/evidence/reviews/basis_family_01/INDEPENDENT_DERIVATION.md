# Independent mathematical reconstruction, before inherited verdict labels

Recorded UTC: 2026-10-13T23:07:05.908681+00:00. Checkpoint completion estimate: 40%.

Inputs consulted so far: the assignment's exact literal target, submitted REPORT.md, SUBMITTED_PINS.json, and actual local Git objects at 56b3a35182e5cb04b05e41f5017e47caf50582c1. I have not read submitted ACCEPTANCE.md, README.md, SOURCE_AUDIT.md, STATUS.json, PROVENANCE.md, or any previous audit. I do not use their conclusions as premises.

## Exact claim and logical domain

The target is a single positive real alpha that works for every finite ground set V and every nonnegative monotone submodular f with f(empty)=0 and f({i})=1, with a single ordinary matroid M on V permitted to depend on (V,f). Both inequalities must hold for every S subset V:

r_M(S)/alpha <= f(S) <= alpha r_M(S).

The matroid is unweighted and unscaled. The denominator on the left is alpha, and that inequality is needed to control the approximant's rank on an independent set. The counterexamples choose V=[n] for positive integers n. The empty ground set, if quantified, is harmless: the only relevant f and matroid rank are identically zero. No growth claim is inferred from a finite computation.

For nonempty V, singleton ranks are in {0,1}. The upper inequality 1 <= alpha r({i}) forces every element to be a nonloop and alpha >= 1; hence total rank R is an integer in [1,n]. This disposes of alpha < 1 and rank zero before any division by R. A basis exists by maximizing cardinality over the finite independent sets; it has size R and rank R. No representability assumption is needed.

## A general envelope mechanism, derived directly

Let f(S)=h(|S|), with h(0)=0, h(1)=1, h nondecreasing, and its increments nonnegative and nonincreasing. Then h is submodular as a set function: for A,C, write t=|A intersect C|, a=|A minus C|, c=|C minus A|. The a increments starting at t have at least the sum of the a increments starting at t+c. This is exactly f(A)-f(A intersect C) >= f(A union C)-f(C); empty sums cover all containments and empty sets.

The same increment conditions give h(k) <= k and nonincreasing h(k)/k for k>=1: h(k)/k is the average of the first k increments, and each additional increment is no greater than that average. In particular all h(k)>0 for k>=1.

Any admissible matroid of total rank R must have alpha >= R/h(R) by evaluating the lower inequality on a basis, and alpha >= h(n)/R by evaluating the upper inequality on V.

For U_(R,n), r(S)=min(|S|,R). On 1<=k<=R, k/h(k) increases and h(k)/k decreases; on R<=k<=n, R/h(k) decreases and h(k)/R increases. Therefore the maximum of all r/f ratios is R/h(R), and the maximum of all f/r ratios is max(1,h(n)/R). Since R/h(R)>=1, the smallest valid two-sided factor is exactly

E_h(R)=max(R/h(R),h(n)/R).

Thus, for each total rank R, the uniform matroid attains the universal basis/full-set lower envelope. Taking the minimum over integer R in [1,n] gives the optimum over ALL ordinary matroids, without assuming an optimal matroid is symmetric, uniform, or representable. Matroids with loops cannot be competitors.

## Square-root function, all n and all integer ranks

h(k)=sqrt(k). Its increments for k>=0 equal 1/(sqrt(k+1)+sqrt(k)), and the denominator increases strictly with k, so the required increment properties hold. At k=0 the denominator is one, so there is no zero denominator. h is nonnegative, normalized, and monotone.

The exact total-rank-R envelope is E(R)=max(sqrt(R),sqrt(n)/R) for every positive integer n and every integer R in [1,n]. Equivalently E(R)^2=max(R,n/R^2), useful for exact rational computation without numerical square roots.

If the comparisons hold, the basis implies R/alpha<=sqrt(R), hence R<=alpha^2. The full set implies sqrt(n)<=alpha R<=alpha^3. All quantities are positive, so taking the sixth root gives alpha>=n^(1/6). Given any fixed alpha>0, an integer n>alpha^6 exists and defeats it. This is a quantified disproof of the literal universal claim.

The exact global optimum is min_(integer 1<=R<=n) max(sqrt(R),sqrt(n)/R). Put x=n^(1/3). The first term increases in R, the second decreases, and their unique crossing is at R=x. Therefore a minimizing integer lies among floor(x),ceil(x), with duplicate values and inadmissible values discarded. At n=1 these both equal one. At n=m^3, m is a positive integer and R=m is admissible; both terms equal sqrt(m)=n^(1/6). This proves the claimed sharpness for that family. It does not assert equality for all integer n: n=2 has optimum sqrt(2)>2^(1/6).

## Rational family and denominator-safe route

For a positive integer m, let n=m^2, h(0)=0, and h(k)=(m+k-1)/m for k>=1. Its increments are 1 followed by 1/m repeated, nonnegative and nonincreasing because m>=1. This independently verifies submodularity without relying on a decomposition into rank functions. Values are rational, singleton values are exactly one, and every nonempty value is positive.

For any admissible matroid, alpha>=1, R>=1, and at a basis

mR<=alpha(m+R-1), hence m<=alpha+alpha(m-1)/R.

At V, h(n)=m+1-1/m >= m, hence R>=m/alpha. As alpha,R,m are positive and m-1>=0,

m <= alpha+alpha(m-1)/R <= alpha+alpha^2(m-1)/m <= alpha+alpha^2.

All inequality directions remain valid at m=1; the product with m-1 is simply zero. There is no division by m-alpha. From alpha>0 and alpha^2+alpha-m>=0, alpha >= (sqrt(1+4m)-1)/2. Since alpha>=1, alpha^2+alpha<=2 alpha^2, and alpha>=sqrt(m/2)=n^(1/4)/sqrt(2). The reported bounds are necessary and need not be tight at small m. At m=1,n=1 the actual optimum is one.

The general envelope additionally gives the exact fixed-R optimum for this family:

max(mR/(m+R-1),(m^2+m-1)/(mR)), 1<=R<=m^2.

The first term is at least one because (m-1)(R-1)>=0. This further formula is my audit deduction, rather than a submitted claim. It is available for finite exact cross-checks.

## Adversarial boundary and altered-model checks

1. Alpha<1 cannot work on a normalized singleton, so a proof invoking alpha>=1 is justified here.
2. Rank zero or a loop immediately violates the upper singleton inequality; excluding them is necessary, not an assumption imposed on an otherwise feasible solution.
3. Omitting the left comparison destroys the obstruction: U_(n,n) has r(S)=|S|>=sqrt(|S|), so the upper comparison alone holds with alpha=1 for every n.
4. Omitting the upper comparison likewise destroys it: U_(1,n) satisfies r(S)<=sqrt(|S|) for every S with alpha=1.
5. The claim is not a statement about one fixed finite V. On fixed n, the free matroid supplies a finite bound, and n^(1/6) remains finite.
6. Neither n^(1/6) sharpness for all functions nor a tight n^(1/4)/sqrt(2) bound is asserted or proved.
7. The all-matroid optimality argument uses one actual basis, not the unjustified assertion that all matroids of rank R have uniform rank on every set. For example a rank-two matroid on three elements with {1,2} parallel has r({1,2})=1, while U_(2,3) gives rank two. This is a concrete refutation of that hidden shortcut; the lower-envelope argument remains valid.

Preliminary mathematical verdict: the exact displayed claims in REPORT.md are correct under the stated literal target. Remaining audit work: finite exhaustive rank-function checks, fault-sensitive sanity controls, reading the submitted metadata for any additional mathematical claims or overstatement, final identity checks, and final report. Source interpretation and bibliographic priority are assigned to a separate approach family; no claim of novelty or publication is made here.
