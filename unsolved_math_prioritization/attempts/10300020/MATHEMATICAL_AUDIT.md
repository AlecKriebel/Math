# Independent audit: exact norm spectra for normal lamination cycles

Problem 10300020 / AMR-102-0020; Calegari Question 7.5; rank 1249.

## Verdict

**ACCEPTED AS A CORRECTED PARTIAL RESULT, 1/5.** The report distributed as [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md) proves the stated padding and upper-ray theorems and the exact infimum-plus-endpoint reformulation in its finite real singular-chain setting. The zero-volume and closed-hyperbolic nonattainment arguments are valid. Its applications to prior restricted normalization results are sound, with the qualifications below.

This is **not** an unrestricted solution, counterexample, novelty certificate, or current-openness certification. In particular, neither equality of the flexible normal infimum with ordinary simplicial volume nor the general endpoint condition has been proved.

The distributed report has 24,227 bytes and SHA-256:

`1709810a11d27a9399525b9b6bf9e8151f8b3f180250608ef316eef4c846ae14`.

This AI-assisted, unrefereed proof-and-audit edition retains all mathematical arguments and qualifications. Private input identities and supplemental computational commentary are omitted. Scoped acceptance is not external human peer review, journal acceptance or formal proof-assistant certification.

## 1. Scope and original quantifiers

The audited theorem concerns a nonempty, connected, closed, oriented 3-manifold; finite real chains in the ordinary, unnormalized singular complex; and nonempty essential laminations. The chain norm is computed after collecting identical parameterized singular maps. No identification by reparameterization or homotopy is allowed.

The original question permits the replacement lamination to depend on the supplied cycle. It does not require the new lamination to be isotopic to the supplied one. The input lamination therefore establishes that the manifold admits an essential lamination; it does not fix the lamination against which every later cycle must be normalized. The positive-coefficient question occurs separately in the source's following discussion. The accepted result does not promise positive coefficients.

The original source page was independently inspected: Calegari's problem list, printed/PDF p14, Question 7.5 and its surrounding remarks. Its p2 coorientation warning was also read. The target identity, source interpretation, and restrictions agree with that page. The older literature summary was not treated as evidence that no later solution exists.

A scope issue has been repaired: statements equating the original question with a numerical condition must assume that M actually carries a nonempty essential lamination. If there is no input lamination, the original assertion has no instances, whereas the union defining B is empty and its infimum is infinite. Corollaries 3.3–3.4 and Consequence 4.3 retain this hypothesis expressly; section 1 supplies it for all discussions of the original question. Empty laminations are expressly excluded from B.

## 2. Normality and chain conventions

Kuessner's published normality definition on printed p115 (issue PDF p117) was inspected directly. It is a condition on inverse-image disks and their edge incidences. It is not a requirement that those disks themselves be affine subsets. Consequently, precomposing by a homeomorphism fixing the boundary pointwise preserves the condition.

For each leaf F and boundary-fixed h, the inverse image under sigma composed with h is the h-inverse image of the old inverse image. Disk components remain disk components. Each edge is fixed pointwise, so each disk's edge-intersection sets are unchanged, not merely bounded by a comparable number. Every face restriction is exactly the old parameterized face restriction. Any applicable full-face or whole-leaf exceptional convention is also unchanged. Thus the proof is independent of whether particular constant simplices are admitted as normal.

Calegari's finite-real-chain definition was inspected on p5 of *The Gromov norm and foliations*. Thurston's first definition in section 6.1 independently makes the basis of all continuous parameterized maps explicit. These justify the support convention needed by padding. The source's later use of other chain models does not authorize changing this manuscript's chain model.

The manuscript does not infer normality from literal affine transversality. Kuessner's assertion that the two relevant notions coincide for foliations is used only in the attributed fixed-foliation obstruction, not in the elementary padding proof.

## 3. Detailed padding audit

### 3.1 Existence of infinitely many new parameterized maps

A nonconstant continuous map on the closed simplex cannot be constant on its interior, because the interior is dense and M is Hausdorff. Its interior image is connected and has at least two points. A finite Hausdorff space is discrete, so a connected image with at least two points is infinite.

Fix an interior point x0. The boundary-fixed homeomorphism group of the 3-ball acts transitively on its interior: a compact path between two interior points can be covered by finitely many small interior balls, and point-moving homeomorphisms supported in those balls can be composed. This uses no geometry of the lamination.

Evaluating sigma composed with h at x0 therefore produces infinitely many different values. For any finite set E of old singular maps, exclude the finite evaluation set consisting of eta(x0), for eta in E. Two different remaining values give two maps distinct from each other and from every old basis element. The method excludes coincident maps, which is the necessary chain-level condition. Disjoint geometric images are neither required nor asserted.

