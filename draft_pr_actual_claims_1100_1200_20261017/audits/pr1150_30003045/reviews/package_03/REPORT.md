# PR1150 whole-package adversarial review 03 — frozen edition 3

**Disposition: NEEDS MINOR REPAIR; not CLEAN_PASS.** One remaining static output-path preflight issue is established below. No mathematical defect was found in the explicit counterexample, full three-summand exclusion, positive degree-one boundary, or repaired exponent-one discussion. The six frozen release files are intact, internally consistent, and reproducible. This is an internal AI review of specified bytes, not external human peer review, formal proof verification, a firstness certificate, or publication permission.

Completed 2026-10-18 UTC. All mutations, executions, and rebuilds used this review's ignored private copies. No release input was edited. The review reached 100% of its assigned bounded scope; that percentage does not measure literature completeness or discovery progress.

## 1. Remaining operative issue

### R1 — P3: Preflight the existing output type before replacing any earlier output

The edition-3 builder now correctly rejects output symlinks before writing, and its unique temporary files plus atomic replacements preserve existing hardlinked targets. Those repairs pass this review. A narrower structural gap remains at `publication/build_package.py` lines11–20 and47: the initial calls to `safe(destination)` reject symlinks but do not reject an existing directory at a generated-file destination. The final `os.replace` in lines31/42 detects that directory only after earlier outputs have already been replaced.

This is a demonstrated static-path failure, without a concurrent race. In independent private copies, replace the kit destination or receipt destination by an empty directory, then run the unmodified builder:

| Directory occupying destination | Ordinary and optimized outcome | Earlier output replacement before failure |
|---|---|---|
| `output/zenodo-upload-kit.zip` | exit1, `IsADirectoryError` at atomic replacement | source ZIP |
| `PACKAGE_RECEIPT.json` | exit1, `IsADirectoryError` at atomic replacement | source ZIP and kit ZIP |

The distinction between bytes and filesystem replacement matters. In controls beginning with valid generated outputs, earlier outputs kept exactly the same SHA256 bytes but received different inodes and modification times. In separate controls beginning with recognizable pre-existing marker contents, those earlier outputs also changed bytes to the newly generated payloads. Both behaviors are recorded, rather than describing a byte-identical deterministic rewrite as a content change. A directory occupying the first/source destination fails without changing the other outputs.

`EXTRA_PATH_CONTROLS.json` records before/after SHA256, inode and mtime for all three destinations, using distinct marker contents. `VALID_OUTPUT_DIRECTORY_CONTROLS.json` records four ordinary/optimized runs beginning with correct output bytes: no earlier content hash changed, but earlier files were replaced. `extra_path_controls.py` provides the checkable marker/directory/hardlink reproduction. No outside sentinel was harmed.

Before any output write, require every already-existing generated-file destination to be a regular file, and every existing relevant parent to be a directory, in addition to rejecting symlinks. Check all three destinations together. Preserve the documented exclusion of malicious concurrent filesystem races. This finding concerns the stated complete preflight/preservation contract; it does not invalidate the mathematics, current archive bytes, atomic replacement of each individual file, or the successfully repaired output-symlink controls. It is minor but prevents a zero-remaining-issues clean disposition.

No other operative issue was established, including minor citation, credit, metadata, current-edition, or reproduction defects. Prior package01 and package02 findings are properly historical and repaired to the extent they describe: the listed/unlisted directory and ancestor symlinks are rejected, standalone norm proof reference exists, intermediate/final proof identities are distinguished, Milne is cited as items rather than all theorems, and output symlink aliases are rejected before any output change.

## 2. Independence, initial seal, and actual exposure

This agent began with the task brief and repository instructions, without earlier parent research conversation or prior report bodies. The brief supplied the candidate, six expected identities, edition history, credited antecedent, access limits and adversarial attack surfaces. Thus this is independent checking of a supplied candidate, not blind rediscovery or a claim of causal isolation from the brief.

