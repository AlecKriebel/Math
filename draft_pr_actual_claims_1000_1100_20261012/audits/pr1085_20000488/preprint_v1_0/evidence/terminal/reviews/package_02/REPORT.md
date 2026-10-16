# PR #1085: new complete whole-package adversarial review 02

## Verdict

**ZERO actionable P0–P3 findings in the unchanged current preprint and support kit.** I independently accept the mathematical statements at their exact stated scopes, the credited-prior-theorem framing, the source/version qualifications, the seven-page PDF, bibliographic metadata, and the tested package interfaces. This is a complete new review, not a review limited to findings from the first whole-package review.

This verdict is an AI-assisted, unrefereed adversarial assessment. It is not human peer review, a formal proof certificate, a worldwide priority census, a claim of novelty, or authorization to disregard the ascending publication hold. Root adoption and terminal administrative sealing remain separate. The canonical prepared-stage STATUS still has readiness false and zero new whole reviews, and that dated stage was deliberately preserved rather than rewritten by this reviewer.

## Candidate, custody, and independence

The exact PR head is `5e23f0c801d23976830657d2eef2b32bdc7da05a`, problem 20000488. I independently read all six original files and authenticated every actual Git body against the submitted snapshot and recorded size/SHA256. No original executable exists, and I do not represent any new checker as an original-program replay.

Before consulting historical verdicts or derivations, I read the current complete `paper.tex` and the complete original mathematical report, derived the form-domain, essential-spectrum, nongraph binding, graph lower-bound, bounded-transform/Fourier and exact-example arguments, and froze that reasoning in `INDEPENDENT_DERIVATION_BEFORE_LABELS.md`. The task itself identified mathematical claims and source names, so this was not a claim of bibliographic blindness. The independent derivation predates my subsequent reading of the earlier priority report and original audit labels. It includes every theorem in the current paper and the additional sufficient-capacity test retained in the submitted report.

`INPUT_PINS.json` freezes 341 pre-existing regular files selected from the audit tree, without copying them. Full source bodies and complete preparation history are independently covered by the 192-file preparation-input stage and source-body ledger. My terminal verification found no alteration in any of those 341 selected inputs, any of the 192 preparation inputs, or any of the 110 current prepared outputs. All six original Git bodies match exactly. The 66 exact historical copies plus 126 individually justified exclusions form a disjoint complete partition of all 192 preparation inputs. Every copied body also equals its original local source. These are independently rehashed checks, not acceptance of a green manifest alone.

Only this review's own folder was written. The canonical manuscript, PDF, package, external descriptors and earlier histories were preserved. I used one disposable clean extraction, removed automatically on completion. My seven new render images were individually hashed after actual viewing and then deleted to conserve disk; their receipt preserves their identities. I did not delete prior renders, source bodies or another worker's files. No Git branch/index mutation, commit, push, PR mutation, upload, spreadsheet action, external communication or sibling-agent contact was performed. Messages went only to the assigning parent.

## Exact mathematical scope verified

The attractive form is integral of squared gradient minus beta times boundary trace squared on H1, with beta>0, outward derivative beta u, and threshold -beta². A smooth compact perturbation is connected, smooth, nontrivial and equal to the half-space off a bounded region. Its boundary may have overhangs or compact extra components. The graph claim uses compact W1,infinity functions.

The verified results are:

1. Essential spectrum is exactly [-beta²,infinity) for the stated smooth compact perturbations and compact Lipschitz graphs.
2. Every nontrivial connected smooth compact perturbation in ambient dimensions two or three binds below threshold for every positive beta, including the stated topology.
3. Every fixed compact Lipschitz graph in ambient dimension at least four has no below-threshold spectrum at sufficiently weak positive beta, with the interval depending on the graph.
4. The nonzero smooth graph f=h/100, h=exp[-1/(1-|x|²)] on the unit ball and zero outside, in R4 at beta=1 has spectrum [-1,infinity).
5. For each separately prescribed positive beta, a sufficiently small nonzero epsilon h provides another example, allowed to depend on beta.

