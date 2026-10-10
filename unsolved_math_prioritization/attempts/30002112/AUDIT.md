# Independent mathematical audit: additive boundary eigenvalue estimate

## Verdict

**ACCEPT, for the stated class of smooth bounded Euclidean domains without a connected-boundary restriction.** No mathematical correction to the frozen proof is required.

The independently reviewed original proof has SHA-256 `0123ee87f7fe6ee04eed80939015df01e9c36a15bcb576085f30385c18d25ac9`. The distributed PROOF.md changes only its review-status and authored-contribution framing; its entire mathematical argument and source references are unchanged. STATUS.json records original and distributed document identities. The proof's conclusion is stronger than a single-dimensional counterexample: for each fixed integer `m >= 2`, it supplies connected bounded smooth domains in `R^(m+1)` with exactly two boundary components that defeat every proposed finite pair of dimension-only constants in

`lambda_k(boundary Omega) |boundary Omega|^(2/m) <= A_m I(Omega)^(1+2/m) + B_m k^(2/m)`.

Here `I(Omega) = |boundary Omega| / |Omega|^(m/(m+1))`, and eigenvalues include all zero modes and multiplicities, starting at index 1. The conclusion concerns the induced intrinsic Laplace-Beltrami operator. It does not concern Steklov, Dirichlet, Neumann, Robin, or Wentzell eigenvalues.

The verdict is an independent internal AI mathematical review of the argument. The AI-assisted proof and audit are unrefereed; no external human peer review, journal acceptance, formal machine proof, historical novelty or literature-wide priority determination is claimed. Supplementary finite diagnostics described below are not distributed in this prose edition and are not mathematical premises. In particular, it does **not** answer the version that requires the boundary to be connected. Dimension 1 is outside this verdict.

## 1. Exact source scope

The relevant part of Bruno Colbois's Oberwolfach survey starts on printed p. 2034, states Theorem 3 on p. 2035, and asks the additive question on p. 2036. I read that entire talk, including its initial standing context. Theorem 3 concerns bounded Euclidean domains with smooth boundary; neither that statement nor the talk's standing context imposes connectedness on the boundary. The additive question explicitly refers back to Theorem 3. Its isoperimetric exponent is `1 + 2/m`, and the separate index exponent is `2/m`. [OWR]

I also checked the cited Colbois-El Soufi-Girouard paper. Its introduction numbers the complete spectrum starting at 1 with non-strict inequalities. Theorem 1.1 has the same smooth-domain class. Crucially, Example 3.1 uses a boundary with two components and explicitly counts two zero eigenvalues. That example is in a different ambient geometry and is not itself the Euclidean counterexample under review; it verifies that disconnected boundaries and all their zero modes are part of the source's conventions. Calling the second eigenvalue the first positive eigenvalue elsewhere in that paper does not override this explicit example. [CEG]

A connected domain can have disconnected boundary. The proof satisfies domain connectedness independently, so the usual connected meaning of the word "domain" creates no loophole. A separate connected-boundary hypothesis would change the problem and invalidate this particular example; no such strengthened result is asserted.

## 2. Audit of the established geometric input

### 2.1 High normalized first positive eigenvalues

Colbois-Dryden-El Soufi's standing assumption is that the submanifold is compact, connected, and without boundary. Their indexing is `0 = lambda_0 < lambda_1 <= ...`, so their `lambda_1` is the candidate's `lambda_2` on each connected component.

Their Theorem 1.4 has two parts. In dimension 2 it gives embedded orientable surfaces in `R^3` with unbounded first-positive-eigenvalue times area. In dimension at least 3 it gives unbounded normalized first positive eigenvalue on any fixed smooth manifold already embedded in the prescribed Euclidean space. Taking the original manifold to be `S^m` and the codimension to be 1 gives the required hypersurfaces. The theorem therefore covers every dimension used here, rather than only high codimension or a varying ambient dimension. [CDE]

I read the full Section 5 derivation, not only the theorem title. Its higher-dimensional input is the large-eigenvalue-metric theorem of Colbois-Dodziuk. The two-dimensional input uses compact orientable surfaces of increasing genus with a spectral gap bounded below while their area increases. It then applies a codimension-preserving C1 isometric embedding theorem and smooth approximation, whose induced metrics are arbitrarily close in the quadratic-form sense. These are exactly the types of conclusions needed here. The candidate correctly allows varying genus when `m = 2`; it does not incorrectly claim unbounded normalized gap on a fixed topological 2-sphere.

