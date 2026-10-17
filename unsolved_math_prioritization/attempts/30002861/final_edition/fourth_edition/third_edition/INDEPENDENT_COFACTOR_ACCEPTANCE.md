# Independent acceptance of the corrected cofactor normal form

## Decision and exact scope

**Accepted after the narrow mandatory correction incorporated in [COFACTOR_NORMAL_FORM.md](COFACTOR_NORMAL_FORM.md).** The local normal-form equivalence, Hessian and edge-gradient identities, nonsingular four-star derivative maximum, explicit compact quadratic, Hessian cancellation, and restricted macro-patch obstruction are correct. The uncorrected assertion about the piecewise function on an entire supporting line is false: the agreement is on incident edge segments, or on the full-line restrictions of the two adjacent polynomial pieces. The three-ray lemma must use the same segment formulation.

This audits one branch of the same shared third substantive pass for row 1761 / problem 30002861 / OWR-13678-002. It is not an additional counted pass.

This acceptance applies to the corrected mathematical text. The literal whole-line statements in the earlier wording are false and are not accepted; Section 1 gives explicit counterexamples.

The accepted second-pass theory and construction audits, linked in [DEPENDENCIES.md](DEPENDENCIES.md), supply the particular quartic row normalization, the necessity of the local cofactor span, and the exterior-attachment theorem. This audit independently verifies the new algebra, geometry and counterexamples. It does not construct an admissible balanced support, prove universal quartic interpolation, certify worldwide novelty, or infer literature openness.

## 1. The necessary correction

On triangle T_i the difference q_i-p_v is x_v s_i L_i L_(i+1)/a_i. Therefore it vanishes on the two incident edge segments of T_i. Both adjacent polynomial pieces restrict to p_v on the entire supporting line of their common segment, by polynomial continuation. However, the piecewise function on the opposite ray can use a different polynomial, which need not agree there.

The authored four-star already demonstrates the distinction. With its own notation and 0<t<1, the point (-t,0) lies inside T_1 since

    (-t,0) = (t/14)d_1 + (5t/14)d_2,

and the two positive coefficients sum to 3t/7<1. At that point,

    q(-t,0)-p_v(-t,0) = 5t²/14,

although (1,0)=d_0 is an incident edge direction. Thus the old sentence asserting agreement on every full ray line cannot be used literally.

There is also an exact counterexample to a whole-line interpretation of the old three-ray conclusion. Take p_v=0, x_v=1 and the cyclic even fan

    (1,0), (1,1), (0,1), (-1,1),
    (-1,0), (-1,-1), (0,-1), (2,-1),

with s_i=(-1)^i and q_i=s_i L_i L_(i+1)/a_i. All consecutive areas are positive. The entire portions of the lines x=0, y=0 and y=x inside this fan have zero q because each of their two rays is incident. Nevertheless, (-2t,t), for 0<t<1/2, lies in the sector between (-1,1) and (-1,0), where

    q(-2t,t)=t².

This point is on the supporting line of the incident direction (2,-1), so the full-line conclusion is false even with three actual full zero lines. Zero row entries are allowed by the stated lemma, as required for this example.

The correction replaces whole-line statements about q with statements about incident edge segments. It also makes explicit that a macro vertex must have an actual full even fan with the quartic proportionality imposed before the local lemma is applied. The examples, coefficients, identities and final restricted construction conclusion require no numerical change.

## 2. Exact local equivalence and its quantifiers

For three successive rays u=d_(i-1), v=d_i, w=d_(i+1), put A=det(u,v), B=det(v,w), C=det(u,w). The generic linear-form identity is

    L_w/B + L_u/A = C L_v/(AB).

Both sides vanish on v and agree on w; these are independent vectors because B>0. Alternation of the signs then gives

    s_i L_i L_(i+1)/a_i
      - s_(i-1) L_(i-1)L_i/a_(i-1)
      = rho_i L_i².

This computation uses only nonzero consecutive determinants, and no division by rho_i. It therefore retains all zero-entry cases. An even number of rays is essential for the alternating signs to close cyclically. An actual counterclockwise full fan is essential; positive determinants alone on an arbitrary indexed collection would not certify winding or the intended geometry.

If q has the stated jumps for one scalar x_v, subtraction of these explicit bubbles makes every adjacent polynomial difference zero. The cycle is connected, so the resulting polynomials are one polynomial p_v. Conversely, the proposed formula directly gives every jump, including the cyclic seam. Those jumps are divisible by squared edge equations, hence give C1 agreement across every edge. The bubbles have zero value and gradient at v. Thus p_v has exactly the jet of q at v.

