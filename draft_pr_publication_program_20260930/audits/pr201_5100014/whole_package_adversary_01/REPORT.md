# Independent whole-package adversarial review 01 — frozen PR201 package v1

## Verdict and exact target

**NOT CLEANPASS for the entire publication package. One substantive packaging/provenance finding (P2) remains in frozen v1. No substantive error was found in the current mathematical proof, theorem scope, source attribution, chronology qualification, author/AI disclosure, supplied portable controls, supplied pin maps, or PDF readability.** This is a scoped adversarial review, not a formal correctness certificate, novelty determination, historical independence certificate, or publication authorization.

Reviewed target: `../publication_package_v1` only. Its exact `PACKAGE_SEAL.json` is **81,493 bytes**, SHA-256 **c4a151a0129b6ad4aab7a7ee60bc506fbd498e40ef87938f9bf4ef5f7b7ca3e6**. Later packages and proposed repairs are outside this verdict.

The falsification plan was written at **2026-10-16T06:32:58.858460+00:00**, before reading prior favorable audit verdicts. The current manuscript was independently reconstructed before consulting earlier mathematical-family favorable verdicts. `INDEPENDENT_PROOF_RECONSTRUCTION.md` preserves the detailed deductions and challenges for every mathematical step; it is an integral companion to this report. Earlier audit conclusions were not substituted for proof. The intended contribution was assessed as the attributed alternative presentation of Ferudun's exact theorem; novelty, firstness and independence were not imposed as acceptance criteria that the package disclaims.

## F1 — P2: the promised original 24-file submission is not included

**Location.** `materials/README.md:22` says the audit payload preserves the immutable original 24 submission files with custody. Line 19 also says original programs are preserved under `audit/`. Manuscript source line 358 refers to the original submitted head preserved in the supplement.

**Evidence.** The ZIP and `materials/` exactly match and contain 209 entries, but there is no original submission directory and no `CANDIDATE.md`, original `SOURCE_AUDIT.md`, `turns.json`, `turn1_exact.py`, or the other corresponding original paths. `audit/ORIGINAL_SUBMISSION_CUSTODY.json` lists 24 paths with byte lengths, SHA-256 and Git-blob identities; it describes custody rather than supplying those files. Searching all payloads by original basename and exact size/SHA finds **23 unique original payloads absent**. The remaining `independent_review/independent_receipt.json` payload appears as a replay receipt elsewhere, which does not provide a coherent 24-file archive. `INTEGRITY_RECEIPT.json` records the missing-payload list.

**Effect.** A reader of the self-contained ZIP cannot inspect the archived candidate, the original source-audit wording being corrected, original author/reviewer programs, turn record, or original manifests as promised. Historical original-file custody checks cannot be reproduced solely from this package. This does not invalidate the current theorem or portable controls. A manifest cannot detect a promised input never added to it.

**Repair required before treating a revised package as complete.** Include all 24 original files in their original relative layout within a clearly labeled immutable historical directory, authenticated against the custody size/SHA/Git-blob records. Keep the current manuscript, metadata and source correction authoritative over superseded historical wording. Rebuild the root manifest, ZIP and external seal and give that new *complete package* a fresh whole-package review. Root acknowledged this omission during the review. Any later repair has not been reviewed here and does not change this frozen-v1 finding.

## Mathematical assessment

The strongest result verified by the written argument is exactly: a>b>0, 0<lambda<b², a fixed proper nondegenerate confocal elliptical caustic with translation of exact least order N=2m, odd m>=3, and every fixed finite real M imply phase independence of the signed outer-tangent polygon area times its signed pedal area. Primitive stars, reversal, zero and negative pedal area survive. Feet are on entire boundary tangent lines. Other parities, moving M, arbitrary repeated lists, unsigned face area, circular boundaries, hyperbolic/degenerate caustics and general nonconfocal pairs are not asserted.

The companion reconstruction independently checks:

