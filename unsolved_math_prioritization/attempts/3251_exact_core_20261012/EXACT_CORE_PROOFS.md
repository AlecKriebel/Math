Editorial note: The complete authored proof or audit is preserved below. The clearly labeled representation-size correction supersedes two false historical complexity sentences and qualifies the earlier acceptance. Other changes replace only operational artifact identities, byte counts, locations and original replay directions. All mathematical arguments, exact finite scopes and substantive limitations remain. This edition's public manifest identifies the distributed prose.

# Exact high-incidence-core extension and signed tree obstructions

## Status and definitions

This is one component of the fourth substantive pass for problem 3251 / ordered row 1753. The unrestricted odd-hole-free 2-divisibility conjecture remains unresolved. The results below are exact extension reductions and necessary conditions, not a counterexample or a complete solution. No novelty claim is made.

All graphs are finite and simple. A division of a graph with clique number k>=2 is a two-coloring without a monochromatic maximum k-clique. Maximum means maximum cardinality. For k>=3 let M be the family of distinct maximum cliques, let d_M(v) count occurrences in this original family, and put X={v:d_M(v)>=3}. Throughout, P contains X. The incidence condition is never silently recomputed after deleting vertices or edges.

The accepted boundary-extension theorem and mixed-constraint lemma, the accepted core addendum, and the sharp chromatic-order theorem are mandatory identified dependencies listed in [dependencies](DEPENDENCIES.md). Their proofs have been read in full. The elementary statements below use no odd-hole-free assumption until Section 4. In particular, the clique shadow is never asserted to inherit odd-hole-freeness.

## 1. Exact propagation criterion

Prescribe any coloring alpha of P. Maintain these prescribed colors and apply the following procedure to the original maximum cliques.

1. A clique already meeting both colors is satisfied and never needs attention again.
2. If every vertex of a clique is assigned the same color, report a conflict.
3. If exactly one vertex of a clique is unassigned and its other vertices all have the same color c, assign the remaining vertex color 1-c. Record that clique as its creator.
4. Repeat until a conflict occurs or no rule applies.

All cliques have k>=3, so the reference to the color of the other vertices is unambiguous. The same statements hold for a finite family of distinct sets of sizes at least three, if each vertex outside P belongs to at most two sets.

**Theorem 1 (exact extension).** The coloring alpha extends to a division if and only if exhaustive propagation terminates without conflict. Any exhaustive order of the applicable rules is valid.

**Proof.** Each forced assignment is necessary in every extension of the assignments already made. Consequently any reported conflict proves that alpha has no extension.

Suppose instead that propagation is exhausted without conflict. Discard every satisfied clique. Delete the assigned vertices from every remaining clique. Each residual set has at least two vertices: size zero would be a conflict and size one would be another applicable rule. Give a residual set demand B when its original clique has no assigned vertex, and otherwise the one-sided demand forbidding the single assigned color present in that original clique. Every residual vertex lies outside P and has incidence at most two, counted by original clique occurrences. A residual B set still has its original size k>=3. In particular, every size-two residual set is one-sided.

The accepted exact mixed-constraint lemma states that a family with all edge sizes at least two and vertex incidence at most two is unsatisfiable precisely when it contains an all-B pure odd-cycle component. No such component is possible here, since none of the size-two edges is B. The lemma therefore supplies a residual coloring satisfying every remaining demand. Combining it with the assignments already made gives a division extending alpha. This proves both directions for any exhaustive propagation order. The same reasoning only uses original edge sizes at least three in the stated nonuniform set-family variant. QED.

This strengthens the sufficient criterion that alpha have no monochromatic (k-1)-clique. It handles exactly the otherwise unresolved singleton residuals. The criterion decides whether a specified core coloring extends; it does not guarantee that a successful core coloring can always be chosen.

Given the explicit maximum-clique list, propagation can be implemented with incidence lists and a queue, updating each incidence only when its vertex is assigned. Its work is O(n+L), where L is the total number of listed clique incidences. The accepted constructive mixed lemma supplies a completion in the same linear-incidence scale. Enumerating all assignments on X consequently gives an O(2^|X| (n+L)) decision algorithm after M and X have been supplied. This is an input-list statement: enumerating maximum cliques of an arbitrary graph is not claimed to be polynomial in the graph's order or encoding length.

## 2. Complete finite tree certificates for failure

A selected nonempty subfamily F of M is a P-tree if every vertex outside P that occurs in F belongs to exactly two members of F, and the multigraph T with node set F and one edge for each such vertex, joining its two containing cliques, is a tree. A tree here is connected and has no cycles; parallel edges would make a two-cycle and are excluded by the tree condition. A one-node P-tree is a clique contained entirely in P.

Choose either bipartition label sigma: F -> {0,1} of T. The prescribed coloring alpha matches the signed P-tree when

    alpha(x)=sigma(Q) for every Q in F and x in Q intersect P.

