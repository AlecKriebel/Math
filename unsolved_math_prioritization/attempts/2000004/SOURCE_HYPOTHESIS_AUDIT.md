# Source and hypothesis audit for Ball Problem 4

## Review status of this edition

This AI-assisted mathematical exposition and independent internal AI source/proof audit are unrefereed. Bounded acceptance here does not mean external human peer review, journal acceptance of these authored documents, or formal proof-assistant certification. The AKM result is prior published work; no novelty is claimed. Deep cited existence, finite-distortion, change-of-variables and topological dependencies remain external. No author was contacted.

## Audit decision

Accept an attributed prior result in the exact two-component Ciarlet–Nečas setting, with the two-dimensional strict range 1<q<p/(p−2) and the three-dimensional range 3<p<4, 2<q<p/(p−2). Preserve two independent qualifications: the printed two-dimensional endpoint competitor fails its determinant-integrability requirement; and a connected reference body with only boundary constraints is not supplied by the written examples. This conclusion neither awards a new solution nor proves that every stronger formulation remains open in all literature.

## Ball's controlling formulation

Ball's author manuscript is 44 PDF pages. The surrounding setup, rather than the isolated sentence of Problem 4, determines what can be attributed to it.

1. PDF page 2, Section 2.1: the reference body is a bounded domain Omega in R^3 with Lipschitz boundary. The boundary is split into disjoint relatively open prescribed-displacement and free portions, apart from a surface-null remainder. Deformations begin in W^{1,1}; y equals a prescribed displacement on the first portion. The material is homogeneous, so the internal energy has integrand W(Dy) with no x-dependence. W is C^1 on positive-determinant matrices and bounded below. No body force or nonzero traction is needed in the model discussed there.
2. PDF page 3, (2.7)–(2.9): W tends to infinity as det F tends to zero from above and is extended by infinity on det F<=0. Thus finite energy enforces a positive Jacobian almost everywhere, but Ball expressly distinguishes this from local or global invertibility. Frame indifference is part of the elastic setup. Isotropy is an optional extra property, satisfied by the later example.
3. PDF page 4: Ball's base finite-energy class includes the trace condition, and he states that invertibility may be imposed in different ways. His displayed global-existence theorem assumes polyconvexity and |F|^2+|cof F|^{3/2} coercivity; the surrounding Problem 4 is not a claim that those lower-growth hypotheses alone force continuity. The AKM choice with p>3 is stronger and satisfies this coercivity, because |cof F|^{3/2} is controlled by a constant multiple of |F|^3.
4. PDF pages 7–8: cavitation illustrates an earlier gap involving a discontinuous minimizer. Ball then gives p>3 growth as a sufficient continuity mechanism, while discussing a further borderline p=3 result. The present audit uses only the unambiguous supercritical condition p>d and makes no borderline claim.
5. PDF pages 8–9, Problem 4 and the paragraph after it: the question concerns elasticity with continuity-forcing energy growth. Ball already knew the one-dimensional Ball–Mizel phenomena and the two-dimensional Foss–Hrusa–Mizel sector/container examples. The latter add a global image-container restriction. He explicitly distinguishes the unsupplied mixed-boundary version of type (2.1), even in two dimensions, and an interior-singularity mechanism.
6. PDF page 16, Section 2.5: Ball explicitly discusses the Ciarlet–Nečas integral constraint together with the same mixed displacement condition, almost-everywhere injectivity, and self-contact. Thus CN is a relevant elasticity formulation within the article, but the precise choice must be stated. It cannot be swapped for full injectivity or omitted without changing the variational problem.

The word “domain” normally denotes an open connected set. Ball does not separately analyze disconnected bodies at Problem 4. The AKM introduction instead deliberately uses “open bounded set,” and Section 2 states that its examples have two components. A scope-sensitive attribution must preserve this difference rather than settle it by terminology alone.

## Why the older one-dimensional rationale does not settle this target

Ball–Mizel's one-dimensional examples concern integrals depending on x, y and y'. Their continuous singular minimizers motivate Ball's elasticity question. They are not, just by citation, a three-dimensional homogeneous frame-indifferent energy with the prescribed boundary and admissibility conditions. A bar reduction would need to establish the lifted energy, determinant penalty, growth, admissible class and comparison of the relevant infima. Citation of the one-dimensional examples alone does not supply such a reduction. Moreover, failure of the weak Euler–Lagrange equation is not a definition of a Lavrentiev gap; the strict comparison of infima must be established separately.

An unqualified “solved by Ball–Mizel” conclusion is therefore rejected. The later AKM result is accepted on its own precise terms, without validating an unspecified elastic-bar reduction.

## AKM hypotheses checked against the claims

### Energy and continuity

Equations (2.1)–(2.2), Proposition 2.1 and (2.7) occur on arXiv pages 4–6 / publisher pages 3–5. Convexity of F -> |F|^p and of t -> t^(−q) on t>0, with the infinity extension on t<=0, gives polyconvexity in the minors. The determinant singularity and p-growth are both indispensable to the construction's energy estimates. The calibration gamma=p d^(p/2−1)/q makes rotations minimizers and allows the nonnegative normalization W−W(I). It is not an arbitrary positive coefficient when using the printed normalization and Taylor estimates.

