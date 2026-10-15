# Independent derivation before inherited verdicts

This file records the reviewer’s reconstruction after reading the complete mathematical report and before reading MATHEMATICAL_AUDIT, STATUS, README, SOURCE_METADATA, or MANIFEST. The report’s claims are hypotheses. Independent primary-source scope checks follow separately. No numerical experiment is used as a premise.

## Exact hypothesis and checks

Let n=m+1≥2, H={y>0}, β>0. The form on H¹(Ω) is q[u]=∫Ω|∇u|²−β∫∂Ω|u|². For the nongraph statements Ω is connected with C∞ boundary, Ω△H bounded, Ω≠H. Success means: prove the form realization is well-defined, prove essential spectrum exactly [−β²,∞), establish a negative shifted form trial for every such Ω when m=1,2, and establish an all-function nonnegative shifted form certificate for every compact Lipschitz graph when m≥3 at small β. The explicit graph must satisfy the certificate at β=1, without any numerical premise. The exact conclusion is absence of spectrum below the threshold; equality of spectrum with essential spectrum does not exclude embedded eigenvalues.

Boundary cases include overhangs, cavities, several boundary components, flat Ω, the critical m=2 logarithmic cutoff, any fixed graph with very large slope, large β, and the distinction between a prescribed β with a geometry chosen afterwards and a single geometry with all β.

## Closed realization and essential spectrum

All geometric deviations and all nonflat boundary lie in a sufficiently large compact set. A finite smooth-boundary cover there and the flat trace estimate elsewhere give ∥Tr u∥²≤ε∥∇u∥²+Cε∥u∥². Taking βε<1 proves semiboundedness and a shifted coercive form norm equivalent to H¹. The trace term is bounded in that norm, hence q is closed. The same argument applies to a globally Lipschitz compact graph. Smooth functions compactly supported on the closure are dense in the smooth case by boundary flattening, partition of unity, and truncation; the Lipschitz graph follows by a bi-Lipschitz flattening and H¹ density on H.

For the flat half-space, integrating ∂y|u|² gives

qH[u]+β²∥u∥²=∥∇x u∥²+∥∂y u+βu∥².

Thus the lower threshold is −β². Take a smooth partition χ²+ζ²=1 with χ compactly supported and ζ zero on a whole neighborhood of the geometrical change. The product ζu extends as a member of H¹(H) because it vanishes near any mismatch of the domains. Its shifted flat form is nonnegative. IMS and semiboundedness of the compact part then imply QΩ[u]≥−C∫K|u|² for fixed bounded K.

If λ<−β² were essential, a normalized weakly null operator Weyl sequence has q[u_j]→λ. The trace coercivity gives bounded H¹ norms. Local compactness (finite smooth/Lipschitz charts) gives ∫K|u_j|²→0, contradicting Q[u_j]→λ+β²<0. This argument gives no essential spectrum below −β² and does not assume a compact resolvent for the full domain.

For every k∈R^m, let η∈C∞c(R^m) have L² norm one, take η_R(x)=R^(−m/2)η((x−a_R)/R), and choose a_R so its support eventually escapes every compact set and is disjoint from the projection of the deformation. Put u_R=(2β)^(1/2)η_R(x)e^(ik·x)e^(−βy) on its flat supported part and zero elsewhere. It lies in H¹, has norm one, and satisfies the Robin condition on y=0. More directly, integration by parts against all H¹ test functions shows q[u_R,v]=⟨−Δu_R,v⟩, so u_R is in the operator domain without assuming an unproved global H²-domain characterization. The residual at λ=|k|²−β² is the tangential term −e^(ik·x)(Δη_R+2ik·∇η_R), of norm O(R^(−2))+O(|k|R^(−1)). Weak escape supplies the Weyl criterion. Since |k|² spans [0,∞), the essential spectrum is precisely [−β²,∞). Spectrum strictly below it consists of isolated finite-multiplicity eigenvalues, possibly accumulating only at −β².

## Ground-state identity and nongraph binding

Set φ=e^(−βy). Then Δφ=β²φ, ∂νφ=−βν_yφ. Expansion of |∇(φv)|² and integration of div(φ∇φ|v|²) yield

Q[φv]=∫Ωφ²|∇v|²−β∫∂Ω(1+ν_y)φ²|v|².

For complex v take real parts. Crucially ν_y∈[−1,1], independently of whether the boundary is a graph, and the flat lower plane has ν_y=−1. The boundary coefficient is nonnegative; on an upper-facing part or an obstacle it can be strictly positive. No coordinate parametrization is needed.

Bβ=∫∂Ω(1+ν_y)e^(−2βy) is finite by compact support of the nonflat part and finite smooth-chart cover. If Bβ=0, continuity of the nonnegative integrand forces ν=−e_y at every boundary point. Each boundary component is locally a horizontal plane; connectedness gives one height per component. It is both relatively open in that plane and closed in R^n (a connected component of the closed boundary is closed), hence is the whole horizontal plane. Any such plane at height c≠0 contradicts compact agreement with ∂H; the y=0 plane must be present at infinity. Thus ∂Ω={y=0}. The only connected open set with this boundary and agreement with H outside a compact set is H. Contradiction: Bβ>0 for Ω≠H. This excludes the possible loophole of nonflat geometry somehow retaining normal −e_y everywhere.

