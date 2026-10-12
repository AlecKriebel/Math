# Rational-arc escape and the residue-capacity barrier

12 October 2026. Research continuation for problem 2350 / Erdős 864, row 1741.

## Result and exact limits

This note concerns arbitrary strong Sidon sets, not a particular finite-field construction. It proves three results.

1. If a strong Sidon set B⊂[L] occupies s residue classes modulo m, then for every positive integer H,

       |B|² ≤ s(⌈L/m⌉+H−1)(1+(|B|−1)/H).                 (A)

   Consequently a certificate of triple avoidance based solely on forbidden residue classes modulo m=o(√L) forces |B|²≤(1/2+o(1))L. This permits arbitrary unions of classes, not just one affine class, and also covers the shifted equation associated with a single half-integer lattice coset. Actual integer avoidance does not provide such a certificate automatically.

2. Suppose B_L is macroscopically uniform, |B_L|/√L→c, and put x=c². For every fixed modulus, all nonzero rational-arc profile functions together have squared L² norm at most 1−x. Their total signed quartic contribution has absolute value at most

       C₀(1−x)²L,     C₀=3√3/16.                         (B)

   The zero arc contributes x²L/6. Hence any triple-avoiding sequence with x≥2/3 must have signed quartic contribution at most

       −Δ(x)L,    Δ(x)=x²/6−C₀(1−x)²>0,                (C)

   outside the arcs around every fixed denominator, in the precisely specified iterated/subsequential sense below. In particular Δ(2/3)=2/27−√3/48>0, and Δ(1)=1/6. Rational peaks cannot account for all of the necessary negative correlation in this regime.

3. The macroscopic sum/difference packing relaxation remains feasible at mass one even when one retains every fixed residue class for every modulus, with full compatibility under reduction of moduli. Thus that entire residue-resolved weak relaxation still cannot prove the desired mass bound √(2/3).

The signed escape result is an unconditional necessary condition on a hypothetical avoiding sequence; it is not a proof that such a sequence cannot exist. A stated minor-arc signed-decorrelation hypothesis gives an explicit positive supersaturation theorem, but that hypothesis is not established for arbitrary Sidon indicators. No unconditional improvement of the interval constant, resolution of the problem, novelty claim, or publication is made.

## 1. Conventions

Strong Sidon means that a+b=c+d implies equality of the unordered pairs, with repetitions allowed. Let B⊂[L], k=|B|, and

    F_L(α)=Σ_{b∈B}e(bα),       e(t)=exp(2πit).

For a fixed integer v define

    T_v(B)=#{(a,b,c,d)∈B⁴:a+b+c−d=v}
          =∫_T e(−vα)F_L(α)³ conjugate(F_L(α))dα.       (1)

All quadruples are ordered. Integer radii use v=0. For radii in Z+1/2, put A=B+1/2 in [M], where M=L+O(1); the forbidden equation becomes a+b+c−d=1 in A. Apply all results to this integer gauge, with v=1. No dilation by two is used.

The uniform-profile hypothesis is

    L^(−1/2)Σ_{b∈B_L}δ_{b/L} ⇒ c 1_[0,1](t)dt.         (U)

We use the accepted endpoint identities only for interpretation. The new proofs below directly use difference uniqueness, weak convergence, elementary convolution identities, and Cauchy–Schwarz.

## 2. A finite residue-capacity inequality

**Theorem 1.** Let B⊂[L] be strong Sidon, let m≥1, and write k_r=|B∩(r+mZ)| for r=1,...,m. Put N=⌈L/m⌉. For every integer H≥1,

    Σ_r k_r² ≤ (N+H−1)(1+(k−1)/H).                     (2)

If s classes are occupied, (A) follows. Also, by finite Parseval,

    Σ_{j=0}^{m−1}|F_L(j/m)|²
       ≤m(N+H−1)(1+(k−1)/H).                           (3)

**Proof.** For each r map b=r+mt to t+1 and call the resulting subset of [N] C_r. For d>0,

    Σ_r #{(u,w)∈C_r²:u−w=d}≤1,                         (4)

because two such pairs would give two occurrences of the nonzero difference md in B.

