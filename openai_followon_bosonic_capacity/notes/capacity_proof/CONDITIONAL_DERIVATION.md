# Conditional dynamic-capacity derivation

Checkpoint: 2026-10-06 21:20 Pacific (2026-10-07 04:20 UTC).

**Status.** This verifies the entropy-to-capacity reduction conditionally. It does not validate family 273, prove the entropy premise, establish priority, or certify the full project for publication. **Subsequent operational audit found that the private source's literal secrecy condition excludes consumption of key by the one-time pad, and refutes the private formula at zero channel energy. Read PRIVATE_SECURITY_DEFECT_AND_REPAIR.md: it gives the counterexample and a repaired converse under conventional generated-resource secrecy. The private conclusion below must be read with that correction, not as certification of the literal printed source convention.** The reduction and the Gaussian inner regions are inherited from Wilde–Hayden–Guha (WHG), with a particularly clean formulation in De Palma's Theorem 11 and Corollary 12. A publication must describe their application as a consequence of a separately verified new entropy theorem, not a new invention of the coding formulas.

## 1. Exact claim and entropy premise

Write \(\mathcal L_t\) for the single-mode quantum-limited attenuator (pure loss, vacuum environment) with transmissivity \(t\), and \(H_n=\sum_{j=1}^n a_j^\dagger a_j\) for total photon number. Fix \(1/2\le\eta\le1\) and \(0\le N<\infty\). Every logarithm in this note is base two, so

\[
g(x)=(x+1)\log_2(x+1)-x\log_2x,\qquad g(0)=0.
\]

The conditional entropy premise is

\[
\tag{VE}
S(\mathcal L_t^{\otimes n}(\sigma))
\ge n g\!\left(tg^{-1}(S(\sigma)/n)\right)
\]

for every integer \(n\ge1\), every density operator \(\sigma\) on the full \(n\)-mode Fock space with \(\operatorname{Tr}H_n\sigma<\infty\), and the relevant transmissivities \(t\in[0,1]\). No Gaussian, product, separability, phase-invariance, or finite-rank assumption is allowed in (VE). For the quantum reduction at a fixed \(\eta\), only \(t=\eta\) and \(t=(1-\eta)/\eta\) are used. For the private reduction only \(t=(1-\eta)/\eta\) is used. At \(\eta=1\) no nontrivial entropy premise is needed.

The claim is about the ordinary asymptotic vanishing-error dynamic capacity regions under a **block average input photon constraint**

\[
\operatorname{Tr}H_n\bar\rho^{(n)}\le nN.
\]

Here \(\bar\rho^{(n)}\) is the channel-input marginal averaged over the operational uniformly distributed classical messages, maximally mixed quantum source (equivalently a maximally entangled reference source), and prescribed resource states. A per-message/per-codeword expected-energy constraint, a photon-number occupation constraint, a peak cutoff, and a strong converse are separate statements. The ordinary capacity formulas do not by themselves prove those stronger claims.

The **quantum** target is the closure of the union, over \(\lambda\in[0,1]\), of all real triples \((C,Q,E)\) satisfying

\[
\begin{aligned}
C+2Q&\le g(\lambda N)+g(\eta N)-g((1-\eta)\lambda N),\\
Q+E&\le g(\eta\lambda N)-g((1-\eta)\lambda N),\\
C+Q+E&\le g(\eta N)-g((1-\eta)\lambda N).
\end{aligned}
\]

The **public/private/key** target, retrieved from WHG Theorem 7, Eqs. (48)–(50), is the corresponding closure of the union of all real \((R,P,S)\) satisfying

\[
\begin{aligned}
R+P&\le g(\eta N),\\
P+S&\le g(\eta\lambda N)-g((1-\eta)\lambda N),\\
R+P+S&\le g(\eta N)-g((1-\eta)\lambda N).
\end{aligned}
\]

Both formulas have resource-generation positive and resource-consumption negative. Imposing \(C,Q,E\ge0\) or \(R,P,S\ge0\) would give only an octant, not the full target.

## 2. Coding-theorem dependencies and operational conventions

The primary quantum source is Wilde–Hsieh, *The quantum dynamic capacity formula of a quantum channel*, arXiv:1004.0458v3, Theorem 1, Secs. 3–6. The sender uses one encoding map, arbitrary joint inputs to \(n\) copies of the noisy channel, noiseless **forward** classical and quantum resource channels, and preshared maximally entangled states; the receiver decodes. The model consumes and generates the same resource types catalytically, recording their net rates. It does not supply uncounted feedback, free backward communication, or two-way distillation. The correctness criterion is vanishing trace distance to ideal classical correlations, quantum reference entanglement, and generated shared entanglement (Sec. 3, Eq. (4)).

