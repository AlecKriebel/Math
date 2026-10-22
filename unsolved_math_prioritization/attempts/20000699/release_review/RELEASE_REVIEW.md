# Independent release review: conditional Möbius–ratios–prime witness

Date: 16 October 2026. Target: row 1795, ID 20000699, AIM-ANALYTIC_NUMBER_THEORY-0063.

## Decision

**PASS — the frozen public candidate faithfully preserves the accepted amended conditional V1 witness and is suitable for authorized draft-PR publication.** No release-blocking discrepancy was found. This is a release and reproducibility review of an already accepted proof, not a new mathematical pass, a proof of the arithmetic hypothesis, or a broader resolution claim. No publication was performed by this review.

The queue disposition is accepted only with its explicit qualifier: **resolved, 1/5, for the amended conditional finite-polynomial interpretation**. Before publication, recheck the current repository queue base and preserve every unrelated byte; this review verifies the supplied pinned queue candidate, not future repository state.

## Frozen identities and complete proof preservation

- Public `MANIFEST.json` SHA-256: `17270a8e1f6c83d8aec8f0b04ce53d4385eb67ed33ab07c858ec9cb20f793a98`.
- Frozen candidate manifest SHA-256: `9f42c461ba6a3f1f594dc8d80e372aa20a17ba3e38bc0fccb0ddabb74bd019da`.
- Accepted original combined theorem SHA-256: `17b1ea3cc46ee519f5c5353f172dffadbc9cd61bfcf0c0927aed846b2ee6eccc`.

All 33 public files match the frozen candidate. The 18 original frozen-audit bindings and all eight exact-audit-receipt bindings were independently checked against the accepted original bytes. Their union, together with the two receipts themselves, yields 22 complete authored editions: 13 byte-identical and nine presentation-only. All 22 sealed originals agree with the original research files. The accounting file correctly covers all 27 historical references, including the separately referenced source audit.

Every presentation diff was inspected. Edits remove coordination wording, explain the historical gate's status, make inspected arXiv versions explicit, and clarify assertion-enabled replay. They do not change mathematical formulas, proof arguments, hypothesis quantifiers, conclusion strength, or checker bytes. The full sharp transfer, sharp-to-linear comparison, Euler/Mellin proof, reverse theorem, nonvacuity obstruction, exact audit, interpretation amendments, combined theorem, and acceptance records are present. The original unamended gate is prominently marked as historical and superseded.

## Mathematical scope preserved

The combined theorem retains all of the following:

1. The mandatory parameter correction `0 < psi <= phi < 1`, together with `1 < lambda < min(2,1/phi,1/(1-psi))`. Removing the known obstruction does not assert that the remaining arithmetic hypothesis is true or fully consistent.
2. Explicit, uniformly quantified `H_CK` on the actual two oriented cumulative coefficient sums and the prescribed Ramanujan density. Its constants, real endpoints, integer gap range, complex four-shift polydisc, and optional fixed small-endpoint threshold are stated. `H_CK` remains unproved.
3. The exact finite polynomial, sharp coefficient cutoff, exact logarithmic Fourier kernel, both orientations, endpoint equality cases, and local collision holomorphy. The forward estimate remains `O(N^phi)` and the mixed Cauchy loss remains exactly `rho^(-2)`.
4. The corrected one-swap factor `B_(-beta,-alpha-s,gamma+s,delta)(1)`. The Euler identity is obtained from the prescribed density, rather than by accepting the literal printed spectral-parameter formula.
5. The whole-real, real Schwartz band-limited weight and the explicit endpoint
   `E_z = 2 pi w(0) N^(1-alpha-beta) / [(1-alpha-beta) zeta(1+gamma-alpha) zeta(1+delta-beta)]`.
   No `w(0)=0` substitution removes it. The final correspondence retains the stronger `O(N/(T (log N)^2))` sharp-to-linear error, the contour residue, and the finite-height order-of-integration qualification.
6. The evaluated Hardy–Littlewood singular-series **smoothed prime-power aggregate**, with exact diagonal, all four derivative signs, prime powers, odd-gap obstruction, and quantified density-convention difference. Its conditional error is `O(N^phi (log N)^2/c^2)=o(T)`.
7. Explicit exclusions of individual fixed-gap Hardy–Littlewood asymptotics, unrestricted full-zeta ratios, all-rank conclusions, proof of arithmetic randomness, novelty, priority, or exhaustive literature absence. Conrey–Keating and earlier uniform-differentiation work are credited.

