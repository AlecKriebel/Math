# Turn 2: exact template linear programs and an obstruction to same-support reversal

Substantive author turn **2/5**. The natural strategy of reversing a graph and adjusting its positive vertex weights on the same retained incidence pattern does **not** suffice. We give a family where the best forward template value is1/2 and the best reverse template value is2y>1/2, even though the two universal values ψ are both1/2. This is a proof-route obstruction, **not a counterexample to the original symmetry question**.

The turn also organizes the weighted problem into three independent feasibility polytopes and two different objective linear programs. The global problem compares their lower envelopes over all incidence patterns, not their values on each individual pattern.

## 1. The exact linear programs for a retained pattern

Fix finite labeled nonempty parts A,B,C and binary incidence matrices P (A by B) and Q (B by C). Let R be the Boolean product matrix, with R_ac=1 exactly when some b has P_ab Q_bc=1. Let p,b,q be the weight vectors on A,B,C, each nonnegative with sum1. The four biconstraints are exactly

 P b>=x1_A,          P^T p>=x1_B,
 Q q>=y1_B,          Q^T b>=y1_C.                               (1)

Thus feasibility separates into the three polytopes

 A_x={p in Δ_A:P^T p>=x1_B},
 B_(x,y)={b in Δ_B:P b>=x1_A, Q^T b>=y1_C},
 C_y={q in Δ_C:Q q>=y1_B}.                                     (2)

The forward reach maximum is max(R^T p), depending only on p; the reverse reach maximum is max(R q), depending only on q. On this fixed retained pattern define the closed-program values

 f_(P,Q)(x)=min_(p in A_x) max(R^T p),
 g_(P,Q)(y)=min_(q in C_y) max(R q).                              (3)

When all three polytopes are nonempty these are ordinary finite linear programs, using an extra scalar objective bound. Their minima exist by compactness. The joint feasibility of b is not silently omitted; it is needed to turn either objective into an admissible tripartite weighting.

For the relation to graphs with every retained type present, assume that each of the three polytopes has a point all of whose coordinates are **strictly positive**. Then the infimum of the forward value over positive admissible weights is exactly f, and similarly for g. Indeed mix an optimizer with a fixed positive feasible point in that same polytope. The mixtures remain feasible and positive, and their objective values converge to the closed-program optimum. The other two weight vectors can stay at their fixed positive feasible values.

If x,y are rational, the polytopes have rational coefficients. Positive feasible points can be chosen rational, and an optimum can be chosen at a rational vertex of the compact linear-program polytope (a full-rank set of active rational equations gives rational coordinates). Taking rational mixing coefficients gives positive rational near-optima. Their common-denominator blow-ups are actual finite simple graphs with exactly the specified nonempty types and exactly the same weighted reach fractions: every positive middle type receives at least one copy, so Boolean reachability is preserved.

Consequently, at rational x,y, ψ(x,y) is the infimum of f_(P,Q)(x) over all finite patterns for which (2) has positive feasible points; ψ(y,x) is the infimum of g_(P,Q)(y) over the **same** eligible patterns. One direction follows by viewing every finite graph with its uniform part weights. The other follows from the positive rational near-optima and exact blow-ups above. We do not identify a zero-weight middle vertex with a positive type: deleting it can remove paths and change which degree inequalities are required.

This lower-envelope formulation is an organization of the credited weighted/linear-programming framework, with its positive-support and nonattainment details supplied. It is not an equality between f and g for every template.

## 2. Simple dual certificates, with their directions checked

Let u be a probability vector on C, v a nonnegative vector on B, and λ a real number such that

                         R u−P v>=λ1_A.                         (4)

Then every p in A_x satisfies

 max(R^T p)>=p^T R u>=p^T P v+λ>=x sum(v)+λ.                     (5)

This is a directly verified lower certificate for f. Dually, for a probability vector u on A, nonnegative v on B and

                       R^T u−Q^T v>=λ1_C,                       (6)

every q in C_y has max(R q)>=y sum(v)+λ. Finite linear-program duality identifies these as the usual dual problems, but only the displayed elementary inequalities are needed for the certificates below. Matching feasible weights prove optimality without relying on a numerical solver.

## 3. A family with different optimal values on the same retained pattern

