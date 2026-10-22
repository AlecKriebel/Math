# Independent acceptance of the regular-radius counterexample

13 October 2026. Problem 30003527 / queue row 1767. Independent adversarial audit within shared substantive pass 4 of 5. This audit is not an additional substantive attempt.

## Verdict and precise scope

**Accepted without a required mathematical correction.** The frozen report constructs a compact movable stationary set C for a bounded globally Lipschitz full flow such that M_1(C) is nonmovable, although its ambient distance function has no Clarke critical value anywhere in [3/5,infinity). The unit distance sphere is a compact Lipschitz surface and equals the boundary of the closed unit neighborhood. The invariant core meets that boundary along nonstationary orbit segments, at points where the distance function is smooth and the boundary is planar.

For this same C, every radius 0<r<1 satisfies M_r(C)=C. Accordingly, the construction defeats the proposed sufficiency of a regular ambient distance radius for movability of the invariant metric core. It does not refute the existence of arbitrarily small good radii, an almost-every-radius assertion, or the full invariant movable-enlargement question. In fact C itself is a permitted movable invariant enlargement of C.

The audited artifact is REGULAR_RADIUS_COUNTEREXAMPLE.md, 11,447 bytes, SHA-256:

9b906d10aa3b4789619065ff345eda4def4389ba4a5040c57f51c0c465c54389

It was read in full, checked against the exact accepted stretched-book construction, and left unchanged. The report below supplies expanded checks of the coordinate encoding, endpoint and boundary cases, regularity implication, and source hypotheses. It contains authored mathematics and verification metadata, not copied source bodies.

## 1. Exact inherited stretched-book encoding

The original pass-2 construction uses a solenoid copy K in the three-page book

T_book = ([0,1] x [-1,1] x {0}) union ([0,1] x {0} x [0,1]).

Its common edge is E=[0,1] x {0} x {0}. The quotient q from the stretched book fixes the bottom rectangle, collapses the vertical binding intervals onto E, and sends a top point (u,v,1) to (u,0,v). Thus the exact planar sets encoded in the present report are

P_0 = {(u,v): (u,v,0) is in K},

P_1 = {(u,v): 0<=v<=1 and (u,0,v) is in K},

S = {(u,0): (u,0,0) is in K}.

They are compact. They satisfy P_0 subset [0,1] x [-1,1], P_1 subset [0,1] x [0,1], and P_0 intersect {v=0} = P_1 intersect {v=0} = S. Their union with the full binding columns is exactly q^(-1)(K), not merely a shape-equivalent proxy.

The binding S is nonempty. Otherwise the connected K lies in one of the three components of T_book minus E, each contained in a single planar page; planar movability and homeomorphism invariance would contradict the nonmovability of the solenoid. Since S is contained in both P_i, both P_i are nonempty as well. This avoids any nonemptiness assumption about incidental page interiors.

The original proof and its independent acceptance were read in full. The explicit homeomorphisms h_t from the stretched book onto T_book converge uniformly to q, and q composed with h_t^(-1) has an explicit small armwise homotopy to the identity. The direct neighborhood argument fixes its domain before the subsequent arbitrary target. It therefore transfers hypothetical movability of q^(-1)(K) to K with the correct quantifier order. The accepted nonmovability of A is available without a new cell-like-map theorem or a finite-gluing assumption.

The imported established topology is Bing's circle-like embedding theorem, solenoid nonmovability, and Borsuk's planar movability and shape invariance, with the scope verified in the existing pass-2 acceptance. This audit relies on that accepted topological input rather than claiming a new independent proof of those classical theorems.

## 2. The new stationary compactum is movable

Under L(u,v)=(u/10,1+v/10), the sets Q_i=L(P_i) and T=L(S) have the stated ranges. The two sheets C_-=Q_0 x {-2} and C_+=Q_1 x {2} are disjoint because of their heights. Each is disjoint from W=[-1,1] x {0} x [-2,2], because their y-coordinates are at least 9/10. All three pieces are nonempty compact planar sets, hence movable.

Finite disjoint unions preserve movability with the required quantifiers. Given an outer neighborhood of C, choose pairwise disjoint open neighborhoods of the three pieces inside it. Choose a movability domain for each piece in its corresponding outer neighborhood. The union of these three fixed disjoint domains is a neighborhood of C. For every subsequent target neighborhood, the three separate homotopies combine continuously on that disjoint union and remain in the original outer neighborhood. No assertion about general finite unions of movable compacta is involved.

## 3. Full flow and the invariant-neighborhood convention

