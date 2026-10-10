# Acceptance report: corrected scoped partials

Date: 7 October 2026. Problem 30005600 / OWR-14297736-006, queue rank 952.

## Accepted scope

The independent AI audit accepts the one-variable full-first-positive-eigenvalue theorem under max f <= integral_0^b f, the weighted kernel-corrected scalar Rayleigh formula, its elementary weighted bound, and the exact Fourier Ritz matrices. Its proof checks the operator and form domains, harmonic kernel, skew-lattice quasiperiodic sectors, conformal covariance and area scaling. It credits the published b>2*pi result and the b=2*pi endpoint consequence.

Acceptance requires the exact corrections in `review/SCOPE_CORRECTIONS.patch`, applied to the two separate reading copies. The energy obstruction applies only to a pulled-back harmonic map and its associated eigenpair. It leaves lower modes of literal cover metrics uncontrolled. No necessity of concentration or nonexistence of a smooth minimizer is inferred from the numerical search's failure to capture the known sub-flat comparison at b=2.

The complete pi-threshold lower bound remains unproved: the flat-value range pi<b<2*pi and the spherical-value range b<=pi, including equality of the candidate branches at b=pi. The five-approach budget is exhausted without a full proof or counterexample. Queue disposition is `unsolved`, with `5/5` turns. This is not a novelty assessment, human peer review, formal verification, or a spectral lower-bound certificate from computations.

## Preserved identity and reproducibility

- Author archive: 25,093 bytes; SHA-256 891e8c125dbb0310074a63f83d4071712cc50bab1584c6153ae829a5d5ed7782.
- Original proof: 20,099 bytes; SHA-256 c8bebb5be39bab1bbc1f2d28bbe99d021eeaf478499c3f385b1b689d3916c44b.
- Full audit: SHA-256 76e8414f0f0b75a5623befc01ceae7bb37283520f94e108c6affd3cc7e5ffa33.
- Exact scope patch: SHA-256 5e1af7fa8603e35e840661152c154b606d1e1189bea64ac939c947e261a7a99e.
- Corrected proof: SHA-256 71998b923d90e2aab30669c1d9fe6d829aaaf656869439191b9b13dcba4ce296.
- Corrected research log: SHA-256 bbb0e9ce433114e584fcd9cce456f47fd0ac5d5f9fb5c283d6092004b47b5077.

The original archive and all eleven extracted members are preserved byte for byte. The exact patch reconstructs the reading copies. All ten author-manifest entries and all ten review-manifest entries are checked against their recorded bytes and SHA-256 values by the source-free driver.

The normal and optimized Python exact controls reproduce the frozen JSON: 5,600 finite dual-lattice mode checks, 729 variance cases, 34 cosine parameters, three nontrivial parity characters, and three rejected-shortcut controls. These are finite algebraic checks, not verification of the infinite-dimensional analytic proof.

The independent auditor reran the complete numerical search and obtained byte-identical output (SHA-256 d4bd15167fe3881a4d7939b7221d7fefcfd6edebd54cd8a6cb8fc551b179900e). The independent direct-grid cross-check and exact-control replay receipts are preserved in `review/`. The default publication driver checks those frozen receipts and reruns the exact controls; it does not claim to rerun the numerical search unless `--numerical` is given.

## Public-source and publication limits

Primary citations and public-source inspection metadata are preserved with the corrected proof and source manifest. The mathematical auditor verified four locally supplied public PDF identities; those PDFs are deliberately excluded. The source-free publication driver neither re-downloads them nor verifies dataset hashes against absent dataset contents. Repository/corpus search history and source status are bounded dated evidence, not a worldwide-open-status guarantee.

Only this problem's `Status`, `Turns` and `Findings` queue cells are changed, using the actual header names. Existing Chat/DOI cells, all other rows and the existing malformed header bytes are preserved. No queue regeneration or unrelated ledger changes are part of this publication.

This packet is intended for one draft pull request. It authorizes no merge, release, DOI creation or outreach. The reported 12% full-goal completion estimate in the research log remains a historical heuristic, not a probability or measurement.
