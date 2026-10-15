# Independent final preprint and package review 02

**Decision: CLEAR. No mandatory repair or actionable concern was found within the stated claim and publication scope.**

PR 822 / problem 30001168 / OWR-3389-021. Review opened 2026-10-15 03:09 UTC; completed 2026-10-15 UTC after an interruption and fresh hash revalidation. Review completion estimate: **100%**. This is an independent adversarial AI review of the finite theorem, source attribution, complete four-page note and sealed R2 package, not external human peer review, formal verification, or a novelty certificate.

## Inputs, independence and permitted scope

The authorities were `PACKAGE_SEAL_R2.json` (10 core files), `LOCAL_PR_ASSEMBLY_R2.json`, and `PREPARED_PR_MAPPING_R2.json`. The assembly was `/Users/alec/Documents/Math/draft_pr_claimed_solved_800_900_20261012/work/pr822_revision_r2`. The original recorded head is `c9fd5a0462d1fa98f21aa7037f7a5e061fbbee9c`, exact queue status `claimed_solved`, original proof effort `1/5`. The current record's dated open label was treated as catalog history, not proof of current openness.

I independently reconstructed the theorem from the note and actual primary passages before consulting previous verdicts. `INDEPENDENT_RECONSTRUCTION.md` records that reconstruction and its falsification targets. The work was verification of the existing finite argument; no new central proof search was undertaken. All review-authored files, copied cases, raw tool outputs and renderings are inside `package_review_02/`, with temporary/raw material under `private_sources/` and note page renderings under `rendered/`. I made no Git, PR, release, service, sealed-input or original-file edit and initiated no external communication or retrieval.

The 10 core files, three authority files and all 163 assembly files match the opening hashes at final revalidation. `INPUT_HASHES.json`, `INPUT_HASHES_AFTER.json`, `HASH_COMPARISON.json` and `RESUME_HASH_REVALIDATION.json` contain exact individual before/after digests. The broad audit-folder comparison observed one research-log change and four new root audit artifacts during concurrent root work; these are explicitly listed in `HASH_COMPARISON.json`, outside the sealed core and assembly, and were not authored by this review. They do not alter this decision's inputs.

## Mathematical findings

**Exact target.** I read the original OWR text and visually inspected printed pages 421–422, item (16). The note uses the original smooth positive weight, integral of W^(n/2) against round volume, positive operator `Delta+n(n-2)/4`, both exterior powers `W^(-1/2)`, round L2 space, and maximum over all positive times. A finite admissible S3 counterexample refutes the universal assertion over n>=3. The note consistently leaves the n>=4 restriction and the adjacent monotonicity conjecture unaddressed. The already-known dimension-three initial increase is not substituted for the required maximum violation.

**Smooth finite construction.** The denominator defining chi is positive everywhere. Its flat endpoint jets give smooth transitions to the exact cylinder and sech caps. The absolute-value corner at the center is harmless because u is constant there. At either pole the displayed coefficient is a positive smooth function of squared Cartesian stereographic radius. The constant e^10000 is a finite real number; no numerical evaluation or limiting singular metric is needed. Each prescribed cap contributes less than 2 to the radial integral, so `4pi L <= V_L < 4pi(L+4)`. The fixed cap specification supplies this bound; an arbitrary A–J pointwise cap inequality would not suffice. The power `a=(2pi^2/V_L)^(2/3)` gives exactly the historical normalization.

**Operator and variational argument.** Conformal covariance has powers -5/4 and 1/4; the unitary multiplier has power 3/4 and conjugates to the exact round-L2 operator. Smooth compact positive multipliers preserve the required closed-form domain. The displayed `3/(4 max W)` lower bound proves a positive spectral gap without a transition scalar-curvature sign assumption. The cylinder scalar curvature is 2 and its Yamabe potential is +1/4. Zero-extended Dirichlet sine functions are in H1 because the function traces vanish; a jump of normal derivative does not obstruct H1. The diagonal form matrices give `lambda_k <= 1/4+(pi k/L)^2` for every full-spectrum index, with multiplicities. Finite heat sums and monotone limits then justify the trace lower bound. There is no fixed-index convergence-to-trace transfer or unproved cap-decoupling assumption.

**Normalization, time and strict lower gap.** The decreasing Gaussian integral gives `L/(4sqrt(pi))-1`. Constant metric rescaling requires `t_*=4a`; its prefactor is `8a^(3/2)=16pi^2/V_L`. The volume upper bound and positive numerator give the strict lower bound in the note. Independent rational calculation reproduces

