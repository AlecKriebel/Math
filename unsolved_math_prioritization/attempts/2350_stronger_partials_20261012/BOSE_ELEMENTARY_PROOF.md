# An elementary 0.843061 retention bound for canonical Bose–Chowla lifts

12 October 2026. Original construction-specific proof, subsequently independently accepted without mathematical changes in AUDIT_BOSE_RETENTION.md. The original pre-audit status is recorded in PRESERVATION.json. No novelty claim. No repository mutation or publication was part of the original research.

## Main theorem

Under the full affine Bose–Chowla setup and either canonical lift defined in Part I, every triple-sum-free subset B′ satisfies

    |B′| ≤ (127070161/150724800 + o(1)) p.

The error is uniform over odd field orders, translations, unit dilations, and the two lift conventions separately. Its constant is approximately 0.843060737184591. This statement uses only polynomial Dirichlet L-function RH, together with the accepted full-seed carry/equidistribution theorem copied in BOSE_CARRY_DEPENDENCY.md. It uses no character-sheaf estimate on a positive-genus curve. Arbitrary deleted subsets are covered through measure domination; no interval shape is assumed. This is not a theorem about arbitrary Sidon sets or a resolution of Erdős 864.

## Part I. Conditional incidence estimates

# Elementary conditional source law and target marginal bound

12 October 2026. Standalone supplement using only the polynomial Dirichlet RH input already accepted in the Bose–Chowla carry proof. No curve-sheaf RH is used here. No repository mutation or publication.

## Setup and conclusions

Use the notation of the accepted proof: odd finite-field order p, K=F(θ), θ²=δ nonsquare, q=p²−1, arbitrary generator g and λ≠0, and one of the positive canonical lifts with ε=0 or 1/2. Put μ=λ²g^(2ε), and X_a=B_a/q∈(0,1]. Let S(a) and T(a) be the numbers of genuine ordered zero-carry equalities with a fixed in one prescribed source position and the target position, respectively.

Uniformly in all parameters and a:

    S(a) ≤ p(1−X_a)²/2 + o(p),
    T(a) ≤ 2pX_a/3 + o(p).

Outside at most two explicitly identified source points the source inequality is equality to within o(p). At those source points the count is exactly zero. More generally, for any fixed 0≤τ≤1 the count S_≤τ(a) in the prescribed source role whose target has normalized coordinate at most τ satisfies

    S_≤τ(a) ≤ p(τ−X_a)_+²/2 + o(p),

with asymptotic equality at all nonexceptional source points. In particular this applies to τ=7/10. The complementary target range has limiting source count

    p[(1−X_a)²−(τ−X_a)_+²]/2

at nonexceptional source points, and zero at the exceptional source points. The little-oh errors are uniform in the vertex and all algebraic/lift parameters.

## 1. Source fibers, using the accepted degree-five argument

Fix a and M=μ(θ+a)=uθ+v. With U=ub+v,V=vb+uδ, the ordinary source fiber is c=(1−V)/U,d=Uδ+Vc. Exactly as in the accepted proof, the at most two roots of N(M)=−u are exceptional. Each such fiber is the union b=b0,d=c and c=b0,d=b, where b0=−v/u and M(θ+b0)=1. Genuine equality would require B_a+B_b0=0, so all its zero-carry source counts vanish.

On every other fiber, for r=θ+1/conj(M),

    θ+c=−conj(M)(b−r)/(ub+v).

If r≠−θ, two distinct irreducible quadratics and an optional linear denominator give, by the accepted CRT/Dirichlet-RH argument, a ≤4√p bound on every fixed nonzero two-coordinate Fourier coefficient in the b,c logs for sufficiently large p.

The only collision is M=1/(2θ), for which b≠0,c=δ/b and θ+c=θ(θ+b)/b. At frequency (n,m) the sum is a unit scalar times

    Σ_{b∈F*} χ^(n+m)(θ+b)χ^(−m)(b).

