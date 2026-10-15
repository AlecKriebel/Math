# Fresh independent whole-preprint/package adversarial review 01

**Frozen scope:** PR1031/problem30002816, publication candidate version1.0. Original pinned head `f6570e093267a7f910faf9cdd60dfbc1c12f5681`. ZIP104 entries,339736 bytes,SHA256 `18e7a23e07b8c1b3a1b44034c1533d37400f00480f821927bc2e6adbbe75c67a`. Candidate exact-file pins are in INPUT_PINS.json. This review was conducted independently of prior PASS conclusions; old audit verdicts were not proof premises. No other new whole-package review was read. No candidate/original bytes, Git/index/queue/PR or publication service state was changed; no individual was contacted and no outreach was prepared.

**Outcome:** The complete stated mathematical theorem survives this review. Two actionable P3 package-prose issues remain; therefore the whole-package verdict is **REPAIR_REQUIRED**, not CLEAN. No P0/P1/P2 issue was identified. The existing pending immutable-publication gate is appropriate. Completing or passing this review does not authorize a deposit, release or publication.

## Exact hypothesis and success criteria

The claim is that the oriented real mass ball `C(4,12)=conv(X(4,12))`, for all decomposable unit four-vectors of both orientations in real exterior-power495-space, has no arbitrary finite projected SDP lift. Consequences are failure of the original all-supporting-functions degree-at-most-one SOS assertion modulo the **full real vanishing ideal**, an existential rational **unnormalized** failing functional, and an existential constant closed comass-one four-form on R12 with no finite norm completion even at one point, hence none locally. Fawzi's normalized **complex** Sep(3,3) obstruction is an established external theorem, not an assumption validated by finite checks. No explicit coefficient list, exact maximum/comass, rational normalized calibration, least dimension or lower-dimensional classification is claimed.

Success requires a real linear injective ambient embedding, exact face/section identities at the **full generator hull** level, transfer of **any finite projected lift**, a compact first-moment consequence without hidden duality/closure assumptions, rational strict separation and correct absolute comass normalization, and the pointwise/local Harvey–Lawson interface. Package success additionally requires accurate prior credit, source versions/locators, current/historical separation, complete original Git preservation, genuine portable checker executions, safe reproducible archive and clean six-page rendering.

## Actionable findings, sorted by severity

### PK01 — P3 — portable negative-case coverage prose

`SUPPLEMENT.md:109–111` says that faults alter “embedding/minor/projector certificate values.” The certificate contains embedding columns, Gram/inverse metadata and schema; there are no independently supplied minor/projector-value fields. The fifteen fault families are six coordinate faults plus nine structure/metadata faults. Their45 executions all reject before the general projector and mixed-minor verification functions. Those identities are genuinely checked in the three unchanged symbolic baselines. They are also independently tested by my new source faults, but those new reviewer runs are not the package's48-run suite.

Repair the sentence to: “The faults alter embedding coefficients or certificate structure and metadata. The three unchanged baselines also check the full polynomial projector and mixed-minor identities.” Retain the correct48=3+45 count and the certificate-fault versus defective-source distinction. Exact complete evidence: `receipts/EXTRACTED_REPLAY.json` and `receipts/HOSTILE_CONTROLS.json`.

### PK02 — P3 — missing spaces in current public prose

The current README/supplement/index/deposit metadata contain systematic fused word/number boundaries: `Version1.0`, `12October2026`, `Python3.10`, `Pythonflags`, `Question6.5`, `in2019`, `bounded84-query`, `All29original`, `all225Hermitian`, `all25425upper-triangle`, `with11760`, among others. These are current reader-facing statements rather than code identifiers or preserved original records. The TeX/PDF is readable and does not have this systemic problem.

Copyedit the current prose to conventional spacing, synchronize metadata and its deposit wrapper, and rebuild the manifest/ZIP. Do not modify the29 original files or historical audit bodies to accomplish the copyedit. Representative locations: README5/34–43; SUPPLEMENT4/17–27/65–76/88–121; metadata description/references; deposit wrapper of the same metadata; evidence INDEX8/29–31.

