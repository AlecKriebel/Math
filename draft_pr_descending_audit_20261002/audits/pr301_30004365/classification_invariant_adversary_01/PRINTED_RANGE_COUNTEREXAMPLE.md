# Exact counterexample to the truncated peripheral range

Independently derived 2026-10-05 before historical review. This is a counterexample to the literal printed APS7.4 range and workshop Theorem3.3 summary, **not** to the candidate's full peripheral comparison key.

## Quivers over an arbitrary fixed field k

For m,n>=3 define A(m,n)=kQ/I. Vertices are a_0,...,a_(m-1), b_0,...,b_(n-1). Arrows u_i:a_i->a_(i+1 mod m), v_j:b_j->b_(j+1 mod n), and z:a_0->b_0. Relations are all u_i u_(i+1 mod m) and all v_j v_(j+1 mod n). No composition involving z is a relation. Composition order is the APS/PPP left-to-right convention.

Every ordinary cycle vertex has one incoming and one outgoing arrow with their composition related. At a_0, the unique incoming u_(m-1) has related continuation u_0 and unrelated continuation z. At b_0, the unique outgoing v_0 has related predecessor v_(n-1) and unrelated predecessor z. Thus the gentle degree and unique continuation/predecessor conditions hold everywhere.

The only allowed length-two paths are u_(m-1)z and zv_0; the only allowed length-three path is u_(m-1)zv_0. There are no length-four allowed paths. Hence I is admissible, A(m,n) is finite dimensional, and dim_k A=2(m+n)+4. The quiver is connected.

## Surface and peripheral data

There are no infinite straight permitted walks. The Koszul dual has precisely the two original full-relation cycles as infinite straight walks. PPP Remark4.11(i),(iv),(v) therefore gives no white punctures and exactly two black punctures. The number of vertices is V=m+n; arrows E=m+n+1. PPP4.11(vii) gives

    2g = E - V - b - p + 2 = 1 - b.

There is at least one boundary component: APS Definition3.7 requires both puncture colors nonempty if boundary is empty, while Pwhite is empty. Since b>=1 and g>=0, this equation forces b=1,g=0.

The maximal finite permitted paths are the length-three path u_(m-1)zv_0 and each of the remaining m+n-2 cycle arrows. There are m+n-1 such paths. No trivial permitted thread occurs: every ordinary vertex has related incoming/outgoing composition, while the two bridge endpoints have more than one incoming or outgoing arrow. Equivalently, in the blossom matching every finite straight walk contains one of these paths. PPP4.11(i) gives m+n-1 white boundary marks. Alternation gives the same number of black boundary marks.

Around a black puncture associated to an r-cycle of relations, a sufficiently small simple peripheral loop crosses exactly r incident dual black arcs. Orient it with the puncture disk on the left and the remaining surface on the right. In every sector polygon, the white mark is outside the loop, to the right. APS Lemma3.18 thus gives w(c)=-r. This also agrees with APS Remark6.2: the puncture AG pair is (0,r).

For the compact core with d=b+p=3 peripheral circles and g=0, APS Proposition3.20(5) gives

    w(outer) - m - n = 4 - 2d - 4g = -2,
    w(outer) = m+n-2.

## Concrete pair

| invariant | A(3,5) | A(4,4) |
|---|---:|---:|
| dim_k |20|20|
| g,b,p |0,1,2|0,1,2|
| white marks on the original boundary |7|7|
| total boundary marks |14|14|
| original-boundary winding |6|6|
| puncture winding multiset |{-3,-5}|{-4,-4}|
| AG pairs |{(7,1),(0,3),(0,5)}|{(7,1),(0,4),(0,4)}|

The literal printed APS7.4(1),(2) hold: all topological/cardinality data match and the sole original-boundary marked count and winding match. There is no handle criterion in genus zero. Thus the printed iff with winding equality only for j=1,...,b would declare them derived equivalent. Yet APS6.1 requires an orientation-preserving marked-surface homeomorphism preserving winding of **every** simple closed curve. Such a homeomorphism permutes the puncture loops, whose windings here have unequal multisets. Thus the algebras are not derived equivalent. The differing AG pairs provide the same obstruction.

Workshop Theorem3.3 also omits the paired peripheral windings and would declare the same pair equivalent from its listed genus-zero data. Problem3.4 nevertheless unambiguously asks to compute its listed data; that literal computational request survives the erroneous completeness summary.

## Consequence for candidate

The candidate's records {(7,6),(0,-3),(0,-5)} and {(7,6),(0,-4),(0,-4)} correctly distinguish this pair. Keeping all puncture winding values cannot be dismissed as an optional refinement. It is mandatory for an actual complete derived-equivalence key. Sufficiency should be proved through LP Theorem1.2.4 on the compact puncture-truncated core, then APS6.1/7.2, rather than invoking the false printed APS7.4 sufficient direction. This is an additive source/proof correction; no change to the candidate's numerical key is needed.