For an input ensemble \(\{p_x,\rho_x\}\), arbitrary \(n\)-mode \(\rho_x\), average \(\bar\rho=\sum_xp_x\rho_x\), a purification of each \(\rho_x\) gives the one-block bounds

\[
\tag{Q1} n(C+2Q)\le S(B)+\sum_xp_x[S(\rho_x)-S(E_x)],
\]
\[
\tag{Q2} n(Q+E)\le\sum_xp_x[S(B_x)-S(E_x)],
\]
\[
\tag{Q3} n(C+Q+E)\le S(B)-\sum_xp_xS(E_x),
\]

where \(B_x=\mathcal L_\eta^{\otimes n}(\rho_x)\), \(E_x\) is its complementary output, and \(B=\sum_xp_xB_x\). The region is the closure of the union over all \(n\), after division by \(n\). These are WHG Proposition 1, Eqs. (3)–(5), and De Palma Eqs. (87)–(91). For actual finite-block codes, each bound has the usual \(o(n)\) continuity correction; dividing by \(n\) then taking vanishing error gives the displayed rate bounds.

The primary private source is Wilde–Hsieh, *Public and private resource trade-offs for a quantum channel*, arXiv:1005.3818v3, Theorem 1, Secs. 2–5 and Lemma 6. Public and private communication are **forward** resources. The model gives the environment of a consumed public noiseless channel to Eve. The private channel is confidential from Eve; consumed shared key is initially independent of the public information and Eve. Its source security condition is trace-norm decoupling of the joint private registers from Eve and the entire public transcript, for uniform classical source messages, together with correctness. This is not a semantic-security theorem for arbitrary message priors or adversarially correlated auxiliary information.

For a degradable channel, a pure-state refinement \(\{p_xp_{y|x},\psi_{xy}\}\) with \(\rho_x=\sum_yp_{y|x}\psi_{xy}\) gives

\[
\tag{P1} n(R+P)\le S(B)-\sum_{x,y}p_xp_{y|x}S(B_{xy}),
\]
\[
\tag{P2} n(P+S)\le\sum_xp_x[S(B_x)-S(E_x)],
\]
\[
\tag{P3} n(R+P+S)\le S(B)-\sum_xp_xS(E_x).
\]

These are WHG Proposition 2, Eqs. (19)–(21), and De Palma Eqs. (101)–(106).

There is a 2012 erratum, DOI 10.1007/s11128-012-0451-2. Its introduction and revised theorem statements retract a claim that the generic optimization is a convex program; it revises Theorem 2 of each original paper, not their capacity Theorem 1. This derivation uses the corrected v3 papers and never uses the invalid convex-optimization assertion.

### Coordinatewise justification of the private pure-state refinement

This can be checked without an optimizer or a support-function argument. Start from the general mixed ensemble \(\rho_{xy}\) in the private theorem and spectrally refine it with a new classical variable \(Z\), producing pure \(\psi_{xyz}\), while preserving \(\rho_x\), \(\bar\rho\), and average energy. Adding \(Z\) increases \(I(XY;B)\). Because Eve is degraded from Bob,

\[
I(Z;B|XY)\ge I(Z;E|XY).
\]

Since each refined input is pure, \(S(B|XYZ)=S(E|XYZ)\), so this inequality says \(S(B|XY)-S(E|XY)\ge0\). Consequently all three original private right-hand sides are dominated simultaneously by (P1)–(P3) for the refinement. In infinite dimension the spectral refinement can be countable; conditional sums remain finite by the energy bounds below, and mutual informations are defined by relative entropy, so no finite \(H(XYZ)\) assumption is necessary. Equivalently, approximate finite subsets and pass to their conditional sums.

**Security continuity caution.** The private source paper's sentence following its security condition claims an information leakage bound \(I\le\epsilon\) directly from trace-norm distance \(\epsilon\). That literal dimension-independent implication is false: the continuity correction contains the logarithm of the private-register dimension. The converse needs only an \(o(n)\) correction, which follows from vanishing trace distance with fixed finite asymptotic resource rates. If an absolute mutual-information leakage tending to zero is separately claimed, one must invoke sufficiently rapid decay of the coding error (or separately impose that secrecy criterion); it cannot be obtained from \(\epsilon_n\to0\) alone. Nothing here upgrades the model to semantic security.