Before opening any root, older or sibling verdict report, I read all13263 bytes of `publication/main.tex`, rendered and viewed all four frozen paper pages, independently fetched the original EMS report, and read the full Laghribi contribution printed248–251 in text and all four page images. I reconstructed and attempted to falsify the exact target and candidate before sealing `INITIAL_ASSESSMENT.md` at **2026-10-18T00:06:09.225632+00:00**, **5317 bytes**, SHA256 **`d1779938ae125c368548050fe9bf3022cabd362988ccd00115a70da00910b468`**. Its separate receipt pins that unchanged assessment. The tool transcript provides chronological file-access evidence; a hash alone cannot prove absence of other exposure.

Only after that seal did I read the operative final proof, exact complete historical/intermediate/final diffs, current16-file PR documents/programs, original historical inputs, root mathematical and priority assessments, all six complete earlier mathematical/priority family reports, their detailed read-scope records, independence disclosure, repair/provenance records, and both package01/package02 reports. I inspected actual arithmetic, all operative runners/builder, and historical custody-checker code. JSON records and inventories were parsed programmatically; retaining or hashing a record is not called semantic reading of every field or source mentioned in it. `INSPECTED_INPUTS.json` gives each of the141 source-archive entries an explicit exposure category.

After my own private directory reproduction and message, the parent asked me to finish and seal this frozen review, said a future structural preflight repair would follow, and cautioned me to distinguish byte changes from inode/mtime replacements. That was not mathematical evidence and did not precede the finding. I did not communicate with a sibling/shard or outside individual, prepare outreach, edit a PR, publish, or mutate Git state.

## 3. Independent mathematical result

The exact target is OWR5/2016 Question2 on printed251. It asks equality of the composite Kato kernel and the sum of the L/F, K/F, and F(B)/F kernels for every finite purely inseparable L/F, separable quadratic K/F, and anisotropic bilinear Pfister B remaining anisotropic over L. Printed248 explicitly defines F(B) by the projective quadric of B(v,v). There is no exponent-one, dimension-at-least-four, smoothness, geometric-reducedness, or positive-dimensional condition. A permitted n=1 negative instance refutes the universal equality. The adjacent quadratic-Pfister question is different.

For F=F2(b,z,s,t), beta^4=b and L=F(beta), the b-valuation proves b nonsquare, degree four and exponent exactly two. The odd s-pole of s^-1 proves that theta^2+theta=s^-1 gives a genuine separable quadratic extension, including after the later completion. The independent t-valuation proves that B=<1,t>_b stays anisotropic over L. A separable algebraic extension cannot supply a new purely inseparable square root. The binary projective quadric is the integral zero-dimensional field chart F(gamma), gamma^2=t. Consequently M=LF(B)=F2(beta,z,s,gamma), the full composite is M(theta), and its total degree over F is16. No empty zero-fold quadric or nonsingular quadratic Pfister substitution is used.

The natural identification H_2^2(E)=Br(E)[2] takes u dlog(v) to the displayed characteristic-two quaternion [u,v), with i^2+i=u, j^2=v, ji=(i+1)j, and commutes with scalar extension. Milne's general finite-Galois crossed-product theorem applies to imperfect fields. For a quadratic group, a normalized two-cocycle is determined by its invariant scalar c on the nonidentity pair; coboundaries multiply it by a norm. Hence the entire relative kernel for the genuine Artin–Schreier quadratic field consists of [s^-1,c), c in F*. This does not assert that every arbitrary Brauer class is a single quaternion. The splitting/norm criterion is valid for the same genuine separable field, and is explicitly confirmed by the published Voight characteristic-two theorem. These are established dependencies, not a newly proved foundation of Kato or Brauer theory.

In L, let f=1+beta^2 z and h=beta^2 z/f. Since d(beta^2)=0, dlog(f)=h dlog(z) and h^2=bz^2/(1+bz^2). The two logarithmic Artin–Schreier relations give

    xi_L = [s^-2,f)_L = [s^-1,f)_L,

