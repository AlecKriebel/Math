# Research log: exceptional \(d=4\) Hecke Yang--Baxter operator

All times are America/Los_Angeles (PDT, UTC-07:00).

## 2026-07-27

- **19:33:15** -- Opened an independent audit of the proposed \(16\times16\)
  witness for the exceptional class
  \([e^{i\pi/3},\tfrac12,4]\).
- Initially preserved the supplied verifier under `verify_supplied.py`. In
  version 1.1.1 the byte-for-byte file was renamed
  `verify_supplied_original.py`, while `verify_supplied.py` became the hardened
  supported adaptation. The original checks the final witness but is not
  evidence about how the witness was discovered.
- Audit scope fixed before publication: exact matrix and tensor-word checks;
  tensor ordering; Hecke normalization; spectrum and partial traces; the
  Markov-trace/localization claim; amplification to larger dimensions;
  minimum local dimension; generalized-Yang--Baxter interpretations; and a
  primary-source priority search.
- Independent-research rule recorded: no author, expert, or other outside
  individual will be contacted.  Potentially useful outside review will be
  listed as a limitation only.
- Repository state: work is being carried out on `main` in a dedicated folder.
  Unrelated untracked files from parallel research programs are excluded from
  every stage and commit.
- **19:42:53** -- Core verification checkpoint completed.
  - The supplied SymPy verifier passed using SymPy 1.14.0.
  - A new standard-library checker independently implemented exact arithmetic
    in \(\mathbb Q(\sqrt2,\sqrt3,i)\).  It directly checked the \(16\times16\)
    Hecke and unitarity identities, the \(64\times64\) Yang--Baxter equation,
    both partial traces of the spectral projection, and the \(32\times32\)
    \((3,2)\)-generalized Yang--Baxter equation after the required coordinate
    permutation.
  - A second new checker worked only in the abstract tensor-word algebra.  It
    found exactly 18 words in the generic cubic residual and matched every
    rational polynomial coefficient against a hard-coded certificate.
  - The involution circle \(H(\alpha,\beta)^2=I\) is exact.  On that circle all
    18 residual coefficients vanish exactly when
    \(\beta^2=1/3\), hence \(\alpha^2=2/3\).
  - Both unnormalized partial traces of
    \(P=(I-H)/2\) equal \(2I_4\).  This supplies the Markov parameter
    \(\eta=1/2\) needed for the full localization argument, rather than merely
    the two-site spectrum.
- Corrected the provenance copy of the supplied verifier to be byte-for-byte
  identical to the download.  SHA-256:
  `df5ccbc8807c20a2f782762681100e3ad06cb95a750b7e052839584006fe3677`.
- **19:56:20** -- First complete nine-page manuscript compiled successfully.
  The paper turns the five terms into two anticommuting reflections, prints
  the entire 18-word generic cubic certificate, proves the partial-trace
  Markov property and faithfulness on \(H_n(3,6)\), proves minimal local
  dimension four, and gives the correctly reordered \((3,2)\)-generalized
  active form.
- **20:00:04** -- All three release verification routes passed in one run.
  The dependency-free direct checker and abstract word checker are independent
  of the preserved SymPy attachment.  The successful output was frozen in
  `verification_output.txt`.
- **20:01:12** -- Focused priority audit checkpoint completed.
  - Galindo--Hong--Rowell (advance publication 14 February 2012) supplied the
    broad open localization question, the two-dimensional nonexistence result,
    and the quaternionic \((3,1)\)-generalized operator, but no ordinary
    four-dimensional operator.
  - Lechner v1 (20 March 2026, 17:34:47 UTC) explicitly left
    \([e^{i\pi/3},1/2,2m]\) unresolved and identified the two-dimensional
    member as empty.
  - Searches of primary sources, scholarly indexes, general web results,
    public code, exact Pauli-word pairs, and the preprint identifier found no
    earlier ordinary representative of the four-dimensional class.
  - The approved conclusion is “appears new”; absolute priority, uniqueness,
    and inequivalence to the older quaternionic tower are not claimed.
  - No external contact occurred.  Comparison with unpublished expert notes
    is recorded only as a limitation.