## 3. Energy and ensemble hypotheses

For any \(n\)-mode state \(\sigma\) with total mean photons at most \(nM\),

\[
\tag{EM} 0\le S(\sigma)\le\sum_{j=1}^n S(\sigma_j)
\le\sum_{j=1}^n g(\operatorname{Tr}a_j^\dagger a_j\sigma_j)
\le ng(M).
\]

The middle inequality follows from positivity of relative entropy to a one-mode Gibbs state; its optimizer is the thermal state. The last is concavity of \(g\). This proves all input and output entropies below are finite. Pure loss scales total mean photons exactly by its transmissivity.

If \(\operatorname{Tr}H_n\bar\rho\le nN\), nonnegativity and Tonelli give

\[
\sum_xp_x\operatorname{Tr}H_n\rho_x=\operatorname{Tr}H_n\bar\rho<\infty.
\]

Every component with positive probability has finite mean energy in a discrete ensemble; for a general measurable ensemble this holds almost everywhere. No bound \(\operatorname{Tr}H_n\rho_x\le nN\) for every \(x\) is inferred or needed. Concavity of entropy and (EM) give

\[
\sum_xp_xS(\rho_x)\le S(\bar\rho)\le ng(N),
\quad
\sum_xp_xS(B_x)\le S(B)\le ng(\eta N).
\]

The same observation applies after spectral refinement in either converse. It handles unequal per-mode energies, rare high-energy codewords, entanglement between modes, and non-Gaussian states.

## 4. A self-contained convexity lemma

Define \(f_t(s)=g(tg^{-1}(s))\). It is continuous and nondecreasing on \([0,\infty)\). For \(0<t<1\), it is convex. To verify this, constants converting logarithm bases do not affect signs, so take natural logs temporarily. For \(x=g^{-1}(s)>0\), put \(L(x)=\ln(1+1/x)\). Then

\[
f_t'(s)=\frac{tL(tx)}{L(x)},\qquad
f_t''(s)=\frac{t}{xL(x)^3}
\left[\frac{L(tx)}{x+1}-\frac{L(x)}{tx+1}\right].
\]

The second derivative is nonnegative because \(h(u)=(u+1)L(u)\) is decreasing:

\[
h'(u)=\ln(1+1/u)-1/u<0,
\]

and \(tx\le x\). The continuous extension at \(s=0\) remains convex. At \(t=0\), \(f_0=0\); at \(t=1\), \(f_1(s)=s\). Thus Jensen's inequality applies to arbitrary probability weights, not only uniform weights. For \(t>0\), the inverse \(f_t^{-1}\) is increasing and concave.

This replaces the slightly modified thesis corollary cited by WHG with an explicit proof. It does not replace (VE).

## 5. Conditional converse with a single shared parameter

First suppose \(N>0\). Define normalized conditional entropies

\[
s_A=\frac1n\sum_xp_xS(\rho_x),\quad
s_B=\frac1n\sum_xp_xS(B_x),\quad
s_E=\frac1n\sum_xp_xS(E_x).
\]

By Sec. 3, \(0\le s_B\le g(\eta N)\). Hence there is a unique \(\lambda\in[0,1]\) with

\[
\tag{L} s_B=g(\eta\lambda N).
\]

Applying (VE) at \(t=\eta\) to every \(\rho_x\), then Jensen, yields

\[
s_B\ge\sum_xp_x f_\eta(S(\rho_x)/n)\ge f_\eta(s_A).
\]

Since \(f_\eta\) is strictly increasing (\(\eta\ge1/2>0\)), (L) gives

\[
\tag{A} s_A\le g(\lambda N).
\]

The pure-loss complement is \(\mathcal L_{1-\eta}\), up to an output phase rotation. Since \(\eta\ge1/2\), set \(\delta=(1-\eta)/\eta\in[0,1]\). The attenuation composition law gives

\[
E_x\simeq\mathcal L_\delta^{\otimes n}(B_x).
\]

Bob's conditional state has finite mean energy, so a second application of (VE) and Jensen gives

\[
s_E\ge\sum_xp_x f_\delta(S(B_x)/n)\ge f_\delta(s_B)
=g((1-\eta)\lambda N).
\tag{E}
\]

