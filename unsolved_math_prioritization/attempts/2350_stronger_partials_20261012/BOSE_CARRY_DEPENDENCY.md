# A carry obstruction for full Bose–Chowla lifts

12 October 2026. Erdős 864 / problem 2350 / row 1741. Independently audited construction-specific research partial; see the accompanying acceptance report and fixed file hashes. No novelty claim. No publication or repository mutation is part of this packet.

## 1. Precisely scoped statement

Let p tend to infinity through odd primes (the proof also applies to odd prime powers, with p then denoting the field order). Let F be the field with p elements, let δ be a nonsquare in F, put K=F(θ), θ²=δ, and choose any generator g of K*. Set q=p²−1. For any λ in K*, define the p-element Bose–Chowla residue set

    T = {log_g(λ(θ+a)) : a in F} in Z/q.

Use either of the following two lifts, separately:

- Integer lift: represent T by B⊂{1,…,q}, representing the zero residue by q.
- Half-integer lift: represent T by r∈{0,…,q−1} and take B={r+1/2}⊂(0,q].

For j∈Z and ordered quadruples in B⁴, including every repetition, define

    C_j = #{(x,y,z,w): x+y+z−w=jq}.

**Theorem.** Uniformly in λ and in the generator g (hence uniformly in every translate and unit dilation of the Bose–Chowla residue set),

    C_0=(1/6+o(1))p²,
    C_1=(2/3+o(1))p²,
    C_2=(1/6+o(1))p².

All other C_j are zero for q sufficiently large. The little-oh terms are uniform over the stated choices and the two lift conventions.

