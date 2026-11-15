# Independent initial source/scope reconstruction — record 23331080

No verdict. This file is written after personally reading the complete actual four-page PDF, all272 lines/13221 bytes of controlling TeX and all four individual page rasters, before any foreign primary body, deposited program/results, archived/current review, triage or peer/root scientific finding. Earlier work by this agent acquired opaque native bytes and identity/checksum metadata only; that exposure is disclosed in INTAKE_AND_EXPOSURE.json. No target scientific content was read during acquisition. Other paper packets remain immutable. Root117's scientific gate is closed.

## Exact object, question and mathematical quantifiers

The reviewed native version is1.0, manuscript/declared date12October2026, DOI10.5281/zenodo.23331080. Record creation/update are13October2026UTC and are distinct. Actual PDF SHA-256:d5c31033f40afaa8dbd1f8642d7c729dfd7a858553e1c1c0856520a10f23bedd. Controlling TeX SHA-256:2f38b06e7243966af7afda844edc4b6672be38bb9c10759816c2cce2e4e75bfe. SOURCE_READY.json SHA-256:3833194084fd0343a18c5640400418893203c6e575272997c114bc326d34e2af. The actual source asset order is PDF then ZIP; all40 original payloads remain opaque before this initial except the controlling target TeX.

The paper answers a UNIVERSAL total-space positivity-preservation question by ONE explicit compact rank-two example for the particular probability-normalized relative anticanonical flow actually defined by Naumann. It does not claim failure for all initial metrics, all bundles or the Griffiths conjecture. Set S=P¹, E=O_S(1)⊕O_S(1)=O_S(1)⊗C². With X=P(E*) and f_*O_E(1)=E, X=P¹_s×P¹_z, O_E(1)=O(1,1), L=O_E(2)=O(2,2). E is ample and even has obvious Griffiths-positive metrics. K_(X/S)^−1=L⊗f*(detE)^−1, so L restricts fiberwise to the anticanonical line, with a determinant frame used to express densities.

The exact flow on a smooth fiberwise positively curved Hermitian weight φ_t on L is

    ∂tφ_t = log[MA(φ_t)/μ_(φ_t)],
    μ_φ = e^(−φ)dA_z / I(s),  I(s)=∫_(P¹)e^(−φ(s,z))dA_z.

MA is curvature volume divided by its fixed fiber mass. Both measures are probabilities. The density formula uses compatible anticanonical frames, not an arbitrary fixed background-area scalar interpretation. Changing determinant frame or adding a base function cancels in μ. In local fiber coordinate g=φ_(z zbar)>0, the claimed scalar equation is

    φ_t = log g + φ + log I + C,

where C is a fixed convention constant. The reaction coefficient for THIS L-weight and THIS time is1. Dropping only the fixed MA mass is claimed to change a time-only gauge and not curvature; dropping logI changes the actual flow and is outside scope.

Theorem1 asserts a smooth globally strictly positive initial metric e^(−φ0) on the compact X whose actual smooth nonlinear solution obeys, at the fixed point (s,z)=(0,0), for finite t≥0,

    (φ_t)_(s sbar)(0,0)=1/96−(1−e^(−2t))/24.

At t*=(log2)/2 this is exactly−1/96, although fiberwise curvature remains positive. Rotational symmetry makes the mixed coefficient zero on s=0, so this horizontal coefficient is both the geodesic curvature there and the actual curvature on tangent ∂/∂s. The positive square-root metric e^(−φ0/2) on O_E(1) supplies the source question's initial-data category. The first negativity occurs after t>(1/2)log(4/3). No infinite-time limit or base-direction convergence is needed.

## Independent reconstruction of the explicit proof

Put ε=1/96, δ=1/4, u=|s|², v=|z|², p=u/(1+u), x=v/(1+v). The initial weight is

    φ0=2log(1+u)+(2−ε)/(1+u)+2log(1+v)+δ p x².

