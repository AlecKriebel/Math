# Independent adversarial review — Zenodo 23430642

Completed 2026-10-25T02:01:27.269947+00:00; assigned review 100%.

**Verdict: SUPPORTED AT THE STATED SCOPE.** No substantive defect was found in the nine-page published argument, the necessary primary interfaces, independently reconstructed exact controls, or fresh replay of the two supplied mathematical helpers. This is a mathematical review with explicit limits, not conventional human peer review or formal proof-assistant certification. It makes no worldwide novelty or priority determination.

## Bound inputs and coverage

The selected manuscript is `paper.pdf`, 9 pages, printed **13 October 2026, Version 1.0**, DOI [10.5281/zenodo.23430642](https://zenodo.org/records/23430642). Its SHA-256 is `3ba83c50a4a2369a70897ee165a43f56324aa31574cf9c199e664174cbce0449`. The complete published `supportkit-v1.0.tar.gz` has SHA-256 `cd20964fe478365bd9c2db9b6cd8f6032aea0168073e7da21149865ec2f6d34c`. Both original assets were independently size/MD5/SHA-checked at intake and completion, and all 538 safely extracted regular files were rehashed twice. The original sources remain unchanged. The archive's embedded output PDF is the same edition as the main PDF, as established by the acquisition receipt.

All nine pages were read: the ordinary-language definitions and theorem (p.1), source gadget (pp.2–3), all-real-demand isolation (p.4), injective simplex and uniform exact penalty (pp.5–6), rank-one game and exhaustive crossings (pp.6–7), encoding and certificate membership (pp.7–8), and disclosure/references (p.9). The supplied 179-line flow helper and 243-line game helper were read completely **after** the independent controls and checkpoint. No historical prose report or full-package status wrapper was used.

`DERIVATION.md` gives the complete independent argument and attacks; `fresh_controls.py` and `boundary_controls.py` are new standalone exact-arithmetic artifacts. Their results are recorded separately from the reproduced supplied checks. No source repairs were made.

## Exact claim assessed

For explicitly listed rational games of variable positive dimensions with **rank(A+B)=1 exactly**, deciding whether there is exactly one mixed-strategy **pair** is coNP-complete and deciding whether there are at least two is NP-complete. Arbitrary degeneracy and equilibrium continua are allowed. The reduction supplies a known strict pure equilibrium; Partition has a solution if and only if there is an additional equilibrium. Both ordinary languages reject malformed/rank-invalid inputs.

The theorem is not a claim of strong NP hardness, fixed-dimension hardness, nondegenerate-promise hardness, payoff uniqueness, or difficulty finding one equilibrium. No result about all rational bimatrix games is substituted for the exact-rank-one reduction.

## Adversarial findings by dependency

| Dependency | Attack and outcome |
|---|---|
| Signed source counter | Checked actual journal arc formulas, source normalization, unit bottlenecks, both even/odd bridge comparisons and the synchronized companion step. The candidate's arithmetic corrections agree with the displayed gadget. Fresh tests include n=1, no/yes cases, repeated weights, five weights, and 81-bit integer weights. No off-by-one demand or cap failure found. |
| Universal shortest-path choices | The strict comparison/state argument addresses all choices, not only one tie rule. Exhaustive small reachable-state searches confirm this. Removing the base delta makes a yes instance admit a missed bridge event, a meaningful negative control. |
| Perturbation and real demand | Same-state original shortest comparisons are preserved; nonzero projected cycles cannot remain zero. Sign-conformal circulation decomposition proves uniqueness even for irrational demand. Interpolation optimality is established by residual path/cycle costs, not integer integrality. |
| Positive normalization | A topological potential changes only the fixed-demand objective constant, preserving events and uniqueness. Every shifted arc cost is positive; the DAG gives zero as the only demand-zero flow. |
| Simplex injectivity and retention | Explicit inverse coordinates are unique; the slack row creates no multiplicity. Every no-instance unrestricted optimum and the required yes midpoint remain feasible in the restricted LP. The proof does not need all yes optima to survive. |
| Uniform exact penalty | A fixed rational pointed dual has an optimal vertex for each real parameter. Cramer bounds are independent of that parameter and remain valid with redundant constraints/lower-dimensional faces. M>C strictly excludes every infeasible minimizer. Numerical size does not imply exponential encoding size. |
| Exact rank one and scalar correspondence | Opposite parameter constraints make b nonzero and a_0 is nonzero. Both best-response sets agree at lambda=a^T x, including zero probabilities and all opposing optima. Fresh exact full-game matrices and payoff inequalities agree. |
| Negative/zero/boundary parameter cases | Negative parameters have unique row zero, consistency at −epsilon, and one strict diagnostic column. Lambda=0 admits only zero flow and no crossing. Every remaining candidate is inside the penalty-valid interval; a yes midpoint lies strictly below its top boundary. |
| No-case full-pair exhaustion | Every nonnegative candidate requires f_e=1/2, excluded for every no-instance optimum. The sole negative pair is strict for both players. No hidden column degeneracy survives in the no case. |
| Degenerate membership witnesses | Closed support-product cells add no false equilibria, cover all equilibria and have polynomial-bit rational vertices. A nonsingleton union must contain two distinct vertex pairs. Tests include rank-one continua and one-player-single-action boundaries. |
| Ordinary languages and bit complexity | Rank-invalid/malformed inputs are handled in the complement branch; the reduction outputs valid rank-one games. It constructs only polynomial-sized rational matrices and never executes its exponentially long SSP curve. |

No examined dependency was left as an unsupported claim equivalent to the main theorem. The actual universal reasoning is in `DERIVATION.md`; computation alone is not treated as a proof of these rows.

## Fresh independent controls

The initial reconstruction used only the current manuscript and primary publications; no supplied helper was imported or read. `independence_checkpoint.json` fixes that checkpoint.

- **14 source instances**, **280** unit augmentations and **840** fractional-demand controls at one-third, one-half and two-thirds of each segment. Exact residual reduced-cost certificates check optimality; capacity/conservation, original-shortest comparison preservation and complete bridge event locations are checked.
- **6 complete rank-one games**, with M reaching **7,560 binary bits**, **48** exact primal/dual auxiliary equilibrium pairs, and **12** explicitly verified additional Nash pairs. Matrices are rebuilt from the manuscript, and both players' inequalities are checked exactly.
- **12 exhaustive small original-shortest-choice searches**, including all one- and two-weight tuples over {1,2,3}. All terminal event flags agree with Partition.
- **300** rational boundary/grid strategy pairs check the complete best-response transformation, including zero supports. Moving the parameter away from a^T x changes the column response set in **140** of those pairs, confirming the scalar condition matters.
- Exact rank-one equilibrium continua are checked in dimensions 1x2, 2x1, 2x2 and 3x4. The zero-penalty control exhibits an infeasible origin of cost zero at demand one while a feasible flow costs 539/30 and every nonzero feasible flow has positive shifted cost.

The flow/game artifact records 112,577 individual assertions, many repeated residual feasibility inequalities; the boundary artifact records 677. These are finite check totals, not distinct theorems or an exhaustive equilibrium enumeration.

A first local harness execution failed because integer zero dual entries divided by M became floating-point zeros, causing conversion overflow when multiplied by huge rationals. Converting every dual entry explicitly to Fraction fixed this local harness error before any passing result was reported. No manuscript or published helper was changed. The final tests use exact integer/rational arithmetic only.

## Supplied mathematical helper replay

After the independent checkpoint, the two standalone helpers were copied byte-for-byte to ignored isolated directories and run in normal Python mode. Their source hashes are bound by `published_helper_bindings.json`; originals were not executed in place because the helpers write result files next to themselves.

Fresh execution reproduced **37 flow instances, 660 augmentations, 864 residual-cycle checks and 6 exhaustive original-choice searches**. Its four deliberate negative controls passed. The game helper freshly reconstructed **6 games** and **204 exact auxiliary pairs**, plus strict default checks, wrong-sign/default/invalid-certificate controls, degenerate continua and an exact penalty-threshold toy example.

These are outputs of the current executions, retained as `published_flow_replay.json` and `published_game_replay.json`; no archived results were adopted. Normal-mode game assertions were active. The full archive wrapper and optimized-mode replay were not run, and no such coverage is claimed. The standalone helpers do not exhaust all games, demands, source instances or equilibria; the universal claims rely on the proof.

## Direct primary interfaces

Raw primary files obtained by the scope agent were independently hash-checked; acquisition logistics alone were shared. `primary_sources.json` records URLs, SHA-256 values and exact reading scope.

- [Disser–Skutella, journal body](https://www2.mathematik.tu-darmstadt.de/~disser/pdfs/DisserSkutella18.pdf): Section2 normalization and Proposition2.1, complete Lemmas3.1–3.2, Figures1–3 context, and Corollary1.7. Figure1's edge labels were visually checked. The arithmetic clarifications correspond to the actual displayed edges; the exact SODA edition is not needed as a separate imported theorem.
- [Adsul et al., published article](https://par.nsf.gov/servlets/purl/10317978): Section3 rank reduction and complete best-response correspondence, journal Theorem1. [arXiv v4](https://arxiv.org/abs/1812.04611v4) Theorem7 and equations8–12 independently confirm the numbering and specialization. The manuscript also proves its needed instance directly.
- [Erickson–Fox–Lkhamsuren](https://ekfox.web.illinois.edu/publications/holiest/holiest.pdf): Lemma3.3 proof and Theorem3.4 confirm that uniqueness for real capacities/demands has precedent. The candidate's simpler ternary scheme is checked on its own cycle argument; it is not justified by silently importing this surface-graph theorem to arbitrary graphs.
- [Gilboa–Zemel](https://itzhakgilboa.weebly.com/uploads/8/3/6/3/8363317/gilboa_zemel_nash_complexity.pdf): Section3.13 directly supplies the established rational-support certificate idea. The candidate's explicit closed-cell bounds were reconstructed rather than assuming irrational initial equilibria are themselves short witnesses.
- [Nash (1951)](https://irving.vassar.edu/faculty/gj/FTU/io/literature/Nash51.pdf): equilibrium/support definitions and Theorem1 existence proof were read through completion. This justifies complementing uniqueness/nonuniqueness on valid finite games.

LP duality, pointed polyhedral faces and determinant estimates are standard ingredients reconstructed explicitly here. This review does not claim to have read every bibliography entry, every historical version, or priority-audit document. The paper's stated novelty gaps remain novelty gaps rather than missing hypotheses of the reduction.

## Independence and incidental status exposure

No current sibling review finding, historical dedicated verdict/report, status file, acceptance file or audit prose body was read. Acquisition manifests exposed historical filenames and hashes only. The current paper's p.9 necessarily exposes its authored historical check counts and AI-review disclosure; the supplied helper docstrings claim earlier independent authorship. Those assertions were not adopted as validation. Fresh helper output after execution is evidence of that execution, not authority over the universal proof.

The authored archive contains many historical and review files; they were rehashed for byte integrity but their opinion bodies remained opaque. Only the two mathematical checker source files were inspected and replayed after independent evidence existed.

No site, promotion, spreadsheet, Git, deployment, Zenodo or external communication action was taken. The review recommends no repair because no substantive defect was found. Publication disposition belongs to the parent after all independent gates.
