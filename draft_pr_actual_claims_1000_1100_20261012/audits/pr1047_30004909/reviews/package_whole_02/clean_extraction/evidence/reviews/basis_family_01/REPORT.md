# Adversarial audit of PR 1047 / problem 30004909

Head audited: `56b3a35182e5cb04b05e41f5017e47caf50582c1`.
Approach family: independent basis/cardinality-envelope reconstruction and exhaustive finite ordinary-matroid ranks.

## Verdict

**PASS for every mathematical claim in the nine-file submitted edition, under its explicit literal target.** No correction to a proof step or mathematical statement is required. This verdict concerns the specified dimension-independent constant, one ordinary matroid rank on the same finite ground set, and the exact two comparisons `r(S)/alpha <= f(S) <= alpha*r(S)` for all subsets. It does not certify bibliographic priority or a different intended question. Source interpretation is left to the separate primary-source family.

The strongest verified result is the complete nonexistence theorem for this literal target. The exact optimal-factor claim for the square-root family also holds among **all** ordinary matroids, not merely uniform matroids. Both rational-family lower bounds are valid for every positive integer m. There is no remaining mathematical gap within those claims.

## Independence and input identity

The initial input identity checks ran before inherited acceptance/audit labels were read. They verified all nine originals and SUBMITTED_PINS.json, checked actual local commit/tree/blob object contents against their Git identifiers, compared every submitted byte with its blob in the exact head, and checked that the complete head tree contains exactly the pinned nine-member problem package. The root tree is `460994102e10a1af434dd32a34f1abfed6be7681`; the full recursive tree has 158,741 entries. Initial and final identities are in INPUT_PINS_INITIAL.json and INPUT_PINS_FINAL.json.

INDEPENDENT_DERIVATION.md was saved and hash-frozen at the timestamp in DERIVATION_FREEZE.json before reading submitted ACCEPTANCE.md, README.md, SOURCE_AUDIT.md, STATUS.json, PROVENANCE.md, MANIFEST.json, ARTIFACT_MANIFEST.json, and SOURCE_PROVENANCE.json. The theorem statements in REPORT.md were read to define the audit target. No old audit or acceptance conclusion was used as a premise. The subsequent metadata reading found no stronger mathematical claim than those reconstructed below.

## Exact claim ledger

| Claim | Domain and quantifiers | Finding |
|---|---|---|
| No universal alpha | There is no single real alpha>0 working for every finite V and every nonnegative monotone submodular f with f(empty)=0 and f({i})=1, allowing M to depend on (V,f) | Proved by n>alpha^6 |
| Square-root validity | Every integer n>=1; every pair of subsets | Normalization, monotonicity, nonnegativity, and submodularity proved |
| Square-root lower bound | Every ordinary matroid on [n] and every real alpha>0 satisfying both comparisons on all subsets | alpha>=n^(1/6) |
| Exact fixed-rank envelope | Every integer n>=1 and every integer total rank 1<=R<=n | Uniform minimum is max(sqrt(R),sqrt(n)/R); every ordinary rank-R matroid has at least this factor |
| Global square-root optimum | Minimize the preceding envelope over integer R, among all ordinary matroids on [n] | Correct; no continuous-rank substitution |
| Cube sharpness | Every positive integer m, n=m^3 | Rank R=m attains alpha=sqrt(m)=n^(1/6) |
| Rational validity | Every positive integer m, n=m^2 | g_m(empty)=0; g_m(S)=(m+|S|-1)/m on nonempty S is rational, normalized, monotone, nonnegative, submodular |
| Rational bounds | Every admissible ordinary matroid and alpha>0 for that g_m | alpha^2+alpha>=m; alpha>=(sqrt(1+4m)-1)/2; alpha>=sqrt(m/2)=n^(1/4)/sqrt(2) |

The empty ground set does not obstruct the universal quantifier: both f and rank are zero there. It is sufficient to disprove the assertion on positive cardinalities.

## Proof reconstruction and adversarial checks

For a nonempty normalized domain, singleton rank is zero or one. The upper comparison at a singleton forces rank one, prohibits loops, and gives alpha>=1. Thus total rank R is an integer between one and n. Every denominator involving R or sqrt(R) is positive. Any alpha<1 fails already at a singleton. A basis exists by a finite cardinality maximum; its size and rank are both R. The selected basis can depend on the proposed approximating matroid because the comparison is quantified over every subset.

For square-root cardinality, successive increments equal `1/(sqrt(k+1)+sqrt(k))`, including k=0, and decrease. Comparing sums of increments at the intersection and union proves the all-pairs submodular inequality, including empty sums. A second derivation removes radicals from the set-pair check: with a=|A|, c=|C|, i=|A intersect C| and u=|A union C|, one has a+c=i+u and ac-iu=|A minus C|*|C minus A|>=0. Since both radical sums are nonnegative, their squared comparison proves `sqrt(a)+sqrt(c)>=sqrt(i)+sqrt(u)`.

At a basis the lower comparison gives `R/alpha<=sqrt(R)`, hence `R<=alpha^2`. At V the upper comparison gives `sqrt(n)<=alpha R<=alpha^3`. Taking powers of positive quantities gives the claimed sixth-root lower bound. Choosing an integer n>alpha^6 defeats every fixed proposed alpha. This proves a universal disproof, not only rejection of finitely many numerical factors.