- **20:13:12** -- Independent adversarial audits closed.
  - A separate Pauli-word implementation reproduced the involution and cubic
    identities exactly and confirmed the tensor ordering.
  - The partial-trace argument was audited against the precise localization
    definition: the pulled-back normalized matrix trace is the
    \(\eta=1/2\) Markov trace, and its trace-form radical equals the matrix
    kernel by positivity.
  - The dimension-three minimality step was strengthened.  A
    Temperley--Lieb candidate kills
    \(T=P_1P_2P_1-P_1/3\), whereas the exceptional trace gives
    \(\operatorname{tr}(T^*T)=1/18\); the complementary case is analogous.
  - The earlier speculative retraction of the \((3,2)\) interpretation was
    rejected.  After swapping the two qubits in every ququart, the active
    order is \(a_i,b_{i+1},a_{i+1}\), one global qubit is a spectator, and
    the standard \((3,2)\) equation holds exactly.  The global conjugacy also
    makes the generalized localization faithful.
  - GHR Example 3.14 is a prior \((3,2)\) operator, so that label alone is
    not novel.  Its projective eigenvalue ratio is \(i\); the present active
    operator has ratio \(-e^{i\pi/3}\), excluding unitary conjugacy up to
    phase.  No equivalence with GHR's category-specific \((3,1)\) tower is
    claimed.
- **20:16:22** -- The reviewed paper, three exact verification routes,
  priority audit, source package, and GitHub Pages files entered `main` in
  commit `f81879a1547f779dc29d7bf094e503c7641c9801`.
- **20:17:09** -- GitHub Pages reported that exact commit built successfully.
  The live paper page and PDF were retrieved. The served PDF SHA-256 was
  `3295256c746f5f011f18af2eff8537de88b9a592a44dcd50989efb3a315174a9`,
  exactly matching both frozen repository copies.
- **20:50:36** -- Completed an independent audit of the post-publication
  revision proposals.
  - Accepted the explicit conjugate-linear \(*\)-structure, kernel formula,
    quotient-tower compatibility, direct dimension-three argument, formal
    sitewise-swap proposition, historical consequence, and
    index-\(4\)/standard-braided consequence.
  - The complementary Temperley--Lieb obstruction was independently checked
    and added to the dependency-free exact verifier; its squared \(L^2\)-norm
    with respect to the exceptional trace is also
    \(1/18\).
  - Corrected both unnumbered-display label defects.  The review mentioned
    only the cubic identity; the Markov display had the same defect.
  - Adopted human-only bibliographic authorship while retaining detailed AI
    provenance and the lack of specialist review in the disclosure.
  - Rejected a fabricated DOI, an unsupported cryptographic-signature claim,
    self-referential PDF commit/checksum metadata, and an outreach invitation.
    A normal annotated version tag and GitHub release are the appropriate
    archival step.
  - The complete decision record is `REVISION_AUDIT.md`.  No external contact
    occurred.
- **21:10:58** -- Published the version 1.1.0 archival release.
  - Annotated tag `exceptional-ybe-d4-v1.1.0` resolves to artifact commit
    `e2669c5b2f99338c79381dc42bdbc61ee8b963c3`.
  - The GitHub release contains the paper PDF, a curated source-and-verifier
    archive, and a checksum file.
  - The PDF asset has SHA-256
    `af4ff57c4b8c5cd37f47f8a6da880b4f93b9c22d6e2908a3ef1f6ebf5fb1d049`;
    the curated source archive has SHA-256
    `099995bdfd446169caab2e458e74b9808d0b02134708486bded4e3623459f45d`.
  - The release is public and non-draft. It is an ordinary annotated release,
    not a cryptographically signed release, and no DOI is claimed.
  - No external contact occurred.
- **21:12:37** -- GitHub Pages completed deployment of publication commit
  `c1dc7a02f91645e4edee059092a622c9eac7ac01`.
  - The live project index and paper page display version 1.1.0, the artifact
    commit, publication time, and PDF checksum.
  - Fresh downloads of the Pages PDF and GitHub release PDF both have
    SHA-256
    `af4ff57c4b8c5cd37f47f8a6da880b4f93b9c22d6e2908a3ef1f6ebf5fb1d049`,
    identical to the frozen repository copy.
  - A live browser rendering showed no horizontal overflow at desktop width.
    The complete ten-page PDF had already passed page-by-page visual review.

## 16 August 2026 — Submission-readiness hardening

