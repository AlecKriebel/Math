# Independent acceptance: arbitrary complex phase under second-harmonic dominance

## Decision and exact scope

**Accepted. No theorem-level or proof correction is required.** The fifth-pass argument proves the quantitative full-torus median bound for arbitrary continuous complex periodic coefficients A and B satisfying |A|≤|B|. It closes the phase-coherence gap left by the accepted fourth-pass theorem. The proof covers zeros, arbitrary nonuniform phase, both angular resonances, and distributionally nonnegative forcing with singular measure components.

The exact accepted conclusion is

    average_s[M(s)/(2π)] ≥ ((Γ−k)/2) average_s|A(s)|,
    Γ = 6√2/(8+√2),  k = 3√3/(2π),
    (Γ−k)/2 > 1/80.

If A is not identically zero, the average is strictly greater than (1/80) average|A|, and M is positive at some phase. If A is identically zero, M(s)=2πc(s)≥0 at every phase. The strict conclusion is deliberately conditional: the identically zero triple has zero median at every phase.

The assumptions are precisely those of the reviewed report: ρ,ω>0; integer n≥1; continuous 2π-periodic real c and complex A,B; |A(s)|≤|B(s)|; and distributional nonnegativity of

    L H_j,  L=(ω∂s+ρ)²+∂θ²,
    H_j=c+Re(A exp(inθ)ζ^j+B exp(2inθ)ζ^(2j)),
    ζ=exp(2πi/3), j=0,1,2.

The [full reviewed proof](../proofs/complex_dominance.md), its [author certificate](../certificates/phase_author.json), and the [independent audit certificate](../certificates/phase_audit.json) are included. The inherited angular identity is proved and audited in the [fourth-pass acceptance](../baseline/accepted_public/audits/relative_phase_acceptance.md).

This is an adversarial audit of the final fifth contribution, not another research pass. Outside second-harmonic dominance, the unrestricted two-amplitude theorem, arbitrary independent triples, the general periodic assertion, and the original normalized-supremum conjecture remain unresolved. No historical novelty claim or counterexample to those conjectures is made. The original problem source remains A. Eremenko, *Conjectured inequality for subharmonic functions*, 4 April 2015, [author-hosted PDF](https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf); source attribution is inherited from the accepted prior audit, not a new literature search.

## 1. First-order complex L1 coercivity, including zeros and negative factors

Let u be a smooth complex periodic function, a real, and ω>0. Put Rε=(|u|²+ε²)^(1/2). Direct expansion in real and imaginary parts gives

    Re[conjugate(u)(ωu′+au)/Rε]
      = ωRε′+a|u|²/Rε.

This is a genuine smooth identity for every ε>0, including at zeros of u. Integrating over the circle eliminates the derivative. Taking the absolute value of that integrated equality, rather than applying an incorrect pointwise sign estimate, gives

    |a| ∫|u|²/Rε
      ≤ ∫(|u|/Rε)|ωu′+au|
      ≤ ∫|ωu′+au|.

The nonnegative function |u|²/Rε converges to |u| at every point, including zeros, and is bounded by |u|. Dominated convergence therefore proves

    |a| ∫|u| ≤ ∫|ωu′+au|.                         (A)

No argument or logarithmic derivative of u is used. There is no division by u, |u|, or a. The proof works unchanged for negative a. At a=0 it states the valid inequality 0≤∫|ωu′|. Smoothness of |u| at its zeros is not assumed.

Now let T_r=(ω∂s+ρ)²−r², r>0. The real first-order factors commute:

    T_r=(ω∂s+ρ−r)(ω∂s+ρ+r).

Apply (A) to v=(ω∂s+ρ+r)u with a=ρ−r, then apply it to u with a=ρ+r. The intervening multiplier |ρ−r| is nonnegative, so multiplying the second inequality preserves its direction. This proves

    ∫|T_r u| ≥ |ρ−r|∫|(ω∂s+ρ+r)u|
               ≥ |ρ−r|(ρ+r)∫|u|
               = |ρ²−r²|∫|u|.                  (B)

At ρ=r the first lower bound is zero. This is not a failed inverse or a limiting argument; it is a direct valid inequality. Nonzero constant u attains equality in (B) whenever ρ≠r. The sharpness statement concerns the coercivity constant alone.

## 2. Independent inverse-kernel sign and total-variation audit

