# Independent reconstruction sealed before historical comparison

Audit family: density / contact rank / area formula / boundary cases.

Frozen candidate commit supplied by parent: `99e403e85d38d92b021198c4a57bbad3cd8775ba`.

Inputs actually inspected before this document was sealed:

- workspace `AGENTS.md` and nested `unsolved_math_prioritization/AGENTS.md`;
- `source_snapshot/CANDIDATE.md`, SHA256 `b04aaf0b5a42d79ad26daf27880774a3f126858ef545b3f366a2b8b62e277252`;
- `source_snapshot/source_record.json`, SHA256 `b90fc595a14ea6522ec5d01bbb04fd3d0445362bc0a3257e2cc927f350f3afb5`;
- authored primary text, Leon Simon, *Introduction to Geometric Measure Theory*, Stanford-hosted PDF, SHA256 `e4e2367b5a0555feed16712061b39b534fe554f0c920bb609ab983f3e698b88d`.

No historical review or checker, source README, literature log, root conclusion, or sibling conclusion was used. This reconstructs the existing proof and tests its assumptions; it is not a new attempt at the central theorem.

## Exact claim and acceptance criterion

For pairwise disjoint convex sets K1,K2,K3 in R3, a tangent line must both meet each Ki and lie in one of its supporting planes. Supporting planes need not be unique. Ki need not be closed, bounded, smooth, strictly convex, or full dimensional. Empty sets are permitted and give an empty common-tangent locus. The hypothesis is that the union of all common tangent lines has Lebesgue outer measure zero, equivalently is contained in a Lebesgue-null measurable set.

The claim under test is not countable containment in 2-manifolds. Lipschitz sweeps with zero 3-Jacobian prove the stated measure assertion only.

Acceptance requires checking the cap-chart input, compact Borel tangency, the contact-rank constraint at almost every retained parameter, three distinct contact heights, local Lipschitzness of the sweep, all exceptional parameters, the noninjective equal-dimensional area formula, a countable global cover, and all dimension and nonclosed/unbounded boundary cases. Finite computations cannot establish these analytic statements.

## 1. Compactness and Borel parameter sets

Work first with nonempty compact convex sets. In a line chart write a line as L(u,v)={(u+zv,z):z real}, with u,v in R2. If L(uj,vj) converges to L(u,v) and is tangent to compact C, choose contacts aj in C and outward unit normals mj of supporting planes containing Lj. Subsequence compactness gives aj->a in C and mj->m on S2. The limits obey m dot (y-a)<=0 for all y in C, m dot (v,1)=0, and m dot ((u,0)-a)=0. The contact heights also converge because contacts are bounded, and a belongs to the limiting line. Thus tangency is closed. This does not require unique contact or normal or a full-dimensional C.

Lines contained in a fixed planar affine hull form a closed line-space set. A single fixed affine line is closed. Their complements are open, so tangency intersected with the retained exclusions is Borel. Its inverse image E under a continuous Lipschitz line chart F is Borel in the open domain U. All intersections with bounded patches and height intervals are measurable. A chart can include extra lines and can be noninjective.

## 2. Density gives every required approach direction

Let q0 belong to E, be a density-one point of E, and be a differentiability point of F. For each fixed h, dist(q0+tau h,E)=o(tau) as tau decreases to zero. Indeed, if for some eps>0 a sequence of distances were at least eps tau, the balls B(q0+tau h,eps tau/2) would miss E and lie in B(q0,(|h|+eps/2)tau). Their area is a fixed positive proportion of that containing ball, contradicting density one. For h=0, q0 itself is available. Approximate distance minimizers give qtau in E with qtau=q0+tau h+o(tau); no existence of a nearest point is assumed. U is open, so these points remain in U for sufficiently small tau.

The exceptional subset of E has 2-dimensional measure zero by the Lebesgue density theorem and Rademacher's theorem. Nothing presumes that E contains an open region or a differentiable curve. If E itself is null, its entire sweep is dealt with by the exceptional-set argument below.

## 3. Fixed affine shear and rank meaning

At a chosen good q0, the affine bijection (x,z)->(x-u(q0)-zv(q0),z) makes F(q0) the vertical line L(0,0). It preserves convexity, incidence, supporting planes, and tangency; it has determinant one and preserves nullity. The chart derivatives A=Du(q0), B=Dv(q0) become exactly the same matrices, since only constant intercept and slope vectors were subtracted. The contact height z0 is unchanged. A metric interior ball may change under the shear, but a fresh ball can be chosen in the transformed full-dimensional set. No preservation of Euclidean balls by shear is assumed.

