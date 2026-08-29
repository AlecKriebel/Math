# Research Log

## 2026-08-20 18:41 PDT — Program relocation and optimization start

- Established this dedicated top-level research folder on the repository's
  `main` publication line without disturbing unrelated active worktrees.
- Recovered the prior conversation's theorem status: all global proof layers
  are closed conditional on the finite assertion `FA+`; the remaining gate is
  the exhaustive four-port dummy-role/restoration relation sweep with bound
  five-port children.
- Began recovery of the exact conversation attachments.  The referenced
  projectless workspace was empty and the available in-app browser session was
  not authenticated, so the originating conversation was asked to re-surface
  its retained byte-identical archive and SHA-256 inventory.
- Fixed a 60-minute optimization budget beginning when the package is locally
  available.  The optimization may stop earlier once the safe worker count and
  dominant hot path are addressed and equivalence tests pass.
- Hardware constraint: Apple M1 Pro, 10 CPU cores, 16 GB RAM.  The full run
  must leave headroom for concurrent research workloads and must never trade
  exactness or resumability for speed.

## 2026-08-20 18:45 PDT — Resource and provenance audit

- The retained portable package contains 13 files.  Its two K2P-specific exact
  caches are `atlas/descriptors_4.pkl` (80,293,252 bytes) and
  `atlas/rank_certs_4.pkl` (29,859,039 bytes); they do not coincide with any
  local JC cache or Git object.
- The topology provenance is the JC closure grammar on `origin/main`:
  `core_universe.py`, `graph_model.py`, `support_universe.py`, and
  `completion_universe.py`, with the optimized relation architecture in
  `atlas_compiler.py`.  The package counts agree with 831 selected completions
  plus 1,983 marginalized-incoming completions, giving 67,536 raw
  target/port presentations per source.
- Current machine state is not safe for an unguarded production launch: about
  3.1 GiB disk is free, 6.57/7.68 GiB swap is occupied, and a separate exact
  computation has held one CPU core for several days.  That process is not to
  be disturbed.
- Production policy: require at least 20 GiB free before a fresh launch and
  pause safely below 10 GiB; default to two single-threaded long-lived lanes;
  use bounded queues and atomic streamed records; cap aggregate sweep memory
  near 5 GiB.  Four workers are admissible only if a representative pilot
  proves less than roughly 1 GiB peak RSS per worker.
- Planned source balance for two lanes is 1,023 classes versus 908 classes:
  lane A `theta0(1) + theta1(0)` and lane B
  `theta0(0) + theta1(1) + theta3(0) + theta3(1)`.
- Referee determinism requirements include fixed hash seed, single-threaded
  numerical libraries, sorted semantic JSON, timing/RSS excluded from record
  hashes, validated pickle hashes before unpickling, and serial-versus-parallel
  normalized record equivalence.

## 2026-08-20 19:07 PDT — Exact artifacts imported

- The user downloaded the retained chat archives into `~/Downloads`, removing
  the cross-conversation attachment transport blocker.
- Moved five K2P archives into `archives/original/`, including both names of
  the byte-identical first checkpoint archive, the second continuation, the
  non-pickle transport subset, and the complete four-port package.
- Extracted the two checkpoints and complete four-port package under
  `package/original/`.  The original files remain untouched; optimization will
  occur only in a separate `package/referee/` copy.
- The complete four-port ZIP matches the preserved archive SHA-256
  `53d8f6771589197b16690ff0fb790cc2aa845fa91e86424e589476ffe352c875`.
- The 60-minute optimization clock starts after the artifact-import commit is
  published to `main`.

## 2026-08-20 19:48 PDT — Bounded optimization and qualification complete

- Stopped optimization inside the fixed 60-minute budget.  All changes are in
  `package/referee/k2p_offline_sweep_portable`; the original package remains
  byte-for-byte preserved.
- Measured pickle/compiler startup at about 4 seconds and 1.39–1.50 GB peak
  RSS per independent process.  Six workers are unsafe on this 16 GB machine.
  The referee runner supports one worker by default and at most two staggered,
  balanced long-lived lanes.  Current local launch policy is one worker.
- Reused validated pickle hashes rather than rereading 110 MB, compacted the
  separately unpickled rank-descriptor graph, retained fixed-source quadratic
  products lazily across classes, discarded target-local products, prepared
  fixed-source exact mixed graphs, and cleared source caches between sources.
- Replaced six sequential universe loads with one multi-source load per lane.
  Changed growing-manifest checkpoints from every class to every 25 classes;
  the estimated logical manifest writes fall from about 2.20 GB to 95 MB.
- Repaired two frozen-package fail-closed defects found during qualification:
  resume previously accepted a removed hard certificate after a recomputed
  outer checksum, and the merge previously returned success for fabricated
  incomplete manifests.  Record semantics, class/source identities, current
  package bindings, exact ID coverage, and merge completion are now checked.
- Added deterministic semantic record, source-manifest, and complete-sweep
  hashes that exclude only operational timing/platform diagnostics.
- Found and repaired an exact-kernel zero-column defect that could miss a
  separator, plus a rational-coefficient conversion defect in the SymPy
  differential oracle.  The seeded width-1-through-16 differential suite now
  passes.
- Narrowed graph-conversion error handling so unexpected implementation or
  dependency faults abort instead of becoming mathematical nonrelations.
- The prepared exact graph path matched the frozen path on all 4,012 eligible
  presentations.  Frozen-versus-optimized output matched on eight declared
  benchmark records (four direct hard cases and four ordinary source-5
  classes), semantic aggregate SHA-256
  `74663db39da3e87bd3042ed16e1da7bf1cc72adcd5cc5414fb09ef3cf3913d59`.
- Full hash, dependency, census, rank, hard-binding, graph-path, resume, exact
  kernel, and adversarial mutation qualification passed in 45.61 seconds at
  1,507,999,744 bytes maximum RSS.
- Built and integrity-tested the 5,397,019-byte referee archive
  `archives/k2p_four_port_referee_optimized_20260820.zip`, SHA-256
  `dcdfe50f36d231a2940a53f2ec196dba52c5850078f2e92ee24ec3ca2747dc82`.

## 2026-08-20 19:49 PDT — Production launch safely gated

- The guarded full-run invocation was issued with one low-priority worker.
  Preflight correctly refused to start: 2.61 GiB disk was free versus the
  20.00 GiB safety requirement.  No production relation process was launched.
- The guard will stop below 10 GiB free disk or above 3.5 GiB aggregate sweep
  RSS, propagates termination/hangup to the detached process group, forces all
  numerical-library thread counts to one, and preserves every atomic class for
  resume.
- Independent audit identified theorem-level gates not solved by runner
  optimization: an explicit topology/rank exclusion ledger and dimension
  upper-bound certification, bound five-port restoration children, explicit
  graph witnesses/exact certificate replay in the released package, and a
  careful restriction of the hard-case conclusion to its proven `D_plus`
  domain.  These are recorded as closure requirements; the optimized sweep
  must not itself be described as a completed final theorem.

## 2026-08-20 20:36 PDT — Manifest schema repair and completed lane recovery

- After disk cleanup, recovered and resumed the guarded four-port production
  records. All six source lanes now have complete contiguous manifests with
  source class counts `536, 747, 276, 276, 64, 32`; the resumable driver
  reused every retained record on the final replay.
- The first final merge exposed a package defect rather than a mathematical
  failure: immutable record metadata overwrote the residual manifest's own
  schema tag. The driver now preserves the v2 manifest schema separately from
  `record_schema`, and the package smoke test checks both fields.
- Updated the fail-closed input lock for the repaired driver and verifier.
  Exact sparse-kernel differential tests, portable-driver mutation tests, the
  complete package gate, and the 4,012-presentation prepared-relation audit
  all pass under Python 3.14.6.
