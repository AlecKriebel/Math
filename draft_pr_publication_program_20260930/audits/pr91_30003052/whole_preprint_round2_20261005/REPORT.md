# Fresh independent whole-preprint adversarial review, round 2

Review date: 2026-10-05. Scope: the seven payloads selected by `publication_package_v1/zenodo-deposit.json`, their eleven-member support archive, current source/code/metadata, and the relevant primary-source claims. All audit writes are confined to `whole_preprint_round2_20261005`. No original, public package, Git/index/branch, PR, release, Zenodo, Sheet, editor/UI, or PR50 content was changed. No outside individual was contacted and no outreach was prepared.

## Verdict

**PASS for scientific and reproducibility readiness of the exact frozen current package. No mandatory issue remains in this review's scope.** The complete theorem is valid under the precise stated hypotheses. The historical framing is sound as an explicit present solution of a question expressly open in the 2015 source, by a short classical specialization. The original supporting-code optimization defect and round-one attribution wording defect are both resolved throughout the current selected package and archive.

This verdict is extensive AI adversarial verification, not conventional human peer review, a worldwide novelty certificate, a deposit/API validation, or authority to publish, merge, release or contact anyone. It does not certify continued openness between 2015 and 2026. Audit completion is 100%; those other authorities and claims do not follow from that percentage.

## Actual independence and reading order

1. Before reading the manuscript, archive, code, metadata or prior reports, I wrote `INDEPENDENT_PROOF_OBLIGATIONS.md`. It derives the expected splitting and identifies counterexample families: an oblique projection in a non-product norm, nonnormal stable Jordan blocks, unbounded recurrence indices, dense irrational Gamma, invertible contractions with a zero Koopman eigenvalue, and peripheral/nilpotent mixtures. The two principal exclusion obligations were exact boundary point spectrum and an analytic full-spectrum upper bound in the nilpotent-only case.
2. I then read the entire current TeX, public instructions/license/digests, metadata/frozen administrative manifest, code/provenance and retained results, and current public priority supplement. I freshly extracted the ZIP, compared every member bytewise with its public source, and ran the unmodified portable wrapper from the extracted root. I freshly rendered and inspected all six actual current-PDF pages.
3. I directly extracted/read Küster 2015 Section 3.1, printed 35–43/PDF 44–52; the entire Pure Koopmanism contribution, printed 320–322/PDF 24–26; EFHN printed 308–313/PDF 326–331 plus its dated title pages. `INDEPENDENT_JUDGMENT_BEFORE_PRIOR_REPORTS.md` records my own mathematical, reproduction and principal-source judgment before any old review or ROOT adjudication was read. The supplement was read as a current public document, not as prior-review authority.
4. I independently located the declared original/minimal-repair code by byte hashes, inspected the original-to-public and original-to-repair diffs, and tested private false guards. Only after my own judgment did I read the round-one report, previous peripheral/full-spectrum/general-priority/exact-reproduction reports, author-family priority report/verdict, and ROOT adjudication summaries for unresolved-finding comparison.
5. Additional direct primary readings then covered thesis printed 58–59/PDF 67–68; Küster 2019 v3 PDF 20–21 and24; Küster 2021 PDF 61 and123; Kitover–Orhon Part VII PDF 4–5; and Ikeda–Ishikawa–Schlosser v3 PDF 5. I newly rendered and inspected thesis PDF 52, OWR PDF 25, EFHN PDF 331 and EFHN PDF 1. This is bounded reading, not an assertion of reading every later source or every book chapter in the aggregate supplement. Large embedded ROOT evidence lists were not used as mathematical authority.

`READ_ORDER.json` and `RESEARCH_LOG.md` preserve checkpoints. An initial broad Git-status read returned filenames only; no prior report content was read there and no Git command modified anything. No later Git operation was performed.

## Exact claim and independently checked proof