so xi vanishes over LK. These are quotient/cohomology equalities. In the fixed logarithmic basis the generally nonzero exact correction d(s^-2 h) is retained by the actual program; wp is not treated as coefficient-linear on an arbitrary presentation.

For a hypothetical three-summand decomposition xi=x+y+w, write y=[s^-1,c) for an arbitrary nonzero base-field rational function c. Restrict to M: both x and w vanish. It follows that [s^-1,f/c)_M=0. This explicitly includes the full third Pfister kernel; two-field nonsplitting alone would be insufficient.

Complete M to D=k'((s)), k'=F2(beta,z,gamma). With pi=theta^-1, pi^2+s pi+s=0, conjugate pi+s, and N(pi)=s. Every element of D(theta) is A+B pi, and its norm is

    A^2+sAB+sB^2.

For nonzero coefficients put a=v_s(A), b'=v_s(B). The leading valuations2a and1+2b' have opposite parity;1+a+b' exceeds their minimum in both a<=b' and a>=b'+1. Thus the norm valuation is min(2a,1+2b'). The cases A=0 or B=0 follow from the same formula; A=B=0 is excluded by the nonzero norm domain. A unit norm has a=0, b'>=0, and square residue. No perfectness, defect assumption or residue norm-surjectivity claim is required.

Every c in k(s)*, k=F2(b,z,t), has leading term s^r c0 with arbitrary integer r and c0 in k*. Multiplying f/c by the norm N(pi^r)=s^r makes it a unit norm, including negative r, so f/c0 must lie in k'^2. Set S=k'^2=F2(beta^2,z^2,gamma^2), R=F2(beta^4,z^2,gamma^2). Since k=R(z) has degree two over R, every rational c0, with arbitrary denominators, is u+vz for u,v in R. Since z is not in S, comparing1,z coefficients in

    1+beta^2 z = q(u+vz), q in S*,

forces qu=1 and qv=beta^2. The zero cases u=0 or v=0 fail immediately; otherwise beta^2=v/u belongs to R, contradicting its odd independent-variable valuation. Thus every c is excluded. The contradiction proves full three-summand nonmembership and also xi itself nonzero. All construction denominators are nonzero by algebraic independence. These are universal field deductions, not finite sampling.

At n=0, Artin–Schreier roots cannot first arise in purely inseparable or rational extensions. An anisotropic quasilinear form of dimension d>=2 has a projective-chart field purely inseparable quadratic over a rational field in d-2 variables. Separable extension preserves the needed anisotropy by linear disjointness. A root in LK(B) descends through that chart to KL and then K; the other two degree-one kernels vanish. Binary d=2 has no rational variables. The separately assigned zero-fold F(B)=F convention is treated explicitly without defining a function field for an empty projective quadric.

Both adverse boundaries check. Choosing the Pfister slot z kills dz and absorbs xi. In the exponent-one variation b=u^2 and beta^2=u, the calculation takes place over L, where du=0; the second slot f=1+uz descends to F, proving membership in the sum of L and K kernels. It does not prove a base-field single-symbol equality, where d(1+uz)=u dz+z du. Failure of that representative shortcut is not itself claimed to decide inequality of two cohomology classes. The exact original-to-intermediate diff changes only this bullet; intermediate-to-final strengthens only prior credit. FINAL_PROOF/current COUNTEREXAMPLE agree at12651 bytes, SHA256 `7808df31d74049fe649231a905e6dc330929caa87c86dca6ebfa6dcfb6d6c275`.

## 4. Primary dependencies, credit, and honest limits

