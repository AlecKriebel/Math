# Independent review of the fractional coloring counterexample

## Conclusion and scope

The proposed family is valid. For each integer \(k\ge 5\), take a clique of order \(k\) and attach \(k\) distinct pendant vertices to each clique vertex. The resulting finite simple graph \(G_k\) satisfies

\[
\chi_f(G_k)=k>
\max_{u\in V(G_k)}\frac{\sum_{v\in N_{G_k}[u]}\gamma_{G_k}(v)}{d_{G_k}(u)+1}
=\frac{3k}{4}+1,
\qquad
\gamma_G(v)=\frac{d_G(v)+1+\omega(G[N_G[v]])}{2}.
\]

The strict threshold is exactly \(k\ge5\) within this family. The case \(k=1\) must be calculated separately, and \(k=4\) gives equality rather than a counterexample. The smallest member of this family that works is \(G_5\), with 30 vertices, 35 edges, fractional chromatic number 5, and maximum closed-neighborhood average \(19/4\). No claim of minimum order among all counterexamples is made.

This is a verification of the existing counterexample associated with problem ID 30002271, OWR-12330-013, not a novelty or publication claim. The mathematical proof below is self-contained. It does not depend on the bibliographic history of the example.

## Graph definition

Let the core be \(C=\{c_0,\ldots,c_{k-1}\}\). Add vertices \(p_{i,j}\), where \(0\le i<k\) and \(1\le j\le k\). Join every pair of distinct vertices of \(C\), and join \(p_{i,j}\) only to \(c_i\). There are no other edges.

Thus the graph is finite, simple, and connected for every positive integer \(k\). It has

\[
|V(G_k)|=k+k^2=k(k+1),\qquad
|E(G_k)|=\binom{k}{2}+k^2=\frac{3k^2-k}{2}.
\]

The pendants are all distinct. They are not joined to the other core vertices or to one another.

## Local parameters for all vertex types

Assume first that \(k\ge2\).

A core vertex \(c_i\) has \(k-1\) core neighbors and \(k\) pendant neighbors. Consequently

\[
d(c_i)=2k-1,\qquad |N[c_i]|=2k.
\]

The induced subgraph on \(N[c_i]\) contains the entire core clique. Any clique that contains a pendant has order at most 2. Hence

\[
\omega(G_k[N[c_i]])=\max\{k,2\}=k,
\qquad \gamma(c_i)=\frac{2k+k}{2}=\frac{3k}{2}.
\]

For every pendant \(p_{i,j}\), its closed neighborhood is exactly the edge \(\{p_{i,j},c_i\}\). Therefore

\[
d(p_{i,j})=1,\qquad |N[p_{i,j}]|=2,\qquad
\omega(G_k[N[p_{i,j}]])=2,\qquad \gamma(p_{i,j})=2.
\]

These calculations use closed neighborhoods. In particular, the local clique number at a pendant is 2, not 1. It is also not the global clique number \(k\) when \(k>2\).

## Every closed-neighborhood average

Write

\[
A_G(u)=\frac{1}{d_G(u)+1}\sum_{v\in N_G[u]}\gamma_G(v),
\qquad M(G)=\max_{u\in V(G)}A_G(u).
\]

For a core vertex, its closed neighborhood contains all \(k\) core vertices, including itself, and exactly its own \(k\) pendants. Thus

\[
A_{G_k}(c_i)
=\frac{k(3k/2)+k(2)}{2k}
=\frac{3k}{4}+1.
\]

For a pendant,

\[
A_{G_k}(p_{i,j})
=\frac{3k/2+2}{2}
=\frac{3k}{4}+1.
\]

The equality of the two vertex-type averages is exact. It proves the stated maximum without overlooking a vertex type or invoking a symmetry assumption that would identify cores with pendants.

## Exact fractional chromatic number

The core clique gives \(\chi_f(G_k)\ge k\). More explicitly, in the independent-set formulation of fractional coloring, every independent set contains at most one core vertex. Summing the unit coverage requirements over all core vertices forces total color weight at least \(k\).

For the reverse inequality, give \(c_i\) color \(i\), and give every pendant attached to \(c_i\) color \(i+1\pmod{k}\). For \(k\ge2\), each pendant has a different color from its unique neighbor. The core colors are pairwise distinct, so this is a proper \(k\)-coloring. A proper coloring is also a fractional coloring of the same total weight. Therefore

\[
k\le\chi_f(G_k)\le\chi(G_k)\le k.
\]

In particular, \(\chi_f(G_k)=\chi(G_k)=k\), and

\[
\chi_f(G_k)-M(G_k)=k-\left(\frac{3k}{4}+1\right)=\frac{k-4}{4}.
\]

This proof does not infer the fractional chromatic number from the ordinary chromatic number alone. The clique lower bound is essential.

## Small cases and the exact threshold

For \(k=1\), the graph is \(K_2\). Both vertices have degree 1, local clique number 2, and \(\gamma=2\). Its fractional chromatic number and both closed-neighborhood averages equal 2. The formula \(\gamma(c_i)=3k/2\) is invalid here because the local clique number is \(\max\{1,2\}=2\), not 1. The cyclic coloring described above is also invalid for \(k=1\).

For the remaining small cases:

- \(k=2\): \(\chi_f=2\), \(M=5/2\), and the gap is \(-1/2\).
- \(k=3\): \(\chi_f=3\), \(M=13/4\), and the gap is \(-1/4\).
- \(k=4\): \(\chi_f=M=4\), so the strict inequality fails.
- \(k=5\): \(\chi_f=5\), \(M=19/4\), and the gap is \(1/4\).

