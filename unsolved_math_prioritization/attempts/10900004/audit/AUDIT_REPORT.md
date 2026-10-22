# Independent adversarial audit: glued figure-eight exteriors

Problem 10900004 / AMR-108-0004, Danciger Question 1.4, rank 508.

**Verdict: PASS_SCOPED_PARTIAL. Recommended disposition: unsolved 5/5. Full resolution: false.**

The frozen package supplies valid elementary restrictions on five proposed construction routes. It neither constructs convex structures for arbitrary torus gluings nor proves that a particular glued manifold lacks all such structures. No mathematical blocking defect was found. One nonblocking comment-level terminology error is recorded below. This is an independent assisted audit, not human peer review or a historical-priority certificate.

## 1. Frozen input and replay

The reviewed input consists of the seven files named in the author's freeze manifest: README.md, RESEARCH_LOG.md, RESULT.md, SOURCE_AUDIT.md, STATUS.json, checks/check.py, and checks/results.json. All byte counts and SHA-256 hashes matched before review and again after verification. The audit did not edit any frozen file. FROZEN_INPUTS.json records the identities independently.

The author verifier was copied to a separate directory before execution because it writes results.json next to itself. Its **127,601 assertions passed**, and its output file was byte-for-byte identical to the frozen checks/results.json. author_rerun.json contains that compact output, not an imported source document.

The independent audit_controls.py imports no author code. Its **44,395 exact assertions passed**, including **11 negative controls** aimed at plausible overgeneralizations. It uses only the Python standard library and can be run from any working directory:

`python audit_controls.py --output audit_controls.json`

The assertion totals count finite controls, not independent theorems. In particular, 127,601 successes do not certify a global projective holonomy or settle an infinite family. The author already states this limitation correctly.

## 2. Source and target identification

The original first page of Delp--Hoffoss--Manning, *Problems In Groups, Geometry, and Three-Manifolds*, was inspected in rendered form and extracted text. Question **1.4** asks about two figure-eight exteriors glued by a homeomorphism and explicitly distinguishes the known identity double. Interpreting the residual problem as arbitrary gluing is correct. Question 1.5 is the broader hyperbolic-JSJ question; this package does not resolve it.

The local published Ballas--Danciger--Lee paper was checked at Theorems 1.1, 1.3 and 1.4, Remark 3.3, the middle-eigenvalue discussion and Definition 5.2, the Section 6 gluing argument, and Theorem 7.5. The rendered published page 1598 confirms equation (1-1) and Theorem 1.4 without relying only on damaged PDF text extraction.

These checks establish the following distinctions:

- Theorem 1.1 constructs the double under relative infinitesimal projective rigidity. Remark 3.3 identifies the figure-eight complement as satisfying that hypothesis.
- Theorem 1.3 supplies genuine convex pieces with principal totally geodesic boundary. It does not supply arbitrary prescribed boundary representations.
- Theorem 1.4 requires full neighborhood holonomy matching under the prescribed boundary marking. The inverse placement of the conjugator in RESULT.md is equivalent to BDL's convention: the author's C is BDL's g inverse.
- Principal boundary includes the geometric thickening needed for convex gluing. A triangle action or an arbitrary representation of the amalgam cannot replace this hypothesis.
- Theorem 7.5 has lattice-isometry and nonconstant deformation hypotheses. It does not assert arbitrary torus gluing.

The bibliographic identity used by the package is BDL, *Convex projective structures on nonhyperbolic three-manifolds*, Geometry & Topology 22 (2018), 1593–1646, DOI 10.2140/gt.2018.22.1593, arXiv:1508.04794. The erroneous arXiv:1510.07739 is not used as support for a mathematical claim.

This audit independently checks the core source content locally. It does not rerun live repository searches or certify the completeness of the author's current-literature scan. The 2024–2026 abstract-level checks and duplicate searches in SOURCE_AUDIT.md remain bounded author-reported research history. No proof here depends on those searches returning no later result. Likewise, the exact numbering of the cited Benoist survey was not independently re-fetched; the strict-convexity/word-hyperbolicity implication itself is correctly stated and is also identified on the original problem source's first page. No remote access or remote mutation was performed during this audit.

