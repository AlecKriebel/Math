# Independent arborescences with singly connected pairwise overlaps

Problem 3000044 / AMR-029-0044. Structural partial, 10 October 2026.

**Review status:** accepted as a structural partial by the accompanying [mathematical audit](MATHEMATICAL_AUDIT.md). This AI-assisted manuscript is unrefereed. Acceptance denotes that audit, not external human peer review, journal acceptance, or formal proof-assistant certification. The unrestricted conjecture remains unresolved.

## Result and limitation

The unrestricted question is **not resolved here**. This note proves a sufficient structural case with arbitrary roots, arbitrarily many prescribed sets through a vertex, parallel arcs, and arbitrarily long directed paths. It also supplies a polynomial local-matching characterization for that case, a recorded supplementary finite census, and a concrete obstruction to extending an arbitrary previously chosen independent prefix. The latter is not a counterexample to the original existence question. No novelty claim is made for the elementary structural lemma.

The strongest result below needs the additional structural assumption only on overlaps between indices with different roots. The self-contained base theorem first imposes it on every pairwise overlap. Delete the common root from that overlap when the two roots agree. After ignoring parallel-arc multiplicities, between any ordered pair of vertices of the remaining induced digraph there must be at most one directed path. We call this the **unique-overlap-path condition** below; this name only abbreviates the stated condition.

## Exact conventions

Let D=(V,A) be a finite loopless acyclic directed multigraph. Distinct parallel arcs remain distinct members of A. For indices i=1,...,k, let r_i be a vertex of a prescribed convex set U_i. Convex means that every directed path with both endpoints in U_i stays in U_i. Roots and prescribed sets may repeat. A path from a root to itself has length zero.

Put I(v)={i:v∈U_i} and J(v)={i∈I(v):r_i≠v}. Two paths ending at v are independent when they have disjoint arc sets and their vertex intersection is exactly {v}, together with their common root if their roots agree. The question's hypothesis selects one simultaneous independent path system for each v, with no initial consistency requirement between different terminals.

For i≠j put

X_ij=(U_i∩U_j)\{r_i} if r_i=r_j, and X_ij=U_i∩U_j otherwise.

The unique-overlap-path condition is that D[X_ij], with parallel arcs collapsed, has at most one directed vertex-sequence path between any ordered pair of vertices. The empty path causes no ambiguity in a DAG. In particular, the condition does not prohibit parallel arcs.

## A local bipartite graph

For every v let R(v)={r_i:i∈I(v)}. Define a bipartite graph B_v with left side J(v). Its right-side resources are:

1. One resource q_t for each distinct tail t∉R(v) of an arc t→v.
2. One resource q_a for each individual arc a=t→v whose tail t lies in R(v).

The left index i is adjacent to q_t precisely when t∈U_i. It is adjacent to q_a precisely when the tail of a equals r_i. Thus an active root is available as a predecessor only to its own root group, and each parallel arc leaving such a root is a separate resource.

A matching saturating J(v) selects a parent arc a_i(v) for each i∈J(v). For an ordinary-tail resource q_t use any one actual arc t→v; only one index uses that resource. For q_a use the actual arc a. The parent tail lies in U_i. The selected arcs at v are distinct. Moreover, if two selected parent arcs have the same tail, that tail is the common root of their indices.

### Lemma 1: necessity of these matchings

The question's simultaneous independent paths to v yield a matching saturating J(v) in B_v.

**Proof.** Use each nonzero path's last arc. Two such arcs cannot coincide. If two last arcs have the same tail t, the paths share t≠v, so their roots both equal t. If a last-arc tail t equals the root of some active index j with a different root, the i-path and j-path share t distinct from their permitted common terminal; this is impossible. A last-arc tail cannot equal v in an acyclic graph. All last-arc tails lie in the required prescribed sets by convexity. Consequently the last arcs use precisely the allowed distinct resources. ∎

This lemma requires neither the unique-overlap-path assumption nor a conclusion about coherent trees.

## Main structural theorem

**Theorem.** Suppose the unique-overlap-path condition holds. The following are equivalent:

(a) The original terminalwise simultaneous independent-path condition holds.

(b) Every B_v has a matching saturating J(v).

(c) There are independent r_i-out-arborescences F_i with vertex sets exactly U_i.

Furthermore, choose any saturating matching independently in every B_v, and use its selected parent arcs. The resulting F_i satisfy (c).

**Proof.** The implication (c)⇒(a) is immediate, and Lemma 1 proves (a)⇒(b). Assume (b), choose the matchings, and give F_i all the vertices of U_i and exactly the selected arc a_i(v) entering each v∈U_i\{r_i}.

