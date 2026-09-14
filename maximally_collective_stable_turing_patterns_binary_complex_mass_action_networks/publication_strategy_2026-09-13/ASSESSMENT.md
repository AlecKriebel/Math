# Publication assessment: Exact Diffusion Design for Maximally Collective Stable Turing Patterns

Assessment date: September 13, 2026 (America/Los_Angeles). Scope: the paper in row 8 of *Papers (4).xlsx*, not the other papers in that workbook.

**Recommendation: 7.8/10 conditional impact. Seek focused specialist feedback now and target journal submission September 28–October 5, 2026. Do not make full Lean formalization a prerequisite.** The existing primary and secondary journal choices are retained.

## What was reviewed

The current main manuscript and technical supplement each have 19 pages. I read the main proof chain, the relevant supplementary derivations and certificates, and commissioned separate adversarial algebra and PDE reviews. Those reviews began with the current arguments rather than historical audit conclusions. Their reports and independently written checks are preserved in `algebra_review/` and `pde_review/` beside this assessment.

The public [Zenodo preprint](https://doi.org/10.5281/zenodo.22729355) is version 1.0.11, deposited September 12. Zenodo's API metadata and checksums were retrieved directly after the web page failed to load. All eight local deposit files match the public record's MD5 checksums. The archived main and supplementary TeX differ from the working source only in relative figure/data paths; the bibliography is identical. This establishes that the assessed mathematical text is the deposited version, not a stronger unpublished revision. The preprint DOI and the [companion software DOI](https://doi.org/10.5281/zenodo.22625980) are distinct.

No publication-blocking mathematical defect was found in this bounded review. That is a review finding, not a proof of correctness, an exhaustive novelty determination, or journal peer review.

## Contribution and impact score

The workbook asks: assuming correctness, genuine novelty and publication, how important would the theorem be in its actual subfield? The score therefore concerns structural reaction-network theory and multicomponent reaction–diffusion bifurcation. It does not discount the result for the author's affiliation, lack of arXiv access, or preprint status. It is not a probability of acceptance or correctness.

The central contribution is a conjunction of three results:

1. **A topology-wide extremal construction.** For every n≥4, one binary-complex classical mass-action topology has every nonempty principal Jacobian block of order below n−1 Hurwitz at every positive-equilibrium realization, while an order-(n−1) block is unstable. The complete flux/equilibrium parametrization is essential: this holds throughout the positive realization space, not just at a favorable numerical Jacobian. Here “principal subsystem” means a principal Jacobian block; it does not automatically mean a physically isolated reaction network obtained by deleting species.
2. **An exact quantitative law.** On the homogeneously stable realization domain, a positive diagonal diffusion ray has a nonzero stationary threshold exactly when d_Z > 8 h_Z Σ(d_j/h_j), with j=2,…,n−2. The signed omission-minor structure yields a unique threshold, the nonattained fixed-equilibrium diffusion infimum and χ_D χ_H > 8(n−3).
3. **Stable nonlinear realizations in every dimension.** An exact rational profile has a primary supercritical branch with local exponential stability. A second family reallocates diffusion and concentration contrast so both grow as √n, matching the topology-specific stationary minimax lower bound in exponent. The conservation-compatible zero-mode correction and the new spectral argument after equilibrium scaling are substantial parts of this result.

**My score is 7.8, with a reasonable judgment range of 7.5–8.1.** This is the rubric's “strong specialist result” tier and qualifies as a flagship project under its recommended-treatment bands. I would revise the existing ChatGPT score of 8.4 downward. The independent Claude score of 7.4 is preserved; the existing average becomes 7.6.

Why below 8.4: the paper does not settle a recognized central longstanding conjecture, classify a broad class of networks, or establish a biological mechanism. It gives one deliberately engineered infinite family. Its stable-pattern conclusions are local, the parameter robustness is retuned and dimension-dependent, and the exact nonlinear constants and full frontier remain open. I do not yet see a basis for predicting that this will be one of the niche's most important results for several years. Why above a routine 6–7: arbitrary dimension, every-positive-realization quantification, an exact transport law, and rigorous nonlinear stability are a substantial combination.

The constants help calibrate the claim. With ν=n−3, the certified contrast product is 23(91ν−1)/63, compared with the necessary stationary bound 8ν: asymptotically a factor of about 4.15. At the certified √ν endpoint, the larger contrast is about 37.14√ν, compared with the minimax lower bound √(8ν), a factor of about 13.1. The exponent theorem is meaningful, but it is not near-optimality in constants or an exactly balanced design. Neither improvement is required to publish the present result.

## Closest literature and the presentation issue to fix

General fixed-matrix unstable-subsystem theory already allows large responsible blocks; [Villar-Sepúlveda and Champneys (2023)](https://doi.org/10.1007/s00285-023-01870-3) provide general diffusion-driven instability conditions and constructions. [Vassena and Stadler (2024)](https://doi.org/10.1098/rspa.2023.0694) study unstable cores in parameter-rich kinetics. The present paper's constrained classical mass-action realization space and all-positive-realization quantifier are therefore central to distinguishing it. These are related results, not equivalent claims.

[Conradi, Mincheva and Uecker (2026)](https://arxiv.org/abs/2605.16049) is especially relevant: it derives sufficient spatial-instability conditions from monomial steady-state parametrizations and investigates nonlinear branches numerically. Your paper already cites it and distinguishes its theorem suite. Keep that comparison prominent. [Krause and colleagues (2024)](https://doi.org/10.1007/s11538-023-01250-4) explain why linear instability alone does not ensure persistent patterns; your nonlinear stability theorem addresses exactly that logical gap in this construction.

The most useful small revision is to make the **fixed-interval, fixed-integrated-mass, long-wave scope visible in the abstract**, not only in the introduction and theorem assumptions. The determinant law gives a positive-real instability band 0<q²<s*. Thus arbitrarily small positive wavenumbers are unstable in the continuous dispersion relation. The first Neumann mode is selected on the prescribed finite interval; the paper does not prove an intrinsic finite wavelength that persists as the domain is enlarged. The homogeneous Jacobian also has a conservation zero; stability means stability on the stoichiometric/fixed-mass restriction. Both points are handled in the proof. They deserve equally explicit front-page wording so readers do not import stronger standard interpretations of “stable” or “Turing pattern.” The recent Conradi paper explicitly discusses this long-wave terminology distinction.

Preserve the synthetic-network qualification and the separation between stationary and wave instability. Do not expand this submission to solve global existence, biological realization, the full wave-instability region or the constant-optimal frontier.

## Best next step and useful readers

The sheet records the September 12 deposit but no specialist circulation for this paper. Its “Circulating” status alone does not establish that anyone has read it. The next useful milestone is a small amount of substantive specialist input on novelty and proof scope.

Start with two complementary readers, and optionally add a third:

| Reader | Why this person fits | Scientific issue their input could resolve |
|---|---|---|
| [Edgardo Villar-Sepúlveda](https://research-information.bris.ac.uk/en/persons/edgardo-enrique-villar-sep%C3%BAlveda) | Author of the 2023 general instability criteria and subsequent diffusion-design work | Distinction from fixed-matrix subsystem results; interpretation of the long-wave stationary threshold |
| [Maya Mincheva](https://www.niu.edu/clas/math/about/directory/mincheva.shtml) | Reaction-network structure, diffusion and bifurcation; coauthor of the closely related 2026 paper | Classical mass-action novelty, complete realization quantifier and conservation restriction |
| [Andrew L. Krause](https://arxiv.org/abs/2308.15311) | Work on the gap between linear instability and persistent patterns, and on diffusion design | Local nonlinear stability, the fixed-interval claim and the value of the scaled family |

Nicola Vassena is an additional strong structural-CRNT reader if that aspect needs more scrutiny; his unstable-core paper is the relevant connection. This is a fit-based list, not a prediction that anyone will respond. There is no need to contact all of these people or an entire coauthor group at once.

For any circulation the human author chooses to undertake, the existing preprint DOI and portable reproducibility package are sufficient reference materials. The narrowly useful feedback is whether a specific theorem is already implied by prior work, whether a proof step is unclear, and whether the fixed-domain scope is framed appropriately. A request for a complete unpaid referee report or an endorsement would be a much larger ask. No message or outreach draft was prepared or sent in this review, in accordance with the project's independent-research policy.

## Lean decision

**A complete Lean formalization is unlikely to offer enough additional publication benefit to justify making it the next major investment.** The paper already has transparent exact algebra and executable certificates. The remaining credibility-sensitive work includes the connection from finite matrices to the conservation-compatible semilinear PDE, center manifolds, spectral perturbation and nonlinear stability. A formal proof of coefficient positivity alone would not formally prove those conclusions.

Lean could add useful assurance for a carefully delimited theorem. If resources remain after circulation and submission preparation, the best pilot is the general principal-minor diffusion-ray theorem, including its hypotheses, characteristic-polynomial identity, monotonicity and simple stationary root. Another bounded target is selected polynomial positivity certificates, provided the bridge from the reaction-defined matrices to the printed polynomials is included or explicitly left outside the formalized claim. Current [mathlib determinant](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/Determinant/Basic.html) and [characteristic-polynomial](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/Charpoly/Univ.html) infrastructure support the choice of a finite-algebra pilot; this is not an audited estimate of end-to-end formalization effort.

A useful completion criterion would be a kernel-checked, assumption-audited theorem mapped to an exact manuscript statement, with no unproved replacement of its central claim. Avoid presenting a finite-dimension check or an axiomatized PDE theorem as “the paper formalized.” A pilot should have a fixed resource cap chosen by the author. Stop or defer it if most effort goes into building unrelated analytic infrastructure. Affiliation does not change the mathematical proof obligation, and a Lean badge does not establish novelty or journal fit.

## Submission timing

During the week of September 14, make the small scope/abstract clarification and begin any specialist circulation the author chooses. Allow roughly two to three weeks for initial feedback. Resolve concrete objections as they arrive. **Target September 28–October 5 for submission** if no substantive mathematical problem emerges. This is a planning recommendation, not a journal deadline or a required preprint waiting period. If someone commits to a detailed review on a definite nearby date, a short extension is reasonable. Otherwise silence should not cause indefinite postponement, and it should not be interpreted as validation.

The existing primary venue's [editorial policy](https://epubs.siam.org/journal/siads/editorial-policy) fits mathematical dynamical-systems theory and strongly encourages accessible reproducibility materials. Its [consent form](https://epubs.siam.org/pb-assets/files/Consent_to_Publish_Journals.pdf), section 1, explicitly excepts preprints from the prior-publication warranty. Its editorial policy asks authors to disclose earlier appearances. Consequently the Zenodo preprint is not a reason to wait for arXiv or bioRxiv access. Identify the preprint and companion software when submitting, and provide the supplement as part of the review materials. Public circulation can continue during peer review; submit to only one journal at a time.

## Verification record and remaining gap

- Algebra: independently reconstructed exact reaction/rank/omission identities for m=3,…,7; 912 proper principal-set SCC checks including the edge-cancellation case b=2a; symbolic triad Routh positivity; stationary-ray boundary/equality cases including n=2; finite critical-profile and contrast checks; and 324 numerical stress probes.
- PDE: 15 independent reaction-derived exact unit/scaled cubic cases for m=3,4,5,8,12, plus 75 complementary numerical spectral probes. Conservation gauges and transformed left vectors were checked explicitly.
- The repository's symbolic-certificate suite replayed successfully, separately from the newly written checks. Finite exact and floating-point probes do not replace the manuscript's all-dimensional arguments, and repeated execution of the same code is not new independent evidence.
- Exact outstanding uncertainty: no domain specialist has supplied an external report in this review, exhaustive literature priority is not established, and journal significance/acceptance remains an editorial judgment. These are reasons for focused circulation and peer review, not reasons to label the theorem false or delay it for a separate Lean program.

The updated workbook changes this paper's title, next action, dated assessment, ChatGPT impact score, actual preprint server, notes and source URLs. It retains the prior deposit event, independent Claude score, average formula and journal choices. Other papers were not assessed.
