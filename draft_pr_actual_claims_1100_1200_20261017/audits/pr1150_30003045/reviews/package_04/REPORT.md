# PR1150 whole-package adversarial review 04 — frozen edition 4

**Disposition: CLEAN_PASS. No remaining operative issue, including a minor issue, was established within this completed review.** The explicit counterexample satisfies the exact original hypotheses and excludes the full three-summand sum. The positive n=0 boundary and repaired exponent-one statement are sound. The frozen package authenticates, runs offline and rebuilds exactly. All three earlier nonclean package reviews are correctly preserved as historical reviews of their own editions, with their operative findings repaired here.

This is an internal AI review of specified bytes. It is not external human peer review, proof-assistant certification, a novelty/firstness/global-openness certificate, or publication permission. Completion is 100% of this bounded review, not of an exhaustive literature search. Completed 2026-10-18 UTC.

## Independent assessment and exposure order

I first created this folder and wrote `.gitignore`, covering private/, sources/, tmp/, rendered/ and __pycache__. I read the workspace AGENTS.md and PDF skill. Before opening any root, earlier or sibling verdict report, I read ALL 13,263 bytes of publication/main.tex; rendered and viewed ALL four frozen paper pages; independently fetched the original EMS PDF; read the complete Laghribi contribution printed248–251; and rendered and viewed all four corresponding PDF pages34–37. I reconstructed and attempted to falsify the exact claim at that stage.

INITIAL_ASSESSMENT.md was sealed at **2026-10-18T00:13:46.251040+00:00**, **6,942 bytes**, SHA256 **64796ae52046edf5a493e26eaf57c8ce6ab03031a85f6ef281d97abbf59be463**. INITIAL_SEAL.json records the input identities and actual read order. The assessment remains unchanged. Its provisional mathematical pass preceded the historical verdict reading.

The task brief supplied the construction, expected identities, credited antecedent, historical repair topics and attack surfaces. This is supplied-candidate independent checking, not blind rediscovery or perfect causal isolation from the briefing. The initial six mathematical/priority families had parent context available; their narrower statements about unopened files do not establish absence of related context. REVIEW_INDEPENDENCE.md and the paper disclose that limitation accurately.

After sealing my assessment I read the final proof, complete original/intermediate/final diffs, original historical prose and acceptance, current sixteen-file PR edition, root mathematical and priority assessments, all six complete mathematical/priority family reports, their core assessments, detailed read scopes and logs, all three preceding complete package reports, repair notes, provenance and relevant metadata. I inspected the actual arithmetic, all operative runners and builder, and six historical receipt-checker scripts. All archive JSON records were parsed and authenticated programmatically; that is not called semantic reading of every serialized query, embedded patch or source record. INSPECTED_INPUTS.json gives all143 source members explicit exposure labels; PRIMARY_READ_SCOPE.json separates my own source reading from prior reviewers' larger scopes.

After my own computations, controls, historical accounting and scope record were complete, the parent reported its separately passing edition4 checks and asked me to finish and seal. That message supplied no new mathematical evidence and did not precede my findings. I communicated only with the parent, not a sibling, shard or outside person. No outreach was prepared.

## Exact claim and universal mathematical check

OWR5/2016 Question2, printed251, asks equality of the composite Kato kernel with the sum of the L/F, K/F and F(B)/F kernels for finite purely inseparable L/F, separable quadratic K/F, and bilinear Pfister B remaining anisotropic over L. Printed248 defines F(B) through the **projective quasilinear quadric** of B(v,v). There is no exponent-one, dimension-at-least-four, smoothness, geometric-reducedness or positive-dimensional requirement. The binary positive-fold case is admissible. A counterexample at its allowed index n=1 refutes the universal equality; no failure at every index is necessary or asserted.

