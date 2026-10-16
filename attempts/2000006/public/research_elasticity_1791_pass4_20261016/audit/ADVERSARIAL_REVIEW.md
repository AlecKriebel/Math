# Independent adversarial audit: E-6322, shared pass 4 of 5

16 October 2026. Frozen target: `recovery_elasticity_1791_20261015/formulation_gate/RESEARCH_TARGET.md`. The prior pass-3 audit remains sealed. No publication or delegation to further agents was performed in this review.

## Verdict

**Accept the reviewed pass-4 results as rigorous partial progress. E-6322 remains unresolved.** No report proves a global essential Jacobian lower bound for every full-class minimizer, and no report constructs a singular full-class minimizer.

The strongest new accepted results are:

1. Smooth graph transformations of the actual inverse, including ordinary affine cutoff expressions at the natural inverse exponent, belong to the exact inverse class whenever their resulting dual energy is finite. This is proved in the high-exponent primal coordinates, with the entire boundary term retained.
2. A minimizer has a finite weighted inverse-cube moment against every same-trace rank-one-connected endpoint whose Jacobian is nonnegative, even if that endpoint has infinite barrier energy. The endpoint must actually exist; the theorem does not furnish it.
3. There is an admitted nonminimizing map for which no fixed one-component same-trace repair can have a uniform positive Jacobian. Thus existence of the repair needed to exploit the preceding theorem cannot be imported from competitor-class membership alone.
4. The exact homogeneous-core exclusion is stable under controlled annular limits. The audit addendum improves the hypotheses to strong W^{1,∞} annular convergence and C¹ homogeneous angular data, with positive limiting angular determinant explicitly required.
5. The new examples and finite comparison estimates identify genuine sign, energy, marginal-volume, and coercivity obstacles. They do not amount to impossibility results for all minimizer-specific arguments.

Forty independent audit checks, fifty-five exact-lane checks, and twenty-two positivity-lane checks were executed successfully. These checks supplement, rather than replace, the analytic proof review. The audit manifest binds the frozen inputs and the authored audit files.

## 1. Scope and retained benchmark hypotheses

The complete target was reread. Throughout the review,

W(F)=a|F|⁶+b|cof F|³+cJ²+dJ^{-2},  J=det F>0,

with arbitrary fixed finite positive a,b,c,d, and W=+∞ for J≤0. The original domain is any permitted bounded connected smooth domain, with the full trace of a smooth orientation-preserving diffeomorphism G. The competitor class is all finite-energy W^{1,6} maps with that trace, with no imposed injectivity, smallness, or regularity. The requested conclusion is an essential bound over the whole domain, including all boundary collars.

The inverse baseline from previous audited passes is used only in its proved form: a.e. inverse, genuine weak derivative, area formula, and full inverse trace. Pointwise homeomorphism of a general competitor is never assumed. The exact inverse class B_g is characterized by finite dual energy and the full-boundary transported Piola identity. The dual density is

V(H)=a|cof H|⁶/K⁵+b|H|³/K²+c/K+dK³,  K=det H>0.

Its natural gradient exponent is 9/5 and its cofactor exponent is 9/4. Those facts alone do not identify an arbitrary finite-V map with an original inverse.

All new diagnostic maps are checked against the original full trace and energy conditions. When a diagnostic is nonminimizing, this is stated explicitly, often with an independent affine-uniqueness or stationarity certificate.

## 2. Structured natural-exponent inverse comparisons

Accepted files: `literature/STRUCTURED_NATURAL_EXPONENT_COMPARISONS.md` and `literature/NATURAL_EXPONENT_EXTENSION_LIMITS.md`.

### 2.1 The positive theorem

Let v=y^{-1} be the actual inverse of any original competitor on D=G(Ω). Let Φ(z,x) be smooth near Dbar×Ωbar, and equal x when z is near ∂D. Set u(z)=Φ(z,v(z)). If ∫V(Du)<∞, then u∈B_g. Therefore an inverse minimizer compares with every such u; infinite-energy instances merely give a trivial extended-valued inequality.

The proof correctly avoids smoothing the low-exponent inverse. Put k(x)=Φ(y(x),x). Since y∈W^{1,6} is continuous on the closure and takes its boundary into ∂D, k∈W^{1,6} and k=id on a source boundary collar. With F=Dy, A=D_zΦ(y,x), and B=D_xΦ(y,x),

