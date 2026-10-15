# Linking-family universal arguments and falsifiers

These are verification controls for the explicitly unresolved original PR34. They are not a new attempt to solve Ghomi's intended unit-binormal problem. None of the normal-field examples below is promoted to a binormal counterexample.

## 1. Continuous sections on an embedded curve

Let γ:S¹→R³ be a smooth embedding and V a continuous nowhere-zero field perpendicular to γ'. Compactness and the tubular-neighborhood theorem give a radius r>0 such that the normal-bundle map F(t,v)=γ(t)+v is injective when |v|<r. If M=max|V|, then every 0<ε<r/M gives a continuous embedded push-off ηε(t)=F(t,εV(t)), disjoint from γ. Distinct base parameters have distinct normal footpoints, and a nonzero normal vector never maps to the zero section. This proves the exact claim for continuous fields; smoothness of V is unnecessary for disjointness or topological linking.

For disjoint continuous oriented loops, the Gauss map (t,s)↦(η(s)−γ(t))/|η(s)−γ(t)| on the oriented torus has integer degree. This defines linking and agrees with the usual smooth Gauss integral and half the signed mixed-crossing sum. It also works for disjoint immersed cycles: individual self-intersections alone do not invalidate the Gauss map. Reversing one component negates linking; reversing both preserves it.

Positive continuous scaling V↦a(t)V preserves linking on an embedded center curve: choose ε small for the maximum norm throughout the positive interpolation and use F to obtain a disjoint homotopy. Normalization therefore preserves linking in this setting. It does not preserve injectivity of the field; that is a separate hypothesis, illustrated in §4.

For an immersion, uniqueness of normal footpoints fails. Here is an exact local obstruction: one straight branch is γ₁(s)=(s,0,0), with unit binormal B₁(s)=(0,sin s,cos s), and a distinct straight branch is γ₂(t)=(0,0,t). B₁ is orthogonal to both derivatives of γ₁, and is injective on a short interval. Nevertheless γ₁(0)+εB₁(0)=γ₂(ε) for every small ε>0. This is a local countermodel to an automatic immersed-curve tubular argument, not a full closed-curve counterexample satisfying all target hypotheses. A complete global target counterexample is neither constructed nor asserted.

## 2. Disk computation for framed unknots

Take γ(t)=(cos t,sin t,0), T=γ', N=γ'' the inward unit radial normal, and Z=(0,0,1). For integer m, the normal field Vₘ(t)=cos(mt)N(t)+sin(mt)Z is unit, normal, and periodic. Its ε push-off has radius 1−εcos(mt) and height εsin(mt), with 0<ε<1. It is embedded by its polar angle t, and disjoint from γ. For m≠0, its intersections with the oriented unit disk z=0 occur at mt∈πZ; only the |m| parameters with cos(mt)=1 lie inside the disk. The height derivative there is εm, so every intersection has sign sign(m). Thus linking is m. For m=0 the push-off is a concentric planar circle; moving it vertically in the complement gives linking 0. The exact twist density T·(Vₘ×Vₘ') is m, consistent with these signs and normalization.

These are genuine framed unknots, not admissible binormal candidates: Vₘ·γ''=cos(mt) is not identically zero for any m. On the circle, a continuous unit field orthogonal to both T and γ'' can only be constantly Z or −Z. It cannot be injective. An arbitrary framing cannot replace the binormal condition.

## 3. An exact zero-linking, nonzero-twist normal ribbon

Let η=1/20, h(t)=η(sin t+(sin 2t)/2), and γ(t)=(cos t,sin t,h(t)). This is a smooth embedded curve because its planar projection is the unit circle. Use the inward radial unit normal N(t)=(−cos t,−sin t,0), which is injective and perpendicular to γ'. Its small push-off has radius 1−ε and the same height h(t). Linking is zero by a direct disjoint homotopy: independently remove the heights of the two curves, maintaining their distinct fixed radii throughout. The resulting concentric planar circles have linking zero. No twist formula is needed for that topological computation.

Writing f(t)=cos t+cos 2t, the unit tangent is γ'/sqrt(1+η²f²), and

Tw(γ,N)=(1/(2π))∫₀²π ηf(t)/sqrt(1+η²f(t)²) dt.

The integrals ∫f=0 and ∫f³=3π/2 are exact. For x≥0, Taylor's theorem gives (1+x)^−1/2=1−x/2+R(x), with 0≤R(x)≤3x²/8, since its second derivative is 3(1+x)^−5/2/4. As |f|≤2, the remainder after integration and division by 2π has magnitude at most 12η⁵. Consequently