For each h and its density sequence, u(qtau)=tau Ah+o(tau), v(qtau)=tau Bh+o(tau). At fixed height z0 the first-order transverse displacement is tau (A+z0B)h. The candidate's contact claim is rank(A+z0B)<=1 at every contact with a retained set.

## 4. Full-dimensional contact: scaled interior ball contradiction

Suppose A+z0B were onto R2. Pick B(c,r) inside C, c=(w,cz), and h with (A+z0B)h=w. At height z0+tau(cz-z0), the perturbed line has transverse coordinate tau w+o(tau); the extra slope-height product is O(tau^2). Convexity and a=(0,z0) in C put the open ball

    B((1-tau)a+tau c, tau r)

inside C for 0<tau<1. The point of the perturbed line has exactly the center's height and transverse error o(tau), so it lies in that ball for small tau. A line through an ambient interior point cannot be contained in a supporting plane. This contradicts qtau in E. The argument needs an actual contact a in C; a mere supporting-plane incidence without meeting would not suffice.

## 5. Planar contact: exact intersection derivative

Let H=aff C have equation Nx dot x+Nz(z-z0)=0. Retaining only transverse lines makes Nz nonzero after the shear. A nearby line intersects H uniquely, with height

    z(q)=(Nz z0-Nx dot u(q))/(Nz+Nx dot v(q)).

Choose a relative interior disk B_H(c,r) in C, c=(w,cz). Under the same hypothetical onto rank, select h with (A+z0B)h=w. The derivative of this height function along h is

    Dz(q0)h=-(Nx dot (Ah+z0Bh))/Nz
              =-Nx dot w/Nz=cz-z0,

because c-a lies in H. Consequently the full intersection point is a+tau(c-a)+o(tau), and both it and the relative-disk center lie in H. The scaled relative disk of radius tau r is contained in C by convexity, so the intersection is a relative interior point.

A supporting affine plane through a relative interior point of a 2-dimensional convex set must be H: its linear functional vanishes on both signs of every tangent direction to H, hence on the entire 2-dimensional direction space. The perturbed line remains transverse near q0 and therefore cannot lie in H. This supplies the contradiction. The exception for contained planar lines is essential; they are removed because their swept points lie in H, which is already null.

## 6. Segment contact: lambda control without an interior assumption

Write the affine hull of a 1-dimensional compact C as a+lambda(dx,dz). Excluding equality of this affine line with L(0,0) forces dx nonzero. For every nearby q in E, its actual intersection with C is an intersection with that affine hull, and

    nu(q):=u(q)+z0v(q)=(dx-dzv(q))lambda(q).

The coefficient after dotting with dx is |dx|^2-dz dx dot v(q), bounded away from zero near q0. Thus lambda(q)=O(|u(q)|+|v(q)|), with the fixed factor |z0| absorbed. Along the density sequence it is O(tau). For any n perpendicular to dx,

    n dot nu(qtau)=-dz (n dot v(qtau))lambda(qtau)=O(tau^2).

Dividing by tau and taking the differentiability limit gives n dot (A+z0B)h=0 for every h. The image is contained in span(dx), so rank is at most one. This uses the entire affine hull rather than relative interior of the interval and is valid when the contact is an endpoint or lies in a contact segment. If dz=0, the perpendicular component is exactly zero. If the affine line were vertical, it would coincide with the base line and belongs to the discarded null locus.

## 7. Point contact

If C={a}, then every retained q in E obeys u(q)+z0v(q)=0. Density sequences yield (A+z0B)h=0 for every h, so the rank is zero. Supporting planes for a point present no obstruction: every incident line has such a plane. The point-chart reduction later does not depend on a unique support plane.

## 8. Three distinct contacts are exactly enough

Choose one contact from each Ki on the base line. Pairwise disjointness guarantees three different contact points and hence three distinct z heights; contacts may lie in segments, and no genericity or uniqueness is needed. P(z)=det(A+zB) is a polynomial of degree at most two. Each of the three contacts gives a root, forcing every coefficient to vanish. This argument is exact and independent of root spacing, conditioning, or contact selection.

The conclusion is P identically zero, not A=B=0. Rank-one line families and nonzero slopes are compatible with it. If only two roots are known, P need not vanish identically; an explicit two-set geometric control is given below.

## 9. Sweep, exceptional parameters, and area formula

For G(q,z)=(u(q)+zv(q),z), pick bounded open parameter balls with closure inside U, and bounded height intervals. F is bounded on each such patch; the term (z-z')v(q') is then bounded by a constant times |z-z'|. Together with F's Lipschitz bound and |z|<=M this proves G is Lipschitz on the patch product. Boundedness of the parameter domain alone is not used as a substitute for boundedness of F: the latter follows from its Lipschitz bound and a fixed value on the patch.