On the integers put h_r(n)=Σ_{j=0}^{H−1}1_{C_r}(n−j). Its support lies in [1,N+H−1], and Σ_n h_r(n)=Hk_r. Cauchy–Schwarz for each color r gives

    H²Σ_r k_r²/(N+H−1) ≤ Σ_{r,n}h_r(n)².

The right side equals

    Hk+2Σ_{d=1}^{H−1}(H−d)Σ_r #{(u,w)∈C_r²:u−w=d}
       ≤Hk+H(H−1),

by (4). Division proves (2). The occupied-class Cauchy–Schwarz inequality k²≤sΣ_r k_r² proves (A). Orthogonality in Z/m gives Σ_j|F_L(j/m)|²=mΣ_rk_r², proving (3). ∎

For fixed m and k=O(√L), take H=⌈L^(3/4)⌉. If k/√L→c, (3) yields

    limsup L^(−1)Σ_{j=1}^{m−1}|F_L(j/m)|²≤1−c².         (5)

This is a bound at rational points. Section 4 proves its stronger function-valued version, which is what controls arcs.

**Corollary 2 (congruence-only certificates).** Suppose m=m_L=o(√L), and B_L lies in a set S_L of residue classes modulo m for which

    (S_L+S_L) ∩ (v+S_L−S_L)=∅.                         (6)

Then |B_L|²≤(1/2+o(1))L.

**Proof.** Each of S+S and S−S has cardinality at least s=|S|, so (6) gives 2s≤m. Strong Sidonicity gives k(k−1)/2≤L−1, hence k=O(√L). Thus N=⌈L/m⌉ satisfies k/N→0. For k≥1 choose H=⌈√(Nk)⌉; then H/N→0 and k/H→0. Theorem 1 gives

    k²≤sN(1+o(1))≤(m/2)⌈L/m⌉(1+o(1))
       ≤(1/2+o(1))L.

The empty-set case is immediate. Condition (6) is exactly the absence of a+b+c−d=v in S, with repetitions allowed. ∎

The theorem does not assume the residue set itself is Sidon. It therefore addresses a different regime from the earlier strong-modular-Sidon bound (3k²−k)/2≤q−1. Its asymptotic corollary requires m=o(√L); no assertion for arbitrary growing m is obtained by dropping this condition. The finite inequality remains valid for every m.

## 3. A signed simplex bound

Here Fourier transform on R is ĝ(t)=∫g(u)e(tu)du. Write

    Q(g)=∫_R ĝ(t)³ conjugate(ĝ(t))dt.

**Lemma 3.** If g∈L²(R) is supported on [0,1], then

    |Q(g)|≤C₀||g||₂⁴,           C₀=3√3/16.             (7)

More precisely, if M=∫|g|²>0 and μ=M^(−1)∫u|g(u)|²du, then

    |Q(g)|≤M²√(μ(1−μ)³).                              (8)

No optimality is claimed for C₀.

**Proof.** Compact support puts g in L¹, and ĝ in L²∩L∞, hence in L⁴. Plancherel and convolution give

    Q(g)=∫_{a,b,c≥0; a+b+c≤1}
              g(a)g(b)g(c)conjugate(g(a+b+c)) da db dc.

This identity can also first be verified for bounded functions and then obtained by L² approximation, using Young's inequality for the triple convolution. Put h=|g|. Applying Cauchy–Schwarz on this three-dimensional simplex, with factors h(a)h(b) and h(c)h(a+b+c), bounds |Q(g)|² by I₁I₂, where

    I₁=∫_{a+b≤1}(1−a−b)h(a)²h(b)² da db,
    I₂=∫_{0≤c≤d≤1}(d−c)h(c)²h(d)² dc dd.

The second identity follows by using d=a+b+c and integrating a over [0,d−c]. If X,Y are independent with probability density h²/M, then

    I₁/M²=E(1−X−Y)_+ ≤E[(1−X)(1−Y)]=(1−μ)²,
    I₂/M²=E(Y−X)_+ =½E|Y−X|≤μ(1−μ).

For the last inequality use |x−y|≤x+y−2xy on [0,1]². Thus |Q(g)|²≤M⁴μ(1−μ)³, proving (8). The maximum of μ(1−μ)³ on [0,1] is 27/256, at μ=1/4. Taking square roots gives (7). The case M=0 is trivial. ∎

