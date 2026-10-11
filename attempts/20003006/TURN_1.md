# Turn 1: the all-degree strong-grid model and Grandis's comparison

Status: complete candidate theorem for an explicitly specified model; independent source-scope and proof review required. This is a credited consequence of Grandis's construction and realization theorem, with the finite-domain comparison proved below. It is not a claim to identify every convention called digital homotopy or digital homology.

## 1. Definitions and theorem

Let X be a finite set with reflexive symmetric adjacency, with basepoint x₀. Maps preserve adjacency. For a positive integer vector m=(m₁,…,mₙ), let B_m be the integer box ∏[0,mᵢ] with adjacency u~v precisely when |uᵢ−vᵢ|≤1 for every i. Its boundary consists of vertices with some coordinate equal to 0 or mᵢ. A based n-array is an adjacency-preserving f:B_m→X constant at x₀ on the boundary.

If M≥m coordinatewise, extend f by x₀ on B_M outside B_m. Declare f and g equivalent when their basepoint extensions to a common box are joined by a map H:B_M×[0,T]→X for categorical adjacency, stationary at x₀ on ∂B_M×[0,T]. Denote the quotient by D_n(X,x₀). The equivalence relation is established in Section 2. For D₀ use graph components, with their distinguished component when based.

For n≥1 define a product by first padding the last n−1 coordinates to common lengths, then concatenating in coordinate 1 with a one-unit basepoint pause. Specifically, if the first-coordinate lengths are m₁ and r₁, use f for i₁≤m₁ and the translate of g for i₁≥m₁+1. Both interface slices are constant x₀. The remaining coordinates use the padded common box.

**Theorem.** The D_n are natural groups for n≥1, abelian for n≥2. The functor

F(X)=|Cl(X)|,

where Cl(X) is the clique complex and maps act by their vertex functions, has natural isomorphisms

D_n(X,x₀) ≅ π_n(F(X),x₀), for all n≥1,

and a natural bijection on components. In degree 1, D₁ is naturally the published Lupton–Oprea–Scoville subdivision-based fundamental group. In degree 2, D₂, including its group law, is naturally the published Lupton–Musin–Scoville–Staecker–Treviño-Marroquín group. Thus these two already specified digital groups admit an all-degree extension using exactly the same strong rectangular model, realized by one functor F.

The published input for all degrees is Grandis, *An intrinsic homotopy theory for simplicial complexes, with applications to image analysis*, Applied Categorical Structures 10 (2002), 99–155; the complete author version arXiv:math/0009166v1, §§2.1–2.8, 6.2 and Theorem 6.6, is used here. All new notation D_n distinguishes this chosen extension from unverified or incompatible existing definitions.

## 2. Elementary finite-domain facts

**Boundary extension.** Extending a based array by x₀ is continuous. An edge joining the old box to its exterior can only have its interior endpoint on the old boundary: an integer vertex strictly interior has distance at least two from any exterior vertex in some coordinate. Both relevant values are therefore x₀. The same argument extends a boundary-fixed homotopy, including its time-coordinate cross edges.

Consequently extension-equivalence is reflexive and symmetric, and is transitive: extend two homotopies to a common larger box, using the previous observation, then concatenate the time intervals. At the common time slice both homotopies agree, so every cross-time adjacency is already checked in one of the constituent homotopies. Postcomposition preserves the relation. No separate coordinatewise-in-time test replaces categorical continuity.

**Clique comparison.** A finite subset of a strong integer grid is a clique exactly when every coordinate takes at most two consecutive values. The clique complex of B_m is therefore the categorical product of the simplicial intervals. An array B_m→X is exactly a simplicial map Cl(B_m)→Cl(X). This uses flagness of the target Cl(X): pairwise adjacency suffices for its image to be a simplex. For maps f,g with this domain, a one-step strong homotopy is equivalent to simplicial contiguity. Indeed its cross-time condition is f(u)~g(v) whenever u~v. This condition makes f(σ)∪g(σ) a clique for each domain simplex σ; conversely apply contiguity to each two-vertex domain edge, including singleton loops.

The domain is not a triangulated Euclidean cube. A unit square gives a tetrahedron; a unit n-cube gives a simplex with 2ⁿ vertices. A continuous Euclidean cube map used later is obtained by multi-affine interpolation of its vertex labels inside the image simplex, not by identifying the whole domain realization with a Euclidean cube.

## 3. Delays and translations, with the strong cross edges checked

