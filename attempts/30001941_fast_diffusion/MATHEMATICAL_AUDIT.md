# Fast-diffusion sharp all-time decay: scoped mathematical audit

Row 1909 / ID 30001941. 21 October 2026. Research artifact, not a solution or novelty certificate. No repository publication or queue modification.

## Target and normalization

The Dolbeault–Toscani OWR contribution (pp.3183–3186, https://ems.press/content/serial-article-files/46370) asks for sharp all-time decay with explicit initial-data control in adaptive best-matching variables. Its assumptions are d≥3, m1=(d−1)/d≤m<1, positive finite mass M, integrable u0^m, and finite second moment. The zero-mass case is the zero solution and is separated. Center the data by its conserved physical barycenter. Put mc=(d−2)/d, q=d(1−m)/2∈(0,1/2], D=d(m−mc)=2−2q, K=∫|x|²B1, σ=K^−1∫|x|²u. Define f=Fσ[u] and j=Iσ[u] with exactly the report's normalizations. The physical equation is ∂τv+div(v∇v^(m−1))=0, not ∂τv=Δv^m without a constant time conversion.

The source does not specify a unique variational class for “sharp.” Neither a faster-than-four exponent nor an explicit prefactor by itself certifies a best all-time envelope. No full resolution or continued-openness certificate is established here.

## Credited prior results and precise scope

Dolbeault–Toscani, *Improved interpolation inequalities, relative entropy and fast diffusion equations* (2013), https://arxiv.org/abs/1110.5175, Lemma 7 and Theorem 8 give, for m>m1,

f' = −j,  σ' = −k σ^(1−q) f,
j' +4j ≤ h j σ'/σ,
k=2d(1−m)²/(mK), h=D d(m−m1)/2,
j ≥4f+C f²/σ^q, C=kh/2.

The differential identities are used at positive regular times (or in the integrated dissipation formulation supplied by the cited theory); finite initial Fisher information is not an added hypothesis. For the scalar comparison one may start at ε>0 and take ε↓0 using initial entropy continuity. This audit does not re-prove the weak-solution regularization theory. These are prior results, not new claims. The paper's Remark 4 explicitly explains discarded terms, and its introduction does not claim the stability coefficient optimal. At m=m1, h=C=0: this particular remainder gives no improvement.

Bonforte–Dolbeault–Nazaret–Simonov (2023), https://arxiv.org/abs/2202.09693v2, Corollaries 2–3 prove constructive all-time exponent improvements in fixed confining variables, including an optimized functional at the endpoint. They require A[v0]=sup(r>0)r^β∫|x|>r v0<∞, β=2/(1−m)−d. The 2025 memoir version, https://arxiv.org/abs/2007.03674v4, Theorem 5.1/Corollary 5.2 state dependence on A and G=F[v0]. Corollary 4 of the shorter paper refers back to ζ from Corollary 3, so its abbreviated displayed hypotheses do not establish removal of A.

There is a structural reconciliation of the apparent A-only versus (A,G) parameter dependence: for fixed mass, layer-cake integration gives

∫|x|²v ≤ β/(β−2) M^(1−2/β) A^(2/β).

Indeed ∫|x|²v=∫0∞2r·mass(|x|>r)dr and split at r=(A/M)^(1/β), using min(M,Ar^−β). Since β≥d≥3, the denominator is positive. In the normalized B=(1+|x|²)^(1/(m−1)) frame and matched mass,

F[v] = [∫B^m +m(∫|x|²v−∫|x|²B)−∫v^m]/(1−m)
≤ [∫B^m +m β/(β−2) M^(1−2/β)A^(2/β)]/(1−m).

Thus the entropy input can be bounded from tail data in the normalized setting. This explains why A-only bounds are plausible; it does not certify that the two publications use identical constants, nor audit every threshold in the memoir.

## Five scoped approaches and exact outcomes

### 1. Integrate the known quadratic entropy production

Since σ(t)≤σ0, a=C/σ0^q≥0 gives f'≤−4f−af². For f0>0, differentiate e^−4t/f(t) or solve the scalar Riccati equation to obtain

f(t) ≤ f0 e^−4t / [1+(a f0/4)(1−e^−4t)].

For f0=0 the flow is at equilibrium. This is an explicit initial-data prefactor improvement, valid for the full moment/integrability class when m>m1, by the cited theorem and entropy dissipation. At the endpoint a=0 it reduces to the baseline. Its asymptotic exponent remains 4, so it does not solve the sharp-asymptotic/all-time connection. No novelty is asserted for integrating a published inequality.

### 2. Retain the adaptive scale rather than freezing it

Put s=σ^q. Then s'=−qk f exactly, and the previous inequality becomes f'≤−4f−C f²/s. The baseline f≤f0e^−4t implies

s(t)≥s0−(qk f0/4)(1−e^−4t),
s∞≥s0−qk f0/4≥(1−q)s0>0.

For the last inequality use f0=2mK s0/[d(1−m)²]−(∫u0^m)/(1−m), hence qk f0/4≤q s0. This gives explicit scale comparability and verifies positivity without treating σ∞ as known.

An attempted improvement by substituting this lower bound for s in −C f²/s has the wrong direction: a lower bound on s gives an upper bound on 1/s, not the lower bound needed for stronger decay. The exact identity s=s0−qk∫0^t f gives a nonlocal scalar inequality, but comparison with its equality system is not established just by the scalar Riccati comparison: dependence on the accumulated entropy has competing signs. This route retains useful structure but does not close the sharp bound.

### 3. Audit the tail bridge, rather than silently importing it

Choose p strictly between max(d+2,d/m) and 2/(1−m), and set u0(x)=c(1+|x|²)^−p/2. This interval is nonempty: at m≥(d−1)/d, 2/(1−m)≥2d>d+2 and d/m<2/(1−m). The datum is smooth, positive, centered, integrable, has finite second moment, and ∫u0^m<∞. But its exterior mass is asymptotic to a positive constant times r^(d−p), so r^β exterior_mass≈r^(2/(1−m)−p)→∞.

This is a counterexample to implication “OWR hypotheses ⇒ finite A,” not a counterexample to any claimed entropy decay. Truncating this datum at radius L gives finite A_L, but A_L grows at least as L^(2/(1−m)−p) by testing r=L/2. Therefore a tail-dependent ζ(A_L) cannot be passed to a uniform positive improvement without an independent lower bound. No claim is made here that the flow cannot improve this tail, or that all data fail a sharper rate.

### 4. Convert fixed-frame improvements with both clocks visible

Let Rf(τ)=(1+2Dτ)^(1/D), r=(1/2)log Rf, and Ra(τ)=exp(2t) be the adaptive physical length scale with Ra(0)=Rf(0)=1. The exact equations are

Ra'=2σ^−D/2 Ra^(1−D), dτ/dt=σ(t)^(D/2)e^(2Dt),
λ=Ra/Rf=e^(2(t−r)).

The centered densities are related by u_ad(t,x)=λ^d v_fixed(r,λx). Optimized entropy is homogeneous under this dilation:

Fopt[λ^d w(λ·)]=λ^−2q Fopt[w].

Consequently, conditional on a valid fixed-frame Fopt bound with exponent 4+ζ in the correctly mass-normalized variables,

f_ad(t)≤f_ad(0) exp[−4qt−(4+ζ−4q)r(t)].

It is invalid to replace r(t) by t. With s∞ bounded below as in approach 2 and σ0 above, τ(t)=∫0^t σ(z)^(D/2)e^(2Dz)dz gives explicit two-sided clock bounds. More explicitly, let L=[(1−q)s0]^(D/(2q))>0 and η=4+ζ−4q>0. Then r(t)≥log[1+L(e^(2Dt)−1)]/(2D), and hence

f_ad(t)≤f_ad(0)e^(−4qt)[1+L(e^(2Dt)−1)]^(−η/(2D))
≤f_ad(0)min(1,L)^(−η/(2D))e^(−(4+ζ)t).

These are explicit adaptive prefactors, but only conditional on the tail-controlled fixed-frame result and the normalization covered by that theorem. This is a conditional transformation audit, not a proof that the stated ζ is the optimal adaptive spectral rate.

### 5. Spectral bootstrap with an explicit entry time

Suppose, in the adaptive frame, an independently justified estimate j≥Λε f holds for all t≥Tε, with Λε approaching the appropriate orthogonality-improved linearized spectral rate as ε→0. Combining it with approach 1 yields

f(t)≤f0 e^−4t/[1+(af0/4)(1−e^−4t)] for t≤Tε,
f(t)≤{f0e^−4Tε/[1+(af0/4)(1−e^−4Tε)]}e^−Λε(t−Tε) for t≥Tε.

This proves exactly what an explicit entry time would buy: a fully initial-data-controlled prefactor for each verified Λε. The missing step is a quantitative Tε on the original unrestricted class, with all regularity/weighted-closeness hypotheses checked. The 2023/2025 constructive theory supplies related thresholds under additional tail controls; it is not an unrestricted bridge. Passing ε→0 may send Tε and the prefactor to infinity, so it does not establish the exact limiting rate with finite explicit prefactor. Endpoint dilation removal must be retained; translation removal alone does not give the needed endpoint improvement.

## Disposition

Five distinct scoped approaches yield a credited all-time logistic bound, explicit scale lower bounds, an exact tail-class separation, a clock/homogeneity conversion, and a conditional spectral-splicing formula. None establishes the original sharp unrestricted target. In particular, no best envelope, optimal coefficient, full-domain quantitative entry time, or optimal exponent with explicit prefactor has been proved. The correct disposition is a qualified partial mathematical audit, not solved and not a certified statement that the problem remains open.

## Source-formula caution: exact remainder is not needed above

Independent adversarial derivation detected apparent normalization slips in Remark 4 of the inspected 2013 source version. This observation concerns the exact auxiliary ODE, not Theorem 8 or the valid inequality used in approach 1. Let a=D/2=1−q, b=d(1−m)=2q, and z=σ^a∇u^(m−1)−2x. Equation (21) gives the adaptive contribution a(σ'/σ)(j−4bf). Algebraically this is

ab(σ'/σ)(j−4f)+h(σ'/σ)j,

because h=a(1−b). The displayed Remark 4 instead has b rather than ab on the first term. Moreover, multiplying the frozen-scale equation (10) by m/[(1−m)σ^a] gives the remainder

R=2∫u^m[|∇z|²−(1−m)(div z)²],

without the extra σ^(2a) factor printed there for that z. Thus the independently reconstructed smooth identity is

j'+4j=a(σ'/σ)(j−4bf)−R.

The quadratic expression defining R is nonnegative for m≥m1 by |∇z|²≥(div z)²/d. Since j≥4f and σ'≤0, this still implies j'+4j≤h(σ'/σ)j. Consequently the main inequality audit is unaffected. This is an algebraic audit of the inspected version, not a claim that no erratum or corrected later version exists, and no new PDE justification of all integrations by parts is supplied.
