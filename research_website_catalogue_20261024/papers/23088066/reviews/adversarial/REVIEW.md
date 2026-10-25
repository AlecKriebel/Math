# Adversarial review — Zenodo 23088066

**Verdict: PASS for the stated existence theorem.** No substantive mathematical defect or unresolved central proof gap was found in the actual published v1.0 paper, *A two-dimensional complex with embedding-dimension gap two*.

## Object, independence, and scope

All five published PDF pages and the corresponding source were read. The mathematical portions of the probability derivation and first-subdivision supplement, and all five verification programs, were examined.

- PDF SHA-256: 5325fceeed4352f74b531a033e8474ca1fabeeff0a6b6ecb54337e17dadb4dd6
- ZIP SHA-256: b1e4a1c22fc3eec24c9d8f479b48110ddf6d72052181995037de64b99d46791f
- Record: https://zenodo.org/records/23088066

Initial proof reasoning came from the manuscript. The fresh exact program was written before reading archived verifier implementations. No sibling opinion or historical adjudication body was consulted. The mathematical support documents do contain incidental assessment phrases: the probability derivation says certain candidate steps are correct, and the subdivision supplement's introductory wrapper mentions a previous adversarial pass. Those phrases were visible and are disclosed; they were not used as evidence. The probability document's introductory verdict and artifact-assessment sections were skipped. This review is therefore not described as perfectly blinded to every historical status phrase.

The strongest verified result is the existence of a finite two-dimensional simplicial complex \(K\) with
\[
e_{\mathrm{PL}}(K)=3,\qquad e_{\mathrm{lin}}(K)=5,
\]
whose first abstract barycentric subdivision has a straight simplicial embedding in \(\mathbb R^3\). Here linear embedding means affine on the **original** simplices. Subdivision is allowed only for the PL invariant. The theorem neither asserts a manifold example nor supplies an explicit enormous facet list.

**Exact remaining central gap:** none identified. The universal result is supported by the written proof and checked imported theorems. Finite controls alone do not prove it.

## Geometric proof and boundary cases

The incidence graph construction is valid even with cycles. Distinct nodes on the three-dimensional moment curve make every four nodes affinely independent. Two nonincident segments cannot intersect without an affine dependence among their endpoints; incident segments cannot have an extra intersection without a three-point dependence.

Within an original facet, the three displacement vectors from its facet node form a basis. In these coordinates, the six small triangles are exactly the cone from the origin over the six-cycle
\[
e_1,\ \varepsilon(e_1+e_2),\ e_2,\ \varepsilon(e_2+e_3),\ e_3,\ \varepsilon(e_3+e_1).
\]
Each is nondegenerate. Coplanar pairs meet in the intended diagonal, and pairs in different coordinate planes meet only on their common coordinate axis. The resulting intersections are the abstract subdivision's common faces.

The edge-subdivision vertices can be assigned independently because linearity of the triangle family makes each original edge private to one facet. “Barycenter” names an abstract vertex of the subdivision; it is not a constraint to use an arithmetic midpoint in the target. This distinction is explicitly made in the paper.

For different facets, the distance estimate to an incidence segment is at most \(\varepsilon L\). The original-vertex balls can be chosen uniformly because there are finitely many disjoint compact nonincident edges. After removing smaller open balls, distinct incidence stars are compact and disjoint, so a positive separation \(\delta\) exists. The two-radius argument prevents an alleged intersection outside the larger balls from being hidden inside the removed portion of a star.

Inside a vertex ball, a small triangle whose associated segment is nonincident to that vertex is excluded by the \(3r\) separation. For the remaining triangles, writing
\[
x-v_i=\alpha(f-v_i)+\mu\varepsilon a_j,\qquad
\alpha\ge\mu(1-\varepsilon)
\]
bounds the relative directional error by
\[
q=\frac{\varepsilon L}{(1-\varepsilon)\ell}.
\]
Away from the common vertex, \(\alpha>0\). The finite minimum angle between distinct facet rays is positive. Thus a sufficiently small common \(\varepsilon>0\) makes all angular cones disjoint. The same choice can satisfy every distance and angle inequality. No uniform-in-size lower bound on \(\varepsilon\) is required.