Consider a simplicial net a:Zⁿ→K, supported in a finite integer box, whose faces are constant at the basepoint. A net here means that every elementary unit cube has its entire set of vertex labels in one simplex of K. For K=Cl(X), this is precisely strong-grid continuity. Zero outside a box is equivalent to finite support with all faces constant at the basepoint.

For an integer s define δ_s(j)=j for j≤s, and δ_s(j)=j−1 for j>s. Let a_s be a with δ_s applied in one selected coordinate. For adjacent thresholds s and s+1, a_s and a_{s+1} are contiguous. To see this, take a unit cube in the domain. Its selected coordinate is {j,j+1}. The union of its images under δ_s and δ_{s+1} is either a singleton or two consecutive integers: for j=s it is {s,s+1}, and for j=s+1 it is again {s,s+1}; outside these two cases the two images agree. The other coordinates are unchanged. Thus both cube images lie in one original unit cube, and their combined labels form a simplex. In the graph case this verifies every spatial/time cross edge.

For s at or beyond the upper support face, a_s=a. Moving s finitely down to any chosen threshold gives a finite caterpillar homotopy. It stays constant outside a common finite box, with fixed basepoint faces. This proves invariance under insertion of a repeated coordinate layer. It also proves invariance under finite translations: if s is at or below a lower support face, a_s is the unit right translate of a. Reverse the same finite homotopy for left translation and repeat in the necessary coordinates.

For arrays initially anchored in the nonnegative box, right translations can be performed within a larger nonnegative box: take thresholds from the upper bound down to 0. The coordinate-0 face remains x₀, and the added upper face is x₀. Reversing this shows that an array shifted right by a common nonnegative vector represents the same finite-domain class. This last, boundary-preserving form is needed for injectivity below.

This argument is Grandis's caterpillar mechanism (§2.8) in finite-array language. A direct one-step translation generally fails: for the path a(0),a(1),a(2) with only consecutive distinct labels adjacent, it can require a(0)~a(2). No such one-step translation is used.

## 4. Exact comparison with the integer-supported model

Write Π_n^G(K) for Grandis's intrinsic group π₀(ΩⁿK). His path functor consists of maps Z→K constant outside a finite interval. Its n-fold iteration consists of nets Zⁿ→K constant beyond finite coordinate bounds, with loop faces at the basepoint (§§2.1–2.4 and 6.2). A finite path in ΩⁿK is a fixed-face net homotopy with a **common finite** support in the n spatial coordinates.

Here uniform support is not an extra compactness assumption. An outer path has finitely many nonconstant slices. Inductively each slice in PⁿK has a finite support box; the union of the finitely many boxes, and the endpoint supports, is contained in a common finite box. Conversely a finite supported net has exactly such an iterated-path interpretation. The linked-set structure on the function complexes requires all labels in every unit cube, not merely coordinatewise edge conditions for a nonflag K.

Send a based finite array f to its zero extension a_f:Zⁿ→Cl(X). The boundary-extension argument proves it is a net. Extending f to a larger nonnegative box does not change a_f. A finite rectangular homotopy extends in the spatial variables by the basepoint and in the time variable by its endpoint arrays; it is a Grandis fixed-face homotopy. Thus we have a natural map

q:D_n(X,x₀)→Π_n^G(Cl(X),x₀).

**Surjectivity.** Choose a finite support box for any representative integer net. Translate it by a sufficiently large nonnegative vector so that its support lies in a nonnegative box. Section 3 shows that translation preserves its Grandis class. Restrict to a larger nonnegative box whose boundary has only basepoint labels. This is a based finite array mapping to the desired class.

**Injectivity.** Suppose a_f and a_g are joined by a path in ΩⁿCl(X). Choose a common finite spatial support box for all its slices, and translate the entire homotopy so this box lies in a nonnegative box with basepoint boundary. It restricts to a finite categorical homotopy between right-translated copies of f and g, each padded by the basepoint. Section 3 identifies these right-translated copies with the original finite-domain classes of f and g. Therefore f and g are extension-equivalent. This addresses homotopies whose original support runs through negative integer coordinates; simply restricting them to the positive orthant would be invalid.

**Products.** After padding transverse coordinates, our first-coordinate product becomes an admissible concatenation of two Grandis nets with one repeated basepoint layer. Grandis's §2.5 permits a choice of admissible supports; changing these supports changes the result by delays. Section 3 removes the extra basepoint pause. Therefore q preserves products. Grandis's §6.2 proves these products form groups and commute for n≥2. The bijection q consequently proves precisely the same assertions for D_n; the group property is not assumed to prove injectivity.