Public references:

- Original problem: https://arxiv.org/abs/1512.04620
- BDL: https://doi.org/10.2140/gt.2018.22.1593 and https://arxiv.org/abs/1508.04794
- Benoist's cited survey: https://www.imo.universite-paris-saclay.fr/~yves.benoist/prepubli/06beijing.pdf

## 3. Approach 1: topology and the strict-convexity obstruction

### Homology and marking convention: PASS

For column coordinates, A sends the meridian to (a,c) and the longitude to (b,d). The meridian generates H_1(M), while the preferred longitude maps to zero. Consequently the two abelianized gluing relations are x-a y=0 and b y=0. Eliminating x yields exactly Z/bZ, including Z when b=0. The injective map on H_0 in Mayer--Vietoris supplies no extra free summand.

The coefficient is **b**, not c. The independent verifier counts all homomorphisms of this presentation into Z/n for n=2 through 13 and all 360 unimodular matrices in the box [-4,4]^4. The answer is gcd(|b|,n), as required. These controls use character counts rather than repeating the author's matrix reduction. The explicit upper shear with b=3,c=0 rejects the transposed convention.

Both determinant signs are legitimate in the unoriented problem. Two orientable pieces joined along their sole boundary component can be coherently oriented by reversing the chosen orientation of one piece as necessary. Thus b=1 indeed gives an integral homology sphere: H_1 vanishes and orientability plus duality supplies the remaining homology groups. Positive k values at least two give distinct homology orders; no claim incorrectly distinguishes k from -k using homology alone.

Swapping the pieces replaces A by A inverse. Its upper-right entry is -b/det(A), so the absolute torsion order is unchanged. This is an additional convention check in the independent controls.

### Strict proper convexity: PASS, with the stated scope

Each boundary subgroup is an injected Z^2 in a finite-volume hyperbolic knot group. Van Kampen produces an amalgam of the two vertex groups over this subgroup, not an HNN extension and not a Dehn filling. The normal-form theorem preserves injection of the edge group. Hence every N_A contains Z^2 in its fundamental group.

A closed manifold with a strictly properly convex developing image has a cocompact dividing group. Benoist's strict-convexity/word-hyperbolicity theorem applies in this cocompact setting. Its group cannot contain Z^2. The contradiction therefore excludes the **strictly properly convex** variant for every A.

Nothing in this argument excludes properly convex domains with boundary segments. This distinction is essential because the known double provides precisely the relevant non-strict type of example. The package maintains it throughout.

## 4. Approach 2: transfer and amalgam holonomy

### Extendable boundary maps: PASS

The formula E_2 A E_1 inverse follows by applying h_1 and h_2 to the gluing relation. Every extendable map preserves the kernel Z lambda of the inclusion on H_1. Since it is integral and invertible, its second column is (0,epsilon), with epsilon equal to 1 or -1. Such matrices form a subgroup, so the left/right orbit of the identity has upper-right entry zero.

Therefore nonzero upper shears do not arise by this particular transfer of the double. This is not a classification of all homeomorphisms of the glued manifolds, nor an assertion that every lower-triangular unimodular marking extends. The body of Proposition 2.1 states exactly this limited conclusion. Independent controls also check that these left/right actions preserve |b|.

### Representation matching: PASS

With the second edge injection precomposed by A, the common-conjugator equation is rho_1(h)=C rho_2(Ah) C inverse. The universal property of the amalgam gives the asserted equivalence for extension of the two **specified** representations, with the second allowed one global conjugation. Checking the two peripheral generators with the same C suffices because they generate the edge group.

The trivial representations expose why matching alone says nothing about faithfulness, discreteness, or a developing embedding. The application of BDL adds actual convex structures on both entire pieces with principal boundary; it does not infer those structures from local matrices. The imported geometric conclusion is existential: suitable positioning and, if needed, a centralizing reflection arrange the pieces on opposite sides. It should not be read as a claim that every chosen algebraic conjugator gives a convex realization. The frozen text does not make that stronger claim.

