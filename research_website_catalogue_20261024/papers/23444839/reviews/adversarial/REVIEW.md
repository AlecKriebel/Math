# Independent adversarial review — Zenodo 23444839

**Verdict: PASS for the exact stated theorem.** I found no substantive mathematical defect in the construction, its vertex-deletion Cohen–Macaulay argument, or its exclusion of homology-sphere subcomplexes under the stated local-link definition. The exact imported building interfaces were checked against primary sources. This is an AI review, not external human peer review, a formal proof certificate, a priority certificate, or permission to publish.

## Object, scope and independence

The reviewed paper is *A negative answer to Nevo's homology-sphere decomposition question*, v1.0.0, 17 October 2026, Zenodo 23444839. The entire five-page PDF and complete `main.tex` were read. PDF SHA256: `0f3bd7b0b576188794376e5a6428f7049bd19a1e778b68ad5c63b696a73c3a01`. ZIP SHA256: `7919adebe0119f34df35e905ebe3665b1d66e79477fa36a06c30801bbe736a5b`. The 120-member support archive contains a byte-identical embedded main PDF and no other reader PDF.

The exact claim is the existence of a finite pure two-dimensional abstract simplicial complex \(K\), doubly Cohen–Macaulay over **every characteristic-zero field**, with **no two-dimensional homology-sphere subcomplex over any field**. The field \(\mathbb F_{11}\) constructs the geometry; it is not the homology coefficient field. The paper does not establish 2-CM in every positive characteristic. Nor does it claim that \(K\) is a manifold, a topological sphere, a PL sphere, or a complex without nontrivial top-dimensional cycles.

Fresh controls were written and run before reading packaged mathematical helpers. They use an affine-chart projective-plane construction and a nine-vertex periodic-grid torus, materially different from the supplied normalized-vector incidence construction and seven-vertex torus. A second fresh script directly multiplies elements of the cyclic algebra over \(\mathbb F_{11}(t)\), rather than importing the supplied matrix formula. Current finite/matrix helpers and their runner were subsequently read and replayed in an isolated copy. No historical review report, verdict body, sibling assessment or priority-audit body was read. Their filenames appeared in the inventory; prior-review and literature-search assertions in the required manuscript/verification instructions were incidental and not evidence.

The imported standard lattice/building results remain mathematical dependencies: neither this review nor the programs enumerate the complete finite quotient or independently reconstruct all building theory. The proof interfaces, not just citation titles, were inspected. All source bytes are unchanged and bound in `evidence-bindings.json`.

## Original question and the meaning of a sphere piece

I checked Nevo's original Oberwolfach Theorem 7/Problem 8 and the published Definition 3.1, Theorem 3.4 and Problem 3.7, also cross-checking the arXiv edition. The question concerns replacing the minimal cycle **subcomplexes in a union decomposition of the given complex** by homology spheres, with overlap and reordering properties. It is not a question about mapped-in spheres, subdivisions, changes of ambient complex, or a numerical decomposition of an invariant. The two-dimensional case is within the stated \(d\ge1\) range, and a counterexample over \(\mathbb Q\) suffices. [Nevo, published article](https://link.springer.com/content/pdf/10.1007/s00454-007-9017-y.pdf)

