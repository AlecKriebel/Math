# A regular distance radius can have a nonmovable vertical invariant core

Problem 30003527 / queue row 1767. Authored 13 October 2026 within shared substantive pass 4. This is a counterexample to another proposed construction lemma, not to the full invariant-enlargement question or to the existential good-radius assertion.

## Result

There is a compact movable stationary set C for the bounded globally Lipschitz field

F_C(x,y,z)=min(1,dist((x,y,z),C))e_3

such that:

1. M_1(C)=Inv({dist(.,C)≤1}) is nonmovable.
2. The value 1 is a regular value of the ambient distance function, in the Clarke sense. In particular, its distance sphere is a compact Lipschitz surface, and is the boundary of the closed unit neighborhood.
3. In fact, the distance function has no critical value in [3/5,∞).
4. For every 0<r<1, M_r(C)=C, so these smaller radii are good. The construction does not refute the existence of arbitrarily small good radii.

The bad radius in the pass-3 two-sheet example arose from antipodal nearest endpoints and hence was an ambient distance-critical value. The present construction uses a separate stationary wall to set the gap threshold. The wall makes that threshold an ambient regular value, while the invariant core still acquires the same nonmovable stretched book.

## 1. Accepted topological input and normalization

Use the nonmovable stretched-book compactum from the accepted pass-2 construction:

A=(P_0×{0})∪(P_1×{1})∪(S×[0,1]).

Here, in planar coordinates (u,v),

P_0⊂[0,1]×[-1,1],
P_1⊂[0,1]×[0,1],
S⊂[0,1]×{0},
P_0∩([0,1]×{0})=P_1∩([0,1]×{0})=S.

Thus P_0∩P_1 lies in v≥0, and its intersection with v=0 is exactly S. Both P_i and S are nonempty. Indeed, omission of either page, or of the common binding, would put the connected solenoid used in that construction inside one planar part, contrary to its nonmovability.

The input was obtained by embedding a dyadic solenoid in a three-page book and stretching its common edge into intervals. Its nonmovability has an accepted direct neighborhood-homotopy proof using explicit near-homeomorphisms. No new cell-like transfer or finite-gluing theorem is assumed here.

The imported established results are Bing's circle-like embedding theorem and Borsuk's planar movability and shape invariance. The present argument uses the resulting A and the fact that every planar compactum is movable.

## 2. The stationary set

Let ε=1/10 and define the planar affine map

L(u,v)=(εu,1+εv).

Put Q_i=L(P_i), T=L(S), and set

C_- = Q_0×{-2},
C_+ = Q_1×{2},
W = [-1,1]×{0}×[-2,2],
C = C_-∪C_+∪W.

The ranges are

Q_0⊂[0,1/10]×[9/10,11/10],
Q_1⊂[0,1/10]×[1,11/10],
T⊂[0,1/10]×{1}.

The three pieces are pairwise disjoint compacta. Each is planar, so movable. A finite disjoint union of movable compacta is movable: for a prescribed outer neighborhood, choose pairwise disjoint smaller outer neighborhoods of the pieces, use their movability separately, and combine the resulting homotopies on disjoint domains. Therefore C is movable.

The field F_C is globally Lipschitz and bounded, hence has a unique continuous full flow. Its stationary set is precisely C. As in the accepted vertical-flow classification, every nonstationary orbit is a full open complementary interval of a vertical fiber. Compact invariant supersets of C can therefore add only whole bounded fiber gaps. The maximal invariant part of a metric neighborhood selects exactly the gaps whose full closures are in that neighborhood.

## 3. Exact invariant core at radius 1

The horizontal projections of W and of C_-∪C_+ are disjoint: the former has y=0, while the latter has y≥9/10. Fibers above the wall projection are already the full interval [-2,2]. Fibers above Q_0∪Q_1 contain either one endpoint or both endpoints -2,+2. Thus every bounded gap of C has the form

