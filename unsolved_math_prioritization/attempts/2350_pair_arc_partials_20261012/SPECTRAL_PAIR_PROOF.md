# Uniform two-source mixing for canonical Bose–Chowla lifts

12 October 2026. Authored research continuation for Erdős 864, subsequently independently accepted unchanged in AUDIT_PAIR_MIXING.md. The original research made no repository mutation or publication. It addresses the specified canonical Bose–Chowla construction only.

## 1. Statement and dependencies

Let F have odd order p, let K=F(θ) with θ²=δ nonsquare, and write q=p²−1. Let μ∈K*. For a,b∈F write

    μ(θ+b)=u_b θ+v_b,
    U_ab=u_b a+v_b,   V_ab=v_b a+u_b δ.

If U_ab≠0, define

    c(a,b)=(1−V_ab)/U_ab,
    d(a,b)=U_ab δ+V_ab c(a,b).

These are precisely the unique c,d∈F with

    μ(θ+a)(θ+b)(θ+c)=θ+d.

For a nonprincipal multiplicative character γ of K*, let the p-by-p matrix K_γ have entries

    K_γ(a,b)=γ(θ+c(a,b)) if U_ab≠0, and 0 otherwise.

**Spectral theorem.** Uniformly in the field, δ, μ, and every nonprincipal γ,

    ||K_γ||_(ℓ²→ℓ²)
      ≤ [5p^(3/2)+2p]^(1/2)+(2p)^(1/2)
      ≤ 4p^(3/4).

No bounded-order or bounded-frequency hypothesis is imposed on γ. In particular, this is a genuine operator-norm estimate for arbitrary row and column restrictions. It is not inferred from row sums of K_γ.

The sole external input for this new spectral theorem is polynomial Dirichlet L-function RH: for a nonprincipal character Ψ modulo a squarefree polynomial M∈F[T] of degree D, extended by zero on nonunits,

    |Σ_(a∈F) Ψ(T+a)| ≤ (D−1)√p.                 (RH)

We use D≤6. No primitivity, irreducibility of M, or parity condition is required. A directly inspected primary exposition is Swastik Kopparty, *The zeta function, L-functions, and irreducible polynomials*, 13 October 2013, https://www.math.toronto.edu/swastik/courses/rutgers/finitefields-F13/zeta.pdf . The general-modulus definition is on printed page 3; Lemma 1 on page 4 bounds the degree of L; Theorem 4 on page 5 and the factorization on page 6 bound all inverse roots by √p. The coefficient of its degree-one term is the sum in (RH), giving the displayed estimate also for imprimitive characters.

The carry convention and the weighted one-vertex incidence upper bounds needed later are taken from the independently reviewed four-fifths proof, linked in DEPENDENCIES.md and included in full in the preceding stronger-partials appendix. The new pair law itself needs only (RH) and the elementary parametrization above.

## 2. All exceptional columns and quadratic collisions

Put M_b=μ(θ+b) and

    r_b=θ+1/conj(M_b).

Straight substitution gives, at every regular pair U_ab≠0,

    θ+c(a,b)=−conj(M_b) (a−r_b)/(u_b a+v_b).   (1)

The map b↦r_b is injective: b↦M_b is injective, and conjugation, inversion on K*, and translation preserve injectivity.

The element r_b lies in F exactly when N(M_b)=−u_b. Indeed

    r_b−conj(r_b)=2θ[1+u_b/N(M_b)].

Write μ=α+βθ. Then u_b=α+βb and

    N(M_b)=N(μ)(b²−δ).

The condition N(M_b)+u_b=0 is a polynomial equation of degree two in b with nonzero leading coefficient. Thus there are at most two exceptional columns. Every other r_b has degree two over F.

For two nonexceptional columns b,b′, the minimal polynomials of r_b and r_b′ coincide exactly when r_b′=r_b or r_b′=conj(r_b). The first case means b′=b. By injectivity, for each b there is at most one distinct b′ in the second case. These conjugate collisions are retained as exceptional Gram-matrix entries and bounded trivially; no cancellation or nonresonance is asserted for them. In particular, characters lifted through the norm and other high-order resonances cause no unexamined gap here.

The possible collision r_b=−θ is harmless in this argument. There is no separate a+θ factor in a column correlation: row-character factors are diagonal unitary multipliers and cancel in K_γ* K_γ. We do not need to remove that column.

## 3. Off-collision Gram entries

Take nonexceptional b,b′ with distinct minimal polynomials. Up to a scalar of modulus one, their Gram entry is

    Σ_a γ((a−r_b′)/(a−r_b))
            γ((u_b a+v_b)/(u_b′ a+v_b′)),        (2)

