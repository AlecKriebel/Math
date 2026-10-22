# Turn 3: fixed edge fractions fail even with freely chosen interior metrics

Problem 30002820. Third substantive author turn. **Original unresolved, 3/5.** This removes the induced-metric restriction from one important combinatorial class. It does not rule out metric-dependent edge fractions or other refinement topologies.

## 1. Precise class and theorem

Consider the triangular disk with old vertices 1,2,3 and arbitrary nondegenerate Euclidean edge lengths l_12,l_23,l_31. Fix the 1-to-4 refinement topology, with one inserted vertex m_ij on each old edge and the three midpoint-to-midpoint edges forming a central triangle. The inserted vertices need not be geometric midpoints.

For each oriented old edge i<j fix a number theta_ij∈(0,1), independent of the input metric. Require only that the refined edge lengths on its boundary path be

    l′_(i,m_ij)=theta_ij l_ij,
    l′_(m_ij,j)=(1−theta_ij)l_ij.                            (1)

The three inner edge lengths may be arbitrary positive functions of **all** input lengths. They need not be induced by points in the old Euclidean triangle; no locality, continuity, symmetry or homogeneity is assumed. Require, however, that the four new faces are genuine nondegenerate Euclidean triangles.

**Theorem.** No scheme in this class preserves discrete conformal equivalence for all nondegenerate input triangles.

Thus allowing arbitrary metric-dependent inner edge lengths does not repair a fixed-fraction 1-to-4 rule. Even the triangle inequalities for its central face eventually fail under the lengths forced by conformal preservation.

## 2. Conformal preservation forces the interior lengths

Fix the equilateral input l_12=l_23=l_31=1. Let k_i>0 be the scheme's inner edge length joining m_ij to m_ik, for {i,j,k}={1,2,3}. If the reference output is not a valid metric, the scheme has already failed, so assume it is valid.

Every other nondegenerate input triangle is discretely conformally equivalent to the reference triangle. Consequently preservation would supply positive output vertex multipliers b_v such that l′_vw=b_v b_w l′⁰_vw, where l′⁰ is the reference output.

Because the fixed fraction theta_ij cancels in each of the two ratios in (1), the boundary edges imply

    b_i b_(m_ij)=l_ij=b_j b_(m_ij).

Every b_(m_ij) is positive, so b_1=b_2=b_3=c>0. Hence

    b_(m_ij)=l_ij/c,
    l′_(m_ij,m_ik)=k_i l_ij l_ik/c².                       (2)

This conclusion is independent of the chosen fractions and of all regularity properties of the scheme. In particular the central triangle's side ratios are forced by the three products of old side lengths, up to the fixed reference constants k_i.

## 3. A valid skinny triangle makes the central face impossible

Choose the input

    l_12=epsilon,       l_23=l_31=1,

where 0<epsilon<2, so the input satisfies all strict triangle inequalities. Formula (2) forces the central triangle sides, up to the common positive factor 1/c², to be

    k_1 epsilon,       k_2 epsilon,       k_3.

Its strict triangle inequality would require

    k_3 < (k_1+k_2)epsilon.                                 (3)

Choose epsilon=min(1,k_3/[2(k_1+k_2)]). It is positive and at most 1, hence the original triangle is nondegenerate, while the right side of (3) is at most k_3/2. This contradicts (3). The free common multiplier c cannot fix the failure, because it scales all three central sides together.

This proves the universal nonexistence statement for the stated class. No limit argument or numerical degeneracy is needed: epsilon is an explicit strictly positive number determined by the reference output.

For the ordinary midpoint reference output k_1=k_2=k_3=1/2, epsilon=1/4 suffices. Any conformally equivalent refined assignment obeying the fixed boundary fractions would have central sides proportional to(1/8,1/8,1/2), which cannot form a triangle. The original side lengths(1/4,1,1) are entirely valid.

## 4. Why this is a new scope relative to earlier turns

Turn 1 fixes all refined lengths to the induced midpoint geometry. Turn 2 fixes all barycentric positions and uses induced Euclidean lengths. The theorem here allows arbitrary new interior metric functions and does not require an isometric realization inside the old face. Its remaining restrictions are the 1-to-4 topology and fixed input-independent boundary split fractions. It therefore supplies an obstruction outside the induced-metric setting of the earlier results.

The result does not cover a scheme whose split fraction changes with the input lengths, more inserted vertices, a different interior triangulation, metric surgery or changes to old edge lengths. It also does not turn the broad source wording into a global no-scheme theorem. It identifies precisely why edge-interpolatory fixed fractions and universal conformal preservation are incompatible in this topology.

The positive vertex-multiplier definition is the source's exp((u_i+u_j)/2) condition with b_i=exp(u_i/2). The fact that every original triangle is in one conformal class is credited to the elementary calculation in Bobenko–Pinkall–Springborn, Section 2.2, https://arxiv.org/abs/1005.2698 . Exact problem: Bauer, OWR 13/2015 printed 721–722, https://ems.press/content/serial-article-files/46561 . No novelty claim is made.

The checker uses rational fractions, valid reference refined metrics, the explicit epsilon choice, and exact vertex-multiplier equations. It checks the central failure rather than mistaking positive edge assignments for valid discrete metrics. The proof above covers arbitrary positive real reference constants and every fixed fraction in (0,1).

Subjective completion estimate toward the unrestricted intended question: 15%. Author turns completed: 3/5. The next turn investigates genuinely metric-dependent edge placements.
