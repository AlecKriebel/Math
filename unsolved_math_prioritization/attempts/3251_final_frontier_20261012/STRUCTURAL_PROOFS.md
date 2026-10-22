Editorial note: This is the complete authored text. Only references to undistributed operational files, their identities, locations and replay directions have been replaced. All mathematical arguments, exact finite counts, corrections and limitations are retained. The public manifest identifies the actual distributed files.

# Final-pass chromatic barriers, critical structure, and the Folkman frontier

## Status and conventions

This is a component of the **fifth and final substantive pass** for problem 3251 / ordered row 1753. At least five substantive passes are confirmed; the lifetime count before the recorded sequence is unknown. The general conjecture remains unresolved. There is no sixth pass, counterexample claim, novelty claim, or remote/queue/publication action in this packet.

All graphs are finite and simple. Write n=|V(G)|, q=chi(G), k=omega(G). For k>=2 a division is a two-coloring with no monochromatic maximum k-clique. A graph with no division is indivisible. The open antineighborhood M(v) consists of the vertices other than v that are nonadjacent to v. The high-incidence core X always uses incidence in the **original distinct maximum-clique family**: v belongs to X precisely when it belongs to at least three such cliques. Incidence is never recomputed inside G[X].

The accepted fourth-pass exact propagation/tree theorem and the third-pass core and separator deductions are pinned dependencies. Their conclusions are used only in their stated scopes. In particular, a division of the induced core is not asserted to extend, and compatible clique-cutset traces are not assumed. The separately accepted final-pass linear-compression correction is also a pinned dependency: it supersedes the earlier exponential representation-size sentence, while retaining the exact propagation and tree criteria. The companion realization theorems are independent and are not premises here.

## 1. Critical join decomposition: the identified external input

A graph J is vertex-critical if deleting any vertex reduces its chromatic number. We use Gallai's theorem in the vertex-critical form:

> If J is vertex-critical and its complement is connected, then |V(J)| >= 2 chi(J)-1.

This is a classical external theorem, not a new claim. The exact vertex-critical convention and inequality were checked in Matej Stehlik's author-hosted lecture *Gallai's theorem on colour-critical graphs and related results*, September 18, 2009, PDF pages 2 and 10 (1-based), https://oc.g-scop.grenoble-inp.fr/fichiers/stehlik.pdf. The retrieved PDF has 372,167 bytes and SHA-256 cf3dda65f07a466a89b50f3cd7a9106f033bc269db2a150d574662d7c13333a8. Local text extraction confirms the non-strict inequality, where one web extraction misread its glyph. The primary paper is Stehlik, *Critical graphs with connected complements*, JCTB 89 (2003), 189-194, DOI https://doi.org/10.1016/S0095-8956(03)00069-8; its publisher abstract states a strengthening of this theorem. We rely on the external theorem, not on a fresh complete audit of its proof. No source document is included in this packet.

Here is the elementary consequence used repeatedly. Choose an induced q-critical subgraph H of G by repeatedly deleting vertices without reducing chi. Let H_1,...,H_t be induced on the components of the complement of H. They are pairwise completely joined. Put q_i=chi(H_i), r_i=omega(H_i), and r'=omega(H). Then

    q=sum q_i,    r'=sum r_i <= k,    |H| >= sum(2q_i-1)=2q-t.       (1)

Each H_i is vertex-critical: if a vertex deletion preserved q_i, it would preserve q in H. Each complement component is connected, including the one-vertex case. Thus Gallai applies separately to each factor. None of this requires G itself to be critical, or that chi-criticality and division-minimality coincide.

## 2. Antineighborhood order theorem, with an equality restriction

**Theorem 1.** If every vertex of a nonempty graph G has a maximum k-clique in its open antineighborhood, then

    n >= 2 chi(G)-1.

If equality holds and chi(G)>omega(G), then G itself is vertex-critical and its complement is connected.

**Proof.** Use H and its t factors from (1), and write m=n-|H|. Choose a factor with minimum clique number r_i and any vertex v in it. Every vertex in the other factors is adjacent to v. A maximum k-clique anticomplete to v therefore has at most r_i vertices in H, so at least k-r_i vertices outside H. Consequently m>=k-r_i. Since the other t-1 factors have clique number at least one, r_i<=r'-(t-1)<=k-t+1, and hence m>=t-1. Combining this with (1) proves n>=2q-t+(t-1)=2q-1.

