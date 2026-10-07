# Independent audit: positive-current repair and conditional recursion

Problem 30004711. Audited 7 October 2026.

## Verdict and exact scope

**Accept Approach 5's odd-component current-level theorem, and accept Approach 3's conditional recursion comparison. No mathematical correction to either frozen target is required.** This report supplies explicit checks of the analytic, algebraic, normalization, and source hypotheses that make these acceptances valid.

Frozen targets:

- `AUTHOR_APPROACH_5_POSITIVE_CURRENT_REPAIR.md`: 10,732 bytes; SHA-256 `d6e451d3f193ccf9400180bf17fb924d8b4ea7d2efecf8c8c0401c1796547779`.
- `AUTHOR_APPROACH_3_GEOMETRIC_RECURSION.md`: 9,943 bytes; SHA-256 `6994b76c1ed8d96f1784d88c147fe6789ba9fabc57fb3b4a42808547deddd88f`.

The newly accepted analytic conclusion is specific: on the odd-spin, once-NS-punctured genus-one stack, the canonical Petersson metric on `E=F∨=H³` has positive curvature on the open locus. That curvature extends as a finite positive current representing `c₁(E)`, has no atom at the Ramond cusp, and has open integral `+1/32` in the unrigidified stack convention. The inverse metric on `F` has integral `−1/32` with its standard complex orientation.

This acceptance uses the independently audited extending line/frame and uniform growth bounds of Approach 4. It does not reinstate the smooth-metric or bounded-curvature extension disproved there. It does not identify a torsion-induced measure, prove the full original OWR identity, include the even component, or extend higher-rank top Chern forms. The original torsion-volume identity remains unresolved by these five approaches.

The targets and earlier source/acceptance files were preserved. This audit made no publication, commit, or push.

## 1. Source inspection and separation of the two extension problems

The two positivity sources were downloaded afresh from their cited public URLs. Both files exactly match the hashes in Approach 5's source manifest:

