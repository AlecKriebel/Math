# Public source and scope summary

Target: 8000011 / AMR-079-0011, The Toda lattice with random initial data. The repository queue ranks it 427. Five substantive author turns were completed; the original general-dimension expected-time problem remains unsolved.

## Literal problem

Percy Deift, *Some Open Problems in Random Matrix Theory and the Theory of Integrable Systems* (2007), Problem 11, printed pp.8–9: https://arxiv.org/abs/0712.0849. The question concerns average diagonalization time for a random finite tridiagonal GOE matrix under Toda dynamics until all positive off-diagonal entries are below a given epsilon. The source is an open-ended average-complexity question; it prescribes no fixed-n or coupled n/epsilon limit. It also discusses one-end deflation, which is a distinct stopping rule.

The source gives independent Gaussian diagonals and chi_(n−j) off-diagonals, but does not print the diagonal variance there. This work explicitly declares a_i~N(0,2), b_i~chi_(n−i), and J'=[B,J] with positive upper and negative lower entries in B. The exact stopping time is the first simultaneous crossing, not permanent decoupling.

## Classical inputs and related literature

- Moser's finite Toda spectral evolution and the Gram/Hankel determinant formulas provide the classical deterministic solution. The proofs show how positive finite spectral sums yield the stopping-time bounds; the independent review checks the clock directly through q_j'=(lambda_j−a_1)q_j.
- Dumitriu–Edelman, *Matrix Models for Beta Ensembles* (2002): https://arxiv.org/abs/math-ph/0206043. Theorem 2.1 gives the GOE tridiagonal construction; Corollary 2.2 and Theorem 2.12 supply eigenvalue/first-row-coordinate independence and normalized chi coordinates. Squaring gives Dirichlet(1/2,...,1/2) spectral weights. Their matrix scale differs by sqrt(2) from the declared convention.
- Pfrang–Deift–Menon, empirical eigenvalue-runtime study: https://arxiv.org/abs/1203.4635. Deflation-runtime observations do not determine this all-coupling mean.
- Deift–Trogdon, largest-eigenvalue Toda universality: https://arxiv.org/abs/1604.07384. Its large-N 1-deflation distributional theorem is not a general finite-N all-coupling expectation theorem. Convergence in distribution alone does not establish convergence of means.
- Deift's 2017 update: https://arxiv.org/abs/1703.04931.
- Deift–Dubach–Tomei–Trogdon, 2025 monograph: https://doi.org/10.1017/9781009664332. The public Chapter 6 scope statement, https://doi.org/10.1017/9781009664332.007, explicitly concerns 1-deflation. The full monograph was not supplied for audit.

The bounded literature check found no verified general all-coupling mean resolution. That is not proof of novelty or an exhaustive current-literature certificate. The imported prior report was qualitative and is credited without counting as a new proof turn.

## Dataset provenance

The imported record was extracted only after the source files matched the repository manifest for ulamai/UnsolvedMath snapshot 37e53eabe540fb458758e198be61634bd02ee008:

- problems.json: 68,931,837 bytes, SHA-256 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf
- research_results.json: 80,334,822 bytes, SHA-256 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b

Repository manifest: https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/manifest.json. The independent review preserves hashes of its supplied reading copies in SOURCE_INVENTORY.json without redistributing them. No raw PDFs or imported full reports are included.
