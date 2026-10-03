# Turn 2: characteristic-core descent and its exact limit

Completed 2026-10-02 UTC. Original unresolved, 2/5 substantive turns; subjective progress 13%. This turn constructs the maximal common characteristic subgroup as a limit of finite, open computations and identifies exactly what a convergence proof would still require.

## 1. Topology clarification, additive to the frozen source gate

Nikolov–Segal, *On finitely generated profinite groups, I: strong completeness and uniform bounds*, Annals165 (2007), 171–238, Theorem1.1 on printed172, proves that every finite-index subgroup of a topologically finitely generated profinite group is open. The page also credits the earlier pro-p case to Serre. Primary source: https://annals.math.princeton.edu/2007/165-1/p05 . The exact statement and the definition of strong completeness were read and printed172 was inspected visually.

Consequently every abstract automorphism of F, or of an open subgroup U_i, is continuous: preimages of open subgroups have finite index and are therefore open. Thus abstract and continuous characteristicity coincide for the ambient groups in this problem. This does not assert that an arbitrary subgroup K is closed. Rather, if K is common characteristic and contained in every U_i, its closure is also common characteristic and contained in every U_i, since the U_i are closed and all their automorphisms are homeomorphisms. K is trivial if and only if its closure is trivial. Hence the source's version quantifying all subgroups is equivalent to the version quantifying closed subgroups. This uses the credited strong-completeness theorem rather than silently changing the question.

## 2. An open characteristic-core operator

For an open subgroup V of a finitely generated pro-p group G, define

    c_G(V)=intersection_{alpha in Aut(G)} alpha(V).

The orbit is finite. Indeed, all alpha(V) have the same finite index, and G has finitely many open subgroups of each index: their continuous coset actions into a finite symmetric group are determined by the images of finitely many topological generators. Thus c_G(V) is open, characteristic in G, and contained in V. It is the largest characteristic subgroup of G contained in V, even among nonclosed subgroups: if K is such a subgroup, K=alpha(K)<=alpha(V) for every alpha. The finite-index counting input also appears in Barnea et al., Lemma2.21.

Now fix a finite family U_1,...,U_n as in the source, including F. Put V_0=intersection_i U_i. Apply the operators c_{U_1},...,c_{U_n} repeatedly in cyclic order to obtain

    V_0 >= V_1 >= V_2 >= ... .

Every step is valid because its argument remains contained in every U_i. Every V_t is open in F. Define C=intersection_{t>=0}V_t.

**Theorem.** C is the largest subgroup of F contained in, and characteristic in, every U_i. In particular the chosen family answers the source question exactly when C=1.

For each i, the terms immediately after applying c_{U_i} form a cofinal subsequence of this decreasing chain. Those terms are characteristic in U_i, and their intersection equals C, so C is characteristic in U_i. It is contained in V_0 and is closed. Conversely any common characteristic K is contained in V_0. If K<=V_t and the next operator is c_{U_i}, the maximality property just proved gives K<=V_{t+1}. Induction gives K<=C. This proves both assertions, including the formulation with nonclosed K. QED.

It is important that a single round need not already be characteristic in all U_i. Later operators can destroy an earlier individual invariance. The cofinal-subsequence argument, not an unsupported assertion about one round, supplies simultaneous invariance at the limit.

## 3. Each individual core is a finite-quotient calculation

This section concerns a single step, not a termination algorithm for the original question. Let G be finite-rank free pro-p and V<=G open. Its coset action has finite p-group image Q. Let e be any integer with p^e>=|Q|. Iterated Frattini subgroups of a nontrivial finite p-group strictly decrease until trivial, so Phi^e(Q)=1. Functoriality under epimorphisms gives

    Phi^e(G) <= kernel(G -> Q) <= V.

The quotient P=G/Phi^e(G) is finite, and V is the full preimage of a subgroup V_bar of P. The map Aut(G)->Aut(P) is onto. To prove this, take any automorphism of P and lift its images of a free basis of G to elements of G. Their images in G/Phi(G) form a basis (Phi^e(G)<=Phi(G) when e>=1), so the free pro-p basis criterion makes them a basis of G. The resulting automorphism of G induces the specified automorphism on P. The case e=0 only arises when Q=1, hence V=G, whose core is already known.