Let x=1/2 and **1/4<y<=1/3**. Take

 A={a1,a2}, B={b0,b1,b2,b3}, C={c1,c2,c3},

 P = [1 1 1 0]        Q = [1 1 0]
     [0 0 0 1]            [1 0 0]
                           [0 1 0]
                           [0 0 1].

Its Boolean product is

                         R = [1 1 0]
                             [0 0 1].                            (7)

A strictly positive feasible weighting is

 p=(1/2,1/2),
 b=(1/4,1/8,1/8,1/2),
 q=(y,y,1−2y).                                                   (8)

Indeed P b=(1/2,1/2), every coordinate of P^T p is1/2, Q q=(2y,y,y,1−2y)>=y1, and Q^T b=(3/8,3/8,1/2)>=y1. Positivity is valid throughout the stated interval.

Every feasible p must be(1/2,1/2), since the retained middle vertices demand at least1/2 from each of the two disjoint A types. Thus all three coordinates of R^T p equal1/2, proving

                           f_(P,Q)(1/2)=1/2.                    (9)

For an explicit dual certificate take u supported on c1 and v supported on b1. Then R u=P v=(1,0)^T and λ=0 in(4), yielding the same bound1/2.

Every feasible q must satisfy q(c1)>=y and q(c2)>=y, since b1 has only neighbor c1 and b2 only neighbor c2. Therefore its reverse reach from a1 is at least2y. The weights in(8) attain max(2y,1−2y)=2y. Hence

                             g_(P,Q)(y)=2y.                      (10)

The reverse dual certificate in(6) is u concentrated on a1 and v=(0,1,1,0) on B. Both R^T u and Q^T v equal(1,1,0)^T; λ=0 gives the lower bound2y. This proves the obstruction for **every** positive reweighting on this retained pattern, not just the sample weights(8).

For any common target bound z with1/2<=z<2y, forward weights meeting that bound exist, while reverse weights on the same positive support do not. The two extra minimum-degree conditions therefore cannot be preserved by blindly extending the source's one-direction reweighting argument on a fixed support.

## 4. An explicit ordinary graph, and why it is not a symmetry counterexample

At y=3/10 use common denominator40 in(8). Replace the types by twin classes of sizes

 A:(20,20),  B:(10,5,5,20),  C:(12,12,16),

and make the complete or empty bipartite pairs indicated by P,Q. This is a finite simple graph of order120, with40 vertices in each part. Its A–B degrees are all20 in either direction. Its B→C degrees by type are24,12,12,16; C→B degrees are15,15,20. It is therefore(1/2,3/10)-biconstrained. Every C vertex reaches20 A vertices, while the two A types reach24 and16 C vertices respectively. Its forward value is1/2 and its reversed value is3/5. The same-support lower certificates prove that positive reweighting cannot lower the reverse optimum below3/5.

Nevertheless

                    ψ(1/2,y)=ψ(y,1/2)=1/2                      (11)

for every0<y<=1/2. The lower bound max(x,y) is already credited in the primary paper; for this family it gives1/2. Two disjoint three-vertex paths, with one vertex in each part per component, give the matching upper bound for both parameter orders. Thus (11) is a known minimal-value regime, not a newly discovered asymmetric pair.

There is also an explicit way to leave the obstructed support. Delete b1 and b2, give b0 and b3 weight1/2 each, keep p=(1/2,1/2), and set q=(1/4,1/4,1/2). The remaining graph is feasible for the whole interval1/4<y<=1/3, and both reach maxima are1/2. The two C types c1,c2 can then be merged. The removed degree constraints q(c1)>=y and q(c2)>=y are precisely what obstructed the previous fixed support. This illustrates why vertex deletion or a different incidence pattern is a substantive operation in the global lower envelope.

## 5. Scope and next gap

The exact LP formulation provides finite rational certificates for a specified pattern, and the family(7) proves that template-by-template reversal optimality is false. It does not disprove equality of the lower envelopes defining ψ. The120-vertex graph is emphatically not an original-question counterexample, since(11) evaluates both universal values equally.

The remaining question is whether a change of support/incidence can always compensate for such a template discrepancy, or whether one can prove a universal reversed lower bound above a particular forward construction. Turn1's finite certificate requires that global distinction; a single-template dual lower bound cannot be substituted for it. Original unresolved2/5.