The inverse interpretation is also correct, although the theorem does not need it. For a≠0,

    R_a f(s)=∫₀∞ exp(−at)f(s−ωt)dt                  if a>0,
    R_a f(s)=−∫₀∞ exp(at)f(s+ωt)dt                 if a<0.

Integration by parts gives (ω∂s+a)R_a f=f in both cases. The second formula needs both the leading minus sign and the forward shift. Its kernel is negative, not positive. The periodic homogeneous equation has only the zero solution because exp(−2πa/ω)≠1.

An equivalent periodized convolution kernel, integrated with ordinary dy on [0,2π), is

    g_a(y)=exp(−ay/ω) / [ω(1−exp(−2πa/ω))].

Its sign is sign(a), its jump satisfies ω[g_a(0+)−g_a(2π−)]=1, its signed mass is 1/a, and its total variation is 1/|a|. The distinction between signed mass and total variation is essential below resonance.

For ρ≠r, convolution of g_(ρ−r) with g_(ρ+r) has one fixed overall sign, sign(ρ−r). There is no cancellation in its absolute mass. Consequently

    ||kernel(T_r^−1)||TV
      = 1/(|ρ−r|(ρ+r)) = 1/|ρ²−r²|.

This is valid above and below resonance. Normalizing both L1 integrals by 2π leaves the operator norm and (B) unchanged.

One companion-verifier label is broader than its actual assertion: the author's check named “two-factor inverse total variation product” verifies the signed algebraic identity 1/[(ρ−r)(ρ+r)]=1/(ρ²−r²). It does not by itself verify the absolute total variation below resonance. This is a coverage limitation, not a false assertion in the report. The independent verifier separately checks positive and negative kernels, their jumps and differential equations, and both sign regimes. The analytic argument above supplies the full conclusion. No theorem correction is needed.

## 3. Positive forcing controls mean moduli with the correct normalizations

First suppose c,A,B are smooth. The forcing of H_0 is

    p_s(x)=f₀(s)+Re(f₁(s)e^(ix)+f₂(s)e^(2ix)), x=nθ,
    f₀=(ω∂s+ρ)²c, f₁=T_n A, f₂=T_(2n)B.

Distributional positivity is then ordinary pointwise positivity. Since n≥1, x=nθ covers the entire angular circle. Thus p_s(x)≥0 for all s,x.

For a nonnegative polynomial p₀+Re(ue^(ix)+ve^(2ix)), rotate x so that u is nonnegative real. At 3π/4 and 5π/4 the two second-harmonic terms cancel even when v is complex. The sum is 2p₀−√2|u|, proving |u|≤√2p₀. For the other bound, choose x₀ with Re(ve^(2ix₀))=−|v| and add the values at x₀ and x₀+π. The first harmonic cancels and gives |v|≤p₀. When either coefficient is zero, no rotation choice is needed for that bound.

Both constants are separately sharp, as shown by

    (cos x+1/√2)²=1+√2 cos x+(1/2)cos 2x,
    2cos²x=1+cos 2x.

Averaging these inequalities in s, applying (B), and integrating periodic derivatives of c gives

    |ρ²−n²| average|A| ≤ average|f₁| ≤ √2ρ² average c,
    |ρ²−4n²| average|B| ≤ average|f₂| ≤ ρ² average c.    (C)

The coefficients in H are real parts, not pairs of coefficients without the usual factor two. The polynomial tests are stated in exactly the same real-part convention, so there is no missing Fourier-normalization factor. Both sides of every s-average use ds/(2π). In particular, the bound is on average|A|, not |average A|.

## 4. Continuous coefficients and singular positive forcing

For continuous coefficients, no distribution is evaluated at a fixed s or restricted to an angular curve. Let ηε be a nonnegative smooth approximate identity on the s-circle. Convolve c,A,B only in s. Convolution commutes with the constant-coefficient operator L and preserves positivity of its distributional forcing.

The resulting coefficients are smooth in s and the profiles contain only finitely many angular modes. Hence their forcing is a smooth function of both variables. A smooth positive distribution is pointwise nonnegative: a negative value would persist in an open neighborhood and contradict a nonnegative test supported there. The smooth proof of (C) therefore applies to every mollified triple.