Take F=F2(b,z,s,t), with four independent variables, beta^4=b, L=F(beta), theta^2+theta=s^-1, K=F(theta), and B=<1,t>_b. The odd b-valuation proves b nonsquare, degree4 and exponent exactly2. The odd negative s-valuation proves the Artin–Schreier field genuine, including over the later completion. The independent t-valuation proves B_L anisotropic. A separable extension cannot introduce a new purely inseparable square root. The binary projective quadric lies entirely in its Y-chart, whose ring F[X/Y]/((X/Y)^2+t) is the field F(gamma), gamma^2=t. It is integral and zero-dimensional; geometric reducedness is neither true nor required. Thus M=LF(B)=F2(beta,z,s,gamma), and LK(B)=M(theta), of total degree16 over F.

The natural identification H2^2(E)=Br(E)[2] sends u dlog(v) to precisely the characteristic-two quaternion [u,v), with i^2+i=u, j^2=v and ji=(i+1)j, compatibly with extension. Milne's finite-Galois crossed-product theorem applies over arbitrary, including imperfect, fields. For the quadratic group, a normalized two-cocycle is specified by its invariant scalar c at the nonidentity pair; a coboundary changes c by a norm. Consequently the ENTIRE separable quadratic relative kernel is {[s^-1,c):c in F*}. This does not assert that an arbitrary Brauer class is a single quaternion. The splitting/norm criterion is independently confirmed by the official Voight2021 characteristic-two theorem. These are standard foundational inputs, not claimed new results or full foundational reproofs.

In L, put f=1+beta^2 z and h=beta^2 z/f. Since d(beta^2)=0, dlog(f)=h dlog(z), and h^2=bz^2/(1+bz^2). Applying the logarithmic Artin–Schreier relation twice gives

    xi_L = [s^-2,f)_L = [s^-1,f)_L,

for xi=s^-4 bz^2/(1+bz^2)dlog(z). Hence xi dies over LK. These are quotient/cohomology equalities. The actual fixed-logarithmic-basis code retains the generally nonzero exact correction d(s^-2 h); wp is never treated as a scalar-linear operator on an arbitrary differential presentation.

If xi=x+y+w were in the full three-kernel sum, write y=[s^-1,c) for an arbitrary c in F*. Restrict to M: both x and w vanish. Thus [s^-1,f/c)_M=0. This step includes the whole third Pfister kernel; a two-field nonsplitting assertion alone would not suffice.

Complete to D=k'((s)), k'=F2(beta,z,gamma). For pi=theta^-1,

    pi^2+s pi+s=0,   conjugate(pi)=pi+s,   N(pi)=s,
    N(A+B pi)=A^2+sAB+sB^2.

For nonzero coefficients with a=v_s(A), b'=v_s(B), the valuations2a and1+2b' have opposite parity and cannot tie. The middle valuation1+a+b' exceeds their minimum: split a<=b' and a>=b'+1. Therefore the norm valuation is min(2a,1+2b'). The cases A=0 or B=0 follow directly from the same formula; A=B=0 is excluded by the nonzero norm domain. A unit norm has a=0 and b'>=0 and square residue. This direct argument needs no perfect residue field, defect assumption or norm-surjectivity claim.

Every c in F*=k(s)*, k=F2(b,z,t), has c=s^r c0(1+O(s)), r any integer and c0 in k*. Multiplying f/c by N(pi^r)=s^r makes a unit norm, including negative r. Its residue forces f/c0 in k'^2. Let

    S=k'^2=F2(beta^2,z^2,gamma^2),
    R=F2(beta^4,z^2,gamma^2).

Since k=R(z) has degree2 over R, every rational c0 has a unique expression u+vz with u,v in R, arbitrary rational denominators included. The odd z^2-valuation shows z is outside S. Comparing 1,z coefficients in f=q(u+vz), q in S*, gives qu=1 and qv=beta^2. Thus u cannot be0; v=0 also fails immediately; otherwise beta^2=v/u belongs to R. Its odd beta^2-valuation contradicts the even valuations in R. This excludes EVERY c, and also proves xi nonzero. All construction denominators are nonzero by algebraic independence. No finite enumeration establishes this universal conclusion.

