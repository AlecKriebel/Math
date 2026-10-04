# Independent whole-current source-first review

Started UTC: 2026-10-03T00:17:33.492115+00:00

Completion estimate: 5%. No full candidate proof or acceptance script read yet.

Independent initial mathematical derivation from the stated target:

Let P consist of n distinct planar points and let r_p count distinct distances from p to other points. The supplied statement says integer distances; the literal scope must be checked carefully: either all mutual distances are integral or only the integers among arbitrary distances are counted. The advertised all-line and circle and two-pin bounds assume r_p counts all realized distances, so a literal mismatch is an immediate falsifier to test.

For collinear P and any p, each distance value reaches at most two other points, hence r_p >= ceil((n-1)/2), and trivially r_p <= n-1. Therefore the possible integer r values occupy ceil(n/2) integers, so sigma <= ceil(n/2). Equally spaced collinear points have r at position i equal to max(i,n-1-i), realizing every integer from ceil((n-1)/2) to n-1 and attain ceil(n/2).

For n points on a positive-radius circle, fixed p and fixed distance d>0 have at most two other points on that circle. Same interval and same sigma bound follow, but attainment for every n must not be assumed.

For two distinct pins p,q with all realized distances counted, each other point belongs to intersections of circles centered p,q at one of r_p and r_q radii. There are at most two points per ordered pair, hence n-2 <= 2 r_p r_q. If sigma distinct r values occur and the smallest two values a<b are present, b <= n-sigma+1, a <= n-sigma, so n-2 <= 2(n-sigma)(n-sigma+1). Solving x(x+1)>=(n-2)/2 with x=n-sigma gives sigma <= n-(sqrt(2n-3)-1)/2. This requires sigma>=2 to select distinct representative pins and must use real-valued bound or an explicit floor. For sigma=1, the displayed upper bound can fail at small n if inappropriately asserted.

Near-line/circle with t exceptions: every core point has at least ceil((n-t-1)/2) core-distance values, at most n-1 overall. Therefore core values lie in an interval of length n-ceil((n-t-1)/2), and exceptions add at most t distinct values, giving sigma <= min(n,n+t-ceil((n-t-1)/2)). A stronger interval upper bound n-t-1+t=n-1 is same. Edge case no core or singleton core should be handled.

Generic separated gluing: a per-pin partition into one internal palette (size <= max block size-1) and unique cross-block distances (one per outside point) yields r_p=n-|B_p|+r_p(internal), a deficit d_p=|B_p|-r_p(internal) in {1,...,max block size-1} for nonsingleton blocks when internal degree >=1. Singletons have deficit 1 and all coincide with existing possible range only if max block >=2. All-singleton configuration r_p=n-1 gives sigma=1; formula sigma<=max block-1=0 is false unless separately excluded. Nongeneric collisions alter the formula and cannot receive this bound by implication.

Adversarial targets: exact literal distance scope; singleton and n<3 cases; unproved universal collision control; overclaim to fixed-proportion disproof/full solution/novelty; static evidence presented as current execution; circular saved-vs-actual receipts; foreign authored closure inclusion.
