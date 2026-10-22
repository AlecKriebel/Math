# Independent acceptance of the left-Hausdorff-continuous bad core

13 October 2026. Problem 30003527 / queue row 1767. Independent adversarial verification of an already completed candidate within shared substantive pass 5, the final pass. This is an audit, not a sixth exploratory or research pass.

## Verdict and exact scope

**Accepted without a required mathematical correction.** The frozen candidate constructs a nonempty compact movable stationary set C in R³ for the bounded globally Lipschitz vertical field

F_C = min(1,dist(.,C)) e_3

with all four advertised properties:

1. M_1(C)=Inv({dist(.,C)<=1}) is nonmovable.
2. The compact-valued family r |-> M_r(C) is Hausdorff-continuous at 1 from both sides.
3. Every core M_r(C) with 0<r<1 is movable.
4. The ambient distance function has no Clarke critical value in [3/5,infinity).

The conjunction of a nonjump radius, ambient regularity, and movability at every strictly smaller radius is therefore insufficient to imply movability of the limiting core. This is a statement about this metric invariant-core construction. It does not refute the existential arbitrarily-small-good-radius assertion, a co-countable or almost-every-radius assertion by some other proof, or the full invariant movable-enlargement problem. Here C itself is movable and invariant, and B=C meets every enlargement request for this particular C.

There is one harmless convention to state explicitly in the candidate's generic right-continuity observation: ordinary Hausdorff distance is defined on nonempty compact sets. For a general full flow and an unrelated compact C, invariant cores can be empty. The decreasing-intersection identity remains valid, and an empty limiting core forces eventual emptiness under the common compact bound. The usual Hausdorff statement applies to nonempty cores. All cores in this construction contain the nonempty stationary set C, so this convention has no effect on any claimed property or proof.

Audited candidate: LEFT_CONTINUITY_COUNTEREXAMPLE.md, 16,075 bytes, SHA-256:

8a57becaf77173e252c9041617dd21764ec5632674614ba840d89e0729320b26

The candidate was read in full, independently checked against the accepted exact stretched-book and regular-wall inputs, and left unchanged. This report expands delicate selection, topology, separation, and quantifier details. It contains authored mathematics and verification metadata, without imported source bodies.

## 1. The inherited compactum is exactly the required stretched book

The accepted pass-2 construction starts with a copy K of the dyadic solenoid in

T_book = ([0,1] x [-1,1] x {0}) union ([0,1] x {0} x [0,1]).

Its common binding is E=[0,1] x {0} x {0}. The explicit stretched-book quotient is identity on the bottom rectangle, maps (u,0,w) to (u,0,0), and maps the upper rectangle point (u,v,1) to (u,0,v). Thus the planar sets in its inverse image are exactly

P_0^old = {(u,v):(u,v,0) in K},
P_1^old = {(u,v):0<=v<=1 and (u,0,v) in K},
S = {(u,0):(u,0,0) in K}.

Their intersections with v=0 both equal S. The accepted direct near-homeomorphism argument proves nonmovability of

A = (P_0^old x {0}) union (P_1^old x {1}) union (S x [0,1]).

Its neighborhood domain is fixed before the later arbitrary target, so the input is ordinary movability, not a weaker condition. No general cell-like-map theorem is needed for this implication.

The binding S is nonempty: otherwise connected K would lie in one component of the book off E, hence in a planar page; planar movability and homeomorphism invariance would contradict nonmovability of K. This also makes both old planar sets nonempty.

Under L(u,v)=(u/10,1+v/10), put Q_i=L(P_i^old) and T=L(S). The ranges and intersections asserted by the candidate follow exactly. The affine ambient homeomorphism

(x,y,z) -> (10x,10(y-1),(z+2)/4)

carries

D = (Q_0 x {-2}) union (Q_1 x {2}) union (T x [-2,2])

to A. Consequently D is the accepted nonmovable compactum in the new normalization. In particular, the argument does not replace the input by an arbitrary pair of planar sets for which nonmovability has not been established.

