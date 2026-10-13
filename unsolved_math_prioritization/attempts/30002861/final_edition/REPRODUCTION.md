# Exact reproduction of the final mathematical checkpoint

All fractions are exact. Vertex indices are zero-based unless a preceding certificate explicitly uses named vertices. The new certificates contain authored mathematical data. No particular program is needed to interpret them. Finite checks corroborate the general proofs and their independent acceptances; they do not prove an all-disk theorem by sampling.

## Inherited conventions and cubic attribution

The preceding [fourth-edition guide](fourth_edition/REPRODUCTION.md) fixes the coordinates, face order, determinants, fan starts, actual reduced rows and maximal minors of the eight-, twelve- and fifteen-vertex controls. Its [third-edition guide](fourth_edition/third_edition/REPRODUCTION.md) and [second-edition guide](fourth_edition/third_edition/second_edition/REPRODUCTION.md) fix their own conventions. Each certificate must be read with its own fan start and nonzero row scaling; rank equivalence does not make all displayed entries identical.

For Qiu's cubic example, obtain the coordinates and triangles from [arXiv:2609.06364v1](https://arxiv.org/abs/2609.06364v1), Table 1 and equations (7)–(8). The preserved [cubic proof](fourth_edition/third_edition/second_edition/first_edition/CUBIC_PROOF.md) reconstructs the full spline space and evaluation obstruction. This checkpoint does not redistribute that source dataset or its paper.

## Candidate and exact old-weight matrix

The [additive certificate](ADDITIVE_OBSTRUCTION_CERTIFICATE.json) refers to seed_extension in the [fourth-pass certificate](fourth_edition/FOURTH_PASS_CERTIFICATES.json). Start with seed.coordinates and seed.weights. Append the three entries of nonpencil_step.additional_vertices in index order. Concatenate seed.faces, reflex_ear_step.additional_faces and nonpencil_step.additional_faces, in that order. This gives precisely fifteen vertices, twenty-one positively oriented triangles and thirty-five edges.

Put V_v=(P_vx,P_vy,1)^T and U_v=x_v V_v. Process the oriented faces in displayed order. For each face, record the opposite vertex at each unordered edge. Store each edge increasingly and sort the distinct edge list lexicographically. The twenty-eight edges occurring twice are the interior edges. Their opposite order (u,z) is first encounter, second encounter. Define

    a_e=det(V_v,V_u,V_z), b_e=det(V_w,V_u,V_z), e=(v,w), v<w.

A three-column determinant uses the vectors as columns. The certificate's endpoint_determinant_pairs must agree exactly. Reversing both opposite vertices negates both coefficients and leaves the equation unchanged, but not its printed pair.

Construct M with one row per listed interior edge and columns 0 through 14. Put a_e in column v, b_e in column w and zero in every other column. Check a_e and b_e are nonzero, a_e x_v+b_e x_w=0, and det(U_v+U_w,U_u,U_z)=0. The latter equation includes the nonzero opposite weights and is not merely asserted from a floating-point residual.

For the fourteen listed tree edges, multiply column i by x_i and divide row (v,w) by its displayed nonzero a_e x_v. Each row becomes the oriented incidence row +1 at v and -1 at w. Delete column 0. The normalized determinant is -1. These rows prove rank(M)>=14; Mx=0 with nonzero x proves rank(M)<=14. Any other full-support solution has equal ratios y_v/x_v along the tree and hence is one common nonzero scalar multiple of x. This includes negative scaling.

The independent_audit_certificates record additionally supplies the original unscaled fourteen-column minor, its normalized matrix and the kernel normalized to coordinate 14. The scaling identity is

    original_minor * product_(i=1,...,14)(x_i)
       / product_(tree edges e)(a_e x_first(e)) = -1.

This reproduces the potentially large rational original determinant by a short incidence certificate.

## Whole-cone separation

