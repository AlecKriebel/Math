# Relative collapse under subdivision: exact local reduction and a planar certificate

**Status: the general problem remains unresolved.** This note records an elementary reduction and a constructive low-dimensional case, with no novelty claim. The known theorem after an additional barycentric subdivision is credited separately. Independent review pending.

Target: 30002061 / OWR-11786-016, Hudson's relative subdivision problem.

## 1. Conventions and the exact remaining question

All complexes here are finite simplicial complexes. An elementary collapse deletes a maximal simplex τ and a codimension-one face σ contained in no other maximal simplex. Neither σ nor τ belongs to the retained target. A collapse is a finite sequence of such moves. The empty face is not deleted in a move.

A subdivision is **linear/geometric on every original simplex**. This is the explicit convention immediately before Problem 2 on printed p. 1460 of the original OWR report [1]. It is not an arbitrary triangulation of a homeomorphic ball and does not mean only a regular/coherent subdivision. Write D|A for the subcomplex consisting of simplices of D contained in a specified original subcomplex or geometric set A.

The question asks whether

\[
 C\searrow C',\qquad D\text{ a linear subdivision of }C,
 \qquad D'=D|\,|C'|
 \quad\Longrightarrow\quad D\searrow D'.
 \tag{1}
\]

The target D' is prescribed. A collapse of D to some other subcomplex or to a point does not establish (1).

Adiprasito–Benedetti [2, Theorem 4.3] prove instead

\[
 \operatorname{sd}D\searrow\operatorname{sd}D'.
 \tag{2}
\]

This is a published, credited theorem, not a new result of this attempt. A sequence on sd(D) is not already a sequence on D. The original report states the same extra-subdivision conclusion in its Corollary 2. The present note does not remove that subdivision in general.

## 2. Reduction to one subdivided simplex with a protected boundary part

For a d-simplex Δ, d≥1, and a facet F of Δ, define the retained boundary subcomplex

\[
 L(\Delta,F)=\partial\Delta\setminus\{F\}.
\]

Only the simplex F itself is removed from the boundary face set; all its proper faces remain. Geometrically, |L(Δ,F)| is the boundary of Δ minus the relative interior of F.

Consider the following local condition in every dimension up to d:

> For every simplex Δ of dimension between 1 and d, every facet F, and every linear triangulation T of Δ, there is a collapse
> \[
> T\searrow T|\,|L(\Delta,F)|.
> \tag{3}
> \]

**Proposition 1.** The universal statement (1) for complexes of dimension at most d is equivalent to this local condition.

**Proof.** Necessity follows by taking C to be the face complex of Δ and C'=L(Δ,F). Deleting the free facet F together with Δ is one elementary collapse.

For sufficiency, take an elementary step C_i↘C_{i+1} deleting (σ,τ), and put D_i=D|\,|C_i|. The restriction T=D_i|τ is a linear triangulation of τ. Because σ is free,

\[
 T\cap D_{i+1}=T|\,|L(\tau,\sigma)|=:K,
 \qquad D_i=T\cup D_{i+1}.
 \tag{4}
\]

Use (3) to collapse T onto K. Each pair removed in this local sequence remains a free pair after adjoining D_{i+1}. To see this explicitly, suppose a removed free face a had an additional coface b in D_{i+1}. Since D_{i+1} is a subcomplex, it would also contain a. Then a would lie in T∩D_{i+1}=K, contradicting that the local collapse retains K. No new obstructing coface can therefore occur outside T. The local sequence gives D_i↘D_{i+1}.

Apply this to every elementary step of C↘C'. The final restriction is exactly D', proving (1). ∎

This reduction also identifies why an absolute collapsibility theorem for every subdivided simplex is not, by itself, the missing argument: (3) must retain the whole specified boundary subcomplex K throughout.

## 3. Every triangulated disk collapses to a proper boundary path

**Proposition 2.** Let T be a finite triangulated closed 2-disk, and let K be a nonempty connected proper subcomplex of its boundary. Then T collapses to K. Here K is a path or a single vertex.

**Proof.** Choose a boundary edge e not in K and let τ0 be its unique incident triangle. The dual graph of the triangles, joining triangles that share an interior edge, is connected. Indeed, an interior path between two triangle interiors can be chosen to avoid all vertices and cross edges transversely; it then gives a dual walk. Choose a spanning tree of this dual graph rooted at τ0.