Let X=(C^k,||.||), k>=1, with any complex norm; let U be its closed unit ball; let A be complex-linear with its induced norm at most one. K_A f=f composed with A acts on **all** continuous complex-valued functions C(U), with the supremum norm. Define S=sigma(A) intersect T, J={alpha in sigma(A):0<|alpha|<1}, Gamma=<S> with every integer exponent and empty-generated group {1}, and Z_A={0} iff A is singular. The verified conclusion is:

| Condition | Point spectrum | Full bounded-operator spectrum |
|---|---|---|
| J nonempty | open unit disk union Gamma | closed unit disk |
| J empty | Gamma union Z_A | closure(Gamma) union Z_A |

The analytic proof, rather than a finite matrix surrogate, establishes the result:

- **Matrix splitting and the given norm.** Power boundedness rules out a peripheral Jordan chain: A^n w=lambda^n w+n lambda^(n-1)v has norm at least n||v||-||w||. The peripheral part B is semisimple, while every stable Jordan block decays in norm. A convergent torus subsequence indexed by strictly increasing m_j gives n_j=m_(2j)-m_j>=j and every peripheral phase lambda_i^n_j->1. Thus A^n_j->P in the actual operator norm and ||P||<=1. The n_j need not themselves be strictly increasing; n_j>=j is sufficient. The empty peripheral set uses n_j=j. Hence P(U)=U intersect E, without a product-ball or Euclidean-orthogonality assumption.
- **Surjective peripheral isometry.** B^n_j->I gives B^(n_j-1)->B^(-1). Both B and its inverse are contractions in the original restricted norm, so B(V)=V and ||Bx||=||x|| for V=U intersect E. E=0 is treated as the singleton V={0}, whose function space is the constants.
- **Unimodular factorization.** For K_A f=zeta f, |zeta|=1, the equality |f(x)-f(Px)|=|f(A^n x)-f(A^n Px)| holds for every x. Both arguments remain in U and their difference N^n(I-P)x tends uniformly to zero. Compactness and uniform continuity therefore give f=fP exactly. Pullback and restriction preserve nonzero functions and intertwine the peripheral and original operators.
- **Exact Gamma, including dense groups.** Coordinate/conjugate monomials realize every signed exponent. They are nonzero on V because V contains a relative neighborhood of zero. Their algebra contains constants, separates points and is conjugation closed, so complex Stone–Weierstrass gives uniform density. For zeta in T outside Gamma, the contractive means M_m=m^(-1) sum_(j=0)^(m-1) zeta^(-j) K_B^j kill each fixed polynomial as m->infinity. A zeta-eigenfunction is fixed by every mean. Approximating that function first by a polynomial proves it is zero. No uniform frequency separation or closedness of point spectrum is assumed; a countable dense Gamma stays the exact point spectrum.
- **Peripheral full spectrum.** K_B and its inverse have norm one, so outer and inner Neumann series exclude every value off T. Closedness contains closure(Gamma). An infinite circle subgroup is dense: nonidentity elements can approach 1, and the powers of sufficiently small-angle elements yield arbitrarily fine circle nets. A finite group of order q gives B^q=I and K_B^q=I, so polynomial factorization excludes every value outside that group. These are resolvent/closedness arguments for the full Banach operator.
- **Every interior mu, including zero.** For a nonzero stable alpha, a left eigenfunctional ell exists even for defective A. Put a=|alpha| and R=max_U |ell|>0. For 0<|mu|<1 choose s=(log|mu|+i theta)/log a with exp(i theta)=mu/|mu|. The function exp(s log(|ell(x)|/R)), extended by zero at ell(x)=0, is continuous because Re(s)>0, nonzero, and scales by a^s=mu. Its logarithm is real on positive radii, so no angular branch is hidden. The separate positive-part function max(0,|ell(x)|/R-a) vanishes on A(U) and is positive at a maximizer; thus zero is an eigenvalue even when A is invertible. The operator norm bound and exact peripheral exclusion give the point row. Closedness of spectrum and the interior inclusion give the full disk.
- **Nilpotent-only stable part.** J empty makes N nilpotent. The commuting bounded projection Qf=fP has isometric range C(V) and kernel the functions vanishing on V. A^d(U) lies in V, so K_A^d vanishes on ker Q. That summand is nonzero iff F is nonzero, as witnessed by a linear functional zero on E. A nilpotent operator on a nonzero space has a zero eigenvector and spectrum {0}; when the summand is absent it contributes no spectrum. The closed invariant direct sum gives the union of point and full restricted spectra. Here F nonzero iff A is singular.