1. Four distinct transverse finite E∩C branch points, connected smooth genus-one cover, branched involutions and a translation of *exact* order N. A smaller flag order would contradict least period. Nonidentity translations act freely.
2. Central inversion preserves the real direction component and commutes with T. The invariant-metric circle argument gives I=T^m without assuming winding numerator one; equality extends globally from the real circle.
3. The free quotient is genus one and unramified. Original infinities give at most two quotient pole points. Adjacent distinct and coincident infinite vertices are excluded separately, so A has only possible simple poles. Directed chord positivity holds for stars. Reversal rules out a globally constant A. Riemann–Roch then forces two genuinely distinct simple poles and L(D)=span(1,A), without assuming the two infinity orbits are distinct in advance.
4. The rational foot map is regular at original infinities: the leading normal has nonzero bilinear norm. Its only finite poles are four simple isotropic-normal contacts. They are common tangent flags fixed by sigma, but lie off E∩C, so pi is unramified there. The proof correctly distinguishes pi from the chord projection rho, which is branched at common tangencies.
5. Odd-half-period congruence 2k=1-m places every foot-pole orbit above the original infinity support. Exact order makes the sigma-fixed indices precisely 0,m. Every contact flag is either sigma-fixed or T times one, making {0,1,m,m+1} exhaustive. At m=3 the only cyclic adjacent singular pairs are still (0,1),(3,4). Parallel residues cancel every potential double pole, including special M that kills a residue.
6. Reversal acts with the same fixed M, so B_M=c_M A+d_M has d_M=0. No area or c_M is divided by. Zero and negative pedal areas create no hidden exception.
7. Polarity identifies W=[a²u:b²v:w] with the actual outer intersection. The w=0 lines have distinct finite opposite endpoints, unramified rho and simple W poles; adjacent W's cannot both be infinite. The congruences 2k=m-1 and 2k=m+1 produce sigma- and tau-fixed representatives in the two possible supports. These supports are disjoint since 2j=1 is impossible modulo even N. The relevant finite vertex lists are palindromes, whose signed areas vanish, cancelling every simple pole of AA'. Compactness proves constancy. Thus Section 4 supplies the narrow dependency directly rather than inheriting unexamined details of a broader published proof.
8. Strict inner containment excludes parallel real outer tangents; real normal norms are positive. The radial coefficient has the displayed sign and factor 1/8. Central pairing removes the linear term without dividing by a possibly vanishing curvature-weight sum. Radiality alone is correctly distinguished from phase invariance. The least-period caveat and repetition scaling are necessary and correct.

No unsupported central claim was accepted merely by relabeling it. The historical Euclidean reduction is expressly partial/blocked at two scalar phase invariants and is not counted as another complete proof. The current complex proof closes the gap. No mathematical repair is requested on this evidence.

## Primary sources, positioning and disclosure

The neutral title, abstract, theorem framing, README and deposit metadata consistently describe an attributed alternative proof. The exact overlapping theorem and ancillary results are prominent. There is no current theorem-novelty, first-proof, new-general-method, absolute-priority or certified-independent-rediscovery claim.