For equality, every inequality in this chain must be equality. If t>=2 then r_i=k-t+1 and every factor has clique number at least this minimum, whence t(k-t+1)<=r'<=k. Also t<=k. Thus (t-1)(k-t)<=0 forces t=k. All r_i are then one. An independent vertex-critical graph consists of one vertex, so every factor has q_i=1, and q=t=k, contrary to q>k. Therefore t=1. Equality then forces m=0 and |H|=2q-1. Thus G=H is vertex-critical and has connected complement. QED.

**Corollary 2.** Every indivisible graph with k>=2 satisfies n>=4k-3. If equality holds, then chi(G)=2k-1 and G is vertex-critical with connected complement.

**Proof.** A proper coloring with at most 2k-2 colors can be grouped into two groups of at most k-1 proper colors, giving a division. Hence chi(G)>=2k-1. For any v, if omega(G[M(v)])<k, the sets N(v) and {v} union M(v) would both have clique number below k: the first is at most k-1, and the second has clique number max(1,omega(G[M(v)])). This would divide G. Thus Theorem 1 applies. Equality in n>=2q-1>=4k-3 forces q=2k-1>k, so its equality restriction applies. QED.

This is an elementary structural derivation using Gallai, **not a best-known numerical Folkman bound**. Section 6 records stronger existing bounds and the exact difference in scope.

## 3. An odd-hole-free chromatic-gap bound

We additionally use the already source-checked Chudnovsky-Robertson-Seymour-Thomas theorem that every K4-free odd-hole-free graph is four-colorable. A triangle-free odd-hole-free graph is bipartite: a shortest odd cycle, if present, is chordless and has length at least five. An independent vertex-critical graph is a singleton. A critical graph with chi=omega is a complete graph, since a maximum clique already has chi vertices and cannot omit a vertex of a vertex-critical graph.

It follows that a factor H_i in (1), when G is odd-hole-free, has exactly one of these forms:

- a singleton, with (q_i,r_i)=(1,1);
- a nontrivial factor with r_i=3 and q_i=4;
- a factor with r_i>=4.

Indeed, a factor with r_i=2 is bipartite; criticality would make it K2, whose complement is disconnected. If r_i=3, q_i is at most four. Equality q_i=r_i would make a complete graph and again disconnect its complement, so q_i=4.

**Theorem 3.** If G is odd-hole-free and q=chi(G)>=r+2, where r=omega(G), then

    n >= 2q-r+3.                                                   (2)

If equality holds, then r>=4 and

    G = K_(r-4) join J,

where J is odd-hole-free, vertex-critical, has connected complement, clique number 4, chromatic number q-r+4, and order 2(q-r+4)-1.

**Proof.** Apply (1), with r'<=r. If there is a factor of clique number at least four, then sum(r_i-1)=r'-t>=3, so t<=r'-3. Therefore n>=|H|>=2q-r'+3>=2q-r+3.

Otherwise let a count singleton factors and b count the (4,3) factors. Then q=a+4b, r'=a+3b, and t=a+b=r'-2b. Since q>=r+2>=r'+2, b=q-r'>=2. Equation (1) gives n>=2q-r'+2b>=2q-r+4. Thus this case cannot attain equality in (2).

Equality in the first case requires G=H, r'=r, t=r-3, and equality in Gallai for every factor. The sum of r_i-1 is exactly three. Hence there is exactly one factor of clique number four and every other factor is a singleton. There are r-4 of those singletons; their removal gives J with the stated parameters. Criticality and complement connectedness of J were established in Section 1. QED.

No existence or sharpness is claimed for the equality family with chromatic gap at least two. The classification is a necessary form conditional on equality.

## 4. Consequences for the original high-incidence core

The accepted core theorem supplies chi(G[X])>=2k-3 and omega(G[X]) in {k-1,k} for any indivisible G with k>=3. For odd-hole-free G and k>=5, the gap is at least k-3>=2, so Theorem 3 gives:

**Corollary 4.** Every odd-hole-free indivisible graph with k>=5 satisfies

    |X| >= 3k-3.

