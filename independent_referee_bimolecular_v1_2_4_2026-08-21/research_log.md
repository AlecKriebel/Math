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
