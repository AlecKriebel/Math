# Five approaches to real active visual-hull events

Queue 1859, ID 20000204. Research date 2026-10-21. Original AIM question: which visual event surfaces appear on visual hulls of algebraic surfaces? This document develops exact tests and audits the imported attempt. It does not solve the unrestricted question and claims no novelty for the 2004 or 2018 classifications. Independent mathematical review passed; see INDEPENDENT_REVIEW.md for scope and remaining limitations.

## Fixed model and sources

Throughout Approaches 1–4, O is a nonempty compact regular-closed semialgebraic subset of R^3, with an explicit Boolean polynomial membership predicate Phi. Its all-external-view hull is H={p: every affine line through p meets O}. Artificial boundary A=boundary(H) minus boundary(O). No camera restrictions are implicit. General complex projective surfaces are introduced only where stated.

Primary sources inspected: Bottino–Laurentini (2004), https://doi.org/10.1109/TPAMI.2004.130 and https://cgvg.polito.it/Articles/The%20Visual%20Hull%20of%20Curved%20Objects.pdf ; Kohn–Sturmfels–Trager (2018), https://doi.org/10.1007/s40306-017-0240-1 and https://arxiv.org/abs/1707.01877 ; AIM http://aimpl.org/algvision/4/ . The source audit independently distinguishes the smooth external model from finite-camera and singular variants. The arXiv metadata was rechecked live on this research date. Source text is not reproduced here.

The 2004 necessary generic artificial-boundary candidates are tangent crossing and triple point. The 2018 general projective event discriminant has five components. These are different assertions. A positive complex degree does not prove a real active patch exists.

## Approach 1: exact global semialgebraic activity, including singular inputs

### Lemma 1: elementary hull properties

O is contained in H, H is closed, and H is contained in conv(O). Consequently H is compact. For closedness, if L=p+Rv misses compact O then dist(L,O)>0: the distance function to the closed line attains a strictly positive minimum on O. Every sufficiently small translation of L also misses O, so points near p are outside H. For convex containment, strictly separate any p outside compact conv(O) by a plane: some n satisfies n·p>sup_{x in O} n·x. Choose nonzero v perpendicular to n. The entire line p+Rv lies in the separated plane and misses O. The remaining statements follow directly.

Interior(O) is contained in interior(H), since O is contained in H. Hence A=boundary(H) minus O, equivalently boundary(H) intersect complement(O).

### Exact membership and boundary formulas

Define

M(p) := for every v with v·v=1, there exists real t such that Phi(p+tv).

F(q) := there exists v with v·v=1 such that for every real t, not Phi(q+tv).

Then the following first-order formula is EXACTLY A:

not Phi(p) AND M(p) AND [for every epsilon>0 there exists q with |q-p|^2<epsilon^2 AND F(q)].

Proof: M is the definition of H and F is its complement. Since H is closed, membership in H together with arbitrarily close complement points is precisely its boundary. The preceding lemma justifies replacing removal of boundary(O) by removal of O. No smoothness or genericity is used.

Consequences: quantifier elimination over real closed fields yields a semialgebraic description of A when coefficients are rational or effectively represented real algebraic numbers. A cylindrical algebraic decomposition adapted to A and a proposed reduced algebraic candidate C determines whether dim_R(A intersect C)=2. For a real algebraic surface with regular two-dimensional real locus, this is the appropriate existence test for a relatively open active patch on some smooth stratum. For a specific irreducible component, use that component and discard its lower-dimensional singular locus. This is a decision procedure in principle, not a practical complexity bound or a newly classified finite event list. It avoids the unproved step that root-isolation on one generator determines activity.

Failure/limit: eliminating all quantified variables may be prohibitively expensive. It also presupposes the real solid, not merely an equation f=0 with unspecified inside or selected components. No full CAD run for a nonconvex generic example is claimed.

## Approach 2: oriented local contact test and why it is only a pruning rule

### Lemma 2: strict escape certificate

Let p be outside O, v a unit vector, and L=p+Rv meet O at exactly finitely many smooth boundary points x_i=p+t_i v, with no intersection with interior(O). Let n_i be outward unit normals. If a vector w perpendicular to v satisfies