For explicit upper bounds, a nilpotent restriction H^d=0 has (zI-H)^(-1)=sum_(j=0)^(d-1) z^(-j-1)H^j for z!=0. For finite peripheral order q and z^q!=1, (zI-K_B)^(-1)=[sum_(j=0)^(q-1) z^(q-1-j)K_B^j]/(z^q-1). These bounded inverses combine through the commuting projections; no approximate finite spectrum is substituted.

The attempted boundary cases all agree: A=0/nilpotent gives {0,1}; A=I gives {1}; finite peripheral rotations give finite root groups; irrational rotations give exact dense Gamma and full circle; peripheral plus nilpotent gives closure(Gamma) plus zero; adding a nonzero stable eigenvalue gives the disk; invertible strict contractions still have a Koopman kernel. Spectral sets can change discontinuously at radius0 or1; no continuity of those sets is asserted. No unsupported equivalent/stronger central claim remains.

## Sources, classical mechanism and contribution size

The 2015 setup is exactly an arbitrary norm on C^k, a contractive matrix, its closed unit ball and C(U). Theorem 3.1.14(i), printed 43/PDF 52, states the mixed inclusion and its immediately following paragraph expressly leaves the converse open. The 2016 Example 4/Theorem 5(ii), printed 321/PDF 25, use the same setting and state inclusion only. The 2016 contribution does not expressly declare continued openness; current wording preserves that distinction.

The cited prior all-peripheral, nilpotent, open-disk and stable-only statements are present at the stated locations. The full disk is already an immediate consequence of the 2015 open-disk inclusion plus norm one and spectral closedness. The paper, README, deposit description and supplement correctly credit this and do not present it as a novel full-spectrum discovery.

EFHN is the author manuscript dated April 22, 2016 of the book published in 2015. Printed308–309 define the reversible range via the minimal idempotent; Theorem 16.33(a), printed 313/PDF 331, places unimodular eigenvectors there. The current manuscript checks the applicability: the matrix-power closure H is compact abelian; uniform continuity makes its composition image strongly compact and also weakly closed; the peripheral group ideal {DP:D in G_B} lies in H and has identity P. Multiplication by P makes every nonempty ideal meet that group, and any such intersection must be the entire group. Hence the minimal idempotent corresponds to Qf=fP. This is a sound concrete specialization of preexisting JdLG theory. Strong compactness of the power family is not a claim that K_A is a compact operator.

The later thesis passages handle convergent powers, a special periodic/zero case, and strict operator-norm contraction; the 2019 passages concern fixed-factor quotients; the 2021 passages concern Kronecker factors or a restricted weakly stable ideal. The inspected Part VII theorem concerns full spectrum with an injective proper compact selfmap; its displayed open-disk typography cannot literally be a nonzero bounded-operator spectrum. The current package acknowledges that source caveat and does not base its proof on it. The RKBS v3 explicitly includes all C(X) and restates the classical image-stabilization full-disk criterion, as credited in the supplement. These directly inspected passages do not explicitly print the mixed point-spectrum completion.

