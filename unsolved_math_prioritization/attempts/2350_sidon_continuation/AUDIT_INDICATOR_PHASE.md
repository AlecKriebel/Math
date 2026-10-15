# Independent audit: genuine Sidon indicators, residue phases, and nonnegative rounding

Audit date: 12 October 2026 UTC. Target: row 1741 / problem 2350 / Erdős 864.

## Verdict and scope

MATHEMATICAL PASS for the frozen proof identified in the original indicator proof identity recorded in INPUT_PINS.json, after two clarifications requested during independent review and incorporated before freezing. The accepted conclusions are actual uniform-profile strong Sidon, triple-avoiding indicator sequences with integer phase −1/32 and single-coset half-integer phase −1/20; an exact rational-frequency decomposition locating their leading negative phase; the stated quantitative rounding inequalities and their approximate versus exact preservation boundary; and the L⁴ separation of the earlier signed polynomial from every nonnegative coefficient model.

Neither construction refutes κ=1/14. Neither has globally small Fourier residual. The proposed κ=1/14 inequality is equivalent, under the existing uniform-profile hypotheses, to a positive supersaturation estimate only in the regime c²>2/3. That regime is not reached here. No resolution of the original interval problem, unrestricted upper-constant improvement, global novelty, or priority claim is accepted. This is an independent internal AI mathematical audit of an AI-assisted, unrefereed manuscript, not human peer review or formal proof certification.

The proof and the controlling endpoint proof and audit were read in full. The author's diagnostic program was neither inspected nor executed; only its bytes were hashed for input identity. The audit diagnostics were independently written from the mathematical definitions.

## 1. Normalization and exact moment checks

The Fourier transform is the unnormalized sum F_B(α)=Σ_{b∈B}e(bα), with probability Haar integral on R/Z. Strong Sidonicity includes equal-entry pairs. Orthogonality gives

- ∫|F_B|²=k;
- ∫|F_B|⁴=k+4 binom(k,2)=2k²−k;
- for G=(k/L)D_L and R=F_B−G, ∫|R|²=k−k²/L;
- ∫F_B³ conjugate(F_B)e(−vα)=#{(a,b,c,d)∈B⁴:a+b+c−d=v}.

The sign in the character is important and is correct. The ordered interval pair multiplicities give ∫|D_L|⁴=(2L³+L)/3. For shift zero the ordered triple-to-single count is binom(L,3); for shift one it is binom(L+1,3). Repetitions are counted throughout.

For completeness the controlling mixed-term statement uses no microscopic convergence assumption. Macroscopic weak uniformity yields R(t/L)=o(sqrt(L)) uniformly on each fixed compact t-interval by a uniform derivative bound and a finite mesh. Sidon energy and the dense interval energy first give ∫|R|⁴=O(L), without assuming the desired asymptotic. On the fixed major arc of width K/L, each mixed quartic is o_K(L). Outside it, the fourth energy of G is O(LK^(−3)); Hölder gives O(LK^(−3(4−j)/4)) for j residual factors. First take L→∞ and then K→∞. Expanding the two quartics gives

    E_R=[2c²−(2/3)c⁴+o(1)]L,
    T(B)=[c⁴/6+o(1)]L+Re∫R³ conjugate(R).

Multiplication by a unit character leaves all mixed bounds unchanged. Thus the shifted half-integer version is justified with exactly the same constants.

## 2. Finite-field seed and macroscopic uniformity

For an odd prime p let q=p²−1 and let θ generate F_(p²)^×. Its order excludes θ∈F_p. Each θ+x with x∈F_p is nonzero and has a unique discrete logarithm s_x modulo q. Distinct x give distinct exponents; no exponent is zero, since θ+x=1 would put θ in the smaller field. They can therefore be represented in [q], and there are exactly p of them.

If s_x+s_y=s_u+s_v modulo q, multiplying the corresponding field elements and cancelling θ² gives

    (x+y−u−v)θ+(xy−uv)=0.

Linear independence of 1 and θ gives equal sums and products. The monic quadratics with those roots agree, including repeated roots, so the unordered exponent pairs agree. This proves strong modular Sidonicity, hence ordinary integer strong Sidonicity. There is no assumption that pair entries are distinct and no unproved numerical feature of a particular finite field.

