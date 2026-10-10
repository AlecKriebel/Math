# Independent full mathematical audit: three-dimensional dihedral comparison

Date: 2026-10-08. Target: 30003471 / OWR-15427-013, rank 999.

## Verdict

**Accept the mathematical argument in the frozen candidate. No blocking gap and no required mathematical correction were found.**

The proof establishes its advertised strengthening: for compact full-dimensional convex three-dimensional polytopes with a fixed face-lattice correspondence, weak inequality of every corresponding interior dihedral angle forces equality of the complete corresponding facet-normal Gram matrices. It therefore implies the exact original one-edge weak-comparison question. The audit includes nonsimple vertices and arbitrary combinatorial equivalence; it does not replace either hypothesis by smooth equivalence of corners.

This is a mathematical audit relative to the explicitly imported smooth-domain Dirac results and the standard functional-analytic foundations. It is not a formal proof certificate, journal acceptance, a novelty determination, or an audit of the complete recent Wang-Xie-Yu manuscript. Computations are supplementary diagnostics only.

The audit was carried out independently of other reviews. The complete frozen candidate was read, the specialized analytic input was inspected directly in the primary-source manuscript, and every geometric, topological, limiting, and algebraic link was checked. Neither the frozen packet nor the reference files were changed.

## Frozen inputs

- `PROOF.md`: 21,855 bytes; SHA-256 `6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415`.
- `MANIFEST.json`: 1,252 bytes; SHA-256 `1cd8291f2025524b351c5cc3cb5780b35ba5fa4c4afde78c6e288daddd350e9f`.
- The packet verifier passed in normal and optimized Python modes. In each mode it checked nine files, replayed 5,066 finite diagnostics, rejected 19 negative-control mutations, and passed its read-only relocation test.
- A separate, newly written diagnostic program passed 4,146 checks in normal and optimized modes, producing byte-identical results. It does not import the candidate's diagnostic program.
- All nine locally available reference PDFs matched their recorded byte counts and SHA-256 pins. This is provenance verification, not proof verification.

## 1. Exact scope and logical target

The OWR report, printed page 1198, question 4, asks about corresponding edges of combinatorially equivalent convex polytopes in three-space. Akopyan-Karasev's Conjecture 5.1 states the analogous ridge comparison in arbitrary dimension. The candidate correctly proves only the three-dimensional case, while stating a stronger conclusion within that dimension.

The initial logical reduction is correct. If every source interior angle were strictly larger than its target counterpart, reversing the two polytopes would satisfy the candidate's weak comparison hypothesis. Its equality conclusion then contradicts strictness. The original report's alternative allowing equality of all angles adds nothing to the requested existence of one weak inequality.

Both the orientation repair by reflecting the target and the final conclusion are invariant under an orthogonal change of coordinates. The fixed correspondence is preserved; no relabeling chosen after comparing the angles is being smuggled into the argument.

## 2. Specialized analytic input and matrix convention

The applicable source is Brendle, *Scalar curvature rigidity of convex polytopes*, arXiv:2301.05087v4, Section 2, published bibliographic reference Inventiones Mathematicae 235 (2024), 669-708, DOI 10.1007/s00222-023-01229-x.

I inspected the definitions, boundary identity, trace-norm estimate, energy inequality, Fredholm regularity, and positive-index argument in that section. The existence and regularity propositions require a smooth compact convex domain and a smooth sphere-valued map homotopic to its Euclidean Gauss map. They do not require matching dihedral angles, strict convexity, a map between two polytopes, or a nonsingular extension of the eventual polyhedral correspondence. The matching-angle condition in the paper's separate polytope theorem is irrelevant to these propositions.

In dimension three, the spin module has complex dimension two. In a fixed flat spin frame, write a tuple of spinors as the columns of a matrix A. Let c be its Clifford representation. The tuple coefficient of basis vector beta in c(v) applied to basis vector alpha is c(v)_{beta,alpha}. Consequently the coefficient array acting on the tuple label is transposed relative to ordinary column-vector notation. Inserting this into the source's tuple boundary formula gives exactly

    chi_eta(A) = -c(nu) A c(eta).

