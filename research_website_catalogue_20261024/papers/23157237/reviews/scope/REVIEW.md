# Publication scope and primary-literature review: 23157237

## Conclusion and review boundary

No substantive publication-scope or attribution defect was identified in this bounded comparison. Candidate content is suitable for consideration only after the separate mathematical gates. This report is not a proof certificate, worldwide novelty certification, or human peer review. The own scope conclusion was recorded at the 60% checkpoint before consulting any current sibling mathematical findings.

**Independence exception:** the published `independent_classical_derivation.md` combines a mathematical alternative-estimator derivation with historical AI attack dispositions and a final verdict. Reading that requested mathematical support exposed those historical opinions. `SOURCE_EDITIONS.md` also exposed historical priority-audit assertions. Consequently strict exclusion of archived opinions cannot be claimed. Those assertions were not used as evidence of correctness. No current sibling mathematical findings or dedicated external archived-review files were consulted.

## Actual edition and completeness

Fresh Zenodo record 23157237 identifies version **1.0**, published **2026-10-05**, DOI **10.5281/zenodo.23157237**. The eight-page manuscript prints **October 5, 2026** but no version label. The version comes from Zenodo; it was not silently inserted into the manuscript metadata. Both published assets were freshly acquired and checked against the public MD5 plus locally recorded SHA-256. See `source_integrity.json` and the immutable source receipt for exact bytes.

The entire eight-page manuscript was read. Page 1 was rendered and visually inspected for title, date, model, and complete abstract. The source ZIP has 20 files, no additional PDF or nested archive; all 20 extracted file bytes match, and all 19 manifest payload hashes pass. The complete mathematical `classical_regularization_application.md` and `independent_classical_derivation.md` were read. Source-edition notes and the manuscript TeX were inspected where needed. Finite-control outputs, historical verdicts, and package status assertions were not accepted as mathematical validation. No script execution is claimed by this scope reviewer.

## Exact target claim and assumptions

The model is a stationary reversible diffusion on a **known bounded connected smooth domain** D in R^d, d ≥ 2. Both the symmetric conductivity tensor S and invariant density μ are C∞ up to the boundary. Known positive bounds give ℓI ≤ S ≤ ΛI and c ≤ μ ≤ C, with integral μ = 1. The generator is L = μ⁻¹ div(S∇), with **conormal reflection n·S∇u = 0**. Exact stationary positions are observed at one known positive lag Δ. No shrinking lag, path observations, additive measurement error, unknown boundary, or nonreversible dynamics are included.

S is not itself the interior SDE covariance: that covariance is Σ = 2S/μ, and drift is β = div(S)/μ. Ordinary normal reflection cannot replace conormal reflection for an anisotropic tensor. The domain need not be convex. Known bounds do not include the unknown truth's spectral gap; the tuning is specified from the model/domain rather than an estimated oracle gap.

The estimator constructs a symmetric finite-rank estimate of the stationary joint kernel and a positive normalized density estimate, and uses **all positive empirical eigenpairs**. Signed smoothing can produce negative empirical eigenvalues, which are omitted; zero is omitted too. Positive eigenvalues above one are not artificially ruled out. The fit uses the eigenvalue fourth power and vanishing ridge, with no fixed number of modes or eigenvector labeling. The divergence vector is **fitted separately**: the statement is not that differentiating the estimated S yields the fitted divergence.

On one probability-one event, the tensor estimate and separately fitted divergence converge uniformly on every interior compact set. The ellipticity-clipped tensor converges globally in L²(D), and the density converges in C² on the closure. Covariance and drift follow locally uniformly. The paper does **not** prove a rate, uniform convergence of the raw tensor at the boundary, derivative convergence of the tensor, class-uniform conditioning, effective quadrature bounds, or a working general-domain numerical implementation.

## Mechanism and checkable interfaces

The mixed derivative consistency argument must accommodate dependent, overlapping lag pairs. It uses reversibility, the positive fixed-lag spectral gap, dyadic sampling, variance/net estimates, boundary-corrected signed kernels, and Borel–Cantelli. The extension construction has explicit derivative-matching coefficients and is applied on a known smooth atlas.

Functional calculus packages the sum of all positive empirical eigenpairs through continuous functions that vanish appropriately at zero, including t² and t² log t on the positive half-line. This avoids unstable individual eigenvector choices at multiplicity, rank loss, and zero crossing. The jet includes Hessian entries with doubled off-diagonals and first derivatives. Spectral completeness plus compactly supported prescribed affine/quadratic jets establish full excitation, with elliptic graph-norm regularity supplying C² convergence of the spectral partial sums. The lower conditioning bound is local and truth-dependent, not a finite-mode universal rank claim.

