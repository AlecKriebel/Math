# Independent audit: harmonic spheres and the energy parameter

Problem 30006419 / OWR-14299521-012, rank 969. Audit date: 7 October 2026.

## Verdict

**PASS: complete negative resolution of the general-admissible-energy formulation inspected in the cited sources.** The frozen PROOF.md constructs an admissible compact smooth Riemannian target and a smooth sphere homeomorphism that is locally minimizing for Reshetnyak energy, with the full fixed-trace Sobolev-competitor quantifier, but has no finite infinitesimal quasiconformality constant. No mathematical correction patch is required.

**Separate verdict: PASS for the frozen KOREVAAR_SCHOEN.md theorem**, including its explicit nonsharp bound 4 + sqrt(17). This is a distinct affirmative result for the fixed Korevaar–Schoen energy. It is not needed to validate the counterexample.

These are mathematical audit judgments, not proof-assistant certification, human peer review, or historical-priority judgments. The energy name and the source-version limitation must accompany any summary.

## Frozen objects and review method

The complete nine-file author packet was copied without changing its originals. Its external manifest pin is:

`9cb1f5c242224d4f04a34b1d28e660a29fb2f63d47215d16257f5d4073c001cb`

The two principal files are:

- PROOF.md, 16,750 bytes, SHA-256 `2634e714b9a06a1770ae39b0201031c7d2a7ce6e97f3330f8745d0e2453d4fef`.
- KOREVAAR_SCHOEN.md, 6,702 bytes, SHA-256 `4bac91a7e34b266391051d48ae2ef10adc60d10b6ed0d57d1c5cb8395e2a6abe`.

I read both arguments in full, rederived their mathematical steps, inspected the relevant primary-source passages, and wrote independent controls. I did not rely on another audit or use an additional reviewer. The immutable source packet retains its original pre-audit status descriptions; this separately signed-off report supplies the later disposition.

## Source scope and current-source limitation