## 2. Empty interior below the binding is justified

Only the following limited fact is needed: Q_0 has no nonempty planar open disk below y=1. Suppose a disk existed. By shrinking it, its inverse under L lies strictly away from the book binding and from the outside edges of its page. In that region the book has just its one planar page. The disk, being contained in K and open in that page, is consequently an open subset of K. This checks the otherwise important relative-openness step.

The dyadic solenoid has local charts J x Z_2, with J an open interval and Z_2 the Cantor space of 2-adic integers. One can see this directly from its inverse limit of the maps z |-> z² on the circle: above an open arc of the initial circle, choose a continuous argument, and record the compatible choices of inverse branches at all successive levels. Their discrete choices form the inverse limit of the finite sets of residues modulo 2^n, namely Z_2. The continuous argument gives the J-coordinate. Thus this local product property does not impose any additional regularity on the particular Bing embedding.

In such a chart every connected subset has singleton projection to the totally disconnected space Z_2. It lies in J x {c}, which has empty interior since Z_2 has no isolated points. An open disk in K would have a smaller connected open subdisk contained in one of these charts, an impossibility. Therefore the required planar disk cannot exist.

No property of the binding T beyond compactness and nonemptiness is inferred from this argument. In particular, neither zero dimensionality of T nor a tame or locally flat embedding of K is being assumed.

## 3. All auxiliary selections exist and have only the intended accumulation

Set b_n=2^(-n-5), and choose a finite b_n-net R_n in compact T. For each t in R_n the region

B(t,b_n) intersect {0<x<1/10, 1-b_n<y<1}

is a nonempty planar open set, even when the x-coordinate of t is an endpoint of [0,1/10]. A small horizontal move into that interval and downward move below y=1 stays in the ball. Because Q_0 is compact with empty interior in this region, its complement there contains a nonempty open set. Q_1 contributes no points below y=1. Deleting finitely many earlier choices cannot exhaust a nonempty planar open set. The choices q(n,t) therefore exist and can all be made distinct.

There are only finitely many previous choices at every finite stage: R_1,...,R_(n-1) are finite, as is the current level. Thus the recursive selection does not quietly require avoiding an uncontrolled dense countable set.

Every chosen q is outside Q_0 union Q_1 and satisfies |q-t(q)|<b_n and 1-b_n<q_y<1. Since b_1=1/64, the asserted weaker strip 9/10<q_y<1 holds. The following consequences are independent of the sizes of the finite nets.

- Q is countable, with finitely many points at each level.
- Any sequence of distinct points of Q eventually leaves every fixed finite collection of levels. Its assigned b_n tends to zero.
- Its distance to T tends to zero. Every accumulation point of Q therefore belongs to compact T.
- For each t in T choose t_n in R_n with |t_n-t|<=b_n. Then |q(n,t_n)-t|<2b_n, so these distinct points converge to t. Every t is an accumulation point.
- Consequently closure(Q)=Q union T.
- For any a<1, once b_n<1-a, all level-n choices have q_y>a. Hence only finitely many q have q_y<=a, including when a exactly equals the y-coordinate of an earlier choice.

For q in Q, compactness of Q_0 union Q_1 gives positive distance from q to those original sets. If q were not isolated among Q, a sequence of distinct other q's would converge to it, forcing q in T, a contradiction. Thus q is isolated in Q union Q_0 union Q_1. This is the stronger isolation needed later for the retraction and the compact finite-component decomposition.

If distinct q_j converge to t in T, then |q_j-t(q_j)| tends to zero and t(q_j) tends to t. Finally P_i=Q_i union Q is closed because all omitted Q-limit points are in T subset Q_i; it is bounded and therefore compact. No compactness of Q by itself is asserted or needed.

## 4. Movable stationary set and exhaustive fiber classification

The new stationary set is

C = (P_0 x {-2}) union (P_1 x {2}) union W,
W = [-1,1] x {0} x [-2,2].

Each piece is compact and planar. The sheets are separated by height 4; both are separated from W by y>=9/10. Standard planar movability therefore applies to every piece, even though the planar bases include infinitely many added isolated points.