The p>d assumption supplies a continuous representative by Sobolev embedding on each Lipschitz component. The fixed finite positive distance between components poses no continuity issue for the union. It excludes cavitation-type discontinuity in the admissible class. A p=2 neo-Hookean result in d=3 would not supply this hypothesis.

### Admissibility and self-contact

The class Y_s explicitly has all four ingredients: W^{1,p}, positive Jacobian almost everywhere, the same partial trace, and CN. A finite-energy competitor is continuous and almost everywhere one-to-one. Its exceptional collapsed material cross-sections are allowed by CN because they have zero reference volume and their image has zero volume. The energy is nevertheless integrable only if the rate of collapse satisfies the strict exponent inequalities.

ArXiv pages 2–4 / publisher pages 1–3 discuss this difference from everywhere-injective maps and warn that the deep contact may lack a physical interpretation. These warnings are material qualifications, not an invitation to relabel the example a homeomorphism. The energy gap is specifically between Y_s and its Lipschitz subclass. “Smooth” without a boundary-regularity convention is less precise, because a function smooth only in the interior need not be globally Lipschitz.

CN cannot be omitted in this example. The trace extension y_0 consisting of two translations has gradient I everywhere and normalized energy zero; it is Lipschitz on the separated reference components. Its overlapping image violates CN. Enlarging both comparison classes by removing CN therefore makes both infima zero here.

### Actual geometry and boundary data

Theorem 3.2 uses two separated planar strips, equation (3.1), arXiv p.7 / publisher pp.5–6. Theorem 4.1 uses two separated three-dimensional cuboids, equation (4.1), arXiv p.15 / publisher p.12. These are not merely disconnected pieces of a connected ambient material. Their union is the entire reference set over which the energy is integrated.

On each component only its two longitudinal end edges/faces are prescribed. The translations make the preferred whole-component images cross, and the noninterpenetration constraint creates the obstruction. The rest of the boundary is free. No additional image-container requirement occurs in the printed Y_s. The prescribed boundary sets meet the free sets along lower-dimensional edges; changing whether those edges are included does not change the Sobolev trace condition.

The singularity is inside the reference components: the low-energy maps collapse the central transverse section of each. In 2D the collapsed sets are line segments and their common image is a point; in 3D they are planar rectangles and their common image is a line. This is materially closer to the mixed-boundary/interior mechanism sought by Ball than the earlier sector-tip container examples, while retaining the disconnected-set and CN qualifications.

## Dependency trace for the strict-range gap

### Existence and coercivity

Proposition 2.2 quantitatively controls deviation of the operator norm from one. Its proof uses the positive-definite Hessian of the energy in singular values and integrates along the segment to (1,...,1). Theorem 2.3 then invokes Ciarlet–Nečas [AKM reference 13, Theorem 5] to obtain a minimizer once Y_s is nonempty and its energy infimum is finite. These premises are supplied by the explicit competitors. The existence theorem is relied on as an external established result; it was not independently reproved in this audit.

### Low-energy construction

For the central part of the first planar strip the power-law map is

(x_1,x_2) -> (sign(x_1)|x_1|^alpha, |x_1|^beta x_2/s^beta),

and outside |x_1|<=s it is connected affinely in the first coordinate to the endpoint datum, leaving x_2 fixed. The second strip uses the rotated translated copy. Choose

1−1/p < alpha < beta < 1, and q(alpha+beta−1)<1.

The three derivative/determinant integrability tests are p(alpha−1)>−1, p(beta−1)>−1, and q(1−alpha−beta)>−1. Such a choice exists exactly within the subcritical bound relevant here. The determinant is positive away from the collapsed section. For sufficiently small s, the two noncollapsed images lie in separated horizontal/vertical cones and meet only at the collapsed point. CN follows from almost-everywhere injectivity and the change-of-variables formula.

The normalized energy is bounded by a constant times

s^[p alpha−p+2] + s^2 + s^[2+(1−alpha)q] + s^[1+2alpha],

where every exponent is strictly greater than one. The outer affine part has energy O(s^[1+2alpha]) because DW(I)=0. This gives o(s).

In d=3, keep x_1 unchanged and apply the same squeeze to (x_2,x_3), with the rotated copy on the second cuboid. The extra fixed-length x_1 direction only multiplies the estimates by a constant and adds a harmless derivative entry. The plane-to-line collapse preserves almost-everywhere injectivity. Proposition 4.2 therefore uses the strict power-law case, not the disputed logarithmic endpoint.

### Why regular maps cannot use that construction

For finite-energy Lipschitz maps, J^(−q) is integrable and |gradient y| is bounded, hence K_y=|gradient y|^d/J is in L^q. Because q>d−1, the finite-distortion theorem cited as AKM reference 30 implies that each nonconstant component is open and discrete. Positive J and CN then force injectivity on the whole union. The normalized-energy estimate needs the additive W(I)|Omega_s| term, as recorded in ENDPOINT_AND_PROOF_NOTES.md; integrability is unchanged.

