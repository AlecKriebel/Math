# Research log

## 2026-08-27 06:48 PDT — Audit initialized

- Created a dedicated v1.2.5 referee workspace.
- Recorded submitted archive SHA-256:
  `e8302556f356ac04add887a59ab370d4a496f011d59ccfd8a3e87cc19876551e`.
- Inspected all 45 ZIP entries before extraction: no absolute paths, parent
  traversal components, or symbolic-link entries were found.
- Observed unrelated pre-existing changes elsewhere in the repository; they
  will remain untouched and unstaged.
- Review policy: read the manuscript before consulting packet prompts or the
  prior report; treat the editor's repair summary as hypotheses to falsify.

**Best-guess completion:** 5%.

## 2026-08-27 06:50 PDT — Archive provenance verified

- Copied the submitted ZIP into the audit workspace and extracted its sole
  top-level packet directory.
- All 41 files listed by the packet manifest passed SHA-256 verification.
- The audit-local ZIP copy has the same SHA-256 as the submitted attachment.

**Best-guess completion:** 8%.

## 2026-08-27 06:54 PDT — Paper-first and reproducibility checkpoint

- Read the 20-page manuscript in full before consulting the packet's support
  prompt, earlier referee report, or editing summary.
- Rendered and visually inspected every manuscript page, then read and
  visually inspected both pages of each supporting PDF (24 pages total).
- No clipped equations, missing glyphs, broken hyperlinks, or unreadable
  tables were found. The PDFs are untagged, an optional accessibility matter,
  but their static page layouts are clean and readable.
- Audited the manuscript's Version 2/Version 3 history directly against the
  primary arXiv PDFs. Version 2 literally contains the K2P Lemma 5.6 and the
  JC/K2P Corollary 5.8; Version 3 removes those K2P claims, explains the
  leaf-order obstruction, and poses high-level K2P/K3P extension as open.
- Ran `RUN_REFEREE_REPLAY.sh --with-pdf` from the packet. Normal and optimized
  complete suites, focused replays, four-leaf regression, K2P/K3P mutation
  guards, compact-certificate regeneration, PDF rebuild/text comparison, and
  both integrity passes all succeeded.
- Static diff against v1.2.4 confirms that the previously reported K3P graph
  semantic gaps and compact-K2P transition-row gap are addressed in executable
  code, not only in the coverage prose. Further independent hostile testing is
  still required.

**Best-guess completion:** 45%.

## 2026-08-27 07:02 PDT — Independent falsification checkpoint

- Reconstructed the compact K2P and quartic K3P factorizations, all 64 Fourier
  and ordinary-state coordinates, literal four-graph pruning, rank-9 and
  rank-15 minors, and the K3P fixed-output tangent in a clean SymPy 1.14
  environment that imports no packet code or certificate. All checks passed.
- Ran 18 independent hostile K3P probes. These include every v1.2.4 escape and
  fresh graph, descriptor, collision, pruning-source, Jacobian, and tangent
  corruptions. Every mutation failed at an operative semantic comparison.
- Mutated each of the six compact-K2P network transition rows and each of the
  three tree rows separately. All nine were rejected by their specific stored
  row comparison, including `K_odot_K`.
- Negative packet-boundary controls confirmed rejection of a changed byte,
  added file, missing file, and symbolic link.
- Strict duplicate-key JSON parsing passed for all five certificate files.
- Confirmed that all 35 packet `materials/` files are byte-identical to their
  counterparts at the stated canonical tag. The local and remote annotated tag
  peel to commit `9f8d2682ead74e23b7badd9d7f46869477b4e84f`; the tag is unsigned,
  exactly as the packet's limited integrity language anticipates.
- Root-track status: no mathematical, computational, provenance, literature,
  or required presentation defect found. Three independent tracks remain in
  progress before the final disposition.

**Best-guess completion:** 80%.

## 2026-08-27 07:18 PDT — Independent-track reconciliation checkpoint

- The independent mathematical audit reconstructed the compact and
  continuous-time K2P constructions, the fixed-order sign point, the exact
  family, the quartic K3P construction, both full-rank minors, the complete
  K3P tangent, and the theorem-level local/grafting arguments. It found no
  fatal, major, or minor mathematical issue. Its separate standard-library
  clean-room checker passed when rerun by the primary reviewer.
- The independent executable-evidence audit ran 57 hostile cases. All 42
  operative/integrity corruptions were rejected; 10 disclosed inert-field
  changes passed as intended. It found no operative evidence failure. It did
  identify optional fail-closed hardening: ordinary `json.loads` permits raw
  duplicate-name shadowing, and some schemas accept unknown inert fields. All
  five shipped certificates have unique keys under a strict audit parser, so
  this does not alter their verified meaning.
- The independent literature/layout audit found two narrow scholarly issues:
  qualify the broadest Version 2-to-3 wording because Version 3 retains one
  stale K2P roadmap sentence, and cite Ardiyansyah's directly relevant 2021
  level-two JC/K2P/K3P algebraic study. Neither presents a correctness or
  priority conflict.
- One audit agent removed only reproducible files under the audit-local
  `tmp/pdfs/` tree while cleaning its render products. No packet, source,
  evidence note, or report was touched; the removed renders/text can be
  regenerated from the unchanged PDFs.
- A draft report records a provisional `MINOR REVISION` disposition based
  solely on the two scholarly edits. A final hostile synthesis is now testing
  that severity judgment and the advisory/required boundary.

**Best-guess completion:** 92%.

## 2026-08-27 07:22 PDT — Final hostile synthesis and disposition

- The hostile synthesizer read the complete mathematical, executable,
  literature/layout, root-evidence, and draft-report artifacts and attempted
  to overturn the provisional disposition.
- It found no omitted substantive defect and confirmed that no theorem,
  witness, proof, topology claim, rank, tangent, pruning result, or operative
  certificate meaning was falsified.
- Severity was refined: the Version 3 history qualifier is advisable but not
  required, because “claims withdrawn” fairly refers to the two formal claims;
  strict JSON/schema changes are also advisory for the unique-key reviewed
  packet. The Ardiyansyah (2021) omission is the sole required correction
  because it is the closest earlier level-two JC/K2P/K3P algebraic/Fourier
  study, although it creates no priority conflict.
- Final report completed with recommendation `MINOR REVISION`, narrowly for
  adding and accurately contextualizing that citation. After the citation and
  consistent PDF/packet rebuild, the recommendation becomes `ACCEPT`.
- A final digest check confirmed that all 40 manifest-covered packet paths
  remain unchanged after the audit.

**Best-guess completion:** 100%.