- A fresh post-lock six-source sweep processed all 1,931 canonical classes with
  zero errors and produced six complete v2 residual manifests. Its qualified
  merge correctly remains non-final because 36 classes retain the explicit
  `unresolved` status; the exploratory merge nevertheless passes all schema,
  hash, binding, and exact-coverage checks.
- This closes the production-run and manifest-engineering milestone but not
  the theorem-level obligations listed above. Best-guess completion is
  **100%** for the exact six-lane production milestone and **80%** for the
  overall K2P closure program.

## 2026-08-20 21:05 PDT — Proof-first analysis of the 36 direct residuals

- Cancelled the no-longer-relevant hourly sweep monitor after confirming that
  the 94-second process had finished normally. The speed was explained by the
  110 MB precompiled descriptor/rank inputs: the run classified 1,931 retained
  classes and did not regenerate the topology universe or close restoration.
- Reduced the 36 direct rows to three symmetry families rather than launching
  a broad higher-degree atlas. Exact graph-derived parameterizations were used
  as the proof objects; modular/kernel searches served only as finders.
- Found a 14-term cubic separating source-5 classes 9 and 10. Independent
  characteristic-zero substitution gives zero target pullbacks, a shared
  96-term nonzero source pullback, and a strict positive-domain witness.
- Found one 32-term quintic whose port orbit separates all 22 non-symmetric
  `theta0` repair-1 relabelings. Exact replay over all 24 permutations leaves
  zeros only at the identity and the sole semi-directed graph symmetry.
- Found three sparse quartics whose symmetry transports cover all 12 remaining
  `theta1/theta3` and `theta3/theta3` rows. Direct displayed-tree expansion,
  bridge multihomogeneity, strict witnesses, and 145 coefficient/index
  mutations all passed.

## 2026-08-20 21:36 PDT — Unified direct-candidate proof closure

- Built one deterministic verifier binding the exact 36 production records to
  the 22 quintic, 12 quartic, and 2 cubic proofs. It reconstructs paired-sector
  Fourier maps directly from graph switches and loads neither atlas pickle nor
  separator search code.
- The first adversarial review independently rescanned all 1,931 records and
  replayed every obstruction. It found no mathematical counterexample, but it
  exposed two qualification defects: Python `-O` disabled assertions, and the
  first unified script trusted non-candidate census fields.
- Refactored the verifier to reject optimized mode and to recompute all six
  semantic manifest hashes, the 1,931-row status census, the merged payload,
  and the complete semantic sweep root before any proof PASS is possible.

## 2026-08-20 22:07 PDT — Current-lock release run and fail-closed cubic repair

- Integrated the exhaustive degree-3 pass into the optimized driver. A fresh
  run moves source-5 classes 9 and 10 from `unresolved` to exact cubic
  `separated`, leaving 34 higher-degree proof-overlay rows.
- An adversarial resume mutation showed that cubic records were initially
  shape-checked but not bound to the exact fixed certificate. Added an exact
  case/payload binding and a mutation test that changes a coefficient,
  recomputes every outer hash, and must still be rejected.
- Generated the final current-lock run with one low-priority process in
  361.42 seconds. All 1,931 records merged with counts
  `845/20/35/997/34/0` (separated/isomorphic/triangle/restoration/unresolved/
  error), peak recorded RSS 1,502,134,272 bytes, and semantic sweep root
  `2a9a19ba3e9498df1c77582b07fcfd5ac315a4437ee634d25ce8ec4aa5cbaab0`.
- Froze the six complete manifests plus the 36 proof-relevant raw records in
  the referee package. Separate engine and direct-closure locks avoid a hash
  cycle while keeping the run reproducible and fail-closed.

## 2026-08-20 22:19 PDT — Referee release frozen and replayed from archive

- Added a separate 60-file direct-closure lock binding 9,455,330 bytes of
  proof, result, and release-harness inputs. Its SHA-256 is
  `89ebf377aa30fd27cd6480382fedcdd895519905f5accb51537a584b5dd8bc92`;
  the underlying immutable engine lock remains unchanged.
- The outer harness independently reconstructs all 1,931 manifest summaries,
  the six semantic manifest roots, and the complete sweep root before replaying
  the 36 obstructions. It rejects Python optimized mode and contains no
  assertion-dependent qualification checks.
- A freshly re-locked mutation suite rejected changes to the merged root,
  manifest status and unresolved lists, missing or swapped records, port and
  semantic hashes, and one coefficient in each of the quintic, quartic, and
  cubic proof families.
- Built the 7,117,602-byte referee archive
  `archives/k2p_four_port_direct_closure_referee_20260820.zip`, SHA-256
  `73b60f9815d428e5220ab6f7d0b3391073559fc6eb982b84b6747599047b69c0`.
  ZIP integrity passed.
- Extracted that archive at a different absolute path and ran the full
  one-command qualification. It passed in 106.12 seconds with a maximum RSS of
  1,508,294,656 bytes, reproduced the golden proof certificate byte for byte,
  and returned `remaining_unproved_among_36=0`.
- Completion estimate: **100%** for the fixed 36-candidate direct-residual
  milestone and a conservative **82%** for the overall final-theorem program.
  The latter remains deliberately low because restoration, raw-universe
  certification, mixed-sign scope, and global theorem assembly are still
  load-bearing.
- Two final read-only reviewers independently accepted the current archive.
  One reconstructed the exact 76-file lock partition and ran the full
  fresh-path gate in 105.69 seconds; the other replayed under Python 3.11 and
  3.14 with pinned dependencies and a randomized hash seed. Both recovered
  the same 1,931-class root and 36-case proof census, and neither found a
  mathematical, portability, or packaging blocker for the scoped release.

## 2026-08-21 18:12 PDT — Principal-domain K2P theorem closure promoted

- Promoted the principal-domain classification to unconditional `K2P-SAME`:
  for binary standard semi-directed strongly tree-child level-2 networks on
  \(\mathcal D_+\), directed containment, equality up to ordinary-triangle
  moves, and generic model intersection coincide. No mixed-sign extension is
  claimed.
- Independently regenerated the complete four-port and theta2 primitive raw
  universes, proved exact rank upper bounds for every retained descriptor, and
  replaced the invalid rooted tree/sunlet oracle with full-map Fourier
  certificates. The corrected four-port ledger has 405,216 raw rows and the
  corrected theta2 ledger has 2,946,240 raw rows, with zero unclassified rows.
- Closed all 997 four-port restoration parents: 2,540 physical roots generate
  36,568 first-level and 256 second-level edges, with 36,792 terminal leaves,
  zero missing children, zero cycles, and zero unresolved leaves.
- Closed the all-primitive coherence layer from 176 physical equality anchors.
  The one-port ledger has 29,964 rows and 2,107 equality survivors; the
  two-port ledger has 544,571 rows and 32,729 equality terminals. Every
  transport, restriction, reverse marginal, and global triangle choice was
  independently replayed, with zero unresolved or incoherent records.
- Assembled the main classification theorem, generic-identifiability and exact
  reconstruction corollaries, strict continuous-time corollary, and the weak
  tree-child \(4n-3\)-dimensional sharpness theorem. The final manuscript SHA-256
  is `6cd540649c146b5ff5932c432dcaac07745d57de77b18031ae1ebf8b9c704670`.
- Froze the fail-closed referee release in
  `work/final_theorem_release/RELEASE_LOCK.json`, SHA-256
  `0c17eeaa3344f0982998ea694c1eb92f72f5ced0841e2acad0d39566e2ec71c3`,
  with `promotion_ready=true`, no blockers, and 194 outer locked files. A bare
  clean copy passed all 19 quick qualification layers and all 23 outer
  mutations; optimized mode, missing dependencies, and every tested ledger,
  rank, child, transport, and separator corruption failed closed.
