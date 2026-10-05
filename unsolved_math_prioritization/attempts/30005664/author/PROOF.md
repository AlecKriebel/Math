# Scoped results for the critical massive Dirac problem

## 1. Target, conventions and source credit

Let d≥2 be an integer, m>0, and N=2^floor((d+1)/2). Choose Hermitian N×N matrices α₁,…,α_d,β with

    α_j α_k + α_k α_j = 2 δ_jk I,    α_j β + β α_j = 0,    β²=I.

Write D₀=−i α·∇ and D_m=D₀+mβ. Units are ℏ=c=1. The potential is a nonnegative scalar multiplying I, not a mass-type potential multiplying β. For V∈L^p(R^d), p≥d, use the distinguished self-adjoint realization described in [DGPV, Proposition 2.1]. In our main range p>d and d≥2 its domain is H¹(R^d,C^N). Its essential spectrum is (−∞,−m]∪[m,∞).

The quantity λ_D(V) in the source is the lowest eigenvalue in the open gap, with the upper endpoint convention when there is no such eigenvalue. The optimized value is

    Λ_D(a,p;m)=inf{λ_D(V): V≥0, ‖V‖_p=a}.

The critical strength a_*(p,d;m) is the limit of its inverse as the gap energy tends to −m from above. It is not defined by the condition “−m belongs to the spectrum”: −m already belongs to the essential spectrum for every admissible potential, including V=0. The inverse-spectrum expression in the short OWR report is understood only inside the gap before taking the limit.

DGPV Theorem 1.1 supplies subcritical optimizers satisfying the Kerr equation

    D_m Ψ − |Ψ|^(2/(p−1)) Ψ = λ Ψ,
    V=|Ψ|^(2/(p−1)),    ∫|Ψ|^(2p/(p−1))=∫V^p.

The spinor is not normalized to have L² norm one in this equation. The threshold in question is λ=−m, not λ=0 for a massless Dirac operator. The question is whether the global critical strength equals the explicit candidate strength below, with a corresponding optimizer.

The finite-width formula requires **p>d**, although the surrounding general existence theorem permits p≥d. The value p=d is a separate limiting issue. The mass-free formula displayed on OWR printed page 2290 is the m=1 formula; general mass contributes a factor m^(p−d) to the pth power of the norm.

[DGPV, §5.4, (5.7), Lemma 5.1] already gives the explicit two- and three-dimensional profile and its upper bound, and explicitly leaves global optimality, optimality among radial competitors, and uniqueness of its radial nonlinear system open. We do not present that construction as a new solution. The following derivations record its scope and prove additional limited identities without a first-discovery claim.

## 2. Clifford construction and an upper bound in every dimension

**Proposition 1.** Fix d≥2, p>d, m>0. Put

    μ=(p−d)/(2m),    s=μ²+|x|²,
    V_*(x)=pμ/s,
    Ψ_*(x)=(pμ)^((p−1)/2) s^(−p/2) (μ+i α·x) ξ,

where ξ∈C^N has |ξ|=1 and βξ=ξ. Then Ψ_*∈H¹ is nonzero,

    |Ψ_*|²=V_*^(p−1),    (D_m−V_*)Ψ_*=−m Ψ_*.

Moreover, with C(p,d)=π^(d/2)Γ(p−d/2)/Γ(p),

    A(p,d;m)^p := ‖V_*‖_p^p
      =p^p μ^(d−p) C(p,d)
      =p^p [2m/(p−d)]^(p−d) C(p,d),

and a_*(p,d;m)≤A(p,d;m).

**Proof.** The positive β eigenspace is nonzero: any α_j maps its two eigenspaces isometrically onto one another. Set X=α·x. The Clifford relations give X²=|x|²I and βXξ=−Xξ. Therefore

    |(μ+iX)ξ|²=μ²+|x|².

For g=s^(−p/2), direct differentiation gives

    D₀[g(μ+iX)ξ]
      =g[(d−p|x|²/s)ξ + i(pμ/s)Xξ].

On adding m(β+I), then subtracting V_*, the X coefficient vanishes and the scalar coefficient is d−p+2mμ=0. Multiplication by the constant in Ψ_* proves both identities.

At infinity Ψ_*=O(r^(1−p)) and ∇Ψ_*=O(r^(−p)); both are bounded near zero. Thus Ψ_*∈L² exactly when p>1+d/2, and its gradient is square-integrable when p>d/2. Our p>d, d≥2 range satisfies both. In particular this is an actual H¹ threshold eigenstate, not merely a formal spinor or a resonance. The statement concerns this explicit potential; it does not assert endpoint attainment for every optimizing sequence.

