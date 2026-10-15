# PR196 family B — Legendre, regularity and PDE audit

**Verdict: PASS for the assigned concave-duality, pre-contact curvature, and PDE-transfer family. No mathematical repair required in this family.** This verdict depends on the credited published contact-arc construction supplying exactly the geometry used in the candidate. The separate geometry and source-contract families remain independent checks; this report grants no priority, firstness, or publication clearance.

Audited candidate: frozen `original_submitted_head/TURN_4_CANDIDATE.md`; parent-pinned original HEAD `a229ac722a3b1733bcb590a5f796b4a52f68cc73`, original status `claimed_solved`. Four recovered author turns are preserved; earlier interrupted consumption remains unknown/nonzero. The original favorable review was read only after the independent mechanism freeze and independent scalar derivation/verifier were complete.

## 1. Exact claim and success criterion

The target is a smooth function f on P¹×∂D, with ω_FS+ddᶜ_z f(·,τ)>0 at every boundary τ, for which the bounded weak Bedford–Taylor HCMA solution Φ on P¹×D is not twice differentiable at an actual interior point. Smooth semipositive data would suffice for the supplied source target; the candidate claims strictly positive data. A boundary defect, failure of maximal rank, or a discontinuous Hessian without failure at the selected point would not certify the stronger candidate claim.

The mechanism has three logically separate pieces: a finite-time positive-length arc contact gives a strict drop in the right time derivative of a(t)=ψ_t(w*); smooth strong-flow dependence before contact gives finite negative curvature L=a″_−(T); concave duality turns these into unequal one-sided quadratic coefficients at a negative disc logarithmic radius. The present audit checks the second and third pieces, their edge cases, and their PDE interpretation. It also checks the analytic interface needed from the first piece, without substituting for the independent geometry audit.

## 2. Primary dependencies actually checked