{(x,y)}×(-2,2), with (x,y)∈Q_0∩Q_1.

For a point on such a closed segment, its x-coordinate is in [0,1/10] and z-coordinate in [-2,2]. Consequently its distance to W is exactly y.

Every common base has y≥1. If y=1, the entire closed gap is within distance 1 of W and hence of C. It is therefore selected by M_1(C).

If y>1, examine the midpoint (x,y,0). Its distance to W is y>1, and its distance to either horizontal sheet C_- or C_+ is at least 2. Hence its distance to C is greater than 1. The gap is not selected.

Since (Q_0∩Q_1)∩{y=1}=T, this proves the exact identity

M_1(C)=W∪D,

where

D=(Q_0×{-2})∪(Q_1×{2})∪(T×[-2,2]).

The affine ambient homeomorphism

(x,y,z)↦(10x,10(y-1),(z+2)/4)

takes D to the accepted nonmovable A. Therefore D is nonmovable. It is a clopen subcompactum of M_1(C), since D lies in y≥9/10 and W lies in y=0.

A clopen subcompactum of a movable compactum is movable: separate it and its compact complement by disjoint outer neighborhoods, apply movability in their union, and restrict to the chosen component of the homotopy domain. A path starting in one of the separated outer neighborhoods cannot switch to the other. Thus M_1(C) is nonmovable.

The same midpoint test shows that no gap is selected at any radius 0<r<1. Therefore M_r(C)=C for all those r.

## 4. No ambient distance-critical values at or above 3/5

Write d=dist(.,C), and for a point a outside C let Π(a) be its nonempty compact set of nearest points in C. We first establish that

no a with d(a)≥3/5 belongs to conv Π(a).

Suppose otherwise, and write a=(x,y,z) and ρ=d(a). Since a∈conv C, the coordinate ranges of C give

-1≤x≤1, 0≤y≤11/10, -2≤z≤2.

The orthogonal projection (x,0,z) belongs to W. Therefore dist(a,W)=y, and

ρ≤y≤11/10.

In particular, ρ≤11/10<2. The two horizontal sheets cannot both contain nearest points: if c_-∈C_- and c_+∈C_+ were both nearest, their vertical separation would imply

4≤|c_--c_+|≤|c_--a|+|a-c_+|=2ρ≤22/10,

which is impossible.

At least one sheet must contain a nearest point, since a convex combination of points of W alone would have y=0, contradicting y≥ρ≥3/5. Thus Π(a) uses exactly one sheet, at a height σ∈{-2,2}, possibly together with a nearest point of W.

If W has a nearest point, it is uniquely (x,0,z). In a convex combination representing a using Π(a), let λ be the total coefficient on that wall point; set λ=0 if it is absent. We have λ<1 because y>0. All remaining points have height σ, so

z=λz+(1-λ)σ,

which forces z=σ. Likewise, the x-coordinates of all sheet points lie in [0,1/10], and

x=λx+(1-λ)x_* for some x_*∈[0,1/10]

forces x∈[0,1/10].

Now choose any point c in this nonempty sheet. Its x-coordinate is in [0,1/10], its y-coordinate is in [9/10,11/10], and its z-coordinate equals z=σ. Since

3/5≤ρ≤y≤11/10,

we get

|x-c_x|≤1/10,
|y-c_y|≤1/2,
|z-c_z|=0.

Consequently

ρ=d(a)≤|a-c|≤sqrt((1/10)^2+(1/2)^2)=sqrt(26)/10<3/5,

a contradiction. This proves the claim for every ρ≥3/5.

### Why this is Clarke regularity

For completeness, only the following standard implication is needed, and it has an elementary proof:

if a∉conv Π(a), then 0∉∂^C d(a).