- **10:03 PDT** -- Began a fresh line-by-line mathematical, reference,
  verifier, archive, Zenodo, arXiv, and journal audit from exact current
  `origin/main` commit `8fbf2c358eb4ac1e35ce20a0eb30dde42a458c60`.
- **10:20 PDT** -- Reconfirmed all three exact mathematical routes in the
  locked Python 3.14.6 / SymPy 1.14.0 / mpmath 1.3.0 environment. Independent
  dense checks also confirmed both partial traces, both obstruction norms,
  site swapping, generalized Yang--Baxter, and far commutativity. No
  scope-changing mathematical defect was found.
- **10:32 PDT** -- Reproduced two archival blockers: optimized Python could
  disable scientific assertions, and the package checksum file referred to a
  stale website hash and to website files absent from the curated archive.
- **10:45 PDT** -- Found that the active GitHub--Zenodo integration had placed
  seven unrelated monorepo releases under concept DOI
  `10.5281/zenodo.21753404`. Recorded a hard rule to disable that integration
  before future releases and to use a fresh manual upload/DOI family for this
  paper. No Zenodo state was changed.
- **10:52 PDT** -- Completed current official submission-policy checks.
  Journal of Algebra is the first target and applies Elsevier research-data
  Option C; JPAA is the sequential fallback. arXiv `math.QA` is the primary
  category, `math.RT` is a defensible cross-list, and `quant-ph` remains a
  moderator/endorsement-dependent attempt rather than a manuscript claim.
- **10:58 PDT** -- Completed the refreshed priority and bibliography audit
  through 16 August. No public collision or citation of Lechner's preprint was
  found; all bibliography records and pinpoint citations were validated. The
  only bibliographic correction was Wenzl's official “type A_n” title.
- **11:00 PDT** -- Hardened all supported verifiers, retained the original
  attachment byte for byte, added mutation and optimized-mode negative tests,
  made checksums package-local and path-safe, pinned the build environment,
  and added explicit licenses and complete Zenodo/arXiv/journal handoff
  metadata. The mathematical claims and scope were unchanged.
- **11:44 PDT** -- Closed the final adversarial manuscript and verifier audit.
  - The line-by-line proof audit found no gap, normalization error,
    convention error, unsupported theorem dependency, or scope-changing
    mathematical issue.
  - Every bibliography entry, DOI, title, version-sensitive locator, and
    substantive citation was rechecked against primary sources. A fresh
    priority search through this date found no public collision; the paper
    retains the deliberately limited “appears new” claim.
  - The verifiers now bind the positive phase (q=e^{+i\pi/3}), bind the
    printed four-qubit witness to the independently encoded active witness,
    and distinguish the two partial-trace legs on an asymmetric test matrix.
    Fourteen negative tests reject optimized execution, phase and coefficient
    drift, algebra mutations, unsafe checksum paths, and archive-boundary
    violations.
  - A clean Tectonic 0.16.9/default-bundle-v33 rebuild was byte reproducible.
    The 11-page PDF has SHA-256
    `946e2b6595a67ff2fc9148d54ed5fa07a5fc4d6744270622caf3c0cf548b2dc3`;
    both mirrors match, all fonts are embedded, all 12 external links are
    valid, and every page passed a fresh visual inspection.
  - Submission policy and provenance were re-audited for Zenodo, arXiv,
    Journal of Algebra, and JPAA. The handoff now reserves a fresh manual
    Zenodo DOI before publication and builds one consistent DOI-bearing
    manuscript edition. The author-supplied full postal address and phone
    remain an explicit journal-only human gate; neither was invented here.
- No outside individual was contacted, and no Zenodo, arXiv, or journal
  submission was initiated.

## 16 August 2026 — Version 1.1.2 frontier-review adjudication

- **14:05 PDT** -- Began an item-by-item audit of two additional
  frontier-model reviews. Every proposed mathematical edit was checked
  against the published Galindo--Hong--Rowell article, Lechner's immutable
  arXiv v1, the printed argument, and exact calculations. No incorrect theorem
  or scope-changing issue was found.
- **14:42 PDT** -- Completed the manuscript revision without changing the
  operator or theorem scope. The revision expands the trace-kernel and tower
  bridge, prints the dimension-three obstruction calculation, corrects
  categorical-dimension language, states the GHR conjectural consequence,
  and makes the generalized tower compatibility explicit.
