# Eight mutually edge-adjacent planar faces: a credited literal resolution

**Target:** UnsolvedMath 7200087 / AMR-071-0087, queue rank 451.  
**Checked:** 3 October 2026.  
**Disposition:** the catalog's literal at-least-one-edge question has an affirmative answer in prior literature. This is a source-derived certificate, not a new construction or an original discovery. Mathematical attempt budget used: **0/5**.

## 1. Exact scope

The statement preserved in the pinned catalog asks for an embedded, nonconvex polyhedron in three-dimensional Euclidean space with more than seven planar faces such that every two faces share an edge. It does not say that the shared edge is unique.

Here a face is the closed disk bounded by a simple planar polygon. The union must be a connected, embedded, closed two-manifold; it must have no accidental intersections. Intersections of distinct faces may consist of more than one common edge. This is the acoptic convention allowing overarching faces, discussed by Grünbaum and Szilassi [4, introduction]. Each individual face nevertheless has one connected, simple boundary, with no holes, disconnected pieces, self-crossings, or repeated vertices.

**This convention matters.** The example below does not satisfy a stronger requirement that two faces meet in exactly one common edge. Eight pairs meet in two disjoint collinear edges. The stricter question is not resolved here. The live Wikipedia list now expressly asks for exactly one edge; that is stronger than the pinned catalog's statement. See `SOURCE_AUDIT.md`.

## 2. Credited answer

Ruslan Mizhaev's eight-face construction appeared in 2020 [1]. His 2026 preprint [2] supplies an integer-coordinate realization. Röst and Vígh subsequently gave a different eight-face realization [3]. The preprints are cited as preprints; no journal acceptance or priority beyond the inspected evidence is claimed.

The integer data in [2] yield the following witness, independently checked by the accompanying code:

- 24 distinct vertices, 36 edges, and eight faces;
- each face is a simple planar nonagon and bounds a disk;
- each vertex has a triangular link and degree three;
- each edge belongs to exactly two faces, with compatible orientations;
- every pair of faces meets precisely in its prescribed common edge or edges;
- 20 face-pairs share one edge; the other eight pairs share two;
- the surface is connected, closed, orientable, embedded, and of genus three.

In particular, eight is greater than seven, and the surface is nonconvex. This proves the literal existence claim.

## 3. Reproducible exact certificate

Run, with ordinary Python 3 and assertions enabled:

```sh
python3 verify_witness.py > verification-fresh.json
```

No third-party package, random seed, floating-point arithmetic, numerical tolerance, network connection, or source-paper software is needed. The file contains the integer coordinates, face boundary cycles, and plane equations from [2, Tables 1–2 and Section 4], with full attribution. `VERIFICATION.json` records the executed result, including all 28 pair-intersection certificates.

For clarity, the supporting planes are

\[
\begin{array}{rlrl}
F_1:&21x+3y-10z=-1440,&F_2:&21x+3y+10z=1440,\\
F_3:&3x+z=234,&F_4:&3x-z=-234,\\
F_5:&3y-z=234,&F_6:&3y+z=-234,\\
F_7:&3x-21y+10z=-1440,&F_8:&3x-21y-10z=1440.
\end{array}
\]

The plane equations alone are not the polyhedron: the closed polygonal regions specified by the boundary cycles are essential.

### Why the finite checks prove the geometric assertion

1. **Faces are embedded disks.** Substitution proves coplanarity of every face vertex. Dropping a coordinate with nonzero plane-normal component gives an injective affine planar projection. In that projection, the code rejects collinear consecutive edges, checks all nonadjacent edge pairs for intersection, and verifies nonzero signed area. Thus each polygon is simple. The planar Jordan theorem identifies its bounded region as a disk. Mixed turning signs give nonconvex faces; the computed reflex-corner counts are `(2,2,3,3,3,3,2,2)`.

2. **The gluing is a closed surface.** The edge list has 36 distinct unordered vertex pairs, each appearing twice. Reorienting faces by `(+,+,-,-,-,-,+,+)` makes the two occurrences of every edge have opposite directions. At each of the 24 vertices, the predecessor/successor data give a connected triangular link. Therefore the abstract gluing is a closed orientable two-manifold, rather than a surface with a boundary or pinched vertices. Its edge graph is connected.

