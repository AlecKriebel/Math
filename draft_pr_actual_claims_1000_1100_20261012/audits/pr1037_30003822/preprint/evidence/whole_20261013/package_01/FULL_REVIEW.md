# Full adversarial current-paper and package review 01

Disposition: **mathematics, source credit, provenance, rendering and archive integrity PASS; one P3 release-wording repair remains.** No P0, P1 or P2 issue was found. The frozen input is a sound credited proof exposition, but its durable public prose should not permanently state that the current whole review is pending after that review is complete. This is a scope assessment and concrete repair, not an additional user-permission gate or authorization to publish.

## Frozen candidate and review order

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| paper/forest_transfer_catalan.pdf | 123244 | 9ed04da332b9815dd91a7fe25b76217f788228ce3b1a75ff5ccd2193750fb95e |
| paper/forest_transfer_catalan.tex | 37685 | 8eb445dc33481825b99cdec1001cd425b6961903472873282d5ddc1d9ce8285b |
| pr1037_supportkit_v1.0.zip | 316215 | f235148c8b191160ae557c45e6d214a48508d98f2a8cc91c4de984546f93480b |
| original PROOF.md | 25072 | 546d9df387da3266b1b20d31b1cd6017a65fe9f497f1b37d2a99319e6194755c |
| original AUDIT.md | 14983 | 2d2a03db98576bd58e9726198b3fd050f77cde68a97ef2b5670c6c538678285b |

The original Git head is e87236a97c4b87818d2768cd5789043c7c3f4e39. INPUT_PIN.json froze all 121 actual candidate/original files before review. I then read the whole current TeX and wrote INITIAL_INDEPENDENT_DERIVATION.md before reading old root derivations, family derivations, PASS reports or historical acceptances. It is a full written all-n reconstruction, including all seven lemmas, sign/normalization checks and ring descent; it is not a numerical extrapolation or an adoption of inherited verdicts. Only afterward did I compare the historical proof/audit, root dispositions and fresh family records. The root independently flagged the pending-review release-wording lead during this review; I checked its actual locations and propagated public-prose instances and adopted the P3 finding below. The mathematical reconstruction remained independent.

## Exact mathematical conclusion

For every n>=1 and generic independent commuting A=(a_ij), the full Bell-partition transfer matrix T satisfies (det A)^C_n | det T in Z[a_ij]. Each input block has one arbitrary fixed unweighted tree. Each interlayer subset is counted once; it survives exactly if its union with the fixed trees is a forest, every component meets Y, and its Y component intersections induce Q. The proof covers nonsymmetric and signed entries, nonplanar forests, singular matrices and any vanishing row sums by polynomial specialization. It establishes a divisor and does not establish exact multiplicity, cofactor irreducibility or complete factorization.

My strongest independently verified operator statement is det(G_A|W)=(det A)^C_n with scalar/sign +1, where W=Λ(U⊗Q²)^SL₂ is a constant image of dimension C_n and U is the sum-zero row hyperplane. A constant rational kernel splitting then gives the full Bell determinant factor over Q[a_ij], and primitivity gives the integral quotient.

### All-n obligations and adversarial attempts

