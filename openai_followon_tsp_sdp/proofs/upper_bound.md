# Exact subset-state upper bound (independent derivation)

For N>=3 fix city 1 and write Q={2,...,N}, q=N-1. Create an acyclic directed graph with source s, sink t, and vertices (S,i) for nonempty S subset Q and i in S. Add arcs s->({i},i), arcs (S,i)->(S union {j},j) for j in Q\S, and arcs (Q,i)->t. Label these arcs by undirected edges {1,i}, {i,j}, and {i,1}, respectively.

The graph has 2+q 2^{q-1} vertices and m=2q+q(q-1)2^{q-2} arcs. The second count follows by fixing ordered i!=j and selecting any S containing i and excluding j among the remaining q-2 cities. All source-sink paths list a permutation of Q; their labels form a Hamiltonian cycle. Every Hamiltonian cycle has two oriented representations. Thus the linear label-sum projection maps path incidence vectors exactly onto tour incidence vectors.

Let z>=0 obey divergence 1 at s, -1 at t, and 0 elsewhere. Every such flow is a convex combination of source-sink unit paths: repeatedly follow positive arcs from s, reaching t because the graph is acyclic and conservation prevents a stop; subtract their minimum positive flow. Finite arc support shrinks at every subtraction. No residual circulation survives in an acyclic graph. Flow coefficients sum to 1. The feasible set consequently projects exactly onto P_TSP(N).

Embed z as the diagonal of an m-by-m real symmetric matrix X; impose X_ab=0 for a!=b and the flow equalities on its diagonal. Positive semidefiniteness is equivalent to z>=0. This is one affine section of S_+^m followed by a linear projection, hence sxc_R(P_TSP(N))<=m=2(N-1)+(N-1)(N-2)2^{N-3}=2^{O(N)}. Size counts matrix order m, not ambient dimension m(m+1)/2 and not maximum block order if scalar blocks are counted separately.

The acyclic flow proof is independent of algorithmic TSP hardness or P versus NP.