The external finite-distortion theorem is not independently reconstructed here. The audit checks that its stated integrability, positivity, Sobolev and nonconstancy hypotheses are supplied, and records its precise role. The area formula and openness explanation show why almost-everywhere injectivity is enough for these Lipschitz maps, but not for the singular low-energy maps.

### Two-dimensional lower bound

Proposition 3.4 uses planar separation and the imposed four ends: for each transverse parameter one of the two image curves must make a detour, with length at least 2 sqrt(2)(1−s). Since that exceeds the direct endpoint distance 2 for small s, Proposition 2.2 and the integrated positive-part/Hölder estimate give a uniform energy cost on a set of total width 2s. A simple sheared detour competitor provides the matching O(s) upper bound. The detailed local normalization and pointwise-inequality clarifications are in the companion proof note.

### Three-dimensional lower bound

Proposition 4.3 is not merely the planar lower bound times an interval: curves have more room in three dimensions. It uses the following additional argument, arXiv pp.18–22 / publisher pp.15–19.

- A finite-energy Lipschitz competitor above an (M+1)s threshold already has the required lower bound. For a competitor below it, Markov's inequality leaves a shared set of transverse slices of measure at least (18/10)s with slice energies at most a fixed N.
- On these two-dimensional slices, Morrey's embedding gives a uniform Hölder bound with exponent gamma=1−2/p. The fixed end faces give nonnegative line-length excess.
- If the L^p-in-x_1 integral of that excess is small, a good-lines/bad-lines argument makes the entire sheet uniformly close to the corresponding straight strip, with error C epsilon^[gamma/(p+1)]. For 3<p<4, gamma<1/2, which accommodates the square-root curve-length deviation. The elementary curve-length estimates cover both axial projections inside and outside the endpoint segment.
- If both crossing sheets were so close, define g(x_1,tau_1,tau_2)=y(x_1,tau_1,sigma)−y(0,sigma+4,−tau_2). The boundary traces and the closeness estimates give opposite strict signs on each pair of cube faces. Poincaré–Miranda (equivalently topological degree) forces a zero in the interior, contradicting injectivity of the Lipschitz map.
- Thus at least one slice has a definite line-excess integral. Proposition 2.2 plus the corrected integrated positive-part estimate converts it to a positive energy per good slice. Integrating gives m s. A three-dimensional detour competitor has energy at most M s for small s.

The mechanism and all exponent interfaces are therefore traceable through the source. The accepted statement relies on this established architecture with the explicitly recorded elementary clarifications, not on a claim that the entire chain of deep theorems was independently reproved.

## The exact remaining connected-domain interface

Remark 3.1, arXiv pp.7–8 / publisher p.6, sketches adding a connector from one prescribed end of S_1 to a prescribed end of S_2. It expressly leaves extra behavior and minimum energy on that connector to be controlled. Its further obstacle suggestion is more speculative still.

A completed connected boundary-only extension would need all of the following, none established by this remark alone:

1. An actual bounded connected Lipschitz reference domain, including junction neighborhoods, with a specified boundary/free split. Touching closures without opening the interfaces does not make the union an open connected reference body.
2. Trace-compatible extensions of both the singular low-energy competitor and at least one Lipschitz competitor, with positive Jacobian and CN across the whole connector and the old components, not merely on each piece separately.
3. Quantitative control of the connector energy sufficient to preserve a strict difference. If a connector imposes a common leading contribution, it must be compared on both variational classes; an unspecified added O(s) cost can overwhelm the known m s separation.
4. A lower-bound argument for every regular competitor on the enlarged geometry. Removing previously prescribed faces can change the endpoint obstruction. Retaining the old faces after filling them in imposes interior data rather than only boundary data of Ball's type (2.1).
5. If an obstacle replaces the internal constraints, a precise new variational problem and proof that it still answers the selected formulation. An obstacle restriction cannot be treated as an absent container restriction by renaming it.

No connected construction or connector estimates are supplied by this audit. The connected boundary-only scope is not settled by this cited result as inspected.

## Bounded later-source crosscheck

A paper dated 24 March 2026 by Barchiesi, Henao, Mora-Corral and Rodiac, A Lavrentiev phenomenon in the neo-Hookean model, describes AKM's disconnected self-contact configuration in its introduction. Its own main result uses p=2 in three dimensions and a gap involving a weak H^1 closure, so it does not supply the missing continuity-forcing connected formulation. Only its introduction and statement interface were inspected; no acceptance of its full proof is intended. https://cvgmt.sns.it/media/doc/paper/7610/Lavrentiev.pdf

## References

- Ball manuscript: https://people.maths.ox.ac.uk/ball/Articles%20in%20Conference%20Proceedings%20and%20Books/JMB%202002%20re%20Marsden%2060th.pdf
- AKM arXiv v2: https://arxiv.org/abs/2309.08288v2
- AKM publisher article: https://doi.org/10.1007/s00033-023-02132-4
- AKM publisher PDF: https://link.springer.com/content/pdf/10.1007/s00033-023-02132-4.pdf
