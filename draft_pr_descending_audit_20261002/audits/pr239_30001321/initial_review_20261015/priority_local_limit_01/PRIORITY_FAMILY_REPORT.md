# PR239 / 30001321 local-limit and invariant-density priority audit

**Audit date:** 2026-10-15 UTC. **Family:** random average process, invariant density, independent particles, stochastic-flow and related dynamic-RWRE local limits. **Scope:** exact full claim, not validity review of the submitted proof. No outreach or Git/provider mutation was performed.

## Finding

No inspected complete primary theorem in this family has been shown to imply the submitted full conclusion. The strongest authenticated earlier coverage for the exact scalar-law model includes an almost-sure quenched invariance principle and the classical replica/quenched-mean mechanism, together with a stationary past-dependent L2 density and an exact covariance formula. They establish substantial precedent for the ingredients and averaging picture. They do not, in their inspected stated forms, supply the required all-K environmental probability bound on the single-origin coarse-L1 discrepancy.

**This is a bounded negative search result, not a novelty proof.** A material original source remains unread: BMP1999, cited by later authors for a weighted local limit. Its 2007 primary survey account contains a range ambiguity and a strong quasi-locality definition. We prove that literal uniform quasi-locality would already give the necessary concentration of its stationary factor at every slowly diverging scale. The remaining question is its local-limit residual and exact object/assumptions. Therefore this lane does not clear BMP1999 as irrelevant and does not classify the overall result as novel.

## Exact target and pass criteria

Fix one iid law of scalar p_(t,x) with0<p<1 almost surely. Let μ_N^ω be the quenched endpoint law of the ±1 walk from0 and α_N=Eμ_N^ω. For every deterministic equal-interval scale M_N→∞, every ε>0 and K>0, and every deterministic alignment, the submitted claim is

    P_env(Σ_I |μ_N^ω(I)−α_N(I)|>ε)≤C_(ε,K)N^(−K)

for all sufficiently large N. The threshold may depend on the sequence M_N; constants may depend on the fixed law. No uniform ellipticity, symmetry, inverse moments, or quantitative lower rate for M_N is allowed. Alignment constants must be uniform. The source-to-target implication must preserve the sum over the entire terminal partition, not only one point or finitely many macroscopic test functions.

The input hashes are in INPUT_HASHES.json. The exact frozen PROOF.md and both earlier turns were read before fixing this comparison. Their mathematical soundness is not decided again here.

## Complete primary results inspected

The concise source descriptions below are followed by original implication derivations in separate artifacts.

| Source | Authenticated content relevant here | Exact target coverage / gap |
|---|---|---|
| Rassoul-Agha–Seppäläinen, arXiv math/0411602v1 (2004), PTRF133(2005)299–314, Theorem1; Section4 | Quenched functional invariance principle under annealed second moments and non-determinate iid space-time transitions; replica difference walk yields subdiffusive quenched-mean variance. | Applies to the target. Weak convergence at the diffusive scale has no all-K environmental convergence rate and does not control a growing family of microscopic intervals. |
| Balázs–Rassoul-Agha–Seppäläinen, arXiv math/0507226v2, CMP266(2006)499–545, Theorem3.1; Sections3–4 | Quenched invariance principle, quenched-mean fluctuation limits at N^(1/4), and origin-perturbed difference-walk Green function analysis. | Applies after exact parity shear. These are clear ingredient precedents, not a coarse-L1 tail theorem. Homogeneous auxiliary-walk local limits in the proof are not quenched endpoint LLTs. |
| Joseph–Rassoul-Agha–Seppäläinen, arXiv1110.1889v1/v2 and published2019 chapter | Proposition3.1 constructs f_N=Σ_z K_(−N,0)(z,0)→f a.s./L2, Ef=1. Theorems1.1/1.2 describe invariant particle laws and covariance; Corollary1.3 gives zero off-diagonal covariance for consecutive two-site jumps. | Exact target law fits after parity shear. f_N is a column sum from all starting sites. Its stationary law and infinite-particle equilibrium convergence do not identify μ_N with α_Nf or give the target tail. |
| Dunlap–Gu, May27,2021 author manuscript and arXiv2105.07907v3; JFA282(2022)109372, Theorem1.1 | Gaussian velocity white in time, smooth compactly supported spatial covariance, Brownian molecular diffusivityν>0. In d1: sup_x E|u−G U|²≤Ct^(−4/3)logt, EU=1 and covariance decay. Latest version adds temporal covariance. | Different continuum model. Even granting a discrete analogue, direct integration gives only a fixed polynomial expected residual, not all-K environmental tails. |
| Deuschel–Guo, arXiv1710.05508v2 (Dec3,2019), PTRF182(2022)111–156, standing assumptions/Theorem4 | Continuous time, d≥2, pointwise balanced, uniformly elliptic, space-time ergodic rates; a.s. LLT for q^ω=p^ω/ρ_ω. | Model mismatch plus no stated environmental convergence-rate theorem. Mean-centering a random scalar drift does not make it balanced. |
| Thiery–Le Doussal, arXiv1605.07538v1 (May24,2016), SectionsIVD–E | Exactly solvable Beta-law transition probabilities; diffusive one-point Gamma fluctuation asymptotics and multipoint formulas. Equations81–83 distinguish fixed endpoint/varying starts from fixed start/varying endpoints. | A special law family; single-point moment/Laplace asymptotics do not assert whole-partition environmental concentration. Constant Gamma process in their chosen orientation cannot be mistaken for a common factor across a normalized forward endpoint law. |
| Barraquand–Corwin, arXiv1503.04117, Sections1.6/5 | Exact Beta RWRE moment/Fredholm formulas and fluctuation results, chiefly ballistic large deviations; classical diffusive CLT and quenched-mean variance discussed separately. | Useful related precedent, no inspected full coarse-L1 all-scale tail theorem. A Beta special-case result would still need an explicit transfer to every fixed elliptic scalar law. |