## 5. Approach 3: joint characters and false positives

### Projective normalization and joint eigenspaces: PASS

Positivity matters. For positive determinant-one diagonal lifts, a scalar relating conjugate lifts must be positive, and its fourth power is one; hence it is one. There is no extra projective scalar character. Distinct joint characters on Z^2 give four one-dimensional common eigenspaces even when either generator separately has repeated eigenvalues. A conjugator must permute those lines, giving precisely W_1=P W_2 A. If a prescribed triangle is to be preserved, its complementary eigenline must also be preserved.

For the author's (U,V) and (U,V') examples, the independent control computes the maximum rank of a simultaneous intertwiner from its joint-eigenvalue blocks. It is **two**, so no invertible simultaneous conjugator exists. This independently supports the simpler argument from the distinct eigenvalues of U. The determinant-one normalization also eliminates a possible projective rescaling loophole.

The triangle translation matrices have determinants 18 and -6, respectively. Both therefore give free proper cocompact actions on the open triangle. The first three character rows sum to zero and have rank two; on a nonzero vector their evaluations cannot all vanish, and their zero sum forces a strictly negative minimum and a strictly positive maximum. This proves the transverse middle-eigenvalue property for all real nonzero vectors, beyond the author's bounded samples. It still does not imply extension over the knot group or existence of a convex piece.

### Quadratic data: PASS as necessary, correctly rejected as sufficient

The Gram identity follows by multiplying the joint-character identity by its transpose. W_0 and -W_0 have the same positive definite Gram matrix but different row multisets, so the displayed false positive is valid. Rank-two triangle action and the middle transverse eigenvalue do not repair that failure.

The independent controls add a separate transverse-holonomy false positive. Compare character matrices 10W_0 and the matrix with rows (11,1),(1,11),(-9,-9),(-3,-3). On their first-three-coordinate triangle, all character differences agree, so the induced projective surface actions are identical. Their full four-row multisets differ. The fourth row in the second model is the positive barycentric combination with weights 1/5,1/5,3/5 of the first three rows. Thus even this nondegenerate middle-eigenvalue example shows why surface holonomy cannot replace neighborhood holonomy. This control, too, is purely peripheral.

## 6. Approach 4: bending, finite stabilizers, and rays

### Centralizer: PASS

The multiplication C to ZC preserves the gluing equation when Z centralizes the **entire** first peripheral image. The domain group remains the same amalgam with the same A. A matrix centralizing only one generator is insufficient; the independent negative control uses repeated meridian eigenvalues and a permutation that changes the longitude.

No claim that all resulting representations are distinct or convex is needed or made. Allowing conjugation of one piece by a peripheral centralizer is not permission to change the topological marking.

### Fixed full-rank model: PASS

From WA=PW and P^m=I one obtains WA^m=W, hence A^m=I because W is injective as a map from R^2. There is at most one A for each P. The bounds 24 and six are therefore valid upper bounds, without a classification of all finite subgroups of GL(2,Z).

The full-rank hypothesis is indispensable. The independent negative control has four distinct rows all supported on the second coordinate; it is fixed by a nontrivial upper shear. The model is rank one and thus outside the stated proposition. Distinct joint characters alone would not suffice.

### Independent scaling: PASS

The hypotheses inherited from the fixed-model discussion are rank(W)=2 and A in GL(2,Z), with both scaling factors nonzero. Under these hypotheses the author's permutation-power argument is valid. An independent proof starts from A transpose Q A=r^2 Q, where Q=W transpose W is positive definite. Determinants give (det A)^2=r^4, so |r|=1. Substituting back in the finite-permutation relation gives finite order. If both parameters lie on the same positive ray, r=1.

For W_0 the independent computation derives candidates from Q(x,y)=2(x^2+xy+y^2), rather than extracting rows from permutations as the author does. The six integral vectors with x^2+xy+y^2=1 supply all possible columns. There are twelve integral Q-isometries and exactly six preserving the character multiset. The other six are their negatives. This independently recovers the displayed stabilizer and its signed-ray extension.

