# Independent complete-record adversarial review C

Review finalized: 2026-10-07T05:06:04.285658+00:00. Reviewer: `/root/record_review_c`, newly assigned to the complete revised record, with a separately delegated read-only construction falsification pass. No frozen files, git state, upstream sources, deposit or tracker were modified. No external individual was contacted.

## Exact reviewed version and verdict

Reviewed `record-v3`, the 62-file authored snapshot in `VERIFICATION_FILESET.json` / `reviews/record_v3_fileset.json`. Manifest SHA-256: `059fcc657768b1bd7124d9665ad5980286fcb39ddfaebef6a081198f207a755f`. Exported PDF SHA-256: `a118a16c3a652b981b0061531a582bf64fe5ba9478895fea30e4783b2e5d1677`. Reproduction program SHA-256: `454e85e09d31467a69eda7ac60abe24bf4fd77f5baf566ec907dcd92bcedfbff`.

**No substantive issue identified in the latest exact record within the reviewed scope.** The conditional reductions and their representation/complexity claims are mathematically supported; the imported theorem's scope is stated accurately; the record does not establish a new in-scope research contribution or a completed publication goal. Withholding a new-solution Zenodo deposit is consistent with the user's priority boundary. This verdict is limited evidence, not formal certification, conventional human peer review, or a claim that an independent agent vote proves the upstream theorem.

The recorded v2 checker defect is repaired. The v3 constructor is invoked with an explicit output destination after its copied fixture is deleted, and the complete freshly generated JSON is compared. Independently changing the first saved requested degree from 2 to 99 in a disposable copy, and rehashing its manifest so that the hash check passes, causes v3 to exit 1 with `Construction JSON differs from saved output`. A successful copied-fixture equality cannot produce the current pass. No other substantive checking defect was found.

## Actual scope

I read the local policy and original research target, the complete current TeX and five-page exported PDF, exact theorem/dependency/approach/log/decision documents, both READMEs, licenses and BibTeX. I inspected the extension and construction proofs/pseudocode, algebraic/analytic/geometric source audits, both priority notes, the new-scope search and coherence counterexample. I read the arithmetic, linear-algebra, factorization, construction, comparison and consolidated-reproduction programs. Saved data were compared with newly executed outputs, and receipt/manifest/version qualifications were checked. Earlier reviewer reports were treated as historical records; their favorable findings were not used as mathematical premises.