A finite disjoint union of compact movable sets is movable with the full neighborhood quantifiers. Given an outer neighborhood, first choose pairwise disjoint smaller outer neighborhoods around the pieces. Fix each piece's movability domain there. For every later target, combine the finitely many homotopies on those disjoint domains. This establishes movability of C without an arbitrary finite-gluing assertion.

Distance to C is 1-Lipschitz. Its minimum with 1 remains 1-Lipschitz and is bounded, so the vector field generates a unique full flow for all real times. Its zero set is exactly C and the horizontal coordinates remain fixed. In a complementary interval of a vertical fiber, the scalar speed is positive. The orbit cannot approach an interior point in infinite time, because speed there is bounded below by a positive constant, and cannot reach a finite stationary endpoint in finite time by uniqueness. Its image is the whole complementary interval.

The complete stationary fiber list is:

- an interval [-2,2] over the wall projection;
- one endpoint -2 or +2 over a base in only one sheet;
- the two endpoints {-2,2} over a common sheet base;
- empty over all other bases.

The wall projection y=0 does not meet a sheet projection y>=9/10. Thus no wall-to-sheet gap is omitted. The only bounded nonstationary gaps are (-2,2) over

P_0 intersect P_1 = (Q_0 intersect Q_1) union Q.

The displayed set identity itself is a distributive identity. The additional disjointness of Q from the original bases is essential for the later separation and retraction, and is satisfied. Every other nonstationary orbit is unbounded in at least one time direction and cannot belong to a compact invariant core.

For the closed metric neighborhood N_r(C), the expression

Inv(N_r(C)) = intersection over t in R of phi(t,.)^(-1)(N_r(C))

is a closed invariant subset of compact N_r(C). The preceding classification proves that it consists of C and exactly the bounded full gaps whose closed segments remain in N_r(C). This checks both time directions, closed endpoint inclusion, and absence of partial-orbit contributions.

## 5. Exact distance threshold, including every auxiliary column

For any common base p=(x,y), one has x in [0,1/10] and 9/10<y<=11/10. At -2<=z<=2 its nearest wall point is (x,0,z), and the wall distance is y. The same base p belongs to both endpoint sheets, so the respective sheet distances are exactly 2+z and 2-z. Other sheet points cannot improve on those vertical lower bounds. In fact the stronger formula

dist((p,z),C)=min(y,2+z,2-z)=min(y,2-|z|)

holds. Because y<=11/10<2, the maximum over the gap closure is exactly y, attained at z=0. Arbitrarily close auxiliary endpoints cannot reduce this midpoint test, as they remain at heights +/-2.

It follows for every r>0 that

M_r(C) = C union ( {p in (Q_0 intersect Q_1) union Q : p_y<=r} x [-2,2] ).

The weak inequality includes all equality cases, and the formula is exhaustive by Section 4. At r=1 the original common bases selected are exactly T, whereas all q in Q are selected. Consequently

M_1(C)=W union X,
X=D union (Q x [-2,2]).

The set X is compact: sequences in a fixed auxiliary column remain in that compact column; sequences of distinct auxiliary bases can accumulate only in T, where all limiting heights are included in D. Equivalently X is the union of the original compact sheets with the compact product (Q union T) x [-2,2]. Its distance from W is at least 9/10.

## 6. The explicit retraction is globally continuous

Define R:X->D to fix D and to send (q,z) to (t(q),z) on every auxiliary column. It is unambiguous because auxiliary bases are outside Q_0 union Q_1, hence also outside T. Each auxiliary column is separated from the rest of X and carries a continuous restriction of R.

It remains to check sequences approaching D. Points already in D are fixed. A sequence in a fixed auxiliary column cannot converge to D, since that compact column is disjoint from D. A sequence from finitely many auxiliary columns has the same exclusion after passing to a subsequence. For a sequence from distinct auxiliary columns, any limiting base is t in T, and |q_j-t(q_j)| tends to zero. Thus