Empty or single-facet cases are trivial; absent pairwise constraints are omitted. Isolated vertices, when included as in the supplement, are handled by finite separation. None of these boundary cases affects the main nonempty construction.

## Balanced Radon witnesses and the deletion quantifier

The seven-point argument works for every generic configuration, not only cyclic configurations. The homogenized \(5\times7\) matrix has a two-dimensional kernel. A nonzero kernel vector cannot have two zero coordinates because that would give a dependence among five columns. Coordinate-zero directions on its circle are therefore distinct and each crossing changes the positive count by one. A half-turn changes the count from \(k\) to \(7-k\), forcing a transition between three and four positives. At that transition the remaining coefficients split three positive and three negative, yielding intersecting disjoint triangles.

Counting witness/seven-set incidences gives
\[
|W_\pi|\ge\frac{\binom n7}{n-6}=\frac{\binom n6}{7}.
\]
No uniqueness assumption about the witness in a seven-set is used. Removing any \(m\) triangles destroys at most \(mM\) pairs. The conditions \(n\ge12\) and \(n^{7/4}\ge107520\) give the stated lower bound \(cn^6\), with \(c=1/645120\).

The independent Bernoulli variables are indexed by whole triangles. Two pair indicators that merely share geometric vertices or edges can still be independent. Distinct witness events are dependent exactly when their two-element supports share a triangle, in which case the joint expectation is \(p^3\).

The ordered off-diagonal overlap count is
\[
\sum_\sigma d_\sigma(d_\sigma-1)\le M^3.
\]
The diagonal contributes \(\mu\). Consequently the stated Janson denominator \(\mu+\Delta\) and exponent are valid. In particular, omitting the diagonal or silently switching to an unordered sum would be wrong; the manuscript does neither.

On each six-set, signed five-point minors determine the Radon split, so the labeled simple order type determines every witness pair. The exact bound \(n^{20n}\) has the required labeled, generic scope. There is no coordinate-grid restriction.

The union bound ranges over **all** deletion sets from the full triangle ground set, not just one fixed deletion or only deletions chosen independently of the sample. Therefore its complementary event applies to the cleanup chosen after observing the entire sample. This is the central robustness step, and its quantifiers are in the correct order.

## Nongeneric embeddings and exact minima

If an original-simplex affine embedding exists, every pair of disjoint nonempty faces has positive distance. There are finitely many such pairs, so small perturbations preserve all separations.

These conditions also prevent degeneracies or excessive intersections of overlapping faces. Subtract two barycentric representations of an alleged collision and cancel common coefficients. The positive and negative residual supports are disjoint subfaces, with equal positive total mass; normalizing gives an intersection of their images, a contradiction. Generic placements are dense, and unused labels can be added while avoiding finitely many determinant-zero sets. Thus restricting the obstruction to generic placements does not lose a possible nongeneric embedding.

The cleanup chooses one endpoint of each edge-sharing pair and takes their union. It deletes at most the number \(B\) of offending pairs and hits every such pair. Neither independence between collision indicators nor independence of the three favorable events is assumed.

After cleanup, more than \(n\) triangles remain and each contributes three distinct graph edges. The one-skeleton has more than \(3n\) edges on at most \(n\) vertices, contradicting the planar simple-graph edge bound. Hence the PL embedding dimension is at least three, and the subdivision construction supplies the reverse bound.

The robust obstruction excludes original-linear embeddings in \(\mathbb R^4\), and therefore also all lower dimensions. The five-dimensional moment curve makes every set of at most six vertices affinely independent. Any two original faces use at most six vertices, so their convex hulls meet exactly in their common face. This gives the matching upper bound five.

