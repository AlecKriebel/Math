# Independent adversarial review: explicit constructions and ambient fusion

Checkpoint: **2026-10-24 17:30:37 UTC**. Review completion estimate: **100% for the claims and checks recorded here**. This is supplemental to `constructions_solvable_review.md`; it does not repeat the kernel proof. The unrestricted discovery task remains incomplete, and this is not a solution, originality certification, or publication recommendation for Kourovka 21.136.

Materials inspected: Sections 2-4 of `../approach_constructions.md`, the entire `../construction_artifacts/verify_tree_support.py`, and its recorded `tree_support_checks.json`. The subsequently proposed abelian torsion-subgroup lemma was independently checked from the parent's explicit proof proposal.

## Verdict

**PASS after one minor qualification:** in the coordinate-permutation argument, delete trivial factors before asserting that every coordinate orbit is finite. Nontrivial-factor coordinate orbits are indeed finite. An infinite family of trivial groups can be permuted arbitrarily without affecting continuity of the induced trivial base action, so the unqualified assertion literally has that exception. This correction does not affect the obstruction or any infinite-order example.

The affine obstruction, block-order coding, antichain odometer proof, and exact finite checker pass. The further lemma about an abelian torsion subgroup of unbounded exponent also passes, with its full proof in Section 5 below.

## 1. Affine fusion really occurs, but the whole group still fails the target hypothesis

Let B=Z_p additively and U=Z_p^times. In B semidirect U, conjugation of a translation by a multiplier multiplies its translation parameter by a unit or its inverse, depending on conjugation convention. Both have the same orbits. The nonzero parameters therefore form exactly one orbit for each nonnegative p-adic valuation. The translation subgroup alone has only countably many ambient infinite-order classes.

The projection onto U is an abelian quotient. Its value is invariant under conjugation in the full group. The subgroup 1+pZ_p for odd p, or 1+4Z_2 for p=2, has continuum many nonidentity elements and is torsion-free. Their lifts (0,u) are infinite order and pairwise nonconjugate whenever their multiplier coordinates differ. Thus the full affine group has continuum infinite-order classes.

A compact torsion group acting continuously on Z_p has image inside the finite torsion subgroup of U; its translation fusion orbits are consequently finite. No appeal to the finite generation theorem is used here. The argument is specifically about this scalar action and does not claim arbitrary closed-subgroup inheritance of the class-count hypothesis.

## 2. Compact coordinate-permutation actions have finite nontrivial coordinate orbits

Let B=product_i F_i, with F_i finite nontrivial groups. Suppose a compact group K acts jointly continuously on B by factor permutations together with transporting isomorphisms. Fix a target coordinate i, and consider the maps

    f_k : B -> F_i,  f_k(b)=pi_i(k.b).

The compact-open topology on the space C(B,F_i) is discrete. Indeed for any f, each fiber f^{-1}(a) is compact and clopen. The finite intersection, over a in F_i, of the compact-open requirements that a map send f^{-1}(a) into {a} consists of f alone.

The map k -> f_k is continuous. An elementary verification avoids any function-space theorem: for fixed k_0 and every b in B, joint continuity supplies a neighborhood U_b of k_0 and a neighborhood V_b of b on which f_k equals the fixed value f_{k_0}(b); shrink V_b into the corresponding fiber of f_{k_0}. Finitely many V_b cover compact B. Intersect the corresponding finitely many U_b. For every k in that intersection, f_k=f_{k_0} on all of B.

Its compact image in a discrete space is finite. Distinct nontrivial source coordinates give distinct maps to F_i, even after transporting isomorphisms: set only one source coordinate nonidentity and all others identity to distinguish them. Consequently only finitely many source coordinates can be sent to i, and the K-orbit of i is finite.

If trivial factors are allowed, discard them first. Their arbitrary index permutations act trivially on B, and their orbit finiteness cannot be inferred from continuity of that base action. This is the only correction required in the reviewed passage.

## 3. Block orders survive all semidirect-product conjugation

Group the nontrivial factors into finite K-orbits J. Each block B_J=product_{i in J} F_i is finite. Conjugation in B semidirect K of a base element acts on each block by a transporting automorphism followed by inner coordinate conjugations. It preserves the order of that block component.

For an element b of the base, uniformly bounded block orders imply finite order: if each order is at most M, the integer lcm(1,...,M) kills all components. Thus an infinite-order b has unbounded block orders. Select a sequence of distinct blocks J_n on which b has strictly increasing orders, all greater than 1. For every infinite subset S of the positive integers, retain b's full block component on J_n exactly when n is in S and use identity elsewhere. These elements have infinite order, because their nontrivial block orders are unbounded. Distinct supports differ in a block order (identity versus an order greater than 1), and hence cannot be conjugate even in the full semidirect product. Infinite subsets supply continuum many classes, with no continuum hypothesis.

For a direct product without K the same proof uses individual coordinates as blocks. If the base and K are both torsion, the semidirect product is torsion: a power of any element enters the base and another power is identity. If the base is torsion but K is a putative counterexample, the construction has merely retained a counterexample quotient; it has not generated a first counterexample by new fusion. These are the precise cases covered.

## 4. Rooted-tree antichain odometers and independent finite reproduction

For a prime p, the iterated cyclic wreath group W_p is closed in Aut(T_p) and is an inverse limit of finite p-groups. Truncating all local permutations after finite depth gives finite-order elements forming a dense subgroup. The standard odometer has order p^m at tree level m and hence infinite order in W_p.

The vertices v_n=1^n0 form an antichain for every p>=2. An odometer supported below v_n fixes the rest of the tree and the vertex v_n itself. Distinct supported odometers commute because their supports are disjoint. For any subset S of the nonnegative integers, the product g_S is well defined: at tree level m only indices n<=m-2 act nontrivially. These finite-level actions are compatible, so define an element of W_p. A nonempty support gives infinite order by restriction to any active subtree.