For the constant function g=c1_[0,1], its actual signed integral is c⁴/6, since the three-dimensional simplex has volume 1/6.

## 4. Joint residue-profile capacity

Fix m. Passing to a subsequence when necessary, all m nonnegative measures

    ν_{L,r}=L^(−1/2)Σ_{b∈B_L; b≡r (mod m)}δ_{b/L}

converge weakly to measures ν_r supported on [0,1]. Their masses are bounded by k/√L.

**Lemma 4.** Each ν_r has a nonnegative L² density f_r, and

    Σ_r||f_r||₂²≤1/m.                                  (9)

Under (U), Σ_rf_r=c1_[0,1]. Define

    g_j(u)=Σ_{r=0}^{m−1}e(jr/m)f_r(u),   0≤j<m.

Then

    g_0=c1_[0,1],
    Σ_{j=1}^{m−1}||g_j||₂²≤1−c².                       (10)

**Proof.** Nonzero differences within the same residue class are multiples of m and occur at most once across all r. Hence

    Σ_rν_{L,r}*tilde(ν_{L,r})
      ≤(k/L)δ_0+(1/L)Σ_{d∈mZ; 0<|d|<L}δ_{d/L}.

Taking weak limits gives Σ_rν_r*tilde(ν_r)≤(1/m)λ. For η_ε=ε^(−1)1_[−ε/2,ε/2], Tonelli implies

    Σ_r||ν_r*η_ε||₂²≤1/m.

Weak compactness in the finite direct sum of L² spaces and the approximate-identity limit identify the ν_r as f_rdu and prove (9). Under (U) their sum is cdu on [0,1]. Finite Parseval pointwise in u, followed by integration, gives

    Σ_j||g_j||₂²=mΣ_r||f_r||₂²≤1.

The j=0 term is c². Subtract it to get (10). In particular c≤1. ∎

The densities f_r need not be constant. This proof does not assume uniformity separately inside residue classes and does not infer a global Fourier supremum bound from (U).

## 5. Rational-arc escape theorem

For fixed m,K and large L define disjoint arcs

    M_{m,K,L}=⋃_{j=0}^{m−1}{α∈T:||α−j/m||_T≤K/L}.

Work along a subsequence having the residue-profile limits of Lemma 4. Then, uniformly for t in each fixed compact interval,

    F_L(j/m+t/L)/√L → ĝ_j(t).                           (11)

This follows by weak convergence and a uniform Lipschitz bound in t. Multiplying by e(−vα) adds the limiting factor e(−vj/m).

Consequently the iterated major-arc limit exists and equals

    A_{m,v}:=lim_{K→∞}lim_{L→∞} L^(−1)
       Re∫_{M_{m,K,L}}e(−vα)F_L³ conjugate(F_L)dα
      =ReΣ_{j=0}^{m−1}e(−vj/m)Q(g_j).                   (12)

For fixed K, (11) proves the equality with integrals over [−K,K]. Then take K→∞: each ĝ_j lies in L⁴ by Lemma 3, and the sum has only m terms. No assertion for an arbitrary cutoff K=K(L) is being used.

By Lemmas 3 and 4,

    |ReΣ_{j=1}^{m−1}e(−vj/m)Q(g_j)|
       ≤C₀Σ_{j=1}^{m−1}||g_j||₂⁴
       ≤C₀(Σ_{j=1}^{m−1}||g_j||₂²)²
       ≤C₀(1−c²)².                                    (13)

The j=0 term is c⁴/6. Thus, writing x=c²,

    A_{m,v}≥Δ(x)=x²/6−C₀(1−x)².                       (14)

**Theorem 5 (escape).** If (U) holds and T_v(B_L)=0, then for every fixed m, along every subsequence admitting residue-profile limits,

    lim_{K→∞}lim_{L→∞} L^(−1)
      Re∫_{T\M_{m,K,L}}e(−vα)F_L³ conjugate(F_L)dα
        =−A_{m,v}≤−Δ(c²).                              (15)

In particular this is strictly negative for c²≥2/3, with magnitude at least 2/27−√3/48. For c=1 it is exactly −1/6, since all g_j for j≠0 vanish.

