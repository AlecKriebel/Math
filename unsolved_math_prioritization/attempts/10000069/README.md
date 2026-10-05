# Qualified credited spectral characterization: 10000069

Problem 10000069 / AMR-099-0069, rank 711. Release review: 2026-10-05.

**Disposition: partial, credited exact implicit spectral characterization. Queue: unsolved; one substantive route, 1/5. The informal full “shape” is not claimed solved.** The independent analytical audit found no fatal spectral-proof gap. This is a reconstructed prior result, not a new theorem, novelty certificate, human peer review, or formal verification.

## Mandatory local correction

This guide adopts erratum E1 in [ERRATA_AND_SCOPE.md](independent_audit/ERRATA_AND_SCOPE.md). In the frozen author/PROOF_RECONSTRUCTION.md, line 90 must be read as

E(X-Y)^2 = 2(EX^2-1) <= 2(R-1).

The frozen equality with the second-moment cap is incorrect: R bounds EX^2 and need not equal it. The corrected chain preserves the stated minimum bound, rho bound, and right-end asymptotic. Both original packets remain byte-for-byte unchanged. Read this controlling guide and the erratum before using the reconstruction.

## Exact result and credit

Credit belongs to [DannyExperiments/random-series-parallel-distance-exponent](https://github.com/DannyExperiments/random-series-parallel-distance-exponent/tree/a875da08e8bfbdb70fd8165c097ab036731b5f6f), pinned commit a875da08e8bfbdb70fd8165c097ab036731b5f6f. The audited theorem concerns the terminal-distance **expectation** exponent delta(p) = lim log(E D_n)/n for independent hierarchical multigraph edge replacement, where p is the probability of series replacement. It proves an actual attained maximal nonlinear eigenprofile and matching lower/upper variational formulas for p in (1/2,1), rather than merely renaming the defining limit.

No elementary scalar formula, full global-shape theorem, global convexity, eigenprofile uniqueness, or convergence of every normalized law is claimed. The known critical endpoint is obtained here using the published near-critical theorem and monotonicity; p=1 is deterministic. The published convention is epsilon=p-1/2 and delta(1/2+epsilon)/sqrt(epsilon) tends to pi/sqrt(6). Finite controls do not replace the analytic arguments.

## Source limitations and later literature

**Original author PDF: HTTP 404, corroboration only through indexed primary excerpts. Exact catalogue: HTTP 403.** Neither original PDF bytes nor the full current catalogue statement nor raw-corpus statement hashes are certified. These limits remain after review.

[The independent audit](independent_audit/AUDIT.md) reviews the complete spectral argument. The frozen author packet's “pending independent review/acceptance” and “no remote changes” sentences describe its earlier checkpoint; the qualified disposition in this guide now controls. Its route accounting remains 1/5; audit and publication do not consume new discovery routes and do not establish five-route exhaustion.

[The source update](independent_audit/SOURCE_UPDATE.md) records Ding, He, Liang and Zheng, *Distance and resistance on random series-parallel graphs: logarithmic speeds and near-critical asymptotics*, [arXiv:2609.23802v1](https://arxiv.org/abs/2609.23802v1), submitted September 2026. Its statements claim almost-sure and L1 logarithmic speeds matching the expectation exponent. The statements were inspected, but the 41-page proof and stated Lean formalization were not audited. This preprint is not a dependency of the spectral characterization. The candidate theorem's exclusion of almost-sure claims is not a literature-wide assertion of openness.

## Reproducible package

- author/: 10 frozen files, including its manifest; 2,158 exact control assertions.
- independent_audit/: 12 frozen files, including its manifest; 156,596 separately authored exact assertions and ten mathematical negative controls.
- RELEASE_STATUS.json: current qualified disposition.
- RELEASE_MANIFEST.json: exact release inventory, byte counts, and SHA-256 hashes.
- verify_release.py: standard-library, offline byte-binding and exact-output replay with actual corruption controls.
- REPLAY_RESULTS.json: portable replay and mutation-control outcome.

Run `python3 -I -B verify_release.py --self-test` from any directory. The audit is invoked with the explicit sibling author directory; no original workspace path is required. Integrity gates also run under Python optimization. The package excludes downloaded PDFs, extracts, images, raw external records, and private coordination. Public scholarly titles, URLs, hashes, byte counts, and inspection status are metadata only.

This draft contains no merge, release, DOI deposit, or outreach. GitHub checks, if absent, are not represented as passed. Completion estimate for this scoped publication/reconstruction deliverable: 100%; no numerical completion estimate is asserted for the original full-shape question.