There is no additional transpose or adjoint on the final right-hand Clifford matrix. Since c(eta)^2=-I, the positive boundary condition is equivalent to

    c(nu) A = A c(eta).

The source's orientation branch can be represented by c(e_j)=-i sigma_j, for which c(e_1)c(e_2)c(e_3)=-I. The decisive baseline check is that when eta=nu the constant identity matrix satisfies chi(I)=I. On the opposite branch, a constant matrix would have to anticommute with all c(e_j), forcing it to vanish. Thus the candidate uses the positive-index branch, not its opposite. Direct tuple/matrix calculations and exact commutant/anticommutant rank checks independently verified this bookkeeping.

Proposition 2.14 supplies a Fredholm boundary problem and smooth kernel. Proposition 2.15 supplies index at least one, so its kernel is nonzero. With zero scalar curvature and DA=0, Proposition 2.9 gives the stated energy inequality; replacing its signed boundary coefficient by its positive part only weakens the upper bound. The trace norm is indeed the sum of the two singular values of the tangential differential.

No singular polyhedral Dirac domain, self-adjoint extension at a corner, or Wang-Xie-Yu index calculation is used. The general Sobolev, extension, compactness, and homotopy results listed by the candidate remain standard imported foundations, rather than newly proved results.

## 3. Global auxiliary map and nonsimple vertices

The barycentric face construction gives a genuine PL boundary homeomorphism. On a polygonal facet, coning its subdivided boundary to an interior point supplies the relevant triangles; the shared subdivisions agree. Applying the face-lattice isomorphism yields corresponding triangulations and a piecewise affine homeomorphism. Its finite triangulations make it bi-Lipschitz. A target reflection corrects a negative boundary degree without changing any Gram matrix.

After centering both polytopes at interior points, radial projection of the target boundary has positive degree. For every point in a source facet, the image belongs to the corresponding target facet and therefore has strictly positive inner product with that facet's outward normal after radial normalization. The support-number lower bound is uniform over all facets.

At a nonsimple vertex, the same radial vector has positive inner product with every incident target facet normal. This simultaneous hemisphere condition is the important point: the proof never needs a smooth map taking a neighborhood of one nonsimple corner to a neighborhood of the other.

The radial collar extension is Lipschitz. Uniform smooth approximation on a compact subcollar, followed by normalization, preserves both the homotopy class and a fixed positive hemisphere margin. Finiteness of the facets then supplies a common neighborhood size. The auxiliary q is fixed before lambda tends to infinity, so its derivative bound is independent of lambda.

## 4. Smoothing and uniform geometry

The proposed double-integral bump has all required properties: it is smooth and flat at -2, strictly increasing above -2, convex, and can be normalized to have value one at zero. The smoothed sublevel set lies inside the original polytope and contains a common centered ball for all sufficiently large lambda.

The radial pairing argument prevents cancellation in nonnegative combinations of active facet normals. On the level set, after clipping inactive cutoff arguments at -2, the compact set of possible cutoff values has a positive lower bound for the sum of first derivatives. The level gradient is therefore bounded below by a constant times lambda. This proves smoothness of the boundary even where it retains an exactly planar facet patch.

The radial displacement bound follows by shrinking points toward the origin by an amount proportional to lambda^{-1}. Convex bodies between two fixed concentric balls have uniformly positive, uniformly Lipschitz radial functions: their reciprocals are support functions of their polar bodies. The ratio of the original and smoothed radial functions therefore defines a uniformly bi-Lipschitz raywise map and inverse. This remains true when those maps are extended to all of three-space. Smoothness at the origin is unnecessary for Sobolev transport.

Consequently both the bulk H^1 norms and boundary measures transform with uniform bounds. Transporting the fixed-polytope H^1-to-L^4 trace inequality gives precisely the uniform estimate needed later. A fixed Lipschitz-domain extension, combined with the global radial maps, gives H^1 extensions to one common ball. The extension is equal to the original field on its moving domain; no boundary condition is imposed on the extension.

## 5. Active-facet localization, including nonadjacent pairs

