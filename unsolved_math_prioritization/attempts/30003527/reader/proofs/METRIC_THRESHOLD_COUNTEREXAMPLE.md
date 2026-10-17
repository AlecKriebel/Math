# Metric gap filling can create nonmovability

Problem 30003527 / OWR-15575-006, queue row 1767. Authored 13 October 2026 within shared substantive pass 3. This is a counterexample to a proposed construction lemma, not to the invariant-enlargement question.

## Results

For a nonempty compact C in R³ let φ_C be the full flow of

F_C(p,z)=min(1,dist((p,z),C))e₃,

and let M_r(C)=Inv_φC({x:dist(x,C)≤r}).

1. For every prescribed r>0 there is a **movable** compact stationary set C for which **M_r(C) is nonmovable**. The set C is a disjoint union of two compact planar graphs. At exactly radius r, metric filling joins them into a compactum homeomorphic to the accepted stretched-book solenoid example from pass 2.
2. There is one movable compact stationary set C_∞ and a sequence r_n↓0 for which every M_(r_n)(C_∞) is nonmovable. Thus the proposed assertion that every sufficiently small metric fill is movable is false, even for an initially movable set.
3. For the original stretched-book compactum A, the exact maximum distance of a unit-gap segment from A is min(1/2,dist(p,S)), where S is its planar binding set. This verifies the suggested metric formula. It does not establish movability of any small M_r(A).

These results leave open whether every compact C has arbitrarily small *some* good radii, or admits suitable invariant movable enlargements chosen by another rule. In both counterexamples here, C itself is movable and stationary, so B=C already satisfies the original enlargement request for every neighborhood. No all-enlargements counterexample is claimed.

## 1. The accepted topological input in planar-base form

Take the compact nonmovable stretched-book set from pass 2. It can be written

A=(P₀×{0}) ∪ (P₁×{1}) ∪ (S×[0,1]),

where P₀,P₁ are compact subsets of R² and S is a nonempty compact subset of their intersection. More precisely, start with a dyadic solenoid K in

T=([0,1]×[-1,1]×{0}) ∪ ([0,1]×{0}×[0,1]).

Define

P₀={(x,y):(x,y,0)∈K},
P₁={(x,y):y≥0 and (x,0,y)∈K},
S={(x,0):(x,0,0)∈K}.

The passage from K to A replaces each point of K on the common binding by a full vertical interval. The direct near-homeomorphism argument in pass 2 proves that A is nonmovable. It avoids any need for a general cell-like-map theorem. The independent pass-2 acceptance checked the embedding input, the explicit maps, and the full neighborhood-homotopy quantifiers.

The required S is nonempty. If K avoided the binding, its connectedness would place it in one component of T minus the binding, hence in a single planar page. It would then be movable, contradicting solenoid nonmovability.

The imported primary inputs are Bing's embedding theorem and Borsuk's planar movability and shape invariance. The new construction below needs only the resulting displayed A and those elementary invariances.

## 2. General vertical-flow facts

The vector field F_C is bounded and globally Lipschitz, so its ODE has a unique continuous full flow. It fixes precisely C. Horizontal coordinates are constant. Every nonstationary orbit is an entire open component of R minus the fiber C_p: velocity is positive there, cannot have an interior limiting point with positive velocity, and cannot reach a finite zero in finite time by uniqueness.

Consequently a compact invariant set containing C can add points only by adding whole bounded fiber gaps. A closed union of such gaps and C is invariant. The maximal invariant set M_r(C) is exactly C plus those bounded gaps whose entire closed segments have distance at most r from C. This follows because an unbounded orbit cannot fit in the compact r-neighborhood of C, and a bounded orbit fits precisely when its closure does.

M_r(C) is compact: it is the intersection, inside the compact r-neighborhood of C, of its inverse images under all time maps. It is invariant by the group law. It contains C and lies in every prescribed neighborhood of C for sufficiently small r.

These properties alone say nothing about movability.

## 3. A bad metric radius for a movable stationary set

Fix r>0 and put

g(p)=r+dist(p,S), p∈R².

Only the facts that g is continuous, g≥r, and g=r exactly on S will be needed. Define

C⁻={(p,-g(p)):p∈P₀},
C⁺={(p, g(p)):p∈P₁},
C=C⁻∪C⁺.