All 62 current file sizes and SHA-256 values match, with no duplicate paths. I also independently checked all 46 source-manifest entries against both their pinned copies and the read-only upstream clone, whose HEAD remains `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The historical v2 ZIP exactly matches its 49-file manifest; its additional manifest member and nested historical records are explicitly historical. No source scans, upstream tree, caches or secret files occur in that archive. The current authored fileset excludes the research-only third-party copies.

Primary inputs inspected independently include family142's exact introduction/theorem and full auxiliary-prime analytic section; family029's exact all-cyclotomic theorem and selected zero-density, contour and final Mellin proof sections; the actual family003 solution declarations and their fixed-field definition; source citation READMEs and upstream README; Berlekamp's original §5 trace-separation passage; Shoup's §§3–4 primary reduction passages; and Rai's primary Algorithm 2, representation and orbit argument, with its ECCC public record. A separate read-only construction reviewer checked the complete construction supplement against Shoup §§2–4, including the prime-power branches and Lemma 2.4.

This fresh complete-record review does **not** independently redo every representation-theoretic calculation in family029 or every symbolic norm/divisor step of family142. Their complete needed-source audits are separately preserved and their precise scope is disclosed. I checked the pivotal interfaces and inspected original proof nodes rather than assuming that publication, a Lean directory or earlier verdict establishes the theorem. No enormous prime-field branch, full norm solver, Lean build or transitive Lean axiom audit was executed. The review makes no broader source-certification claim.

## Mathematical falsification attempts

### Factorization and representation

The CRT identities give the q-fixed algebra K-dimension s and p-fixed algebra F_p-dimension s. The direct matrix has um rows and columns over F_p; treating p-Frobenius as K-linear would fail, and neither proof nor program does that. The trace construction applies quotient-algebra powers to q-fixed elements, whose component values are in K. It is not an unjustified coefficientwise trace of arbitrary quotient elements.

The nonzero trace-polynomial argument remains valid when p divides m. Multiplication by a nonzero component difference, together with the full power basis, proves pair separation. The first power relation is unique at its first dependence and equals the product over distinct F_p component values, so its coefficients really are in F_p, it is squarefree, and its degree is at most s. Checked roots reconstruct the entire queried polynomial; gcd level sets partition the squarefree support. Early termination after s blocks is justified by the known fixed-algebra dimension.

The squarefree procedure was checked factor by factor. Its residual C contains exactly factors whose current multiplicities are p-divisible; inverse coefficient Frobenius uses a^(p^(m-1)), including the identity exponent at m=1. No loop up to p or q is hidden in powering or exponent-index division. Disjoint emitted supports give sum of degrees at most n, which justifies the global mn/n call bounds and mn²/n² sum-of-query-degree bounds. Constants retain their leading coefficient; zero has an explicit undefined-factorization status/rejection. Both interface conventions are qualified, rather than zero being silently assigned irreducible factors.

All coefficient coordinates remain canonical residues. Dense field/input size includes h and the leading coefficient; exponent bit lengths are O(mL), multiplicities have O(log(n+1)) bits, and Gaussian elimination uses exact arithmetic. Schoolbook multiplication and extended Euclid provide the theoretical field-operation bit bound. The independent direct reference uses exponent inversion instead; its supplement explicitly accounts for the extra factor and retains a polynomial bound. Toy oracle and comparator enumeration is confined to verification and is not substituted for the uniform theorem.

### Construction

The degree-md lift's orbit length is md/gcd(md,m)=d, independently of the chosen isomorphic copy of the supplied field; no primitive root or isomorphism oracle is needed. Degree-one outputs and m=1 are handled explicitly. Trial division factors only the numeric dense-output degree N=md, not an arbitrary binary integer.

For odd r different from p, exact root orders justify the selected cyclotomic factor degrees and the prime-power binomial, with the trace generator certified by distinct residues. The r=p Artin–Schreier tower's nonzero absolute trace certifies irreducibility and its chosen generating element. The p=3 mod4 quadratic branch handles the genuine fourth-power exception; the preserved F3 factorization is correct. Coprime composita and flattening keep the required algebra and matrix dimensions polynomial. Oracle degrees at most N², O(NL log(N+1)) calls, O(NL)-bit valuation integers, and the deliberately loose polynomial overhead are compatible with dense output size. No factoring of p-1 or primitive-root oracle appears.

The reference constructor implements only documented feasible portions and fixed small fixtures. Its restrictions are stated explicitly; it does not masquerade as a full universal implementation. Optional root extraction is a factoring consequence polynomial in numeric r, with no binary-log-r promise.

### Imported input and scope

Family142's main theorem includes multiplicities and has the quoted fixed bit exponent. Its large-characteristic auxiliary-prime reduction depends on numeric auxiliary size E. Family029's input covers all finite-order Hecke characters over cyclotomic fields containing mu12, including principal poles and arbitrary height/conductor. The field Q(mu_(12q)) and its cyclic Kummer extension satisfy the application assumptions. The fixed numerical strip converts the explicit formula to a polynomial numerical auxiliary-prime bound. A field-dependent onset in family029's final Mellin estimate does not shrink its common convergence half-plane.

Actual family003 declarations refer to Dirichlet functions and a Hecke family defined over `CyclotomicField 3 Q`. They cannot replace the varying cyclotomic input. The manuscript correctly states that no relevant Lean build or formal follow-on verification was reproduced. Finite Gauss, matrix and exponent checks are presented as bounded consistency/falsification checks, not analytic nonvanishing certificates.

## Fresh reproduction and evidence

Executed the required clean command with output `reviews/record_review_c_receipt.json` and PDF compilation. All seven unittest families pass, including 377 exhaustive small monic inputs. All 346 direct/trace/trial-divisor comparisons pass. The four trace examples reproduce byte for byte; the five direct examples reproduce structurally apart from Python metadata; all six complete construction fixtures/statistics are freshly generated and equal; the exact F25 coherence counterexample matches. All three dependency finite-check scripts execute and their saved structures match with stated numerical tolerances. Counts overlap and are not additive independent coverage.

I independently tested two further mixed-multiplicity cases: F27 represented by T³+2T+1 with multiplicities 9 and 4, and F16 represented by T⁴+T+1 with multiplicities 8 and 3. Here p divides m and Tr(1)=0 in both fields. Distinct linear factors and multiplicities agree between the independent direct and trace implementations. These additional finite checks, source hashes and the stale-data rejection are recorded in the receipt.

The exported PDF was freshly rendered and all five pages inspected. Formulas, text, references, author/ORCID, page breaks and disclosure are legible; no clipping, unresolved citation or missing glyph was found. All fonts are embedded. The PDF metadata identifies Alec Kriebel and an attributed consequence record with no Zenodo deposit. An additional independent clean compilation has exactly the same extracted text as the exported PDF (text SHA-256 `411cdca9f9988e56e90f70dda82f376a63f211eb11bf853648e6859894ae898d`), beyond merely observing a successful editor preview or build.

Historical clean-v1/v2 receipts' construction equality flags remain unsupported as regeneration evidence; the response and current README explicitly qualify them. The v3 preflight has its own prefreeze manifest hash and is not substituted for this exact 62-file review receipt. This review's receipt records the current manifest hash above.

## Priority, publication and minor wording

Berlekamp's original primary passage supplies all power-basis trace coordinates and the nondegeneracy/gcd separation argument. Shoup's primary theorem supplies the deterministic construction reduction, already with arbitrary supplied extension bases. Rai Algorithm 2 explicitly supplies the degree-product lift and lexicographic selection; the ECCC record supplies the earlier October 4, 2024 disclosure. The new mathematical input comes from OpenAI, and its supplied author/title citation information is preserved. A syntactically broader combined theorem or explicit accounting does not by itself establish a new mathematical contribution. The record does not claim literal duplication of a previously printed combined theorem or exhaustive priority knowledge.

The new-scope search is appropriately bounded. It distinguishes publicly stated canonicalization from a fully audited proof, preserves a false pairwise-choice shortcut, and supplies no primitive-root, Conway-polynomial or unsupported coherent-map upgrade. Its counterexample is exact and not advertised as a new theorem.

No substantive novelty or mathematical reason to reopen new-solution publication emerges from this review. The absence of a deposit, DOI and tracker row is honestly stated and the persistent publication goal remains incomplete. An accurately attributed repository record is not described as a production Zenodo publication.

One minor wording observation: LICENSES.md's exclusion of fonts should refer to standalone font files. The PDF necessarily embeds ordinary Latin Modern/MSBM subsets; embedding does not make those fonts newly authored prose or relicense them. This is not an identified redistribution or mathematical blocker. The parent plans a post-freeze factual clarification without changing reviewed proof/code bytes. This review does not approve an unreviewed altered mathematical package.

## Completion and limits

The assigned complete-record inspection and feasible reproduction are complete (local review estimate 100%). This is not a percentage of the requested novel publication goal, and it is not evidence of theorem truth. No known substantive issue remains in the exact record after this fresh pass. The strongest supported output remains an attributed inherited consequence and verification package. A materially changed proof, algorithm, dependency or novelty claim requires a fresh review; this verdict supplies no authorization to manufacture a new-solution deposit or mark the publication/tracker goal complete.