The finite-dimensional nearest-point argument in equation (4.3) is valid. At a projection point onto an intersection of facets, the normal cone is the span of the equality normals plus the nonnegative cone of the remaining active inequality normals. The displacement toward a point in the polytope satisfies those remaining inequalities. A limiting unit displacement annihilating all equality normals would have nonpositive inner product with its own normal-cone representation, contradicting its unit norm. There are finitely many face types, and the cones are closed polyhedral cones, so a uniform positive bound follows.

For an empty facet intersection, compactness gives a positive lower bound on the maximum violation of the corresponding equality conditions. Since only finitely many facet subsets occur, such subsets cannot be active for sufficiently large lambda.

In dimension three, an actual edge has exactly two incident facets. Thus an active set with at least three facets is within O(lambda^{-1}) of a vertex, even if that vertex has arbitrarily many incident facets. A pair of nonadjacent facets having a vertex as its intersection is also localized to that vertex. The candidate expressly handles that pair case; it does not mistake every two-facet intersection for an edge.

As a diagnostic of the nonsimple case, the independent controls used the regular octahedron, with four incident facets at every vertex. Among 396 actual smoothed-boundary samples at three lambda values, 209 had at least three active facets. The measured maximum lambda times vertex distance was below 3.908. These finite samples are consistent checks, not the justification of the general localization theorem.

## 6. Exact edge contraction and smooth compatibility

The angle direction is correct: weakly smaller source interior angles mean weakly larger source exterior-normal angles, so beta<=alpha. Both exterior angles are strictly between zero and pi for distinct adjacent actual facets.

On a two-active chart, the source normal lies on the minor great-circle arc between its two facet normals. The edge direction annihilates both defining functions, so the smoothed surface has a zero principal curvature in that direction. Its other principal curvature is nonnegative. Thus the differential of the Gauss map has trace norm equal to mean curvature and rank at most one.

Transporting fractional arclength between the two normal arcs multiplies the only possible nonzero singular value by beta/alpha. It is essential that the construction uses fractional arclength, rather than the same normalized linear endpoint weights: the latter can expand even when beta<alpha. An independent negative control exhibits that distinction. The candidate uses the correct construction.

At a two-active to one-active transition, the disappearing cutoff weight and all of its derivatives vanish. A local atan2 coordinate for the source arc is smooth at its endpoint. Its composition with the target arc therefore glues with the constant facet value to all orders. Distinct two-active charts cannot require incompatible definitions outside the excluded vertex region. No derivative of arccos at one is required.

The target minor-arc interpolation is a positive sine-weighted combination of its endpoints. The sum of its coefficients is at least one. Since q has the same positive lower pairing with each endpoint, its pairing with every interpolated value retains that margin. The needed hemisphere is uniform in lambda and over the finitely many edges.

## 7. Spherical interpolation while q varies

This step is sound and does not silently freeze q during spatial differentiation. For theta=dist(q,z)<pi/2, the endpoint differential in z has singular values

    t,  sin(t theta)/sin(theta).

Both are at most one. The apparent quotient singularity at theta=0 is removable, with limit t. In fact, by reversing the interpolating geodesic, the q-endpoint differential has singular values

    1-t,  sin((1-t) theta)/sin(theta),

so it too has operator norm at most one in this hemisphere. The candidate only requires its weaker uniform bound. The parameter derivative has norm theta.

The chain rule therefore gives

    ||d eta||_tr <= ||d zeta||_tr + ||d q||_tr + theta |dt|.

For the last term, the differential has rank at most one. The middle term is uniformly bounded because q was fixed in advance. This proves the claimed pointwise error bound. Outside a hemisphere the first endpoint derivative need not be contractive; an independent negative control verifies that the hemisphere assumption is substantive.

The logarithmic cutoff is flat at both endpoints. Its inner radius delta^2=lambda^{-1/2} is asymptotically much larger than the O(lambda^{-1}) exceptional region. Thus zeta exists wherever its derivatives enter the interpolation. Inside the exceptional cap eta is just q. These facts establish global smoothness, rather than merely piecewise regularity.

