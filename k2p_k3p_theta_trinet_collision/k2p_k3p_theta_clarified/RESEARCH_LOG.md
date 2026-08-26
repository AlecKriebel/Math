# Research log

## 2026-08-25 21:47 PDT -- Version 1.1.0 source-freeze checkpoint

- Completed independent post-revision proof and verifier audits. No remaining
  mathematical, computational, or manuscript defect was found; neither audit
  recommends changing the title or principal theorems.
- Rebuilt the 14-page manuscript and both two-page supporting PDFs after the
  last source edit. The final logs contain no TeX warning, overfull/underfull
  box, unresolved citation/reference, or error; all fonts are embedded, and
  full-page visual inspection found no clipping, overlap, or broken layout.
- Replayed all exact checks in normal and genuinely optimized modes under
  Python 3.14 and Python 3.11. Every run exactly matches the stored transcript
  and ends with `ALL EXACT CHECKS PASSED`.
- Hardened the release builder so the requested version, committed
  `CITATION.cff`, and exact tag must agree; the canonical manifest path set,
  both archive forms, stored transcripts, clean replay, and rebuilt PDF text
  and rendered pages are all fail-closed release gates.
- Best-guess completion: **99% of technical bioRxiv readiness**. The remaining
  technical step is the commit/tag-bound archive replay. Portal account email,
  distribution license, subject/category confirmation, and submission approval
  remain author-controlled choices.

## 2026-08-25 -- Version 3 response and submission-repair checkpoint

- Independently compared arXiv:2607.12919v2 and v3. Version 3 removes the
  arbitrary-level K2P lemma and global K2P corollary, identifies the same
  leaf-order obstruction, leaves high-level K2P and K3P trinet questions open,
  and publicly acknowledges Alec Kriebel.
- Replayed the untouched version `1.0.0` exact suite before revision; all
  checks passed.
- Adjudicated every item in an external adversarial review. The mathematical
  collisions, ranks, local dimensions, and analytic K3P argument remain intact.
  Valid repairs concern source-version framing, `Theta_0`, edgewise
  continuous-time scope, global genericity, tree-child scope, terminology,
  related work, and release isolation.
- No external communication was initiated by the revision process. Suggested
  outreach was excluded under the independent-research policy.
- Best-guess completion: **85% of version 1.1.0 bioRxiv readiness**. Remaining
  work is full text review, verifier/report regeneration, PDF build and visual
  QA, clean release replay, independent adversarial freeze review, and the
  author-controlled portal choices.

## 2026-08-23 22:35 PDT -- latest-main and release-builder checkpoint

- Rebasing onto the latest remote `main` added an independent K2P-SAME quartet
  audit. Its exact checker confirms a coordinate defect in that separate
  project's printed quartet separators; it does not affect this paper's
  three-leaf coordinates, collision theorems, or verifiers.
- The first commit-pinned release build exposed a provenance-byte mismatch:
  shell newline stripping made the archived `FILE_SHA256SUMS` differ from the
  hash recorded for that file. The builder now preserves final newlines and
  compares both generated metadata files byte-for-byte inside both ZIP and
  tar.gz forms before emitting either archive.
- Best-guess completion: **99% of technical bioRxiv readiness**. Remaining work
  is the corrected archive rebuild, clean-extraction replay, tag/push checks,
  and the author-controlled portal decisions.

## 2026-08-23 22:25 PDT -- adversarial submission freeze checkpoint

- Completed independent proof and verifier audits. No high- or medium-severity
  mathematical or computational defect remains, and no title or principal
  theorem change was required.
- Made model conventions, unrestricted parameter maps, exact minors, local
  collision geometry, and continuous-time implicit-function claims directly
  checkable in the paper and bound them to named certificate data.
- Hardened certificate schema, field-label, topology, isolating-interval,
  sidecar, minimum-margin, and Python optimized-mode checks. Targeted corrupted
  certificates fail closed, and the simple generator remains byte-identical.
- Rebuilt and visually inspected all 13 manuscript pages and both pages of each
  supporting PDF. All fonts are embedded and the final build emits no TeX
  warning or error.
- Replayed the complete exact suite normally and with optimization enabled;
  both runs ended with `ALL EXACT CHECKS PASSED`.
- Best-guess completion: **97% of technical bioRxiv readiness**. Remaining work
  is manifest/release generation, clean-extraction replay, exact Git publication,
  and author-only portal choices (email, affiliation confirmation, category,
  distribution license, and confirmation of funding/competing interests).

## 2026-08-23 21:56 PDT -- bioRxiv and archival preparation checkpoint

- Audited current official bioRxiv/openRxiv guidance for scope, research-article
  screening, author-created PDF formatting, subject/result categories, funding
  metadata, distribution licenses, DOI assignment, posting permanence, and
  screening timing.
- Identified the main platform-specific risk: mathematical work is accepted only
  when directly relevant to the life sciences. The submission worksheet therefore
  foregrounds the consequences for evolutionary/phylogenetic inference and
  suggests Evolutionary Biology and New Results for author confirmation.
- Designated this clarified directory as the sole canonical submission and
  release source without deleting the historical parent files.
- Added citation, code-license, mixed-material-license, bioRxiv metadata,
  Zenodo-template, and clean deterministic release-build support.
- No manuscript theorem/title/abstract edits, verifier edits, release creation,
  DOI creation, or external communication were performed in this subtask.
- Best-guess completion: **95% of the submission/archival-support subtask** and
  **70% of overall bioRxiv readiness**. Remaining work is the mathematical and
  editorial manuscript repair, verifier hardening, regenerated PDFs/reports and
  manifests, final author metadata/license choices, clean-checkout replay, and
  portal preview.

## 2026-08-13 07:00 PDT

- Confirmed that the focused displayed-tree verifier did not itself perform the five-coordinate Lemma 4.1 convention check described in the clarification note; that check had existed only in the complete suite's separate source-convention step.
- Audited an exact rational proposed check against the source paper's five displayed formulas and the existing convention checker.
- Embedded the check in the focused verifier, replayed the focused and complete exact suites successfully, and refreshed the author-facing audit package.

## 2026-08-12 20:36 PDT

- Created this dedicated clarification directory from the latest public `main` snapshot without overwriting the pre-clarification paper, summary, certificates, or original verifier modules.
- Confirmed the repository is public and located the earlier combined package at commit `ca21a733`.
- Replayed the untouched compact and complete exact verifier suites successfully before editing.
- Confirmed that the figure already assigns `S` to both `p`-arcs and `T` to both `q`-arcs; the defect is textual underspecification and compact-verifier coverage.
- Implemented an exact graph-derived displayed-tree verifier in `Q(sqrt(71))`.
- Verified the four retained-parent monomials, common `K` factor, all sixteen core identities, exact transition matrices, all 64 Fourier coordinates, and all 64 direct-pruning probabilities.
- Added the clarified paper, two-page summary, and compact clarification note; no mathematical witness or conclusion was altered.