## Independent universal mathematical derivation

### Kähler face, orientation and reality

Fix `J e_j=f_j`, `J f_j=-e_j` and `omega=sum e_j^* wedge f_j^*`. The compressed skew map of J on any real four-plane has two skew singular magnitudes at most1. `Phi=omega^2/2` evaluates on an oriented orthonormal frame as their signed product. Equality+1 forces both magnitudes1, so every compressed J vector has the same norm as its full J vector; orthogonal projection then has no lost component. The plane is J-invariant. The positive Pfaffian selects exactly complex orientation. Conversely a complex orthonormal pair has real frame `(a,Ja,b,Jb)` and Phi1. Finite convex combinations achieving the upper bound1 contain only generators achieving1. Thus the exposed face is the complete convex hull of positive complex two-planes, with no selected-subset assumption.

In the complexification, `u_j=(e_j-i f_j)/sqrt2` is in J's+i eigenspace. The225 elements `u_I wedge bar(u_J)` form a basis of the complex(2,2)-space. For Hermitian H, complex conjugation swaps H indices, and swapping the degree-two exterior factors has positive sign. The map A in equation(2) is therefore real and injective on the full225-dimensional real Hermitian space into495-space. Its unnormalized-w formula requires exactly1/4. There is no loss of the imaginary off-diagonal directions. A left inverse on this image extends to all495 ambient coordinates; no assumption that arbitrary mass-ball points are initially in the image is used.

Writing `hat(a)=sum a_j u_j`, direct expansion gives `a wedge Ja=-i hat(a) wedge bar(hat(a))`. Two factors of-i give-1, and commuting bar(hat(a)) past hat(b) gives another-1. Thus `A((a wedge b)(a wedge b)^*)=a wedge Ja wedge b wedge Jb`, with positive orientation. A unit decomposable bivector has a complex orthonormal factorization after absorbing phase; conversely each complex oriented two-plane comes from such a bivector. Therefore the face equals A of the standard convex hull K of normalized decomposable complex bivector projectors. On all Hermitian coordinates—not merely a sample of projectors—Phi∘A is trace. Q∘A is pure-block trace.

My independent Gaussian-rational bit-mask exterior implementation imports no candidate arithmetic. It reproduces all225 certificate columns, all25425 upper Gram entries (norm1 diagonal/norm2 off-diagonal), Phi/Q functionals and twelve varied rational complex frames against their complete real-plane coordinates. This independently corroborates rank225, rationality and the delicate sign/phase normalization. The universal identities are justified by the preceding algebra, not by finite frames alone.

### Complex normalized separable section and arbitrary lift inheritance

For `E=U orthogonal-sum Z`, the pure exterior blocks D and mixed block B are orthogonal. Every H∈K has a finite convex expression in unit decomposable projectors. If pure trace is zero, `sum lambda_t ||P_D z_t||^2=0`, and each positive-weight generator has P_D z_t0. This establishes a **full generator** restriction, stronger than merely knowing H's matrix support. Negative weights/cancellation do not occur.

For nonzero `a wedge b` entirely in B, the U projections of a,b are dependent and so are the Z projections. Neither projection span vanishes, since then membership in B would force the wedge zero. Choosing their respective one-dimensional generators x,y expresses a,b in span{x,y}; their nonzero wedge is a scalar multiple of x wedge y. The converse is immediate. This is exactly the k1=k2=1 specialization of Vrana–Lévay's prior theorem. T identifies orthonormal tensor basis elements with orthonormal mixed exterior basis elements. Unit wedge norm means product of factor norms1; rescaling gives unit complex x,y and the projector `xx* tensor yy*`. Thus K0 is exactly normalized complex trace-one Sep(3,3), including the full complex phase coordinates. It is not a real-only state body or an unnormalized cone.

