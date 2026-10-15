# Exact source and readiness: 30005244

The primary problem is Section 4, p. 2582 (PDF p. 72), of Costabel's report in Oberwolfach Report 43/2022, DOI 10.4171/owr/2022/43. The report is a 2022 workshop report published in 2023. The original contribution spans pp. 2580–2582 and credits joint work with Monique Dauge and Khadijeh Nedaiasl. The clean dataset title is a later catalog title, not the original talk title.

The source matrix uses the cubic-grid centers belonging to Ω, off-diagonal blocks h³K_κ(x_m-x_n), and zero diagonal. K_κ=−(D²+κ²I)g_κ, with g_κ=exp(iκ|x|)/(4π|x|). It approximates A_κ−I/3. The printed T^h_κ is occasionally flattened into T_{κh} by extraction; it denotes a finite matrix on the particle, not the full-lattice nonzero-frequency convolution operator.

The static interval is the exact numerical range closure of the bounded selfadjoint full-lattice static operator. The particular endpoint decimal values are numerical conjectures about symbol extrema. The theorem in CANDIDATE.md uses the exact interval; it does not certify those decimals.

The actual question asks for a mathematically correct description and proof of the observed approximation of isolated nonreal volume-operator eigenvalues away from the real accumulation interval. Our proposed precise answer is no spectral pollution and preservation of algebraic multiplicity, plus norm convergence of embedded Riesz projections, outside that interval. The source's shift is carried throughout.

## Geometric qualification

The three-page report says that the contrast is supported in a compact particle and does not impose a technical boundary assumption. A point-membership grid cannot be expected to approximate every pathological measurable set. The candidate explicitly assumes convergence in measure of the voxel union to the intended particle. It proves the result for all such geometrically consistent sequences, including all bounded Lipschitz and all bounded boundary-measure-zero particles, with arbitrary lattice translations. This is a necessary scope disclosure, not a claim that the report explicitly states this assumption. Independent review must assess the scope as well as the analysis.

## Literature and established inputs

Costabel–Dauge–Nedaiasl, *Stability Analysis of a Simple Discretization Method for a Class of Strongly Singular Integral Equations*, Integral Equations and Operator Theory 95, article 29 (2023), DOI 10.1007/s00020-023-02750-7, proves the static bounded-lattice theorem. The full accessible author manuscript arXiv:2302.13159v3 was read, especially Sections 1.2, 1.6, 2.2, 2.4, 3.5 and Proposition 3.15. Its introduction explicitly reserves the nonzero-frequency treatment for later work. The final publisher metadata and abstract were accessed; the full typeset article is subscription-restricted and was not accessed.

On 2026-10-01 the author's current recent-publications list and targeted searches for subsequent DDA stability, nonreal spectral convergence, and the announced nonzero-frequency paper were checked. No exact later resolution was identified. This is a bounded literature check, not a novelty guarantee. The candidate credits the static theorem and standard compact Fredholm/Riesz theory; it does not label those as discoveries.

The complete pinned problem record was read. No separate research_results entry exists under OWR-11101924-008; the catalog review hash matches the join with an empty report object. The problem record itself contains its dated source triage. No previous Alec/campaign PR, exact target branch, or committed target folder was found in the gate. No source/review-history files were overwritten and the global queue was not regenerated.

Primary URLs and full-file hashes are in source_manifest.json. Source PDFs and page images remain local reading copies, outside this portable packet.
