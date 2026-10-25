# Complete independent adversarial upstream-dependency review

**Verdict: PASS_UPSTREAM_REQUIRED_VE.** The full central proof in the pinned 32-page upstream paper survives this independent adversarial audit. I found no substantive error or unresolved central gap. The required finite-block vacuum-port entropy inequality is supported for every finite number of modes, every finite-energy input, arbitrary entanglement among its modes, an independent vacuum port, and every transmissivity in [0,1]. This conclusion follows from checking the proof, not merely matching theorem statements.

Completed: 2026-10-25 UTC. Audit assignment completion: **100%**. Review family: upstream adversarial; model preference: GPT-6.1 Sol Ultra, as assigned by the parent; no descendant agents.

## Claim, evidence identity, and independence

The exact downstream dependency is

\[
\frac1n S\!\left(\mathcal L_t^{\otimes n}(\rho)\right)
\ge g\!\left(tg^{-1}\!\left(S(\rho)/n\right)\right),
\qquad n\in\mathbb N,\quad \operatorname{Tr}\rho N<\infty,\quad t\in[0,1].
\]

The vacuum environment is independent of ρ; ρ may have arbitrary internal multimode entanglement. g(r)=(r+1)log(r+1)−r log r uses natural logarithms. The proof checked actually establishes the stronger finite-energy two-independent-input EPnI in upstream Theorem 1.1, with the necessary vacuum statement as a direct specialization.

