# Research log: dB extremality paper

## 2026-08-20 — package opened

- Chose a unified paper around the normalized complete-kernel gap, with the
  fixed-graph strong-selection theorem and the full-directed fitness-two
  local theorem as co-headlines.
- Preserved the earlier manuscript as provenance and opened this isolated
  package for the expanded paper.
- Fixed the claim boundary: local maximality is in normalized replacement-
  kernel space; raw incoming-column scalings are dynamical gauge directions.
- Fixed the quantifier boundary: the paper rules out one **fixed finite**
  universal dB amplifier, but does not rule out a fitness-independent graph
  sequence whose population threshold depends on fitness.
- Assigned independent theorem, scope, and reproducibility audits before
  authoring.
- Best-guess completion: 10% of the publication package; theorem components
  are proved, but synthesis, replay integration, rendering, and adversarial
  review remain.

## 2026-08-20 — hostile normalization audit and claim correction

- An independent audit unwound the proposed standard-sector quotient to the
  labelled active chain and found that the previously cited phase theorem
  signs a nearby inverse-rank reward, not the physical Poisson reward in the
  fixation Hessian.  There is no established positive scalar normalization
  between them.
- Removed the unsupported full-directed local-maximality claim.  The exact
  theorem retained here is stronger than the old regular/undirected result:
  the complete kernel is stationary in every normalized tangent direction
  and strictly locally optimal throughout the full directed bistochastic
  subpolytope.  The symmetric-balanced and antisymmetric-balanced sectors are
  both proved for every order; the standard column-imbalance sector is now
  stated explicitly as open.
- Removed the non-load-bearing standard verifier from the paper replay and
  replaced the symmetric quotient's unspecified positive normalization with
  its exact physical identity.
- Best-guess completion: 35% of Paper I.  The claim set is now conservative;
  full certificate integration, rendering, and repeated hostile review
  remain.

## 2026-08-20 — physical standard sector repaired and independently audited

- Replaced the nonphysical auxiliary standard reward by the exact Poisson
  reward induced by the labelled active-chain Hessian.  The quotient scalar
  is
  $\Phi_N=\sigma(I-H)^{-1}\gamma$, with
  $\mathcal R_n^{(2)}(E(\xi))/\|\xi\|^2
  =\Phi_N/[4(N+1)^2(N-1)]$.
- Proved $\Phi_N>0$ for every $N\ge2$: exact Schur elimination, a positive
  first-phase barrier, a uniform completed-phase contraction, and a Neumann
  tail handle $N\ge10$; exact rational values close $2\le N\le9$.
- A hostile audit caught an invalid attempted use of the local $W$ barrier in
  the lower-bound step.  The final proof instead uses the independent global
  resolvent bound $R_Qq\le4N\mathbf1$.  The corrected distinction is explicit
  in the theorem note and verifier.
- Two independent reviewers rebuilt the labelled quotient and normalization,
  checked every population-size polynomial identity and boundary inequality, and
  replayed the final exact verifier.  No mathematical objection remained.
- Restored the full row-stochastic directed local theorem and integrated all
  three physical tangent sectors into the manuscript.

## 2026-08-20 — journal package and provenance pass

- Converted references to author--year form, expanded the graphical-duality
  context, and made the full-versus-finite verification boundary explicit.
- Disclosed the public v1.0.0 strong-selection/low-order archive and separated
  its previously released results from the fitness-two coverage, collision,
  and all-sector Hessian theorem introduced in this manuscript.
- Added exact standard and symmetric normalization bridges, explicit channel
  ranges, journal-style declarations, and a readable quantifier ledger.
- Best-guess completion: 75% of Paper I.  Remaining work is the standalone
  bundle, final clean-room replay, full-page visual audit, and repeated
  adversarial manuscript review.

## 2026-08-20 — Paper I frozen after clean-room and hostile review

- Expanded the symmetric-sector appendix to include the every-order labelled
  incoming-current normalization, fixed-count sampling identities, channel
  ranges, positive-resolvent premises, and every finite/large-order boundary
  certificate used by the sign proof.
- Replayed the complete exact suite from the development tree and from a
  fresh extraction with Python 3.14.6, SymPy 1.14.0, and python-flint 0.9.0.
  Both replays exited zero.  A first clean-room attempt exposed one omitted
  transitive verifier dependency; the deterministic manifest was corrected,
  and a second genuinely clean extraction passed in full.
- Rebuilt the manuscript reproducibly inside the extracted archive.  Its
  26-page PDF was byte-for-byte identical to the repository build, with
  SHA-256
  `2720d0a5d372330c3c2b3212dcf16c6d74ddedf0e0bd7a2b06cd8946e131184e`.
