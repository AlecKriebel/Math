# Genuine indicator phase obstructions and the exact positivity boundary

12 October 2026. Continuation for row 1741 / problem 2350 / Erdős 864.

## Result and limits

This note gives actual indicator examples, rather than signed Fourier-function models. It also gives a quantitative rounding theorem specifying exactly what positivity and near-idempotence do and do not preserve.

1. There are macroscopically uniform, strong Sidon integer sets B in [L], with B disjoint from B+B+B, for which |B|/sqrt(L) tends to 1/sqrt(3) and the signed residual phase tends to **−1/32**. Thus no universal phase lower bound with κ<1/32 is valid even for genuine integer indicators.
2. In the single half-integer coset relevant to the original reflected-core problem, the corresponding examples have |B|/sqrt(L) tending to 1/sqrt(2) and signed residual phase **−1/20**, with the required shifted Fourier phase. Thus κ<1/20 is impossible for a theorem covering both permitted lattices.
3. These negative phases are produced, to leading order, by nonzero rational major arcs. The examples have residual supremum of order sqrt(L); they do not meet the stronger global Fourier-uniformity hypothesis ||R||∞=o(sqrt(L)). Macroscopic uniformity alone allows these arithmetic peaks.
4. A [0,1]-coefficient model with mass and second moment asymptotically equal and with asymptotically Sidon fourth moment can be rounded to an indicator with o(L) fourth-power error, preserving the leading signed phase. This guarantees only an o(L) nontrivial additive-energy defect. The positive support is exactly Sidon if and only if the weighted defect is zero; this condition is sufficient for the rounded set to be exactly Sidon. A zero nonnegative weighted triple count likewise suffices for exact triple avoidance after rounding. Approximate moment matching is not substituted for exact Sidonicity.

The residue-class constructions themselves are elementary and no novelty is claimed. Neither phase −1/32 nor −1/20 reaches −1/14. These results do not disprove the proposed κ=1/14 hypothesis, improve the unrestricted upper constant, or resolve the integer or half-integer symmetric residual problem. The rounding theorem is a positivity/occupancy statement, not another absolute-norm transfer estimate.

## 1. Conventions and the controlling endpoint identities

For an integer set B⊂[L] of cardinality k, write

    F_B(α)=Σ_{b∈B} e(bα),  D_L(α)=Σ_{n=1}^L e(nα),
    G_B(α)=(k/L)D_L(α),   R_B=F_B−G_B,

where e(t)=exp(2πit), and integrate over the probability circle. A strong Sidon set allows repeated entries: a+b=c+d implies equality of the unordered pairs.

The accepted endpoint proof establishes the following under

    L^(−1/2) Σ_{b∈B} δ_{b/L} ⇒ c 1_[0,1](x) dx.        (U)

For k/sqrt(L)→c>0,

    E(R_B):=∫|R_B|⁴=(2c²−(2/3)c⁴+o(1))L,              (1)
    T(B):=#{a+b+c=d in B⁴}
        =(c⁴/6+o(1))L+Re∫R_B³ conjugate(R_B).          (2)

Thus T(B)=0 forces

    Re∫R_B³ conjugate(R_B)/E(R_B)
        → −c²/[4(3−c²)].                                (3)

For a set B in Z+1/2, put A=B+1/2⊂[M], M=L+O(1), define R_A with the integer interval model, and use

    R_B=e(−α/2)R_A.

The signed functional is then ∫e(−α)R_A³ conjugate(R_A). It is periodic, even though R_B is antiperiodic. The forbidden equation in A is a+b+c−d=1. Equations (1)–(3), with L and M asymptotically interchangeable, retain the same constants.

For clarity, the required mixed-term fact is: whenever H_L has fourth moment O(L), H_L(t/L)=o(sqrt(L)) uniformly on each fixed compact t-interval, and G_L is the interval model of mass O(sqrt(L)),

    ∫|G_L|^(4−j)|H_L|^j=o(L),   j=1,2,3.                (4)

On |α|≤K/L use the stated compact convergence. On its complement use Hölder and the bound ∫_{|α|>K/L}|G_L|⁴=O(LK^(−3)); then let K tend to infinity. This argument also works with a unit-modulus half-integer modulation. This is the only endpoint transfer lemma needed below.