These statements concern fixed marked full-rank peripheral shape. They do not describe the entire deformation space of either piece. Rank collapse and unipotent Jordan limits are expressly excluded. The independent controls reject both omission of unimodularity and identification of zero logarithmic eigenvalues with trivial holonomy.

## 7. Approach 5: covers and descent

### Cancellation of inherited peripheral data: PASS

For the chosen column convention, A B_1=B_2 D is the correct commutative cover diagram. Matching inherited holonomies gives W_1 B_1=P W_2 B_2 D. Substitution and right cancellation of the nonsingular real matrix B_1 yield the original downstairs condition. Restricting distinct real characters to a finite-index lattice does not merge them, because the lattice spans R^2. Thus allowing a new simultaneous conjugator upstairs does not defeat the argument.

The independent controls include 496 nonsingular integer cover matrices, four gluing matrices of both determinant signs and different dynamical types, and four upstairs basis changes D, including nonidentity ones. They compare whole row multisets for three model pairs. This extends the author's D=I controls and tests both mismatching and exactly matching cases.

The restriction to positive diagonal data is material. If U is the author's positive diagonal matrix, multiplying its first two diagonal entries by -1 produces a matrix that is not projectively conjugate to U but has the same square. Keeping the other commuting generator fixed gives agreement on an even-index lattice despite disagreement downstairs. This is outside the positivity hypothesis and demonstrates why that hypothesis cannot simply be dropped. Omitting the cover diagram is also rejected: one may not replace the prescribed downstairs gluing by a convenient different upstairs marking.

The calculation concerns torus covers and inherited representations. It does not assert that every such torus cover extends to a cover of the whole knot exterior, or that newly chosen upstairs structures descend. Any actual manifold-cover construction has those additional obligations.

### Representation extension and convex descent: PASS as necessary conditions

For H normal of finite index in G, an extension must implement the conjugation action of G on sigma(H), satisfy all multiplication relations, and in particular satisfy the stated power relation for a coset representative. Normalizing the subgroup alone is insufficient; the controls include a conjugacy-compatible choice that fails the required square relation.

The author's semidirect model is internally correct: the order-two element swaps the generators of H=Z^2. Its two positive determinant-one spectra are not conjugate even after allowing every possible projective scalar. Hence its specified representation does not extend. The independent controls verify both the group relation and scalar-aware spectral obstruction.

The semidirect product contains torsion and is not presented as a glued-manifold group. Its role is solely to demonstrate the algebraic extension obstruction. Even a successful group representation extension would leave geometric descent to check, including compatibility with the developing map, invariance of the domain, and the appropriate free proper action. The package states necessary conditions and does not claim an unproved converse. Passing to a normal core is the usual preliminary step if an actual finite cover is not regular.

## 8. Findings and release boundary

**Blocking findings: none.**

**Nonblocking terminology:** checks/check.py, line 46, calls the homology relation matrix “row-equivalent” to its diagonal form. The implemented operation is explicitly a column operation. “Unimodularly equivalent” or “column-equivalent” is the accurate description. The actual computation, the cokernel conclusion, and RESULT.md's proof are correct. No frozen file was changed to repair this comment.

For maximal standalone clarity, Proposition 4.3 could restate rank(W)=2 and A in GL(2,Z) instead of inheriting them from the preceding discussion. This is editorial clarification, not a missing hypothesis in the package's context and not grounds for HOLD.

There is no basis to upgrade the status to solved. The remaining central gap is still global: find convex-piece representations with genuinely suitable varying peripheral shapes for every A, or establish an obstruction to every possible convex realization for one A. None of the finite computations supplies that missing step.

The portable audit consists only of this authored report, the independent verifier and its compact output, author_rerun.json, FROZEN_INPUTS.json, and AUDIT_MANIFEST.json. It excludes all PDFs, complete source extracts, screenshots, source-corpus records, private material, and execution work directories. This audit authorizes no remote mutation and makes no historical novelty claim.