- Generated the deterministic 92-entry source-and-certificate archive twice
  at the clean-room checkpoint; the copies were byte-for-byte identical, with
  checkpoint SHA-256
  `0993ee6d138508c9bd3e8729dbbad60c1127528690fc695ffb54c94cd8dde217`.
- Three adversarial reviews checked the headline quantifiers, directed dual,
  collision normalization, tangent decomposition, physical normalization of
  all sectors, strong-selection closure, submission metadata, archive
  dependency closure, and every rendered page.  The final verdict was a
  clean pass.  The sole remaining token is the intentionally human-gated
  postal address in cover-sheet material.
- Paper I completion: 100% of the requested manuscript, certificate,
  reproducibility, and submission package.

## 2026-08-20 — external adversarial-review revision

- Adjudicated twelve detailed reviewer comments against the labelled chains,
  exact certificates, source, and primary literature.  No headline theorem
  was withdrawn.  The review correctly identified an ambiguous phase order in
  the collision interpretation, an overly compressed antisymmetric coupling,
  and several explicitness and positioning gaps.
- Rewrote the collision statement in the stationary sample--then--retarget
  chain, with the two conjugate stationary laws displayed.  Expanded the
  strict rank-Poisson monotonicity argument into a four-chain heat-bath
  coupling and made the finite symmetric-sector calculation a formal exact
  computer-assisted lemma with its case ranges, minimum margin, expected
  output, and verifier hash.
- Added proofs of dual irreducibility and aperiodicity, strict positivity near
  the complete kernel, the standard-sector Frobenius normalization, and
  fitness monotonicity.  Retitled the paper to foreground local optimality,
  sharpened the boundary with the Tkadlec et al. theorem, and added a neutral
  new-versus-released result ledger.
- Expanded the ancestry and contemporary amplification context using primary
  literature.  Replaced unverifiable human-execution language by a precise
  responsibility statement and instructions for independent replay.
- Hardened the release command so that it replays the exact suite and rebuilds
  the PDF before packaging.  A new clean-room replay, deterministic archive,
  and final hostile review remain before this revision is frozen.
- Best-guess completion: 90% of the adversarial-review revision; the proof and
  presentation edits are complete, while clean-room and final-review gates
  remain.

## 2026-08-20 — adversarial revision clean-room checkpoint

- Replayed the complete exact suite after the accepted review changes; every
  load-bearing assertion passed.  The paper-level integration audit now also
  checks the standard-sector Frobenius conversion introduced in the revision.
- Generated two byte-identical deterministic archives from the same inputs.
  In a new extraction, all manifest hashes passed, the pinned Python 3.14.6
  environment with SymPy 1.14.0, python-flint 0.9.0, and mpmath 1.3.0
  installed cleanly, and the full exact replay exited zero.
- Rebuilt the 29-page PDF inside that extraction.  It matched the repository
  PDF byte for byte, with SHA-256
  `3af20b4648c6a69e1946e6cdd32f5df9557ca55a2ec1a1c16b29a8dbb6e92d98`.
- Inspected every rendered page at full-page resolution.  No clipping,
  malformed equations, unreadable certificate text, or bibliography/layout
  defect was found.
- Best-guess completion: 97% of the adversarial-review revision.  Only the
  final independent hostile review, any resulting repair, and the final
  commit/push remain.

## 2026-08-21 — second adversarial review and final validation

- Adjudicated the revised-paper review point by point.  Accepted the genuine
  formal repairs: rectangular sample/retarget phase spaces, stationary-law
  uniqueness, mixed-difference definitions, normalized-kernel/raw-weight
  notation, and neutral disclosure of the public simultaneous-amplification
  companion.  The purported large-order strictness issue was a presentation
  gap rather than a theorem gap; the already positive certificate supplies
  the strict inequality.
- Added exact integration guards for the empty-cache phase boundary and raw-
  versus-normalized strong-selection defect.  Strengthened the finite
  symmetric certificate so that it explicitly asserts the exact minimum
  rational margin printed in Appendix A, then bound the manuscript to the
  verifier's updated SHA-256
  `b4d45a83ce5f21a1fd3e09403b376e071330290a01affff64711574b69e024bc`.
- The full development replay and a genuinely fresh Python 3.14.6 bootstrap
  replay both exited zero.  Every internal archive-manifest entry passed, and
  two independently generated 84-member archives at the pre-log checkpoint
  were byte-for-byte identical.