- The recursively locked evidence bundle contains 369 unique files; including
  the release lock it is 434,661,763 bytes with canonical content-ledger root
  `c79fa2d3cb6431207823e3c66c3440cbeb94226d8a9925960883efca7dca2416`.
  The deterministic 14-page theorem PDF has SHA-256
  `a176f8c67a8a0b3dcf0d22acf9268cfea020367ab6ef296f9c964b6c67a38ca5`.

## 2026-08-22 11:01 PDT — final clean-replay dependency repair (98%)

- The first detached-checkout exhaustive replay passed all mathematical gates
  reached in 620.14 seconds, then exposed a clean-room staging omission before
  the exact-rank calculation: `k2p_atlas_core.py` had not been copied into the
  temporary rank verifier tree.
- The rank stage now hash-checks and copies that exact locked module, rejects a
  deliberate omission with the expected import error, and runs a positive
  import-closure preflight with ambient `PYTHONPATH` disabled.
- The rebuilt release remains promotion-ready with no mathematical blockers.
  Best-guess completion is 98% pending the repaired full replay, final PDF QA,
  and deterministic referee archive.

## 2026-08-22 14:55 PDT — targeted referee revision and clean release complete

- Scrutinized the fresh adversarial report item by item. The mathematical
  recommendations were valid and were applied without weakening the promoted
  `K2P-SAME` theorem. The revision corrects the Huber/Englander/current-work
  provenance split, replaces the triangle inverse-function wording by exact
  submersion and constant-rank arguments, formalizes the complete paired K2P
  restriction descriptor, and clarifies the repair-tagged completion census.
- Exposed the already-derived proof compression rather than beginning a second
  research cycle: the supplement now prints 23 quadratic templates, five
  higher-degree bases, their coordinate dictionaries and allowed transports,
  and three worked examples. It also names every weak-sharpness Jacobian
  column and adds the generic complex/physical rank justification. Independent
  template and sharpness replays, with 18 and 15 adversarial mutations
  respectively, pass.
- A detached clean checkout regenerated and replayed all 35 release layers in
  5,172.89 seconds (86.2 minutes), with maximum RSS 1,960,001,536 bytes and
  measured peak memory footprint 491,504,408 bytes. The report SHA-256 is
  `7939b389880de80b7d8abd69022e0b69d2dc4188815854b294d3384fa24c9e18`;
  its telemetry SHA-256 is
  `8779854633d9a52ba3d7bc9278ccbcc3918e51987bb4c30204c0adcd9771ce16`.
  All layers pass, `promotion_ready=true`, and the blocker list is empty.
- Rebuilt and visually inspected all 48 final PDF pages. The 24-page article
  has SHA-256
  `e30ea98ccde1756bb98ad9ce500c83a64c87d5d9985bc06b432f6d9fc79df064`;
  the 24-page supplement has SHA-256
  `0a0c55e16b5f7298c9749912a3901d1a0a1323578ab25ef7db13c06e0b912131`.
  Both have embedded fonts and no undefined references, citation failures,
  overfull boxes, or visual clipping.
- Built the deterministic 448-member referee archive twice independently;
  both builds are byte-identical. The 178,002,570-byte archive
  `proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260822.zip`
  passes ZIP integrity and has SHA-256
  `0e73c6fdd66daf59ede5c919c589e1e6c2f5dfff7e1fdf15b99ffc78f1bb6013`.
  Its manifest binds 374 frozen files and 73 submission files with combined
  content root
  `49f1a24c18f04aee9185aca150ce733acc00943b6c76430a2f363d341defd64d`.
- The final compact qualification battery passes exact old/new equivalence,
  proof compression, independent bundle checking, and all associated mutation
  suites. No mathematical or reproducibility issue remains. PC-PARTIAL is the
  final proof-compression status and a deliberate stopping point.
- A final read-only adversary independently checked the repaired 374+73-file
  crosswalk and the 448-member archive, then cleared the interim submission
  hold. Its final verdict found no mathematical, computational, packaging, or
  PDF blocker.
- Best-guess completion is **100%** for the principal-domain theorem and its
  reproducibility package. Journal-submission administration is **96%**:
  corresponding email, contribution approval, funding/conflict statements,
  license choices, and the eventual public tag/DOI remain human decisions and
  were not invented by the research workflow.

## 2026-08-22 16:17 PDT — second conditional-pass review closed

- Scrutinized the later adversarial review independently. Its two remaining
  proof-completeness findings were valid: the article asserted, but did not
  display, the exhaustive directed theta event-placement case split, and the
  genericity argument used finiteness of the topology list without printing a
  reticulation bound. Both are now proved self-containedly.
- The four theta orientations were independently regenerated across every pole
  role: tree/tree gives two classes, one-reticulate-pole gives two more up to
  pole exchange, and two-reticulate poles give no valid acyclic orientation.
  The repair obstruction clauses and minimal transversals match the primitive
  core certificate exactly.
- Added (r\leq|\mathcal X|-1) and
  (|V|\leq4|\mathcal X|-3), made the compression table a fail-closed source
  dependency, stated zero-based sharpness rows, and corrected reconstruction
  to use global exact semialgebraic membership rather than treating generic
  rank certificates as pointwise separators. The exact-input convention is
  now explicit.
- All compact mathematical gates pass: seven-command old/new equivalence,
  11 compression mutations, 18 printed-appendix mutations, 15 named-column
  mutations, and 12 package mutations. Three independent read-only audits
  found no mathematical blocker after correction.
- Rebuilt the 26-page article (SHA-256
  `204537cef40f155d1fd418c4b17cd7b8cd5e432773b0de037a829690f8ba77e1`)
  and retained the clean 24-page supplement (SHA-256
  `19865ffb832abf5757d5fb5d534e1888d22f3b11ea7ea035e451203359ca275a`).
  All 50 pages passed visual inspection, all fonts are embedded, and both logs
  are clean.
- The final deterministic 448-member referee archive was built twice
  byte-identically, passes ZIP integrity, and is 178,014,299 bytes with
  SHA-256
  `e641cab404b72fc935f7efd48fbf96bd14981c7405d6ce9efacebba42bcc4e15`.
  Its manifest binds 374 frozen files plus 73 submission files with payload
  `dccb7894e5627912b62139b62b7e736d4c35cbc3c932f49d8f79672fe282fd78`.
- Principal-domain theorem and reproducibility-package completion remain
  **100%**. Journal-submission administration remains **96%**, pending the
  human metadata, licenses, immutable tag, DOI choice, and then one final
  immutable-commit full replay for provenance.

## 2026-08-22 23:15 PDT — third mathematical-pass review reconciled

- Scrutinized the latest adversarial review with three independent read-only
  audits. No theorem defect or reason to reopen the atlas or proof-compression
  search was found.
- Corrected one genuinely stale runtime paragraph: the frozen
  computational-evidence lock contains no end-to-end timing record, while the
  crosswalk's global C11 entry and the submission bundle byte-bind the detached
  35-layer replay and its 5,172.89-second wall time. Entries C01--C10 and
  C12--C13 retain null end-to-end runtimes; no quick-suite runtime is inferred.
- Strengthened genericity using the total locus
  `rank D Phi_N < d_N`. Finite Nash strata have restricted rank at most
  `d_N-1`, so the image of total rank drop has smaller semialgebraic dimension
  before the proof invokes a regular source-image germ. This avoids the invalid
  interpretation based on vanishing of only one maximal minor.
- Proved source completeness operationally: exactly five TeX/Bib files compile
  the 26-page article and 24-page supplement in a clean preserved directory
  tree. No custom class/style, external figure, image, font, or shell-escape
  asset is required. Package mutations now reject omitted bibliography and
  certificate appendix as well as the compression table.
- All compact gates pass: seven-command old/new equivalence, 11 compression
  mutations, 18 printed-appendix mutations, 15 named-column mutations, and 14
  package/source mutations. All 50 PDF pages were rendered and visually
  inspected; logs and embedded-font checks pass.