A short note presenting this historical question's explicit solution with full classical credit is scientifically defensible. Its significance is a concrete synthesis/specialization, and the public framing accurately reflects that size. Global firstness, an exhaustive absence search, unread theorem bodies, and uninterrupted 2015–2026 openness remain unverified and unclaimed. The aggregate supplement's broader bounded-reading statements are supported by the scoped audit reports; I do not convert those aggregate reads into my own direct reading. The published2015 book text was not byte-compared with the2016 author manuscript. Original Scheffold 1971, some Kitover versions, the Küster journal version, and full 2026 Mezić chapter remain documented ordinary coverage gaps.

## Fresh reproduction, safeguards and source provenance

The ZIP was extracted to the private `extracted_root`. From that archive root, the exact outer argv was:

```
/usr/bin/python3 -E -B verification/run_all.py --output-dir <audit>/portable_reproduction
```

Outer child PID 68521, recorder PID 68520; started 2026-10-05T19:59:01.451641+00:00, ended 2026-10-05T19:59:08.822036+00:00; exit 0; elapsed 7.369912 seconds. `wrapper_process/execution.json` retains exact absolute cwd/argv, input and wrapper hashes and full binary stdout/stderr. Native Python 3.9.6 imports SymPy 1.14.0 from its ordinary installed path; no PYTHONPATH was injected. `/usr/bin/python3` resolves to the Xcode Python executable, which appears explicitly in child execution records. Both ordinary and optimized children carry -E and -B; the optimized ones also carry -O.

| Suite | Exact/discrete per mode | Floating per mode | Total |
|---|---:|---:|---:|
| Submitted controls, repaired/adapted |473|0|473|
| Earlier independent controls, repaired/adapted |907|0|907|
| Boundary controls |774|566|1340|
| Per-mode total |2154|566|2720|

All six fresh suite receipts, family counts and numerical-diagnostic records agree with included results; stable receipt hashes are identical. Fresh runtime naturally differs. The artifact hash is the current source SHA256 `7ff89914b44a8940cc665e5f90aaf6e56a76e3cd7dbe85571d92eae83c348792`. The floating maximum recorded error is 1.2775558388966601e-11 within 2e-10*(1+abs(rhs)). Repeating modes does not create 5440 distinct controls. The 80/224 elementary radial orbit controls remain finite algebra/phase encodings, as publicly disclosed; the boundary suite adds actual sampled complex-function evaluations. None proves universal continuity, recurrence, arbitrary-norm geometry, density, the infinite-dimensional spectrum or priority.

Private deliberate false ck calls were inserted immediately after the unchanged explicit guard in separate copies of all three checkers. Each failed with exit 1 in both ordinary and -O modes, with the false label in stderr, empty stdout and no success receipt. A private altered-source wrapper copy fails before running children on its source-hash mismatch. The unmodified wrapper also rejects the already nonempty private result directory. No public byte was changed. `NEGATIVE_CONTROLS_SUMMARY.json` records all eight expected failures; each execution keeps exact PID/argv/cwd/UTC/exit and complete streams.

The public provenance's three source identities match actual bytes. The submitted and earlier independent originals have removable Assert guards; their minimal repairs change only that guard to If/Raise, with increments afterwards. The repaired and current-public guard ASTs match. Their mathematical bodies are byte-identical through original, positive repair and CLI adaptation. The boundary mathematical body is likewise unchanged after excluding its removed output-root declaration/trailing whitespace; its unnecessary optimization prohibition was removed. Public additions are artifact/output CLI and receipt/provenance clarification. Computed original Git-blob SHA1 agrees with the preserved original-byte manifest for the submitted and independent sources. The manifest's immutable-head association is provenance supplied by that preserved authentication record; this review did not fetch/revalidate a remote PR head.

`SOURCE_PROVENANCE_INDEPENDENT_COMPARISON.json`, the three original-to-public diffs and two original-to-repair diffs are checkable artifacts. `PROCESS_SUMMARY.json` indexes 16 retained controlled execution records: outer reproduction, native-runtime probe, six positive children and eight negative controls. Full process streams and all source/input snapshots are hashed in the closed custody manifest.

