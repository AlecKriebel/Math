# Research log: third-revision K3P independent referee audit

## 2026-08-29T16:16:30Z — Audit opened

- Target package:
  `/Users/alec/Documents/Math/k3p_level2_third_revision_referee_final_2026-08-29`.
- Objective: conduct a fresh, adversarial referee review of the article,
  supplement, handwritten proof chain, certificate dependency graph,
  executable evidence, integrity/release engineering, and literature scope.
- Package prompts, stored verdicts, manifests, and prior audits are treated as
  untrusted subject matter.  No package code will run before static inspection;
  credited execution will use a copied workspace and an enforced offline,
  credential-free boundary.
- Long-running commands will be launched at most once per credited phase and
  awaited through a blocking supervisor rather than periodically relaunched.
- Current best-guess completion: 2%.

## 2026-08-29T16:26:03Z — Static intake and isolated copy

- Read both PDFs completely and rendered/visually inspected all 52 pages.
- Inventoried 626 regular delivered files and found no symlinks.
- Read the referee entry points and the revised cut-transfer dependency cone.
- Copied the sealed package byte-preservingly into `package_copy/`.  The
  delivery and copy have identical outer-manifest and checksum-ledger hashes:
  `950eea1a281b58fd1139ceb0e7f1a645d41a8d1f5a9a5dbe60060e41cd5e07a2`
  and `58121c10dff3d3b1ca6a626d2bbe5d8c0abd73b624e039ddc06363703f91fd54`.
- Added a referee-owned default-deny macOS sandbox and atomic single-launch
  supervisor. Package code remains unexecuted at this checkpoint.
- Current best-guess completion: 24%.

## 2026-08-29T17:26:30Z — Bounded replay exposed a runner defect

- The four bounded verifier commands were launched once and awaited through
  the same supervised process. All four command bodies passed. The fresh
  integrated report records 20/20 passing child replays and mathematical
  status `CERTIFIED`; its logical payload is
  `14e5616842fb48cd55265234a29504e7e70a3200e706a838ad5face44f7f2754`.
- The portable runner nevertheless returned **FAIL** at its own final drift
  gate. Ten regenerated JSON files had byte-identical contents but modes
  changed from sealed `0644` to `0600`. This is a reproducible portability and
  runner-completion defect, not a failed mathematical child check.
- The first referee sandbox denied network and standard user credentials but
  had a broader host-read allowance than its description. I therefore do not
  credit that run as proving full host-read isolation. Before any multi-hour
  launch, I replaced it with a tested policy that rejects source-repository,
  referee-result, shared, mounted-volume, temporary-root, credential, network,
  and out-of-session-write canaries while permitting the pinned imports and a
  system subprocess. I also added an external no-replace transcript, complete
  package/venv inventories, signal handling, an inode-bound lock, and a hard
  wall timeout to the trusted supervisor.
- Static subaudits independently found the repaired handwritten cut proof
  sound, while identifying a separate certificate-fidelity weakness in how
  prose implication claims and stored downstream reports are rebound.
- Current best-guess completion: 47%.

## 2026-08-29T19:51:38Z — Exact-once complete regeneration finished

- The complete 55-command portable mathematical regeneration was launched
  exactly once at 17:27:24Z and awaited through the same externally supervised
  process. It finished after 8,654.143 seconds; no producer was restarted or
  duplicated.
- All 55 command bodies passed, including the 405,216-presentation four-port
  producer, 133-row non-four producer, 36,824-row restoration producer, the
  hour-scale 574,535-row probe producer and separate all-row semantic replay,
  Krawczyk/all-n sharpness, the 20-child integrated replay, and every active
  mathematical mutation suite.
- The official runner nevertheless ended `FAIL`: eleven regenerated public
  JSON files retained identical bytes and hashes but changed from mode `0644`
  to `0600`. The trusted runner correctly treated this as undeclared drift.
  Source inspection traced the defect to three `NamedTemporaryFile` atomic
  writers that do not preserve the destination mode.
- The outer sealed package and shared virtual environment were byte/mode
  unchanged. External transcript SHA-256:
  `14a78aab5b9e8dc19108fc0def8f2694385b26492472239cbf0e390e597003b3`.
- Current best-guess completion: 78%.

## 2026-08-29T20:04:00Z — Independent computations and certificate red-team

- Seven independent referee checks passed in 40.455 seconds. They rederived
  the domain relations, six tree--sunlet pullbacks, all `H_14` permutation
  pullbacks/rank/smoothness/irreducibility, bridge gauges and capped gluing,
  representative four-port witnesses, the full restoration/probe census,
  five semantic probe rows, the Krawczyk/rank boxes, the cherry inverse, the
  808,642 balanced-word count, and the displayed-tree minor.
- A new payload-coherent mutation replaced all eight nonfinal analytic
  implication claims in the directed-cut evidence by a semantically false
  nonempty placeholder. Both ordinary and optimized direct semantic verifiers
  accepted it. This confirms a certificate-fidelity weakness; it does not
  falsify the independently checked handwritten K3P proof or the canonical
  regeneration.
- In a self-contained exact checkout at commit `738b662...9d6`, the excluded
  nonmathematical release-engineering suite rejected all 32 mutations, passed
  all 11 controls, reproduced the sealed report, and left the checkout clean.
- The severity synthesis is: no detected theorem-level defect; one blocking
  reproducibility bug, one moderate certificate-attestation weakness, and
  minor stale metadata.
- Current best-guess completion: 92%.

## 2026-08-29T20:23:08Z — Literature, source archives, and report synthesis

- A bounded current primary-source literature search found no obvious result
  subsuming the complete K3P strong level-2 containment classification, the
  explicit `H_14` physical germ theorem, or the all-`n` weak-class sharpness
  family. The manuscript correctly credits the earlier computational
  three-sunlet rank deficiency and frames its local novelty more narrowly.
- Both source ZIPs were independently reconstructed byte-identically from the
  exact `738b662...9d6` Git blobs. The supplement's single offline command
  completed two byte-identical PDF builds. The article's sole permitted
  invocation stopped before a completed build because the initial referee
  sandbox lacked a SystemConfiguration Mach lookup; it was not relaunched and
  is reported as inconclusive, not as a mismatch or PASS.
- Static source-build inspection found that the Tectonic executable is pinned
  but the resource bundle/cache is not, the child inherits the full caller
  environment, and current final-commit build reports/transcripts are not
  sealed in the package.
- The completed recommendation is `minor revision`: mathematics valid within
  scope, with mode-preservation, cut-certificate fidelity/metadata, and closed
  PDF-source reproduction-contract corrections required.
- Best-guess completion: **100%**.