Inside the mass ball the two simultaneous equations Phi1,Q0 first force membership in the Kähler face, then the pure-trace section. Hence equation(6) is exact. Q can be negative elsewhere on the mass ball: reversing a pure positive complex plane gives Phi-1,Q-1, which I checked exactly. The equations alone do not define Sep; my fresh Bell projector has Phi1,Q0 and exact partial-transpose quadratic witness-1. This supplies an adversarial boundary control for the essential mass-ball membership qualification.

If C=π(S) for any finite LMI with any auxiliary variables, imposing `Phi(π(s))=1,Q(π(s))=0` merely adds affine equalities to S. Apply the ambient extension of A's inverse followed by T's inverse on the mixed support. The result is a finite projected lift of Sep(3,3). A real-symmetric LMI is a Hermitian LMI, so the published Fawzi definition and theorem exclude it; arbitrary affine equalities can also be encoded in the spectrahedron. This contradiction proves no arbitrary finite lift of C(4,12), not just failure of a fixed hierarchy or an unprojected LMI. No nonexposed-face or polar-representation inference is used.

### Full-ideal compact moment consequence and rational unnormalized gap

The space `J2=I(X) intersect polynomials_degree≤2` is finite-dimensional even if the full ideal has additional generators or subtle real-radical issues. Imposing its finite basis on a496-square moment matrix defines a finite affine spectrahedron. It contains rank-one `(1,p)(1,p)^T` matrices for every p∈X. The sphere relation belongs to the **full** vanishing ideal, and with M00=1 forces `sum Mii=1`, hence trace2. PSD implies each diagonal is in[0,2] and `|Mij|≤sqrt(Mii Mjj)`, so the closed feasible set is bounded and compact. Its linear projection is compact. No Slater, duality, SDP attainment or closure of a nonclosed shadow is needed.

If a supporting affine function δ−ell is affine SOS modulo I(X), its discrepancy has degree≤2 and therefore lies in J2. Evaluation by any feasible M gives `δ−ell(x)=sum a_j^T M a_j≥0`. All supporting halfspaces thus cut the projection back down to conv(X), and rank-one inclusion gives equality. That equality would supply a finite lift, already excluded. Therefore the compact first-moment projection strictly contains the mass ball.

For x outside the compact convex mass ball, strict separation supplies c with gap `g=c·x−max_X c·p>0`. For perturbation d, the support function changes by at most `||d|| max_X||p||=||d||`; the projected value changes by at most `||d|| ||x||`. Thus any `||d||<g/(||x||+1)` preserves a positive gap. Rational coefficient vectors are dense, so a rational c' remains strictly separating. The same feasible M makes the rational support's value negative, excluding any affine SOS. This is existential and unnormalized; no rationality of δ or ell/δ is inferred. A zero c' could not retain positive gap. Signed coordinate wedges lie in X and span495-space, so its nonzero ell has positive maximumδ. Compactness attains that maximum. Symmetry X=-X gives absolute comass exactlyδ, making the constant form ell/δ closed and comass1.

### Harvey–Lawson pointwise/local interface and optional converse

At any point, a differential four-form is a linear functional on exterior four-vectors. The original Question6.5 asks for finitely many such forms giving `phi(p)^2+sum psi_j(p)^2=||p||^2` on **all simple** vectors, locally. On unit simple vectors the exact algebraic identity `1−phi=(1−phi)^2/2+sum psi_j^2/2` would give an affine SOS. Multiplication by positiveδ would then give an SOS for the chosen unnormalized supporting function, contradiction. Consequently the constant calibration fails at every point; any local completion would give a prohibited pointwise completion. Closure of the additional forms is not assumed or required.

The paper's optional pointwise converse is correct: subtract the identities at±p to get B^T a=-phi/2, add them to get `||a||^2+||Bp||^2=1`, and use a maximizer p0 with Bp0=-a. The identity at-p0 gives4||a||²2. Orthogonal projection onto a-perp then gives `2||P Bp||²=1−phi²`. Homogeneity extends it to all simple vectors. No smooth local selection is inferred from this pointwise result.

## Primary sources, dates, credit and priority framing