Dk=AF+B,   Du∘y=A+BF^{-1}=Dk F^{-1}.

Consequently

(det Du)∘y J=det Dk,
(cof Du)∘y J=(cof Dk)Fᵀ.

Every transpose and Jacobian factor was independently checked. The transported Piola expression for u changes into

∫Ω [ψ(y) det Dk div φ(k)+φ(k)·cof Dk D(ψ∘y)].

Approximate k−id and y−G by compactly supported smooth functions strongly in W^{1,6}. The maps converge uniformly, the quadratic minors strongly in L³, the cubic minors strongly in L², and the chain gradients strongly in L⁶. These are sufficient for every displayed product. The approximations retain the exact boundary flux

∫∂Ω ψ(G(x)) φ(x)·νΩ.

No finite barrier energy, positive Jacobian, or injectivity of the auxiliary k is needed for this high-exponent integration identity. Finite V of u is then used at the final exact-class characterization step. In particular, u=θv+(1−θ)ℓ is covered when θ is smooth and one near the entire boundary and ℓ is smooth. Its difference from v need only have the natural W^{1,9/5} regularity.

This is a genuine improvement over the earlier sufficient W^{1,9/4} additive-difference theorem. It resolves the inverse-class issue for the displayed structured expressions, conditional on their energy. It does not establish that an arbitrary cutoff has positive determinant or finite reciprocal-determinant terms.

### 2.2 The remaining arbitrary-addition issue is correctly limited

For generic H₁,H₂∈L^{9/5}, mixed quadratic products are only controlled in L^{9/10}. Extra endpoint cofactor integrability does not supply a direct pointwise domination of the mixed polarization. The diagonal test

H₁=diag(L,L^{-1/5},L^{-1/5}),
H₂=diag(L^{-1/5},L,L^{-1/5})

has endpoint V≈L^{9/5}, but mixed (3,3) cofactor L²+L^{-2/5}. This rejects a proposed algebraic bound, not a differential-constraint or compensated-compactness theorem. The report explicitly does not pretend the test matrix fields are compatible gradients.

The bounded map q=(x₁/r,x₂/r,0) on a cylinder belongs to W^{1,p} for p<2 and has zero pointwise cofactors. Its distributional (3,3) cofactor is nevertheless πδ_axis. The coefficient is verified by ∮q₁dq₂=π. Its smooth radial regularizations have cofactor ε²/(r²+ε²)², whose cross-sectional mass tends to π, while the maps converge strongly in W^{1,p}, p<2. This demonstrates a genuine failure of naive minor identification under low-exponent smoothing. Because det Dq=0 and its defect has zero row divergence, it is neither a finite-V counterexample nor a weak-Piola counterexample. Those qualifications are essential and are present.

The conditional extension under an extra W^{1,2} assumption is valid: compact W^{1,2} differences give integrable mixed products, and resulting finite V supplies the conjugate cofactor pairing. That extra regularity is not silently assigned to all inverses. Generic finite-V W^{1,9/5} additions remain unsettled.

## 3. Finite inverse-addition intervals and their obstructions

Accepted files: `variations/FINITE_ADDITION_INTERVALS.md` and `variations/RANK_ONE_AND_CUTOFF_LIMITS.md`.

### 3.1 An actual interval criterion

For compact ζ∈W^{1,9/4}, assume M=Dζ F∘v is essentially bounded. If |t|‖M‖∞<1/2, then

H+tDζ=(I+tM)H,
K_t=det(I+tM)K>0.

The relative matrices and their inverses have uniformly bounded distortion. The exact density identity and fixed-matrix minor bounds imply V(H+tDζ)≤C V(H). Therefore these are genuine finite-energy inverse competitors. There is no assumed lower bound on the primal Jacobian in this argument.

For smooth ζ, however, ξ=ζ∘y has bounded derivative Dξ=M∘y and compact source support. Hence v+tζ=(Id+tξ)∘v, with Id+tξ bi-Lipschitz for small t. The criterion is a safe realization of already legitimate material compositions, not an independent high-level truncation mechanism. The report does not assume this Sobolev-composition conclusion for merely W^{1,9/4} ζ.

### 3.2 A controlled rank-one endpoint

For compact ζ∈W^{1,9/4}, suppose H_e=H+Dζ is rank-one connected to H and, for M≥1,

