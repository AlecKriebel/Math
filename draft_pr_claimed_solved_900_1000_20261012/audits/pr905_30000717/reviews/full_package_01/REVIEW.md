# Independent full-package adversarial review 01: PR905 / 30000717

**Disposition: required citation repair before publication. The mathematical result and the supported reproduction workflow pass.** One required issue, R1 below, was found in frozen candidate revision 1. No mathematical counterexample, proof gap, packaging failure, or unsupported first-priority claim was found. This is a fresh AI-assisted review, not human or journal peer review.

Reviewed head: `330a544a53b9e3e01bb0ed70817a5f4a79cc6a0a`. The frozen paper, PDF, archive, metadata, and supporting publication files were independently hashed against `publication/PREPUBLICATION_FREEZE.json`. The final before/after check still matches every frozen file. This reviewer modified no frozen artifact, made no Git mutation, and contacted no outside individual.

## Required repair R1: distinguish Laurent's published chapter from its updated manuscripts

**Priority P2; source accuracy and checkable attribution, not a mathematical failure.** The current manuscript cites the tangency-infimum identity as Section 7.2.3, Lemma 7.21 of reference [5], whose bibliography names the 2009 Springer chapter, pages 157–270, and links only its DOI. The README explicitly calls the same locator “Laurent (2009)”; the deposit description does likewise. Its final reference says “author manuscript” but supplies neither a version date nor that manuscript's URL.

Fresh retrieval uncovered a version distinction missed in the earlier source/priority checks:

