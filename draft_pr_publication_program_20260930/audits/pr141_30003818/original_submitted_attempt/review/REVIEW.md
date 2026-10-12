# Independent review of the Brownian first-visit joint law

**Verdict: PASS_COMPLETE_EXPLICIT_TRANSFORM_LAW.** No mandatory mathematical correction was found. The candidate gives the complete finite-k joint law in the explicitly claimed analytic-transform format, for both independent uniform and equidistant starts. This is an independent adversarial AI audit, not human peer review. Priority remains unestablished.

Frozen `JOINT_LAW.md` SHA-256:
`f5445282b2044937620acd7f273e9ac21ac0dae0b42edd1050ced91e2a29fddf`.

## 1. The source asks for this finite-k distribution

I independently read the complete [OWR report](https://ems.press/content/serial-article-files/46745) and inspected the rendered original printed p. 1452. Georgakopoulos asks for the joint Lebesgue measures of first-visit cells of independent Brownian particles, with uniform random or equidistant seeds. There is no large-k limit, prescribed named distribution, density requirement, or computational-complexity bound in the question.

An explicit multivariate Laplace transform uniquely determining the whole probability measure therefore meets the literal distribution request, provided its coefficients really have been reduced to specified analytic quantities. They have: each coefficient in the submission is a finite sum of finite-dimensional deterministic integrals of the displayed interval kernels, with fully specified linear hitting-time inequalities. No unknown ownership probability or unevaluated path expectation remains as a definition of those coefficients.

The answer deliberately uses total circle length one. The source's possible geometric circumference convention is recovered by multiplying the output lengths by that circumference, or scaling the transform variables. Brownian spatial scaling changes all time clocks by the same factor; common time rescaling preserves all first-arrival comparisons. This is a valid normalization rather than a change of model.

## 2. Physical ownership and measurable cell lengths

The candidate compares the absolute first hitting times T_i(x) of each point by each walker. Walkers continue through other seeds, previously visited territory, and encounters with other walkers. They are neither stopped nor coalesced by those events. This is exactly the source's physical first-arrival rule.

The measurability argument is correct. For fixed t, the distance of x from a continuous path's range up to t is the infimum of its distances at a countable dense set of times, with the endpoint included. Compactness of that path range makes distance zero equivalent to having been visited. Thus the events T_i(x)≤t, and hence the joint path/point hitting-time map, are measurable.

For fixed x outside the finite seed set, singleton-circle hitting times are finite and atomless. Conditional on fixed seeds, the k hitting times are independent. Their ties therefore have probability zero. Fubini upgrades this pointwise statement to the required assertion that the exceptional set of spatial points has Lebesgue measure zero almost surely. No claim that ties are absent simultaneously at every spatial point is needed. The least-index convention supplies a measurable version, and the resulting lengths are nonnegative and sum to one.

## 3. Interval kernels: signs, diffusivity and improper-integral safety

[Lalley's primary notes](https://galton.uchicago.edu/~lalley/Courses/312/BrownianMotion312.pdf), Exercise 6(A)–(C), give the killed unit-interval sine expansion with eigenvalues n²π²/2. Spatial and temporal scaling yields the submitted kernel H with the 2/ell prefactor and generator one-half the second derivative.

I independently checked both outward-flux signs. If h_0(y)=1−y/ell, then

    P_alpha(tau>t, exit at 0)=∫ H(t;alpha,y) h_0(y)dy.

Using the heat equation and the zero boundary values gives its derivative −H_y(t;alpha,0)/2. The left-exit density is consequently +H_y/2 at zero. The right-exit density is −H_y/2 at ell. Differentiating the sine expansion produces exactly the π/ell² prefactors and the right-end sign (−1)^(n+1) in equation (2).

The kernel series and their differentiated series converge absolutely and locally uniformly when t stays positive. Positivity and total masses follow from their probability-density interpretation and bounded optional stopping, not from a potentially invalid termwise integration of the signed Fourier series down to t=0. The hyperbolic-sine Laplace transforms independently solve u''/2=su with the correct endpoint data. The normalization is consistent; in particular the total mean exit time is alpha(ell−alpha), with no missing factor of two.

The later time integrals use these **summed nonnegative kernels**. The candidate never interchanges the improper time integral with a signed Fourier expansion term by term. This distinction removes a potential convergence gap.

## 4. The finite-target recursion uses the right absorbing set

For a finite remaining target set A and a current position outside A, Brownian motion stays in the containing open arc until its next visit to A. Lifting that arc gives an ordinary interval. Only its endpoints can be the next target. If A is a singleton, both endpoints of the lifted interval represent the same circle point, so the correct kernel is the sum of both exit fluxes. The submission explicitly includes this essential case.

After a new target has been hit, it is removed from A. It becomes ordinary traversable territory for every later stage of that walker's calculation. This is an auxiliary stopping-time decomposition of an unstopped Brownian path; it does not create an absorbing cell boundary in the original process. The winding history of a lift is immaterial, since the future circle process is determined by its circle position.

The stopping times are finite. Distinct targets have positive separation in each fixed configuration, so successive first visits cannot occur at the same time. Applying the strong Markov property successively gives the product density D_i^pi. I checked the exact finite-stopping-time statement in [Mörters–Peres, Theorem 2.16](https://www.mi.uni-koeln.de/~moerters/book/book.pdf). Summing over the possible next endpoints at every stage gives total density mass one. Impossible permutations correctly acquire a zero kernel factor.

All query points are distinct and avoid the seeds in this calculation. Repeated query coordinates, or a query exactly at a seed, lie on a finite union of zero-Lebesgue-measure diagonals in the later moment integrals. Discarding them is therefore legitimate for the joint length law. There is no assertion that a nonsingular hitting-time density exists for repeated targets. Such pointwise queries would require grouping repeated coordinates, but the theorem does not need or claim that additional formula.

## 5. Ordering increments does not replace physical hitting times

For each walker, equation (9) reconstructs the physical hitting time of target j as the sum of all preceding increments in that walker's own target order. Equation (10) then compares these reconstructed sums **across walkers**. This preserves both the dependence of different target hitting times of one walker and the independence between different walkers.

The ownership regions are finite systems of strict linear inequalities. Every tie boundary is a proper hyperplane in the full increment variables, because it compares variables from distinct walker rows. The product density is absolutely continuous on the positive orthant, so these boundaries have zero mass. Away from them exactly one label vector owns all test targets. This proves equation (12) and the bound 0≤Q_a≤1, including total normalization over labels.

Comparing raw increments instead of cumulative times would be wrong, as would treating one walker's target hitting times as independent clocks. Neither error occurs in the candidate.

## 6. Full transform, absolute convergence and error bound

Let Z=Σ_i theta_i L_i for theta_i≥0. The partition identity gives 0≤Z≤theta_*, where theta_*=max_i theta_i. Tonelli applied to the m-fold spatial integral gives

    E[Z^m]=∫ sum_a (product_j theta_(a_j)) Q_a(x;p) dx=M_m.

Every Q_a is already the deterministic integral in equation (11), so this moment identity is a proof of the explicit coefficient formula, not an unresolved probabilistic prescription.

The absolute series is bounded by Σ_m theta_*^m/m!=exp(theta_*), justifying the expectation/series interchange. Taylor's theorem for exp(−z) on z≥0 gives the stronger remainder bound

    |remainder after degree M|≤z^(M+1)/(M+1)!.

Its derivatives have absolute value at most one on the relevant interval. Taking expectation yields the stated uniform factorial bound without an extra exponential factor. This bound concerns the outer transform series only; the author correctly disclaims a certified quadrature or inner-Fourier truncation algorithm.

The transform determines every mixed moment. Bounded support justifies differentiation at zero, or equivalently coefficient extraction from the homogeneous polynomials M_m. Polynomial functions separate points on the compact simplex and are dense in its continuous functions. Hence the full probability measure is uniquely determined. A named density is unnecessary for this claim.

## 7. The two initial-position laws and symmetry

Equidistant starts use p_i=(i−1)/k, with common rotation irrelevant. The resulting labeled law has cyclic and dihedral symmetry; the candidate does not incorrectly assert full permutation exchangeability.

For independent uniform starts, conditioning on p and integrating over T^k gives equation (16). The same uniform coefficient and remainder bounds justify every interchange. Coincident seeds form a null set. If labels were assigned by circular sorting instead, the fixed-p formula remains valid and must be integrated against that different seed law; the candidate states this distinction explicitly.

The checks k=1, all theta_i equal, and E[L_i]=1/k are consistent with these symmetries. The one-query reduction is the ordinary competing-clock integral, while the higher-query formula retains the essential within-walker correlations.

## 8. Reproducibility and independent controls

All **8,520 submitted assertions** replayed byte-identically. The receipt SHA-256 is `fbb17a6dc53c17794d28c5941f2060d4d43c9638c5ad70cd7da3bd70d4c11ab1`.

The separate checker passes **46,056 independent exact assertions**. It compares the exit Laplace transform's formal hyperbolic-sine quotient with an independently solved polynomial ODE recurrence; verifies normalization and mean-exit-time scaling; enumerates complete target-order weights for rational circle configurations through six targets; checks the singleton two-endpoint rule; reconstructs physical arrival times and verifies ownership-region partitions; and tests the factorial envelope using certified rational bounds for the exponential.

These are finite diagnostics of the formulas. They do not prove the Brownian law through a random-walk simulation, and do not substitute for the strong-Markov, measurability and integration arguments above.

## 9. Final verdict

The exact finite-k joint transform and its deterministic coefficient formula pass. No revision of the frozen mathematical snapshot is required. The verdict covers both requested seed laws and the claimed fixed-seed extension, under the declared circle-length normalization. It does not claim a simple density, efficient numerical evaluation, optimal complexity, new probabilistic ingredients, or established historical priority.