The source is OpenAI, *The entropy photon-number inequality*, September 24, 2026, from official revision `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, path `preprints/The-entropy-photon-number-inequality-September-24-2026/paper.pdf`. Its SHA-256 is

`d826f8ebe18596419871100e79611868dff2a45a4aa157433c58e6f49a234d82`.

The full 32-page PDF text was read, including all central §§3–6, the finite-energy preliminaries, all boundary arguments, and the broadcast section and references. The same-commit TeX was independently acquired into this review's `inputs/tex` directory. Central sections 2–6 were read in their exact TeX form as well. See `READ_LEDGER.json`, `acquisition_receipts.json`, and `HASH_SEAL.json` for precise ranges, source identities, acquisition dates and file hashes.

No sibling upstream analytic/current review or historical upstream audit report was read. No favorable report, external theorem label, finite-dimensional numerical experiment, or compilation claim was treated as proof. No external individual was contacted and no outreach was prepared. Original sources were read only. No Git, release, Sheet, site, UI or deployment operations were performed.

## Adversarial audit outcomes

| Attack family | Source locator | Direct check | Outcome / exact remaining gap |
|---|---|---|---|
| Illegal noncommutative interpolation | §3.1, equations (3.5)–(3.7); Theorem 3.1 | Reconstructed parallel-sum source minimization and target inequality without assuming L_i commutes with multipliers. Checked identity-tail finite-parameter tests and target Fatou limits. | Survives. No gap identified. |
| Unsupported Stieltjes property | §3.2, Lemma 3.2, equations (3.10)–(3.16) | Checked the proper conformal inverse domain, no-critical-point sign, branch continuation at s=1, two Herglotz representations, positivity/nonvanishing of sG(s), and measure integrability. | Survives. The derivative property is proved, not inferred merely from scalar monotonicity or Pick character. |
| Scalar interpolation singularities | §3.3, equations (3.17)–(3.20) | Recomputed the scalar quadratic minimum for x²≠y², x=y, x=−y and x=y=0. | Survives. No missing diagonal or antidiagonal case. |
| Hypothetical violation lost in regularization | §4.1, equations (4.1)–(4.3) | Checked finite-support witness approximation, entropy-zero boundary, positive thermal slack and the parameter order. | Survives. κ's later bound uses only already fixed parameters. |
| Nonattainment or insufficient Gibbs domains | §§4.2–4.3, Lemma 4.1, Proposition 4.2 | Reconstructed energy coercivity, fourth-moment lower semicontinuity, cross-entropy majorant, exact log identity and the W^7 Gibbs bootstrap from the form eigen-equation. | Survives. Higher-moment bounds need not be uniform in ζ. |
| Formal Hessian differentiation | §4.4, equations (4.8)–(4.12), Proposition 4.3 | Checked finite input eigenblock perturbations, finite output test partition function, dual optimization and all h_i, λ_i, w_i, κ coefficients. | Survives. No differentiability claim on arbitrary infinite-dimensional output perturbations is needed. |
| Hidden mode independence / projection error | §5.1, equations (5.1)–(5.4) | Checked orthogonal one-port projections in both arithmetic norms and the exact interpolation hypotheses on centered matrix tests. | Survives. Product structure is used across input ports only. |
| Defect norm or weak commutator error | §5.2, Lemmas 5.2–5.3, equations (5.5)–(5.8) | Recomputed spectral defect representative, absolute logarithmic summability and weak trace convolution; checked the complex conjugate of μ in TeX. | Survives. Finite energy justifies weak traces without assuming bounded Z preserves d's domain. |
| Wrong mixture estimate / missing means | §5.2, Proposition 5.4, equations (5.9)–(5.10) | Recomputed mixture variance, the scalar logarithmic-mean comparison, dual norm triangle inequality, and Young bound on κ. | Survives. The separate mean term is retained and controlled. |
| Formal unbounded generator calculus | §6.1, Lemmas 6.1–6.2, equations (6.1)–(6.6) | Checked bounded factors around W³ρW³, weighted cutoff and partial-trace continuity, logarithmic slicing, and absolutely convergent eigenbasis expansion. | Survives. Stationarity is algebraic pairing of an exact Gibbs identity. |
| Wrong cancellation / uncontrollable moment penalty | §6.2, equations (6.7)–(6.12) | Recomputed energy drift, quartic drift leading coefficient −4, centered mixture energy and the full signed cancellation. | Survives. Both defect and mean squares vanish with ζ. |
| Compactness assumes energy or mean convergence | §6.2, equations (6.13) and following | Passed weak identities using fixed finite number-basis tests, then independently solved the full multi-index recurrence. | Survives. Trace-norm compactness plus uniform energy and entropy continuity suffices. |

The detailed derivations are in `DERIVATIONS.md`, including the mechanism and all essential constants for each row. These notes are the main checkable artifact; the table is only an index.

## Strongest verified result and exact logical closure

The audited proof derives the two-input EPnI for every finite n and finite-energy independent ports. It includes arbitrary correlations and entanglement within each port. The exact final mechanism is:

1. A strict violation yields regularized minima with J_ζ≤−c for fixed c>0, uniformly for sufficiently small ζ.
2. The four-weight interpolation supplies the precise thermal metric at those minima, rather than a universal channel inequality assumed without proof.
3. The Gibbs logarithm identity, weighted generator covariance and the centered-energy identity give

   `0 = ||q_0||_*² − (1+ε)A_*² − εM_*² − κ(1−κ)|μ_γ|² + ζP`.

4. The checked defect estimate and a uniform upper bound on P give `(ε/2)(A_*²+M_*²) ≤ Cζ`.
5. A trace-norm input subsequence therefore has vanishing weak thermal defects and means. The number-basis recurrence forces both entire n-mode limit states to be their fixed thermal references.
6. Output thermal mixing and entropy continuity make the entropy part of J_ζ tend to zero; both penalties are nonnegative. Thus liminf J_ζ≥0, contradicting J_ζ≤−c.

The argument never needs convergence of the energies, convergence of unbounded first moments, two-sided positivity of ρ+tLρ, uniform high moments as ζ vanishes, or vanishing of the penalties themselves. I specifically tested whether any of those stronger unsupported claims was hidden in the limiting step and found it was not.

Setting the independent second input to vacuum yields the exact VE statement above, since g^{-1}(0)=0. At t=0 and t=1 the outputs are respectively vacuum and input, giving equality. At zero input entropy the bound reduces to nonnegative entropy. Finite energy ensures finite input and output entropies throughout. No conditional substitution for the required published conclusion is being proposed.

**Exact remaining gap in this audited upstream proof: none identified.** This is a positive mathematical proof audit, not machine-checked formal verification. No Lean compilation was attempted or claimed. No claim is made outside the source's finite-energy, finite-mode, independent-port scope.

## Reproducible controls and negative controls

Run `python3 verify_controls.py` from this folder. It uses only the Python standard library. The result file is `control_results.json`.

* Exact rational polynomial algebra verifies the stationarity cancellation. Perturbing the energy penalty gives the nonzero residual `−Delta*E − Delta*M`, so the control detects a materially wrong coefficient.
* Exact rational polynomial expansion verifies that the fourth-moment drift has N-degree four and leading coefficient −4 for symbolic n,r. Its potentially dangerous N^5 terms cancel.
* Scalar interpolation checks include x=y, x=−y, x=y=0 and unequal signed values. Doubling the additional E weight produces a detected nonzero residual.
* A faithful noncommuting 4×4 density operator with a nonzero annihilation mean checks the entropy-production/defect identity directly. Correcting for finite Fock CCR gives a residual about −4.44×10^{-16}. Incorrectly using infinite CCR gives residual 0.7, exactly the predicted top-number boundary term. This guards against falsely promoting a finite cutoff computation into evidence for the universal theorem.

These computations are transcription and falsification controls. The universal result rests on the checked analytic derivations, not a numerical PASS or finite sampling.

## Publication relevance and exclusions

This review closes the previously unexamined upstream-proof dependency for the required VE use in the capacity paper. It does not independently re-audit the capacity paper's coding/security deductions, which were outside this assigned family and were not used as premises here. It also does not establish priority, novelty of the downstream paper, external acceptance, or any infinite-energy extension. Within the exact necessary theorem scope, I recommend that the parent treat the upstream proof as positively audited, subject to independent cross-family adjudication.
