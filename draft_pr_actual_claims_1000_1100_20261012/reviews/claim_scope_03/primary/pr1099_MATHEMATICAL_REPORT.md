# Shortest round-trip orientation in mixed graphs

Problem 3000061 / AMR-029-0061. First substantive attempt, 10 October 2026.

## Status and scope

**Partial result. The general deterministic exact polynomial-time question is not resolved, and no NP-hardness reduction for the target is claimed.**

The accompanying independent mathematical audit accepts this scoped partial result. This AI-assisted manuscript is unrefereed; acceptance is not external human peer review, journal acceptance, or formal proof-assistant certification. No mathematical proof correction was required for this edition.

This note proves the following, with constructive orientation recovery and binary-rational arithmetic:

1. Exact decomposition at articulation vertices.
2. A general polynomially computable lower bound and a sound, sometimes successful optimum certificate.
3. A deterministic polynomial algorithm when each relevant underlying block contains at most one fixed directed arc.
4. A deterministic polynomial algorithm for two-terminal series-parallel mixed graphs given their decomposition, allowing arbitrary fixed arcs; the algorithm uses three scalar states per component.
5. An explicit four-vertex mixed family for which the lower bound has unbounded multiplicative gap and every feasible round trip repeats an undirected edge in the same direction.
6. A value-preserving equivalence with arbitrary two-pair mixed min-sum orientation.

These are authored proofs of restricted results and obstructions to specific approaches. No priority or novelty claim is made for these tractable cases or elementary reductions. In particular, none is a full answer to the EGRES question.

The model is a finite explicit mixed multigraph $G=(V,E,A)$. Each element of $E$ is an independently orientable undirected edge, and each element of $A$ has a fixed tail and head. Parallel elements retain separate identities. Each length is a nonnegative binary-encoded rational, possibly zero. The objective is

\[
\operatorname{OPT}(G;s,t)=\min_D\bigl(d_D(s,t)+d_D(t,s)\bigr),
\]

where $D$ ranges over completions of all undirected edge directions. Infinite distance means infeasibility; the whole digraph need not be strongly connected. For $s=t$, return value zero and any completion. Nonnegative loops can be deleted during optimization and assigned an arbitrary allowed direction on output. Henceforth $s\ne t$ and loops have been deleted.

A finite directed shortest walk can be made vertex-simple by deleting closed subwalks without increasing length, including when lengths vanish. Consequently every finite optimum has a witness consisting of a simple $s\to t$ path and a simple $t\to s$ path. The *two different paths* can share vertices and edges; any shared edge must have the same direction in both paths. Their concatenation need not be a simple cycle.

## 1. Articulation decomposition is exact

Let $U(G)$ be the undirected multigraph obtained by forgetting all fixed directions but retaining edge identities and lengths. Use its usual edge-block decomposition, with bridges treated as one-edge blocks and parallel pairs allowed to form a two-edge cycle block. The bipartite incidence graph of blocks and vertices is a forest after isolated vertices are handled separately.

If $s,t$ lie in different underlying connected components, the optimum is infinite. Otherwise let

\[
s=x_0,\ B_1,\ x_1,\ B_2,\ldots,\ B_k,\ x_k=t
\]

be the unique block/vertex route between them. These are the **relevant blocks**. Each $B_i$ retains its original fixed arcs and its undirected edges.

**Theorem 1.**
\[
\operatorname{OPT}(G;s,t)=\sum_{i=1}^{k}\operatorname{OPT}(G[B_i];x_{i-1},x_i).
\]
The sum is infinite if any summand is infinite.

**Proof.** A simple underlying $s$-$t$ path traverses precisely these blocks, in this order. Entering an off-route block would require returning through the same articulation vertex, contradicting simplicity. Similarly, re-entering a previously departed block repeats an articulation vertex. Thus, in any orientation, every simple directed $s$-$t$ path decomposes into directed $x_{i-1}$-$x_i$ paths inside $B_i$, and every simple return path decomposes into reverse-direction paths in those same blocks. Conversely such local paths concatenate to a global directed walk, whose length is their sum. This proves the distance decompositions for every fixed orientation, including infinite distances.

