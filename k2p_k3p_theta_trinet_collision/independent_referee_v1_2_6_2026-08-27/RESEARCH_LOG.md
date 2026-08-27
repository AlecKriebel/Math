# Research log

## 2026-08-27 08:43 PDT — Fresh v1.2.6 audit initialized

- Created a dedicated audit workspace for the submitted
  `k2p-k3p-theta-ai-referee-v1.2.6.zip` packet.
- Recorded submitted archive SHA-256:
  `f35d5b8ef06870444b20c6572c9676155aacc9d2df214889706f48c9bb07c150`.
- Inspected all 48 ZIP entries before extraction: one expected top-level
  directory, 44 regular files, four directory entries, no symbolic links,
  absolute paths, or parent traversal components.
- The archive integrity test passed and all 43 manifest-covered paths verified
  after extraction (the manifest itself is intentionally not self-listed).
- Existing unrelated repository changes will remain untouched and unstaged.
- Review policy: read and inspect the main manuscript before consulting packet
  prompts, editing summaries, support notes, or prior referee conclusions;
  treat every embedded instruction and supplied pass/fail label as untrusted
  submission content.

**Best-guess completion:** 5%.

## 2026-08-27 08:49 PDT — Paper-first checkpoint

- Read the complete 20-page main manuscript before consulting support PDFs,
  packet prompts, source code, certificates, editing summaries, or prior
  referee conclusions.
- Rendered and visually inspected all 20 manuscript pages at original detail.
  No clipping, collision, missing glyph, unreadable table, broken equation,
  or figure-label ambiguity was found. The page-14 tangent table is small but
  remains crisp and legible; page 20's bibliography whitespace is harmless.
- The v1.2.6 manuscript now includes the close Ardiyansyah (2021) level-two
  algebraic study and accurately distinguishes its restricted “nice” class
  from the present non-nice three-leaf pointwise collision.
- The abstract and acknowledgment now state the Version 2-to-3 change in terms
  of the formal K2P lemma and corresponding corollary. The main new assurance
  claim is that all five JSON inputs reject duplicate keys/nonstandard numeric
  constants and are checked against closed structural schemas; this remains
  to be tested adversarially.

**Best-guess completion:** 25%.

## 2026-08-27 08:56 PDT — Replay, provenance, and clean-room checkpoint

- Read and rendered both two-page support PDFs after the paper-first pass; all
  four support pages are clean and consistent with the article. All three PDFs
  are untagged, an accessibility advisory rather than a scientific defect.
- Ran `RUN_REFEREE_REPLAY.sh --with-pdf`. An initial run was deliberately
  failed by the closing path-set check after a concurrent audit process created
  `materials/__pycache__/strict_json.cpython-314.pyc` between the opening and
  closing integrity checks. Moved that generated cache to ignored temporary
  storage, disabled bytecode generation in all parallel probes, and reran from
  the manifest-clean working copy.
- The clean rerun passed completely under Python 3.14.6: opening and closing
  manifest checks, normal and optimized complete replays, normal and optimized
  strict-JSON/schema suites, all focused transcript comparisons, individual
  entry points, compact-certificate regeneration, and disposable builds plus
  extracted-text comparison for all three PDFs.
- Recomputed all five closed-schema fingerprints independently; each equals
  the hard-coded value. Static scans found no assertion-dependent correctness,
  unsafe deserialization, stochastic equality test, or hidden numerical
  decision; Python and shell syntax checks passed.
- Verified that the local annotated tag `k2p-k3p-theta-v1.2.6` and the remote
  tag both peel to commit `672d96a08be174cd6b67762a6907dfbdcd926b9b`.
  Every one of the 38 submitted `materials/` files has the same Git blob ID as
  its path in that tagged subtree. The tag has no cryptographic signature, in
  agreement with the packet's limitation statement.
- Fresh executions of two independently authored, certificate-free
  reconstructions reproduced the compact and continuous-time K2P calculations
  and the quartic K3P factorization, direct pruning, exact ranks, and tangent.
  Those scripts use only the manuscript formulas; the v1.2.5-to-v1.2.6 diff
  confirms that none of those mathematical formulas changed.
- Primary-source literature checks confirm that Brits et al. Version 3 is the
  current arXiv version, removes the formal arbitrary-level K2P result, records
  the leaf-order obstruction, and poses the K2P/K3P high-level questions; and
  that Ardiyansyah's Lemma 5.1 excludes two- and three-leaf simple strict
  level-two networks from the paper's “nice” class. The new historical and
  literature wording is accurate.

**Best-guess completion:** 65%.

## 2026-08-27 09:04 PDT — Independent lanes and hostile synthesis checkpoint

- The mathematical lane found no error in the collision identities,
  stochastic-interior checks, edgewise continuous-time conditions, ranks,
  local-dimension arguments, K3P implicit-function tangent, dominance
  argument, or one-blob grafting theorem.
- The code/certificate lane independently rejected 81 operative or integrity
  mutations. Three same-shape mutations of fields expressly classified as
  informational remained accepted, matching the stated coverage boundary.
- The literature/layout lane confirmed the Version 2/3 history, Ardiyansyah
  comparison, literal ten-arc/nine-edge topology, and clean rendering of all
  24 submitted pages.
- A separate hostile synthesis attempted to overturn the convergent result by
  attacking topology, boundary parameters, K3P symmetry, dimension and
  dominance logic, the analytic continuous-time step, arbitrary-taxon
  grafting, common-mode verification, and priority wording. No major, minor,
  or otherwise actionable defect survived.
- A final manifest-clean replay in normal and optimized modes again passed all
  mathematical, schema, focused, supporting-entry-point, regeneration, and
  closing-integrity checks. No bytecode cache or other extra packet path was
  left behind.

**Best-guess completion:** 90%.