- Rebuilt the 30-page PDF inside the clean extraction.  It was byte-for-byte
  identical to the repository PDF, with SHA-256
  `229747f2a62906dea8976bbad747d0b8a109fb606a4a7695548613a245a93e66`.
  A visual audit caught and repaired one floating $K_4$ figure; the final
  every-page recheck found no clipping, malformed equations, stretched
  bibliography text, or misplaced floats.
- Independent mathematical, visual, submission, and reproducibility audits
  reported no remaining actionable defect.  Human-only submission fields
  (city/country, postal address, factual funding/conflict confirmation, and a
  future persistent release identifier) remain deliberately unfilled.
- Paper I completion: 100% of the requested second-review revision,
  validation, and reproducibility cycle.

## 2026-08-22 10:08 PDT — final availability and referee-handoff checkpoint

- Adjudicated the final external review.  Its sole required point is correct:
  the manuscript still contained an internal future-release instruction.
  Replaced it with final submission prose naming the exact accompanying
  source archive, its detached whole-archive checksum, its internal payload
  manifest, and the clean-replay guide.  This avoids both a mutable-branch
  citation and an impossible archive self-hash.
- Accepted the three nonblocking clarity edits: smoother triangle/$K_4$
  grammar, ``strict local rigidity'' in place of ``full local rigidity,'' and
  a responsibly rounded companion threshold while retaining the rigorous
  inequality $R_{\rm hyb}>3/2$.  No theorem, hypothesis, equality case, or
  citation scope changed.
- Added a neutral AI-referee handoff design: independent-review prompt,
  theorem-to-code inspection map, report template, package verifier, and a
  disposable clean-replay/PDF-identity command.  The referee-facing source
  archive now omits prior verdicts, research diaries, and saved successful
  output while retaining all proof documents and independent checking code.
- Best-guess completion: 70% of this final-review task.  Source validation,
  frozen packaging, a clean referee-package replay, visual inspection, final
  hostile review, and commit/push remain.

## 2026-08-22 10:27 PDT — frozen AI-referee package and final hostile pass

- Replayed the complete Paper I suite while regenerating the final release:
  all six unit tests and all seventeen invoked verifier/cross-check programs
  exited zero.  Rebuilt and visually inspected the 30-page manuscript.  Its
  SHA-256 is
  `a6bda621b764ca8ee86658f6b68de0245790b84315eb77a6cc7ca45f7953bd2d`.
- Froze a 70-member scientific source archive after removing prior review
  verdicts, research diaries, saved successful output, and the historical
  reproduction report.  All proof documents and independent checking code
  remain.  The whole-archive SHA-256 is
  `b1b7b7c4c9393ee4fa85eeacd54cefc4bcc94a3eca759d500c9ee6a362eddd2b`,
  and every nonsynthetic archive member was byte-checked against source commit
  `3652cfda20a3edad1b4e9ca75a4e5536f6f7f5ba`.
- Built the copied referee folder with 80 outer-manifest payloads, an exact
  extracted source tree, convenience PDF, neutral prompt, claim-to-code map,
  report template, package verifier, and disposable replay command.  Its
  deterministic transport archive has SHA-256
  `d5634b0c8a1adf05d9c623b010a61e357b95869ef4264ca0b3f3aa781dd53b2d`.
- Executed the delivered referee command end to end from the package with a
  fresh pinned environment.  It rechecked both manifests, installed Python
  3.14.6 dependencies, repeated the complete replay, rebuilt the PDF with the
  pinned document tools, and obtained byte identity.  The 156-line transcript
  has SHA-256
  `fcbc301382989fc0119f56c02b8ff13ff5dd39242a94150bc1b8bd0b9064a713`.
- A final independent hostile audit repeated package, transport, commit-byte,
  executable-mode, neutrality, replay, and post-run immutability checks.  Its
  verdict was a clean pass with no remaining blocker or material minor issue.
- Paper I final-review and AI-referee-handoff task: 100% complete.  Only
  human-controlled submission metadata and portal actions remain outside this
  task.

## 2026-08-22 14:37 PDT — independent-referee correction checkpoint

- Adjudicated all five findings in the independent referee report.  No
  mathematical claim, range, normalization, equality case, or theorem proof
  required repair.  The certification defect under optimized Python was real;
  the helper-reachability, proof-status wording, dependency provenance, and
  standalone Make-target findings were also accepted in their narrowed forms.
- Replaced all 406 bare assertions in the delivered scientific Python files,
  and all 28 in the development submission guard, by explicit failure checks.
  An AST comparison confirmed that every original test expression and message
  was preserved.  The new bundled-source audit finds no remaining
  optimization-elidable `assert` and at least 406 explicit scientific checks.