Fifteen primary PDFs were freshly fetched into `sources/raw`, with exact URLs, final URLs, SHA256s, versions and extraction hashes. Complete critical source-body pages were read, including Fawzi's published definition/Theorem1, the original Sanyal conjecture, Harvey–Lawson's actual equation and local question (also rendered/viewed), Vrana–Lévay's full lemma/theorem/proofs and the fermionic projector definitions. The detailed fresh inspection ledger is `sources/SOURCE_INSPECTION.json`; raw third-party bodies exist only under `sources/raw`. Search snippets are not theorem evidence. Fawzi's proof is not independently reproved, and this precise external dependency remains disclosed.

The nine global priority obligations are substantively satisfied in the current paper/abstract/README/supplement/metadata:

| Fix | Fresh assessment |
|---|---|
| PF01 | Title/abstract/result explicitly apply Fawzi; published2021 and first preprint2019 credited. Fresh arXiv HTML verifies4May2019 submission. |
| PF02 | Classical Wirtinger/Kähler face, established fermionic projector body, and Vrana–Lévay's exact2009 tensor-to-wedge theorem credited. |
| PF03 | Theta/moment, cone-lift/factorization and survey lineage credited; compact trace argument described as a self-contained specialization. |
| PF04 | Sanyal's joint Rostalski work and pre2015 connection credited;2010slides and2013chapter explicitly precede the2015 report;1982Question is not promoted as a proven affirmative theorem. |
| PF05 | BSV and BKM homogeneous quadratic/projective/Sym²-exterior results distinguished from oriented supporting affine functions and the ambient-linear mass-ball section. No first Grassmann no-shadow claim. |
| PF06 | Unprojected-LMI obstruction, fixed-hierarchy failure and arbitrary finite projected lifts distinguished. Full Orbitopes Theorem7.6 context ends by distinguishing projections. |
| PF07 | Rational unnormalized existence only; no explicit coefficients/comass/minimality/classification; positive Kähler calibration not identified as failing. |
| PF08 | No worldwide-first/current-worldwide-open/certified-priority/human-peer-review/journal-acceptance/formal-certification claim. Historical statements explicitly mapped as historical. Extensive AI use and AI review disclosed. |
| PF09 | Current fresh whole-package gate explicitly pending; review does not silently flip publication authorization or readiness. |

The existing ledger actually has21batches/84exact query strings, matching its count; its26fetch rows comprise25successful PDF retrieval records and one explicitly excluded non-PDF response. Existing records include URLs/hashes/version/locator/inspection-level/limits. I independently freshly inspected15relevant PDFs rather than pretending to repeat all25PDFs or84queries. A separate four-query spot check located no additional full-assembly predecessor; irrelevant/nonprimary results were not relied upon. This is bounded corroboration only. Worldwide priority remains unestablished, consistently with all current framing.

## Checker, reproduction and hostile controls

Both the complete standalone runner and exact validator were inspected before execution. The historical runner's main UID1000/environment permission harness was inspected but never executed or simulated. Only the reviewed pure mutation function and literal data are extracted from hash-pinned source by AST. The validator arithmetic uses exact Gaussian integer pairs and Fraction parsing, constructs independent determinant columns and a complete polynomial projector identity, and checks all495coordinates/11760terms and nine mixed minors. Required conditions use explicit exceptions rather than optimization-sensitive assertions. Its optional historical read-only probing function is not invoked by the portable kit. No network, credentials, special UID or external solver is required.

The safely extracted clean archive's `run_checks.py` produced a fresh receipt with **3actual symbolic baselines plus45actual defective-certificate executions** across normal/-O/-OO. Complete stdout/stderr bytes, actual subprocess exits, certificate hashes and recursive JSON types matched references. All baseline exits0, all fault exits1, every stderr empty, intended rejection reasons—not crashes—observed. The original checker source/certificate/historical runner remained unchanged. Three optimization modes repeat mathematical cases, rather than giving three independent mathematical mechanisms. Python's isolated/optimization flags are not a sandbox, consistently disclosed. Independent family code is stage evidence, can write receipts and some historical guards use assertions; it is not part of this48-run guarantee.