where terms at either denominator zero of the original columns are omitted. Reversing the two columns or conjugating (2) does not change its absolute value.

Build a polynomial Dirichlet character by CRT as follows:

- At the irreducible quadratic minimal polynomial of −r_b′, evaluate T at −r_b′ and apply γ.
- At the distinct irreducible quadratic minimal polynomial of −r_b, evaluate T at −r_b and apply γ^−1.
- When u_b≠0, include the linear modulus factor T−v_b/u_b, evaluate T at v_b/u_b, and use γ restricted to F*. When u_b′≠0, include T−v_b′/u_b′ with the inverse restricted character. Their evaluations on T+a are a+v_b/u_b and a+v_b′/u_b′, respectively, and all nonzero scalar factors are absorbed outside the sum. These vanish precisely at a=−v_b/u_b and a=−v_b′/u_b′. Include these factors even when the relevant restricted character is principal, so those omitted terms are assigned zero. If u_b=0 or u_b′=0, that denominator is a nonzero constant and contributes no factor. Repeated linear factors, if any, are combined into one local character and still retained to exclude their zero.

The modulus is squarefree of degree at most six. Neither linear factor meets either irreducible quadratic. The two quadratic factors are distinct, and either quadratic local character is nonprincipal because γ is nonprincipal. The total character is therefore nonprincipal by CRT, independently of what happens at the other factors. Formula (RH) gives

    |(K_γ* K_γ)_(b,b′)| ≤5√p.                  (3)


## 4. Operator norm

Write K_γ=K_good+K_bad, zeroing the at most two exceptional columns in K_good and the other columns in K_bad. Since all entries have modulus at most one,

    ||K_bad|| ≤ ||K_bad||_F ≤√(2p).

Each row of the Hermitian Gram matrix K_good* K_good has at most two entries requiring the trivial p bound: the diagonal and possibly its conjugate-collision partner. All other entries satisfy (3). Consequently its absolute row sum is at most

    2p+5p√p.

The Hermitian spectral radius is at most its maximum absolute row sum (or use the row/column Schur bound). Hence

    ||K_good||² ≤2p+5p^(3/2).

The triangle inequality proves the first spectral bound. For p≥3,

    sqrt(5+2/sqrt(p))+sqrt(2)/p^(1/4)<4,

which proves its simpler form. This covers all odd field orders.

## 5. Arbitrary-subset two-source law

Choose any generator g of K*, any λ∈K*, and either canonical lift, separately:

- integers: B_a is the representative of log_g(λ(θ+a)) in {1,…,q};
- half-integers: B_a=r_a+1/2, with r_a∈{0,…,q−1} representing the same logarithm.

Put X_a=B_a/q∈(0,1], ε=0 or 1/2, and μ=λ²g^(2ε). Let D,E be arbitrary subsets of F; they may depend on every parameter and on p, and may coincide. Define

    ν_D=(1/p)Σ_(a∈D) δ_(X_a),   ν_E=(1/p)Σ_(b∈E) δ_(X_b).

Let S={(x,y,z): x,y,z>0, x+y+z<1}. For any fixed continuous W compactly supported in S, write

    H_W(x,y)=∫_0^1 W(x,y,z) dz.

Then uniformly over all the preceding choices and subsets,

    (1/p²) Σ_(B_a+B_b+B_c=B_d) 1_D(a)1_E(b) W(X_a,X_b,X_c)
      = ∫ H_W(x,y) dν_D(x)dν_E(y)+o_W(1).       (4)

Every quadruple is ordered and all repetitions are included. The same theorem holds for either of the other two source-role pairs by permutation.

### Proof

There are at most p pairs with U_ab=0: for a fixed b with u_b≠0 there is exactly one, and when u_b=0 the constant v_b is nonzero. A singular pair with U_ab=0,V_ab=1 admits p solutions c,d=c; there are at most two such pairs, since its b must be one of the exceptional columns. All other singular pairs admit no solution. Thus discarding all singular pairs costs O_W(p) in the weighted quadruple count. (For positive zero-carry equations these particular p-point fibers actually contribute zero, but that stronger fact is unnecessary.)

Extend W periodically to T³. Its zero extension is continuous because its support avoids every coordinate seam. Approximate it uniformly by a fixed trigonometric polynomial. The uniform approximation error in both sides of (4), before division by p², is O(p²||error||_∞), since the modular variety has p²+O(p) points and ν_D,ν_E have total mass at most one.

For a Fourier monomial exp(2πi(nx+my+kz)), the factors in a and b are diagonal unit-modulus weights. More explicitly, if χ(g)=exp(2πi/q), then

    exp(2πikX_a)=exp(2πikε/q)χ^k(λ(θ+a)).

