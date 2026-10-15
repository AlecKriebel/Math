# Independent audit: the fourth-order Sidon Fourier endpoint

Audit date: 12 October 2026 UTC. Target: row 1741 / Erdős 864.

## Verdict and exact scope

**MATHEMATICAL PASS, with the explicit single-coset convention for the half-integer extension.** The frozen note correctly proves the uniform-profile mixed-term lemma, the residual fourth-moment asymptotic, the signed-count decomposition, the conditional phase threshold, and both norm-only countermodels. No mathematical change to those formulas is required. Its near-perfect modular conclusion is valid under the strong modular Sidon hypothesis it explicitly invokes.

For the half-integer paragraph, read “half-integers” as the single coset Z+1/2. This is the reflected-radius setting and is the exact hypothesis under which A=B+1/2 is integral. A later standalone version should say that explicitly. The unchanged constants are not asserted for arbitrary mixed subsets of (1/2)Z. This is a scope clarification, not a factor-of-two correction to the intended theorem.

This audit accepts only the stated partial analytic conclusions. It does not accept an unconditional phase estimate, a nonnegative-coefficient or indicator counterexample, a sharper unrestricted interval upper bound, a resolution of Erdős 864, or a novelty claim. The public edition preserves this limited mathematical verdict.

## Artifact identity and independence

The entire final proof was read, including its half-integer extension and signed polynomial countermodel:

- Original authored proof: 17,396 bytes, SHA-256 `fb9e4d462e8edf70b55442b4950ca5f60aad6961998039ac99e4b4b8ab97b29c`.
- Original proof freeze record: 1,455 bytes, SHA-256 `229ea1e9704737a9f607212d4e8de85dd5454e76aa7b5891d399ff41474f7b48`.

The observed proof pin agrees with the author's freeze and the recorded final pin. The author's diagnostic program was hashed only as opaque bytes; it was not inspected, imported, or executed. Author diagnostic outputs were also only hashed. A fresh independent diagnostic program was written from the mathematical definitions. All source-file observations were recorded during the original audit; this edition supplies [input identities](INPUT_PINS.json) and [aggregate verification metadata](VERIFICATION.json).

The accepted continuum proof and audit were read for normalization, as were the modular carry proof and its audit. Their original identities are pinned separately in [INPUT_PINS.json](INPUT_PINS.json). The arguments needed here are reconstructed below, so the present audit does not merely inherit their conclusions.

## 1. Definitions and exact moment identities

The Sidon convention is strong: unordered pairs include repeated entries, and every unordered pair has a distinct sum. Let B lie in {1,...,L}, k=|B|, F=sum over B of e(b alpha), G=(k/L)D_L, and R=F-G. Integrals use Haar probability measure; e(t)=exp(2 pi i t).

Orthogonality gives integral |F|²=k. An unordered diagonal pair contributes one ordered pair and each unordered off-diagonal pair contributes two. Consequently the energy is k+4 binom(k,2)=2k²-k. Parseval applied to the real coefficients 1_B-k/L gives integral |R|²=k-k²/L exactly. There is no omitted diagonal correction.

The constant Fourier coefficient of F³ conjugate(F) is the number of ordered quadruples with a+b+c=d, including repetitions. Its integral is real. More generally, multiplying by e(-v alpha) selects exactly a+b+c-d=v; the sign is correct.

For the interval, the ordered pair-sum multiplicities are 1,2,...,L-1,L,L-1,...,1. Their squared sum is (2L³+L)/3. Positive ordered triples with sum at most L are counted by binom(L,3), giving the stated dense-model signed moment. Multiplication by (k/L)^4 is consistent in both formulas.

## 2. Weak uniformity really suffices for the mixed terms

Write nu_L=L^(-1/2) sum over B of delta_(b/L). Under (U), nu_L converges to c times Lebesgue measure on [0,1]. At each fixed real t,

    F(t/L)/sqrt(L) -> c integral_0^1 e(tx) dx.

