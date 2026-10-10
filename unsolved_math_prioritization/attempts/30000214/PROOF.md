# A negative answer to the homology-sphere cover question

## Result and scope

There exists a finite, two-dimensional simplicial complex K that is doubly Cohen–Macaulay over Q but contains no two-dimensional homology-sphere subcomplex over any field. In particular, the homology-sphere version of Nevo's decomposition question has a negative answer: even an unordered cover is impossible. This disproves the statement before its overlap and reordering requirements arise.

The coefficient field in the counterexample is fixed throughout as Q. The same K works over every characteristic-zero field, by invariance of ranks of integer boundary matrices under characteristic-zero extension. No assertion for every prescribed positive characteristic is needed or made. No subdivision is performed. “Homology sphere” includes the homology conditions on every face link, including the empty face.

The construction uses the unconditional vertex-regular lattice of Lubotzky–Samuels–Vishne (LSV). It does not use their Ramanujan-spectrum theorem or any global Jacquet–Langlands correspondence. All spectral and homology arguments needed below are proved directly.

## 1. A finite complex with projective-plane links

Set q=11, F=F_11((y)), and t=1/y. Let B be the affine building of PGL_3(F). Its lattice-chain description in [LSV, Section 2] makes it a connected, locally finite, pure two-dimensional simplicial complex. For each vertex x, the link is the incidence graph G of the points and lines of PG(2,11): the nonzero proper subspaces of F_11^3, with adjacency given by inclusion.

The unconditional input from [LSV, Sections 3–4, especially Proposition 4.8] is a group Γ acting simply transitively on the vertices of B and a faithful matrix representation

    ρ: Γ → GL_9(F_11[t]).

Indeed LSV use the conjugation representation on a nine-dimensional algebra, define R_0=F_q[1/y], and prove Γ=Γ′⊆GL_9(R_0). Their Equation (9) shows that the matrices of the generators b_u have entries of degree at most one in t. By Corollary 4.6, each vertex adjacent to a fixed base vertex o is γo for an element γ that is either a b_u or a product of two b_u's. Hence each such neighbor element has matrix entries of degree at most two.

Define the finite-index normal subgroup

    Γ_9 = ker(Γ → GL_9(F_11[t]/(t^9))).

If γ∈Γ moves o a graph distance at most four, a path from o to γo expresses γ as a product of at most four neighbor elements. Its matrix entries consequently have degree at most eight. If also γ∈Γ_9, every entry of ρ(γ)−I is divisible by t^9 and has degree at most eight. Thus ρ(γ)=I and γ=1. Normality and vertex transitivity then imply

    dist(x,hx)>4 for every vertex x and every nonidentity h∈Γ_9.   (1)

For completeness, if x=go, the distance in question equals dist(o,g^−1hgo); normality puts g^−1hg in Γ_9, so the preceding argument applies.

Let K have vertex set Γ_9\B^(0), and define its simplices to be the images of simplices of B. This is a genuine finite abstract simplicial complex, with no repeated vertices in a simplex. There are finitely many vertex orbits because Γ_9 has finite index and Γ is vertex-transitive. Connectedness follows from that of B. Its maximal dimension is two, and every face lies in a triangle.

Here is the needed local verification, beyond merely torsion-freeness. Distinct vertices in the closed star of x are at distance at most two, so (1) prevents them from having the same image. Every quotient triangle containing the image of x lifts to a triangle containing x: choose a lift and translate its vertex in the orbit of x to x. The other vertices of that lift are then uniquely determined, because two neighbors of x in the same orbit would violate (1). The identical argument applies to edges. Consequently

    lk_K(v) ≅ G for every vertex v of K.                         (2)

In particular the quotient has unchanged links, and the passage to an abstract simplicial complex has neither collapsed nor identified local faces. The construction is the orbit complex, not an operation of adjoining extra cliques.

Only the building description, the explicit polynomial representation, and the simply transitive lattice action have been used from LSV. Their Section 6 Ramanujan assertion plays no role.

## 2. Link expansion survives a vertex deletion

The graph G has 133 point vertices and 133 line vertices and is 12-regular. Let M be its 133×133 point–line incidence matrix. Two distinct points lie on one common line, while each point lies on 12 lines. Therefore

    MM^T = 11 I + J.

