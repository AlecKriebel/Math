# Second fresh full adversarial package review: PR1047

**Verdict: no actionable P0, P1, P2, or P3 findings.** This is a new complete review of the unchanged v1.0 candidate, not a spot-check or adoption of the first package review's clean conclusion. It independently supports the precise elementary obstruction and the package's reproducibility and credited-expository framing. Completion: 100% of this assigned second review. It does not perform terminal administrative approval, publication, deposit, merge, or release.

## Frozen target and independence

Before substantive inspection, `INPUT_PINS.json` froze all **854 pre-existing regular audit files**, with bytes and SHA-256; candidate, original submitted edition, and root records were copied into reviewer-owned `frozen/`. The dedicated folder did not previously exist. The complete current candidate has **177 files**. Its authoritative three artifact pins are:

| Artifact | SHA-256 |
| --- | --- |
| Four-page PDF | `1ce63633a68179f5e9296fee9493632c4d6272918b8a42172eb382fbb0e0532d` |
| Complete LaTeX source | `70b64ede7f3b8c628e5be0b6debe21127aa1e3b4954032670633c7624f946592` |
| Support ZIP, 628830 bytes | `f6b3e2282cfe23b7135bf686c4f190884388af1dced82afff2c3da794f60f20d` |

`INDEPENDENT_DERIVATION.md` was written after reading the candidate mathematics and before reading prior review reports/verdicts. It derives both obstructions, exact finite square-root optimum, all boundaries, coefficient identity, oracle distinction, and copied-block distinction from their definitions. Subsequent root review records were used to identify administrative stage and required scope, never as proof premises. The new `independent_finite.py` uses hereditary independent-set families and the augmentation axiom, materially different from the packaged basis-family enumeration.

All nine original submitted bodies were read in full, and their bytes were matched to the root's original-file pins, the package's evidence copies, and the earlier frozen actual-Git-object copies under package_01. The historical edition is bound to head `56b3a35182e5cb04b05e41f5017e47caf50582c1` by the preserved original records. No Git command or live service query was performed in this review, so the present GitHub state is not newly certified. The source edition had **zero executables**. No unavailable predecessor or omitted historical computation is reconstructed or claimed replayed.

## Exact claim and independent mathematical attack

The claim is false under the explicit uniform interpretation:

`exists alpha>0, for every finite V and every normalized nonnegative monotone submodular f on V, exists one ordinary unscaled matroid M on that same V, for every S subset V: r_M(S)/alpha <= f(S) <= alpha*r_M(S)`.

Normalization means `f(empty)=0` and `f({i})=1` for every element. The approximant is one integer-valued ordinary rank, with no scalar, weights, copy expansion, sum, oracle restriction, or hidden uniform-matroid assumption. Success is disproving this exact quantified assertion. It does not require a novel input function, a new decomposition, an algorithmic query lower bound, or a result about an alternative intended formulation.

The direct decreasing-increment proof of square-root-cardinality submodularity works for every pair of subsets, with empty sums covering containments and empty cases. Singleton upper comparisons force every element to be a nonloop, `alpha>=1`, and positive integer total rank `R`. A basis B has both size and rank R, so the **lower** comparison there gives `R<=alpha^2`; the **upper** comparison at V gives `sqrt(n)<=alpha*R<=alpha^3`. Thus `alpha>=n^(1/6)`. Choosing integer `n>max(1,alpha^6)` defeats any proposed fixed constant. The basis may depend on the matroid because comparisons cover every subset. This is not circular.

For each fixed total rank R, every loopless matroid is forced by B and V to have factor at least `max(sqrt(R),sqrt(n)/R)`. Uniform rank `min(k,R)` attains it after checking both ratios on the intervals `1<=k<=R` and `R<=k<=n`. The empty comparisons are zero. Minimizing over all positive integer ranks proves the exact finite optimum **among all ordinary matroids**, not just uniform ones. At `n=m^3,R=m` the bound is attained. At n=2 the optimum is sqrt(2), so the candidate correctly declines general equality with n^(1/6) and any optimal exponent over the entire input class.

