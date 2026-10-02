# Two-thirds leaf limit: complete credited first-turn candidate

Problem 30002545 / OWR-12872-015. A complete combinatorial proof candidate is recorded at turn 1/5 and awaits independent review. No further author turn is needed if the full source-requested proof is accepted. No new numerical result or historical priority is claimed.

For n≥2 the candidate proves the exact probability p_n=(2n−1)/(3n), hence p_n→2/3; p_1=1. It does not assume existence of the limit and does not use generating functions or an induction/recurrence proof.

The proof composes the credited Koganov–Janson contour correspondence with the credited Gessel ternary correspondence, detailed by Janson–Kuba–Panholzer. It identifies leaves with empty middle slots in a ternary increasing tree on n−1 internal vertices. Cyclically rotating all three child-slot names equates the three aggregate empty-slot counts; each tree has 2n−1 empty slots. Static interval descriptions prove both bijections without inductive enumeration. The required limit follows from this finite double count.

TURN_1.md contains the full argument, boundary cases, source correction and credit. The OWR total-leaf formula has an index typo; the argument is independent of it and agrees with Bóna–Pittel's corrected Example 2.3. Existing exact-mean identities and the relevant bijections predate the question, so this is a literature-derived reconstruction, not an asserted new discovery.

The exhaustive checker covers all 146,599 objects across n=2,…,8, with 3,346,451 exact controls of both inverses, order constraints, leaf/plateau/empty-slot identities, rotations and exact finite means. These finite tests supplement the all-n written proof. Independent review must assess the complete source scope and the no-induction/simple-combinatorial-proof requirement before final disposition.
