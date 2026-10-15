# Independent derivation before consulting prior labels

Frozen head: `5e23f0c801d23976830657d2eef2b32bdc7da05a`. This note was written after reading the entire frozen report and before opening the prior audit, source metadata, README, or STATUS. The report's introductory accepted label is disregarded as evidence. Scope: full Theorems A/B, explicit counterexample, essential spectrum, and the exact original target (original target to be authenticated next).

## Primary adversarial family: Hardy/weighted-trace/global absence

Let m≥3, K⊂closed B_R, a₀=(m−2)/2, pδ=x/(r²+δ²). For a compactly supported smooth complex a,

∫|∇a|² ≥ a₀∫(div pδ−a₀|pδ|²)|a|²
=∫[a₀²r²+a₀mδ²]/(r²+δ²)² |a|²
≥a₀²∫r²/(r²+δ²)² |a|².

The integration by parts uses Re(ā∇a)=∇|a|²/2 and has no boundary term. Fatou at r≠0 proves the ordinary tangential Hardy bound. On closed B_R, r²≤R² almost everywhere; the origin is null, so inclusion of the boundary r=R causes no failure. A=4R²/(m−2)² yields ∫K|a|²≤A∫|∇a|². The same inequality holds on each slice and can be integrated with the nonnegative weight e^(−2βt).

For compactly supported w on the closure of the half-space, put L=∫K×R₊e^(−2βt)|w|², T=∫K|w(0)|², X=∫He^(−2βt)|∇xw|², Y=∫He^(−2βt)|wt|². The fundamental theorem applied to the weighted square gives

T=2βL−2Re∫K×R₊e^(−2βt)w̄wt.

Cauchy–Schwarz gives T≤2βAX+2√(AXY)≤(2βA+√A)(X+Y). This does not impose Robin boundary data on w. The hypothesis m≥3 enters exactly in a₀>0; zero-capacity cutoffs in m=1,2 would contradict the proposed homogeneous estimate in those dimensions.

Let g=∇f, y=t+f, u(x,t+f)=e^(−β(t+f))w(x,t). At fixed physical y, ∇xv=∇xw−g wt and vy=wt, where v=e^(βy)u. Expand the shifted form on a compact core. Its cross terms plus 2β²φ²|v|² equal −β∂y(φ²|v|²). The lower endpoint of each vertical fiber gives +βe^(−2βf)|w(0)|². Subtract the Robin boundary term βs e^(−2βf)|w(0)|² with s=√(1+|g|²). The exact identity is therefore

Q[u]=∫H e^(−2β(t+f))(|∇xw−g wt|²+|wt|²)−β∫e^(−2βf)(s−1)|w(0)|².

The tangential derivative βg that appears if differentiating u in flattened coordinates cancels when the physical gradient is formed; no extra term may be discarded. The flattening map has Jacobian 1, is bi-Lipschitz for f∈W¹,∞, and its graph surface measure is s dx. The boundary defect is nonnegative and supported in K.

The elementary estimate |a|²+|b|²≤2|a−gb|²+(2G²+1)|b|²≤2(1+G²)(|a−gb|²+|b|²) gives c=1/[2(1+G²)]. Hence

Q[u]≥[e^(−2βM)c−βe^(2βM)D(2βA+√A)](X+Y),

D=√(1+G²)−1. Thus βD e^(4βM)(2βA+√A)≤c is genuinely an all-functions sufficient absence criterion. To extend to all H¹ functions, approximate flattened u by compactly supported H¹ functions, apply the identity/estimate there, and use continuity of the original Robin form. Ordinary global multiplication by e^(βy) is neither bounded nor needed. For compact u the transformed w is compact and H¹; smooth w approximation yields the identity and trace estimate. Conversely the transformed compact smooth w yield a dense compact core after multiplying by e^(−β(t+f)). This settles the only plausible form-domain extension trap found so far.

For fixed f the criterion's left side tends to zero with β. Its coefficients are nonnegative and continuous for β≥0, so some interval (0,β₀] satisfies it. For f=0, D=0 gives the conclusion at every coupling. This proves graph absence below −β², subject only to the independently checked common essential-spectrum claim below.