- Philipp Naumann, *Positivity of direct images with a Poincaré type twist*, Forum of Mathematics, Sigma 10 (2022), e89, [public PDF](https://epub.uni-bayreuth.de/id/eprint/6737/1/positivity-of-direct-images-with-a-poincare-type-twist.pdf), SHA-256 `55c20a470b8f6bb343fe0af409694d02528c52f864b0d15aadec30e937075003`.
- Mihai Păun and Shigeharu Takayama, *Positivity of twisted relative pluricanonical bundles and their direct images*, [1409.5504v1](https://arxiv.org/pdf/1409.5504v1), SHA-256 `27cd279ce7d28f8a260a17e41e9734be00d5b259c2978a0b4999c507bbabba57`.

Naumann's setup on pp.2–3, the parameter dependence and Theorem 4.1 on p.14, and the divisor-current argument on p.15 were inspected. Păun–Takayama's Set-up 3.2.1 on p.20, the fiber identifications on pp.21–23, and Theorem 3.3.4 on p.24 were inspected. The decisive theorem pages were also rendered and visually checked.

There are two different divisors:

1. The marked section `D` inside a **smooth family** over the open moduli base. The singular twisting metric must extend across this divisor before the direct-image theorem is applied.
2. The nodal cusp in the **base compactification**. The positive scalar potential is extended across this point only after the direct-image theorem has been applied on the punctured base.

No cited direct-image theorem is being applied across an unverified singular fiber. Keeping these steps separate is essential.

## 2. Family, projectivity, and the actual adjoint line

Take a sufficiently small manifold chart `U` of the smooth odd-spin stack, including a choice of the spin line. The coarse-fiber universal family `π:C→U` is proper and smooth, with connected compact elliptic fibers, and `D` is a holomorphic section. Thus `D` is a relative simple normal crossings divisor; in this dimension it is a single smooth relative divisor.

The pair is log-canonically polarized: `deg(K_Cu+D_u)=1`, so the fiberwise adjoint line is ample. This is the hypothesis relevant to Naumann's Theorem 4.1. Effective parametrization is needed only for strict positivity and is not needed here.

The morphism is projective. On every elliptic fiber, `O(3D_u)` is very ample and has vanishing first cohomology. After shrinking `U`, base change gives a rank-three direct image, its evaluation supplies the relative embedding, and trivializing that direct image embeds `C` into `U×P²`. The theorem requires a projective morphism of complex manifolds, not a compact or projective base manifold. Therefore using analytic coordinate charts is legitimate.

Let `ℓ²=K_(C/U)` be the coarse theta line. The twist is

`L=ℓ(D)`, and `L²=K_(C/U)(2D)`.

The adjoint image is

`E=π_*(K_(C/U)⊗L)=π_*(K_(C/U)⊗ℓ(D))=F∨`.

This is also the duality calculation obtained from `ρ_*θ∨=ℓ∨(−D)` on the twisted curve. The external NS marking is responsible for the divisor `D`; omitting it would give a different line and a different local integrability problem.

The adjoint line on each elliptic fiber has degree one. By Riemann–Roch and Serre duality, `h⁰=1` and `h¹=0`. Consequently `E` is a rank-one locally free direct image and every fiber has the required base-change identification. In Păun–Takayama's notation, `Y_(1,ext)=U`.

## 3. Exact metric and curvature signs

Write the curvature-minus-one hyperbolic metric on a punctured fiber as `ρ²|dz|²`. The induced squared norm on the relative canonical frame is

`h_K(dz)=ρ^(−2)`.

For `D={z=0}`, use the holomorphic frame `e_D=1/z` of `O(D)`. The canonical section is `z e_D`. Requiring that section to have norm one off `D` gives

`h_D(e_D)=|z|^(−2)`, and `c₁(O(D),h_D)=[D]`.

The metrics to use are

`h_(K(D))=h_K h_D`,

`h_L=(h_(K(D)) h_D)^(1/2)=h_K^(1/2)h_D`.

The last square root is a metric on the actual line `ℓ(D)`, through its specified square isomorphism. It does not require a global ordinary square root of a coordinate or of the Hodge bundle on the coarse modular curve.

With `ddᶜ=(i/(2π))∂∂̄`, our convention is `c₁(A,h)=−ddᶜ log h` for squared norms. Hence

`c₁(L,h_L)=(1/2)c₁(K(D),h_(K(D)))+(1/2)[D]`.

The divisor coefficient is exactly one half in this expression, even though `L` contains one full copy of `D`: half of that copy has already been incorporated into `K(D)`. This accounts for all divisor curvature and fixes the sign.

## 4. Total-space semipositivity and uniform marked-cusp control

Naumann's Theorem 4.1 concerns the curvature on the whole total space `C\D`. It is not merely a theorem about the restriction to each fiber. Thus the local weight

`φ_(K(D))=log(ρ²|z|²)`

is plurisubharmonic away from `D`, because `log|z|²` is pluriharmonic there.

The parameter-uniform estimate required for extension is supplied by the setup preceding that theorem. On p.14 the Kähler–Einstein volume is expressed as `exp(v_u)` times a Poincaré model, with the parameter map into the appropriate bounded Hölder space smooth. Restricting to a relatively compact neighborhood of any `u₀∈U` bounds its Hölder norm and therefore its zeroth-order norm uniformly. Smooth model factors are bounded above and below after shrinking the coordinate chart. In local coordinates this gives constants `0<c<C<∞` such that

`c/[|z|²(log(1/|z|))²] ≤ ρ(z,u)² ≤ C/[|z|²(log(1/|z|))²]`.

Only local uniformity over the smooth base is needed. No uniform bound as the moduli parameter approaches its nodal boundary is asserted in this step.

It follows that

`φ_(K(D))=−2 log log(1/|z|)+O(1)`

with the remainder uniformly bounded on that local base chart. This weight is locally bounded above near `D`, so its upper-semicontinuous extension is plurisubharmonic across `D`. Its value on `D` is allowed to be `−∞`. Consequently `c₁(K(D),h_(K(D)))` is a positive current on the total space. The curvature identity of the preceding section then proves total-space semipositivity of `h_L`.

Naumann's Corollary 5 has a compact-base hypothesis for its global nefness/bigness conclusions. Those conclusions are unnecessary here. The local metric argument just given proves the assertion needed on `U`, and agrees with the local divisor-current computation in that corollary's proof.

## 5. Both multiplier ideals and the exact direct-image metric

In the local frame `(dz)^(1/2)/z` of `L`, the uniform estimate gives

`h_L=ρ^(−1)|z|^(−2) ≍ log(1/|z|)/|z|`.

The constant function is locally integrable for this weight. Including the area factor, its transverse integral is proportional to

`∫₀^ε log(1/r) dr = ε(1−log ε) < ∞`.

The same dominating bound holds on a product neighborhood in the total space. Fubini therefore gives local integrability in all variables. Every holomorphic germ is bounded on a smaller relatively compact polydisk, so

`I(h_L)=O_C`, and `I(h_L|C_u)=O_(C_u)` for every `u∈U`.

Off `D` the metric is smooth and positive. In particular it is not identically infinite on a fiber. Thus the natural inclusion of multiplier-ideal adjoint images is an isomorphism, stronger than the generic isomorphism required in Theorem 3.3.4.

All hypotheses of Păun–Takayama 3.3.4 are now satisfied: projective surjective morphism of complex manifolds with connected fibers, smooth morphism, a holomorphic line with semipositive singular metric, locally free adjoint direct image, and the multiplier-ideal condition. That theorem also identifies its metric with the canonical fiberwise L² pairing on `Y_(1,ext)`, which here is every point of `U`. Its conclusion is therefore about this particular metric, not the existence of a different positive metric on an isomorphic line.

For `η=f(z)(dz)^(3/2)/z`, the pairing is, up to a fixed positive area-convention factor,

`∫ |f(z)|²ρ^(−1)|z|^(−2) dx dy`.

This is exactly the Petersson pairing of the permitted simple-pole `3/2` differentials. The source definition is in [Norbury 2005.04378v4, equation (40), p.36](https://arxiv.org/pdf/2005.04378v4), and [2312.14558v3, equation (11), p.8](https://arxiv.org/pdf/2312.14558v3). Multiplying a squared norm by a universal positive constant changes neither its Chern curvature nor this argument's normalization of that curvature.

For a nonzero local frame `s` of `E`, put `M=||s||²`. In rank one the direct-image positivity convention says precisely that `−log M` is subharmonic. Equivalently `c₁(E,M)=−ddᶜ log M≥0`. Passing to the inverse metric on `F=E∨` reverses the sign. The construction is intrinsic and invariant under the finite chart groups.

## 6. Nodal cusp: extending frame, positive measure, and zero atom

The accepted Approach 4 and its independent audit identify the extending line on the compactified odd component as

`F=H^(−3)`, `E=F∨=H³`, `H²=λ`.

Its period-one differential `α=dz=(2πi)^(−1)du/u` is nonvanishing as a relative dualizing section at the Tate node. Its spin square root produces the nonzero extending frame `s=(dz)^(3/2)` of `E`. Thus its norm is being measured in the correct compactified line, with no hidden factor `q^a`.

For `τ=a+iT`, `|a|≤1/2`, that audit establishes

`2(T−2)²/π² ≤ M(τ) ≤ C T² log T`.

With `q=exp(2πiτ)` and `t=log(1/|q|)=2πT`, it follows that, uniformly in argument,

`2 log t+C₋ ≤ u(q):=log M(q) ≤ 2 log t+log log t+C₊`.

The weight `φ=−u` is subharmonic on the punctured disk and bounded above near its center. It therefore has the standard subharmonic extension across zero. This extension is locally integrable, not identically `−∞`, and its distributional `ddᶜ` is a locally finite positive measure.

The uniform estimate gives `φ(q)/log|q|→0`. The logarithmic coefficient of a subharmonic potential is the mass of its point part, up to the fixed `ddᶜ` normalization. Hence the curvature measure has no atom at zero. Unlike a growth-only argument, positivity supplies local finiteness and eliminates the possibility of an uncontrolled signed curvature extension.

If an actual spin chart uses `q=b^k` times a holomorphic unit, the same estimates hold with `t=k log(1/|b|)+O(1)`. The potential remains sublogarithmic in `|b|`, so the zero-atom statement holds on the genuine chart. It then descends with the stack's ordinary finite-group weights.

## 7. Flux estimate, including its factor of two

Let `m(t)` be the angular mean of `u(e^(−t+iθ))`. Subharmonicity of `−u` gives `m''≤0` distributionally. The norm is smooth on the open moduli chart; alternatively, the following argument can be made entirely with the one-sided derivatives of the concave function `m`, avoiding any additional boundary differentiability assumption.

Because `m(t)→∞`, its nonincreasing derivative cannot become negative. Its limiting derivative is zero because `m(t)=o(t)`. For sufficiently large `t`, concavity gives

`0 ≤ m'(t) ≤ 2[m(t)−m(t/2)]/t ≤ 2[C+log log t]/t`.

This is derived from concavity, not by differentiating a comparison inequality.

In the specified convention,

`ddᶜ f=(Δf/(4π)) dx dy`.

Stokes on an annulus gives the curvature mass between radii `e^(−t)` and `e^(−T)` as `(m'(t)−m'(T))/2`, for `T>t`. Sending `T→∞`, using the derivative limit and the absence of a point atom, yields

`∫_(|q|<e^(−t)) c₁(E,M)=m'(t)/2=O((1+log log t)/t)`.

Thus the claimed factor `1/2`, sign, finite flux, and zero limiting cusp mass are all correct. On quotient charts the usual stabilizer factor multiplies both sides. A smooth reference metric contributes only a vanishing small-circle flux.

## 8. Global current class and stack integral

The only compactification boundary of this odd component is its Ramond cusp. On the interior the canonical pairing varies smoothly; near the cusp its logarithm has the locally integrable growth just proved. Choose any smooth positive-definite reference Hermitian metric `h₀` on the extended `E`. Here positive-definite refers to the metric, not an additional assertion about its curvature.

The ratio defines a global locally integrable function `v=log(M/h₀)` on the stack, and

`c₁(E,M)=c₁(E,h₀)−ddᶜv`

as currents. This identity uses the specified extending line and cannot be obtained from an arbitrary open-locus bundle identification. Pairing the exact term with the constant test function on the compact stack gives zero. The extended curvature therefore represents the compactified first Chern class.

The odd theta characteristic is unique on a smooth elliptic curve and has its scalar `μ₂` automorphisms. In the unrigidified convention the forgetful degree of the odd spin component over `M̄_(1,1)` is `1/2`. Since `H²=λ`,

`∫_B c₁(E) = (3/2)·(1/2)·∫_(M̄_(1,1)) λ = (3/2)·(1/2)·(1/24) = 1/32`.

This is compatible with the line calculation in the prior cusp audit and the graph arithmetic in [Norbury 2608.25237v2, pp.39–40](https://arxiv.org/pdf/2608.25237v2). The graph arithmetic is a cross-check rather than the analytic justification.

The current is positive, has finite mass, and has no cusp atom. Its open-locus integral is therefore the same `1/32`. There is no cancellation of divergent positive and negative parts. The inverse metric on `F` gives the negative value. Rigidifying the spin gerbe would change the stack integration convention and is not silently done.

## 9. Approach 3: source recurrence and normalization algebra

Let `T=V^Θ` be the intersection-polynomial sequence, with the common kernel `H` used in Approach 3. Its recurrence is [Norbury 2005.04378v4, Theorem 2, equations (6)–(8), pp.5–6](https://arxiv.org/pdf/2005.04378v4). This is the intersection-number recurrence; using it does not require the disputed smooth-extension step for the canonical metric. In Approach 3, `W` and `S` are explicitly defined rescalings of `T`, not independently established torsion integrals.

For `a_(g,n)=(-1)^n 2^(1−g)`, the merging ratio is `−1` and the nonseparating ratio is `−1/2`. In a separating term `g₁+g₂=g` and `n₁+n₂=n+1`, giving the same `−1/2` ratio. Multiplying the `T` recurrence therefore gives the common-kernel coefficients `−1/4` and `−1` for `S`.

For `w_(g,n)=2^(1−g−n)`, the nonseparating and separating ratios are one and the merging ratio is one half. Thus the `W` coefficients are `1/2` and `1/2`. Both normalization maps preserve all length arguments. The zero genus-zero sequence causes no exception; the displayed ratios themselves remain algebraically valid there.

The kernel called `D(x,y)` in [Stanford–Witten 1907.03363v5, equation (5.41), PDF p.99](https://arxiv.org/pdf/1907.03363v5) is `H(x,y)/2`. Consequently its `−1/2` handle coefficient in equation (5.42), PDF p.100, becomes `−1/4` in the common-`H` convention. Its two merging kernels sum to `R`: expanding the four hyperbolic secants verifies the argument-shift identity exactly.

Appendix D.6, printed p.134 / PDF p.135, does discuss boundary-trivialized spin structures, the extra merging factor two, and the parity-weighted Ramond-seam cancellation. The approach correctly retains those as actual convention data requiring comparison. They cannot be erased by renaming a volume symbol.

## 10. Kernel integrals and nontrivial coefficient check

The genus-one pants kernel is minus one half of `H(2x,b)`. With `a=b/4` and `t=x/2`, its integral reduces to the difference of two translated first moments of `sech`. Extending the odd-power difference to the full real line gives

`∫₀∞ t[sech(t−a)−sech(t+a)]dt=πa`,

and hence

`∫₀∞ x D_SW(b,x,x)dx=−b/8`.

The integral is absolutely convergent for each fixed real `b`, including its zero-length limiting expression. This verifies the scalar analytic evaluation. It does not derive the geometric unfolding that identifies it with a torsion integral. The half-volume and compensating spin-sum factors in equation (D.45), printed p.137 / PDF p.138, were visually checked and are correctly reported.

The same whole-line substitution gives

`∫₀∞ x H(x,L)dx=L`,

`∫₀∞ x³H(x,L)dx=L³+12π²L`.

An independent way to organize these moments is the moment-generating function `exp(Lt) sec(2πt)` for the translated, normalized hyperbolic-secant density. Its first and third derivatives at zero give the two displayed polynomials. These identities hold for real `L`, so the occurrence of `L−L_j` in `R` causes no problem.

The resulting recursion values are

`T_(1,2)=1/8`,

`T_(2,1)=3(L²+12π²)/256`,

`W_(2,1)=3(L²+12π²)/1024`,

`S_(2,1)=−3(L²+12π²)/512`.

In genus two, the handle-plus-separating input is `1/8+1/64=9/64`, while integrating `xy` on `x+y=s` gives `s³/6`; the remaining factor is the recurrence's `1/2`. This checks the ordered-separating-sum convention without adding a second copy of the identical `(1,1)+(1,1)` term. The `S` value agrees with SW equation (5.40), PDF p.99.

## 11. Conditional uniqueness and the remaining geometric premise

For stable pairs with `n≥1`, let `c=2g−2+n`. The initial pairs with `c=1` are `(0,3)` and `(1,1)`. Every merging and nonseparating input has complexity `c−1`; in a separating input the two positive complexities add to `c−1`, so each is smaller. Terms with negative genus or the omitted unstable disk/annulus are absent. Induction therefore proves uniqueness among sequences satisfying the same finite-integral recurrence and the same base data for `L₁>0`. Continuity extends the identity to zero lengths. Polynomiality of an unknown geometric sequence is not required.

The common kernels decay exponentially in the integration variables for fixed external lengths. This proves convergence against each polynomial lower-complexity input of `T`, but gives no independent growth bound for a torsion-defined sequence. The case `n=0` does not enter this induction and requires an additional geometric relation if included in the desired claim.

The source limitations are accurately described:

- [Huang–Penner–Zeitlin 1907.09978v3](https://arxiv.org/pdf/1907.09978v3), Theorem 5.5, p.30, has a constant depending on the fixed super surface; Theorem 6.1 and Proposition 6.3, pp.35–36, concern its once-punctured-torus identity and convergence. They do not themselves provide a uniform integrable majorant over noncompact moduli.
- [Norbury 2608.25237v2](https://arxiv.org/pdf/2608.25237v2), §4.3.3, p.33, explicitly retains a rigor issue involving positive-length Ramond boundaries. This page was visually checked.
- [Johnson 2606.20796v1](https://arxiv.org/pdf/2606.20796v1) compares spectral-curve and volume-recursion formulations, including formal Ramond data. That comparison does not by itself justify integration/interchange for an independently specified OWR torsion measure.

Those three versioned PDFs were downloaded afresh and exactly match the archived source bytes.

In particular, coefficientwise pointwise convergence of a super-McShane sum does not imply convergence of its integral after taking the top odd coefficient against a noncompact torsion density. The displayed requirement `lim_R ∫ top_odd(E_R μ_τ)=0` is a genuine missing analytic condition, not something furnished by formal recursion uniqueness. The gluing, spin, orientation, retraction, base-integral, and Ramond-cancellation hypotheses listed in Approach 3 also remain necessary.

## 12. Acceptance boundaries and effect on the cumulative result

Accepted:

1. The actual canonical metric's total-space positivity input, correctly twisted singular adjoint metric, trivial multiplier ideals, and actual L² direct-image identification on the smooth base.
2. Its rank-one positive-current extension with finite mass, zero cusp atom, vanishing flux, and odd-component canonical integral `+1/32`.
3. The conditional normalization conjugacy, kernel evaluations, recursive coefficients, and triangular uniqueness argument of Approach 3.
4. The source attribution and the explicit limits placed on their geometric consequences.

Not established:

- Equality of the canonical Chern form with the actual OWR/SW torsion representative.
- Equality of retractions, orientations, parity weights, boundary trivializations, or integration conventions for those constructions.
- The full geometric torsion recursion with its noncompact interchange and boundary terms.
- An even-component current theorem, higher-rank singular top-Chern integration, or the original coefficient-one identity.

The source smooth-extension gap is repaired here only for the canonical odd rank-one integral. The full problem's status must remain unresolved; neither a solved-as-written claim nor a counterexample to the literal torsion identity follows. There is no comprehensive novelty or literature-priority claim.

The companion verifier checks target hashes, normalization ratios, local integrability arithmetic, the curvature-flux factor, polynomial moments, and sample numerical improper integrals. These are reproducibility checks, not substitutes for the source-hypothesis and potential-theoretic proof above.
