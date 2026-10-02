# Turn 4: all three-coordinate marginals, and the sharp small-side lattice threshold

2026-10-02. Fourth substantive author turn for 30003338. **Original target unresolved, 4/5.** This turn proves association for any three observed coordinates in an arbitrary bipartite graph, and a stronger lattice theorem when the entire observed side has size at most three. These scopes differ and neither settles arbitrary increasing events on four or more coordinates. No historical novelty is claimed.

## 1. A Boolean three-variable lemma

Let X=(X_1,X_2,X_3) be an arbitrary {0,1}³-valued vector, with no assumption of equal marginals. Suppose

    Cov(X_i, 1_E(X)) ≥ 0                                     (1)

for each coordinate i and every increasing event E. Then X is positively associated.

Here is a complete event proof. Increasing real functions reduce to positive combinations of increasing-event indicators, so it suffices to compare upward events. Nested events are positively correlated under every probability measure. Empty and full events are also trivial.

Call a nonempty event forced if it implies X_i=1 for some i. Apart from constants, the forced events on three coordinates are:

- a singleton-coordinate event X_i=1;
- a two-coordinate conjunction X_i=X_j=1;
- the three-coordinate conjunction;
- a fork F_i={X_i=1 and (X_j=1 or X_k=1)}.

A singleton event is covered by (1), and the three-coordinate conjunction is contained in every nonempty upward event. Let F be a two-coordinate conjunction and k the missing coordinate. If F is not contained in another upward event E, then E must imply X_k=1: otherwise E would contain the maximal state with X_k=0 and hence contain all of F. If E is nonempty, F∩E is the all-one state. By (1),

    P(F∩E)=P(F∩{X_k=1}) ≥P(F)P(X_k=1) ≥P(F)P(E).

Thus every two-coordinate conjunction is positively correlated with every upward event.

Every upward event having no forced coordinate contains the majority event M={X_1+X_2+X_3≥2}; this follows directly from its minimal true states. Consequently it contains each fork. If two different forks F_i,F_j are compared, their intersection is {X_i=X_j=1}. Pairwise positivity from (1), and P(F_i)≤P(X_i=1), give

    P(F_i∩F_j) ≥P(X_i=1)P(X_j=1) ≥P(F_i)P(F_j).

Together with the preceding cases, a forced event is positively correlated with every upward event.

For completeness, an upward event with no forced coordinate is either M or has a true singleton state. To see this, if it has no true singleton, its minimal states are two-element sets or the full set. Any proper subcollection of the three two-element sets has a common coordinate, which would be forced. Thus the only unforced option without a true singleton is M.

Define the dual event E^d={y:1−y is not in E}, and put Y=1−X. If E contains a singleton state {i}, then E^d is forced at i. Property (1) is preserved under complementing all coordinates, because for increasing H,

    Cov(Y_i,1_H(Y))=Cov(X_i,−1_H(1−X)) ≥0.

The function on the right is increasing; (1) extends from event indicators to all increasing functions by the finite superlevel decomposition. Also

    Cov(1_E(X),1_F(X))=Cov(1_(E^d)(Y),1_(F^d)(Y)).

If two unforced events are not both M, at least one dual is forced, so their covariance is nonnegative by the already-proved forced case applied to Y. If both are M, their covariance is a variance. This exhausts all upward-event pairs and proves the lemma. ∎

The finite classification can equivalently be checked on all 20 upward events and their 400 ordered pairs. The companion checker verifies the exact containments, intersections and dual cases used above; it does not substitute numerical sampling for the displayed probability inequalities.

## 2. Application to arbitrary bipartite graphs

Turn 2's monotone Kempe bijection proves (1) for every fixed-color indicator at a vertex of A against every increasing observable of the entire A-zero set. Restricting to any three distinct vertices preserves this property. Therefore:

**Theorem.** For every finite bipartite graph, every q≥3, and every set of at most three vertices of A, their fixed-color indicator vector is positively associated.

This does not require that A itself have only three vertices. It is a universal order-three marginal conclusion. It is consistent with the source singling out a four-vertex conjunction test as unresolved. It also does not assert the FKG lattice condition for an arbitrary three-coordinate marginal: the known dreidel example already violates that stronger condition.

## 3. A stronger theorem when the whole side has size three

**Theorem.** If the entire observed bipartition class A has at most three vertices, its fixed-color marginal satisfies the FKG lattice condition for every finite opposite class B and every q≥3.

Take A={1,2,3}. Discard B vertices of degrees zero and one, since they contribute constants to the A-coloring weight. Let m_12,m_13,m_23 count the corresponding degree-two neighborhoods, and let m count the degree-three neighborhood. Put

    a=q−2≥1, r=q−1=a+1, R=(a+1)/a,
    x=R^m_12, y=R^m_13, z=R^m_23,
    t=R^m, u=((a−1)/a)^m, M=xyz t.

Use u=1 when m=0, including the q=3 case. Up to a common positive factor, the weight of an A-color assignment is M when all colors agree, x,y,z when respectively only that named pair agrees, and u when all three differ. This follows by factoring out a from each nontrivial B-neighborhood extension count.

