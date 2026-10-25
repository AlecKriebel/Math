# Independent analytic check of the complete literal theorem

This reconstruction uses the whole seven-page PDF and all 449 lines of the deposited controlling TeX. Its substantive mechanism was sealed at 08:01:43 UTC before foreign primary bodies or archived/current scientific opinions. The following expands that same mechanism. It does not substitute a restricted theorem.

For every compact E contained in [0,1], put F=R\E and S₂={|z|=2}. The claim is Mod₂Γ(E,S₂)>0 ⇒ Mod₂Γ(E,F)=∞. The modulus is the infimum of planar squared-density energy. Densities are actual extended nonnegative Borel functions, with admissibility on every connector. Connectors are continuous with endpoint limits and locally rectifiable off the endpoints, and their integral is the increasing interior-subcurve integral, counting multiplicity. There is no avoidance condition on intermediate plate or axis contacts. The same proof covers the separate globally rectifiable convention if used in both families.

Suppose the target modulus is finite. The definition of an infimum supplies one finite-energy admissible density ρ; an attained extremum is unnecessary. For E empty the other modulus is already zero. Assume E nonempty.

**Pointwise majorization and the actual potential.** On Q=[−2,3]×[−2,2], h=ρ² is integrable. Choose relatively open Oₖ containing {h>2ᵏ}, with excess area at most 2^(−2k−4), and set H=1+Σ2^(k+1)1_Oₖ and g=√H. Increasing sums of open indicators are lower semicontinuous. Dyadic summation gives H≥h pointwise, including h=∞, and ∫g²≤|Q|+4∫h+1/4. This retains the density's actual values on area-zero sets; replacement only almost everywhere would not suffice for every-curve admissibility.

Let d(z) be the infimum of g-costs of globally rectifiable paths in Q starting in E and ending at z, and u=min(1,d). Constant paths give d=0 on E. Weighted length for continuous a≥0 is the supremum of partition sums of minimum weight times chord length; uniform continuity of a and refinement of chord sums give equality with weighted variation. Each partition functional is continuous in the uniform curve topology. For lower semicontinuous g, increasing continuous capped infimal convolutions aₘ(x)=min(m,inf_y(g(y)+m|x−y|)) converge pointwise to g, including infinite values. Thus g-weighted length is lower semicontinuous.

If zⱼ→z and liminf d(zⱼ)<∞, near-minimal paths have bounded Euclidean lengths because g≥1. Constant-speed parametrization gives a common Lipschitz bound. Arzelà–Ascoli in compact Q, compactness of E, and weighted lower semicontinuity give d(z)≤liminf d(zⱼ). Hence the actual d and u are Borel. Concatenation and reversal give |u(x)−u(y)|≤∫βg for every rectifiable β joining them. If one distance is infinite, any finite-cost connecting path would force both finite; if both are infinite both truncations equal one. These cases do not require subtraction of infinities.

Fubini and Cauchy–Schwarz make g integrable on almost every coordinate line. The inequality on all subsegments proves absolute continuity of the actual u on each such line. Slice integration by parts identifies weak derivatives and gives |∇u|²≤2g². Thus u belongs to W¹,²(int Q). Every auxiliary E-to-F path is an original connector, so admissibility gives u=1 on F∩Q; u=0 on E. These are actual point values, not a Sobolev representative assigned after construction.

**Trace and length zero.** Choose a smooth cutoff η supported in int Q and equal to one near [0,1] on the axis. The zero extension of w=η(1−u) belongs to W¹,²(R²), is compactly supported, and has actual almost-everywhere vertical absolute-continuity trace f=1_E. No assertion about capacity of the exceptional vertical lines is used.

For smooth w, horizontal Fourier transformation and integration of ∂y|W(ξ,y)|² in the upper half-plane give |ξ||f̂(ξ)|²≤∫₀∞(ξ²|W|²+|∂yW|²)dy. Integration in ξ and Plancherel give ∫|ξ||f̂|²≤∫_{y>0}|∇w|². There is no division by ξ at zero. For general w, compactly supported mollifications converge in W¹,². The vertical estimate |v(x,0)|²≤∫₀∞(|v|²+|∂yv|²)dy proves L² convergence to the actual trace; Plancherel, a subsequence and Fatou extend the Fourier bound. Tonelli and t=ξh then give

∫_R ‖f(·+h)−f‖²₂ dh/h² = C∫_R |ξ||f̂(ξ)|²dξ <∞,

where C=∫|e^{it}−1|²dt/t² is finite and positive.

For 0<h<1, N=ceil(2/h)≤3/h makes f and its Nh translate disjointly supported. Telescoping translations in L¹ yields 2|E|≤N‖f(·+h)−f‖₁. For an indicator the latter norm equals the squared L² norm, which is therefore at least (2/3)|E|h. The critical integral diverges logarithmically unless |E|=0. This proves only length zero: a compact null set may still have positive outer conformal capacity.

**The null-set step at every actual endpoint.** Put q=ρ+1_{B(0,3)}, which is still finite-energy and admissible for E-to-F connectors. Suppose one E-to-S₂ connector from an arbitrary e∈E has finite q-cost. Stop at its first hit of S₂. On the preceding image q≥1, so bounded lengths of interior subcurves and endpoint continuity imply finite total variation including the endpoints. It has a global arclength parametrization after constant portions are removed; q∘γ is integrable. This handles the originally permitted infinite-length endpoint behavior without discarding any curve.

For this fixed e, A_e(r)=∫_{|z−e|=r}q²ds satisfies ∫₀δA_e(r)dr<∞ by polar integration. Since |E|=0, e+r∈F for almost every positive r. There are decreasing good radii rⱼ→0 with rⱼA_e(rⱼ)→0: otherwise a positive lower bound on good radii would force divergence of ∫dr/r. This selection holds separately for every e, with no exceptional endpoint set.

Let tⱼ be the first exit arclength from B(e,rⱼ). Every positive initial arclength interval is nonconstant, so tⱼ→0 even if the curve returns, retraces, or winds. Absolute continuity of the finite integral makes its initial cost tend to zero. Join its exit point to e+rⱼ∈F by a circle arc. The added cost is at most √(2πrⱼA_e(rⱼ)), also tending to zero. The concatenation is an actual globally rectifiable E-to-F connector of cost eventually less than one, contradicting admissibility. Intermediate plate contacts are allowed by the original definition.

Consequently every E-to-S₂ connector has infinite q-cost. For every integer n≥1, q/n is admissible on the whole family and has energy n⁻²∫q²→0. Thus Mod₂Γ(E,S₂)=0. The contrapositive proves the complete original implication, including the null positive-capacity case, under each consistently used curve convention.

No central unsupported assertion was detected. Ordinary outer regularity, Fubini/Tonelli, Cauchy–Schwarz, absolute continuity, Arzelà–Ascoli, Euclidean Sobolev mollification and Plancherel are the foundational interfaces. Numerical checks cannot establish this universal theorem; the proof is analytic. Other source conventions (weak admissibility, plate-avoiding curves, planar complement, or reciprocal extremal length) are outside the literal theorem and are not silently substituted.