Uniqueness is correctly conditional on a nonzero row: a nonzero rho_i forces the difference of two proposed x_v values to vanish, then p_v is fixed. When the entire row vanishes, uniqueness is not claimed. For example, on the axial four-star the four bubbles are all -xy and every rho_i is zero, so the bubble contribution can be absorbed into p_v.

At a boundary vertex of a prospective closed support the same proof needs the original full even fan. Its genuine exterior triangles have q=0. The report correctly prohibits closing the supported interval with an invented triangle. The local equivalence does not assert that an arbitrary compact quadratic supplies feasible missing exterior triangles or global balance.

## 3. Hessians and the derivative maximum

With n_i=Jd_i and J=[[0,-1],[1,0]], differentiating L_i L_(i+1)/a_i gives exactly

    S_i=(n_i n_(i+1)^T+n_(i+1)n_i^T)/a_i.

The independently recomputed identities are

    det S_i=-1,
    S_i d_i=-Jd_i,
    S_i d_(i+1)=Jd_(i+1),
    S_i+S_(i-1)=2 det(d_(i-1),d_(i+1)) n_i n_i^T/(a_(i-1)a_i).

The sign in the first edge action follows from n_(i+1) dot d_i=-a_i. Consequently

    D²q_i=B_v+x_v s_i S_i,
    g(v+d_i)-g(v)=(B_v-x_v s_i J)d_i.

These statements hold for arbitrary symmetric B_v; the determinant of S_i alone puts no sign condition on det(D²q_i).

For the rational four-star in the report, the exact polar order and consecutive positive areas (5,14,3,1) give a genuine full fan. All six pairwise line determinants are nonzero, so there are four distinct supporting lines. Its reconstructed row is

    (1/5, 1/70, -1/42, -1/3).

The four polynomials have the same zero jet at the center, and all adjacent jumps have precisely these coefficients. The computed values of partial_x q at the neighboring vertices are

    (-1/4, -3/32, -41/32, -1/32).

The derivative is continuous and affine on each triangle, zero at the center and negative at both other vertices. Barycentric interpolation makes it strictly negative everywhere in that triangle except at the center. Since the full fan contains a neighborhood of the center, this is a strict local maximum. Nonzero cofactors do not invalidate it. The asserted scope is appropriately local: no compact extension or admissible global support is supplied.

## 4. Compact patch geometry and full continuity

The six vertices and seven ordered triangles are exactly those printed in the report. The independent geometry test uses intersections of closed half planes, not the author's segment-intersection and contained-vertex algorithm. Every vertex of a bounded polygonal intersection comes from two independent active supporting lines. Enumerating those pairs and checking all half-plane inequalities therefore gives the complete exact intersection, including segment and point intersections.

All 21 triangle pairs have precisely their prescribed common simplex: three pairs are disjoint, nine meet only at a common vertex, and nine share their specified edge. Every triangle has positive area and lies in ABC. The seven areas sum to 25/2, the area of ABC. Together with the exact nonoverlap checks this proves coverage; a missing relative interior point would give an open missing set of positive area. Boundary coverage is also explicit from the three boundary edges.

There are 12 edges, of which exactly AB, AC and BC have one incident triangle. Every other edge has two. Each boundary vertex link is one path with degrees (1,1,2,2), and each interior link is one cycle with four degree-two vertices. Thus the object is a conforming embedded triangulated disk with the claimed boundary, rather than merely seven positively oriented triangles.

The independent calculation reconstructs every oriented cofactor from polynomial coefficients. With increasing endpoint indices and the actual geometric left and right pieces, it obtains

    3/25, -3/25, 1, -1, 3/25, -1, 1, 1, -1, -5, 5, -5

in the report's edge order. Each identity is exact as a polynomial, not a test at selected edge points. Every coefficient is nonzero. In particular the boundary differences are multiples of the squared boundary equations, with zero exterior polynomial. All first derivatives and values agree across the whole edge, and finite-piece continuity gives the common boundary-vertex jets as well. Extension by zero is genuinely globally C1.

At the three interior vertices the value is 3; at (5/3,5/3) it is 5. The support is genuinely the closed outer triangle: no interior triangle polynomial is identically zero, so each triangle interior lies in the closure of nonzero values.

## 5. Special interior proportionality and Hessian cancellation

Each of a,b,c has four distinct incident supporting lines. Three distinct squared line forms are independent: the quadratic evaluation determinant for three directions u,v,w is

    det(u,v) det(u,w) det(v,w).

