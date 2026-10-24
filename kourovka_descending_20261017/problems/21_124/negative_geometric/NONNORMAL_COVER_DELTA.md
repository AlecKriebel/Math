# A nonnormal cover defeats the overbroad holonomy obstruction

UTC: 2026-10-24T22:26:00Z. Exact proposed partial result; independent review pending. This corrects no claim in the frozen FINITE_HOLONOMY_FILTER.md, which explicitly requires global trivial a holonomy (or a normal cover containing a).

For G_4, the infinite cyclic subgroup <a> is a virtual retract. Thus failure of G_4 itself to be RFRS, as proposed in the earlier note, cannot be promoted to failure of(VRC) using this cyclic subgroup.

Use the connected four-sheeted cover given by the right permutation action

 a=(2 3), b=(0 1), c=(0 2)(1 3), t=identity.

These permutations satisfy all three presentation relators (k=4), and the action is transitive. Let H be the stabilizer of vertex0. Then [G_4:H]=4 and a∈H, but a does not kill the full coset action and H is not normal.

Give the oriented a,b,c,t edges at each vertex the following integer weights:

| vertex | a | b | c | t |
|---|---:|---:|---:|---:|
|0|1|0|0|0|
|1|-1|0|0|4|
|2|0|2|0|2|
|3|0|0|0|2|

Every lift of each defining relator has total weight0, as checked by direct traversal in check_nonnormal_witness.py. These weights therefore define a homomorphism f:H→Z. The a-edge at0 is a loop of weight1, so f(a)=1. The map h↦a^{f(h)} is a retraction H→<a>, proving the assertion.

This is a genuine finite-index quantifier boundary. The same cover has a conjugate a which is not represented by a loop of length1 at vertices2 or3; its square there has weight0. A normal core may contain a^2 while omitting a. Restricting f to that core still detects a^2 based at0, which also demonstrates why the normal-cover theorem cannot replace the hypothesis a∈H by a^e∈H.

The bounded search found no a visibility for G_3 in all transitive permutation representations of degree≤5, including nontrivial a holonomy. This is only bounded evidence. No general non-VRC theorem follows. A separate degree6 search is in progress; negative bounded searches are not promoted to proofs.