The paper explicitly uses the standard local-link homology-sphere condition: each face link has the homology of the sphere of its expected dimension, including the empty face. Swartz's Section 4 states that same convention and identifies these as Gorenstein* complexes. It is stronger than merely having the global homology of a sphere. The paper's obstruction uses this local condition and does not claim to exclude the weaker global-only object. [Swartz, inspected version](https://arxiv.org/pdf/math/0512086v1)

The definition forces the necessary local purity. An edge in a two-dimensional homology sphere has a zero-dimensional link with reduced \(H_0\) of dimension one, so it is incident to exactly two triangles. A vertex link is a connected graph whose vertices all have degree two, hence a simple cycle. These deductions hold over any field and require no surface classification or orientability assumption. Thus the target convention matches the mechanism actually proved.

## Construction and the critical finite-quotient interface

The affine building of \(\mathrm{PGL}_3(\mathbb F_{11}((y)))\) has vertices given by homothety classes of rank-three lattices. Its vertex links are the order complexes of the nonzero proper subspaces of \(\mathbb F_{11}^3\), namely the incidence graph \(G\) of \(\mathrm{PG}(2,11)\).

The essential imported data from Lubotzky–Samuels–Vishne were checked in Sections 2–4, not inferred from later Ramanujan claims:

- The cyclic algebra has dimension nine, center \(\mathbb F_{11}(y)\), relations \(za=a^{11}z\), \(z^3=1+y\), and splits over the local field. Conjugation embeds the projective group faithfully into a nine-dimensional linear group.
- Equation (9) gives entries of degree at most one in \(t=1/y\) for the generators \(b_u\). Definition 4.7 and Proposition 4.8 place the generated group in \(\mathrm{GL}_9(\mathbb F_{11}[t])\), including inverses. The source explicitly distinguishes this matrix definition over \(R_0=\mathbb F_q[1/y]\) from defining the original cyclic algebra over that ring.
- Corollary 4.6 covers lattice indices \(11\) and \(11^2\) by positive words of lengths one and two, respectively. Proposition 4.8 gives simple transitivity on building vertices. Thus an undirected edge step is covered; the argument has not silently bounded only one oriented neighbor type.

These are precisely the interfaces used by the paper. [LSV, inspected v2](https://arxiv.org/pdf/math/0406217v2)

Reduction of the faithful polynomial representation modulo \(t^9\) is a genuine group homomorphism to a finite general linear group, because inverses are polynomial too. Its kernel \(\Gamma_9\) is therefore normal and finite index. If an element moves the base vertex distance at most four, simple transitivity turns the path into a product of at most eight positive generators. Its representing matrix has degree at most eight. Membership in \(\Gamma_9\) makes every entry of the difference from the identity divisible by \(t^9\), forcing the difference to vanish. Faithfulness then forces the element to be trivial. Normality and vertex transitivity transfer this bound to every vertex.

This proof works for the nonreduced ring \(\mathbb F_{11}[t]/(t^9)\). It does **not** invoke Lubotzky–Meshulam Proposition 3.3 as a theorem about this particular quotient: their statement uses an irreducible modulus prime to the specified factors. I read that proposition and its full degree-versus-divisibility proof in the available ten-page author version. It is a correct antecedent for the method, while the manuscript supplies its own argument for the actual modulus. [Lubotzky–Meshulam, author version](https://ma.huji.ac.il/~alexlub/PAPERS/a%20Moore%20Bound%20for%20simplicial%20complexes/a%20Moore%20Bound%20for%20simplicial%20complexes.pdf)

The quotient is defined as an abstract complex with exactly the images of building faces; no clique completion is added. Two vertices of one face, or two neighbors of a fixed vertex, cannot be identified, since their distance is at most two. Conversely a quotient triangle incident to \([x]\) can be translated to a triangle incident to \(x\); its other vertices are uniquely determined by their neighbor orbits. This proves link isomorphism on both vertices and edges, not just equality of link vertex counts. The quotient is finite because the action is vertex-regular and the kernel has finite index, connected because the building is connected, and pure of dimension two because building triangles survive. No facet is collapsed or a link edge introduced by a quotient identification.

## Spectrum after deletion and the 2-CM proof

The graph \(G\) has 133 points, 133 lines and degree twelve. Incidence gives \(MM^{\mathsf T}=11I+J\), so its adjacency eigenvalues are \(\pm12\) and \(\pm\sqrt{11}\); the ordinary Laplacian gap is \(12-\sqrt{11}\). Bipartiteness and unique common lines exclude cycles shorter than six.

Deleting one vertex \(w\) leaves degrees eleven or twelve. Extend an unweighted-mean-zero function on \(G-w\) by zero at \(w\). The extension is mean zero on \(G\), and removed edge energies sum to at most its squared Euclidean norm. Therefore the deleted graph has ordinary energy at least \((11-\sqrt{11})\|x\|^2\). This already proves its connectivity: a nonzero mean-zero function constant on disconnected components would have zero energy. To pass to the **normalized** gap, the degree-weighted variance is bounded above by \(12\|x\|^2\), using the unweighted mean as a permissible center. The direction of this denominator inequality is correct and yields

\[
\lambda(G-w)\ge(11-\sqrt{11})/12>7/12>1/2.
\]

The paper does not confuse ordinary and weighted means on this irregular deleted graph. It also uses a strict threshold, not \(\ge1/2\).

I reconstructed the finite weighted-cocycle proof independently. Purity makes all edge weights \(m(e)\), the number of incident triangles, positive. In a real cohomology class choose the representative minimizing \(\sum m(e)a_e^2\). Variation by a vertex coboundary gives weighted mean zero for the local link function \(u\mapsto a_{vu}\). The triangle cocycle equation identifies local differences with the opposite edge value. Summing the link Poincaré inequalities counts each edge exactly \(m(e)\) times on the energy side and twice with weight \(m(e)\) on the norm side. Thus \(E\ge2\lambda E\), and strict \(\lambda>1/2\) forces \(E=0\). This is a complete argument in the finite setting; the general Garland-type source is attribution rather than an unproved substitute. [Ballmann–Świątkowski, primary preprint](https://archive.mpim-bonn.mpg.de/id/eprint/2255/1/preprint_1996_127.pdf)

For every vertex deletion \(K-z\), a surviving edge loses at most one of its twelve triangles and remains in at least eleven. Every surviving vertex retains at least 265 neighbors, hence lies in a surviving triangle. Thus the deletion remains nonempty and pure of dimension two. A path through \(z\) can be rerouted through its connected link using edges that survive the deletion, establishing global connectivity. A surviving vertex link is exactly \(G\) or \(G-w\); the spectral lemma applies.

Consequently \(H^1\), and by finite-dimensional duality \(H_1\), vanish over \(\mathbb R\) for \(K\) and every deletion. Integer boundary matrices have the same ranks over all characteristic-zero fields, so this vanishing transfers to all those fields without any asserted transfer to arbitrary positive characteristic.

Every face condition is accounted for: at the empty face, connectedness and \(H_1=0\); at a vertex, a nonempty connected one-dimensional link; at an edge, a nonempty zero-dimensional link; and at a facet, the dimension-minus-one empty-face complex with no required lower homology. These establish CM and same-dimensional CM after **every** vertex deletion. Link spectral information alone would not have supplied global connectivity or purity, but both are separately proved.

## Sphere obstruction

If a local-link two-dimensional homology sphere \(S\) were a subcomplex, every edge would have exactly two incident triangles, and every vertex link would be a simple cycle contained as a subgraph of \(G\). It need not be an induced subgraph. Girth at least six gives each vertex degree at least six. Hence

\[
2f_1\ge6f_0,\qquad3f_2=2f_1,\qquad\chi(S)=f_0-f_1/3\le0.
\]

But sphere homology over any field gives Euler characteristic two. This contradiction is field-independent and does not use orientability, PL classification, simple connectivity, or a claim that \(K\) itself has sphere homology. It rules out even one permitted piece, so every proposed cover by such pieces fails before the extra overlap/reordering conditions arise. The corresponding curvature obstruction has a clear antecedent in Januszkiewicz–Świątkowski Example 1.8(5); the elementary count here is independently valid. [Published article](https://www.numdam.org/article/PMIHES_2006__104__1_0.pdf)

## Fresh controls, replay and diagnostic limitations

`fresh_controls.py` constructs \(\mathrm{PG}(2,11)\) using 121 affine points, slope/vertical lines and points at infinity. It checks all pair incidences, the exact Gram identity, all 266 single-vertex deletions, their degree sets, and the strict rational gap bound. Removing one incidence is detected. No floating eigenvalue establishes the bound.

The same fresh script constructs a nine-vertex, 27-edge, 18-triangle torus by triangulating a periodic 3-by-3 grid. Exact rational boundary ranks are eight and seventeen, giving Betti numbers \((1,2,1)\). All vertex links are \(C_6\), with normalized gap exactly one-half. A nonzero closed, weighted-coclosed edge cochain has global energy 36, summed local energy 36 and summed local norm 72. This is an actual countercontrol to weakening the strict spectral hypothesis, using a different torus and a harmonic cochain rather than only a coboundary.

`fresh_polynomial_representation.py` independently uses \(\mathbb F_{11}[\theta]/(\theta^3+\theta+4)\); absence of a base-field root certifies cubic irreducibility. It multiplies the cyclic algebra with \(z^3=(1+t)/t\), reconstructing \(b=1-z^{-1}\) and \(b^{-1}=1+t(1+z+z^2)\). Exact conjugation matrices have polynomial entries of degree one, polynomial inverse, and determinant one. Constant conjugation by \(u\in E^\times\) preserves the degree bound. An initial test used structural equality for a retained finite-field fraction `4/4` and different dense/sparse matrix representations; it was corrected to cross-multiplication and entrywise equality. This was a control implementation issue, not a mathematical counterexample, and is recorded in the log.

The unmodified default verifier ran in an isolated publication copy: both normal/optimized positive runs passed, and all six actual corrupted-incidence/triangle/weight cases failed as required. The optional NumPy local-matrix diagnostic passed in normal mode and correctly refused optimized execution. It checks 133 positive and 133 inverse generators, exact inverse products and local adjacency with 266 vertices, degree twelve and Gram \(11I+J\). Its floating deleted-link eigenvalues, approximately 0.7113, are diagnostic only; the rigorous lower bound is approximately 0.6403 and comes from the symbolic argument. The mathematical checks and opaque file authentication do not adopt the archived reviewers' opinions.

No program enumerated \(K\), computed its complete homology, or exhausted all its subcomplexes. The proof establishes those universal claims using the imported vertex-regular action and the derived local/global arguments. This distinction is retained in the verdict.

## Remaining limits and strongest supported conclusion

The strongest supported result is exactly Theorem 1: there exists a finite two-dimensional 2-CM complex over every characteristic-zero field, with no two-dimensional local-link homology-sphere subcomplex over any field, providing a negative answer to Nevo's stated decomposition question.

No substantive proof gap was found within that scope. The review relies on the checked classical building/lattice interfaces and standard algebraic facts; it does not independently reprove all of LSV, construct the full quotient computationally, or assert global-only sphere exclusion. No minimum vertex count, positive-characteristic 2-CM conclusion, subdivision statement or universal novelty claim is certified.

Nevo's exact question and the cited near-interfaces were checked. The full bodies of the historical Chari/Baclawski references were not independently audited here, and only the relevant introduction of Larson–Stapledon was checked for its nearby decomposition context. A bounded absence-of-prior-result assertion cannot establish firstness. All primary editions, hashes, read extents and access limits are recorded separately. This adversarial assignment is 100% complete.
