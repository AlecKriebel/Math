# Independent audit of general Weddle locus dimensions

## Decision and exact scope

The dimension statements in [PROOF.md](PROOF.md) are accepted by this independent mathematical audit: Theorems A and B, Corollary C, and the elementary regimes in Theorem D. No mathematical correction to the final proof is required. The source-reading correction described below is incorporated in [SOURCE_REVIEW.md](SOURCE_REVIEW.md).

This is AI-assisted acceptance of authored partial results within this unrefereed work, not external human peer review, journal acceptance, formal proof-assistant certification or a priority claim. The original problem 30005298 / OWR-11695864-003 remains **OPEN**. The higher-dimensional conservative residual is n >= 4, d >= 2, d+2 <= r <= binomial(d+n-1,n-1)-2, except for values otherwise settled. The audit does not claim every residual value is independently open.

The target is the reduced closure of the outside-Z locus where the dimension of degree-d forms through Z with multiplicity d at the center exceeds its generic minimum. Nothing here accepts a degree, scheme multiplicity, reducedness of a determinantal scheme, ACM property, irreducibility, or a complete component classification.

The accepted public proof is 21,376 bytes with SHA-256 `89c6bba20bba24184358090101ceaf17408c30faf255e3d06baf94d5271d00af`. The full universal mathematical argument is retained; editorial changes update review status and remove private administrative framing.

## Accepted formulas

Set N = binomial(d+n-1,n-1).

- For n >= 2, d >= 2 and N <= r <= N+n-1, the locus is nonempty of dimension n+N-r-1. It is empty for r >= N+n.
- For n >= 3, d >= 2 and r=N-1, its dimension is n-2.
- In P3, for d >= 2, the dimensions are: empty at r=1; one for 2 <= r <= N-1; two at N; one at N+1; zero and nonempty at N+2; empty from N+3 onward.
- The elementary P1, degree-one, small-cardinality, and P2 classifications are correct as stated. In particular, the P2 endpoint r=d+2 consists of 3*binomial(r,4) distinct intersections of secants with disjoint endpoints for general Z.

## Independent proof audit

### The definition and generic minimum

The rank-N bundle is Sym^d(Q*) for the tautological quotient Q on Pn. Its inclusion in the trivial degree-d form bundle is legitimate. With each original point represented once by a nonzero vector, evaluation is a regular map to a trivial rank-r bundle. Choices of point representatives scale rows and do not change rank. Its fibers are exactly the cone-form spaces, because in coordinates centered at P, multiplicity d for a degree-d homogeneous form eliminates every monomial containing the center coordinate.

For a fixed center the projection map on the other points is dominant onto configurations in P(n-1). Independent conditions on degree-d forms can be constructed inductively until their N-dimensional space is exhausted. The nonvanishing of an appropriate evaluation minor is open. This proves the generic kernel dimension max(N-r,0), with the quantifiers needed for general Z followed by general P. A nonzero cone kernel cannot be equated with jumping below r=N.

The graph-intersection argument for determinantal loci is valid in a smooth local trivialization. The universal rank-drop variety has codimension r-N+1 for an r by N matrix with r >= N, and codimension two for an (N-1) by N matrix. Intersecting with the graph gives an upper bound on codimension of each nonempty component. It never gives equality automatically; equality is supplied separately by incidence upper bounds.

### Uniform incidence and simultaneous generality

Let B_e parameterize the vertex and a nonzero degree-e cone up to scale. It is a projective bundle of dimension D_e=n+N_e-1. For each parameter, its hypersurface has support dimension n-1 even if reducible or nonreduced. The incidence with s ordered points therefore has total dimension D_e+s(n-1). Fiber products of reducible hypersurfaces need not be irreducible, and irreducibility is not used.

There are finitely many irreducible components of each finite-type incidence. A component that does not dominate the configuration base is absent after removing its image closure. For a dominant component, the generic fiber has dimension at most D_e-s. Intersecting the finitely many resulting opens proves the stated upper bound, including emptiness for s>D_e. For fixed d,r there are finitely many degrees and subsets of the r labels. The pullback of each relevant general-position open is dense under the dominant subset projection, so all bounds hold simultaneously. This does not assume a generic structured evaluation matrix or a generality condition uniform in infinitely many parameters.

### Theorem A and nonempty outside centers

The upper bound dim B_Z <= D-r follows directly from incidence, and is negative when r>D. Nonemptiness in the remaining range needs a different argument and is supplied correctly.