The audit relies on Theorem 1.4 as an established result and checks its hypotheses and stated proof mechanism. It does not purport to reprove the underlying Colbois-Dodziuk or arithmetic-surface theorems.

### 2.2 Small-ball control is separately justified

Unbounded normalized eigenvalues alone do not imply that one can impose area, gap, and containing ball independently. The candidate supplies the missing step with the C0-dense form of Nash-Kuiper, rather than silently assuming that a dilation suffices.

Theorem 1.2 in De Lellis-Szekelyhidi states the C0 approximation property for a smooth closed Riemannian `n`-manifold and a smooth short immersion into `R^N`, with `N >= n + 1`; when the starting map is an embedding, the isometric approximant can also be an embedding. I checked that the codimension-one and embedding clauses occur in the actual theorem. [NK]

For arbitrary `S, L, r > 0`, select a smooth metric `g_0` on a connected hypersurface-embeddable manifold with

`lambda_2(g_0) Vol(g_0)^(2/m) > 2 L S^(2/m)`.

Setting `g = (S/Vol(g_0))^(2/m) g_0` gives `Vol(g) = S` and `lambda_2(g) > 2L`. The scale factors are correct: multiplying a metric by `b^2` multiplies volume by `b^m` and eigenvalues by `b^(-2)`.

Take any smooth embedding `e` of the same manifold into `R^(m+1)`. Compactness gives a finite maximum of `e*Euclidean(v,v)/g(v,v)` over the unit tangent bundle. Thus a sufficiently small dilation of `e` is strictly short for `g`, while its image lies inside `B(0,r/8)`. This uses the existing abstract embedding, not an assumption that the high-gap metric already admits a smooth isometric codimension-one embedding.

Choose Nash-Kuiper's C0 error smaller than `r/8`. The resulting C1 isometric embedding lies in `B(0,r/4)`. This verifies the ball constraint with an actual approximation theorem and a positive margin.

## 3. Smooth approximation and spectral continuity

For a compact source manifold, smooth maps are C1 dense in C1 maps, and embeddings form an open subset of the C1 mapping space. Hence the C1 isometric embedding can be approximated in C1 by smooth embeddings. The local full-rank property persists under C1 perturbation; compactness also prevents distant source points from acquiring coincident images. Thus the smoothing does not turn an embedding into a merely immersed or self-intersecting hypersurface. CDE Section 5 explicitly uses this same smoothing step and cites Hirsch.

The candidate's spectral estimate is valid. If `c^(-1)g <= h <= cg`, then:

- volume densities lie between `c^(-m/2)` and `c^(m/2)` times the original;
- inverse metrics lie between `c^(-1)g^(-1)` and `cg^(-1)`;
- Dirichlet energies lie between `c^(-(1+m/2))` and `c^(1+m/2)` times the original;
- squared L2 norms lie between `c^(-m/2)` and `c^(m/2)` times the original.

Consequently the Rayleigh quotient satisfies

`c^(-(m+1)) R_g(u) <= R_h(u) <= c^(m+1) R_g(u)`.

Uniform positive-definite metric comparison gives the same Sobolev space. Applying min-max over all subspaces gives the same two-sided factor for each numbered eigenvalue, including zeros. No comparison of metric-dependent mean-zero subspaces is required. Uniform convergence of the induced metrics therefore gives volume convergence and convergence of the first positive eigenvalue on this fixed manifold.

Writing `S_j` for the smoothed area, a final ambient dilation by `a_j = (S/S_j)^(1/m)` gives exactly area `S`. Since `a_j -> 1`, it also preserves the strict spectral target for sufficiently large `j`. With the smoothed image in `B(0,r/3)` and eventually `a_j < 2`, the final image remains in `B(0,2r/3)`. Thus the final hypersurface is smooth, embedded, connected, has exact area `S`, has first positive eigenvalue greater than `L`, and lies inside the prescribed ball.

Every choice of smoothing accuracy is made after fixing the desired parameters. Neither the original question nor the proof requires uniform bounds on higher derivatives as the parameters vary. The intermediate C1 object is never used as a final boundary.

## 4. Geometry and connectedness of the resulting domain

Fix `m >= 2` and a positive integer `q`. Apply the verified lemma with area `q`, gap target `T_q = q(q+m-1)`, and containing radius `1/2`. Let the result be `H_q`.

A smooth compact connected embedded codimension-one manifold in Euclidean space separates the complement into its bounded and unbounded components. This is the applicable generalized Jordan-Brouwer separation theorem; the hypersurface need not be a sphere. Let `U_q` be the bounded component and `E_q` the unbounded component. Both have boundary `H_q`.