Polar integration and t=r²/μ² yield

    ∫(μ²+|x|²)^(−p) dx
      =π^(d/2) μ^(d−2p) Γ(p−d/2)/Γ(p),

which proves the formula. Equivalently V_*=A₀/(1+B₀|x|²) with A₀=2mp/(p−d), B₀=4m²/(p−d)². Translation of x is allowed.

For clarity, the upper bound can be obtained from the precise interior variational principle, without treating a spectral threshold as an ordinary resolvent point. Put q=2p/(p+1). DGPV §3 proves that

    N(λ)=sup{⟨w,(D_m−λ)^−1w⟩: ‖w‖_q=1},
    a_*(p,d;m)=1 / lim_(λ↓−m) N(λ).

Here duality is between L^q and L^(q/(q−1)). Take w=V_*Ψ_*=(D_m+m)Ψ_*. This belongs to L²∩L^q. If I=∫V_*^p, then ‖w‖_q²=I^((p+1)/p) and ⟨w,Ψ_*⟩=I.

To justify the limiting quadratic form, use the spectral measure of the free D_m on Ψ_*. Write t for its spectral variable shifted by m and ε=λ+m. Its support is t≤0 or t≥2m. The integrand is t²/(t−ε), converges to t, and is bounded in absolute value by 2|t| for 0<ε<m. The latter is integrable because Ψ_*∈H¹. Dominated convergence gives

    lim_(λ↓−m) ⟨w,(D_m−λ)^−1w⟩=I.

Consequently the limiting supremum is at least I/I^((p+1)/p)=1/A, proving a_*≤A. This argument does not reverse the inequality. ∎

## 3. Exact optimization on an explicitly restricted bubble branch

**Proposition 2.** For any μ>0 define b=d+2mμ and

    W_μ(x)=b μ/(μ²+|x|²).

This has a nonzero H¹ threshold eigenstate proportional to

    (μ²+|x|²)^(−b/2)(μ+iα·x)ξ.

For any fixed finite exponent p>d, the unique minimum of ‖W_μ‖_p over μ>0 occurs at μ=(p−d)/(2m), where W_μ=V_*. The minimum is A(p,d;m).

**Proof.** Repeat Proposition 1 with the exponent b in the spinor. The residual is d−b+2mμ=0. Since b>d≥2, the same H¹ estimates apply. There is no claim here that this spinor satisfies the Kerr normalization for the separately fixed exponent p unless b=p.

For fixed p,

    J(μ):=‖W_μ‖_p^p=C(p,d)(d+2mμ)^p μ^(d−p),
    J'(μ)/J(μ)=d[2mμ−(p−d)]/[μ(d+2mμ)].

The derivative has a unique zero with negative sign before it and positive sign after it. Also J tends to infinity at both endpoints μ↓0 and μ↑∞. This proves the asserted global minimum on this branch. ∎

This is deliberately not a classification of all rational potentials with a threshold state. Other spectral branches, other radial shapes, and nonradial potentials are not covered.

## 4. A Pohozaev identity and its explicit regularity scope

Let q=2p/(p−1), p≥d≥2. Say that an H¹ spinor Ψ is dilation-differentiable if t↦t^(d/2)Ψ(t·) is differentiable at t=1 as an H¹-valued curve. A convenient sufficient assumption for a smooth Ψ is x·∇Ψ∈H¹. We impose this assumption rather than silently assuming it for every threshold resonance.

**Proposition 3.** Suppose a nonzero H¹, dilation-differentiable spinor weakly solves

    (D_m+m)Ψ=|Ψ|^(q−2)Ψ.

Then

    2m‖P_+Ψ‖₂²=(p−d)/p · ∫|Ψ|^q,
    P_+=(I+β)/2.

In particular there is no such nonzero spinor when p=d.

**Proof.** All terms are well defined: H¹ embeds into L^q for the stated exponents. Consider the real-valued action

    S(Ψ)=½ Re⟨Ψ,D₀Ψ⟩ + m/2 ⟨Ψ,(β+I)Ψ⟩ − (1/q)∫|Ψ|^q.

The weak equation says its real derivative vanishes on H¹ variations. Let T=Re⟨Ψ,D₀Ψ⟩ and I=∫|Ψ|^q. The amplitude variation gives

    T+2m‖P_+Ψ‖₂²=I.