Thus the local three-by-four moment matrix has rank three. Its cofactor kernel has dimension one, and the nonzero quartic row spans it. This justifies the report's abstract argument.

As a separate stronger check, the audit reconstructs the geometric fan orders, outgoing cofactor signs and a common normal-form polynomial at every interior vertex. In exact polar order, starting in the upper half plane, it finds

    a: neighbors (C,b,c,B), x_a=15/2,
    b: neighbors (a,C,A,c), x_b=15/2,
    c: neighbors (a,b,A,B), x_c=-15/2.

All four pieces at each vertex give the same p_v after subtracting x_v s_i L_i L_(i+1)/a_i. The signs of these x_v values depend on the chosen local fan starting point; they are not an additional global dependency claim.

The exact Hessian determinants are

    (0,-12,0,-12,0,-12,108).

The three negative faces have area 3/2 and the positive central face has area 1/2, giving

    3(3/2)(-12)+(1/2)(108)=0.

Thus cancellation is real, and a purported argument replacing the integral by a strictly signed sum would need further assumptions. The determinant-minus-one identity concerns the bubble matrices, not the complete Hessians.

The outer support cannot be a closed active quartic support under the accepted exterior-attachment theorem. Across AB, an exterior vertex would need the simultaneous representation

    A+t(A-C)=B+s(B-C),   t>0, s>0.

Exact solution gives t=s=-1 and the point C. Hence no required exterior triangle exists. The example also has only three strict corners, below the accepted lower bound of five. Neither compact support, nonzero jumps, nor the three correct interior proportionalities repairs that failure.

## 6. Corrected three-ray lemma and assembly implication

Assume the local normal form, q(v)=0 and gradient q(v)=0. On each incident edge segment q agrees with p_v, and p_v is homogeneous quadratic about v. If q is identically zero on three such nondegenerate segments with distinct supporting lines, then p_v vanishes on all three lines. The three-direction evaluation determinant above is nonzero, so all three homogeneous quadratic coefficients vanish. Therefore p_v=0 and q=0 on every incident edge segment. No conclusion about a nonincident opposite ray is needed or generally valid.

An invertible affine image of the compact patch retains zero value and gradient on its macro boundary. Independently multiplying each image by a scalar and gluing along a conforming macro triangulation therefore produces a C1 quadratic. At an old macro vertex the value and gradient are zero.

For a vertex where an actual full even fan exists and the quartic proportionality is required, three incident macro-edge segments with distinct supporting lines meet the corrected lemma's hypotheses. It follows that every incident micro-edge segment has zero q, including at its neighboring micro vertex. Each macro triangle contributes two such neighbors; both have value 3 times its patch amplitude. Consequently each incident patch amplitude is zero. The explicit full-even-fan condition prevents mistakenly imposing a quartic row at an odd-valence vertex or inventing exterior geometry at a macro boundary.

This proves the same restricted assembly obstruction intended in the report. It does not cover overlapping patches, nonzero boundary data, macro stars with only two supporting lines, or arbitrary box-spline constructions. It is not a universal nonexistence theorem.

## 7. Primary-source inspection and reproducibility

The author-hosted 16-page PDF by Yu Yu Feng, Jernej Kozak and Ming Zhang, *On the Dimension of the C1 Spline Space for the Morgan–Scott Triangulation from the Blossoming Approach*, was independently opened on 2026-10-13. The abstract and introduction on PDF pages 1–2 explicitly state the quadratic dimension criterion, distinguish dimensions seven and six, and describe the seven-triangle inner/outer configuration. The first page bears the 1996 publication notice. These observations support the narrowly stated historical attribution in the report.

Source: https://users.fmf.uni-lj.si/kozak/RaziskovalnoDelo/NekateriClanki/DIMS1N/fengetal.pdf

The three opposite inner-to-outer lines Aa, Bb and Cc in this example were independently checked to concur at (5/3,5/3). The source's dimension result is not used to infer compactness or quartic proportionality; those were checked directly. No source PDF, source text or dataset is reproduced here; no PDF hash is claimed.

The independent exact calculation uses generic symbolic identities, a separate half-plane intersection argument, exact polar fan ordering, direct reconstruction of cofactors and normal forms, and negative controls. The authored finite inputs and derived values are recorded in [THIRD_PASS_CERTIFICATES.json](THIRD_PASS_CERTIFICATES.json), with explicit [reproduction conventions](REPRODUCTION.md).

The proof of the all-fan equivalence, the global C1 conclusion, the corrected three-ray lemma, and the universal scope of the restricted assembly implication are mathematical arguments above. Passing finite examples is not substituted for those proofs.