- Rebuilt the deterministic 448-member referee archive twice byte-identically.
  It is 178,019,313 bytes, passes ZIP integrity, and has SHA-256
  `ab7c3cef83d1bd7bb8c330b25ace118ae7ee583a39f7f55c7363b37e3ab4fe3d`.
  Its manifest payload is
  `1e1b545bc62bb822c560a467026374e69546e603aabb49e0491d6e2a56b6ec7c`.
- Did not infer the suggested email, contribution approval, funding,
  competing-interests, license, tag, release, or DOI fields. Mathematical and
  reproducibility completion remains **100%**; journal administration remains
  **96%** pending those human decisions and any selected final-tag replay
  provenance claim.
## 2026-08-24 — Neutral-referee repair and source-candidate checkpoint

- Corrected the printed quartet invariant and replaced the former semantic
  spot check by an exact Klein-four evaluator covering every promoted quartet
  terminal.  The terminal gate binds 4,414,710 row references and 888
  certificate identifiers; all targeted semantic and binding mutations fail.
- Hardened the ordinary-triangle canonicalizer, exhaustively compared it with
  an independent labelled-graph implementation, and certified graph-derived
  inheritance and restriction transports.  The four-port classification and
  all raw ledgers retain their exact prior censuses.
- Regenerated the 2,946,240-row theta2 composite and 405,216-row raw-four
  composite after provenance rebinding.  Both large ledgers are byte-identical
  to their frozen mathematical predecessors.  The unified five-family
  certificate and all 22 mutations pass with zero unresolved records.
- Replayed all 4,379 exact symbolic rank-upper certificates against the
  primitive raw ledger.  The rank partition is unchanged and the sampled-rank
  substitution mutation is now explicitly rejected.
- Qualified the final 223-file release lock: the 23-layer quick suite and all
  27 release mutations pass with zero blockers and
  `promotion_ready=true`.  Rebound the PC-PARTIAL reader package, printed
  formula appendix, restoration/probe summaries, and weak-sharpness column
  dictionary to that lock.
- Finalized author metadata and licenses.  Per the author, no GitHub Release,
  Zenodo deposit, or DOI will be created by this workflow; only the source tag
  is planned after final qualification.
- Best-guess completion toward a fully submission-ready, immutable referee
  package: **93%**.  Remaining gates are source-candidate commit integration,
  detached clean full replay with telemetry, deterministic PDF build and
  visual inspection, final crosswalk/bundle regeneration, push, and source
  tag.

## 2026-08-24 — Theta2 provenance diagnosis and fail-closed replay repair

- The first detached full replay stopped at the historical five-port theta2
  byte comparison.  Structural regeneration had already reproduced all
  2,946,240 directions, 480 classes, 864 restoration children, and zero
  unresolved records; the first differing gzip was then shown exactly to be
  the frozen rank payload with only its compiler provenance hash rebound to
  the hardened atlas.
- An independent full theta2 regeneration completed in 486.6 seconds.  The
  direct proofs, class partition, and entire raw ledger were byte-identical.
  All 120 rank certificates and all restoration mathematics were identical;
  the only differences were the compiler/canonicalizer/input-lock provenance
  fields and their mechanically dependent summary metadata and seal.
- The theta2 full verifier now requires both the exact legacy bindings and the
  exact current compiler, canonicalizer, and input lock.  It reconstructs only
  the enumerated provenance delta and compares every regenerated output byte
  against that result.  The expanded local suite rejects 18/18 mutations.
- Rebuilt the 223-file outer lock and rebound the PC-PARTIAL reader package.
  The 23-layer quick replay and all 27 outer release mutations pass with zero
  blockers and no theorem, rank, formula, census, transport, or classification
  change.
- Best-guess completion toward the final submission/referee package: **96%**.
  Remaining work is the clean detached full replay at the new exact candidate,
  telemetry, PDF/build audit, deterministic bundle, final push, and Git source
  tag.  No GitHub Release or Zenodo action is authorized.

## 2026-08-25 — Final clean replay and submission qualification

- Completed the detached clean-checkout full primitive replay at source
  candidate `1877985d20132fb186d21a5985e8c5f760a656af`. All 40 layers passed,
  with zero blockers and `promotion_ready=true`. Internal time was
  5,577.570125 seconds; wall time was 5,578.10 seconds; maximum resident set
  size was 2,600,484,864 bytes; and the recorded peak memory footprint was
  503,350,016 bytes. The replay report SHA-256 is
  `ec5fefc3c1ab2210e9c53792240ebe008603da6abd004d093e2b95e15ff5c10b`
  and the independently constructed telemetry SHA-256 is
  `415bf36a59e6006603e4382085c784ffc4e1a1744f1e4c920cd5f0d313fb9df5`.
- Rebuilt the article and reader supplement deterministically. The 26-page
  article has SHA-256
  `2c4433d53c33c337d4ed028c2843cf0b5631263d7bf4a0a42106727985daa3a8`;
  the 24-page supplement has SHA-256
  `9b10797d7503e6940d80a95bc90302b3b32a9ea34cb9f63a54bee3f12f3c06e1`.
  All 50 pages were rendered and visually inspected, all fonts are embedded,
  and the fail-closed build report passes with no undefined references,
  citations, overfull boxes, fatal errors, or clipping.
- The final quick replay passed all 23 layers in 383.261 seconds. All 27 outer
  release mutations were rejected with zero survivors. PC-PARTIAL verification,
  seven-command old/new equivalence, 11 compression mutations, nine telemetry
  tests, the static source audit, and all 27 bundle mutations pass.
- Sealed the portable frozen evidence closure at 399 files and 478,755,815
  bytes with content root
  `072baaa4066569acd31c552149f6afb727323e54b241bdefc98452598309dd61`.
  The revised referee manifest binds those files plus 80 source/reader and
  execution-dependency files, including both PDFs, a neutral archive-native
  referee prompt, and every checker named by that prompt. Its combined
  content root is
  `9cbf9264172b55ebe6fbc3a513e62a43c08de040f78c9c82d128c19c8190a86c`.
- Built the 480-member deterministic referee ZIP twice independently; the two
  archives are byte-identical and ZIP integrity passes. A fresh extraction
  passes every compact prompt command without changing any packaged file. The
  214,790,278-byte
  archive has SHA-256
  `8a86436f7ff1cdaafb18a163469569f6cf8f697db866423d30969bcca35e7535`.
- The qualified immutable source-tag name is
  `k2p-same-biorxiv-v1.0.0`. No GitHub Release, Zenodo deposit, or DOI has been
  created or claimed; those actions remain with the author.
- Best-guess completion is **100%** for the principal-domain theorem,
  reproducibility package, bioRxiv sources, and neutral referee package. No
  mathematical, computational, metadata, source-build, or packaging gate
  remains.

## 2026-08-25 — C02 authority correction after fresh referee review

- Confirmed the referee's C02 finding.  The former
  `topology_direction_certificate.json` treated the revoked depth-one
  restoration split (35,758 quartet plus 646 rooted tree/sunlet rows) as
  current authority, although the corrected forest replaces those 646 rows
  by 606 whole-map `T_i` leaves, eight quartics, and 32 continuations whose
  256 second children are 248 quartets and eight whole-map `T_i` leaves.
- Replaced that certificate and producer in place with a deliberately narrow
  raw displayed-quartet audit.  It independently reconstructs all 405,216 raw
  directions, recovers exactly 360,408 quartet exclusions, binds the current
  corrected raw4 summary, and explicitly disclaims rooted tree/sunlet,
  restoration, and whole-map `T_i` authority.  The regenerated certificate is
  byte-reproducible and rejects optimized Python.
- Rebound the analytic adversarial audit to the corrected 36,824-edge,
  36,792-leaf restoration-v3 forest and to the narrow raw-quartet certificate.
  Its focused replay passes with no blocker, and all 12 analytic mutations
  remain rejected.