−3η³/8−12η⁵ ≤ Tw(γ,N) ≤ −3η³/8+12η⁵,

or exactly −81/1600000 ≤ Tw ≤ −69/1600000 <0. This is a rigorous geometric countermodel to inferring nonzero linking solely from nonzero twist or injective normal framing. It is **not** a counterexample to Ghomi: N·γ''=1, so N is not binormal. It is a verification falsifier, not an additional substantive target attempt or novel research claim.

The standard Călugăreanu identity for a smooth embedded ribbon gives Wr=−Tw in this example. This illustrates why its writhe term cannot be discarded. For the original regular binormal subclass, nonzero torsion fixes the sign of twist, but excluding cancellation still needs a global argument using binormal injectivity. The present countermodel deliberately tests only the invalid shortcut.

## 4. Injectivity is not regularity, and normalization is not injectivity

Set H(t)=t−sin t. Its derivative 2sin²(t/2) is nonnegative and positive away from multiples of 2π. For any a<b<a+2π, ∫ₐᵇ H'>0, so H is strictly increasing with H(t+2π)=H(t)+2π. Therefore Q(t)=(cos H(t),sin H(t),0) is a smooth injective map S¹→S². Yet Q'(0)=0. Its image is even a regular great circle; its parametrization has a stationary point. No assertion is made that Q is compatible with a given regular center curve. This directly invalidates the purely logical implication “injective smooth spherical field ⇒ nonzero derivative.”

For another exact scope control, let v(t)=(sin t,sin 2t,1) and R(t)=(2+cos t)v(t). R is nowhere zero and injective: its z-coordinate recovers cos t, and its x/z ratio recovers sin t. But R/|R| repeats at t=0 and t=π because v is (0,0,1) at both, while R itself has distinct values (0,0,3) and (0,0,1). This proves that radial normalization may destroy vector-valued injectivity. It is not claimed to be a compatible binormal of a closed curve.

## 5. The signed-crossing formula under its actual hypotheses

For a smooth embedded center curve with a differentiable unit binormal B and nowhere-zero B', define N=B×T in arclength. Then T'=κₛN, N'=−κₛT+τB, B'=−τN, with τ continuous and nonzero. For a generic u with u not parallel to any T, let a=u·T, b=u·N, c=u·B. Their derivatives are a'=κₛb, b'=−κₛa+τc, c'=−τb. The blackboard framing V=(u×T)/|u×T| has moving components cos θ=c/sqrt(b²+c²), sin θ=−b/sqrt(b²+c²). Hence θ'=−τ+κₛac/(b²+c²). At a zero of c, b≠0 and θ'=−τ, so the two regular values ±B contribute Rot(V,B)=−(#zeros(c)/2)sign τ. V has linking equal to the signed crossing sum of the projected center curve. The framing-difference formula then yields

Lk(γ,B)=Cr(γᵤ)+(#zeros(u·B)/2)sign τ.

All zero crossings have the needed transversality. Compactness makes their number finite. The angles are lifts on a parameter interval, not globally real-valued functions on the circle when their degree is nonzero. This verifies the sign, factor, and hypotheses of Ghomi–Raffaelli Theorem 1.2; it does not prove that the right side is nonzero. Cr is a signed diagram sum, not an unsigned crossing count or a knot's minimum crossing number. The arithmetic possibility Cr=−1, #zeros=2, sign τ=1 gives zero; it is not an asserted realization with an injective compatible binormal.

## 6. Inflection restrictions and the remaining gap

For the regular unit-binormal subclass, B''·(B×B')=τ²κₛ, |B'|=|τ|, and its outward-oriented spherical geodesic curvature is κₛ/|τ|. Multiplying by spherical arclength |τ|ds gives integral ∫κₛds. If B is also simple, its Jordan-region area is strictly between 0 and 4π, so Gauss–Bonnet gives |∫κₛds|<2π. If κₛ had one sign, then ∫|κₛ|=|∫κₛ|<2π contradicts Fenchel's theorem. Thus inflections are necessary in that subclass. No division by κₛ is used at an inflection; the Darboux frame remains defined.

The original continuous immersed formulation does not automatically satisfy the regular embedded hypotheses above. A claimed approximation must preserve binormal compatibility, injectivity, closure, disjointness, and linking simultaneously. None was supplied. A direct disk argument settles zero linking only when a spanning surface and a disjoint contraction in the complement of the push-off are actually available, as in the paper's Note 1.6. Those properties cannot be inferred from the binormal's simple spherical image. The exact unresolved gap remains the global exclusion of signed-crossing/writhe cancellation, or a valid full-hypothesis counterexample. The original PR correctly records that gap.