(t_i n_i)·w>0 for every i,

then p is outside H.

Proof. At every contact choose a C^1 local defining function g_i, positive outside O, with gradient equal to a positive multiple of n_i. The original line near x_i has g_i>=0, since it misses the interior. In the perturbed line p+t(v+epsilon w), the derivative at epsilon=0 is t grad(g_i)(p+tv)·w. It is strictly positive at t_i and uniformly positive on a small parameter neighborhood, by continuity. For sufficiently small positive epsilon, the entire such interval is outside O. On the remaining compact interval in which any intersection with O is possible, the original line has positive distance from O, and this persists under perturbation. Outside a fixed parameter interval, boundedness of O and v+epsilon w bounded away from zero exclude intersections. Thus the perturbed line through p is free. Smoothness implies n_i·v=0 because a non-tangent crossing would enter the interior. Also t_i is nonzero since p is outside O.

### Corollary: positive-dependence necessary condition

If p is in H under these hypotheses, 0 belongs to conv{t_i n_i}. Equivalently there exist lambda_i>=0, sum lambda_i=1, with sum lambda_i t_i n_i=0. Proof: if 0 is outside this finite convex hull, the closest point a to 0 has a·(t_i n_i)>=|a|^2>0. All normals lie in v-perp, so w=a is a strict escape certificate. The converse separation implication follows by dotting a putative convex relation with w.

One contact is therefore impossible. With exactly two contacts, t_1 n_1 and t_2 n_2 must be oppositely directed. In particular the tangent planes agree, but orientation adds information: if p lies between the two contacts, their outward normals must point in the SAME direction; if p lies outside their closed segment, their outward normals must point in OPPOSITE directions. Parallel normals alone omit this essential side/position test. For three contacts, merely having multiplicities 2+2+2 is insufficient: the signed normals must not lie in an open half-plane of v-perp.

### Exact odd-contact obstruction

At a smooth chosen boundary point with regular local defining function g, suppose g restricted to the line has a zero of finite odd order. Its sign changes through the contact, so the line meets interior(O) on one side. Such a line cannot be a limiting free line. In particular an exact real order-three contact in an ordinary 3+2 cusp-crossing configuration fails the no-interior-intersection test outright. This does not remove complex cusp-crossing event components, contacts on unselected real components, or degenerate situations in which a singular polynomial is not a regular boundary defining function. Even-order contacts still require a side test.

Failure/limit: lack of a strict first-order escape is NOT proof of local trapping, and local trapping around this direction is NOT proof that every direction through p meets O. Curvature and higher-order perturbations matter at the zero-margin cases. Even positive spanning in one direction cannot replace the global formula of Approach 1. This elementary lemma does not recover every genericity or contact-degeneracy assertion in the 2004 theorem.

## Approach 3: global obstructions and exact counterexamples to equality

### Lemma 3: convex objects have no artificial boundary

For any compact convex solid O, Lemma 1 gives O subset H subset conv(O)=O. Thus H=O and A is empty. In particular positive algebraic event degree can never by itself force activity.

This counterexample can be made compatible with GENERAL smooth complex projective quartics, not merely spheres or special quadrics. Start with f_0(x)=|x|^4+|x|^2-1. Its Hessian is 8xx^T+(4|x|^2+2)I. A sufficiently small coefficient perturbation through real quartic polynomials preserves positive definiteness globally: the perturbation Hessian is bounded in operator norm by C delta(1+|x|^2). It also preserves positive quartic leading form and f(0)<0. The sublevel O={f<=0} is therefore a compact strictly convex solid with smooth boundary; its gradient cannot vanish at level zero since its unique minimum is negative. This is a nonempty Euclidean-open family of real quartic coefficients. It intersects any nonempty Zariski-open generality locus defined over R, since a nonzero real polynomial cannot vanish on a Euclidean open set. Choose a member satisfying the 2018 generality hypotheses, as well as any Zariski-open conditions they require. Its complex edge event surface has the general quartic degree 160, but A is empty. This is an existence proof; it does not assert an explicit rational sample has been certified generic or that real differential genericity beyond these conditions has been checked.