Empty intersections impose no requirement. Thus no prescribed vertex can belong to nodes on both sides of this bipartition in a matching certificate. Extra edges of the original graph, and maximum cliques not selected in F, are not deleted or disregarded as graph-theoretic assumptions.

**Theorem 2 (tree obstruction characterization).** The prescribed coloring alpha fails to extend if and only if a matching signed P-tree exists. If it fails, one can obtain such a tree directly from a propagation run, with at most |V(G) minus P|+1 clique nodes, and at most |M| nodes.

**Proof, extraction.** By Theorem 1, an exhaustive run encounters a fully assigned monochromatic clique R. Opposite demands on a single vertex can be treated in this form: apply the first forced color, and the other demanding clique becomes fully monochromatic. If R lies entirely in P, take the one-node tree.

Otherwise start with R. Whenever a chosen clique contains a vertex v outside P whose color was forced earlier, include the creator clique of v, unless this is the clique that itself created v. Continue backward through the finite recorded assignments. Each creator creates only one vertex: at the moment it forces that last vertex, the clique becomes satisfied forever. Every chosen creator other than R has its created vertex used in a later chosen clique. Since that vertex lies in at most two original maximum cliques, it can be used in at most one other chosen clique.

All other outside-P vertices of a chosen creator had already been assigned when it acted. Recursively including their creators ensures that every outside-P vertex occurring in the chosen family appears in both its creator and its unique later consumer. No other selected occurrence is possible. Direct each such edge from creator to consumer. Every selected node except R has exactly one outgoing edge; R has none; creation times strictly increase along each directed edge. The selected ancestor graph is connected to R and acyclic. It is therefore a tree. In particular, this argument also rules out parallel selected edges. Its t nodes have exactly t-1 distinct outside-P vertices, giving t<=|V(G) minus P|+1; all nodes are distinct members of M, giving the other bound.

Label R by its conflict color. Label each other selected clique by the common color of its vertices just before it forced its last vertex. An edge from a creator Q to its consumer Q' carries the color opposite the label of Q, and it belongs among the equally colored inputs of Q' (or the conflict clique R). Hence the labels at its ends are opposite. Every prescribed vertex of a selected clique has the label of that clique. These labels are the required sigma, proving extraction.

**Proof, obstruction.** Conversely root a matching P-tree at any node R. A leaf different from R has exactly one outside-P vertex, its edge to its parent, since every such vertex is represented by an incident tree edge. Its other k-1 vertices lie in P and all have color sigma(leaf). It therefore forces its parent-edge vertex to the opposite color, namely the parent's sigma. Remove that leaf conceptually, keeping the forced color. At every later node, its child-edge vertices have been forced to its own sigma, as have all its prescribed vertices. Thus it forces its parent-edge vertex to the parent's sigma. Continuing inward makes all vertices of R equal to sigma(R), a conflict. The same inward induction works for nonuniform sets of sizes at least three. No satisfying extension can exist. QED.

A nontrivial obstruction tree has at least two leaves. Each leaf supplies a monochromatic (k-1)-clique in P. Leaves on opposite bipartition sides supply differently colored, hence disjoint, such cliques. Leaves on the same side may share prescribed vertices, so this statement must not be promoted to two disjoint cliques without the parity hypothesis. The one-node obstruction is exactly an already monochromatic maximum clique in P.

## 3. An exact constraint system on the core, and its limitation

Set P=X. For every X-tree F and either tree bipartition (A_F,B_F), collect the core vertices appearing in its two parts into S_F and T_F. Trees with S_F intersect T_F nonempty cannot match any coloring and may be discarded. For every remaining tree, forbid the two patterns

    all S_F color 0 and all T_F color 1;
    all S_F color 1 and all T_F color 0.

Empty sets are interpreted vacuously. These are two complementary signed clauses on original core vertices. Theorem 2 proves that this constraint system is exactly equivalent to extendability. It includes the one-node constraints from maximum cliques wholly in X. Editorial correction: the original exponential-size assertion is superseded by the [accepted complexity correction](COMPLEXITY_CORRECTION.md). The explicit system has at most 2|M| clauses and at most 2L literal occurrences; Theorem 1 is a linear-incidence separation procedure for a proposed assignment and returns a violated tree when one exists.

This is a color-constraint reduction, not an induced-subgraph reduction. In particular, signed tree constraints are generally not the maximum-clique constraints of G[X]. Replacing them merely with a division of G[X] loses necessary constraints and is unjustified. The companion fourth-pass work provides an explicit connected chordal example of that failure; its independently frozen packet is separate from this packet and is not a runtime dependency or a premise of the results here.

## 4. Stronger necessary order and clique conditions on X

