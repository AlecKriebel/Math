# Independent audit of gradient constrained Ginzburg Landau minimizers

Problem 30005994 / OWR-14298587-009, queue rank 959. Review date: 7 October 2026 UTC.

**ACCEPT as a source-qualified partial mathematical report, with disposition UNSOLVED for the original general-potential question after five substantive approaches.** No full solution, counterexample, novelty, or priority claim is accepted. The inspected quartic-potential theorem is credited to its authors and remains a preprint in the records checked. This is an AI-assisted independent review of the submitted arguments, not journal peer review or a formal proof-assistant certificate.

No change to the mathematical author report is required. The author packet is preserved byte for byte. A non-blocking packaging weakness is documented below and covered by the stricter gate supplied with this audit.

## Frozen subject of review

- Author REPORT.md: 15,531 bytes; SHA-256 `5a69336298d8a448f4614bed8e0fc291b0d9622afbd8ad86b2b2bb775bd445f5`.
- Original author ZIP: 14,746 bytes; SHA-256 `2257767b04521b39bc59ccd62bfc03321d0ec87d81532b35d09d0d98bc263670`.
- Seven regular top-level author files were inspected, including AUTHOR_MANIFEST.json. Six payload files are listed by that manifest. The archive and directory have identical member bytes, with no nested entries or duplicate names.
- AUTHOR_BASELINE.json pins all seven original files, including the original manifest. The historical pending-review wording in the author files is intentionally preserved; this separate acceptance records the completed review.

The review read the complete REPORT.md, checked each mathematical argument, inspected the scripts rather than merely trusting their output, repeated normal and optimized execution from other working directories, and reconstructed the algebra independently using rational arithmetic and sparse polynomials. The independent script uses no SymPy and imports none of the author's code. Independence here describes the separate mathematical and computational derivation, not an assertion of human or institutional review.

## Primary source scope