## 2. A self-contained near-maximal Sidon family

Let p run through odd primes and set q=p²−1. In the field F_(p²), choose a generator θ of its multiplicative group. In particular θ∉F_p. For each x∈F_p there is a unique exponent s_x modulo q such that

    θ^(s_x)=θ+x.

Let S_p be these p exponents, represented in {1,...,q}. None is zero modulo q, since 1=θ+x would put θ in F_p.

**Lemma 1.** S_p is strong Sidon modulo q, hence is strong Sidon as an integer subset of [q]. Moreover |S_p|=p and its normalized measures converge to uniform measure:

    q^(−1/2) Σ_{s∈S_p} δ_{s/q} ⇒ 1_[0,1](x) dx.         (5)

**Proof of Sidonicity.** If s_x+s_y=s_u+s_v modulo q, then

    (θ+x)(θ+y)=(θ+u)(θ+v).

Subtracting and cancelling θ² gives

    (x+y−u−v)θ+(xy−uv)=0.

Since 1,θ are linearly independent over F_p, the sums and products agree. Thus the monic quadratic polynomials with roots {x,y} and {u,v} agree, including repeated roots. Their unordered root multisets agree, and so do the exponent pairs. The exponents are distinct because θ+x is distinct for distinct x. This is the usual elementary finite-field Sidon construction; it is not presented as new.

**Proof of uniformity, without a Fourier equidistribution theorem.** Here is the general argument for any integer Sidon sequence S⊂[q] with |S|/sqrt(q)→1. Put ν_q=q^(−1/2)Σ_s δ_(s/q). Its nonzero ordered differences are distinct. Consequently

    ν_q*tilde(ν_q)
      =(|S|/q)δ_0+(1/q)Σ_{d≠0} r_S(d)δ_(d/q),

with r_S(d)≤1 for d≠0. Every weak subsequential limit ν therefore satisfies ν*tilde(ν)≤Lebesgue measure. Compact support and bounded masses justify convergence of convolutions.

Let η_ε=ε^(−1)1_[−ε/2,ε/2]. Tonelli gives

    ||ν*η_ε||₂²
      =∫(η_ε*tilde(η_ε))(t)d(ν*tilde(ν))(t)≤1.

Weak compactness in L² and the approximate-identity limit show that ν=f dx, supported on [0,1], with ∫f²≤1. Its mass is one. Cauchy–Schwarz forces f=1 almost everywhere on [0,1]. Every subsequential limit is therefore the same uniform measure, proving convergence of the full sequence. Since p/sqrt(p²−1)→1, this applies to S_p. No finite computation or external equidistribution result is used. ∎

