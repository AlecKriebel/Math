# Independent adversarial derivations — record 23578142

Completed 2026-11-15 UTC. This develops the paper-only mechanisms sealed in `INITIAL_RECONSTRUCTION.md`, before foreign bodies or supplied code were opened. It is a verification of the complete literal theorem, not an extension or replacement of it.

## 1. Category, quantifiers and full-prefix dependence

Fix an arbitrary positive integer r. P is an ordinary, unweighted, locally finite N-graded poset with one minimum, finite ranks P_j, and the integer counting identity DU−UD=rI at every rank (including rank zero). An edge is a covering relation, not a weight or a multiple edge. The corresponding degree identities are u(x)=d(x)+r and common-upper-count(x,y)=common-lower-count(x,y) for distinct same-rank x,y. The argument is not an identity only modulo a prime, nor a statement about arbitrary three-layer commuting matrices.

For completeness, common-cover counts are at most one. If a pair x,y had two distinct common lower covers v,w, then v,w would have two common upper covers x,y and hence two common lower covers. Repeating downward contradicts the singleton rank zero (or choose a minimal-rank offending pair). A pair with two common upper covers first yields two common lower covers, so is excluded as well. This uses the whole downward prefix, not just two middle commutators.

Every element has an upper cover since r>0. Write B_j for the bipartite cover graph between P_{j−1} and P_j, with both ranks retained. B_1 is a star. If B_{j−1} is connected, its paths connect any two P_{j−1} vertices by pairs with a common lower cover; each such pair has a common upper cover in P_j. Hence all P_{j−1} vertices are in one component of B_j, and every P_j vertex has a lower cover. Thus B_j is connected for all j≥1. No minimum-degree-two hypothesis is used: B_1 has degree-one vertices, including the r=1 one-edge case.

## 2. Exact edge, cycle and slack identities

Put p_j=|P_j|, e_j=|E(B_j)|, and b_j=β(B_j). Summing u=d+r over P_{j−1} gives e_j=e_{j−1}+rp_{j−1}, with e_0=0. Therefore

    e_j = r Σ_{k=0}^{j−1} p_k,
    b_j = e_j − p_{j−1} − p_j + 1.

The second equality uses connectivity, already proved. For n≥2 set

    U_n = 1 + r Σ_{k=0}^{n−2}p_k + (r−1)p_{n−1}.

Direct substitution, with no inequality or asymptotics, gives

    p_n = U_n − b_n,
    b_n − b_{n−1} = r p_{n−1} + p_{n−2} − p_n,
    U_n − (r p_{n−1}+p_{n−2}) = b_{n−1}.

Thus nonnegativity of b_n is exactly Byrnes's cumulative bound; general monotonicity b_n≥b_{n−1} would be the stronger local recurrence. Nonnegative graph cycle rank alone proves no such monotonicity.

## 3. Correct supported graph and all isolates

Fix n≥2, Z=P_{n−2}, X=P_{n−1}, Y=P_n. Let

    S = {z∈Z : some a∈X has its entire lower-cover set equal to {z}}.

A singleton successor refers to a's lower-cover set; it does not say that z has only one successor. H_S has vertices S ⊔ X, including every X isolate, and edges z—x for z∈S below x. Set q=β(H_S)=|E|−|V|+c. Consequently

    q = Σ_{z∈S}(u(z)−1) − |X| + c(H_S).

The full previous graph B_{n−1} is connected, but H_S need not be. Since the cycle space of a subgraph injects into the full graph's cycle space, 0≤q≤b_{n−1}. Adding or deleting isolated vertices does not change β, but the displayed component formula must use consistent vertex and component sets. In particular S=∅ gives |X| isolated vertices, c=|X| and q=0.

## 4. Actual witness trees and simultaneous compatibility

Choose independently any singleton witness a_z over each z∈S. Put N_z={x∈X:z<x}. For each y∈N_z−{a_z}, the pair a_z,y has exactly one common lower cover z, and hence exactly one common upper cover t_z(y)∈Y.

If a nonsingleton t covers a_z, every other lower cover y of t shares a lower cover with a_z. Since pred(a_z)={z}, y∈N_z. The sets pred(t)−{a_z}, over nonsingleton t covering a_z, form a disjoint partition of N_z−{a_z}: existence follows from t_z(y), and two occurrences would give the pair a_z,y two common upper covers. Therefore the graph T_z consisting of all these complete stars and all terminals N_z is a tree, possibly the one-vertex tree if |N_z|=1. Omitting any edge of a chosen star or adding a nonterminal would invalidate this conclusion; the construction uses the actual whole predecessor sets.

