# Root preliminary mathematical derivation

This records root deductions from the full submitted REPORT, followed by fresh direct original-source inspection. The old SOURCE_AUDIT was also read for comparison; its acceptance labels are not mathematical premises. Two NEW distinct basis and primary-source reviewers remain pending, so this is not final acceptance or priority clearance.

## Literal target and success criterion

The target is one universal positive factor for every finite ground set and normalized monotone nonnegative submodular function, using one ordinary matroid rank on that same set and both comparisons r/alpha <= f <= alpha r on EVERY subset. The source's actual left denominator is essential. The complete original printed2946 contribution has no weights, extra scalar multiplier, expanded set or sum of ranks. It says constant without a separate V quantifier; the dimension-independent interpretation must stay explicit. A source naming slip uses f for the rank in a sentence but r in its display. Different intended formulations are unverified.

## Square-root counterfamily

For n>=1, f(S)=sqrt(|S|). Decreasing increments d_k=1/(sqrt(k+1)+sqrt(k)) imply the full submodular inequality: if t=|A intersect C|, a=|A minus C| and c=|C minus A|, compare the a increments starting at t and t+c. Empty sums are valid. All remaining normalization, monotonicity and positivity conditions hold.

For every singleton, the upper comparison excludes loops and forces alpha>=1. Finite ground sets have a basis B of size R=r(V)>=1. Since comparisons hold for ALL subsets, the basis may depend on the proposed approximant. The lower comparison at B is R/alpha<=sqrt(R), hence R<=alpha²; the upper comparison at V is sqrt(n)<=alpha R<=alpha³. Thus alpha>=n^(1/6). Choosing an integer n>alpha^6 refutes any fixed factor. No oracle or runtime restriction is used.

For any matroid of total rank R, the same two evaluations force alpha>=max(sqrt(R),sqrt(n)/R). A uniform U_(R,n) attains exactly that bound: for k<=R the two ratios are sqrt(k) and1/sqrt(k); for k>=R they are R/sqrt(k) andsqrt(k)/R. Their global maximum is the displayed bound, including k=R and n=R. Therefore minimizing over integer 1<=R<=n gives the optimum among all matroids, not only uniform ones. When n=m³ and R=m, factor sqrt(m) attains n^(1/6). This is sharp only for this particular family. For n=1 it is exactly1; no n=0 denominator case is needed for the counterexample, and the empty ground set satisfies the original comparison vacuously.

## Rational strengthening

For integer m>=1 and n=m², define g(empty)=0 and g(S)=1+(|S|-1)/m otherwise. It equals (1-1/m)u+(1/m)|S| where u=min(|S|,1). The latter is an ordinary rank-one uniform rank: its submodularity follows directly by checking empty/nonempty intersections, and cardinality is modular. Nonnegative coefficients give monotone submodular g; singletons equal1. This does not claim a single ordinary matroid represents g.

Singletons again force R>=1 and alpha>=1. At a basis, R/alpha<=(m+R-1)/m, or m<=alpha+alpha(m-1)/R. The full-set upper comparison gives alpha R>=m+1-1/m>=m and hence R>=m/alpha. Because m-1>=0, substitution has the correct direction: m<=alpha+alpha²(m-1)/m<=alpha+alpha². Its nonnegative root gives alpha>=(sqrt(1+4m)-1)/2; alpha>=1 further gives m<=2alpha², so alpha>=sqrt(m/2)=n^(1/4)/sqrt2. No division by m-alpha occurs. For m=1, g is cardinality on a one-element set and the weaker quadratic lower bound is compatible with the singleton alpha>=1. No optimality exponent over all normalized submodular functions is inferred.

## Current boundaries

The family proofs appear complete, with no numerical computation needed to prove the universal contradiction. Fresh finite checks can corroborate but cannot substitute for the all-matroid basis argument. The original nine-file edition has no executable or fixture to replay. Source interpretation and global priority remain separate obligations. No worldwide originality, new literature discovery, current openness, human review or formal certification is asserted. Full final mathematical adoption waits for both fresh assigned families and root comparison of their complete reports.