The [official Oberwolfach report](https://ems.press/content/serial-article-files/50045), printed pages 2133–2136, explicitly sets a general C¹ convex potential W, positive away from zero, before posing Question 2 for gradient fields. The displayed functional in the question retains W. The review inspected the cached PDF text and both relevant rendered pages. This supports the author's decision not to replace the original question by its customary quartic special case. The same report states the N≥4 gradient result in that setup, but the reviewed packet does not independently establish the regularity extension discussed next.

The [published Ignat–Nahon–Nguyen article](https://link.springer.com/article/10.1007/s00205-025-02082-3) explicitly assumes C² convex W in Section 1.1. Its Theorem 1 states 4≤N≤6; the next sentence obtains N≥7 from earlier work. Thus the author report's short attribution of N≥4 to Theorem 1 should be read with that immediately following attribution. This is a citation precision note, not a change to the claimed dimensional coverage. The publisher gives 24 January 2025 and volume 249, article 14. Neither the author nor this audit silently identifies its C² assumptions with the OWR C¹ setup.

The energy and admissible class preceding [Ignat–Nguyen, arXiv:2609.35398v1, Theorem 1.1](https://arxiv.org/html/2609.35398v1) are the standard quartic energy and all H¹ vector fields with trace Id. The theorem states uniqueness for every dimension at least two and every positive parameter. Its [record](https://arxiv.org/abs/2609.35398) shows v1 submitted 28 September 2026. The review checked the theorem, its surrounding normalization and the comparison mechanism in the introduction and Section 2; it did not independently certify the complete proof. The transfer to gradient fields and the supporting-potential corollary therefore retain this external-theorem dependency. No general-W theorem or journal acceptance is inferred from that source.

The planar precursor [Chen–Liu–Wei–Yang, arXiv:2608.15957v1](https://arxiv.org/html/2608.15957v1), Theorem 1.1, concerns the same standard potential and full planar boundary class; it is a credited precursor, not an additional general-W resolution. The [local-minimality paper](https://ems.press/content/serial-article-files/47561), Theorem 1.2 on printed page 666, provides positive second variation for C² convex potentials in every N≥2. Applying only its standard-potential consequence in Approach 3 is valid. Local minimality alone does not supply the missing global comparison for general W.

Only the cached OWR source has locally verified PDF bytes in this audit. Its SHA-256 is `cc69a577a16754228ce3d35c2f8c5530bf672f67818daf32dc30a38f64859ccf`, size 800,617 bytes. Other sources were inspected through public web representations. Opening a web PDF does not certify a local PDF byte count or hash. No new shell download was attempted during this completion review. There is no claim of exhaustive literature coverage, current universal openness, or proof certification for entire cited papers.

## Common comparison and admissibility

For a finite-energy competitor, v=u−U belongs to H¹₀. Put t=1−|U|² and q=2U·v+|v|². Both potential arguments are within W's domain because t−q=1−|u|²≤1. Convexity gives W(t−q)−W(t)≥−W′(t)q. Since a=ε⁻²W′(1−f²) is bounded and U is bounded, the weak PDE may be paired with v by H¹₀ density, and its linear term cancels the gradient cross-term. The remaining bound is exactly G(U+v)−G(U)≥F(v)/2, with the stated coefficient and sign. Infinite-energy competitors cannot improve the finite energy of U. No W″, bounded competitor, or modulus truncation is required.

The radial potential Φ(r)=∫₀ʳf(s)ds produces U. The regular profile has f/r and f′ bounded near zero; the Hessian of Φ has radial eigenvalue f′ and tangential eigenvalues f/r. Consequently Φ∈H² and has the required gradient trace. The weaker phrase f=O(r) in the report is used together with the cited regular-profile premise, not as a standalone implication controlling f′. Uniqueness is of the vector field; adding a constant to a potential changes no admissible field.

## Assessment of the five approaches

### 1 Global spectral domination

Because zero is an interior minimum of differentiable W, W′(0)=0. Convexity makes W′ nondecreasing, and W(1)>0 implies M=W′(1)>0. The profile stays between zero and one, so 0≤a≤M/ε². Componentwise Dirichlet Poincaré gives F(v)≥(λ_D−M/ε²)‖v‖²₂. Strict positivity for ε²>M/λ_D proves uniqueness in the entire vector class. Zero extension from the ball to (−1,1)^N followed by the one-coordinate interval inequality gives λ_D≥π²/4 and hence the stated sufficient ε>2√M/π. The estimate is deliberately nonsharp; neither its endpoint nor small-parameter positivity is claimed. This is a valid complete restricted result.

### 2 Angular mean removal

Substituting v=fz and using −Δf−af=−(N−1)f/r² gives the claimed ground-state identity. On each sphere the componentwise zero-mean condition permits the sharp spherical Poincaré constant N−1, leaving the nonnegative radial term. The identity has the correct sign of its angular subtraction and radial ODE term.

The analytic passage is sound. Spherical averaging is a bounded H¹ projection: radial derivatives commute with averaging, Jensen bounds the radial energy, and removing a constant angular mode cannot increase angular energy. Apply the complementary projection to smooth compactly supported approximants. For each bounded smooth approximant, radial cutoffs around zero give H¹ convergence because a point has zero H¹ capacity in N≥2; logarithmic cutoffs handle N=2. A diagonal sequence keeps zero mean and avoids the origin. This is an H¹ vector-field argument and does not falsely assert density of functions avoiding zero in H² in N=2,3.

F is continuous in H¹ because a is bounded. On each fixed annulus, division by positive regular f is bounded on H¹, so the radial lower bound passes to the limit. Exhausting by annuli yields the full lower bound. Equality of energies forces ∂r(v/f)=0 almost everywhere on every annulus. Thus v=f c(θ), and the zero outer trace with f(1)=1 forces c=0. No equality classification at the singular origin is needed.

For the scalar-potential assertion, testing spherical integration by parts against θᵢ gives average(∇φ)=A′+(N−1)A/r. Therefore absence of degree-one scalar harmonics implies the required vector mean condition. The clamped polynomial ψ=x₁(1−r²)² is a genuine missed mode: its gradient has a factor 1−r², whereas its mean is [(N−(N+4)r²)(1−r²)/N]e₁. The boundary constraint therefore does not remove the mode. The report correctly leaves its nonlinear interaction with the other modes unresolved.

### 3 Antipodal parity comparison

For even v and odd U, the cubic integral ∫(U·v)|v|² vanishes. Expanding the standard quartic energy after weak-PDE cancellation gives t²Q(v)/2+t⁴‖v‖⁴₄/(4ε²), with Q=F+2ε⁻²∫(U·v)². The cited nonnegative second variation then gives strict increase for every nonzero v and amplitude. Finite-energy competitors are in L⁴ for this potential; otherwise their energy is infinite, so there is no hidden high-dimensional Sobolev embedding assumption.

For W(s)=s⁴ the proposed pointwise Hessian lower bound has residual −309/10000 at a=1/2, b=1/10, c²=1/10. The explicit vectors in the report realize these values, satisfy Cauchy–Schwarz feasibility, and keep both potential arguments at most one. The calculation refutes that lower bound only. It neither constructs an admissible lower-energy field nor disproves global minimality. That logical limit is correctly stated.

### 4 Supporting quadratic comparison

Under (6.1), δ=ε/√c gives the exact normalization c/(4ε²)=1/(4δ²). The potential inequality holds for every possible argument 1−|u|²≤1, including negative arguments from |u|>1. At the standard radial minimizer, all such arguments lie in [0,1], where equality holds. The energy sandwich and equality case therefore transfer uniqueness from the cited quartic theorem. Equality of W with the quadratic on [0,1], including its C¹ derivative, also makes the radial equations coincide. The example ct²/2+(−t)₊⁴ is C² and convex. The ratio s⁴/(s²/2)=2s² tends to zero, so this device cannot cover the test potential s⁴ with any positive c. The external theorem dependency is explicit and appropriate.

### 5 Entire profile Bregman comparison

The exact Bregman expansion follows from the same cancellation as the common identity, and convexity gives nonnegativity of each separate remainder. When perturbations are multiplied by ρ=F/f, the change of squared modulus is ρ²q. For the quadratic potential the remainder difference is (1−ρ⁴)q²/2. For W(s)=s⁴, f²=9/10, F²=1/2 and q=1/100, the independently reconstructed remainders are 561/100000000 and 48241/1049760000, with difference −1654369/41006250000. An orthogonal perturbation realizes positive q pointwise in every N≥2.

The report explicitly makes availability of an appropriate entire profile an additional premise. It does not claim the selected pointwise f and F values occur simultaneously on actual profile solutions, or that the quadratic terms cannot offset the negative difference. Accordingly this is a valid obstruction to a convexity-only transfer, not a counterexample or instability result.

These are five distinct mathematical routes with calculations and identified limitations. Bibliographic searches, algebra replays, and packaging steps are not counted as mathematical approaches. The full original target is not concluded by any route or by combining the restricted cases.

## Reproduction and negative controls

The author's 43 checks replay identically under normal Python and Python −O, both in isolated mode and from a different working directory. The independent standard-library implementation also passes 43 controls in both modes and matches the two rational witnesses. Explicit runtime checks are used rather than assertions disabled by optimization. These checks do not prove the functional-analytic arguments, which were assessed separately above.

The completed audit rehashed and parsed both full cached datasets. problems.json has 15,458 records, 68,931,837 bytes, and SHA-256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`; exactly one target record matches the author's extracted source record. research_results.json has 6,701 records, 80,334,822 bytes, and SHA-256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`; the exact target key is absent. The existing retrieval receipt associates both with revision `37e53eabe540fb458758e198be61634bd02ee008`. This is a fresh local byte/parse check of cached files, not a new remote fetch or exhaustive repository-history certificate.

The original verify_packet.py enumerates only paths for which is_file() is true. It rejects changed payload bytes and extra regular files, but ignores an unexpected subdirectory; it can also follow a same-byte symbolic link. The actual pinned archive contains neither. Thus its successful run alone is insufficient as a general exclusion gate, although the inspected frozen packet is clean. The audit's verify_audit.py requires exact top-level membership, uses lstat to reject nonregular members, pins the original manifest as well as its payload, checks ZIP membership/types/hashes, and replays both algebra suites. Its negative controls reject extra files, empty and populated directories, symlink substitution, altered report bytes, altered manifest bytes, and corrupted ZIP bytes. Separate witness mutations fail under normal and optimized execution. See CONTROL_RESULTS.json for actual outcomes.

Hash manifests are integrity aids, not cryptographic signatures. An independently retained ZIP hash is the external freeze anchor. Do not accept an edited packet merely because someone recomputed its manifest. Publication, if separately authorized, should use explicit allowlisted regular files and exclude all source PDFs, extracted texts, images, dataset contents, private source records, and coordination material.

## Final disposition

Accept the exact frozen author report as a careful UNSOLVED 5/5 partial analysis. The common estimate, restricted proofs, conditional credited corollary, and algebraic obstructions are mathematically consistent within their stated premises. The regularity distinction and external-preprint dependency must remain visible. The subdirectory exclusion weakness is handled by the independent strict gate without rewriting historical author bytes. This audit itself performs no publication.