**Proof.** Subtract the major arcs from the exact zero identity (1), then use (12)–(14). On [0,1], Δ is increasing because Δ'(x)=x/3+2C₀(1−x)>0. At x=2/3,

    Δ(2/3)=2/27−√3/48>0;

for instance positivity is equivalent to 96>27√3, whose squares are 9216>2187. ∎

Take m to be the least common multiple of 1,...,Q to include every reduced rational with denominator at most Q. A diagonal subsequence gives compatible residue profiles for every fixed modulus. Thus a hypothetical high-density avoiding sequence must retain a negative signed contribution outside every fixed-denominator family of 1/L-scale arcs. That contribution can lie at irrational centers, at rational denominators growing with L, or at offsets t/L with |t| escaping every fixed cutoff. The theorem does not distinguish these possibilities or assert one specific mechanism.

The same conclusion holds with the endpoint residual R=F−(k/L)D_L in place of F on the complement after the iterated limit: the interval-model fourth-energy tail outside the zero arc is O(LK^(−3)), while ∫|F|⁴ and ∫|R|⁴ are O(L). Hölder controls every term in the quartic difference. At nonzero fixed rational arcs the interval model is o(√L), and at the zero arc the residual limit is zero. Hence (13) genuinely bounds the fixed-rational part of the residual's signed phase.

### An explicit sufficient signed-decorrelation hypothesis

More generally suppose T_v(B_L)/L→τ along the residue-profile subsequence. This can always be arranged by further extraction because |T_v(B_L)|≤∫|F_L|⁴=2k²−k=O(L). If, for some fixed m and η≥0,

    lim_{K→∞}lim_{L→∞} L^(−1)
       Re∫_{T\M_{m,K,L}}e(−vα)F_L³ conjugate(F_L)dα≥−η, (H)

then

    τ≥Δ(c²)−η.                                         (16)

In particular η=0 gives positive supersaturation for

    c² > ρ:=√(6C₀)/(1+√(6C₀)) < 2/3.

For c²∈[2/3,1], Δ(c²) is strictly larger than c²(3c²−2)/14, the target supersaturation coefficient from the accepted endpoint identity. To check this, their difference is

    x(3−x)/21−C₀(1−x)².

This quadratic is concave, and is positive at both endpoints x=2/3 and x=1. Therefore (H) with η=0 is an explicit sufficient additional hypothesis for more than the desired bound in this subclass.

Hypothesis (H) is a condition on signed fourth-order phase, not on the Fourier supremum or on absolute fourth-energy concentration. It has not been proved for arbitrary Sidon sets. It is included to state exactly which positive result the unconditional rational estimate supports, not to repackage it as an unconditional theorem. In particular it cannot be inferred from ||R||∞=o(√L).

## 6. Every fixed residue refinement of the packing relaxation still allows mass one

For an actual triple-avoiding strong Sidon integer set, positive difference occupancies and unordered-sum occupancies are disjoint. Retaining only those sites in residue class s modulo m, and passing to the weak limits above, yields, for t>0,

    D_{m,s}(t)+½S_{m,s+v}(t)≤1/m,                       (17)

where

    D_{m,s}=Σ_r f_{r+s}*tilde(f_r),
    S_{m,s}=Σ_r f_r*f_{s−r}.

It also yields D_{m,s}≤1/m on the whole real line. The shift in (17) follows from a+b=v+(d−c). For v=0 this is the usual positive sum/difference packing. For fixed v≠0, sums are sampled at n+v while differences are sampled at n; the macroscopic shift v/L vanishes. The possible finitely many boundary sites do not affect the weak limit. Diagonal unordered sums have total normalized mass O(k/L)=o(1).

These are necessary relaxed inequalities, not the assertion that the limiting densities have disjoint supports.

**Proposition 6 (compatible residue barrier).** For every c≤1 the choice

    f_{m,r}(u)=(c/m)1_[0,1](u),    all m≥1, all r∈Z/m,  (18)

satisfies every inequality (9), (17), and D_{m,s}≤1/m, and is compatible under reduction of moduli. It has total mass c; at c=1 it attains the largest mass permitted by the ordinary difference relaxation.