If omega(G[X])=k-1, then |X|>=3k-2.

This strengthens the fourth-pass bounds by one vertex in both cases. If the first bound is attained, then necessarily omega(G[X])=k, chi(G[X])=2k-3, and

    G[X] = K_(k-4) join J,
    omega(J)=4, chi(J)=k+1, |J|=2k+1,

with J vertex-critical, odd-hole-free, and complement connected. If omega(G[X])=k-1 and the second bound is attained, the analogous form is

    G[X] = K_(k-5) join J,
    omega(J)=4, chi(J)=k+2, |J|=2k+3.

The zero-order clique at k=5 in the latter formula means no additional factor. These statements concern the induced core only; its join decomposition does not make the whole graph a join or ensure core-color extension.

At k=4 the previously accepted conditions remain |X|>=8, omega(G[X])=4, and chi(G[X])>=5, without minimality. The eight-core boundary has the following more precise description.

**Proposition 5.** If an odd-hole-free indivisible graph with k=4 has |X|=8, then G[X]=K1 join J, where J is a seven-vertex, 4-critical, odd-hole-free graph of clique number three and connected complement. In particular G[X] is 5-critical and has a universal vertex.

**Proof.** Theorem 3 rules out chi(G[X])>=6, so the chromatic number is five. Choose an induced 5-critical H inside G[X] and decompose it as in (1). A factor of clique number at least four would leave no room for another factor because omega(H)<=4. Gallai would then require |H|>=9, impossible. Thus all factors are singletons or (4,3) factors. Their chromatic sum five and clique sum at most four force exactly one (4,3) factor and one singleton. Gallai requires orders at least seven and one. Hence H=G[X] and all conclusions follow. QED.

We do not classify all such seven-vertex J in this packet. The seven-antihole is one: its complement is C7, it has clique number three, chromatic number four, and deleting any vertex makes it three-colorable. Consequently K1 joined to that antihole is an explicit eight-vertex core satisfying this chromatic boundary. All its vertices already lie in at least three maximum K4s (the universal vertex in seven, every rim vertex in three). The graph itself is divisible by separating the universal vertex from the rim. Thus the boundary is not excluded merely by the core's order, criticality, or join structure.

## 5. Refined clique-cutset side bounds

The accepted separator argument says that for a clique cutset C of a minimal indivisible graph, each side H_i=G[C union D_i] has omega(H_i)=k, has chi(H_i)>=2k-1, and excludes at least one admissible coloring of C. Here minimality uses proper nonedgeless induced subgraphs at their own clique numbers. For odd-hole-free G, each side is odd-hole-free. Applying Theorem 3 gives

    |H_i|>=3k+1  (k>=4).

For k>=5 equality would make H_i=K_(k-4) join J and hence give it a universal vertex. Such a graph cannot exclude an admissible coloring of a clique, by the following elementary observation.

**Universal-vertex flexibility.** Let u be universal in H and let omega(H)=k>=2. Every admissible two-coloring of any clique C extends to a division. If u is prescribed, give every unprescribed vertex the color opposite u. The color of u occurs only on a proper monochromatic subset of C, of size at most k-1; the other color lies in H-u, whose clique number is k-1. If u is not prescribed, choose its color so that at most k-2 vertices of C have that color. This is possible because C lies in H-u and has size at most k-1. Again give all other unprescribed vertices the opposite color. The color of u has at most k-1 vertices, and the other color lies in H-u. Both induced clique numbers are below k.

Therefore |H_i|>=3k+2 for k>=5. If s=|C| and t is the number of components after deletion, counting the common boundary yields

    |G| >= s+t(3k+1-s)             for k=4,
    |G| >= s+t(3k+2-s)             for k>=5.

At k=4 every side has at least 13 vertices; any clique cutset requires at least 22 total vertices, and an edge cutset at least 24. For k>=5 the corresponding bounds are 5k+4 and 6k+2. These are necessary bounds, not constructions, optimality claims, or clique-cutset exclusion. The former trace-orbit restrictions remain unchanged.

## 6. Existing Folkman bounds must take precedence numerically

