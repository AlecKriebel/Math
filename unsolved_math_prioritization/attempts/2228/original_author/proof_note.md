# Cycle-density reductions and a maximum-degree-four classification

Problem: UnsolvedMath 2228 / EP-642 / Erdős 642. Date: 2026-10-06.

## Scope and outcome

This note does not solve the linear extremal-bound problem and does not improve its known asymptotic bounds. It proves elementary reductions, classifies the maximum-degree-four case, and isolates an exact missing inequality in the proposed minimum-degree/longest-cycle route. No novelty is claimed for these elementary observations.

All graphs are finite, undirected, and simple. A cycle is simple and has at least three vertices. For a cycle C with vertex set S and length l=|S|, let q_G(C) count edges of G joining nonconsecutive vertices of C. Call a graph admissible if q_G(C)<|C| for every cycle C. Let f(n) be the largest edge count of an admissible n-vertex graph. The unresolved target is a constant K, independent of n, with f(n)<=Kn.

## Proposition 1: the exact edge and boundary identities

For every cycle C with vertex set S,

q_G(C)=e_G(S)-|S|

and

2(q_G(C)-|S|)=sum_{v in S}(d_G(v)-4)-e_G(S,V(G)\S).

Proof. Exactly |S| edges of G[S] belong to C; all other induced edges are chords. The degree sum on S is 2e_G(S)+e_G(S,V(G)\S). Substitute the first equality and rearrange. Consequently C violates admissibility precisely when e_G(S)>=2|S|, equivalently when the displayed degree surplus is at least the boundary size. These identities refer to edges of the original graph, not edges of a drawing or of a chosen spanning subgraph. QED.

## Proposition 2: constant-core equivalence

The following are equivalent.

1. There is K>0 such that every admissible graph G satisfies e(G)<=K|V(G)|.
2. There is an integer D>=1 such that every nonempty graph of minimum degree at least D contains a cycle C with q_G(C)>=|C|.
3. There is an integer r>=0 such that every admissible graph is r-degenerate.

Proof. The admissibility property passes to arbitrary subgraphs: deleting vertices or edges cannot increase the chord count of a surviving cycle. If (1) holds, choose an integer D>2K. A nonempty graph with minimum degree D has e(G)>=D|V(G)|/2>K|V(G)|, so cannot be admissible. This proves (2).

If (2) holds and an admissible graph had a nonempty subgraph of minimum degree at least D, that subgraph would contain a forbidden cycle whose chords also occur in the original graph. Thus every nonempty subgraph has a vertex of degree at most D-1, establishing (3) with r=D-1.

Finally, successively delete vertices of current degree at most r. Charge each edge to its earlier deleted endpoint. Every vertex receives at most r charges, giving e(G)<=r|V(G)| and hence (1), for example with K=max(1,r). QED.

Thus extracting a core is a valid reduction; proving the required absolute minimum-degree theorem is still the original problem in equivalent form.

## Proposition 3: exact classification when maximum degree is at most four

Let G have maximum degree at most four. It contains a cycle with at least as many chords as vertices if and only if some connected component of G is four-regular and Hamiltonian.

Proof. If C is such a cycle, with S=V(C), then

2|S|<=e_G(S)<=1/2 sum_{v in S}d_G(v)<=2|S|.

All inequalities are equalities. Each vertex of S has degree four in G, and no edge joins S to its complement. Since the cycle makes G[S] connected, S is the vertex set of a connected component. C is a Hamiltonian cycle of that component, which is four-regular. Conversely, a Hamiltonian cycle in a four-regular component on s vertices has 2s-s=s chords. QED.

In particular, any connected four-regular non-Hamiltonian graph is admissible. This disproves the candidate minimum-degree threshold D=4; any valid threshold in Proposition 2 must be at least five. It does not disprove existence of a larger absolute threshold.

### An explicit eleven-vertex example

Take two disjoint copies of K_5. Delete one edge a_i b_i in copy i, for i=1,2. Add a vertex z and the four edges za_1, zb_1, za_2, zb_2. Every old vertex and z has degree four. There are eleven vertices and twenty-two edges. Removing z separates the two copies, so z is a cut vertex. A Hamiltonian graph with at least three vertices has no cut vertex: deleting a vertex from its Hamiltonian cycle leaves a path through all remaining vertices. Therefore this graph is non-Hamiltonian, and Proposition 3 proves it admissible. Every longest cycle in this example still has fewer chords than vertices.

## Proposition 4: a simple linear lower-bound family

For n>=6, the complete bipartite graph K_{3,n-3} is admissible and has 3n-9 edges.

Proof. Any cycle alternates between its two parts and therefore has length 2k with k in {2,3}. Its vertices induce K_{k,k}, with k^2 edges. Its chord count is k^2-2k=k(k-2), which is respectively zero or three, strictly below 2k. QED.

This family shows that an eventual coefficient K in f(n)<=Kn cannot be less than three. It is a lower bound of linear order, not a counterexample to the requested linear upper bound.

## The precise longest-cycle gap

In a graph of minimum degree D, Proposition 1 would give a violating cycle if one could find C, with S=V(C), satisfying

e_G(S,V(G)\S)<=sum_{v in S}(d_G(v)-4).

A sufficient, stronger condition is e_G(S,V(G)\S)<=(D-4)|S|. No argument establishing either condition at an absolute D is provided here.

Longest-cycle maximality alone only forbids particular extensions. For example, an outside vertex cannot be adjacent to two consecutive cycle vertices, since it could replace their edge and lengthen the cycle. That local restriction does not establish the required global boundary inequality. The four-regular example above refutes the boundary conclusion at D=4 even for a longest cycle. It does not refute a suitably strengthened argument at larger D.

## Why the 2026 almost-linear theorem does not close the gap

Draganić and Girão, arXiv:2601.08769v1, Theorem 1.1, state that there are fixed positive constants c,C (and a positive implicit multiplicative constant a) such that minimum degree at least C forces some cycle of length l with at least a*l/(log l)^c chords. The quantifier is existence of a cycle of some length; it does not prescribe that length or say that every length occurs.

For fixed a,c>0, a/(log l)^c tends to zero. Thus this lower bound alone cannot imply q_G(C)>=l for the returned cycle. Repeated application supplies no stated control over whether the resulting cycles have compatible vertex sets or whether their chords accumulate on a single cycle. Removing the denominator or otherwise establishing density at least one is still necessary.

## Conclusion

The reduction, the maximum-degree-four classification, the explicit obstruction, and the lower-bound family above are proved. The absolute minimum-degree theorem and f(n)=O(n) remain unproved here. The investigation stops at a stalled partial result after three approaches, below the five-approach cap.

## Public references

- T. F. Bloom, Erdős Problem 642 and its revision history: https://www.erdosproblems.com/642 and https://www.erdosproblems.com/history/642
- N. Draganić, A. Methuku, D. Munhá Correia, B. Sudakov, Cycles with many chords, Random Structures & Algorithms 65 (2024), 3-16; Theorem 1.1: https://arxiv.org/abs/2306.09157 and https://doi.org/10.1002/rsa.21207
- N. Draganić, A. Girão, Cycles with almost linearly many chords, arXiv:2601.08769v1 (2026), Theorem 1.1: https://arxiv.org/abs/2601.08769
- S. Letzter, A. Methuku, B. Sudakov, Nearly Hamilton cycles in sublinear expanders, and applications, Journal of the London Mathematical Society (2026), Corollary 7.2: https://arxiv.org/abs/2503.07147 and https://doi.org/10.1112/jlms.70452
