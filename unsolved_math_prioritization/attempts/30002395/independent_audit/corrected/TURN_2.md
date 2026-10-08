# Turn 2: Replace a Polish cover by a locally compact one

Substantive approach: start from an open continuous Polish presentation of a Dini space, then precede it by a locally compact Polish presentation. The missing local compactness looks at first like an auxiliary coding issue. The following argument proves that this generic repair is impossible.

Lemma. If f:Q->P is continuous, open, and onto, Q is locally quasicompact, and P is Hausdorff, then P is locally compact. For p=f(q) choose an open neighborhood V of q inside a quasicompact neighborhood K. Then f(V) is open, contains p, and lies in f(K). The latter is quasicompact by continuity and is compact and closed because P is Hausdorff. Thus p has a compact neighborhood. The same argument works inside any preassigned open neighborhood of p by first restricting to its preimage.

For a T1 target, a continuous pseudo-epimorphic map is surjective: apply density in the closed singleton {p}. A continuous pseudo-open map to a T1 target is open onto its image; it is open into the target when it is also surjective. To see the latter directly, its pseudo-graph is the equivalence relation R={(q,r):f(q)=f(r)}. For open V in Q, the saturation f^{-1}f(V) is pr_1(R intersect (Q times V)), open by the projection condition. It is invariant, so its image f(V) is open in f(Q), by the invariant-image condition. If f is onto, this is open in P.

Take P=N^N with the product of discrete topologies. It is Polish under the usual complete first-disagreement metric. It is not locally compact. Every neighborhood contains a cylinder C fixing finitely many coordinates. Such a cylinder is closed and is covered by the pairwise disjoint cylinders obtained by fixing the next coordinate; there is no finite subcover. If a compact neighborhood K existed, it would contain some such closed cylinder C, making C compact, a contradiction.

Therefore no locally quasicompact Q admits a continuous pseudo-open pseudo-epimorphic map onto N^N. In particular, an arbitrary Polish source cannot be repaired by a preceding locally compact pseudo-open cover. Choosing a universal Polish presentation and then applying this nonexistent repair is invalid.

This does not produce a counterexample to the question: N^N is not itself a Dini space because it is not locally quasicompact. It obstructs only the general two-stage construction. A different locally compact domain mapping directly to a particular Dini X remains possible.

Outcome: exact failure certificate for this route. The underlying obstacle is already noted in Harnisch–Kirchberg Section 6; the proof here reconstructs it rather than claiming new discovery.