At n=0, Artin–Schreier roots cannot first arise in purely inseparable or rational extensions. An anisotropic quasilinear form of dimension d>=2 has projective function field purely inseparable quadratic over a rational field in d-2 variables; the binary case has no rational variables. Separable extension preserves its anisotropy by linear disjointness. A root in LK(B) therefore descends to KL and then K; the other two individual degree-one kernels are zero. This gives exactly the stated positive boundary. The separately assigned zero-fold F(B)=F convention is handled without inventing a function field for an empty projective quadric.

The adverse variants are consistent. Choosing Pfister slot z kills dz and absorbs xi. If b=u^2 and beta^2=u, the computation is over L, where du=0; the descended second slot proves membership in the L+K kernel sum. It does not prove the old single-symbol equality over the base, where d(1+uz)=u dz+z du. Failure of that representative shortcut is not itself asserted to decide cohomology-class inequality. The exact original-to-intermediate diff changes only this ancillary bullet; intermediate-to-final changes only exact prior credit. FINAL_PROOF.md/current COUNTEREXAMPLE.md are identical:12651 bytes, SHA2567808df31d74049fe649231a905e6dc330929caa87c86dca6ebfa6dcfb6d6c275.

## Primary dependencies, antecedent credit and limits

I independently fetched all six primary PDFs successfully, including fresh Milne bytes. These match the package's relevant historical source identities. My actual reading is bounded as follows:

| Source | Own reading and visual scope |
|---|---|
| Original EMS OWR report | Complete Laghribi contribution printed248–251/PDF34–37, all four pages viewed; no unrelated whole talks claimed |
| ALO author manuscript, dated15August2019 | Complete PDF1–5 and8–9: introduction, Definition1.3, Theorems1.4–1.5, opening fixed-basis definitions, Section3 setup and complete Lemma3.1 proof; pages3,4,9 viewed. Not all28 pages or the full Theorem1.4 technical proof |
| ALO2016 author manuscript | Complete PDF1–4: introduction/main statements/corollaries, exponent-one and affine conventions; pages3–4 viewed. Not complete technical proofs or final journal comparison |
| Chapman–Queguiner-Mathieu arXiv2111.15251v3 | Complete PDF2–3 symbol/Kato/Brauer conventions; page3 viewed. Not unrelated main theorem/final publication |
| Milne CFT v4.03,6August2020 | Complete PDF140–146/printed131–137, relative kernel and general-field crossed-product construction/proofs through3.14 plus3.15; page146 viewed. Not full book or all foundations |
| Voight official2021 Chapter6 | Complete PDF7–8/printed91–92, surrounding6.4, full norm theorem6.4.11, short proof pointer and neighboring splitting lemma; page8 viewed. Not full chapter/book or reproof of the cited exercise |

PRIMARY_RETRIEVAL.json and PRIMARY_READ_SCOPE.json give bytes/SHA and scopes. In particular the ALO2019 PDF is406587 bytes/SHA6bee75060598e61159fb78dd1f3167c5dfc3de24611d8af280a791bb1f8a5b03; Milne is2072714 bytes/SHA50d79af78250a9f1117ad9d337e0b231704a533fc707966ed1bfa52e13d498f5; the official Voight chapter is252106 bytes/SHA734db57499918d0d90100d1d839255fa6fc074c2b617ebc7bc112c254313bf83. Retention and hashes establish identity, not mathematical truth or whole-document reading.