At every good q and every finite z, direct differentiation (including the mixed O(|delta q delta z|) term) gives

    DG(q,z)=[ A+zB  v(q) ; 0 0  1 ],
    |det DG(q,z)|=|P(z)|=0.

If N is the 2-null exceptional parameter set, N times a bounded interval is 3-null by product measure/Fubini. A Lipschitz map from R3 to R3 maps such null sets to null sets. Alternatively, apply the area formula directly to E times the interval with its almost-everywhere zero Jacobian, including these exceptional parameters. Their image cannot acquire volume simply because z supplies a third parameter.

The applicable area formula is the noninjective formula, counting possibly infinite multiplicity. Its equal-dimensional specialization yields

    L3(G(S)) <= integral_S |det DG| dL3 = 0

for a measurable bounded S. Injectivity is unnecessary; every image point has multiplicity at least one. This is not Sard's theorem. If a version stated for global maps R3->R3 is used, extend the locally Lipschitz G coordinatewise outside a slightly larger patch; the extension agrees and has the same derivatives in the smaller open patch. Simon's measurable-domain formulation already covers that localization.

Exhaust U by countably many bounded balls with closure in U, heights by integer M, and all line-family charts by a countable list. The swept image is null after this countable union. Images of Borel sets may be analytic rather than Borel, but the null outer-measure conclusion supplies a measurable null hull in any event; the target only asks containment in one.

## 10. All compact dimensional cases and open extensions

Discard, once and for all, lines contained in the affine plane of any planar Ki and lines identical to the affine line of any interval Ki. Their swept loci lie in finitely many fixed planes or lines and are null.

- If at least two Ki have affine dimension at least two, apply the candidate's cap-chart Lemma 1 to those two. The rank and area argument applies to the tritangent Borel subset of each chart, regardless of extra lines or chart multiplicity.
- If some Ki is a point, every common tangent line passes through that point. The projective direction space RP2 has a finite atlas. In a graph-line direction chart, a point at height z0 fixes u=a_x-z0v, a smooth map of the two direction parameters v. This covers all directions after a finite choice of coordinate axes and gives the required open parameter domains.
- Otherwise at least two Ki are genuine compact intervals. Write their points as a(s),b(t). Compact disjointness gives a positive minimum distance, so d(s,t)=b(t)-a(s) never vanishes on the closed parameter rectangle. Locally choose a coordinate component d_k nonzero; slope and intercept are rational expressions with denominator d_k and hence smooth with bounded derivative after taking a smaller bounded neighborhood. This neighborhood can extend slightly beyond endpoints while retaining nonzero denominator. The original closed rectangle is covered by finitely many such neighborhoods (a countable cover would also suffice), including corners and edges. The third tangency condition is selected on the extended open chart by E; selecting extra extended lines causes no problem.

The dimension cases are exhaustive: if there is no point and fewer than two dimension>=2 sets, at least two of three dimensions are one. Empty Ki has already made the locus empty. A degenerate interval is a point, not an unaddressed case.

## 11. Arbitrary sets, closure, and countability

For a given tangent L to arbitrary disjoint convex Ki, choose ai in L intersect Ki. They are distinct. Pick pairwise disjoint closed balls with rational centers/radii in fixed original Cartesian coordinates, ai in their interiors, and sufficiently small diameters. This is possible without any minimum distance between the original sets or their closures, because only the three chosen points must be separated.

Ci=closure(Ki) intersect Bi is nonempty compact convex, contains ai, and is disjoint from the other Cj because the balls are disjoint. The original supporting plane bounds the closure by continuity, so L remains tangent to each Ci. Closure contact elsewhere or overlapping closures cannot break this localized argument. Each triple of rational balls is one of countably many; each compact-case locus is null. The union of these null hulls contains the original swept locus. Unboundedness and nonclosedness need no additional parameter chart. No measurability of the original Ki was invoked.

## 12. Direct independent inspection of the cap input

The remaining geometric input is Lemma 1. I inspected its proof directly, rather than taking another family's conclusion:

1. The signed support-gap function is globally Lipschitz for a bounded cap. With an interior planar projection, its zero set is exactly projected boundary tangency.
2. The cap preserves supporting normals at the base line because the selected contact is inside its ball. A functional positive at an original point would also be positive on an initial portion of the contact-to-point segment inside the cap. This also preserves affine dimension.
3. The increment bounds have the stated signs: support-function increments range between extrema of -z n dot delta v, so subtracting them yields extrema of n dot (delta u+z delta v).
4. For own motions, initial maximizing normals give the lower bound (1-eps)alpha/2 >= alpha/4. For cross motions, the absolute coefficient is at most eps for every unit normal. Normal compactness gives the local alpha/2 bound, including nonunique normal faces.
5. The V_A,V_B motions are independent because evaluation at s,t isolates e_A,e_B. Their coordinate completion is invertible.
6. Strict monotonicity and sign brackets give unique roots for nearby parameters. Their cross constants are eps/(alpha/4)<1/4. First choose the square size, then a small parameter ball: root values are bounded by their cross constants times the square radius plus their parameter-Lipschitz bounds, so the square is invariant. The fixed point is Lipschitz in the two free parameters.
7. The graph covers every nearby cap common tangent in its chosen ambient neighborhood, not merely the selected base point. For a fixed rational cap pair, the set of eligible tangent lines has an open cover in the second-countable line manifold, and thus a countable subcover. Only then take the countable union over rational pairs. This order avoids the invalid claim that all nearby original-body tangencies meet the same cap.

No definite gap was found in this direct inspection. The global theorem remains logically conditional on correctness of this cap cover; the dedicated cap audit may examine it more thoroughly. The rank/area theorem proved here is independently valid for any countable Lipschitz two-parameter line-family cover, whether or not that input is obtained by this particular cap construction.

## 13. Exact falsification controls

**Two contacts can sweep positive volume.** Let A=[0,1] times [-1,1] times {0}, and B=[-1,1] times [0,1] times {1}. These are disjoint compact planar convex rectangles. For s,t in (-1,1), the line through (0,s,0) and (t,0,1) is tangent to A in the plane x-tz=0 and to B in the plane y+s(z-1)=0. The line chart is u=(0,s), v=(t,-s). Its sweep is (zt,(1-z)s,z). The determinant is z(z-1), zero at precisely the two contact heights, and on 0<z<1 the image is an open region with volume 4 integral_0^1 z(1-z) dz=2/3. Thus two rank-one contact evaluations are insufficient.

**Intersection is insufficient.** Three radius-1/2 closed balls centered at (0,0,0),(0,0,3),(0,0,6) are pairwise disjoint. Every vertical line x=u, |u|<1/2, meets the interior of all three. Their sweep is an open cylinder and has positive volume on every nontrivial bounded height interval. At all contacts of this intersection family A=I,B=0, invalidating the asserted rank constraint. Actual tangency is essential.

**Disjointness is essential.** If all three sets equal {0}, every line through the origin is tangent to all three and their union is R3. All contacts have the same height, so three repeated roots give no determinant identity.

**Density cannot be omitted from the pointwise rank assertion.** Let C be the unit ball in R3 and F(q)=(u=q,v=0). The vertical line is tangent exactly when q is on the unit circle. F is differentiable everywhere, with A=I,B=0, including those tangent parameters, so rank two persists. The tangent parameter circle has 2-measure zero and no density-one points. Its sweep is a null cylinder surface, consistent with the area conclusion.

These are checkable analytic constructions. A small exact control checker records polynomial and rational-volume identities, but no checker replaces the arguments above.

## 14. Primary theorem hypotheses checked

Primary authored reference: Leon Simon, *Introduction to Geometric Measure Theory*, [Stanford PDF](https://web.stanford.edu/class/math285/ts-gmt), chapters 1–2.

The inspected text supplies density one for almost every point of a measurable set under a locally finite Borel-regular measure with its Vitali property (Ch. 1, Theorem 3.16 and Euclidean discussion 3.11); differentiability almost everywhere for Lipschitz Euclidean functions (Ch. 2, Theorem 1.4), applied coordinatewise; and a measurable-domain Lipschitz area formula with multiplicity (Ch. 2, 3.2–3.4). Here the measure is Lebesgue measure, parameter domains are open, dimensions in the sweep are 3 and 3, and the domain subset is Borel. These hypotheses match. Equal-dimensional Jacobian is |det DG|, and multiplicity gives the image bound without injectivity.

The source is an actual author-written primary textbook, independently inspected. Historical citation names alone were not accepted as evidence. A more precise theorem-and-page citation in the candidate would improve exposition; this is optional and not a mathematical repair.

## Independent preliminary verdict

No mandatory repair is identified in the measure/rank/area or boundary/dimensional reductions. The strongest independently verified result is: within any countable family of Lipschitz two-parameter line charts, the tritangent locus of three disjoint compact convex sets sweeps a Lebesgue-null set; the rank claim holds in every affine dimension after removing the explicitly null contained-line exceptions. The complete arbitrary-convex-set theorem follows once the cap-chart Lemma 1 is accepted. Direct inspection of that lemma found no gap, while leaving its detailed adversarial review to its assigned family.

Priority is not certified here. No source novelty assertion is accepted merely because the local proof passes. The original stronger manifold conjecture remains outside what these artifacts establish.