## 8. Critical boundary norm and absorption

The boundary error is supported in the delta-neighborhoods of finitely many vertices and is bounded by a constant plus the annular weight 1/(r |log delta|). Pulling back by the radial boundary map changes r by O(lambda^{-1}), which is o(delta^2). On its annular support the original and pulled-back radii are therefore uniformly comparable.

For small enough delta, only source facets incident to the chosen vertex contribute. On each such planar facet, the squared annular weight is bounded by the full planar polar integral. With ideal radii delta^2 and delta, that integral is exactly

    2 pi / |log delta|.

Fixed multiplicative enlargements of the annulus do not affect convergence to zero. The boundary Jacobians are uniformly bounded, and the squared L2 norm of the constant indicator contribution is O(delta^2). This yields the stated

    ||W_lambda||_L2 <= C(delta + |log delta|^{-1/2}) -> 0.

In particular this is a norm on the moving, genuinely smoothed boundary, not an estimate only on the limiting facets. The radial comparison closes that possible gap.

Holder pairs W in L2 with |A|^2 in L2, and the uniform H^1-to-L^4 trace estimate supplies the latter. There is no loss of an exponent and no use of an L-infinity spinor estimate. Hence the boundary quadratic form is bounded by a vanishing coefficient times the H^1 bulk norm. This is exactly what the energy absorption requires. Merely using a cutoff of width proportional to delta would not make its analogous planar L2 gradient norm vanish; the logarithmic scale is doing real work.

## 9. Degree and applicability of the index result

The positive pairing q dot eta allows normalized straight interpolation globally between eta and q, including the inner caps where they already agree. Equivalently, the geodesic interpolation supplies the homotopy. The auxiliary q has degree one on the smoothed boundary because its collar homotopy identifies it with the PL correspondence followed by target radial projection; the radial identification of the source boundaries preserves orientation.

Every smoothed boundary surrounds the same centered ball. Its supporting plane therefore gives nu dot x>0. Its Gauss map is homotopic to its radial map, even though it has flat patches, and has degree one. The smooth boundary is a sphere, so equality of degrees gives the required homotopy to the Gauss map.

Thus all hypotheses of the smooth-domain existence theorem hold for each sufficiently large lambda. No uniform elliptic regularity constant for the changing boundary is claimed or needed: existence and smoothness are used separately on each domain; uniformity comes instead from the energy, radial extension, and trace estimates already proved.

## 10. Constant limit, no escaped mass, and facet traces

Normalize the nonzero kernel matrix by its bulk L2 norm. The energy estimate and vanishing boundary form give

    E_lambda <= a_lambda(E_lambda+1),  a_lambda -> 0.

For a_lambda<1, this implies E_lambda<=a_lambda/(1-a_lambda), hence E_lambda->0. The uniform extensions are H^1-bounded on a fixed ball, so a subsequence converges strongly in L2 there. Every compact subset of the polytope interior eventually lies inside every moving domain. Testing derivatives on these subsets shows that the limit is constant on the connected interior.

The normalization cannot escape into a collapsing layer. Strong L2 convergence implies convergence of squared norms in L1. The characteristic functions of the moving domains converge almost everywhere to that of P. Combining these two facts gives exactly

    1 = vol(P) |C|^2.

This is a valid moving-domain argument; no unproved uniform integrability assertion is being substituted for it.

For each individual facet, choose a compact interior patch. Every other defining inequality has a uniform negative margin on a neighborhood of that patch. Consequently a fixed half-ball lies in every sufficiently late smoothed domain, and the flat face part of its boundary is unchanged. On this half-ball, strong L2 convergence together with vanishing gradient energy is strong H^1 convergence to C. Its ordinary fixed-domain trace theorem passes the exact boundary intertwining relation to the limit. The construction does not take traces on edges or vertices.

## 11. Algebraic conclusion

The adjoint relation is correct, and C*C commutes with each target Clifford normal. The target facet normals span three-space because the polytope is bounded. Their Clifford images generate the full complex two-by-two matrix algebra. Hence C*C is scalar; positivity and C!=0 imply its scalar is strictly positive, proving invertibility.

