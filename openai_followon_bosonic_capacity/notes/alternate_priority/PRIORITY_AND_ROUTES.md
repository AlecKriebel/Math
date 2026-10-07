# Exact scope and independent primary-literature audit

Audit date: 2026-10-06, America/Los_Angeles. This is a scoped literature audit, not a certificate that all public work has been found or that a release theorem is correct. Searches used “multimode constrained minimum output entropy,” “quantum-limited attenuator trade-off,” “pure-loss dynamic capacity,” and “entropy photon-number inequality,” including date and arXiv-domain restrictions. Exact primary statements and selected proofs were inspected; abstracts alone were not certification.

## Strongest present conclusion

The exact dynamic formulas and their reduction to sharp multimode entropy are inherited published results. Inspected pre-release literature leaves the unrestricted finite-energy multimode input unresolved. A valid #273 makes the capacity formulas carefully attributed consequences of that input plus established coding/converse machinery. This project must not claim discovery of the formulas or an independent solution of EPnI.

Quantum formula: Eq. (78) of [De Palma 1805.12469v3](https://arxiv.org/html/1805.12469v3). Public/private/key formula: Eq. (79), with beta in [0,1],

\[
C+P\leq g(\eta N),\quad P+K\leq g(\eta\beta N)-g((1-\eta)\beta N),\quad C+P+K\leq g(\eta N)-g((1-\eta)\beta N).
\]

De Palma presents C,P>=0 and K real; negative K means net key consumption. Full net-resource orthants must be matched to Wilde–Hayden–Guha, rather than inferred from this slice. His quantum presentation similarly uses C,Q>=0 and real net entanglement generation G. His logarithms are natural; changing entropy/rates together gives bits.

## Dated primary source ledger

| Inspected source/version | Public arXiv submission; last version | Exact inspected scope | Implication |
|---|---|---|---|
| [Wilde–Hayden–Guha 1105.0119v4](https://arxiv.org/abs/1105.0119v4), PRA 86, 062306 | 2011-04-30; v4 2012-11-22 | Conditional pure-loss dynamic regions, assigned Sections III.G–H | Formulas and reduction are inherited. V2 history reports adding EPnI-based optimality. Earliest appearance of every formula not assigned without comparing versions. |
| [De Palma–Trevisan–Giovannetti 1705.00499v1](https://arxiv.org/html/1705.00499v1) | 2017-05-01; v1 only | Theorem 11, Eqs. (40)–(41): arbitrary n, input diagonal in some product basis | Classical correlations in the basis allowed; arbitrary entangled/non-diagonal inputs excluded. |
| [De Palma 1805.12469v3](https://arxiv.org/html/1805.12469v3), IEEE TIT 65, 5959–5968 | 2018-05-31; v3 2019-07-30 | Corollary 5: sharp entanglement-breaking bounds; Theorem 6: weaker unrestricted bounds; Theorem 11 / Corollary 12: entropy-to-capacity reduction | Precise finite-average-energy reduction, but no sharp pure-loss premise. |
| [Beigi–Rahimi-Keshari 2311.09572v2](https://arxiv.org/html/2311.09572v2), AHP 26, 2737–2778 (2025) | 2023-11-16; v2 2024-09-28 | Theorem 11: one-mode CMOE; conclusion explicitly leaves multimode case open | Tensorization of central functional would be a new proof, not existing input. |
| [Falco–De Palma 2410.14472v2](https://arxiv.org/html/2410.14472v2), IEEE TIT 2025 | 2024-10-18; v2 2025-07-07 | Eq. (13), Theorem III.1: conditional exponential EPI for general linear mixing | Unconditional vacuum specialization weaker than photon-number bound. |
| [Beigi–Mehrabi 2504.02206v3](https://arxiv.org/html/2504.02206v3), CMP 407, article 199 (2026) | 2025-04-03; v3 2026-08-04 | Theorem 1: subset-convolution exponential entropy powers, finite second moments | Resolves different Guha conjecture, not sharp g-inverse CMOE. |
| [Ji 2608.17239v1](https://arxiv.org/html/2608.17239v1) | 2026-08-18; v1 inspected | Theorems 1–2: single-mode one-shot Holevo optimum; Scope and supplement section 13 withhold additivity | Does not duplicate arbitrary-block target; correctness of its central claims not endorsed here. |
| [Li 2609.40061v1](https://arxiv.org/html/2609.40061v1) | 2026-09-30; v1 inspected | Theorems 1–2: qEPI equality classes; Section 1.1 distinguishes stronger EPnI | Equality for weaker bound not minimum for unequal entropy; proof correctness not needed for scope distinction. |
| OpenAI #273, assigned pinned snapshot | manuscript label 2026-09-24; public release identified 2026-10-06, provenance audit pending | Claimed finite-energy EPnI / thermal attenuation; ordinary classical broadcast; excluded quantum/dynamic/wiretap/additive noise | Public release time requires repository records; source correctness is separate mandatory gate. |

The [QIQCOP entry](https://qiqc-op.com/problem/op_3cd14aef409b226b/), last edited 2026-09-04, describes the multimode constrained pure-loss statement as open and points to the same chain. It is a discovery aid, not technical evidence or priority certification.

## Conditional reduction precisely extracted

Define A_tau as vacuum attenuation and f_tau(s)=g(tau g^{-1}(s)). De Palma Theorem 11 assumes S(A_tau^{tensor n}(rho))>=n f_tau(S(rho)/n) for every finite-average-energy n-mode rho and requires f_tau increasing/convex. For tau>0 it is strictly increasing; at tau=0 it is constant zero, and no inverse is needed for Bob's physical channel eta>=1/2.

Theorem 11 parametrizes Bob's output entropy as n g(beta eta N), then uses the degrading attenuation (1-eta)/eta. Substitution gives

\[
f_\eta^{-1}(g(\beta\eta N))=g(\beta N),\qquad f_{(1-\eta)/\eta}(g(\beta\eta N))=g((1-\eta)\beta N),
\]

recovering Eqs. (78)–(79). Eta=1 has zero-output degrading channel and zero environmental entropy; eta=1/2 has identity degrading channel and zero coherent-information differences. Increasing/convex scalar property is [1705.00499v1, Lemma 15](https://arxiv.org/html/1705.00499v1): g(a g^{-1}(s)+b), b>=0, 0<=a<=b+1. This is inherited scalar machinery.

Theorem 11 proof starts from a regularized entropy characterization. Energy/operational/truncation assumptions still require lead-task validation; its citation alone does not establish the requested infinite-dimensional coding conventions.

## Alternate mechanism table

| Family | Mechanism/evidence | Status | Exact gap |
|---|---|---|---|
| Published converse plus #273 | Substitute f_tau into Theorem 11 / Sections III.G–H | Viable if input audited | Finite-energy EPnI validation and operational infinite-dimensional characterization |
| Exponential / conditional qEPI | Vacuum bound ln(tau exp(s)+1-tau) | Blocked as sharp input | Strictly below thermal equality candidate; missing sharp strengthening |
| 2019 entanglement-breaking optimization / integral Stam | Theorem 6 unrestricted lower bound | Blocked as exact input | Improved bound still below thermal value for generic positive entropy / nontrivial attenuation |
| One-mode plus chain rule | Induction if quantum-memory theorem existed | Blocked | Quantum conditional entropy can be negative; no classical conditional-ensemble reduction. Sharp conditional CMOE would transfer difficulty to stronger unsupported assertion. |
| Product-basis classicalization | 2017 theorem for product-basis diagonal states | Blocked for arbitrary inputs | Dephasing changes input/output entropy and does not give needed comparison from original output to dephased output. |
| Meta-log-Sobolev tensorization | One-mode variational result | Blocked | Authors leave multimode functional optimality open; ordinary constants / exponential hypercontractivity insufficient. |
| Subset convolution / symmetric CLT | 2026 finite-second-moment subset exponential bound | Blocked as sharp input | Controls exponential power and identical-copy smoothing, not unequal thermal comparison. |
| qEPI equality classification | September 2026 exact equality classes | No repair of sharp gap | Strictness does not identify required larger minimum. |
| Thermal-to-additive limit | Exact identity, bounded output energy | Conditional optional consequence | Relies on audited sharp thermal inequality; no alternate proof of premise. |

## Exact mismatch certificate and numerical reproduction

Natural logs, s=g(1)=ln4, tau=1/2. Exponential qEPI: ln(5/2). Thermal output: g(1/2)=ln(3 sqrt(3)/2). Difference ln(3 sqrt(3)/5)>0, since 27>25. Thus inspected exponential mechanisms cannot be substituted verbatim for the strong entropy hypothesis.

`compare_bounds.py` reproduces illustrative double-precision qEPI and De Palma 2019 values. These are not universal proofs or validated numerical certificates.

## Attribution / novelty recommendation

If #273 and the operational audit pass, describe the dynamic regions as unconditional consequences of OpenAI's finite-energy EPnI combined with Wilde–Hayden–Guha coding/converse results and De Palma's formulation. This project's contribution is the explicit scoped derivation, operational closure audit, and any justified additional entropy corollary. It is neither formula discovery nor the base EPnI proof, ordinary pure-loss quantum/private capacities, amplifier capacities, two-way assistance, or thermal-channel quantum capacity.

Release of a stronger theorem can make unstated consequences publicly available in a logical sense. Use “consequence” language and no unsupported “first” claim. Searches found no public paper expressly proving both full targets unconditionally, but this is limited evidence. Publication suitability depends on the exact final proof and priority judgment.