| Obligation / attempted failure | Independent finding |
|---|---|
| Cycle annihilation and representative trees, §1/Lemma 1 | The incidence wedge separates with (−1)^(s(s−1)/2); cycle vectors are dependent. Tree incidence vectors form a Z-basis of the sum-zero lattice. A ±1 basis change appears in both species and squares to +1. Fixed tree choices are never averaged. |
| Exact full transfer, §2/Lemma 2 | Even square-zero edge factors give one term per subset. X-only components lack top degree. Replacing an already selected tree by a Y-rooted star is an equality, not a new sum. Each X leaf pair has coefficient +1; even pairs introduce no sign. The output is exactly f_Q. |
| All-n infinitesimal invariant dimension, §3.1/Lemma 3 | E*=F and [E,F]=H identify weight-zero invariants with ker E and prove E:M₀→M₂ onto. The weight-two orthogonal cokernel equation forces zero by positivity of the auxiliary Hermitian form. Rational kernels descend from C. This is not positivity of A. |
| All-degree generation, §3.2/Lemma 4 | Noncrossing epsilon tensors have distinct largest Dyck words of coefficient 1 and attain the tensor invariant dimension. An explicit normalized antisymmetrization has exterior projection as left inverse. Thus invariant tensor lifts exist and project to products of b(u,v). No unproved invariant-quotient exactness is assumed. |
| Epsilon sign, normalization and full Bell spanning | Odd reordering produces b(u,v)=ξ(u)ξ̄(v)+ξ(v)ξ̄(u); b(u_i,u_i)=2q_in. The other quadratic identity generates every edge q. Every q monomial is zero or a forest state of an arbitrary component partition. Φ from the complete Bell space is onto and A-independent. Noncrossing matchings are only a tensor-basis device. |
| Catalan total and endpoints, §3.3 | d_r=binom(m,r)^2−binom(m,r−1)binom(m,r+1), with out-of-range terms zero; Vandermonde gives C_n. d_r=d_(m−r) gives total degree md. Endpoint degrees and n=1 are retained. |
| All-matrix determinant character, §3.4/Lemma 5 | The invariant subspace has torus weights; permutation conjugacy equalizes exponents; scalar degree sum fixes each exponent to d. Conjugacy and polynomial density extend the identity to all characteristic-zero matrices. Scalars or finite diagonal tests alone would not suffice. |
| Gaussian signs and top coefficient, §4 | Exact completion uses D of row sums, B=D⁻¹A and symmetric zero-sum S. Paired top extraction gives +det D, not an unpaired-order sign. Odd translation's top coefficient is +1. |
| H_D and M_S stability / order, Lemmas 6–7, (26) | Differences remain differences under normalized lowering; simultaneous SL₂ equivariance makes extraction invariant. H_D strictly lowers degree except its identity diagonal. The S quadratic is an invariant in differences, so its exponential strictly raises degree except identity. Both determinants are 1. The actual identity is (det D) M_S ρ(g_B) H_D in this order; no H/rho or H/M commutation is needed. |
| Row versus column hyperplane, (25) | u↦uB preserves u1=0 because B1=1; the ambient quotient has identity action. Thus det g_B=det B=det A/det D, with no column-stochastic requirement. |
| Singular / all-zero-row-sum boundary | G_A already has polynomial entries on a constant rational basis before localization. Equality in Q(a_ij) therefore holds in Q[a_ij] and every specialization. Intermediate D⁻¹ need not exist after specialization. |
| Constant kernel and integral quotient, §5 | Fixed rational kernel basis plus fixed quotient lifts make a free polynomial splitting and a polynomial complementary block. L_A has matrix Tᵗ. A variable-dependent rational splitting would be insufficient, but none is used. Primitive det A powers and Gauss's lemma give Z-divisibility, including zero quotients. n=1 is direct. |

I found no unsupported equivalent central claim, hidden planarity condition, circular dimension assumption, unexplained Gaussian normalization, or variable-denominator transfer of the difficulty. The complete checkable derivation is in INITIAL_INDEPENDENT_DERIVATION.md.

## Source and priority credit

SOURCE_NOTES.md records fresh public primary objects, hashes, exact body locators, inspection bounds and failures. The exact public Ferudun Theorem 1.2 has the same normalization and all-n integral conclusion. I read its actual definition and core proofs in §§2–6, including both forest/inverse and tree-pairing/bordered-determinant arguments; no gap affecting the divisor was found. Its additional computer-assisted exactness computations were not reproduced or certified.

The current abstract, theorem introduction, main introduction, dated addendum, README and both metadata descriptions identify this exact same conclusion globally. The comparison is not buried as an adjacent grove citation. Fresh public records verify PR creation 9 October 22:16:52 UTC, original head committer date 22:16:22 UTC, and the matching DOI registration 11 October 13:01:38 UTC. Historical visibility, independent discovery, copying and intellectual/worldwide priority are correctly left unestablished. No current-open or first-solution marketing claim remains in the durable mathematical prose.

The full source interfaces were checked against fresh CSS v2, Sportiello Chapter 10 and Kenyon–Wilson v4. CSS's forest/exponential/elimination identities are prior work; its basis statement is an announcement with deferred proof. The thesis supplies a completed normalized polynomial basis treatment; its selected triangular coefficients survive λ=0. The catalogue year is 2010, distinct from cover academic years. KW supplies the equivalent full-partition projection/tree pairing; associated meander nonsingularity is credited to its earlier authors and is not a premise here. CJSSS forest-representation credit is included. Re-deriving these ingredients does not make them new, and the paper does not claim otherwise.

The dated source addendum accurately supersedes the historical no-match framing while retaining the October 9 bytes. The inspected Laplace/FPSAC versions are now readable critical-body comparisons. Kogan's entire 17-page text was read, including its nonplanar coloring tensors; exclusion by planarity alone is not used. Li–Yan full body remains unknown after access failure. CSS 2017, version comparisons, self-similar followups, forward citation chains and discovery history remain partial. Those uncertainties limit novelty/priority claims, not the stated algebraic theorem. They are explicitly disclosed and require no new hypothesis or permission gate for credited exposition.

## Whole PDF, TeX and prose inspection