For each attachment_obstructions record, use v=reflex_vertex, a=previous_boundary_vertex, c=next_boundary_vertex and b=old_opposite_vertex. Verify that (v,a) and (v,c) are actual one-face boundary edges, each with old opposite b. Compute

    (U_v+U_a) cross U_b, (U_v+U_c) cross U_b.

Both are nonzero line coefficient vectors and are proportional. Clear denominators in either vector, divide by the greatest common divisor of its integer entries, and choose the sign so the first nonzero coefficient is positive. This gives primitive_forced_line=(l_1,l_2,l_3), representing L(X,Y)=l_1 X+l_2 Y+l_3.

Recompute every line_values entry. The three cone_polynomial_coefficients are exactly

    L(P_v), L(P_a)-L(P_v), L(P_c)-L(P_v).

At 12 all three are strictly negative, and at 14 all three are strictly positive. Therefore L is strictly of that sign for every point P_v+alpha(P_a-P_v)+beta(P_c-P_v), with alpha,beta>=0 and no bound on their sum. Verify each displayed reflex turn by det(P_v-P_a,P_c-P_v)<0. The local lemma in the [proof](FIFTH_PASS_ADDITIVE_OBSTRUCTION.md) establishes that every conforming new opposite must lie in this whole missing cone. The affine strict-sign identity excludes every position, including bounding rays and simultaneous additions.

The independent records also give P_1's coordinates in each cone basis. Solve

    P_1-P_v=alpha(P_a-P_v)+beta(P_c-P_v).

Both coordinates are negative in each case. P_1 satisfies the algebraic line equation but is geometrically illegal. This is an exact control against ignoring the retained star.

## Actual reduced rank and independent corner elimination

The old-weight matrix M has shape 28 by 15. It is not the actual quartic matrix R, whose eight rows belong only to interior vertices 0,1,6,7,8,9,10,11 of this uncompleted disk. R has thirty-five edge columns and rank eight.

The fourth certificate fixes its fans at the smallest neighbor index. The independent audit instead uses the least polar angle in [0,2pi), measured from the positive x-axis. Each local_corner_elimination record gives that audit's counterclockwise polar_fan. With d_i=P_wi-P_v and a_i=det(d_i,d_(i+1))>0, compute

    beta_i=det(d_(i-1),d_(i+1))/a_(i-1),
    gamma_i=-a_i/a_(i-1).

The corner matrix has row t_i-gamma_i t_(i-1); it has rank n-1. Its supplied nonzero left-null vector lambda satisfies C^T lambda=0. Eliminating the corners gives edge coefficients lambda_i beta_i. The record's nonzero row_scale relates them to

    r_i=(-1)^i det(d_(i-1),d_(i+1))/(a_(i-1) a_i).

These audit rows differ from the fourth-certificate rows by factors (1,1,-1,1,-1,-1,1,1), in the stated vertex order. This sign change is recorded rather than silently mixed between certificates.

For the eight columns in rank8_minor.column_edges, divide each selected row by its listed nonzero raw diagonal. The normalized matrix is upper triangular with unit diagonal; its determinant is one. The only nonzero off-diagonal entries are in the first row and are printed exactly. Thus the candidate's actual reduced matrix has full row rank, and arbitrary quartic vertex jets are attainable on this nonconvex disk. Weight-rigidity rank fourteen and reduced rank eight refer to different matrices and different unknowns.

## Canonical collars and three finite polygon controls

The [boundary certificate](BOUNDARY_COMPLETION_CERTIFICATE.json) starts from the exact strictly convex pentagon

    (0,0),(4,0),(5,3),(2,5),(-1,3).

For strict corners A_i listed counterclockwise, e_i=A_(i+1)-A_i, compute

    D_i=det(e_(i-1),e_(i+1)),
    t_i=det(e_i,e_(i+1))/D_i,
    s_i=det(e_(i-1),e_i)/D_i,
    Q_i=A_i+t_i e_(i-1)=A_(i+1)-s_i e_(i+1).