Its degree-three Dirichlet character is principal only if q divides n+m and p−1 divides m. For fixed (n,m)≠(0,0) this cannot occur once p is large. Hence the same limiting two-dimensional Haar law holds at this collision point as well, with ≤2√p Fourier bounds. Alternatively the collision can be discarded as one additional exceptional vertex at an O(p) aggregate cost; the asserted source formula retains it.

The constant coefficient is p+O(1). Therefore the free source coordinates are uniformly equidistributed on T² in every nonexceptional source fiber.

## 2. Moving carry regions and target weights

For a fixed source coordinate x=X_a, genuine zero carry and target at most τ require y+z≤τ−x, outside coordinate seams and equality boundaries. The triangle's area is (τ−x)_+²/2. Uniformity for varying x follows by sandwiching triangles between finitely many triangles indexed by a mesh in [0,1]; the area difference is O(mesh size). Fixed-frequency uniformity gives convergence on each of the finitely many mesh triangles, whose boundaries have Haar measure zero. First let p tend to infinity and then let the mesh size tend to zero.

More generally, for any fixed bounded continuous target weight h on [0,1], the weighted source count divided by p converges uniformly on nonexceptional fibers to

    ∫_0^(1−x) t h(x+t) dt.

The same holds for finitely many fixed jumps of h, by the mesh/continuity-set argument. This includes either side of the cutoff 7/10.

For the integer lift, only one element can lie at the torus seam. Within a nonexceptional source fiber, fixing either other source to that element gives at most one point, and fixing the target gives at most two by pair-sum Sidonicity. Thus correcting seam representatives changes each count by O(1). Half-coset coordinates have no seam. Their constant Fourier phases and the parameter μ=λ²g do not change any bound. This proves all the source assertions.

## 3. Fixed-target modular source marginals

Fix d and write R=(θ+d)/μ=Aθ+B, A,B∈F. For each a, let n_a be the number of ordered pairs (b,c) in the modular target fiber. Dividing the fixed product by θ+a gives

    b+c=(Aa−B)/(a²−δ),
    bc=(Ba−Aδ)/(a²−δ)−δ.

The denominator is nonzero for every a∈F. If φ is the quadratic character of F extended by φ(0)=0, the quadratic formula gives

    n_a=1+φ(D(a)),

where

    D(a)=(Aa−B)²−4[Ba−Aδ−δ(a²−δ)](a²−δ).

This includes repeated roots with multiplicity one. D has degree four, leading coefficient 4δ (a nonsquare in F), and

    D(θ)=(Aθ−B)²≠0,
    D(−θ)=(−Aθ−B)²≠0,

because R and conj(R) are nonzero.

Write D=c Q² H, where H is monic squarefree and includes precisely the irreducible factors of D occurring to odd multiplicity. If H is constant, c is a nonsquare because the leading coefficient of D is a nonsquare. Thus n_a is zero except possibly at the at most four zeros of D. The entire modular target fiber then has O(1) points, so every asserted target bound follows immediately.

Suppose H is nonconstant. The sum of φ(D(a)) is O(√p), by polynomial Dirichlet RH applied to the quadratic characters at H's irreducible factors; zeros belonging to even factors change at most four terms. Hence Σ_a n_a=p+O(√p).

For any nonprincipal multiplicative character ξ of K*,

    Σ_a ξ(θ+a)n_a
      =Σ_a ξ(θ+a)+Σ_a ξ(θ+a)φ(D(a)) = O(√p).

Here is the precise nontriviality justification. At the irreducible quadratic T²−δ use the local character ξ. At each irreducible factor h(a) of H, use the quadratic character of its residue field, evaluated at a minus a root of h; its value is φ(h(a)), by the norm identity. In Dirichlet notation these are the corresponding irreducible factors h(−T), up to harmless scalar normalization. They are coprime to T²−δ because D(±θ)≠0. CRT therefore gives a nonprincipal composite character of total squarefree modulus degree at most six, even if the character at one or more other local factors is principal. The degree-six RH bound is ≤5√p, with O(1) corrections at the even-multiplicity roots; the first sum has bound √p. All constants are absolute.