In particular the full canonical lifts, and any lift retaining p−o(p) points, cannot be integer triple-sum-free. More quantitatively, if B'⊂B and B'∩(B'+B'+B') is empty, then

    |B'| ≤ (29/30+o(1))p.

This is a theorem about the specified algebraic modular seeds and canonical length-q lifts. It neither proves the desired √(2/3) interval bound nor excludes arbitrary Sidon constructions or lifts in longer/different intervals. It does not replace q by an unrelated interval length. The two half-lattice cosets are never mixed.

## 2. The external input, with exact hypotheses

We use the standard Riemann hypothesis for polynomial Dirichlet L-functions in the following form. If M∈F[T] has degree D and χ is a nonprincipal character of (F[T]/M)*, extended by zero on nonunits, then

    |Σ_{a∈F} χ(T+a)| ≤ (D−1)√p.                         (RH)

No irreducibility, primitivity, or oddness condition on the character is required. Here it is enough to use squarefree M of degree at most 5.

For clarity, (RH) follows from the standard assertion that L(u,χ) is a polynomial of degree at most D−1 whose inverse roots have modulus at most √p. Its coefficient of u is Σ_a χ(T+a), and is the negative sum of the inverse roots. Imprimitive factors may have inverse roots of modulus 1, which satisfy the same bound.

An inspected primary expository source is Swastik Kopparty, *The zeta function, L-functions, and irreducible polynomials*, Rutgers Topics in Finite Fields notes, 13 October 2013: https://www.math.toronto.edu/swastik/courses/rutgers/finitefields-F13/zeta.pdf . The general modulus is defined on printed page 3, Lemma 1 on page 4 gives the degree bound, Theorem 4 on page 5 gives the zero-location theorem, page 6 explicitly derives the inverse-root bound for the general modulus, and the coefficient argument is exhibited on page 7 for the irreducible special case. The general-modulus version above uses the general Lemma 1 and Theorem 4, not an unjustified extension of an irreducible-only bound. This packet takes that standard theorem as an external input; it does not purport to prove function-field RH.

## 3. Sidonicity and a uniform parametrization

The residue set T is strongly Sidon, including repeated entries. Indeed, equality of two pair products cancels λ² and gives

    (θ+a)(θ+b)=(θ+c)(θ+d).

Comparing coefficients yields a+b=c+d and ab=cd. Thus the two unordered root pairs coincide. This proves modular strong Sidonicity and also integer strong Sidonicity of either lift.

We first study, for arbitrary μ∈K*, the algebraic quadruple variety

    Ω_μ = {(a,b,c,d)∈F⁴: μ(θ+a)(θ+b)(θ+c)=θ+d}.

This allows more than just μ that are squares. That extra scope is needed for the half-integer case.

Fix b and write

    M_b=μ(θ+b)=uθ+v,          u,v∈F.

M_b is never zero. Multiplying once more gives

    M_b(θ+a)=Uθ+V,
    U=ua+v,                 V=va+uδ.

If U≠0 there is exactly one solution (c,d), namely

    c=(1−V)/U,              d=Uδ+Vc.                    (1)

If U=0 and V≠1 there is no solution. If U=0 and V=1, every c∈F is a solution and d=c.

The case U=0,V=1 can occur only when

    N(M_b)=−u,                                          (2)

where N is the norm K/F; conversely (2) makes a=1/M_b−θ belong to F and gives U=0,V=1. To verify the equivalence, conjugate θ to −θ and note

    1/M_b−1/conj(M_b)=−2uθ/N(M_b).

The expression 1/M_b−θ is in F precisely when this difference equals 2θ, giving (2). As a function of b,

    N(M_b)=N(μ)(b²−δ),

while u is affine-linear in b. Thus (2) has at most two roots. Its quadratic coefficient N(μ) is nonzero. Also u=0 for at most one b: if μ=α+βθ then u=α+βb, and β=0 implies α≠0.

For all other b there are p or p−1 solutions. For the at most two exceptional b there are at most 2p−1 solutions. Hence

    |Ω_μ|=p²+O(p),                                      (3)

with an absolute, μ-independent constant.

## 4. Four-character sums and all degeneracies

Let χ₁,χ₂,χ₃,χ₄ be arbitrary complex multiplicative characters of K*. Define

    S_μ(χ₁,χ₂,χ₃,χ₄)
      =Σ_{Ω_μ} χ₁(θ+a)χ₂(θ+b)χ₃(θ+c)χ₄(θ+d).

Set α=χ₁χ₄, β=χ₂χ₄, γ=χ₃χ₄. On Ω_μ the summand equals

    χ₄(μ) α(θ+a) β(θ+b) γ(θ+c).                      (4)

The **resonant tuples** are exactly α=β=γ=1, equivalently

    χ₁=χ₂=χ₃=χ₄⁻¹.

For these tuples S_μ=χ₄(μ)|Ω_μ| exactly. We claim that every other tuple satisfies the uniform bound

    |S_μ| ≤ 4p√p+12p.                                  (5)

Here are the nontriviality and degeneracy details.

For fixed b, put

    r_b=θ+1/conj(M_b).

Formula (1) implies, whenever U≠0,

    θ+c = −conj(M_b)(a−r_b)/(ua+v).                    (6)

The following are the only b-parameters excluded from the character argument:

(i) r_b∈F. Conjugating r_b shows that this is exactly N(M_b)=−u, the at most two roots of (2).

(ii) r_b=−θ. This means M_b=1/(2θ), possible for at most one b because b↦M_b is injective.

The equality r_b=θ is impossible since 1/conj(M_b)≠0. Therefore outside at most three b-values, r_b has degree two over F and its minimal polynomial differs from the minimal polynomial of θ and of −θ.

Suppose first that at least one of α,γ is nonprincipal. For each nonexcluded b, the a-dependent factor in (4), apart from a scalar of modulus one, is

    α(a+θ) γ(a−r_b) γ(ua+v)⁻¹,                      (7)

with the unique zero of ua+v omitted if u≠0.

Construct a polynomial Dirichlet character using the Chinese remainder theorem:

- At the irreducible quadratic minimal polynomial of θ, use evaluation T↦θ followed by α.
- At the distinct irreducible quadratic minimal polynomial of −r_b, use evaluation T↦−r_b followed by γ.
- If u≠0, at the distinct linear factor T−v/u, use evaluation T↦v/u followed by the inverse of γ restricted to F*. This gives γ(a+v/u)⁻¹ on T+a. Include this linear factor even if that restricted character is principal, so the forbidden denominator zero is assigned value zero.

If u=0, the denominator v is a nonzero scalar and no linear factor is used. Scalar values such as γ(u)⁻¹ and γ(−conj M_b) have modulus one and do not affect the estimate.

The total squarefree modulus degree is at most 5. The composite character is nonprincipal because at least one of the two independent quadratic local characters α or γ is nonprincipal. CRT allows that one local coordinate to vary while all others are 1. Neither conjugation of roots nor the linear denominator can cancel a character on a different irreducible factor. This explicitly establishes nontriviality for every tuple in this case, not just for generic character orders.

Applying (RH) bounds each nonexcluded b-slice by 4√p. At an excluded b, the entire slice has at most 2p−1 terms and hence absolute value at most 2p. Their total contribution is at most 6p. This proves (5), with room in its constant.

It remains to treat α=γ=1 and β nonprincipal. In (4) the weight depends only on b. If n_b is the number of solutions in that slice, the parametrization gives

    Σ_b |n_b−p| ≤ 3p.

Indeed, ordinary slices differ by at most 1 and at most two exceptional slices add at most p−1 each. Therefore

    |S_μ| ≤ p |Σ_b β(θ+b)| +3p ≤ p√p+3p,

using (RH) with the irreducible quadratic modulus. This proves (5) for every nonresonant tuple. The numerical constants are deliberately conservative.

## 5. Uniform torus equidistribution, including lift endpoints

Let ε=0 for the integer lift and ε=1/2 for the half-integer lift. Let t_a∈{0,…,q−1} be the exponent log_g(λ(θ+a)). Use

    x_a = t_a/q modulo 1                          if ε=0,
    x_a = (t_a+1/2)/q modulo 1                    if ε=1/2.

Integer representatives use x=1 rather than 0 when t_a=0; these define the same torus point.

A quadruple has integer-valued normalized carry precisely when

    t_a+t_b+t_c−t_d+2ε ≡ 0 (mod q).

Consequently its algebraic equation is Ω_μ with

    μ=λ² g^(2ε).                                      (8)

Here 2ε is 0 or 1, so (8) is meaningful for the half-integer coset even though q is even. No inverse of 2 modulo q is used.

Give every such quadruple mass p⁻² at its four normalized lifted coordinates on (R/Z)⁴. Call the resulting measure ν. We claim that these measures converge uniformly in λ,g,ε to Haar probability measure σ on the subgroup

    H={x₁+x₂+x₃−x₄=0 modulo 1}.

To check this, fix n=(n₁,n₂,n₃,n₄)∈Z⁴ and use the character of K* that takes g to exp(2πi/q). The Fourier coefficient of ν is a scalar of modulus one times p⁻² S_μ with χ_i(g)=exp(2πi n_i/q). For all sufficiently large q, the tuple is resonant exactly when

    n₁=n₂=n₃=−n₄.

In that case the coordinate character is identically 1 on every point being counted, so the coefficient is |Ω_μ|/p²=1+O(1/p). In every other case (5) bounds it by 4/√p+12/p. These are precisely the Fourier coefficients of σ in the limit, with uniform error at each fixed frequency. All the measures are supported on H. Restrict the ambient trigonometric polynomials to H; these restrictions are uniformly dense in C(H), for example by Stone–Weierstrass. Thus the fixed-frequency bounds and the uniform total-mass bound give uniform convergence against every fixed continuous function on H. Positivity and continuous upper and lower approximations on H then give uniform convergence for each fixed set whose boundary in the relative topology of H has σ-measure zero. This is a relative continuity-set argument on H, not an assertion about the ambient boundary of H in the four-torus.

Represent H using x₁,x₂,x₃∈[0,1) independent and uniform, and x₄={x₁+x₂+x₃}. For j=0,1,2 its carry-j region is the set

    j≤x₁+x₂+x₃<j+1.

Its boundary in H is contained in the coordinate seams and finitely many planes, all of σ-measure zero under the three-coordinate Haar parametrization. The volumes are 1/6, 2/3, 1/6. Thus ν gives these regions the claimed limiting masses, uniformly.

For the integer convention t=0 is represented by q rather than 0. It affects at most one element. For any fixed entry in a strongly Sidon modular set, the number of congruent quadruples having that entry in one specified source role is at most 2p−1: each choice of a second source yields at most one ordered nonzero difference, except the one choice giving zero difference, when there are p. In the target role the count is at most 2p. Therefore changing the representative of this one element affects at most 8p quadruples. This is o(p²), so the endpoint convention does not change the constants. For ε=1/2 no coordinate is a seam.

All B elements lie strictly between 0 and q, except the permitted integer endpoint q. Hence −q<x+y+z−w<3q for q>2. The only multiples of q are 0,q,2q. This proves the stated carry theorem, including repetitions.

## 6. Deletion bound, with exact incidence control

For any positive integer or single-coset half-integer strong Sidon set B of size p, and any fixed a∈B, the number of ordered equations

    a+y+z=w

is at most p. For each y, the required ordered positive difference w−z=a+y has at most one representation; if it lies outside the difference range there is none. This handles repeated entries without change. By symmetry the same bound applies with a in either other source position.

For fixed w=a, choosing x leaves y+z=a−x, which has at most two ordered representations by strong Sidonicity, including the possibility of a repeated-entry pair with only one. Thus at most 2p ordered equations have target a.

The total number of equations involving a in any role is therefore at most 5p, by the union bound. Repeated appearances of a only make this upper bound safer. Deleting r elements destroys at most 5pr ordered equations. A triple-sum-free subset must destroy all C₀ equations, so

    5pr ≥ C₀ = (1/6+o(1))p²,
    r ≥ (1/30−o(1))p.

This gives the stated 29/30 retained-size bound. It holds for arbitrary subsets of the canonical lift; the deleted set need not have any interval structure.

## 7. Obstruction and remaining gap

The accepted finite modular counting bound forces many congruent triple-to-single configurations but does not locate their carries. This result supplies such localization for the full Bose–Chowla family: an asymptotic one-sixth have zero carry in the stated positive lifts, whatever translation or unit dilation is chosen. It therefore closes the near-full-Bose-seed route to an interval counterconstruction. The argument uses algebraic mixed-character cancellation beyond one- and two-point continuum constraints.

The bound for retained subsets is only 29/30 relative to p, not √(2/3), and arbitrary large Sidon sets need not be close to a Bose–Chowla seed. The interval conjecture remains unresolved. Longer lifts, different noncanonical representative choices, other seed families, and genuinely nonalgebraic constructions are outside this theorem. The finite program is a diagnostic of the algebra and small examples, not an asymptotic proof. The accompanying independent review accepts this precisely scoped partial theorem, using standard function-field RH as its external input; it does not accept a resolution of the interval conjecture.

## Narrowed public edition notice

All mathematical arguments, hypotheses, examples, substantive audit discussion and corrections above are retained. This edition removes unpublished artifact identifiers and related provenance metadata, replaces obsolete locators, and updates editorial history only. The scope of each theorem and review is unchanged. Exact reversible redaction records and private integrity inventories remain local and are not distributed. [EDITION_MAP.md](EDITION_MAP.md) describes the changes; [PRESERVATION.json](PRESERVATION.json) records mathematical-text preservation without republishing redacted identifiers. [PUBLIC_DEPENDENCIES.json](PUBLIC_DEPENDENCIES.json) identifies only distributed mathematical texts and already-published dependencies. [VERIFICATION.json](VERIFICATION.json) gives aggregate diagnostic results without program or diagnostic-file identities. No source document, executable code, raw per-case collection, dataset contents, private source, personal information or coordination record is included.