Neither spectral-set equality nor this review excludes embedded eigenvalues. There is no all-strength absence theorem for one fixed nonzero graph, no arbitrary high-dimensional nongraph classification, no unintended dimension restriction imported into the original target, and no firstness assertion.

### Forms and essential spectrum

The trace argument is valid with a finite local chart cover of the changed compact boundary and the flat trace inequality elsewhere. The shifted form norm controls H1; compact-support core density is justified in the smooth setting and by global bi-Lipschitz flattening in the Lipschitz graph setting. Trial functions need not satisfy operator boundary conditions.

The IMS exterior localization vanishes near every altered part and extends to H1 on the flat half-space. The compact remainder gives a local-L2 error, not an unsupported comparison of operator domains. An essential operator Weyl sequence below threshold has bounded H1 norm; local Rellich makes its compact-region mass vanish and contradicts the localized form lower bound.

Conversely, tangential wave packets with their entire vertical supports in untouched flat fibers satisfy the Robin condition and have operator-domain membership by integration by parts against every H1 test. This does not require a global H2 characterization. Their residuals vanish as R^-1 and R^-2, including the k=0 threshold case. Thus every energy in the full stated essential interval is obtained. This proves the discreteness conclusion below the threshold used by min–max.

### Normal defect, topology and low dimensions

I rederived the ground-state identity using phi=exp(-beta y), including the sign of its outward derivative and complex cross terms. Its boundary defect is (1+nu_y), nonnegative on every component. Strict positivity follows because zero defect forces every boundary normal downward and hence each connected component to be an entire horizontal plane. Compact agreement permits only y=0, which together with the smooth one-sided boundary condition and connectedness forces the unchanged half-space. Compact obstacles therefore cannot disappear from the sign argument, and overhangs create no graph assumption.

The physical trial phi psi(x) is H1 because the actual domain is bounded below and the upper tail decays exponentially. Vertical truncations have vanishing error for each tangential cutoff. Its derivative lies only on truly flat full vertical fibers. The energies are exactly 2/L for the two one-dimensional tapers and 2pi/log(R/R0) for the logarithmic annulus. They tend to zero while the boundary defect stays strictly positive. This yields a negative actual-domain form value at each fixed beta and therefore a discrete eigenvalue. The auxiliary mixed-boundary null sequence is checked on this same domain, rather than transferred by analogy from flat criticality.

The original graph capacity test is sufficient, not necessary. Its strict inequality provides a negative test function because the gradient support lies outside supp f, so its exponential weight is exactly one. Failure of that sufficient condition is not used as evidence of absence.

### All-form graph stability and exact example

I checked the weak chain rule under flattening, unit volume Jacobian, full Robin surface Jacobian, fiber endpoint and both exponential weight directions. The shear coercivity is valid for complex vectors and arbitrary slopes with the deliberately coarse positive constant c=1/[2(1+G²)]. The regularized Hardy square has the stated additional nonnegative a0 m delta² term. Its dimension restriction m>=3 is essential. Weighted vertical integration has the correct sign and coefficient, yielding T_K<=(2beta A+sqrt A)E.

The all-function extension starts on a dense compact-support core where the exponential and inverse are locally bounded. Once Q>=0 there, form continuity extends it to every H1 function. The proof never assumes the growing exp(beta y) preserves global ordinary H1. The small-beta criterion therefore controls all admissible functions, rather than a separable ansatz. The f=0 case and the fixed-graph/fixed-strength quantifiers are explicitly consistent.

I independently verified smooth extension of h across the sphere, nonzero value, slope bound, diffeomorphisms and bounded symmetric difference. The exact Hardy certificate is c>1250/2501 versus defect<1/480, giving rational margin 597499/1200480. The alternate source-count certificate is N<1/240. These analytic inequalities, together with the established essential interval, prove the spectral-set equality; there is no numerical PDE or discretized spectral inference.

### Complete prior-theorem implication

