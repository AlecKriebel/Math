# Five approaches to the near-one second moment

Date: 2026-10-21. Scope: queue 1862 / ID 20000707. This is an elementary audit and partial analysis, not a solution of the broad Wooley AIM question and not a claim of novelty. Classical inputs and their retrieval limits are documented in SOURCE_STATUS.md. No announcement is promoted to a proved theorem. The accompanying independent mathematical audit accepts these deductions only within the stated partial scope.

## Notation and accepted inputs

For 0<q<1/2 put σ=1−q/2, A(q)=ζ(2−q), N(q)=(2π)^(1−q)ζ(q), C(q)=N(q)/q, and D(q)=−2πζ(1−q). Define

Fq(X)=∫₀ˣ |ζ(σ+it)|² dt = A(q)X+C(q)X^q+Eq(X).

This defines Eq; it is not a claim of an exact two-term evaluation. Lau's fixed-q theorem says ∫₁ˣ Eq(t)dt=D(q)X+O_q(√X). Source: https://doi.org/10.5802/jtnb.553 . Its constants are not asserted uniform. At σ=3/4 its stated bound has an additional log X. The endpoint primitive starts at 1, not 0: with

R(X)=∫₁ˣ |ζ(1+it)|²dt−ζ(2)X+πlog X,

BIR's classical bound is R(X)=O((log X)^(2/3)(log log X)^(1/3)) as X→∞. The gate records the original-download limitation and corroborating exposition https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/0886-02.pdf .

## Approach 1: Exact smoothing and boundary audit

Let ψ∈C_c²((0,∞)), possibly complex, with support in [c,d], c>0. Define Hq(X)=∫₁ˣ(Eq(t)−D(q))dt for X≥1. For cT>1, ordinary integration by parts gives the exact identity

∫ ψ(t/T)|ζ(σ+it)|²dt = A(q)T∫ψ(u)du + N(q)T^q∫ψ(u)u^(q−1)du + T^(−2)∫ψ''(t/T)Hq(t)dt.

Proof: integrate ψ against dFq. The error is −T^−1∫ψ'(t/T)Eq(t)dt. Substitute Eq=D+Hq'; the D term vanishes because ∫ψ'=0. A second integration by parts gives the displayed positive sign. All boundary terms vanish because ψ and ψ' vanish at the support endpoints. Adding any constant to Hq changes nothing. Thus fixed-q Lau gives absolute error O_q,ψ(T^−1/2), not merely a relative error. No positivity or normalization is required. Explicit bound: if |Hq(t)|≤Kq√t on [cT,dT], error ≤Kq T^−1/2∫c^d |ψ''(u)|√u du.

At σ=1, the same argument starting above t=1 gives

∫ψ(t/T)|ζ(1+it)|²dt = ζ(2)T∫ψ − π∫ψ(u)/u du − ∫ψ'(u)R(Tu)du.

BIR alone bounds the last term by Oψ((log T)^(2/3)(log log T)^(1/3)), which does not isolate the constant secondary term. If one additionally assumes the announced Ivić estimate ∫₁ˣR=BX+O(X/log X), two integrations by parts instead give Oψ(1/log T). This implication is conditional on that input; the announcement is not a fully audited proof. The unknown B cancels. A weight nonzero at t=0 makes the endpoint integral divergent.

**Outcome:** fixed-q result proved as a classical consequence; exact signs and boundary terms checked. Endpoint constant remains unsupported by the audited endpoint pointwise bound alone.

## Approach 2: Boundary-layer expansion and exact obstruction

Fix 0<a<b and λ>0. Let L=log T, q=2λ/L. For the unsmoothed interval [T^a,T^b], subtraction gives exactly

∫(T^a to T^b)|ζ(1−λ/L+it)|²dt − ζ(2−2λ/L)(T^b−T^a)
= C(q)(e^(2bλ)−e^(2aλ)) + Eq(T^b)−Eq(T^a).

