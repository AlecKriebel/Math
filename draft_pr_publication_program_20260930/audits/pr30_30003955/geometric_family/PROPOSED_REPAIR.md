# Required local repair to the frozen large-genus argument

This is an audit-proposed replacement for the killed-curve paragraph of PARTIAL §4, not an edit to the original artifact. It preserves the stated sufficient bound. The original same-tree quotient claim and old reviews must not be represented as verified merely because this replacement works.

Write m=|G| and fix either genus-m one-boundary block U. We use a planar subsurface N with m+1 boundary circles c_1,...,c_m,delta whose first m boundary classes are independent in H_1(U;Z). One explicit model constructs U by gluing every boundary circle of N, a sphere with m+1 holes, to the corresponding boundary of a sphere Q with m+2 holes, using orientation-reversing identifications and leaving the extra boundary of Q unglued. The glued surface is connected, has one boundary and Euler characteristic (1-m)-m=1-2m, hence is the genus-m block. Cutting the first m seam circles leaves N and Q joined only along delta, a connected sphere with 2m+1 boundary components; thus these seams form a standard cut system. For each i, an arc from c_i to delta in N joined to such an arc in Q gives a closed dual crossing c_i once and every other c_j zero times. Consequently [c_1],...,[c_m] are independent. This model may be embedded in the already chosen U by a homeomorphism.

Choose standard coherent based peripheral loops s_1,...,s_m in N, in boundary order, using an embedded comb of paths from a common base point. In the usual disk-with-holes model, the boundary of a disk enclosing precisely the consecutive holes i+1,...,j represents s_{i+1}...s_j up to common conjugation and inversion. This follows by tracing its boundary after cutting along the comb; each enclosed hole is traversed once in the same peripheral orientation. Singleton intervals give a parallel copy of c_i and the full interval gives a parallel copy of delta. These boundary circles are embedded for every nonempty interval.

Let p_0=1 and p_j=rho(s_1...s_j), for 1<=j<=m. There are m+1 prefix images in a group with m elements, so p_i=p_j for some 0<=i<j<=m. Then

\[
\rho(s_{i+1}\cdots s_j)=p_i^{-1}p_j=1.
\]

The corresponding simple interval-boundary curve alpha is killed by rho. Its homology is the sum of the nonempty interval of independent boundary classes, up to an overall sign, and is nonzero. A separating simple curve in a one-boundary oriented surface has zero homology, so alpha is nonseparating in U. The path from this block to the global base point conjugates all prefix images by the same element and does not change either equality or triviality.

Apply this construction independently in U_1 and U_2 to obtain disjoint killed nonseparating alpha and beta. The existing dual-curve, one-holed-torus, connecting-band, five-holed-sphere and essential-four-boundary construction can then continue. At m=2 and g=4 the two blocks still exist with annular exterior, the prefix argument still has three images in a group of order two, and the subsequent genus-two subsurface has a genus-two exterior. No larger genus bound, added discovery claim or additional source-question scope is required.