For z≠w, no upper vertex can belong to both T_z and T_w: it would cover distinct a_z,a_w with disjoint singleton predecessor sets, which is forbidden by the off-diagonal identity. Thus different T_z have disjoint internal vertices and can meet only at terminals in X. This simultaneous compatibility is the central issue; separate per-center trees would not alone prove the theorem.

Let K be their union with all of X, including isolates. K is an actual subgraph of B_n. Replacing each z-centered star of H_S by T_z preserves connections among terminals. If T_z has k_z internal vertices, both edge count and vertex count change by k_z−1. Disjoint internal vertices make these counts additive. The components therefore agree and β(K)=β(H_S)=q. Subgraph cycle-space inclusion gives b_n≥q. Combined with section 2, this proves every asserted upper bound for every r and n in the stated category, with arbitrary witness choices.

## 5. Independent common-contraction proof

There is another exact way to see β(K)=β(H_S), without relying on a drawing or informal replacement. In H_S contract every edge z—a_z. These edges are a matching, so form a forest. The result is a graph on X whose remaining edges, with their original labels, are a_z—y for each (z,y) with y∈N_z−{a_z}.

In K contract every edge a_z—t for t internal to T_z. The union of these contracted edges is a disjoint union of stars (internal vertices are disjoint and witnesses distinct), hence a forest. Every remaining edge y—t becomes y—a_z for the unique t_z(y). The two resulting graphs are the same labelled graph on X, including isolates. Contracting forest edges preserves components and cycle rank. This proves the same equality for one-terminal trees, disconnected H_S and arbitrary witness choice as well.

## 6. Independent explicit cycle-chain injection

The theorem also has a checkable cycle-space map. Work over an arbitrary field F; this is a graph statement and does not reinterpret the defining integer poset axioms modulo F. Orient H_S edges z→x and B_n edges x→t. A cycle c has coefficients c_{z,x}, with zero sums at every z and every x. Since a_z has only the neighbor z in H_S, c_{z,a_z}=0.

Define, linearly on a cycle,

    Φ(c) = Σ_{z∈S} Σ_{y∈N_z−{a_z}}
              c_{z,y} ( [a_z→t_z(y)] − [y→t_z(y)] ).

The boundary of each parenthesis is y−a_z. The coefficients at ordinary X terminals sum to zero by the X equations for c; the additional coefficient at each a_z is −Σ_y c_{z,y}=0 by the z equation. Boundaries at internal upper vertices cancel within each parenthesis. Thus Φ(c) is a cycle in B_n.

The coefficient on the actual edge y→t_z(y), for y≠a_z, is precisely −c_{z,y}. No other center uses the same internal vertex, and within one tree that nonwitness terminal occurs in exactly one block. That edge also cannot be the witness edge for another center. Hence Φ(c)=0 forces every nonwitness coefficient to vanish, and all witness coefficients were already zero. Φ is injective. It follows directly that dim Z_1(B_n)≥dim Z_1(H_S)=q. This proves the full inequality without finite sampling. The sign is essential in odd characteristic; the independent F_3 control deliberately replaces the minus sign by a plus sign and detects a nonzero boundary on a genuine positive-q example.

## 7. Conditional local recurrence and exact equality category

If every z∈Z has a singleton successor, then S=Z and H_S=B_{n−1}. Thus q=b_{n−1}, so p_n≤r p_{n−1}+p_{n−2}. If rank n−1 was formed by Wagner reflection, it contains r singleton successors over each z; the next rank n may be any admissible extension.

For the stated equality theorem assume n≥3 and at least two distinct singleton successors over every z. Under equality b_n=b_{n−1}=β(K), K is connected and contains all X. Adding an unused upper vertex with all d(t) of its incident edges adds d(t)−1 to cycle rank. Since d(t)≥1, equality forces every unused upper vertex to be singleton.

Fix z, chosen witness a=a_z, and a different singleton witness b. Every nonsingleton upper t covering b must lie in K. If t belonged to T_w with w≠z, b and a_w would have a common upper cover despite disjoint singleton predecessor sets. Therefore t lies in T_z and covers a. For any y∈N_z−{b}, the unique common upper cover of b,y is such a t, and also covers a. It is the unique common upper cover h of a,b. Thus h covers all of N_z. Since n≥3, z has a predecessor and |N_z|=d(z)+r≥2; h is nonsingleton. No second internal vertex can coexist with h in T_z, because it would duplicate a pair a,y. The h_z are distinct across z.

Each x∈X belongs to d(x) neighborhoods N_z. Those h_z account for d(x) of its d(x)+r upper covers; all remaining covers are singleton, exactly r over x. This is precisely reflection, up to relabelling the upper rank. Conversely reflection has |Z|+r|X| upper vertices, so equality holds. This verifies the theorem under its actual sufficient hypothesis. No necessity or optimality of the two-witness hypothesis is claimed or needed; this review does not seek a stronger replacement theorem.