New reviewer controls go beyond reproducing PASS: three source mutations directly damage the projector factor sign, Phi trace factor and mixed-minor sign; all nine normal/-O/-OO executions reject for the intended GENERAL_PROJECTOR_IDENTITY/PHI_TRACE/MIXED_PLUCKER_MINORS reasons. Three fresh certificate faults (Boolean index, Boolean coefficient, noncanonical rational2/2) reject for strict type/canonical reasons. The runner's recursive comparator independently distinguishes Boolean/int, int/float and list/tuple while accepting identical recursive types. Full streams/exits and exact source/input hashes are saved in HOSTILE_CONTROLS. These new controls are clearly reviewer evidence, not fabricated or added to the candidate48-run count. They also substantiate PK01's narrow documentation repair.

Finite code corroborates the elementary bridge. It does not validate Fawzi's universal external theorem, prove the existential failing calibration numerically, compute exact comass, establish priority or provide proof-assistant certification. All these limits are respected in the paper and metadata.

## Original bytes, archive, manifests, metadata and navigation

`git show` for each original pinned path at the actual original head agrees byte-for-byte with every authored original file in the package and each corresponding original SHA256/size. A separate recursive `git ls-tree` finds exactly29original files, with exactly the pin set: preservation is complete, not merely29selected matching examples. Original historical acceptance/status/permission seals and priority counts remain intact and the evidence index explains their stage meaning.

The archive's104file entries are sorted, unique (also casefold-unique), ASCII safe paths inside one top-level folder, regular files (no symlinks), with fixed12October2026timestamps. CRC validation passes. After stripping the documented top-level prefix, every archive entry equals the corresponding candidate disk bytes. All103non-self manifest entries match sizes/SHA256s; the inventory plus its self-excluded manifest is exactly the104archive-file set. Rebuilding the archive from its exact entries/metadata reproduces its complete bytes. All README/supplement/index relative links exist. Metadata.json exactly equals zenodo-deposit.json's metadata wrapper and its two file references exist. No raw third-party primary bodies are redistributed in the candidate bundle; authored source URL/hash records remain.

The candidate current review state correctly records no fresh package review yet, immutable-publication-ready false, `all_actionable_issues_resolved=false`, publishedfalse. This review finds P3s and does not rewrite that candidate state. Candidate pins are checked again at freeze.

## PDF/source review

All six pages were freshly rendered by Poppler at1600pixel page scale and viewed separately. Page1 title/abstract/original question and Fawzi interface are legible; page2 theorem and complex embedding equations preserve signs/bars/normalization; page3 section/positivity proof and two hyperplanes are clean; page4 moment/rational/calibration/converse derivations render fully; page5 limitations/credit/AI disclosure and first references are clean; page6 remaining bibliography is clean. No clipping, overlaps, missing glyphs, broken math/citation numbers or unresolved reference markers were observed. All14references match their in-text numbering. References split onto page6 normally, without stray content.

The saved extracted standalone TeX compiled successfully with the built-in desktop compiler, with no diagnostic warning reported by that interface. The candidate's own layout receipt additionally records compiler success/no relevant warnings. The built-in tool does not expose a full raw compiler warning transcript; this review does not fabricate one. Source and PDF substantive statements agree with the independently checked claim and metadata. PDF SHA256 is pinned in INPUT_PINS.

## Strongest verified result, remaining gap and repair acceptance

The strongest checked result is the entire written existential universal-negative theorem, conditional only on the precise established published Fawzi theorem, with full original source preservation and genuine exact48-run reproduction. There is no unresolved mathematical gap found. Priority is bounded and not worldwide certified; explicit coefficients/comass/minimality/classification remain outside the claim.

The exact remaining package gap is PK01+PK02. Suggested repairs are current-prose-only changes, followed by synchronized metadata and regenerated inventory/archive, then a fresh adversarial review of repaired bytes according to the user's fix-loop requirement. This frozen review does not retrospectively certify changed bytes. CLEAN is available only with zero actionable issues; a CLEAN review still supplies no inferred publication authorization.

Frozen UTC: 2026-10-13T21:59:17.763959+00:00