The projective image K of B_d in the space of forms has dimension D. Indeed a cone over a smooth degree-d hypersurface has a unique singular point, its vertex. For n=2 this is the union of d distinct concurrent lines, which also has just that singular point. Every degree-d cone vertex is singular for d>=2; hence one fiber of B_d to K is zero-dimensional. Since B_d is irreducible and the map is projective, the generic fiber is zero-dimensional. Thus dim K=D.

The conditions of passing through each original point are genuine hyperplanes in the ambient projective space of forms. Any projective variety of dimension D meets any r hyperplanes nontrivially for r<=D, with dimension at least D-r. No general-hyperplane assumption is needed. Pullback gives dim B_Z >= D-r.

Centers equal to an original point cannot exhaust this incidence: fixing z_i=P gives universal dimension D+(r-1)(n-1), hence general fiber dimension at most D-r-(n-1). This is strictly smaller than D-r for n>=2, including the endpoint where D-r=0 and the boundary is empty. There are only r such boundary conditions. Consequently an outside center exists. The determinantal lower bound D-r and incidence upper bound D-r then agree for the center locus. Taking closure preserves dimension.

The restrictions n>=2 and d>=2 are substantive. For n=1 a marked cone through the sole point can have only the excluded center. For d=1 a hyperplane has an entire hyperplane of vertices, and dim K is n rather than 2n-1. Those cases are treated separately in the proof.

### Theorem B and the factor strata

At r=N-1, jumping means a kernel of vector dimension at least two. It is therefore covered by the incidence of two-dimensional vector subspaces of the cone space. For coprime pencils, the parameter dimension is n+2(N-2). Two coprime homogeneous polynomials in n>=3 variables form a height-two ideal: no height-one prime contains both, and the ideal is generated by two elements. Its projective zero set has dimension n-3, and its affine cone viewed inside Pn has dimension n-2. The general-configuration parameter fiber thus has dimension at most n+2N-4-2(N-1)=n-2.

A pencil with common divisor has a unique gcd up to scale, of degree e between 1 and d-1. After dividing by it, the residual degree-f pencil is coprime. The relative parameter space of [G] and the residual pencil has dimension n+N_e+2N_f-5. Multiplication is injective on a residual pencil for fixed nonzero G, so this parameter count does not undercount it. Repeated factors and reducibility of G are included.

Every base point is on G=0 or on the residual codimension-two cone. Label the indices lying on G by S, with size s; allowing overlap only enlarges the covering incidence. For fixed e,S the dimension of its general-configuration fiber is at most

n+N_e+2N_f-2N-3+s.

Crucially, the lower-degree cone bound already established simultaneously for every subset implies s<=n+N_e-1. This bound applies to the original points on the factor cone, regardless of collisions in their projections. It is therefore legitimate even though G and the center depend on the tuple. The resulting bound is

2n-4-2(N-N_e-N_f).

Discrete convexity gives N_e+N_f<=N_1+N_(d-1), so N-N_e-N_f >= binomial(d+n-2,n-2)-n >= n(n-3)/2. For n>=4 the parameter-fiber bound is at most -(n-1)(n-4), hence at most zero. For n=3 the exact gap is ef-1, yielding 4-2ef<=0 when d>=3.

At n=3,d=2, the coarse expression is 2, which would not prove the target dimension one. The final proof correctly replaces the coarse occupancy bound by s<=3, since four general points do not lie in a plane. Substitution into the uncombined expression gives s-3<=0. This is essential, not cosmetic.

Thus every gcd stratum has a zero-dimensional or empty general parameter fiber, and the coprime stratum has dimension at most n-2. Images and closures of these finitely many constructible strata have no larger dimension. No guessed dimension of the set of pencils over a fixed center is subtracted. Secant lines provide nonemptiness, and the maximal-minor codimension bound two provides dimension at least n-2. Both halves match.

The optional local Schur-complement lower-bound explanation is also consistent: at a general point on a fixed secant, the N-2 distinct projected points impose independent conditions, so an invertible rank-(N-2) block leaves two local equations. The general determinantal argument already suffices without this optional explanation.

### Monotonicity and the edge regimes

Adding r'-r conditions reduces a kernel by at most r'-r. When r<=r'<=N, a jump for Z away from Z' remains a jump for Z'. The qualified closure inclusion W(Z) contained in W(Z') union Z' is correct and handles newly excluded centers. A general small tuple can be extended to an appropriate general large tuple because projection of a nonempty configuration open contains a nonempty open. In P3 the upper dimension one from r'=N-1 and the secant lower bound yield the full subcritical range. In higher dimension this only yields the bound n-2 and does not supply equality throughout the residual range.