### Shell example: invisible volume need not add artificial boundary

For 0<r<R let O={x:r^2<=|x|^2<=R^2}. Then H={|x|<=R}. Indeed every line through a point of the outer ball meets its outer sphere, and hence O; for a point outside the ball choose a perpendicular direction to its radius, yielding a line entirely outside the ball. Yet A is empty: boundary(H) is the outer sphere, already part of boundary(O). Thus H\O nonempty does not imply A nonempty. This object has smooth but disconnected algebraic boundary, defined by (|x|^2-r^2)(|x|^2-R^2)=0. It is not a general irreducible projective surface example. It also illustrates why choosing the solid and boundary components matters.

### Explicit local trapping with a globally free direction

In coordinates (x,y,z), take three disjoint closed unit balls centered at c_i=(t_i,n_i), where t_i=(3,6,9) and n_i are unit vectors in the yz-plane at angles 0,120,240 degrees. Their union is a compact solid with smooth disconnected real algebraic boundary; its defining product of three sphere equations is reducible, not a general projective surface. The x-axis is tangent at (t_i,0,0) to each ball and otherwise avoids their interiors. The outward normals at those contacts are (0,-n_i).

At p=0, every sufficiently small nonzero rotation of this axis meets the interior of a ball. Write its direction as (1,u). For ball i the condition that its squared distance to this line is <1 is exactly

t_i^2 |u|^2 - 2t_i n_i·u - (n_i·u)^2 < 0.

Some n_i·u is at least |u|/2. For 0<|u|<1/9, the displayed expression for that i is bounded above by t_i^2 |u|^2 - t_i |u|<0. Nevertheless p is not in H: every line through p contained in the plane x=0 misses all balls. Thus even rigorously proved local rotational trapping around a contact line does not establish hull membership.

Moreover the tangent x-axis is a limit of unconstrained free lines, so adding that condition does not repair sufficiency. Set a=(-1,-15/2), b=(0,1) in the yz-plane and use lines (t,delta(a+tb)). The dot products n_i·(a+t_i b) are -1, 1/2-3sqrt(3)/4, 1/2-3sqrt(3)/4, all negative. The derivative at delta=0 of the squared distance from c_i to the line is -2n_i·(a+t_i b)>0. For sufficiently small positive delta all three squared distances exceed 1. This counterexample has a limiting free tritangent line and locally blocked rotations through p, but fails the global all-directions condition.

Failure/limit: none of these examples realizes a positive active edge or tritangent patch. They refute equality and volume-to-boundary implications, but do not establish which nonempty degree-spectrum cases are attainable at each degree.

## Approach 4: algebraic envelope, patch-level repair, and degree audit

Assume, separately, the real generic external-hull hypotheses needed by the 2004 candidate theorem and a general smooth irreducible complex projective degree-d surface X for the 2018 formulas. Denote its edge and tritangent surfaces E and T, omitting absent low-degree components.

The safe statement needed for an envelope corollary is: every two-dimensional smooth semialgebraic stratum of A is contained in E union T (or its closure is). Let A_2 be the union of those two-dimensional strata and let Z_2 be the union of two-dimensional complex irreducible components of the Zariski closure of A_2. Then Z_2 is a union of some of E,T. Proof: closure preserves containment in a closed algebraic set; an irreducible component of dimension two contained in the union of two irreducible surfaces lies in one of them, and equality follows from dimension. This is a formal consequence of existing theorems, not a certified novel theorem. Semialgebraicity ensures a finite stratification and prevents a one-dimensional semialgebraic seam from acquiring a two-dimensional algebraic closure.

For d>=3, the general degrees are e_d=d(d-2)(d-3)(d^2+2d-4) and t_d=d(d-3)(d-4)(d-5)(d^2+3d-2)/3. Hence the NECESSARY degree set is {0,e_d,t_d,e_d+t_d}, with absent components omitted. It is not a realization theorem. Values d=3,...,7: (e_d,t_d)=(0,0),(160,0),(930,0),(3168,624),(8260,3808).