|H_e|≤M|H|,   |cof H_e|≤M|cof H|,   0≤K_e≤MK.

All minors are affine along the segment. Thus K_t≥(1−t)K and V(H_t)≤M⁶(1−t)^{-5}V(H), for 0≤t<1, even if the endpoint itself has infinite energy. These maps are actual inverse comparisons by the earlier additive-class theorem.

Writing X=V−dK³, dominated one-sided differentiation gives, on a set E outside which ζ vanishes,

3d∫E K²(K−K_e)≤11(M+1)∫E X.

The constants were checked directly: the first perspective term costs at most (6+5)(M+1), the second at most (3+2)(M+1), and c/K at most M+1 times its original value. Relative minor hypotheses control every denominator and derivative. A useful high-K endpoint with these properties has not been constructed. The left side is signed, so increases elsewhere cannot be discarded.

### 3.3 A smooth direction can have no nonzero finite amplitude

For 1/3≤α<1/2, the established admissible identity-trace map

yα=(r^{-α}x₁,r^{-α}x₂,r^{5α}x₃)

has J≈r^{3α} and F₁₁≥(1−α)r^{-α}. Let v be its actual inverse, and ζ(z)=−χ(z)z₁e₁ with χ smooth, compactly supported, and one near zero. On a primal core mapping into χ=1,

det(Dv+tDζ)=K(1−tF₁₁).

Every t>0 gives a negative determinant on a set of positive target measure. Every t<0 makes the dK_t³ term dominate a positive multiple of ∫₀ r^{2−9α}dr, which diverges, including logarithmically at α=1/3. Thus the comparison energy is finite only at t=0 along this one smooth direction.

The starting map is not a minimizer, since its full identity trace has the unique affine minimizer. The result proves that no finite amplitude interval follows from baseline admissibility alone. It does not prove such an isolated direction occurs at a minimizer. Weak Piola preservation by smooth additions is compatible with this example; sign and energy are the obstruction.

### 3.4 Determinant conservation and smooth cutoff failure

The weak Piola identity gives ∫(cof H)_i·∇φ=0 for compact scalar φ. A compact one-component determinant change therefore cannot be nonnegative everywhere, or nonpositive everywhere, unless it vanishes. A literal pointwise clamp of K is not automatically a determinant of an admissible addition; a nontrivial redistribution must compensate.

Even the genuine affine minimizer v(z)=diag(−1,−1,1)z can be blended with the positive-determinant identity to give zero determinant on an open midpoint plateau. This is a valid counterexample to automatic finite-energy affine cutoff admissibility, while the actual minimizer has determinant one. The final report correctly cross-references the now-proved structured natural-exponent theorem rather than leaving that class issue open.

## 4. A one-sided minimizer-specific mixed moment

Accepted file: `positivity/MIXED_MOMENT_VARIATION.md`.

Let y minimize in the full original class. Suppose v∈W^{1,6} has the same complete trace, rank(Dv−Dy)≤1 a.e., and J_v≥0 a.e. The endpoint may have zero determinant and infinite barrier energy. For every 0≤t<1, its segment with y is nevertheless admissible because all minors are affine and J_t≥(1−t)J_y.

The positive density H has |DH(F)|≤C|F|⁵. Hence its directional derivative against Dv−Dy is integrable, and the positive-energy difference quotients converge in L¹. The barrier secants decrease as t↓0 and are bounded above by 6J_y^{-2} for t≤1/2. Applying monotone convergence to that upper bound minus the secants permits an extended negative limit. A value −∞ contradicts minimality because the H derivative is finite. This proves both

∫ J_v J_y^{-3}<∞,

2d∫J_v J_y^{-3}≤∫DH(Dy):(Dv−Dy)+2d∫J_y^{-2}
≤∫[H(Dv)−H(Dy)]+2d∫J_y^{-2}.

No ordinary full Piola integrability or unrestricted additive Euler equation is used. Rank-one convexity here follows from convexity in the independent minors along this actual rank-one segment; full matrix convexity is not asserted.

If v=y off E, the exact cancellation is

∫E H(Dy)+2d∫E J_vJ_y^{-3}≤∫E H(Dv)+2d∫E J_y^{-2}.