Also G(t/L)/sqrt(L) has the same limit, by an ordinary Riemann sum and k/sqrt(L)->c. The t-derivatives of both normalized expressions are bounded in absolute value by 2 pi k/sqrt(L), hence by one constant along the sequence. A finite mesh on [-K,K] therefore upgrades pointwise convergence to uniform convergence for every fixed K. In particular the supremum of |R(t/L)| there is o_K(sqrt(L)). No estimate at frequencies growing with L has been inferred from weak convergence.

The energy identity and the explicit dense energy show that both F and G have fourth norm O(L^(1/4)). The triangle inequality gives integral |R|^4=O(L) before any expansion is used. Thus there is no circular use of the desired residual asymptotic.

On the major arc ||alpha||<=K/L, the product |G|^(4-j)|R|^j is at most C epsilon_K(L)^j L², where epsilon_K(L)->0. Multiplication by its length 2K/L gives o_K(L).

Outside that arc, the geometric-series inequality |D_L(alpha)|<=min(L,1/(2||alpha||)) yields integral |G|^4<=C L/K³. Hölder then gives

    integral_outer |G|^(4-j)|R|^j <= C L K^(-3(4-j)/4).

For j=1,2,3 the exponent of K is strictly negative. First let L grow for fixed K; then let K grow. This proves o(L) for all three mixed integrals. It does not require choosing an unproved growing major-arc cutoff or establishing microscopic convergence.

The same argument bounds mixed integrals with any extra character e(-v alpha), with exactly the same error bound, because its absolute value is one. Consequently the error is uniform over all integers v, including v depending arbitrarily on L.

## 3. Pure terms, residual energy, and the supremum obstruction

Expanding either |G+R|^4 or (G+R)^3 conjugate(G+R), every nonpure term is bounded by one of the three mixed integrals above. Therefore

    integral |R|^4 = [2c²-(2/3)c^4+o(1)]L,
    T(B) = [c^4/6+o(1)]L + Re integral R³ conjugate(R).

The first coefficient is positive for 0<c<=1. The ordinary Sidon upper constant c<=1 can also be recovered from the continuum argument in the next section. In the signed expansion, the conjugations do not alter the absolute mixed-term bounds; no positivity of the signed functional was assumed.

Since integral |R|^4 <= ||R||_infinity² integral |R|² and integral |R|²=(c+o(1))sqrt(L),

    ||R||_infinity >= [sqrt(2c-(2/3)c³)+o(1)]L^(1/4).

At c=1 the energy coefficient is 4/3 and the supremum coefficient is 2/sqrt(3). The comparison with the main signed term L/6 has ratio eight exactly.

For a telescoping four-factor estimate, remove one R in supremum norm. Hölder bounds the remaining three factors by their third norms. Interpolation gives ||F||_3³ <= ||F||_2 ||F||_4²=O(L^(3/4)); G obeys the same upper bound. Thus the conventional absolute-value estimate is C||R||_infinity L^(3/4). To certify an o(L) error from this estimate alone would require the impossible o(L^(1/4)) residual bound. This is a failure of that estimate to certify transfer, not a claim that the actual signed error can never be o(L) or that every Fourier method fails.

## 4. Near-maximal Sidon sets have the required profile

The normalization in the accepted continuum note is exactly nu_L above, with positive-radius interval length L. For ordinary Sidon sets, distinct positive differences alone imply that the nonzero part of nu_L*tilde(nu_L) is bounded by the lattice Riemann-sum measure on [-1,1]. The diagonal mass is k/L=o(1). Any subsequential weak limit nu therefore satisfies nu*tilde(nu)<=Lebesgue measure. Triple-sum avoidance is not needed.