Distinct blocks have disjoint edge sets, so their undirected orientations can be chosen independently. Minimize each local round-trip sum independently and concatenate the witnesses. Orient all remaining undirected edges arbitrarily. This gives the asserted minimum and an output orientation. ∎

In particular, a relevant bridge makes the instance infeasible, whether that bridge was directed or undirected. Irrelevant blocks can contain any number or configuration of fixed arcs. The theorem reduces the substantive optimization question to underlying blocks; it does not solve general blocks.

## 2. A useful lower bound

Define
\[
L(G;s,t)=\min\{\ell(P)+\ell(Q): P,Q\text{ are edge-disjoint undirected }s\text{-}t\text{ paths in }U(G)\}.
\]
Set $L=\infty$ when no such pair exists, and $L(G;s,s)=0$.

**Lemma 2.** $L(G;s,t)\le\operatorname{OPT}(G;s,t)$.

**Proof.** Consider two finite directed paths witnessing a feasible orientation, and let $H$ consist of the distinct underlying edge identities they use. Every cut of $H$ separating $s$ and $t$ has at least two edges. If such a cut had just one edge, the outward and return paths would have to traverse that physical edge in opposite directions, impossible in an orientation. The edge version of Menger's theorem therefore gives two edge-disjoint underlying $s$-$t$ paths in $H$. Their total length is at most the sum of the lengths of all distinct edges in $H$, and hence at most the original two directed path lengths. Both inequalities use nonnegativity. Minimize over feasible orientations. ∎

### Exact polynomial computation and cycle-chain extraction

For each underlying nonloop edge $uv$ of length $w$, introduce separate network arcs $u\to v$ and $v\to u$, each of capacity one and cost $w$. Compute an integral minimum-cost flow of value two from $s$ to $t$.

This can be done by two successive shortest residual augmentations from the zero flow. The first network has nonnegative costs. Minimum-cost residual optimality ensures there is no negative residual cycle after an optimal augmentation. Thus exact shortest residual paths can be found by Bellman–Ford, also after negative-cost reverse residual arcs appear. If an augmentation fails, no value-two flow exists. This is the standard integral minimum-cost-flow argument; the requested value is two, not a binary-encoded large flow amount.

For completeness, the augmentation optimality argument is short. Given a minimum-cost integral value-\(k\) flow, its residual network has no negative cycle, since augmenting such a cycle would improve the flow without changing its value. The difference between any integral value-\(k+1\) flow and the current flow decomposes in the residual network into a unit source-to-sink path and circulation cycles. The cycles have nonnegative total cost, and the path costs at least a shortest residual path. Augmenting a shortest such path is therefore minimum-cost among value-\(k+1\) flows. If no residual source-to-sink path exists, the usual reachable-set cut rules out a greater flow value. Apply this for \(k=0,1\).

If both network arcs associated with one physical edge carry flow, cancel their common unit. This preserves balances and decreases cost by $2w\ge0$. Next repeatedly remove directed circulation cycles in the positive-flow support. This also preserves balances and never increases cost. Since the starting flow was minimum-cost, neither operation can lower its value below that optimum. The resulting support is acyclic and uses at most one direction of each physical edge.

Decompose this integral acyclic value-two flow into two edge-disjoint simple $s$-$t$ paths $P,Q$. The cost equals $L$: every physical edge-disjoint path pair was feasible in the network, and the cancellation procedure maps an optimal network solution back to such a pair without increasing cost.

Any common vertices of $P,Q$ occur in the same order on both paths. Otherwise the two directed subpaths between a reversely ordered pair of common vertices create a directed cycle in the support. List the common vertices as
\[
s=z_0,z_1,\ldots,z_r=t.
\]
Between consecutive common vertices, the two paths have no common internal vertex and have no common edge. Their union is a simple undirected cycle $C_i$, including a length-two cycle for parallel edges. The union is therefore a chain of edge-disjoint simple cycles, meeting only at consecutive articulation points within this support. Its length is $L$.