I checked the precise older generator in the dated ALO2019 author manuscript: Definition1.3 with n=m=1, f0=1, f1=z gives the only nonzero term (beta^2 z/(1+beta^2 z))^2 dlog(z). Multiplying by a=s^-4 gives exactly xi. Lemma3.1 supplies the prior vanishing mechanism, and Theorem1.4's power hypothesis uses l=2>1. The identity s^-4+s^-1=wp(s^-2+s^-1) gives the same quadratic field. The paper, proof, README, PR body and metadata credit this exact antecedent prominently; no new generic mixed-generator or firstness claim survives.

The predecessor's Theorems1.1–1.2 impose exponent-one multiquadratic square-root extensions. Their affine-cone convention adds a rational variable to the projective field, leaving the restriction kernel unchanged by rational-extension injectivity. That theorem is not silently enlarged to exponent two. The direct third-kernel survival proof is actually supplied rather than inferred from the name of a mixed term.

My primary reading is precisely bounded in `PRIMARY_READ_SCOPE.json` and the identities/failures in `PRIMARY_RETRIEVAL.json`:

| Source | Actual scope in this review |
|---|---|
| Original EMS report | Entire relevant contribution printed248–251; all four pages viewed; no unrelated whole talks claimed |
| ALO2019, dated15August2019 | Introduction/main statements through Definition1.3 and Theorems1.4–1.5; Section2.1 fixed-basis definitions; complete Lemma3.1 proof/setup; pages3,4,9 viewed. Not whole28-page technical body or final journal comparison |
| ALO2016 author manuscript | Introduction/main Theorems1.1–1.2 and surrounding corollaries; affine and bilinear/Pfister conventions, selected pp1–5; pages3–4 viewed. Not all technical proofs |
| Chapman–Quéguiner-Mathieu explicit arXiv2111.15251v3 | Complete pp2–3 symbols/cohomology preliminaries; page3 viewed. Not unrelated main theorem/final publication |
| Milne v4.03,6August2020 | Complete PDF140–146/printed131–137, relative definition and general-field crossed-product construction/proofs through3.14; page146 viewed. Not whole book or all foundations |
| Voight official2021 Chapter6 | Surrounding Section6.4 and full norm theorem6.4.11, short proof pointer and adjacent splitting lemma; page8/printed92 viewed. Not full chapter/book or Exercise6.13 reproof |

The original, both ALO manuscripts, explicit Chapman v3, and official Voight chapter were freshly fetched. Direct Milne bytes returned406; I independently opened the primary web PDF, then copied and checked the earlier norm family's primary PDF, read/rendered its relevant pages, and matched the2072714-byte SHA256 `50d79af78250a9f1117ad9d337e0b231704a533fc707966ed1bfa52e13d498f5`. That is a custody copy, not a successful fresh byte download. An initially guessed current Voight author URL returned404; the actual official2021 chapter succeeded at252106 bytes/SHA256 `734db57499918d0d90100d1d839255fa6fc074c2b617ebc7bc112c254313bf83`.

Fresh publisher-deposited Crossref factual fields confirm ALO's Journal of Algebra542(2020),249–276 and the2016 volume449,635–659. The2019 metadata creation date is not called publication. Primary PDFs/extracts/renders and raw responses remain ignored. Their byte pins establish identity, not mathematical truth or full-document reading.

I read all three earlier priority reports and their detailed limitations, not all sources those reports cite, and did not repeat their168 query inputs. Counts20+53+47+48 include overlaps/low-yield work and do not denote168 relevant works or exhaustive coverage. Final ALO2020 journal-body comparison, full adjacent nonnormal2020 DOI10.1080/00927872.2019.1686510, transfer2022 DOI10.1016/j.jpaa.2021.106930, the unlinked2026 lead, and broader screened2025/2026 bodies are not newly cleared by this review. The separate reported Sobiech correction concerns a pure-extension differential-kernel formula that this direct norm proof does not invoke; its whole literature context was not independently re-audited here.

The current paper and metadata preserve access/version limits, extensive AI use, inherited parent context in the initial six families, no perfect isolation or causal-independence claim, unrefereed status, no external human peer review and no proof-assistant verification. Initial-family claims about unopened report files are not expanded into absence of related inherited context. No global openness, novelty, firstness or absence-of-prior-work certificate follows from this review.