The adjacency eigenvalues of G are 12, −12, and ±√11. It follows that, for a real function f of unweighted mean zero on G,

    Σ_{ab∈E(G)}(f(a)−f(b))² ≥ (12−√11) Σ_a f(a)².               (3)

This is also a direct proof that G is connected. Bipartiteness excludes odd cycles, and uniqueness of the line through two points excludes four-cycles, so G has girth at least six.

Let H=G−w, with any one vertex w deleted. For a real function x of unweighted mean zero on H, extend x by zero at w. Its extension still has mean zero on G. Applying (3) and subtracting the energies of the edges incident to w gives

    Σ_{ab∈E(H)}(x(a)−x(b))²
      ≥ (12−√11)Σ_{a∈H}x(a)² − Σ_{a∼w}x(a)²
      ≥ (11−√11)Σ_{a∈H}x(a)².                                (4)

In particular H is connected. Its degrees are 11 or 12.

We use the normalized spectral gap in its precise weighted-variance form:

    λ(L)=inf_{f nonconstant} E_L(f) /
          min_c Σ_a deg_L(a)(f(a)−c)²,

where E_L(f)=Σ_{ab∈E(L)}(f(a)−f(b))². Subtracting the unweighted mean in (4), and using deg_H≤12, yields

    λ(H) ≥ (11−√11)/12 > 7/12 > 1/2,                         (5)

where √11<4. Similarly

    λ(G) = (12−√11)/12 > 1/2.                               (6)

These inequalities use the actual, generally unequal degrees of H. They do not treat a deleted link as if it remained regular.

## 3. A weighted cocycle proof of H^1 vanishing

We prove the exact finite-complex spectral implication needed here.

Lemma. Let X be a finite pure two-dimensional simplicial complex such that every vertex link is connected and has normalized spectral gap strictly greater than 1/2. Then H^1(X;R)=0.

Proof. Give each edge e the positive weight m(e), the number of triangles of X containing e. Represent a real simplicial 1-cocycle by antisymmetric numbers a_uv=−a_vu. In its cohomology class choose a representative minimizing

    E(a)=Σ_{unoriented edges uv} m(uv)a_uv².

The minimum exists: this is a positive-definite norm on a finite-dimensional vector space, and coboundaries form a linear subspace. Orthogonality to all coboundaries gives, at each vertex v,

    Σ_{u∼v} m(vu)a_vu=0.                                    (7)

On the graph lk_X(v), put f_v(u)=a_vu. The degree of u in this graph is exactly m(vu), so (7) is exactly the weighted-mean-zero condition for the normalized link Laplacian. For a triangle {v,u,w}, the cocycle equation implies

    f_v(u)−f_v(w)=−a_uw.

Let λ be the minimum link gap; there are finitely many vertices, so λ>1/2. The link Poincaré inequality gives

    Σ_{{u,w}∈E(lk_X(v))} a_uw²
       ≥ λ Σ_{u∼v} m(vu)a_vu².                              (8)

Summing (8) over v, each edge uw on the left occurs once per triangle containing it. Thus the left sum is E(a). Each edge appears at its two endpoints on the right, so that sum is 2λE(a). Hence E(a)≥2λE(a), forcing E(a)=0. The chosen representative is zero, proving the lemma. ∎

All weights in this proof are determined by X itself. The lemma therefore applies unchanged after deleting a vertex, using the surviving triangle counts.

## 4. All Cohen–Macaulay conditions, before and after deletion

Fix any vertex z of K, and put X=K−z, the induced deletion.

Purity and dimension. Each edge of K belongs to exactly 12 triangles: this is the degree of the corresponding link vertex in (2). Deleting z removes at most one triangle through any surviving edge, so every surviving edge is in at least 11 triangles. Each vertex originally has 266 neighbors and loses at most one, so there are no isolated surviving vertices. Thus every face of X is contained in a triangle, and X is pure of dimension two. K is itself pure of dimension two by construction.

