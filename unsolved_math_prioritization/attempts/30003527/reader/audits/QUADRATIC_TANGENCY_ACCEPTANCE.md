# Independent acceptance of the quadratic-tangency supplement

13 October 2026. Problem 30003527 / queue row 1767, shared substantive pass 4 of 5. This is a supporting audit, not another substantive attempt. It is separate from the frozen flat-wall acceptance.

## Verdict and limits

**Accepted.** The parabolic-wall replacement gives a compact movable stationary C' with nonmovable M_1(C'), no Clarke distance-critical values in [3/5,infinity), and only strict quadratic internal contacts of the bad book's invariant trajectories with the smooth unit boundary. All radii 0<r<1 are still good, for a different reason than in the flat-wall construction: the curved wall's own gaps can fill, and their selected union remains movable.

Audited supplement: QUADRATIC_TANGENCY_SUPPLEMENT.md, 5,619 bytes, SHA-256:

c7b0fbe3434e87d7e694e1a3757b249c3f31b81b1b6a40d40cb058b368f7d395

The exact main construction, its accepted stretched-book input, and the regularity and level-surface implications are audited separately in REGULAR_RADIUS_ACCEPTANCE.md. The present supplement does not establish either the existential good-radius assertion or the full invariant movable-enlargement statement. It does not challenge genuine isolating-block hypotheses.

## 1. Wall hull and exact bad core

Put delta=1/100. The wall W_delta is the graph y=delta z^2 over the rectangle -1<=x<=1, -2<=z<=2. It is ambiently flattened by (x,y,z)->(x,y-delta z^2,z), so it is movable. It is disjoint from both movable endpoint sheets: its y-range is [0,1/25], while the sheets have y>=9/10. Their finite disjoint union C' is movable.

The wall projection is [-1,1] x [0,4delta]. At an interior projection height y>0 its two fiber points are z=+/-sqrt(y/delta). The full vertical hull is exactly

H_delta={-1<=x<=1, delta z^2<=y<=4delta}.

The displayed inequalities already imply |z|<=2. This hull is convex because it is the intersection of a convex epigraph with three halfspaces. Its distance to the wall is bounded above by y-delta z^2<=4delta, using the same-height point. It is therefore fully selected at radius 1. The sheet and wall projections are disjoint, so there are no mixed bounded gaps.

At a sheet-overlap midpoint (x,y,0), where 1<=y<=11/10, minimizing squared distance to the wall reduces to

y^2+(1-2delta y)s^2+delta^2 s^4, -2<=s<=2.

The coefficient 1-2delta y is at least 489/500>0. Hence the unique minimizing vertical coordinate is s=0, and matching x is allowed. The wall distance is exactly y. Each sheet distance is exactly 2, since the base lies in both sheets. Thus the midpoint distance to C' is y, and every sheet gap with y>1 is excluded at radius 1.

For y=1, the same-height wall comparison bounds every gap point's distance by 1-delta z^2<=1; the quantity remains nonnegative throughout |z|<=2. Exactly the binding gaps are selected. Consequently M_1(C')=H_delta disjoint union D. The separation in y makes D clopen. It is the same nonmovable affine image of the accepted stretched book, so the core is nonmovable.

## 2. Correct small-radius statement despite the new wall gaps

For every 0<r<1, all sheet gaps remain absent by the preceding midpoint lower bound. The wall gaps require a separate argument and cannot be ignored.

At a fixed wall base (x,y), 0<=y<=4delta, the midpoint distance to the wall is exactly y by the same polynomial calculation, now with 1-2delta y>0. Its distance to either endpoint sheet is at least 2 because its height is zero. Hence the midpoint distance to all of C' is y. Every other point of this gap has distance at most y to the same-height wall point. The maximum distance along the gap is therefore exactly y, irrespective of possible sheet comparisons elsewhere along the gap.

Thus the selected wall component is exactly

E_r=W_delta union {points of H_delta with y<=r},