## 5. Entire operative package, replay, guards, and provenance

Safe extraction checked unique nonabsolute/nontraversing ZIP paths, absence of symlink/directory members and regular payloads before writing only into the ignored private area. The source has141 members:140 nonself manifest entries comprising11 fixed base files,128 explicitly authored audit members and provenance, plus the self-excluded manifest. The kit has5 members. Every nonself source manifest pin matches. All69 source JSON records parse. The only PDF member is the authored paper; copied third-party source bodies/extracts/renders/raw responses are not distributed. Factual authored metadata and private-source pointers are distinct from those omitted bodies.

Offline ordinary and optimized outer replay runs pass with networking blocked by an inherited Python socket guard. They agree exactly with the frozen full replay receipt and authenticate128 authored members plus the16-member current edition. Each replay executes both algebra programs in ordinary/optimized modes, matches all four complete positive output byte strings and observes18 actual wrong-result failures. Those are nine computed false assertions in both modes, with precise CHECK FAILED ValueErrors; the unexpected-success fallback is excluded. They are not invalid-argument exits or unconditional failures. Guard failures are counted separately.

Actual arithmetic inspection confirms parity-set GF(2) polynomials, cross-multiplication rational equality, characteristic-two quotient differentiation, fixed-log-basis wp with the nonzero exact correction, sparse Laurent norm multiplication and valuation calculations. Optimization does not remove explicit exception checks. The symbols output is1313 bytes/SHA256 `2c15e49d6e392649b56c1044e8dc914fa60f8c0584f22d319b79ead6cdb0845a`; the norm output is338 bytes/SHA256 `6d9c613f25f0ae26239e157f914f4e41ccd5923cd23f976ef6a5777bc6d99614`. Counts match13 symbolic assertions,1023 bounded coefficient pairs,143 quotient derivatives,24 rational pairs,49 quadratic norm examples;961 Laurent pairs,62 zero-coefficient cases and16 unit cases. Norm's three alternative-normalization comparisons are computed sanity checks, not three more failing processes. No finite program decides Kato cohomology or replaces the universal proof.

The builder ran only in the private extraction. Both ZIPs were actually regenerated; all six rebuilt/copied release files and PACKAGE_RECEIPT match byte-for-byte. The archived PDF is a pinned input. This does not claim that a new TeX compilation reproduces timestamped PDF bytes. All four frozen PDF pages were rendered and viewed; equations, disclosure, ORCID, references, margins and page breaks are legible with no clipping/overlap. Independent pdfinfo confirms title/author/subject, four letter pages, no encryption/forms/JavaScript.

The first58 static controls include proof/baseline corruption, missing current file, extra flat file/directory/directory-symlink, listed leaf alias, exact-payload authored ancestor alias, unsafe allowlist traversal, PDF ancestor alias and metadata disagreement. Both outer verifier and builder reject their relevant input aliases in ordinary/optimized runs. All six generated-output symlink cases reject before any output changes and preserve outside sentinels, even when the other outputs begin with recognizable marker bytes. This confirms the edition-3 repair, not merely its eventual error message.

Twelve additional detailed runs document the directory failure and six meaningful hardlink controls. In the latter, each linked outside target initially contains bytes deliberately different from generated payloads; successful ordinary/optimized builders replace the output inode with the exact frozen result while preserving the outside sentinel's bytes/inode/mtime. Six earlier hardlink runs with identical starting payloads are weaker sanity checks and are not relied on for that conclusion. Four final directory runs with already-correct outputs distinguish unchanged content hashes from inode/mtime replacement as described in R1. These integrity/path executions are separate from the18 mathematical wrong-result failures, and no adversarial concurrent-race defense is claimed.