The proof's uniformity argument is independently valid. For any strong Sidon sequence S⊂[q] with |S|/sqrt(q)→1, set ν_q=q^(−1/2)Σδ_(s/q). Each nonzero ordered difference occurs at most once. The difference measure is consequently dominated, apart from a diagonal atom of mass |S|/q→0, by the full grid Riemann sum of spacing 1/q on [−1,1]. Compact support and bounded mass ensure that any weak subsequential limit ν satisfies ν*tilde(ν)≤Lebesgue measure.

For η_ε=ε^(−1)1_[−ε/2,ε/2], the convolution identity and that domination imply ∥ν*η_ε∥₂²≤∫η_ε*tilde(η_ε)=1. Weak L² compactness along ε→0 identifies ν=f dx, with support in [0,1], f≥0, and ∫f²≤1. Its mass is one. Equality in Cauchy–Schwarz forces f=1 almost everywhere. Every subsequential limit is the same, so the full sequence converges. Since p/sqrt(p²−1)→1, the finite-field seeds meet this hypothesis.

This is self-contained macroscopic uniformity. It does not apply an extremal Fourier theorem directly to the dilated examples, whose density constants are below one. It does not infer global Fourier smallness from weak convergence.

## 3. Exact affine avoidance and both phase constants

Fix m≥2 and a≥0 in (1/2)Z, with m not dividing the integer 2a. For B=mS+a and L=mq+a, strong Sidonicity follows by cancelling the affine change in any pair equality. A forbidden triple equality would imply

    m(s₁+s₂+s₃−s₄)=−2a,

which is impossible by the stated divisibility condition. This is exact avoidance for every seed, including repeated variables.

The affine coordinate differs from s/q by O(1/q), uniformly over the seed, and sqrt(q/L)→1/sqrt(m). Therefore the limiting measure is c dx with c=1/sqrt(m). The endpoint formulas give

    E_R/L → 2/m−2/(3m²),
    Re∫R³ conjugate(R)/L → −1/(6m²),
    phase → −1/[4(3m−1)].

For integer a, m=2 always divides 2a, while m=3,a=1 works. In that example c²=1/3, E_R/L→16/27, and the signed functional divided by L tends to −1/54. Their quotient is −1/32. This is a genuine counterexample to a universal uniform-profile integer phase lower bound with κ<1/32.

For m=2,a=1/2, B lies entirely in Z+1/2. Put A=B+1/2=2S+1, an integer set in [M], M=2q+1. The forbidden equation becomes a'+b'+c'−d'=1; its left side is even because all entries are odd. With R_B=e(−α/2)R_A, magnitudes are unchanged and

    R_B³ conjugate(R_B)=e(−α)R_A³ conjugate(R_A).

This quartic is periodic although R_B is antiperiodic. Thus c²=1/2, E_R/L→5/6, the shifted signed functional divided by L tends to −1/24, and their quotient is −1/20. No lattice scaling by two, lost mass factor, or incorrect unshifted integral is used.

The strongest phases within this explicitly defined single-residue family are correctly identified. No optimization over arbitrary sets or more complicated residue unions is established. Since 1/32<1/14 and 1/20<1/14, neither example refutes the desired bound.

## 4. Exact alias decomposition and rational arcs

Let U=(p/q)D_q and V=F_S−U. Set H=e(aα)U(mα), K=e(aα)V(mα), use the full ambient interval model G in the actual unit-lattice gauge, and put J=H−G. Then R_B=J+K exactly.

The seed mixed-term bounds survive α↦mα because that map preserves Haar measure. At the zero major arc, K(t/L)=o(sqrt(L)); its fourth energy is O(L), so the G,K mixed terms are also o(L). Since |J|≤|H|+|G| and the relevant powers are 1, 2, or 3, the J,K mixed terms are o(L). Similarly H and G have identical limiting zero-arc profiles, so J has the compact smallness needed to make every G,J mixed term o(L). These deductions do not require a pointwise bound on V away from zero.

For periodic integrable Z,

    ∫e(ℓα)Z(mα)dα=0 when m does not divide ℓ.

Indeed partitioning the circle into m cells produces the geometric sum Σ_j e(ℓj/m)=0. Here ℓ=2a is an integer. Hence the signed quartics of H and K vanish exactly, even for half-integer a. The cancellation has no coefficient-positivity premise.