Definition1.3 with n=m=1, f0=1 and f1=z gives the sole nonzero term (beta^2 z/(1+beta^2 z))^2 dlog(z). Multiplication by a=s^-4 is exactly xi. Lemma3.1 gives the antecedent mixed vanishing; Theorem1.4's power condition holds with l=2>1. Since s^-4+s^-1=wp(s^-2+s^-1), the quadratic field agrees. This exact generator and mechanism are prominently credited in the abstract, introduction, final proof, README, PR description and metadata. No firstness or new generic mixed mechanism is asserted. The direct third-kernel survival proof is actually supplied.

The predecessor imposes exponent-one square-root multiquadratic extensions. Its affine field differs from the projective field by a rational variable, which does not change the relevant restriction kernel. No exponent-two positive theorem is silently inferred. The current Milne citation correctly says items3.11–3.14 rather than calling both intervening lemmas theorems.

Fresh direct Crossref retrievals failed (one timeout and one406), and the web endpoint was unavailable. I do not claim a fresh Crossref body. The primary author's live publication list independently confirms Journal of Algebra542(2020),249–276 and449(2016),635–659. Earlier successful publisher-deposited metadata claims are preserved as authenticated historical evidence. BIBLIOGRAPHY.json records this distinction.

I read all three complete historical priority reports and their exact read-scope records; I did not repeat their168 query inputs or read every source they mention. The counts20+53+47+48 include overlaps and low-yield searches, not168 distinct relevant papers or exhaustive coverage. Final ALO2020 journal-body comparison, full adjacent nonnormal2020 DOI10.1080/00927872.2019.1686510 and transfer2022 DOI10.1016/j.jpaa.2021.106930 bodies, the unlinked2026 lead, and broader screened2025/2026 bodies are not newly cleared here. The separate reported Sobiech correction concerns a pure-extension differential-kernel formula not used by this direct norm argument; I did not independently re-audit its complete context. The paper accurately preserves these limits and asserts no absence-of-prior-work theorem.

Extensive AI assistance, initial inherited parent context, unrefereed status, no external human peer review and no proof-assistant verification are stated. These limitations do not disappear because the package passes internal review.

## Complete package, execution and path controls

Safe extraction rejected unsafe absolute/traversal/duplicate names and nonregular payload types before writing only within my ignored private area. The source has143 regular payload members:142 nonself-manifest entries comprising11 fixed base files,130 authored audit members and provenance, plus the self-excluded manifest. The kit has5 members. Every source-manifest and authored-allowlist pin matches. All71 JSON members parse; the separately generated private PACKAGE_RECEIPT also parses. The only distributed PDF is the authored paper. No copied third-party body, extract, render or raw service response is included; factual source identities and custody pointers are distinct from those omitted bodies.

The ordinary and optimized outer replays both match the complete frozen4176-byte receipt exactly, SHA25644d3f26d4434929c60698b9bcd8da0b12bf711412f2b691f0847ec7fe7efd156. I additionally ran both modes with socket construction, connections and address lookup disabled through an inherited Python guard, including every child process; both complete outputs remain exact. Each replay authenticates130 authored members and the current16-member edition, matches four complete positive program outputs and requires18 actual computed wrong-result failures.

I also independently executed the two programs directly in both modes and all nine wrong modes twice. DIRECT_MATH_EXECUTIONS.json records the actual22 process outcomes; raw diagnostics remain private. Positive symbol output is1313 bytes/SHA2c15e49d6e392649b56c1044e8dc914fa60f8c0584f22d319b79ead6cdb0845a; norm output is338 bytes/SHA6d9c613f25f0ae26239e157f914f4e41ccd5923cd23f976ef6a5777bc6d99614. All18 wrong-result processes fail through their own computed ValueError: CHECK FAILED assertions, with the unexpected-success fallback excluded. These are not invalid-argument exits or unconditional failures.

