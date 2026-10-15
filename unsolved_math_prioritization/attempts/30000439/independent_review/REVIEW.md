# Independent review of the PL and linear embedding dimension gap

**Verdict: PASS.** The candidate proves that a finite two-dimensional simplicial complex has PL embedding dimension exactly 3 and linear embedding dimension exactly 5. This answers the existential question in the cited source. No mandatory mathematical revision was found. Historical priority is not established, and this independent AI review is neither human peer review nor a formal proof certificate.

Review date: 2026-09-30. Reviewer model and effort: gpt-6-astra, xhigh.

Reviewed `CANDIDATE.md` SHA-256: `23705f2868d66526eeded2cf644d36138acd8223af13d5202ee22da415753502`.

The reviewer did not develop the candidate and made no edits to it. The preceding snapshot differed only in the citation locator for Janson's inequality. The final frozen snapshot was independently checked against the original question and the imported theorems.

## Exact scope

The claim concerns the minimum ambient dimensions for embeddings of a finite abstract simplicial complex. The linear embedding must be affine on its original simplices; the PL embedding may use a subdivision. These are the notions used by the original source.

I read the complete Brehm contribution on pp. 701–702 of Oberwolfach Report 12/2006 and visually inspected p. 702. The question is existential for simplicial complexes and expressly highlights dimension two. It does not require a manifold or a small explicit triangulation. Thus a positive-probability construction of the stated finite complex supplies the required existence claim. [Original report](https://ems.press/content/serial-article-files/46044)

## Imported ingredients

The relevant source statements match the candidate:

- Newman's Theorem 9 and Corollary 10 give the required balanced Radon pair among seven points in four-dimensional space and the resulting six-vertex witness count
- Newman's Theorem 11 and Lemma 12 give at most (n^{20n}) labeled generic order types for this dimension; determinant signs determine each Radon partition
- Lee–Nevo Lemma 3.1 covers every finite linear 4-uniform hypergraph and embeds its generated simplicial complex PL in three-dimensional space; the definition uses pairwise hyperedge intersections of size at most one
- Frieze–Karoński Theorem 34.13, equation (34.36), gives the lower-tail estimate with the diagonal term included in the overlap denominator

I inspected the relevant typeset pages, and independently checked the published Lee–Nevo statement. The withdrawn odd-dimensional threshold claim in an earlier Newman version is not used. [Newman](https://arxiv.org/pdf/2212.09576), [Lee–Nevo preprint](https://arxiv.org/pdf/2307.14195), [published Lee–Nevo](https://link.springer.com/article/10.1007/s00454-026-00856-4), [Frieze–Karoński](https://www.math.cmu.edu/~af1p/BOOK.pdf)

## Combinatorial and probabilistic audit

**Witness count.** Every seven-set supplies at least one unordered intersecting pair of disjoint triangles. Any particular pair uses six labels and occurs in exactly (n-6) seven-sets. This proves the factor (\binom n6/7) without assuming uniqueness of the pair within a seven-set. Removing a set of (m) triangle labels destroys at most (mM) witness pairs, where (M=\binom n3). Multiple counting of destroyed pairs only makes this upper bound weaker. The constant (c=1/645120) and the condition (n^{7/4}\ge107520) in the displayed survivor estimate are correct.

**Bernoulli variables.** Each entire triangle is sampled independently. The two-triangle witness indicators share a random variable precisely when their witness pairs share an identical triangle. Sharing vertices or edges between different triangles creates no probabilistic dependence. Two distinct witness pairs cannot share both triangles. An ordered dependent pair is specified by its common triangle and its two ordered other triangles, so at most (M^3) such pairs occur, each with expectation (p^3). The diagonal contribution is (\mu), rather than another (p^3) term.

**Janson exponent.** For (p=n^{-3/2}), the survivor estimate gives (\mu\ge cn^3). The upper bound on (\mu+\Delta) is (n^3/72+n^{9/2}/216\le n^{9/2}). Inserting the lower bound for the numerator and upper bound for the denominator therefore gives the claimed uniform failure estimate

\[
\mathbb P(Z_{\pi,F}=0)\le\exp(-c^2 n^{3/2}/2).
\]

The use of ordered distinct pairs for (\Delta), with the diagonal added separately, is a valid conservative convention. There is no missing factor that affects the stated constant.

**Adaptive deletions.** The union bound ranges over every ambient triangle set (F) with at most (m=n^{5/4}) elements, not just a fixed deletion rule. It also ranges over all relevant generic order types. Its logarithmic prefactor is at most

\[
\log(m+1)+(20n+3m)\log n.
\]

This is (o(n^{3/2})), so the bound tends to zero. In particular the event obtained holds for the cleaning set selected after inspecting the random family. No independence between that cleaning set and the sample is assumed. A representative per order type suffices because the entire witness graph, including the deletion operation, is determined by the Radon partitions.

**Cleaning.** The count (\binom n2\binom{n-2}2) counts each unordered pair of distinct triangles sharing an edge exactly once. Its expectation after sampling is at most (n/4). Choosing one triangle from each offending pair and deleting their union uses at most one deletion per pair and hits all offending pairs. A surviving pair of triangles therefore intersects in at most a vertex. The robust event just proved still forbids a linear embedding in four dimensions after this operation.

**Nonplanarity.** The triangle count is binomial with mean (\lambda=Mp) and variance at most (\lambda). The Chebyshev estimate is valid, and the chosen parameters ensure (\lambda/2-m>n). Each retained triangle contributes three different edges because no two share an edge. The resulting simple graph has more than (3n) edges and at most (n) vertices, violating the planar graph bound. Hence a PL embedding of the complex in the plane is impossible. The simultaneous-event argument uses only a union bound, not independence of these events.

## Geometric audit

**Nongeneric embeddings.** The perturbation argument is correct. Images of disjoint nonempty faces under an embedding are disjoint compact sets; the minimum of their distances over finitely many pairs is positive. Moving every vertex sufficiently little preserves these disjointness conditions. If affine images of two points of the complex coincided, subtracting their barycentric coordinate vectors and cancelling their common coefficients would produce intersecting convex hulls of disjoint faces unless the points were identical. Thus the preserved conditions ensure both nondegenerate simplices and global injectivity. Generic configurations are dense, so a nongeneric linear embedding could be replaced by a generic one.

If some of the (n) labels disappear from the complex when triangles are deleted, their positions can be added arbitrarily in general position. Thus counting placements of all (n) labels still covers every embedding of the retained subcomplex. This is an immediate completion of the labeling convention, not an additional hypothesis.

**PL upper bound.** Giving every retained triangle a different new private vertex creates a linear 4-uniform hypergraph: two augmented edges have exactly the same intersection as their original triangles. Lee–Nevo therefore supplies a PL embedding of its generated tetrahedral complex in three dimensions. The original triangle complex is a subcomplex, and restricting a subdivision-based embedding to a subcomplex gives a PL embedding. No linear embedding of the original triangulation is inferred from this step.

**Exact minimum dimensions.** The preceding nonplanarity gives (e_{\rm PL}\ge3), while inflation gives the opposite inequality. Robust nonembedding in four dimensions gives (e_{\rm lin}\ge5). For the upper bound, points on the five-dimensional moment curve make any six vertices affinely independent. The union of two triangles has at most six vertices, so their convex hulls meet exactly in their common face. This embeds every finite two-dimensional complex linearly in five dimensions. Both claimed dimensions are therefore exact.

## Explicit finite parameters and computation

All 16 assertions in the submitted standard-library checker passed on replay, with outputs confined to the review directory. I also checked the log inequalities analytically: (\log n<256), (\log(m+1)\le2m), and the resulting entropy estimate is below (2^{331}), whereas the stated Janson exponent exceeds (2^{343}). The three failure bounds sum to less than one for (n=2^{256}), so the proof does not rely solely on an unspecified asymptotic threshold.

A separate checker imports no candidate code. Using the exact surviving-pair lower bound and a separate overlap upper bound, it verifies a stronger rational upper bound on the combined failure probability, using (e^{-x}\le1/(1+x)) after subtracting the entropy bound. It also verifies finite eight-vertex witness/dependency counts. All **396 exact assertions passed**. Files: `check_results.json`, `independent_checks.py`, and `independent_checks.json`.

Neither checker constructs the enormous complex or certifies the imported theorems. The existence result is the mathematical probabilistic argument, supplemented by exact arithmetic checks.

## Novelty and publication boundary

The source's older fixed-ambient-dimension examples do not themselves supply the asserted gap of two. The inspected Newman separation likewise compares PL and linear embeddings in the same even ambient dimension. The uniform deletion step and the inflation step are both necessary to the present proof.

A bounded independent search for the exact gap, low-dimensional PL-versus-linear dimensions, and the Newman/Lee–Nevo combination did not locate an earlier statement of this precise construction. This is not proof of historical novelty or priority. The appropriate public description is a **complete candidate proof that passed independent AI review, with priority unconfirmed**. No assertion about manifolds, small vertex sets, or formal certification should be added.

No mathematical corrections are required for the reviewed snapshot. Administrative review-status updates may refer to this verdict; any change to the mathematical argument should be separately hashed and rechecked.