### 3.2 The explicit cone identity

Regard h1 and h2 as singular 3-simplices in the convex target Delta^3. Because they agree with the identity on the entire boundary, their singular boundaries agree term by term.

The cone K with apex w is continuous even at its cone vertex: the scalar factor multiplying the bounded image of f tends to zero. The zeroth face of K(f) is f. Its face with index i+1 is K of face i of f, with sign (-1)^(i+1). Hence in positive degree

`boundary K(f) = f - K(boundary f)`.

It follows exactly that the 4-chain K(h1)-K(h2) has boundary h1-h2. Composing both 4-simplices with sigma proves the claimed boundary identity in M. Degenerate simplices are retained, as they must be in the ordinary singular complex. No stationary-prism term is discarded. The filling chain need not be normal; only the final 3-cycle does.

This argument is stronger than an informal appeal to homotopy relative to the boundary: it supplies the chain and verifies its signs.

### 3.3 A nonconstant supported term exists

The singular boundary of the constant 4-simplex at p is the constant 3-simplex at p, since the five alternating face signs sum to one. Thus every finite chain supported entirely on constant 3-simplices is a boundary. A real fundamental class of a nonempty closed oriented manifold is nonzero, so a fundamental cycle has a nonconstant supported simplex with nonzero coefficient.

The argument does not require the lamination to have a complementary open ball. In particular, it works when the lamination is a foliation of all of M.

### 3.4 Exact norm increase

The two fresh maps tau1 and tau2 are normal and satisfy tau1-tau2 = boundary B. They are distinct basis elements outside the old support. For t=(r-||z||_1)/2 >= 0,

`z_r = z + t(tau1-tau2)`

represents the same class, and its collected norm is exactly ||z||_1+2t. Arbitrary signs on the old coefficients cause no problem. When t>0 the new coefficients have opposite signs; the manuscript correctly disclaims preservation of an all-positive convention. When t=0 the old cycle is reused.

**Conclusion:** Lemmas 2.1–2.4 and Theorem 2.5 pass. In particular, the objection that reparameterization might destroy a literal affine disk arrangement does not apply to the published normality definition being used.

## 4. Spectra, endpoints, and variable laminations

For each fixed L, any attained normal norm r yields every larger real norm by padding while retaining L. A nonempty B_L is bounded below by zero and has finite infimum. Given s above that infimum, some element of B_L is below s; padding then realizes s. Thus the only remaining choice is inclusion of the infimum itself.

The same conclusion holds for the union B. The lamination witnessing one element of the union also witnesses all larger elements. The proof does not require one fixed lamination to work for a sequence approaching the flexible infimum. Nor does it confuse an infimum over laminations with a minimum over laminations.

Ordinary fundamental cycles exist, and the same padding proof without normality gives the upper-ray form of A. Every normal cycle is ordinary, so B is a subset of A and V <= N whenever B is nonempty. If B is empty, the manuscript's infinity convention is consistent; N=V is then impossible because V is finite.

Theorem 3.2 is correct:

- The original exact replacement assertion says precisely A is a subset of B; combined with the automatic reverse inclusion, it says A=B.
- Equal sets have equal infima and agree on inclusion of the ordinary endpoint.
- Conversely, N=V supplies every attainable ordinary norm strictly above V. If an ordinary minimizer exists, the stated endpoint condition supplies the one remaining norm.

The endpoint condition must ask for a witness among **some** permissible laminations. It does not require every fixed lamination to attain its own infimum. The report uses the correct quantifiers.

When V is not attained, every ordinary norm r satisfies r>V. If an r fails to lie in B, upward closure forces N>=r>V, including the empty-B case. Conversely N>V yields an ordinary norm below N by the definition of V. This verifies Corollary 3.4. Strict positive gaps for individual laminations need not have a strictly positive common lower bound when infinitely many laminations are allowed; the manuscript explicitly recognizes this distinction.

The example chain complex in section 6.4 is also correct. Its linear functional annihilates each specified boundary and takes value one on the target class. Each admissible representative is finite and nonzero; on its finite support all functional coefficients have absolute value strictly below one. Therefore its norm is strictly greater than one, while the displayed single-basis representatives approach one. This is a valid logical model of an endpoint mismatch, not a manifold counterexample.

## 5. Nonattainment results

### 5.1 Vanishing simplicial volume

In the finite chain norm, only the zero chain has norm zero. It cannot represent the nonzero fundamental class. Proposition 4.1 is immediate and correct, independently of whether essential laminations exist. Its application to the original question uses the additional existence hypothesis.

### 5.2 Closed hyperbolic manifolds