Lastly \(S(B)/n\le g(\eta N)\). Substituting this, (L), (A), and (E) into (Q1)–(Q3) yields precisely the three quantum target bounds, **with the same \(\lambda\)**. This is valid at every block length, so arbitrary entanglement across channel uses does not leave an unbounded regularization gap.

For the private converse use the same \(\lambda\) from (L), the same bound (E), and nonnegativity \(S(B_{xy})\ge0\). Substitution in (P1)–(P3) yields precisely the three private target bounds. The input-entropy estimate (A) is not needed for this part.

If a sequence of codes has asymptotic budget \(N+o(1)\), use that sequence's \(N_n\) and \(\lambda_n\); continuity and compactness give the same limiting region at \(N\). The statement does not need to assume that every finite code already achieves a point on a boundary.

## 6. Achievability and infinite-dimensional approximation

WHG's inner regions require no entropy premise. The quantum seed is the ensemble of purifications of

\[
\rho_\alpha=D(\alpha)\theta_{\lambda N}D(\alpha)^\dagger,
\qquad
\alpha\sim\mathcal{CN}(0,(1-\lambda)N),
\]

where \(\theta_M\) is a thermal state with mean photons \(M\). Its average input is \(\theta_N\). Displacement covariance and the thermal attenuation formula give the four entropies

\[
S(B)=g(\eta N),\quad
\mathbb E S(\rho_\alpha)=g(\lambda N),\quad
\mathbb E S(B_\alpha)=g(\eta\lambda N),\quad
\mathbb E S(E_\alpha)=g((1-\eta)\lambda N).
\]

The private seed is

\[
\alpha\sim\mathcal{CN}(0,(1-\lambda)N),\quad
\beta\sim\mathcal{CN}(0,\lambda N),\quad
\psi_{\alpha\beta}=|\alpha+\beta\rangle\langle\alpha+\beta|,
\]

with independent variables. Conditionally on \(\alpha\), the input mixture is the same \(\rho_\alpha\). Both channel outputs of each coherent state remain pure, so the extra average in (P1) is zero. These identities give all three inner-region bounds exactly at the entropy level.

The operational finite-dimensional coding theorems cannot merely be applied to a continuous alphabet and infinite-rank thermal seed without an approximation argument. The following construction makes the needed approximation precise at the ensemble level.

1. Work first with \(N'<N\), for \(N>0\), so there is an energy margin. Discretize each circular Gaussian by symmetric finite angular and radial quantizers: map the outer tail to zero, round radii downward, and use an even number of equally spaced angles. The quantized variable has zero mean, second moment no larger than the original, and converges almost surely to it as the disk/grid expand/refine. For the private seed, use independent quantizers; then \(\mathbb E|\alpha_m+\beta_m|^2=\mathbb E|\alpha_m|^2+\mathbb E|\beta_m|^2\le N'\). For the quantum seed, the mean energy is \(\lambda N'+\mathbb E|\alpha_m|^2\le N'\).
2. For a fixed finite quantum alphabet, let \(P_K=\sum_{j=0}^K|j\rangle\langle j|\) and replace each mixed input by
   \[
   T_K(\rho)=P_K\rho P_K+\operatorname{Tr}[(1-P_K)\rho]|0\rangle\langle0|.
   \]
   This is a trace-preserving finite-support map, and it never increases photon expectation. Select an arbitrary purification of each resulting finite-rank state. As \(K\to\infty\), the trace distance tends to zero. Pure loss maps the cutoff subspace into the same cutoff subspace at both Bob and Eve, so its restriction is a genuinely finite-dimensional channel with no separate output cutoff.