and M_r(C')=C_- union C_+ union E_r. At y=0 there is only one wall fiber point, already included in W_delta; no degenerate gap is being added incorrectly.

The homotopy (x,y,z)->(x,(1-t)y+t delta z^2,z) fixes W_delta. For a point of the cap portion of E_r its new y-coordinate remains between delta z^2 and its original y<=r, so it stays in that portion. For a wall point above r it is constant. This is a continuous strong deformation retraction of all E_r onto W_delta. Homotopy equivalence implies shape equivalence, and movability is shape invariant. Hence E_r is movable. Its positive separation from the endpoint sheets proves movability of the entire M_r(C').

In general M_r(C') is larger than C' because wall gaps fill. The supplement correctly claims movability, rather than inheriting the flat-wall equality M_r(C)=C.

## 3. Clarke-critical exclusion including wall edges

Assume a=(x,y,z) lies in the convex hull of its nearest points and rho=d(a,C')>=3/5. Convex-hull containment gives -1<=x<=1, 0<=y<=11/10 and -2<=z<=2. Thus the same-height comparison wall point is available even at parameter endpoints, and

rho<=|y-delta z^2|.

If y<delta z^2, the right side is at most 4delta=1/25<3/5. Consequently the positive alternative is forced, and y>=rho+delta z^2>=3/5. Also rho<=11/10. The sheet separation of 4 again prevents both sheets from contributing nearest points. Any convex representation of a must give positive total weight to a sheet, since every wall point has y<=1/25.

Suppose the participating sheet has height 2. Its nearest-point status implies z>=2-rho>=9/10>0. Since x is inside [-1,1], every nearest wall point matches x exactly. Its vertical parameter minimizes

f(s)=(y-delta s^2)^2+(z-s)^2, -2<=s<=2.

For s<0, reflection to -s strictly reduces the second term and leaves the first unchanged, so a negative minimizer is impossible. For 0<=s<z,

f'(s)=2(s-z)-4delta s(y-delta s^2)<0,

using y-delta s^2>=3/5-1/25>0. Every nearest wall parameter therefore satisfies s>=z, including the cases where the minimum is attained at s=2. All wall nearest points have height at least z and every participating sheet point has height 2. Their convex combination, with positive sheet weight, can have height z only if z=2. This conclusion is also immediate if there is no wall weight. Reflection proves z=-2 for the lower-sheet case.

The x-coordinate equation forces x in [0,1/10], since all wall nearest points have coordinate x and the total sheet weight is positive. Choose any point c on the participating sheet. Then |x-c_x|<=1/10, |y-c_y|<=1/2, and z=c_z, giving rho<=sqrt(26)/10<3/5. This is the required contradiction.

No assumed uniqueness of the nearest wall point is needed for this exclusion. The main audit's strict-separation proof now implies absence of Clarke critical values throughout [3/5,infinity). The same primary regular-level theorem applies unchanged.

## 4. Smoothness and strict quadratic internal tangency

Fix (x,1) in the binding and a=(x,1,0). The nearest point is uniquely (x,0,0), by the strictly positive polynomial coefficient in Section 1. The sheets have a strict distance margin of 1. At wall parameter zero, the second derivative of the squared-distance objective in s is 2-4delta>0. A compactness gap away from s=0 and the implicit function theorem preserve a unique interior minimizing parameter smoothly in a neighborhood of a. The x-coordinate is strictly inside the wall's x-range, even when x is an endpoint of the binding's smaller interval. No wall-edge singularity occurs. Since the distance stays positive, distance itself is smooth there.

The displayed unit-normal offset of the parabola is correct:

y(s)=delta s^2+(1+4delta^2 s^2)^(-1/2),

z(s)=s-2delta s(1+4delta^2 s^2)^(-1/2).

It is locally the unit distance surface by the unique nearest-point calculation. Its expansions are

y(s)=1+delta(1-2delta)s^2+O(s^4),

z(s)=(1-2delta)s+O(s^3).

Since 1-2delta=49/50>0, inversion gives the claimed graph

y=h(z)=1+[delta/(1-2delta)]z^2+O(z^4).

The quadratic coefficient is 1/98>0. The vertical orbit has fixed y=1 and nonzero vertical speed; a smooth change to the time parameter preserves a nonzero quadratic contact. For every sufficiently small nonzero z, indeed for every 0<|z|<=2 along the closed binding segment, the same-height wall bound is 1-delta z^2<1. Both sides of the contact are inside N_1(C'). This is an internal quadratic tangency, not an entry/exit point.

All of H_delta lies strictly inside N_1(C'), and all endpoint sheets have distance zero. On each binding column only its midpoint can have distance 1, by the preceding strict bound. Therefore

M_1(C') intersect boundary(N_1(C'))=T x {0}.

The invariant-boundary contact contains no nonstationary orbit segment. In particular the unit neighborhood is still not isolating.

## 5. Clarification of the stronger no-boundary-segment phrasing

The preceding local and invariant-core statement suffices for the described bad contacts. The stronger claim that no nontrivial orbit segment anywhere can be contained in the unit boundary is also valid here, by the following additional argument.

Fix any horizontal base (x,y). Each sheet's squared distance as a function of z is b_+^2+(z-2)^2 or b_-^2+(z+2)^2, with b_+,b_- fixed distances to the planar bases. Each equals 1 at at most two heights. If d(.,C') were identically 1 on a nontrivial vertical interval, removing those finitely many heights would leave a subinterval on which the wall distance is identically 1.

Write a_x=dist(x,[-1,1]). The wall's squared distance is a_x^2+min_{|s|<=2} f(s), with f as in Section 3. Wall distance 1 somewhere implies -1<=y<=1+4delta. In this range

f''(s)=2-4delta y+12delta^2 s^2>0

throughout [-2,2]. The minimizing parameter s(z) is therefore unique and continuous. The elementary minimum-envelope derivative gives the derivative of squared wall distance in z as 2(z-s(z)), including a constrained endpoint minimizer because the minimizer is unique. A constant distance on an interval would force s(z)=z throughout it. For an interior z in (-2,2), the first-order minimizer equation would then force z(y-delta z^2)=0. With y fixed, that equation has only finitely many solutions. At endpoint parameters or outside [-2,2], the equation s(z)=z likewise cannot hold on an interval. This contradiction excludes every nontrivial vertical boundary segment.

Nonstationary orbit images are vertical intervals by the accepted full-flow classification. Thus excluding boundary orbit segments globally, or asking only for nondegenerate quadratic internal contacts, does not repair the movable-core proposal. The entrance/exit conditions of a genuine isolating block remain materially stronger and are not contradicted.

## Verification record

The frozen main artifact was not changed. The supplement was read in full and hash-checked before and after this audit. The separate flat-wall acceptance is preserved. No additional literature search or source-body publication was needed, and no remote mutation or external communication was performed. The accompanying verification manifest records exact identities and read-only source inspection. All claims remain within shared substantive pass 4.
