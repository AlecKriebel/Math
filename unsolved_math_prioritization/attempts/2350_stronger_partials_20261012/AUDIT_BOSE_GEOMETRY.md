# Independent geometry and character audit

Date: 12 October 2026 (UTC).

## Verdict and exact scope

**ACCEPT the conditional source/target incidence laws in Part I, subject to one mandatory local correction to the final endpoint sentence in §6.** No substantive obstruction was found in the genus bound, reducibility classification, characteristic-3 treatment, tensor-induced character calculation, low-frequency nontriviality, or uniform normalization error. The uniform upper laws used by the weighted deletion argument survive the correction unchanged.

This is an audit of Part I, §§1–6, of the frozen stronger candidate. It does not independently accept Part II, the optimality claim, or a theorem for arbitrary Sidon sets. The candidate was read but not changed. No publication or remote mutation was performed.

The stronger candidate and accepted carry dependency were inspected. Their complete mathematical contents, with the required stronger-proof corrections, are retained in BOSE_FOUR_FIFTHS_PROOF.md and BOSE_CARRY_DEPENDENCY.md. [Editorial redaction: unpublished-version identity metadata omitted.]

Here p denotes the odd base-field order, q=p²−1, and conjugation means the nontrivial automorphism of K/F. In particular, p is not required to be prime.

## 1. Required correction: the target endpoint has an exception

The last sentence of §6 says that X=1 is included, with source count zero and target limiting count p/2. The target clause must retain the already-stated exceptional-target qualification. The counterexample is not merely a small-field discrepancy.

For every field F of order p=3^k, choose any nonsquare δ, set θ²=δ, use the integer lift, and take

- d=0;
- λ=θ⁻¹;
- μ=λ².

Then λ(θ+d)=1, so the positive canonical representative of this target is B_0=q and X_0=1. Moreover

R=(θ+d)/μ=θ³=δθ=−8δθ

in characteristic 3. This is exactly the exceptional reducible target. Its only modular triple is (0,0,0), because a²=−3δ forces a=0. That triple has three source representatives equal to q, so it is not a genuine equality with target q. Consequently T(0)=0 for this entire unbounded family, contradicting an unqualified T(0)=p/2+o(p).

A small additional example is F_5, δ=2, d=2, λ=(θ+2)⁻¹. Here R=(θ+2)³=4θ=−8δθ and X_d=1. The modular triples are (2,2,2) and (3,3,3). With generator g=θ+2, the latter source has exponent 16 modulo 24, so T(d)=0. With the inverse generator it has exponent 8 and T(d)=1. Thus specifying a generator matters if reporting the exact small-example value, but never changes its O(1) size.

Suggested replacement, kept separate from the candidate:

> The endpoint X=1 is therefore included: its source count is zero, and its target count is p/2+o(p) when the target is nonexceptional. An exceptional target still has T≤2. In particular, both uniform upper laws hold at X=1.

This defect does not change the correctly qualified theorem statement at the start of Part I. It also does not damage any uniform upper bound: an exceptional target contributes at most 2, which is o(p), and an exceptional source contributes zero exactly.

## 2. Source fibers and the collision case

Write M=μ(θ+a)=uθ+v. The coefficient equations give

(ub+v)c+(vb+uδ)=1,

d=(ub+v)δ+(vb+uδ)c.

The exceptional condition N(M)=−u forces u≠0. In that case the first equation, after multiplication by u, becomes

(ub+v)(uc+v)=0.

Thus the entire modular fiber consists of b=b_0 or c=b_0, where b_0=−v/u. On these two lines the target is respectively c or b. Their intersection is counted once, giving 2p−1 modular configurations. Every corresponding genuine equality would require B_a+B_b0=0; positivity rules this out exactly, including for half-integer lifts and repeated vertices.

As a polynomial in a, N(μ)(a²−δ)+u has degree two and nonzero leading coefficient, so there are at most two exceptional source vertices for each seed. Outside them, the linear denominator either has no zero or one excluded zero, giving p or p−1 points.

For the ordinary character argument, r=θ+1/conjugate(M) lies in F exactly in the exceptional case. Apart from that case, the only collision with the quadratic factor for θ is r=−θ, since r=θ is impossible. The accepted CRT argument therefore applies on every other slice, with a squarefree modulus of degree at most five and a nonprincipal quadratic local character whenever one of the two coordinate characters is nonprincipal.