All arcs have both endpoints in U_i. The root has indegree zero, every other vertex has indegree one, and F_i is acyclic because D is. Following predecessors backwards must terminate; it can terminate only at r_i. Thus every vertex is reached from r_i and F_i is an out-arborescence on exactly U_i. This argument includes singleton U_i. No original full paths are retained or assumed consistent.

The F_i are globally arc-disjoint: if an arc were used twice, its head v would have received the same parent arc from two indices, contrary to the matching construction. This fact alone does not prove vertex independence.

Fix i≠j and v∈U_i∩U_j. Suppose the root-to-v tree paths share a vertex w other than v and, when applicable, their common root. Consider their suffixes from w to v. Each suffix has both endpoints in each prescribed set, so convexity traps both suffixes inside U_i∩U_j. If the roots coincide at r, neither suffix can pass through r: the tree path already reaches w from r, and a return to r would give a directed cycle. Therefore both suffixes lie in X_ij.

By the unique-overlap-path condition, these suffixes have the same vertex sequence. In particular, their last arcs have the same tail t∈X_ij. These are exactly the two parent arcs selected at v. By the matching construction, equal tails are possible only when t=r_i=r_j. Such a vertex was removed from X_ij. This contradiction proves that no forbidden w exists. The required allowed common vertices occur automatically, and arc-disjointness was already established. Hence the trees are independent. ∎

### Hall form and construction time

Condition (b) is equivalently |N_{B_v}(S)|≥|S| for every v and every S⊆J(v). This is an ordinary bipartite-matching condition, not an invocation of Edmonds' arc-disjoint packing theorem as a vertex-independence substitute.

Given membership tables, the B_v have O(km) total adjacency-list size. Repeated augmenting-path matching uses at most k augmentations per terminal and gives the conservative bound O(k²m+kn) for testing (b) and constructing all parents. This bound does not include testing the structural assumption. That assumption is also polynomially checkable: collapse parallel arcs; for each pair i,j and each start vertex in X_ij, count directed paths in topological order with counts capped at two. This path-counting test uses integer counts capped at two.

## Stronger theorem: only different-root overlaps need the condition

The following refinement permits completely arbitrary overlaps among indices sharing a root. It explicitly uses the credited common-root DAG theorem, rather than claiming to re-prove that result as new work.

**Theorem 2.** Suppose that, whenever r_i≠r_j, the simple digraph obtained from D[U_i∩U_j] by collapsing parallel arcs has at most one directed vertex-sequence path between any ordered pair. No such restriction is imposed when the roots agree. Then (a), (b), and (c) in the preceding theorem are equivalent. Arbitrary local matchings suffice after a common-root reconstruction inside each root group.

**Proof.** Necessity is Lemma 1. Assume all the matchings exist and first assemble their parent arcs as before. These give rooted arborescences, though independence is not yet claimed. For each distinct root r let G_r={i:r_i=r}, V_r=⋃_{i∈G_r}U_i, and H_r be the graph on V_r containing all the selected parent arcs assigned to that group.

For v∈V_r\{r}, put g_r(v)=|G_r∩I(v)|. Exactly g_r(v) distinct arcs of H_r enter v. Every vertex of V_r is reachable from r in H_r, by the assembled parent arborescences. Parallel arcs in H_r can only leave r: a tail outside R(v) has only one matching resource, while a tail in R(v) is available only to its own root group.

We check the hypothesis of the established common-root theorem directly. Fix v≠r and write q=g_r(v). Let d be the number of H_r arcs directly from r to v, and remove these d arcs to obtain H'. If d=q, they already give q independent paths. Otherwise we claim that H' has q−d internally vertex-disjoint r-to-v paths.

By the directed vertex version of Menger's theorem (r and v are no longer adjacent), failure would give a set S⊆V_r\{r,v} of fewer than q−d vertices separating r from v. Let W be the vertices from which v is reachable in H', including v. For every w∈W\{r}, an r-to-w path in H_r followed by a w-to-v path is a path in D: a repetition would contradict acyclicity. Every prescribed set of this root group containing v therefore also contains w, by convexity. Hence g_r(w)≥q.