| Exact primary file | Version and pagination | What Lemma 7.21 says |
|---|---|---|
| [Author-hosted chapter with published pagination](https://homepages.cwi.nl/~monique/files/laurent-ima.pdf) | Title dated 8 May 2008; 114 PDF pages, printed 157–270 | Printed p.242, PDF page 86: constancy on irreducible components of the **gradient** variety. It is not the cited tangency-infimum lemma. |
| [Updated manuscript](https://homepages.cwi.nl/~monique/files/moment-ima-update.pdf) | Explicitly “Updated version: November 12, 2009”; 143 pages | Section 7.2.3, Lemma 7.21, pp.113–114: the tangency and truncated-tangency infimum identity. |
| [Later updated manuscript used in the packaged priority audit](https://homepages.cwi.nl/~monique/files/moment-ima-update-new.pdf) | Explicitly “Updated version: February 6, 2010”; 147 pages | Section 7.2.3, Lemma 7.21, pp.117–118: the cited tangency identity; Theorem 7.22 retains the truncation multiplier. |

The chapter's printed page range and the updated manuscript's lemma number cannot be blended into a single precise citation. The primary files and complete relevant pages were independently inspected; hashes and the repair's exact locations are in `evidence/source_metadata_checks.json`. Raw source PDFs, text, and renders remain ignored inspection material.

**Repair:** identify and link the updated manuscript actually used, with its explicit version date and manuscript locator. Keeping the original 2009 chapter DOI as bibliographic context is appropriate, provided the tangency locator is assigned to the updated version. Update `publication/note.tex:152` and its Laurent bibliography entry at lines 223–228, `publication/README.md:15–16`, and both the description and Laurent reference in `publication/zenodo-deposit.json`. The shipped sealed source/priority reviews use the later manuscript but label it under the 2009 bibliographic record; preserve their history and add a release-level qualification explaining this version distinction. Recompile, rebuild the archive, and freeze the corrected bytes for the next newly assigned sequential reviewer.

**Acceptance condition:** a reader following the cited version and URL must find the tangency lemma at the named location, and every current public summary must distinguish the updated manuscript from the original chapter. There are no optional requested repairs.

## Independently reconstructed mathematical result

The exact tested claim is: for the displayed classical Robinson sextic R, for either explicitly defined ideal J_R of tangency minors or K_R of separate off-diagonal products, and every real epsilon >= 0,

`R >= 0` and `R + epsilon is not a finite SOS of real polynomials modulo I_R(L)`.

Here I_R(L) is the full ideal of polynomials vanishing on the real zero set. The ordinary radical and original ideal are contained in it. Thus epsilon zero refutes the exact ordinary-radical condition; every positive epsilon separately refutes the original-ideal perturbation condition. These are two distinct quantifier checks. An attained minimum is included when an attainment assumption is removed.

I reconstructed the argument from the manuscript before consulting the favorable historical and fresh reports. The deductions are:

1. The symmetric squared-variable cubic has the stated Schur decomposition. Ordering its nonnegative arguments proves both terms nonnegative. This proves R >= 0; zero is attained.
2. R and its gradient vanish on each of the ten whole real zero lines. Every off-diagonal product and minor therefore vanishes there. On each coordinate axis the generators also vanish, while R(u,0,0) = u^6.
3. The six two-coordinate representatives leave the asserted four-dimensional cubic kernel. The four remaining sign characters kill it. Lower-degree injectivity follows by multiplication by a power of x in the integral domain. Exact ranks are 1,3,6,10 in degrees 0,1,2,3; the stated-order cubic determinant is -128.
4. Restricting a hypothetical certificate to a whole zero line gives a constant sum of real polynomial squares. Every individual restriction is bounded, hence constant. Comparing powers of the line parameter annihilates exactly the homogeneous components of degrees one, two, and three. Positive-epsilon constants are correctly retained.
5. On the additional axis, finite real leading-square coefficients cannot cancel. The degree-six left side forces every nonzero axis restriction to have degree at most three, regardless of its ambient degree. The already-annihilated components then force constant axis restrictions, a contradiction.

The maximum degree exists because the number of summands is finite. Empty sums and identically zero restrictions cannot supply the u^6 term; zero epsilon and arbitrarily small or large positive epsilon create no exception. No ambient SOS-degree bound, radicality, component classification, finite variety, fixed numerical epsilon, formal certification, or numerical infeasibility is assumed. For a negative real constant, evaluation at the origin immediately gives a contradiction, so the same argument also yields the separate elementary all-real-constant extension.

The scope is essential: complex or signed squares can cancel leading coefficients, infinite families require other definitions, and rational/localized or inequality-multiplier certificates are different cones. The manuscript does not claim those stronger exclusions. The actual gradient ideal contains R by Euler's identity, so the counterexample does not conflict with the gradient-ideal theorem.

The sphere-minimum argument is valid for every polynomial: a negative value at the origin is already on the minor variety; otherwise compact positive-radius sphere minimization gives a negative tangency point. It works without a global lower bound or global attainment, and in one variable the empty minor list gives the whole line. The literal-product Q diagnostic is also correct. Its Groebner basis is `x^2 - xy, y^2`; independently checked x^3 and y^2 belong to the product ideal. Its real zero set is the origin, Q is positive there and negative at the stated point, and the reciprocal path has the stated unattained infimum. This diagnostic remains explicitly separate from the minor equivalence.

**Strongest verified result:** the universal finite-real-SOS nonexistence modulo the full real vanishing ideal for both explicit ideals, hence both target certificate implications fail. **Exact mathematical gap:** none identified. The source-version repair changes attribution, not this proof.

## Fresh controls and meaningful falsification attempts

`independent_math.py` constructs R, all derivatives/generators, and evaluation matrices directly; it imports no submitted program, stored result, or candidate data. Its 67 explicit guards pass normally and under -O. The outputs agree after their timestamps are removed. These controls support the written universal deduction; they are not a universal SOS-search algorithm.

Beyond reusing recorded PASS outputs, this review checked:

- Removing each one of the ten cubic-evaluation directions gives rank nine and a checkable nonzero cubic vanishing on the remaining nine. This new sensitivity check prevents treating a deficient direction set as the full obstruction.
- A quartic in the evaluation kernel has a u^4 axis trace, corroborating the existing sharpness control: the proof cannot eliminate all positive homogeneous degrees. The separate axis degree argument is necessary.
- Complex-square cancellation and a signed-square identity explicitly invalidate overextensions beyond real SOS; the note keeps the proper cone.
- The genuinely SOS sextic x^6 admits exact certificates for zero, very small and very large positive, and irrational positive constants. Nonnegative sextic degree and an axis alone cannot justify the candidate's obstruction.
- Arbitrary constant shifts preserve derivatives; a negative scaling of R violates the nonnegativity hypothesis on the axis. The Q coordinate-power ideal controls independently supplement the real-branch argument.

`tool_attack.py` performed 24 controls: sixteen new outer-validator mutations across normal and optimized execution, four substantive central-coefficient mutations of the fresh independent checkers, the documented unauthenticated consistency positive control, and three shipped utility runs. All twenty rejection cases were rejected; no test was skipped. New filesystem/manifest cases include a Unix socket, nested FIFO, listed file replaced by a directory, noninteger byte count, path traversal, a same-size changed PDF, a rehashed manuscript with the trusted pin unchanged, and alteration of a nonanchor original script. Both fresh checkers reject changing the central Robinson coefficient from 3 to 4 under normal and optimized execution.

A self-rehashed changed manuscript passes consistency when no trusted external pin is supplied. This is the documented trust boundary, not an undisclosed authenticity guarantee. A trusted accepted manifest binds the code and manuscript. The full shipped supplemental runner independently reproduced its attacks, including the historical raw assertion-checker optimization false positives; the supported outer wrapper launches isolated children without optimization and is not vulnerable to that failure mode. Those historical limitations are correctly explained in the current README and reports.

## Archive, utilities, PDF, and metadata

The 185,574-byte ZIP has SHA256 `115849f0e818e7683dc4f6c504dd77b47cdae189958e81dc0fe1e8b87d9ca959`. It contains 83 payload files plus the manifest, all regular, unique, relative-path members. The manifest SHA256 matches the supplied trusted `4bf17667e368b032dce0f34de931de2860a79f73774015be556db11525b963b5`. Membership, every byte count/hash, root/archived manuscript and wrapper equality, and all thirty exact original files were independently checked. The source-free payload contains authored text, Python, JSON, and pinned requirements, with no source PDFs, page images, raw datasets, article corpora, or credentials.

Normal and -O supported `verify_package.py` runs pass from the extracted archive with both `--expected-manifest` and `--pdf`. The author/historical suites, sixty-one integrity mutations, and both fresh arithmetic suites replayed. Distributed bytes remained unchanged. The archive-layout `verify_review.py`, `seal_manifest.py`, and computational `replay_and_attack.py` all run successfully in separate disposable copies. No optional utility requires the original workspace or unshipped source asset. The historical original statements are explicitly preserved and superseded by current release claims.

The released four-page PDF has SHA256 `1f3394d8a4afd9a3cb0abf2f39fe0fba426b573066a8adabd0c957e612bd7b92`. All four complete pages were independently rendered and visually inspected: no clipped or overlapping text, missing glyphs, broken theorem layout, or incomplete references were found. Both the desktop standalone compiler and an independent Tectonic compilation succeeded. The standalone log has no overfull/underfull box warnings; extracted text from the rebuilt PDF exactly matches the release PDF. The source-version defect remains visible in the bibliography despite otherwise correct rendering.

The deposit file names and paths describe the actual PDF and ZIP. The creator, affiliation, exact ORCID, CC BY 4.0 license, open access, preprint/version/date, classical form/cubic-method credits, extensive AI use, unrefereed status, absence of independent human/journal review, and finite-computation limitations are consistent across the package. Apart from R1, the description accurately reflects the proof and artifact contents. Its 66-record citation graph really has 66 distinct work IDs and is explicitly a metadata screen, not a complete full-text literature audit.

## Independently checked formulation and priority limits

Fresh publisher-report retrieval and complete visual inspection of printed pp.798,810,811 confirm the classical Robinson formula, ordinary radical versus original ideal, every-positive-epsilon quantifier, removal of attainment, and the comma-separated product display. The exact-ID local catalogue/corpus record independently confirms explicit differences in the catalogue normalization. That normalization cannot be described as an authenticated author correction, and the note does not do so.

Fresh Reznick reprint inspection of printed pp.258–259 confirms the form, same ten directions, and classical cubic-evaluation obstruction. The submitted attribution is appropriate. The base of Q matches Schweighofer's equation (6). Fresh Guo–Safey El Din–Zhi text and the updated Laurent manuscript retain the truncation inequality/SOS multiplier and their neighboring assumptions. This review accepts no inference that the ideal-only counterexample refutes those positive theorems.

Historical first priority, exhaustive literature coverage, continued open status in 2026, author-approved correction of the printed products, complete inaccessible 2008/2009 Hà–Pham contents, and unread citation-graph texts remain unestablished. The note and deposit explicitly preserve those limits. None is being filled by search absence, metadata titles, or favorable earlier AI reviews. This reviewer performed primary-text checks relevant to accuracy, not an exhaustive independent new priority audit. The accurate modest negative-result scope is publishable after R1, without claiming newly discovered classical ingredients or a verified first resolution.

## Completion and evidence

Review completion: **100%** for this assigned full-package gate. Candidate readiness estimate: **90%**, with R1 as the sole required repair. No further mathematical work was found necessary, but the frozen revision is not accepted for publication until the citation-version repair and renewed sequential review.

Intentional evidence is sealed in this review folder's `MANIFEST.json`: independent arithmetic controls, normal/optimized archive replays, new tooling attacks and supplemental replay, source/metadata version evidence, catalogue hash checks, compile logs, final frozen-byte/PDF checks, scripts, and timestamped `RESEARCH_LOG.md`. Raw sources and temporary copies are ignored and are not public review artifacts.
