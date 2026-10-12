# Strong NP-completeness of aggregate root-dependent spanning-tree cost

**ID 30003996 / OWR-16633-013. Status:** mathematically audited candidate; final fresh family authentication pending, priority unestablished. Two substantive approaches used. No novelty or human peer-review claim.

## Exact source and decision formulation

Volker Kaibel's Problem 1 in [Oberwolfach Report 50/2018](https://ems.press/content/serial-article-files/46772?nt=1), printed p3014, asks whether minimizing the sum of root-dependent arborescence costs is NP-hard. Each undirected edge supplies both directed arcs, and each vertex r has its own arbitrary arc-cost vector c_r. This is not the adjacent Problem 2, which assigns costs to paths in one fixed-root arborescence.

We prove the following precise decision version strongly NP-complete. The input is a finite connected simple undirected graph G=(V,E), a nonnegative integer c_r(u,v) for every r in V and both orientations of each edge, and an integer threshold K, all explicitly encoded in binary. Is there a spanning tree T such that

    F(T)=sum_(r in V) sum_((u,v) in T^r) c_r(u,v) <= K?       (1)

Here T^r is oriented away from r. If the source instead uses inward arborescences, replace every c_r(u,v) by c_r(v,u); this preserves every objective and the reduction. The construction uses only costs 0,1,n+1 on a graph with N=n+m+2 vertices and K=(n+1)m+n. Thus hardness also holds with unary-encoded numerical data. Since this nonnegative-integer subclass lies inside the source's real cost vectors, it establishes the requested optimization hardness under ordinary finite input encoding.

Membership in NP is immediate: check the N-1 listed edges form a spanning tree, orient them by a traversal from each root, and add the binary costs. Both the number of operations and bit lengths are polynomial in the explicit input size.

## Reduction from 3-CNF satisfiability

Use the standard NP-completeness of satisfiability with at most three literals per clause, as in [Karp's original reduction list](https://doi.org/10.1007/978-1-4684-2001-2_9). Remove repeated literals and tautological clauses. An empty clause maps to a fixed no-instance: two vertices with their unique edge, all arc costs1 at both roots and threshold1, whose unique tree has cost2. An empty remaining formula maps to the same graph with all costs0 and threshold0, a fixed yes-instance. Delete unused variable declarations and relabel the actual occurring variable symbols densely; n counts these symbols, never the largest numeric label. Consequently assume n>=1 variables and m>=1 nonempty clauses, with no variable occurring in both signs within one clause. Clauses may have one, two or three literals. These elementary preprocessing steps preserve the NP-hard source problem.

Construct vertices:
- two hubs t and f;
- one vertex v_i for each variable x_i;
- one vertex q_j for each clause C_j.

Construct edges:
- the hub edge tf;
- tv_i and fv_i for every variable;
- q_j v_i when x_i or its negation occurs in C_j.

The graph is simple and connected. It has N=n+m+2 vertices and at most 1+2n+3m edges. Set B=n+1 and K=Bm+n.

### Costs at the hub root t

For both orientations of an edge, set

    c_t(tf)=0,
    c_t(tv_i)=c_t(fv_i)=1,
    c_t(q_j v_i)=B.                                         (2)

This vector is symmetric in arc direction, so its contribution is an ordinary edge sum independent of the orientation at t.

### Costs at each clause root q_j

For variables occurring in C_j, assign

    c_(q_j)(v_i,t)=0 and c_(q_j)(v_i,f)=1   if x_i occurs,
    c_(q_j)(v_i,t)=1 and c_(q_j)(v_i,f)=0   if not x_i occurs. (3)

Every other arc cost at root q_j is zero, including the reverse hub-to-variable arcs and the costs for variables absent from C_j. Cost vectors for the remaining roots f and all v_i are identically zero. These rules fully specify (1) and involve no tree-dependent or unencoded data.

## Structural threshold lemma

For any spanning tree T let q be its number of clause-variable edges, p its number of hub-variable edges and h be1 if tf lies in T and0 otherwise. Every clause vertex has degree at least1 and is incident only to clause-variable edges. Each such edge is incident to exactly one clause vertex. Hence q>=m.

Counting all tree edges gives

    p+q+h=N-1=n+m+1.

The cost at root t is therefore exactly

    p+Bq = K+(1-h)+n(q-m).                                  (4)

All other costs are nonnegative. If F(T)<=K, equation(4) forces h=1 and q=m. Consequently every clause vertex is a leaf. Deleting these leaves leaves a tree on the hubs and variable vertices containing tf. Each variable must attach to at least one hub; it cannot attach to both because that would form a triangle with tf. Thus every variable has exactly one hub attachment. Such a tree encodes a truth assignment: x_i is true exactly when tv_i is present.

Conversely, any truth assignment together with a choice of one incident variable for each clause defines a tree of precisely this form, with base cost K.

## Literal-cost lemma

Consider a structured tree from the preceding lemma and root it at q_j. Let v_i be the unique neighbor of q_j. The path toward the hub core begins q_j -> v_i -> h_i, where h_i is the chosen hub for v_i. Thus its hub edge is directed v_i -> h_i. Every other variable edge is directed from its hub toward that variable: after removing the selected clause leaf, the core is two stars joined by tf, and the unique route from q_j enters any other variable from the hub side.

Therefore exactly the selected variable's hub edge can contribute a nonzero cost from vector c_(q_j). By(3), its contribution is0 exactly when the selected literal in C_j is true under the encoded assignment, and1 otherwise. All other arc contributions from that root are zero. It follows that for every structured tree

    F(T)=K + number of clauses whose selected literal is false. (5)

## Correctness and complexity

If the formula is satisfiable, attach variables to their truth-value hubs and attach each clause leaf to a variable furnishing a true literal. This is a spanning tree and(5) gives cost K.

If a spanning tree has cost at most K, the structural lemma yields an assignment and selected literals, and(5) says every selected literal is true. Every clause is satisfied. Hence the formula is satisfiable if and only if the decision instance is a yes-instance.

The graph, all N cost vectors and K are computable in polynomial time. Every cost is at most n+1<=N, and K is polynomially bounded in N. The same reduction remains polynomial when the integers are encoded in unary, establishing strong NP-hardness. Together with NP membership it proves strong NP-completeness, and hence NP-hardness of finding an optimal tree.

If strictly positive costs are desired, add1 to every arc cost for every root and add N(N-1) to K. Every spanning tree uses exactly N-1 arcs for each of N roots, so this changes all objectives by the same constant and preserves the answer. We make no bounded-degree, planar, fixed-number-of-roots, approximation or adjacent path-cost claim.

## Verification and boundaries

`verify.py` constructs explicit cost vectors, enumerates spanning trees for a finite suite of small formulas, independently orients each tree from every relevant root, and checks the reduction in both directions. It also checks equation(4) on every enumerated tree, including unstructured ones, and validates satisfying-assignment witnesses. These controls support the all-size proof above; finite enumeration alone is not the hardness proof.

The primary source's Problem1 and Problem2 are kept distinct. The standard NP-completeness of 3-CNF satisfiability is the imported complexity-theoretic input. A current source search found no exact earlier resolution of this target, but priority has not been established. No external outreach or journal submission is involved.

The inherited native runtime was used without model or reasoning-setting changes; the exact runtime model identifier was not exposed to this worker.
