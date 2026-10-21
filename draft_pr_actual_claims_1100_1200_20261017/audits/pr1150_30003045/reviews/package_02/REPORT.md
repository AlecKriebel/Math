# PR1150 whole-package adversarial review 02 — frozen edition 2

Completed UTC: 2026-10-18T00:04:24.258253+00:00

**Disposition: NEEDS REPAIR; not CLEAN_PASS.** One operative builder path-safety defect remains. No mathematical defect was found in the supplied counterexample, its full three-summand exclusion, its positive degree-one boundary, or its repaired exponent-one discussion. The released files themselves are intact and reproducible. This is an internal AI review of specified bytes, not external human peer review, formal proof verification, a priority certificate, or publication permission.

## 1. Actionable finding

### R1 — P2: Reject all output symlinks before any builder write

`publication/build_package.py` validates input paths carefully, but its output writes do not use the path validator before opening their destinations. `archive()` at lines26–28 calls `mkdir()` and opens `ZipFile(path,'w')` directly. Lines44 and46 use it for the source ZIP and upload kit. Only afterwards does line47 call `pin()` on those two paths. That detects a leaf symlink after its target has already been truncated and replaced. The receipt destination at the end of line47 is written with `write_bytes()` without any corresponding path validation.

This is demonstrated behavior, independent of a concurrent filesystem race. In separate copies of the fully authenticated extracted package, I replaced each of these three output files with a symlink to a private sentinel outside that extraction root:

| Output destination | Ordinary and optimized result | Sentinel after the run |
|---|---|---|
| `output/mixed-kato-counterexample-source-and-verification.zip` | exit1, late symlink error | overwritten by the367362-byte source ZIP, SHA256 `5d9dc5a8d19b4c79822c58461c018c6fafc8ae5eb0022f8c88c257c9f85bb2ea` |
| `output/zenodo-upload-kit.zip` | exit1, late symlink error | overwritten by the414513-byte kit, SHA256 `cf0965989388edd2d4fd9720eb10ff1dbe6af9fa60c376ddda5fb277b1831511` |
| `PACKAGE_RECEIPT.json` | exit0, reported success | overwritten by the30789-byte receipt, SHA256 `ad6292fae51760b80aca02d2d6db523290fe50c51d7b2da2ec873b5a0ac21eb9` |

All sentinel targets remained inside this review's ignored private controls area; no release or unrelated user file was touched. `CORRUPTION_PATH_CONTROLS.json` records each run, mode, actual exit, diagnostic and target-change result. The four late failures are not safe rejection controls. The two successful receipt runs contradict the intended rejection contract outright.

Preflight every builder output destination and every relevant ancestor within the distribution root, including source ZIP, kit ZIP and receipt, **before the first output write**. Preserve the stated exclusion of concurrent malicious races; no race defense is needed to fix these static cases. Add ordinary/optimized controls requiring both rejection and preservation of the outside sentinel. A check after writing is insufficient. Do not count these path controls among the18 mathematical wrong-result failures.

No other operative issue was established, including minor documentation/citation matters. The four findings from package01 are repaired in this edition: flat current-PR inventory rejection, input ancestor-symlink rejection, the standalone proof reference, intermediate/final proof identification, and the Milne item label all check as described below. R1 is an additional output-write gap, not a claim that those demonstrated input repairs failed.

## 2. Independence, seal and exact exposure

I began without inherited parent conversation history. The task supplied the candidate, expected release identities, current head and attack surfaces. This was adversarial independent verification of a supplied candidate; it was not blind rediscovery.

Before any root, previous or sibling verdict file, I read the entire13263-byte `publication/main.tex`, independently fetched the original EMS OWR PDF, read the entire Laghribi contribution printed248–251, and viewed all four frozen paper pages and all four original contribution pages. I then sealed `INITIAL_ASSESSMENT.md` at **2026-10-17T23:59:36.832363+00:00**:4044 bytes, SHA256 **`9b837792c51f8b5948796fa66a9d334972688484fc95b040010bb04a05e1e0b4`**. Its separate receipt pins that assessment; it does not rewrite it after later reading.

