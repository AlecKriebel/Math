# Independent referee research log

## 2026-08-21 22:15 PDT — checkpoint 0: evidence freeze and blind protocol

- Goal: independently determine whether the theorem, proof, computational
  claims, and supporting package for manuscript version 1.2.4 are valid.
- Working hypothesis: undecided. The requested conclusion is treated as a
  hypothesis, not an assumption.
- Success criterion for a positive mathematical status: every necessary link
  in the twelve-item proof chain is affirmatively verified, including boundary
  cases, with no unresolved substantive gap; computational evidence must be
  accurately scoped and artifact claims independently reproduced.
- Falsification criteria: an exact counterexample or contradiction; a missing
  material implication; an unjustified limiting, stopping, or integrability
  step; a mismatch between manuscript and code; or an unreproduced artifact
  claim represented as verified.
- Information barrier: before three preliminary reports exist, do not open
  `audit/`, `preservation/`, `research_log.md`, `revision_log.md`,
  `expert_audit_note.md`, `supplement/reviewer_checklist.md`, any committed
  verification report, expected/golden output, or validation summary. File
  names and hashes may be inventoried without reading their contents.
- Packet root:
  `/Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4`
- Submission root:
  `/Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/bimolecular_positive_recurrence_submission_v1_2_4`
- Starting PDF:
  `bimolecular_positive_recurrence_submission_v1_2_4/manuscript/main_jap.pdf`
- Host: Apple arm64; macOS 26.5.2 (build 25F84); Darwin 25.5.0.
- Python: `python3` 3.14.6; `python` 3.9.6.
- Tectonic: 0.16.9.
- Poppler `pdfinfo`: 26.08.0.
- PDF SHA-256:
  `77b4f098a1f0655ed4e04423caccec79a051cf11297b17d5fa2d630d539e7c4d`.
- TeX source SHA-256:
  `00c0d9f2b281d6f36a388ff45776d9f90f9d6388dce0e83d9eb7b6aa80a4deba`.
- Bibliography SHA-256:
  `00bd5723e1c518841e94e8bd02637c709b0295891f191ed65dffbcc10a034e61`.
- Submission ZIP SHA-256:
  `66e1f89f97840650f400ae917ccb76ce5f08a9291a3a7692fe7bf2222d8af54f`.
- Copied packet ZIP SHA-256:
  `77f9a3641e19f702aeadf05e8ad0eb84fad46e2482d4cddf1c12d826fddb3522`.
- Deterministic SHA-256 of the sorted per-file hash listing for the unpacked
  packet (relative paths included):
  `65860b70007afc68d685eb242e1b9e119aa4e08040b0af341bc85f2a14723309`.
- The copied packet has no `.git` directory. The surrounding research checkout
  is on `main`, but that does not establish packet provenance. Its available
  matching tags stop at `bimolecular-positive-recurrence-v1.2.3`; no matching
  `v1.2.4` tag was present at evidence freeze. Thus content can be checked, but
  a claimed v1.2.4 Git-tag provenance is not presently available locally.
- Main PDF metadata: 16 US-letter pages, 156,340 bytes, PDF 1.5, unencrypted.
- Boundary probes queued: zero complex; self/parallel channels; equal
  displacements; coordinate faces; lattice/parity restrictions; repeated
  species; absent species; zero-weight divergent coordinates; zero-length
  target paths; extreme positive rate ratios; absorbing states; improper
  exceptional sets; explosion and physical-time return failures.
- Estimated completion: 2%.

## 2026-08-21 22:34 PDT — checkpoint 1: blind manuscript mathematics

- Read all 16 pages of `main_jap.pdf`; visually rendered all pages and found no
  clipping, overlap, missing glyphs, or unreadable references.
- Reconstructed the theorem and independently checked all twelve proof
  interfaces. The detailed blind assessment is in `main_math_preliminary.md`.
- Re-derived the motivating cycle, the Anderson–Cappelletti–Kim boundary
  example, and the rate-dependent exceptional-set example source by source.
- Tested zero complex, repeated species, lattice restriction, absorbing,
  absent-species, equal-displacement, zero-length-path, and extreme-rate
  branches. No exact counterexample was found.
- Strongest provisional result: the displayed analytic argument is internally
  complete, conditional only on later primary-source confirmation of the
  standard Markov/regenerative facts and on no contradiction emerging from
  independent tracks.
- Exact remaining gap: verifier static/runtime audit, independent mutations,
  artifact reproducibility, literature verification, and author-record
  comparison have not yet been performed.
- Estimated completion: 23%.

## 2026-08-21 22:35 PDT — checkpoint 2: blind static software audit

- Read all 1,846 mathematical/verifier module lines, all 868 test lines, and
  release/PDF/manifest/archive tooling without execution or golden-report
  access.
- Confirmed 57 verifier tests and four separate release-tool tests by static
  enumeration.