For fixed integer R, the uniform rank is min(k,R) on a set of size k. Its `r/f` ratio is sqrt(k) up to R and R/sqrt(k) afterward, so its maximum is sqrt(R). Its `f/r` ratio is 1/sqrt(k) up to R and sqrt(k)/R afterward, so its maximum is max(1,sqrt(n)/R). As sqrt(R)>=1, the full factor is exactly max(sqrt(R),sqrt(n)/R). The basis and full-set evaluations force the same two terms on every ordinary rank-R matroid. This proves optimality among all matroids without any symmetry assumption. Minimizing over the finite integer set [1,n] preserves the integer constraint. At n=m^3, R=m is admissible and equalizes the terms. For n=2 the actual optimum is sqrt(2), illustrating that equality with n^(1/6) is not claimed for every n.

For g_m, the cardinality increments are one followed by 1/m, so monotonicity and submodularity hold independently of the submitted convex-combination argument. The latter is also correct, with nonnegative coefficients including m=1. At a basis,

`m <= alpha + alpha*(m-1)/R`.

At V, `m+1-1/m<=alpha R`, in particular `R>=m/alpha`. Since alpha>0, R>0, m>0, and m-1>=0, substitution gives

`m <= alpha + alpha^2*(m-1)/m <= alpha + alpha^2`.

This argument divides only by strictly positive quantities. It works for alpha=m, alpha>m, and m=1, so there is no omitted sign case involving m-alpha. The positive quadratic root gives the displayed root bound. Singleton normalization gave alpha>=1, so alpha+alpha^2<=2alpha^2 establishes the weakened n^(1/4)/sqrt(2) bound. At m=1 the actual best factor is one, while the weakened bounds are simply nonsharp necessary conditions.

An audit extension, useful for exact checks, is that the rational family's optimal fixed-rank factor is

`max(m*R/(m+R-1),(m^2+m-1)/(m*R))`.

This follows from the same monotone cardinality ratios and is not needed to certify a stronger submitted claim. Full details of the general concave-cardinality envelope are preserved in the frozen independent derivation.

## Exhaustive and exact finite evidence

The final independently written checker enumerates every nonempty family of equal-size candidate bases for n=1 through n=5, enforces basis exchange, constructs the rank on every subset, and independently validates integer bounds, monotonicity, and every rank submodularity pair. This enumerates all labelled ordinary matroids in that finite range, including loops; loops are then excluded by the singleton comparison. No original executable exists in the nine-file edition, so this is newly created evidence, **not replay of a submitted checker**.

The enumeration produces 2, 5, 16, 68, and 406 distinct matroid rank functions respectively, a total of 497. Their loopless counts are 1, 2, 6, 27, and 185. For every feasible R at each size, the minimum exact square-root factor squared equals `max(R,n/R^2)`; for the rational cases m=1,2, the minimum factor equals the exact rational envelope above. Every enumerated admissible matroid satisfies the claimed necessary bounds.

Additional exact sweeps cover 20,100 uniform square-root size/rank pairs with n=1..200, cube sharpness for m=1..100, and 9,455 uniform rational size/rank pairs with m=1..30. The direct submodularity checks include 87,381 square-root set pairs across n=0..8 and 262,404 rational set pairs across m=1..3. Integers and Python Fraction comparisons avoid floating-point tolerances. Square-root factors are compared via their exact squares, and square-root pair inequalities via the nonnegative squared-sum reduction. These finite checks supplement the proofs; they cannot establish the infinite claims by themselves.

Actual streams are checker.stdout.jsonl and checker.stderr.txt; CHECKER_RESULTS.json records the scope, counts, timings, and final checker hash. Initial and second streams/results are retained because scope wording was clarified and a direct square-root pair check was subsequently added. The final checker uses explicit require guards, no optimization-sensitive assertions, and runs with bytecode writing disabled.

## Counterexample and scope controls

- Dropping the lower comparison permits the free matroid with alpha=1 to satisfy the upper comparison for square-root cardinality at every n.
- Dropping the upper comparison permits U_(1,n) with alpha=1 to satisfy the lower comparison at every n.
- A nonuniform rank-two matroid on three elements with bases {1,3} and {2,3} has rank one on {1,2}. Therefore the shortcut “every rank-R matroid has rank min(|S|,R)” is false. The submitted proof does not make that shortcut; its all-matroid optimality uses only a basis and V.
- If scalar-rescaled ranks are allowed, the ordinary sixth-root inequality itself can fail: on n=16 use `(1/sqrt(2))*r_(U_(4,16))` with alpha=sqrt(2). All subset comparisons hold, while alpha^6=8<16. This is a finite modified-model control, not a conclusion about that modified model's universal theorem.
- Dropping singleton normalization allows f identically zero and the rank-zero matroid with every alpha>0. This shows that the nonloop/alpha>=1 inference depends on normalization; it is not an unsupported matroid assumption.

These controls find no hidden premise in the submitted literal claim. They identify which proof implications are genuinely dependent on its explicit model.

## Limits and completion

The proofs are elementary mathematical deductions. There are no empirical assumptions, units, numerical stability claims, oracle-learning assumptions, or randomization to audit. No outside individual was contacted, no other worker was consulted, and no Git service was accessed or modified by this family. No worldwide-first, novelty, or publication claim is made. Acceptance and status labels in the submission are treated as untrusted conclusions to check, not as verification evidence.

Mathematical audit completion: 100% of this family's assigned claims after final input identity and artifact checks. Source interpretation, provenance of historical review events, and publication priority require the separately assigned source family and are not certified by this report.