Geodesic straightening is a chain map chain-homotopic to the identity. Each simplex in a finite ordinary singular cycle lifts to a simplex whose vertices are actual points of hyperbolic space; no ideal vertices arise merely by straightening. Signed volume evaluation on the straightened fundamental cycle gives the volume of M. Coinciding straightened maps and cancellations do not invalidate this equality: evaluation is linear on the original finite list as well as on the collected chain.

For a nondegenerate finite-vertex tetrahedron, send an interior point to the origin of the Klein ball. Extend the four vertex rays to the sphere at infinity. The origin remains in the interior of the convex hull of the extended vertices: a positive linear dependence among the finite vertex vectors gives a positive dependence among their unit radial vectors by rescaling the coefficients. Each original vertex lies on a segment from that origin to an ideal vertex. Therefore the finite tetrahedron lies in the ideal one. The containment is strict, with a nonempty open region in the difference, since the ideal tetrahedron extends toward infinity beyond the compact finite tetrahedron. Its volume is strictly larger. The ideal tetrahedron's volume is at most that of the regular ideal tetrahedron. Degenerate straightened tetrahedra have signed volume zero.

Thus each absolute simplex volume is strictly less than v3. There are finitely many supported terms, so their maximum q is also strictly less than v3. The fundamental cycle is nonzero and has positive norm. The triangle inequality gives

`Vol(M) <= q ||C||_1 < v3 ||C||_1`.

There is no use of a nonexistent uniform gap applying to all finite simplices: q depends on C. There is also no assumption that every straightened simplex is nondegenerate. The proportionality formula identifies the ordinary infimum with Vol(M)/v3, completing Proposition 4.2.

Thurston section 6.1, especially printed pp124–126, was inspected for straightening, finite/ideal volume comparison, and the proportionality statement. Kuessner's section 2C confirms the relevant simplicial-volume convention. The proof is not silently extended to ideal chains, measure chains, completed l1 chains, noncompact locally finite cycles, or all manifolds with hyperbolic JSJ pieces.

## 6. Prior-result applications and their hypotheses

### 6.1 Tight, unbranched, and one-sided cases

Kuessner's Proposition 2.3 and Lemma 2.4, printed pp116–119, were read with their proofs. The general lemma requires an aspherical oriented compact manifold, pi1-injective aspherical leaves, and the stated order-tree property; the essential-lamination proposition supplies the three-dimensional application. The boundary condition in the unbranched/one-sided statement has not been dropped for compact manifolds with boundary.

The proof explicitly normalizes a given cycle in a face-compatible way and preserves its homology class. A coefficient-preserving list can acquire cancellations after identical new maps are collected, so the direct norm conclusion is nonincrease, not necessarily equality. Once the resulting normal fundamental cycle exists, Theorem 2.5 restores the prescribed original norm. This justifies the manuscript's exact-cycle application without assuming ordinary nonattainment.

The restricted normalization results are credited as prior results. This audit verifies their stated applicability; it is not a new proof audit of the whole Kuessner paper or of every theorem it invokes.

### 6.2 The surface route for general closed M

The original essential-lamination hypothesis matters. Under it, the Gabai–Oertel consequences cited in Kuessner's proof give the relevant irreducibility/asphericity and universal-cover conclusions. In such an M, a two-sided closed pi1-injective surface S of positive genus is an essential surface. Cutting along it preserves irreducibility and gives incompressible boundary. There are no boundary-compression issues for the closed surface. The lifts are properly embedded planes, and the locally finite dual decomposition has a Hausdorff tree. If one follows Kuessner's no-isolated-leaves convention, replace S by its trivially laminated product neighborhood; this retains the tight essential-lamination route.

Kuessner's compact tight-lamination theorem therefore gives normal cycles for arbitrary closed M in this scope, not only hyperbolic M. Padding gives exact equality. A torus is allowed: pi1-injectivity excludes a torus bounding a solid torus. No claim is made that an incompressible positive-genus surface alone makes an arbitrary reducible manifold satisfy the essential-lamination hypotheses.

The report records this reasoning expressly. It does not rely on silently broadening the standing geometric context of Agol's volume paper.

### 6.3 Tao Li's tightening claim

Kuessner printed p169 was inspected. The closed, orientable, atoroidal, transversely orientable tightening premise is explicitly attributed there to Li's 2006 manuscript. The manuscript under audit conditions this route on that attributed result; it does not claim to have independently checked Li's proof.

On 10 October 2026 the departmental publication page still described the manuscript as a preliminary draft. The linked personal publication list was also inspected and did not list it. Those facts justify reporting the visible status and the retrieval limitation only. They do not establish withdrawal, invalidity, or current publication status elsewhere. The unsuccessful legacy-PDF fetch is recorded by the author. No proof conclusion in sections 2–4 depends on this inaccessible manuscript.