3. For a fixed finite private alphabet, replace each coherent vector by its normalized projection \(P_K|\alpha_m+\beta_m\rangle\). The state remains pure. The photon distribution is a Poisson distribution conditioned on photon number at most \(K\), whose mean is no larger than the unconditioned mean. The code ensemble therefore still obeys the same average-energy upper bound. The projected vectors converge in norm.
4. All needed entropies converge. At fixed finite alphabet this follows from uniform energy-constrained entropy continuity on oscillator states; at the Gaussian-alphabet limit the average output states converge in trace norm with a uniform mean-energy bound, and the conditional entropy constants have the displayed limits. A suitable explicit source is Winter, arXiv:1507.07775v6, Lemma 15 / Meta-Lemma 16 and its oscillator specialization. Its Gibbs hypothesis is satisfied here because \(\operatorname{Tr}e^{-bH_n}=(1-e^{-b})^{-n}<\infty\) for every \(b>0\). The important condition is a uniform energy bound, not trace convergence by itself.
5. Apply the finite-dimensional father/private-father coding theorem to each fixed finite approximant, preserving the input ensemble's average cost through its standard typical/random code construction. For a fully self-contained constrained coding proof, explicitly check the following cost lemma in that construction: the expected energy of the random average code input is \(\le nN'+o(n)\). Given that lemma, ordinary Markov selection is enough: the proportion of code samples with average energy exceeding \(nN\) is at most \(N'/N+o(1)<1\); expected error/security error tends to zero, so there exist samples satisfying both the energy constraint and vanishing error. Finite cutoff makes the typical-source approximation harmless for cost because the per-mode observable is bounded. No analogous selection can be asserted for a maximum per-codeword constraint from this expectation alone.
6. Let the alphabet and Fock cutoff tend to their limits, then \(N'\uparrow N\), and include rate boundary points through operational closure. The ideal unit-resource protocols act on separate noiseless resource systems and do not add photons to the noisy channel inputs.

**Remaining operational audit item.** Steps 1–4 above are independently checkable. Step 5 requires checking the precise father/private-father random-code construction or invoking an established cost-constrained version; I have inspected the dynamic theorem's use of those protocols and WHG's finite-dimensional extension discussion, but have not independently reconstructed the complete direct coding proof of each underlying father protocol. This is an inherited coding-theorem dependency, not a new entropy gap, and must be cited or verified accurately. WHG's entropy-level achievability argument and De Palma's capacity formulation agree on a mean input constraint. Do not state that the full operational theorem has been formalized.

## 7. Closures, convexity, units, and boundary checks

The parameter union is already closed at fixed finite \(N\): for any convergent sequence of finite rate triples, a subsequence of their \(\lambda\)'s converges in compact \([0,1]\), and all right-hand sides are continuous. The operational closure remains appropriate in the theorem statement. There is no missing convex hull. More explicitly, parameterize by \(s=g(\eta\lambda N)\). The quantum right-hand sides are

\[
g(\eta N)+f_\eta^{-1}(s)-f_\delta(s),\quad
s-f_\delta(s),\quad
g(\eta N)-f_\delta(s),
\]

which are concave in \(s\). The private right-hand sides are constant, \(s-f_\delta(s)\), and \(g(\eta N)-f_\delta(s)\), also concave. Their hypograph feasibility sets are convex, and projection to the rate coordinates preserves convexity. Time sharing therefore fits the displayed union, including mixtures of different \(\lambda\)'s.

| Boundary | Verified behavior |
|---|---|
| \(N=0\) | Nonnegative photon Hamiltonian has a one-dimensional zero-energy space, so every positive-weight channel input is vacuum. Both regions reduce exactly to their unit-resource cones. |
| \(\lambda=0\) | Quantum bounds are \(C+2Q\le g(\eta N)\), \(Q+E\le0\), \(C+Q+E\le g(\eta N)\); private bounds are \(R+P\le g(\eta N)\), \(P+S\le0\), \(R+P+S\le g(\eta N)\). |
| \(\lambda=1\) | Conditional and average thermal input coincide; the three displayed formulas have their literal endpoint values. Displacement randomness is a point mass, not a density with zero variance. |
| \(\eta=1/2\) | Bob and Eve channels coincide up to a phase, \(s_E=s_B\), so \(Q+E\le0\) and \(P+S\le0\). For the private region \(\lambda=0\) dominates the union. The quantum first inequality still needs (VE) at \(t=1/2\). |
| \(\eta=1\) | Complement is vacuum and Bob receives the input. Quantum union is dominated by \(\lambda=1\): \(C+2Q\le2g(N)\), \(Q+E\le g(N)\), \(C+Q+E\le g(N)\). Private union is dominated by \(\lambda=1\): each of \(R+P,P+S,R+P+S\) is at most \(g(N)\). |
| Units | WHG rates use bits/qubits/ebits. De Palma defines \(g\) with natural logarithms and uses nats in its plots. Converting every entropy by \(1/\ln2\) gives the same formulas; mixing those conventions produces a systematic factor error. |

For \(N=0\), the quantum cone has generators \((-2,1,-1)\), \((2,-1,-1)\), \((0,-1,1)\), with respective nonnegative weights \(-(C+Q+E)/2\), \(-(Q+E)/2\), \(-(C+2Q)/2\). The private cone has generators \((-1,1,-1)\), \((1,-1,0)\), \((0,-1,1)\), with weights \(-(R+P+S)\), \(-(P+S)\), \(-(R+P)\). This verifies exact sufficiency of each zero-energy cone, including negative resource coordinates.

## 8. Exact gaps and exclusions

* The central unresolved project dependency is the unconditional validity of (VE) for arbitrary finite-energy entangled multimode states. A valid single-mode theorem, a Gaussian-only theorem, a quantum entropy-power bound with a different function, or a formally verified scalar inequality is insufficient.
* I have not inspected or validated upstream family 273 in this subtask. No claim about that source's proof, Lean scope, assumptions, or priority is made here.
* The clean reduction is already present in substance in WHG 2012 and explicitly in De Palma 2019 Theorem 11 / Corollary 12. If (VE) becomes available, exact dynamic regions are an immediate previously conditional consequence. Their formulas and proof machinery are not new.
* Finite-energy inputs suffice for the specified average-energy capacity converse; infinite-mean inputs are excluded by the model. There is no route here to unconstrained thermal-channel quantum capacity.
* These bounds do not address two-way-assisted capacities, ordinary single-resource pure-loss capacity novelty, amplifier capacities, ordinary classical broadcast novelty, or confidential broadcast for \(\eta<1/2\).
* The saved quantum adversarial audit was read. Its \(\eta=0\) common-message counterexample excludes blindly importing the confidential-broadcast low-transmissivity branch. No confidential-broadcast or additive-noise extension is used in this core derivation.
* A new full-publication candidate must undergo independent checks of the entropy proof, priority, direct coding/energy lemma, exact manuscript, and final package; this subtask alone is not publication clearance.

## 9. Primary references and versions actually read

1. WHG, *Quantum trade-off coding for bosonic communication*, Physical Review A **86**, 062306 (2012), DOI 10.1103/PhysRevA.86.062306. Author-hosted final PDF: https://www.markwilde.com/publications/PhysRevA.86.062306.pdf . Read Propositions 1–2; Theorems 3 and 7; Sections III.G–H; their primary coding citations.
2. G. De Palma, *New lower bounds to the output entropy of multi-mode quantum Gaussian channels*, arXiv:1805.12469v3 (2019), IEEE Trans. Inf. Theory **65**, 5959–5968, DOI 10.1109/TIT.2019.2914434. https://arxiv.org/abs/1805.12469v3 . Read Conjecture 1, Theorem 11, Corollary 12, and Eqs. (87)–(106). The word “Gaussian” there describes the underlying quantum system/channel; the input states in the multimode premise are arbitrary.
3. M. M. Wilde and M.-H. Hsieh, *The quantum dynamic capacity formula of a quantum channel*, arXiv:1004.0458v3 (25 June 2012), Quantum Inf. Process. **11**, 1431–1463, DOI 10.1007/s11128-011-0310-6. https://arxiv.org/abs/1004.0458v3 . Read operational model, Theorem 1, catalytic converse, and pure-state refinement.
4. M. M. Wilde and M.-H. Hsieh, *Public and private resource trade-offs for a quantum channel*, arXiv:1005.3818v3 (25 June 2012), Quantum Inf. Process. **11**, 1465–1501, DOI 10.1007/s11128-011-0317-z. https://arxiv.org/abs/1005.3818v3 . Read operational/security model, Theorem 1, catalytic converse, and Lemma 6.
5. Wilde–Hsieh erratum, Quantum Inf. Process. **11**, 1503–1509 (published online 7 August 2012), DOI 10.1007/s11128-012-0451-2. Publisher PDF: https://link.springer.com/content/pdf/10.1007/s11128-012-0451-2.pdf . Read introduction and revised theorems; correction concerns generic convex optimization.
6. A. Winter, *Tight uniform continuity bounds for quantum entropies: conditional entropy, relative entropy distance and energy constraints*, arXiv:1507.07775v6 (12 January 2016), Commun. Math. Phys. **347**, 291–313, DOI 10.1007/s00220-016-2609-8. https://arxiv.org/abs/1507.07775v6 . Read bounded-energy Gibbs hypothesis and oscillator continuity lemmas.

Accessed 2026-10-06 Pacific. Private research source downloads are in `sources/`; they are third-party materials, not automatically approved for redistribution in a publication package. `SOURCE_HASHES.sha256` identifies the bytes read. No external individual was contacted.
