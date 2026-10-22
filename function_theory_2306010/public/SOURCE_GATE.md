# Source, resolution, and duplication gate

Checked **2026-10-04 UTC**. Target: **2306010 / AMR-022-6010 / Function Theory 6.10**, rank **581**.

## Exact source and normalization

1. Requested catalogue: https://www.unsolvedmath.com/problems/2306010 . The web fetch was inaccessible. It is not relied on for current status.
2. W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2). Problem 6.10 and Update 6.10 are on printed p.119 (PDF page120); that page image was inspected. The class Σ is defined on printed p.114 by analytic univalent Laurent series z + Σ[n≥1] bₙz⁻ⁿ, with zero constant term. The construction in PROOF.md satisfies this exact normalization.
3. The original question concerns convexity of the omitted compact set for a convex combination of two exterior-convex maps. It is not a question about convexity of their image domains, nor the analogous unit-disk question 6.11. The 2018 update reports no progress then; it cannot establish current openness.

## Verified prior resolution

Yuankai Guo and Xiaozhe Hu, *A Counterexample to a Problem of Pommerenke on Convex Functions in the Class Σ*, [arXiv:2609.04279v1](https://arxiv.org/abs/2609.04279v1), submitted 2026-09-03. The six-page PDF and the [primary HTML](https://arxiv.org/html/2609.04279v1) were inspected. The exact negative certificate on PDF p.5 was checked visually. Sections 2–3 give the same complete target and an explicit rational counterexample, not merely a conditional reduction or numerical candidate.

PROOF.md reconstructs the complete analytic, geometric and algebraic argument. In particular it verifies single-valuedness of the primitive, the power branch, global injectivity, correct convex-complement geometry, and exact negativity at an interior exterior-disk point. It independently proves the required smooth-boundary implications rather than silently treating positive curvature as a definition of convexity. The construction and negative answer are credited to Guo–Hu, and no novelty is claimed for the reconstruction.

A bounded literature check used exact problem-number, author/title, counterexample, error, correction and arXiv-ID searches. The arXiv primary landing page showed only v1. No later correction or withdrawal was located. This is a bounded source check, not a guarantee about all unpublished or unindexed developments. No peer-reviewed publication was established in this check.

## Formalization scope

The author's [public formalization](https://github.com/Theophilus1030/Pommerenke/tree/bdc48d75778148730d551812647bfdac82d51df3) was inspected at the pinned commit `bdc48d75778148730d551812647bfdac82d51df3`. The README, `MainTheorem.lean`, `Problem610GeometricNonconvex.lean`, toolchain and dependency manifest were read. The last file provides a geometric nonconvexity bridge beyond the analytic-only predicate in the older top-level theorem. Its final certificate is named `pommerenke_complete_geometric_counterexample_certificate`.

This packet does **not** claim to have rebuilt the Lean project or checked its full dependency graph. Lean and Lake were absent. The pinned toolchain is Lean `v4.34.0-rc2`; Mathlib revision is `85e3a25e006c35636f0e53b0e9296caca2685bc0`. The conventional proof is sufficient independently of that build.

## Imported statement and previous report

The complete selected imported statement and complete prior report were read privately. The report is only OPEN-TRIAGE: it says the problem was open as of the 2018 edition, that a web search found nothing, and that preservation of convexity remains. It supplies no earlier proof, computation, or partial theorem. This report predates or misses the September 2026 resolution and is superseded by it.

The cached problem corpus is upstream revision `372682f27c1b0d3d39e75fa63ad7932c7a2e1bde`; the repository manifest currently pins `37e53eabe540fb458758e198be61634bd02ee008`. This version distinction is explicit. The exact selected statement was independently reconciled with Hayman–Lingham's primary source. The report corpus SHA256 matches the repository's pinned report manifest. No full corpus or source PDF is included in the public packet.

## Repository and duplicate check

Baseline main: [`df9f2c05f61cad48f851c2d2ba7a63611a0acfa0`](https://github.com/AlecKriebel/Math/tree/df9f2c05f61cad48f851c2d2ba7a63611a0acfa0).

The live queue row is rank581, `queued`, `0/5`. The full queue bytes were independently checked against the pinned read-only GitHub REST response: blob `c1009ab2e12b93cffb15cb17c0ac893979ce5a44`, 385544 bytes. A malformed historical header inside the file includes a different old SHA and size; it is content, not current metadata. It is unrelated to this investigation and must remain unchanged in any own-row update.

The complete current state file contains no target entry. Exact-ID code search, all-state PR searches for `2306010`, `AMR-022-6010`, and `6.10`, an exact-ID branch search, and the live attempts-directory listing found no matching prior repository attempt. A Pommerenke PR search returned a different target, Function Theory 4.9 (2304009), which is not a duplicate. The related-target grouping has no 2306010 entry. A bounded corpus comparison located other Σ/convexity mentions, but 6.8 concerns integral means, 6.112–6.113 concern neighborhoods, and 6.11 concerns the unit disk; none has this exact target. These checks do not assert access to every deleted or unreachable historical branch.

## Disposition

Proposed classification: **already_solved**, **1/5** substantive turns, by full reconstruction of Guo–Hu's prior counterexample. There is no remaining mathematical gap in this candidate reconstruction; the fresh independent audit is still pending. Queue change, if approved, is restricted to this row's Status and Turns. No remote writes have been made.