The [published Ross–Witt Nyström AIF paper](https://www.numdam.org/item/10.5802/aif.3237.pdf) supplies the contact construction (Proposition 3.4), current formula (Proposition 2.5), lifted strong family through T (Theorem 2.15), transformation (Proposition 4.2), Legendre duality (Theorem 4.4), and smooth Green dependence (Appendix A). Its Theorem 6.2 proof verifies nonvanishing limiting boundary velocity. These inputs were checked in shared read-only primary text; the primary PDF was also opened online. The published theorem’s nonsmoothness conclusion is at the boundary and is not being substituted for the candidate’s interior argument.

The earlier [harmonic-disc paper](https://www.numdam.org/item/10.1007/s10240-015-0074-0.pdf), Proposition 1.3 and Theorem 2.7, confirms finite concave decreasing continuous time envelopes and the duality endpoint convention. It does not impose differentiability in time that would forbid the proposed slope drop. Source identities, hashes and runtime are in `SOURCE_DEPENDENCY_STATUS.json`. No copied article or private extraction belongs to this report’s safe files.

## 3. Full scalar argument: global branches and endpoints

Let a be finite and concave on [0,1], let T∈(0,1), suppose a is C² immediately before T, and assume

    lim_{t↑T} a′(t)=κ0<0,
    lim_{t↑T} a″(t)=L∈(−∞,0),
    a′_+(T)≤b<κ0.

A finite concave function has finite one-sided derivatives at every interior point: fix points on either side and bound all local slopes by their finite secant slopes. Endpoint finiteness is available for ψ_t(w*) when w*≠0. Indeed t log(|w|²/(1+|w|²))+C is an admissible lower barrier after choosing C uniformly below the smooth obstacle (including the infinity chart), while ψ_t≤φ. Concavity is inherited directly from convex combinations of competitors. Thus neither hidden endpoint values nor an unbounded branch create an alternative maximizer.

For t<T, concavity gives a(t)−a(T)≤κ0(t−T); for t>T it gives a(t)−a(T)≤b(t−T). Hence b<κ<κ0 makes a(t)−κt strictly smaller than a(T)−κT for every t≠T, including endpoints. T is the unique global maximizer. This establishes the plateau over the entire optimization range.

For κ>κ0 close enough, strict negativity of a″ before T gives exactly one nearby tκ<T satisfying a′(tκ)=κ. A tangent to a concave function is a global supporting line, so tκ is globally optimal. A second maximizer would force a−κt to be constant between them, contradicting strict concavity near tκ. No post-contact branch can overtake this maximizer. No post-contact smoothness is needed.

Set

    F(κ)=κ+sup_{0≤t≤1}{a(t)−κt}.

For b<κ≤κ0,

    F(κ)=a(T)+(1−T)κ.

For κ>κ0 sufficiently close,

    F′(κ)=1−tκ,
    F″(κ)=−1/a″(tκ).

The common first derivative at κ0 is 1−T. Inverting a′ gives tκ−T=(κ−κ0)/L+o(κ−κ0). Thus for h>0,

    F(κ0+h)=F(κ0)+(1−T)h−h²/(2L)+o(h²),

whereas for h<0 sufficiently close the remainder after the linear term is exactly zero. The coefficient −1/(2L) is strictly positive. Therefore no common second-order Taylor expansion exists at κ0. Equivalently, the two one-sided difference quotients of F′ tend to −1/L and 0. This is failure of twice differentiability at the point, not merely a discontinuous second derivative nearby.

`INDEPENDENT_DERIVATION.md` contains the detailed independent proof and exact piecewise-quadratic normal form. `exact_scalar_verifier.py` verifies polynomial coefficient identities and support signs over the reals using exact rational arithmetic. It has no writes and uses explicit exceptions rather than optimizable Python assertions. Its numerical rational parameters corroborate the normal-form algebra, while the analytic argument proves the general lemma.

## 4. Finite strictly negative pre-contact curvature

Use precisely the potential furnished by the credited construction, avoiding a general assertion about all tangency flows. Its lifted strong-flow family U_t is smooth on an open interval through T by Theorem 2.15. The projection remains conformal and injective on the fluid interiors up to T, so the lifted Green function equals G_{Ω_t} after composition. A point w*∈Ω_T lies in Ω_t for all t sufficiently close to T from the left; its lift and the lifted pole are fixed because the covering map is fixed.

Appendix A is stated in planar domains. This introduces no missing analytic step on the chosen covering surface: the universal cover is a noncompact simply connected Riemann surface, hence has a global conformal chart into C or D. The compact smooth lifted domain and a collar lie inside this chart. The fixed pole can be placed at its origin. The proof of Appendix A then applies to a smoothly varying compact domain family with fixed singular part. Alternatively its uniformly elliptic Dirichlet argument works directly in finitely many fixed charts. Only the lifted family is extended through T; no projected post-contact regularity is asserted.

To justify the time derivative of ψ rather than assume it, write u_t=ψ_t−φ on each smooth fluid domain. It solves the Dirichlet problem

    ddᶜu_t=tδ0−ω_φ,     u_t|_{∂Ω_t}=0.

Pulling this problem to the smooth lifted family and subtracting the fixed logarithmic singularity gives smooth parameter dependence by elliptic Dirichlet theory. The current identity makes ∂tψ_t harmonic away from the pole with logarithmic coefficient one. Smooth fit ∇ψ_t=∇φ on the smooth free boundary, together with ψ_t=φ there, makes its boundary value zero after differentiating the moving boundary condition. Green uniqueness therefore gives

    ∂tψ_t(w*)=G_{Ω_t}(w*,0).

The fixed logarithmic singularity of G does not depend on t. Thus H=∂tG_t at T− is finite and harmonic even at the pole, where the differentiated singularity cancels. Differentiating G_t(x_t,0)=0 on the smooth lifted boundary gives

    H=−V ∂nG_T.

The outward normal derivative of a negative Dirichlet Green function is positive by Hopf’s lemma, and the increasing strong flow has V>0. Consequently H<0 on the whole compact smooth boundary; the maximum principle gives H(w*)<0. This proves

    −∞<L=a″_−(T)<0.

There is no projection singularity in this calculation. A Green-function normalization different by a fixed positive constant would scale both sides consistently; here ddᶜlog|w|²=δ0 fixes coefficient one as in the candidate.

## 5. Analytic interface from contact geometry

The assigned geometry hypothesis is an interior slit point q and a small disc B with B\S⊂Ω_T, where S has zero area and positive length. Put D+=Ω_T∪B, a proper Greenian connected domain. The current identity has no residual line measure on S, so ψ_T+ρ is distributionally harmonic on D+ away from the pole. For h>0, monotonicity gives v_h=(ψ_{T+h}−ψ_T)/h≤0, and on D+

    ddᶜv_h=δ0+h⁻¹ 1_{Ω_{T+h}ᶜ} ω_φ≥0.

The pole coefficient is exactly one, so the negative-Green extremal principle gives v_h≤G_{D+}. Domain monotonicity has the correct sign G_{D+}≤G_{Ω_T}. At a smooth interior slit point, G_{Ω_T} tends to zero from each fluid side whereas G_{D+}(q)<0; cancellation at the pole and the strong maximum principle make the inequality strict throughout Ω_T away from 0. Taking h↓0 yields the scalar gap a′_+(T)≤G_{D+}(w*,0)<G_{Ω_T}(w*,0)=κ0.

This argument only needs nonpositive subharmonicity and the fixed pole; no guessed post-contact branch or filling rate is used. A point contact alone would not establish the strict domain comparison.

## 6. PDE, interior point and coordinate invariance

Choose a finite w*∈Ω_T\{0}; such points exist because Ω_T is open and contains 0. The proper domain’s Green function is finite and strictly negative there. Hence κ0=G_{Ω_T}(w*,0) lies in (−∞,0), and

    τ*=exp(κ0/2)∈(0,1),      z*=w*/τ*

is a genuine interior point of P¹×D. The exact source transformation is

    Φ(z,τ)+log|τ|²+log(1+|z|²)
       = Φ̃(τz,τ)+log(1+|τz|²).

On the smooth curve c(κ)=(w*exp(−κ/2),exp(κ/2)), it becomes

    Φ(c(κ)) = F(κ)+log(1+|w*|²)−κ−log(1+|w*|²exp(−κ)).

The correction is C∞ for finite κ near κ0. It changes both one-sided quadratic coefficients equally and cannot repair their difference. If Φ had a second-order Taylor expansion at c(κ0), composition with the C∞ curve would have a common quadratic coefficient in h from both signs, contrary to §3. This proves the exact failure of ambient second differentiability. The twist (z,τ)↦(τz,τ) is biholomorphic when τ≠0; no assertion is extended through its excluded central locus.

For |τ|=1 the rotation R_τ:z↦τz acts smoothly on P¹ and preserves ω_FS. Therefore f(z,τ)=φ(R_τz) is jointly smooth, and

    ω_FS+ddᶜ_z f = R_τ* (ω_FS+ddᶜφ)>0.

The source’s envelope definition and Section 4 assert the weak HCMA solution. Its boundedness is also immediate: min φ is an admissible lower constant, and restriction to each vertical disc plus the maximum principle gives the upper bound max φ. Thus the Bedford–Taylor product is well-defined; it is the local maximal-plurisubharmonic envelope product, after adding a smooth local background potential. The source supplies the boundary value and homogeneous equation. No merely formal classical Hessian computation is being used to define the weak PDE.

## 7. Adversarial controls, history and code discrepancies

The independent normal form was frozen before reading the archived scalar code. Six invalid-hypothesis controls cover absent gap, zero/positive left curvature, terminal contact, boundary radius, and nonconcave post-contact branch. Additional analytic controls in `INDEPENDENT_DERIVATION.md` show why infinite negative left curvature can make F″ exist and equal zero, why L=0 invalidates the claimed finite jump formula, and why pole/contact/endpoints cannot be silently included.

The archived `scalar_duality_check.py` was inspected and replayed without mutation. Normal Python execution reports 81 cases and 486 assertions, exactly matching its stored JSON. Its two quadratic branch extrema plus endpoints are a complete optimizer list. No normal-mode code/output discrepancy was found. Under Python −O its assertions disappear yet the displayed count remains 486: optimized output alone is not evidence that these checks ran. This is a reproducibility caveat, not a mathematical defect in the normal replay. The independently authored verifier retains its checks under −O.

Recovered turns 1–3 analyze terminal slit mechanisms and report their obstructions, with explicitly conditional hypotheses in turn 3. The present finite-time arc mechanism does not assume or require the false general inference that rank loss forces nonsmoothness. No earlier failed route was relabeled a proof, and no unknown earlier research consumption was reset.

## 8. Strongest checked result and remaining scope

The scalar lemma, finite negative curvature on the smooth lifted strong family, smooth positive boundary data, weak PDE identification, and interior coordinate transfer pass. Given the credited positive-length finite-time contact construction with the stated two-sided slit geometry, they yield a bounded Bedford–Taylor solution failing second differentiability at (z*,τ*). There is no remaining mathematical gap in this assigned approach family and no proposed modification of the originals.

Separate judgments still required from the parent process are the independently assigned contact geometry, the exact OWR source contract and any overall package/publication decision. Novelty and firstness were not investigated or asserted. No person was contacted, and no Git, index, reference, remote-write, editor or tab operation was performed.
