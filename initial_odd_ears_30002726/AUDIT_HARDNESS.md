# Adversarial audit: simple-graph Set Cover hardness for initial odd ears

Audit date: 20 October 2026. Target: queue row 1828, ID 30002726.

## Verdict

**PASS. The supplied reduction proves NP-completeness of deciding whether β(G) ≥ q, even when G is a simple 2-vertex-connected graph with a universal vertex whose deletion leaves a connected bipartite graph.** No mathematical gap was found in either implication, the cone identity, polynomial size, or membership in NP. The statement concerns an input threshold q, not a fixed constant. It does not establish a new literature-priority claim or external peer review.

The completed primary manuscript `NP_COMPLETENESS_PROOF.md` was subsequently read in full and passed the same checks. Its audited SHA-256 is `5e7fd90b5ad5178702797896619542aebb179f5056ad9f7426b1d296625ca252`. The cone lemma's nonempty-set wording is sufficient because a nonempty perfectly matchable set has at least two vertices; explicitly writing that bound would merely make the 2-connectivity convention clearer.

The accepted manuscript explicitly uses an inclusion-minimal subcover in the forward direction, retains the connectivity constraint in the cone identity, and handles trivial Set Cover inputs before applying the construction. These details are necessary for the proof.

## 1. Exact target and source alignment

The source gate was checked against Benchetrit–Sebő's paper, not merely against its summary. Section 1.1 defines open ear-decompositions and counts the initial circuit. Proposition 1.13 permits extension of an ear-decomposition of a 2-connected subgraph. Theorem 3.2 gives the odd-ear characterization of 2-connected factor-critical graphs. Section 3.1 explicitly identifies the initial-odd-prefix parameter with the maximum cycle rank of such a subgraph. Thus the audited target is

β(G) = max{ |E(H)| − |V(H)| + 1 : H is a 2-connected factor-critical subgraph of G },

with value zero if this family is empty. The subgraph need not initially be induced or spanning. One-edge ears count; adding chords therefore does not create a mismatch with the objective. Closed ears and the total number of odd ears are not being substituted.