Each $C_i$ can be oriented cyclically in either direction. If all fixed arcs on $C_i$ agree with one cyclic direction, choose that direction. If every cycle passes this check, the resulting orientation contains an $s\to t\to s$ round trip of length $L$. Lemma 2 proves that the resulting directed distances sum to exactly $L$, even if extra unused edges create other paths. This is a sound optimum certificate on arbitrary mixed inputs.

**Crucial limitation:** when a cycle contains incompatible fixed directions, failure of this particular certificate means **unknown**, not infeasibility and not a hardness result. The counterexample in Section 5 makes this distinction necessary, even when $\operatorname{OPT}=L$.

## 3. At most one fixed arc per relevant block

**Theorem 3.** Suppose every relevant underlying block contains at most one fixed directed arc. Then
\[
\operatorname{OPT}(G;s,t)=L(G;s,t),
\]
and the algorithm in Section 2 returns an optimal orientation or correctly reports infeasibility in deterministic polynomial time.

**Proof.** If $L=\infty$, Lemma 2 implies infeasibility. Otherwise use the acyclic minimum-cost flow and its simple-cycle chain. Each simple cycle lies within one underlying block, and all its edges lie on underlying $s$-$t$ paths, so this is a relevant block. Hence each cycle contains at most one fixed arc. A cycle with no fixed arc can be oriented either way; a cycle with one fixed arc has exactly one allowed cyclic direction. Orient each cycle accordingly. The cycles are edge-disjoint, so these decisions are compatible. Their directed cycle chain supplies both terminal directions at total length $L$. Finish unused edges arbitrarily, preserving every fixed direction. Lemma 2 yields global optimality. ∎

This includes the completely undirected weighted problem and the case of at most one fixed arc in the whole graph. It is stronger than a fixed-number-of-undirected-edges enumeration: a relevant block can contain arbitrarily many undirected edges and arbitrary topology. It also permits many fixed arcs globally when they occur in separate blocks, as well as unrestricted fixed arcs in irrelevant blocks.

For an underlying cactus there is a further elementary exact case with unrestricted fixed arcs. Each relevant block is either a bridge or one simple cycle. A relevant bridge is infeasible. A relevant cycle supports both directions between its entry and exit exactly when all its fixed arcs agree with one cyclic orientation. If every relevant cycle passes, orient each cyclically and return the sum of all their edge lengths. If one fails, no round trip exists. The reason is that a simple directed path between the two attachment vertices must use one of the cycle's two sides, and the return path must use the other side. There is no third path through an off-route block.

## 4. Three-state algorithm for two-terminal series-parallel mixed graphs

A two-terminal series-parallel expression has a leaf for each nonloop edge or arc, with ordered terminals. A series node identifies the second terminal of its first child with the first terminal of its second child; the children otherwise have disjoint vertices. A parallel node identifies the two first terminals and the two second terminals; the children otherwise have disjoint vertices. Edge identities are always disjoint across children. The expression is an explicit, checkable decomposition of the input graph. This section assumes this decomposition is supplied; no recognition result is needed for its correctness or running-time claim.

For a component $H$ with ordered terminals $x,y$, store:

- $A(H)=\min_D d_D(x,y)$, with no requirement on $d_D(y,x)$;
- $B(H)=\min_D d_D(y,x)$, with no requirement on $d_D(x,y)$;
- $C(H)=\min_D[d_D(x,y)+d_D(y,x)]$.

An infeasible value is $\infty$, and addition involving infinity gives infinity. The minima in these three states need not be attained by the same orientation; separate witness choices must be stored.

For a leaf of length $w$:

- Undirected edge: $(A,B,C)=(w,w,\infty)$.
- Fixed arc from first to second terminal: $(w,\infty,\infty)$.
- Fixed arc from second to first terminal: $(\infty,w,\infty)$.

For a series node $H=H_1\circ H_2$:
\[
A=A_1+A_2,\qquad B=B_1+B_2,\qquad C=C_1+C_2.
\]

For a parallel node $H=H_1\parallel H_2$:
\[
A=\min(A_1,A_2),\qquad B=\min(B_1,B_2),
\]
\[
C=\min(C_1,C_2,A_1+B_2,A_2+B_1).
\]