Choose R₀ strictly larger than the projection of all geometric changes and ψ compactly supported in x, equal to one on a neighborhood of B_R₀. Since Ω differs from H only in a bounded set, Ω is bounded below. Thus u=φψ∈H¹. Multiply by a vertical cutoff equal to one below height T, with bounded derivative and zero above T+1. Once T exceeds the deformation, the tail is flat and every cutoff error is O(e^(−2βT)); the identity passes to u. On support of ∇ψ the exact vertical fiber is (0,∞), even if other fibers have multiple intervals. Consequently

Q[u]=(1/(2β))∫R^m|∇ψ|²−βBβ.

For m=1 the two linear taper intervals of length L give energy 2/L. For m=2 the radial logarithmic taper from R₀ to R gives energy 2π/log(R/R₀). Both approach zero while the negative term is fixed. Choose the energy below 2β²Bβ. This yields Q[u]<0, hence a discrete eigenvalue below −β² by the established essential spectrum and min–max. The proof handles connected domains with overhangs and compact obstacle boundary components, without graph assumptions or Robin conditions on form trials.

## All-function graph absence, independently checked

Let f∈W¹,∞c(R^m), m≥3, Ωf={y>f(x)}, K=supp f⊂B_R, M=∥f∥∞, G=∥∇f∥∞, D=√(1+G²)−1, A=4R²/(m−2)², c=1/[2(1+G²)]. For a compact-support flattened core write u(x,t+f(x))=e^(−β(t+f(x)))w(x,t). Chain rule yields bulk weighted energy |∇x w−∇f wt|²+|wt|², and vertical integration of the cross term leaves the boundary defect −βe^(−2βf)(√(1+|∇f|²)−1)|w(x,0)|². This is an identity for the full core, not merely a transverse-mode trial family.

Tangential Hardy gives L_K≤A E_x, where L_K=∫K×R+e^(−2βt)|w|² and E_x,E_t are the weighted derivative energies. Integrating ∂t(e^(−2βt)|w|²) over t gives T_K≤2βL_K+2√(L_K E_t)≤2βAE_x+2√(AE_xE_t)≤(2βA+√A)(E_x+E_t). The sign of the derivative term and the factor two are correct.

Pointwise |a|²+|b|²≤2|a−gb|²+(2G²+1)|b|²≤2(1+G²)(|a−gb|²+|b|²). Bounding the f weight from below in the bulk and from above in the defect therefore gives

Q[u]≥[e^(−2βM)c−βe^(2βM)D(2βA+√A)](E_x+E_t).

The bracket is nonnegative when βD e^(4βM)(2βA+√A)≤c. The map and inverse are bounded on each compact support; extension to every H¹ form function uses density and continuity of q, not boundedness of the globally growing multiplier e^(βy) on H¹. For any fixed f, the left side tends to zero as β↓0, and is continuous and increasing in β≥0, so an interval (0,β₀] exists. With essential spectrum this proves σ=σess=[−β²,∞), while allowing the logical possibility of point spectrum embedded in that interval.

## Exact counterexample and coupling quantifiers

For h=e^(−1/(1−r²)) on r<1, zero outside, standard flatness of e^(−1/s) at s=0 proves h is C∞. It is nonzero. Set f=h/100. With q=(1−r²)^(−1)≥1, |∇h|=2r q²e^(−q)≤2q²e^(−q)≤8/e²<2. Thus M<1/100, G<1/50, D≤G²/2<1/5000. At β=1, R=1 and m≥3, A≤4. Then 2A+√A≤10, e^(4M)<e^(1/25)<2, so the certificate’s left side is <1/250, whereas c>1/3. The gap is positive by exact rational inequalities. The graph is connected and smooth, and (x,t)↦(x,t+f(x)) is a global diffeomorphism H→Ωf. It differs from H only in {|x|≤1, |y|≤1/100}, a bounded set. In n=4 this disproves universal binding at β=1.

At prescribed β*>0, choosing f=εh makes M=O(ε), G=O(ε), D=O(ε²), while c→1/2. Hence the absence certificate holds for positive sufficiently small ε. This establishes ∀β*>0 ∃nonzero f absence at β*, not ∃nonzero f ∀β>0 absence. Nothing here classifies arbitrary nongraph domains in n≥4, proves absence at large β, or establishes novelty.

## Provisional independent result

No mathematical falsification found in the full report. The strongest reconstructed scope is exactly the two stated theorems plus the explicit counterexample. Primary-source attribution and all six-file consistency still require review. A small terminology caveat: “coordinate-free” for an identity explicitly using the preferred half-space direction means no boundary chart or graph coordinates; it is not invariant under choosing an unrelated direction. This wording does not affect the proof.