Under the L²-preserving dilation, T scales by t, the mass term is unchanged, and I scales by t^(d(q/2−1)). Differentiating the action using the assumed H¹ differentiability gives T/2=dI/(2p). Combining the two equalities proves the identity. If p=d, P_+Ψ=0. Projection of the equation onto the negative β eigenspace then gives 0=|Ψ|^(q−2)Ψ, because D₀ interchanges β eigenspaces. Thus Ψ=0, a contradiction. ∎

This does not prove nonexistence of all possible threshold resonances or of endpoints outside the stated class. It also does not contradict subcritical attainment from DGPV. Proposition 1's explicit states satisfy the dilation condition, so the identity applies to them.

## 5. Concentration at the boundary p=d

**Proposition 4.** On the branch of Proposition 2, with the norm exponent fixed at d,

    ‖W_μ‖_d^d=C(d,d)(d+2mμ)^d.

Its infimum is d^d C(d,d), is approached as μ↓0, and is not attained at any μ>0. More precisely, as finite measures,

    W_μ(x)^d dx  ⇀  d^d C(d,d) δ₀.

For every x≠0, W_μ(x)→0.

**Proof.** The norm identity follows from the same beta integral and is strictly increasing in μ. For every bounded continuous F, the change of variables x=μy gives

    ∫F(x)W_μ(x)^d dx
      =(d+2mμ)^d ∫F(μy)(1+|y|²)^(−d)dy.

The integrable majorant is a constant multiple of (1+|y|²)^(−d). Dominated convergence proves the measure limit. The pointwise claim is immediate. ∎

Thus a finite limiting norm is not a finite-width optimizing function. The limit A(p,d;m) as p↓d is d sqrt(π)[Γ(d/2)/Γ(d)]^(1/d); the factor [2m/(p−d)]^((p−d)/p) tends to one. This is consistent with the source's displayed limit but supplies no missing global lower bound.

A massless conformal argument cannot be imported without a new comparison. Under the natural Dirac dilation V_t(x)=tV(tx), the mass changes from m to tm and ‖V_t‖_p=t^(1−d/p)‖V‖_p. Except at p=d this norm is not scale invariant; even at p=d the fixed positive mass is not invariant. The concentrating branch exhibits the distinction explicitly.

## 6. Exact angular factorization for the fixed candidate in two dimensions

Use d=2, p>2, μ=(p−2)/(2m), V=V_*=pμ/(μ²+r²), and

    P=−i(∂₁+i∂₂),    w=1/V=(μ²+r²)/(pμ).

With D_m in the Pauli representation, the threshold equation for upper and lower components (u,v) is

    (2m−V)u+P* v=0,    Pu−Vv=0.

Eliminating v gives the threshold Schur form

    Q[u]=∫_(R²) w|Pu|² +(2m−V)|u|² dx.

**Proposition 5.** For u∈C_c^∞(R²,C), Q[u]≥0. If u_nr denotes the sum of the nonzero angular Fourier modes, then

    Q[u] ≥ (4m/p) ‖u_nr‖₂².

The constant 4m/p is sharp on the nonradial subspace.

These statements extend by closure to the form domain defined by completion of C_c^∞ in the norm (‖u‖₂²+∫w|Pu|²)^(1/2). In that domain the nullspace of Q is exactly the complex span of

    h₀(r)=(μ²+r²)^(−p/2).