**Theorem 4.** These recurrences compute the exact round-trip optimum of every such mixed graph, with arbitrary fixed arcs and nonnegative rational lengths. They recover a full optimal orientation whenever $C<\infty$.

**Proof.** A simple terminal-to-terminal path in a series node passes through its common articulation vertex, so the one-way distances add. Both directed terminal directions require both children to provide both directions. Their orientations are independent, giving all three series recurrences.

A simple terminal-to-terminal path in a parallel node lies entirely in one child: moving from one child to the other requires visiting an outer terminal, which would either revisit the source or already reach the destination. Choose simple paths for the outward and return directions. They either both lie in child 1, both lie in child 2, or lie in different children in either of the two possible assignments. The first two cases are bounded below by $C_1,C_2$. The other two are bounded below by $A_1+B_2,A_2+B_1$, respectively. Each finite bound is attainable by combining child witnesses, since the child edge sets are disjoint. This proves the parallel recurrence. The one-way recurrences follow from the same path containment argument. Induction from the leaves proves the theorem.

Store an attaining case for each finite state. At a series node recursively request the corresponding state in both children. At a parallel node request the selected state(s), and orient unused child edges arbitrarily while preserving fixed arcs. Every leaf then receives at most one requested direction; this reconstructs a full orientation. Rechecking directed shortest distances independently verifies its stated value. ∎

The number of arithmetic operations is linear in the expression size. Witness reconstruction can be linear by storing pointers, instead of copying orientation maps at each node. Rational numerators and denominators have polynomial bit length: each finite state is the sum of lengths of at most two simple paths, with each input edge counted at most twice. Exact rational comparison and addition therefore give polynomial **bit** complexity; neither integer-weight subdivision nor randomness is used.

Theorem 1 permits applying this dynamic program separately whenever relevant blocks have such expressions with their entry/exit vertices as terminals. Other relevant blocks can be handled by Theorem 3 or any independently valid exact method. This does not imply that arbitrary underlying series-parallel graphs with arbitrary chosen terminals come with the required two-terminal expression, and it does not apply to general mixed graphs.

## 5. Four vertices force an undirected edge to be repeated

For $M\ge0$, take vertices $s,t,a,b$, four fixed arcs
\[
s\to a,\quad t\to a,\quad b\to s,\quad b\to t,
\]
each of length one, and one undirected edge $ab$ of length $M$.

If $ab$ is oriented $b\to a$, neither $s$ nor $t$ can reach the other. If oriented $a\to b$, the unique simple outward and return paths are
\[
s\to a\to b\to t,\qquad t\to a\to b\to s.
\]
Therefore
\[
\operatorname{OPT}=4+2M.
\]
The feasible orientation is strongly connected on all four vertices, so the example does not rely on a disconnected or otherwise infeasible remainder.

In the underlying undirected graph, the two edge-disjoint paths $s-a-t$ and $s-b-t$ have total length four. No pair has smaller total length because the two edges incident with $s$ and the two edges incident with $t$ are distinct unit-length edges that any edge-disjoint pair must use. Thus $L=4$, independently of $M$.

Consequences:

- For positive $M$, the lower-bound ratio is $1+M/2$, which is unbounded even on a simple four-vertex mixed graph with one orientable edge.
- Every feasible round trip uses that undirected edge twice in the same direction. Requiring edge-disjoint component paths, or a simple directed cycle containing both terminals, changes the problem.
- At $M=0$, $L=\operatorname{OPT}=4$, but no edge-simple compatible round trip exists. Hence equality of the lower bound with the optimum does not guarantee that the cycle-chain certificate of Section 2 will succeed. The repeated zero-length edge is essential.

These statements obstruct particular relaxations; they are not NP-hardness results.

## 6. Opposite terminal pairs versus arbitrary two pairs

Consider a mixed graph $H$ with requests $(a,b)$ and $(c,d)$, whose objective is $d(a,b)+d(c,d)$ in one orientation. Add new vertices $s,t$ and four fixed zero-length arcs
\[
s\to a,\quad b\to t,\quad t\to c,\quad d\to s.
\]