I independently rendered the actual frozen PDF with pdftoppm at 110 dpi and individually viewed all 12 page images. PAGE_INSPECTION.json pins every render. The PDF has 12 letter pages, matching its build receipt; no encryption, JavaScript, images or embedded files were found. The 31 displayed numbered equations, all seven lemmas, theorem scope, author/ORCID, date/version and bibliography match the source.

| Page | Content reviewed | Result |
|---:|---|---|
| 1 | Title, author/ORCID, version, abstract, AI/unrefereed/license disclosure, introduction | Legible and correct global same-target credit |
| 2 | Chronology, exact full Bell definition and theorem | No clipping; all normalization conditions visible |
| 3 | Incidence/tree proof and integration convention | Equations/signs and section transitions clean |
| 4 | Exact subset transfer proof and invariant quotient definition | All forest cases and +1 coefficient are readable |
| 5 | E/F invariant dimension and epsilon tensor basis setup | No missing glyph or mathematical sign defect |
| 6 | Leading words, explicit antisymmetrization, b identities, Φ and degree counts | Formula normalization preserved |
| 7 | Catalan sum, symmetry, determinant character and Gaussian setup | Dense text fits and equations are clear |
| 8 | Completion, lowering proof and raising definition | Pair order and Gaussian normalization readable |
| 9 | Raising continuation, row quotient, ordered factorization, quotient determinant, lifting start | Correct order visible; no layout defect |
| 10 | Constant kernel, Gauss descent, n=1 and source attribution | Ring argument and source locators intact |
| 11 | Dated addendum, evidence/provenance and review status | Content matches source; P3 pending-state wording below |
| 12 | All 12 bibliography entries and license footer | Links/citations/typesetting intact; no overlap or clipping |

No fresh TeX edit or compile was performed by me. The prior compile/export receipt has the same current source/PDF hashes; independent full-page viewing verifies the actual supplied export. No P0–P2 copyedit or visual defect was identified. The only required P3 prose change is the durable release wording below.

## Historical edition, authored evidence and stages

PACKAGE_CHECK_RESULTS.json records actual `git ls-tree -r` of the complete problem subtree at the original head and `git show` for every one of its ten files. The actual subtree contains exactly those ten files and no executable/checker/fixture/log. Each Git blob equals both submitted snapshot and included original copy and matches its recorded hash/length. Historical AUDIT's RECONSTRUCTED_PROOF.md name maps to the exact PROOF.md bytes, not to the new TeX/PDF. The historical CSS bibliography range correction is reported without inventing an unavailable earlier artifact identity. Historical source identities and no-match conclusions remain dated records; no omitted historical program was replayed.

All 76 actual authored evidence files were checked byte-for-byte against EVIDENCE_INDEX source paths and recorded hashes/lengths. FULL_EVIDENCE_INVENTORY.json records the complete UTF-8/JSON content inventory; there are no source-copy symlinks or binary bodies. Their mathematical, priority and preparation stages are distinguishable. Old family PASS labels and root dispositions do not purport to approve the new paper. Receipt paths/hashes for excluded raw objects are provenance metadata, not redistribution of those objects. Whole report/derivation reading, machine inspection of complete JSON outputs and fresh re-execution were used according to each artifact's role.

The input CURRENT_REVIEW_STATE.json truthfully says PENDING_NEW_WHOLE_01, publication_ready=false and no submission/publication. That is an appropriate input gate. This review does not mutate those records or interpret an earlier stage's acceptance as current publication approval.

## Actual finite evidence and independent replay

I read both complete fresh scripts and ran byte-identical copies only under my ignored sources/raw/rerun. Bytecode generation was disabled. The invariant all-mode replay checked max-m 6, max-n 7 and max-r 6 using exact standard-library arithmetic. It exited 0 in 0.584 seconds and reproduced every nonvolatile saved result. The transfer all-mode replay exited 0 in 20.534 seconds and reproduced all 52 named substantive records from the three saved modes, including negative controls; every saved output receipt hash/length matches. REPLAY_COMPARISON.json and RERUN_RECEIPTS.json record these facts.

The first transfer replay under the bundled interpreter failed because SymPy was absent. The retry used the already installed fresh family's pinned Python/SymPy environment without changing it, while executing my own copied script and writing only my own outputs. This is an environment-selection failure, not a hidden checker failure; its actual stderr is retained.

