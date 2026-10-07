# Equilateral polygon locking: accepted stalled partials

**Problem 2731 / KP-1.72, rank 906. Unsolved, 3/5 approaches.**

The [original proof notes](author_original/PROOF_AND_GAPS.md), [full independent audit](independent_audit/INDEPENDENT_AUDIT.md), and [exact acceptance](independent_audit/EXACT_ACCEPTANCE.json) are preserved unchanged. The two original ZIPs and their external manifests are in `archives/`. No mathematical correction was required and no corrected derivative exists. Historical pending-audit and unpublished fields remain as part of the original freeze; the later acceptance and this publication do not rewrite them.

Accepted scope: an embedded unit-edge subdivision family demonstrating loss of coarse bar constraints; an explicit flattening motion under embedded projection and equal absolute height increments; a precise obstruction to that common-rescaling formula; a smooth based semialgebraic configuration-space formulation; effective decision reduction for each fixed n; and quantitative local embedding stability.

The general problem remains unresolved. There is no locked equilateral example, universal fixed-edge unlocking theorem, executed component decomposition, or uniform bound on n. The finite tests are not a proof of global connectivity. No novelty, priority, human peer review, or formal proof-assistant certification is claimed.

The whole simple-projection class was already treated by Calvo, Krizanc, Morin, Soss, and Toussaint in [Convexifying polygons with simple projections (2001)](https://doi.org/10.1016/S0020-0190(01)00150-8). The accepted restricted formula does not extend that result. Calvo's [Geometric knot spaces and polygonal isotopy](https://arxiv.org/abs/math/9904037) separates unit-edge and variable-edge spaces: the unit-hexagon unknot component is connected, so any counterexample requires at least seven edges. Variable-edge heptagon statements are not substituted for equilateral ones.

## Reproduce

Run `python -I -S -B verify_publication.py`, then the same with `-O`. The wrapper checks all publication file hashes and the exact inventory, hard-pinned freeze objects, every ZIP/member equality, independent acceptance and semantic scope, and runs the unchanged independent audit under normal and optimized Python from a different working directory. The latter includes author relocation, 12 checker-mutation rejections, two input-pin controls, 61,776 independent segment-oracle comparisons, and 4,000 symmetry checks. These remain finite regressions supporting, not replacing, the written mathematical audit.

Run `python -I -S -B test_publication.py`, then the same with `-O`, for relocation and fail-closed publication negative controls. The wrapper uses explicit exceptions, not removable assertions.

Optional full inputs: pass `--catalog FILE --problems FILE --reports FILE --source-dir DIRECTORY`. Corpus options must be supplied together. The source directory needs the four PDF basenames listed in the unchanged independent replay. Full-source checks require Poppler (`pdfinfo` and `pdftotext`); the other checks use the Python standard library. Source PDFs and corpus data are deliberately not bundled. The wrapper records omitted inputs as skipped and emits metadata only. No network is used. Full-input normal and optimized runs in the publication record match the accepted replay exactly; this verifies the pinned local sources and corpus, not a new literature search.

Optional `--queue-base FILE --queue-current FILE` verifies that only the target Status and Turns cells change. Findings, notes, chat links, DOI cells, and every unrelated queue byte are preserved from the stated fresh main commit. The publication manifest excludes itself by design; the remote receipt binds every published file including that manifest.

Third-party PDFs, extracted source text, source-page images, corpus contents, private sources, and private coordination material are excluded. The K3 preliminary author source prohibits reposting without permission; it is cited only. This is a draft PR publication, with CI reported separately. No checks is not a CI pass.