- The verifier genuinely regenerates canonical JSON twice. Fixed expected
  counts/digests are regression anchors around recomputation and certificate
  validation, not copied answers.
- The strongest exact finite evidence is the factorial/entropy algebra, lifted
  cycles, ACK episode cross-interface check, and 98,261-certificate top atlas.
- The universal compactification, exceptional-set, trace, CTMC, and
  regenerative implications remain analytic and are not implemented; package
  documentation accurately says so.
- No substantive code defect found. The unavailable v1.2.4 Git tag remains a
  concrete nonmathematical provenance discrepancy to verify remotely.
- Estimated completion: 39%.

## 2026-08-21 22:38 PDT — checkpoint 3: three-track blind assessment frozen

- All three separated preliminary reports now exist and their SHA-256 values
  are recorded in `provisional_independent_assessment.md`.
- Only after each report was written were their conclusions compared. The
  analytic, adversarial, software-static, and main-referee passes agree that
  all twelve mathematical obligations pass and no counterexample was found.
- The static software pass confirms genuine regeneration and accurately
  limited finite evidence; runtime behavior remains unverified at this point.
- Primary-source checks support the material prior-work comparisons, subject
  to the unavoidable limits of a time-bounded novelty search.
- Shared concrete defect: the manuscript's public v1.2.4-tag claim is false at
  review time; the exact remote ref is absent and both manuscript URLs return
  404. Content verification remains distinct from tag provenance.
- Frozen pre-author-record disposition: **CORE RESULT SOUND, REVISION
  REQUIRED**; provisional recommendation **minor revision**, contingent on
  canonical replay, mutations, artifact rebuild, and record comparison.
- Estimated completion: 52%.

## 2026-08-21 22:52 PDT — checkpoint 4: replay, mutations, and author records

- The exact packet command `./RUN_ALL_CHECKS.sh` exited 0 in 26.556 seconds.
  All 57 verifier tests and all four release-tool tests passed with no skips;
  both report regenerations, both 82-file manifests, all three report copies,
  all four PDF byte rebuilds, and the 84-member ZIP byte rebuild agreed.
- The canonical report SHA-256 is
  `dc14127494eaa6ccf3b36a91f5d714ba6f79e76476f8d199760bd3b5faeed586`;
  the manifest SHA-256 is
  `e8562cfb54fd411e4c1926bd2e15cf394a1ece014def06d3621e12a0fcce5caf`;
  the release ZIP SHA-256 is
  `66e1f89f97840650f400ae917ccb76ce5f08a9291a3a7692fe7bf2222d8af54f`.
- Production-free oracles completed 528,810 factorial, 1,153 entropy,
  40,537 lifted-cycle, 118,261 top-alternative, 5,800 episode, 700 stationary-
  cycle, and 37,587 scalar cases without failure. These remain finite
  falsification evidence, not proof.
- Golden-report, unlisted-Python, mathematical-source, manifest/content,
  PDF, and ZIP mutations all failed closed at the expected layer.
- A clean disposable Git repository with the exact package but no tag exposed
  a material provenance failure: `validation/replay_release.sh` printed
  `Exact tag: none`, completed every check, exited 0, and printed a Version
  1.2.4 PASS. The script never asserts the expected tag, contrary to the packet
  README. Together with the absent public tag, this makes v1.2.4 Git provenance
  unverified even though standalone content reproducibility passes.
- Post-barrier author records agree with the proof audit but are derivative,
  author-generated, AI-assisted inventories rather than independent evidence.
  They disclose no prior independent human expert review. Their research log
  also says public release sequencing remained pending, contradicting current
  present-tense release claims.
- Mathematical conclusion remains unchanged; final report drafting and the
  bounded literature sweep remain.
- Estimated completion: 88%.

## 2026-08-21 23:02 PDT — checkpoint 5: final referee report

- Completed the bounded primary-source literature pass. The ACK theorem and
  Section 6.1 dependency, Xu v2 nonexplosion/open-problem boundary,
  Pauleve--Craciun--Koeppl reachability terminology, deterministic
  boundedness/permanence results, and official two-species announcements all
  match the manuscript. No exact public overlap was found through the cutoff;
  absolute priority and the unpublished two-species proof remain unverified.
- Completed the final seven-part referee report with the exact theorem, all
  twelve proof obligations, severity-ranked findings, complete computational
  and artifact outcomes, author-record comparison, and residual uncertainty.
- Final report SHA-256:
  `ca859338d1e06cf1785e1377f72c1b5e8ec854b873dfb77eff50697185cc96b4`.
- Final mathematical status: **CORE RESULT SOUND, REVISION REQUIRED**.
- Journal recommendation: **minor revision**.
- Exact repair condition: publish and externally resolve the intended v1.2.4
  annotated tag and make the release replay fail on absent/wrong tags, or
  remove tagged-release claims and describe the packet as an untagged
  candidate. No mathematical repair is required.
- Estimated completion: 100%.