A uniformly positive endpoint on a region yields inverse-cube integrability there. Such an endpoint is a substantive hypothesis, not a conclusion of this calculation. At v=y the moment is exactly the already known inverse-square moment.

The coefficient 2 in the residual barrier source survives arbitrarily small amplitudes. At J_v=0 the cost per t is dJ_y^{-2}(2−t)/(1−t)², tending to 2dJ_y^{-2}. A smooth compact one-component flattening of the identity provides an actual compatible endpoint with an open zero-J region and a finite segment for every t<1. This verifies the obstruction to the proposed small-step absorption mechanism, not optimality of the constant in every imaginable minimizer inequality.

## 5. A fixed-direction repair can fail for every direction

Accepted file: `positivity/SINGLE_DIRECTION_REPAIR_OBSTRUCTION.md`.

For 1/6<κ≤1/2, let L(r)=log(e/r) and

y(x)=r^{1/2}L(r)^κ x on B₁, with y(0)=0.

The radial radius R=r^{3/2}L^κ is strictly increasing from zero to one, and its radial derivative is r^{1/2}L^κ q with q=3/2−κ/L between one and 3/2. Thus y is a C¹ radial homeomorphism with identity trace. Its gradient is bounded and

J=r^{3/2}L^{3κ}q,
∫J^{-2}≈∫₀¹ dr/[r L^{6κ}]<∞.

All original class conditions hold for every positive coefficient tuple. In target variables its inverse determinant is

K(z)=1/[R L^{2κ}q]≈1/[|z|log(e/|z|)^{2κ}].

The exact relation log(e/R)=3L/2−1/2−κlog L implies L≤log(e/R)≤3L/2, so the comparison is uniform. Projection onto any two-dimensional plane has source-volume density

ρ(z′)=∫_{(z′,t)∈B₁}K(z′,t)dt.

For h=|z′| small this is at least c∫_{2h}^{1/2}dt/[t log(e/t)^{2κ}], which diverges as h↓0. The density is essentially unbounded on positive-measure sets, rather than merely singular on one fiber.

Any same-trace W^{1,6} v with v−y parallel to one fixed direction and J_v≥δ>0 would preserve this projection marginal. The full-class degree/area formula gives

∫f(πy)=∫f(πv)≤δ^{-1}∫f(πv)J_v
=δ^{-1}∫B₁ f(πz)dz≤2δ^{-1}∫f.

This would bound ρ by 2/δ a.e., a contradiction. No pointwise homeomorphism of v was assumed. Radial symmetry covers every fixed target direction.

The map is a nonminimizer by affine uniqueness. The obstruction concerns a uniform bound on the whole ball and a fixed target direction. It does not exclude varying-direction rank-one differences, coupled multi-component changes, merely local lower bounds, or a theorem specific to actual minimizers. These limits are preserved in the final report.

## 6. Reference ceilings, normalization, and local boundary data

Accepted file: `positivity/REFERENCE_CEILINGS_AND_LOCALIZATION.md`.

For any smooth positive-J same-trace reference H, the null-Lagrangian volume is fixed:

∫Ω det DH=|G(Ω)|=:V.

If m_H=min σ_min(DH), then m_H³|Ω|≤V. Hence the safe threshold m_H/(2CΩ) in the earlier reference truncation has a finite ceiling depending only on V/|Ω| and the domain constant. Choosing references with increasingly large gradients also loses the explicit upper comparison constant. This rejects an unproved uniform high-threshold interpretation of that particular construction; it is not a no-go theorem for every adaptive method.

The same calculation on a ball with a genuine same-trace local reference yields m_H≤(average J_y)^{1/3}. The final statement correctly uses L⁶-Lebesgue points of Dy to infer convergence of local averages of J_y. The initial ordinary-Lebesgue-point wording was corrected during review; no substantive theorem changed.

For Aε=diag(1,1,ε), multiplication of the energy by ε² gives, uniformly on compact subsets of GL⁺,

ε²W(AεM)→d(det M)^{-2}.

For the exact relative-minor excess from pass 3,

ε²R_{Aε}(AεM)→d[(det M)^{-2}+2det M−3].

At M=diag(2,1/2,1), the latter limit is zero while |AεM−Aε|²=5/4. Thus there is no center-independent lower bound of this normalized excess by an unweighted fixed positive strain norm. This is a finite-dimensional loss of coercivity, not a Gamma-convergence claim or an exclusion of correctly weighted excess arguments.

