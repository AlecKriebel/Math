# Post-freeze cross-family challenge

Target: the other priority family's REPORT.md and VERDICT.json, frozen 2026-10-17 18:28:01 UTC. This challenge began **after** my independent report was frozen in freeze_20261017T183121Z. That frozen report and its manifest were rechecked and remain unchanged.

Target identities:

- REPORT.md SHA-256: \`0f82bb3a8409b98efb52af4d0c741ae7b9341fe22c9e74888a5f791602c80f6d\`.
- VERDICT.json SHA-256: \`414c93b68eb2c6eded03f915e7d1e6d29f8e7e4adb402db401580b3d743dd577\`.

## Decision

**The mathematical prior-implication verdict survives this challenge.** Both Nikula's theorem and the earlier Bayart–Matheron Proposition 3.3 specialize correctly to the required IID complex-Gaussian derivative jets. The older general theorem route is applicable to the Fréchet space \(H(\mathbb C)\); it does not rely on a Banach-only theorem or on treating an unspecified Gaussian measure as having IID jets.

**One source-date statement needs qualification:** the target report calls the later internal Nikula date “TeX-generated” and a “compilation date.” The current PDF's internal date and creation metadata were observed, but the cause has not been authenticated. A possible automatic recompilation should be presented as an explanation, not as an established fact. This correction does not affect the positive pre-project literature overlap.

The historical first explicit multiplier-disproof date is still unestablished. A general theorem's dated availability and an audit's present deduction do not by themselves show when the corollary was first explicitly recognized.

## 1. Nikula route challenged

My independently frozen report and its separately adversarial [verification](verification/VERIFICATION.md) already checked the source and the full implication before any cross-family access. The target agrees on the following points:

- Theorem 1 in the inspected [version-specific arXiv PDF](https://arxiv.org/pdf/1209.6209v1), pp. 2–3, requires IID complex coefficients with full-plane support and a logarithmic tail bound. A circular complex Gaussian meets both hypotheses; a real Gaussian would not meet full-plane support.
- The conclusion is almost sure entire convergence and **frequent** differentiation hypercyclicity. No stronger tail/moment condition from the paper's separate growth theorem is needed.
- The probabilities \(1-e^{-r^2}\) and \(e^{-R^2}\) make the lower \(n^{-3/4}\) and upper \(\log(n+e)\) exceptional events summable.
- One eventual coefficient event implies, deterministically for any \(p\) of degree \(d\ge1\), a leading contribution of size \(\gtrsim_p n^{d-3/4}\) and a smaller \(O_p(n^{d-1}\log n)\) remainder. This handles \(d=1\), phases, arbitrary complex coefficients, and all polynomials without an uncountable probabilistic intersection.
- Adding any polynomial leaves the sufficiently high derivative orbit and the sufficiently high product jets unchanged. Thus a single good \(F\) gives the dense affine family \(F+\mathbb C[z]\). A full-support proof of the Gaussian law is also valid but not needed for this particular density argument.
- The raw Gaussian lower bound \(n^{-1/2}\) fails infinitely often almost surely. The target correctly distinguishes it and uses a null-orbit coefficient correction. Its replacement by the positive-real threshold has error at most \(2n^{-1/2}\), which is sufficient; radial projection would improve the constant but is unnecessary.

The target's clipping statement is an **eventual** annular-existence/density conclusion. It need not be read as fixed-\(M\) relative density. My separately frozen argument additionally proves fixed-\(M\) relative density by clipping into each full annulus and checking full relative support. These are compatible scopes.

## 2. Exact Bayart–Matheron Proposition 3.3 specialization

### Actual source and scope

Independently acquired [arXiv:1112.1289v1](https://arxiv.org/abs/1112.1289), whose official version record dates it to **6 December 2011, 14:35:24 UTC**. The current version-specific PDF has SHA-256
\[
\texttt{876a1afbb75181a96e91d262468ef397b4beb3b73ec3e949df4e88c86efb16bd}.
\]

For this cross-challenge I additionally read the mixing definitions on PDF pp. 8–10, the section-wide Fréchet context and Gaussian definitions on pp. 11–13, the eigenfield definitions and complete Proposition 3.3 on pp. 14–15, and its proof/context through p. 17. Proposition pages 14–15 were rendered and visually inspected. This is additional post-freeze source inspection, not a retroactive change to the independent audit's recorded scope.

The beginning of Section 3 expressly fixes a **separable complex Fréchet space** \(X\). Proposition 3.3 assumes a norm-closed ideal \(\mathcal S\subset\ell^\infty(\mathbb Z_+)\), an eigenfield \((E,\phi)\), a gamma-radonifying integral operator \(K_E\), \(m\)-spanning, and \(\mathcal S\)-continuity of all required image measures. It asserts mixing for the **specific** law \(\mu_{K_E}\). The nearby Banach type/cotype results are not hypotheses of this proposition.

### Hypothesis-by-hypothesis calculation

Set \(X=H(\mathbb C)\), \(T=D\), \(\Omega=\mathbb T\), \(m\) normalized Haar measure, \(\phi(\lambda)=\lambda\), and
\[
E(\lambda)(z)=e^{\lambda z},\qquad
K_Eu(z)=\int_{\mathbb T}u(\lambda)e^{\lambda z}\,dm(\lambda).
\]

1. **Space and operator.** \(H(\mathbb C)\) is separable and complete for compact-open disk seminorms, and differentiation is continuous by Cauchy estimates. It is within the proposition's stated Fréchet scope.

2. **Measure space and integration.** Haar probability is sigma-finite and its \(L^2\) space is separable. The field \(E\) is continuous with \(\|E(\lambda)\|_R\le e^R\); it is measurable and square-integrable for every defining seminorm. For \(u\in L^2(m)\),
\[
\|K_Eu\|_R\le e^R\|u\|_{L^1(m)}\le e^R\|u\|_{L^2(m)}.
\]
The integral may also be defined by its uniformly convergent exponential expansion, so its existence as an entire function and continuity into the Fréchet space are explicit.

3. **Eigenfield and intertwining.** \(DE(\lambda)=\lambda E(\lambda)\); bounded compact convergence permits differentiation under the displayed integral. Hence \(DK_E=K_EM_\phi\), with the correct domains.

4. **Fourier signs and the exact law.** With \(e_k(\lambda)=\lambda^k\), \(k\in\mathbb Z\), an orthonormal basis for complex \(L^2(m)\), the source's integral contains **no complex conjugation on \(u\)**. Therefore
\[
K_Ee_k=
\begin{cases}
z^{-k}/(-k)!,&k\le0,\\
0,&k>0.
\end{cases}
\]
Using \(\bar\lambda^n\) for the surviving basis vectors gives the same formula indexed by \(n\ge0\). Enumerate all integers in any order. In the corresponding Gaussian series, the coefficients attached to nonzero images are a subsequence of independent standard **complex** Gaussians, hence remain IID with real and imaginary variances \(1/2\). Thus
\[
\mu_{K_E}=\operatorname{Law}\left(\sum_{n\ge0}g_nz^n/n!\right).
\]
No assertion about a generic Gaussian law was substituted for this computation.

5. **Gamma-radonifying in the Fréchet topology.** For each integer radius \(R\),
\[
\sum_{k\in\mathbb Z}\|K_Ee_k\|_R=\sum_{n\ge0}R^n/n!=e^R.
\]
Consequently
\[
\mathbb E\sum_{k\in\mathbb Z}|g_k|\|K_Ee_k\|_R
=\mathbb E|g_0|\,e^R<\infty.
\]
Tonelli gives almost sure absolute convergence in each seminorm; intersecting over integer radii gives compact-open convergence in the complete space. This is exactly the source's gamma-radonifying criterion. It also removes any issue about ordering the two-sided Fourier basis.

6. **Spanning and full support.** The range contains every monomial \(z^n/n!\), so it is dense. The source explicitly equates dense range with \(m\)-spanning for \(K_E\), and identifies the Gaussian support as the closed linear span of its coefficient vectors. Both the required spanning hypothesis and full support therefore hold. A direct check is also available: a continuous functional annihilating \(E(\lambda)\) off a Haar-null set annihilates the entire analytic function of \(\lambda\), hence every monomial.

7. **Fourier-decay hypothesis.** Set \(\mathcal S=c_0(\mathbb Z_+)\), a norm-closed ideal of \(\ell^\infty\). For every \(u\in L^1(m)\), \((u m)\circ\phi^{-1}=u m\); its Fourier coefficients tend to zero by the Riemann–Lebesgue lemma. This is exactly \(\mathcal S\)-continuity, including arbitrary complex \(u\).

Proposition 3.3 applies to this specific \(\mu_{K_E}\). The source's Definition 2.1 identifies \(c_0\)-mixing as strong mixing; hence the measure is invariant and ergodic. For a countable topological base of nonempty open sets \(U_j\), full support gives \(\mu_{K_E}(U_j)>0\). The pointwise ergodic theorem applied to their indicators gives positive visit frequencies simultaneously for all \(j\), on one probability-one event. Thus almost every sample of precisely the IID Gaussian series is frequently \(D\)-hypercyclic. The independently verified Gaussian coefficient argument then applies unchanged.

There is no missing local boundedness, Banach geometry, covariance, normalization, IID-law, or Fréchet integration assumption in this specialization.

The source's p. 17 proof has an apparent dimensionally invalid intertwining expression. The correct identity is stated on p. 14 and was computed directly in item 3 above. This typographical issue does not create a gap in the stated proposition's specialization.

## 3. Dating and framing corrections

The target report's phrase “a later TeX-generated date” asserts a cause for the observed Nikula internal date. The source evidence establishes only that the currently served v1 PDF displays “Date: August 2, 2018,” that its PDF metadata is later, and that the official version record dates v1 to September 2012. It does not authenticate why. Correct the reusable project account to:

> The official repository dates v1 to September 2012; the currently served v1 PDF also has a later internal date. The reason for that discrepancy was not independently authenticated.

This does not claim a byte-identical historical PDF. The publisher's independent 2013/2014 publication dates and the 2011 Bayart–Matheron versioned general theorem are adequate to establish pre-project implication.

The 51-page author-hosted Bayart–Matheron file's later explicit remark about this Gaussian model and Nikula remains **undated for this audit**. The verified older route uses Proposition 3.3 in the separately inspected 47-page v1, not that later remark. No later statement is backdated.

The proposed project framing—an attributed historical negative answer and a self-contained elementary Baire proof, with no firstness, new-existence or current-openness claim—is consistent with both independent priority audits and this challenge. Novelty of the fine fixed-polynomial null-orbit-coset refinement remains unestablished.

## 4. Post-freeze integrity and scope

This challenge changes neither family's frozen report. Source images created during it remain in ignored \`sources/\`. Exact cross-challenge inputs, expanded inspection scope and final verification status are recorded separately in CROSS_FAMILY_CHALLENGE.json. No Git, publication, external edit, contact or outreach draft was performed.

