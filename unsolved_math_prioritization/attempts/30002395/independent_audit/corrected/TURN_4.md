# Turn 4: Upgrade monotone lattice data

Substantive approach: exploit the available maps into open-set lattices that preserve arbitrary infima and increasing countable suprema, and try to upgrade them to the complete-lattice embedding needed for realization. The missing finite-join property is a genuine extra condition.

Let X={1,2} be discrete and P={u,v,w} be discrete. Define Psi on the four-element lattice O(X) by

Psi(empty)=empty, Psi({1})={u}, Psi({2})={v}, Psi(X)=P.

This map is injective and preserves top, bottom, and arbitrary infima. For a family of subsets of X, the only nontrivial meet is {1} intersection {2}=empty, and its images also meet in the empty set; top, bottom, repetitions, and empty families cause no exception. Every nonempty upward directed family in the finite lattice O(X) has a largest member: successive upper bounds within the family absorb its finitely many distinct elements. Hence Psi preserves its supremum. In particular it preserves increasing countable suprema.

But Psi({1} union {2})=P, whereas Psi({1}) union Psi({2})={u,v}. Thus these hypotheses do not imply preservation of even binary joins. Nor is Psi an inverse-image map: if some function P->X induced it, the value of w would be either 1 or 2, forcing w into one of the two indicated preimages.

Adding the missing union {u,v} to the image does not repair the map with the same range lattice. The enlarged lattice has five elements rather than four. In this example the enlarged lattice is the open-set lattice of a different three-point T0 space, with opens empty,{u},{v},{u,v},P. Thus simply closing the range under joins can change the space one is trying to realize.

There is an exact upgrade lemma. Suppose X is second countable and Psi:O(X)->O(P) preserves binary unions and increasing countable unions. Then Psi preserves every nonempty union. If it also preserves the empty set, it preserves all unions. For any family (U_i), choose countably many members U_{i_n} with the same union: select one containing each basis element that lies in some U_i. Put W_n=U_{i_1} union ... union U_{i_n}. Then

Psi(union_i U_i)=union_n Psi(W_n)=union_n union_{k<=n} Psi(U_{i_k}).

Monotonicity follows from binary-union preservation, so each Psi(U_i) lies in Psi(union_i U_i); this gives equality with union_i Psi(U_i). Finite and empty families are handled directly. Thus, for an already injective top/bottom and arbitrary-infimum preserving map with increasing-union continuity, binary-union preservation is precisely the additional property sufficient for the required complete-lattice embedding.

Harnisch–Kirchberg Remark 6.2 records a map for every Dini space with the weaker monotone-union conditions. The finite example proves that the stronger join condition is not a formal consequence of those listed axioms. It does not show that a better map cannot exist, since the particular finite X here already has a commutative realization.

Outcome: an exact missing-axiom reduction, plus a finite falsification of the attempted automatic upgrade. No construction of the required binary-join preserving map for arbitrary Dini X was found.