The general reverse implication requires only the displayed uniform finite-ratios bound; the combined result invokes `H_CK`. The density-based Euler argument does not import the source's additive-twist pole-extraction assertion. The latter retains its GRH qualification whenever separately invoked.

## Source-version and disclosure boundaries

The correction notice identifies the displayed formulas in Conrey–Keating, *Pair correlation and twin primes revisited*, [arXiv:1604.06124v2](https://arxiv.org/pdf/1604.06124v2), and the corresponding singleton discussion in *Averages of ratios of the Riemann zeta-function and correlations of divisor sums*, [arXiv:1611.09198v1](https://arxiv.org/pdf/1611.09198v1). It does not declare either whole paper invalid or transfer arXiv theorem/page numbering to the separately identified journal edition. The whole-line endpoint is identified as a weight/contour adaptation requirement. Prior ratios differentiation is credited to [Conrey–Snaith, arXiv:math/0509480v2](https://arxiv.org/pdf/math/0509480v2).

Public historical-source metadata agrees with the supplied source-preparation records. The public package contains authored proofs and permitted verification metadata, with no copied PDFs, extracted source documents, dataset contents, or private coordination files. All explicit local Markdown links resolve within the package. A text scan found no workspace paths, private chat links, email addresses, or credential patterns.

This review did not redownload the cited sources, refresh the datasets, or recertify whole source papers. The public offline verifier accurately labels excluded-source and dataset checks as historical metadata rather than live verification. All 26 original research-tree files, including retained source originals, still match the builder's baseline and were unchanged by this review.

## Independent portable replay

The 33 public files alone were copied to a fresh temporary directory with spaces in its name. Every invocation ran from an unrelated working directory with the independently supplied manifest trust anchor. No original-tree fallback was needed. The frozen verifier and four mathematical checkers were inspected before execution.

Python 3.12.14 with SymPy 1.14.0 passed six configurations: normal Python, `-O`, `-OO`, inherited `PYTHONOPTIMIZE=1`, inherited `PYTHONOPTIMIZE=2`, and `-OO` combined with `PYTHONOPTIMIZE=2`.

Results:

- 24 clean mathematical checker executions: four in each configuration.
- 108 successful negative-control rejections: 24 false-assertion tripwires, 24 mathematical mutants, and 60 integrity corruptions.
- Every child ran with optimization zero, `__debug__` true, a rejected false-assertion probe, and explicitly unoptimized compilation.
- Every stored output was deleted before replay. Exact, Euler, and independent-audit output bytes matched their fixtures. The reverse check matched every nonfloating field, satisfied its finite `1e-12` floating tolerance, and also matched the original bytes on this platform.
- All public and original research bytes remained unchanged. Standard error was empty for all six complete verifier runs.

The verifier's internal consistency checks are not an authenticity guarantee if an attacker replaces both payload and manifest; the README correctly supplies the optional external manifest trust anchor. Finite regression counts overlap and do not establish the infinite analytic theorem or `H_CK`.

See `INDEPENDENT_REPLAY_MATRIX.json` and the six `REPLAY_*.json` records for the exact execution receipts. `STATIC_BINDINGS_REVIEW.json` and `SOURCE_AND_BOUNDARY_REVIEW.json` record the independent binding and disclosure checks.

## Queue boundary

The reviewed queue base is commit `20c8cb80f5d21b2598a580a18da095d4fec86940`, Git blob `3f30cf4aafb054045fae15e18eba0957f8b763bc`. The candidate SHA-256 is `4a3d1272abbf3a6661d7d6b9b3773c733e07e13d0a9ff4f06836586cdccc95f7`.

Exactly one row changes: 1795. Exactly three cells change: Status, Turns, and Findings. They state `resolved`, `1/5`, and the qualified conditional result, including all three mandatory corrections and the broader-claim exclusions. The header, other cells, all unrelated rows, and existing notes and links are byte-preserved. The candidate's Git blob and SHA-256 were independently recomputed.

**Final release disposition: PASS for the frozen, explicitly amended conditional witness, subject only to checking the repository queue base at publication time.**