Convolution preserves average c exactly. Uniform convergence cε→c, Aε→A, Bε→B follows from continuity on the compact circle. Since ||z|−|w||≤|z−w|, the modulus averages converge as well. Passing to the limit gives (C) for the original continuous coefficients.

At no point in this passage is |Aε|≤|Bε| asserted or needed. Complex modulus dominance does not generally survive averaging. Indeed, with ρ=ω=n=1, c=5, A=1, B=e^(is), the original coefficients have equal moduli and the forcing has minimum 5−√20>0. Temporal heat convolution at time h>0 leaves A unchanged and replaces B by e^(−h)e^(is), destroying dominance. Thus even admissibility does not repair that invalid shortcut. The reviewed proof correctly postpones all uses of dominance until after returning to the original coefficients.

### Explicit nonsmooth complex test with atomic forcing

Set q(s)=|sin s|, and off s=0,π write v=q′=sign(sin s)cos s. Let

    ρ=ω=n=1,
    c=4+(3/10)q,
    A=(1/10)q e^(is), B=(1/5)q e^(2is).

These are continuous and periodic, have common zeros, and are not differentiable at those zeros. Dominance holds pointwise. Distributionally,

    q″=−q+2(δ₀+δπ).

The regular forcing coefficients are

    f₀,reg=4+(3/5)v,
    f₁,reg=e^(is)[((1+i)v+(−1+i)q)/5],
    f₂,reg=e^(2is)[((2+4i)v+(−8+4i)q)/5].

Using |q|,|v|≤1, their full polynomial is bounded below by

    17/5 − 2√2/5 − 6√5/5 > 1/10.

For example, √2<3/2 and √5<9/4 already give the strict final rational bound. At each atom the angular density is

    2[3/10+Re((1/10)e^(is)e^(iθ)+(1/5)e^(2is)e^(2iθ))],

which is nonnegative by the triangle inequality. Cyclic translates preserve this property. This gives an exact admissible example with genuinely complex coefficients and positive singular forcing. Its quotient A²/B=q/20 extends continuously through the zeros. The example confirms the claimed regularity scope without assuming classical second derivatives.

## 5. Uniform ratio certificate and both resonances

For the original coefficients set

    C=average c, X=average|A|, Y=average|B|,
    t=n²/ρ²>0.

Dominance gives Y≥X≥0. Divide (C) only by the strictly positive ρ²:

    C≥|1−t|X/√2,
    C≥|1−4t|Y≥|1−4t|X.                          (D)

The second substitution has a nonnegative coefficient, including at t=1/4. No sign assumption about a complex mean is involved.

Let w₁=8/(8+√2), w₂=√2/(8+√2). These are positive and sum to one. A convex combination of the two lower bounds in (D), followed by |1−t|≥1−t and |1−4t|≥4t−1, yields

    C≥[w₁(1−t)/√2+w₂(4t−1)]X
      = [3√2/(8+√2)]X = (Γ/2)X.                  (E)

This is one certificate for every t>0, not a numerical scan or an argument missing an interval. The relaxed envelope max(|1−t|/√2,|1−4t|) attains this value at t=(2+√2)/(8+√2), which lies strictly between 1/4 and 1. Thus (E) is optimal for these two relaxed scalar bounds; optimality for the full theorem is not claimed.

At ρ=n, t=1 and the second bound in (D) gives C≥3X. At ρ=2n, t=1/4 and the first gives C≥3X/(4√2). Both exceed (Γ/2)X. The proof never divides by ρ−n, ρ−2n, either modal determinant, or X. It therefore covers resonances and X=0 directly.

The strict rational gap is correct. The integer inequality 578>576 implies √2>24/17 and hence Γ>9/10. Since π>3 and √3<7/4, k<7/8. Therefore

    Γ−k>9/10−7/8=1/40,
    (Γ−k)/2>1/80.

The numerical half-gap approximately 0.0371666429006605 is descriptive only; the theorem's strict rational lower bound is exact.

## 6. Inherited angular identity: conventions, zeros, and final averaging

The accepted fourth-pass angular identity is exactly

    average_x med_j Re(Ae^(ix)ζ^j+Be^(2ix)ζ^(2j))
      = −(k/2)Re(A²/B),                          (F)