Applying two intertwining relations in opposite orders and adding gives the equality of the two Clifford anticommutators. Each anticommutator is a scalar matrix determined by the corresponding Euclidean dot product, so cancellation yields equality of every pairwise facet-normal dot product, including nonadjacent facets.

As a harmless simplification, invertibility is stronger than needed for this final scalar equality: a scalar multiple of a nonzero matrix cannot vanish unless the scalar is zero. The candidate's invertibility argument is nevertheless correct and supplies additional useful structure.

## Nonblocking presentation suggestions

No change is required for mathematical validity. Two optional clarifications may help readers:

1. Include the explicit tuple coefficient-to-column-matrix conversion given in Section 2 of this audit, to prevent a mistaken right-side transpose or opposite boundary branch.
2. The q-derivative in spherical interpolation can be bounded by one by reversing the geodesic. The current uniform-bound statement is sufficient and correct.

The acceptance is tied to the frozen proof hash above. A later substantive proof change should receive a corresponding delta review. Updating status or recording this audit does not turn the result into formal verification or an externally accepted publication.

## Independent finite diagnostics

`independent_controls.py` exercises the following independently of the candidate's test program:

- exact Clifford anticommutation, skew-adjointness, and odd-dimensional volume;
- exact rank-three commutant and rank-four anticommutant linear systems;
- positive and negative boundary branches on rational unit vectors;
- involution eigenspace dimensions and the boundary principal-symbol anticommutation;
- exact tuple-to-matrix translation, including transposes of coefficient arrays;
- 1,615 edge arclength-contraction samples, including nearly antipodal source endpoints;
- 391 finite-difference checks of the spherical endpoint Jacobi formula and 391 moving-q bounds;
- octahedral nonsimple incidences and 396 actual smooth-boundary samples;
- logarithmic annular integrals and scale separation;
- negative controls for same-weight interpolation, nonhemisphere interpolation, and nonlogarithmic cutoffs;
- all frozen-input and recorded source pins.

Maximum numerical discrepancy in the edge norm calculation was 8.89e-16. The maximum discrepancy between a finite-difference spherical differential and its Jacobi formula was 1.35e-10. These numerical values do not establish the universal statements; the preceding mathematical audit does.

## Public primary-source references and dependency boundary

- Original target: [OWR 19/2017](https://publications.mfo.de/bitstream/handle/mfo/3583/OWR_2017_19.pdf?isAllowed=y&sequence=1), printed page 1198, question 4.
- General-dimensional formulation: [Akopyan-Karasev, arXiv:1505.05263v2](https://arxiv.org/abs/1505.05263v2), Conjecture 5.1.
- Specialized analytic dependency: [Brendle, arXiv:2301.05087v4](https://arxiv.org/abs/2301.05087v4), Section 2, especially Propositions 2.9, 2.14, 2.15; [published bibliographic record](https://doi.org/10.1007/s00222-023-01229-x). The proof text inspected for this audit was the pinned author manuscript, with direct visual checks of printed pages 3, 11, and 12 as well as the Section 2 text.
- Credited smoothing strategy: [Bi, arXiv:2608.06320v1](https://arxiv.org/abs/2608.06320v1). The candidate supplies the needed geometric and limiting arguments rather than invoking Bi's theorem as an unsupported smooth-corner transfer between arbitrary polytopes.
- Relevant but unused recent claim: [Wang-Xie-Yu, arXiv:2606.30130v1](https://arxiv.org/abs/2606.30130v1), Theorem 1.2 and Definition 2.8. Its allowance for maps nonsmooth at vertices was checked. Its complete singular-index proof was not audited or used.
- Version-specific caution: [Bar-Hanke-Schick, arXiv:2202.05180v2](https://arxiv.org/abs/2202.05180v2). The cited criticism concerns a specified older WXY version and does not invalidate the separate smooth-domain input used here.

The report, controls, and result files contain authored audit material and public verification metadata only. No primary-source PDF, copied source exposition, dataset contents, or private coordination material is included.