## Finite parameter check

The finite choice \(n=2^{256}\), \(p=2^{-384}\), \(m=2^{320}\) was checked with exact integers and fractions, without evaluating enormous exponentials or generating a random complex.

The fresh calculation checks the exact surviving-witness count, the expectation and dependence envelopes, \(an^{3/2}>2^{343}\), a prefactor logarithm below \(2^{331}\), and a net exponent exceeding \(2^{342}\). It also verifies the collision bound \(2^{-66}\), \(\lambda>2^{379}\), the triangle-count failure bound \(2^{-377}\), \(\lambda/2-m>n\), and the total failure bound below one. The logarithm bounds use elementary inequalities, not floating-point approximations.

## Primary-source interfaces

Fresh downloads and hashes are in reference-receipts.json.

- [Brehm's original 2006 report](https://ems.press/content/serial-article-files/46044), pp.701–702, asks about the difference of the two **minimum** dimensions without a manifold restriction. The theorem addresses that question.
- [Brehm–Sarkaria's original preprint](https://archive.mpim-bonn.mpg.de/id/eprint/1946/1/preprint_1992_52.pdf), definitions and Theorem A, distinguishes original-simplex linear embeddings from derived-complex embeddings. Its fixed-ambient separation does not itself identify a minimum-dimension gap of two.
- [Goodman–Pollack's original article](https://link.springer.com/content/pdf/10.1007/BF02187696.pdf), Theorem1 and §2, gives \(n^{d(d+1)n}\) for simple numbered configurations. Both the statement and its finite sign-polynomial argument were checked.
- [Newman v3](https://arxiv.org/pdf/2212.09576v3), Theorem11/Lemma12 and the Radon discussion, use the same labeled order-type interface. The manuscript uses ambient dimension four, safely within the corrected even-dimensional scope of v3.
- [Frieze–Karoński's August 7, 2026 text](https://www.math.cmu.edu/~af1p/BOOK.pdf), §34.6/Theorem34.13, applies to indicators of fixed subsets of an independently sampled ground set. The triangle-variable model satisfies those hypotheses.
- [Janson–Warnke's primary paper](https://arxiv.org/pdf/1406.1248), opening definition and equation(2), independently confirms the ordered-pair plus diagonal convention and the lower-tail bound. The original 1990 article was not separately read in full; the explicitly cited textbook theorem and this primary restatement establish the precise formula used.
- [Lee–Nevo v1](https://arxiv.org/pdf/2307.14195v1), Lemma3.1, concerns linear \((d+1)\)-uniform hypergraphs in dimension \(d\ge3\). For triangle families in \(\mathbb R^3\), one may adjoin a private vertex to each triple and restrict a resulting PL embedding. The manuscript's self-contained lemma supplies the stronger first-subdivision conclusion directly, without transferring that stronger claim from Lee–Nevo.

## Evidence and limits

The fresh standard-library program passed 2,986 exact checks, including 12 generic configurations, all 1,024 triangle subfamilies on five labels for cleanup, and all 1,161 pairs of subdivision triangles across five examples. The examples include shared vertices, an incidence cycle, and the Fano plane. Exact basic-feasible-solution enumeration checks whole intersection polytopes, not sampled points. Three additional controls detect transversal/coplanar forbidden intersections and reject a disjoint intersection.

All five published programs replayed in isolated temporary folders. Their deterministic receipts matched; only the explicitly designated primary-receipt timestamp was ignored. The probability program includes ten rejected mutations; the geometry program includes 861 Fano triangle pairs and 84 isolated-point checks. All 41 package-manifest files and all acquired top-level hashes matched.

These tests do not enumerate the existential witness, formalize the imported theorems, prove historical priority, or predict journal acceptance. The source's bounded historical literature audits were not adopted as a new novelty certification. No source repair, external communication, Git operation, website, spreadsheet, or Zenodo mutation was performed.