## 7. Barriers are not counterexamples

The fixed-foliation obstruction is correctly limited. Calegari's asymptotic-separation theorem concerns a prescribed foliation. Combining its strict foliated-norm gap with Kuessner's foliation normality convention obstructs replacing every cycle using that same foliation. It does not produce a lower bound uniform over all essential laminations on M.

The overlapping-ball example correctly shows that independently compatible source-domain plaques can have crossing target images. The example is only a failure of the implication from domain normalization to a target lamination; it is not an essential-lamination counterexample.

Similarly, normalization in a finite cover only gives an appropriate downstairs normal cycle if its lamination genuinely descends, for example when it is the full preimage of a downstairs essential lamination. Pushing forward and dividing by the degree then preserves the fundamental class and is norm-nonincreasing. Arbitrary upstairs laminations do not have this property, because their deck translates can cross.

The ambient coorientation warning is supported by the original source p2. The section rejects an automatic extension of the familiar foliation cover argument to all laminations. It does not claim that no individual lamination can lift to a coorientable one. These sections do not establish universal nonexistence assertions.

## 8. Relative, disconnected, and orientation issues

The principal accepted equivalence is only the stated connected closed oriented theorem. The underlying padding argument also works for a nonempty finite disjoint union with its specified fundamental class, because that class is nonzero and the proof needs only one nonconstant supported term. Extending the entire flexible-lamination statement would additionally require explicit conventions about which components must carry nonempty laminations; this extension is not claimed in the manuscript.

For the limited relative-chain remark, use the quotient chain norm on C3(M,boundary M;R), represented by deleting basis maps contained wholly in the boundary. If every remaining map were constant, the constant 4-simplex identity would make the class zero. A nonconstant remaining sigma has image not wholly in the boundary, and each reparameterization has the same image. The fresh maps therefore remain distinct nonzero basis elements in the quotient. Their difference bounds absolutely and hence relatively. This verifies the padding remark without asserting a geometric relative-normalization theorem under unspecified boundary conditions.

An orientation is needed to specify the nonzero real fundamental class. The argument is not extended to a nonorientable manifold with ordinary real coefficients, where the top class may vanish. Reversing the chosen orientation does not affect any norm assertion. Negative real coefficients are legitimate; rational- or integer-coefficient exact spectra would be different questions.

## 9. Corrections and final disposition

The report incorporates the following audit corrections:

1. It expressly excludes the empty lamination.
2. It retains existence of a nonempty essential lamination wherever the original question is converted into an infimum or gap assertion.
3. It states the general unresolved task as infimum equality **and** endpoint preservation wherever the ordinary infimum is attained.
4. It explains why the incompressible-surface route is valid for the general closed setting under the existing essential-lamination hypothesis, rather than on arbitrary reducible manifolds.

No core padding, cone, upper-ray, or strict-volume proof required correction. The supported classification remains **partial, attempt 1 of 5**. The audit consumes no additional proof-search turn.

## Primary sources and inspection limits

- Danny Calegari, *Problems in foliations and laminations of 3-manifolds*, Question 7.5 and p2: https://arxiv.org/abs/math/0209081
- Thilo Kuessner, *Generalizations of Agol's inequality and nonexistence of tight laminations*, Pacific J. Math. 251 (2011), pp109–172; relevant printed pp115–119 and 169: https://msp.org/pjm/2011/251-1/pjm-v251-n1-p.pdf
- Danny Calegari, *The Gromov norm and foliations*, finite-chain definition and Theorem 2.4.5: https://arxiv.org/abs/math/0007120
- Ian Agol, *Lower bounds on volumes of hyperbolic Haken 3-manifolds*, definitions and Lemma 5.1: https://arxiv.org/abs/math/9906182
- William P. Thurston, *The Geometry and Topology of Three-Manifolds*, section 6.1: https://library.slmath.org/nonmsri/gt3m/PDF/Thurston-gt3m.pdf
- Tao Li departmental status page: https://www.bc.edu/bc-web/schools/morrissey/departments/math/people/faculty-directory/tao-li.html
- Tao Li linked personal publication list: https://sites.google.com/bc.edu/tao-li/

During the mathematical audit, the first five cited PDF byte counts and SHA-256 values were independently recomputed. Selected source pages were read as PDF text; the original question, normality definition, theorem hypotheses, Li attribution, finite-real-chain definition, and ideal-volume-bound pages were additionally inspected visually. No claim is made to have audited Li's missing manuscript or the complete proofs of all cited prior theorems.