The pure fourth energies and the mixed estimates give

    E(K)/L → 4/(3m),
    E(J)/L → 2(m−1)/(3m²),
    Re∫J³ conjugate(J)/L → −1/(6m²).

The first line is the seed residual energy 4q/3. For the second line, subtract E(G) from E(H) using H=G+J and the vanishing mixed integrals. For the third line subtract the positive dense signed quartic from the exactly zero signed quartic of H. Combining J and K reproduces the previously derived total constants. No claim is made that their nonnegative fourth energies cancel.

For an explicit arc calculation write α=(j+t/q)/m. At each fixed t,

    H(α)/sqrt(q) → e(aj/m)h(t),  h(t)=∫₀¹e(tx)dx.

For j≠0, G(α)/sqrt(q)→0; at j=0 the H and G profiles cancel in J. The Jacobian is dα=dt/(mq). The real-line Fourier identities are ∫|h|⁴=2/3 and ∫h³ conjugate(h)=1/6, obtained respectively from the triangular convolution of 1_[0,1] and its triple-to-single integral. Thus each surviving arc contributes (2/3)L/m² to E(J), while its signed contribution is e(2aj/m)L/(6m²). The nonzero arc factors sum to −1, since the full sum is zero.

The rigorous interpretation is first q→∞ for each fixed scaled cutoff K, then K→∞. The geometric-series tail of D_q is O(qK^(−3)); the corresponding ambient tail has the same order after fixed-m rescaling. This controls the mass outside the arcs. No arbitrary growing-cutoff assertion is needed.

For m=3 the nonzero arcs carry 4L/27 of fourth energy and signed total −L/54; K carries 4L/9 of energy and exactly zero signed integral. For m=2 the single nonzero arc carries L/6 of energy and signed total −L/24; K carries 2L/3 of energy and exactly zero signed integral. These sum to 16L/27 and 5L/6, respectively.

At a rational center j/m, j≠0, F_B=e(aj/m)p exactly while G=O(p/L). Hence ∥R_B∥∞≥(1+o(1))p and also ∥R_B∥∞≤2p. The examples therefore have residual supremum of order sqrt(L). A phase theorem adding ∥R_B∥∞=o(sqrt(L)) is not tested by these constructions.

## 5. Meaning of κ=1/14

Under the uniform-profile identities,

    Re∫R³ conjugate(R)≥−E_R/14+o(L)

is equivalent to

    T(B)≥[c²(3c²−2)/14+o(1)]L.

To check the algebra, c⁴/6−(2c²−2c⁴/3)/14=(3c⁴−2c²)/14. Nonnegativity of the true count supplies this automatically when c²≤2/3, but does not supply its positive right side when c²>2/3. The integer and half-integer examples have c²=1/3 and 1/2, strictly below that threshold. The corresponding shifted version has the same reasoning and sign.

## 6. Weighted positivity and occupancy identities

For nonnegative w, separate trivial ordered equal-pair relations from nontrivial relations. The trivial sum is exactly 2(Σw_n²)²−Σw_n⁴, with the subtraction correcting the double count of a=b=c=d. Therefore

    ∫|F_w|⁴=2(Σw_n²)²−Σw_n⁴+Δ(w).

Every summand in Δ(w) is nonnegative. It vanishes exactly when no nontrivial relation has all four indices in the positive support. This proves Δ(w)=0 if and only if supp(w) is strong Sidon. Likewise T(w)=0 if and only if the positive support avoids a+b+c=d, and the same equivalence holds for shift one.

The circle convolution identity is R⋆R=(1−2ρ)R+ρ(1−ρ)D_L, with ρ=k/L. Coefficientwise it is r_n²=(1−2ρ)r_n+ρ(1−ρ). Its roots are exactly −ρ and 1−ρ, so for real coefficients on [L] the converse forces indicator occupancy after adding the dense coefficient ρ. This is a full coefficient identity, not a consequence of two scalar moments.

## 7. Quantitative rounding and exact preservation scope

For 0≤w_n≤1, let m_w=Σw_n, δ=Σw_n(1−w_n), A={n:w_n≥1/2}, and h=1_A−w. Each coordinate obeys

    |h_n|≤2w_n(1−w_n),  h_n²≤w_n(1−w_n),  |h_n|≤w_n.