Only elementary finite-field existence and cyclicity of its multiplicative group are used in constructing S_p; the construction, Sidon verification, and uniformity argument are explicit. The seed is the h=2 Bose–Chowla construction; a primary exposition is Melvyn B. Nathanson, [The Bose–Chowla argument for Sidon sets](https://arxiv.org/pdf/2104.12711), Theorem 1, printed page 3. The plus sign used here is equivalent to the source’s minus sign by changing the field parameter.

## 3. Genuine indicator examples on the two permitted lattices

Fix an integer m≥2 and a fixed a∈(1/2)Z with

    m does not divide 2a.                                (6)

Take a≥0 for convenience, and put

    B_p=mS_p+a,       L_p=mq+a.

Its points lie on one of the two permitted unit-lattice cosets. Translation and dilation preserve strong integer Sidonicity. If b₁+b₂+b₃=b₄, then

    m(s₁+s₂+s₃−s₄)+2a=0,

contradicting (6). Thus B_p is triple-sum-free exactly, not only up to an error term.

By (5), its normalized profile is uniform with

    |B_p|/sqrt(L_p)→1/sqrt(m).                            (7)

Indeed b/L_p=s/q+O(1/q) uniformly, and q^(1/2)/L_p^(1/2)→1/sqrt(m). Apply (1)–(3), or their stated half-integer version, to get

    E(R_B)=[2/m−2/(3m²)+o(1)]L_p,
    Re∫R_B³ conjugate(R_B)=[−1/(6m²)+o(1)]L_p,
    phase(R_B)→−1/[4(3m−1)].                              (8)

For integer radii choose m=3,a=1. This gives c²=1/3 and phase −1/32. No integer a satisfies (6) for m=2. Thus m=3 is the smallest dilation usable by this single-residue integer construction, and −1/32 is the most negative phase within that particular family.

For half-integer radii choose m=2,a=1/2. Then B=2S_p+1/2, while A=B+1/2=2S_p+1 consists of odd integers. The equation a+b+c−d=1 in A is impossible because its left side is even. This gives c²=1/2 and phase −1/20, using ∫e(−α)R_A³ conjugate(R_A). This is also the most negative member of the single-residue construction on the two allowed lattice cosets, since m=1 always divides 2a.

The words “most negative” in this paragraph concern only this explicitly parametrized family, not all admissible sets. The affine-residue avoidance principle is established prior methodology: Ortega and Prendiville, [Extremal Sidon Sets are Fourier Uniform, with Applications to Partition Regularity](https://jtnb.centre-mersenne.org/item/10.5802/jtnb.1239.pdf), Proposition 1.13 and Remark 1.14, printed page 118, give this construction principle for homogeneous equations whose coefficients do not sum to zero. The present contribution is its explicit endpoint-phase accounting and the carefully scoped positivity/rounding analysis, without a claim of priority for those analyses either.

## 4. Where the negative phase is located

The examples permit an exact separation between congruence peaks and the smaller-scale residual of the Sidon seed. This distinguishes the genuine arithmetic mechanism from an arbitrary signed-function model.

Write

    U_q(β)=(p/q)D_q(β),    V_q(β)=F_(S_p)(β)−U_q(β),
    H(α)=e(aα)U_q(mα),    K(α)=e(aα)V_q(mα).

Thus F_B=H+K. Let G be the full ambient interval model in the actual unit lattice: for integer a it is (p/L)D_L with an integer endpoint L=mq+a; for half-integer a use M=L+1/2 and G=e(−α/2)(p/M)D_M. Set

    J=H−G,        R_B=J+K.                               (9)

The uniformity in Lemma 1 and (4), applied at scale q, gives

    ∫|U_q|^(4−j)|V_q|^j=o(q),   j=1,2,3.                 (10)

The map α↦mα preserves Haar measure, and modulation preserves magnitudes. Therefore the corresponding mixed H,K terms are o(L). Also K(t/L)=o(sqrt(L)) on each compact t-interval, and ∫|K|⁴=O(L), so the mixed G,K terms are o(L) by (4). The inequality |J|≤|H|+|G| then proves

    ∫|J|^(4−j)|K|^j=o(L),   j=1,2,3.                     (11)

The coefficient profile of H is uniform at macroscopic scale, just as G is, and ∫|H|⁴=O(L). Hence J(t/L)=o(sqrt(L)), ∫|J|⁴=O(L), and all mixed G,J terms are o(L).

For every integrable periodic Z and integer ℓ not divisible by m,

    ∫ e(ℓα) Z(mα)dα=0.                                  (12)

Split the circle into m equal intervals and use the vanishing root-of-unity sum Σ_{j=0}^{m−1}e(ℓj/m). Taking ℓ=2a, (6) and (12) give the **exact**, finite identities

    ∫H³ conjugate(H)=0,      ∫K³ conjugate(K)=0.           (13)

There is no positivity assertion for K here; the cancellation follows from its residue-class modulation.

The seed endpoint theorem at c=1 gives

    ∫|V_q|⁴=(4/3+o(1))q.

The interval identities and (9)–(13) now give

    ∫|K|⁴=[4/(3m)+o(1)]L,
    ∫|J|⁴=[2(m−1)/(3m²)+o(1)]L,
    Re∫J³ conjugate(J)=[−1/(6m²)+o(1)]L.                (14)

For the second and third lines, expand H=G+J. All mixed terms are o(L); ∫|H|⁴=(2/3+o(1))q, ∫|G|⁴=(2/(3m²)+o(1))L, and ∫G³ conjugate(G)=(1/(6m²)+o(1))L. The last identity uses the shifted interval count in the half-integer case. Then use (13). Expanding R_B=J+K with (11) recovers all of (8).

The large values of H occur near α=j/m. At the zero arc, H−G=o(sqrt(L)) on the 1/L scale. The other m−1 arcs remain in J. More explicitly, a fixed scaled coordinate α=(j+t/q)/m gives

    H(α)/sqrt(q)→e(aj/m) h(t),
    h(t)=∫₀¹e(tx)dx.

For j≠0, G(α)/sqrt(q)→0. The signed profile on that arc is multiplied by e(2aj/m). These factors sum to −1 over j=1,...,m−1 because their full sum, including j=0, is zero. This explains the negative sign in (14). Tail bounds for D_q allow passage to the integrals in (14) by first taking L→∞ at a fixed scaled-arc cutoff K, and only then taking K→∞; alternatively the preceding expansion proves the constants without a pointwise arc integration.

At a nonzero rational point j/m,

    F_B(j/m)=e(aj/m)p,       G(j/m)=O(p/L),

with the analogous modulated statement in the half-integer case. Therefore

    |R_B(j/m)|=(1+o(1))p=(1/sqrt(m)+o(1))sqrt(L).         (15)

This explicitly verifies that the examples do **not** contradict a possible phase theorem with the additional global hypothesis ||R_B||∞=o(sqrt(L)). They contradict overly strong phase claims under macroscopic uniformity alone.

## 5. What the desired κ=1/14 assertion really asks for

For a uniform-profile Sidon sequence of limiting mass c, insert (1)–(2) into

    Re∫R³ conjugate(R) ≥ −κ∫|R|⁴+o(L).

At κ=1/14 this is exactly equivalent to the combinatorial supersaturation statement

    T(B) ≥ [c²(3c²−2)/14+o(1)]L.                         (16)

This is an equivalence of asymptotic inequalities under the stated hypotheses, not a proof of either one. Simple coefficient positivity gives T(B)≥0, and therefore only the weaker phase bound

    phase(R) ≥ −c²/[4(3−c²)]+o(1).                        (17)

For c²≤2/3 the right side of (16) is nonpositive, so positivity already gives (16). The unproved content is at c²>2/3. Our integer and half-integer examples have c²=1/3 and 1/2 respectively, strictly below this threshold. They show that strict negative phase is genuine arithmetic, but they do not approach the missing density regime.

## 6. Exact positivity and occupancy identities

Let w=(w₁,...,w_L) be a nonnegative coefficient sequence and F_w=Σ_n w_n e(nα). Define its weighted nontrivial additive defect

    Δ(w)=Σ_{a+b=c+d, {a,b}≠{c,d}} w_a w_b w_c w_d.        (18)

All indices here lie in [L], and unordered pairs include repetitions. Orthogonality gives the exact identity

    ∫|F_w|⁴=2(Σw_n²)²−Σw_n⁴+Δ(w).                      (19)

Every term of Δ(w) is nonnegative. Consequently

    Δ(w)=0  iff  {n:w_n>0} is strong Sidon.              (20)

Likewise, for

    T(w)=∫F_w³ conjugate(F_w)
        =Σ_{a+b+c=d}w_a w_b w_c w_d,

nonnegativity gives

    T(w)=0  iff  supp(w)∩(supp(w)+supp(w)+supp(w))=∅.     (21)

Thus an exact weighted Sidon identity and an exact zero signed count are already exact combinatorial statements about the support. Signed coefficients can evade these equivalences through cancellation; nonnegative coefficients cannot.

An indicator additionally has coefficient idempotence. For p=|B|/L and r_n=1_B(n)−p on [L], write convolution of functions on the circle as ⋆. Since Fourier coefficients multiply under ⋆,

    R⋆R=(1−2p)R+p(1−p)D_L.                              (22)

This follows from r_n²=(1−2p)r_n+p(1−p) at each occupied or unoccupied site. It is a nonlocal Fourier identity, not a scalar second/fourth-moment condition. For real coefficients supported on [L], with the same p, equation (22) conversely forces each r_n to equal −p or 1−p, hence forces indicator occupancy. No claim is made that (22) by itself presently yields (16).

## 7. A quantitative positivity-to-indicator rounding theorem

The following shows how far approximate moments go without silently asserting exact Sidonicity.

**Theorem 2.** Suppose 0≤w_n≤1. Put

    m=Σw_n,          δ=Σw_n(1−w_n),
    A={n:w_n≥1/2},   h=1_A−w.

Then

    ||h||₁≤2δ,          Σh_n²≤δ,                         (23)
    ∫|F_A−F_w|⁴≤2δ²+Δ(w),                              (24)
    Δ(1_A)≤16Δ(w),       T(1_A)≤16T(w).                  (25)

In particular, consider a sequence with

    m/sqrt(L)→c>0,
    δ=o(sqrt(L)),
    ∫|F_w|⁴=2m²+o(L).                                  (26)

Then |A|=m+o(sqrt(L)), Δ(w)=o(L), Δ(1_A)=o(L), and

    ||F_A−F_w||₄=o(L^(1/4)).                             (27)

If the normalized coefficient measures of w have a fixed weak profile, A has the same profile. If R_w and R_A use their respective masses in the same ambient interval model, then

    ||R_A−R_w||₄=o(L^(1/4)),
    ∫|R_A|⁴−∫|R_w|⁴=o(L),
    Re∫R_A³ conjugate(R_A)−Re∫R_w³ conjugate(R_w)=o(L).  (28)

Exact Δ(w)=0 guarantees exact strong Sidonicity of A. Exact T(w)=0 guarantees exact triple avoidance of A. Approximate hypotheses (26) alone guarantee neither exact conclusion.

**Proof.** For 0≤t≤1, rounding at 1/2 gives

    |1_{t≥1/2}−t|≤2t(1−t),
    |1_{t≥1/2}−t|²≤t(1−t),
    |1_{t≥1/2}−t|≤t.

Summing the first two proves (23); the last inequality says |h_n|≤w_n. Decompose the fourth moment of F_h into the trivial additive relations and the nontrivial ones. The former sum to 2(Σh_n²)²−Σh_n⁴≤2δ². After taking absolute values, the latter are bounded by Δ(w), coefficient by coefficient. This proves (24). On A, w_n≥1/2, so 1_A(n)≤2w_n. Multiplying four such inequalities in each nonnegative count proves (25).

Under (26), Σw_n²=m−δ and Σw_n⁴≤m=O(sqrt(L)). Equation (19) gives

    Δ(w)=∫|F_w|⁴−2(m−δ)²+Σw_n⁴=o(L).

Equations (23)–(25) prove the mass and defect conclusions and (27). The total variation of the normalized coefficient measures changes by at most 2δ/sqrt(L)=o(1), proving weak-profile preservation.

The difference of the interval models has fourth moment

    (|A|−m)⁴ L^(−4) ∫|D_L|⁴
      =O((|A|−m)⁴/L)=o(L).

Together with (27), this gives the first line of (28). Both original Fourier transforms have fourth norms O(L^(1/4)), by (26) and (27), and their interval models have the same order. Telescoping the two quartic functionals and applying Hölder gives the other two statements in (28). Exact structural preservation follows either from (25) or directly from A⊂supp(w) and (20)–(21). ∎

The same rounding proof works for the shifted count Σ_{a+b+c−d=1} w_a w_b w_c w_d, and therefore for the half-integer lattice convention. The additive-energy identities and coefficient idempotence remain in the integer gauge A=B+1/2.

## 8. Why approximate energy does not certify exact Sidonicity

There is a simple explicit obstruction to strengthening the last sentence of Theorem 2 without extra work.

Start with the integer example B=3S_p+1 from Section 3. Let x<y be its first two elements and put u=2y−x. Uniformity implies x,y=o(L), so for all sufficiently large p one has 1≤u≤L. Also u>y. Sidonicity of B implies u∉B, since otherwise 2y=x+u would be a nontrivial additive relation in B. Set A=B∪{u}.

Then:

- A is an indicator set and has the same limiting mass and uniform profile as B.
- A is not Sidon, because 2y=x+u.
- All its elements remain 1 modulo 3, so A is exactly triple-sum-free.
- Its additive defect is only O(|B|)=o(L), so ∫|F_A|⁴=2|A|²+o(L).

For the last claim, count new energy quadruples. With exactly one occurrence of u, choose its position (four choices), then a remaining single entry in B (k choices); Sidonicity permits at most two ordered choices for the remaining pair. This gives at most 8k quadruples. With exactly two occurrences of u on opposite sides there are 4k possibilities. On the same side there are at most four possibilities in total. Three occurrences would force the fourth entry to be u and so contribute nothing to the “exactly three” case. Four occurrences contribute one. Thus the total increase in energy is at most 12k+5. Since the old defect was zero and the trivial energy changes by 4k+1, the new defect is at most 8k+4. At least one nontrivial relation exists, as already exhibited.

Approximate hypotheses also fail to certify exact triple avoidance: instead add 3x, where x is the smallest element of B. For large p, 3x≤L by uniformity, and 3x∉B because it is 0 modulo 3. The new set contains x+x+x=3x, while the same one-point energy bound preserves (26) and the limiting profile.

Applying rounding to w=1_A in the first example does nothing at all: δ=0 and the rounded set is A. Thus even exact triple avoidance, exact indicator occupancy, uniform profile, and correct leading Sidon energy do not let one label the rounded set “Sidon.” This example is repaired by deleting one point; it is not a claim that no o(sqrt(L))-deletion repair theorem could hold. Such a theorem is neither proved nor used here.

## 9. Separation from the earlier signed polynomial model

The accepted signed-polynomial model has, at frequency 3, coefficient

    (b+o(1))L^(1/4),   b<0,

where b²=y>0 is fixed. This form covers both the unperturbed construction and its exact-zero perturbation. For any nonnegative-coefficient polynomial P_L, its frequency-3 coefficient differs from this by at least (|b|+o(1))L^(1/4). The magnitude of any Fourier coefficient is at most the L⁴ norm, by Hölder. Hence

    ||P_L−F_L||₄⁴≥(b⁴+o(1))L=(y²+o(1))L.               (29)

In particular it cannot be rounded to a nonnegative or indicator model with o(L) fourth-power error. The obstruction is quantitative, not merely a statement that one coefficient has the wrong sign. This does not prohibit an entirely different positive construction.

## 10. Verification and remaining question

The accompanying diagnostic constructs finite-field seeds independently from the displayed asymptotic argument, verifies their modular and integer Sidonicity, forms both integer and half-integer examples, and computes finite residual quartic coefficients by exact rational convolution. It also tests the rounding inequalities with a separate direct four-index implementation on short rational coefficient sequences, and checks the near-Sidon non-Sidon example. These are diagnostics of identities, not an asymptotic extrapolation.

The controlling accepted Fourier endpoint packet and reflected-core/continuum/modular packet were read before this continuation. The present proof supplies its own finite-field construction and uniform-profile argument. A bounded literature query was exploratory. The two primary PDFs cited above were freshly inspected on 12 October 2026 to identify the established Bose–Chowla and affine-residue construction methods. The uniform-profile claim is proved in Section 2 rather than imported from a rate-sensitive Fourier theorem. No PDF byte hash, novelty, or exhaustive-status claim is made.

What remains is a quantitative arithmetic supersaturation theorem such as (16) in the regime c²>2/3, or a counterexample in that regime. Positivity alone makes the relevant counts nonnegative; exact indicator occupancy supplies (22); exact weighted Sidon energy supplies (20). None of the arguments here converts those facts into (16). Nonuniform profiles remain a separate issue. No repository, publication, or queue change was made.

## Public edition notice

The preceding text is the complete accepted historical proof or audit, with only the locator edits recorded in [EDITION_MAP.md](EDITION_MAP.md). Statements about accompanying diagnostic programs, original input records, or the absence of publication describe the original research or review stage. This prose-only edition distributes no executable program, detailed diagnostic collection, source PDF or image, or private record. Original and accepted file identities are recorded in [INPUT_PINS.json](INPUT_PINS.json); public-file identities are recorded in [MANIFEST.json](MANIFEST.json). [VERIFICATION.json](VERIFICATION.json) distinguishes exact finite checks, floating-point diagnostics, and integrity checks. This notice changes no mathematical argument, verdict, or hypothesis.