Check D_i,t_i,s_i are positive. With H_j(X)=det(e_j,X-A_j), Q_i must have H_i<0, H_(i-1)=H_(i+1)=0 and H_j>0 for every other j. Check all Q_i are distinct.

For each side i, insert the subdivision parameters in increasing order, interpreting t as A_i+t(A_(i+1)-A_i). Store the original five strict corners first, then the new subdivision vertices in increasing side order and displayed parameter order. Append the arithmetic mean of the five strict corners as a center. Append Q_0 through Q_4 last. The unsubdivided example inserts none. The subdivided example inserts the exact parameters stored in the certificate, including 1/1001 and 1000/1001 on one side.

For the uneven affine example, first apply the certificate's determinant-one affine map to the five strict corners. Its matrix is ((1000000,999999),(0,1/1000000)) and translation (7,-3). Then insert the listed subdivisions and center as above. This exact affine distortion tests unequal scales and near-parallel directions without numerical tolerances.

For every successive pair (a,b) of a side chain, add the two counterclockwise triangles (a,b,center) and (a,Q_i,b). At each strict corner add (i,Q_(i-1),Q_i). The resulting counts are (V,E,F)=(11,25,15), (16,40,25) and (13,31,19). All original polygon vertices are interior in each completed mesh; the boundary is exactly the Q cycle. These generic fan examples test collar geometry and are not asserted to have the required closed-support degrees or balanced weights.

## Geometry tests sufficient for conformity