For rank one, there are r elements and each has r+1 upper covers. At z, every nonsingleton upper uses a nonempty subset of the other r−1 elements, and these subsets are disjoint by common-cover uniqueness. There are at most r−1 such uppers and at least two singleton successors. This is exactly the established Gaetz–Venkataramana Proposition 3.4 input. Therefore for every r≥1, p_3≤r p_2+r, with equality exactly for reflection from rank two.

## 8. Infinite realization and sharp coefficient, not just finite counts

Given any valid finite ordinary prefix through rank m≥1, add one upper vertex with predecessor set N_z for every z∈P_{m−1}, and r distinct singleton upper vertices over every x∈P_m. Each x receives d(x)+r upper covers, and each pair receives as many common upper covers as it has common lower covers. Every new vertex has a predecessor and each new rank is finite. Iterating, with no changes to earlier ranks, gives an infinite ordinary differential poset. This elementary verification matches Stanley Proposition 6.1; it is not an unsupported assumption about extending an arbitrary locally commuting triple.

For r=3, Y^3 through rank two has one pair vertex over each pair of the three rank-one elements and two singleton vertices over each, giving (1,3,9). Reflect once: p_3=3+3·9=30, e_2=3(1+3)=12 and e_3=3(1+3+9)=39, so b_2=b_3=q_3=1. U_3=31. The bound U_3−q_3=30 is attained, and this prefix extends indefinitely by reflection.

For r=1, Young's lattice through rank five has (1,1,2,3,5,7). Two reflections give 12 and 19. Here e_6=19, b_6=19−7−12+1=1. Reflection creating rank six makes S all of rank five; hence q_7=1, and the next reflection gives b_7=1. U_7=20, with the attained upper rank 19. Again this is an actual infinite-poset prefix.

For either example q=1 and p_n=U_n−q. Every universal coefficient c>1 in U_n−c q would give a strict false upper bound. The result is coefficient sharpness for the stated formula, not a claim that the formula is the optimal bound obtainable from arbitrary preceding incidence information. These are classical reflected Young prefixes, not new poset families.

## 9. Boundary cases and remaining allowance

b_1=0 and no b_0 is required. At n=2, S consists of the minimum, H_S=B_1 is a star and q_2=0. Thus p_2≤r^2+1. If r=1 the witness tree has one terminal and no internal vertex, so the degenerate-tree argument remains valid. For S=∅ the cycle correction is zero, regardless of how many X isolates there are.

Always the unremoved allowance is exactly b_{n−1}−q_n≥0. Young's lattice at n=6 gives b_5=1, q_6=0, U_6=13, local proposed bound12 and actual rank11. This is an example of a strict residual allowance, not a counterexample to the local recurrence. The general recurrence would still require b_n≥b_{n−1}, which this theorem does not claim. A global Fibonacci-envelope improvement or a combinatorial strict-growth proof also does not follow. The strict-growth convention must retain the r=1, p_0=p_1 exception.

## 10. Meaning and limits of the exact diagnostics

`independent_cycle_controls.py` was written and first run before the supplied checker body was successfully personally read. It builds Young products and reflected prefixes with its own partition/corner incidence construction, validates every integer commutator including rank zero, computes graph components by disjoint sets, and separately computes cycle kernels and the explicit Φ images over F_2 and F_3 by elimination. It verifies actual witness stars, internal disjointness, full subgraph inclusion, forest-contraction labels and injectivity. All witness products up to32 are exhausted; otherwise first, last and a rotating choice are checked. Its universal arbitrary-choice justification is sections4–6 above, not the selected samples.

The final two modes each check seven fixtures,23 rank interfaces,166 field/map instances and five positive-q interfaces. They reproduce both sharp attained examples and the Young residual. Invalid full prefixes, a removed top vertex, wrong r and a forced internal collision are rejected; an incorrectly signed path is detected over F_3. The relaxed (1,3,3,7) example satisfies both middle commutators for r=1 but fails at rank zero. All these tests are finite diagnostics, and none proves the general recurrence or substitutes for the all-rank proof.

The unchanged native `verification/exact_checks.py` was fully read, then copied and executed alone in an isolated directory. It partitions the required pair-edge graph into clique blocks, filling residual allowed incidences with singletons. Selecting the least uncovered edge determines its block, so the recursion enumerates labelled block multisets once; it is not an isomorphism enumeration. The full14748-byte expected output, including all example records and negative-control fields, is identical in normal, -O and -OO runs. The recorded5764 witness choices retain exactly the manuscript's cap/first-last selection convention. No builder, old package-wide campaign, original historical checker or publication routine was executed. The arbitrary-rank result rests on the proof above.