Strict separation supplies a vector v and a constant α>0 such that (a-c)·v≥α for every c∈Π(a). By compactness of C and continuity of distance, nearest points to points b approaching a approach the set Π(a). Hence, after restricting b to a small neighborhood of a, every nearest point c_b satisfies (b-c_b)·v≥α/2. For all sufficiently small t>0,

d(b-tv)^2≤|b-tv-c_b|^2
           ≤d(b)^2-αt+t^2|v|^2.

Take t small enough that the last term is at most αt/2. Distances near a are bounded above and away from zero; dividing the difference of squares then gives a fixed negative upper bound for

[d(b-tv)-d(b)]/t.

Thus the Clarke directional derivative of d at a in direction -v is strictly negative. By the definition of the Clarke subdifferential, zero cannot belong to it.

The geometric contradiction above therefore establishes that d has no Clarke critical points at any distance at least 3/5. In particular, radius 1 lies inside an entire interval of regular ambient distance values.

## 5. Regular distance sphere, but a non-isolating neighborhood

The regular-point Lipschitz implicit function theorem implies that {d=1} is locally a Lipschitz graph at every point. It is compact because C is compact. The local strict monotonicity also shows that every point of {d=1} is a boundary point of {d≤1}; thus {d=1}=∂{d≤1}.

A primary reference inspected for this implication is Rataj and Zajíček, Proposition 2.13(i), PDF pp.5–6. Their Definition 2.4 and Lemma 2.5 specify the same Clarke regularity convention. No assertion that merely being differentiable suffices is used.

This does not make the unit neighborhood isolating. For each (x,1)∈T and -1<z<1, the unique nearest point in C is (x,0,z) on the wall, and d(x,1,z)=1. In a neighborhood of each such point, d is simply the y-coordinate; the distance sphere is a smooth planar patch there. Nevertheless these points lie on one of the full bounded vertical orbits adjoined to M_1(C).

Thus the invariant core meets the boundary along nonstationary orbit segments even where that boundary is smooth. The regularity of the ambient distance sphere does not supply the dynamical entry/exit condition of an isolating block.

## 6. Scope and remaining question

The construction disproves each of the following sufficient conditions for this metric-core proposal:

- an ambient regular distance value;
- a compact Lipschitz distance sphere;
- avoiding all ambient distance-critical values in a neighborhood of the chosen radius.

It does not disprove an assertion that almost every radius is good, and it does not disprove the assertion that some arbitrarily small radius is good. Here every radius below 1 is good and C itself is an allowed invariant movable enlargement. Scaling the entire construction puts a bad regular radius at any prescribed positive size, but changing C with that scale is not a counterexample to the existential good-radius statement for one fixed C.

The full all-flow invariant-enlargement target likewise remains unresolved. A useful positive argument must do more than replace a wild neighborhood boundary with a regular metric distance sphere.

## Sources and verification scope

- R. H. Bing, *Embedding Circle-Like Continua in the Plane*, Canadian Journal of Mathematics 14 (1962), 113–128, Theorem 8. https://doi.org/10.4153/CJM-1962-009-3 . Used only through the accepted pass-2 stretched-book construction.
- K. Borsuk, *On movable compacta*, Fundamenta Mathematicae 66 (1969/1970), 137–146, planar movability and shape invariance. https://doi.org/10.4064/fm-66-1-137-146 . Used with the scope already checked by the pass-2 acceptance.
- J. Rataj and L. Zajíček, *Critical values and level sets of distance functions in Riemannian, Alexandrov and Minkowski spaces*, arXiv:0911.4020v1. Definition 2.4, Lemma 2.5 and Proposition 2.13(i) were read in the primary PDF: https://arxiv.org/pdf/0911.4020 . Theorems 3.4 and 4.2 also explain the almost-every-radius result in dimensions 2 and 3, but that measure-theoretic theorem is not needed for this counterexample.

The affine-wall construction, exact metric-core computation, quantitative critical-value exclusion, and elementary regularity implication above are authored here and require independent audit. No remote mutation or source-body publication was performed.