Using ζ(0)=−1/2 and ζ'(0)=−log(2π)/2, N(0)=−π and N'(0)=0. Hence C(q)=−π/q+O(q). The secondary increment is

L Φ(λ)+O_a,b,λ(1/L),   Φ(λ)=−π(e^(2bλ)−e^(2aλ))/(2λ).

The coefficient extends continuously to Φ(0)=−π(b−a). The expansion of the secondary increment alone is uniform for λ in bounded positive intervals, including as λ tends to zero: its error is O(λ²/L) there. This is an analytic expansion, not a uniform moment theorem. The desired moment asymptotic with error o(L) is equivalent to Eq(T^b)−Eq(T^a)=o(L). Uniform moment claims require this increment uniformly in the corresponding λ-set. At λ=0 Eq itself is undefined; the actual endpoint formula must be treated separately.

The leading ζ(2−2λ/L) must not be silently replaced by ζ(2). Even its first difference times T^b is of order T^b/L, much larger than L. A finite Taylor truncation also leaves an error of order T^b/L^k for some fixed k, still much larger than L.

**Outcome:** correct transition coefficient and next-order control for the explicit term; no proof of the required error increment.

## Approach 3: What averaged control can and cannot buy

For compactly supported smoothing, a hypothetical estimate |Hq(X)|≤K q^(−m)√X, uniform for small q and the relevant large X, would imply an error Oψ,λ(T^−1/2 (log T)^m) along q=2λ/log T. It would therefore prove the smoothed transition

∫ψ(t/T)|ζ(1−λ/log T+it)|²dt
= ζ(2−2λ/log T)T∫ψ − πe^(2λ)∫ψ(u)/u du + Oψ,λ(1/log T),

for fixed λ>0. The O(1/log T) includes the expansion of u^q; N'(0)=0 does not remove that contribution. This is a sufficient criterion, not a claim that Lau supplies its hypothesis.

Why a primitive estimate is inadequate for a sharp unsmoothed increment: even for fixed q, the usual positivity argument loses powers. On X large, Eq'=|ζ|²−A−N X^(q−1)≥−M_q with a finite M_q. Write G=Eq−D and assume |∫₁ˣG|≤K_q√X. For h≤X/2, comparison with G(X) on [X,X+h] and [X−h,X], followed by division by h, gives

|G(X)| ≤ 2K_q√(X+h)/h + M_q h/2.

Choose h proportional to X^(1/4), with q-dependent constants: G(X)=O_q(X^(1/4)). This is far too large to give o(log T). The argument is rigorous but not a claimed best known pointwise bound. Positivity is one-sided derivative control, not a bound on |Eq'|.

**Outcome:** precise sufficient criterion for smoothed transition and quantitative explanation of the loss for sharp windows. No unsmoothed transition follows.

## Approach 4: Explicit countermodel to unsupported uniformization

This is a model of the information in the bounds, not an assertion about the actual zeta error. Fix a,b,λ as above. Let h(v)=(1−v²)²(1−7v²) for |v|≤1, and zero otherwise. It is C¹, h(0)=1, ∫h=0, and its primitive from −∞ to v on [−1,1] is v(1−v²)³. In particular |h'|≤120 and this primitive has absolute value at most 1.

Choose K=1000, xq=exp(2bλ/q), wq=K/q, and, for all sufficiently small q>0, set

E*q(X)=D(q)+q^−1 h((X−xq)/wq),  X≥1.

Its centered primitive H*q=∫₁ˣ(E*q−D) is zero outside the bump and bounded by K/q² inside it. For small enough q the bump lies in [xq/2,3xq/2]. Since q^−2 exp(−bλ/q) is bounded, there is a constant independent of small q with |H*q(X)|≤C√X for every X≥1. In particular this model satisfies the fixed-q Lau-shaped law ∫₁ˣE*q=D(q)X+O_q(√X); the extra integration constant −D(q) is absorbed only with q-dependent constants. The centered uniform estimate is stated explicitly to avoid hiding that issue.

