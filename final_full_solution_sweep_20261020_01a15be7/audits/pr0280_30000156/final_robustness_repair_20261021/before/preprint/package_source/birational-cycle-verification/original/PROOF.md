# A birational permutation with no prime-by-prime limiting cycle distribution

Target: 30000156 / OWR-768-006. **Turn 1 complete candidate; independent full review required.** No historical novelty is certified.

## Theorem and exact source scope

Consider the fixed rationally invertible polynomial map over Q

    L(u,v) = (u,(u²+1)v),       L⁻¹(u,v) = (u,v/(u²+1)).

For every prime p≡3 (mod 4), its reduction is a permutation of the entire affine plane F_p². Let T_p(u,v) be its least positive period, and use the original point-weighted normalization

    D_p(x) = p⁻² #{(u,v)∈F_p² : T_p(u,v)≤px}.

For **each fixed x with 1/2≤x<1**,

    limsup_(p→∞, p≡3 mod4) D_p(x) = 1,
    liminf_(p→∞, p≡3 mod4) D_p(x) ≤ 23/24.

In particular D_p(3/4) has no limit. The same sequence of maps has no weak limiting distribution of normalized periods: a proposed limiting distribution function could have only countably many discontinuities, whereas convergence fails at every point in this interval.

This answers negatively the literal universal birational-map statement in Vivaldi's Conjecture 1, OWR 54/2004, printed pp.2944–2945. That source explicitly allows a suitable positive-density set of reduction primes, fixes the extension degree, and then takes q=p. The class p≡3 mod4 has prime density 1/2; here both map and inverse are everywhere defined on the finite affine phase space. Thus no undefined orbit, discarded line, transient point, or assignment at infinity enters the counterexample.

The example is algebraically integrable, with I(u,v)=u and genus-zero generic level curves, and has infinite order over Q. The source's universal assertion does not impose polynomial inverse, constant Jacobian, genus-one fibers, or the single-reversing-family condition of its separate refinement. This is not a claim about every narrower reversible-polynomial-automorphism or elliptic-foliation conjecture. The 2009 random-involution theorem is an ensemble-average theorem and does not supply the disputed fixed-map, prime-by-prime conclusion.

## 1. Finite dynamics and an exact counting formula

For p≡3 mod4, −1 is not a square. Thus a_u=u²+1 lies in F_p* for every u. Multiplication by a_u is bijective on every vertical fiber, and its inverse is multiplication by a_u⁻¹. Points (u,0) have period one; for v≠0 the period is exactly ord_p(a_u). All p² points lie on cycles.

Put N=p−1, θ_p=φ(N)/N, and

    P_p = #{u∈F_p : ord_p(u²+1)=N}.

Fix x∈[1/2,1). Every proper divisor of N is at most N/2≤px. For sufficiently large p, N>px. The only excluded cycles therefore have length N, and every parameter u counted by P_p gives exactly p−1 such points. Hence, for all sufficiently large p in the chosen class,

    D_p(x) = 1 − (p−1)P_p/p².                         (1)

This counts points, not cycles. No normalization by the number of vertical fibers or by the number of cycles is substituted.

## 2. Primitive values of u²+1: an elementary character estimate

We prove

    |P_p/p − θ_p| ≤ θ_p(2^ω(N)−1)/√p,                 (2)

where ω counts distinct prime factors. All character statements below concern the cyclic group F_p*, and characters are extended by zero at zero, including the trivial character.

### 2.1 Primitive-element indicator

For a∈F_p*,

    1_(ord(a)=N)
      = θ_p Σ_(d|N) μ(d)/φ(d) Σ_(ord χ=d) χ(a).      (3)

To verify this, choose a generator g and write a=g^k. The inner sum is the Ramanujan sum c_d(k). Terms with nonsquarefree d vanish, and the sum factors as

    θ_p ∏_(ℓ|N) (1−c_ℓ(k)/(ℓ−1)).