The bounded map U=exp(beta f)u(flat) is a genuine invertible H1 map. Its exact energy identity is the stated graph expression with b=U_t+beta U, including the same boundary area defect. The comparison coefficients a_beta and v_beta follow with correct exponential signs. Completing each Fourier fiber gives the nonnegative square plus (sqrt(|p|²+beta²)-beta) times the boundary trace squared. The trace lies in H1/2.

A bounded compact-support potential is relatively form small, and its square-root multiplier is compact from H1/2 to L2 by local Rellich. Hence its essential spectrum remains [0,infinity), so a negative-eigenvalue count below one really excludes all negative spectrum. The published source uses boundary dimension m as spatial dimension, and Robin strength beta as source mass. At theta=1/4 its coefficient is 1/4. Both potential factors scale with beta^(m/2), giving beta^m, as required. These checks complete the earlier-theorem corollary and do not silently use an effective-operator heuristic or the inapplicable older theta formula.

## Actual source and priority framing audit

`SOURCE_INTERFACE_DERIVATIONS.md` gives the full source-by-source mapping. `SOURCE_READ_LEDGER.json` records ten actual primary bodies, exact identities and bounded read scopes. I used existing ignored bodies in place to avoid unnecessary disk duplication and freshly opened the decisive publisher/arXiv sources with the web tool. I directly re-fetched AIM successfully over HTTP and read the entire visible Robin section. Its current body matches the recorded exact bytes and imposes no global ambient restriction on Problem 1.4. This proves the literal counterexample scope, not intended unstated dimension or worldwide current openness.

Exner–Minakov's Section 5 already proves planar binding and uses exactly the physical exponential/Stokes normal-defect mechanism. Both receive prominent credit. The actual publisher HHRV Theorem A.6 on printed page 817, independently viewed, permits theta<1/2 and denominator (1-2theta)²; the older arXiv v2 uses theta<1/4 and (1-4theta)². The paper clearly distinguishes those versions and uses the publisher formula correctly. Its complete geometric/Fourier bridge makes graph absence and the explicit example substantive credited corollaries.

The Frank–Laptev form-compactness hypothesis does not include a nondecaying constant attractive baseline; the paper credits the mechanism and derives the required shifted identity instead of misapplying its theorem. Pinchover–Versano's ground-state and null-sequence framework is credited without treating its fixed-boundary potential remark as a domain-perturbation theorem. Pankrashkin–Popoff's strong-coupling result is compatible with weak-coupling absence. The 2017 delta/Robin passages are expectations with a different amplitude parameter, and the form-domain order does not permit delta absence to imply selected-side Robin absence. The full BSZ positive-magnetic-field, large-beta assumptions exclude zero field; only applicability, not its entire correctness, is claimed audited.

After my independent proof freeze I read the full earlier extensive priority report and checked its decisive interfaces against the primary bodies. I did not claim to rerun all 72 historic queries or to audit all 22 bodies completely. The current title, abstract, theorem commentary, README, STATUS, source metadata, exact upload metadata and proposed PR framing consistently identify credited exposition and prior-theorem corollaries. Exact remaining geometric priority, novelty, worldwide open status and independent discovery stay UNKNOWN. Unread sources and access failures remain limits. Historical original files with narrower attribution are preserved verbatim and expressly superseded by the new edition; they are not silently rewritten into a false past audit.

## Fresh exact controls and semantic mutations

`check_independent_forms.py` is newly written for this review and is separate from all shipped and historical checkers. Its new rational controls total 1,083: 500 complex-shear cases, 48 regularized-Hardy divergence-square cases, 450 polynomial-times-exponential Fourier-fiber completions, 45 weighted polynomial vertical endpoint identities, 36 mass-scaling cases and four exact normal/area cases. It independently recomputes both strict example margins.

The polynomial fibers differ materially from the old finite exponential-mixture checker. They use exact integrals of polynomial products against decaying exponentials, including nontrivial real and imaginary components, and compare direct shifted energy with the completed square. Seven semantic mutations independently fail in both normal and optimized Python: Fourier trace-sign reversal, wrong mass exponent, normal-sign reversal, lost area factor, old-preprint theta substitution, m=2 Hardy use, and flat endpoint-sign reversal. New normal and optimized full result JSON objects agree exactly. Explicit exceptions enforce the controls under -O.