A finite-feature Gram formula avoids inverting a potentially singular feature Gram matrix and supplies measurability. It is a mathematical finite-rank description, not a polynomial-time or discretized implementation claim.

The alternative classical-regularization note is a **different estimator**, using a forward transition-kernel map over Sobolev-bounded admissible coefficients and penalized nonlinear inversion. It checks common H¹ form domains despite changing conormal operator domains, semigroup/kernel continuity, identification and compactness. This prevents promoting general consistency or identifiability as uniquely new. It does not establish consistency of the manuscript's specific spectral fit, nor does an application written in the present package prove that this particular application was already historically published.

## Primary comparisons and attribution

Fresh primary PDFs and retrieval/hash receipts are in `primary-sources/`; relevant passages rather than every page of every predecessor were read.

- **Reiß with Chorowski, Gobet and Hoffmann, OWR24/2017, printed pp. 1507–1509:** read the complete contribution. It asks for convergence analysis of matrix-coefficient reconstruction from generator eigenpairs and invariant density, leaving mode selection and estimator details open. The present paper addresses an explicitly smooth reversible conormal model; it should not be described as settling arbitrary diffusion reconstruction.
- **Hansen–Scheinkman, NBER Technical Working Paper 141 (1993), Proposition 5.5:** scanned PDF printed p. 26 visually read, with following scalar illustration on p. 27. Selfadjoint continuous-time generators are identified by the fixed-lag transition operator. The absence of reversible aliasing is old, not the new theorem here. The working-paper edition is the inspected source, not an assumed identity with a later final edition.
- **Crommelin–Vanden-Eijnden (2006), CMS 4, 651–668:** original journal PDF spectral residual and nonparametric/grid-fit sections inspected. Spectral fitting is an established reconstruction method, not newly invented here.
- **Crommelin–Vanden-Eijnden (2011), CWI author manuscript revised 31 August 2011:** inspected eigenvalue-power weighting (equation 4.7), data-estimation limitations and finite-expansion/nonparametric discussion. The publisher-final body was not obtained, so exact final-edition identity is not asserted. Weighting by eigenvalue powers is credited as prior art.
- **Nickl, arXiv:2210.13008v3:** scalar diffusivity/potential/normal-reflection model inspected. **Giordano–Wang, arXiv:2405.01372v3:** inspected the model and §1.3 discussion of anisotropic extensions. These already establish substantial multidimensional low-frequency inference; the present claim must specify its general tensor and estimator instead of claiming the first multidimensional result.
- **Alberti–Barnes–Jambhale–Nickl, arXiv:2410.19393v2:** Lemma 3.8, its spectral-cutoff/gradient-excitation proof and its use were read. This is a close excitation predecessor. The manuscript's extension uses full Hessian-and-gradient jets for the tensor/divergence vector, not an entirely new spectral-completeness idea.
- **Grubb, Regularity of spectral fractional Dirichlet and Neumann problems:** Theorem 2.2 and Corollary 2.3/domain interfaces inspected. Classical elliptic graph regularity remains a substantive imported analytic dependency; this scope review does not reprove it.
- **Lenzen–Scherzer, ECCOMAS 2004:** §3, operator assumptions and Theorem 3.2 read. Classical nonlinear Tikhonov convergence is the proper attribution for the supplementary variational route. Its hypotheses still have to be checked for the particular diffusion forward map.

The paper also cites other inverse-coefficient sources. This bounded review does not independently check every cited body or certify global first priority. The source-edition package's historical priority conclusions do not substitute for primary-source comparison.

## Public presentation and follow-up decision

Lead with a consistency theorem for a specified spectral-equation estimator. Explain fixed-lag recovery, the smooth reversible model, local versus global convergence, and the distinction between conductivity and physical covariance. Keep the complete original abstract separate from AI/status disclosures. State unrefereed status and extensive AI assistance without presenting internal checks as human peer review or formal certification.

**No public follow-up proposed.** Rates, noisy observations, boundary recovery and implementable discretizations are natural directions, but no sufficiently supported new mechanism or sharply justified conjecture was established here. Listing them would not meet the requested high bar. Collaboration can instead invite substantive independent verification, comparison with existing estimators, and journal preparation without an authorship promise.