These are compact graphs. Projection identifies each graph homeomorphically with its planar base, so both are movable. They lie respectively in z≤-r and z≥r, and are disjoint. Their union is movable: apply movability separately inside disjoint neighborhoods and combine the homotopies on their disjoint domains. This is a valid finite-disjoint-union argument, not the false arbitrary-gluing principle.

A fiber of C is empty, a singleton, or the two points {-g(p),g(p)}. Thus a bounded gap exists exactly when p∈P₀∩P₁, and then it is (-g(p),g(p)).

If p∈S, its endpoints are ±r. Every point of its closed gap is within r of one endpoint. Hence the entire gap is included in M_r(C).

If p∉S, consider its midpoint (p,0). For every q in either planar base, the squared distance to the corresponding point of C is

|p-q|²+g(q)² ≥ r².

Equality is possible only if q=p and g(q)=r, which would give p∈S. Since C is compact, the minimum is attained. Therefore

dist((p,0),C)>r whenever p∉S.

Thus no bounded gap with base outside S can be included. The orbit classification gives the exact identity

M_r(C)=C ∪ (S×[-r,r]).

Define the ambient homeomorphism

H(p,z)=(p,(z+g(p))/(2g(p))).

Its continuous inverse is H⁻¹(p,t)=(p,2g(p)t-g(p)); the denominator is nonzero because g≥r>0. This homeomorphism takes C⁻ to P₀×{0}, C⁺ to P₁×{1}, and each column over S onto S×[0,1]. Therefore

H(M_r(C))=A.

By homeomorphism invariance M_r(C) is nonmovable, proving Result 1.

For 0<s<r every bounded gap still has a midpoint at distance at least r, so M_s(C)=C. This single-copy example has good radii below the bad one. It specifically shows that increasing the permitted metric radius need not preserve movability.

## 4. One movable stationary set with arbitrarily small bad radii

Use the preceding construction with r=1 and call its stationary set C₀. With the displayed coordinate normalization of P₀,P₁,S, both C₀ and its full vertical hull lie in the closed Euclidean ball of radius 4 about the origin: the horizontal norm is at most √2, the distance to S is at most √2, and |z|≤1+√2.

For n≥1 let

c_n=(2⁻ⁿ,0,0), a_n=2⁻⁴ⁿ⁻¹⁰,
C_n=c_n+a_n C₀, r_n=a_n,
C_∞={0} ∪ ⋃_(n≥1) C_n.

The sets C_n shrink and converge to 0, so C_∞ is compact. Their horizontal projections lie in disks centered at (2⁻ⁿ,0) of radius 4a_n. These disks are pairwise disjoint and avoid 0. Hence a vertical fiber meets at most one C_n, unless it is the fiber of the isolated point 0; the latter has no bounded gap. Every possible bounded orbit of φ_(C∞) belongs to the vertical hull of one C_n.

### 4.1. Other copies do not affect the decisive distance threshold

Write V_n for the full vertical hull of C_n. It lies in the closed ball of radius 4a_n about c_n. If m≠n and k=min(m,n), then

|c_m-c_n|≥2⁻ᵏ⁻¹,
4a_m+4a_n≤8a_k.

Since a_k=2⁻⁴ᵏ⁻¹⁰≤2⁻ᵏ⁻¹³, it follows that

dist(V_n,C_m)≥2⁻ᵏ⁻¹-8a_k > a_k ≥ a_n.

Also dist(V_n,{0})≥2⁻ⁿ-4a_n>a_n. These lower bounds remain positive uniformly in m for each fixed n: the case m>n has the same lower bound with k=n, and only finitely many m<n remain. Thus

dist(V_n,C_∞ minus C_n)>a_n.

Every point of V_n is consequently within distance a_n of C_∞ if and only if it is within distance a_n of C_n. The full-gap selection at radius a_n inside this block is exactly the selection for the isolated scaled copy. Hence

M_(a_n)(C_∞) ∩ V_n
  = c_n+a_n M₁(C₀).

The right-hand compactum is nonmovable by Section 3. It is clopen in M_(a_n)(C_∞): an open vertical cylinder over a slightly enlarged projection disk isolates V_n from every other possible bounded orbit and from 0.

A clopen subcompactum of a movable compactum is movable. Indeed, separate it from its compact complement by disjoint open sets, impose that separation in the outer neighborhood in the movability definition, and restrict the resulting homotopies to a neighborhood of the chosen part. A trajectory of each homotopy starting in one of those open sets cannot switch to the other. Therefore M_(a_n)(C_∞) cannot be movable.