- **15:10 PDT** -- Extended the dependency-free exact route with a literal
  transcription of GHR Equation (5.2), its normalized Hecke checks, the exact
  residual table \((0,48)\) versus \((24,0)\), far commutativity, and the
  six-dimensional three-strand image. Orientation-sensitive fingerprints and
  deliberate sign, block-order, and \(\zeta\)-orientation mutations bind the
  published transcription rather than merely its symmetry-invariant data.
- **15:25 PDT** -- Refreshed the same-day priority and reference audit. No
  public construction realizing the class or prior ordinary
  four-dimensional localization was found; the qualified “appears new” claim
  and the paper's stated limitations remain unchanged.
- **15:38 PDT** -- Rebuilt the final 12-page manuscript with Tectonic 0.16.9
  and default bundle v33. The build has no TeX warning, overfull box, or
  undefined-reference diagnostic. The PDF SHA-256 is
  `5be8c8b90410db7c22bdc29ef0f7c3ad74065cdc8cb310e61ee84ea2ae4159a6`.
  All three supported verification routes passed in the locked Python 3.14.6
  / SymPy 1.14.0 / mpmath 1.3.0 environment, and their frozen output has
  SHA-256
  `b24067217009d8fbee4e412ef5b02dd3c4923de8ac699a19900a97de5524f83f`.
- **15:42 PDT** -- All 18 adversarial failure-mode tests passed. They reject
  optimized execution, altered witness coefficients and phases, the three
  guarded GHR transcription drifts, algebra mutations, unsafe checksum
  paths, omitted current-release records, and archive-boundary violations.
- **15:44 PDT** -- Rendered and inspected all 12 final PDF pages. No clipped,
  overlapping, missing, or malformed content was found. All 30 used fonts are
  embedded; the PDF contains 12 external-link annotations to 11 unique
  targets; its title, author, date, page count, and other metadata are correct.
- **15:45 PDT** -- Built the deterministic version-1.1.2 Zenodo and arXiv
  artifacts from the package-local allowlist. Both outer checksum files
  verified. A clean extraction passed all 33 internal hashes and reproduced
  the frozen output of all three routes; the isolated one-file arXiv archive
  reproduced the final PDF byte for byte.
- No outside individual was contacted, and no Zenodo, arXiv, journal, or
  GitHub release action was initiated.

## 16 August 2026 — Version 1.1.3 correction audit

- **16:15 PDT** -- Began an item-by-item audit of a further model review.
  The three proposed required corrections and the optional presentation
  changes were checked against primary sources rather than accepted on
  authority.
- **16:30 PDT** -- Resolved all version-sensitive source locators.
  - Lechner's immutable v1 PDF confirms that the projection-form Hecke
    relation is Equation (3.1), not (3.2); the manuscript nevertheless now
    refers directly to its displayed relation.
  - Rowell--Wang arXiv v2 numbers the localization statement Conjecture 4.1,
    while the published CMP article numbers it Conjecture 3.1 on p. 601.
  - GHR arXiv v1 numbers the restatement Conjecture 1.4, while the published
    IMRN article cited by the manuscript numbers it Conjecture 1.5 on p. 695.
    The manuscript now uses the published locators and credits Rowell--Wang.
- **16:40 PDT** -- Rechecked the AI product terminology against current
  official OpenAI documentation. GPT-5.6 Sol remains the model; Pro and Ultra
  are modes, and the documentation expressly says not to use a separate Pro
  model slug. The disclosure was made parallel and unambiguous without
  adopting the review's inaccurate “GPT-5.6 Sol Pro” label.
- **16:53 PDT** -- Completed a fresh public-collision audit across arXiv,
  Crossref, DataCite, Zenodo, HAL, and GitHub. No independent candidate was
  found; Lechner remains at v1. The qualified “appears new” language and its
  limitations remain unchanged.
- **16:59 PDT** -- Rebuilt the corrected manuscript with Tectonic 0.16.9 and
  default bundle v33 under `SOURCE_DATE_EPOCH=1786923000`. The PDF remains 12
  pages and has SHA-256
  `66374c63fa4ddefb0c6a848187ca864922bc152f8a7485aeec32e31bb170b4c1`.
  The supported exact routes reproduced the unchanged frozen output. The
  promoted GHR convention remark, conjecture credit, Lechner wording, and AI
  declaration all passed visual inspection.
