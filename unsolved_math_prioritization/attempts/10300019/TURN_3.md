# Author turn 3: switch ordering, reconnection, and the compact-transversal gap

**Partial: exact compatibility tests for a faithful-union model, with explicit limits. The general source operation is unresolved.** 2026-10-01.

This turn attacks the branched-switch step missing from the unbranched construction. A geometric Haken exchange is allowed to reconnect leaves; preserving all original leaf labels is a stronger model. The distinction is essential throughout.

## 1. A finite transverse diagram can be checked exactly

Specify finitely many local transversals indexed by v. At each v let X_v=X_v^0 disjoint-union X_v^1 be finite, with the order on each input color already fixed. Supply:

- Partial bijections between subsets of the X_v representing proposed leaf/holonomy identifications, each preserving color
- The required orders of blocks at each branch switch, expressed as inequalities between the points on the relevant transversal
- Any orientation signs for the partial bijections

An admissible faithful interleaving is a linear order on each X_v extending the two intrinsic orders and all prescribed switch inequalities, for which every partial bijection is order-preserving or order-reversing as specified.

There is an exact finite decision procedure: enumerate all shuffles of the two ordered sets at each v and check the finite constraints. The number of candidates is the product over v of binomial(|X_v|,|X_v^0|). Necessity and sufficiency are immediate for this explicitly defined finite order problem: every permitted total order is one such shuffle, and every condition has been checked. This does not claim that a finite holonomy diagram encodes every unmeasured lamination or every geometric exchange.

For a *given complete* collection of geometric product charts, such orders are a necessary consistency test for preserving the original leaves. The charts must still glue continuously, satisfy their cocycles, embed in the ambient manifold, and have closed compact transverse sets. Those are additional conditions, not consequences of the finite shuffle count.

## 2. A genuine branch can require reconnection

Return to the torus train track of turn1 carrying meridian alpha and longitude beta. Their algebraic intersection is1, so no representatives of their isotopy classes are disjoint: signed intersection of disjoint representatives would be0, contradicting invariance under isotopy. Consequently a common carrier for them cannot place disjoint unchanged copies of both input curves into its interval fibers. At the two switches the transverse orders cannot be made coherent while following both original loops unchanged.

The product example gives the same conclusion for the carried tori alpha×S^1 and beta×S^1. Their dual degree-one cohomology classes have nonzero cup product; their algebraic intersection represents the third circle. Disjoint isotopic representatives would have zero intersection class. Thus a faithful disjoint union is impossible in that common-carrier model.

Nevertheless the classical regular exchange exists and produces the slope(1,1) torus. Its leaves have been reconnected. This example is a positive control showing that the faithful-union order test is **not a necessary condition for Haken addition allowing reconnection**. It also shows why the successful product compression from turn2 cannot simply be applied sector by sector across a genuine branch.

As in turn1, this explicitly concerns the common-carrier formulation. No specific preassigned triangulation or equivalence between arbitrary carrying and compatible normal carrying is being asserted.

## 3. Finite compatibility alone does not produce a valid infinite transversal

A possible strategy is to solve every finite transverse diagram and pass to a limit. There is a precise obstacle even before leaf gluing: the resulting ordered set may not embed in a real interval, whereas a codimension-one lamination in a metrizable manifold has transversals that are closed subsets of such intervals.

Let X=[0,1]×{0,1}. Impose the within-color orders and the interleaving constraints

    (x,0)<(x,1)<(y,0) whenever x<y,
    (x,0)<(x,1) for every x.

The resulting order is the lexicographically split interval. Every finite subset of these requirements has a real-line realization: sort its finitely many first coordinates and place the two labels consecutively whenever both occur. Hence every finite shuffle test succeeds.

There is no order embedding of all of X into R. If j were such an embedding, choose a rational number q_x strictly between j(x,0) and j(x,1) for each x. For x<y these nonempty intervals are disjoint, so q_x are distinct. This would inject the uncountable interval[0,1] into Q. Contradiction.

Thus an abstract compactness argument for finite order constraints does not suffice to construct a compact metrizable transversal with continuous holonomy. Completing the order or identifying gaps may change the original input supports or their leaves; this would require a specified and justified monotone-equivalence rule. The source remark does not provide one automatically.

The split-interval constraints are an **abstract method countercontrol**. We have not realized them as the exact constraints forced by a pair of normal laminations on a finite branched surface. Therefore they are not a counterexample to the original question.

## 4. What a general positive construction would still need

The unbranched case succeeds because global stacking gives a continuous, metrizable order amalgam in advance. In a branched case, one needs compatible choices of reconnection, continuously varying across compact transverse sets, with all return identifications satisfied. Checking finite shuffles handles only one part of those requirements. The split-interval example forbids an unsupported passage from arbitrary finite successes to an interval-valued solution.

No source-compatible general topology or monotone equivalence has been selected. No impossibility theorem for every operation has been obtained. The remaining attempts will test transverse dynamics directly and formulate a controlled gluing criterion without silently assuming the missing compactness/continuity.

Substantive author turns:3/5. Estimated completion25%. Original unresolved; no historical novelty claim.
