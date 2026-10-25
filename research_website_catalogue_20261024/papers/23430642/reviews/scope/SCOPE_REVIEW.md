# Acquisition and scope review — Zenodo 23430642

**Status: SCOPE COMPLETE; mathematical verdict pending independent reviewers.** This report authenticates the published edition, maps its claims and boundaries, checks the identified primary-source interfaces and attribution, and supplies draft explanatory content. It is not a mathematical PASS and makes no claim to have replayed the package's verification programs.

## Published edition and acquisition

Alec Kriebel, *A flow reduction for equilibrium uniqueness in rank-one bimatrix games*, v1.0, 13 October 2026, DOI [10.5281/zenodo.23430642](https://doi.org/10.5281/zenodo.23430642), nine pages. Zenodo identifies the author as an independent researcher, ORCID 0009-0001-9320-500X, and licenses the authored material CC BY 4.0.

Fresh API metadata and **all two public assets** were acquired. Each public file matches both Zenodo's MD5/size and the inventory expectation:

| Asset | Bytes | MD5 | SHA256 |
|---|---:|---|---|
| paper.pdf | 108357 | b76c3ef22276d51e8a2db86a57954aae | 3ba83c50a4a2369a70897ee165a43f56324aa31574cf9c199e664174cbce0449 |
| supportkit-v1.0.tar.gz | 680672 | 5f6e7546d0911d2ed0c94e2449eb0df9 | cd20964fe478365bd9c2db9b6cd8f6032aea0168073e7da21149865ec2f6d34c |

The TAR was extracted with absolute/traversing paths, backslashes, links and special nodes rejected. Its 538 regular files are individually hash-bound in `sources/receipt.json`. Sources were released read-only for review. The archive's `rank_one_uniqueness_v1_0/output/pdf/paper.pdf` is byte-identical to the public PDF. There is **one distinct reader PDF and nine distinct reader pages**, with no additional reader PDF hidden among the historical evidence. `reader_document_map.json` records the map. Source TeX is `published-source/rank_one_uniqueness_v1_0/paper.tex`.

## Reading scope and independence

Read all nine actual manuscript pages, the entire 287-line TeX, README and SUPPLEMENT, the original 132-line `evidence/original/submitted/PROOF.md`, and the full mathematical certificate note `evidence/original/submitted/certificates/LEMMA_REPORT.md`. Visually checked manuscript pages 1, 3, 6 and 8, including the theorem, source-event table, scalar game equations, and rational certificates. Exact hashes of the read supporting sources are in `read_support_hashes.json`.

The package includes a large historical audit tree. Dedicated old ACCEPTANCE/STATUS/AUDIT/review verdicts and current sibling reports were not opened. Necessary README/SUPPLEMENT text explicitly asserts historical acceptances and review outcomes; the original proof header refers to earlier gap repairs and pending acceptance. Those incidental assertions were seen and are disclosed here, but have no evidentiary role in this review. The original proof also describes an absent historical six-game/39-network script; the current paper and supplement expressly distinguish it from the newer included scripts. This scope review does not treat either set of historical receipts as a fresh replay.

## Exact claim and quantifier map

Theorem 1 (PDF p.1) claims coNP-completeness of UNIQUENESS₁ and NP-completeness of NONUNIQUENESS₁ under polynomial-time many-one reductions. Input is **explicitly listed rational matrices** A,B of variable positive dimensions m,N, with binary rational encoding and **exact rank(A+B)=1**. Both players maximize expected payoff. Uniqueness concerns the **entire mixed-strategy pair (x,y)**, including pure strategies, not just payoffs or the support of one equilibrium. Arbitrary degeneracy and positive-dimensional equilibrium sets are allowed. Rank-invalid or malformed inputs are in neither language; the coNP-membership discussion includes the invalid-input branch of the ordinary complement.

Hardness is claimed even if a **known strict pure equilibrium** is supplied. The source problem is PARTITION on nonempty lists of positive integers. A no instance must produce exactly the default equilibrium; a yes instance must have another pair. The construction does not promise that every additional equilibrium is isolated, that every output game is nondegenerate, or that there are exactly two equilibria.

The paper does **not** claim strong NP/coNP hardness, hardness at fixed dimensions, a nondegenerate-input promise result, payoff-uniqueness hardness, or a polynomial-time algorithm to decide uniqueness. The polynomial algorithm in the paper is the reduction constructing the game. The exponentially long successive-shortest-path (SSP) trajectory is used in its correctness argument and is not executed to build the output.

| Stage | Exact asserted interface | Boundary requiring mathematical review |
|---|---|---|
| Diagnostic network, pp.2–3, Lemma 2 | n positive weights; DAG with V=4n+6, p=8n+7, maximum value F=2^(n+1); every legitimate unperturbed SSP execution uses the bridge iff PARTITION is yes | Universal tie choices, both parity states, immediate bridge reversal, and fractional midpoint q≤F−3/2 are load-bearing; Corollary 1.7 alone does not supply the later all-optimum claim |
| Isolation, p.4, Lemma 4 | Rational ternary perturbation preserves nonzero path comparisons in the **same residual state** and yields a unique optimum for **every real** demand q∈[0,F] | Needs nontrivial projected-cycle isolation, sign-conformal difference decomposition and optimality of fractional interpolation, not just integer vertices |
| Simplex, pp.4–5 | f_i=LF x_i, h=F(1−x₀), q=h−Kf_e, K=1/(2L); encoding is injective, with a single slack coordinate | Unrestricted optimum means post-perturbation/post-potential, before simplex restriction; no-case optima and a yes-case half-bridge witness must survive restriction |
| Exact penalty, pp.5–6, Lemma 5 | A single positive integer M of polynomial **bit length** makes **all** minimizers feasible and optimal, uniformly for real λ∈[0,F] | The rational dual feasible region is independent of λ; its vertex norm bound must cover degeneracy and irrational objectives; selected minimizers would be insufficient |
| Game, pp.6–7, Lemma 6/Proposition 7 | A+B=abᵀ has exact rank one; complete equilibrium correspondence at λ=aᵀx=h−ε; candidate interval [−ε,F−ε] | Every opposing strategy/optimal face must be covered. The sole negative crossing is strict pure; every nonnegative crossing is equivalent to f_e=1/2 |
| Size/membership, pp.7–8 | Output dimensions (8n+9)×(16n+22); all entries polynomial in binary input length; two rational equilibrium-pair certificates suffice | Numerically large capacities and M are allowed; rational witnesses must cover continua/irrational initial witnesses; no polynomial enumeration of all support cells is claimed |

These interfaces are accurately described in the main paper and supporting proof. Their mathematical validity is the responsibility of the independent analytic and adversarial reviews, rather than being inferred from scope consistency.

## Primary sources and attribution

Fresh primary PDFs and text are in the ignored `.reference-cache`; `primary_source_receipts.json` records exact URLs, hashes and retrieval times. Source statements were inspected at the interfaces below; this is not a full proof audit of each cited paper.

1. **Disser–Skutella, author-hosted journal edition**, [DOI 10.1145/3280847](https://doi.org/10.1145/3280847), [PDF](https://www2.mathematik.tu-darmstadt.de/~disser/pdfs/DisserSkutella18.pdf). Read the normalization/flow definitions, Sections 3.1–3.2 with Lemmas 3.1–3.2 and Figures 1–3 context, and Corollary 1.7. The source owns the signed counter, distinguished bridge, SSP activity reduction and parametric-flow activity hardness. Its normalized positive rational weights have total below 1/12 and a common positive granularity; the manuscript's total 1/24 and η=1/(24S) fit that scope. The manuscript explicitly identifies two printed arithmetic/envelope clarifications rather than silently changing the source. The scope review authenticates those source locations but does not independently certify the strengthened universal execution argument. The journal footer says November 2018; some volume bibliographies label the issue 2019. The exact SODA 2015 body remains uninspected.
2. **Adsul, Garg, Mehta, Sohoni and von Stengel**, [journal PDF through NSF PAR](https://par.nsf.gov/servlets/purl/10317978) and [arXiv v4](https://arxiv.org/pdf/1812.04611v4). The journal Theorem 1 gives the rank-reduction/hyperplane correspondence; its Theorem 4 gives a polynomial-time algorithm finding **one** equilibrium, Theorem 5 describes maximal Nash subsets including degeneracy, and Theorem 6 provides exponentially many equilibria. Their arXiv-v4 numbers are respectively 7,19,20,21. Journal Theorem 7 is instead a fixed-sum-matrix homeomorphism result. The numbering distinction in the manuscript is correct. The scalar representation is prior work, not a novelty claim of this preprint.
3. **von Stengel's joint-work contribution**, [Oberwolfach Report 38/2018](https://ems.press/content/serial-article-files/46760), printed p.2332. The contribution explicitly presents rank-one uniqueness coNP-hardness as a conjecture, while emphasizing that one equilibrium can be found in polynomial time. This authenticates the historical question; it cannot establish current worldwide openness or priority.
4. **Gilboa–Zemel**, [author-hosted journal scan](https://itzhakgilboa.weebly.com/uploads/8/3/6/3/8363317/gilboa_zemel_nash_complexity.pdf), Sections 3.1–3.2 and 3.13. Their general two-player uniqueness hardness uses a default pair and another equilibrium corresponding to a clique; Section 3.13 gives rational basic-solution certificates and the coNP uniqueness membership argument. These are earlier unrestricted results. No rank-one restriction is imposed in those displayed constructions. The first author-site acquisition failed DNS; the cited alternate author-hosted scan was successfully acquired.
5. **Conitzer–Sandholm**, [author manuscript](https://www.cs.cmu.edu/~conitzer/nashGEB08.pdf), Definition 4, Theorem 1 and Corollary 2. The SAT construction has a default equilibrium and other equilibria from satisfying assignments; Corollary 2 states NP-completeness of having more than one equilibrium, even for symmetric two-player games. This precedes the default-plus-witness design pattern; it is not a rank-one hardness theorem.
6. **Erickson–Fox–Lkhamsuren**, [author manuscript](https://ekfox.web.illinois.edu/publications/holiest/holiest.pdf), Section 3, Lemma 3.3/Theorem 3.4. Their lexicographic perturbation yields a unique minimum-cost feasible flow for real capacities and real demands in their surface-graph framework. This is prior isolation context. The preprint's particular rational, comparison-preserving perturbation and its coupling to the diagnostic event require their own proof; the cited result is not a black-box certification of those steps.
7. **Nash**, [1951 article scan](https://irving.vassar.edu/faculty/gj/FTU/io/literature/Nash51.pdf), definitions pp.286–287 and Theorem 1 p.288. Finite games with real payoffs have mixed-strategy equilibria. This matches the finite positive-dimensional bimatrix domain, so “not more than one” means exactly one on valid game inputs.

The claimed contribution is the specific quantitative connection between the existing flow gadget and the complete rank-one equilibrium set, together with the reduction's all-real-demand and all-minimizer safeguards. Generic perturbation, the zero-sum correspondence, LP duality, determinant bounds, and unrestricted rational membership are not presented as newly invented. The paper expressly leaves worldwide priority unknown and identifies unrecovered Murty 1980/SODA 2015/Mehta 2012/Patris 2026 bodies. This bounded fresh interface inspection does not close those literature gaps or certify firstness.

## Abstract and explanatory candidates

`CONTENT_CANDIDATE.md` contains a complete standalone technical abstract and plain-language explanation, conditional on mathematical clearance. The main interest is a separation between efficiently finding one equilibrium and the claimed hardness of determining whether any other exists, even when a strict default is already supplied. This should not be described as proving P≠NP or making every individual rank-one game difficult.

**Follow-up question: null.** Nondegenerate-promise hardness, strong hardness, payoff uniqueness and practical algorithms are natural extensions, but this scope review has not established their novelty, tractability or sufficient paper-level substance. None is proposed merely to fill a section.

## Reproducibility and final limits

No verification program was executed in this scope assignment. The published 37-weight/660-augmentation/864-cycle flow counts and six-game/204-pair game counts remain **reported by the paper**, not fresh replay results here. Scripts are mapped in `scope.json` for the mathematical reviewers. No historical acceptance is used to approve the mathematics, no website text was published, no source was repaired, and no site, spreadsheet, Git, Zenodo or outreach action was performed.

Completion is **100% of acquisition/scope work**. Mathematical promotion remains pending the independent analytic/adversarial decisions and any required actual replays. The source hashes and necessary exact hypothesis boundaries are now available for those reviews.