**Proof.** When d divides m, summing the m/d densities whose residues reduce to r gives (c/d)1_[0,1], establishing compatibility. Also

    Σ_r||f_{m,r}||₂²=c²/m≤1/m,
    D_{m,s}(t)=(c²/m)(1−|t|)_+,
    S_{m,s}(t)=(c²/m)(1_[0,1]*1_[0,1])(t).

For 0<t<2 the left side of (17) is (c²/m)(1−t/2), and it is zero for t>2. Thus it is at most 1/m, independently of s or v. The difference inequality is immediate. The ordinary m=1 difference relaxation forces an L² density of norm at most one supported on [0,1], hence total mass at most one by Cauchy–Schwarz. ∎

Equivalently, the product of the uniform interval measure and the compatible uniform measures on all finite cyclic quotients is feasible for this entire hierarchy. No existence of integer sets realizing that product with the exact microscopic disjointness is asserted. The conclusion is only that adding every fixed residue refinement to this weak packing relaxation still cannot rule out mass one.

## 7. Why this does not make a modular-carry transfer

There are three different objects:

- A residue-support certificate, condition (6), excludes the congruence for every selection of occupied classes. Corollary 2 applies to this strong hypothesis.
- The rational-arc integrals are local Fourier limits, keeping macroscopic spatial profiles. They are not the finite count of congruent quadruples modulo m.
- The actual integer count is one Fourier coefficient, T_v(B). Congruent quadruples include all carries v+jm, and integer avoidance removes only the j=0 coefficient.

The earlier exact modular-carry identity explicitly permits nonzero carries to bear all modular coincidences. Nothing here removes that permission. In particular neither (17) nor coarse positivity of the residue profiles can identify which microscopic sum/difference sites coincide.

The accepted affine residue examples have c²=1/3 (integer) and c²=1/2 (half-integer); Corollary 2 is compatible with both. Their rational peaks account for the signed phase. Theorem 5 explains why that explanation cannot simply persist to c²>2/3, regardless of how the finitely many residue profiles are chosen. A new mechanism or a genuinely microscopic estimate is still needed.

## 8. Sources, diagnostic scope, and residual

The controlling accepted indicator-phase proof, its independent audit, the accepted Fourier endpoint proof and acceptance statement, and the earlier modular-carry and continuum-barrier proofs were read. Their public mathematical editions are linked in DEPENDENCIES.md. This note supplies complete proofs of its new statements; no source theorem is imported to supply the missing signed estimate.

A fresh inspection of Ortega and Prendiville, “Extremal Sidon Sets are Fourier Uniform, with Applications to Partition Regularity,” Journal de Théorie des Nombres de Bordeaux 35 (2023), 115–134, official PDF https://jtnb.centre-mersenne.org/item/10.5802/jtnb.1239.pdf, confirmed the established background of extremal Sidon equidistribution in residue classes and Bohr neighborhoods (Corollaries 1.6–1.7). This manuscript does not claim that residue equidistribution itself is new. The source's partition-regularity application has at least five variables and supplies no missing four-variable bound here. Only this attribution/applicability statement is drawn from that source. The PDF was inspected through the web tool; no retained PDF byte hash is claimed.

The accompanying independently authored-from-definitions checker exhausts short integer Sidon sets and finite residue supports, tests the exact window identity and inequalities, checks the simplex identities using rational cell integrals, and verifies the compatible-profile and constant calculations by exact arithmetic. Finite diagnostics do not prove the asymptotic passage; the proofs above do. No remote state, publication, queue entry, or existing accepted proof was changed.

The precise open issue remains the negative signed contribution outside every fixed rational-arc family. Theorem 5 locates a necessary amount of it. It does not bound it from below, construct it for an indicator, or settle the nonuniform-profile case.


## Public editorial notice

All mathematical statements, proofs, examples, substantive audit arguments and scope limitations are retained. EDITION_NOTES.md describes the nonmathematical editorial changes: updated acceptance history, public dependency links and removal of excluded provenance metadata. The distributed edition is identified by MANIFEST.json. The complete one-vertex dependency and its audits are linked in DEPENDENCIES.md. Diagnostic summaries report checks rather than replacing mathematical proof. Independent internal AI acceptance is not external human peer review or proof-assistant certification.