The logarithmic cylindrical shear from pass 2 has bounded positive J and finite energy but non-Lipschitz trace on every sufficiently small centered sphere. The north-pole comparison gives difference quotient of order ρ^{-1/3}log(e/ρ)^{-σ}, which diverges. A Lipschitz map on a ball has a Lipschitz continuous trace, so no Lipschitz replacement can match those local sphere traces. Again this is an admitted nonminimizer: it shows a local reference hypothesis cannot be borrowed from class membership or from the smooth outer trace.

## 7. Controlled annular tangent exclusion and audit refinement

Accepted frozen files: `counterexample/ANNULAR_TANGENT_EXCLUSION.md` and `counterexample/DEGENERATE_PROFILE_RESTRICTION.md`.

The lane theorem assumes componentwise weighted rescalings converge in C¹ on a fixed closed annulus to a C² weighted-homogeneous profile with positive angular determinant, positive sorted exponents, and sum s>3. It correctly obtains m>1/2 and s<9/2 from absolute continuity of the shrinking-annulus energy, including strict exclusion of both equality cases. No disjointness of annuli is required.

Each selected physical annulus has bounded gradients and a positive determinant lower bound, so compact additive first variations are legitimate there. This does not assert ordinary stationarity across the singular point. Stress rows, rather than their divergences, are normalized. The third-row barrier exponent is α1+α2−2−3(s−3); its gap below the positive row is η=2(3α1+α2+2α3−6). If η>0, the limit is the barrier-only weak row equation. If η≤0, the first row becomes scalar 6-harmonic, with the four positive relative gaps checked explicitly. Uniform coefficient convergence is sufficient; no derivative of a remainder and no second-derivative convergence is used.

Exact homogeneity of the limit extends its limiting equation beyond the annulus. The inherited positive-degree ray obstruction and scalar removability argument then exclude it. The limiting angular determinant's positivity is explicit: finite original energy does not force an asymptotic angular barrier integral to remain bounded after normalization.

The localized regular-axis statement is also accepted. In the η>0 range, a possibly angularly degenerate profile cannot have φ1=φ2=0 at a positive-J angle. The proof is restricted to a positive-J neighborhood. It does not infer a global degree or the existence of such an axis preimage for an arbitrary degenerate profile.

### Independent refinement

`audit/WEAK_ANNULAR_REFINEMENT.md` proves that strong W^{1,∞} convergence of the rescalings to a C¹ positive-angular-J homogeneous profile already suffices. Essential gradient bounds justify the physical weak first variation and L∞ stress passage. In the barrier range, the local C¹ inverse-coordinate change X=U(z) turns the equation into

∂_{X3}[J_U(U^{-1}(X))^{-3}]=0.

Continuity makes the scalar constant along each local vertical segment. At a regular third-axis preimage, J_U=r^{s−3}j varies strictly along the corresponding radial segment, a contradiction. This removes the need to differentiate the limiting determinant. In the scalar range, the weak spherical identity and removable-puncture estimate require only first derivatives. Scalar 6-harmonic regularity is applied only after weak removability is proved.

This refinement is independently authored in the audit and does not alter the frozen lane files. It still assumes a strong annular tangent and a positive angular determinant. No theorem guaranteeing these properties for arbitrary minimizers has been proved, and no boundary singularity is addressed.

### Angular repair diagnostic

The map y=(x₁,x₂,x₃³r^{-3/2}+x₃r) has full trace of the global smooth diffeomorphism G=(x₁,x₂,x₃³+x₃). Its determinant is

J=r^{1/2}μ²(3−3μ²/2)+r(1+μ²)>0 off zero.

The angular integral of J^{-2} is comparable to r^{-7/4}, leaving integrable radial power r^{1/4}. Its bounded gradient gives finite positive energy. The leading angular determinant vanishes on the equator, so the example genuinely verifies the need to keep angular repair possibilities distinct.

It is not stationary. Along the positive third axis, J=3t^{1/2}/2+2t and the third barrier divergence is (8d/9)t^{-5/2}(1+o(1)), while the positive stress divergence is O(t^{-1/2}). The leading coefficient and powers were independently checked. The earlier conditional stationary C^{1,β} theorem supplies an additional rejection because this map is C^{1,1/2}. Neither route certifies a minimizer.