The logarithms supply O(2,2) transitions; p,x are globally smooth moment coordinates. At s-infinity the correction (2−ε)/(1+u) becomes (2−ε)|w|²/(1+|w|²), and p=(1+|w|²)^−1. At z-infinity x²=(1+|ζ|²)^−2 after subtracting the fiber transition. Thus no cutoff, local extension or degenerate boundary patch is silently needed.

In product Fubini–Study unit frames, direct radial differentiation is claimed to give

    A=4p+(ε+δx²)(1−2p),
    B=2+2δpx(2−3x),
    Q=4δ²p(1−p)x³(1−x).

Here Q is the squared mixed coefficient. For EVERY p,x in the CLOSED square[0,1]² (including both infinity charts), set A0=ε+(167/48)p, B0=3/2, Q0=p/4. The polynomial identities

    A−A0=δx²+2δp(1−x²),
    B−B0=2δ[(1−p)+p(1−x)(1+3x)],
    Q0−Q=4δ²p[1−(1−p)x³(1−x)]

are nonnegative there. A0,B0>0 and

    AB−Q ≥ A0B0−Q0 = 1/64+(159/32)p > 0.

These are continuum certificates, not grid samples. At p=x=0, A=ε>0; at p=x=1, B=3/2>0, so the fragile endpoints are explicitly included. Dividing φ0 by2 halves a positive curvature form and is a globally compatible square root on O_E(1).

Finite-time smooth existence on X×[0,∞) is an explicit imported analytic assertion from Naumann Theorem5, via fiberwise normalized anticanonical Kähler–Ricci flow/Berman. Its hypotheses and precise finite-time parameter regularity MUST be authenticated in actual primary bodies; a generic infinite-time convergence claim is not a substitute. The paper gives an independent uniqueness argument: |logI(φ)−logI(φtilde)|≤||φ−φtilde||∞, and the logarithmic Hessian difference is nonpositive at a fiber maximum. Thus D⁺||difference||∞≤2||difference||∞, proving uniqueness and preservation of base U(1) symmetry.

At s=0, φ_s=φ_sbar=φ_(s zbar)=0 for all finite t. The central fiber starts at 2log(1+v)+2−ε, where normalized MA and μ agree, so it remains exactly stationary. Set w=(φ_t)_(s sbar)(0,z), g_F=2/(1+v)² and Δ_F=((1+v)²/2)∂z∂zbar. The Laplacian is nonpositive on nonconstant eigenmodes. Differentiation of the ACTUAL scalar flow, not a perturbative ansatz, gives

    (logg)_(s sbar)=Δ_Fw,
    I_s=0, I_(s sbar)=−I∫w μ_F,
    w_t=Δ_Fw+w−∫w μ_F,  w(x,0)=ε+δx².

The derivative-under-integral step needs smooth parameter dependence and compact fiber, precisely the imported finite-time input. Base symmetry kills the cross terms that could otherwise invalidate this closure. The nonlocal negative mean term is essential. At x=0 initially, w_t=−δ/3<0, consistent with positivity loss despite w>0 initially.

The pushforward μ_F is uniform dx on[0,1]. Independently, v→x=v/(1+v) turns Δ_F into(1/2)[x(1−x)∂²+(1−2x)∂]. For P1=2x−1 and P2=6x²−6x+1, the means vanish and eigenvalues are−1,−3. Since x²=1/3+P1/2+P2/6, the exact solution is

    w=ε+δ/3+(δ/2)P1+(δ/6)e^(−2t)P2.

Its mean is constant; the difference of two such solutions with identical data has zero mean and solves a_t=Δ_Fa+a. The maximum principle for e^(−t)a proves uniqueness. At x=0, this reduces to ε−δ(1−e^(−2t))/6, giving the stated coefficient and finite strict negativity.

## Exact normalization/source discrepancies and historical boundaries