- Hardened every advertised launcher against inherited Python optimization,
  import-path, and Make overrides.  Added ordinary and `python -O` negative
  controls, a fresh-environment wheel-only SHA-256 lock, dependency-origin
  checks, and a pinned Tectonic v33 bundle digest.  Paper I now invokes all
  seventeen verifier/cross-check programs directly; the historical Make target
  remains intact for the earlier manuscript but is absent from this archive.
- Corrected the helper function-level reachability map and finite-versus-
  analytic proof-status language.  The manuscript now states explicitly that
  the universal directed and all-order antisymmetric conclusions come from the
  analytic proofs, while the literal-chain runs are finite consistency tests.
- A post-fix hostile launcher audit found and closed two additional bypasses:
  a non-Python command supplied through `PYTHON` could previously return zero
  without running the preflight, and an inherited external bytecode-cache
  prefix could affect later non-isolated imports.  Replay now authenticates a
  preflight sentinel, clears the full import-control set, rejects the false
  interpreter in a package negative control, and checks the exact per-file
  inventory of all 406 converted scientific conditions.
- A fresh Python 3.14.6 bootstrap installed all three hash-verified wheels, and
  the complete six-test/seventeen-program replay exited zero.  Two document
  builds were byte-identical; the visually inspected 30-page PDF has SHA-256
  `22142ee518e75c00d1948b19c210818ec797946df86a5e3272c9d1017800b0f4`.
- Best-guess completion: 75% of the referee-correction task.  The corrected
  source release, r2 referee package, mobile-access copy, independent hostile
  review, and final commit/push remain.

## 2026-08-22 15:07 PDT — corrected r2 referee package and final hostile pass

- Bound the corrected scientific source, release archive, and manuscript to
  commit `e63cc44748e4084ade67c5ff7dc5d1bf2a872f7c`.  The 71-member source
  archive has SHA-256
  `1754bee519537105f192a40d98f83a4b2fd5097897e0632d88ace1e9892d59ed`;
  the 30-page PDF has SHA-256
  `22142ee518e75c00d1948b19c210818ec797946df86a5e3272c9d1017800b0f4`.
- Built the separately named r2 referee folder with an 81-entry outer payload
  manifest and an exact extracted source tree.  Its deterministic transport
  archive has SHA-256
  `a39d45004fa7bd5cd5a8df01f91ae96f93f5a1a9821ef6f1a5a34e5c39938936`.
- Executed the delivered command in a hostile inherited environment.  All
  four negative controls, six unit tests, seventeen verifier/cross-check
  programs, hashed dependency checks, pinned document-tool checks, and the
  deterministic PDF identity comparison passed.  The package manifest still
  passed after execution.
- A final independent hostile audit byte-compared all 69 project-source
  members to the bound commit, independently checked all manifests and
  sidecars, verified the exact wheel-hash inventory and claim-to-code map,
  repeated the fail-closed controls and full workflow, and confirmed that the
  package tree digest was unchanged.  It reported a clean pass with no
  blocker or minor finding.
- Copied, without replacing the original referee delivery, the r2 folder,
  transport archive, detached checksum, current `main.tex`, and bibliography
  source `references.tex` to the existing Google Drive Paper I folder.  The
  copied package passed its own integrity verifier and the three top-level
  files were byte-identical to their source copies.
- Paper I independent-referee correction and r2 handoff: 100% complete.  No
  theorem or proof changed; only human-controlled submission actions remain.

## 2026-08-22 22:01 PDT — R2 re-review hardening checkpoint

- Independently reproduced both integrity defects reported in the R2
  re-review.  A marker-printing program supplied through the public `PYTHON`
  override could satisfy the old token-based launcher without executing any
  verifier, and a timestamp-valid adjacent bytecode file could execute from
  an otherwise hash-valid source extraction.  Both findings are therefore
  accepted.  Neither affects a theorem, proof, exact certificate, numerical
  value, or the 406 scientific failure conditions.
- Replaced the token-authenticated workflow by one sole certified entry point,
  the package-root `run_all_referee_checks.sh`.  It rejects interpreter
  overrides, exact-scans the delivered package, extracts only verified regular
  files into a new empty source directory, and invokes the bootstrap and
  replay scripts only as internal stages tied to its private runtime.
- Added exact file-and-directory inventories, `lstat`-based rejection of
  symlinks and special nodes, explicit rejection of bytecode and cache nodes,
  and a fresh private cache supplied through `-X pycache_prefix` for every
  project-Python invocation.  The safety audit derives its AST inventory
  directly from the verified manifest before importing project code and
  confirms that the cache is empty both before and after replay.
