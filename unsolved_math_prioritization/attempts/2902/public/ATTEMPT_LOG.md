# Five substantive attempts

Outcome: **unresolved, 5/5**. These are five distinct mathematical approaches, not five catalogue searches. No resolution is claimed and the budget is not used as evidence about the truth of the question.

## Attempt 1: transport closed embedding obstructions through doubling

Tested whether a known obstruction to a closed homology sphere could obstruct its puncture. The exact neighborhood construction gives the equivalence between embedding Y₀ and embedding Y # (−Y). The latter already bounds Y₀ × I for every Y. This proves why homology-cobordism obstructions to closed embeddings do not decide the punctured question. The tempting reverse argument by doubling that filling was tested with van Kampen: its identity double retains π₁(Y). Remaining gap: a complementary filling and gluing with standard smooth total space. See Proposition 1.

## Attempt 2: build the ambient manifold by ordinary spinning

Constructed (S¹ × Y₀) ∪ (D² × S²) explicitly. Integral Mayer–Vietoris proves that the ambient space is a homology 4-sphere, while van Kampen gives π₁ = π₁(Y). Thus this universal construction cannot be S⁴ when the group is nontrivial. A proposed disjoint cap for the puncture would incorrectly imply a homology-ball filling of every closed Y. Remaining gap: remove the fundamental group without changing the required smooth ambient type. See Proposition 2.

## Attempt 3: change the surgery circle to a diagonal graph

Used a graph of a loop g in S¹ × Y to preserve a single punctured slice. Computed the full quotient (Z × G)/normal(tg) = G/normal([g,G]), and proved its triviality is equivalent to normal generation by g when G is perfect. The relative integral homology sequence checks that the ambient surgery remains a homology sphere. Normal generation thus yields a smooth homotopy 4-sphere, not a proof of smooth standardness. Remaining gaps: a universal normal generator and standardness of a suitable resulting sphere. See Proposition 3.

## Attempt 4: extend the known positive families

Checked Zeeman's compact-fiber theorem and its complete relevant proof, distinguished its Corollary 4 from the source's Corollary 2 citation, and tested the Poincaré sphere as a positive punctured/negative closed control. Proved the exact connected-sum closure and converse restriction. Compared the scope of accessible Larson surgery results with the stronger thesis statement credited in K3; did not replace an inaccessible proof with a different theorem. Remaining gap: a reduction of arbitrary Y to the verified cyclic-cover family or another universally valid construction. See Proposition 4 and the source gate.

## Attempt 5: repair the ambient group by further surgeries

Tried killing a finite normal generating set of the ordinary spun ambient group. Van Kampen kills the selected generators, but the Euler characteristic and integral homology calculation show that each additional circle surgery adds two to b₂. Even granting preservation of the embedded puncture, r > 0 such surgeries cannot themselves produce S⁴. Remaining gap: actual relative smooth geometric cancellations, with control of the surviving puncture. No algebraic-to-geometric cancellation inference is made. See Proposition 5.

## Verification boundary

The Python script checks a finite perfect-group model, a nonperfect negative control, an abelianization determinant, and the ranks of the exact-sequence maps used in the constructions. These computations neither decide the universal embedding problem nor certify any smooth 4-manifold identification.