The paper expressly separates the actual Naumann defining flow(13) from a literal same-weight/time reading of r c in the displayed evolution equation(14). Its product calibration is φprod=2log(1+|s|²)+2log(1+|z|²), stationary for the probability-ratio flow, with c=2 and(logI)_(s sbar)=−2 at the central basepoint, while fiber Laplacian and Kodaira–Spencer terms vanish. A same-convention r=2 reaction would incorrectly give c_t=2. This is a claimed convention discrepancy, not a claimed explanation of the author's intent. Actual primary formulas must be examined before accepting the source identification.

The alternative variables ψ=φ/r, τ=t/r transform the scalar PDE into ψ_τ=logψ_(z zbar)+rψ+log∫e^(−rψ)dA+C′. Rescaling weight AND time leaves the sign-loss phenomenon but not the numerical t/formula unchanged. A frozen denominator μ_(φ0), a missing logI, a different background density or an unannounced r-factor would change the problem.

The source flow construction is old. Berman's earlier preservation theorem is said to concern a NONnormalized weight flow, whereas his Remark4.11 already discusses normalized anticanonical negativity in effectively parametrized Fano families. The target claims a locally isotrivial P¹-bundle application, not the first positivity loss for every normalized relative flow. It declines historical firstness and records an unrecovered relevant Naumann habilitation listed in2025. That specific lead must remain explicit; unsuccessful searching cannot certify its contents or current worldwide openness. No statement about Griffiths' conjecture, all special metrics or unrelated normalizations is licensed.

## Distinct validation/attack families and falsifiable success criteria

1. **Actual-question and bundle interface.** Read the full relevant OWR contribution and actual published Naumann §3.3. Match rankr, projectivization/pushforward, determinant twist, initial O_E(1)-root metric, amplitude and total-versus-fiber positivity. A theorem for a changed flow or input category is not an answer to the original question.
2. **Defining PDE, gauge and coefficient attack.** Inspect actual equations(13),(14), probability measures and time/weight conventions. Independently derive the product calibration and scaled variables. An extra base function, denominator frozen in time, or r-factor mismatch is a checkable falsifier.
3. **Analytic import and symmetry.** Authenticate finite-time smooth existence with smooth compact-base dependence and persistent fiber positivity in actual Theorem5/Berman. Test uniqueness, stationary central fiber and differentiability under the fiber integral without relying on unproved base regularity at infinite time.
4. **Global initial-data geometry.** Derive A,B,Q and all chart transitions independently, test both infinity endpoints and prove determinant positivity on the whole square. Verify the O_E(1) square root is globally defined and retains positivity. A small sampled grid cannot establish this part.
5. **Exact jet closure and spectral sign.** Recompute all omitted mixed terms, the sign of(logI)_(s sbar), Fubini–Study Laplacian scale, Legendre eigenvalues, constant mode and the exact finite-time solution. Distinguish an actual nonlinear derivative identity from a formal linearization.
6. **Priority and contribution.** Read Berman's actual preservation/normalized-negativity statements and the projective-bundle source. Locate the2025 habilitation if possible without outreach; preserve failures honestly. Credit old flow/earlier negativity and bound any exact-example contribution without firstness claims.
7. **Deposited support/certificate fidelity.** Only after this seal, inspect actual supplied programs and stated finite results, identify dependencies, assertion/optimization behavior and writing routes, and reproduce only meaningful small checks in owned outputs. Do not read archived audit opinions as a substitute for proof. All40 original payloads and mixed native JSON/header objects remain byte-identical.
8. **Limiting/degenerate cases.** Examine ε→0 initial semipositivity versus actual ε>0, δ=0 stationary product behavior, t=0, t*, onset time, mean preservation and alternate unnormalized flows. Require the exact stated finite example, not a narrowed rescue. If a substantive gap is found, preserve it and stop repair.

Success is support for the FULL original stated finite-time counterexample with exact normalization, imports and prior-work limits. A source mismatch or unsupported analytic premise requires precise evidence, not promotion of another equation or a smaller theorem. Keep all117science local until the explicit root117 initial gate; only early/final seal and custody metadata may be sent. No source/prior packet/config/site/core/Sheet/Git/deploy/redirect/outreach changes.
