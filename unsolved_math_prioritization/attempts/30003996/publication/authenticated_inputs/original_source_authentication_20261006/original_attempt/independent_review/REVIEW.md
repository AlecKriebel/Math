# Independent adversarial review: aggregate root-dependent spanning-tree hardness

## Verdict and exact coverage

**PASS_COMPLETE_STRONG_NP_COMPLETENESS.** No mandatory correction is required. The submitted reduction proves strong NP-completeness of its explicitly encoded nonnegative-integer decision problem and therefore NP-hardness of the exact optimization problem in the source.

The frozen `PROOF.md` SHA-256 is

`1a6c267c6240b66c1d804397f4bbbe246f5b6147c3930e1a68396e60b618d615`.

This is a fresh independent adversarial AI audit. It is not human peer review, and historical priority has not been established. No verifier, proof, or verdict for the adjacent path-cost problem was imported or used as verification of this result.

## 1. Exact source objective

I read the complete Kaibel contribution, including both problems and their separate motivations, on printed pp.3014–3015 of [Oberwolfach Report 50/2018](https://ems.press/content/serial-article-files/46772?nt=1), and visually inspected the first problem on p.3014. The primary PDF hash is `a90207e0cadc310ab5a52a228c4b25a16f5e5f617542f006e9909cf90d4c72d2`.

Problem 1 gives an undirected graph, both directed copies of every edge, and an arbitrary cost vector for **each root vertex**. For one selected undirected spanning tree it sums the costs of all its root-induced arborescences. It does not choose the arborescences independently, and it does not sum destination-dependent costs only along paths in a fixed-root tree. The latter is the distinct Problem 2. The submitted reduction matches Problem 1 exactly.

The candidate explicitly uses outward arborescences. If the convention is inward, reversing every supplied arc-cost entry gives an objective-preserving reduction, because every induced tree arc reverses. Thus the orientation convention causes no gap. The original real-valued cost notation contains the finite, nonnegative-integer subclass proved hard here; no complexity claim about unencoded arbitrary real numbers is needed.

The imported NP-complete source problem is satisfiability with at most three literals per clause, item 11 in [Karp's original list](https://doi.org/10.1007/978-1-4684-2001-2_9). Its standard NP-completeness is the only complexity-theoretic hardness input. Targeted current searches did not establish priority for this particular reduction; the lack of a novelty claim is appropriate.

## 2. Preprocessing, graph, and cost specification

Deleting a repeated literal and deleting a tautological clause preserve satisfiability. Nonempty remaining clauses contain each participating variable in exactly one sign. Empty clauses and empty formulas have fixed no/yes outputs: for example, the two-vertex, one-edge instance with both rooted costs 1 and threshold 1 is a no-instance, while all costs zero with threshold zero is a yes-instance. Variables can be relabeled by their distinct occurrences, so the numbers of vertices and clauses used in the reduction are polynomial in the formula's explicit length.

The constructed graph has exactly the two hubs, n variables and m clauses described in the proof. Clause incidences are present precisely for occurring variables. The graph is simple; no parallel edges or loops are required. It is connected because the hub edge joins the hubs, every variable is adjacent to both hubs, and each nonempty clause has an incident variable. Repeated clauses create distinct clause vertices and do not cause a difficulty. Variables absent from some or all clauses are also harmless.

The root-t cost vector assigns the same value to both orientations of each edge. It therefore charges every hub-variable edge 1 and every clause-variable edge B, regardless of how the tree is oriented at t. At a clause root, the only possibly positive costs are the indicated variable-to-hub arcs. Costs on their reverses, on clause edges, on the hub edge and on absent-variable incidences are zero. Other root vectors are identically zero. These are explicit input entries, independent of the eventually chosen tree.

## 3. Exhaustive structural argument for arbitrary trees

The key step genuinely applies to **every** spanning tree, before any canonical shape is assumed.

Every clause vertex has positive degree in a spanning tree. Its only incident edges are clause-variable edges, and each such edge is counted at exactly one clause. Hence q is the sum of clause degrees and is at least m. The three edge categories partition the tree edges, giving `p+q+h=n+m+1`, with h either 0 or 1.

Substituting B=n+1 gives the exact root-t contribution

`p+Bq = Bm+n + (1-h) + n(q-m)`.

Both extra terms are nonnegative, and n is positive. Since all other roots have nonnegative costs, total cost at most K=Bm+n forces h=1 and q=m. This excludes trees omitting the hub edge, trees using clauses as internal connectors, and every proposed shortcut through extra clause edges. No negative cost is available to compensate for an excess in the base contribution.

Equality q=m makes every clause degree exactly one. Delete these leaves. The remaining graph is a connected tree on the two hubs and all variables, contains the hub edge, and has only hub-variable edges otherwise. Each variable must attach to a hub. Attaching to both would create the triangle through the hub edge, forbidden in a tree. Thus each variable attaches to exactly one hub, even if it is unused by the formula. This establishes the claimed truth assignment without any hidden normal-form assumption.

Conversely, choosing one hub for each variable, including the hub edge and then adding each clause as a leaf produces a connected graph with N-1 edges and no cycle. Every such structured tree has base cost exactly K.

## 4. Clause-root orientations and both directions

Fix a structured tree and root it at q_j. The root has a unique neighbor v_i, so the first two arcs toward the hub core are `q_j -> v_i -> h_i`. The selected variable's hub edge is consequently directed **from the variable to its chosen hub**.

For any other variable v_k, its unique hub edge separates it, together with any clause leaves attached to it, from q_j. Thus that edge is directed **from the hub to v_k**. This argument remains valid when v_i has several other clause leaves attached to it and when the route crosses the central hub edge. Every unselected variable-to-hub arc is absent from this rooted arborescence.

Therefore the clause vector charges exactly the selected literal if that literal is false, and charges zero if it is true. For a positive literal, choosing the f hub costs 1; for a negative literal, choosing the t hub costs 1. No other selected arc can contribute under this root vector. Summing over all clause roots gives the exact integer identity

`F(T)=K + number of false selected literals`.

A satisfying assignment supplies a true choice in every clause and hence a tree of cost K. In the reverse direction, any tree of cost at most K first acquires the structured form by Section 3; the displayed identity then forces all selected literals true, satisfying every clause. Unsatisfiable formulas cannot exploit either noncanonical trees or interactions between clause costs. This proves the required if-and-only-if reduction.

## 5. NP membership, size, and strong hardness

A proposed edge set is checked to be a spanning tree in polynomial time. Traversing it from each of the N roots yields exactly N-1 directed arcs per root. The resulting N(N-1) binary integers can be added with polynomial bit length and compared to K. This establishes membership in NP for the explicit decision problem.

The reduction constructs N=n+m+2 vertices, at most `1+2n+3m` undirected edges, and exactly `2N|E|` explicitly specified cost entries. Every cost is 0, 1 or n+1, hence at most N. The threshold `(n+1)m+n` is bounded by a polynomial in N. Consequently even the unary encoding of every numerical entry and the threshold has polynomial length. The same reduction proves NP-hardness on this bounded-numerical-data subclass, which is strong NP-hardness. Together with membership, the stated strong NP-completeness conclusion follows.

An algorithm finding an optimal spanning tree would decide these instances by evaluating its returned tree and comparing with K, so the source's optimization question is settled. The proof does not assume a fixed number of roots, a degree bound, planarity, metric costs, or an approximation promise.

The strictly-positive-cost variant is also correct. Adding 1 to every arc cost in every root vector adds exactly N(N-1) to every spanning-tree objective, including contributions from roots whose original vectors were zero. Shifting K by that same constant preserves the answer and polynomial numerical bounds.

## 6. Fresh independent exact tests

The submitted verifier was replayed unchanged in an isolated copy. All **78,056** assertions passed for **212** formulas and **37,629** spanning-tree/formula cases; its receipt reproduced byte-identically. The verifier hash is `02182aac6b9c300105b48d6049384954c26ef57cb11dae66a3908b6926dbbe7c`.

The separate checker uses a materially different method:

- It enumerates labeled trees by Prüfer sequences, then filters by the constructed graph, rather than enumerating edge subsets with the author's union-find test
- It evaluates the entire aggregate objective by the bipartition created by deleting each tree edge: a root in the tail component selects one orientation, while a root in the other component selects its reverse
- It checks arbitrary trees, individual clause-root costs, inward-cost reversal, the positive shift, and satisfying-assignment witnesses
- It uses no code or result from the adjacent path-cost problem

The independent run passes **600,122** assertions across **550** formulas, including 32 unsatisfiable formulas, on 96 distinct graphs. It evaluates **94,959** tree/formula cases. Among them, **80,285** are noncanonical, with 56,157 omitting the hub edge and 59,320 using extra clause edges; those two categories can overlap. All are excluded by the threshold. The 14,674 canonical cases include 10,988 with a positive false-literal penalty. These counts directly exercise the potential shortcuts rather than only checking satisfying witnesses.

Run from the review directory:

```sh
python independent_checks.py
(cd author_replay && python verify.py)
```

Both scripts use only the Python standard library. The tests are finite controls. The proof of all-size hardness is the structural and orientation reasoning above, not the size of the census.

## 7. Final disposition

The exact frozen proof is complete for the source's aggregate rooted-arborescence optimization problem, with the stronger nonnegative-integer decision result stated in the artifact. No mathematical correction is required before an authorized draft publication. Retain the distinction from Problem 2, the finite-encoding convention, the absence of unsupported graph restrictions, and the unestablished-priority qualification.