- Added fail-closed controls for the former public-token interpreter attack,
  adjacent hostile bytecode, an extra regular file, an extra empty directory,
  a symlink, and a FIFO.  The hostile-bytecode control preserves the companion
  source file's size, modification time, and manifest hash, so it directly
  exercises the reported cache-selection mechanism.
- Updated the manuscript and all bundled reproduction documents to distinguish
  the sole certified package route from development and internal stages.  A
  clean Python 3.14.6 development replay passed all six unit tests and all
  seventeen verifier/cross-check programs; the 30-page PDF rebuilt cleanly.
- Best-guess completion: 70% of the R2 re-review correction task.  The frozen
  source archive, r3 referee package, outer certified replay, independent
  hostile review, Drive copy, and final commit/push remain.

## 2026-08-22 22:35 PDT — frozen R3 package and independent hostile pass

- Froze the corrected scientific source at commit
  `b9a415f763e82d9cc45c83de96c895b109e158a4`.  The 73-member deterministic
  source archive has SHA-256
  `12a8c89b77aa898e9c16a1efdf93e77f35ea3cee3eed93ad34c7f497eaad3eb0`;
  all 71 nonsynthetic members independently byte-match that commit.  A second
  archive generation was byte-identical.
- Rebuilt and visually inspected the 30-page manuscript.  Two consecutive
  builds were byte-identical, with PDF SHA-256
  `5d2bc6cfa9d02b21e816d3dd30252d067e23b51ecd0c58bb8c3cfb116ab937bd`.
  No theorem-bearing manuscript text or scientific predicate changed; only
  the certified-route reproducibility description was revised.
- Built the R3 referee folder with 83 manifest payloads and 84 total regular
  files.  Its deterministic transport archive has SHA-256
  `7e218882df2cf1bba3c5a914a706552bcfe22820dcbc98461df01511286c6717`.
- Ran the sole certified launcher under hostile inherited import, bytecode-
  cache, and Make settings.  It rejected the token-printing interpreter,
  timestamp-valid hostile bytecode, extra regular file, extra empty directory,
  symlink, and FIFO before project import; then all six unit tests and all
  seventeen verifier/cross-check programs passed with the private cache empty.
  The rebuilt PDF matched byte-for-byte.  The 173-line transcript has SHA-256
  `8312c9a552c0be05459cdb7e6efa6ba61c41acdebef4d94473785a1caa0aa347`.
- A separate hostile package audit repeated the exact-tree, source-commit,
  transport, attack-fixture, replay, and PDF-binding checks.  It found no
  blocker or minor defect; the 110-node package fingerprint was unchanged
  before and after execution at
  `dcea48df9a6a1b6f337ff33d45a94a15e2353e9677670f745bc9063c4eb36899`.
- Copied the separately named R3 folder, transport archive and checksum, and
  current `main.tex` and `references.tex` into the existing Google Drive Paper
  I handoff location.  The copied R3 folder passed its own exact package
  verifier.
- Paper I R2 re-review correction and R3 handoff: 100% complete.  Both
  referee findings were real and are closed on the sole certified route; no
  theorem or proof changed.  Only human-controlled submission actions remain.

## 2026-08-23 18:36 PDT — Figure 1 and month-only date refresh

- Reproduced the reported Figure 1 collision in the rendered manuscript: the
  open-problem sentence crossed the blue fitness-two axis.  Moved that label
  wholly to the right of the axis and split it at a natural phrase boundary;
  its mathematical meaning is unchanged.
- Replaced the day-specific title-page date by `August 2026` so the same PDF
  can be submitted throughout the month.  No cover-letter date, theorem,
  proof, citation, formula, or scientific verifier changed.
- The first visual pass confirmed that correction but missed a second, subtler
  collision: the black vertical axis crossed the blue local-optimality label.
  A separate hostile layout audit caught it.  Moved the entire blue label to
  the left of the vertical axis, then rebuilt and inspected the full-resolution
  page-3 render; all blue, black, and red elements now have clear separation
  with no clipping.  The hostile auditor independently confirmed the final
  layout, and page 1 displays the month-only date exactly.
- Replayed all six unit tests and all seventeen verifier/cross-check programs
  before regenerating the deterministic source archive.  The current PDF
  SHA-256 is
  `ec8c09fbc4ef5f382272351f69721b6544c69f5d48bee961447e1907de2c0180`,
  and the 73-member source archive SHA-256 is
  `7220a09d7eb31fdd81c42b35cbeb680f8c1b257df3b3002d37146b00d81e588e`.
  A second PDF build and second archive generation were byte-identical.
- Best-guess completion: 85% of the submission-layout refresh.  A refreshed
  source commit, R4 referee-package replay, Drive sync, and final push remain.