Actual code inspection confirms GF(2) parity-set polynomial operations, rational equality by cross multiplication, characteristic-two quotient differentiation, fixed-logarithmic-basis wp with exact correction, and the sparse Laurent/quadratic norm calculations for their stated uses. Explicit exceptions survive optimization. Counts agree with the prose:13 symbolic assertions,1023 bounded coefficient pairs,143 actual quotient derivatives,24 rational coefficient pairs and49 quadratic norm examples;961 valuation pairs,62 zero-coefficient cases and16 unit cases. The norm program's three alternative-normalization comparisons are computed sanity checks, not three extra failing processes. Finite diagnostics supplement the universal proof and do not decide Kato cohomology.

The builder was run ONLY in my private extracted source copy. Both ZIPs were actually regenerated. All six resulting release files match the assigned frozen bytes exactly, and the regenerated PACKAGE_RECEIPT matches the workspace receipt. The PDF is a pinned input; this does not claim a new TeX compilation reproduces timestamped PDF bytes. I did not run the workspace builder or recompile TeX. All four frozen PDF pages were personally rendered/viewed, and independent pdfinfo confirms title/author, four letter pages, no encryption/forms/JavaScript. Text, equations, references, ORCID, disclosure, margins and page breaks are legible without clipping or overlap.

The builder visibly preflights ALL THREE generated destinations—source ZIP, kit ZIP and receipt—before any output write. The validator rejects symlinks/ancestor aliases beneath distribution roots, existing nonregular destinations, and existing nondirectory ancestors. It uses unique temporary files plus atomic replacement for generated files, with the same validator at the write boundary.

I ran **62 separate path/integrity controls**, all passing:56 safe rejection cases and6 meaningful successful hardlink cases. PATH_INTEGRITY_CONTROLS.json and EXTRA_INTEGRITY_CONTROLS.json record them, with public reproduction scripts.

* In both ordinary and optimized modes, every one of the three generated-file destinations was occupied in turn by a directory, FIFO, socket or outside-target symlink. All reject before other output files change; outside sentinel contents are preserved. The records preserve other outputs' content hashes, inodes and modification times, so a byte-identical rewrite would still be detected.
* Output ancestors occupied by a regular file or valid-payload directory symlink reject. Valid-payload authored-directory aliases reject in BOTH runner and builder. Flat extra files/directories/directory symlinks, listed leaf aliases, missing listed files and unsafe allowlist traversal reject.
* Operative proof and baseline corruption are independently tested against BOTH runner and builder in both modes. Disagreeing deposit/metadata objects reject before output mutation.
* Six successful hardlink controls cover all three output files in both modes. Each outside target begins with bytes deliberately DIFFERENT from the generated payload. The builder replaces the output inode with the exact expected generated bytes while preserving the outside sentinel's contents, inode and modification time. These are meaningful preservation tests, not same-payload-only comparisons.

These62 controls are distinct from the18 mathematical wrong-result failures. No protection against malicious concurrent filesystem races or arbitrary future IO failure is claimed or inferred. No operative path-integrity issue remains in the stated static contract.

## Historical custody, edition boundaries and metadata

All63 available authored/input pins in the six mathematical/priority family receipts authenticate, and all six external root-recorded receipt seals match. Their163 private body/tool/history pins are intentionally absent from the extracted distribution. I inspected the historical checker code but did not run its full-private-source mode against absent files or rewrite sealed receipts. Full custody cannot be replayed offline without independently obtaining those sources. That is an expressly documented availability boundary, not a failed operative mathematical check or a claim that historical web execution has been reproduced. HISTORICAL_AUTHENTICATION.json records each available/omitted entry separately.

The original11-member input manifest and current16-member manifest authenticate their10/15 nonself entries. Current/family symbols code is identical. The standalone norm copy differs only in the corrected REPORT.md-to-COUNTEREXAMPLE.md docstring; its arithmetic and output bytes are unchanged. Original historical no-correction acceptance and13/25-check claims remain preserved and expressly superseded. Absent original programs are not represented as rerun. Intermediate12322-byte and operative12651-byte proof identities are clearly distinguished.