`1106714561/1700054750 - 13/20 = 3357947/3400109500 > 0`.

**All positive round times.** The round multiplicity and potential are correct. Differentiated Gaussian Poisson summation has the printed factors and negative corrections on `(0,7/5]`. The first mode increases to 2, while every higher mode decreases after 2/5. The j>=3 ratio bound gives the factor 18 in D(a), hence each bound controls its whole interval, not a sample. The six adjacent intervals cover `[7/5,2]`; all modes decrease after 2. The small-time row and six interval rows were independently reconstructed, with exact rational exponential tails and integer square-root enclosures, in `independent_arithmetic.py`. Both interpreter modes passed. Every exact value lies strictly below its displayed rational enclosure; the largest displayed enclosure is `641202/10^6 < 321/500 < 13/20`.

**Literal maxima.** The normalized leading heat coefficient is `sqrt(pi)/4`. Positive-time continuity, the strict witness above that boundary value, and positive-gap exponential decay at infinity give an attained weighted maximum. The round first mode at 2 exceeds its zero-time limit; the sufficient inequality `128>pi e^3` was separately checked with certified constant bounds. Thus both literal maximum statements are justified.

No circularity, missing central estimate, hidden minimizer hypothesis, unsupported dimension transfer, wrong form-domain assumption or omitted time rescaling was found. This conclusion uses standard smooth elliptic spectral theory, conformal covariance, min–max, Poisson summation and heat asymptotics with the stated hypotheses; software arithmetic alone does not prove those analytic results.

## Primary sources, attribution and claim limits

`BINDINGS_AND_SOURCE_RECEIPT.json` records exact hashes and inspected locators for the actual OWR, Ammann–Jammes, Morpurgo and selected broader-theorem sources. I re-inspected the A–J author manuscript's construction in section 3.2, its introduction and fixed-index theorem, including visual inspection of printed pages 7–8. It materially supplies the classical cylindrical geometry and credits earlier Pinocchio work. The chosen fixed rescaled cap plus ordinary all-index longitudinal trial spaces and a strict elementary round bound assemble the qualitative negative answer. The current note and metadata explicitly credit that classical mechanism. They do not claim that A–J explicitly stated Morpurgo's exact refutation or that their fixed-index eigenvalue theorem alone proves it.

The chapter citation's title, DOI, year 2011 and pages 1–23 agree with retained bibliographic metadata. The note distinguishes the first arXiv submission in 2007 from the inspected author manuscript dated 8 December 2008 and does not claim final-version byte identity. The retrieved v1 text bears an early arXiv banner and a regenerated body date; those are not silently conflated.

I re-read the retained partial Morpurgo 2002 author-text capture at the transform definition, Theorem 4.1, Corollary 4.2 and Theorem 5.10. Its convex continuous transformed-trace class and integrability hypotheses do not directly provide a single-time point mass or nonlinear maximum comparison. No inverse-Mellin inference was assumed. Final Duke full text and several older versions remain unavailable in the stated audit. The unresolved regularized-zeta sign/version issue is preserved as a source limitation and is not used to prove the present theorem. Selected Sire–Xu, HPP and Frank counting statements were checked for normalization, dimension and implication direction; they do not supply an automatic transfer to the current target.

I independently verified the retained corpus's 74 source-file hashes, 26 PDF copies representing 25 distinct byte versions, and 107 overlapping recorded queries. These are retrieval and search-record counts, not a claim that all retrieved pages were read or that a worldwide census was completed. The bounded audit's non-detection is accurately framed. **Historical application priority, worldwide firstness, present openness and eligibility as a novel discovery remain unestablished.** No new geometric or spectral mechanism is claimed. These limits are explicit in the note, current-priority document, README and metadata and do not create a gap in the finite mathematical refutation.

## Package, replay and controls

Before execution I read all 17 unique Python-script versions represented by 29 paths, including child entry points; `SCRIPT_INSPECTION.json` records hashes and duplicate groups. There was no network or external-service behavior in the replay entry points. Receipt-writing tools were confined by the published wrapper to disposable copies. The priority receipt checker requires its excluded private source corpus and is explicitly an audit-time tool, not promised as a portable completeness check.