For h=e^(−1/(1−r²)) on r<1, h=0 otherwise, every derivative at r=1 tends to zero because each is a finite sum of inverse powers of 1−r² times this exponential. Thus h is nonzero C∞ with compact support closed B₁. Put q=(1−r²)⁻¹≥1. |∇h|=2r q²e^(−q)≤2q²e^(−q)≤8/e²<2. For f=h/100: M<1/100, G<1/50, D≤G²/2<1/5000. At β=1 and m≥3, A≤4 and 2A+√A≤10. The elementary series bound e^x≤1/(1−x) for 0≤x<1 gives e^(4M)<25/24<2. Therefore the criterion's left side is <1/250 while c>1/3. This is a strict analytic certificate, with rational margin >247/750. No floating computation is needed. At arbitrary fixed β*, reducing ε in f=εh forces M,G,D to zero and gives a nonzero counterexample depending on β*.

## Independent full-scope cross-check

For the attractive form q=∫|∇u|²−β∫∂Ω|u|², integration by parts gives ∂νu=βu. On H, ν=−ey and e^(−βy) satisfies −uy=βu, so the threshold −β² has the correct sign.

For a connected smooth compact perturbation, the trace inequality from a finite atlas on the altered part plus the half-space tail yields relative form bound zero, closedness, and lower semiboundedness. Smoothness together with compact agreement excludes accumulating microscopic boundary components that would destroy a finite local Lipschitz atlas. Density of compact closure-smooth restrictions follows by local boundary extension, finite partition, truncation, and ordinary smoothing; graph density uses bi-Lipschitz flattening instead. No operator boundary condition is required for trial functions.

The half-space identity QH=∫|∇xu|²+∫|uy+βu|² is valid by integrating ∂y|u|². Localized χ,ζ with χ²+ζ²=1, compact χ, and ζ=0 around the full alteration give QΩ[u]≥−C∫K|u|². An operator Weyl sequence at λ<−β² has bounded H¹ norm by the relative trace bound, hence local L² mass vanishes by Rellich and weak convergence. This contradicts the displayed lower bound. For each λ=|k|²−β²≥−β², normalized tangential packets translated outside the perturbation and dilated to infinity, times √(2β)e^(−βy), satisfy the actual Robin boundary condition and have residual O(R⁻¹)+O(R⁻²); they prove membership in essential spectrum. Their support is entirely in the unaltered vertical fibers, including for nongraph domains. This proves σess=[−β²,∞) for both classes. All negative Q trials therefore imply discrete eigenvalues below this threshold, and graph absence implies equality of spectral sets with that interval. Equality of sets does not exclude embedded eigenvalues; the report does not make that stronger assertion.

For nongraph Ω let φ=e^(−βy). Direct completion by integration by parts gives Q[φv]=∫φ²|∇v|²−β∫∂Ω(1+νy)φ²|v|². Since νy≥−1, the boundary defect is nonnegative even on overhangs and compact obstacle boundaries. It has compact support and finite measure. If its integral B vanishes, ν=−ey everywhere by continuity. Each connected boundary component is locally horizontal, hence open in its containing horizontal plane; it is closed in Rn because it is a component of the closed boundary. It must be the full plane. Compact agreement at infinity leaves only y=0. Connectedness and agreement with H then force Ω=H. Thus B>0 for every stated nontrivial smooth Ω.

Choose a tangential ψ=1 on the projection of the altered region, and put u=φψ. Ω is bounded below; exponential decay makes u∈H¹, while upper truncation errors vanish. The support of ∇ψ lies on flat fibers, so Q[u]=(2β)⁻¹∫|∇ψ|²−βB. The one-dimensional linear cutoffs give 2/L→0; two-dimensional radial logarithmic cutoffs give 2π/log(R/R₀)→0. This proves Theorem A in ambient dimensions 2 and 3 without a graph restriction. In higher dimensions these energies do not tend to zero for a fixed positive-capacity ball, so this construction neither refutes nor substitutes for the Hardy absence argument.

## Provisional adversarial result

No material mathematical gap found in the complete report. Proofs independently reproduce the stated graph stability and exact m≥3 bump certificate as well as the full smooth nongraph n=2,3 binding claim. Original source wording, literature statements, package labels, member consistency, and executable exact guard controls remain to be checked. No novelty conclusion has been drawn. No historical audit has been consulted at this checkpoint.
