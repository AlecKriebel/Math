# Independent review of the bounded nonlinear EKI partial theorem

**Verdict: PASS_SCOPED_BOUNDED_FORWARD_STRONG_PATH_CONVERGENCE.** No mandatory correction was found in the frozen artifact. The bounded, locally Lipschitz, finite-dimensional theorem is proved in the stated expectation-of-path-supremum norm, including the exact initial-moment endpoint. The unbounded globally Lipschitz example defeats the proposed global quadratic estimate, not convergence. The original general nonlinear target remains **unsolved, 2/5**.

Reviewed `PARTIAL.md`, SHA-256
`6fdce06f9de27f5fbd5010c866c2b30af5f6b28765646aff4ce16fb48906982d`.
This is an independent AI mathematical/source audit using gpt-6-astra at xhigh. It is not human peer review or a certification of novelty. The author's mathematical files were not edited.

## 1. Exact model and prior-result scope

I read the complete Schillings contribution in [OWR 38/2018](https://ems.press/content/serial-article-files/46760), printed pp. 2341–2343, and visually inspected p. 2342. The ensemble size is fixed; the parameter space is allowed to be a separable Hilbert space; observation dimension is finite; and the Brownian observation perturbations are independent across particles. The displayed cross-covariance has normalization 1/J, not 1/(J−1). The question concerns the discrete-to-continuous time-step limit in the general nonlinear setting. It does not prescribe an Lq exponent or locate the time supremum relative to expectation.

The artifact correctly narrows its theorem to finite-dimensional parameters and bounded locally Lipschitz forward maps, and specifies the stronger path norm explicitly. It does not turn this special case into a complete solution of the source question.

I also checked the complete institutional copy of the published [2022 SIAM paper](https://d-nb.info/1290144702/34), DOI [10.1137/21M1437561](https://doi.org/10.1137/21M1437561), including the scheme, Theorems 2.11, 3.2, 3.5, and Remarks 2.13 and 3.4. Theorem 3.2 supplies path convergence in probability under its globally Lipschitz assumptions and finite second initial moments. Theorem 3.5 supplies a conditional moment conclusion with supremum outside expectation. Remark 2.13 discusses moving the supremum inside expectation without carrying out that additional proof. Remark 3.4 discusses cutoff forward maps. These prior results and the localization/moment strategy are properly credited. The frozen theorem does not rely on interpreting compact support as a deterministic invariant box.

This review checks applicability and the new written partial argument. It does not certify an exhaustive later-literature search or priority of its bounded-forward formulation.

## 2. Whitening, covariance bounds, and existence

Let L=Gamma^(1/2), with the positive-definite symmetric root. With H=L^(-1)G, the raw covariances satisfy

\[
 C^{up}=CL,\qquad C^{pp}=LSL.
\]

Thus

\[
 C^{up}(\Gamma+hC^{pp})^{-1}L
 =C(I+hS)^{-1}.
\]

This verifies the order of the noncommuting matrix factors. Multiplying the raw gain by the observation perturbation of covariance h^(-1)Gamma produces the diffusion term with an actual Brownian increment of covariance hI. There is no missing factor of h or square root of h. The continuous drift and diffusion whiten in the same way, and the interpolation agrees with the exact discrete method at every grid time.

The centered empirical identities give the stated bounds:

\[
 \|C(U)\|_{HS}\le M\|U\|/\sqrt J,
 \qquad 0\preceq S(U)\preceq M^2I.
\]

The second inequality follows because the operator norm is bounded by the trace, and the centered observation variance is at most the uncentered one. The resolvent is a contraction and differs from identity by at most hM². Stacking all J particles then gives exactly the stated homogeneous linear-growth estimates for drift and diffusion. The noise matrix is block diagonal because the Brownian motions are independent, so its squared Hilbert–Schmidt norm is J times that of the single-particle matrix.

Local Lipschitz continuity of G implies local Lipschitz continuity of C and S. The identity

\[
 R_h(U)-R_h(V)
 =hR_h(U)(S(V)-S(U))R_h(V)
\]

shows that the resolvent's local Lipschitz bounds are uniform for 0<h≤1. This justifies the coefficient consistency and uniform local estimates used later. No differentiability or global Lipschitz constant for G is needed in the partial theorem.

The continuous coefficients are locally Lipschitz with global linear growth, giving a unique global strong solution by the standard localized existence argument. The Euler-type recursion is explicit and its resolvent is defined for every ensemble. On a finite time interval it therefore yields a well-defined continuous stochastic interpolation. The zero ensemble is absorbing even if H(0) is not zero, because every centered parameter deviation vanishes there.

## 3. Uniform path moments

For any r≥2, the integral form of either process, the inequality for the rth power of a sum, Hölder's inequality, and BDG give a bound of the form

\[
 \mathbb E\sup_{v\le t}\|Y_h(v)\|^r
 \le C\mathbb E\|U_0\|^r+
 C_{r,T}\int_0^t\mathbb E\sup_{v\le s}\|Y_h(v)\|^r\,ds.
\]

For the stochastic term one uses

\[
 \mathbb E\left(\int_0^t\|g_h(Y_h(\eta_h(s)))\|_{HS}^2ds\right)^{r/2}
 \le T^{r/2-1}\int_0^t
 \mathbb E\|g_h(Y_h(\eta_h(s)))\|_{HS}^r ds.
\]

The grid value is bounded by the preceding running maximum. All growth constants are uniform in h and independent of the initial truncation level. Gronwall yields (9). The corresponding stopped continuous estimate has the same constants. Its second-moment exit bound proves nonexplosion; stopping can then be removed. The homogeneous right side C E||U0||^r is justified by the homogeneous growth bounds and absorbing zero, rather than a bound with an unexplained additive constant.

These estimates are for expectation of the path supremum, so they establish precisely the norm later needed for uniform integrability. They are not merely fixed-time moment estimates.

## 4. Stopped within-step error and convergence in probability

The only subtle indicator step in (10) is valid. Fix s and let eta=eta_h(s). Define

\[
 J_s=\int_{\eta}^{s}1_{\{r\le\sigma_R\}}
       f_h(Y_h(\eta_h(r)))\,dr
 +\int_{\eta}^{s}1_{\{r\le\sigma_R\}}
       g_h(Y_h(\eta_h(r)))\,dW(r).
\]

On the event s≤sigma_R, this equals Y_h(s)−Y_h(eta). The stopped integrands are bounded by constants depending only on R: when r≤sigma_R, their grid arguments occur no later than r and have norm at most R. Hence

\[
 \mathbb E[1_{\{s\le\sigma_R\}}
   \|Y_h(s)-Y_h(\eta)\|^2]
 \le\mathbb E\|J_s\|^2\le C_R(h^2+h).
\]

The indicator is not treated as independent of the Brownian increment, or pulled through Itô isometry incorrectly. It is absorbed into stopped adapted integrands before the estimate. Integrating gives (10).

For the common stopped error, subtract the two integral equations and compare coefficients first at U(s) and Y_h(s), then at Y_h(s) and its grid value. Uniform local Lipschitz estimates control the first two differences; the consistency error contributes O(h). BDG, (10), and Gronwall then give (11), with matching initial states. This argument does not require any independence between the stopping time and the error.

The global path moments bound the probability of an exit from radius R uniformly in h. Therefore, for any fixed positive error threshold, the full error probability is bounded by a term tending to zero as h→0 at fixed R plus C/R². Taking the limits in that order proves (12). A global convergence rate is not asserted, correctly, because the local Lipschitz constants may grow with R.

## 5. The initial-moment endpoint is genuinely covered

A uniform qth-moment bound alone would not imply uniform integrability of the qth powers. The proof correctly avoids that invalid shortcut.

For bounded initial data, every higher moment r>q is finite. Uniform path moments of order r then make the qth powers of the path errors uniformly integrable; probability convergence yields strong Lq path convergence.

For the general initial ensemble, A_L={||U0||≤L} is measurable at time zero. The same Brownian driver is used, and both the SDE and discrete interpolation are zero when started at the zero ensemble. Pasting on this initial event therefore gives

\[
 U^L=1_{A_L}U,\qquad Y_h^L=1_{A_L}Y_h.
\]

This is an event-pasting identity, not a homogeneity assertion for nonlinear coefficients under arbitrary scalar multiplication. It follows from the two choices of the indicator, time-zero measurability, and pathwise uniqueness (or the explicit recursion). The analogous complementary process starts at 1_(A_L^c)U0. Applying the already proved moment estimate to it yields the tail bound (13) with a constant independent of L and h. The tail E[1_(A_L^c)||U0||^q] tends to zero under exactly the stated qth-moment assumption. Taking h→0 first on A_L and then L→infinity proves the claimed endpoint.

The Brownian motions' independence from the initial ensemble supplies the usual initial filtration setting. No unrecorded q+epsilon moment is used. As an independent control, one can take initial magnitudes 2^k with masses 2^(-qk)/(k(k+1)), putting leftover probability at zero. This has finite qth moment and no moment of any larger order; its q-moment tail after level K is exactly 1/(K+1). The truncation proof still applies.

## 6. The two obstruction diagnostics have the stated limited meaning

For the compact-support bump at the ensemble (0,1/2), direct empirical covariance calculation gives C=−1/8 and S=1/4. The first update is Gaussian with mean h/[8(1+h/4)] and strictly positive variance h/[64(1+h/4)²]. Its support is unbounded for every positive step. Thus compact support of G does not imply a deterministic state box invariant under every Brownian realization. This does not contradict finite path moments or convergence, and the candidate does not attribute a stronger interpretation to the source's informal boundedness wording.

For the smooth globally Lipschitz map equal to zero on the negative half-line and to x on x≥1, at U_R=(R,−aR) one has C=(1+a)R²/4, S=R²/4. The quadratic generator is

\[
 -2R^2C+2C^2=(1+a)(a-3)R^4/8.
\]

The factor two in the diffusion contribution is required by the two independent particle noises and is present. The discrete expected energy equals the sum of the two squared updated means plus twice the common variance. Expanding it gives exactly equation (16).

For a=5 and h=R^(-4), the expected one-step increase tends to 3/2, whereas h(1+V(U_R)) tends to zero. This defeats a single global constant in the proposed one-step quadratic estimate. The generator ratio similarly diverges quadratically. It does not prove moment divergence, explosion, or nonconvergence of the process, nor does it show that such states must be reached from any prescribed initial ensemble. The artifact preserves these distinctions, consistently with the published probability-convergence theorem for globally Lipschitz maps.

## 7. Reproducibility and conclusion

All **1,954** submitted exact assertions were replayed successfully, and the resulting receipt is byte-identical to the frozen author's receipt. The independent standard-library checker passes **3,270** assertions. It uses three-parameter/two-observation bounded nonlinear ensembles of four different sizes, noncommuting whitening matrices, an independent resolvent identity, scalar Gaussian energy expansions, and exact endpoint-moment tail controls. It does not invoke the author's verifier.

Neither set of finite controls proves stochastic convergence or disproves the general nonlinear problem. The path-norm result rests on the analytic argument audited above. The scope is a valid bounded-forward finite-dimensional partial theorem plus precise estimate obstructions. Preserve **unsolved 2/5**, existing-source credit, the stronger-versus-weaker norm distinction, and the absence of a novelty claim. No correction to the frozen manuscript is required.