## Package, metadata, PDF and mandatory-finding disposition

Exactly seven selected payloads agree with the frozen manifest, including byte counts and hashes. Metadata SHA256 is `44d339f6c13b221383bff4c99631795f5d8ef11765e3b62dc39f201e1f7bb77c`. Current TeX is the hash above; current PDF is `aa7fd2760e6de36390d79a0b88f8eeac79f6567ecb89a504d2bc14cb7cda20d9`; current ZIP is `571c190582ebea58d00d8194f460feec2fc6f7cecfb9d341aed8fb4e90c1b14c`. Every one of 11 unique safe-relative ZIP members is byte-identical to its public source and frozen member record. All 13 supplied digest lines verify. The digest file excludes itself; the ZIP excludes its own archive/digest and contains no third-party PDF or private audit file.

Title, Alec Kriebel authorship, supplied ORCID, date 2026-10-05, version 1.0, preprint type, CC BY 4.0 license and extensive AI/unrefereed disclosure are consistent across the current source, PDF, README, license and metadata. Licensing authored code under CC BY 4.0 is an uncommon choice but is clearly stated; third-party software/documents retain their own terms. This is a content consistency check, not legal advice or a live Zenodo schema test. The standalone source has its embedded bibliography and no external source-PDF dependency.

The actual PDF is unencrypted, six letter-size pages with the matching title/author and no JavaScript. I inspected every freshly rendered page. The table, formulas, accents, footnote, reference URLs and page numbers are legible; no clipping, overlap or broken glyph was found. The references now begin together on page 6, so the prior optional split-reference polish issue is resolved. White space on that bibliography page is a harmless style choice.

| Prior requirement/finding | Current disposition, verified globally |
|---|---|
| Original removable assertions permit false -O PASS | **Resolved.** Current explicit If/Raise guards in public source and byte-identical archive; six new false controls fail ordinary/-O. |
| Round1 M1: supplement said express openness in “these sources” | **Resolved.** Current sentence distinguishes2015 express open question from2016 inclusion; repaired archive member matches; ZIP/digests/manifest all verify. |
| Attribution must credit prior disk/peripheral/nilpotent cases and classical JdLG | **Resolved.** Complete current paper, supplement, README and metadata do so. |
| No full-disk novelty or worldwide/continued-openness claim | **Resolved.** Current selected prose explicitly disclaims those claims. |
| Finite counts, floating classification and repetition must be accurate | **Resolved.** 2154 exact/discrete plus 566 floating per mode; 2720 per mode, not 5440 distinct; analytic proof separated from finite controls. |
| Portable archive default layout/current artifact/provenance | **Resolved.** Fresh native run from extracted archive root; current artifact hash, preserved source identities and all receipts verified. |
| Round1 optional bibliography split | **Resolved style change.** Only TeX change from round1 is newpage before bibliography; all current PDF pages newly inspected. |

No newly detected mandatory finding or unsupported route remains. These dispositions are based on current evidence, rather than inheritance of old PASS verdicts. `FINDING_DISPOSITION.json` distinguishes required and optional items.

## Closed result and exact remaining gap

The strongest independently verified result is the exact two-row analytic classification and scientific/reproducibility readiness of the selected frozen package under its bounded historical framing. No remaining mathematical or package repair was identified. Worldwide priority and conventional human peer review remain outside this result and are openly unclaimed. Future publication/API operations require their own authority and evidence.

`CLOSED_CUSTODY_MANIFEST.json` covers all selected files, metadata, frozen manifest, actually consulted external inputs, extracted archive bytes, computations, process records, full streams, snapshots, visual/extraction evidence, reports and logs. The manifest and its detached hash exclude themselves from their artifact list to avoid self-reference. A final independent rehash check closes package custody and verifies that selected package bytes still match the initial read.
