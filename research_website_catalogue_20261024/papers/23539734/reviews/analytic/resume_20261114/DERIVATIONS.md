# Analytic reconstruction and attempts to falsify it

Record 23539734, version 1.1, DOI 10.5281/zenodo.23539734. Completed 2026-11-14 UTC. This is an AI technical review of the published claim, not a replacement theorem or human peer review. It continues an already sealed lane; no claim of a historically fresh lane is made.

## Exact claim and success criteria

Let L(u,v)=(u,(u²+1)v) over Q and S={prime p:p≡3 mod 4}. For p∈S, every affine point must be periodic, weighted uniformly by point with mass 1/p², and periods must be divided by p. Write θp=φ(p−1)/(p−1), μp=p⁻²∑z δ(Tp(z)/p), Dp(x)=μp([0,x]). The target is all three parts of Theorem 1 at their stated quantifiers:

1. For each fixed x∈[1/2,1), the published explicit error bound eventually holds along S.
2. The limsup is 1 and the liminf is at most 23/24 along S.
3. Every A⊆S with positive upper relative prime density has nonconvergent Dp(x), for every fixed x∈[1/2,1), and nonconvergent probability measures μp in the weak topology on [0,∞).

Proposition 4 separately requires the corresponding nonconvergence along every positive-upper-density subset of all odd primes, with every regular point retained, uniform point weights renormalized, and arbitrary deletion or finite nonnegative period assignments restricted to the exceptional fibers. It does not claim that L is a permutation of the entire affine plane for all odd primes. Success requires checking the original theorem, the classical imports, this extra convention-dependent proposition, and their exact interfaces. Finite sampling cannot satisfy the infinite-prime success criterion.

## 1. Geometry, category and exact point counts

The rational inverse (u,v/(u²+1)) composes with L to the identity where u²+1≠0, a dense open set, so L is birational over Q. L has a polynomial forward formula and has no polynomial inverse over C: restricting an alleged inverse's second coordinate to fixed u would require division by u²+1, and its zero fibers contract. The invariant u has affine-line generic fibers, genus zero. Iteration multiplies v by (u²+1)^m, and this nonconstant rational function is never identically 1 for m>0. Thus the map has infinite order. No genus-one or polynomial-automorphism hypothesis is supplied or needed.

For p≡3 mod 4, a=u²+1 never vanishes. On a fixed fiber, v=0 has period 1, and v≠0 has least period ord(a). There is no transient orbit and no multiplicity weighting issue. Put N=p−1 and Pp=#{u:ord(u²+1)=N}. Every proper divisor d of N obeys d≤N/2<p/2. For fixed 1/2≤x<1 and p(1−x)>1, the maximal period N is strictly larger than px while every proper divisor is smaller than px. Exactly (p−1)Pp points are excluded:

    Dp(x)=1−(p−1)Pp/p².                                      (A1)

The condition is strict and essential. At x=N/p, every point is counted. At p=3,x=3/4 the eventual identity is inapplicable. At x=0 the CDF is 0; at x=1 it is 1. An estimate uniform for moving x→1 would be false. Equal weighting of cycles is also different: at p=7,x=3/4 the point CDF is 25/49, while the equal-cycle CDF is 17/21. This countercontrol was obtained independently from exact fiber periods.

## 2. Primitive indicator and the error term

For a generator g of Fp×, write a=g^k. With every multiplicative character extended by 0 at 0, including the principal one,

    1(ord(a)=N)=θp ∑d|N μ(d)/φ(d) ∑ord(χ)=d χ(a).             (A2)

For squarefree d, the inner sum is the Ramanujan sum cd(k), and the whole sum factors over primes ℓ|N as ∏(1−cℓ(k)/(ℓ−1)). It vanishes when any ℓ|k and otherwise equals ∏ℓ ℓ/(ℓ−1)=1/θp. The factor θp is indispensable. The exact integer Ramanujan formula cd(k)=∑e|gcd(d,k) e μ(d/e) gives a finite independent check without complex arithmetic.