Choose the earliest vertex w of W\(S∪{r}) in a topological ordering that is unreachable from r in H'−S; such a w exists because v is unreachable. Every tail of an H' arc entering w lies in W. Any such tail outside S is either r or an earlier reachable vertex, which would make w reachable. Thus all incoming tails lie in S. None is r, so these arcs have distinct tails, and indeg_{H'}(w)≤|S|. On the other hand, if w≠v that indegree is g_r(w)≥q, and if w=v it is q−d. Both contradict |S|<q−d. This proves the claim by Menger. Adding the d distinct direct arcs gives q arc-disjoint paths whose only common vertices are r,v. Convexity keeps every one of these paths in every U_i of the root group that contains v.

The common-root theorem [Frank–Fujishige–Kamiyama–Katoh 2013, Theorem 4] now supplies independent trees for all indices in G_r, using only H_r and with their exact prescribed vertex sets. Its hypotheses hold because convexity is preserved under deleting arcs and the required paths have just been proved. Do this for each distinct root.

It remains to compare different groups. Their arc pools are disjoint. At each terminal v, the tails of parent arcs available to two different root groups are also disjoint: an ordinary-tail resource belongs to only one selected index, and an active-root resource belongs only to its own root group. For i,j with different roots, if the reconstructed paths to a common terminal v shared a vertex w≠v, their w-to-v suffixes would lie in U_i∩U_j by convexity. Unique directed vertex-sequence paths there would force equal penultimate vertices. That contradicts the disjoint predecessor-tail pools of the two groups. Thus paths from different groups are independent as well. ∎

The construction remains polynomial. Before applying the credited algorithm, remove singleton prescribed sets U_i={r_i} and restore their one-vertex trees afterward. A group containing only singleton sets needs no algorithm call. Every remaining pool H_r is weakly connected because every vertex is reachable from r, and all remaining prescribed sets are non-singleton. Thus the exact hypotheses of Frank–Fujishige–Kamiyama–Katoh 2013, Theorem 5 apply. Its O(|G_r||A(H_r)|) common-root algorithm has total cost at most O(km) across the disjoint pools, in addition to O(kn) membership/singleton preprocessing and the local matching work. The recorded supplementary implementation used the eligible-tree peeling construction with ordinary lists for auxiliary orders; no O(km) performance claim was made for that implementation. The polynomial bound here is the credited algorithmic theorem with the hypotheses just checked.

The equal-root restriction is genuinely removed, not silently assumed away. For example, start with the two-common-root diamond DAG used in the usual crossed-prefix obstruction, retaining two parallel arcs to each first-layer vertex. Add one new distinct source with only an arc to the final sink, and prescribe its set to contain just that source and sink. The first two sets may contain their entire diamond, while every cross-root intersection is a singleton. This has different roots and overlap three; Theorem 2 applies although the all-pairs base hypothesis fails.

## Corollaries and actual scope beyond the credited cases

1. The theorem applies when the underlying simple undirected graph of every D[X_ij] is a forest. It also applies to some overlaps with undirected cycles: uniqueness is directed, not undirected.
2. Under the original path hypothesis, the conclusion holds whenever D has no directed path of three arcs. Indeed, if two distinct vertex-sequence paths existed from w to v in X_ij, one would have at least two arcs. Since w is not a common root, at least one of r_i,r_j differs from w and has a positive-length path to w. Concatenating that prefix with the two-or-more-arc path would give a directed path of at least three arcs. Acyclicity ensures that the concatenation has no repeated vertices. Thus the structural hypothesis follows.
3. Arbitrarily large overlap and arbitrary depth really are allowed. Take distinct roots r_1,...,r_k, distinct private vertices p_1,...,p_k, and a shared chain c_1→...→c_l. Add r_i→p_i and p_i→c_j for every i,j, and set U_i={r_i,p_i,c_1,...,c_l}. These sets are convex, their pairwise overlaps are the whole chain, and paths r_i→p_i→c_j are independent for every shared terminal. For k≥3 this is outside both the common-root case and the overlap-at-most-two case. Directed paths can have l+1 arcs. The matching theorem constructs the required trees without bounding k or l.

The example only demonstrates the scope of the proved sufficient condition; it does not establish a new literature result by itself.

## A genuine failure of arbitrary-prefix extension

The following simple DAG has three distinct roots and overlap three. It satisfies the original hypothesis and has independent trees, but one particular independent prefix cannot be extended by adding the final vertex.

Roots are r_1,r_2,r_3. The remaining vertices are a,b,c,d,e,z. Arcs are

r_1→a, r_1→b, r_2→a, r_2→b;
a→c, b→c, a→d, b→d;
r_3→e;
c→z, d→z, e→z.

Set U_1={r_1,a,b,c,d,z}, U_2={r_2,a,b,c,d,z}, and U_3={r_3,e,z}. All are convex. On D−z take the first tree's paths to c,d through a,b respectively, and the second tree's paths to c,d through b,a respectively. Take the third tree's sole nontrivial prefix r_3→e. At a,b,c,d,e these prefix trees are independent.

Any extension to z forces the third tree through e. If the first two trees choose the same predecessor c or d, their paths share that predecessor. If they choose c,d respectively, both use a. If they choose d,c respectively, both use b. These are all four parent pairs, so the prefix is unextendable.

Nevertheless an independent full family is obtained by making the first tree use a to reach both c,d, the second use b to reach both c,d, and then choosing c→z for the first and d→z for the second. The third uses e→z. Thus every terminal has the required independent paths. This does not disprove the conjecture, but it rules out the proof shortcut that an arbitrary already independent prefix can always be extended at the next vertex. Its pairwise overlap contains two directed vertex-sequence paths a→c→z and a→d→z, so the structural theorem correctly makes no arbitrary-choice promise here.

The supplementary audit independently checked this prefix, rejected all four extensions, and verified a global family. The explicit argument above is independent of those checks.

## Recorded supplementary computation and its limits

The accompanying audit records exact enumeration of directed paths with distinct arc identities, including zero paths, and exact backtracking tests of the terminalwise hypothesis. The coherent solver assigned parents in topological order, maintaining previously completed root paths and backtracking when necessary. Exhaustion was finite nonexistence within a tested instance; there was no numerical optimization tolerance. A separate witness check reconstructed each returned family. Programs and raw outputs are not distributed in this proof-only edition, and edition preparation did not rerun these computations. The analytic verdict depends on no omitted executable.

All 2^10=1,024 simple DAGs whose vertex labels 0,...,4 are topological were considered. For each, every nonempty convex set reachable from its necessarily unique possible root (its least vertex) was enumerated, then every unordered triple with repetition was considered. Omitting unreachable rooted sets discards only instances already failing the hypothesis. Permuting the three indices does not affect the question. There were 504,836 triples; 149,344 had not-all-equal roots and a nonempty three-way overlap. Of these residual instances, 37,380 passed the original local hypothesis, and all 37,380 had verified coherent families. Every simple DAG on at most five vertices is represented up to a topological relabelling and isolated padding. This is bounded finite verification for three trees, not a proof for larger graphs, arbitrary k, or multigraphs.

The strengthened replay additionally checked local-matching equivalence and its constructed parents in 138,124 unique-overlap residual instances, including 36,002 locally feasible instances. It checked the depth-two statement in 63,024 residual instances, including 16,546 feasible ones. Explicit controls cover parallel root arcs, repeated roots, zero-length paths, unequal-root intersections, nonconvex sets, an overlap-three depth-four chain, and a forbidden diamond. The stronger different-root-only condition was replayed in 141,632 residual instances, including 36,002 feasible ones. In addition, 2,000 seeded eleven-vertex multigraph instances with repeated-root groups of sizes 2,3,4,5 and one further distinct root all produced independently checked trees; these stress the credited peeling implementation with arbitrary equal-root diamonds and parallel root arcs.

Seeded supplementary searches also found no counterexample: 300 random eight-vertex DAGs yielded 950 feasible sampled triples; 1,000 random ten-vertex DAGs yielded 3,125; 10,000 layered reachability-set instances with three distinct sources yielded 2,066. All yielded exact coherent witnesses. Eleven of the last group required backtracking, with at most 2,286 visited search nodes. These are sampled observations only. The audit records retention of programs and seeds at review time, but not the complete sampled populations or every witness. Those programs, seeds and raw outputs are not part of this edition.

## What remains

A general proof must handle overlaps between different-root groups containing alternative directed vertex paths while choosing all trees coherently. The last-arc matching condition remains necessary there but the proof that arbitrary local choices work is false, as the explicit prefix obstruction demonstrates. Neither the structural theorem, the finite searches, nor the obstruction establishes the unrestricted statement or its negation.

## Source attribution

The exact originating target is Question 2 in A. Frank, S. Fujishige, N. Kamiyama, and N. Katoh, *Independent arborescences in directed graphs*, Discrete Mathematics 313 (2013), 453–459, DOI https://doi.org/10.1016/j.disc.2012.11.006, author PDF https://andrasfrank.web.elte.hu/cikkek/FrankJ63.pdf. Its established cases include common roots in DAGs and arbitrary roots with overlap at most two. Theorem 5 gives O(km) for the former; Theorem 7 gives O(km) for the latter. General cyclic-digraph counterexamples do not answer the acyclic question. The base structural proof is self-contained; Theorem 2 explicitly uses the credited common-root theorem. These established results are not counted as new work.