### 4.2. The original C_∞ is movable

This point is proved explicitly rather than inferred from a countable-union theorem. Fix an open O⊃C_∞. Choose a small round ball about 0 contained in O whose boundary falls between two consecutive clusters. Increasing the finite index if necessary gives a radius t and an index N for which

⋃_(n≥N) C_n ⊂ B(0,t),
cl B(0,t)⊂O,
cl B(0,t) is disjoint from ⋃_(n<N) C_n.

The explicit geometric spacing above supplies such radii tending to zero. Choose mutually disjoint neighborhoods O_n of the finitely many C_n, n<N, inside O and outside cl B(0,t). Since each C_n is movable, choose its movability neighborhood V_n⊂O_n. Put

V=B(0,t) ∪ ⋃_(n<N) V_n.

This is a neighborhood of C_∞ fixed independently of any subsequent target W⊃C_∞. On B(0,t), contract linearly to 0, which belongs to W; the contraction remains in O. On each V_n, use its movability homotopy inside O_n with target W∩O_n. The domains are disjoint, so these homotopies combine continuously to move V inside O into W. This proves movability of C_∞.

The flow of F_(C∞) fixes C_∞ pointwise, while the radii a_n tend to zero and all their maximal metric invariant parts are nonmovable. Result 2 follows.

## 5. Exact metric formula for the original stretched book

Return to A=(P₀×{0})∪(P₁×{1})∪(S×[0,1]). For p∈P₀∩P₁ and z∈[0,1], the distance to its bottom piece is exactly z, to its top piece exactly 1-z, and to its binding columns exactly dist(p,S). The equality for the bottom and top follows because the point with the same base p is present. Thus

dist((p,z),A)=min(z,1-z,dist(p,S)).

Taking the maximum over z gives

max_(0≤z≤1) dist((p,z),A)=min(1/2,dist(p,S)).

For 0<r<1/2 the resulting exact metric-fill formula is

M_r(A)=A ∪ ((P₀∩P₁∩N_r^(2)(S))×[0,1]),

where N_r^(2)(S) is the closed planar r-neighborhood. At r≥1/2 all remaining unit gaps fill. These identities are purely geometric. Neither the good nor the bad behavior of the new stationary set C in Section 3 proves movability or nonmovability of small M_r(A) in this original example.

## 6. Consequence for the full target

There remains a meaningful candidate statement: for every compact C and every η>0, there is *some* 0<r<η for which M_r(C) is movable. If true, it would settle the requested enlargement property for vertical-slowing flows. The constructions above neither prove nor refute that existential-radius statement. They show why one cannot use arbitrary radius, eventual uniform small-radius movability, or a monotonicity claim in its place.

The full problem ranges over all continuous full flows in R³, beyond this special class. It still needs either a general invariant movable enlargement construction or a specific flow, compact invariant A, and neighborhood U excluding every such enlargement. This report supplies neither. Equality B=A remains allowed, and for the constructed C and C_∞ it resolves their own enlargement requests immediately.

## Source and verification scope

- R. H. Bing, *Embedding Circle-Like Continua in the Plane*, Canadian Journal of Mathematics 14 (1962), 113–128, Theorem 8, printed pp.121–122. Primary theorem and its fin construction were directly read in the publisher PDF during this pass: https://doi.org/10.4153/CJM-1962-009-3 .
- K. Borsuk, *On movable compacta*, Fundamenta Mathematicae 66 (1969/1970), 137–146. Corollary (5.5), printed p.145, gives planar movability; Corollary (3.11) gives shape invariance. The relevant local primary-page image was inspected, and the pass-2 independent audit checked these exact statements: https://doi.org/10.4064/fm-66-1-137-146 .
- The authored stretched-book construction and direct transfer proof are in the pass-2 VERTICAL_GAP_COUNTEREXAMPLE.md, independently accepted in VERTICAL_GAP_ACCEPTANCE.md. Their original mathematical and source scope is preserved.

The threshold deformation, exact midpoint test, scaled-copy argument, explicit movability homotopies, and metric equality above are authored here. They require independent audit before being labeled accepted. No new broad cell-like-map or finite-gluing theorem is invoked. No remote mutations or external outreach were performed, and no copied source text is included.