- Narrowed machine crosswalk claim C02 accordingly.  Added unmistakable
  historical banners to the former probe-input and global-proof checkpoints,
  and mapped every absent legacy referee entry-point name to the current
  supported command or authority in the referee/release README chain.
- Global locks, generated crosswalks/manifests, PDFs, and the referee archive
  were intentionally not regenerated in this checkpoint.  After all fresh
  referee fixes are integrated, the exact required order is: regenerate the
  quartet semantics certificate and its relocation/mutation evidence (the
  historical `GLOBAL_PROOF.md` byte changed); regenerate the quartet terminal
  binding and mutation report; rebuild/check `RELEASE_LOCK.json`; run quick
  replay and release mutations; run one detached full replay; rebuild/check
  the theorem-artifact crosswalk; rebuild/check the revised bundle manifest
  and bundle-mutation report; regenerate the portable file ledger and
  deterministic referee ZIP; then publish a new source tag.  Article and
  supplement PDFs need rebuilding only if a submission-source byte changes.
- Best-guess completion: **100% for the C02 authority repair itself**; final
  package qualification remains pending the other referee fixes and the
  ordered global reseal above.

## 2026-08-25 — Relocatable mutation evidence and provenance hardening

- Adversarial output-collision testing found that a caller-supplied quartet
  mutation report could still overwrite its specification or another locked
  source. Repaired the quartet semantics and terminal-binding mutation writers
  to require external caller-owned output, with an explicit override licensing
  only the exact nonsymbolic canonical certificate.
- Removed traceback hashes and runtime/path fields from the quartet and outer
  mutation reports. The outer report is now schema v2 and retains only stable
  semantic rejection markers, return codes, fixed bindings, and a payload
  seal.
- All four actively rerun small mutation producers (quartet semantics,
  quartet terminal binding, canonicalizer completeness, and parameter
  transport) now publish through an fsynced same-directory temporary file and
  atomic replacement. Direct source collisions and source-resolving symlinks
  reject; external hardlinks and deterministic late symlink swaps cannot
  truncate source inodes.
- Added bound, mandatory output-contract preflights. The quartet relocation
  test passes across differently named extractions with report SHA-256
  `a1bf423637775b295fb1d6554401352834c59eab326798f7db4753a3855a4a9e`.
  The outer focused report has SHA-256
  `a1f01d2ad623d09ca393e0b4e7bfc6b7c80600d4d4d973b948b00e6d7e695cff`.
  The canonicalizer external report remains byte-identical at
  `10b8eebaa739f3853434527bd6b55d90cdb28028345cb6285d687a8c3961dfdc`.
- Semantically pinned C02 to raw displayed-quartet direction and tree-of-blobs
  recovery only. Added crosswalk mutations against the former overbroad claim
  and erased exclusion boundary. Added explicit historical or revoked banners
  to the misleading pre-closure topology, probe, and restoration narratives
  found in the audit, and updated the historical registry hashes and seal.
- The focused fixes are complete. The parameter-transport certificate and
  dependent mutation report now require ordinary deterministic regeneration
  because they bind the changed runner/producer bytes; all outer locks,
  crosswalks, PDFs, replay telemetry, and archives remain intentionally stale
  pending the ordered final reseal.
- Best-guess completion: **100% for referee Findings 1, 3, 4, and 5 and their
  adjacent output-safety surface; approximately 85% for the full release
  qualification**, with deterministic regeneration and long clean replays
  still outstanding.

## 2026-08-25 — Final referee-defect closure and submission qualification

- Replaced the former raw4 and theta2 composite pseudo-mutation summaries by
  22 genuine complete-ledger, production-verifier-facing attacks. Together
  with optimized-mode and source-immutability guards, the two component suites
  pass 14/14 and 12/12. The then-current outer report contained 27 conceptual
  gates, all rejected, with zero survivors and payload
  `b7e1776e44ff5b50f92ed58f8b62d3c15ea49a358819bd8bc9dfac76ebd9df37`.
  The 26 August round-2 qualification initially added a separate rank
  production-mutant gate.  Its later evidence-role audit removed three
  revoked or historical rows from promotion accounting, so the current
  required outer census is 25 stronger, active gates.
- Made every nested mutation writer caller-owned, atomic, path-independent,
  and fail-closed against direct collisions, symlink resolution, hardlink
  truncation, and late symlink swaps. A clean-extraction regression exposed
  one overstrict assertion that required a canonical reseal to change already
  current bytes; the corrected idempotence rule permits no change exactly when
  the canonical report is already byte-current and otherwise permits only the
  canonical certificate to change. Independent adversarial review passed.
- Corrected C02 so its current authority is exactly the 405,216 raw
  four-port directions and 360,408 displayed-quartet exclusions. Restoration,
  whole-map `T_i`, and rooted tree/sunlet claims are explicitly excluded and
  remain assigned to their current certificates.
- Resealed the 227-file promotion-ready outer lock at SHA-256
  `c319977f350923ab900a883235e32ec945d55a864338c14a08ce266ed3a1c78a`
  and payload
  `dcc15b8ae2bb46674344595809690657119e5271611bab8c3c47fccade0fa509`.
  The recursive closure contains 403 files and 478,865,262 bytes with root
  `de6c2f7162164bb460bc608bffefb96b0494965c734c1063f304530a0cc36b82`.
  A semantic delta audit found only the intended relocation-test binding
  change; every classification census remained unchanged.
- Ran the complete outer mutation program in two differently named clean
  archive extractions. Both passed, produced byte-identical report SHA-256
  `c60fdc2e5f70c702abbbc426f8e9595a1f64464b80a6bdccac13614ee5b2a28a`,
  and left all 646 extracted project files unchanged.
- Ran the final full primitive replay from a detached clean checkout of
  candidate `83821850e02bc6b6a0383dbc9d3d42ab24a261f5`. All 40/40 layers passed
  with zero blockers in 5,428.031056 seconds internal and 5,428.67 seconds
  wall time; maximum RSS was 2,548,498,432 bytes. The report SHA-256 is
  `d26ce0841a50ebdc50a5e5d75a25ac2e12d9b647759051c8ceea29d803bd799e`
  and the exact source/lock/time telemetry SHA-256 is
  `dc4bd8faafef195a1fd7879b2c8ac7197ebb56cf8fee46c799ab0415b1e3ec08`.
- Rebuilt and visually inspected the 26-page article and 24-page supplement;
  the PDF build payload is
  `556ba6792d8dd1e27a3e35d52e306d74d835c1f8d35a49f698039127964dc94d`.
  The static audit, 13-claim crosswalk, 31 crosswalk/bundle mutations, and
  revised manifest pass. The manifest binds 403 frozen files plus 80
  submission/execution files with payload
  `1a4b0999d6c7c2cc6f4ff9cb322ab3189f90aa9b4cdf020464d666aa78148c81`
  and combined root
  `ab13d87f2b784d1c12f4fa2a398e33aeb8ba4d2eb8d6c5071611c71c90b2a5ff`.
- A final fail-closed audit caught one historical adversarial-review addendum
  that still presented superseded lock and replay values as active. Corrected
  that provenance-only record to the current lock, recursive closure, replay,
  runtime, memory, and telemetry values; the mathematical sources, executable
  evidence, frozen censuses, PDFs, and full replay were unchanged. Resealed the
  manifest and archive after the correction.
- The final exact-archive quick and mutation run passed all 23 quick layers,
  seven old/new comparisons, 11 compression mutations, nine telemetry tests,
  and 27/27 outer mutations with zero survivors. Its strict inventory guard
  then detected two newly generated `__pycache__` files: all 484 packaged files
  were unchanged, but the literal complete-file invariant was not. Repaired
  the neutral referee instructions to export `PYTHONDONTWRITEBYTECODE=1`
  across nested subprocesses and to treat any new cache as drift. No verifier,
  theorem source, lock, PDF, replay, or finite certificate changed.