The first two sum to the stated L¹ and L² bounds. The fourth moment of the real signed sequence h is a sum over additive relations. Its trivial contribution is 2(Σh_n²)²−Σh_n⁴≤2δ². The absolute value of the nontrivial contribution is bounded term by term by Δ(w), because |h_n|≤w_n. Thus

    ∫|F_A−F_w|⁴≤2δ²+Δ(w).

On A, 1_A(n)≤2w_n. Multiplying four copies in each relation gives Δ(1_A)≤16Δ(w) and T(1_A)≤16T(w), including the shifted count. The constant 16 is not asserted optimal.

Assume m_w/sqrt(L)→c>0, δ=o(sqrt(L)), and ∫|F_w|⁴=2m_w²+o(L). Since Σw_n²=m_w−δ and Σw_n⁴≤m_w=O(sqrt(L)), the exact weighted identity implies Δ(w)=o(L). The displayed rounding bound then gives ∥F_A−F_w∥₄=o(L^(1/4)), while | |A|−m_w |≤2δ=o(sqrt(L)). The normalized coefficient measures differ in total variation by o(1), proving preservation of any fixed weak profile.

The differing ambient interval models have fourth energy O((|A|−m_w)⁴/L)=o(L). Their residuals therefore differ by o(L^(1/4)) in L⁴. Each original residual has L⁴ norm O(L^(1/4)). Telescoping either quartic and using Hölder gives o(L) changes in residual energy and signed quartic. For any normalized phase ratio, a positive limiting residual-energy coefficient is additionally needed to divide; this holds for the stated uniform-profile strong-Sidon normalization when c>0.

The exact conclusions must stay separate. Δ(w)=0 implies that the rounded A is exactly Sidon; T(w)=0 implies exact avoidance of A. Conversely, A may be Sidon or avoiding after low-weight support points were discarded even when the corresponding weighted defect/count was positive. For example weights (1/4,1/2,1/4) at indices 1,2,3 have positive nontrivial defect from 1+3=2+2, but their rounded set is {2}. They also have positive T(w) from 1+1+1=3 while {2} avoids triples. Thus the two iff statements apply to supp(w), not to rounded A.

## 8. Explicit approximate-versus-exact countercontrols

Let x<y be the first two points of B=3S+1. Uniformity forces both x/L and y/L to tend to zero: each fixed positive initial fraction eventually contains arbitrarily many seed points. Therefore u=2y−x lies in [L] for all sufficiently large seeds. It is not in B, because otherwise 2y=x+u contradicts strong Sidonicity. Adding it creates a genuine nontrivial pair relation, while retaining residue 1 modulo 3 and hence exact triple avoidance.

The new energy quadruples are bounded as follows: exactly one occurrence of u contributes at most 4·k·2=8k; exactly two on opposite sides contributes 4k; exactly two on the same side contributes at most four; exactly three contributes zero; four contributes one. This gives total energy increase at most 12k+5. The trivial energy increases by 4k+1, so the new defect is at most 8k+4=o(L). The set remains macroscopically uniform and has the correct leading energy, but is not Sidon. Rounding its indicator does nothing. This validates the proof's boundary without asserting that a small-deletion repair theorem is impossible.

A separate exact-avoidance countercontrol is obtained by adding 3x instead. For large seeds 3x≤L and 3x is not in B by residues. The equation x+x+x=3x now holds. The same one-point energy bound keeps the leading energy unchanged. Thus approximate moment hypotheses also do not themselves imply exact avoidance.

## 9. Separation of the earlier signed polynomial

The earlier model has a negative frequency-3 coefficient (b+o(1))L^(1/4), with b<0. In the unperturbed polynomial the lower-order remainder is O(L^(−1/2)); in the exact-zero perturbed polynomial it can be O(1). The final proof correctly uses the common leading formulation.

Any nonnegative-coefficient polynomial differs at that coefficient by at least (|b|+o(1))L^(1/4). A Fourier coefficient is bounded in magnitude by the L¹ norm, hence by the probability-space L⁴ norm. Raising to the fourth power gives the claimed lower bound (b⁴+o(1))L=(y²+o(1))L. Thus that signed model cannot be approximated in o(L) fourth-power error by any nonnegative or indicator polynomial. This does not exclude other positive constructions.

## 10. Corrections incorporated before acceptance