- **17:03 PDT** -- All 20 adversarial failure-mode tests passed. The expanded
  suite binds the current conjecture attribution, published-edition locators,
  AI terminology, version metadata, and archive epoch in addition to the
  mathematical mutations and packaging boundaries covered in version 1.1.2.
  All 35 package-local SHA-256 digests also verified.
- **17:05 PDT** -- Built the deterministic version-1.1.3 Zenodo and arXiv
  artifacts. A clean source-archive extraction reproduced the frozen output
  of all three supported routes and passed all 20 adversarial tests; repacking
  that extraction reproduced all five submission files byte for byte. The
  isolated one-file arXiv archive compiled to the final PDF byte for byte.
  Both outer checksum files verified, all PDF mirrors agree, and the 12-page
  PDF's fonts, links, metadata, and rendered pages passed the final inspection.
- **17:12 PDT** -- Completed independent final mathematical/reference,
  editorial/policy, and artifact/CI red-team passes. The mathematical and
  artifact audits returned GO. The editorial audit identified one remaining
  journal-facing bibliography improvement: arXiv's issued DOI for Lechner's
  preprint. It also recommended two nonblocking historical/status wording
  cleanups.
- **17:22 PDT** -- Added `10.48550/arXiv.2603.20158` while retaining the
  immutable version-1 URL, applied both status cleanups, and repeated the full
  freeze. The final 12-page PDF has SHA-256
  `0b73f54a80f45ae57186d04c6f68ae5a45912a41c2990c7ecec7afc13287bedb`;
  its final reference page is visually clean. All three supported routes
  reproduced the unchanged frozen output, all 20 adversarial tests passed,
  and all 35 package hashes and both outer manifests verified. A clean source
  extraction repeated those checks and reproduced all five submission files
  byte for byte; the isolated arXiv archive again compiled to the final PDF.
- No outside individual was contacted, and no Zenodo, arXiv, journal, DOI,
  GitHub release, or other submission action was initiated.

## 16 August 2026 — Reserved-DOI final production freeze

- **18:30 PDT** -- The human author supplied the version DOI
  `10.5281/zenodo.21971507`, reserved in a fresh manual Zenodo draft. Public
  DOI, DataCite, and Zenodo lookups remained unresolved, as expected before
  publication of a private draft. No automated process opened, edited,
  uploaded to, or published the draft.
- **18:36 PDT** -- Applied the three accepted editorial changes without
  altering the operator, theorem, proofs, or scope: made the abstract
  antecedent explicit, simplified the public title block to “Independent
  researcher” with email and ORCID, and moved the GHR convention remark to
  immediately after the proof it qualifies. A full postal address and phone
  remain a separate journal-only human gate.
- **18:40 PDT** -- Inserted the reserved version DOI in the manuscript,
  bibliography, citation metadata, project page, handoff files, and current
  release records. The OpenAI declaration was rechecked against official
  product guidance and retained: GPT-5.6 Sol is the model, with Pro and Ultra
  identified as the respective modes.
- **18:42 PDT** -- Rebuilt the manuscript with Tectonic 0.16.9 and default
  bundle v33 under `SOURCE_DATE_EPOCH=1786930200`. Concise but complete
  bibliography formatting keeps the paper at 12 pages. The PDF SHA-256 at this
  checkpoint was
  `9a18d2206987cdebf77b2a1efff4b1eb8b7688da25f5fddebf4db7ee36922f87`.
  All 12 rendered pages were inspected; the public author block, relocated
  remark, DOI availability statement, and seven references are clean, with no
  clipping, overlap, malformed glyphs, or layout warning.
- **18:45 PDT** -- All three supported verification routes reproduced the
  unchanged frozen output, and all 20 adversarial failure-mode tests passed,
  including the new DOI, title-block, abstract, remark-placement, epoch, and
  metadata bindings.
- **18:48 PDT** -- Regenerated the 35-file package manifest and all five
  deterministic submission files. Both outer checksum manifests verified. A
  clean source extraction passed every internal hash, reproduced the three
  supported routes and all 20 adversarial tests, and repacked byte identically
  under both Python 3.14.6 and Python 3.11. The isolated one-file arXiv archive
  compiled to the final PDF byte for byte.