The condition that G of clique number k is indivisible is exactly the vertex-Ramsey relation G -> (K_k,K_k)^v with no K_(k+1). Thus its minimum possible order over all graphs is the vertex Folkman number F_v(k,k;k+1). This equivalence follows directly from the definitions; it does not use an odd-hole assumption.

A directly inspected primary published source is Aleksandar Bikov and Nedyalko Nenov, *Lower bounding the Folkman numbers F_v(a_1,...,a_s;m-1)*, Annual of Sofia University, Faculty of Mathematics and Informatics 104 (2017), 39-53. Its Theorem 5.2 proves F_v(4,4;5)>=19. Hence:

    every k=4 indivisible graph, and in particular every odd-hole-free one,
    has at least 19 vertices.

This is an imported external computational theorem. The source's definition, theorem, proof outline, Algorithm 3.5 dependence, and reported enumeration table were inspected. Its large graph enumeration was not reproduced or independently certified in this packet. The public journal PDF and the arXiv v1 PDF are separately identified in the source identity record; neither copied source document is included here.

The same source attributes F_v(p,p;p+1)>=4p-1 to Xu and Shao, *On the lower bound for F_v(k,k;k+1) and F_e(3,4;5)*, Utilitas Mathematica 81 (2010), 187-192. We have not inspected that original proof or verified its complete parameter scope; this packet does not import it as an independently checked theorem. This prior-credit observation already rules out describing Corollary 2 as a new or best-known numerical Folkman lower bound. Nor is the 2017 bound of 19 asserted to be the latest best bound as of 2026. The exact imported assertion is the valid historical lower bound in Theorem 5.2.

## 7. Final unresolved boundary and verification scope

The results tighten necessary conditions and clarify the exact source boundary. They do not show that odd-hole-freeness forces satisfiability of the exact signed core constraints. The eight-core k=4 case is narrowed to a universal-vertex critical join but is not excluded, because universalness inside X is not universalness in G. A putative counterexample at k=4 needs at least 19 total vertices by the imported Folkman theorem and at least eight original high-incidence vertices containing K4. If that counterexample is induced-minimal, a clique cutset additionally requires at least 22 total vertices (24 for an edge cutset). For k>=5 the core bounds are 3k-3, or 3k-2 when its clique number is k-1. No arbitrary core-division extension, clique-cutset gluing, or shadow odd-hole inheritance is used.

The checker exhausts all 33,868 labelled simple graphs on orders zero through six; checks all induced-set clique and chromatic values, the antineighborhood hypothesis, critical decomposition, theorem/equality implications, odd-hole-free hypotheses, and direct two-color divisibility; and includes named larger benchmark families and exact finite parameter enumerations. The graph universe includes 1,722 graphs satisfying the antineighborhood hypothesis, 624 of these with chi>omega, and 12 attaining its equality with chi>omega. All 624 indivisible graphs in that small universe have clique number two; the core-gap and k>=3 indivisibility consequences therefore have no nonvacuous exhaustive small case. The universal-vertex construction is separately checked on 24,312 admissible clique-boundary assignments through order five. Seven larger named benchmarks include the eight-core fixture, the join of two seven-antiholes, and the join of two C5s, the last explicitly demonstrating the odd-hole-free hypothesis is necessary for the strengthened gap bound. A separate exact 25-vertex C5[C5] fixture has 125 maximum K4s and is indivisible, certified by all 32 local block colorings and all 243 possible nonempty block-edge-color patterns; it contains an induced C5 and is not an odd-hole-free counterexample. There are 10,814 bounded critical-factor parameter records and 3,213 cutset arithmetic records. The exact mandatory scope, totals, and case-stream hashes are fixed in the mandatory scope record and the exact expected-results record. These finite regressions do not reprove Gallai or CRST, replay the 2017 Folkman enumeration, or resolve the general conjecture.

All acceptance gates use explicit exceptions and are run under normal Python, -O, and -OO. A manifest and externally retained pin fix the complete packet, with mandatory dependency checks, exact regular-file inventory, nonsymlink path components, duplicate-key rejection, and fixed scope. Hostile controls mutate only disposable copies. This certifies a pinned static snapshot and the tested failure modes, not concurrency-race security, all malformed representations, or simultaneous replacement of every trust anchor.