The direct primary links, hashes, historical submission times, and precise page/section pointers are recorded in PRIMARY_RETRIEVAL.json and SOURCE_VERSIONS_AND_SECTIONS.json. Full third-party PDF and extracted text files are private reading objects and are excluded from authored manifests.

## Important exact implications

1. **Parity is not a disqualifying assumption.** Y_t=(X_t+t)/2 has iid {0,1} transition probabilities p̃_(t,y)=p_(t,2y−t), with span one. Equal real cells transform exactly; odd integer cell counts alternate by at most one. This lets the RAP/JRS results apply without importing aperiodicity as an extra target hypothesis.

2. **The invariant density yields genuine averaging evidence.** With q=Ep, a=q(1−q), δ=E[p(1−p)] and σ²=Var(p), JRS's Fourier formulas give β=δ/a, Var f=σ²/δ and zero off-diagonal covariance after the shear. For ν_N(y)=b_N(y)f(T_(y,N)ω), the original derivation gives, uniformly in alignment,

       E||ν_N(coarse)−b_N(coarse)||_1
          ≤ C√(R/M+N^(−1/2))+C/R².

   It tends to0 for every M_N→∞. This ν_N is not automatically normalized and is not asserted equal to μ_N. The derivation carefully uses only positivity and Ef=1 for its tails.

3. **Finite-order local errors leave a real rate gap.** A hypothetical discrete bound sup E|μ_N−b_Nf|²≤CN^(−1−η) gives central-window expected L1 error CRN^(−η/2). Binomial tails permit logarithmic radius growth. This still yields a fixed polynomial exponent under Markov, not arbitrary K. The adversary's exact normalized binomial modulation satisfies stronger local L2 bounds and eventual a.s. equality while retaining a coarse-L1 tail exactly N^(−2). It demonstrates nonimplication of these summaries, not a counterexample to iid RWRE.

4. **Fixed-law approximation must respect quantifiers.** Quantizing p within h changes quenched endpoint L1 by at most2Nh, and changes coarse discrepancies by at most4Nh. A fixed approximation is insufficient for all large N. Choosing h_N=o(1/N) creates changing laws, so a finite-state theorem with law-dependent constants/thresholds needs additional uniformity before covering all scalar laws.

5. **A corrector is compatible with coarse smoothing.** Nontrivial local density fluctuations and N^(1/4) mean fluctuations do not establish a fixed-ε coarse-L1 lower bound. The density covariance calculation explicitly averages the former; a Gaussian shifted by N^(1/4) changes L1 by only O(N^(−1/4)).

Full proofs are in IMPLICATION_DERIVATIONS.md. Its first checkpoint was independently reviewed; two precise wording refinements concerning global tail-radius optimization and variable clocks were incorporated.

## BMP1999 / 2007: open priority fork, not an exclusion