Audit of generated attempt:

1. Its known two-type classification is correctly attributed, but cannot be called a new resolution of the original unqualified AIM question.
2. Its pointwise displayed A subset E union T is stronger than a discussion only about surface-producing families; the imported proof does not independently resolve every exceptional seam or higher-contact point. Use the patch-level statement above unless exact hypotheses and pointwise source support are supplied.
3. Its limiting-line argument needs compactness of directions and persistence of an interior crossing. These are repairable: take unit directions of free lines through p_j approaching p, extract a convergent subsequence, and note that an interior intersection of the limiting line persists for nearby lines.
4. Its single-contact perturbation and nonparallel-normal assertions have a rigorous local version in Lemma 2. The stronger conclusions for arbitrary degeneracies must not be silently inferred.
5. Its assertion that all non-surviving event types are excluded needs the actual generic source theorem, not simply contact counts. Smoothness alone does not remove cusp/flecnodal/parabolic projection events.
6. Its characteristic-line derivation for a regular one-parameter family of distinct bitangent planes is sound when h and h' are independent and the contact points distinct. These regularity conditions must be stated.
7. Its irreducibility/degree argument is valid conditionally, with the patch-level correction; the arithmetic is correct. Neither novelty nor nonempty real realization follows.
8. Its detailed nine-type transcription from the 2008 piecewise-smooth paper is NOT independently certified by the recovered publisher preview; do not reuse that symbol table as a checked theorem.
9. A polynomial f|_L only tests contact and signs relative to a specified solid. It does not test all other directions through a candidate point. Approach 1 supplies the missing exact global test.

Failure/limit: no degree-specific realization theorem is proved. General projective degree formulas do not apply to arbitrary smooth real boundaries or special complex closures.

## Approach 5: finite-direction and singular variants, explicitly not the original theorem

### Exact finite-direction counterexample

For the unit ball B and an orthographic camera direction v, the silhouette reconstruction is the cylinder C_v={p: distance(p,Rv)<=1}. For the three coordinate-axis directions, the reconstructed hull is

H_3={x^2+y^2<=1, x^2+z^2<=1, y^2+z^2<=1}.

It contains p=(1/sqrt(2),1/sqrt(2),1/sqrt(2)), whose norm squared is 3/2>1. More strongly, near q=(1/sqrt(2),1/sqrt(2),1/2), the boundary is the cylinder x^2+y^2=1 because the other two inequalities are strict (3/4<1); norm(q)^2=5/4>1. Thus a two-dimensional artificial cylinder patch appears even though the underlying sphere is strictly convex and its all-direction hull has no artificial boundary. These are orthographic cameras at infinity, not finite perspective centers. A finite perspective reconstruction similarly uses camera cones, but no separate unproved formula is asserted here.

### Singular extension that is actually established

Approach 1's exact formula applies unchanged to compact regular-closed semialgebraic solids with creases, corners, and singular algebraic boundary. It decides activity in principle without purporting to classify a finite set of singular-contact event surfaces. Lemma 2 does not apply at a nonsmooth contact because a unique outward normal need not exist. Replacing it with a chosen arbitrary normal is invalid; one needs a tangent/normal-cone analysis and higher-order or stratified contact data. The 2008 piecewise-smooth literature is evidence that the two smooth candidate types do not transfer unchanged, not a proof of a universal algebraic-singularity catalogue.

Failure/limit: exact decision and a finite-camera counterexample do not settle the singular event-classification problem. No generic finite-perspective theorem or universal normal-cone sufficiency assertion is accepted.

## Outcome and remaining work

Five approaches completed as above. Independently reviewed and accepted within stated scope: elementary exact membership/boundary formulas, oriented necessary escape test, counterexamples, and conditional patch-level degree bookkeeping. The unrestricted original classification remains unresolved here. Meaningful next research would certify an explicit nonconvex algebraic solid with a positive active edge or tritangent patch using the global criterion, then investigate degree realization. This report claims no resolution of the original question.
