# Recovered substantive turn 3: a conditional pressure/Legendre obstruction

Problem 30004690. This is documented recovered substantive turn 3; the historical count is unknown. The exact smooth-semipositive-boundary, interior-non-C² target remains unresolved.

## Mechanism

Instead of choosing another explicit shape, analyze the source's proposed inverse-flow construction through the conformal velocity and the Hessian of its Legendre envelope. This yields the conditional statement below. Its hypotheses are deliberate and must not be silently asserted for every smooth-data weak Hele–Shaw flow. In particular, the terminal boundary-derivative convergence is a substantive additional condition.

**Conditional obstruction.** Suppose a smooth strong Hele–Shaw flow with smooth nonnegative density approaches a slit, and the normalized Riemann maps have the ordinary first-order boundary convergence specified below. Then the associated Legendre solution glues C² across the terminal harmonic-disc interface. Thus, within these hypotheses, loss of rank at that interface alone does not produce the desired failure of C².

This is a proposed rigorous partial result, not a global nonexistence theorem or a claim that the announced construction is false. Independent review is required before promoting it.

## 1. Explicit hypotheses and conventions

Use dd^c log|z|²=δ0 and a smooth nonnegative probability area density ρ(z)dA on P¹, with smooth local potential ψ on C and ψ−log(1+|z|²) smooth on P¹. The injection point is 0. Let Ω_t, t0<t<1, be strictly increasing smoothly bounded simply connected domains in C containing 0, varying smoothly with nonzero normal velocity, with ρ positive along each ∂Ω_t. Assume their weighted area is t and they satisfy Darcy's law for ρ.

Assume Ω_t increases to Ω_1=C\γ, where γ is a slit arc in P¹ containing infinity and avoiding 0. Normalize conformal maps f_t:D→Ω_t by f_t(0)=0 and f'_t(0)>0. Assume f_t converge locally uniformly on D to a conformal f_1:D→Ω_1. Let ζ_t=f_t^{-1}.

At one finite slit endpoint, assume there is an open circle interval I and a parameter θ0 in I such that, for almost every θ in I except θ0,

    f_t(e^{iθ}) -> f_1(e^{iθ}),
    f'_t(e^{iθ}) -> f'_1(e^{iθ}),

the image stays in a coordinate neighborhood where ρ is bounded, and

    |f'_1(e^{iθ})| <= C |θ−θ0|.

This is the usual quadratic endpoint behavior for an analytic slit, but here it is an explicit hypothesis together with the required convergence. No convergence at θ0 itself is needed.

Let ψ_t be the local Hele–Shaw obstacle potentials. In the smooth-flow region use the standard identities

    ∂_t ψ_t(w)=G_t(w)=log|ζ_t(w)|²,        w in Ω_t,
    ψ_1(w)=log|w|²+C0.

Assume the associated solution is given by the Ross–Witt Nyström Legendre formula

    U(z,τ)=sup_{0<=t<=1}{ψ_t(τz)−t log|τ|²},
    Φ=U−log(1+|z|²),

with its usual removable interpretation at τ=0. These identities are part of the source framework, not an extension to arbitrary unrelated HCMA boundary data.

## 2. Conformal velocity necessarily diverges