Two changes were requested during audit:

1. The introductory iff formulation was narrowed explicitly to the positive support of w. The rounded set is only guaranteed to inherit exact Sidonicity when Δ(w)=0; no converse is asserted.
2. The frequency-3 statement now uses (b+o(1))L^(1/4), covering both the unperturbed and exact-zero perturbed earlier models.

The author also made the iterated rational-arc limits explicit and added precise source attribution. These changes do not alter any accepted leading constant, finite identity, or rounding bound. The final frozen bytes, rather than an earlier draft, are the accepted target.

## 11. Scholarly checks and source boundary

The audit independently opened the following primary scholarly documents on 12 October 2026:

- Melvyn B. Nathanson, “The Bose-Chowla argument for Sidon sets,” arXiv:2104.12711, PDF https://arxiv.org/pdf/2104.12711. Theorem 1, PDF pages 3–4, gives modular Sidon sets of order h and cardinality p in modulus p^h−1. The h=2 construction matches the one reconstructed here (the sign of the field parameter is immaterial). This is a modern proof exposition, not a claim that Nathanson originated the construction.
- Miquel Ortega and Sean Prendiville, “Extremal Sidon Sets are Fourier Uniform, with Applications to Partition Regularity,” Journal de Théorie des Nombres de Bordeaux 35 (2023), 115–134, DOI https://doi.org/10.5802/jtnb.1239 and official PDF https://jtnb.centre-mersenne.org/item/10.5802/jtnb.1239.pdf. Theorem 1.2, printed p.116, and Theorem 6.3, p.128, use the same unnormalized Fourier convention. Proposition 1.13 and Remark 1.14, p.118, already describe affine-residue avoidance constructions for homogeneous equations with nonzero coefficient sum. Theorem 1.15 requires at least five variables and does not supply the desired four-variable conclusion.

The manuscript's construction and weak-uniformity proof are reconstructed above and do not depend on importing an unverified rate. In particular the source Fourier bound is not asserted for the diluted examples with constant density deficit. The finite-field argument and residue trick are not presented as novel. No exhaustive literature-status inference is drawn. The audit observed rendered PDF text through the web tool; it did not retain and independently hash complete PDF bytes, so no PDF size or digest is claimed.

## 12. Independent computation and reproducibility limits

Two new diagnostic programs were authored independently. Neither imports, reads, nor executes the author's program.

- The finite-field checker constructs ten seeds for primes 3,5,7,11,13,17,19,23,29,31 using an explicit quadratic finite field and primitive-element cycle. It verifies strong modular Sidonicity and both exact avoidance constructions, computes residual second moments, fourth energy, and signed shifted/unshifted integrals by integer convolution, and checks the exact dense interval formulas for all lengths 1–80. Integer-convolution overflow is excluded by a checked absolute bound before every convolution. Final products and rational reductions use arbitrary-precision Python integers.
- The rounding checker directly enumerates four-index relation lists and all 3,905 coefficient vectors in {0,1/4,1/2,3/4,1} at lengths 1–5. It checks the weighted energy identity, both support iff conditions, all rounding inequalities, and signed counts at shifts 0 and 1. It finds 1,307 cases with positive weighted defect but a Sidon rounded set, independently guarding against the incorrect rounding converse.

Each program produced byte-identical PASS output under normal Python, −O, and −OO. The programs use explicit runtime checks rather than assertions that optimization could erase. Exact diagnostic identities support, but do not establish by extrapolation, the universal asymptotic statements. The full written argument is the mathematical basis for acceptance. No remote mutation, repository publication, or queue edit was performed by this audit.

## Public edition notice

The preceding text is the complete accepted historical proof or audit, with only the locator edits recorded in [EDITION_MAP.md](EDITION_MAP.md). Statements about accompanying diagnostic programs, original input records, or the absence of publication describe the original research or review stage. This prose-only edition distributes no executable program, detailed diagnostic collection, source PDF or image, or private record. Original and accepted file identities are recorded in [INPUT_PINS.json](INPUT_PINS.json); public-file identities are recorded in [MANIFEST.json](MANIFEST.json). [VERIFICATION.json](VERIFICATION.json) distinguishes exact finite checks, floating-point diagnostics, and integrity checks. This notice changes no mathematical argument, verdict, or hypothesis.