After the seal, I read the repair notes; entire operative final proof and exact historical/intermediate/final diffs; current16-file PR edition; all original11-file inputs (the unchanged original proof content is covered by final-proof reading plus complete diffs); root mathematical and priority assessments; all six complete mathematical/priority family reports; their detailed read-scope and independence disclosures; and package01's complete report. I inspected actual verification/arithmetic/builder and historical custody-checker code. All archive JSON/inventories were parsed and checked programmatically; hashing or extraction alone is not represented as semantic reading of every query or source body. `INSPECTED_INPUTS.json` records these distinctions explicitly.

The coordinator later read my local log and sent a message acknowledging the already-recorded output-symlink finding, asking me to finish this frozen review and describing a future repair. That arrived after my own seal and private reproduction; it supplied no mathematical evidence. I did not consult another current whole-package review or communicate with a sibling/shard or outside individual. No outreach was prepared.

## 3. Independent mathematical assessment and falsification

The target is the exact universal equality in OWR5/2016 Question2, with finite purely inseparable L/F, separable quadratic K/F and bilinear Pfister B anisotropic over L. The source's projective quasilinear-quadric convention is explicit. Neither exponent one nor dimension at least four is required. An admissible counterexample at n=1 refutes that equality; failure at every index is not claimed.

The construction has F=F2(b,z,s,t), beta^4=b, theta^2+theta=s^-1 and B=<1,t>_b. Independent-variable valuations prove b nonsquare, extension degree4/exponent2, the genuine Artin–Schreier field, and t nonsquare over L. Separable extensions cannot acquire a new purely inseparable square root. The binary projective quadric is the integral zero-dimensional scheme with chart field F(sqrt(t)); geometric reducedness and positive dimension are not source hypotheses. With gamma^2=t, M=LF(B)=F2(beta,z,s,gamma), and the full composite M(theta) has degree16 over F.

The natural H2^2-to-Br[2] identification uses precisely u dlog(v) mapped to the characteristic-two cyclic quaternion [u,v), with the displayed generator convention, and commutes with extension. The cyclic relative Brauer theorem applies over arbitrary, including imperfect, fields: a normalized quadratic two-cocycle is determined by one invariant scalar c; its coboundary changes c by a norm; its crossed product gives the fixed first slot. This does not assert that every arbitrary Brauer class is a single symbol. The splitting/norm criterion is valid for the genuine separable quadratic field used here. These standard facts were checked against the primary dependency passages below; they are established inputs, not a claimed new foundational proof.

In L, f=1+beta^2 z and h=beta^2 z/f have dlog(f)=h dlog(z) and h^2=bz^2/(1+bz^2). Two logarithmic Artin–Schreier relations give xi_L=[s^-2,f)=[s^-1,f), hence vanishing over LK. These are cohomology equalities modulo exact differentials. The fixed-basis implementation correctly retains the generally nonzero exact correction d(s^-2 h); wp is not being treated as a scalar-linear operation on arbitrary representative expressions.

For a hypothetical decomposition xi=x+y+w in the three individual kernels, the entire quadratic relative kernel has y=[s^-1,c) with **arbitrary c in F***. Restriction to M kills both x and w. It forces [s^-1,f/c)_M=0, explicitly including the added Pfister summand.

In D=k'((s)), k'=F2(beta,z,gamma), pi=theta^-1 satisfies pi^2+s pi+s=0, conjugate pi+s and norm s. Every element of D(theta) is A+B pi, with norm A^2+sAB+sB^2. For nonzero coefficients with a=v(A), b'=v(B), the valuations2a and1+2b' cannot tie, and1+a+b' is strictly greater than their minimum, by splitting a<=b' and a>=b'+1. Thus the norm valuation is min(2a,1+2b'). The zero-coefficient cases follow from the same formula. A unit norm has a=0 and b'>=0, so its residue is a square. This argument needs neither perfectness nor an unsupported defect/norm-surjectivity hypothesis.

Every nonzero rational c in k(s), k=F2(b,z,t), has leading term s^r c0 with r any integer and c0 in k*. Multiplying f/c by N(pi^r)=s^r gives a unit norm, including negative r, hence f/c0 in k'^2. Let S=k'^2=F2(beta^2,z^2,gamma^2), R=F2(beta^4,z^2,gamma^2). Since k=R(z) has degree2, every rational c0 has a unique expression u+vz with u,v in R, including arbitrary rational denominators. Since z is not in S, coefficient comparison in1+beta^2 z=q(u+vz), q in S*, forces qu=1 and qv=beta^2. The cases u=0 and v=0 immediately fail; otherwise beta^2=v/u belongs to R, contradicted by parity of its independent-variable valuation. Both A=B=0 and c=0 are excluded by the nonzero norm/scalar domain. All construction denominators are nonzero. This is a universal full three-summand exclusion, and also proves xi itself nonzero.