Define

    p_t(ζ)=dot f_t(ζ)/(ζ f'_t(ζ)).

The singularity at ζ=0 is removable, with p_t(0)=d(log f'_t(0))/dt real. On |ζ|=1, normal velocity is |f'_t| Re p_t. Harmonic measure at the injection point is dθ/(2π). Darcy flux consequently gives

    Re p_t(e^{iθ}) = 1/[2π ρ(f_t(e^{iθ})) |f'_t(e^{iθ})|²].    (1)

Thus Re p_t is a positive harmonic function on D. By the mean-value identity,

    p_t(0)=(1/2π) integral_0^{2π} Re p_t(e^{iθ}) dθ.

On I, the endpoint hypotheses and a local upper bound M on ρ give the almost-everywhere lower limiting bound

    liminf_(t->1) Re p_t(e^{iθ})
        >= 1/[2π M |f'_1(e^{iθ})|²].

The right side has a nonintegrable inverse-square singularity at θ0. Fatou's lemma proves

    p_t(0) -> +infinity.                                  (2)

By Harnack's inequality, for every r<1,

    inf_(|ζ|<=r) Re p_t(ζ)
        >= (1−r)/(1+r) p_t(0) -> +infinity.               (3)

Allowing ρ to vanish at the endpoint does not remove this estimate; only an upper bound on ρ was used.

## 3. Consequence for the Legendre Hessian

For real local coordinates X on the product, write

    F(t,X)=ψ_t(τz)−t log|τ|².

At an interior maximizer t=t(X),

    F_t=G_t(τz)−log|τ|²=0,

equivalently |ζ_t(τz)|=|τ|. Implicitly differentiating f_t(ζ_t(w))=w gives

    ∂_t ζ_t(w)=−ζ_t(w) p_t(ζ_t(w)),

hence, at fixed w,

    ∂_t G_t(w)=−2 Re p_t(ζ_t(w)).

Therefore

    F_tt=−2 Re p_t(ζ_t(τz)),                              (4)
    D_X² U = D_X² F − (D_X F_t ⊗ D_X F_t)/F_tt.           (5)

Equation (5) is the full **real Hessian** formula. Continuity of only the complex Levi form would not, by itself, suffice for the conclusion below.

The terminal interface is locally

    |ζ_1(τz)/τ|=1,

with ζ_1(τz)/τ extending holomorphically at τ=0. Its z derivative is nonzero, so it is a smooth real hypersurface. On its degenerate side the optimizer is t=1 and U=log|z|²+C0. On the other side, approaching the interface forces t(X)→1; otherwise the point would remain strictly inside f_t(|τ|D)/τ for some t<1.

On any compact patch of this interface with |τ|<1, ζ_t and their spatial derivatives converge uniformly in an appropriate neighborhood, by local uniform conformal convergence and Cauchy estimates. In particular, the derivatives D_X F_t remain bounded. At τ=0, use

    F_t=log|ζ_t(τz)/τ|²

after removing the common logarithmic term; this is smooth near the interface because its holomorphic argument has modulus near one. The same boundedness holds there.

For completeness, the fixed-t spatial derivatives D_X² F converge to those of the terminal branch. One can see this from the usual logarithmic-potential formula

    ψ_t(w)=t log|w|² + integral_(Ω_t^c) log|w−ξ|² ρ(ξ)dAξ + C,

where C is independent of t. On a compact subset of Ω_1, the remaining measure is supported away from that compact set and has mass 1−t. All spatial derivatives of the integral tend uniformly to zero; its zeroth-order tail is controlled by smoothness of the area form on P¹, which gives integrable logarithmic growth at infinity. The same formula removes the source logarithm near w=0. Local potentials in the infinity chart give the identical conclusion if the product patch meets z=infinity.

Now (3) and (4) imply −F_tt→infinity uniformly on the patch. The correction term in (5) tends to zero, while the first term converges to the terminal branch's real Hessian. Values and first derivatives converge to those of that branch as well. The two smooth formulas therefore glue C² across the interface.

## 4. What this does and does not close

The derivation blocks a specific proposed inference: a terminal slit and an open rank-zero region do not, under the stated regular conformal-limit hypotheses, force an interior jump in the second derivatives. It explains why proving only smooth density and simple connectivity is not by itself a finished non-C² construction. The endpoint's harmonic-measure concentration makes the Legendre curvature F_tt diverge and suppresses the Hessian correction instead of keeping it bounded away from zero.

This is conditional. We have not proved the boundary derivative convergence for an arbitrary candidate flow. We have not ruled out a nonelliptic construction violating that condition, a singular intermediate flow time, a different degeneration, or boundary data outside the rotating-data Hele–Shaw correspondence. Nor is this a proof that every smooth-data HCMA solution is C².

A next substantive turn should target a mechanism that evades the hypotheses, rather than simply repeat fixed-shape flattening or assume a discontinuous Levi form from rank loss. The full original target is still active.

## Sources

The strong-flow/Darcy and obstacle-potential identities are the framework of Ross–Witt Nyström's [full duality paper](https://arxiv.org/pdf/1509.02665), Sections 2 and 5, and their [2017 survey](https://arxiv.org/pdf/1712.00405), Sections 6–8. The [2021 source report](https://ems.press/content/serial-article-files/46904), pp. 1323–1324, supplies the proposed interior construction and the remaining smooth-density issue. The present conditional calculation does not replace an independent check of their full intended construction.
