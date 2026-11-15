# Independent derivations and bounded falsifiers

These arguments follow the reconstruction sealed in INITIAL_RECONSTRUCTION.md before foreign bodies or deposited code/results. No sibling scientific findings were consumed. They concern the whole stated counterexample, including its exact flow and initial-data class. The computer checks are algebraic supplements to the following proof, not a substitute for the analytic import.

## 1. Intrinsic object and defining equation

Use the quotient convention f_*O_E(1)=E. For A=O_{P¹}(1) and E=A⊗C², projectivization cancels A*, so X=P(E*)=P¹×P¹. The quotient line is A⊠O_{P¹}(1), hence O_E(1)=O(1,1), L=O_E(2)=O(2,2). Thus E is ample, det E=O(2), and K_{X/S}^{−1}=L⊗f*(det E)^{−1}=O(0,2). A positive metric on L has a positive square-root metric on the specified O_E(1); this is not an abstract existence claim about an arbitrary square root.

In compatible determinant/anticanonical frames the fiber density is e^{−φ}dA. Under a determinant-frame change its numerator and integral acquire the same positive base factor. Thus μ=e^{−φ}dA/I, I=∫e^{−φ}dA, is intrinsic. The fiber curvature has fixed mass V; in dimension one MA=g dA/V with g=φ_{z zbar}, allowing a harmless fixed convention factor in V. Consequently the stated probability-ratio flow is exactly

    φdot=log g+φ+log I+C.                         (D1)

Its reaction coefficient in this L-weight and time is one. For any smooth base function b(s), replacing φ by φ+b multiplies I by e^{−b} and leaves the right side invariant; therefore the lifted flow with initial φ0+b is φ_t+b. This is a time-independent base gauge, not permission to add arbitrary time-dependent horizontal curvature. Removing the fixed curvature mass adds a constant to the right side and hence only a time-dependent spatial constant to the solution. Removing log I changes the flow.

## 2. Complete global initial positivity

Write ε=1/96, δ=1/4, u=|s|², v=|z|², p=u/(1+u), x=v/(1+v). The initial weight is

    φ0=2log(1+u)+2log(1+v)+(2−ε)/(1+u)+δ p x².

The first two terms transform as O(2,2). The remaining terms are smooth functions on the two compact projective factors. For example, s→1/w changes p to 1/(1+|w|²) and 1−p to |w|²/(1+|w|²); subtracting 2log|s|² makes the base logarithm 2log(1+|w|²). The analogous fiber transition makes x²=(1+|ζ|²)^{−2}. The joint infinity chart is obtained by both operations. All four charts are checked by the owned verifier.

For a radial function F(u,v), ∂s∂sbar F=F_u+uF_uu, ∂z∂zbar F=F_v+vF_vv, and |∂s∂zbar F|²=uv F_uv². Differentiating the displayed weight gives its product-Fubini–Study normalized Hessian entries

    A=4p+(ε+δx²)(1−2p),
    B=2+2δpx(2−3x),
    Q=4δ²p(1−p)x³(1−x),

where Q is the squared off-diagonal modulus. Define a0=ε+167p/48, b0=3/2, q0=p/4. On the closed square 0≤p,x≤1,

    ra=A−a0=δ[x²+2p(1−x²)] ≥0,
    rb=B−b0=2δ[(1−p)+p(1−x)(1+3x)] ≥0,
    rq=q0−Q=4δ²p[p+(1−p)((1−x)(1+x+x²)+x⁴)] ≥0.

The last decomposition follows from 1−x³(1−x)=(1−x)(1+x+x²)+x⁴ and has only visibly nonnegative factors. The determinant has the exact identity

    AB−Q=(a0b0−q0)+ra B+a0 rb+rq,
    a0b0−q0=1/64+(159/32)p >0.                  (D2)

Since B≥b0>0 and a0>0, every term used in (D2) has the stated sign. Both endpoints p=1 or x=1 are included. At the particularly small horizontal endpoint p=x=0, A=ε>0; at p=x=1, B=3/2>0. This proves strict positive definiteness on the entire compact X. A finite sample is not being used to infer a universal inequality. The positive root weight φ0/2 supplies the source's exact initial metric class.

## 3. Applicable finite-time analytic input and uniqueness

The imported assertion is smooth finite-time existence and persistent fiber positivity for the normalized relative flow on O_E(r), not horizontal regularity of an infinite-time limit. The actual Naumann published Theorem5 (printed1519, physical15) states smoothness on X×[0,∞), and its proof identifies the fiberwise denominator with the anticanonical probability measure. The relevant assumptions are a smooth holomorphic projective bundle, smooth fiberwise positively curved initial metric and projective-space/Fano–Kähler–Einstein fibers. Here X→P¹ is a proper smooth product with fiber P¹, and global positivity proved above is stronger than fiber positivity. Nontrivial holomorphic vector fields on P¹ do not obstruct the finite-time existence assertion. Naumann's Remark1 on printed1517 explicitly distinguishes the potentially unclear horizontal regularity of a limit. That stronger limit assertion is unused.

Berman's actual Theorem4.1 gives finite-time existence/smoothness of the canonical/anticanonical flow; the extra absence-of-holomorphic-vector-fields and existence-of-KE conditions in its convergence clause do not become hypotheses for finite-time smoothness. His Section2C records local uniform finite-time parameter stability. We do not adopt any unnecessary blanket uniqueness claim about all Kähler–Einstein fixed points modulo constants when automorphisms are present. Initial-value uniqueness needed here has a separate direct proof:

For v=φ−ψ on a compact fiber, e^{−||v||∞}I(ψ)≤I(φ)≤e^{||v||∞}I(ψ). Thus |log I(φ)−log I(ψ)|≤||v||∞. At a maximum of v, its fiber Hessian is nonpositive, so the difference of logarithmic Hessians is nonpositive. Equation(D1) applied to v and −v gives D⁺||v||∞≤2||v||∞. Grönwall proves uniqueness for equal initial data. This argument is unaffected by adding compatible local frame transition functions, because the difference is a globally defined fiber scalar.

## 4. Exact derivative of the nonlinear solution

Base rotations lift to the line bundle and preserve the initial weight in the chosen finite frame. Intrinsic flow equivariance and initial-value uniqueness preserve that symmetry. At s=0 this implies φ_s=φ_sbar=φ_{s zbar}=0 for every z and every finite t. Since these identities hold along the whole fiber, also g_s=g_sbar=0 there.

At s=0 initially, φ=2log(1+v)+2−ε. Normalized curvature and anticanonical volume coincide, so the central fiber remains exactly stationary by uniqueness. Put g_F=2/(1+v)² and w=φ_{s sbar}(0,z,t). The smooth finite-time parameter dependence just authenticated permits differentiating(D1), including under the compact-fiber integral. The nonlinear quadratic terms vanish by the first-base-derivative identities:

    (log g)_{s sbar}=g_F^{−1}w_{z zbar},
    I_s=0,
    I_{s sbar}=∫(|φ_s|²−φ_{s sbar})e^{−φ}dA
              =−I∫w μ_F,
    (log I)_{s sbar}=−∫w μ_F.

Hence the actual second base derivative, with no small-parameter truncation, satisfies

    w_t=Δ_Fw+w−∫w μ_F,
    w(x,0)=ε+δx²,
    Δ_F=(1+v)²∂z∂zbar/2.                       (D3)

The mixed coefficient is zero, so w is the Schur complement/geodesic curvature and is also the curvature on the actual horizontal vector ∂/∂s. A negative w therefore witnesses genuine failure of total-space positivity even though the fiber direction stays positive.

## 5. Closed solution, endpoints and exact finite loss

The normalized radial measure is dv/(1+v)²=dx, so mean in(D3) is ordinary integration on [0,1]. For an arbitrary smooth radial F,

    Δ_FF=[x(1−x)F″+(1−2x)F′]/2.

The owned verifier checks this as a generic-function chain rule, not only on finitely many monomials. Put P1=2x−1, P2=6x²−6x+1. They have zero means and Laplacian eigenvalues −1 and −3. Since x²=1/3+P1/2+P2/6, the solution is

    w=ε+δ/3+(δ/2)P1+(δ/6)e^{−2t}P2
     =ε−δ(1−y)/6+δ(1−y)x+δyx², y=e^{−2t}.  (D4)

This has initial value ε+δx² and solves(D3) exactly. To identify it with the actual derivative, integrate the difference equation: its mean is constant and initially zero. The difference then satisfies a_t=Δ_Fa+a; the maximum principle for e^{−t}a proves zero difference. The degenerate coefficients of the radial operator at x=0,1 are simply smooth sphere poles; the maximum principle is on the compact P¹, not an unsupported interval boundary condition.

For finite t≥0, 0<y≤1 and w_x=δ[(1−y)+2yx]≥0. At the actual pole x=0,

    w(0,t)=1/96−(1−e^{−2t})/24.

It starts strictly positive, crosses zero at t=(log(4/3))/2, and at t*=(log2)/2 is exactly −1/96. Its initial derivative is −1/12. None of these conclusions uses t→∞ or a formal time Taylor approximation. Taking δ=0 makes the constant-mode generator vanish; taking ε=0 would remove the strict initial positivity margin and is not the example being promoted.

## 6. Source convention falsifier and necessary scope limits

The product weight φ_prod=2log(1+u)+2log(1+v) defines a positive L-metric. Its probability measures agree for every basepoint, so it is exactly stationary for the defining flow. Along s=0, c=2, Δc=0, the metric-induced Kodaira–Spencer term vanishes, and (log I)_{s sbar}=−2. The coefficient-one evolution gives 0=2−2. A literal same-weight/time reading of the printed rank-two r c term in Naumann's equation(14) instead gives 2. This is a concrete calibration inconsistency with that literal reading, not an attempt to determine undocumented authorial intent. The target explicitly identifies the discrepancy and derives its result from the unambiguous probability-ratio defining equation(13).

If ψ=φ/r and τ=t/r, then φ_t=ψ_τ and φ_{z zbar}=r ψ_{z zbar}; (D1) becomes

    ψ_τ=log ψ_{z zbar}+rψ+log∫e^{−rψ}dA+C′.

This consistent weight-and-time conversion allows a coefficient r. It does not permit transporting the original exact coefficient/time formula unchanged. Positive metric rescaling preserves the sign-loss event but does not certify other normalization choices.

Seven meaningful algebraic negative controls are rejected by verify_exact.py: literal same-convention rank-two product reaction, omission of the evolving normalization, reversed mean sign, reversed Laplacian sign, insertion of rank-two reaction without conversion, decay e^{−t} instead of e^{−2t}, and an already-negative initial pole. The first has residual2; omitting the mean gives residual−3/32. These distinguish the asserted phenomenon from nearby equations and a degenerate initial metric. They are bounded diagnostics, not a numerical PDE campaign.

## Strongest verified claim and exact remaining gap

The full stated finite-time counterexample for the declared probability-normalized O_E(r)-weight flow is supported at the explicitly cited classical smooth parabolic input level. No substantive mathematical gap was found. Computation does not constitute a formal PDE existence proof. Historical first priority remains uncertified: the actual university-listed2025 Naumann habilitation body was not recovered. The older flow construction and Berman's earlier normalized Fano negativity must be credited, and no firstness/current-worldwide-openness claim follows. These are stated scope/priority limits already present in the target, not a weaker replacement theorem.
