# Source and prior-attempt audit

Checked on 30 September 2026. The mathematical artifact is a scoped unresolved attempt, not a literature-completeness or novelty certificate.

## Exact source

The assigned `https://www.unsolvedmath.com/problems/30003390` did not return usable content. The complete pinned record was read instead, followed by the full official [OWR 9/2017](https://ems.press/content/serial-article-files/46671). The relevant Hefter–Jentzen contribution occupies printed pp.466–469. Its p.467 was also rendered to verify the absolute-value bars, infimum over Borel functions, equidistant Brownian observations, and initial value $x\ge0$. The conjecture follows equation (4) on p.468. The dataset's prose year 2018 conflicts with its correct 2017 DOI.

The target is terminal mean absolute error on the same probability space and with the same scalar Brownian driver. It is not distributional simulation, weak error, a supremum-path norm, adaptive observation, or fractional Brownian motion. The dimension is $\delta=4a/\sigma^2$, while many papers call $\delta/2$ the Feller index.

## Prior-attempt and duplicate gate

The checkout began from main `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`. The live eligible queue contains rank 187, ID 30003390, queued with 0/5 attempts. Exact-ID branch and all-state PR checks found no prior campaign branch or PR; the tracked attempt path and exact-ID history checks were empty. Related-target metadata had no entry for this ID. A broad repository grep was interrupted and is not counted as a completed exhaustive content search; completed targeted history/path and queue checks are the evidence used here.

The pinned full corpus was searched for Cox–Ingersoll–Ross, Cox-Ingersoll-Ross, squared Bessel, and CIR process formulations: this was the only matching problem. The pinned research-results dictionary has no exact problem-number entry; `prior_imported_report.json` records that absence. The dataset's own dated literature triage is retained unchanged in `source_record.json`, rather than treated as an attempted proof.

## Retrieved primary papers and exact use

1. [Hefter–Jentzen, arXiv:1702.08761v2](https://arxiv.org/abs/1702.08761): full PDF retrieved. Theorem 1 covers the boundary lower bound for $0<\delta<2$, all source initial values. Corollary 2 gives exact two-sided bounds for $0<\delta<1$. This is the CIR lower-bound paper incorrectly identified by the dataset's other arXiv link. Later publication in Finance and Stochastics 23 (2019), 139–172 is corroborated by the author's publication list; the final journal PDF was not compared line by line.
2. [Hefter–Herzwurm, arXiv:1608.00410v1](https://arxiv.org/abs/1608.00410): full PDF retrieved. Theorem 2 is the precise $L^1$ bound, with a logarithm only at $\delta=1$; Theorem 3 verifies the truncated Milstein assumptions. This is stronger in $L^1$ than merely reading the epsilon-loss abstract. The stochastic interpolation and observation conventions were checked. The full technical proof is credited, not independently re-certified here.
3. [Hefter–Herzwurm, arXiv:1601.01455v1](https://arxiv.org/abs/1601.01455): full PDF retrieved. Proposition 1 supplies the same-driver reflected-Brownian formula; Theorems 2–3 and Corollary 1 establish the dimension-one, zero-reversion sharp rate. Remark 7 concerns a stronger supremum-path norm for nonzero reversion. Its adaptive super-polynomial result is explicitly kept separate. The new note's finite-grid median computation is a direct elementary use of the known representation and Brownian reflection.
4. [Hefter–Herzwurm–Müller-Gronbach, arXiv:1710.08707v1](https://arxiv.org/abs/1710.08707): full PDF retrieved. Section 7.1.1, Corollary 14 and the following discussion give the local noncommutativity lower bound and the known $\delta>4$ sharp regime. The displayed initial-value restriction $x>0$ is preserved. The singular exception $\delta=1,b=0$ is not discarded. This is not a Hefter–Jentzen paper.
5. [Alfonsi, arXiv:1206.3855v1](https://arxiv.org/abs/1206.3855): full PDF retrieved. Theorem 2 requires $x>0$ and $a>\sigma^2$; it is not a full-Feller-range order-one theorem. Its continuous-time interpolation uses Brownian values between grid points, but its terminal value uses only the grid, as required here. The preprint's printed compilation date does not replace its arXiv submission or journal publication chronology.
6. [Deng–Fei–Fei–Mao, arXiv:2410.05614v1](https://arxiv.org/abs/2410.05614): full PDF retrieved; Section 4.3 and Corollary 4.6 checked. The displayed CIR results require Feller index greater than five. Their general positivity-preserving title and abstract do not close the original intermediate-parameter question. No full proof audit of this paper is claimed.
7. [Pavlis–Çetin, arXiv:2607.07552v1](https://arxiv.org/abs/2607.07552): full PDF retrieved; its theorem studies weak payoff error. Its introductory summary of earlier strong results is not substituted for the earlier theorems' exact hypotheses. No strong-rate consequence is imported.

## Current-source access hold

[Hefter–Herzwurm–Ritter, Journal of Complexity 90 (2025), 101959](https://doi.org/10.1016/j.jco.2025.101959) is a relevant later primary paper. The publisher abstract explicitly announces a new CIR upper bound through reflected Ornstein–Uhlenbeck approximation. Crossref confirms its identity and publisher article PII S0885064X25000378. The publisher full page/PDF/API attempts did not return usable full text; OpenAlex and Semantic Scholar exposed no alternate deposited PDF. The exact theorem is therefore **not independently checked** here. This qualification is especially important for any claim about the best current dimension-one, nonzero-reversion bound.

The publisher's [March 2026 Journal of Computational Finance issue](https://www.risk.net/journal-of-computational-finance/volume-29-number-4-march-2026) describes Tang's projected Euler–Maruyama paper as an order-one-half strong result over a broad parameter regime. Its full paper was not audited, and it is not used as a rate theorem.

The search did not produce a verified full-range solution. This is not proof that no such result exists. The artifact states a verified baseline and exact elementary information formulas, while retaining the unresolved full target and the later-source access limitation.

## Verification and ownership

The source PDFs and rendered source image remain in the adjacent research cache and are not copied into the repository package. `source_manifest.json` records URLs and SHA-256 values. The checker uses only exact rational or symbolic controls and does not infer a stochastic rate from simulation. Model: gpt-6-astra at xhigh. Two substantive approaches are recorded; queue changes are owned by the parent task.
