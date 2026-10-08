# PR141: independent adversarial audit of the transform reduction

**Verdict: PASS for the finite-k analytic-transform characterization, with no mandatory mathematical correction found.** This is a mathematics-stage AI review of the unchanged original head `523247e3246a5f44c7b0089074bb304c1f642bd0`; it is neither a priority audit nor a publication-package acceptance. Novelty remains unestablished. I did not infer validity from the previous review's verdict or diagnostic counts.

## 1. Exact claim and the original question

I independently read the [primary report](https://ems.press/content/serial-article-files/46745), printed p.1452 (PDF zero-based page71), and inspected the supplied rendering of that page. The question concerns the joint vector of Lebesgue measures of the sets first visited by independent Brownian particles, using uniform random or equidistant starts. The page does not impose a density, a named distribution, large-k asymptotics, or a complexity bound.

The candidate's strongest verified claim is an exact deterministic formula for every homogeneous coefficient of the multivariate Laplace transform, an absolutely convergent outer series, a uniform factorial outer remainder, and uniqueness of the associated probability measure. An explicit transform of this kind is a complete characterization of the requested probability distribution. This conclusion does not say that an unevaluated stochastic expectation would have sufficed: here every finite-dimensional ownership probability is reduced to specified scalar exit functions, finite permutations, and ordinary finite-dimensional integration. The enormous dimensions and permutation counts limit practical usefulness but do not leave an unknown probability, a path integral, or an unsolved integral equation inside a coefficient.

This audit does not establish a new closed-form density or historical priority. The representation uses standard ingredients. Those facts must remain visible in any later paper and priority decision.

## 2. Kernel positivity, signs and improper integration

For generator one-half the second derivative, the Dirichlet sine heat kernel has prefactor `2/ell` and eigenvalues `n^2*pi^2/(2*ell^2)`. At each strictly positive time its spatial and time derivatives converge locally uniformly; differentiation at the endpoints yields the displayed exit fluxes. The derivative at the left boundary enters with `+1/2`, while the derivative at the right boundary enters with `-1/2`. Consequently both formulas in (2), including the alternating sign at the right end and the factor `pi/ell^2`, are correct.

The positivity argument does not require the Fourier summands to be positive. Let `h_0(beta)=1-beta/ell`. The Markov property gives the probability of surviving to time t and eventually leaving at the left endpoint as `integral H(t;alpha,beta) h_0(beta) d beta`. The heat equation, followed by two integrations by parts and the Dirichlet boundary values, makes its derivative `-H_beta(t;alpha,0)/2`. Its negative derivative is the nonnegative density of a left exit. Using `h_1(beta)=beta/ell` gives the right flux. Continuity of Brownian paths excludes an atom at zero for an interior start; bounded-interval exit is almost surely finite, so these densities account for all mass. Bounded optional stopping for the stopped coordinate gives masses `1-alpha/ell` and `alpha/ell`.

The two hyperbolic-sine Laplace transforms also solve the boundary-value problem `u''/2=s*u` with the stated endpoints. A stopped exponential martingale and bounded convergence identify them with the respective exit transforms. No missing diffusivity factor is apparent. In particular, the total mean exit time is `alpha*(ell-alpha)`.

I inspected Lalley's Exercise6 eigenfunction-expansion discussion and the actual Mörters--Peres Theorem2.16 and proof on printed pp.43--44. The strong-Markov theorem requires an almost surely finite stopping time, a condition satisfied at every stage here. The preliminary shared extraction beginning at printed46 is not being used to verify that theorem.

Crucially, the later integrals use the **summed nonnegative kernels** as functions. They do not integrate the absolute values of their individual Fourier terms over all positive times, nor do they interchange an improper t-integral with the signed Fourier series. That otherwise plausible operation is not justified in general. As written, the candidate avoids it. The claimed absolute convergence applies to the outer Laplace series; it is not a claim of absolute convergence of an expanded multi-index Fourier sum after time integration.

## 3. Arbitrary finite targets and physically correlated clocks

Before the next first visit to the remaining target set A, the circle path is confined to the containing open arc. Any continuous lift is a Brownian interval path until it leaves that arc, and only the two arc endpoints can be the next target. The lift's integer offset has no effect. If A is a singleton, both endpoints correspond to the same circle point and **both** exit densities must be added. This essential case is present.

After the first target is reached, removing it from A makes it ordinary traversable territory. The path may revisit it arbitrarily often. It is not killed by other seeds, other walkers, or earlier ownership. Removing newly visited test points therefore decomposes the genuine uninterrupted circle path rather than altering the model.

The successive times of first reaching a still-unvisited target are stopping times. At each fixed configuration, distinct target points have positive separation, so their first visits cannot coincide, and each interval-exit time is finite. The strong Markov property successively yields the product subdensity in (7) for a specified order. It is a subdensity for the entire order event, not a conditional product obtained by incorrectly conditioning on future visits. Summing all orders gives total mass one by iteration of the next-target normalization. Impossible permutations have a zero factor. No hidden winding variable or unvisited-target condition is discarded.

For each walker, the physical time of reaching query j equals the **sum of all preceding increments in that walker's own target order**. Equation(9) uses this sum. Equation(10) compares the physical sums across independent walkers. Thus it retains the substantial dependence among hitting times belonging to one walker. Raw increments or independent copies of the individual first-hit clocks would be wrong.

The equality of two walkers' reconstructed times is a proper hyperplane: the positive increment variables of the two different walker rows occur on different sides. The full product density is absolutely continuous, so these equality boundaries have zero probability. Off the boundaries there is exactly one winner at every query. For fixed queries, singleton hitting times are atomless and independent across walkers, giving the same tie conclusion without relying on the hyperplane argument.

I added an independent exact continuous-time finite-cycle diagnostic. Its oracle solves the global Feynman--Kac equations on `(remaining target set, current site)` without enumerating target permutations. A second calculation sums permutation products of killed-walk resolvents with the cumulative-time weights in the candidate. These agree in **2,052** configurations, spanning cycle sizes3--7, up to4 targets, irregular placements, every eligible start, all-zero, partially-zero, and unequal positive transform rates. Every rational linear-system solution has its residual checked.

The diagnostic explicitly rejects two realistic errors. For cycle size7, targets `(1,4,5)`, start0 and rates `(1/3,2/5,3/7)`, the correct transform is `175662828236626125/22107849816831252929`. Weighting only the next increment gives `343377212835161/9901266583585520`; multiplying single-target independent clock transforms gives `1057875/123545423`. Both differ exactly. A two-walker increment example also reverses the ownership labels if raw increments replace cumulative times. These are falsifying controls for incorrect substitutes, not empirical evidence of a Brownian limit.

## 4. Measurability, Tonelli and the outer bound

On continuous-path space, the range up to a fixed time is compact. Its distance from a query point equals the infimum of continuous distance functions at a countable dense set of times, together with the endpoint. The condition that this distance vanishes is precisely that the point was hit by that time. This establishes joint path/point measurability of first-hit times and hence of the least-index ownership indicator.

For each fixed point outside the finite seed set, all first-hit times are finite and the times belonging to distinct independent walkers tie with probability zero. Fubini applied to the nonnegative exceptional-set indicator gives an almost surely null exceptional spatial set. No false claim of absence of ties simultaneously at every circle point is needed. The cell measures are measurable, nonnegative, and sum to one almost surely.

Coincident query coordinates or queries at seeds lie on a finite union of zero-measure diagonals in the spatial moment integrals. Removing them is valid. Pointwise formulas for repeated query points would require grouping those targets; they are not being asserted. As two distinct queries approach each other, individual kernels need not admit uniform pointwise bounds. This creates no integrability gap: their summed ownership probability is at most one at every admissible configuration. Tonelli applies to the nonnegative summed kernels, then to the spatial integral.

For nonnegative theta, `Z=sum(theta_i*L_i)` lies between zero and `theta_*=max(theta_i)`. Expanding its mth power as a product of spatial integrals and using Tonelli proves exactly `E[Z^m]=M_m`. The bound `M_m<=theta_*^m` follows before any Fourier interchange. The sum of the absolute outer terms is at most `exp(theta_*)`, so averaging the exponential series is legitimate.

Taylor's integral or mean-value remainder for `exp(-z)` on nonnegative z has derivative magnitude at most one. Thus the remainder after degree M is at most `z^(M+1)/(M+1)!`, and taking expectation gives the submitted uniform bound without an extra exponential factor. It certifies neither a particular quadrature nor a uniform inner-kernel truncation; the submission correctly says so.

## 5. Mixed moments and uniqueness

For a multi-index nu of total degree m, the coefficient of `theta^nu` in `M_m(theta)` is

    m! / product(nu_i!) * E[ product(L_i^nu_i) ].

Hence the displayed homogeneous polynomials determine all mixed moments; their values on the nonnegative orthant determine the polynomial coefficients uniquely. Alternatively, compact support justifies differentiating the transform at zero, with derivative `(-1)^m` times the mixed moment. Access only to nonnegative real theta is sufficient; bounded support supplies the unique entire extension and the one-sided derivatives agree with those derivatives.

The coordinates and constants form an algebra separating points of the compact simplex. Stone--Weierstrass makes its polynomials dense in all continuous functions. Equality of these moments therefore implies equality of integrals against all continuous functions, which uniquely identifies a finite Borel measure. This is actual joint-law determinacy, not merely separate marginal determinacy.

The new checker independently extracts every mixed coefficient through total degree6 from a finite probability space with three labels, correlated owner patterns, and unequal spatial piece lengths `(1/7,2/7,4/7)`. It verifies the multinomial factor, partially-zero and all-zero theta, all-equal theta, direct moment evaluation, and the uniform bound. This test would catch a missing factorial or a product-of-marginals substitution; it is supplementary to the continuum proof.

## 6. Boundary and symmetry checks

* k=1: all query owners are label1; the normalized query densities give `M_m=theta_1^m`, and the transform is `exp(-theta_1)`.
* k=2: both possible target orders and both directions around a singleton are included; no independence between one walker's two target clocks is introduced.
* Zero theta coordinates cause no singularity. All theta zero gives transform1; all theta equal t gives `M_m=t^m` and transform `exp(-t)`.
* Fixed distinct irregular seeds need no symmetry. All finite-target and bounded-support arguments remain valid. Seeds arbitrarily close together do not affect the uniform outer remainder.
* Independent uniform seeds are integrated over the full labeled product circle. Coincident seeds are a null set. The bound independent of p permits integration of the absolute outer series. Circularly sorted labels are a different start law and are explicitly distinguished.
* Equidistant seeds have cyclic and dihedral label symmetry. For k>=4 these symmetries are smaller than full label permutation symmetry; the candidate does not assert the latter.
* Circumference and a common Brownian diffusivity only rescale space/time as stated. Distinct per-walker diffusivities would change winners and are not part of this theorem.

## 7. Reproduction, limitations and outcome

The original author program reproduces all **8,520** checks with stdout SHA256 `fbb17a6dc53c17794d28c5941f2060d4d43c9638c5ad70cd7da3bd70d4c11ab1`, byte-identical to the previous receipt. The old independent program reproduces its **46,056** checks and the same semantic receipt. The new checker passes **11,777** exact checks both normally and with Python optimization enabled. Four bounded child processes exited zero, were reaped, and had absent process groups; the actual PID/time/output custody is retained in `CHILD_JOURNAL.json`.

The original author's `ck` uses Python `assert`, which disappears under `python -O`. Normal reproduction is what was promised and tested, so this is not a defect in the Brownian theorem. For a later verification package I recommend replacing that diagnostic guard with an explicit exception or documenting that it must run without optimization, so an optimized receipt cannot imply checks were executed. The new controls use explicit exceptions and survive optimization. This is a verification-package hardening suggestion, not a mathematical correction.

The finite-state controls do not prove convergence of discrete walks to the Brownian ownership law, and no such convergence argument is claimed. The theorem is established by the direct continuum kernel, stopping-time, nonnegative integration, and compact-support arguments above. I found no circular central lemma, hidden stopping/coalescence modification, or unsupported interchange.

**Mandatory mathematical corrections: none.** Priority remains a separate task. The supported outcome is the complete explicitly stated analytic-transform characterization; no efficient algorithm, named density, exhaustive novelty conclusion, or publication approval follows from this review alone.