For small cardinality, the products of separating linear forms prove independence for any m<=d+1 distinct projected points. Thus a jump is precisely a projected collision, equivalent to a secant center. In P2, the target is P1 and the kernel is max(d+1-m,0). The finite general-position exclusions prevent three original collinear points and concurrency of three secants away from Z. A triple concurrence away from Z would use six distinct endpoints, and its determinant condition is proper. Consequently at most two collisions occur; at r=d+2 the distinct double collisions give exactly three pairings per four endpoints. The P1 and d=1 calculations also account correctly for the removed single-point center.

## Exact tests and attempted failure cases

The historical independent verification used a separate implementation. Its aggregate match results and mathematical failure cases are recorded below. Programs, generated certificates and raw results are not distributed; none is a premise of the universal proof.

- It rederives seven projective-line avoidance certificates for (n,d)=(3,2),(3,3),(3,4),(3,5),(4,2),(4,3),(5,2). Each uses gcd one over F_1009 and an explicit full-rank point at infinity. Further evaluation points check interpolation.
- It verifies 34,300 triples with 3<=n<=30, 2<=d<=50 and every 1<=e<d, including the sharp exceptional handling.
- For the five-point projective frame in P3 over Q, it computes the quadratic derivative matrix, its maximal-minor Groebner basis, and initial-ideal height two, giving projective dimension one. All ten secants are checked by symbolic substitution. Every linearly general five-point tuple in P3 is projectively equivalent to this frame.
- Planted common polynomial factors are detected. Homogenizing the same affine polynomials to one degree higher exposes a shared point at infinity, showing why affine gcd alone is insufficient.
- The incorrect coarse treatment of n=3,d=2 yields upper bound two instead of one. Omitting the factor occupancy restriction yields bound 16 in the n=3,d=6,e=1 adverse case, so that missing step is detected.
- The n=3,d=2,r=1 example has generic outside kernel dimension five everywhere, but kernel dimension six at Z. This exposes both the mistake of equating existence with jumping below N and the mistake of including excluded centers.
- The n=3,d=2,r=4 example has secant curves while an unstructured rectangular-matrix prediction gives dimension zero. This exposes the forbidden generic-matrix shortcut.

These checks supplement the uniform proof, and are not evidence that finite sampling settles an infinite parameter family. The finite-field witnesses do lift to characteristic-zero opens because pivot nonvanishing, coprimeness and the infinity test are algebraic nonvanishing conditions. None computes the general scheme's degree or decomposition.

## Primary source verification and the reading correction

The original OWR definition and Question 1 were independently checked at printed pages 3102-3103. The all-parameter target is the dimension of the outside-Z jumping-locus closure. The neighboring Question 2 has a different target and is outside this audit. Source: Luca Chiantini, Generalized Weddle loci, OWR 54/2022, https://ems.press/content/serial-article-files/46990 and https://doi.org/10.4171/owr/2022/54.

The primary arXiv landing page for Weddle schemes lists v1 dated 23 June 2026. Its Theorem 3.2 uses ambient P(n+1); reindexing is necessary for the present Pn notation. The abstract is not used as a formula. Proposition 5.3 is conditional on codimension two, and Conjecture 5.4 remains presented as a conjecture. The audit does not rely on the point-deletion assertion in Theorem 5.1 or on any conditional scheme-degree formula. Source: Chiantini et al., https://arxiv.org/abs/2606.25060v1 and https://arxiv.org/html/2606.25060v1.

An earlier authored reading of Conjecture 5.4 as an expected-dimension claim was unsupported and has been corrected. Original-resolution visual inspection and OCR of both retained page images, PDF text extraction, a fresh source-bound rendering and the primary HTML all agree: the wording is “expected codimension, namely 2.” A same-resolution rerender was byte-for-byte identical to the earlier retained image. The source PDF is 807,915 bytes, SHA-256 `ef9525e7d7b7b1eb45b8a44b5b34384ddd8f7bb876fb74fc5d33cfe8ece0c5a3`. There is no supported image/PDF discrepancy, source change, or current typo allegation. This corrects the authored source reading and does not alter the mathematics.

## Publication boundary and limits

This proof-only edition includes the complete universal proof, substantive mathematical audit, scoped acceptance and public source metadata. Historical exact finite checks are supplementary; acceptance does not depend on omitted software or certificates. Programs, raw outputs, generated certificates, datasets, copied source documents, source text, source images and private coordination material are excluded. No degree, entire-scheme, ACM, irreducibility, full component or novelty conclusion is added. The general all-parameter problem remains unresolved by this work.
