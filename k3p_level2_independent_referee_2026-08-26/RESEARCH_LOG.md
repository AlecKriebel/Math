# Independent referee log: K3P level-2 identifiability

## 2026-08-26 — Intake checkpoint

- Scope: independent referee assessment under the supplied neutral referee prompt.
- Safety boundary: no external communication; all executable review work will occur in `package_copy`, an isolated copy of the supplied package.
- Initial state: source repository is on `main`; unrelated pre-existing changes were observed and will not be touched.
- Evidence status: referee prompt read; package inventoried; article and reader-supplement PDFs copied, text-extracted, and rendered for complete primary-source review.
- Completion estimate: 3%.

## 2026-08-26T16:58:00-07:00 — Primary-source and integrity checkpoint

- Read the 33-page article and 12-page reader supplement completely before relying on generated reports. Rendered and visually inspected all 45 pages; no material layout defect found.
- Restated the principal-domain, strict continuous-time, generic-identifiability, exact-reconstruction, ordinary-triangle, no-proper-containment, outer-obstruction, and weak-class sharpness claims with their quantifiers and exclusions.
- Inspected the top-level integrity checker before execution. The pre-environment integrity run passed: 574 outer payload files (153,326,366 bytes) and 548 proof-core members (152,714,245 bytes), both bound to source commit `983086779dab08f6a0d76d0a10c614b7cee4affe`.
- Created an offline Python 3.14.6 environment by copying the project-local environment into the isolated package. Exact installed versions: mpmath 1.3.0, networkx 3.5, numpy 2.5.2, sympy 1.14.0.
- Completion estimate: 22%.

## 2026-08-26T18:03:00-07:00 — Independent proof/code checkpoint

- Independent handwritten audit found a load-bearing but apparently repairable omitted case: equality of bridge split sets does not distinguish an ordinary trivalent component from a three-boundary cycle/sunlet, while the global proof immediately invokes a theorem restricted to cycle/theta factors. The article's own strict tree--sunlet six-circuit separator appears to supply the missing repair.
- Static code audit found that no active command regenerates or independently classifies the full 405,216 four-port relation universe (or the 27,834 post-topology cases). Active exact checks begin with the frozen 40-survivor/14-orbit lock. This remains load-bearing for exhaustiveness.
- Static code audit also found that the advertised independent probe verifier checks hashes, row structure, and stored metadata but does not reconstruct graph transports/restrictions or the row-specific quartet/tree--sunlet semantics. A coherently self-hashed semantically invalid transport was accepted by its validation function. The hour-scale producer is therefore still load-bearing for the meaning of the 574,535 probe rows.
- Representative independent exact checks support the inverse-Fourier domains, CT inclusion, tree--sunlet pullbacks, H14 pullbacks/rank/smoothness/irreducibility, bridge anchors and gluing bounds, six representative four-port separator/rank cases, Krawczyk inclusion/ranks/margins, and the cherry inverse. These are spot checks, not universe completeness proofs.
- Completion estimate: 55%.

## 2026-08-26T18:08:46-07:00 — Fresh replay checkpoint

- Added an external macOS sandbox profile: host reads and local subprocesses allowed, writes confined to `package_copy`, network denied. Used an empty caller environment with no credential-bearing variables. The broad read rule means this was not complete filesystem-level credential isolation; that limitation was recognized later and is disclosed in the final report. A local `mktemp` shim rewrites BSD `mktemp -t` into the runner's phase-local `TMPDIR`; this was needed because macOS ignores `TMPDIR` for that invocation.
- Preserved two failed harness attempts. Session `20260827T005735Z` reached the clean-room checks and then failed because BSD `mktemp -t` attempted a denied write under `/var/folders`. Session `20260827T005931Z` completed the ten-child integrated replay in 190.80 seconds but the outer runner rejected sandbox-degraded `platform.platform()` metadata. Allowing writes to `/dev/null` restored the canonical platform probe without broadening filesystem or network access.
- Clean session `review_runs/20260827T010421Z` passed all four requested verification commands: release-input bindings, artifact bindings, the ten-child integrated fresh replay, and active classification mutations. Total 193.749 seconds; declared workspace drift was empty. Report SHA-256 `da448cca65c7787d48a7e537ea707d6f032b019434a7c1688ba062833c5b4afa`; transcript SHA-256 `04404b9c5959c2fbb33db33b13d7757686a958125ff48e764418818125b83db2`.
- Started the required 44-command portable producer/verifier regeneration exactly once. No duplicate probe process will be launched.
- Completion estimate: 68%.

## 2026-08-26T18:29:52-07:00 — Semantic probe and draft-report checkpoint

- Reconstructed five probe rows independently of the producer/atlas: one-port isomorphism, triangle, quartet, tree--sunlet, and two-port restriction/inventory. Graph incidence, arrowheads, transports, restrictions, quartet splits, and literal tree--sunlet circuits matched for those samples. This sampling does not establish all 574,535 rows.
- Tested the package's actual `validate_transport` with a coherently self-hashed record whose claimed target edge is not induced by its vertex map and contains an unmapped target vertex. The validator accepted it. This confirms a load-bearing certificate-verification weakness, not a mathematical counterexample.
- Completed the handwritten-proof, code/certificate, independent-computation, and literature audits. Drafted the full referee report with verdict `not fully assessable` at confidence 0.91, pending only the exact once-only regeneration result and final validation.
- The regeneration has passed its first 29 commands, including the full restoration producer/replay/mutations, and is progressing normally through the single hour-scale probe producer.
- Completion estimate: 82%.