For eta_epsilon=epsilon^(-1) 1_[-epsilon/2,epsilon/2], Tonelli and this domination imply ||nu*eta_epsilon||_2²<=1. Weak compactness in L² and the approximate-identity limit identify nu=f dx with f supported on [0,1], nonnegative, and integral f²<=1. Thus its mass c is at most one by Cauchy-Schwarz. If c=1, equality forces f=1 almost everywhere.

Compact support gives subsequential compactness; every subsequential limit of a near-maximal sequence has mass one and is this same uniform measure. Hence the full sequence satisfies (U). The earlier continuum note assumed triple avoidance for its additional packing inequality, but this part of its proof uses only difference uniqueness and remains valid for every ordinary strong Sidon sequence. This checks the potentially important hypothesis distinction.

## 5. Signed phase and the conditional threshold

For large L, E_R=integral |R|^4 is positive. The identity R³ conjugate(R)=|R|^4 exp(2i theta) shows that Psi is the |R|^4-weighted average of cos(2 theta). Its universal scalar range is [-1,1].

If T(B)=0, division of the signed asymptotic by the residual energy gives

    Psi -> -c²/[4(3-c²)].

This equals -1/8 at c=1. If Re integral R³ conjugate(R)>=-kappa E_R+o(L), the same expansion gives

    0 >= c^4/6-kappa(2c²-(2/3)c^4).

Dividing by c²>0 and rearranging yields c²(1+4kappa)<=12kappa. Both the inequality direction and the denominator are correct. At c²=2/3 the equality value of kappa is 1/14. Any fixed kappa<1/8 excludes c=1 under the stated hypotheses. For kappa=0 the hypotheses allow no c>0, as the formula correctly implies.

The threshold is sharp for this algebraic conditional argument. It is not asserted to be an established Sidon inequality or an optimal arithmetic theorem. Nor can a hypothesis only on the uniform subclass be used to conclude the conjecture for nonuniform profiles.

## 6. Carry coefficients and the half-integer phase

T_0([L])=binom(L,3). For the upper carry, the reflection n->L+1-n sends a+b+c-d to 2(L+1)-(a+b+c-d). Thus T_(2L)([L])=T_2([L])=binom(L+2,3): positive triples of sum at most L+2 give the last count, and no coordinate can exceed L when the triple sum is at most L+2.

For each ordered (a,b,c) in [L]^3, there is a unique d in [L] congruent to a+b+c modulo L. The expression a+b+c-d lies strictly between -L and 3L, so exactly carries 0,L,2L can occur. Therefore their counts sum to L³, which leaves T_L([L])=(2L³-2L)/3. These formulas include L=1 and L=2.

In the strong modular Sidon setting, put h=L-1-k(k-1). The exact identity is R_mod=k²-sum_holes r(u)+(k-1)r(0), with 0<=r(u)<=2. When k/sqrt(L)->1, h=o(L), the hole term is o(L), and the zero correction is O(k)=o(L). Thus R_mod=(1+o(1))L, not merely a lower bound. Representatives in [L] have distinct residues automatically, so the carry partition is injective. Since the interval-model carries sum to k^4/L=(1+o(1))L, the three residual coefficients sum to o(L). If zero carry is absent, its residual coefficient is -L/6+o(L), and the other two sum to +L/6+o(L). Nothing in this accounting rules out that bias.

For the half-integer extension, assume B is in the single coset Z+1/2. Taking A=B+1/2 puts it in [M], M=L+O(1), and

    a+b+c=d in B iff a'+b'+c'-d'=1 in A.

The interval count T_1([M]) is binom(M+1,3), so the leading coefficient remains 1/6. If R_B=e(-alpha/2)R_A, magnitudes are unchanged and R_B³ conjugate(R_B)=e(-alpha)R_A³ conjugate(R_A). The residual is antiperiodic but this quartic expression is periodic. Its phase average is well-defined on a full period, and the same moment and threshold constants follow. This independently checks the phase sign and eliminates a spurious factor-of-two loss. The shift is not integral for a mixed subset of (1/2)Z, which is why the single-coset convention must remain explicit.