Check distinct vertices, positive triangle areas, edge multiplicities, connected face-dual graph, one boundary cycle, each interior link a cycle and each boundary link a path, and V-E+F=1. The [fourth-edition guide](fourth_edition/REPRODUCTION.md#exact-embedded-disk-checks) gives a complete exact common-simplex intersection test, including zero-area contacts. Every triangle pair must meet in exactly its shared indexed simplex. There are 105, 300 and 171 pairs in the three polygon examples, and 378 in the integer control below, for 954 pairs.

The all-polygon collar theorem rests on the supporting-half-plane proof, not these finite controls. The resulting outside polygon need not be assumed convex. The proof establishes its simplicity and the conforming collar incidences.

## Integer closed but unbalanced control

Use the vertices and triangles from the preserved [second-pass certificate](fourth_edition/third_edition/second_edition/SECOND_PASS_CERTIFICATE.json), without changing their order. Strict support corners are 0 through 5, inner support vertices 6 through 11, and exterior collar vertices 12 through 17. Reconstructing Q_i from corners 0 through 5 reproduces vertices 12 through 17 exactly.

Reconstruct complete counterclockwise fans at vertices 0 through 11, starting at their smallest-index neighbor. With the row formula above, every edge toward an exterior Q has zero coefficient and every edge inside the twelve-vertex support has nonzero endpoint coefficients. Its actual reduced matrix R is 12 by 45 with rank twelve. Its complete support-edge magnitude matrix M, constructed using the two actual collared opposite vertices of every support edge, is 27 by 12 with rank twelve. Therefore no nonzero full-support balanced weighting exists.

For each listed support boundary edge (v,w), compute the transfer tau=-a_e/b_e. The exact boundary_transfers records use the increasing endpoint order printed in the certificate; edge (0,5) is opposite to the counterclockwise boundary traversal. These individual ratios are not substituted for a single product condition. The old sign-balanced support remains magnitude-unbalanced; collar geometry alone does not create a quartic counterexample.

## Boundary forms and transfer identity

The [boundary proof](FIFTH_PASS_BOUNDARY_COMPLETION.md) obtains the local common polynomial from actual exterior triangles where the compact quadratic is zero. In local affine coordinates, strict exterior rays (-r,0),(0,-h) give p=xXY. A straight exterior triangle with Q=(k,-h) and its other side vertex (r,0) gives p=-xY(hX+kY)/h. Here r,h,x are nonzero. These factorizations show the exact two zero lines. The strict form is nonzero at (1,1), while the straight form vanishes on the forced line hX+kY=0. This uses the corrected incident-edge segment identity, never an unsupported whole-line claim about a piecewise function.

For an edge v=(0,0), w=(L,0), with opposite vertices u=(P,H), z=(R,-J), let L,H,J be positive. The opposite-line intersection with the edge's supporting line has coordinate (PJ+HR)/(H+J). With a=-(PJ+HR), b=L(H+J)-PJ-HR and tau=-a/b, the balanced weighted affine expression L tau/(1+tau) equals that coordinate whenever the endpoint coefficients are nonzero. The proof establishes that 1+tau is nonzero in an actual balanced active edge. A subdivided-side transfer need not be positive; the crossing lies in the whole strict side, not necessarily in the particular subedge.

## Evidence limits

Useful genuine certificate changes to reject include a moved Q, unordered subdivisions, a wrong census, false control rank, an altered boundary transfer, a changed old candidate weight, a wrong tree factor or minor, a false cone coefficient, a false reflex turn, and an alleged rank defect in the full-rank candidate. No finite check proves all possible supports are impossible. The final exact existence question remains the one stated in the [reader guide](README.md).

## Independent collar certificate: normalization and broader samples

The separate [independent collar certificate](INDEPENDENT_COLLAR_CERTIFICATE.json) supplies all four polygon inputs and exact subdivision parameters, including a rational-circle pentagon, rational octagon and determinant-one affine map with coefficients of order one billion. Construct vertices as above: original strict corners, subdivision vertices ordered by side and parameter, center, then Q vertices. For each strict side, list all old center-fan triangles first, then all exterior subedge triangles, then its corner triangle. Its recorded boundary cycle can start at a different Q; cyclic rotation does not alter the oriented boundary.

These four examples have 15, 23, 23 and 32 faces, giving 1,107 triangle-pair checks. The independent integer control adds 378 for a total of 1,485. Its actual support coordinates are the existing second-pass certificate. For this control's face signs, list the twelve core annular triangles first, then the four central triangles, then for each i the two collar triangles (i,12+i,i+1) and (i,12+i-1,12+i), with cyclic indices reduced before the offset 12. Give the first triangle sign +1 and reverse signs across every interior edge. This uniquely fixes every sign because the full dual is connected and bipartite.

Use the least-polar-angle counterclockwise fan at each vertex. At ray vw_i use the sign of triangle (v,w_i,w_(i+1)) in place of (-1)^i in the row formula. The resulting face_sign_normalized_rows can differ by a nonzero vertexwise sign from the earlier smallest-index rows. They are not substituted without that normalization.

For each increasingly oriented support edge v to w, take u to its left and z to its right. Set A=det(w-v,u-v)>0 and B=-det(w-v,z-v)>0. If s is the left-face sign, the common column factor is -s/(AB). Multiply the row of M, with coefficients det(u-v,z-v) and det(u-w,z-w), by that factor to recover the corresponding column of the actual normalized R. All twenty-seven factors are printed. The selected twelve row edges give the nonzero determinant -6624693947958945585230391966837094249267200/402018373. The actual boundary transfer product is 585991946946275/301150964543077, which is not one.

For the six actual exterior polynomial factorizations, use x_v=1, the same face signs and global variables X,Y. For every actual exterior triangle (v,a,b), compute -s det(a-v,(X,Y)-v) det(b-v,(X,Y)-v)/det(a-v,b-v). At each strict vertex all three exterior triangles yield the identical printed polynomial. This is local exterior algebra on a magnitude-unbalanced control, not a claimed global compact quadratic on it. The independent generic strict/straight forms have the opposite sign from the author's illustrative local forms because the face signs differ; their zero lines and Hessian determinants agree.