At n=0, purely inseparable and rational extensions create no new Artin–Schreier roots. An anisotropic quasilinear form of dimension d>=2 has projective field purely inseparable quadratic over a rational field in d-2 variables; binary d=2 is included. Separable extensions preserve quasilinear anisotropy by linear disjointness. Roots in LK(B) descend to KL and then K, giving exactly the stated degree-one equality. The paper treats an assigned zero-fold F(B)=F convention separately and does not invent the function field of an empty projective quadric.

The two adverse boundaries are correct. Replacing the independent Pfister slot by z kills dz. In the exponent-one variation b=u^2 and beta^2=u, the calculation is over L, where du=0; descent of the second slot proves membership in the L+K kernel sum. It does not justify a single-symbol equality in the base, where d(1+uz)=u dz+z du. Failure of that representative shortcut alone is not asserted to prove inequality of cohomology classes. The original-to-intermediate diff corrects only this bullet; the intermediate-to-final diff strengthens only exact antecedent credit. Final proof/current COUNTEREXAMPLE agree at12651 bytes, SHA256 `7808df31d74049fe649231a905e6dc330929caa87c86dca6ebfa6dcfb6d6c275`.

## 4. Credit, primary read scopes and remaining access limits

I independently checked the exact older generator specialization against ALO's dated author manuscript, not a search snippet. Its Definition1.3/Lemma3.1 supplies the mixed class with n=m=1, f0=1, f1=z and a=s^-4; Theorem1.4's power condition uses l=2>1. Also s^-4+s^-1=wp(s^-2+s^-1), giving the same quadratic field. The paper, operative proof, README, PR description and metadata prominently credit the generator and vanishing mechanism and refuse firstness for the class/example/target deduction. The direct third-kernel survival proof is supplied rather than inferred from the existence of a mixed term.

The bibliographic record is consistent: Crossref's publisher-deposited record gives Journal of Algebra542(2020),249–276, DOI10.1016/j.jalgebra.2019.09.012. Its2019 metadata creation date is not called publication. The preceding exponent-one statements and differing affine convention were checked; a rational extra variable does not change the relevant restriction kernel.

My own primary reading is narrower than the combined historical priority audit, and is reported exactly:

| Source | Actual text/visual scope in this review | Byte identity |
|---|---|---|
| Original EMS OWR5/2016 | Full Laghribi contribution printed248–251; all four pages viewed; no other complete talks claimed |514462; SHA256 `75a01e6e34988e672e0b6b48a56a3467ef7de59ee7fecc850a71e29110bf748c` |
| ALO2019 author manuscript | Entire pp1–4 and8–10, including full Definition1.3/Theorem1.4 and complete Lemma3.1 proof; pages3,4,9 viewed; no complete28-page proof audit |406587; SHA256 `6bee75060598e61159fb78dd1f3167c5dfc3de24611d8af280a791bb1f8a5b03` |
| ALO2016 author manuscript | Entire pp1–5, including exponent-one statements and affine/bilinear definitions; no entire proof or final publisher comparison |380905; SHA256 `f6fd774bef7afe291a24ea87d253ef3548cdfb070c29793b1482ed1932df5507` |
| Chapman–Quéguiner-Mathieu explicit arXiv2111.15251v3 | Entire pp2–3, symbol convention/cohomology identification; p3 viewed; no unrelated theorem/final-publication audit |181281; SHA256 `3ab10955c9511e7a8460ad293899fcd71a5a4e1f0a1d4fd0834e90efc08f428c` |
| Milne CFT v4.03 | Entire PDF140–146/printed131–137, relative definition through crossed-product construction and theorem/proofs; PDF144–146 viewed; no full-book audit |2072714; SHA256 `50d79af78250a9f1117ad9d337e0b231704a533fc707966ed1bfa52e13d498f5` |
| Voight official2021 Chapter6 | Entire PDF7–8/printed91–92, including full norm theorem6.4.11 and short proof pointer; p8 viewed; no full-book/dependency audit |252106; SHA256 `734db57499918d0d90100d1d839255fa6fc074c2b617ebc7bc112c254313bf83` |