## 7. The measurable-function countermodel

E has measure 3/4, is symmetric, and stays distance at least 1/8 from zero. With a=2/sqrt(3), R=a L^(1/4)1_E exp(i theta sign(alpha)), its squared and fourth absolute moments are sqrt(L) and (4/3)L. The signed fourth moment is (4/3)L cos(2theta). Conjugate symmetry follows by reflection; the possible ambiguity at the circle endpoint is a measure-zero issue that the author's convention removes. R vanishes at zero, so F(0)=sqrt(L).

On E, |G|=O(L^(-1/2)). A mixed quartic with j R factors is O(L^(3j/4-2)); the largest is O(L^(1/4)) at j=3. The second-moment cross term is O(L^(-1/4)). Pure dense terms give integral |G|²=1, integral |G|^4=(2/3)L+O(L^(-1)), and T(G)=L/6+O(1). Thus all errors in (19) have the stated order, uniformly in theta.

The signed functional is real by conjugate symmetry and continuous in theta by its explicit finite expansion. At theta=0 its leading coefficient is 3/2; at theta=pi/2 it is -7/6. Uniform smaller errors guarantee opposite signs for large L. IVT produces an exact zero and then cos(2theta_L)=-1/8+O(L^(-3/4)). No numerical root choice is being used as an existence proof.

This model matches leading moments, not the exact indicator identities. Its residual second moment differs by order one from the k=sqrt(L) indicator value, and its total fourth moment need not match the lower-order -sqrt(L) term in 2k²-k. The proof explicitly makes only the leading-order claim. Its value at zero, conjugate symmetry, and strong relative supremum uniformity do not turn it into an indicator Fourier transform.

## 8. The real-coefficient polynomial countermodel

At x=4/5 and x=81/100, direct exact rational evaluation gives the two displayed opposite-sign values. For the entire interval, y>0 and

    z >= 1-81/100-1/[36(4/5)^3] > 0.

Continuity therefore provides an admissible root. With a=sqrt(x), b=-sqrt(y), d=sqrt(z), one has a²+b²+d²=1 and a³b=-sqrt(x³y)=-1/6. The six pair sums of {1,3,10} are 2,4,6,11,13,20, all different. The sole triple-to-single relation is 1+1+1=3. Consequently

    integral |P|^4 = 2(a²+b²+d²)²-(a^4+b^4+d^4)=4/3,
    integral P³ conjugate(P)=a³b=-1/6.

For F=qD_L+sP, where s=L^(1/4) and q=L^(-1/2)-P(0)L^(-3/4), every coefficient is real and its support is in [L] for L>=10. At zero, qL+sP(0)=sqrt(L) exactly. Relative to G, R=sP-P(0)L^(-3/4)D_L, so its supremum is O(L^(1/4)). The negative frequency-3 coefficient is bL^(1/4)+O(L^(-1/2)), genuinely negative for all sufficiently large L.

For completeness, direct bounds justify the leading moments without assuming Sidonicity of the signed coefficient sequence. Its sparse contribution has squared norm sqrt(L), while the dense squared norm is O(1), and the cross term is O(L^(-1/4)). Thus the full squared norm is sqrt(L)+O(1). For any quartic functional, the mixed term with j sparse factors has absolute bound

    O(L^(-2+3j/4) integral |D_L|^(4-j)).

For j=1 this is O(L^(3/4)); for j=2, O(L^(1/2)); for j=3, O(L^(1/4) log L). All are O(L^(3/4)). The dense energy is (2/3)L+O(L^(3/4)); the sparse energy is (4/3)L. Dense signed count is L/6+O(L^(3/4)); sparse signed count is -L/6. This proves (21). For the residual, the dense correction has fourth norm O(1), whereas sP has fourth norm O(L^(1/4)); expansion shows its residual energy is (4/3)L+O(L^(3/4)).