The original11-member and current16-member manifests validate all10/15 nonself entries. Current/family symbols code is identical; the standalone norm copy differs only in its corrected REPORT.md-to-COUNTEREXAMPLE.md docstring, with identical arithmetic/output. Historical family receipts authenticate all63 available authored/input pins;163 private/history entries are intentionally absent from the distribution. Their complete source-custody checker modes were not run against absent sources. That is an honest availability boundary, not a failed mathematical check. Authenticating these pins does not reproduce historical searches or establish source reading.

Historical original inputs and old no-correction/13-and25-check claims are explicitly superseded. No absent old diagnostic program is represented as rerun. Root's intermediate mathematical review retains its actual12322-byte scope; current PR AUDIT_REPORT separately pins the final12651-byte proof. PACKAGE_REPAIR_NOTES explains both preceding nonclean package reviews and the repairs, without retroactively calling them clean reviews of edition3. The final whole-package reports stay outside the frozen archive, avoiding circular self-attestation.

Fresh read-only GitHub retrieval finds PR1150 open/draft at **4e8e5db5c47fb879d97cb1a734a76fd59d8f633a**. All16 remote file bodies match the current frozen PR edition, and the4473-byte description matches its saved body exactly, SHA256 `628e37b879f9fa5ac4f5a0eb031f11ae5bce237aaa9bd84a0372595830fc2109`. Original99f43020e142374629848e97113d354b43fd9f8e and first repairedf0e04d3ed92c3deea51813269e685311ee2b3fae are clearly historical. No PR action, comment or message was sent.

Production/portable metadata objects and payload copies agree exactly; only the portable deposit's two relative file paths differ. Title, Alec Kriebel, ORCID0009-0001-9320-500X,17October2026 date, version1.0.0, preprint type, CC-BY4.0, exact mathematical scope, prior credit, diagnostic counts and access/review disclosures agree. No DOI or completed-publication fact is fabricated. The current acceptance gate records edition3, no clean reviews and unpublished status. This nonclean review supplies no permission to publish or completed readiness gate.

## 6. Final identity boundary and handoff

The assigned six files under `publication/` were checked at the beginning and end and remain unchanged:

| File | Bytes | SHA256 |
|---|---:|---|
| main.tex |13263|739e8dc4654df90d61b4e71d516537f8e3a4211595b53697eacd2075fe0c65e4|
| output/pdf/mixed-kato-counterexample.pdf |71463|01ef963f6dbebc0c3aa91bfb10f13d293c983a46238c4465ae53bf4db99f1c96|
| output/mixed-kato-counterexample-source-and-verification.zip |370294|3077317576f44166ce0da48971777062fa24abbb997eb2b315baf7c6e8e6745d|
| output/zenodo-upload-kit.zip |417097|7fbad4a071acabbf30a375bb41308f1ee13fa5ee9819720e1d1796072fa88a88|
| zenodo-metadata.json |3835|32f29280706b83c336031f40b1a29cc44bc124918dda83e1267ccac0d88eaabd|
| zenodo-deposit.json |4144|8071626dd0b8f94d38db640e4083447d24881e8c9abc24bf084d4cd299ea1391|

`EXTERNAL_FINAL_RECEIPT.json` pins this report and authored evidence/log/read-scope artifacts without pinning itself. Its byte count and SHA256 are delivered externally after writing; no pinned artifact depends on that digest. All review writes are confined to `reviews/package_03`. The shared checkout stayed on main; there were no Git/ref/index writes, PR mutations/comments, deposit/release/tracker actions, or outside-human contact.

**Strongest verified result:** the supplied explicit n=1 construction meets the exact original hypotheses and universally excludes all three kernels; the n=0 and repaired exponent-one boundaries check. The complete frozen package authenticates, replays offline and rebuilds byte-for-byte with accurate attribution and evidence limits. **Exact remaining gap:** static destination-type preflight/preservation in R1. After repair, release identities change and the specified new-clean-review sequence must start again.