The original, both ALO manuscripts, Chapman version and official Voight chapter were freshly downloaded. My direct Milne download returned406; web opening succeeded, and I independently read/rendered a copied pre-existing primary PDF from the norm family's ignored source custody, matching its pin. This is not called a fresh successful Milne byte retrieval. Primary bodies/extracts/images and raw metadata remain ignored. `PRIMARY_RETRIEVAL.json`, `PRIMARY_READ_SCOPE.json` and `BIBLIOGRAPHY_CHECK.json` record identities and boundaries.

I reviewed all three historical priority reports, root reconciliation, detailed read-scope records and claimed query-input counts20+53+47+48=168. I did not repeat168 searches or reread every cited paper; those counts include overlaps and low-yield work and are not168 relevant works or an exhaustive literature certificate. Authenticating retained receipts does not independently reproduce past search execution or prove that every retained source was read.

Final ALO2020 typeset-body comparison and full adjacent nonnormal2020/transfer2022 bodies remain disclosed access limits. This review does not newly clear them. The unlinked2026 lead and2025 experimental-HTML/version dating caution remain in the supplement. I did not independently redo the separate Sobiech-correction literature audit; the supplied direct norm proof does not invoke that disputed pure-extension differential-kernel formula. No firstness, worldwide continued openness, causal independence, or absence-of-prior-work conclusion follows from these limits.

Extensive AI use, inherited context in the initial six families, lack of perfect isolation, unrefereed status, no external human peer review and no proof-assistant certification are candidly stated. Historical family claims about unopened files are qualified by the global inherited-context disclosure rather than expanded into claims of perfect information isolation.

## 5. Entire package and reproduction

Safe extraction independently checked unique nonabsolute/nontraversing ZIP paths, absence of directory/symlink members, and regular-file modes before writing. The source archive contains139 members:138 nonself manifest entries, including126 explicit authored audit members,11 fixed base members and provenance, plus the manifest. The kit contains5 regular members. Every manifest entry matched actual bytes/SHA. No third-party body, extract, render or raw service response is distributed; factual source identity/inspection records are distinguishable from those omitted bodies.

The extracted package replay was run with networking disabled through inherited Python socket guards. Both ordinary and optimized outer runs succeeded, agreeing exactly with the frozen replay record. Each authenticates126 authored members and the current16-file edition, runs both exact algebra programs normally and optimized, matches all4 full output byte strings, and observes18 actual computed wrong-result failures. These failures arise from nine false algebra/differential expectations in two modes, not unconditional failure fallbacks or mere invalid-argument rejection. The runner requires the precise CHECK FAILED ValueError and excludes unexpected-success fallbacks.

The symbols output is1313 bytes, SHA256 `2c15e49d6e392649b56c1044e8dc914fa60f8c0584f22d319b79ead6cdb0845a`; the norm output is338 bytes, SHA256 `6d9c613f25f0ae26239e157f914f4e41ccd5923cd23f976ef6a5777bc6d99614`. Actual code implements parity-set polynomial arithmetic, rational cross multiplication, quotient differentiation, fixed-log-basis wp, and the quadratic norm identities correctly for these uses. Counts match:13 symbolic assertions,1023 bounded pairs,143 quotient derivatives,24 rational pairs,49 norm examples;961 Laurent valuation pairs,62 zero-coefficient cases,16 unit cases. Norm's three wrong-normalization comparisons are computed sanity checks, not additional failing processes. Finite checks do not decide Kato cohomology or prove all-parameter nonmembership.

I ran the builder only in the ignored extracted copy, using the frozen PDF as its input. All six rebuilt/copied release files matched original bytes exactly; both ZIPs were actually regenerated. This does not claim a TeX recompilation reproduces timestamped PDF bytes. All four frozen PDF pages were rendered and visually reviewed; equations, disclosures, references and page breaks are legible. `pdfinfo` reports the correct title/author, four letter pages, no encryption/forms/JavaScript. An initial visual suspicion of a margin overflow was falsified by actual PDF word bounds (rightmost about542.12pt on a612pt page) and the absence of layout warnings; it is not an operative finding.