For any nonempty compact C, distance to C is 1-Lipschitz. Its minimum with 1 is still 1-Lipschitz and is bounded. Therefore F_C=min(1,dist(.,C))e_3 is globally Lipschitz and bounded, and its ODE has a unique full flow for all real times. The zero set of F_C is precisely C. Horizontal coordinates are fixed along every orbit.

On an open complementary interval of a vertical fiber C_p, the scalar velocity is strictly positive. A nonstationary orbit cannot tend to an interior point of that interval in either time direction, because velocity near that point is bounded below by a positive constant. It cannot hit a finite endpoint in finite time, by uniqueness against the stationary endpoint solution. Its image is therefore the entire open complementary interval. If that interval is unbounded, the full orbit is unbounded.

Write N_r(C)={d<=r}. For r>0 this is compact, and

M_r(C) = intersection over all real t of phi_C(t,.)^(-1)(N_r(C))

is a closed invariant subset of N_r(C). The formula uses both time directions. Consequently it contains C and exactly the bounded complementary fiber intervals whose entire closed segments lie in N_r(C). Endpoints cause no issue: they already lie in C, and N_r(C) is closed. A point on a fiber with no stationary point cannot contribute an extra bounded invariant orbit merely because part of its fiber intersects N_r(C).

The stationary wall's projection is y=0, while the endpoint sheets project into y>=9/10. Thus there are no bounded gaps joining the wall to a sheet, no additional wall gaps, and no cross-piece fiber ambiguity. Every bounded gap is exactly {p} x (-2,2) for p in Q_0 intersect Q_1.

## 4. Exact distance and exact selected gaps

Let p=(x,y) belong to Q_0 intersect Q_1 and let -2<=z<=2. Then x is in [0,1/10], y is in [1,11/10], and (x,0,z) lies in the wall, including its horizontal and vertical boundary cases. Orthogonal projection therefore gives

dist((p,z),W)=y.

Because p itself belongs to each sheet's base, the two sheet distances are exactly 2+z and 2-z, respectively. No point on either sheet can be closer than the vertical coordinate difference. Hence the stronger exact formula

d((p,z),C)=min(y,2+z,2-z)=min(y,2-|z|)

holds throughout every closed gap. Its maximum in z is y, attained at z=0 because y<=11/10<2.

It follows directly that a gap is selected at radius 1 exactly when y=1. The intersection of the common base with that line is T. Therefore

M_1(C)=W union D,

D=(Q_0 x {-2}) union (Q_1 x {2}) union (T x [-2,2]).

The map (x,y,z) -> (10x,10(y-1),(z+2)/4) is an affine ambient homeomorphism and takes D exactly to A. The distance formula also confirms that every bounded gap has maximum distance at least 1, so none is selected at any 0<r<1. Thus M_r(C)=C at all those radii, including arbitrary radii approaching 1 from below.

## 5. Nonmovability of the core and clopen inheritance

The set D lies in y>=9/10 and the wall lies in y=0. They are separated by a positive distance, so D is a clopen compact subset of M_1(C). Since D is homeomorphic to A, it is nonmovable.

For completeness, let X be a movable compactum and D a clopen compact subset, with compact complement E. Given an arbitrary outer neighborhood O_D of D, choose disjoint open O_1,O_2 with D subset O_1 subset O_D and E subset O_2. Apply movability of X in O_1 union O_2 to obtain a fixed neighborhood V, and use V_D=V intersect O_1 as the domain for D. For a subsequent target W_D of D, apply movability of X with target (W_D intersect O_1) union O_2. A homotopy path starting in O_1 cannot cross between the two disjoint relatively clopen parts of O_1 union O_2. The restriction to V_D therefore remains in O_D and ends in W_D. The choice of V_D precedes W_D, so D is movable. The case E empty is immediate.

Applying this implication contrapositive proves that M_1(C) is nonmovable. The disjoint added wall cannot conceal the bad block.

## 6. Adversarial audit of the critical-point exclusion

Let a=(x,y,z) be outside C, rho=d(a)>=3/5, and suppose a belongs to the convex hull of its nearest-point set Pi(a). In finite-dimensional Euclidean space the convex hull of the compact Pi(a) is compact, and a has a finite convex representation. Since Pi(a) is contained in C, the coordinate bounds on C give

-1<=x<=1, 0<=y<=11/10, -2<=z<=2.

These bounds are needed before projecting to W. They ensure that the orthogonal projection (x,0,z) really belongs to the finite wall rectangle, even if x or z is at an endpoint. Projection onto this closed convex rectangle is unique. Thus dist(a,W)=y and