For a prime ℓ, c_ℓ(k)=ℓ−1 if ℓ|k and −1 otherwise. The product is zero when gcd(k,N)>1; otherwise it equals θ_p∏ℓ/(ℓ−1)=1. This also proves the coefficient and order conventions in (3).

### 2.2 The required quadratic character sum

Let η be the quadratic character and χ any nontrivial multiplicative character. Counting square roots of t gives

    S_χ := Σ_(u∈F_p) χ(u²+1)
         = Σ_t (1+η(t))χ(t+1)
         = η(−1) J(η,χ),                             (4)

where J(α,β)=Σ_s α(s)β(1−s). The first term Σ_t χ(t+1) vanishes; the substitution t=−s gives the last identity.

For completeness, the needed bound |J(η,χ)|≤√p follows from elementary Gauss-sum identities. For a nontrivial character α and e_p(t)=exp(2πit/p), put G(α)=Σ_t α(t)e_p(t). Substituting t=uy in |G(α)|² and summing first over y≠0 shows

    |G(α)|² = (p−1) − Σ_(u≠0,1) α(u) = p.

If α,β,αβ are nontrivial, decomposing the double sum G(α)G(β) according to z=t+s gives

    G(α)G(β)=J(α,β)G(αβ),

so |J(α,β)|=√p. If β=α⁻¹, the substitution w=s/(1−s) gives J(α,α⁻¹)=−α(−1), of modulus one. Apply this with α=η. Consequently |S_χ| is √p, except for χ=η when it is one. No unproved primitive-root assertion or deep uniform character estimate is being assumed here.

Summing (3) over u, the trivial character contributes exactly p because u²+1 never vanishes. For each d>1 with μ(d)≠0 there are φ(d) characters of exact order d, canceling the denominator φ(d) in the triangle inequality. There are 2^ω(N)−1 such divisors. Equations (3)–(4) prove (2).

For an explicit vanishing error, there are only six primes below 16. For every prime ℓ≥17, 2≤ℓ^(1/4). Thus

    2^ω(N) ≤ 64 N^(1/4),

by separating the prime factors below 16 and using ∏_(ℓ|N)ℓ≤N. It follows from (1)–(2) that

    D_p(x) = 1−θ_p+o(1)                              (5)

along all p≡3 mod4, with the explicit eventual error

    |D_p(x)−(1−θ_p)| ≤ 1/p + 64p^(−1/4).

The rate is deliberately crude. It is enough for every fixed threshold in the stated interval.

## 3. The unconditional mean input

We use the classical unconditional asymptotic

    (1/π(X)) Σ_(p≤X) φ(p−1)/(p−1) → A,
    A = ∏_(ℓ prime) (1−1/(ℓ(ℓ−1))).                 (6)

This is the prime-average totient theorem associated with Stephens's work; it is not Artin's conjecture for a fixed primitive-root base. Full published verification is available in Menici–Pehlivan, *Average r-rank Artin conjecture*, Acta Arith. 174 (2016), pp.255–276: equation (1), and directly Lemma 2 on pp.262–263 with r=m=1. The latter proof is unconditional and invokes Siegel–Walfisz. The original 1969 Stephens full text was not accessed.

Here is the required specialization, to make the analytic dependency and error passage explicit. Möbius inversion gives

    Σ_(p≤X) φ(p−1)/(p−1)
      = Σ_(d≤X−1) μ(d)/d · π(X;1,d).

Take K=(log X)^6. Since π(X;1,d)≤X/d, the tail d>K is O(X/K). The Siegel–Walfisz theorem, uniformly for d≤K, gives

    π(X;1,d)=Li(X)/φ(d)+O_C(X/(log X)^C).

Taking, for example, C=4, its summed error is O(X log K/(log X)^4)=o(X/log X). The series Σ_d 1/(dφ(d)) converges absolutely: the elementary bound φ(d)≥√(d/2) follows by checking the prime-power factors of φ(d)²/d (only the factor at 2¹ can be below one). Thus the truncated coefficient tends to

    Σ_d μ(d)/(dφ(d)) = A