I read all three earlier nonclean package reports, authenticated their external receipts and pinned public evidence, and matched their report/receipt seals to the gate record. PACKAGE_REPAIR_NOTES explains all three and the subsequent fixes. Current tests confirm flat/ancestor alias rejection; the distributed proof reference; intermediate/final labeling; corrected Milne item label; all-output preflight/atomic replacement; and the later static destination/ancestor type checks. Historical edition receipts are unchanged, rather than retroactively relabeled clean. No old receipt is treated as authentication of new ZIP bytes.

A fresh read-only GitHub connector retrieval found PR1150 open and draft at **4e8e5db5c47fb879d97cb1a734a76fd59d8f633a**. Its exact changed-file inventory, all16 file bodies and4473-byte description match the frozen current PR edition, including body SHA628e37b879f9fa5ac4f5a0eb031f11ae5bce237aaa9bd84a0372595830fc2109. Direct HTTP access timed out first; that failure is recorded separately and is not called successful access. Original99f43020e142374629848e97113d354b43fd9f8e and first repairedf0e04d3ed92c3deea51813269e685311ee2b3fae are correctly historical. No PR action, review, comment or message was sent.

Production and portable metadata objects agree exactly; PDF/source/README/metadata payload copies agree; only the portable deposit's two relative payload paths differ. Title, Alec Kriebel, ORCID0009-0001-9320-500X,17October2026 date, version1.0.0, preprint type, CC-BY4.0, exact degree/index scope, older generator credit, diagnostic counts and review/access limits are coherent. No DOI or completed-publication state is invented. At the inspected checkpoint the gate identifies edition4 as unpublished with no earlier clean package review. This review supplies one clean assessment of the specified bytes; it does not satisfy a requirement for two successive new clean reviews by itself or authorize publication.

## Final unchanged six-file boundary and noncircular handoff

The assigned six files under publication/ match the supplied identities and remain unchanged. Every corresponding private rebuilt file is byte-identical:

| File | Bytes | SHA256 |
|---|---:|---|
| main.tex |13263|739e8dc4654df90d61b4e71d516537f8e3a4211595b53697eacd2075fe0c65e4|
| output/pdf/mixed-kato-counterexample.pdf |71463|01ef963f6dbebc0c3aa91bfb10f13d293c983a46238c4465ae53bf4db99f1c96|
| output/mixed-kato-counterexample-source-and-verification.zip |372851|368a3c539c2c40d2cf262104f4cbf39ff01fe346e2aed05842cbb4c3b616b329|
| output/zenodo-upload-kit.zip |419277|9cf52c3db68456bf1798f60c4df2a2d3a699fe8667405b76041b2b5f0c428f83|
| zenodo-metadata.json |3835|32f29280706b83c336031f40b1a29cc44bc124918dda83e1267ccac0d88eaabd|
| zenodo-deposit.json |4144|8071626dd0b8f94d38db640e4083447d24881e8c9abc24bf084d4cd299ea1391|

All review artifacts are outside the frozen archive. EXTERNAL_FINAL_RECEIPT.json pins this report and its evidence without pinning itself; no pinned artifact depends on that receipt's digest. Its byte count and SHA256 are delivered externally in the handoff. A subsequent HANDOFF_RECEIPT.json records that external receipt identity without changing or entering the frozen release. This avoids circular release attestation.

All writes and owned test mutations stayed under reviews/package_04. The shared checkout was read as main. No Git/ref/index write, workspace build, PR mutation/comment/message, production deposit, release, tracker action, or outside-human contact occurred. No publishing permission is requested.

**Strongest verified result:** the supplied n=1 example universally refutes the exact original three-summand equality, with valid n=0 and corrected exponent-one boundaries, accurate antecedent/review limitations, and an authenticated, offline-replayable, byte-reproducible current package. **Remaining operative gap identified by this review: none.** Literature/body-access and foundational-dependency limits remain exactly as stated above; CLEAN_PASS does not erase or resolve those boundaries.