The direct graph route uses DSU cycle/component checks; the exterior route uses explicit bit-mask wedge signs; the Gaussian route constructs lowering, substitution and raising separately and reconstructs full exterior columns. Generic symbolic T determinants through n=3, exceptional signed/singular/zero-row-sum cases, the n=4 full Bell/14-dimensional image and wrong-order/wrong-normalization/X-only fault controls pass. Direct n=4 graph enumeration visits all 65,536 subsets for every input state under star, path and last-root templates (2,949,120 visits total). Separately, all 16 labelled four-vertex exterior tree products are checked. This is the precise meaning of tree-choice evidence; it is not a new claim that direct graph enumeration traversed every possible representative assignment. The all-n tree independence is proved by the unimodular argument. Finite checks remain supplementary and establish no exact all-n multiplicity/cofactor claim.

## Actual archive and metadata audit

The actual archive has 93 unique sorted safe ASCII relative POSIX names: 92 payload files plus MANIFEST.json. Every member is a regular Unix 0644 file with the fixed 2026-10-13 timestamp, create_system=3 and valid CRC; there are no traversal names, symlink members or nested archives. Every extracted member equals its corresponding current file, and all 92 payload hashes/lengths match the noncircular manifest. The manifest omits its own payload hash. ARCHIVE_PIN externally pins the manifest/ZIP and is deliberately excluded from the archive; README's navigation uses this external-sidecar design, while the manifest states the exclusion explicitly.

Without executing the candidate builder or modifying the candidate, I independently assembled the sorted members with the specified timestamp/mode/DEFLATE parameters into a separate in-memory ZIP. It exactly reproduces 316215 bytes and SHA-256 f235148c8b191160ae557c45e6d214a48508d98f2a8cc91c4de984546f93480b. The same-implementation determinism limit in the builder is honest.

The actual payload contents were scanned, not merely exclusion declarations. Types are 50 JSON, 26 Markdown, three Python, three stdout, three stderr, three text, one PDF, one TeX and three extensionless files. All files except the authored paper PDF decode as UTF-8. The PDF has no embedded body/image/attachment. There are no raw third-party PDFs, full extracts, HTML bodies, images, caches, environments or bytecode in the members; no encoded binary/raw body was detected in textual contents. The only duplicate-byte group is the three intentional empty stderr receipts. Source-record hashes and raw-path references were checked as metadata rather than mistaken for included raw payloads.

Parsed `.zenodo.json` equals exactly `zenodo_metadata.json["metadata"]`. Neutral title, sole author/ORCID, date/version, CC BY 4.0, AI/unrefereed disclosure, same-target DOI citation, qualified chronology and theorem/priority limits agree with TeX/PDF/README. The metadata forms are local drafts and no deposit or DOI for this package exists. One durable-description wording change remains below.

## Required actionable issue

**P3 — Pending-review operational prose will be stale in the final submission copy.**

Primary location: `paper/forest_transfer_catalan.tex:372`, final paragraph of Section 7, PDF page 11. Related public-prose locations: `README.md:16` and `README.md:22`; `SUPPLEMENT.md:18`; `zenodo_metadata.json:13` and `.zenodo.json:12` (description field).

The current statements about a pending current whole-paper/package review and local draft status are accurate for this frozen input. If retained verbatim in an accepted final paper or deposited description, they keep saying the current review is pending even after a clean terminal review. This is not a mathematical defect and is not a reason to reinterpret old stages as peer review; it is a lifecycle inconsistency in intended durable release prose.

Required fix: replace the present-tense pending/current-draft assertions in the durable paper/README/supplement/public description with stable wording that points to the supportkit's dated, stage-specific review history and frozen input identities, while retaining the AI/unrefereed/no-human-or-formal-certification disclosure. For example: “Version 1.0 is an unrefereed exposition. The supportkit records dated preparation checks and stage-specific AI reviews, each identified by its scope and frozen inputs; those records are not human refereeing or publication records.” Keep the actual dated preparation log/report and frozen October 9 evidence unchanged. Maintain truthful machine input-state flags during review rather than declaring readiness by deletion of prose. Preserve metadata-object equality, recompile/re-export the changed TeX, regenerate pins/archive, and obtain a NEW full review of the resulting complete artifact set before terminal promotion. This is an artifact review requirement, not an extra human authorization request.

No other actionable P0–P3 issue was found.

## Execution boundary and strongest result

All writes by this reviewer are under reviews/package_01. There was no candidate/original mutation, Git index/branch/remote operation, PR/service/queue/publication mutation, external individual communication, outreach preparation, subagent spawn or other-worker messaging. Public GET requests and read-only Git commands supplied evidence. The shared branch remains main. Original and candidate pins are rechecked immediately before the final report seal.

The mathematical theorem is independently verified for the exact claimed all-n scope. The source-credit and archive claims are checked against actual primary bytes, Git blobs and payload contents. The remaining gap is a single P3 durable release-wording repair and review of its resulting frozen artifacts. Worldwide priority and independent discovery remain UNKNOWN, and the paper correctly makes no such claim.
