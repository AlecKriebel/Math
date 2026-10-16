# Independent proof audit before prior verdicts

Recorded 2026-10-03 02:30 UTC. The reviewer reconstructed primary sources first, then read TURN_1.md through TURN_5.md, RESULT.md and check_turn_3.py through check_turn_5.py. No prior review verdict or prior independent checker was read before this audit and the new triple/deletion controls were completed.

## Target and normalization

The original conjecture is the arbitrary finite mono-constrained problem, all real x,y in (0,1], all integer k>=1, x+ky>1 and kx+y>=1, with a C vertex reaching at least |A|/k distinct endpoints. It has no reverse degree assumptions. Candidate Turn 3-4 address the strict symmetric-threshold subregion x,y>1/(k+1), with uniformly weighted A and bounded cardinality n. They correctly retain arbitrary positive probability weights on B and C.

For uniform A and below-1/k reach, the integer rank is ceil(n/k)-1=floor((n-1)/k), including n divisible by k. Any occurring B neighborhood is contained in a C reach set, since its B vertex has positive C degree. Hence its size is at most r. This is a deduction, not an assumed universal normalization or a replacement by inclusion-maximal neighborhoods.

Here t counts distinct occurring neighborhoods of size exactly r. Those have maximum allowed cardinality. It does not count all inclusion-maximal types of smaller cardinality. Empty B neighborhoods are harmless, but all A vertices are covered because x>0. No uniformization, deletion, laminarization, or size reduction of arbitrary A is proved by this step.

## Turn 3 checks

For an occurring r-type T, all neighbors of a representative B vertex lie in the C class having exact reach T. These classes have gamma mass at least y and are disjoint for distinct T. If k such types existed, a B type contained in none of them could see mass at most 1-ky<y. Thus every B type lies in one of the selected k types. Their union must cover A, contradicting n>kr. This proves t<=k-1. The same reasoning covers r=1; r=0 contradicts positive first degree immediately.

For r>=2, charges 1/r on U and 1/(r-1) elsewhere give every occurring B type charge at most one. Summing the forward A degree inequalities gives

    x <= r(r-1)/(rn-|U|) <= (r-1)/(n-t) <= (r-1)/(n-k+1).

Every denominator is positive: rn-|U| >= (r-1)n>0 and n-t>=n-k+1>0. The direction of each inequality is correct because |U|<=rt and t<=k-1. Overlap strengthens the first bound. The derived lower bound t>=n-(r-1)/x is equivalent and uses x>0.

For n<=4k, r<=3. The r=2 lower size n>=2k+1 gives x<=1/(k+2), and r=3 gives x<=1/(k+1). Thus strict x>1/(k+1) is essential. The n=9,k=2 relaxation has total B mass 1, degree 3/8, and unit charge on each type. Its attempted completion requires 10y<=4(1-y), hence y<=2/7. This is correctly a nonrealizable first-incidence relaxation, not an original counterexample.

## Turn 4 checks

For 4k+2<=n<=5k, r=4 and the Turn 3 inequality gives x<=3/(n-k+1)<=1/(k+1). At the sole remaining size n=4k+1, t<=k-2 would give the same contradiction. Therefore exactly k-1 four-types occur. Removing their disjoint exact-reach C classes leaves gamma mass at most 1-(k-1)y<2y. Any two residual B vertices of C degree at least y therefore have a common C neighbor; their A neighborhoods have union at most four. This uses no C-to-B minimum degree.

Residual triples pairwise intersect in at least two. Two different triples with intersection {a,b}, together with any triple not containing {a,b}, force all triples into their four-vertex union. The classification is correct, including empty and singleton families. In the four-set alternative without a common pair, at least three distinct triples occur and their common intersection has size one or zero.

For no triples the charge total is at least k+3/2. For a common pair P, charges 1/4 on U union P and 1/2 outside give total at least k+1. Contained types stay within U and have charge at most one; every residual triple and pair also stays at most one.

In the nonstar four-set case, the base charge total is

    Z=n/2-|U|/4-|D minus U|/6.

If |U|<=4k-5 it is at least k+13/12, and if |U|=4k-4 with D meeting U it is at least k+1. The only exception is |U|=4k-4, D disjoint from U, with exactly one remaining A vertex w. It occurs in no triple or contained type. A residual pair containing w must use a vertex in the common intersection I of all triples. For |I|=1 the special charges U:1/4,w:1,I:0,D minus I:1/2 have total k+3/2 and bound every used type. For |I|=0 no pair containing w can occur, and U:1/4,D:1/3,w:1 has total k+4/3. Zero charge on I is legitimate in a nonnegative dual certificate, independently of positive graph weights.

Thus the universal algebraic proof establishes the stated bound n<=5k for uniform A, all k>=2, strict x,y>1/(k+1), arbitrary positive B,C weights. This conclusion does not follow merely from finite computation.

## Deletion stability scope, signs and boundaries

Turn 5's stated structural hypothesis is pairwise disjoint inclusion-maximal nonempty A neighborhoods. Every nonempty type belongs to exactly one maximal block, all A vertices are covered, and each block's assigned B mass is at least x. In a putative counterexample all block masses are strictly below 1/k, so m>=k+1. Averaging reach gives y<1/k. For m>=k+2,

    kx+y<k/m+1/k<=k/(k+2)+1/k<=1

for every k>=2 (the last inequality is equality at k=2). For m=k+1, two blocks have combined A mass strictly greater than 1/k by complementing the other k-1 blocks. Thus the representatives' C neighborhoods are pairwise disjoint. Together m*x<=1 and m*y<=1 contradict x+ky>1. The proof permits partial reach into several blocks and does not incorrectly assert that all C vertices stay within one block.

Deleting exceptional B mass epsilon changes the guaranteed normalized A degree to x'=(x-epsilon)/(1-epsilon). The hypothesis 0<=epsilon<x<=1 ensures 1-epsilon>0 and 0<x'<=1. Denominators ky and k+y-1 are positive for k>=2,y>0. The strict wedge becomes epsilon<(x+ky-1)/(ky); the weak wedge becomes epsilon<=(kx+y-1)/(k+y-1). Directions and strictness are correct. At kx+y=1 the latter forces epsilon=0. A negative first numerator excludes any allowable epsilon. This is conditional on an actual structural deletion; neither existence nor smallness of such a deletion is supplied.

## Strongest claim and exact remaining gap

No substantive proof repair identified in the audited Turn 3-4 family or the deletion statement. Strongest verified relevant theorem: with uniform A, x,y>1/(k+1), every k>=2 and n<=5k force at least n/k distinct A reach. The structural Turn 5 theorem also supports the full asymmetric wedge on its explicitly restricted class.

Weighted support cardinality cannot replace uniform A cardinality: weights (1/10,1/10,1/10,7/20,7/20) allow three reached types of mass 3/10<1/2 although the uniform n=5 rank would be two. This falsifies the forbidden rank-normalization step, not the original conjecture. Arbitrarily large overlapping higher-rank families and the general asymmetric wedge remain unsupported. Original disposition remains unsolved, 5/5 turns; no sixth author search or novelty certification.