The32 ordinary/optimized private package controls comprise26 safe rejections,4 late rejections after an outside-target overwrite, and2 success-with-overwrite receipt cases. Safe controls include corrupted proof, missing current file, unexpected flat file/directory/directory-symlink, listed proof leaf alias, same-payload authored directory alias, PDF directory alias, unsafe parent-traversal allowlist entry and disagreeing metadata objects. Both runner and builder reject tested input directory/ancestor aliases. All32 package controls remain distinct from the18 mathematical wrong-result failures.

All63 available authored/input pins from the six historical family receipts match. Their163 private/history entries are deliberately omitted and explicitly classified unavailable in the extracted distribution. I inspected custody-checker code but did not run full-source modes against deliberately absent files or rewrite historical receipts. Those authenticated63 pins do not claim full private-source custody reproduction. Original11-member and current16-member manifests independently validate; the corresponding10/15 nonself entries match. Current/family symbol programs are identical; the standalone norm copy differs only in its corrected proof-reference docstring, with unchanged arithmetic/output bytes.

Read-only GitHub inspection found PR1150 open/draft at **`4e8e5db5c47fb879d97cb1a734a76fd59d8f633a`**. All16 remote files and its description match the frozen repaired edition exactly, including body bytes. Original head99f43020e142374629848e97113d354b43fd9f8e and first repaired headf0e04d3ed92c3deea51813269e685311ee2b3fae are properly historical. The current AUDIT_REPORT explicitly labels the12322-byte reviewed proof intermediate and separately pins the12651-byte operative proof. Old no-correction/13-and25-check claims are preserved historical statements and expressly superseded; absent old programs are not represented as rerun.

Production/portable metadata objects are identical, as are their PDF/source/README/metadata payload copies; only the portable deposit's two relative file paths differ. Title, Alec Kriebel/ORCID0009-0001-9320-500X,17October2026 date, version1.0.0, preprint type, CC-BY4.0, scope, exact older credit, diagnostic counts and limits agree. No DOI or published-state claim is fabricated. Final whole-package review stays outside the frozen archive, preventing circular self-attestation. The two-new-clean-review publication gate is not satisfied by this nonclean review.

## 6. Final unchanged identity boundary and handoff

The following six publication files were independently checked at start and finish and remained unchanged throughout this review:

| File under publication/ | Bytes | SHA256 |
|---|---:|---|
|main.tex|13263|739e8dc4654df90d61b4e71d516537f8e3a4211595b53697eacd2075fe0c65e4|
|output/pdf/mixed-kato-counterexample.pdf|71463|01ef963f6dbebc0c3aa91bfb10f13d293c983a46238c4465ae53bf4db99f1c96|
|output/mixed-kato-counterexample-source-and-verification.zip|367362|5d9dc5a8d19b4c79822c58461c018c6fafc8ae5eb0022f8c88c257c9f85bb2ea|
|output/zenodo-upload-kit.zip|414513|cf0965989388edd2d4fd9720eb10ff1dbe6af9fa60c376ddda5fb277b1831511|
|zenodo-metadata.json|3835|32f29280706b83c336031f40b1a29cc44bc124918dda83e1267ccac0d88eaabd|
|zenodo-deposit.json|4144|8071626dd0b8f94d38db640e4083447d24881e8c9abc24bf084d4cd299ea1391|

`EXTERNAL_FINAL_RECEIPT.json` pins this report and the evidence/log/read-scope records without pinning itself. Its exact bytes/SHA are delivered in the external handoff; no pinned artifact depends on that digest. All writes by this review are inside `reviews/package_02`; no Git writes, branch changes, PR edits/messages/comments, publication/deposit, release, tracker action or external-human contact occurred. Workspace branch was main.

**Strongest verified result:** the supplied explicit n=1 construction satisfies the exact original hypotheses and universally excludes all three kernels; n=0 and repaired exponent-one boundaries check. The frozen package authenticates and rebuilds byte-for-byte. **Exact remaining gap:** pre-write rejection/preservation for all three builder output destinations, demonstrated in R1. This review is complete at100% of its assigned scope; that percentage does not measure literature completeness or certify publication readiness.