Taking ξ=χ^k with any fixed k≠0 gives uniform vanishing of every nonzero fixed Fourier coefficient of the normalized first-source marginal. Thus, for every target fiber with nonconstant H, its one-coordinate modular marginal converges uniformly to Lebesgue measure on [0,1]. The same is true in all source roles by symmetry. Moving the single possible zero residue to the endpoint changes at most two marginal atoms, by pair-sum Sidonicity, so this is a statement for the actual positive lift as well. No claim of two-dimensional joint target equidistribution is needed.

## 4. From uniform marginals to the target bound

Let ρ_d be the first-source marginal of the genuine zero-carry subfiber, divided by p, and put β_d=T(d)/p. This is a positive submeasure of the full modular marginal. In a nonnegligible target fiber every subsequential limit ρ is therefore dominated by Lebesgue measure. Source permutation symmetry and the exact equality x1+x2+x3=X_d give

    ∫ y dρ_d(y)=X_d β_d/3.

Now use the elementary rearrangement inequality: if 0≤ρ≤Lebesgue on [0,1] and ρ([0,1])=β, then

    ∫ y dρ(y) ≥ β²/2.

Indeed, the smallest first moment for mass β is obtained by filling the initial interval [0,β] with density one. Along any sequence of parameters, take subsequences with X_d→x, β_d→β and ρ_d weakly convergent. The previous two displays yield β²/2≤xβ/3, hence β≤2x/3 (also when β=0). Compactness and the uniform marginal estimates make this conclusion uniform over all target fibers. Fibers with H constant have O(1) points and satisfy it too.

This completes a standalone proof of the elementary target bound using only the accepted polynomial Dirichlet RH input. It also proves the stated source cutoff laws, ready for weighted deletion arguments.


## Part II. Exact deletion certificate

# Exact arbitrary-subset deletion certificate from elementary target bounds

Date: 12 October 2026. Local research derivation, with no publication or repository mutation. The required incidence statements are proved in Part I of this packet. In particular, it does **not** assume the sharper full pointwise target law.

## 1. Required inputs

Write normalized canonical lift coordinates as x=b/q, and let p tend to infinity. The following errors must be uniform over the Bose–Chowla seed parameters and over the fixed vertex, apart from O(1) exceptional vertices whose total incidence is O(p).

1. The empirical seed measure p^(-1) sum_{b in B} delta_{b/q} converges to Lebesgue measure on [0,1].
2. The full ordered zero-carry equation measure converges to Lebesgue measure on x+y+z=w, with x,y,z>0 and w<=1. In particular its target marginal is g(w)dw, where g(w)=w²/2.
3. For a vertex of normalized position x, the sum of the three prescribed source-role incidences among equations with target at least a, divided by p, converges to

   s_a(x) = (3/2)[(1-x)² - (a-x)_+²].

4. Its unweighted target-role incidence is at most p[k(x)+o(1)], where k(x)=2x/3.

Part I derives input 3 through two-dimensional source-slice equidistribution and input 4 through an elementary univariate marginal argument. The previously accepted carry theorem supplies input 2. All repetitions may remain counted.

## 2. Arbitrary deletions, without an interval assumption

Let D be an arbitrary deleted subset, and suppose the complement contains no zero-carry equation. Along any subsequence on which |D|/p converges, extract a further weakly convergent subsequence of

   mu_D = p^(-1) sum_{b in D} delta_{b/q}.

Since mu_D is dominated by the full empirical seed measure, its limit is d(x)dx with 0<=d<=1. Let r=integral d.

Also take the target-deletion measure that assigns mass p^(-2) times the target-role incidence to every point of D. It is dominated by the full target marginal, so its limit is e(x)dx with e<=g. Input 4, tested against nonnegative continuous functions and then passed to the limit, gives e<=k d. Thus

   0 <= e(x) <= min(k(x)d(x),g(x)) almost everywhere.