For nonprincipal χ, the square-root count gives

    Sχ=∑u χ(u²+1)=∑t(1+η(t))χ(t+1)=η(−1)J(η,χ).             (A3)

The term ∑tχ(t+1) is 0. The principal term is treated separately. If χ≠η, all η,χ,ηχ are nonprincipal and the Gauss identity G(η)G(χ)=J(η,χ)G(ηχ), with |G(α)|²=p, gives |Sχ|²=p. For χ=η, J(η,η)=−η(−1), so Sη=−1 and |Sη|²=1 in both odd residue classes. The exceptional quadratic case does not invalidate the bound |Sχ|≤√p. The elementary Gauss identity follows by decomposing the product according to the sum of its two variables; the t+s=0 contribution vanishes because ηχ is nonprincipal. The exceptional Jacobi formula follows from s/(1−s), omitting s=1 and accounting for the missing value −1.

Summing (A2) over u, all multipliers are nonzero on S, so the principal term is exactly pθp. Each nontrivial squarefree d contributes at most θp√p after the φ(d) characters cancel the denominator. Hence

    |Pp/p−θp|≤θp(2^ω(N)−1)/√p.                              (A4)

The six possible prime divisors below 16 contribute at most 64, and each ℓ≥17 satisfies 2≤ℓ^(1/4). Thus 2^ω(N)≤64 N^(1/4). Combining (A1),(A4),

    |Dp(x)−(1−θp)|
      ≤θp/p+(1−1/p)|Pp/p−θp|
      ≤1/p+64p^(−1/4).                                     (A5)

The RHS is deliberately loose but tends to zero. No finite tested range establishes this limiting fact; the displayed inequalities do.

## 3. The classical prime mean and two subsequences

The needed mean is ∑p≤X θp/π(X)→A=∏ℓ(1−1/(ℓ(ℓ−1))). It is unconditional, and it is not Artin's conjecture for a fixed integer base. Möbius inversion gives exactly

    ∑p≤X θp=∑d≤X−1 μ(d)π(X;1,d)/d.                         (A6)

With K=(log X)^6, the absolute tail is at most X∑d>K d⁻²=O(X/K). For d≤K, Siegel–Walfisz with exponent 4 gives total error O(X log K/(log X)^4)=o(X/log X). Absolute convergence of ∑d1/(dφ(d)) follows from φ(d)≥√(d/2): the prime-power factors in φ(d)²/d are at least 1 except 2¹, whose factor is 1/2. The truncated coefficient therefore tends to its absolutely convergent Euler product A, and PNT finishes the mean. There is no growing-modulus Dirichlet claim hidden here: the needed uniformity is precisely the standard Siegel–Walfisz range for d≤(log X)^6.

The factor at 2 is 1/2. Since ∑odd prime ℓ 1/(ℓ(ℓ−1))≤∑n≥3,n≠4 1/(n(n−1))=5/12, the elementary product inequality yields A≥(1/2)(1−5/12)=7/24>13/48.

Let Qj be the product of the first j odd primes. CRT gives a coprime class p≡3 mod4 and p≡1 modQj modulo 4Qj. For each j, ordinary Dirichlet provides arbitrarily large primes in that fixed class, permitting an increasing pj. No uniform assertion in j is needed. Since θpj≤(1/2)∏ℓ|Qj(1−1/ℓ)→0, equation (A5) gives Dpj(x)→1 for every fixed x in the stated interval.

If only finitely many p∈S had θp≥1/24, then, because θp≤1/2 at every odd prime and both odd residue classes have prime density 1/2, the mean's limsup would be at most (1/2)(1/2)+(1/2)(1/24)=13/48. This contradicts A≥7/24. An increasing qj∈S with θqj≥1/24 therefore exists, and limsupj Dqj(x)≤23/24. Both selected sequences can be independent of x; only the eventual threshold bound depends on x.

## 4. Atomlessness and the upper-density quantifier