Thus the family gives the required strict inequality if and only if \(k\ge5\).

## Distinguishing other formulations

### Maximum of maximal-clique averages

For \(k\ge2\), the maximal cliques are the core \(C\) and the pendant edges \(\{c_i,p_{i,j}\}\). The averages of the original graph's \(\gamma\)-values on these cliques are

\[
\frac{1}{|C|}\sum_{v\in C}\gamma_{G_k}(v)=\frac{3k}{2},
\qquad
\frac{\gamma_{G_k}(c_i)+\gamma_{G_k}(p_{i,j})}{2}
=\frac{3k}{4}+1.
\]

Consequently

\[
\max_{Q\text{ maximal clique of }G_k}
\frac{1}{|Q|}\sum_{v\in Q}\gamma_{G_k}(v)
=\frac{3k}{2}\ge\chi_f(G_k).
\]

The family therefore does not disprove the version that takes a maximum over maximal cliques, or equivalently asks for the existence of a maximal clique with sufficiently large average. It would refute a version requiring the inequality for every maximal clique when \(k\ge5\), because each pendant edge then has average below \(k\). These are different quantifiers.

### A maximum over subgraphs

Consider the materially different quantity obtained by also maximizing \(M(H)\) over nonempty induced subgraphs \(H\) of \(G\), with degrees, closed neighborhoods, and local clique numbers all recomputed inside \(H\).

For \(k\ge2\), the induced core subgraph \(H=G_k[C]=K_k\) has

\[
d_H(v)=k-1,\qquad \omega(H[N_H[v]])=k,\qquad \gamma_H(v)=k,
\qquad M(H)=k.
\]

Thus \(\max_{H\text{ induced in }G_k}M(H)\ge k=\chi_f(G_k)\). The same observation applies if all subgraphs, not just induced subgraphs, are allowed. It proves that this family is not a counterexample to such a subgraph-max assertion; it does not prove that assertion for arbitrary graphs. It also exhibits why \(M(G)\) cannot simply be assumed monotone under taking induced subgraphs: \(M(K_k)>M(G_k)\) for \(k\ge5\).

If a different subgraph formulation inherits \(\gamma_G\) instead of recomputing \(\gamma_H\), that must be stated explicitly. On the core clique its average is then \(3k/2\), so this family does not refute that version either.

### Fractional coloring with vertex-dependent demands

The ordinary fractional chromatic number requires unit coverage at every vertex and minimizes total palette measure. A different local-demand assertion asks for a unit-measure palette on which each vertex \(v\) receives a measurable set of colors of measure at least

\[
f(v)=\frac{1}{\gamma_G(v)}=\frac{2}{d_G(v)+1+\omega(G[N_G[v]])},
\]

with adjacent vertices receiving disjoint sets. The counterexample to the closed-neighborhood average does not contradict this local-demand assertion.

Indeed, for \(k\ge2\), assign pairwise disjoint intervals of length \(2/(3k)\) in \([0,1)\) to the \(k\) core vertices. Their total length is \(2/3\). Each pendant needs measure \(1/2\) and is adjacent only to its own core vertex. The complement of that core interval has measure \(1-2/(3k)\ge2/3\), so it contains a measurable set of measure \(1/2\) for every pendant. Pendants are mutually nonadjacent, so their sets may overlap freely. All endpoints may be chosen rational, giving an ordinary finite weighted independent-set representation if desired. For \(k=1\), simply assign the two vertices disjoint half-palettes.

Thus this family actually admits these local demands. Such a coloring does not justify replacing its nonuniform demand constraints by the arithmetic average of \(\gamma\) over a closed neighborhood. Rescaling directly gives a uniform palette bound involving \(\max_v\gamma_G(v)\), not \(M(G)\).

## Review of the accompanying audit and exact checker

The mathematical claims in AUDIT.md and the implementation in check_exact.py were inspected after completing the independent derivation above. No mathematical or algorithmic error was found. In particular, intersecting every global maximal clique with a closed neighborhood correctly recovers its local clique number: every clique in that neighborhood extends to a global maximal clique, while every such intersection remains a clique in the neighborhood. Checking the nonnegative dual weights on maximal independent sets suffices, since every independent set extends to a maximal one.

The Bron–Kerbosch helper was also compared with independent brute-force clique enumeration on all 1,099 labeled simple graphs of orders 1 through 5; its maximal-clique sets were correct and had no duplicates. The complete checker was rerun for \(k=1,\ldots,12\) under normal and optimized Python, and both outputs matched EXACT_CHECKS.json byte for byte. Reciprocal local-demand feasibility was additionally checked with exact finite palettes for \(k=2,\ldots,12\): use \(6k\) equal slots, give each core four distinct slots, and give each pendant \(3k\) slots outside its own core's four slots. INDEPENDENT_CHECKS.json records these test outcomes.

The review of AUDIT.md covers its mathematics and the stated role of the computational checks. It does not independently verify its bibliographic assertions; no external source was consulted for this independent review.

## Review verdict

The stated construction and strict inequality pass independent algebraic and combinatorial review, with the required restriction \(k\ge5\). The principal failure modes are an incorrect \(k=1\) extension, forgetting the center in a closed neighborhood, assigning the global clique number to a pendant, treating \(k=4\) equality as strict, claiming absolute minimality from a family threshold, or conflating the target with the distinct quantified assertions above. No such extra conclusion is established here.