## 8. Exact compatible interpolation example

Accepted file: `exact/COMPARISON_AND_TANGENT_CERTIFICATION.md`, with its script and certificate.

The exact lane constructs a compactly supported divergence-free Hamiltonian vector field whose time-one flow is diag(A,A^{-1},1) on a small core. A smooth radial rotation by π on that core, and zero outside a larger ball, has determinant one by the rank-one determinant lemma. Their composition is a global smooth volume-preserving identity-trace diffeomorphism u_A with core gradient diag(−A,−A^{-1},1).

The affine blend with the identity has determinant

[1−(A+1)t][1−(1+A^{-1})t]

on the core. It is negative for 1/(A+1)<t<A/(A+1). In particular A=2,t=1/2 gives −1/8. For any prescribed t∈(0,1), some A makes that amplitude fail. This does not say every sufficiently small amplitude fails for each fixed smooth map.

Support scaling u_{A,ε}(x)=εu_A(x/ε) gives gradient L⁶ difference O(ε^{1/2}), function L⁶ difference O(ε^{3/2}), uniform difference O(ε), and positive energy excess exactly ε³Δ_A. The determinant remains one. Strict affine uniqueness verifies that the examples are nonminimizers. They show that arbitrarily small total distance and total excess do not alone make a blend admissible; normalized small-scale excess on the distorted core stays large, so no proper scale-invariant local regularity theorem is refuted.

The exact lane also independently checks the preceding graph identities, one-sided moments, inverse interval obstructions, stress exponents, angular repair, and projection marginal. Its frozen certificate has 55 passing exact checks.

## 9. Primary-source inspection and validation record

The only new primary source required for this pass's weak-calculus screen is:

Piotr Hajłasz, Armin Schikorra, Jeremy T. Tyson, *Homotopy groups of spheres and Lipschitz homotopy groups of Heisenberg groups*, arXiv:1301.4978v3, 28 November 2013.

https://arxiv.org/pdf/1301.4978v3

The local PDF has 302137 bytes and SHA-256 `005b66fc45a888d3d3dd2f44b46d70188ba65296c4f2ad563ceaad513d9a8783`. The auditor read the statement and proof and visually inspected printed pp.11–12. Lemma 4.1(2) assumes p≥ℓ+1 and bounded smooth form coefficients and derivatives; part (3) assumes p≥2 for the differentiated product rule. These are accurately quoted as sufficient hypotheses of this theorem. They do not rule out every possible theorem using the additional dual-energy structure. The graph proof itself gives a direct high-exponent boundary argument.

The scalar regularity input remains the previously inspected Uhlenbeck (1977) corollary on printed p.222, used with its parameter p=4. Previous source hypotheses and inverse-baseline proofs are inherited through the sealed pass-3 audit, rather than replaced by unverified broad claims.

Executed validation:

- `audit/verify_audit.py`: 40 exact algebra/source-metadata checks, all passed.
- `exact/verify_comparisons.py`: 55 exact checks, all passed.
- `positivity/verify_repairs.py`: 22 symbolic checks, all passed.
- Manual analytic checks: admissibility before differentiation; full-boundary flux; source and target measure factors; essential rather than isolated-point marginal divergence; exact comparison endpoint hypotheses; normalization exponents; whole-domain versus local conclusions.

Only two coordination corrections were requested: the L⁶-Lebesgue qualifier and synchronization of the structured-cutoff theorem's accepted status. Neither changed the accepted mathematical scope. No hidden coercivity, ellipticity, inverse-derivative, or boundary assumption remains in the accepted statements.

## 10. What still prevents a benchmark resolution

There is no high-level admissible truncation with a proven useful energy bound for arbitrary minimizers. Structured inverse cutoffs now have a validated class mechanism, but positive determinant and finite V remain separate, potentially failing conditions. The weighted mixed moment needs a feasible determinant-raising endpoint; a universal fixed-direction repair is false on the full admissible class. No minimizer-specific marginal estimate has replaced that missing construction.

No unconditional L^{6+δ} gradient gain, ordinary stress integrability at the baseline, Dini gradient estimate, tangent existence theorem, or boundary-collar Jacobian bound has been established. None of the explicitly nonminimizing maps falsifies the conjecture. The exact fixed-exponent benchmark, and the broader original adequate-growth question, therefore remain distinct unresolved questions after this pass.