The [Oberwolfach report](https://ems.press/content/serial-article-files/52249), printed page 1625, fixes an energy before posing Question 1. The [arXiv v1 paper](https://arxiv.org/pdf/2503.08553v1) explicitly includes Reshetnyak energy, imposes quasiconvexity, and states neighborhoodwise minimization against every matching-trace Sobolev competitor in Definition 6.1. Question 1.9 is the corresponding question. Definition 2.3 uses an almost-everywhere uniform stretch-ratio bound. These passages match the interpretation used here.

I independently inspected the online primary text and locally rendered the two crucial printed definition/question pages after web screenshots failed. The local source PDF hashes and sizes match the public ledger. The [arXiv record](https://arxiv.org/abs/2503.08553) displayed only v1. The [author's bibliography](https://people.math.ethz.ch/~damameier/research.html) lists the 2026 journal publication; the final publisher text was unavailable in my retrieval as well. Consequently, acceptance is bound to the inspected OWR and arXiv wording, with no assertion that the final journal wording was inspected.

The supplied corpus/inherited-attempt metadata is not independently recertified by this mathematical audit. No exhaustive literature search or priority claim is made.

## Main proof: adversarial examination

### 1. Admissible energy

For a Riemannian target, the approximate metric differential is the norm of the ordinary weak differential, so Reshetnyak energy has density equal to its largest singular value squared. This is not the Hilbert–Schmidt-squared density.

The asserted general-energy axioms hold. On the unit sublevel, every seminorm is bounded by the Euclidean norm, hence is uniformly 1-Lipschitz and bounded on the unit circle. Uniform limits remain seminorms. This proves compactness and therefore properness. The operator norm squared is convex as a function of a linear map into any fixed normed space. The divergence theorem identifies the average derivative of a fixed-affine-boundary competitor with the original linear map; Jensen then proves the required quasiconvexity. The proof establishes a slightly stronger comparison than the immersed-competitor formulation requires.

### 2. Smooth compact target and all target hypotheses

The cutoff has a nonzero denominator everywhere and is constant near each endpoint of its transition. The absolute value in the metric causes no irregularity at zero because the exponent vanishes on an entire neighborhood there.

At the negative end, the change of variables z = exp(s + i theta) turns the metric exactly into |dz| squared; at the positive end, zeta = exp(-s - i theta) does the same. Thus the two added points are ordinary smooth, nondegenerate metric points, not conical singularities or boundary components.

Compact smooth Riemannian geometry supplies completeness, geodesics, and a uniform contractible-ball radius. A small-diameter sphere image lies in one such ball. The chart-cone proof of the local quadratic isoperimetric inequality is valid for the prescribed Lipschitz boundary parametrization: the cone is a Sobolev filling, its area is bounded by half the product of the Euclidean loop length and its maximal distance from the cone point, and the latter is at most half that length. Uniform chart bounds supply the stated local constant and scale.

### 3. Homeomorphism, poles, and Sobolev membership

The cutoff defining a(t) is supported where t squared is at most 1/4. Hence 0 <= a <= 1 globally; its sole zero is t = 0. The integral h is strictly increasing despite that single zero derivative, and its affine tails make it onto the real line. Oddness, the cubic central formula, and the positive constant c follow directly.

At both poles the map is multiplication by exp(c) in the respective complex coordinates. Thus the map is globally smooth, not merely continuous across the compactification. Its inverse need not be differentiable on the equator, which is irrelevant to the stated homeomorphism and W1,2 requirements.

### 4. Flat-belt comparison and escaping competitors

The proof does not confuse intrinsic patch distance with full-target distance. A sufficiently small strongly convex target ball has the relevant ambient-distance property: its minimizing geodesics remain in the flat coordinate patch, where angular displacement is bounded by their lengths. The real angular coordinate is therefore genuinely 1-Lipschitz for the ambient metric on that ball.

McShane extends it to the entire compact target. Composition with every W1,2 competitor is a scalar W1,2 function with the specified trace, and its Dirichlet energy is bounded by the competitor's Reshetnyak energy. The affine scalar x minimizes its Dirichlet energy on any relatively compact Lipschitz subdomain, including nonrectangular or multiply connected ones. The zero-trace integration-by-parts argument supplies the exact lower bound. No continuity of the competitor, image containment, homotopy class, or small-energy hypothesis enters.

In particular, using only local flat coordinates without a global extension would have left a gap. The frozen proof already fixes precisely that issue.

### 5. Conformal-cap calibration and Sobolev Stokes

The cutoff can be chosen with integral m strictly between zero and half the total target area. The resulting coefficient ranges from -m/(A-m) to 1, so the two-form has comass at most one. Its integral is zero and it agrees with the area form near the comparison map's image. On an oriented sphere, zero integral makes it exact. This avoids the false assertion that the target area form itself is exact.

The boundary-invariance proof is valid at the critical W1,2 regularity. A global smooth one-form admits a finite representation as a sum f_j dg_j. For its scalar compositions, bounded W1,2 mollifications establish d(f dg) = df wedge dg in distributions. To spell out a potentially delicate convergence: the uniformly bounded approximants f_n converge almost everywhere, so f_n dg converges strongly in L2 by dominated convergence; f_n(dg_n-dg) also tends to zero in L2. The wedge products converge in L1 by strong L2 convergence of the derivatives. No smooth sphere-valued approximation is assumed.

Matching trace gives a W1,2 glued map. The difference of its pulled-back primitive and the reference pullback is an L2 one-form supported in the compact closure of the comparison domain. Pairing its derivative with a cutoff equal to one there yields zero. The right-hand derivative is the L1 difference of the two-form pullbacks. This proves the required integral equality for every competitor.

Finally, the signed pullback is bounded above by absolute Jacobian, which is bounded above by squared operator norm. The conformal orientation-preserving reference attains equality. Competitors reversing orientation, wrapping the sphere, or carrying extra bubbles do not evade this calibration.

### 6. Locality, seams, and poles

The two open regimes in Section 5 cover the whole source sphere and overlap. Points with |t| = 1/2 are handled by the flat-belt regime; points with |t| = 1 are handled by the conformal regime. The poles have genuine smooth coordinate neighborhoods. The proof supplies one neighborhood at each point and then handles every relatively compact Lipschitz subdomain within it. It does not replace this quantifier with pointwise infinitesimal stationarity or a restricted test family.

### 7. Essential unboundedness and nearby false conclusions

On the central punctured band the stretch ratio is exactly 1/t squared. For every proposed finite bound, a whole positive-area band violates it. Its round area can be written as 4 pi tanh(delta), with delta the positive band half-width. The failure is therefore not an artifact of a null equatorial set or of an ill-chosen representative.

The global comparison is also correct: the conformal coordinate map has energy equal to target area, whereas the constructed map has excess 4 pi c. The change of variables through h is legitimate despite its single vanishing derivative. Numerically, c is approximately 0.372427320021913 and the excess is approximately 4.68005973030790.

The explicit compactly supported positive variation in a positive-t rectangle strictly lowers the Korevaar–Schoen energy. Thus neither global homotopy minimality nor Dirichlet harmonicity is accidentally being asserted. Comparability of the two energies does not imply equality of their minimizers.

## Separate audit of the Korevaar–Schoen appendix

The angular Jacobian for w = Av/|Av| is det(A)/|Av| squared. Applying homogeneity and then dividing by det(A) gives exactly the appendix's inverse-fourth-power angular formula. This makes the domain-matrix dependence smooth even for nonsmooth and degenerate seminorms. Differentiating yields the stated symmetric tracefree stress with factors 4 and 2; there is no missing determinant factor.

A compactly supported domain variation is an admissible fixed-trace competitor. After changing variables, its first variation is the stress paired with DV. Nearby-matrix derivative bounds are controlled by the squared maximum seminorm, which is integrable. Differentiation under the integral is justified. The two distributional divergence equations are precisely the Cauchy–Riemann equations for a - ib.

The scaling and rotation transformation laws give the square of the holomorphic coordinate derivative, as required for a quadratic differential. Each pole is treated by its own local stationarity equation; the proof does not simply discard possible puncture singularities. A global holomorphic quadratic differential on the sphere vanishes, so the stress vanishes almost everywhere.

The quantitative seminorm argument is sound. After normalizing maximum stretch to one, choose a minimizing unit direction with value m and its perpendicular direction with value L. The triangle inequality gives L squared >= 1 - m squared. Comparing with the rank-one seminorm L|v_1| gives a uniform squared-density error at most 2m. The stress kernel has operator norm 2, and the normalized circle integral yields the factor 8m. Rank-one stress has norm L squared. Thus 1 - m squared <= 8m, yielding m >= sqrt(17) - 4 and the stated ratio bound. Zero seminorms satisfy quasiconformality trivially.

This argument needs the metric Sobolev differentiation and domain-chain-rule framework explicitly stated in the appendix. No target topology or isoperimetric assumption enters its later steps. Balanced non-Euclidean fourfold-symmetric norms provide the correct negative control against overclaiming conformality. The Reshetnyak density lacks this uniquely differentiated stress; the appendix does not improperly transfer its conclusion there.

## Controls and artifact integrity

- The author's 257 exact controls passed unchanged under ordinary, isolated, and optimized Python execution. The isolated replay is byte-identical to CHECK_RESULTS.json.
- Independently written controls check the metric/map energy excess, cutoff sample values, positive-area distortion witnesses, exact calibration cancellation, an exact same-trace lowering KS variation, and flat-belt perturbations.
- Independent angular quadrature and finite differences check the KS formulas for Euclidean, l1, linfinity, rank-one, and anisotropic seminorms. They detect the intended distinction between balanced nonround norms and nonzero rank-one stress.
- The independent controls passed both normally and with optimization, with identical output. Their guard checks remain active with optimization.
- The externally pinned author manifest accepts the pristine packet and rejects a wrong external pin, altered proof, missing file, extra file, symlinked proof, and altered manifest. Test mutations were confined to disposable copies.

Finite controls supplement the analytical review; they cannot establish the universal Sobolev comparisons, global smoothness, or a literature-priority claim. No copied source document, source text, dataset content, or private coordination material is included in this audit's public output. No publication action was taken.

## Final disposition

Accept the frozen main proof as a full counterexample to the inspected general-energy question. Accept the KS appendix separately as an affirmative fixed-energy theorem with the displayed nonsharp constant. Preserve all source-version, energy-scope, AI-assistance, unrefereed-status, and non-priority qualifications. No blocker and no required correction remain in this audit.