At Tq=exp(2λ/q), we have E*q(Tq^b)−E*q(Tq^a)=1/q for all sufficiently small q. Dividing by log Tq gives 1/(2λ), not zero. Thus even a uniform centered primitive estimate does not imply the desired unsmoothed increment.

Nor does eventual positivity rescue the implication. Define the model F*q=A(q)X+C(q)X^q+E*q(X). Its derivative is A(q)+N(q)X^(q−1)+(1/K)h'((X−xq)/wq). Uniformly for small q and X above a sufficiently large fixed M, A(q) stays near ζ(2)>1, N(q) is bounded, and |N(q)|X^(q−1) is small; the bump derivative has magnitude ≤0.12. Consequently F*q is increasing on that range. This is only eventual positivity, not a model asserted to equal a zeta primitive from zero.

**Outcome:** fully explicit counterexample to the logical inference from averaged control, even supplemented by eventual moment positivity. It does not disprove the zeta transition.

## Approach 5: Rigorous endpoint partials and renormalization

First, BIR subtraction proves the genuine endpoint result

∫(T^a to T^b)|ζ(1+it)|²dt = ζ(2)(T^b−T^a)−π(b−a)log T + O_a,b((log T)^(2/3)(log log T)^(1/3)).

The error is o(log T). It does not detect the constant −πlog 2 on [T,2T].

Second, the divergent mean D(q) has an elementary explanation that must not be mistaken for an increment obstruction. Write γ for Euler's constant and, for fixed X>0, define

J(X)=∫₀ˣ (|ζ(1+it)|²−t^−2)dt−1/X.

The integrand has a removable bounded singularity at zero, by the Laurent expansion of ζ. Then

lim(q↓0) [Eq(X)−D(q)] = J(X)+πγ−ζ(2)X+πlog X.

Proof: put δ=q/2 and z=−δ+it. Write ζ(1+z)=1/z+γ+z g(z) near zero; away from zero use continuity. The singular square integrates to δ^−1 arctan(X/δ)=π/(2δ)−1/X+o(1). The cross term with γ is −2γδ/(δ²+t²), whose integral tends to −πγ. All remaining terms converge under an integrable uniform bound on the fixed interval: locally z/overline(z) has modulus 1 and g is bounded, and away from zero there is no singularity. Hence Fq(X)=π/q+J(X)−πγ+o(1). Also C(q)X^q=−π/q−πlog X+O_X(q), A(q)→ζ(2), and D(q)=2π/q−2πγ+O(q). Subtraction proves the limit.

For X≥1 its limiting expression is exactly R(X)+J(1)+πγ, since J'(X)=|ζ(1+iX)|² and hence J(X)=J(1)+∫₁ˣ|ζ(1+it)|²dt. Thus the renormalized fixed-X error joins the endpoint remainder up to an explicit fixed constant. The order of limits is essential: this proof supplies no uniformity for X growing like exp(const/q), and cannot justify the boundary layer.

**Outcome:** classical endpoint polynomial-window asymptotic and elementary fixed-X renormalization proved. The remaining near-one growing-window claim is not solved.

## Failed routes and final disposition

1. Fixed-q O constants cannot be substituted along q=2λ/log T without quantitative control.
2. Even uniform centered primitive control cannot by itself give sharp-window increments (explicit countermodel).
3. Formal matching of secondary densities with −π/t proves coefficients, not error bounds.
4. Endpoint pointwise remainder is too large to isolate compact-window constants.
5. An ICM announcement without a located proof cannot be used as a fully audited unconditional input.
6. Fixed-X endpoint convergence cannot be interchanged with exponentially growing X.
7. The gate's Zobnin 2025 nonuniform estimates and small-real-shift results of Bettin / Dutta–Ghoshal–Rajkumar have different hypotheses; none is substituted here.

Classification: PARTIAL_EXPOSITORY. Five substantive routes completed, with useful elementary checks and countermodels. Broad AIM question unresolved by this work; no claim that the specific boundary increment is globally open. No general resolution is claimed.
