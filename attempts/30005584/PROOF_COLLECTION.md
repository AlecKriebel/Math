# Consolidated theorem guide and exact scope

## Original question and common analytic setting

Original OWR29/2023, printed p.1665 (repeated OWR11/2025, p.498): relate the unrestricted four-dimensional expander degrees of X₁, X₂ and X₁#∂X₂, and compute the unrestricted degree of D³×S¹. The precise orbifold, cover, boundary, regularity and localized-degree definitions are in SOURCE_CHECKPOINT.md, with complete primary inputs in source_manifest.json. The answer remains **unsolved 5/5**.

For the analytic partials, fix a member of the known complete gradient expanding family on S¹×R³:

`g=a(r)²dθ²+dr²+b(r)²g_S²`, `f=f(r)`, `Ric+Hess f+(1/2)g=0`.

Here θ has period 2π, a(0)>0, b(0)=0, b′(0)=1, and all origin conditions are the smooth ones of the source. The nontrivial AC family has f″(0)<0. At infinity a/r and b/r have positive finite limits, with the published C² conical estimates. All tensor operators use the real weighted L² space with density e^(−f)dvol_g and the Friedrichs/closed form domain. The Einstein form is

`Q(h)=∫(|∇h|²−2<Rm(h),h>) e^(−f)dvol_g`.

Bamler–Chen Proposition 5.38 supplies the discrete self-adjoint spectrum and compact form embedding for each fixed soliton. The curvature convention is Rm(g)=Ric. All origin arguments refer to the smooth base R³, not a half-line with an artificial boundary. Positive-circle and conical hypotheses are essential; the collapsing-circle S²×R² family is not included in these analytic statements.

## Logical structure of the five turns

### Turn 1: the symmetry-transfer obstruction

The finite-dimensional examples are proved directly, including properness and exact degrees. They show that knowing the restricted degree and having a connected compact symmetry group does not alone provide full regular targets or determine the ambient integer degree. A conditional degree comparison is stated only under all of its full-fiber, regularity and normal-orientation hypotheses. No example is a Ricci soliton or a refutation of the expected degree equality.

### Turn 2: parity and a reducing positive subspace

The finite negative space is a real representation of the circle. Every nonzero Fourier representation has even dimension, giving equality modulo two of the full index and the circle-fixed index. This parity statement does not rule out Fourier kernels. The exact connection/curvature contraction gives a positive reducing form on the coexact circle/sphere mixed sector, with the proper weighted cutoff argument.

### Turn 3: the full reflection-odd circle-fixed form

Write B=R³ with g_B=dr²+b²g_S², K=∂θ, and `h=K^flat odot alpha`, where odot is the sum of the two tensor products, with no half. Put F=f−3log a. The exact form identity, after the positive circle-volume normalization, is the weighted Hodge energy

`Q(h)=2(2π)∫(|d alpha|²+|delta_F alpha|²) a³e^(−f)dvol_B`.

The proof verifies the soliton substitution, form closure, smooth core and weighted endpoints. The kernel vanishes by exactness of closed one-forms on R³ and the separated weighted-harmonic ODE plus finite-energy cutoffs. Thus the entire odd sector has neither negative nor zero eigenmodes. This strengthens, rather than changes, the turn-2 coexact statement.

### Turn 4: the full reflection-even circle-fixed form

Write `h=S+q(a dθ)²`, ℓ=log a, F₁=f−ℓ, and dμ=a e^(−f)dvol_B. Define

`Q₀(S)=∫(|∇^B S|²−2<Rm_B(S),S>+2|S(dℓ,.)|²)dμ`,

`ℛS=<Hess_B ℓ,S>`, `H=−Δ_(F₁)+2|dℓ|²`.

Then `Q_even(S,q)=Q₀(S)+<q,Hq>+4<q,ℛS>`. The scalar block has a positive bounded inverse, and

`Q_eff(S)=Q₀(S)−4<ℛS,H⁻¹ℛS>`

has exactly the even negative index. Its kernel corresponds bijectively via `q=−2H⁻¹ℛS`. The proof is a closed-form congruence/inertia argument; it does not identify the nonzero spectra by a unitary transformation. The residual nonspherical tensor sign is open.

### Turn 5: explicit uniform and spherical-degree bounds

The scalar soliton equation gives `Δ_(F₁)ℓ=λ`, with λ=1/2 here. The positive smooth function `w=a^(−√2)` satisfies `Hw=√2 λw`, yielding the exact ground-state transform and uniform inequality `H≥√2 λ` on the form domain. This improves the per-soliton gap proved in Turn 4; historical turn-4 statements remain valid.

In scalar spherical degree j, the same transform yields `H_j≥V_j=√2 λ+j(j+1)/b²`. The variational inverse inequality, with no commutation assumption, gives

`Q_eff(S)≥Q₀(S)−4∫|ℛS|²/V_j dμ`

for tensors in degree j. A positive lower bound on this explicit local tensor form would remove that sector's negative and zero contribution. No such estimate for every actual profile is asserted. The scalar uniformity cannot be promoted to uniform regularity of the full family or to an integer degree computation.

## Remaining gaps and source credit

The nonspherical tensor sign, nonzero Fourier kernels, unrestricted fiber classification, full symmetric regularity, canonical orientation comparison and boundary-connected-sum gluing remain separate missing steps. The final status is a scoped partial manuscript after five substantive author turns. Known soliton existence, conicality, monotonicity and the restricted degree are credited to the pinned sources, especially Rajan; the ambient spectral/degree theory is credited to Bamler–Chen. The source PDFs and full imported record are not publication artifacts.