Therefore c_G(V) is the full preimage of

    intersection_{beta in Aut(P)} beta(V_bar).

This is a finite calculation. With open subgroups specified by finite coset actions and a free basis, the required finite quotients can in principle be constructed by repeated mod-p Schreier calculations: in the dense abstract free group, repeatedly replace a finite-index free subgroup A by A^p[A,A], using its finite Schreier basis. Each quotient has known finite index, and coset equality is decided recursively by exponent sums modulo p in those bases. The resulting finite coset tables agree with the pro-p Frattini quotients. One may then enumerate all permutations of the finite group P and retain those preserving its multiplication table, compute the finite intersection, and pull it back. No efficiency bound or full implementation of this pro-p procedure is claimed.

The key lifting step uses freeness and the Frattini basis criterion. It would be unjustified to replace the induced automorphism group by all automorphisms of an arbitrary finite quotient.

## 4. The first two steps for an index-p pair

For U of index p, begin with V_0=U and apply c_F followed by c_U. Turn1's transitivity argument gives

    c_F(U)=Phi(F).

Next Phi(U)<=Phi(F)<=U. In the Schreier basis from Turn1, the map

    U/Phi(U) -> F/Phi(F)

sends x_1^p to0 and all p conjugates of x_i to the same e_i for i>=2. Its rank is d-1. Thus Phi(F)/Phi(U) is a proper subspace of U/Phi(U), of dimension D-(d-1), where D=1+p(d-1). Aut(U) induces all GL_D(F_p). The intersection of all linear images of a proper subspace is0: for any nonzero vector, some invertible linear map moves it outside that subspace. It follows that

    c_U(Phi(F))=Phi(U).

This is an exact initial descent, not a proposed formula for all later stages.

Let W_t be the chain sampled after each full cycle c_F then c_U. Each W_t is nontrivial and open. No equality W_{t+1}=W_t is possible: all intermediate terms are nested, so equality after a whole cycle would make W_t characteristic in both F and U; Turn1 rules out such an open subgroup. Therefore [F:W_t] tends to infinity, at least by a factor p at each cycle. This does **not** imply that the limiting common core is trivial.

## 5. The precise remaining convergence question

For the family in Section2, its limit C equals1 if and only if

    for every k>=1, there exists t with V_t <= Phi^k(F).

The reverse direction uses intersection_k Phi^k(F)=1. For the forward direction, if no V_t were contained in an open Phi^k(F), the compact sets V_t intersect (F minus Phi^k(F)) would be nonempty, decreasing and closed. Compactness would give an element of C outside Phi^k(F), contradicting C=1. The Frattini neighborhood-basis fact is the credited Proposition3.10(b) of Barnea et al.

So the missing statement is cofinality with **every** Frattini depth, not merely a growing index. For comparison, the characteristic open groups

    A_t=preimage(p^t Z_p^d) under F -> F_ab

have indices p^{td} tending to infinity but intersection equal to the nontrivial closed derived subgroup of F. This comparison chain is not claimed characteristic in U; it proves only that unbounded indices do not justify the desired inference.

Also, a finite family selected from a single characteristic chain, such as F,Phi(F),...,Phi^k(F), can never answer the question: its smallest member is nontrivial, contained in all the others, and characteristic in them by transitivity. This rules out a common overly simple construction, but does not rule out the nonnested index-p pair.

## 6. Checks and scope

verify_turn2.py exhaustively computes characteristic cores and maximal common characteristic subgroups in several small finite groups, comparing the cyclic iteration with a direct subgroup enumeration. It also checks the exact finite-vector-space dimensions in Section4. These finite analogues test the operator logic; they are not finite quotients on which all source automorphisms automatically descend, and they do not settle the infinite intersection C.

Original unresolved, 2/5. The computable finite steps and the exact cofinality criterion make the remaining gap explicit rather than hiding it in an assumed stabilization or compactness inference.