The scalar input concerns empirical distributions of θp over primes. It is stronger than mere nonconvergence of θp. The following direct lemma uses only atomlessness, with no absolute continuity assumption.

If b_p→c along a prime subset A of upper relative density δ>0 and the full-prime empirical laws converge to an atomless probability ν, then for every ε>0, all but finitely many A-points lie in Iε=[c−ε,c+ε]. Its boundary has ν-measure 0, so its empirical frequency converges to ν(Iε). Taking upper densities gives δ≤ν(Iε). Continuity from above as ε↓0 gives δ≤ν({c})=0, contradiction. The proof works for upper density and for c=0 or 1. A lower-density hypothesis is not smuggled into it.

Since S has prime density 1/2, positive upper relative density inside S implies positive upper density among all primes. Therefore (A5) and the classical scalar law exclude convergence of Dp(x) on every A in Theorem 1(iii). They require no law conditioned on p≡3 mod4.

For measures, a nonconvergent CDF at a putative atom of a limit would alone be insufficient. The published function

    h(t)=max(0,min(1,2t−1)),  t≥0,

is globally bounded and continuous. All proper-divisor periods satisfy h(d/p)=0; a maximal period satisfies h(N/p)=1−2/p. Thus exactly

    ∫h dμp=(1−2/p)(p−1)Pp/p²=θp+o(1).                      (A7)

Weak convergence forces convergence of this moment, contradicting the scalar lemma. This closes the weak-topology interface without selecting CDF continuity points.

## 5. All-odd-prime proposition

For any odd p, rp=#{u:u²+1=0} is 0 or 2. On Ωp={(u,v):u²+1≠0}, all regular points are periodic and |Ωp|=R=p(p−rp). The principal character term in the primitive count is now (p−rp)θp; every nonprincipal bound (A3) is unchanged. Thus

    |Pp/p−θp|≤rpθp/p+θp(2^ω(N)−1)/√p=o(1)

uniformly over odd primes. For fixed x in the original interval and p(1−x)>1,

    Dreg_p(x)=1−(p−1)Pp/R=1−θp+o(1),
    ∫h dμreg_p=(1−2/p)(p−1)Pp/R=θp+o(1).

The factor (p−1)/(p−rp)=1+O(1/p) is uniform for rp∈{0,2}. If e exceptional points remain, 0≤e≤rp p, and arbitrary finite periods are assigned to them, then

    μtilde_p=(R/(R+e)) μreg_p+ξp,
    mass(ξp)=e/(R+e)≤rp/p≤2/p.

For every f valued in [0,1], the difference of integrals is at most e/(R+e); for bounded real f it is at most 2||f||∞e/(R+e). In particular both the CDF and h change by o(1), irrespective of assigned periods growing faster than p. The global definition of h handles normalized periods exceeding 1. Scalar atomlessness therefore excludes the claimed convergence on any positive-upper-prime-density set under every permitted convention. Unbounded test functions, changing the regular points, or changing uniform point weights would go beyond this argument; none is asserted.

## 6. Primary theorem interfaces actually checked

All paths below are under `reviews/scope/cache/primary/`, reused only as raw primary bodies. Hashes are recorded in the custody and final input bindings.

