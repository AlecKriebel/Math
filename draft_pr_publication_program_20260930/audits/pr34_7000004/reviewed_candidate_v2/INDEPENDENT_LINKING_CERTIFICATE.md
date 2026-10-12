# Independent global linking certificate for the supplied candidate

Provenance: the differential family found the construction and the parent sent it here after `FIRST_CONCLUSION.json` had sealed this family's independent audit of the original unsolved package. This is a verification of that supplied construction, not an independent discovery by this family. Root records it as substantive attempt 2/5; this family adds zero substantive attempts. The earlier original-unsolved verdict and proof are preserved as historical evidence.

## Exact candidate and binormal compatibility

For t in R/(2πZ), set c=cos t, s=sin t and

γ(t)=(c,s,(c²−s²)/4), W(t)=(−c³,s³,1), R(t)=sqrt(1+c⁶+s⁶), B(t)=W(t)/R(t).

The planar projection is the standard circle, hence γ is smooth, regular and embedded. Direct differentiation gives γ'=(-s,c,-sc), γ''=(-c,-s,-(c²−s²)), and γ'×γ''=W. In particular W is never zero, its third coordinate being 1. The curve has strictly positive Frenet curvature; its ordinary Frenet binormal is exactly B. Thus the osculating planes exist continuously, and B is smooth, unit length, nowhere zero, and orthogonal to both required derivatives. No arbitrary normal field has been substituted for a binormal.

Global injectivity is exact, not sampled: B₁/B₃=−cos³t and B₂/B₃=sin³t, with B₃>0. Equal binormals imply equal real cubes, hence equal sine and cosine, hence equal parameters modulo 2π. The spherical binormal is therefore a continuous one-to-one field in the literal 2019 Problem 1.4, including the natural unit direction interpretation.

It is not a regular spherical parametrization. Since W₃=1, B'=0 implies W' is proportional to W with proportionality zero, so W'=0. Conversely W'=0 implies B'=0. The equations W'=(3c²s,3s²c,0)=0 hold precisely when c=0 or s=0: four parameter values modulo 2π. The torsion is

τ(t)=3cs/(1+c⁶+s⁶).

It vanishes and changes sign at those four values. These facts do not violate the original continuous-binormal hypothesis. They do exclude the later negatively curved asymptotic-surface subclass, which has |n'|=|τg|>0. The candidate does not resolve Ghomi–Raffaelli Problem 1.1 or Nirenberg rigidity.

## A uniform embedded push-off

Let 0<ε<1/3 and write η(t)=γ(t)+εB(t). Its planar coordinates are

x(t)=c(1−εc²/R), y(t)=s(1+εs²/R).

The factors are strictly positive, since R≥1; therefore (x,y) is never zero and inherits the signs of (c,s). Its winding number about the origin is 1, also seen from the nonzero linear interpolation ε↦λε, 0≤λ≤1. Differentiating R²=2−3c²s² gives R'=−3cs(c²−s²)/R. Direct calculation yields

x y'−y x'=1−ε(c²−s²)/R+3εc²s²(c²−s²)/R³−3ε²c²s²/R².

Because c²s²≤1/4, |c²−s²|≤1 and R≥1, this is at least 1−7ε/4−3ε²/4. For ε<1/3 it is strictly greater than 1/3. Hence the polar-angle lift is strictly increasing. It increases by exactly 2π over one period because the winding number is 1. Equality of planar points therefore forces equality of parameters modulo 2π. The planar projection, and consequently η, is a smooth embedding; its derivative never vanishes. This gives an explicit bound, independently of invoking a tubular neighborhood.

## Direct zero-linking proof

The ambient map H(x,y,z)=(x,y,z−(x²−y²)/4) is an orientation-preserving diffeomorphism with Jacobian determinant 1. It is connected to the identity by Hλ(x,y,z)=(x,y,z−λ(x²−y²)/4), 0≤λ≤1. Its inverse adds the same polynomial. Thus it preserves linking and sends γ to the unit circle C in the plane z=0.

For the push-off, expanding the polynomial gives

H₃(η(t))=ε/R+ε(c⁴+s⁴)/(2R)−ε²(c⁶−s⁶)/(4R²).

Since c⁴+s⁴≥1/2 and |c⁶−s⁶|≤1, this is bounded below by

(ε/R)(5/4−ε/(4R)) ≥ (ε/R)(5/4−ε/4) > 7ε/(6R)>0.

Therefore H(η) is disjoint from the entire planar unit disk D bounded by C, not just from its boundary. In particular η is disjoint from γ. The linking number of C and H(η), with either orientation, is the algebraic intersection of H(η) with D and is zero. Equivalently H(η) contracts in the upper halfspace, disjoint from C. Orientation-preserving ambient isotopy then gives

Lk(γ,γ+εB)=0 for every 0<ε<1/3.

All required objects are smooth embedded oriented loops, so both the standard linking definition and Călugăreanu's ribbon definition apply without an immersed-cycle convention. The value zero is orientation-independent. The normal-bundle theorem additionally supplies an embedded thin ribbon for a possibly smaller positive width if desired; the explicit calculation already certifies both boundary curves for the stated ε range.

## Independent falsification result and scope

The construction satisfies every literal hypothesis checked in the fresh 2019 source, including the natural unit-direction convention, and disproves the broad nonzero-linking assertion. Its stationary binormal points explain why the earlier regular-binormal obstruction does not apply: the spherical Gauss–Bonnet argument for a regular Jordan curve needs correction terms at these cusps. Positive Frenet curvature of the center curve does not restore regularity of its binormal.

The complete exact arXiv v2 and complete September 19 author PDF were read separately. Their Theorem 1.2 and Notes 5.1–5.5 assume a negatively curved embedded surface with a closed asymptotic curve, or the nonzero-torsion framed subclass. The candidate has four zero torsions and is not such a curve. Those results remain compatible with this certificate. The broad literal problem being false does not imply that the narrower surface question, or the rigidity problem motivating it, is solved.

No mathematical issue was found after checking global embedding, unit-binormal compatibility, injectivity, all stationary points, uniform push-off embedding and disjointness, and the direct disk certificate. Priority and the strongest defensible framing of the 2019 question are separate gates; no first-discovery or publication-ready claim is made here. The result must not be cited as a counterexample to the later Problem 1.1.
