# Independent deduction, not an identified prior publication

This records why no new general method should be claimed. It does not assert that an earlier author made this application. The parent-supplied fractional construction remains the shortest proof; the alternative here deliberately tests whether classical geometry subsumes its exact missing bridge.

Write q=1−d and m=sum q, an integer. For a chosen subset J put a=sum_J q. Every projection Q with diagonal q has rank Q[J]≥ceil(a), since its compression is a positive contraction with trace a. The claimed construction attains this bound **for that chosen J**, not simultaneously for every subset. One counterexample projection suffices to invalidate the universal paving property.

Here is an independent moment-polytope derivation. Set k=ceil(a). Trivial empty/full subsets and k=0 are handled by direct sums; k=m makes the constraint below vacuous. Otherwise 0<k<m, k≤|J|, and m−k≤|Jc|, because q coordinates lie in[0,1]. Choose generic real columns indexed by J inside a fixed k-plane in R^m, and generic real columns outside J in R^m. Their m-element bases are exactly B with |B∩J|≤k: dependence of larger intersections is forced, and every permitted determinant is a nonzero polynomial in the free real entries. Each permitted determinant can be nonzero for some choice of entries; the finite product is not the zero polynomial, so a simultaneous real choice exists. These bases exist under the displayed size bounds.

Their indicator convex hull is exactly

`C={x∈[0,1]^n: sum x=m, sum_J x≤k}`.

For completeness, this cut hypersimplex has only integral vertices. If the cut is inactive, two fractional coordinates permit a small preserving exchange, while exactly one fractional coordinate contradicts the integral total. If active, the sums on J and Jc are both integral; any fractional coordinate in either group entails at least two in that group and a preserving exchange. Thus a nonintegral point is not a vertex. Its integral vertices are exactly the permitted basis indicators.

By the old torus-orbit moment-polytope result, any q∈C is the diagonal of a projection associated with a point of this orbit closure, all of which retain rank on J at most k. There is no complex-to-real gap: starting from the real column configuration, complex diagonal scalings and their absolute-value positive real scalings have identical absolute Plücker weights, hence identical moment images. Compactness of the real Grassmannian supplies a real limit for any limiting moment point. Rank≤k is closed. The trace bound then gives rank Q[J]=k. This application uses the quotient-versus-row-space convention consistently: the m-row configuration represents the orthogonal projection onto that row space, whose diagonal is the same moment vector by the determinant formula.

Combining this lemma with the old matroid partition criterion for Q's columns gives the desired universal criterion. For a fixed Q, strict r-paving of P=I−Q is equivalent to partitioning the columns Qe_i into r independent sets, hence to |J|≤r rank Q[J] for every J. Necessity for all projections therefore uses exactly the attained lower bound. Sorting q increasingly reduces the smallest mass at each size to its prefix. Lengths rk+1 are precisely the places where ceil(prefix mass) must exceed k, giving the strict d inequalities. A common epsilon follows only by compactness of the fixed finite fiber.

This deduction is ours for audit purposes. The old general theorem's availability does not identify a prior publication of the full paving application, or establish a continuing open problem. The real Schur–Horn fractional coupling is a simpler elementary specialization of existing spectral machinery. Any eventual novelty claim should be restricted accordingly.

## New exact strict-violation control

Take r=2 and d=(17/20,4/5,7/10,7/20,3/10), total rank3. Its first-three sum is47/20>2. No entry is0 or1, and this is a strict violation, rather than the equality case of the old proposition.

Let u=(sqrt(3/20),sqrt(1/5),sqrt(3/10),7/sqrt(260),sqrt(42/260)) and w=(0,0,0,−sqrt(6/13),sqrt(7/13)). Their squared norms are1, and their inner product vanishes by cancellation of two terms with the same squared magnitude. Thus Q=uu^T+ww^T is a real rank2 projection with diagonal q=(3/20,1/5,3/10,13/20,7/10). Its first-three compression is the nonzero rank-one outer product u_Ju_J^T with trace13/20. Every two-partition has two of those three indices together, making that complementary Gram block singular. Therefore P=I−Q is not strictly2-pavable. The accompanying Fraction-only check verifies the stated rational identities and all32 labeled two-partitions; it is a control, not a replacement for the universal proof.