`BINDINGS_AND_SOURCE_RECEIPT.json` independently verifies the complete 163-file assembly/mapping; all 42 frozen original files; three original ZIPs with 32 safe, regular, exact corresponding members; and all 110 current ZIP members against the extracted package. Archive names, member types, uniqueness, path safety, byte identity and CRC checks pass. Only the authored note PDF occurs as a PDF in the current portable inventory. Downloaded primary works and private state are excluded. Current source/PDF and all publication metadata copies agree. Author ORCID `0009-0001-9320-500X`, CC BY 4.0, preprint status, extensive OpenAI use, and absence of completed external human or formal verification are accurately stated.

In a relocated layout with spaces, the following completed successfully in normal and `-O` modes:

1. Portable `verify_package.py PIN --full` from the extracted ZIP, with a foreign current directory.
2. Current outer `verify_publication.py OUTER_PIN --full` from the copied full assembly, also with a foreign current directory.
3. The published-folder builder command from `publication_20261013/preprint`, supplying `--from-package ../verification_package`, the trusted index and a fresh absolute output directory. Both builds reproduce the exact current index and ZIP. Literal `python3 -I -B` and `python3 -I -B -O` invocations also completed; their saved outputs and output hashes were recovered and revalidated after the interruption.

`REPLAY_RECEIPTS.json` records all full outputs and exact commands. `LITERAL_DOCUMENTED_COMMANDS.json` records the literal published builder commands. `REPLAY_INVENTORY_RECEIPT.json` records identical complete before/after inventories of the relocated 163-file and 110-file layouts. No completed required replay failed.

The repaired current root `package_controls.py OUTER_PIN` passed **22 cases: 2 intact acceptances and 20 expected rejections**, covering both child interpreter modes. The immutable historical harness remains separate and the full replay passed its original 20 cases. The original audit passed 34 controls, and the fresh semantic harness passed 16 expected semantic rejections plus two expected acceptances of wrong analytic prose after local rehashing. Those two deliberate acceptances correctly demonstrate that arithmetic and local artifact integrity cannot certify analytic prose. The external package pins still bind the actual reviewed prose.

`EXTRA_INTEGRITY_CONTROLS.json` adds 16 independent expected rejections across both modes: portable empty-directory, same-size corruption, symlink and wrong-pin cases, and builder wrong-pin, unbound-verifier, output-inside-input and nonempty-output cases. Each produced the expected diagnostic without altering its input/output files. The builder binds the trusted index and included verifier before executing it and rejects invalid output locations.

An optional redundant run of the current harness with an optimized *parent* interpreter was interrupted before a completion receipt and is not counted. Required normal-parent controls already exercise both child modes, and the complete normal/optimized full checks and builders had finished. No claim depends on the interrupted optional run. All required completed replays used only several megabytes of review storage and encountered no ENOSPC failure.

The material package pins, unchanged before and after review, are:

| Artifact | SHA-256 |
| --- | --- |
| Outer manifest, 163 files | `ab68f85b25ce12369da8eb0d818d10edb55b2d835d23ba098b99583a9ef83e9c` |
| Portable index, 110 total files | `b3ac480b710b4a2a6ac8fb438b09697357e0796fe879d614afb54429c10aa374` |
| Verification ZIP | `06cb9c3018eff4ab2e2654e56cee8f302672a8f05ffe4dce0b2d7c78c4fa1d0a` |
| Four-page PDF | `05ab26248c64b1e8dc7aa9c89e1eabd03142226dcefd32a622f78283af839de1` |

## Visual inspection and final disposition

I rendered the exact sealed PDF afresh at 120 dpi and inspected every page. `VISUAL_QA_RECEIPT.json` binds the PDF and four images. The title, theorem, complete cap/operator formulas, strict rational bounds, all seven table rows, maximum argument, references and disclosure are legible. No clipped text, missing glyphs, overlap, broken table or missing page was found. Page continuations preserve the argument. This was read-only PDF review, so no authoring marker applies.

The two known R1 usability defects are repaired in the actual published layout: the current root harness accepts the positional outer pin and runs 22 cases; the builder accepts the documented explicit package input and reproduces the published archive in normal and optimized modes. My decision also rests on the independent analytic reconstruction, primary-source checks, source/version limits, package identity and page inspection, rather than merely on those repair checks or passing code.

**Required repairs: none. Exact remaining gap for the claimed finite S3 counterexample: none found.** Imported analytic results remain manually checked rather than formally certified. Historical priority and novelty remain undetermined, and n>=4 plus the adjacent monotonicity problem remain unaddressed. CLEAR authorizes no external action by this reviewer and asserts no broader scientific novelty or literature completeness.