under |A|≤|B|. This audit relies on its previously accepted analytic proof, including all strict, boundary, and zero degeneracies. Its ζ-powers, signs, and real-part convention match the fifth-pass profiles without any conversion. An angular rotation sends A to Ae^(iδ) and B to Be^(2iδ), leaving A²/B invariant. Equivalently Re(A²/B)=Re(A² conjugate(B))/|B|²; substituting another conjugation would change the formula.

Replacing x by nθ traverses n full angular periods. The Jacobian 1/n cancels their number, so the normalized angular mean in (F) is unchanged. Adding the common c adds c to the median. Consequently

    M(s)/(2π)=c(s)−(k/2)Re(A(s)²/B(s)).            (G)

Where B=0, dominance forces A=0. Define the quotient to be zero there. The bound

    |A²/B|≤|A|≤|B|

proves its continuity at every such point. Hence (G) is a continuous identity over the entire s-circle. There is no measurable-choice or phase-unwrapping issue.

Pointwise Re(A²/B)≤|A|. Average (G) and then use (E):

    average[M/(2π)]
       ≥ C−(k/2)X
       ≥ ((Γ−k)/2)X.

No median was moved across an s-average. Only an already established pointwise angular identity and a scalar inequality were integrated.

If A is not identically zero, continuity implies X>0. The strict rational gap gives the claimed strictly positive full-torus average. The median of three real inputs is 1-Lipschitz in their maximum norm; therefore M is continuous, and a positive average forces a positive phase.

If A is identically zero, (G) gives M=2πc. Angular averaging of the positive distribution L H_0 yields (ω∂s+ρ)²c≥0. For smooth nonnegative forcing f, the unique periodic scalar inverse is

    c(s)=∫₀∞ t exp(−ρt) f(s−ωt)dt≥0.

It is the composition of the two positive first-order inverses with a=ρ. For continuous c and distributional forcing, nonnegative s-mollification gives cε≥0 and uniform convergence gives c≥0 everywhere. This proves the all-phase conclusion in the degenerate case, including c=A=B=0.

## 7. Independent controls, reproduction, and limitations

The author finite calculations were replayed independently in normal, -O, and -OO modes. All three outputs match the [author certificate](../certificates/phase_author.json) byte for byte. No author certificate is relabeled as an independent audit.

The independent verifier reconstructs the regularized complex projection, factorization, both inverse-kernel sign regimes, kernel differential equations and jumps, coefficient tests with imaginary terms present, all-ratio weights, envelope crossing, resonance endpoints, rational gap, invariant-quotient convention, an admissible failure of mollified dominance, and the nonsmooth complex atomic-forcing example above. Explicit exceptions remain active under optimization.

Its finite diagnostics use 16,384 equally spaced points and a fixed random seed. They include 37 complex functions: the zero and constant functions, positive and negative rotations, real and complex zeros, a double zero, random complex trigonometric polynomials, nonuniform phase, and nonuniform phase with zeros. Across parameter signs, small factors, and resonances, they run 777 first-order and 1,110 second-order L1 checks. The smallest normalized second-order slack is about −4.3×10^−22, a roundoff residual at equality. There is no observed failure.

A further 1,000 polynomials are globally nonnegative by construction as |a+b e^(ix)+c e^(2ix)|². Their two coefficient inequalities pass. Direct numerical median quadrature, independent of (F) as an evaluator, checks 216 complex-amplitude/n combinations, including zero amplitudes, dominance boundary points, arbitrary relative phases, varied scales, and n=1,2,5. The maximum normalized error is about 7.3×10^−9.

Five negative controls reject: signed inverse mass substituted for total variation below resonance; a larger constant than the relaxed envelope minimum; preservation of dominance under heat smoothing; mean modulus replaced by modulus of the mean; and extension of (F) outside dominance. For the last, A=2,B=1 has direct median mean −k, whereas the false extension gives −2k.

These finite diagnostics corroborate the analytic proof; they do not establish universal inequalities, distributional limits, or the inherited angular identity. The [independent certificate](../certificates/phase_audit.json) contains exact counts and reproducible numeric residuals. Independent outputs are byte-identical in normal, -O, and -OO modes. The [reproduction guide](../REPRODUCTION.md) describes their separate analytic and computational roles.

**Final disposition:** accept the fifth-pass theorem and proof in their stated dominance region. Retain every unresolved-scope limitation in the report. The signed-mass verifier label is an optional coverage clarification, fully addressed by this independent audit, not a reason to weaken or reject the theorem.