|R(q_j,z_j)-(q_j,z_j)|=|t(q_j)-q_j| -> 0.

Whenever (q_j,z_j) converges to (t,z), its image also converges to (t,z). This covers the entire binding, including its endpoint heights +/-2, and mixed sequences from the sheets and auxiliary columns. Sequential continuity suffices in these metric spaces, proving continuity of R everywhere.

Extend R to M_1(C) by mapping the separated compact wall W constantly to any fixed point of nonempty D. The two pieces are clopen, so the extension is continuous and is a retraction onto D.

For clarity, the candidate's movability-under-retraction proof has the right quantifiers. Let A be a retract of a movable Euclidean compactum Y, and extend its retraction coordinatewise by Tietze to f:R^m->R^m. For a fixed outer neighborhood O of A, f^(-1)(O) is a neighborhood of Y. Movability of Y supplies a fixed domain V_Y there. Choose a neighborhood V of A in V_Y and O sufficiently small that every straight segment from v to f(v) stays in O.

Such a uniform choice exists: choose delta>0 with the closed delta-neighborhood of compact A contained in O. For v sufficiently close to A, both v and f(v) lie within delta/2 of the same nearby a in A, since f fixes A and is continuous uniformly near compact A. Their segment stays in the delta-ball about a. Intersect this small neighborhood with V_Y.

For every subsequent target U of A, use movability of Y with target f^(-1)(U) intersect V_Y. Postcompose its homotopy with f and restrict to V. It starts at f|V, remains in O, and ends in U. Prepend the fixed straight-line homotopy. The neighborhood V was chosen before U. This is ordinary movability of A.

Applying the contrapositive to the retraction onto nonmovable D proves nonmovability of M_1(C). The proof does not infer nonmovability merely from containing D; it uses the verified actual retraction.

## 7. Every strictly smaller core is a finite disjoint union of movable pieces

For 0<r<1 no original common base is selected, since Q_0 intersect Q_1 lies in y>=1. The set Q(r)={q in Q:q_y<=r} is finite, and

M_r(C)=C union (Q(r) x [-2,2]).

Each q in Q(r) is isolated in each P_i. Hence deleting the finite set Q(r) from P_i leaves a relatively closed compact set. The union can therefore be written as the following finite family:

- (P_0 minus Q(r)) x {-2};
- (P_1 minus Q(r)) x {2};
- W;
- the interval {q} x [-2,2], separately for every q in Q(r).

Empty pieces can be omitted. All pieces are compact and pairwise disjoint. In particular, deleting the endpoints before adding the full columns avoids an invalid gluing argument. Compactness plus finite pairwise disjointness gives strictly positive separation between any two retained pieces. Each piece is planar or an interval and hence movable. The finite disjoint-union argument then proves movability of M_r(C), including radii exactly equal to an auxiliary threshold and radii below every threshold.

This statement is stronger than merely exhibiting a sequence of good radii. It does not claim the below-1 family is everywhere continuous: an isolated column may indeed enter at its own threshold.

## 8. Left and right Hausdorff continuity at the bad radius

Every auxiliary column appears at its threshold q_y<1. For each t in T the net construction supplies auxiliary bases q_n tending to t. At any fixed height z in [-2,2], the points (q_n,z) then approach (t,z). Hence every binding column is in the closure of the union of smaller cores. The original sheets and wall are already present in all cores. Conversely all smaller cores are contained in closed M_1(C). Therefore

closure(union over 0<r<1 of M_r(C))=M_1(C).

To obtain uniform Hausdorff convergence rather than merely pointwise approximation, fix epsilon>0. Cover compact M_1 by epsilon-balls centered at points of that union, choose a finite subcover, and choose r_0<1 large enough to include all finitely many centers in M_(r_0). For all r_0<=r<1 the centers stay in M_r by monotonicity. Every point of M_1 is within epsilon of M_r, while M_r subset M_1. Thus d_H(M_r,M_1)<=epsilon for all such r. This establishes left continuity without a rate assumption on the sizes of the finite nets.