This identity includes the integer zero-residue representative X_a=1. If k≠0 is fixed, χ^k is nonprincipal for every sufficiently large p. The spectral theorem bounds its restricted regular-pair sum by

    4p^(3/4) sqrt(|D||E|) ≤4p^(7/4).

Its integral in z is zero. If k=0, the complete a,b sum factors exactly; excluding the at most p nonregular pairs costs at most p. Its main term is precisely p²∫H_W dν_Ddν_E. Sum over the fixed Fourier polynomial, let p→∞, and then improve the approximation. This proves (4) uniformly in D,E and every affine/lift choice.

Finally, modular membership and W≠0 imply x+y+z<1 while 0<X_d≤1. The normalized difference lies in (−1,1) and is an integer, hence is zero. Thus the modular weighted sum used above is exactly the genuine zero-carry weighted sum. The half-coset's product relation uses μ=λ²g, so it never requires division by two modulo q. All endpoints are handled by the support condition and the exact Fourier phase identity.

## 6. Limiting deletion densities and a nonlinear cover constraint

Suppose D_p is a deleted subset and its retained complement has no genuine equation. Along any sequence p→∞, pass to a subsequence for which ν_(D_p) converges weakly to a finite measure ν. The full seed empirical measure converges uniformly to Lebesgue measure on [0,1], by (RH) with its irreducible quadratic modulus for each fixed nonzero Fourier character. Since 0≤ν_(D_p)≤ν_full, it follows that ν=d(x)dx with 0≤d≤1 almost everywhere. Its mass is the limiting deletion fraction.

For one ordered edge let r∈{0,1,2,3} count deleted source roles and t∈{0,1} its deleted target role, including repeated role appearances. Since the edge is covered, r+t≥1. Direct inspection of these eight possibilities gives

    1 ≤ r+t−(2/3) binom(r,2).                 (5)

Multiply (5) by a nonnegative smooth compactly supported W and sum over genuine edges. The accepted everywhere-uniform upper bounds for weighted one-vertex role degrees bound the first term by

    p²∫_S W(x,y,z)[d(x)+d(y)+d(z)+d(x+y+z)]dxdydz+o(p²)

after passage to the limit. The total edge mass is p²∫W+o(p²). For each source-role pair, (4) gives its weighted deleted-pair count, whose limiting integral is ∫_S Wd(x)d(y), and similarly for the other pairs. Weak convergence suffices: H_W is continuous, and the products ν_(D_p)⊗ν_(D_p) converge weakly to ν⊗ν, as follows by finite sums of separated continuous test functions.

Consequently every limiting deletion density satisfies

    d(x)+d(y)+d(z)+d(x+y+z)
      ≥1+(2/3)[d(x)d(y)+d(x)d(z)+d(y)d(z)]     (6)

for almost every (x,y,z)∈S. Indeed its weighted integral holds for every nonnegative smooth compactly supported W, so the usual positive-test-function characterization gives (6). This establishes the proposed nonlinear continuum constraint for arbitrary deleted subsets, with no assumed spatial regularity or model of their geometry.

For later use, the set of measurable d∈[0,1] satisfying all these smooth weighted inequalities is weak-* compact in L∞. Linear terms are weak-* continuous; each quadratic term uses a continuous kernel H_W and is weak-* continuous by uniform approximation of H_W by finite sums f(x)g(y). It is a closed subset of the weak-* compact unit interval. Its objective ∫d is continuous. This is a justification for compactness arguments, not a claim that restrictions of d to a singular curve follow directly from (6).

## 7. Scope and unresolved checks

This packet proves the spectral estimate and arbitrary-subset pair law using the stated established RH input, and derives (6) using the independently reviewed weighted one-vertex theorem. A separate continuum certificate may turn (6) into a stronger numerical deletion constant. No numeric improvement is asserted by this file alone. Finite tests are supplementary diagnostics, never replacements for RH, the analytic limit, or an independent audit.

The assertions are uniform over all odd finite fields, all δ and μ, all generators, all λ, the positive canonical integer lifts, and the positive canonical single-coset half-integer lifts. They say nothing about arbitrary Sidon sets, noncanonical lifts, longer intervals, or mixed lattice cosets, and do not resolve Erdős 864.


## Public editorial notice

All mathematical statements, proofs, examples, substantive audit arguments and scope limitations are retained. EDITION_NOTES.md describes the nonmathematical editorial changes: updated acceptance history, public dependency links and removal of excluded provenance metadata. The distributed edition is identified by MANIFEST.json. The complete one-vertex dependency and its audits are linked in DEPENDENCIES.md. Diagnostic summaries report checks rather than replacing mathematical proof. Independent internal AI acceptance is not external human peer review or proof-assistant certification.