Original: Boldrighini–Minlos–Pellegrinotti, *Central limit theorem for a random walk in dynamical environment: integral and local*, Theory of Stochastic Processes5(21)(3–4)(1999),16–28. The author institution's record is [Sapienza](https://iris.uniroma1.it/handle/11573/28307). It has metadata but no attachment. The journal's public archive examined begins at2005. No full original was obtained.

The primary [2007 survey](https://www.mathnet.ru/eng/rm6849), §1.4.3 printedp680, was partially accessible through indexed passage extraction. Repeated direct requests timed out, the IOP route returned a bot challenge, and the actual-file route also timed out. These failures are recorded. The passage cannot be dismissed as a generic CLT: it expressly discusses a terminal random factor.

There are unresolved range expressions: normalized u_T=o(T^(1/6)) in introductory prose, literal unnormalized x_T−bT=o(T^(1/6)) in its final display, and |x|≪t^(1/3) in Dunlap–Gu's later description. The first corresponds to physical o(T^(2/3)), which contains the diffusive bulk. This audit does not infer the intended theorem range from inconsistent accounts and does not use a narrow-window argument to exclude it.

More materially, its uniform finite-cylinder oscillation definition of quasi-concentration is much stronger than ordinary covariance decay. We prove in QUASILOCAL_SOURCE_BRIDGE.md that this definition would give the stationary factor alone an exp(−c_ε√N) coarse-L1 tail for every M_N→∞, uniformly in alignment. The proof fixes a cylinder approximation radius depending on ε, and uses a weighted bounded-differences convolution estimate. It does not require a numerical rate of quasi-locality. This is a positive implication which a complete priority review must preserve.

**Exact remaining fork:** does the original give a deterministic uniform residual, or an environmental failure probability that can be made O(N^(−K)) for every K, on a window that includes the bulk? If so, the quasi-local concentration bridge could yield an earlier finite-state result. The indexed survey writes an o(1) without furnishing that rate; its main CLT's mode is a.s./L2. One cannot silently promote this residual to a uniform deterministic one.

There is also an object-identification caution. Literal finite-state uniform quasi-locality implies a bounded factor. An independently checked inward-funnel argument proves that JRS's density for a fixed two-atom law {r,1−r},0<r<1/2, has unbounded support. Therefore equating that bounded Φ with generic JRS f needs proof from the original assumptions and definitions. This does not establish that an unread BMP theorem is false.

## Search coverage and exclusions kept honest

Primary full texts were traced through RAP/JRS references, the two discrete references of Dunlap–Gu, and exactly solvable Beta models. Searches also surfaced symmetric dynamic-conductance and balanced-environment LLTs. Their symmetry/balance and ellipticity assumptions cannot be dropped merely because they concern time-dependent nearest-neighbor motion. The percolation-backbone/local-limit family and post2024 quantitative searches are owned by other independent lanes and are not adjudicated here.

No communication to any person was prepared or initiated. The missing original is recorded as a research-source gap. This report does not propose or initiate outreach.

## Reproducibility and adversarial review

- Exact input SHA256s: INPUT_HASHES.json.
- Download receipts/hashes: PRIMARY_RETRIEVAL.json; failed routes: BMP_FAILED_ROUTES.json.
- Source page/version ledger: SOURCE_VERSIONS_AND_SECTIONS.json.
- Independent written audit: adversary/INDEPENDENT_SOURCE_AUDIT.md.
- Exact rational normalized rare-event example: adversary/check_rare_event_obstruction.py and its receipt, N=1..128, PASS.
- Exact rational funnel controls: adversary/check_inward_funnel.py and INWARD_FUNNEL_CONTROL_RECEIPT.json, r=1/10,1/4,2/5 and T=0..64, PASS.
- Parent replay of both exact controls: ADVERSARY_REPRODUCTION.json; all generated result fields agree (saved receipts add a UTC timestamp).
- Re-run validate_lane.py to verify frozen inputs, private source pins and both exact controls; VALIDATION_RECEIPT.json records the completed replay.
- Mathematical deductions, rather than numerical experiments, justify all asymptotic conclusions in this lane.

**Bounded audit status:** complete; final independent check of the quasi-local bridge passed; **overall priority status:** unresolved. Strongest verified contribution of this audit is the exact source-to-target distinction and the positive quasi-local stationary-factor bridge, with the original LLT-residual fork explicitly preserved. Failure to find an exact match is not proof of novelty.
