# Independent review: additive-coloring barriers for the associahedron

**Verdict: PASS_SCOPED_ADDITIVE_OBSTRUCTION.** The fixed-weight characterization, sharp finite ambient-group order bound, and lower bound for the number of realized additive colors are correct. No mandatory correction is requested. They do not settle the original unbounded-chromatic-number conjecture. Retain **unsolved, 2/5**.

This separate adversarial AI review was completed on 2026-09-30 (gpt-6-astra, xhigh). It is not human peer review or a novelty certification.

## Frozen snapshot and checks

- `PARTIAL_RESULT.md`: `d6fc2ab0166a3ff301fbe965d54c275c92a666947b8fa5940f45edd2fe84c6ae`
- Submitted `verify.py`: `991e01eef0c666f9b76b140967e0b531bb78f6fff9d5c42f9b946f0ceedac3f7`
- Submitted receipt: `58643bc5df02e57697bd8c558d980e8db37bb4e1d0711ea5e87c3d3af59a700b`

All **186,463 submitted assertions** reproduced byte-identically, including 2,055 triangulations and 6,733 flip edges. A separately written standard-library verifier passed **19,866 exact assertions**. It constructs explicit completions for 4,368 crossing pairs, enumerates triangulations by maximal noncrossing sets through n=8 rather than using the submitted recursion, and tests small cyclic and noncyclic group assignments. No author files were edited.

## 1. Original graph and source conventions

The [Open Problem Garden page](https://www.openproblemgarden.org/op/chromatic_number_of_associahedron) concerns the chromatic number of the **1-skeleton**, equivalently the flip graph of triangulations of a convex polygon. Its n is the number of polygon vertices; the polytope's dimension is n−3. The candidate uses this convention consistently. A vertex of this graph is a whole triangulation, not a polygon vertex or a diagonal.

I checked [Fabila-Monroy et al., Theorem 4.1](https://dmtcs.episciences.org/460), including its additive construction. The candidate properly credits the known ceil(n/2) upper-bound method. I also checked the introductory statements of the logarithmic-bound paper and [Cioabă–Gupta's spectral paper](https://arxiv.org/abs/2210.08516). Their bounds concern arbitrary colorings; the spectral discussion does not provide an unbounded lower bound.

A current bibliographic update is available without changing the frozen proof: the logarithmic-bound paper is now published in **Journal of Computational Geometry 17(1), 61–74 (2026)**, on 28 May 2026, DOI10.20382/jocg.v17i1a3. I retrieved the [full version-of-record PDF](https://jocg.org/index.php/jocg/article/download/5192/4169/19798) and checked its introduction and Theorem 1. It keeps the same n-gon convention, logarithmic upper bound, and absence of a known nonconstant lower bound in its introduction. This review does not claim to independently reprove that paper's entire coloring construction.

## 2. Exact characterization of additive schemes

For any two crossing internal diagonals, their four distinct endpoints bound a convex quadrilateral. Its sides are either polygon sides or mutually noncrossing internal diagonals. The complementary regions can each be triangulated independently. Filling the central quadrilateral with either diagonal therefore produces two genuine polygon triangulations differing by exactly one flip.

The difference of their group-valued sums is the new diagonal's weight minus the old diagonal's weight. Thus every crossing pair must have distinct weights. Conversely, in any flip all common diagonal contributions cancel, so distinct weights for crossing pairs imply a proper coloring. Abelian group structure makes the sums independent of ordering and supplies cancellation. No assumption that the group is finite is needed for this equivalence.

Boundary edges, if included, contribute the same constant to every triangulation. They change neither properness nor the number of realized colors. The auxiliary crossing graph is used only to characterize permitted weight assignments; it is not identified with the associahedron graph.

## 3. Sharp bound on the finite ambient group

A single weight class contains no crossing pair. Every noncrossing set of internal diagonals of a convex n-gon has at most n−3 members: it can be extended to a triangulation, or the bound follows from maximal outerplanarity after adding the boundary. There are n(n−3)/2 diagonals. For n≥4, dividing by the positive number n−3 forces at least ceil(n/2) distinct weight values and therefore at least that many elements in a finite group G.

This counts weights, not triangulation sums. The proof does not silently substitute |G| for the cardinality of the actual image C.

The proposed cyclic-group construction attains the ambient order. For crossing ac and bd with a<b<c<d, the endpoint sums differ by `(b−a)+(d−c)`. It is at least two. The two remaining cyclic gaps are positive, so it is at most n−2. Consequently the sums are neither equal nor adjacent modulo n. Every fiber of `r↦floor(r/2)` on the residue representatives consists of an adjacent pair, except for the last singleton when n is odd. Crossing diagonals therefore receive different labels. These labels lie between zero and ceil(n/2)−1, so reduction in Z/ceil(n/2) creates no extra identification between them. The characterization proves properness.

This proves sharpness of the **group-order** requirement. It does not assert sharpness of the separate bound on the number of actually used colors.

## 4. Actual color image and the difference-set estimate

Let m=floor(n/2). For i<j<m the diagonals `(i,i+m)` and `(j,j+m)` have strictly interleaved endpoints, so the indicated m diagonals are pairwise crossing. They are internal for n≥4. When n is odd, the final unused vertex causes no change to this interleaving.

Their weights are distinct by the proved characterization. Fixing the first diagonal, every weight difference with another member is realized by the explicit one-flip completion, possibly in a different pair of triangulations for each difference. A common surrounding triangulation for all pairs is neither claimed nor needed. Each difference belongs to C−C, and subtracting a fixed group element preserves distinctness. Including zero gives m distinct elements of C−C.

If C has k elements, zero accounts for one possible difference and ordered unequal pairs give at most k(k−1) others. Torsion or coincident differences only lowers this cardinality, so the argument applies to any abelian group, including infinite groups. Thus

`floor(n/2) ≤ |C−C| ≤ k(k−1)+1`.

The stated ceiling of the positive quadratic root is correct. C is finite because the polygon has only finitely many triangulations, regardless of the ambient group's size.

The crossing family is a clique in the **diagonal crossing graph**, not a clique in the flip graph. The difference-set argument is needed to pass from its weights to realized triangulation colors. It does not furnish an unrestricted chromatic lower bound.

## 5. Remaining gap and reproduction

General graph colorings need not be sums of fixed diagonal weights. Nonlinear recoloring of one or several statistics, or weights depending on the surrounding triangulation, is outside the theorem. A reduction preserving the color count is neither proved nor assumed. In particular, the known O(log n) general upper bound is compatible with the additive image lower bound; extending the latter to all colorings would contradict that upper bound for sufficiently large n.

From this review directory, reproduce the checks with:

```sh
python independent_checks.py
(cd author_replay && python verify.py)
```

Both scripts use only the standard library. The submitted script is working-directory-sensitive and should be run as shown. The independent finite group tests and flip enumerations support the elementary all-n proof; they are not an exact-chromatic-number computation.

The original conjecture remains **unsolved, 2/5**. Preserve the restricted fixed-additive scope and the absence of a novelty claim. No mandatory mathematical correction remains. The newly located journal citation may be added to source metadata without changing the frozen proof.