All constructions commute with based adjacency-preserving maps, including maps that collapse vertices and edges. Thus q is natural.

## 5. Realization and agreement with the two published digital groups

Grandis's Theorem 6.6 supplies a natural group isomorphism

Π_n^G(K)→π_n(|K|)

for every pointed simplicial complex K and all n≥1. Its representative map extends the labels of every unit cube multi-affinely in barycentric coordinates. The simplex condition puts the entire interpolation inside |K|, and the fixed faces remain based. Composing with q proves the stated realization theorem for all n. The component assertion is immediate from edge paths. This is an application of the prior theorem, not a claimed new all-degree simplicial-approximation theorem.

For completeness, F is an unbased functor on digital images. An adjacency-preserving vertex map sends each clique to a clique, hence induces a simplicial map, and realization preserves identity and composition. Choosing a basepoint then gives the natural group maps above. Digital strong homotopies become finite contiguity chains and therefore ordinary homotopies of realized maps.

### Degree 1

The quotient D₁ is the usual edge-path group of Cl(X). One direction follows from realization/Grandis, or directly from a strong grid strip. For a representative-level check, repeating a path vertex is a delay and Section 3 shows it is harmless; inserting a vertex across a triangle is performed by first repeating an endpoint, then changing that repeated value in one strong homotopy step, since all three labels belong to a clique. These are the elementary edge-path relations, including deletions by reversal. Conversely a strong one-step strip is simplicial contiguity of interval maps and yields an edge homotopy. Products differ at most by one repeated basepoint.

Lupton–Scoville, arXiv:1910.08189v1, Theorem 4.6, identifies the **published subdivision-based** fundamental group with this edge group by the identity on loop vertices. Hence our identification is natural and uses exactly those published classes, without assuming that uniform subdivisions and arbitrary extensions are definitionally the same.

### Degree 2

Definitions 2.9 and 4.1 of the published 2024 second-group paper are exactly our based strong rectangles and common-basepoint-extension relation. Thus the underlying equivalence classes agree literally. Its multiplication places f and g in diagonally opposite blocks, rather than side by side. To compare operations, pad to the diagonal product's outer rectangle. On the right-hand slab only, move g from transverse offset 0 to transverse offset m₂+1 by the caterpillar translations of Section 3. The whole boundary of the g-block stays at x₀. In particular, its left boundary and the right boundary of the f-slab are constant at x₀, so patching this homotopy to the fixed left slab preserves all cross-interface categorical adjacencies. The result is exactly the diagonal product after basepoint padding. Thus the group laws agree.

Equivalently, the identity on labels identifies this group with the face group of Cl(X): Section 2 proves the map and homotopy correspondence, the trivial extensions agree, and both published face/digital products use the same diagonal blocks. The face-group Theorem 8.1 then supplies an independent credited degree-2 realization route. Section 9 already announces this digital application; no novelty is claimed for it.

## 6. Source coverage, limitations and controls

The AIM question explicitly presupposes that higher groups have been constructed. The theorem supplies one coherent all-degree construction, agrees with the two specified groups of the workshop-associated strong-homotopy program, and realizes every homotopy group in that construction by a single explicit functor. Whether this convention-qualified construction counts as a complete response to the original open-ended request is reserved for independent source review. It must not be represented as the previously unproved equality of two unspecified group definitions.

No theorem here identifies these groups with graph A-groups. For example the reflexive four-cycle has clique realization S¹, hence D₁=Z. For box-product homotopy its identity contracts by the two time steps with vertex lists (0,1,2,3), (0,0,3,3), (0,0,0,0); each time slice preserves cycle adjacency and each vertex moves at most one edge, but a cross-time diagonal required by strong homotopy fails. Thus the A-theory/box-group realization is genuinely different. The cubical nerve theorem addresses its own model.

Nor does the theorem identify arbitrary digital homology theories with singular homology. Clique simplicial homology does agree with the singular homology of F by the classical simplicial comparison, but that observation does not replace checking a specified digital chain model. The June 2026 closure-space theorem's conjectural digital comparison is accurately retained as a statement about its published scope, even though the explicitly defined D_n model now has the comparison above via the common clique realization.

The finite checks exercise clique/strong-contiguity equivalence, the caterpillar's cross edges, the invalid one-step shortcut, finite-support restriction and product placement. They are diagnostics of the written proof. No finite count proves an all-n comparison or an infinite homotopy-group computation.