For right continuity, invariant-set intersection commutes with intersection of the underlying sets:

intersection over s>r of Inv(N_s(C))
=Inv(intersection over s>r of N_s(C))
=Inv(N_r(C)).

This follows directly from the universal quantifier over all real orbit times. For r<s<=r+1 all sets lie in compact N_(r+1)(C). They are nonempty because they contain C. Decreasing compact sets converge in Hausdorff distance to their intersection; a direct contradiction proof chooses points a_n in M_(r+1/n) a fixed positive distance from M_r, passes to a convergent subsequence in the common compact set, and uses nestedness to put the limit in every M_(r+1/n), hence in M_r. General s decreasing to r follows by squeezing between such radii.

For an arbitrary full flow the same intersection identity is valid even if the cores are empty. If M_r were empty but there were nonempty M_s for s arbitrarily close above r, nestedness and the common compact bound would yield a nonempty intersection, a contradiction. Thus the only omitted convention in the generic wording is eventual emptiness versus the ordinary nonempty Hausdorff metric. It is irrelevant here.

Together the two one-sided arguments prove Hausdorff continuity at the nonmovable radius 1.

## 9. Ambient regularity survives all auxiliary endpoints

The new bases P_i remain in [0,1/10] x [9/10,11/10]. The regular-wall calculation uses only this strip and the exact wall, so it applies to the augmented sheets. Its global nature, including wall edges and corners, can be checked as follows.

Suppose a=(x,y,z) has rho=dist(a,C)>=3/5 and lies in the convex hull of its nearest-point set Pi(a). Since Pi(a) subset C, convex containment gives

-1<=x<=1, 0<=y<=11/10, -2<=z<=2.

Only after these bounds are known may the wall projection (x,0,z) be used. It belongs to W and is its unique nearest point. Thus 3/5<=rho<=y<=11/10. Both sheets cannot supply nearest points: their vertical separation 4 exceeds 2rho<=22/10. At least one sheet must occur with positive weight in a convex representation, since a combination of wall points alone would have y=0.

Let its height be sigma and the weight of the unique wall point be lambda, taking lambda=0 if absent. Since y>0, lambda<1. The height equation z=lambda z+(1-lambda)sigma forces z=sigma. The x-coordinate equation similarly forces x in [0,1/10]. For any point c of that nonempty sheet,

|x-c_x|<=1/10, |y-c_y|<=1/2, z=c_z.

Hence rho<=|a-c|<=sqrt(26)/10<3/5, a contradiction. The inequality 26/100<9/25 is exact. This does not assume that auxiliary points are far apart or ignore any possible nearest points.

Finally, exclusion from conv Pi(a) really excludes Clarke criticality. Strict separation yields v and alpha>0 with (a-c) dot v>=alpha for all nearest points c. Compactness of C and upper semicontinuity of nearest-point sets give (b-c_b) dot v>=alpha/2 uniformly for all nearby b and their nearest points c_b. For sufficiently small positive t,

d(b-tv)^2 <= d(b)^2-alpha t+t²|v|² <= d(b)^2-alpha t/2.

Distances are bounded above and away from zero near a. Dividing the difference of squares gives a uniform negative bound for [d(b-tv)-d(b)]/t, so the Clarke directional derivative in direction -v is negative. Zero cannot belong to the Clarke subdifferential. Thus the entire range [3/5,infinity) consists of noncritical distance values.

The already accepted regular-level implication yields a compact Lipschitz unit distance surface. At a binding midpoint (t,0), t=(t_x,1) in T, the sheet distances are at least 2 and the wall distance is 1. The wall projection is interior to the finite rectangle. This strict margin persists nearby, where distance equals the positive y-coordinate. The same holds along binding points with -1<z<1. These smooth boundary points belong to nonstationary invariant gap orbits, so the unit neighborhood remains non-isolating. Auxiliary endpoints do not disturb this margin.

## 10. Countably many left jumps do not imply movable nonjump cores

