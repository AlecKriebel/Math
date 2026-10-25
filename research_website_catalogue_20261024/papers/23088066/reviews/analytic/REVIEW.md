# Analytic review — Zenodo 23088066, version 1.0

**Verdict: the exact existence theorem and first-subdivision claim are supported. No substantive mathematical gap was found.** There exists a finite two-dimensional simplicial complex `K` with minimum PL embedding dimension three and minimum original-simplex linear embedding dimension five; moreover, `sd K` admits a linear embedding in three dimensions. This is an existence theorem with a finite parameter choice, not a supplied explicit facet list. This review is not human peer review, formal proof certification, or a novelty guarantee.

## Identity, scope and independence

The reviewed publication is Alec Kriebel, *A two-dimensional complex with embedding-dimension gap two*, DOI [10.5281/zenodo.23088066](https://doi.org/10.5281/zenodo.23088066), version 1.0, dated 1 October 2026. The actual five-page PDF has SHA256 `5325fceeed4352f74b531a033e8474ca1fabeeff0a6b6ecb54337e17dadb4dd6`; its source ZIP has SHA256 `b1e4a1c22fc3eec24c9d8f479b48110ddf6d72052181995037de64b99d46791f`. Byte lengths, SHA256 and published MD5 checksums were independently verified.

I read the entire published PDF and TeX, the full PL subdivision and probability derivations, and all five supplied finite-check programs plus their runner. I inspected the displayed subdivision page as rendered, in addition to text/source. The primary source hash ledger was used to locate publications, not to transfer previous review verdicts. Current sibling reports and the other archived mathematical/priority/source reports were not read.

There is a disclosed limitation to blindness: `evidence/probability_derivation.md` embeds an old favorable audit, and `evidence/PL_SUBDIVISION_LEMMA.md` opens with a historical favorable-check statement. These statements were encountered while reading their mathematical derivations and disclosed to the parent before the verdict. They were not mathematical evidence. Historical finite-check code was read and replayed as published computational support; historical review prose outside the two identified derivations was not consulted. Fresh controls import no supplied program, but were written after reading the supplied sources, so no blind-implementation claim is made.

## Exact definitions and target

`e_PL(K)` permits a PL embedding of the polyhedron, equivalently an embedding affine on simplices of a suitable finite subdivision. `e_lin(K)` requires the map to be affine on each **original** simplex. The positions assigned to vertices of the abstract barycentric subdivision need not be arithmetic barycenters of the images of the original vertices. Confusing those requirements would invalidate the geometric interpretation.

A triangle family is linear when distinct facets share at most one vertex; this is hypergraph terminology, distinct from linear embeddability. Its generated complex includes all faces. No manifold, connectedness or local manifold condition is imposed. The result supplies a finite two-dimensional complex, not a triangulated surface, and makes no smallest-witness or effective enumeration claim.

The exact minimum-dimension question in [Brehm's 2006 report, printed p. 702](https://ems.press/content/serial-article-files/46044) was checked directly. It asks about simplicial complexes generally and singles out dimensions two and three; it does not impose a manifold hypothesis. A gap of two with the stated minima therefore answers that question at its actual scope. This does not establish chronological priority over all subsequent literature.

## Reconstructed proof

### A. Linear embedding of the first barycentric subdivision

Place every original vertex and a separate node for each facet on the three-dimensional moment curve at distinct parameters. Four such nodes are affinely independent. Disjoint incidence-graph edges therefore cannot meet, and edges with a common endpoint meet only there. This gives a straight incidence graph even when it contains cycles.

For a facet node `f` and its three original vertices `v_i`, the vectors `a_i=v_i-f` form a basis. Place the abstract edge-subdivision vertex at `w_ij=f+epsilon(a_i+a_j)` with `0<epsilon<1/2`. Because an edge occurs in only one triangle, this assignment is globally well-defined. The six subdivided triangles become `conv(0,e_i,epsilon(e_i+e_j))` in that basis. Their coordinate-plane intersections give exactly their common subdivision faces, and all are nondegenerate. This explicitly embeds the subdivided disk within a single facet; it does not assume convexity of the entire original triangle image.

For separation of distinct facets, every point of `conv(f,v_i,w_ij)` is within `epsilon L` of the incidence segment `[f,v_i]`, where `L` is the largest incidence-edge length. Choose small disjoint balls about the original vertices avoiding nonincident graph edges and facet nodes. After smaller vertex balls are removed, distinct facet stars are disjoint compact sets with a positive minimum separation `delta`. Taking `epsilon L<min(r/2,delta/3)` excludes intersections outside the larger balls. The smaller-ball versus larger-ball distinction ensures that the nearby points on incidence stars really lie in the separated compact portions.

Inside a vertex ball, the proximity estimate excludes triangles associated with nonincident incidence edges. For a remaining triangle,

`x-v_i = alpha(f-v_i) + mu epsilon a_j`, with `alpha >= mu(1-epsilon)`.

Except at `v_i`, `alpha` is positive. After division by `alpha`, this lies in a ball of radius at most `epsilon L/(1-epsilon)` about `f-v_i`. Its direction is thus within angle `arcsin(epsilon L/((1-epsilon) ell))` of that facet ray, where `ell` is the smallest incidence-edge length. Distinct facet rays at a common vertex have a positive angular separation because three moment-curve nodes are not collinear. A sufficiently small common positive epsilon makes their cones disjoint away from the vertex. There are only finitely many distance and angle constraints. Absent pairs impose no condition.

These local and global checks establish an affine embedding of the whole first subdivision. Checking maximal triangles suffices for all subfaces by restriction. Isolated vertices can also be kept apart by the same distance construction. The argument does not require an acyclic incidence graph or successive arbitrary choices that might conflict around a cycle.

**Original theorem interface:** [Lee–Nevo v1, Lemma 3.1](https://arxiv.org/pdf/2307.14195v1) literally concerns `(d+1)`-uniform hypergraphs for `d>=3`. One should not substitute `d=2` into that statement. For triangle families, adding a different private vertex to each triangle produces a linear four-uniform hypergraph; a PL embedding in `R^3` restricts to the triangle subcomplex. That establishes the weaker PL consequence of their result. The stronger assertion about the **first** barycentric subdivision comes from the self-contained construction above, which was checked independently. No gap is left by this distinction.

### B. Enough forbidden triangle pairs in every placement

For seven generic points in `R^4`, the homogenized `5 by 7` matrix has a two-dimensional kernel. No nonzero kernel vector can have two zero coordinates: that would give dependence among five columns. Each coordinate functional on the kernel is nonzero for the same reason. On a half-circle in this kernel, coordinate zeros occur separately, and the number of positive coordinates changes in unit steps from `k` to `7-k`. Hence a transition between three and four positives occurs. At that point precisely one coefficient is zero and the remaining signs split three versus three. Since the first matrix row is all ones, normalizing the positive and negative coefficients gives equal convex combinations of two disjoint triples.

Thus every seven-set contributes a forbidden pair. Each such pair uses six labels and lies in exactly `n-6` seven-sets, giving

`|W_pi| >= C(n,7)/(n-6) = C(n,6)/7`.

This argument does not require uniqueness of a balanced witness in a seven-set. It agrees with the `d=4` specialization of [Newman v3, Theorem 9 and Corollary 10](https://arxiv.org/pdf/2212.09576v3), but the manuscript includes the needed proof directly.

A whole triangle has at most `M=C(n,3)` possible partners. Deleting any specified `F` of at most `m=n^(5/4)` triangles therefore removes at most `mM` witness pairs. For the printed threshold, the binomial estimate gives

`|W_pi(F)| >= c n^6`, `c=1/645120`.

The constants follow from `C(n,6)/7 >= n^6/322560` and `mM <= n^(17/4)/6`; `n^(7/4)>=107520` makes the latter at most half the former. The estimate holds for every placement and deletion set, independent of whether the deletion is chosen before or after sampling.

### C. Probability, dependencies and both uniform quantifiers

The independent Bernoulli variables are indexed by entire triples, with probability `p=n^(-3/2)`. A forbidden pair indicator is a product of two such variables. Two distinct pair indicators are dependent precisely when they share a whole triangle. Merely sharing original vertices or geometric edges does not identify a random variable.

View `W_pi(F)` as a simple graph on the `M` triangle variables. With degrees `d_sigma`, the ordered distinct dependence sum is exactly

`Delta=p^3 sum_sigma d_sigma(d_sigma-1) <= M^3 p^3`.

The diagonal contributes `mu=E Z`. Consequently `mu>=c n^3` and `mu+Delta<=M^2 p^2/2+M^3 p^3<=n^(9/2)`. The Janson lower-tail bound gives `P(Z=0)<=exp(-a n^(3/2))` for `a=c^2/2`.

The [author-hosted Frieze–Karoński book](https://www.math.cmu.edu/~af1p/BOOK.pdf), Theorem 34.13 and its proof on printed pp. 712–714, was checked directly. Its proof identifies the denominator as `sum_i E(I_i Y_i)`, confirming ordered pairs and diagonal terms despite potentially confusing brace notation. The independent-subset product space and `t=mu` endpoint apply here. The paper uses a conservative factor-two version of the bound. This is a standard primary theorem import; no claim is made to formally certify Janson's theorem.

The labeled simple order type determines every six-point Radon partition through signed five-point minors and therefore determines `W_pi`. [Goodman–Pollack, Theorem 1](https://link.springer.com/content/pdf/10.1007/BF02187696.pdf), was checked in the original article: it gives the finite bound `n^(d(d+1)n)` for simple numbered configurations with `n>d`. At `d=4` this is exactly `n^(20n)`, with no hidden asymptotic constant. Its determinant-polynomial proof and finite component-bound interface were also inspected. It counts the needed labeled realizable types.

There are at most `(m+1)n^(3m)` possible deletion sets. The union bound must cover **both** order types and deletion sets; it does so before any adaptive cleanup. On its complementary event, every allowed deletion leaves a crossing in every generic placement. No conditioning on an adaptively chosen deletion and no independence of these failure events is presumed.

An arbitrary original-linear embedding can be perturbed to a generic one. The finitely many pairs of disjoint nonempty faces have positive distance, preserved by a sufficiently small vertex perturbation. An unwanted intersection between overlapping faces, or a degenerate simplex, would yield intersecting disjoint subfaces after canceling common barycentric coefficients. Thus preserving disjoint-face separation suffices for injectivity. Generic placements are dense, and unused labels can be inserted avoiding finitely many affine hyperplanes. The obstruction rules out nongeneric embeddings as well.

### D. Cleanup and both exact minima

The expected number of selected triangle pairs sharing an edge is `C(n,2)C(n-2,2)p^2<=n/4`. Markov bounds the chance of exceeding `m`. For `T`, the selected-triangle count, `E T=lambda=Mp` and `Var T<=lambda`, so Chebyshev bounds `P(T<lambda/2)` by `4/lambda`.

If neither failure occurs, choose one endpoint from each bad pair and delete the union of these choices. At most `B<=m` triangles are deleted and every bad pair is hit. This leaves a linear triangle family. The already uniform event applies to this particular adaptive deletion. Since `lambda/2-m>n`, more than `n` triangles remain.

The cleaned complex has exactly three distinct edges per retained triangle, hence more than `3n` edges on at most `n` vertices. Its simple one-skeleton violates the planar graph edge bound. A PL embedding of the complex in the plane would embed this graph topologically, which is impossible. Combined with the first-subdivision construction, this proves `e_PL=3` rather than only an upper bound.

The robust affine obstruction gives `e_lin>=5`. For the upper bound, place original vertices on the five-dimensional moment curve. Any six or fewer are affinely independent, and any two faces of a two-dimensional complex use at most six vertices. Their convex hulls therefore intersect exactly in their common face. This proves `e_lin<=5`. No subdivision is used for this upper bound.

### E. Explicit finite parameters

For `n=2^256`, `p=2^-384`, `m=2^320`, all powers and deletion budgets are exact. The entropy logarithm is bounded by

`m+256(20n+3m) < 2^331`,

while `a n^(3/2)>2^343`. The negative net exponent exceeds `2^342`, and the exponential failure is below `1/8`. Also `lambda>2^379`, `lambda/2-m>n`, the collision failure is at most `2^-66`, and the count failure is below `2^-377`. Their sum is less than one, so a suitable finite sample exists. No enormous sample, facet list or enumeration is claimed to have been produced.

## Reproduction and fresh controls

The five supplied programs replayed through the published isolated runner with zero exit status and empty standard error. Its input-hash checks confirm pinned sources and receipts were unchanged. The jobs report 16 original arithmetic checks, 396 earlier finite arithmetic/circuit checks, 3,852 probability checks, 841 primary-interface arithmetic/circuit checks, and the Fano-family geometry check with 861 triangle pairs and 84 isolated-point checks. Replaying historical finite code is computation, not adoption of its old review opinion.

The new `independent_controls.py` passed **13,344 exact assertions in 27 families**:

- Five additional linear triangle families: Pasch, six-facet windmill, five-cycle, disconnected triangles and the affine plane of order three. There are 174 subdivided triangles and 3,963 pairs. Intersection checking uses exact plane/segment intersections and coplanar planar orientations, materially different from the supplied basic-feasible-solution enumerator. It verifies expected common faces, absence of excess intersection, nondegeneracy and 348 isolated-point tests. Parameters on the moment curve are interleaved and shuffled.
- Forty generic seven-point placements are checked by explicitly solving for the two-dimensional Gale kernel and evaluating its coordinate-zero directions. This directly tests the half-circle mechanism. A generic six-point simplex-plus-interior-point example has an unbalanced one-versus-five Radon partition, detecting the false replacement of seven points by six.
- Every nonempty witness graph on five Bernoulli variables—1,023 graphs—is evaluated over all 32 samples. Exact moments confirm the ordered-dependence and diagonal formulas. Exact odd Taylor lower bounds for `exp(-x)` give conservative finite Janson controls. Adaptive deletion is strictly worse than a fixed deletion for 1,008 of these graphs, detecting omission of that quantifier.
- Exact integer/fraction calculations recheck the displayed large parameters and a bounded power-parameter scan. The scan is a consistency test, not a smallest-witness claim. Setting epsilon to zero is detected as degeneracy.

These checks support the analytic proof; finite examples do not establish its universal statements by themselves. There was no numerical optimizer, floating-point geometric tolerance, or simulation substituted for the existence proof.

## Remaining gap and disposition

No unresolved mathematical gap was identified for the exact theorem after this review. The imported order-type and probability theorems have the required scope; the PL geometry and generic-perturbation argument were reconstructed directly. A literal direct substitution into Lee–Nevo's lemma would have the wrong uniformity parameter, but the private-vertex restriction argument and the independent first-subdivision proof resolve that interface.

The work does not supply a concrete huge facet list, establish bibliographic priority against all literature, or provide formal/human verification. Those are limitations of what was reviewed and claimed, not defects in the stated finite existence theorem. Primary downloads and rendered pages are ignored caches; URLs, hashes and timestamps remain in `reference_receipts.json`.

No source repair, website, spreadsheet, Git, publication or Zenodo mutation was made. No external person was contacted.
