# Turn 5: Glue locally available realizations

Substantive approach: avoid constructing a global witness from scratch by joining locally compact Polish witnesses on open neighborhoods. The complete-lattice criterion gives a full local-to-global theorem.

## Open-cover theorem

Let X be a sober second-countable T0 space with a countable open cover (U_n). Suppose each U_n is homeomorphic to the primitive ideal space of a separable nuclear C*-algebra. For each n, the Harnisch–Kirchberg characterization supplies a locally compact Polish P_n and a top/bottom preserving complete-lattice embedding

Psi_n:O(U_n)->O(P_n).

Let P be the topological disjoint union of the P_n. It is locally compact and Polish. For completeness, choose a compatible complete metric on each P_n, cap it at 1, and put distance 2 between distinct components. This is a complete metric inducing the disjoint-union topology; a union of countably many countable dense sets is countable and dense. Local compactness is componentwise.

For V open in X define Psi(V) by

Psi(V) intersect P_n = Psi_n(V intersect U_n).

The cover ensures injectivity. If V and W differ, take x in their symmetric difference and choose U_n containing x. Their intersections with U_n differ; injectivity of Psi_n then distinguishes their images. Top and bottom are preserved. Arbitrary unions are preserved componentwise.

For arbitrary families (V_i), the crucial identity is

U_n intersect int_X(intersection_i V_i) = int_{U_n}(U_n intersect intersection_i V_i).

One inclusion is immediate. For the other, a relatively open neighborhood in U_n is open in X because U_n is open; if it lies in every V_i it lies in the left-hand interior. Taking this identity through Psi_n proves preservation of arbitrary lattice infima. Interiors and intersections in a disjoint union are also computed componentwise. Therefore Psi is the complete-lattice embedding required by the characterization, and X has a separable nuclear realization.

Conversely, each open subspace of Prim(A) is Prim(I) for the corresponding closed ideal I of A. Ideals of separable nuclear C*-algebras are separable and nuclear. Thus the property is local on open covers among the spaces in question. An arbitrary open cover reduces to a countable subcover by second countability.

## A useful full subclass

Every locally Hausdorff Dini space has a separable nuclear realization. Choose an open Hausdorff neighborhood at each point. Each such open subspace remains second countable and locally quasicompact, hence is locally compact Hausdorff. It has the commutative realization C_0(U); separability follows from second countability and nuclearity from commutativity. Choose a countable subcover and apply the theorem. This includes the non-Hausdorff doubled-limit space from Turn 3.

The empty space is realized by the zero algebra and can be separated off throughout.

## The exact unresolved step

A general Dini space is not assumed locally Hausdorff. Nor do its axioms assert that each point has an open neighborhood with a complete-lattice embedding into the opens of a locally compact Polish space. The proof therefore does not extend to all Dini spaces without a new local-existence argument. It also does not justify gluing closed covers: the displayed interior identity used openness essentially.

Outcome: a complete open-cover permanence theorem and an affirmative result for locally Hausdorff Dini spaces, obtained as consequences of the established characterization. These are credited consequences with no novelty claim. After five substantive approaches, the universal source problem remains unresolved.