by its absolutely convergent Euler product. Using π(X)∼Li(X) proves (6). This is a restatement of the established mean argument, not a novel analytic-number-theory theorem.

We also use the standard fixed-modulus prime-number theorem in arithmetic progressions, in particular

    π(X;1,4)/π(X)→1/2,   π(X;3,4)/π(X)→1/2,          (7)

and Dirichlet's infinitude theorem in a reduced residue class. These are unconditional. The first assertion in (7) is already a fixed-modulus instance of the same Siegel–Walfisz input; the second follows by subtracting, apart from p=2.

A simple lower bound, sufficient without decimal evaluation, is

    A ≥ 7/24 > 1/4.                                  (8)

Indeed the factor at 2 is 1/2. The sum of 1/(ℓ(ℓ−1)) over odd primes is at most the sum over all integers n≥3 except n=4, namely 1/2−1/12=5/12. For numbers a_i∈[0,1], every finite product ∏(1−a_i)≥1−Σa_i; passage to the decreasing infinite product gives (8).

## 4. Two incompatible subsequences in the same admissible prime class

### 4.1 A subsequence with θ_p→0

Let Q_j be the product of the first j odd primes. The Chinese remainder conditions

    p≡3 (mod 4),       p≡1 (mod Q_j)

define a reduced residue class modulo 4Q_j. Dirichlet's theorem gives infinitely many primes in each class. Choose successively increasing such primes p_j. Every prime factor of 2Q_j then divides p_j−1, so

    0≤θ_(p_j)≤(1/2)∏_(ℓ|Q_j)(1−1/ℓ)→0.

The final convergence is Euler's classical vanishing product over the primes, equivalently divergence of their reciprocal sum. No quantitative least-prime theorem is needed: j is fixed before each infinite progression is used. Equation (5) gives D_(p_j)(x)→1, proving the limsup assertion.

### 4.2 Infinitely many p≡3 mod4 have θ_p≥1/24

For every odd prime p, θ_p≤1/2. If only finitely many primes p≡3 mod4 had θ_p≥1/24, then (7) would imply

    limsup_(X→∞) (1/π(X))Σ_(p≤X) θ_p
      ≤ (1/2)(1/2) + (1/2)(1/24)
      = 13/48.

But (6)–(8) make the limit at least 7/24=14/48. This is a contradiction. Hence an increasing sequence q_j≡3 mod4 satisfies θ_(q_j)≥1/24. Equation (5) yields

    limsup_j D_(q_j)(x)≤23/24,

and therefore the liminf bound in the theorem. This argument extracts a subsequence within the required prime class; a positive average over all primes alone, without the class split, would not justify that step.

Both subsequences are chosen independently of x. Formula (1) eventually applies to each fixed x∈[1/2,1), completing the proof.

## 5. What the result does and does not claim

The literal source uses an unaveraged limit at scale p; it introduces a different prime-averaged statistic at scale p² only for its later Conjecture 2. We do not replace one by the other. The arithmetic mean (6) is solely a proof tool to force one subsequence, not the conclusion requested by the original conjecture.

For p≡3 mod4 the probability space is exactly all p² affine points, and every orbit is periodic. The map is polynomial in the forward direction, with a rational inverse. It is not a polynomial automorphism over C, since the inverse has poles on the two complex lines u=±i. The universal birational source permits rational inverses and almost-everywhere definitions; its finite-field permutation issue is completely removed on the chosen positive-density reduction set. Strengthening the target to a globally polynomial inverse would be a different problem.

The follow-up 2006 elliptic-foliation discussion and the 2009 random-involution model are credited background with their own narrower hypotheses; neither is contradicted here as a proved theorem. The candidate establishes failure of the broad original limit claim, not a classification of all birational cycle distributions. Search did not establish historical novelty, and none is asserted. Finite diagnostics support the formulas only; the two infinite prime subsequences rest on the written unconditional arithmetic argument.