- The [journal RGK source](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Section3.4/Table4 printed p.346, and [arXiv v11](https://arxiv.org/pdf/2004.12497v11), Table4 printed p.6, give the outer-pedal product row for N=2 modulo4 and all M. They define signed shoelace areas. Neither table literally prints least period, as the current correction correctly says. The registered arXiv title, its shorter PDF title and distinct journal title were checked and correctly distinguished.
- The primary [Chávez-Caliz paper](https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf), Theorems3,6, gives the even-period original/outer product for concentric transverse conics; its Section2 supplies the flag framework. The confocal pair satisfies the transverse hypothesis, and the present manuscript independently verifies the narrower needed result.
- Both actual Ferudun PDFs were freshly retrieved as nonexecutable primary literature, streamed through text extraction, and not retained as full texts. [Version1.0](https://zenodo.org/records/23087221), Theorem1, states the same proper-confocal, least-period, arbitrary-point signed-star theorem; Sections6–7 include radial dependence, the general six-period constant and repetition qualification. [Version1.1](https://zenodo.org/records/23088516) retains it. Actual PDF hashes and MD5 values agree with the official archive records; see `PRIMARY_PDF_RECEIPTS.json`. Shared central symmetry, isotropic poles, parallel residues and reversal support the manuscript's description of the difference as a quotient/divisor presentation, not a newly certified mechanism.
- The cited [Steiner offprint](https://doi.org/10.3931/e-rara-3816), printed pp.19–21, was inspected in the existing institutional primary scan/OCR cache, including direct visual review of those three printed pages. Equations26–29 support the classical quadratic radial coefficient. The manuscript supplies its own central-pairing algebra and does not assert a finite general curvature centroid when its denominator vanishes.

Fresh primary API reads independently confirmed all quoted chronology fields:

| Witness | Observed UTC |
|---|---|
| [GitHub PR201 creation](https://api.github.com/repos/AlecKriebel/Math/pulls/201) | 2026-10-01T05:18:49Z |
| [Zenodo v1.0 creation](https://zenodo.org/api/records/23087221) | 2026-10-01T16:56:14.316216+00:00 |
| [DataCite v1.0 registration](https://api.datacite.org/dois/10.5281/zenodo.23087221) | 2026-10-01T16:56:15.000Z |
| [Zenodo v1.1 creation](https://zenodo.org/api/records/23088516) | 2026-10-01T18:12:36.529602+00:00 |
| [DataCite v1.1 registration](https://api.datacite.org/dois/10.5281/zenodo.23088516) | 2026-10-01T18:12:37.000Z |

The live PR head matches original head 90bdb85235979f2ffa7496b9b689036654e55200. These currently served heterogeneous fields do not establish first public visibility, exclude earlier website disclosure, or establish independence. The manuscript accurately preserves those limits. `PRIMARY_HTTP_RECEIPTS.json` retains selected public bibliographic/chronology fields and hashes, not raw payloads.

I freshly read the original turns, queue-turn receipt, candidate revision and research log from that exact public head, executing no retrieved code. Each size/SHA matches custody. They support the statement that the original records one substantive author turn, budget5, and a scope-only original revision; see `ORIGINAL_PRIMARY_RECEIPTS.json`. They do not verify actual model/reasoning effort, which the manuscript leaves unverified. October16 additions are expressly dated later, and extensive AI use plus absence of conventional independent human refereeing or proof-assistant certification is disclosed. Sole-author/ORCID text agrees across source, PDF and metadata with the supplied author metadata.

The audit history's pending statuses, failed early hypotheses and corrected wording are explicitly historical under the README; manuscript/metadata/root correction govern. I did not treat intentionally preserved stage records as contradictory current verdicts. The absent original archive is F1, not a reason to rewrite originals silently.

## Integrity and portable reproduction

The new read-only `audit_integrity.py` verified all supplied integrity claims:

- **213** externally sealed package files, comprising **209** material files and four other payload/deposit files; all three upload pins.
- The root manifest's **208** self-excluded entries and exact coverage.
- All **209** ZIP names, uniqueness, safe relative paths, no symlinks, CRC validity, exact bytes equal to materials, and equality to the seal's ZIP map.
- Ten nested manifest/gate/input-custody pin maps: respectively81,12,8,2,16,9,8,142,43,104 entries. All referenced supplied files are present and match, including the nested manifests repaired before this first frozen review.
- Byte equality of the standalone LaTeX copies, exact metadata equality between materials/deposit/seal, and the deposit's three upload filenames.
- All six portability-provenance scripts: original and portable pins, exactly the stated runtime-path removal or byte identity, and retained expected-source pins. No unstated mathematical-code change.

The 209 material files total **1,252,206 bytes**, all UTF-8 textual authored package material: one LaTeX source,22 Python files, reports, JSON/JSONL, manifests and diagnostic streams. All Python files parse. No distributed third-party dependency implementation, full PDF/scan/OCR, downloaded executable, credentials or browser state was found. Portable entry-point code has no package-output write calls; historical scripts retain their expressly historical local/output conventions.

Only existing Python **3.14.6**, SymPy **1.14.0**, mpmath **1.3.0** were used. Dependencies were imported read-only from the assigned sibling directory with `-B` throughout; no installation or copying occurred.

1. The actual normal portable runner returned PASS and verified every208 manifest entry. All five exact jobs matched expected outputs: source area, exact geometry, independent axes, general-axis/repeated triangle, and classical controls. This reproduces the displayed M=(1,0) repeated-triangle products and154 explicit source-family conditions among other exact identities.
2. Selected optimized source and classical controls matched retained text/JSON. Both `--guard-false` and the preserved false40→41 product fixture failed normally and under `-O` for their intended errors, not missing files/dependencies. `SELECTED_REPLAY_RECEIPT.json` records return codes, output hashes and labels. Old assertion-based optimized PASS counts were not treated as validation.
3. A small85-digit physical replay covered (a,N,winding)=(2,6,1),(2,10,3),(1.0001,14,5),(5,22,9), plus the excluded repeated-odd list(2,6,2). Closure/tangency, direct feet, reversal and positive original/outer orientation passed. The eccentric high-winding lambda is approximately0.9999999957, inside the domain. Worst target relative spread was about1.25e-66; these are finite noninterval diagnostics. The excluded case correctly shows large arbitrary-M phase spreads.
4. N=10 winding3 has a computed radius approximately4.0799382975 giving zero pedal area to about3.2e-72 over three phases, positive area just below and negative just above. This exercises the signed-zero boundary without replacing the no-division proof. See `SELECTED_PHYSICAL_RECEIPT.json`.

The complete old physical sweep and historical suites were not repetitively rerun. This selected physical replay imports the inspected portable construction and is not another independently coded proof. Earlier selected outputs were compared to originals, not simply assumed from their labels.

## PDF/source consistency and readability

The sealed PDF is **76,350 bytes**, SHA-256 **22bea0c90116961321d6dcf64e4be55bd0af254356f9d7d6d6ac62787914e660**. It has six unencrypted letter pages, no JavaScript and14 embedded fonts. Every page was rendered and visually inspected. Complete extracted text and every mathematical display, conjugation bar, sign/index, scope statement, chronology and reference were compared to the source. No clipping, overlap, missing glyph, unreadable equation or unresolved reference was found. Render intermediates were removed after their hashes were recorded.

`PDF_INSPECTION_RECEIPT.json` records the scope. A clean TeX recompile and bit-reproducible build were **not** performed; complete visual/textual agreement and byte equality of the two source copies are the evidence. This is a reproducibility limitation, not an observed mismatch.

## Limits and disposition

F1 remains unresolved in frozen v1 and blocks a whole-package CLEANPASS. No mathematical repair is requested. This detailed analytic reconstruction plus exact symbolic and selected finite numerical controls is not proof-assistant certification; numerics are noninterval. Only Python3.14.6 was exercised, not every advertised compatible Python/platform.

The fresh source review checked decisive cited claims and primary records rather than reproducing every earlier negative search, every version, or every uninspected book. Historical coverage remains bounded. No universal absence, theorem novelty, firstness, actual model/effort or historical independence follows or is needed for the stated alternative-proof positioning. No outreach was initiated or prepared.

All writes were confined to this folder. No package/original/global file, PR, Git/ref/index/branch/checkout, Zenodo, Sheets, browser tab or open Brownian document was changed. No local Git command was used. A temporary filesystem-full error delayed the final report; root freed an already-authorized cache, after which the report and manifest were written. No completed mathematical check needed repetition.

**Assigned review completion:100%. Publication authority from this report:none.** Root retains gate/publication authority. The final safe authored allowlist excludes third-party full texts, dependencies, raw external payloads, temporary renders and private outputs. Later packages require their own complete review.
