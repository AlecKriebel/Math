# The six-edge height-normalization countermodel is also virtually special

UTC checkpoint:2026-10-24T22:55:00Z. New affirmative result for this one test group, pending fresh independent audit; no complete21.124 or priority claim. Full-problem discovery estimate6%.

Use precisely positive_hierarchy/HEIGHT_NORM_COUNTERMODEL.md. Its checked maximal-tree presentation has two commuting vertex bases(a,T),(b,T), and five letters u_i with

    u_i^-1(a^p_i T)u_i=b^q_i T,

where(p_i,q_i)=(0,-2),(1,3),(1,-5),(6,10),(6,-12). Here the original stable-height generators are t=a^-7 T and s=b^-1 T. The earlier source audit gives CAT(0), free fiber F7, and impossibility of equal height Schur complements on the original two-vertex graph. Those facts are not contradicted by virtual specialness.

The exact certificate height_exact_multiset_certificate.json lists82 integer triples(a_j,b_j,t_j), each with a positive integer pair multiplicity. Include each triple and its negative that many times; this gives an indexed finite set Omega of size4370132. Let A,B,H be its three coordinate vectors. Exact full signed aggregation, independently of LP approximations, verifies

    {p_i A_j+H_j:j in Omega}={q_i B_j+H_j:j in Omega}

for all five pairs. Both A and B are nonzero. height_compressed_permutations.json explicitly matches equal values, specifying five literal finite permutations P_i by interval translations. The source and destination interval partitions cover all of Omega exactly. With P_i e_j=e_(P_i j) the identities are

    P_i(p_i A+H)=q_i B+H.

Let Q be the finite permutation group they generate. On Z^Omega directsum Z, let Q fix the last coordinate. Map

    a -> (A,0), b -> (B,0), T -> (H,1), u_i -> P_i^-1.

The inverse on u_i is essential: the displayed group relations have u_i^-1 on the left, so their images conjugate by P_i. Both vertex commutators vanish since these images are translations. Each edge relation is exactly one of the five vector identities, including the unchanged final coordinate. Thus the map is a homomorphism.

The pairs(A,0),(H,1) and(B,0),(H,1) are real linearly independent, so both vertices inject discretely. Changing back to t=T a^-7 and s=T b^-1 preserves this rank-two lattice statement. The image is integral and its finite linear part is Q. Merladet Urigüen–Minasyan2505.18054v3 Theorem1.6(ii), then Proposition1.10 (Appendix with Wu–Ye), prove that the group has(VRC) and is virtually special. Primary source: https://arxiv.org/html/2505.18054v3, freshly read24October2026.

The finite object was found through numerical positive-measure search, then rebuilt by exact rational elimination and checked with integer arithmetic. The positive certificate, its interval permutations and verify_height_positive_witness.py suffice for independent verification without numerical optimization or exact linear-algebra libraries. Numerical failures on smaller boxes are not exact nonexistence claims.

This is an affirmative test of a candidate originally introduced only to defeat a metric ansatz. It strengthens the evidence that that ansatz's failure is not a negative obstruction, but it supplies no general theorem for all CAT(0) free-by-cyclic groups. No paper, Zenodo record or tracker entry is justified by this partial research result alone.