The collision is correctly repaired in the candidate rather than discarded as an exceptional source. It is M=1/(2θ), which cannot satisfy N(M)=−u in odd characteristic. Its fiber is

b≠0, c=δ/b, d=(b+δ/b)/2.

The identity θ+c=θ(θ+b)/b gives the claimed sum with quadratic local character χ^(n+m) and linear local character χ^(−m) restricted to F*. Since χ is faithful of order q, these two local characters are simultaneously principal precisely when

q divides n+m, and p−1 divides m.

For a fixed nonzero integer pair this is impossible for sufficiently large p. The degree-three modulus then gives the stated 2√p estimate. Allowing high-frequency resonances here does not obstruct fixed-frequency torus equidistribution.

No field-order, generator, or affine-seed dependence enters the constants. Multiplication by λ and the half-lattice offset only add unit-modulus phases to Fourier coefficients.

## 3. Target elimination and projective boundary

Eliminating c from

c(a+b)=s−δ−ab,

c(ab+δ)=t−δ(a+b)

gives exactly the candidate's bidegree-(2,2) polynomial F(a,b). Substitution b=−a gives

F(a,−a)=(a²−δ)(a²+s−δ).

For F-rational a, a²−δ is nonzero. Hence a+b=0 forces s=δ−a²≠0, and the second equation gives the unique finite c=t/s. No rational affine points are introduced or lost by elimination.

Over the algebraic closure, the two additional pairs (a,b)=(−θ,θ),(θ,−θ) correspond to c=∞. They are boundary points, not spurious finite triples. The bidegree homogenization has no entire component on a=∞ or b=∞.

The projective equations in (P¹)³ are also correct. If one coordinate is infinite, the other two must be −θ and +θ in opposite order. Two coordinates cannot be infinite, since the remaining coordinate would have to be both −θ and +θ. Thus the boundary is exactly the six distinct P_ij.

At P_12, with x=a+θ, y=b−θ and z=1/c, the linearized equations are

2θx−Rz=0,

−2θy−conjugate(R)z=0.

Their rank is two, and R and conjugate(R) are nonzero. The tangent direction has nonzero x, y and z coordinates. Consequently the point is smooth and all three local parameters vanish to order one. The same argument works at all six points, including in characteristic 3. In particular normalization neither splits these boundary points nor changes the valuations used later.

For an irreducible fiber, the bidegree-(2,2) model has arithmetic genus one. Its smooth normalization therefore has genus at most one. There is no unjustified assumption of smoothness of the original affine fiber.

## 4. Geometric reducibility, including characteristic 3

As a polynomial in b, F has leading coefficient a²−δ and linear coefficient t−sa. At a=±θ the latter is nonzero, because

(t−sθ)(t+sθ)=N(R)≠0.

Thus the coefficients are primitive as polynomials in a. In odd characteristic the discriminant criterion is applicable over the algebraic closure; a rational square discriminant is a polynomial square by unique factorization. There is no omitted vertical component.

I independently recomputed the discriminant and obtained the polynomial printed in the candidate. If t≠0, comparing a possible square (2θa²+A a+B)² forces

A=−t/θ, B=θ(s−2δ), t²=δs²,

and the last identity contradicts N(R)≠0. The calculation divides only by nonzero t, θ, and 2, and remains valid in characteristic 3.

If t=0, the remaining square condition reduces exactly to

(s²+4δs−8δ²)²−64δ³(δ−s)=s³(s+8δ)=0.

Since s=0 would give R=0, the only reducible value is s=−8δ. The displayed factorization into the two (1,1) factors is valid in every odd characteristic. These factors are distinct and exchanged by Frobenius. Their intersection has a=b and a²=−3δ, and the original equations then force c=a. When characteristic is 3, this gives only (0,0,0); no division by a or by 3 is needed.

The injectivity of d↦(θ+d)/μ consequently gives at most one exceptional target in a seed, with at most two modular triples.

The warning about singular irreducible characteristic-3 fibers is substantive and correctly handled. For example, in characteristic 3 take s=δ and any t≠0. If α³=t, then the diagonal point (α,α,α) is singular, while the reducibility classification says this fiber is irreducible. The normalization argument must therefore be retained; treating all nonexceptional curves as elliptic curves would be wrong.