The accepted core theorem gives chi(G[X])>=2k-3 and omega(G[X])>=k-1 for every indivisible graph with k>=3. Put q=chi(G[X]) and r=omega(G[X]); necessarily r is k-1 or k. The accepted sharp chromatic-order theorem says that when q>r and G[X] has no induced C5,

    |X|>=2q-r+2.

For an odd-hole-free graph G, its induced graph G[X] is indeed C5-free. For k>=4 we have q>=2k-3>k>=r. Therefore

**Corollary 3.** Every odd-hole-free indivisible graph with k>=4 satisfies |X|>=3k-4. If omega(G[X])=k-1, then |X|>=3k-3.

These follow respectively from r<=k and r=k-1. At the unresolved k=4 frontier the general bound is **eight high-incidence vertices**, strengthening the earlier bound six. The case r=3 would give nine but can in fact be excluded entirely as follows.

**Corollary 4.** If G is odd-hole-free, indivisible, and omega(G)=4, then omega(G[X])=4, without any induced-minimality assumption.

**Proof.** If omega(G[X])<=3, the K4-free odd-hole-free four-colorability theorem of Chudnovsky, Robertson, Seymour and Thomas gives chi(G[X])<=4. This contradicts the accepted lower bound chi(G[X])>=5. Thus X contains a maximum K4. QED.

The four-color theorem is an external theorem dependency, already source-checked in the accepted maximum-clique-hypergraph audit. This packet does not re-audit its full proof. The exact inspected author PDF is https://thomas.math.gatech.edu/PAP/k4free.pdf (217,207 bytes, SHA-256 2e57b496d24fbc04db44d9efc900f3eb5af4843c9f42adadc5e376837be4b504), *K4-free graphs with no odd holes*, JCTB 100 (2010), 313-331, Theorem 1.3. Corollaries 3 and 4 are necessary conditions; they do not assert an indivisible odd-hole-free graph exists.

## 5. Prior-work and dependency boundary

Qiming Hu, Baogang Xu and Miaoxia Zhuang, *Some properties of minimally nonperfectly divisible graphs*, https://arxiv.org/abs/2603.01967v2, Section 4, already provide relevant minimally non-2-divisible no-basin, minimum-degree, clique-cutset trace-incompatibility and blocking-clique reductions. Those are prior-credit inputs to the overall research frontier; no novelty is claimed for them or for the results of this packet. The inspected source is a preprint. Its restricted statements about minimally nonperfectly divisible graphs cannot be substituted for unrestricted 2-divisibility or clique-cutset closure.

The general conjecture remains open within this work. Neither a shadow-graph odd-hole inheritance claim, nor perfect divisibility, nor an unrestricted clique-cutset closure theorem is used. The arithmetic consequences in Section 4 use original maximum-clique incidences and the induced graph on X only.

## 6. Reproducibility and limits

The original mandatory-input record fixes the finite scope; its expected-results record fixes exact totals and deterministic case-stream hashes. The exhaustive uniform-family universe consists of all 1,078 rank-tagged simple uniform hypergraphs with 3<=r<=n<=5, including empty families separately for each rank. Every partial coloring whose unassigned vertices have incidence at most two is tested: 90,569 cases, of which 35,334 fail extension. The graph universe contains all 1,100 labeled simple graphs of orders zero through five; its 660 graphs of clique number at least three supply 149,013 eligible partial colorings, of which 15,402 fail. Returned graph certificates have one node in 15,372 cases and two in 30 cases. Abstract uniform-family cases include tree certificates through four nodes. Longer abstract fixtures are paths on 2 through 9 nodes at ranks 3, 4 and 5, and rank-r stars with r leaves; both global core colors give 54 failed cases. Every one-core-vertex color flip is checked as a successful repair. These abstract fixtures are not asserted to be exact graph maximum-clique families. Arithmetic checks cover both possible core clique numbers for 4<=k<=30 (54 cases). The checker independently enumerates all full colorings to test extendability, checks propagation and every extracted tree certificate, and checks exact graph clique reconstruction. Explicit longer paths and branching trees exercise nontrivial certificate depths and nodes with no precolored vertices. These are bounded regressions supplementary to the all-size proofs.

The original replay requires four mandatory inputs: the packet directory, a separate external pin, the externally retained digest of that pin, and the dependency root. The external pin fixes the manifest, which fixes the complete original packet. The verifier rejects altered or missing dependencies, unexpected packet files/directories, symbolic-link path components, duplicate JSON keys, incorrect scope, and missing arguments. Normal Python, -O and -OO must have identical results; no acceptance gate uses assert. External receipts report actual replays and hostile controls without altering the sealed packet. This prose edition does not distribute the original programs, input records or replay receipts.

The integrity boundary is a static filesystem snapshot with an externally retained pin. It does not certify protection from concurrent hostile filesystem races, exhaustive malformed-input attacks, or simultaneous replacement of every external trust anchor. No remote repository, queue, or publication is changed.