Counting the remaining nonzero colors gives exact zero-set weights

    w(123)=M,
    w(12)=rx, w(13)=ry, w(23)=rz,
    w(1)=r(z+au), w(2)=r(y+au), w(3)=r(x+au),
    w(empty)=r[M+a(x+y+z)+a(a−1)u].                          (2)

The common factor omitted from (2) does not affect lattice inequalities. The marginal has positive weights. It suffices to prove all local two-coordinate lattice inequalities; these imply the full lattice condition by successive coordinate additions. By permutation symmetry of the notation there are only two forms.

For coordinates 1,2 with the third coordinate absent, division by r² gives the gap

    (t x²−1)yz + a(x−u)(y+z) + a(x−u)(x+au) ≥0,             (3)

since x,y,z,t≥1 and 0≤u≤1.

For coordinates 1,2 with the third coordinate present, the gap is

    r yz [t x(x+au)−r].                                     (4)

It remains to prove t(1+au)≥a+1. Set b=1−1/a² and F_m=R^m+a b^m. Then t(1+au)=F_m, and

    F_0=F_1=a+1,
    F_(m+2)−2F_(m+1)+F_m
        =R^m(R−1)²+a b^m(b−1)² ≥0.

Thus F_m≥a+1 for every nonnegative integer m. Since x≥1, (4) is nonnegative. This proves all local lattice inequalities and hence the theorem for |A|=3. The smaller-side cases follow by adjoining isolated A vertices and restricting a lattice inequality to a fixed face. ∎

The restriction here is on the **entire** side. Eliminating additional hidden A vertices does not preserve the simple neighborhood-count form (2), so this lattice theorem cannot be applied to three selected vertices inside a larger side.

## 4. The side-size lattice threshold is sharp, without a target counterexample

Let A={0,1,2,3}, q=3, and let B have the five degree-two neighborhoods

    {0,3}, {2,3}, {1,3}, {0,2}, {1,2},

together with m≥1 vertices having neighborhood {1,2,3}. Put t=2^m. In binary mask order 0 through 15, direct integration of B gives w(t)=u+t v, with

    u=(52,12,20,4,12,8,12,8,12,8,12,8,8,16,0,0),
    v=(80,16,0,0,0,0,0,0,0,0,0,0,0,0,16,32).

The total is Z(t)=192+144t. The neighborhood masks are (9,12,10,5,6) and m copies of 14. To derive these vectors, assign the four A colors: if colors on {1,2,3} are all different the weight is zero; if all equal the repeated-neighborhood factor is t; otherwise it is one. Multiply by the five pair-neighborhood extension counts and collect zero masks. This yields the displayed integer vectors exactly.

The local lattice gap for zero sets empty,{0},{1},{0,1} is

    w(empty)w({0,1})−w({0})w({1})
       =(52+80t)·4−(12+16t)·20=−32.                         (5)

Thus the universal lattice theorem cannot extend from side size three to side size four. Already m=1 gives a ten-vertex proper-coloring example. This is a stronger-condition counterexample only.

In fact this entire graph family is positively associated. The following complete finite coefficient certificate proves that additional assertion, so (5) must not be advertised as a counterexample to the original source question.

For any upward events U,V on four coordinates, write u(U),v(U) for the sums of the displayed entries over U. Their covariance numerator is the quadratic polynomial

    [192+144t][u(U∩V)+t v(U∩V)]
       −[u(U)+t v(U)][u(V)+t v(V)].                           (6)

There are exactly 168 upward events. The checker enumerates all 14,196 unordered pairs including repetitions, expands (6) in z=t−2, and checks that each of its three coefficients is a nonnegative integer. Hence (6)≥0 for every real t≥2, in particular for every allowed 2^m.

TURN_4_COEFFICIENT_CERTIFICATE.json records the 2,165 distinct coefficient triples (descending powers z²,z,1) with their multiplicities; these sum to 14,196. Its generating checker is short, deterministic and uses only exact integers. This is a complete finite certificate after the analytic parameter reduction, not a sample of t values or of increasing events.

## 5. Controls and remaining gap

The checker also compares formula (2) to direct extension counts in 540 three-side graph/q cases, tests their lattice inequalities, verifies the Boolean three-variable proof classification, reconstructs the family vectors, and proves all coefficients in (6) nonnegative. All 50,011 exact assertions pass. These are author controls, not independent review.

Run python verify_turn4.py to reproduce TURN_4_CHECKS.json and the compact coefficient certificate. The earlier fixed-seed lattice probe is retained separately as an exploratory diagnostic; its negative output was never a source counterexample and is subsumed by the simpler family proof above.

What remains is full association for arbitrary increasing observables on four or more coordinates in arbitrary finite bipartite graphs. The universal three-coordinate theorem, the stronger whole-side-three lattice theorem, and the associated-but-not-lattice family do not close that gap. A final substantive turn will test whether the one-coordinate regression constraints plus color symmetry control the four-coordinate obstruction, while retaining exact distinctions between abstract probability laws and graph-coloring laws. Original target: **unresolved 4/5**.
