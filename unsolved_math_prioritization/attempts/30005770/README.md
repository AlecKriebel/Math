# Diagonal Permuton Limits for Skew Sum Avoidance

## Partial results and exact remaining questions

This reader collects authored proofs, corrections, independent AI mathematical audits, reproducible finite checkers, and public source metadata for target **30005770 / OWR-14298158-015**. The universal target is **unresolved**. The package proves two infinite fixed-pattern families and gives rigorous general and 1324-specific partial results. It gives no positive-uniform-probability counterexample, novelty claim, or human peer-review certification.

The most direct reading route is:

1. [Exact target and credited prior coverage](diagonal_permuton_1778_20261014/CONSTRUCTION_CONTRACT.md)
2. [Two seed cases](diagonal_permuton_1778_20261014/pass1_uncovered_case/TWO_SUBCASE_THEOREM.md), [self-contained enumeration appendix](diagonal_permuton_1778_20261014/pass1_entropy/KERNEL_ENUMERATION_APPENDIX.md), and [family transfer theorem](diagonal_permuton_1778_20261014/pass2_protected_tail_extension/MERGE_TRANSFER_THEOREM.md)
3. [Fresh independent family re-audit](diagonal_permuton_1778_20261014/independent_family_reaudit/INDEPENDENT_ACCEPTANCE.md)
4. [Theorem map and dependencies](PROOF_MAP.md), followed by the selected full proofs
5. [Precise unresolved estimates](#what-remains-unresolved), [source limitations](SOURCES.md), and [verification instructions](CHECKS.md)

All mathematical papers and checkers retained here are byte-for-byte copies of their final accepted artifacts. The [transformation map](TRANSFORMATION_MAP.json) records the identity mapping for mathematical proofs and checkers, plus narrowly edited audit copies with their original and public hashes; no proof was rewritten to make this reader. The dated `pass1`–`pass5` directory names identify successive artifact groups, not five independent proofs of the target. Historical audit statements are read with the supersession notes below.

## Exact target

Fix a nonempty permutation α of size m, independently of n. Let τ=α⊖1, where ⊖ is the skew sum, so τ(i)=α(i)+1 for 1≤i≤m and τ(m+1)=1. Let Π_n be exactly uniform on all classical τ-avoiding permutations of size n.

For π∈S_n, its square-spread permuton μ_π has density n on the n squares

\[
[(i-1)/n,i/n]\times[(\pi(i)-1)/n,\pi(i)/n],\qquad 1\le i\le n,
\]

and zero elsewhere. Each square has mass 1/n; both coordinate marginals are uniform. The target is weak convergence in probability to μ_I=Law(U,U), with U uniform on [0,1]. Equivalently, for every ε>0,

\[
\Pr\{d_{\mathrm{BL}}(\mu_{\Pi_n},\mu_I)>\varepsilon\}\longrightarrow0,
\]

where the bounded-Lipschitz metric uses the Euclidean metric on the square. Existence and identification of the limit are both required. Neither total-variation convergence, a growing forbidden pattern, a rate uniform over α, nor an unspecified almost-sure coupling is part of the target.

The conjecture is stated in Troyka's contribution, joint with Bevan, on printed p.298 of the [Oberwolfach report](https://ems.press/content/serial-article-files/48646?nt=1#page=26). The [full contract](diagonal_permuton_1778_20261014/CONSTRUCTION_CONTRACT.md) resolves the neighboring formulation issues without changing this target.

## What is proved for full uniform avoidance classes

Write J_r for the decreasing pattern of size r and take J_0 empty. For each fixed r≥0 and either

\[
\alpha=132\ominus J_r\quad\hbox{or}\quad\alpha=213\ominus J_r,
\]

exactly uniform Π_n∈Av_n(α⊖1) converges to μ_I. For every fixed ε>0 there are constants C,c>0, depending on α and ε, such that

\[
\Pr\{d_{\mathrm{BL}}(\mu_{\Pi_n},\mu_I)>\varepsilon\}\le C e^{-cn}
\]

for all sufficiently large n. This is the accepted family theorem, not the universal conjecture.

The proof starts with uniform 1342-avoiders. Bóna's credited bijection gives their exact uniform labeled-tree/forest law and preserves left-to-right minima. The weighted catalytic argument yields exponentially small linear-height tails under that labeled law. Skew-component geometry produces a one-sided anti-diagonal envelope; uniform marginals turn it into a weak-metric bound. Reversal and inversion give α=132 and α=213. The transfer theorem then adjoins minima, with the starts-with-1 hypothesis, ambient merge counts, subset discrepancy, actual avoidance denominators, and Bóna's exact growth equality all retained. The underlying uniform law is never replaced by uniform unlabeled tree shapes or by a convenient generator.

The fresh [independent AI re-audit](diagonal_permuton_1778_20261014/independent_family_reaudit/INDEPENDENT_ACCEPTANCE.md) checks all three final proofs, including the exact labeled law, the analytic branch, the weighted depth argument, square-spread geometry, and the transfer's starts-with-1 restriction. It reports no defect within this scope. It is mathematical QA by an AI reviewer, not human peer review or a priority assessment.

Previously credited coverage remains distinct: Hohmeier–Slivken [arXiv:2502.19541v3, Theorem 1.1](https://arxiv.org/pdf/2502.19541v3#page=3), after complement symmetry, covers α=I_a⊖J_b for fixed a≥1,b≥0. That displayed theorem alone does not cover arbitrary α. Its full proof was not independently re-audited in this package.

## General fixed α results

For every fixed α of length at least two, the package proves the following partial results under the exact uniform full-class law. The case α=1 is trivial.

- **Frontier and small values:** the first α-free prefix has an exponential linear-size tail. Every sublinear number of smallest values is localized near the left boundary; the positive-density corner bound retains its binary-entropy cost.
- **Growth and packing:** Av(α) has a strict growth gap below Av(α⊖1). Making a typical avoider α-free requires linearly many deletions, and there are linearly many vertex-disjoint α occurrences with exponentially high probability.
- **Exact continuation states:** the standardized prefix through the first α occurrence determines the full minimum-insertion continuation tree. A scalar prefix length does not.
- **Exact diagonal-cut states:** keeping active endpoint orders and the closed-interior pattern profile gives an exact exposure/transfer description. For every fixed crossing-width bound K the enumeration is rational, with a strict growth constant λ_K<λ and supremum_K λ_K=λ. Thus fixed bounded width is exponentially atypical. This does not show that width/n stays positive or tends to zero.

Two kinds of limitations are proved. A repaired abstract generating tree satisfies the stated scalar numerical completion bounds but has macroscopic weighted ancestors; it is explicitly not a principal avoidance class. Separately, actual avoiding permutations show that global α packing, localized small values, or boundary order without closed-interior context cannot by themselves close the spatial argument. These are nonimplication results, not counterexamples under the uniform law.

## The first remaining 1324 related case

The target α=312 forbids 4231. Reversal makes its desired diagonal limit equivalent to the anti-diagonal weak limit for exactly uniform 1324-avoiders. Both remain unresolved here.

The canonical greedy staircase has nonempty normalized states A avoiding 213 and exact directed shuffle multiplicity K(A,C). Write a_n=|Av_n(1324)|, λ=lim a_n^(1/n), ρ=1/λ, and ℓ_A,h_A for the incoming and outgoing completion factors. The exact count of a marked cell uses z^|A|ℓ_A(z)h_A(z). Neither factor can be dropped.

The proved partial results include:

- exponential smallness of each fixed greedy prefix's total linear mass, exact canonical encoding, and explicit exponential incoming bias;
- arbitrary-index isolated fixed-width block tails and large upward-jump tails; a fixed c<1 with exponentially small probability that a cell has mass at least cn;
- common first- and last-cell exponential marks throughout the subcritical interval, a pointwise terminal-to-initial lift, and joint endpoint marks;
- exact finite-window reroot certificates, g_1=4 and g_2=27/4, and a conditional theorem from divergence of the true logarithmic window gaps;
- an exact increasing-pair generating series, internal-chain reduction, a low-chain-run theorem with restricted-path growth at most 8, and a pure size-weight obstruction at height three;
- a rectangle deletion identity with an admissibility indicator, exponential rarity of favorable occupied rectangles, and a complete coarse occupied/sparse branch reduction.

The package also proves precise barriers to the examined methods: the strict squared-kernel gap is impossible; positive diagonal Hilbert–Schmidt reweighting cannot repair it beyond ρ; certain actual canonical mountains defeat the available one-/two-ended window certificates; comb examples defeat the raw favorable-rectangle entropy score; near-empty examples defeat the implication from short chains plus few exactly-empty pairs; a specified folding map loses exponentially much information; a separate monotone-staircase model has quadratic summable true gaps. Each barrier has its own scope in the [theorem map](PROOF_MAP.md). No deterministic construction is asserted to occur with probability bounded away from zero under uniform 1324 sampling.

## What remains unresolved

No estimate in this package proves the universal fixed-α target or the uniform 1324 weak limit. The remaining sufficient estimates are explicit:

1. **General α:** control macroscopic crossing mass with the actual unbounded cut-state data, allocation compatibility, and incoming/outgoing completion weights retained. Fixed-K transfer growth gaps do not provide this width-uniform control.
2. **1324 marked cells:** a fixed u>1 with
   \[
   \sum_A u^{|A|}z^{|A|}\ell_A(z)h_A(z)<\infty\quad\text{for every }0<z<\rho
   \]
   would imply exponential largest-cell tails. This is unproved, and largest-cell sublinearity is sufficient rather than necessary for the weak limit.
3. **True window gaps:** divergence of ∑_K log(λ/g_K) would activate the adaptive-window theorem. Only summable lower certificates are established. The comparison model does not determine the actual 1324 gaps.
4. **Increasing pairs:** with K_inc the actual cross-increasing-pair shuffle count,
   \[
   I(z)=\sum_A z^{|A|}\ell_Ah_A\operatorname{Inc}(A)
   +\sum_{A,C}z^{|A|+|C|}\ell_Ah_C K_{\mathrm{inc}}(A,C),
   \]
   the desired 1324 weak limit is equivalent to [z^n]I(z)=o(n²a_n). Both terms are nonnegative. Completion-weighted long internal chains and actual cross-edge pairs remain uncontrolled in general. Low-chain runs with large boundaries and high-chain states are not covered by the low-chain theorem; the occupied/sparse rectangle alternatives do not themselves settle the residual branches.

The squared-kernel condition β<λ is no longer a candidate missing inequality: it is **proved impossible for this exact kernel**. The earlier conditional theorem is retained as an implication with an unattainable hypothesis, together with the later obstruction. It is not presented as an active route to the target.

## Source and version safeguards

[Sources and version limits](SOURCES.md) distinguish credited inputs, inspected statement scope, and source-status checks. In particular:

- The displayed count inconsistencies concern the inspected Bóna preprint. Nothing here asserts that the final published version contains them. The authored kernel appendix removes those displayed counts as assumptions; the credited bijection remains an external input.
- A 2023 1342 announcement and the later Hohmeier–Slivken v3 conjectural status are both recorded without inferring a reason, withdrawal, or priority result.
- Norton [arXiv:2608.20292v3](https://arxiv.org/abs/2608.20292v3) explicitly withdraws the larger 10.617 and 10.466425 claims and states 10.412263. That surviving value is below 6+2√5. It supplies **no height-three upgrade**, and its proof is not adopted here.

No third-party PDF or copied source text, dataset contents, private source, credentials, or private coordination material is part of this reader. Public scholarly metadata and authored finite mathematical verification records are included. Retrieval and inspection dates describe the original reviews, not a fresh literature search during packaging.

## Audit history and superseded material

The audit reports are separate AI reviews of the indicated frozen mathematical artifacts. Acceptance is limited to their stated scopes. [AUDIT_INDEX.json](AUDIT_INDEX.json) identifies the mandatory analytic and structural receipts, the family re-audit, and the final supplements. An audit that inspects author check outputs does not thereby claim to have rerun those programs.

Provisional tree-height and three-point-reroot drafts and the initial unresolved tree-shape audit are excluded. Their accepted final replacements are [TWO_SUBCASE_THEOREM.md](diagonal_permuton_1778_20261014/pass1_uncovered_case/TWO_SUBCASE_THEOREM.md) and [REROOTING_ONE_POINT_BOUND.md](diagonal_permuton_1778_20261014/pass3_concentration_audit/REROOTING_ONE_POINT_BOUND.md). Historical acceptance receipts can mention an omitted earlier draft; the derivative acceptance and fresh family re-audit pin the operative final proof.

The coarse abstract countermodel is retained only with its explicit 51>50 failure of a sharper completion inequality. The repaired [COMPLETION_BOUND_COUNTERMODEL.md](diagonal_permuton_1778_20261014/pass2_bulk_concentration/COMPLETION_BOUND_COUNTERMODEL.md) satisfies the full listed numerical constraints and is the operative stronger obstruction. Neither model is an avoidance-class counterexample.

The folding proof's operative pin is the corrected derivative. [FOLDING_DERIVATIVE_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_concentration_audit/FOLDING_DERIVATIVE_ACCEPTANCE.md) distinguishes identical records in the folded output from original source coordinates and supplies the stronger coordinate-record fibre argument. The earlier acceptance must not be read as asserting identical original source coordinates.

## Verification

The finite programs and their meaningful outputs are included beside the relevant proofs. They check exact finite identities, reconstruction, distributions, and hash pins; they do not prove asymptotic statements by extrapolation. Normal, `-O`, and `-OO` outputs are retained where supplied, with timing/mode differences distinguished from mathematical differences.

The [independent package review](PACKAGE_REVIEW.md) accepts this reader after a narrow inventory-validator correction and records its separate claim, editorial, privacy, and reproducibility checks. No mathematical proof or original checker was changed.

Run `python verify_package.py` for the complete package file list and hashes. See [CHECKS.md](CHECKS.md) to replay selected or all finite checkers in a disposable copy without overwriting the frozen reports. The package manifest and audit index are integrity/navigation aids, not independent mathematical proofs.