For `n=m^2`, `g_m(0)=0` and `g_m(k)=1+(k-1)/m` have increments one followed by 1/m, all nonnegative and nonincreasing for integer m>=1. The normalized rational function is the nonnegative combination `(1-1/m)U_1+(1/m)U_n`. A basis gives `m<=alpha+alpha*(m-1)/R`; the full set gives `alpha*R>=m+1-1/m>=m`, hence `R>=m/alpha`. Substitution with `m-1>=0` yields `m<=alpha+alpha^2`. The positive quadratic root and `alpha>=1` imply the displayed root and `sqrt(m/2)` lower bounds. The proof never divides by `m-alpha`, never reverses an inequality at m=1, and never assumes a nonuniform rank equals uniform rank on all subsets.

The empty ground set is harmless: both functions are zero, any positive factor works. On nonempty ground sets loops and total rank zero are impossible. At n=1 the square-root optimum is one. At m=1 the rational function is free rank on one element, factor one; the asserted rational necessary lower bounds are compatible and expressly weaker. If the source's noninteger wording is made an additional restriction, square-root n>=2 and rational m>=2 meet it. For fixed dimension the free rank with alpha=n works for all eligible inputs, using `1<=f(S)<=|S|` on nonempty S. This supports, but does not manufacture, the uniform reading.

The finite-difference coefficients `c_i=d_i-d_(i+1)` for i<n and `c_n=d_n` telescope to `h(k)=sum_i c_i*min(k,i)`. Nonnegative coefficients follow from decreasing increments; normalized h(1)=1 makes their sum one. At n=1 the sole coefficient is d1. This establishes the exact displayed decomposition without trusting a misprinted source coefficient.

No central difficulty was transferred to an unsupported equivalent claim. The strongest verified mathematical result is the full infinite ordinary-rank obstruction, exact square-root-family finite optimum, and rational lower bounds in the stated model. There is no remaining mathematical gap within that model.

## Original source, credit, and limits

`SOURCE_CUSTODY.json` records six pinned primary-body identities freshly inspected in this review, plus the author-listing identity for the GHIM full version. Raw bodies, extracted source text, and the third-party source-page image stay under ignored `_private/`. New readonly web openings independently confirmed the official report, arXiv entry, and author-hosted full-version endpoint. They were source access, not external outreach or publication.