For an integral genus-one-arithmetic curve, the sum of the singularity delta invariants is at most one. There is thus at most one geometric singular point, with at most two geometric branches. Normalization changes the rational-point sum by O(1), uniformly in the parameter. At the finite branches, a±θ and b±θ are units because both product equations have nonzero right sides; the Kummer sheaf introduces no new finite punctures. Each individual character value has modulus one, so the same O(1) bound applies to the weighted character sum, not merely to the unweighted point count.

## 5. Tensor induction: trace and geometric monodromy

Let U be the normalization of a nonexceptional projective fiber with its six boundary points removed. It is smooth and geometrically connected over the finite field. On U_K, the function

f=(a+θ)^n(b+θ)^m

is an invertible regular function, also for negative n or m. Its Kummer character is lisse, rank one, and has finite monodromy of order prime to the field characteristic.

The arithmetic trace and geometric base-change character are different statements and the candidate handles both correctly.

First, if F_x is geometric Frobenius at an F-point, the rank-one tensor induction has trace ρ(F_x²). This is the original Kummer trace at the corresponding K-point, hence exactly χ(f(x)). There is no extra p-th power on this trace.

Second, after restriction back to U_K, tensor induction is the product of the original character and its constant-field conjugate. To check that conjugate directly on this curve's function field, let ξ^q=f and let σ lift the nontrivial constant-field automorphism. For h in the subgroup over K, write

r=h(σ⁻¹ξ)/(σ⁻¹ξ), which lies in the q-th roots of unity K*.

Conjugation acts on r by r↦r^p. Thus the conjugated character is the Kummer character associated to χ^p and conjugate(f). No rationality of the curve function field is needed for this calculation. The geometric tensor product is therefore the Kummer character of χ attached to

f·conjugate(f)^p.

The candidate does not incorrectly apply an affine-space-only statement to a genus-one curve: it explicitly supplies the function-field extension of the calculation. As a consistency check, at an F-point conjugate(f(x))=f(x)^p, so the K-Frobenius trace of this restricted sheaf is χ(f(x))², exactly the square of the F-Frobenius trace. One must not replace the original incomplete sum by a sum of χ(f·conjugate(f)^p); the candidate does not do that.

At P_12 and P_21 the valuations of the geometric Kummer function are respectively

n+pm and m+pn.

If |n|,|m|<p−1, both have absolute value strictly below q. If both were divisible by q, both would equal zero as integers. Solving those two integer equations gives n=m=0. Thus every fixed nonzero Fourier pair yields genuinely nontrivial geometric monodromy for all sufficiently large p, uniformly in R, μ and the generator. This does not require classifying all high-frequency resonances.

A faithful character of order q is nontrivial on local inertia whenever the relevant valuation is not divisible by q. Changing generators replaces that character by a unit power, preserving this criterion. There is therefore no cancellation by a generator change or by a special irreducible fiber within the fixed-frequency range just proved.

**Scope limitation: this is not a claim of nontriviality for every field-dependent character pair.** In the order P_12, P_21, P_13, P_31, P_23, P_32, the full list of boundary valuations is

n+pm, m+pn, n−(p+1)m, pn−(p+1)m, m−(p+1)n, pm−(p+1)n.

I checked the modular kernel independently. Simultaneous divisibility by q forces n≡−pm and (2p+1)m≡(p+2)m≡0 modulo q. Since gcd(q,2p+1,p+2) is 3 when p≡1 modulo 3 and 1 otherwise, the nonzero kernel consists exactly of n≡−m with m≡q/3 or 2q/3 when p≡1 modulo 3. For these large frequencies, boundary valuations do not decide whether the unramified sheaf is geometrically trivial. They must not be advertised as covered by the nontriviality argument. Both nonzero frequencies tend to infinity with p, so this issue is immaterial to fixed-frequency weak convergence and all subsequent fixed-test-function applications.

## 6. Curve-bound hypotheses and uniformity

All hypotheses needed for the rank-one curve estimate are satisfied:

1. U is smooth and geometrically connected after normalization of the irreducible fiber.
2. Its completion has genus h≤1, and the deleted geometric set has exactly six points.
3. The sheaf has rank one and finite monodromy, so its Frobenius eigenvalues are roots of unity and its weight is zero.
4. Its possible ramification is tame at those six points, since the Kummer order q is prime to the characteristic. No Swan conductor appears.
5. The valuation argument proves geometric nontriviality. In rank one this excludes every nonzero constant subsheaf or quotient.