Process the triangles in an order with each parent before its children. Delete τ0 paired with e. For a later triangle τ, pair it with its shared edge e_τ with its parent. At that time the parent triangle has been removed, while τ remains. An interior edge of a triangulated disk has exactly two incident triangles, so e_τ is now a free edge. It has not been removed earlier: a previous move removed only its own triangle and the edge to its own parent, whereas e_τ joins the present triangle to its parent. No pair removes a face of K. The root edge was chosen outside K and all later paired edges are interior.

After all triangles have been removed, the remaining complex G is a finite graph containing K. Every move was an elementary collapse, so G is connected and contractible. A finite connected graph is contractible exactly when it is a tree. Thus G is a tree containing the connected subtree K.

If G differs from K, it has a leaf outside K. One way to see this is to take a vertex outside K of maximum graph distance from K; in a tree it has no neighbor farther from K, hence is a leaf. Pair that vertex with its sole edge. Repeating this pruning retains K and ends exactly at K. ∎

The argument gives an explicit certificate: a parent-first dual spanning tree for the triangle removals, followed by ordinary leaf pruning. It does not presume a shelling or use a barycentric refinement.

**Corollary 3.** For dim(C)≤2, the exact relative statement (1) holds.

For dimension one, a subdivided interval collapses onto either prescribed original endpoint by pruning from the opposite end. For dimension two, the retained part of the boundary of a triangle is the path consisting of the other two sides, with their subdivisions. Proposition 2 supplies (3), and Proposition 1 passes this local sequence through every collapse step of C. Dimension-zero complexes have no nontrivial elementary moves under the stated convention.

This is a classical low-dimensional case, included as a checkable reconstruction and not advertised as a new theorem. Chillingworth's stronger three-dimensional convex-collapse results and their later developments belong to the existing literature; the present elementary certificate proves only the case explicitly stated above.

## 4. The exact higher-dimensional gap

The parent-first dual-tree procedure can remove top-dimensional simplices through selected codimension-one faces in a triangulated ball. In dimension two, its remaining complex is a graph, and contractibility forces that graph to be a tree that can be pruned relative to K. In higher dimensions the residual complex has dimension at least two. Connectedness and contractibility do not provide an analogous relative free-face sequence. This method supplies no such sequence and stops there.

In particular, none of the following fills the gap:

- Replacing the desired target K by an unspecified point
- Treating contractibility or simple-homotopy equivalence as a sequence of collapses without expansions
- Importing (2) and pretending its subdivided faces were already faces of D
- Using a noncollapsible PL ball without proving it is a linear subdivision of the relevant original simplex
- Using a nonshellable example, such as Rudin's ball, as if nonshellability implied noncollapsibility

The outstanding local requirement is exactly (3) in the higher-dimensional cases not covered by a verified existing theorem, or a genuine linear triangulation violating it. No such proof or counterexample has been produced here. The original record remains **unsolved in this attempt**.

## 5. Finite controls and source precision

The accompanying checker constructs exact rational planar triangulations, produces the dual-tree/pruning certificates, and verifies each removed pair directly against the current face set. It also checks that protected faces survive, that the final face set equals the specified target, and that local certificates remain valid after adjoining a second triangulated region along protected faces. These checks support the finite algorithm; they are not a search over arbitrary high-dimensional subdivisions.

The full original OWR passage and the relevant published Adiprasito–Benedetti proof were read. The published Theorem 4.3 reduces to one original elementary collapse, then uses endo-collapsibility after derived subdivision. That source proof explicitly keeps the extra subdivision and cannot simply be reused without it.

## References

1. K. A. Adiprasito, joint work with B. Benedetti, *Barycentric Subdivisions, Shellability and Collapsibility*, in *Triangulations*, OWR24/2012, printed pp. 1459–1462; Problem 2 and Corollary 2 p. 1460. [Full report](https://ems.press/content/serial-article-files/46393?nt=1), DOI [10.4171/OWR/2012/24](https://doi.org/10.4171/owr/2012/24)
2. K. Adiprasito and B. Benedetti, *Barycentric Subdivisions of Convex Complexes are Collapsible*, Discrete & Computational Geometry **64** (2020), 608–626, [DOI 10.1007/s00454-019-00137-3](https://doi.org/10.1007/s00454-019-00137-3), [full published article](https://par.nsf.gov/servlets/purl/10169029). Theorem 4.3 corresponds to Theorem 4.0.3 in [arXiv:1709.07930v1](https://arxiv.org/abs/1709.07930v1).
3. D. R. J. Chillingworth, *Collapsing three-dimensional convex polyhedra*, Math. Proc. Cambridge Philos. Soc. **63** (1967), 353–357, [DOI 10.1017/S0305004100041268](https://doi.org/10.1017/S0305004100041268); correction **88** (1980), 307–310. These are credited background, not a new three-dimensional proof in this note.