Primary reference: [Benchetrit–Sebő, arXiv:1509.05586v1](https://arxiv.org/html/1509.05586v1), §1.1, Proposition 1.13, Theorem 3.2 and §3.1. The same characterization is independently stated in [Benchetrit's author exposition](https://matroidunion.org/?p=1769), Theorem 2 and Definition 3.

## 2. Cone identity: both directions are valid

Let B be a connected bipartite graph with an edge, let a be a new universal vertex, and let G = K₁ ∨ B. Then

β(G) = max{ |E(B[X])| : |X| ≥ 2, B[X] is connected and has a perfect matching }.

Here is a complete verification, including the points most likely to conceal a variant error.

1. Every 2-connected factor-critical subgraph H has at least three vertices and is non-bipartite. Indeed, in a bipartite graph with both sides nonempty, deleting a vertex from each of the two sides would require contradictory equalities between the side sizes. Thus H must contain a.
2. Add every edge of G with both endpoints in V(H). Adding edges preserves 2-connectivity and every perfect matching witnessing factor-criticality. It cannot reduce cycle rank. Hence maximizing over induced subgraphs is legitimate.
3. Write the resulting induced graph as G[{a} ∪ X]. Deleting a gives B[X], which is connected because the cone is 2-connected, and has a perfect matching because it is factor-critical.
4. Conversely, if B[X] is connected with a perfect matching M and |X| ≥ 2, its cone is 2-connected: deletion of a leaves B[X] connected; deletion of any other vertex leaves a connecting all remaining vertices. It is factor-critical: deleting a leaves M; deleting x ∈ X allows a to be matched to x's mate in M, with all other edges of M retained.
5. The cone has |E(B[X])| + |X| edges and |X| + 1 vertices. Its cycle rank is exactly |E(B[X])|, with no off-by-one error.

Connectivity is indispensable here. Replacing the right side by all matchable induced subgraphs, including disconnected ones, would invalidate the reduction. The proof does not do that.

## 3. Set Cover domain and output size

Use ordinary explicit finite Set Cover: U has m ≥ 1 elements, there are n ≥ 1 listed sets S₁,…,Sₙ, their union is U, and 0 ≤ s ≤ n. Empty sets and duplicate sets do not invalidate the proof. For a positive-budget formulation one may additionally remove s = 0 as a trivial case.

These restrictions preserve NP-hardness. From an arbitrary instance, a missing element in the union is immediately NO; an empty universe is immediately YES; a negative budget is NO; and a budget at least n is settled by testing the union. These cases may be mapped to fixed target instances (K₃,1) for YES and (K₃,2) for NO. Otherwise the restricted construction applies. Equivalently, the fixed promised Set Cover YES and NO instances ({u},{{u}},1) and ({u,v},{{u},{v}},1) show that restricting to nonempty, fully covered universes loses no hardness. The standard starting theorem is Set Cover NP-completeness; see [Karp's original chapter record](https://link.springer.com/chapter/10.1007/978-1-4684-2001-2_9). The publisher record was verified; this audit did not visually inspect the scanned original Set Cover theorem.

Set

T = Σⱼ(1 + |Sⱼ|),  k = T + n + 3,  A = (m+1)k²,  F = A − ks.

Construct m+1 disjoint copies of K_{k,k}, indexed by 0,…,m. Block 0 is the root; each other block corresponds to an element. In block i distinguish one right-side vertex ρᵢ. For each set Sⱼ add a left-side connector cⱼ adjacent to ρ₀ and to ρᵢ precisely when element i lies in Sⱼ. Let B be this bipartite graph, and add the universal vertex to obtain G.

B is connected because every element belongs to a set and every connector meets the root block. G is simple: all block vertices are distinct, each incidence is represented once, and the apex is new. G is 2-vertex-connected by the same deletion argument used for the cone identity.

The output has

|V(G)| = 2k(m+1) + n + 1,

|E(G)| = (m+1)k² + T + 2k(m+1) + n.

For the explicit input length L, m,n,T = O(L), so k = O(L), vertices are O(L²), edges are O(L³), and F has polynomial encoding length. This is a genuine polynomial reduction, not a pseudo-polynomial or weighted/multigraph shortcut.

## 4. Forward implication

Assume a cover of size at most s exists. Delete redundant sets until an inclusion-minimal cover C of size r ≤ s remains. For every j ∈ C there is a private element eⱼ belonging to Sⱼ and to no other selected set: otherwise Sⱼ could be removed. These private elements are pairwise distinct.

Select all block vertices except one left-side vertex in each private-element block eⱼ. Also select exactly the connectors cⱼ with j ∈ C. Call the selected set X.

Match cⱼ to ρ_{eⱼ}. In each of these r blocks, k−1 selected left vertices remain and k−1 right vertices remain unmatched; match them internally. Every other block is a full K_{k,k} and is matched internally. This is a perfect matching of B[X]. The private-element argument is exactly what prevents two connectors competing for one representative.

The root and every element block remain internally connected because k ≥ 2. Every selected connector joins the root representative, and the chosen sets cover every element, so B[X] is connected.

Each omitted left vertex removes exactly k block edges; connectors have no left-left edges. Thus

|E(B[X])| = A − kr + Σ_{j∈C}(1+|Sⱼ|) ≥ A − ks = F.

The cone identity gives β(G) ≥ F. No extra assumptions concerning an assignment of all elements to sets are needed.

## 5. Reverse implication

Suppose β(G) ≥ F. The cone identity supplies a connected induced B[X] with a perfect matching and at least F edges.

### 5.1 Every block retains an internal edge

If one block has no internal edge in B[X], at least k² of the A block edges are absent. There are at most T connector-incidence edges in the entire graph, so

|E(B[X])| ≤ A − k² + T < A − ks = F.

The strict inequality follows from k² > ks + T. With s ≤ n and k = T+n+3,

k² − ks − T ≥ k(k−n) − T = k(T+3) − T > 0.

This contradiction does not require knowing how many vertices of the deficient block remain, and it covers blocks reduced to a representative or to an empty set.

### 5.2 At most s connectors are selected

Let r be the number of selected connectors. In block i let aᵢ and bᵢ be the numbers of omitted left and right vertices, respectively. Perfect matchability of the bipartite graph forces equality of the total left and right orders:

(m+1)k − Σaᵢ + r = (m+1)k − Σbᵢ,

hence Σ(aᵢ−bᵢ) = r.

The number L of lost internal block edges is

L = Σ[k(aᵢ+bᵢ) − aᵢbᵢ]
  = kr + Σ bᵢ(2k−aᵢ)
  ≥ kr,

since 0 ≤ aᵢ,bᵢ ≤ k. Therefore

|E(B[X])| ≤ A − kr + T.

If r ≥ s+1, then k > T yields A−kr+T ≤ A−k(s+1)+T < A−ks = F, a contradiction. Thus r ≤ s. The global balance argument is only a necessary matching condition, but that is all this upper bound needs; it does not incorrectly claim sufficiency.

### 5.3 The selected connectors give a cover

Every block contains an internal edge by §5.1, so the root block and every element block contribute selected vertices. Since B[X] is connected and there are at least two blocks, each element block must have an edge to the outside. Its only possible external edges are from its right representative to connectors of sets containing that element. Therefore at least one selected connector represents a set containing each element. The r selected sets cover U, with r ≤ s.

This proves both directions without assuming X is spanning or presupposing that representatives were retained.

## 6. NP membership

A polynomial certificate for β(G) ≥ q consists of a subgraph H with at least three vertices and, for every v ∈ V(H), a perfect matching of H−v. Verify that all listed edges are in G, that H remains connected after deletion of every vertex, that each listed matching covers exactly V(H)\{v}, and that |E(H)|−|V(H)|+1 ≥ q. These are polynomial-time checks; the matching list has polynomial total size. The source characterization then validates the certificate.

One may instead certify an open ear-decomposition with the required odd prefix. The factor-critical certificate avoids any need to construct such a decomposition during this reduction.

## 7. Independent computational checks

Files: `audit_set_cover.py` and `audit_set_cover_results.json` in this directory. The script uses only Python's standard library; it does not import any other matching or β implementation.

Results, all exact and deterministic:

- 63 explicit small block graphs: full enumeration of every vertex subset, with recursive exact perfect-matching and connectivity checks, agreed with an independently coded compressed optimizer.
- 14 corresponding cones: full enumeration of induced factor-critical 2-connected vertex sets agreed with that optimizer and therefore the cone identity.
- 441 fully covered set systems with 1 ≤ m,n ≤ 3: using k = T+n+3, every budget 0,…,n was checked against exact Set Cover. All 1,719 threshold decisions agreed. The largest constructed cone in this compressed check has 148 vertices and 1,455 edges.
- Zero discrepancies.

The compressed optimization has an independent saturation justification. Fix selected connectors and the set of active blocks. In any perfect matching, a block has either equally many retained left and right vertices, or one extra retained right vertex matched through its sole representative to a connector. No other cross-block matching edge exists. In the second case a block can serve only one connector. Add retained vertices up to k+k in the first case or (k−1)+k in the second; this preserves a matching, preserves connectivity, and only adds edges. The active block/connector incidence graph must be connected, and the selected connectors must admit an injection into adjacent active block representatives. These conditions are also sufficient. A state with h active blocks, r connectors and t retained incidences therefore has optimal value hk²−kr+t. With no connectors, the connected optimum is one full block. Enumerating these states computes the exact optimum for the family. This invariant is used only for corroboration, not for the reduction proof.

Finite tests are not a proof of universal correctness. The mathematical arguments in §§2–6 are the acceptance basis.

## 8. Boundary of the accepted conclusion

The accepted theorem is NP-completeness for variable-threshold β on simple 2-vertex-connected graphs, already on cones over connected bipartite graphs. It does not contradict fixed-parameter tractability, does not show fixed-threshold hardness, and does not address the distinct maximum-total-odd-ear problem. The audit does not certify literature priority or that no later paper has independently established the same result.