Let L_r=closure(union over s<r of M_s) for an increasing compact-valued family. If L_r is properly contained in M_r, choose a point of M_r outside L_r and a ball from a fixed countable base meeting M_r and disjoint from L_r. The same ball cannot witness another jump at t>r, because its point in M_r belongs to the union defining L_t. Selecting the first eligible base ball at each jump therefore gives an injection from jump radii into a countable set.

This argument is sound. Right continuity is sound with the compactness and nonemptiness convention above. The missing step in the proposed sufficient-condition route is precisely a claim that equality L_r=M_r forces movability, even assuming movability at every smaller radius. The present example disproves that step while also preserving ambient regularity.

A single bad nonjump radius does not logically refute the possible existence of other arguments proving that co-countably many radii are good. Nor does it produce a bad interval or failure of arbitrarily small good radii for one fixed stationary C. These boundaries are correctly maintained in the candidate.

## Inputs, established dependencies, and verification limits

The following authored inputs were read in full and hash-checked:

- LEFT_CONTINUITY_COUNTEREXAMPLE.md: 16,075 bytes; SHA-256 8a57becaf77173e252c9041617dd21764ec5632674614ba840d89e0729320b26.
- VERTICAL_GAP_COUNTEREXAMPLE.md: 11,970 bytes; SHA-256 85ab6a5e1b948ebc8f83f6506cb04a1d9e8fa644826261fcc40247567b695403.
- VERTICAL_GAP_ACCEPTANCE.md: 14,943 bytes; SHA-256 ef81f2296048ec77a5b8175bb838cd66c6cb6b5d61482f210e14ec04df26d1c8.
- REGULAR_RADIUS_COUNTEREXAMPLE.md: 11,447 bytes; SHA-256 9b906d10aa3b4789619065ff345eda4def4389ba4a5040c57f51c0c465c54389.
- REGULAR_RADIUS_ACCEPTANCE.md: 18,394 bytes; SHA-256 1d2f48c5aba5308dd973ee29353dc6618128aeb87e1d49fa99834b146bed5c01.
- METRIC_THRESHOLD_ACCEPTANCE.md: 15,036 bytes; SHA-256 c87b99b39c647e11305879754374410d73ba0b69c8678414fdde0e3026fa9539.

Inherited public primary references, used with the inspection and hypothesis scope established by the accepted earlier audits:

- R. H. Bing, *Embedding Circle-Like Continua in the Plane*, Canadian Journal of Mathematics 14 (1962), 113-128, Theorem 8. https://doi.org/10.4153/CJM-1962-009-3 . Supplies the actual solenoid-in-a-book embedding.
- K. Borsuk, *On movable compacta*, Fundamenta Mathematicae 66 (1969/1970), 137-146, the solenoid example, Corollary 3.11 and Corollary 5.5. https://doi.org/10.4064/fm-66-1-137-146 . Supplies the established nonmovability and embedding/shape-invariance framework and planar movability.
- J. Rataj and L. Zajicek, *Critical values and level sets of distance functions in Riemannian, Alexandrov and Minkowski spaces*, arXiv:0911.4020v1, Definition 2.4, Lemma 2.5 and Proposition 2.13(i). https://arxiv.org/pdf/0911.4020 . Supplies the already accepted regular-level implication.

The solenoid local product description was additionally checked by the elementary inverse-limit chart argument above. Tietze extension is used only coordinatewise on a closed Euclidean compactum. The retract implication is proved with explicit neighborhood homotopies, not imported as an unexamined stronger theorem.

No new source retrieval or literature search was performed. The earlier audits' primary-source inspections are inherited and are not represented as fresh page inspections in this audit. All universal construction claims were checked by exact arguments, not numerical sampling. The accompanying manifest records actual input/output hashes and source-PDF identities; source PDFs are inherited dependencies, not audit output or publishable source text.

The frozen candidate and inherited authored inputs remain unchanged. No remote mutation, external communication, source-body publication, unrelated proof repair, or sixth substantive search pass occurred. The full row-1767 invariant movable-enlargement problem remains unresolved.