**Proposition 5.** For every orientation of $H$, in the augmented graph
\[
d(s,t)=d_H(a,b),\qquad d(t,s)=d_H(c,d).
\]
Thus the reduction preserves the exact objective, infeasibility, and orientation witnesses.

**Proof.** Any simple $s$-$t$ path must start with $s\to a$ and finish with $b\to t$. Before it ends, it cannot use $t\to c$, because that would already visit $t$, and cannot use $d\to s$, because that repeats $s$. Its middle is therefore an $a$-$b$ path contained in $H$. Conversely every such path extends by the two zero-length connector arcs. Nonnegativity permits reducing all finite walks to simple paths without increasing length. The reverse direction is identical. This also covers coincident terminals among $a,b,c,d$, with an empty middle path when appropriate. ∎

The reverse reduction is immediate by taking requests $(s,t)$ and $(t,s)$. Hence the mixed round-trip question is polynomially equivalent, value-preservingly, to arbitrary two-pair mixed min-sum orientation. This does not import theorems for *undirected* two-pair inputs: the connector arcs are fixed directed arcs. It also does not import two-pair feasibility, separately bounded lengths, or individually shortest-path results.

## 7. Checks and literature boundaries

The original report and accompanying audit record exact-rational finite checks of the lower-bound/certificate algorithm, block decomposition, supplied two-terminal series-parallel recurrence, orientation recovery, and connector reduction. Normal and optimized runs were compared with explicit exception-based checks. These are supplementary implementation evidence, not universal proofs or a polynomial algorithm for the general target. Programs and raw generated outputs are not distributed. Aggregate recorded coverage is retained in [ACCEPTANCE.json](ACCEPTANCE.json); the complete analytic arguments above depend on no omitted executable. Edition preparation did not rerun the mathematical checks.

The exact EGRES statement, as inspected during the original report and audit, controls the mathematical target. Relevant credited background is:

- Hassin–Megiddo, *On orientations and shortest paths* (1989): the two-pair ideal-orientation theorem is for undirected graphs with positive lengths. Its separately bounded two-path problem and arbitrary allowed-subgraph extension are different objectives. Author source: https://theory.stanford.edu/~megiddo/pdf/orientat.pdf
- Fenner–Lachish–Popa, *Min-Sum 2-Paths Problems*: the retained source studies undirected unweighted inputs, gives a PTAS, and relates that objective to min-sum two edge-disjoint paths. It does not prove the arbitrary mixed weighted target here. Author source: https://www.dcs.bbk.ac.uk/~oded/papers/MS2POP.pdf
- Björklund–Husfeldt, *Shortest Two Disjoint Paths in Polynomial Time*: the retained theorem is randomized for its unweighted undirected model. Author source: https://thorehusfeldt.files.wordpress.com/2010/08/spdp-e5d5661.pdf
- Arkin–Hassin, *A note on orientations of mixed graphs* (2002), DOI https://doi.org/10.1016/S0166-218X(01)00228-1: the verified publisher/EGRES scope includes polynomial feasibility for two pairs, not this exact length optimization. The unavailable full proof is not certified by this note.
- Original problem: https://oldlemon.cs.elte.hu/egres/open/Orientation_with_shortest_round_trip

The original report records that bounded searches also encountered recent maximum-reachability orientation and directed disjoint-shortest-path work. Those optimize different quantities. No verified full exact mixed-weighted resolution was found in this attempt. That is a bounded search observation, not an exhaustive literature review or a current-worldwide-open certificate. Edition preparation performed no new scholarly-source retrieval, source-file rehash, source inspection, or literature search.

## Residual question

General underlying blocks can force paths to reuse edges in the same direction, as Section 5 demonstrates, and need not have a two-terminal series-parallel expression. This attempt supplies neither a polynomially bounded state space for their orientation dependencies nor a precise hardness reduction. The original general question therefore remains open **by this work**. A future attempt must address these general mixed blocks rather than relabeling the partial algorithms as a full solution.