- **18:51 PDT** -- Completed the final format audit. The CFF 1.2 metadata
  validates against the official schema; the HTML structured metadata parses;
  all 24 PDF fonts are embedded; and all 16 external-link annotations were
  inspected, including the reserved version DOI. The DOI remains intentionally
  unresolved until the human publishes the private Zenodo draft.
- **18:57 PDT** -- An independent final read-through caught a single page-flow
  defect: page 11 ended with the article “The.” A nonbreaking phrase and a
  shorter equivalent availability sentence now leave page 11 at a complete
  sentence and begin page 12 with “The version-specific Zenodo record.” The
  re-rendered pages are clean. The final PDF remains 12 pages and has SHA-256
  `af1255b7702f78e73ba9981ca29d2cdfffcb26e6aa093b7b5d0a2bcaebf03ec8`.
- **18:59 PDT** -- Repeated the complete freeze after that page-flow edit. A
  clean extraction again passed all 35 hashes, all three supported routes, and
  all 20 adversarial tests; Python 3.14.6 and 3.11 repacks were byte-identical;
  the isolated arXiv source again reproduced the final PDF; and all mirrors,
  archive boundaries, timestamps, modes, CRCs, and outer checksums agreed.
- No paper or archive was submitted or published, no GitHub release was
  created, no external integration was changed, and no outside individual was
  contacted during this final production freeze.

## 16 August 2026 — Final dependency and editorial freeze

- **21:44 PDT** -- Adjudicated the final four review proposals against the
  manuscript and primary sources. Lechner's immutable version-1 PDF confirms
  that Lemma 3.1 and Theorem 3.4 are both used only in the dimension-four
  minimality reduction. The original Wenzl article was inspected directly;
  printed page 373 confirms that Equation (3.2) is exactly the cited uniqueness
  statement for a Markov trace with prescribed parameter.
- **21:46 PDT** -- Applied three scope-preserving manuscript corrections: made
  the complete Lechner dependency explicit, recorded that the positive
  obstruction proves the constructed representation is not Temperley--Lieb,
  and corrected the section roadmap and the location of the four solutions on
  the reflection circle. The verified Wenzl pinpoint was retained. Regression
  bindings cover every accepted correction and the rejected old wording.
- **21:48 PDT** -- Rebuilt with Tectonic 0.16.9 and default bundle v33 under the
  unchanged release epoch. The paper remains 12 pages, with no TeX diagnostic
  or visual defect, and the final PDF SHA-256 is
  `0c7c115229995ac32e9237b00461507a203c0f4a3d86692815f02392d1f287ff`.
- **21:49 PDT** -- All three supported verification routes reproduced the
  unchanged frozen output and all 20 hostile failure-mode tests passed. The
  35-file internal manifest, three submission files, and both outer checksum
  manifests were regenerated for the DOI-bearing version-1.1.3 freeze.
- No theorem, operator, proof scope, priority claim, DOI metadata, version, or
  deterministic epoch changed. No archive was uploaded or published, no tag or
  GitHub release was created, and no outside individual was contacted.

## 18 August 2026 — Private concurrent-work revision

- **13:55 PDT** -- Began a private version-1.2.0 revision after receipt of
  Galindo--Rowell arXiv:2608.16865v1. The historical v1.1.0 tag, artifact
  commit, released files, and dedicated v1.1.3 Zenodo record were treated as
  read-only. No commit, push, release, submission, repository edit, or external
  communication was authorized.
- **14:20 PDT** -- Inspected the supplied arXiv source literally and encoded
  its Section 13 Pauli placements independently. Exact arithmetic over
  \(\mathbb Q(\sqrt2,\sqrt3,i)\) verified the intrinsic quaternionic
  factorization, the essential factor \(-i\), unitarity of the displayed
  four-dimensional matrix, and the local-unitary comparison after reversal of
  the two four-dimensional sites. Omitting the site reversal gives a nonzero
  exact residual.
- **14:35 PDT** -- Audited the public chronology and the historical v1.1.0
  source. The tagged July source already contains all ten recorded
  construction, localization, minimality, amplification, and generalized-form
  items. Public timestamps were normalized to UTC; reported earlier private
  circulation was explicitly separated from the public record and was not
  used to adjudicate private discovery priority.