Every equation with target at least a is destroyed by D. Counting its incidences in deleted source roles and, separately, in the deleted target role therefore gives

   M_a <= integral [s_a(x)d(x) + 1_[a,1](x)e(x)] dx,
   M_a = integral_a^1 g(x)dx = (1-a³)/6.

Any repeated role merely overcounts the right-hand side, which is safe. The conclusion applies to arbitrary microscopic deletion patterns. No assertion that D is an interval or is itself equidistributed has been made.

For complete endpoint rigor, convergence against 1_[a,1] follows because the limiting target measures are dominated by the continuous density g, hence have no atom at a; source profile convergence uses input 3. Alternatively approximate this single target cutoff by continuous weights from above and below.

## 3. A pointwise dual inequality

Put c(x)=g(x)/k(x)=3x/4 for x>0, and set c(0)=0. For any nonnegative weight phi and lambda>=0, let s be its source-incidence profile, and put u=s+phi k. For every d in [0,1],

   s d + phi min(kd,g)
   <= lambda d + c(u-lambda)_+ + (1-c)(s-lambda)_+.

Proof: the left side as a function of d has slope u for 0<=d<=c and slope s for c<=d<=1. Subtract lambda d and integrate its positive slopes over their allowed lengths. Equivalently verify the two line segments directly. This is the fractional-knapsack dual and is valid pointwise.

Consequently every triple-sum-free retained subset satisfies

   r >= [M_phi - J(lambda)]/lambda,
   J(lambda)=integral [c(u-lambda)_+ +(1-c)(s-lambda)_+]dx,

whenever lambda>0.

## 4. A fully rational certificate

Choose a=7/10, phi=1_[a,1], and lambda=1163/1800. Then

   M=219/2000,
   s(x)=153/200-(9/10)x                 for 0<=x<=7/10,
   s(x)=(3/2)(1-x)²                    for 7/10<=x<=1.

Below a the two knapsack slopes coincide with s. Above a the lower slope s is always less than lambda; the upper slope is

   h(x)=(3/2)-(7/3)x+(3/2)x².

The positive excess below a lies exactly on [0,b], b=107/810. Above a it lies exactly on [c,1], c=29/30. These statements follow by solving the linear first equation and the quadratic second equation, or checking h(29/30)=lambda and the sign of the quadratic.

Hence

   J1= integral_0^b (s-lambda)dx
      =11449/1458000,
   J2= integral_(29/30)^1 (3x/4)(h-lambda)dx
      =6409/25920000.

Substitution gives the exact consequence

   r >= (219/2000 -11449/1458000 -6409/25920000)/(1163/1800)
     =23654639/150724800
     =0.15693926281540926... .

Restoring the vanishing errors,

   |B\D| <= (127070161/150724800 + o(1))p
          = (0.8430607371845907... + o(1))p.

This is strictly stronger than the elementary unweighted and unweighted full-target union-bound constants. It still does not reach sqrt(2/3)=0.816496580927726... . Its hypotheses and scope remain confined to these canonical Bose–Chowla lifts.

## 5. Independent arithmetic and related diagnostics

The exact rational diagnostic checks all arithmetic with rational numbers, including the sign-region endpoints and the exact final fraction. The asymptotic input lemmas are proved in Part I, not certified by the arithmetic script.


## Narrowed public edition notice

All mathematical arguments, hypotheses, examples, substantive audit discussion and corrections above are retained. This edition removes unpublished artifact identifiers and related provenance metadata, replaces obsolete locators, and updates editorial history only. The scope of each theorem and review is unchanged. Exact reversible redaction records and private integrity inventories remain local and are not distributed. [EDITION_MAP.md](EDITION_MAP.md) describes the changes; [PRESERVATION.json](PRESERVATION.json) records mathematical-text preservation without republishing redacted identifiers. [PUBLIC_DEPENDENCIES.json](PUBLIC_DEPENDENCIES.json) identifies only distributed mathematical texts and already-published dependencies. [VERIFICATION.json](VERIFICATION.json) gives aggregate diagnostic results without program or diagnostic-file identities. No source document, executable code, raw per-case collection, dataset contents, private source, personal information or coordination record is included.