## 2026-08-26T19:05:01-07:00 — Adversarial report and isolation checkpoint

- Three independent red teams challenged the main mathematical omission, both major code findings, and the report's compliance/wording. The mathematical gap was confirmed at 0.97 confidence with a valid short contextual separator repair; both code findings survived, with the probe finding narrowed to credit the genuinely semantic producer while identifying the absence of an independent semantic replay.
- Corrected an overstatement about isolation. The formal profile enforced network denial, external-write denial, and an empty environment, but allowed unrestricted host reads; it therefore was not full filesystem-level credential isolation. Static inspection and a live-open-file snapshot found no credential access, but cannot prove none occurred.
- Added a common-credential deny overlay and reran all six referee-authored independent scripts inside `package_copy`. All result files were byte-identical. The overlay is a hardening check, not a proof that every possible credential store has been enumerated.
- Added all-path regular-file/symlink diffs for both failed verification workspaces and the clean verification workspace. Against the untouched delivered proof source, the successful workspace had zero changed files, zero removals, and only the `.venv` symlink plus its generated integrated report added.
- Expanded the report's exact hypotheses, issue metadata, path conventions, dependency map, failure disclosures, literature qualifications, and unresolved-check register.
- The once-only regeneration remained healthy at two-port parent 1,700/2,107.
- Completion estimate: 90%.

## 2026-08-26T19:23:40-07:00 — Once-only regeneration checkpoint

- The required portable regeneration was executed exactly once in session
  `review_runs/20260827T010753Z`; the hour-scale probe producer was launched
  once and allowed to finish. All 44 planned mathematical commands exited
  zero and emitted their expected success sentinels. The summed command time
  was 4,202.194 seconds (70 minutes 2.194 seconds), and the transcript wall
  interval was 4,202.237 seconds.
- The outer regeneration runner nevertheless exited nonzero at its final
  zero-drift gate. The sole changed delivered regular file was
  `restoration/K3P_RESTORATION_THEOREM_REPORT.md`: the producer embedded the
  absolute current workspace in a displayed `cd` command. Its mathematical
  content and all downstream restoration verification/mutations passed. This
  location-dependent report is recorded as REPRO-1 and was not repaired or
  rerun in order to preserve the prompt's exactly-once condition.
- Preserved a synthetic summary for the interrupted outer report containing
  all 44 command records, exit statuses, timings, stdout hashes, and sentinels,
  plus a complete all-path before/after diff. Transcript SHA-256:
  `fbf05586be101315a4e2434c83b3c8ae50c9fd3c487f0c73d16928d98e4403d8`.
- Separately executed the active hardened H21 audit that the manifest credits
  with 25 adversarial mutations but the portable wrapper omits. After one
  disclosed shell setup failure that occurred before Python started, the
  actual audit passed its baseline, three optimized controls, five hash
  checks, all 25 mutations, five rank inequalities, and historical replay.
  Its full workspace diff was empty.
- Final evidentiary conclusion remains `not fully assessable` at confidence
  0.91. The decisive unresolved dependencies are the absent active four-port
  universe reclassification and the semantically shallow independent probe
  replay; the handwritten necessity proof also needs an explicit ordinary
  trivalent-versus-sunlet case, apparently repairable from the existing strict
  tree--sunlet separator.
- Git coordination note: checkpoint commit `cb7559e0` also captured unrelated
  K2P paths that another concurrent workflow had already staged. Those paths
  are user-owned work, so no reset, history rewrite, or other destructive
  cleanup was attempted. The final referee commit will be restricted by path
  to this audit folder.
- Completion estimate: 97%.

## 2026-08-26T19:26:29-07:00 — Final validation checkpoint

- Revalidated every referee-authored independent-check artifact against its
  SHA-256 manifest, parsed all six top-level JSON evidence files, parsed all
  eight referee Python sources, and obtained a clean whitespace/error check
  for the audit tree. The original supplied referee package remains unchanged
  in Git.
- Machine-checked the retained regeneration summary: exactly 44 command
  records, no nonzero command exit, ordered names and sentinels present,
  4,202.194286 seconds summed command time. The full regeneration diff is
  three additions, one location-only report change, and no removal; the
  separately run hardened audit diff is empty.
- A final independent prompt-compliance red team found no internal
  contradiction, execution overclaim, missing required report section, or
  competing verdict. It confirmed the already-disclosed procedural
  noncompliance that the once-only formal regeneration allowed broad host
  reads and therefore cannot be certified as fully credential-inaccessible.
  The run was not repeated because the prompt also requires exactly one full
  regeneration.
- Final report SHA-256 before publication:
  `31e7c67463be1b2b56cab814d2833bde1259c88541357540a513103abab8bb14`.
- Completion estimate: 100%.