The bound is consequently at most (2h−2+6)√p≤6√p on U. Passing to the original fiber costs only O(1). The fact that the displayed exponent p in conjugate(f)^p grows with the field order is harmless: rank, number of punctures and tame conductor stay bounded.

The constant coefficient is p+O(√p). Indeed, the smooth completion obeys the ordinary genus-at-most-one point bound, the boundary has no F-rational points (Frobenius exchanges P_ij with P_ji), and normalization changes the affine count by only O(1). These are uniform estimates even through singular families and over nonprime odd field orders.

## 7. Conditional carry regions and the surviving upper laws

The source and target fixed-frequency estimates, together with bounded normalized fiber mass, imply uniform weak convergence against each fixed continuous function on the two-torus. For the moving triangles, a finite mesh of the parameter X and inclusions between adjacent triangles give a uniform squeeze. The area change tends to zero with mesh size, and the fixed mesh has only finitely many continuity sets. This legitimately gives the stated uniform o(p), with no unjustified interchange of a shrinking mesh and the field limit.

The source zero-carry triangle has area (1−X)²/2. For a fixed target, the third source is determined modulo one and the zero-carry triangle has area X²/2. Boundary and seam discrepancies are O(1): fixing a free coordinate leaves at most one point on a nonexceptional source fiber; fixing a target or one source in a target fiber leaves at most two ordered pair representations by strong Sidonicity. Exceptional source lines were already handled exactly.

The half-integer model gives μ=λ²g, requires no division by two modulo the even integer q, and changes the Fourier coordinates only by constant phases. The positive integer seam representative requires the qualification in §1 above, but otherwise the counting argument is correct.

Accordingly, the following conclusions are accepted after that qualification:

- At every nonexceptional source, S(a)=p(1−X_a)²/2+o(p), uniformly.
- Every exceptional source has S(a)=0 exactly.
- At every nonexceptional target, T(d)=pX_d²/2+o(p), uniformly.
- Every exceptional target has T(d)≤2.
- Therefore both upper laws hold uniformly at every vertex, including the integer endpoint.

## 8. Inspected sources and verification record

Primary external source: Lei Fu and Daqing Wan, *A Class of Incomplete Character Sums*, arXiv:1303.3650v3, 6 January 2025. [Versioned primary HTML](https://arxiv.org/html/1303.3650v3), [primary PDF](https://arxiv.org/pdf/1303.3650), [version record](https://arxiv.org/abs/1303.3650v3).

I inspected Proposition 1.2 and its preceding Frobenius trace identity (printed p. 5); the Kummer function-field calculation and Proposition 2.1 (§2, pp. 6–8); and Proposition 4.1/Theorem 4.2 with their curve hypotheses (pp. 12–13). Proposition 1.2 has general geometrically connected scheme scope. The affine-space wording of Proposition 2.1 does not itself establish arbitrary-curve scope, which is why the direct calculation in §5 matters. The version note identifies a correction to Theorem 4.6, which is not used here. The primary text supports the input actually applied. Inspection used primary HTML and PDF extracted text; no local PDF byte count or hash is claimed.

The accepted carry proof was inspected for its polynomial Dirichlet RH statement, its source factorization and degeneracy classification, and its positive-lift conventions. Its external RH input is inherited as an already accepted dependency rather than independently reproved here.

Additional independent algebra: symbolic expansion reproduced the target discriminant, the factorization F(a,−a), and the square-obstruction factor s³(s+8δ). The characteristic-3 endpoint counterfamily and tensor-induction calculations above are exact arguments, not numerical evidence for an asymptotic conclusion.

## Narrowed public edition notice

All mathematical arguments, hypotheses, examples, substantive audit discussion and corrections above are retained. This edition removes unpublished artifact identifiers and related provenance metadata, replaces obsolete locators, and updates editorial history only. The scope of each theorem and review is unchanged. Exact reversible redaction records and private integrity inventories remain local and are not distributed. [EDITION_MAP.md](EDITION_MAP.md) describes the changes; [PRESERVATION.json](PRESERVATION.json) records mathematical-text preservation without republishing redacted identifiers. [PUBLIC_DEPENDENCIES.json](PUBLIC_DEPENDENCIES.json) identifies only distributed mathematical texts and already-published dependencies. [VERIFICATION.json](VERIFICATION.json) gives aggregate diagnostic results without program or diagnostic-file identities. No source document, executable code, raw per-case collection, dataset contents, private source, personal information or coordination record is included.