- **15:15 PDT** -- Completed the manuscript and handoff revision. The paper
  now cites Galindo--Rowell prominently, distinguishes their 16-by-16 ordinary
  Family III operator from the older 8-by-8 GHR generalized operator, and
  states the opposite/site-reversal qualification explicitly. The cover
  letter and two human-gated communication drafts remain private and unsent.
- **15:43 PDT** -- Rebuilt with Tectonic 0.16.9 and default bundle v33 under
  `SOURCE_DATE_EPOCH=1787090400`. The final 15-page PDF has SHA-256
  `27b121f40ad16520413f31587b1a7dfa315d4f2bfd4cee0d787f75165b26b77e`.
  Every rendered page was inspected, and the TeX log has no warning,
  overfull box, unresolved reference, clipping, or collision. All four
  supported exact routes reproduced frozen output SHA-256
  `31642749ae1a5b68b23f80763d7c3e70c9b0bebc18099abab4cac014a44e9dc0`;
  the standalone concurrent transcript has SHA-256
  `69aec973c78bdc44e1a4fa4f11e4c467c715dd2ca83a90b7c7c2d898dffd15bc`.
  All 25 adversarial tests passed, including all five new comparison-specific
  mutations. The internal manifest and deterministic v1.2.0 Zenodo/arXiv
  artifacts were regenerated and verified from a clean extraction.
- No external state was changed and no outside individual was contacted. The
  new Zenodo version DOI remains a human-only post-review gate.

## 18 August 2026 — Final global braid-and-link strengthening

- **21:25 PDT** -- Began the closed strengthening pass specified by the human
  author. Rechecked the original matrix/localization/minimality baseline and
  audited the literal Galindo--Rowell, Rowell, Turaev, and
  Lickorish--Millett sources. No open-ended theorem search was undertaken.
- **21:35 PDT** -- Exact arithmetic verified the scalar enhancement, matrix
  skein identity, local order, low-link values, Pauli quarter-turn
  factorization, complete local Pauli normalization, and the tensor-reversal
  and Garside orientations at strand numbers three and four. The printed
  all-strand proof and the primary-source normalization crosswalks were then
  completed.
- **21:43 PDT** -- The five supported routes passed in the locked CPython
  3.14.6 / SymPy 1.14.0 / mpmath 1.3.0 environment. Their frozen transcript
  has SHA-256
  `5e97e82aa2716db6ef40ad1f7ef4a844ec10c2e12ecaab0d329fc9b3abf03519`;
  the standalone braid-and-link transcript has SHA-256
  `7e2dfd704df1100068bde7bdd03ce35a0ffa723a46a8aec6b6825af296190d40`.
- **21:51 PDT** -- All 31 adversarial tests passed in 144.333 seconds after a
  first run was interrupted solely by exhaustion of the operating system's
  temporary-disk space. The successful rerun rejected every optimized or
  deliberately mutated route. The final 19-page manuscript PDF has SHA-256
  `769187195ebc53bae1b75af63e0aa1608ba32b581d13f30c275246dfb4336f5f`.
- The exact branched-cover formula was retained only after all five source
  gates passed. No finite image group was named, no necessity of site reversal
  was claimed, and no classical topological result was presented as new.
- No commit, push, release, deposit, DOI reservation, submission, email, or
  other external write occurred. Historical releases and the v1.1.3 Zenodo
  record were not modified.

## 19 August 2026 — Section 9 attribution and frame-clarity hardening

- **05:45 PDT** -- Began the final targeted pass. No theorem search or proof
  compression was undertaken. The abstract, Theorem 1.3, and Section 9 were
  separated explicitly into direct matrix consequences, the all-strand
  comparison, transported Family III results, and classical topological
  evaluations.
- **05:52 PDT** -- Independent exact arithmetic verified
  \(R(XIII)R^\dagger\) as the printed eight-term Pauli sum. A one-sign mutation
  has Frobenius norm squared eight and is rejected. Literal five-word
  three-strand calculations give \(-4\) for the figure-eight closure and \(2\)
  for the Borromean closure.