All of `U_q` is inside `B(0,1/2)`. Indeed, any point on or outside the radius-1/2 sphere can be joined radially to infinity without meeting `H_q`, since `H_q` lies strictly inside that sphere. More strongly, compactness puts `H_q` inside a slightly smaller concentric ball. This disposes of any possible closed-ball/open-ball distinction.

Define `Omega_q = B(0,1) minus closure(U_q)`. Its boundary is exactly the disjoint union of the unit sphere and `H_q`; both pieces are smooth, separated, and connected. There are no accidental extra components.

To verify connectedness rather than infer it from a picture, use `Omega_q = E_q intersection B(0,1)`. The open connected set `E_q` is path connected. For any point within radius `3/4`, a path in `E_q` to a point outside the unit ball has an initial segment ending at its first radius-3/4 crossing. This segment stays within the unit ball and outside the cavity. Points of radius at least `3/4` already lie in the full connected annulus between radii `1/2` and `1`. Every point therefore connects inside `Omega_q` to that same annulus. Knotted or complicated cavity geometry cannot disconnect the constructed domain.

Let `omega_(m+1)` be the unit-ball volume and `rho_m = (m+1) omega_(m+1)` the unit-sphere area. The construction yields

`omega_(m+1) (1 - 2^(-(m+1))) <= |Omega_q| <= omega_(m+1)`

and

`|boundary Omega_q| = q + rho_m`.

The cavity volume can be arbitrarily small without harming this estimate. The lower bound comes from the untouched annulus, not from any lower-volume estimate for a high-gap hypersurface.

## 5. Exact spectral rank

The sphere's eigenvalue at harmonic degree `ell` is `ell(ell+m-1)`. Its multiplicity is

`d_(m,ell) = binom(ell+m,m) - binom(ell+m-2,m)`,

where terms with insufficient upper index vanish. This follows from the harmonic decomposition of homogeneous polynomials in `m+1` variables. The degrees below `q` are precisely the sphere eigenvalues strictly below `T_q`. Telescoping the polynomial-dimension differences gives

`N_q = binom(q+m-1,m) + binom(q+m-2,m)`.

The spectral decomposition on a disjoint union is the direct sum of the component operators. The cavity contributes exactly one eigenvalue strictly below `T_q`, namely its zero, because it is connected and its first positive eigenvalue is greater than `T_q`. Thus exactly `N_q + 1` union eigenvalues lie below `T_q`; the sphere contributes a positive multiplicity at `T_q`. The first occurrence of that value in the 1-based complete spectrum is therefore

`k_q = N_q + 2`, and `lambda_(k_q)(boundary Omega_q) = T_q`.

This counts both zero modes. As a direct edge check, at `q = 1` one has `N_q = 1`, `k_q = 3`, and the third eigenvalue is `m`; the first two are zero. For `m = 2`, the identity specializes to `N_q = q^2` and `k_q = q^2 + 2`.

For `q >= m`, each binomial is at most `(q+m)^m`, so

`k_q <= 2(q+m)^m + 2 <= 2^(m+2) q^m`.

Raising to the positive exponent `2/m` gives `k_q^(2/m) <= 2^(2+4/m) q^2`. The bound is deliberately loose and valid. No uniform Weyl asymptotic over changing metrics or domains is invoked.

## 6. Universal quantifiers and asymptotic contradiction

Put `v_m = omega_(m+1)(1 - 2^(-(m+1))) > 0`. From the area and volume bounds,

`I(Omega_q)^(1+2/m) <= v_m^(-(m+2)/(m+1)) (q+rho_m)^(1+2/m)`.

The exponent on volume is correct because `(m/(m+1))(1+2/m) = (m+2)/(m+1)`.

If finite positive constants `A_m, B_m` satisfied the proposed estimate for this fixed dimension, substitution and division by `q^2(q+rho_m)^(2/m)` would give

`1 <= A_m v_m^(-(m+2)/(m+1)) (q+rho_m)/q^2 + B_m 2^(2+4/m)/(q+rho_m)^(2/m)`.

The first term tends to zero like `1/q`; the second tends to zero like `q^(-2/m)`. This contradicts the displayed lower bound. The dimension is fixed before `q` tends to infinity, so the dimension-dependent constants cause no limit-interchange issue. Restricting to positive constants loses no generality: any bound with finite real constants would also hold after increasing each to a positive one.

The unweighted quotient asserted at the start of the candidate also tends to infinity. Divide its denominator by `q^2(q+rho_m)^(2/m)`; the preceding two positive bounds, with coefficients 1, tend to zero, whereas the normalized numerator is at least 1. This proves divergence along the entire chosen sequence, not merely an unbounded subsequence.