**Proof.** First take a finite Fourier sum away from r=0 and write u=Σ_n f_n(r)e^(inθ). Then

    Pu=−i Σ_n e^(i(n+1)θ)(f_n'−n f_n/r),
    Q[u]=2π Σ_n Q_n[f_n],
    Q_n[f]=∫₀^∞ {r w|f'−nf/r|² +r(2m−V)|f|²}dr.

Integration by parts of the cross term shows that its radial differential expression is

    L_n f=−(1/r)(r w f')'
           +[n²w/r²+n w'/r+2m−V]f.

Put k=|n| and h_n=r^k(μ²+r²)^(−p/2). A direct differentiation gives

    L_n h_n=c_n h_n,
    c_n=2n/μ                 if n≥0,
    c_n=2|n|(p−2)/(pμ)       if n<0.

This identity holds for all n and p>2; h_n need not be square-integrable when |n| is large. Only positivity of h_n on (0,∞) is used. For compactly supported f away from zero, the ground-state transformation is

    Q_n[f]=∫₀^∞ r w h_n² |(f/h_n)'|² dr
              +c_n∫₀^∞ r|f|²dr.                         (F)

It follows by expanding the square and using L_n h_n=c_n h_n, so it also holds for complex f after taking the real part of the cross term. Each c_n is nonnegative; c_0=0. For n≠0,

    c_n≥2(p−2)/(pμ)=4m/p.

Smooth radial cutoffs at infinity and logarithmic cutoffs at the origin extend the inequalities from the stated core to C_c^∞(R²); the logarithmic cutoff has gradient energy tending to zero because w is bounded near zero. Fourier partial sums converge in the form norm: the coefficients of w and V are radial and the L² and weighted P norms diagonalize in these modes. The potential term is bounded on L². The inequalities therefore pass to the specified closure.

For the nullspace assertion, first the nonradial inequality makes every n≠0 component vanish. On the n=0 component, identity (F), or its local version followed by the form closure, implies (f/h₀)'=0 in distributions on every compact subinterval of (0,∞). Therefore f is a constant multiple of h₀. Conversely h₀ is in the form domain by cutoffs, since p>2, and direct substitution or (F) gives Q[h₀]=0. Finally h_{−1}(r)e^(−iθ)=(x₁−ix₂)(μ²+r²)^(−p/2) lies in the same form domain for p>2. Formula (F) attains Q[u]=(4m/p)‖u‖₂² there, establishing sharpness. ∎

This theorem proves a fixed-potential angular statement. It does not prove the Hessian is positive when V is varied subject to its L^p constraint, and does not prove an inequality uniform over potentials. In particular it cannot be promoted to global optimality or uniqueness of optimizing potentials.

### Why a scalar modulus shortcut fails even for this weight

Take any nonzero real smooth f compactly supported in μ<r<∞ and put u=f(r)e^(−iθ). Integration by parts gives

    ∫w|Pu|² dx − ∫w|∇|u||² dx
      =2π/(pμ) ∫₀^∞ (μ²/r−r) f(r)² dr <0.

The equality |∇|u||²=|f'|² holds almost everywhere also if f has zeros; one can simply choose f≥0. Hence the weighted diamagnetic comparison that would replace a spinor/complex upper component by its modulus is false for the actual candidate weight. This is an obstruction to that proof strategy, not a counterexample to Proposition 5 or to the conjecture.

## 7. Exact remaining gap and stopping condition

The target remains the reverse inequality a_*(p,d;m)≥A(p,d;m), together with the appropriate equality and attainment statement. Equivalently, in DGPV's formulation one needs to bound the limiting Birman–Schwinger variational supremum from above by 1/A uniformly over all L^q spinors. Proposition 1 gives only the other direction. Proposition 2 compares only one explicit threshold branch. Proposition 5 varies the upper spinor with the potential frozen and therefore cannot supply the required bound over all V.

The p=d boundary additionally requires a precise endpoint formulation; it cannot be settled by declaring the μ=0 expression an admissible potential. No full or prior-literature resolution was found in the bounded source search. Five substantive routes have been used, and no sixth route is asserted or implied.

## References and credit

- [OWR] David Gontier, joint work with Jean Dolbeault, Fabio Pizzichillo and Hanne Van Den Bosch, *Keller estimates for Dirac operators*, in *Many-Body Quantum Systems*, Oberwolfach Reports 20 (2023), report 39, printed pp. 2288–2291; report DOI https://doi.org/10.4171/OWR/2023/39. Publisher report published 18 April 2024. https://ems.press/journals/owr/articles/14297742
- [DGPV] Jean Dolbeault, David Gontier, Fabio Pizzichillo and Hanne Van Den Bosch, *Keller and Lieb–Thirring estimates of the eigenvalues in the gap of Dirac operators*, Revista Matemática Iberoamericana 40 (2024), 649–692, DOI https://doi.org/10.4171/RMI/1443. Formula and section numbering here follows arXiv v2, 24 July 2023: https://arxiv.org/abs/2210.03091. The final publisher PDF and its §5.4 were also inspected.
- Jean Dolbeault, *Sobolev and Caffarelli–Kohn–Nirenberg inequalities for spinors*, Nice workshop slide deck, https://www.ceremade.dauphine.fr/~dolbeaul/Lectures/files/Nice-5-2-2026.pdf, slide 32. The title slide contains a February 5, 2025 date but also names the February 5–6, 2026 workshop. That inconsistency is retained; the conjecture wording on slide 32 is unambiguous.
- Jean Dolbeault, Maria J. Esteban, Rupert L. Frank and Michael Loss, *The CKN inequality for spinors: symmetry and symmetry breaking*, https://arxiv.org/abs/2504.16909, v2 July 2026, DOI https://doi.org/10.1016/j.matpur.2026.103958. This concerns power-weighted spinor interpolation, not the missing uniform fixed-mass endpoint optimization. It is contextual literature, not an imported proof of the conjecture.

All finite checks in this package supplement the written arguments. They are neither a formal proof-assistant verification nor independent peer review.
