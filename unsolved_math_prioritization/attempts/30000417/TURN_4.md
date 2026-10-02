# Turn 4: variable anchors, local extrema and an exact limit of the method

The original floor conjecture remains unresolved. This turn removes the common-label requirement from the anchor method, proves an unrestricted-palette local-extremum family, and exhibits a feasible instance that defeats every optimized modulo-three deficit certificate.

## 1. Variable anchor labels

Choose a residue class I={r,r+3,...} of path vertices. As in turn 2, I is independent in the square of the path and its complement induces an ordinary path. Assign an arbitrary label a_i from L_i to every i in I; these anchor labels need not be equal or close.

For each remaining vertex j, delete the union of forbidden intervals around its anchor neighbors:

    A_j = {x in L_j : |x−a_i|>=d for every i in I with |i−j|<=2},
    delta_j = max(0,2d−|A_j|).

Each remaining vertex has one or two anchor neighbors. If it has two, they are consecutive anchors. Therefore, if

    S(a)=sum_{j not in I} delta_j < 2d,                     (1)

the weighted path lemma from turn 2 labels all remaining vertices. Restoring the chosen anchor labels gives a valid original (d,d)-labeling. This proves an all-size sufficient criterion for completely arbitrary finite lists and arbitrary palette size.

## 2. Exact polynomial optimization of this criterion

List the anchors as i_1<...<i_t. Partition the remaining vertices into those with exactly one anchor neighbor i_h and those with the pair i_h,i_{h+1}. Define

    U_h(a) = total deficit of vertices having only anchor neighbor i_h,
    V_h(a,b) = total deficit of vertices having anchor neighbors i_h,i_{h+1}.

Then the exact cost separates as

    S(a_1,...,a_t)=sum_h U_h(a_h)+sum_{h=1}^{t−1}V_h(a_h,a_{h+1}).

There are no other terms: the distance-two geometry supplies at most two consecutive anchor neighbors. Define

    D_1(b)=U_1(b),
    D_h(b)=U_h(b)+min_{a in L_{i_{h−1}}}(D_{h−1}(a)+V_{h−1}(a,b)).

Induction on h proves D_h(b) is exactly the minimum partial cost with last anchor label b. Taking min_b D_t(b) and backtracking gives a globally optimal anchor assignment for that residue class. Run this for all three residue classes. If any optimum is <2d, (1) certifies feasibility.

For lists of size at most k, evaluating local costs directly gives O(nk^3) integer comparisons, with O(nk) storage for score/predecessor tables. Label sizes affect the bit cost of integer arithmetic but not the number of comparisons. This algorithm optimizes the sufficient certificate exactly; it is not asserted to decide original feasibility. The ordinary reachable-pair algorithm remains the exact feasibility oracle.

## 3. A local-minimum theorem at the conjectured cardinality

Let n>=3, d>=1 and k=floor(3d(1−1/n))+1. Choose a largest modulo-three class I, so q=|V\I|=floor(2n/3). Suppose that for every anchor i, its minimum label a_i=min L_i satisfies

    a_i <= min L_j for all j not in I with |i−j|<=2.        (2)

The a_i may all be different, and the global palette can be arbitrarily large.

For a remaining j, let b_j be the largest of its one or two neighboring anchor labels. By (2), min L_j>=b_j. All labels deleted from L_j therefore lie in the interval from min L_j to b_j+d−1, which has at most d integer positions. Hence |A_j|>=k−d and

    delta_j <= 3d−k = ceil(3d/n)−1.

The same strict arithmetic as turn 2 yields

    sum delta_j <= floor(2n/3)(ceil(3d/n)−1) < 2d.

Thus every list assignment satisfying (2) is labelable at the conjectured cardinality. Reflection gives the corresponding local-maximum theorem: choose each anchor's maximum and require it to be at least every neighboring retained list's maximum. This strictly drops the need for a common label on the anchor class. It is a sufficient family, not a claim that all list-minimum profiles admit such a residue class.

## 4. Exact incompleteness certificate

`TURN_4_CERTIFICATE.json` gives a 42-vertex instance with d=2, six-element lists and palette {1,...,8}. Its source-conjectured cardinality is six. It records:

- A complete explicit valid (2,2)-labeling, checked directly against all lists and all distance-one/two pairs
- Exact minimum costs of 4, 4 and 4 for the three residue classes
- All score/predecessor tables needed to check those minimum costs

Since the sufficient condition requires strict cost <2d=4, it fails for every possible choice of anchor labels and all three residue classes on this instance. Yet the instance is feasible, both by its explicit coloring and by the restricted-palette theorem of turn 3. Therefore even exact optimization of the anchor deficit method cannot itself prove the general conjecture without a genuinely stronger residual criterion or a different decomposition. No minimality of the 42-vertex example is claimed.

This is an obstruction to a proof method, not a counterexample to the original conjecture. The local-minimum theorem and dynamic optimization are still valid, useful sufficient results. This turn leaves the arbitrary-list global upper bound unresolved; one genuine author turn remains.

## 5. Replay and credit

`anchor_solver.py` implements the displayed recurrence. `verify_turn4.py` compares it with exhaustive anchor choices on small instances, checks constructed witnesses and local-extremum families, and independently audits the large certificate's Bellman tables and direct valid labeling. Python 3 standard library only.

The base weighted path lemma and common-extremum approach have prior credit in Kohl's OWR contribution and dissertation. The refinements and computational limitation here carry no novelty claim. They are not being used to reclassify the original conjecture as solved.
