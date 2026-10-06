# Cap-chart family audit — final report

Frozen input: PR 18 / 30001075, head `99e403e85d38d92b021198c4a57bbad3cd8775ba`; candidate SHA-256 `b04aaf0b5a42d79ad26daf27880774a3f126858ef545b3f366a2b8b62e277252`.

**Verdict: the universal nonsmooth cap-chart mechanism passes independent analytic reconstruction. No central mathematical gap was found.** The chart construction includes arbitrary corners, nonunique supporting normals, nonstrict bodies, long contact segments, planar transverse cases, tiny positive contact separations, and arbitrarily narrow normal hemispheres. The exact root-domain and fixed-cap countability arguments are checkably reconstructed in [FIRST_PASS.md](FIRST_PASS.md).

The first pass was sealed at **2026-10-01T17:04:49.460039+00:00**, before reading historical reviews/code/results, root findings, or sibling conclusions. [FIRST_PASS_SEAL.json](FIRST_PASS_SEAL.json) hashes the analytic report, new control program, new results, and independently retrieved primary-source metadata. Its analytic report remains unchanged after sealing. No root or sibling conclusion was subsequently needed to produce this report.

## Strongest verified result and exact gap

For two disjoint compact convex sets of affine dimension at least two, after removing lines contained in a planar set's affine plane, the retained bitangents have a countable Lipschitz two-parameter cover. Localization around strictly interior ball contacts preserves both the entire support-normal cone and affine dimension. The two height-interpolating motions produce strictly positive own-coordinate gap increments and small cross-coordinate increments. Compactness supplies a uniform nearby-active-normal hemisphere. Explicit sign brackets supply root maps on a closed square; the root map is a contraction into its interior, and its fixed point depends Lipschitz-continuously on the two free parameters. The countable extraction uses the zero set of **the same fixed caps** in each neighborhood and remains valid when contacts move.

This lemma composes consistently with the source's density-point rank restriction, three distinct contact heights, identically zero quadratic determinant, and equal-dimensional area formula. The preliminary disjoint-ball closure reduction covers arbitrary convex sets. The strongest supported target is the outer-null union of common supporting-plane tangent lines. The stronger manifold-covering Conjecture 3, historical novelty, and external peer review are not established by this audit.

**Central gap remaining: none found.** The frozen text has two notation defects described below. External worldwide priority clearance is outside this phase.

## Must-fix versus optional

Must fix for publication of the exact frozen text:

1. `CANDIDATE.md:57`: replace the corrupted `u:=u` with `u`.
2. `CANDIDATE.md:190` and `:194`: define a separate `nu(q)=u(q)+z_i v(q)` in equation (13), then use it consistently. The current equation self-redefines the original u, while the following line uses undefined nu. The intended mathematical equation is valid and was independently reconstructed.

Optional explanatory improvements:

- Add the explicit sign-bracket and square-self-map inequalities given in FIRST_PASS.md.
- Name the fixed-cap set T_P and record `T_P intersect U_L subset Gamma_L` before the countable subcover extraction.
- State that alpha and contact separation d may vary with the chart; no global positive lower bound is required.
- If desired, describe the countable closed rational-ball family as having interiors which form a base. This avoids the technical convention that a topological base consists of open sets; it changes no mathematical content.

## Independent finite controls

[independent_controls.py](independent_controls.py) is fresh standard-library-only exact rational code. It read no author/reviewer program before sealing. [independent_results.json](independent_results.json) reports **34,489 passing assertions in 25 categories**. It checks signed support differences on independently generated nonsmooth finite convex hulls, interpolating bases with equal/opposite/nearly aligned directions, own/cross cap increments, concrete nonsmooth prism roots and Lipschitz bounds, strict bracket/self-map constants, tiny rational ambient balls after rotation, and frozen input hashes.

It also detects actual failures when assumptions are removed: reversing the support increment sign, putting a contact on the ball boundary, allowing a cap's heights beyond the other contact, omitting projection interior, and treating an original tangent's neighborhood as if all its contacts stayed in one chosen cap. The last example verifies why the candidate's fixed-cap countability argument is essential. These finite checks do not prove the universal theorem.

## Post-seal historical comparison

Only after sealing did I read `source_snapshot/verify.py`, its result, the historical independent program/result/summary, and `review/REVIEW.md`. The historical review agrees with the independent analytic verdict and discusses the same support/cap/contraction/countability mechanisms. It reports no mandatory corrections; it did not flag the two notation defects above.

Both historical programs were run from byte-for-byte copies under ignored `tmp/historical_run/`. A read-only existing Python environment with SymPy 1.14.0 supplied their dependency; no package was installed and no environment was changed. Bytecode writes were disabled. [post_seal_reproduction.json](post_seal_reproduction.json) records exact JSON equality for both outputs and verifies that **all 15 frozen snapshot files remain unchanged**.

- The author's program reproduced 810 exact finite support-increment cases, four cap-margin models, 81 linear contraction models, and its symbolic algebra identities.
- The historical independent program reproduced its stated 36 named diagnostics: five initial algebra/derivative checks, 25 margin checks, and six finite support-increment checks.

The counts are accurate but do not certify a universal geometric cover. This independent report's universal status comes from the analytic reconstruction, not the historical PASS labels or diagnostic counts.

## Evidence and operational scope

The exact source statement and required standard machinery were read independently from primary sources. [primary_source_manifest.json](primary_source_manifest.json) records URLs, page/theorem locators, UTC retrieval times, byte sizes, and PDF SHA-256 hashes. The OWR definition matches the claim. The complete Banach contraction theorem requires a self-map of a complete space, which the explicit closed-square construction supplies. The equal-dimensional area-formula image inequality does not require injectivity, which is consistent with the sweep argument. The thesis retrieval failed; no unverified thesis statement is used as evidence here.

[RESEARCH_LOG.md](RESEARCH_LOG.md) records UTC checkpoints and nonmonotonic-allowed completion estimates. [verdict.json](verdict.json) is the machine-readable disposition, and [HASH_MANIFEST.json](HASH_MANIFEST.json) records deliverable hashes and unchanged source provenance. All outputs reside in this dedicated family folder, with temporary executions and foreign PDF caches ignored under `tmp/`. No Git operations, canonical edits, queue/ledger changes, research-environment modifications, outreach, paper actions, or release actions were performed.