- Built the 484-member referee ZIP twice independently; both 214,823,405-byte
  archives have SHA-256
  `ca08a3f50154610c7297ca83f92f0c9517fa5422ac7acf53b89582e1e14edbde`.
  ZIP integrity passed. A fresh archive extraction passed every compact prompt
  command with zero packaged-byte drift. The executable evidence is byte-for-
  byte unchanged from the immediately preceding qualified extraction, which
  also passed the 23-layer quick replay and 27/27 outer mutation suite.
- Best-guess completion: **100% for the principal-domain theorem, verifier
  qualification, bioRxiv sources, deterministic referee package, and
  submission readiness**. The only remaining actions are the author-controlled
  GitHub Release/Zenodo/DOI steps, which were explicitly left undone.

## 2026-08-26 — Fresh adversarial round-2 HOLD triage

- Reviewed the fresh referee report as evidence rather than instructions and
  independently inspected the named mutation runners, release binders,
  crosswalk authorities, portable checker, and current literature record.
- Accepted Findings 1--3 as real release-evidence defects: four transport
  cases used tautological byte inequality, while the canonicalizer,
  restoration, and probe wrappers accepted generic nonzero child exits.  The
  production theorem replay itself remains 40/40 PASS and the report found no
  mathematical counterexample.
- Accepted the narrower provenance and presentation repairs: demote stale
  reconstruction prose in C11/C12, expose the executable symbolic-rank replay
  in C05, add an optimized-Python guard to the portable checker, and update
  Brits et al. from arXiv v2 to v3 after confirming that the cited level-1
  Theorem 4.9 is unchanged in the respect used here.
- Recorded the absence of an atlas-free all-family orbit partition as a
  declared nonblocking independence boundary, not as a missing theorem gate.
  No new partition research, mixed-sign extension, compression cycle, or
  verifier rewrite is being opened.
- Best-guess completion remains **100% for the mathematical theorem** and is
  reduced to **approximately 82% for final release qualification** pending the
  verifier-facing mutation repairs, complete reseal, long detached replay,
  deterministic archive rebuild, and independent final audit.

## 2026-08-26 09:43 PDT — Fail-closed wrapper and corrected-universe reseal

- Reproduced the referee's canonicalizer false-PASS mechanism under a missing
  NetworkX dependency and the diagnostic blindness in the restoration and
  probe mutation wrappers.  Replaced generic nonzero-exit qualification by
  clean baselines, exact case diagnostics, explicit rejection of traceback,
  import, timeout, signal, and non-1 failures, and required absence of success
  artifacts.  Added caller-owned atomic outputs and stale-output deletion,
  including optimized-Python negative controls.
- Hardened the corrected restoration, primary probe, probe-input, independent
  probe-graph audit, and unified corrected-universe mutation suites without
  changing any mutation target or mathematical census.  The resulting
  authoritative suites pass 13/13 restoration attacks, 15/15 primary probe
  attacks, 20/20 probe-input attacks plus optimized rejection, 12/12
  independent graph-audit attacks, and 22/22 unified attacks, all with zero
  survivors.
- Independently replayed all 36,824 corrected restoration edges and rebuilt
  the corrected probe and finite-universe provenance chain.  The final unified
  certificate, independent replay, and mutation payloads are respectively
  `f91d8dfcee8af7868d5b821ad2321c0cd2d474b3f3377dfa3f2c22979d364ad8`,
  `636a1c78af804e0bec5405cd0984c0c5f15bc4d2dc4d022c64430e5421b7ef6f`,
  and `fe2636a0bc411b8e1e672eea80c0c8e02e59b43317a3e8c114343b7919f1df75`.
- The authoritative unified run exposed a downstream self-reference: deleting
  its old mutation report made the builder reject the missing output before it
  could regenerate it.  The builder, independent replay, and mutation runner
  now exclude exactly their certificate/replay/mutation outputs from their
  immutable-input fingerprints while still hash-checking every upstream
  locator artifact.  The full corrected-universe validator now passes all five
  families with no blockers; the 405,216 raw-four rows, 2,946,240 theta2 rows,
  36,824 restoration edges, cycle classes, and 34,836 probe equalities are
  unchanged.
- Rebound the theorem-promotion guard to the same byte-verified inputs.  It
  passes its unchanged 23 frozen-input, three probe-artifact, six ledger, ten
  positive-gate, and eight zero-gate census.  No theorem statement,
  classification, or finite census changed.
- Best-guess completion remains **100% for the mathematical theorem** and is
  now **approximately 94% for final release qualification**, pending the
  already-running final parameter-transport reseal, aggregate quick/mutation
  replays, release-lock rebuild, PDFs, and deterministic referee archive.

## 2026-08-26 12:30 PDT — round-2 release-evidence defects closed in source

- Scrutinized all eight fresh referee findings. Findings 1--3 were genuine
  mutation-qualification defects and are repaired with complete
  production-verifier attacks, exact diagnostics, clean baselines, and
  crash/timeout/import/stale-output negative controls. Findings 5--8 were
  valid authority, rank-crosswalk, optimized-mode, and literature metadata
  repairs and are also closed. The atlas-free all-family partition and a
  second symbolic engine remain explicitly disclosed independence boundaries,
  not claimed evidence.
- Replayed the complete raw-rank/raw4 provenance cascade. All 405,216 raw
  directions, 4,379 rank decisions, 16,974 full-map rows, 997 restoration
  parents, 36,824 restoration edges, and every composite classification are
  unchanged. Corrected raw4 overlay, composite, unified-universe, and quartet
  terminal suites pass 9/9, 14/14, 22/22, and 12/12 mutations respectively.
- The release harness now uses the authoritative cycle-promotion replay and a
  fixed ordered contract of 23 quick and 41 full layers. The outer mutation
  suite has 25 active gates; revoked historical suites remain byte-bound but
  cannot qualify the theorem.
- No mathematical, formula, rank, census, transport, reconstruction, or
  theorem statement changed. Best-guess completion is **100% for the
  mathematics** and **approximately 98% for final release qualification**,
  pending the final lock, detached full replay, source-bound PDFs/telemetry,
  deterministic archive, commit, and independent package audit.

## 2026-08-26 17:49 PDT — round-2 qualification passes

- A detached clean sparse checkout at commit `f6befbce38cfb21e27b8dc4a9611d284fdcbc800`
  passed all 41 full-replay layers with zero blockers in 5,697.15 seconds wall
  time and 2,552,119,296 bytes maximum RSS. The source-bound report and
  telemetry hashes are `2489643d65c50f662d027bf5002b9f398c8fa2999d7a17fcf43a5334cb04e86e`
  and `b0f379d5e9d7e3acfd4c9812711964c4f7894dfd15e28045eab8077a9e6bd18f`.
- The final outer suite rejected 25/25 conceptual mutation gates with zero
  survivors in 3,458.50 seconds. Its deterministic report hash is
  `f2a362e9d2606b0315f9fe6e5a7659d328bd73bcf6552f0c1cc4c4f8ecdd0026`.
- Final replay exposed and closed two additional harness defects: a stale
  raw-four byte binding in the theta2 composite differential, and a staged
  dependency-omission test that had invoked `--help` before imports. The
  corrected differential and a real import preflight now pass. Telemetry now
  accepts both BSD compact and POSIX `time` layouts under exact parsing.
- The static audit has zero findings; crosswalk and referee-manifest checks
  pass after removing revoked mutation regressions from current C05 authority
  and explicitly retaining the executable symbolic rank verifier and syzygy
  module.
- No theorem statement, algebraic certificate, classification, rank, finite
  census, restoration edge, transport, probe row, or sharpness witness
  changed. The deterministic 489-member archive was built twice identically;
  two differently named extractions passed the package check, 23-layer quick
  replay, and 25/25 outer mutation suite with byte-identical reports. Best-guess
  completion is **100% for the mathematics** and **100% for release
  qualification**, subject only to the author's GitHub Release/Zenodo choices.