- `deshouillers-hassani-published.pdf`, printed pp.77–79, especially Proposition 2.1 on p.78 and (2.1),(2.2) on p.79. Its g(n)=φ(n)/n and m=2 specialize directly to all odd primes, differing from all primes by one observation. For any prime ℓ, log g(ℓ)=−1/ℓ+O(ℓ⁻²); the first two three-series sums converge absolutely, and the large-log series is empty. The continuity criterion is the divergence of the reciprocal odd-prime sum. This is a continuous CDF, giving an atomless probability measure. A sentence in that primary uses a density notation for its Lebesgue–Stieltjes measure; the present proof does not assume absolute continuity and does not use that notation.
- `aivazidis-sofos-v2.pdf`, printed pp.2–4, Theorem 1.3(i), and pp.16–17, Theorem 6.3 and its application. At n=1, pn(q)=φ(q−1)/(q−1). Their proof first gives the distribution over primes, with f(k)=log(φ(k)/k), g1(t)=t−1 and ρg1(ℓ)=1, proves continuity via ∑ℓ1/(ℓ−1)=∞, then transfers to prime powers. Thus the manuscript's whole-prime input is directly supported, not inferred from an inappropriate field-degree limit. Proper prime powers have o(π(X)) count, so they do not alter the empirical law. The unconditional theorem is separate from the conditional GRH error refinement mentioned elsewhere.
- `menici-pehlivan-published.pdf`, printed p.255 (1), pp.262–263 (8), Lemma 2 and proof. Set r=m=1: Sm(X)=∑p≤X φ(p−1)/(p−1), Cr,m=∑n μ(n)/(nφ(n))=A, giving the needed mean. The cited proof is explicitly the small/large divisor split and Siegel–Walfisz argument reconstructed above. The fixed-base GRH results in that article's introduction are not inputs to this specialization. Aivazidis–Sofos Theorem 1.1(i), n=1, independently confirms this mean.
- `bcst-v2.pdf`, §2, (5),(6), Lemma 1, printed pp.2–3. For q=p≡3 mod4, Q(t)=t²+1 has no roots, e1=1, e2=N. Their exclusion of t=0 makes the principal term p−1, and Q(0)=1 is not primitive for these odd primes. Thus N(1,N)=Pp and their bound gives the same o(1) interface, although the self-contained argument above has principal term p. This is attribution and a cross-check, not an additional unsupported theorem replacing (A3).
- `vivaldi-owr2004.pdf`, both pages, Conjecture 1 and adjacent scope language. It explicitly uses uniform point weighting and scale p, fixes extension degree, permits a suitable positive-density set, and phrases the existence assertion for any birational map. Genus one appears in the later heuristic. The present example's forward polynomial is defined on every affine point, and on S its inverse is too. Proposition 4 is explicitly convention-dependent, so it does not invent an all-prime full-plane permutation. The later prime-averaged p² statistic is a different conjecture and is outside this result.
- `ostafe-shparlinski-v3.pdf`, §2.1, (1)–(4), printed pp.2–3. Swapping coordinates and setting m=1,a=1,b=0,g0(X1)=X1²+1,h0=0 places this map in that old triangular family. Its degree-growth results are not needed as premises here.

## 7. Mechanisms, evidence, exact gaps

| Family | Falsifiable interface | Evidence | Status / remaining gap |
|---|---|---|---|
| Rational geometry | birational vs polynomial automorphism, invariant genus | explicit compositions, invariant and iterates | supported; no elliptic-fiber conclusion |
| Finite dynamics | point weighting, endpoints, zero multipliers | exact fiber proof, independent repeated orders, weighting witness | supported at stated fixed-x threshold |
| Character algebra | principal term, quadratic exception, coefficient count | self-contained derivation; exact cyclotomic norm controls | supported; not a new character theorem |
| Prime mean / subsequences | uniform divisor range, unconditional mean, CRT | (A6) with tail proof; two raw primary interfaces | supported with standard classical inputs |
| Scalar distribution | actual prime law and continuity | DH Prop.2.1 m=2 and AS Thm.1.3(i) n=1/proof | supported; no absolute continuity or residue-class law needed |
| Density / weak topology | upper density, potential atom of measure limit | interval proof and bounded continuous ramp | supported; zero-density selections deliberately not ruled out |
| Exceptional conventions | arbitrary retained count/assigned period sizes | exact mixture bound uniform in assignments | supported under explicitly retained regular domain and uniform weights |
| Historical priority | authenticated exact prior statement | only source's explicit bounded caveat reviewed here | unresolved 2011 bibliographic lead; no firstness claim certified |

No substantive mathematical defect or unsupported transfer was found in these interfaces. This review does not resolve or erase the acknowledged unseen 2011 preprint, and makes no new historical firstness or worldwide novelty determination.