3/5<=rho<=y<=11/10.

Both sheets cannot supply nearest points: two such points have vertical separation 4, whereas the triangle inequality would give their distance at most 2rho<=22/10<4. At least one sheet must supply a nearest point, because the convex hull of wall points alone has y=0, contradicting y>=3/5. Therefore the nearest points use exactly one sheet at height sigma in {-2,2}, possibly along with the unique wall projection.

In a convex representation of a, let lambda be the total wall coefficient, possibly zero. We have lambda<1, since y>0. Every remaining point has height sigma. The z-coordinate equation is

z=lambda z+(1-lambda)sigma,

so z=sigma. The x-coordinate equation is x=lambda x+(1-lambda)x_star, with x_star in [0,1/10], so x is in [0,1/10]. These deductions are still valid if the wall is a nearest point with coefficient zero, or if it is absent.

Choose any point c of this nonempty sheet. Since c_y is in [9/10,11/10], y is in [3/5,11/10], and z=c_z=sigma, we obtain

|x-c_x|<=1/10, |y-c_y|<=1/2, |z-c_z|=0.

Therefore

rho<=|a-c|<=sqrt(26)/10<3/5.

The final inequality is exact: 26/100<9/25. This contradicts the assumed lower bound on rho. The use of an arbitrary sheet point is legitimate; it need not itself belong to Pi(a). Its existence alone gives an upper bound on distance to C.

This proves that a is outside conv Pi(a) for every a with d(a)>=3/5, with no restriction to the candidate gap fibers or to the interior of the wall projection. In particular, possible nearest points at wall edges and corners have not been silently omitted.

## 7. Convex nearest-point exclusion really implies Clarke noncriticality

The report proves the necessary implication directly rather than assuming an unverified equality for the entire Clarke subdifferential. Let a be outside conv Pi(a). Strict separation gives a nonzero v and alpha>0 such that

(a-c) dot v >= alpha for every c in Pi(a).

For nearby b, this inequality persists uniformly as (b-c_b) dot v>=alpha/2 for every nearest point c_b of b. Otherwise a contradicting sequence b_j -> a, c_j in Pi(b_j), has a subsequence converging in compact C to c in Pi(a), contradicting strict separation. This is upper semicontinuity of nearest-point sets, not an assumption of a unique nearest point.

For small t>0, using c_b as a comparison point gives

d(b-tv)^2 <= d(b)^2-alpha t+t^2|v|^2 <= d(b)^2-alpha t/2.

Choose a fixed M bounding both d(b) and d(b-tv) in a sufficiently small neighborhood. Dividing by the positive sum of distances yields the uniform bound

[d(b-tv)-d(b)]/t <= -alpha/(4M)<0.

The neighborhood can be chosen away from C because d(a)>0. Taking the limsup over all b approaching a and t decreasing to zero proves d^0(a;-v)<0. If zero belonged to the Clarke subdifferential, its defining directional inequality would require 0<=d^0(a;-v), a contradiction.

Thus no point at distance at least 3/5 is Clarke critical. The meaning here is nonvanishing Clarke generalized gradient, precisely the regular-point convention of the cited source. It is not an assertion that distance is everywhere differentiable or Clarke-regular as a function in a different terminology.

## 8. Regular level surface: exact source hypotheses and boundary equality

The existing primary PDF of Jan Rataj and Ludek Zajicek, Critical values and level sets of distance functions in Riemannian, Alexandrov and Minkowski spaces, arXiv:0911.4020v1, was locally extracted and its printed/PDF pages 3, 5 and 6 were visually inspected.

Definition 2.4, p.3, defines a regular point by exclusion of zero from the Clarke subdifferential. Lemma 2.5 gives the equivalent uniform strictly decreasing direction. The displayed numerator in that lemma has an apparent typographical d(x) where f(x) is meant; its immediately following proof uses f consistently. Nothing in this audit depends on that typo.

Proposition 2.13 assumes only a locally Lipschitz real function on an open subset of R^n and a noncritical point for its part (i). It concludes a local (n-1)-dimensional Lipschitz surface. Additional DC and semiconcavity hypotheses belong to parts (ii) and (iii) and are not needed for part (i). Definition 2.11(i), p.5, uses local graphs over open subsets of linear subspaces, exactly the kind of Lipschitz surface claimed by the report.

Apply part (i) to d on the open set R^3 minus C at every point of {d=1}. The function is globally 1-Lipschitz, these points are outside C, and Section 7 establishes the noncritical hypothesis. Thus the unit level is locally a two-dimensional Lipschitz graph. It is closed and bounded because C is compact, so the level surface is compact. It is nonempty, for example by the explicit points over T in Section 9.