The construction may depend on `m` and `q`, as the universal estimate quantifies over every domain and every index. It need not depend on the allegedly universal constants. It consequently defeats every fixed pair of such constants in every dimension `m >= 2`.

## 7. Adversarial checks and limitations

The following possible failure modes were examined and do not occur:

- using a high-codimension theorem instead of a hypersurface theorem;
- assuming genus can stay fixed in dimension 2;
- confusing a C1 isometric immersion with an embedding;
- obtaining a high-gap metric without controlling the containing ball;
- smoothing in C0 only, which would not control the metric;
- losing exact area or the strict gap during the final rescaling;
- confusing cavity connectedness with connectedness of its exterior inside the ball;
- omitting an inner zero mode or applying connected-spectrum indexing to a disconnected union;
- using a Weyl law uniformly over a varying family;
- fixing `q` before choosing arbitrary constants, or allowing the dimension to drift in the limit;
- treating a previous multiplicative estimate as an additive one;
- treating a retrieved or old preprint as evidence of a new published resolution.

The known multiplicative estimate is consistent with the examples: it retains the product with `k^(2/m)`. Ordinary Weyl asymptotics on any one fixed domain are also consistent, because both the domain and the selected index change with `q` here.

Independent exact-integer diagnostics checked 15,600 dimension/index pairs (`2 <= m <= 40`, `1 <= q <= 400`) and 1,404 intentionally wrong first-rank variants. They also checked the rational scaling and volume exponents. The same diagnostics passed with Python optimization disabled, enabled, and doubled. These finite calculations are only error-detection aids; the universal proof is the argument above and its established geometric inputs. No numerical embedding, spectral solver, or finite test is represented as proving the existence of the hypersurfaces or the infinite limit.

No proof patch is required. The conclusion should continue to carry the two-component-boundary scope and the disclaimer about priority and connected boundaries.

## 8. Sources and inspection

All four public PDF sources were independently retrieved on 2026-10-10 and matched the frozen proof package's PDF hashes and byte counts exactly. The inspected content included the complete OWR talk, CDE's full Section 5, and the exact Nash-Kuiper theorem and neighboring explanation. Ten decisive PDF pages were also independently rendered and visually examined: OWR 22-24 (printed 2034-2036), CDE 6 and 14-15, CEG 1-2 and 14, and De Lellis-Szekelyhidi 4. Source metadata records the public URLs, byte counts, and hashes. Source copies, extracts, and rendered pages are not part of the authored public mathematical report.

[OWR] B. Colbois, "Upper bounds for the spectrum of Riemannian manifolds," in *Geometric Aspects of Spectral Theory*, Oberwolfach Report 33/2012, printed pp. 2034-2036. [Report DOI](https://doi.org/10.4171/owr/2012/33); [official full report](https://ems.press/content/serial-article-files/46403).

[CDE] B. Colbois, E. B. Dryden, A. El Soufi, "Bounding the eigenvalues of the Laplace-Beltrami operator on compact submanifolds," *Bull. Lond. Math. Soc.* 42 (2010), 96-108. Theorem 1.4 and Section 5. [DOI](https://doi.org/10.1112/blms/bdp100); [author preprint](https://arxiv.org/abs/0909.5346).

[CEG] B. Colbois, A. El Soufi, A. Girouard, "Isoperimetric control of the spectrum of a compact hypersurface," *J. Reine Angew. Math.* 683 (2013), 49-65. Theorem 1.1 and Example 3.1. [DOI](https://doi.org/10.1515/crelle-2012-0008); [author preprint](https://arxiv.org/abs/1007.0826). The inspected preprint is arXiv v2, revised 2011; the internal 2022 compilation date does not make it a new 2022 result.

[NK] C. De Lellis and L. Szekelyhidi Jr., "John Nash's nonlinear iteration," Theorem 1.2, crediting J. Nash's 1954 and N. H. Kuiper's 1955 C1 isometric-embedding theorems. [Author-hosted text](https://www.math.ias.edu/delellis/sites/math.ias.edu.delellis/files/contr_vol_Nash_11.pdf).

The standard smooth-approximation theorem is also cited by CDE to M. W. Hirsch, *Differential Topology*, p. 50. This audit inspected that invocation in CDE and reconstructed the required stability and metric-comparison argument; it does not claim a separate retrieval of Hirsch's book. Generalized Jordan-Brouwer separation is used in its standard smooth compact connected hypersurface form.