3. **The gluing is actually embedded in three-space.** All face planes are pairwise nonparallel. For every pair, the code computes their intersection line rationally and takes one nonconstant coordinate as its parameter. It lists every parameter where the line crosses a polygon edge or contains an edge endpoint. Between consecutive parameters membership in the closed polygon is constant, unless the interval is itself boundary; an exact boundary-inclusive point-in-polygon test handles both cases. Isolated contacts are tested separately. Compactness excludes points beyond the extreme breakpoints. Consequently these finite tests compute the entire closed intersection of each polygon with the line, not a sample-based approximation. Intersecting the two resulting interval unions gives the entire face-pair intersection. In each of the 28 cases this equals exactly the union of their common edges, with no extra isolated contacts. Face simplicity and these pairwise checks show the gluing map is injective. A continuous injection from the compact abstract surface into Euclidean space is a homeomorphism onto its image.

4. **Topology and adjacency.** The Euler characteristic is
   \[
   \chi=24-36+8=-4=2-2g,
   \]
   giving genus `g=3`. An embedded compact orientable surface separates space and is the boundary of its bounded side. A convex body's boundary is a sphere, so this surface cannot be convex. Every off-diagonal entry of the independently counted face-adjacency matrix is positive.

The twice-adjacent pairs are

\[
(1,4),(1,5),(2,3),(2,6),(3,7),(4,8),(5,7),(6,8).
\]

They form the cycle `1–4–8–6–2–3–7–5–1`. The verifier additionally checks that the two common edges in each such pair are disjoint. This is not achieved by treating a bent face as flat, merging disconnected polygons, or replacing a geometric surface with an abstract map.

## 4. What this does not prove

- It gives neither a bound on all possible numbers of faces nor a classification.
- It does not resolve the exactly-one-edge-per-pair variant or impose non-overarching faces.
- It does not construct a 12-face non-overarching realization.
- It makes no claim about the optimal coordinates, genus, volume, or symmetry group.
- It does not infer geometric realizability from combinatorial duality.

The often-quoted relation

\[
g=\frac{(f-3)(f-4)}{12}
\]

requires both exactly one edge per face-pair and three incident faces at every vertex: then `E=f(f-1)/2`, `3V=2E`, and Euler's formula gives the relation. In that restricted class the next integral case after `f=7` is `f=12`. It cannot be used to exclude the eight-face witness, where `E=36`, not `28`. Nor should the trivalence hypothesis be silently dropped when discussing the stronger question.

## 5. Corrections to the imported summary

For a convex three-dimensional polyhedron, pairwise adjacency of all faces would make the planar dual graph complete. Since a planar complete graph has at most four vertices, four is the maximum, attained by a tetrahedron. The imported claim that the convex maximum is seven is false.

Császár's torus has seven vertices joined pairwise, 21 edges, and 14 triangular faces. It is vertex-neighborly. Szilassi's torus has 14 vertices, 21 edges, and seven hexagonal faces; it is face-neighborly and combinatorially dual to Császár's. Neither is convex. A combinatorial dual is not automatically a straight-faced embedded geometric dual.

## References

1. R. Mizhaev, *Equivelar octahedron of genus 3 in 3-space*, OSF Preprints, April 2020, Section 3 (variant V2), pp. 5–7. DOI: [10.31219/osf.io/hvtey](https://doi.org/10.31219/osf.io/hvtey). Original public file and OSF dates inspected; the supplied 2026 integer realization is the one independently certified here.
2. R. Mizhaev, *Integer Realization of an Equivelar Octahedron of Genus 3*, [arXiv:2609.17700v1](https://arxiv.org/html/2609.17700v1), 15 September 2026, Sections 3–5, Tables 1–2. Source of the witness data.
3. G. Röst and V. Vígh, *A second eight-faced polyhedron in which every two faces share an edge*, [arXiv:2609.32998v1](https://arxiv.org/html/2609.32998v1), 26 September 2026, Theorem 1 and Sections 3–5. Corroborating literature and a distinct realization; its coordinates were not independently rerun here.
4. B. Grünbaum and L. Szilassi, *Geometric realizations of special toroidal complexes*, Contributions to Discrete Mathematics **4**(1) (2009), 21–39. [Publisher](https://cdm.ucalgary.ca/article/view/61986); [author-hosted text](https://faculty.washington.edu/moishe/branko/BG277%20Toroidal%20complexes.pdf). The introduction distinguishes acoptic from non-overarching faces.
5. E. Arseneva et al., *Adjacency Graphs of Polyhedral Surfaces*, Discrete & Computational Geometry **71** (2024), 1429–1455. [DOI:10.1007/s00454-023-00537-6](https://link.springer.com/article/10.1007/s00454-023-00537-6). Its Section 1 model permits only a single common corner or side, which excludes the doubled-edge witness.