Connectedness. K is connected. To connect two surviving vertices, take a graph path in K. Whenever it passes through z as a–z–b, replace that segment by a path from a to b in the connected graph lk_K(z)=G. That replacement uses no z. Thus X is connected.

Vertex links. For each surviving vertex u,

    lk_X(u)=lk_K(u)                        if {u,z}∉K,
    lk_X(u)=lk_K(u)−z                      if {u,z}∈K.

Consequently every vertex link in X is G or a one-vertex deletion of G. Equations (5)–(6) show both connectedness and a gap greater than 1/2 for every such link. The same statements hold for the vertex links of K.

Global first homology. Section 3 gives H^1(K;R)=H^1(X;R)=0. Finite-dimensional duality over a field gives H_1(K;R)=H_1(X;R)=0. Since the boundary matrices have integer entries, their ranks over Q and R agree, and H_1(K;Q)=H_1(X;Q)=0.

Remaining links. A surviving edge has a nonempty zero-dimensional link (at least 11 vertices in X, 12 in K). The link of a facet is the complex consisting of the empty face. Thus all negative-degree reduced-homology requirements hold as well.

Reisner's criterion for a finite pure two-dimensional complex now applies face by face: the empty face requires connectedness and H_1=0; a vertex requires a nonempty connected one-dimensional link; an edge requires a nonempty zero-dimensional link; a facet imposes no further vanishing below dimension −1. All these conditions have been established over Q for K and for every X=K−z. Hence K is doubly Cohen–Macaulay over Q.

Using real linear algebra to prove the vanishing of rational homology does not change the coefficient field of the claimed example: it proves the ranks of its rational boundary maps. Equivalently the conclusion holds over every characteristic-zero field.

## 5. No homology-sphere subcomplex exists

Suppose S⊆K is a two-dimensional k-homology sphere, with the local-link condition, over any field k.

For an edge e of S, its link has the reduced homology of S^0. A zero-dimensional complex with that homology has exactly two vertices. Therefore every edge of S lies in exactly two triangles. For a vertex v of S, its link is a graph. Each vertex of that graph has degree two, by the preceding edge condition, and the homology-sphere condition makes the graph connected. Thus lk_S(v) is a simple cycle. Being a subgraph of lk_K(v)=G, its length is at least six.

Write f_i=f_i(S). The cycle lengths show that every vertex of S has at least six neighbors, so 2f_1≥6f_0. The two-triangle edge condition gives 3f_2=2f_1. Consequently

    χ(S)=f_0−f_1+f_2=f_0−f_1/3≤0.

But the global homology of a two-dimensional k-homology sphere gives χ(S)=2, a contradiction.

This argument never assumes orientability from the outset, never identifies a global rational homology sphere with a topological sphere, and never omits the local links. Its incidence and Euler-characteristic equalities hold over every coefficient field. Therefore K contains no allowed sphere piece at all. It cannot have the requested finite cover, in any ordering. ∎

## References

[Nevo-OWR] E. Nevo, “Rigidity and the lower bound theorem for doubly Cohen–Macaulay complexes,” contribution to Oberwolfach Report 17/2005, printed pp. 960–961: Definition 1, Theorem 7, Problem 8. https://ems.press/content/serial-article-files/45990

[Nevo] E. Nevo, “Rigidity and the Lower Bound Theorem for Doubly Cohen–Macaulay Complexes,” Discrete & Computational Geometry 39 (2008), 411–418. The inspected manuscript is arXiv:math/0505334v2, especially Definition 3.1, Theorem 3.4 and Problem 3.7. https://arxiv.org/abs/math/0505334v2

[LSV] A. Lubotzky, B. Samuels and U. Vishne, “Explicit constructions of Ramanujan complexes of type Ã_d,” European Journal of Combinatorics 26 (2005), 965–993, DOI 10.1016/j.ejc.2004.06.007. The inspected manuscript is arXiv:math/0406217v2, especially Section 2, the conjugation embedding on p. 9, Corollary 4.6, Definition 4.7, Equation (9), and Proposition 4.8 on pp. 12–13. https://arxiv.org/abs/math/0406217v2

Status: authored counterexample proof for independent review. This manuscript does not claim priority, a comprehensive literature search, or verification of unrelated statements in the cited papers.