These checks test selected algebra and incorrect variants. They do not replace the universal analytic proof, prove the external source theorem, test compactness by finite sampling, or constitute formal proof-assistant verification.

## Entire support kit, metadata and writer interfaces

I read all six current Python modules/entry points, including their guards and metadata constants, rather than trusting their tests. The declared 90 payload members plus one self-hash-excluded manifest make 91 sorted ZIP members. I independently read every member, checked CRC, complete equality with current source bytes, timestamps, regular-file modes, compression type, flags and absence of archive/member comments or extras. I reconstructed the ZIP independently and compared its buffer only after the writer was closed. It is byte-identical to the canonical archive.

The archive is 348,815 bytes, SHA256 `e297c94c2f71f74d55e77d29d6af850125c52e346652af2672b2671492afd52b`. The PDF is 97,501 bytes, SHA256 `464de043ac6b723f3bd5c03dddb6efd1c0bfeb05b5209bb532006580b7aedc2d`. No third-party full body or nested archive is included. The copy/exclusion partition is complete and individual, and historical path identities are retained rather than interpreted as a promise that private source bodies ship in the ZIP.

I parsed and compared exact metadata in the bare .zenodo object, wrapper, native repository manifest, hash binding and independent literal expected object. All are equal. The native uploader manifest selects the actual PDF and ZIP. The actual repository `zenodo.py check` succeeds locally and reports the exact attachment identities above; no remote deposit is created by this check. Metadata accurately identifies Alec Kriebel/ORCID, preprint version/date, CC BY4.0, extensive AI use, unrefereed status and the qualified credited result. Its preparation-only sentence is dated; it makes no service-completion or human-refereeing claim.

`reproduce_and_attack.py` ran 88 commands on one fresh extraction or this review's own checker, in both normal and optimized modes. Fourteen positive runs passed; 74 expected failures were rejected. Every documented standard-library reproduction command passed, the optional absent external binding was reported false, and the present required native binding was verified true. Removing required descriptors failed as intended. Both archive builds matched the canonical ZIP, and both real Tectonic builds matched the canonical PDF exactly.

Fresh package attacks checked default bootstrap manifest and member-list identical symlinks before parsing; duplicate JSON keys; shipped mathematical mutations; direct protected hardlinks from archive, checker and verifier writers; external descriptor hardlinks; existing output symlinks; symlink ancestors; preserved pre-authoring source aliases in a disposable audit layout; and all four compiler output children, including its source, PDF, log and receipt. The compiler attacks left the pre-existing output child alone and created no new outputs. Every tested alias target retained its original bytes. The entire clean kit matched its before-state after each interpreter-mode run. Guard inspection supports the stated static-file scope, with no concurrent hostile-race guarantee asserted.

## Compilation, visual review, and remaining gate

The built-in compiler first reported another compilation busy, then returned success on the second attempt. Its success is recorded separately and does not imply exported PDF bytes. Two actual clean Tectonic runs separately produced byte-identical canonical PDFs and zero overfull boxes under the installed engine/bundle. Exact identity across unspecified different engines is not promised.

I freshly rendered the current canonical PDF at 100 dpi and actually viewed all seven pages. Text, formulas, theorem scope, proof transitions, credits, limitations and references are legible. No clipping, overlap, corrupted glyphs, broken equations, misleading figure, layout defect or incorrect page numbering was found. Render hashes and the canonical PDF hash are recorded before deleting only my own images.

There are no P0, P1, P2 or P3 changes requested. This second complete review supplies a fresh clean result to the parent. The parent must still read and adopt this entire report and independent/source derivations, verify the seals, and perform the current administrative readiness/sealing step without recasting dated prior-stage records. The preceding PR #1032 priority hold continues to govern services. No publication, DOI row or PR merge has been performed or inferred by this review.

Review completion estimate: 100% for this assigned new whole-package adversarial review, with root adoption and program publication workflow outside this review's scope.