## 2026-08-27 — round-3 referee HOLD repaired in source

- Reproduced both release-evidence defects from the submitted archive: the two
  stale printed composite-reseal hashes and permissive acceptance of a
  same-valued duplicate JSON object name after a legitimate outer reseal.
- Added an integrated 26-row printed-authority gate with nine focused
  mutations, and independent strict duplicate-name parsers in the outer
  producer and checker.  The outer mutation suite now includes both
  same-valued and conflicting-valued duplicate-name attacks after reseal.
- Corrected the citation-check chronology, updated the JC companion reference
  to the public v1.1.7 preprint and data DOIs, replaced the overbroad
  “immutable tag” wording with a designated versioned annotated v1.0.3 source
  tag, completed the crosswalk history, and made unexpected parameter-test
  child failures emit bounded sanitized diagnostics without weakening their
  fail-closed status.
- Resealed every affected downstream certificate.  The parameter transport
  ledgers remain byte-identical and its authoritative mutation suite rejects
  10/10 attacks.  The quartet logic, semantics, terminal, and terminal-mutation
  certificates pass with unchanged mathematical contents.  The unified lock
  is ready with zero blockers, and the regenerated proof-compression package
  retains the same finite classifications and PC-PARTIAL conclusion.
- Rebuilt the 26-page article and 24-page supplement reproducibly.  Both have
  embedded fonts, no undefined references or citations, no overfull boxes or
  PDF-string warnings, and passed a complete rendered-page visual inspection.
- No theorem statement, formula, census, rank decision, separator,
  restoration edge, transport, probe row, or weak-sharpness witness changed.
  Best-guess completion remains **100% for the mathematical theorem** and is
  **approximately 99% for v1.0.3 release qualification**, pending the detached
  quick/full replays, final outer mutation run, deterministic archives,
  independent package audit, commit/push, and annotated source tag.

## 2026-08-27 — round-3 v1.0.3 qualification complete

- A detached clean sparse checkout at source commit
  `1ef5dd2737a50fd33bc3b15d63e0ba70b050e03f` passed all 23 quick layers and
  all 41 full primitive-regeneration layers with zero blockers.  The full run
  took 5,880.83 seconds wall time and 2,617,720,832 bytes maximum RSS; its
  report and telemetry hashes are
  `5a5f62104bea1e88d725aa3cee0441c369d53905f71fe30bc20de82f4eadb35e`
  and
  `200b8f18dcd01c2f9fc4f3013b6963b3b8e8083b1acb6a591e28c6e42f7695e3`.
- The final outer suite rejected all 25 conceptual mutation gates with zero
  survivors in 3,538.22 seconds.  The separately implemented package readers
  rejected all 33 package mutations, including both resealed duplicate-name
  attacks, with payload
  `62a056e21c8a514fe2e7e96ab952464fcb0a1489d785ccde8ff390e5f5006fe2`.
- The static audit has zero findings and binds all 26 printed authority/hash
  rows.  Both 26-page and 24-page PDFs build twice identically, have embedded
  fonts and clean logs, and passed inspection of all 50 rendered pages.
- The deterministic referee archive was built twice byte-identically, passed
  ZIP integrity, passed the strict checker in two differently named fresh
  extractions, and passed the 23-layer quick replay from an extracted copy.
  It is 214,944,591 bytes with SHA-256
  `51f502290434cd3415936ef69e3c5afe71438fa892d5b9e6998feecc47489278`.
  The deterministic five-source bioRxiv ZIP has SHA-256
  `e9eec990d85d349109a1379b6d322da4e6a073891ba94886db385201d0f8e2e5`.
- No theorem statement, formula, finite census, rank decision, restoration
  edge, transport, probe row, or sharpness witness changed.  Best-guess
  completion is **100% for the mathematical theorem** and **100% for v1.0.3
  release qualification**.  GitHub Release, Zenodo, DOI, and submission
  actions remain reserved to the author.

## 2026-08-27 — fresh round-4 HOLD triage

- Read the complete fresh adversarial report as evidence rather than as
  instructions and independently reproduced both blocking interface failures
  against the v1.0.3 sources.  A coherently layer-resealed conflicting JSON
  object-name duplicate in the first compressed probe row was accepted by the
  independent probe verifier, and the documented portable package verifier
  completed successfully under `python -O`.
- Accepted both findings as valid fail-closed and reproducibility defects.
  They do not alter any clean ledger row or supply a mathematical
  counterexample: the referee's clean quick/full replays, independent finite
  scans, exact calculations, and the existing theorem proof all passed.
- Opened bounded repairs for one duplicate-aware, bounded, canonical
  compressed-JSON boundary; semantically resealed duplicate-name mutations;
  optimized-mode preflights on every documented portable entry point; and
  removal of assertion-dependent certificate semantics in the portable atlas.
- Best-guess completion remains **100% for the mathematical theorem** and is
  reduced to **approximately 88% for corrected release qualification**,
  pending focused adversarial qualification, recursive resealing, detached
  quick/full replay, deterministic archive rebuild, commit/push, and a new
  annotated source tag.  GitHub Release and Zenodo actions remain explicitly
  excluded.

## 2026-08-27 — round-4 compressed-JSON boundary repaired

- Reproduced the referee's coherently layer-resealed duplicate-name attack:
  the former probe verifier accepted a conflicting earlier
  `parent_anchor_id` because Python's default decoder retained the later name.
- Added one frozen shared `strict_json.py` reader. It rejects repeated names at
  every nesting depth, non-finite constants, noncanonical decompressed gzip
  JSON/JSONL bytes, blank or unterminated rows, and explicit compressed,
  expanded-stream, document, and row size limits.
- Routed the outer referee-bundle producer, corrected probe replay, and
  crosswalk-designated local compressed-evidence replay surfaces through that
  reader. The independent outer checker implements the same bounded policy
  separately. The isolated full-probe and site-partition harnesses now carry
  the lock-bound reader into their temporary project trees.
- Added exact same-valued duplicate, conflicting duplicate, and noncanonical
  row attacks after a valid probe-layer reseal, plus outer-scanner and bounded
  synthetic syntax attacks. All three probe attacks reject with their intended
  `STRICT_JSON_*` diagnostics and leave no success artifact. A clean scan of
  all 26 shipped compressed JSON families passed after reading approximately
  7.1 GiB of decompressed canonical evidence.
- No tensor, graph, formula, census, rank, separator, restoration parent/child,
  transport, probe relation, or theorem statement changed. Best-guess
  completion remains **100% for the mathematical theorem** and is
  **approximately 92% for corrected release qualification**, pending the
  coordinated certificate/lock reseal and detached quick/full replays.

## 2026-08-28 — round-4 source and finite-evidence reseal checkpoint

- Completed the optimized-mode repair across the enumerated portable
  production surface, replaced all 22 atlas assertion checks by explicit
  invariant failures, and passed the two-mode entry-point matrix with no
  residual output.
- Regenerated the complete raw/rank layer, the four-port direct overlay,
  theta2, restoration, cycle, corrected composite, probe, parameter-transport,
  and unified corrected-universe evidence.  The fresh six-source four-port run
  contains all 1,931 classes and has the same mathematical projection roots as
  v1.0.3.  The theta2 replay rebuilt all 2,946,240 directions with unchanged
  mathematical rows and only the licensed provenance rebind.
- The corrected probe suite now rejects 18/18 attacks, including coherently
  layer-resealed same-valued and conflicting duplicate names and a
  noncanonical compressed row.  The independent probe audit rejects 12/12,
  and the parameter-transport suite rejects 10/10 with zero unresolved rows.