- **Végh:** the complete [official OWR contribution](https://ems.press/content/serial-article-files/46931), printed p2946 / PDF54, was newly rendered and actually visually read through the start of the next titled contribution. It displays `r(S)/alpha <= f(S) <= alpha*r(S)`, same-V rank class, singleton-one and empty-zero nonnegative monotone submodular inputs. Its sentence names the rank f while its display uses r. It does not separately print a quantifier over all V. The candidate explicitly qualifies the conventional dimension-independent interpretation, without asserting an unprinted intention or present worldwide open status.
- **DDSSS:** the complete Appendix D Lemma D.1 statement and proof in the pinned [arXiv body/metadata](https://arxiv.org/abs/1304.4948) were checked. It is prior uniform-rank decomposition and its statement uses integer values. The candidate credits that mechanism, explains its real-valued finite-difference application directly, and correctly uses `c1=2h(1)-h(2)` for n>=2 instead of the source's erroneous first coefficient. The source also has indexing slips. Its margin says v1 submitted17April2013; title block says29October2018. The note does not mistake the latter for the first submission date.
- **Balcan–Harvey:** the pinned SICOMP47(3),703–754 body, Section5 Proposition1, directly presents concave cardinality submodularity and attributes it to Lovász1983 p251. Reference70 identifies the1983 survey. The candidate properly reports this attribution through Balcan–Harvey; the original Lovász survey remains unread. The elementary proof here does not depend on that missing original.
- **GHIM:** both pinned [conference](https://www.cs.ubc.ca/~nickhar/papers/SubmodularEverywhere/SubmodularEverywhere.pdf) and [full-version](https://www.cs.ubc.ca/~nickhar/papers/SubmodularEverywhere/SubmodularEverywhereFull.pdf) primary bodies were checked at Problem1, the actual root-linear output, and the Section6 construction. Polynomial query complexity and an unrestricted approximating function differ from unrestricted existence of one ordinary rank. Their output is `sqrt(sum_i a_i)` with nonnegative coordinates and includes square-root cardinality. Their hard monotone inputs are matroid ranks; each can existentially be approximated by itself exactly. Thus their query lower bound alone cannot establish this obstruction. The stored author's publication list separately labels the full-version draft2010 and conference2009.
- **Schrijver:** the entire Section44.6b, printed776, was checked, including Helgason1974 attribution, disjoint copy blocks, rank formula, and exact representation on block unions. The candidate's explicit m-layer construction gives expanded rank `(m-1)min(k,1)+k=m*g_m(k)`, then divides by m. That uses a larger ground set and scaling, so it is not a same-V ordinary-rank approximant. The original Helgason body remains unread.

These checks support **credited elementary exposition**, not exact historical firstness. Priority of the one-rank argument and generic concave-cardinality envelope is still unresolved. The unpublished GHIM citation and further source-chain consequences remain unverified. No exhaustive-source exclusion, current worldwide open-status, independent-discovery evidence, copying conclusion, intellectual priority, new-function, or new-representation claim is established. The paper, README, supplement, metadata, and preparation report already disclose those limits. They are not actionable omissions in a note that makes no such claims.

The preserved original and historical audit labels are explicitly dated and scoped by `evidence/INDEX.md` and `REVIEW_HISTORY.json`. Earlier pending-priority fields and later credit adoption are separate stages. Static v1.0 preparation labels are not representations of completed whole-package review, human refereeing, journal acceptance, or formal proof certification.

## Complete integrity, custody, and package audit

`PACKAGE_BYTE_CHECKS.json`, produced by new `audit_package.py`, verifies independently:

- all **148** protected preparation inputs against current source bytes and the initial review freeze;
- all **160** declared preparation output pins;
- all **97** selected authored evidence-copy map entries against both source and package bytes;
- all **nine** original bodies, including their earlier frozen actual-Git-object byte copies;
- **142** exact allowlist content entries and every manifest hash;
- exactly **143** ZIP members, no duplicates, safe regular relative paths, expected modes, fixed timestamps, stored compression, payload equality, and CRC;
- exact equality of the normalized metadata objects across request wrapper, bare `.zenodo.json`, and external deposit descriptor;
- one sole named author, supplied ORCID, independent-researcher affiliation, version/date, CC BY4.0, UNREFEREED, extensive AI assistance, and output descriptor naming exactly the PDF and support ZIP.

The manifest deliberately lists sorted content allowlist **followed by** MANIFEST.json, while the ZIP uses sorted complete member order. This is a consistent explicit convention, not a defect. The manifest is a member without a circular self-hash; the archive pin is external. Metadata wrapper normalization is likewise intentional: `{metadata:...}` equals the bare object's content after normalization.

The complete local candidate has177 files, while preparation output pins declare160. The remaining17 are the output-pin file itself, two already hash-bound copied stage output-pin manifests, and14 local layout render images. They were all independently hashed in the854-file freeze. Their relevant distributed manifests are covered by the content manifest; temporary render images are excluded from distribution. No claim was assumed that the160-output list equals every local file.

The explicit allowlist excludes the delivered PDF, external deposit descriptor, private preparation INPUT_PINS, third-party raw bodies/extracted text/images, local render/cache directories, and historical ZIP/PDF binaries. Every content member decodes as authored UTF-8 text; read receipts cover all142 content members. Historical scripts retain original output paths as declared inspection artifacts. The actual portable checker differs only by its documented output-path interface, as verified by exact source replacement and hashes. No historical script with fixed original output paths was executed.

## New reproducibility and fault controls

From a fresh safety-checked extraction of the **current final** ZIP, this review executed every README command: integrity verifier, creation of scoped verification output, portable finite checker with complete stdout/stderr saved, paper directory setup, and standalone Tectonic compilation. All commands actually exited0; finite stderr is empty. The result object's complete mathematical content matches the recorded preparation result after excluding exactly `started_utc`, `completed_utc`, and `checker_sha256`. This declared projection is not raw-byte equality. The run again enumerates497 labelled matroids through n5, checks20100 square-root size/rank pairs for n1..200,9455 rational pairs for m1..30, cube sharpness m1..100, radical-free all-set-pair submodularity, and all packaged semantic controls. Finite checks supplement the infinite derivations.

The new independent-set checker separately enumerates2,5,16,68,406 matroids for n1..5 (total497), verifies each rank's exact square-root optimum lower envelope, and verifies rational envelopes at m1 and2. It checks46376 square-root cardinality triples through n30,83648 rational triples through m8, and coefficient identities through n50 using exact integers/Fraction. Its six semantic controls refute false one-sided, scaled-output, unnormalized, uniformity, and universal-equality extrapolations. The scaled-output witness is finite model sensitivity, not a theorem asserting a universal scaled-rank approximation.

`guard_controls.py` applies every mutation only to reviewer-owned copies. All **15** deliberate negative controls are rejected: corrupted payload; bare request wrapper; unequal metadata; publication-ready state switched true; checker sweep scope changed with a coherently rebuilt manifest; original proof body changed with rebuilt manifest; duplicate evidence path; altered manifest-order convention; absolute and traversal paths; circular manifest member; ZIP member; leaf symlink; ancestor symlink; directory member. Rebuilt manifests in semantic controls prevent mere stale outer hashes from masquerading as the targeted semantic guard. The positive extra-file control confirms unlisted local outputs do not enter the archive and the archive remains byte-identical.

The supplied builder regenerated the final ZIP **byte for byte**, even after local finite/PDF outputs appeared. A separately authored stored-ZIP reconstruction, without executing that builder, also matches exactly. `CLEAN_REPRODUCTION.json` and `GUARD_CONTROL_RESULTS.json` preserve these results and actual failure streams.

## Every PDF page and standalone source

The complete LaTeX source was read, including bibliography and disclosure. All four delivered PDF pages were rendered at120dpi and individually actually viewed:

1. Title, sole author, ORCID, date/license/unrefereed line, abstract, exact formulation, source-quantifier caution, fixed-dimension and empty-ground boundaries.
2. Complete square-root proof and exact optimum, basis/full-set equations, cube sharpness, n2/n1 qualifications.
3. Rational family and every inequality, m1/empty/noninteger cases, classical two-rank credit and corrected decomposition.
4. Actual GHIM mechanism/output, copied-block distinction, unresolved historical scope, extensive AI disclosure, all six references and their stated source limits.

No clipping, overlap, overflow, black replacement glyph, broken equation, unreadable citation, or page-footer problem was found. The four-page count and PDF title/author/subject/keywords match the source. It contains no form, JavaScript, or encryption. The clean default README compilation gives identical extracted text and **exactly equal page-render PNGs** to all four actually inspected pages. Its PDF bytes differ because the default build epoch differs. With the preparation receipt's declared `SOURCE_DATE_EPOCH=1791936000`, a new standalone Tectonic export gives **byte-identical delivered PDF**. The README promises rebuilding the PDF, not unconditional timestamp-independent PDF-byte equality. Therefore the default metadata difference is not an actionable defect.

`PDF_VISUAL_AND_BUILD_RECEIPT.json` binds all four actual inspections, raster checks, and declared-epoch reproduction. No prior worker's page-view statement was used instead of fresh visual inspection.

## Disposition, exact limits, and sealed evidence

No actionable findings were found. Recommend that the root adopt this as the required **second fresh clean full-package review of the exact unchanged pins above**, then apply its separate terminal administrative process and publication sequence hold. Candidate `CURRENT_REVIEW_STATE.json` is correctly a dated preparation-stage hold; this review does not edit it or treat it as terminal clearance. Publication after PR1032 and any further administrative action remain outside this worker's authorization.

All854 initially frozen files remained unchanged at `FINAL_INPUT_RECHECK.json`. Only this new dedicated review folder was written. No candidate, original/historical record, branch, index, Git object, service, publication, release, deposit, or other effort was mutated. No individual or other shard agent was contacted. The research log records timestamps and completion estimates5%,20%,75%,100%.

Runnable new artifacts: `audit_package.py`, `independent_finite.py`, `guard_controls.py`, and `verify_review.py`. Original input custody is `INPUT_PINS.json` plus its checksum. Mathematical reasoning is `INDEPENDENT_DERIVATION.md`; independent results, package-byte results, fresh run streams, primary custody, controls, visual/build receipt, and final input recheck are separately preserved. `VERDICT.json` records zero counts at every P0-P3 severity and the disclosed nonblocking limits. `OUTPUT_PINS.json` is the immutable content inventory of reviewer-authored and generated artifacts; `SEAL.json` pins that inventory, report, verdict, and input freeze without self-reference. Private source bodies are ignored and excluded from output publication inventory. This is AI adversarial review, not human peer review or formal proof certification.