At level m, the active subtree at v_n has exactly p^(m-n-1) descendant vertices, and its odometer is one cycle of that length. All other vertices are fixed. Different n give different nontrivial lengths. Consequently, for 1<=j<=m-1, the number of cycles of length p^j is exactly 1 when m-j-1 is in S and is 0 otherwise. The fixed point count is

    p^m - sum_{n in S, n<=m-2} p^(m-n-1).

Any two distinct supports differ at an index n; level m=n+2 then distinguishes them by the number of cycles of length p. Conjugation by any rooted-tree automorphism conjugates the finite permutation at every level and therefore preserves its full cycle histogram. Thus the support witnesses remain nonconjugate in the larger ambient Aut(T_p), not only in W_p. No claim for arbitrary overgroups without the tree action is needed or proved.

### Exact checker audit

The author's script was rerun successfully: **170 permutations** passed for p=2,3,5. It constructs root-first words, increments the selected suffix with the root digit least significant, and compares the full cycle histogram with the stated formula. Simultaneous assignment of suffix digit and carry uses the old values correctly. The final carry is discarded, giving the required addition modulo p to the suffix length. Its cycle traversal is correct after its independent permutation/bijection check. There is no floating point arithmetic, random sampling, external algebra package, or unchecked numerical tolerance.

A separate implementation, `verify_tree_support_review.py`, was then written without using the author's digit-carry loop. It locates the unique possible antichain prefix by the first digit different from 1 and implements the odometer by wreath recursion on words. It checks complete histograms, bijectivity, exact agreement with every author's word image, and compatibility with restriction to the previous tree level. It also tests levels 0 and 1 and support indices too deep to act at the current level.

The independent check passed **1,396 support choices and 169,148 word images**, using p=2 through level 7, p=3 through level 5, and p=5 through level 4. Its output is `tree_support_independent_checks.json`. The author script SHA-256 for this run is `d5b41aee8d5179b8e74b0db48660bec9c022e787251bfebfe8cfbc2a6d4eaaac`.

These bounded computations independently reproduce the stated finite examples. The argument in the preceding paragraphs supplies the universal all-level proof; finite checks do not establish it on their own and do not solve the unrestricted Kourovka problem.

## 5. Further verified lemma: abelian torsion subgroups of unbounded exponent

> **Lemma.** If an arbitrary profinite group G contains an abelian torsion subgroup T of unbounded exponent, then G has at least continuum conjugacy classes of infinite-order elements.

Neither T nor its closure is assumed normal in G. T need not be closed. Let A be the closure of T, which is closed abelian by continuity of the commutator map.

For every open normal N in G, the subgroup T intersect N has unbounded exponent. Otherwise, if its exponent divided e, then the finite group T/(T intersect N), embedded in G/N, would have some finite exponent d. Every t in T would satisfy t^d in T intersect N and hence t^(de)=1, contrary to unbounded exponent of T.

Start with N_0=G. Inductively, after choosing b_1,...,b_{i-1} of respective finite orders m_1,...,m_{i-1} and open normal subgroups down to N_{i-1}, set

    E_i = lcm(i!, m_1, ..., m_{i-1}).

Choose b_i in T intersect N_{i-1} whose order m_i does not divide E_i. Such an element exists because that subgroup has unbounded exponent. Then b_i^(E_i) is nonidentity. Residual finiteness supplies an open normal N_i contained in N_{i-1} such that b_i^(E_i) is not in N_i.

For any subset S of the positive integers define q_k as the product of b_j over j<=k in S. These finite products are unambiguous because T is abelian. The nonempty compact cosets

    q_k (A intersect N_k)

are nested: the next factor is either 1 or b_{k+1}, and b_{k+1} lies in A intersect N_k. Compactness gives a point x_S in their intersection. The point need not be unique; uniqueness and convergence of an infinite product are not assumed.

In the finite quotient G/N_i the point x_S equals q_i. Every earlier b_j has order dividing E_i, and all chosen elements commute. Therefore the following exact equivalence holds:

    x_S^(E_i) is in N_i  if and only if  i is not in S.

If i is absent, all factors are killed by E_i. If i is present, q_i^(E_i)=b_i^(E_i) is not in N_i by construction. Normality of N_i makes this equivalence an ambient conjugacy invariant. Distinct subsets S consequently give nonconjugate x_S, regardless of which point of each compact intersection was chosen.

For infinite S the element x_S has infinite order. If its finite order were L, choose an index i in S with i>=L. Then L divides i! and hence E_i, so x_S^(E_i)=1, contradicting the displayed equivalence. There are continuum many infinite subsets S, proving the lemma.

### Exact scope and obstruction left over

Under the strict class-count hypothesis of 21.136, every abelian torsion subgroup must therefore have bounded exponent, with a bound allowed to depend on that subgroup. This is a necessary condition on a putative counterexample, not a bounded-exponent assertion about all torsion elements of G. The argument does not apply to arbitrary abelian subgroups: an infinite procyclic torsion-free subgroup supplies no unbounded-exponent torsion subgroup. It does not apply to an arbitrary nonabelian torsion subgroup either: the commuting factors were essential to the exact power test. No existence theorem producing a T of this kind inside every nontorsion profinite group has been proved.

## Final review status

All reviewed explicit mechanisms and finite calculations are correct with the trivial-factor qualification above. The further unbounded-exponent abelian torsion-subgroup lemma has a complete independent proof. No remaining substantive mathematical objection was found to these restricted statements. The original problem for all profinite groups remains unresolved, and no result here is marked solved_verified or published.
