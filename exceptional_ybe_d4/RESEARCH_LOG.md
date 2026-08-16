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
    and added to the dependency-free exact verifier; its trace norm is also
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