The boundary claim does not follow merely from a generic level-set statement; it is justified here by the strict direction. In sufficiently small opposite directed steps from a level point, the uniform slope inequality gives points with d<1 and points with d>1. Thus every point of {d=1} is a boundary point of {d<=1}. Conversely, continuity makes every point with d<1 interior to {d<=1}, and every point with d>1 exterior. Hence

{d=1}=boundary({d<=1}).

No measure-theoretic almost-every-radius theorem is required for this fixed regular radius or for the quantitative exclusion interval.

## 9. Smooth boundary at nonstationary invariant trajectories

For p=(x,1) in T and -1<z<1, the distances to the endpoint sheets are 2+z and 2-z, both strictly greater than 1. The distance to W is 1, with unique nearest point (x,0,z). Because x is in [0,1/10], it is strictly inside the wall's x-range [-1,1]; because z is in (-1,1), it is strictly inside the wall's z-range [-2,2].

Continuity preserves the strict sheet-distance margin in a neighborhood of each such point. Shrink that neighborhood so its wall projections remain in the rectangle and its y-coordinate remains positive. Throughout it the distance to C is exactly the y-coordinate. The local unit distance sphere is therefore the smooth plane y=1, not just an abstract Lipschitz surface. This assertion correctly excludes the endpoint values z=+/-1, where an endpoint sheet can tie with the wall.

Each point lies on the entire bounded complementary orbit {p} x (-2,2), which was selected by M_1(C). It is nonstationary, and its central segment has velocity e_3. Accordingly Inv(N_1(C)) intersects the boundary of N_1(C). The compact unit neighborhood is not isolating in the usual sense Inv(N) subset int N, despite the regular ambient distance sphere and these smooth local boundary patches. Smoothness alone supplies no dynamical entrance/exit condition.

## 10. Frozen inputs, source identity and verification limits

The following authored inputs were read in full and hash-checked:

- REGULAR_RADIUS_COUNTEREXAMPLE.md: 11,447 bytes; SHA-256 9b906d10aa3b4789619065ff345eda4def4389ba4a5040c57f51c0c465c54389.
- VERTICAL_GAP_COUNTEREXAMPLE.md: 11,970 bytes; SHA-256 85ab6a5e1b948ebc8f83f6506cb04a1d9e8fa644826261fcc40247567b695403.
- VERTICAL_GAP_ACCEPTANCE.md: 14,943 bytes; SHA-256 ef81f2296048ec77a5b8175bb838cd66c6cb6b5d61482f210e14ec04df26d1c8.
- METRIC_THRESHOLD_ACCEPTANCE.md: 15,036 bytes; SHA-256 c87b99b39c647e11305879754374410d73ba0b69c8678414fdde0e3026fa9539.

Newly inspected primary-source identity:

- Jan Rataj and Ludek Zajicek, Critical values and level sets of distance functions in Riemannian, Alexandrov and Minkowski spaces, arXiv:0911.4020v1, dated 20 November 2009. Existing PDF: 277,685 bytes; SHA-256 35f29ec695cdf8248b049e8035fadb601a89cafb34fd93ab0cbdeb6253be2bc7. Public URL: https://arxiv.org/pdf/0911.4020 . Definition 2.4 and Lemma 2.5 on p.3, Definition 2.11 and Proposition 2.13 on pp.5-6 were read in extracted text and checked in rendered primary pages. No fresh download was needed.

Inherited public topology references:

- R. H. Bing, Embedding Circle-Like Continua in the Plane, Canadian Journal of Mathematics 14 (1962), 113-128, Theorem 8. https://doi.org/10.4153/CJM-1962-009-3 . Used with the theorem/proof scope recorded in the accepted pass-2 audit.
- K. Borsuk, On movable compacta, Fundamenta Mathematicae 66 (1969/1970), 137-146. https://doi.org/10.4064/fm-66-1-137-146 . Movability definition, solenoid example, shape invariance and planar movability are used with their scope recorded in the accepted pass-2 audit.

All exact geometric and dynamical claims, including boundary and projection cases, were checked symbolically by the arguments above. Sampling is neither used nor presented as proof of any universal statement. The accompanying manifest records frozen input and output hashes, source byte counts, and inspection scope. Original artifacts and source PDF were left unchanged. Source bodies, extracted text and rendered pages remain outside the publishable audit and metadata.

No remote mutation, external communication, source-body publication or additional substantive attempt was performed. The full row-1767 invariant movable-enlargement problem remains unresolved.
