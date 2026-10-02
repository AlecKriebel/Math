# Turn 2: a sparse common-label and deficit-budget theorem

The original arbitrary-list floor conjecture remains unresolved. This turn gives an all-n, all-d sufficient condition that needs a common extremal label only on one largest residue class of path positions, rather than on every vertex. The proof also handles a nonextremal common label when the exact remaining-list budget is sufficient. No novelty claim is made; the extremal case extends the direct argument of Kohl's 2006 dissertation, Theorem 4.14.

## 1. A weighted path-list lemma

Consider an ordinary path on q vertices, where only adjacent labels must differ by at least d>=1. Let its lists A_1,...,A_q be arbitrary finite integer sets. Put

    delta_j = max(0, 2d−|A_j|).

If sum_j delta_j < 2d, then a valid labeling exists.

Proof. Truncate each list to exactly min(2d,|A_j|) elements. This cannot improve feasibility, so finding a labeling of the truncated lists suffices. Each truncated list has size 2d−delta_j.

For a nonempty finite set S of a integers, the set of integers b that are within distance <d from *every* member of S is the integer interval

    [max(S)−d+1, min(S)+d−1].

It contains at most max(0,2d−a) integers, because max(S)−min(S)>=a−1. Define feasible terminal-label sets B_1=A_1 and

    B_j={b in A_j : some a in B_{j−1} has |a−b|>=d}.

Inductively,

    |B_j| >= 2d−sum_{h=1}^j delta_h > 0.

The first equality is the truncated list size; at each next step at most 2d−|B_{j−1}| labels are removed. The strict total-budget inequality makes every partial sum <2d. A label in B_q can be followed backwards through predecessor choices, producing the desired labeling. The argument is valid for q=1 as well.

Equivalently, lists capped at 2d with total cardinality >2d(q−1) suffice. This is the path instance of the weighted tree-list result stated as Theorem 2 in the original report. The proof above is included so its precise strict inequality and arbitrary-list domain are explicit. Equality cannot be relaxed in general: for q=2, two identical d-element consecutive lists have total 2d and cannot be separated.

## 2. Remove every third vertex

Write the original path vertices as 1,...,n. Fix a residue r in {1,2,3} and let

    I_r={i : i == r modulo 3},

where r=3 denotes multiples of 3. Vertices in I_r are mutually at distance at least 3, so they may all receive one common label c whenever c belongs to every list on I_r.

After removing I_r from the square P_n^2, the remaining vertices, in their original increasing order, induce an ordinary path. Successive remaining positions differ by 1 or 2 and hence are adjacent in the square. Any two nonconsecutive remaining positions differ by at least 3: among any three consecutive original positions, one is removed. Thus no extra edges remain. Boundary prefixes and suffixes contain at most two retained positions and obey the same rule.

For each remaining vertex j set

    A_j=L_j \ {c−d+1,...,c+d−1}.

Every constraint to a removed vertex is satisfied exactly by avoiding this interval; if there are two removed neighbors the forbidden interval is still the same one. The remaining constraints are exactly the d-separation constraints along the induced path.

**Deficit-budget theorem.** If a label c belongs to every list at positions in I_r and

    sum_{j not in I_r} max(0,2d−|A_j|) < 2d,                 (2)

then the original assignment admits a (d,d)-labeling.

This follows by the weighted path lemma and then restoring label c on I_r. It is an all-size sufficient condition for arbitrary lists, and c need not be their global minimum or maximum. It is not asserted to be necessary.

## 3. The conjectured cardinality under a sparse extremum condition

Let n>=3, d>=1 and

    k=floor(3d(1−1/n))+1 = 3d−ceil(3d/n)+1.

Choose a largest residue class I_r, so |I_r|=ceil(n/3) and the number q of retained vertices is floor(2n/3).

Suppose the global minimum c of the union of all lists belongs to every list on I_r. It need not belong to any retained-vertex list. Since no label is less than c, deleting labels at distance <d from c removes at most d elements from each retained list. Hence

    |A_j| >= k−d,
    delta_j <= 3d−k = ceil(3d/n)−1.

The latter quantity is nonnegative, since k<=3d. With h=ceil(3d/n)−1, we have h<3d/n, including when 3d/n is an integer. Consequently

    sum delta_j <= q h < (2n/3)(3d/n)=2d.

The deficit-budget theorem applies. Reflection of all labels proves the same result for a global maximum c.

Thus the original conjectured upper bound holds for all assignments whose global minimum or maximum occurs on one largest modulo-three class. This includes but is strictly less restrictive than the previously published condition requiring the global extremum in *every* list. It is a reconstruction/extension of that method, not a claim to settle arbitrary lists.

At n=3 the argument uses a singleton residue class; the global minimum lies somewhere, so it also recovers the known complete triangle case from turn 1. For n>3, the condition need not hold. For example, distinct disjoint lists usually have no common label on a residue class. Such examples may still be easy to label and do not themselves refute the conjecture.

## 4. What this does and does not establish

The theorem provides a constructive certificate for broad, explicitly checkable families, including some assignments with a nonextremal common label and small forbidden-interval intersections. The verifier checks the weighted-path induction and the exact induced-path geometry, and produces/checks complete original-path labelings for random and structured assignments meeting the hypotheses.

The remaining gap is to handle assignments lacking such a common label or lacking the strict deficit budget. No claim that every assignment can be shifted, compressed or otherwise transformed into this family has been proved. Turn 1 gap compression preserves feasibility but does not create common labels. The global arbitrary-list floor formula is still unresolved after two turns.
