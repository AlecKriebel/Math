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