- Fixed one newly exposed relocation control so its deliberately missing
  quartet binder remains the tested dependency while the strict parser is
  supplied explicitly.  This changed no mathematical artifact.
- Best-guess completion remains **100% for the mathematical theorem** and is
  **approximately 97% for v1.0.4 release qualification**, pending the final
  recursive lock, proof-compression/PDF reseal, detached 23/25/41-gate run,
  two-extraction archive checks, commit/push, and annotated source tag.  No
  GitHub Release or Zenodo action is authorized.

## 2026-08-28 05:04 PDT — round-4 output-isolation hardening checkpoint

- Detached qualification exposed that the newly guarded direct-mutation
  runner could leave a stale caller-owned PASS report when optimized mode was
  rejected before output cleanup, and that its standalone source-root policy
  depended on extraction depth.  Both were repaired and their focused direct
  suite again rejected all 11 attacks.
- A separate read-only audit then found the symmetric symlink-policy edge
  case: a lexical path inside the source tree could point to an external
  target and evade validators that checked only the resolved target.  All
  affected nested and outer report validators now reject when either the
  normalized lexical path or resolved target lies inside the source tree.
  The regressions exercise both symlink directions, hardlinks, late swaps,
  stale PASS bytes, optimized mode, and arbitrary-depth portable extraction.
- Replayed and resealed the affected probe-input, canonicalizer, weak-
  sharpness, restoration, probe, direct-closure, and unified finite-universe
  mutation evidence.  The deep primitive probe audit again covered all 176
  anchors, 29,964 one-port rows, 544,571 two-port rows, 67,741 transports,
  and 4,379 restrictions; all 12 independent mutations rejected.  The probe,
  restoration, and unified suites rejected 18/18, 13/13, and 22/22 attacks.
- No theorem statement, graph classification, tensor formula, rank decision,
  census, restoration edge, transport, probe relation, or sharpness witness
  changed.  Best-guess completion is **100% for the mathematical theorem**
  and **approximately 98% for v1.0.4 release qualification**, pending the
  final recursive lock, detached 23/25/41-gate qualification, deterministic
  two-extraction packages, commit/push, and annotated tag.  No GitHub Release
  or Zenodo action is authorized.

## 2026-08-28 05:45 PDT — detached-gate provenance correction

- The first detached quick replay fail-closed on a stale embedded promotion
  hash table.  The underlying regenerated probe, independent replay, and
  mutation artifacts already agreed; the verifier's literal expected hashes
  had not been rebound with them.  Rebound those three identities and the one
  affected restoration-mutation identity, after which the promotion gate
  passed all 23 frozen inputs, three probe artifacts, six ledgers, ten required
  PASS gates, and eight required-zero gates.
- Rebuilt the 231-file outer release lock, the proof-compression baseline and
  family-equivalence certificate, the PC-PARTIAL result, old/new equivalence
  record, printed appendix, referee content ledger, supplement, and both PDFs.
  The old/new replay passed all seven commands twice in 121.676 and 121.543
  seconds; the mathematical residue remains zero.
- The local 23-layer quick replay passed in 399.011 seconds under the new lock.
  All 50 PDF pages (26 article and 24 supplement) were rendered and visually
  checked with no clipping, overlap, or broken table detected.
- No mathematical assertion or finite classification record changed.  Best-
  guess completion remains **100% for the mathematical theorem** and is
  **approximately 98% for v1.0.4 release qualification**, pending the clean
  25-attack mutation run, 41-layer full primitive replay, final telemetry,
  two-extraction archive checks, commit/push, and annotated tag.  No GitHub
  Release or Zenodo action is authorized.

## 2026-08-28 — full-replay staging regression repaired

- The detached 25-attack production mutation run passed with zero survivors
  in 4,142.76 seconds and 2.62 GB maximum resident memory.
- The subsequent full replay passed every layer through the composite-domain
  reseal-difference check, then fail-closed before rank replay because its
  temporary workspace created the shared `work/` parent twice and the second
  creation lacked idempotent directory semantics.  This was a harness staging
  error caused by the newly copied strict reader, not a mathematical or finite-
  evidence disagreement.
- Factored the full-rank temporary layout into one idempotent helper and added
  a focused regression exercising its overlapping parents.  The focused final-
  replay contract now passes.  Rebuilt the 231-file outer lock, PC-PARTIAL
  package, old/new equivalence record, referee content ledger, supplement, and
  PDFs.  The compressed theorem still has zero unresolved mathematical rows.
- Best-guess completion remains **100% for the mathematical theorem** and is
  **approximately 98% for v1.0.4 release qualification**, pending a new clean
  quick/mutation/full run from the repaired commit, final telemetry, archive
  checks, push, and annotated tag.  No GitHub Release or Zenodo action is
  authorized.

## 2026-08-28 — round-4 release qualification closed

- Qualified the exact detached source candidate at commit
  `0b9cbb6eb0de99ad07142609da47f4db657d3ed7`: quick replay passed 23/23,
  the production mutation suite rejected 25/25 attacks with zero survivors,
  and the full primitive replay passed 41/41 layers with zero blockers.
  The full run took 6,259.77 seconds and reached 2,568,503,296 bytes maximum
  resident memory.
- The independent referee-package suite rejected all 37/37 attacks after its
  output was regenerated and checked separately.  The final mutation harness
  uses a 300-second per-command bound because strict canonical scanning of the
  complete resealed package can legitimately exceed the former 90-second
  harness allowance; the verifier result and diagnostic remain fail-closed.
- Built the 495-member referee ZIP twice byte-identically at SHA-256
  `43a620bad862ad14c1b7beb6d605d69354c7da8c534e2882cd7564f7ad4a69db`
  and the five-source bioRxiv ZIP twice byte-identically at SHA-256
  `8e8c4b173e57c310b179f33315da7668f9e5bc13984a97656afaa3dc02dccd84`.
  Two differently named fresh referee-package extractions independently
  passed their portable ledgers, strict bundle checkers, strict-JSON tests,
  and all 23 quick layers.
- Both round-4 referee findings were valid reproducibility defects and are
  repaired.  No theorem statement, graph classification, finite census, rank
  decision, polynomial body, restoration edge, transport, probe relation, or
  sharpness witness changed.  Best-guess completion is **100% for the
  mathematical theorem** and **100% for v1.0.4 release qualification**.
  GitHub Release, Zenodo, DOI, and submission actions remain reserved to the
  author.

## 2026-08-29 — round-5 typed-authority repair checkpoint

- Confirmed the referee's release-only finding: the supplement and static
  auditor had labelled the 16,974-row strict-sign overlay as the 934-class
  raw-four terminal registry.  Rebound the reader anchor to the actual typed
  registry and added duplicate-aware schema/cardinality checks plus coherent
  overlay-substitution and wrong-cardinality attacks.  All 11 focused attacks
  are rejected for their intended diagnostics.
- Updated three stale narrative evidence tables and made their role explicit:
  they are versioned reader snapshots, while the generated release lock is the
  byte authority.  The static source auditor now checks that classification.
- Resealed only the affected quartet document bindings, corrected-universe
  locator/certificate/replay/mutations, 231-file release lock, PC-PARTIAL
  summaries, and PDFs.  No raw-four, theta2, rank, restoration, cycle, probe,
  polynomial, or sharpness ledger was regenerated or changed.
- The new quick replay passed 23/23 layers in 406.35 seconds, and the affected
  outer mutation qualification rejected all 25/25 gates with zero survivors.
  The article and 24-page supplement rebuild cleanly; the changed supplement
  pages were visually inspected with no clipping or overlap.
- Best-guess completion remains **100% for the mathematical theorem** and is
  **approximately 98% for v1.0.5 release qualification**, pending the single
  detached 41-layer full replay, telemetry, final crosswalk/package reseal,
  deterministic double archives, push, and annotated tag.  No GitHub Release
  or Zenodo action is authorized.