- **06:05 PDT** -- The five-route clean run passed in the locked CPython
  3.14.6 / SymPy 1.14.0 / mpmath 1.3.0 environment. Its frozen transcript has
  SHA-256
  `108233f563373cc2b3e3e9fb4012f7f8ea52fb1149f58c2f6795344bfc5f3064`;
  the standalone braid-and-link transcript has SHA-256
  `9081354712384deef6043ad15c2d6f28f8a4b7988148fc1d246a77b02ae0042a`.
- **06:18 PDT** -- Full-page visual inspection caught and repaired the literal
  TeX typo `qquad` in the Lickorish--Millett display. The rebuilt 20-page PDF
  has SHA-256
  `d50c1c3583dd9d8270c09ec2b99223bf0b74ad67254c8739d03597fc652ce691`;
  all rendered pages are clean and the TeX log has no unresolved references or
  overfull boxes.
- The final freeze gate ran and passed all 32 adversarial tests against the
  refreshed package manifest and deterministically reconstructed both
  archives. No
  historical release, DOI record, repository branch, website, submission, or
  communication is modified externally.

## 19 August 2026 — Reserved v1.2.0 DOI insertion

- **06:55 PDT** -- The human author supplied the reserved version DOI
  `10.5281/zenodo.22013710`. Inserted it in the manuscript, bibliography,
  package citation metadata, Zenodo/arXiv/journal handoff, and prepared website
  metadata. No theorem, proof, verifier, historical release, or external
  record was changed.
- Rebuilt the DOI-bearing PDF and deterministic submission artifacts, refreshed
  all dependent hashes, and prepared exactly the PDF, source ZIP, and matching
  `SHA256SUMS` for human upload. The DOI-bearing 20-page PDF has SHA-256
  `6f1b74c294932ccd3fa7ddfc4e75775e1e6bffffe423962f884ba2ee97fc986f`.
  Zenodo publication remains human-only.

## 19 August 2026 — Final two-sentence attribution polish

- Tightened the abstract to state that the scalar enhancement together with
  the skein calculation identifies the HOMFLYPT specialization, and added the
  audited Galindo--Rowell Section 13 citation at its first Section 5 use.
- Retained the 18 August manuscript-version date and the existing AI wording:
  the former records the completed scholarly edition, while current official
  OpenAI model guidance treats Pro as a mode of the selected GPT-5.6 model.
  No theorem, proof, formula, verifier, or historical record changed. The
  rebuilt 20-page PDF has SHA-256
  `7ad5ebe720a55428c64b80c548b39ee0e796c89cc11b7170db6622d5f2692916`.

## 19 August 2026 — Public source-package curation

- Removed four private operational documents from the public source-archive
  allowlist while retaining them locally: the journal cover letter, submission
  checklist, arXiv metadata handoff, and Zenodo deposit handoff.
- Updated the manifest, README, license attribution title, and archive-boundary
  regression test. The verified 20-page manuscript PDF remained byte-for-byte
  unchanged; only the public source ZIP and matching outer checksum changed.

## 19 August 2026 — Final public-status and punctuation freeze

- Replaced the remaining current private/prepublication labels in the public
  README, manifest, and version-1.2.0 release notes with durable archival-release
  language. Historical private-staging statements remain unchanged as
  provenance.
- Corrected the sentence-ending punctuation in the complemented-projection
  argument of Section 6. No formula, claim, proof step, or verifier changed.
  The rebuilt 20-page PDF has SHA-256
  `a3bdfee715fb37e156b4d3e30a4d53818bf45f2f1fef6739874302ca2e343ba2`.

## 19 August 2026 — Durable chronology-status cleanup

- Replaced the final pre-deposit wording in the public chronology record with
  the version-1.2.0 archival DOI and removed the obsolete private-candidate
  closing paragraph from the release notes.
- Extended the public-status regression test to bind those corrections. The
  manuscript and PDF were not changed.

## 19 August 2026 — Final launch-date normalization

- Advanced the current version-1.2.0 manuscript, citation, release, website,
  and deposit dates to 19 August 2026 while preserving every historical July
  and 18 August chronology checkpoint.
- Advanced the deterministic build epoch to `1787176800` (19 August 2026,
  15:00 PDT) and the source-archive timestamp to the same local wall time.
  The rebuilt 20-page PDF has SHA-256
  `a769689a4b5b9c48bf675f79d3b80916a7821ad5a8db0b9ec246df460dffb8de`.