After replacing b by b+delta, with delta in a fixed small interval, all constants above remain uniform. The only pure sparse signed relation is still 1+1+1=3, so its signed moment is L(-1/6+a³delta). The correction to the dense term remains uniformly O(L^(3/4)). Thus the total is a³delta L+O(L^(3/4)), with a>0 fixed. Choose a fixed M greater than the uniform error constant divided by a³. At delta=±M L^(-1/4), the two leading terms dominate with opposite signs for large L. Polynomial continuity in delta supplies an exact root delta_L=O(L^(-1/4)). The perturbation changes the leading normalized moments only by o(1), preserves exact F(0), and preserves the negative coefficient for large L.

This validates the complete IVT perturbation argument, including the uniformity needed before the shrinking bracket is chosen. It establishes a countermodel for scalar leading moments even with real coefficients and support [L]. It does not impose nonnegative coefficients, 0/1 coefficients, or any hidden occupancy/Sidon structure.

## 9. Primary-source applicability and rate check

I independently opened the official [Ortega–Prendiville journal PDF](https://jtnb.centre-mersenne.org/item/10.5802/jtnb.1239.pdf), DOI [10.5802/jtnb.1239](https://doi.org/10.5802/jtnb.1239), on 12 October 2026. Its Fourier convention and probability-circle measure match this note. Theorem 1.2 on printed page 116 has error L^(1/2)(|k/sqrt(L)-1|+L^(-1/6))^(1/2). Theorem 6.3 on printed page 128 replaces the inner L^(-1/6) by L^(-1/4). Hence k/sqrt(L)->1 gives o(sqrt(L)); the stronger cardinality error O(L^(1/4)) gives O(L^(3/8)). Theorem 1.15, beginning on printed page 118 and continuing on 119, requires at least five variables and a nonempty zero-sum coefficient subset. Its direct conclusion does not cover a+b+c=d. These are the only external theorem statements used. No PDF bytes are claimed retained or hashed in this audit, and no exhaustive literature or current global-status claim is made.

## 10. Independent exact diagnostics and limitations

The independent diagnostic program is newly written and does not inspect or execute the author's code. It uses explicit exceptions rather than optimization-removable assertions.

- For every interval length 1 through 160, it checks interval energy, the three carries, their exact total L³, and the shifted half-integer count. Carry counts are separately reconstructed by direct bounded choices of a,b and the allowed d interval.
- It enumerates all 32,766 subsets across [1],...,[14], filters strong Sidonicity by unordered pair sums including diagonals, and checks exact second/fourth moments and residual second moment for every passing subset.
- For each passing subset, it constructs all five coefficients of the energy and signed quartic polynomials in G+tR using integer-scaled coefficients. Their sum is compared with direct four-index enumeration at every carry frequency, and the half-integer shift is separately checked with doubled odd integers.
- It symbolically counts all quartic relations on {1,3,10}, verifies both exact rational root-bracket endpoint values and positivity throughout the interval, and refines a root bracket by 80 exact rational bisections.
- It checks phase-balance/threshold inversion at six exact rational c² values, including 2/3 and 1, and checks the measurable model's moment and IVT endpoint constants.

The normal, Python -O, and Python -OO outputs are byte-identical and report PASS. Detailed counts and exact fractions were recorded in the original diagnostics; [VERIFICATION.json](VERIFICATION.json) retains aggregate counts and output identities. No finite computation is used to infer an asymptotic theorem. Source pins are rechecked on every diagnostic run and after completion.

## Final disposition

Accept the frozen proof as a correct, sharply delimited analytic partial, with the half-integer single-coset interpretation recorded above. No algebraic or asymptotic correction is required. The arithmetic question remains whether the relevant signed phase restriction follows from genuine nonnegative/indicator Sidon occupancy, and how to address nonuniform profiles. The accepted result demonstrates why scalar fourth-moment smallness is unavailable and why scalar norm data alone cannot supply the missing positivity; it does not answer those arithmetic questions.
