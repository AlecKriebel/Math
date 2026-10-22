# Independent original, mathematical and existing-publication review: PR1276

The pinned proof correctly gives a full negative answer to the original mutual-multiphase-domination question. Ferudun's already published Theorem3.1(1) is the same counterexample after an invertible change of component measures. The existing publication is missing from the inspected spreadsheet. One qualified existing-record row is proposed; no new manuscript, Zenodo record or DOI is needed. This packet approves no operational action and performs no external write.

## Bound source and exact original question

Fresh GitHub connector metadata found PR1276 draft/open at unchanged head24f42e149be5b54b579129f739d7f7be9a1e7f92, base4b27092a448d53b61408355ce44ec38d103a1ce4. Its body SHA256 is8d532b5b5e553c87ab12c98e714c559e874eb734c1b213dde536970bfa8bf805. All six actual added files were independently recovered from local Git objects and verified by Git blobSHA1 and SHA256, with the public manifest checked. The full proof, audit, acceptance and other files were read. The PR supplies no corresponding QUEUE edit; the missing-status full-claim route therefore applies, rather than an explicit non-claimed-solved status.

The fresh [primary EMS PDF](https://ems.press/content/serial-article-files/46673) matches the historical5849366-byte SHA256400d411ff8310f28bd79aab8211bb60d57789fb54f61538dc26396689c7ade05. Printedpp388-390/PDF50-52 were extracted; PDF50-51 were visually checked. Wolansky's question asks whether two atomless positive vector-measure spaces that dominate each other admit deterministic componentwise transports in both directions. A common transport family must serve all components. No inverse-map, common-dimension, continuity, component-independence or completed-sigma-algebra restriction is stated. The repeated reverse-space and N/k slips are transparently corrected, not used as loopholes. Subsequent optimal-transport assumptions do not modify this earlier question. The report is labelled OWR7/2017; its Crossref publication date is2018-01-02. Its DOI10.4171/OWR/2017/7 identifies the original report, not the solution.

## Independent mathematical verdict

The PR uses Borel X=[0,1], Y=[0,1]^2 and component probabilities with densities(1,2x) and(1,2u). Bounded-density cuts prove scalar atomlessness and atomlessness of the total positive measures, hence the vector condition. For every x, the common probability kernel delta_x tensor Lebesgue is countably additive and Borel measurable on all Borel target sets by a monotone-class argument. Tonelli verifies both component identities. The reverse common kernel is the deterministic projection(u,v)->u.

A putative forward map T=(a,b) has integral a^2=1/3 from the first component and integral xa=1/3 from the second. Thus integral(a-x)^2=0, so a=x almost everywhere. The Borel graph of b has area zero by its singleton vertical sections, whereas the pushforward of interval Lebesgue gives it mass one. This contradiction rules out the forward map. Since the question requires both maps, this disproves its entire universal implication; failure in both directions is not necessary. DERIVATION.md gives each deduction, including atomlessness, measurability and the topology-free nature of the obstruction.

Completed-source-measurable maps into the Borel square have Borel versions of both coordinates. Absolute continuity preserves both pushforward identities under this single almost-everywhere replacement, so the contradiction remains. A map into a completed planar target would also have to satisfy the Borel identities. This does not construct a simultaneous extension of the forward kernel to every completed planar target set, and neither the PR nor this audit asserts one. The original category already admits the Borel counterexample, so the boundary does not reduce the result to a partial answer.

The strictly positive continuous second-density variant(2/3)(1+x)/(2/3)(1+u) has mass1, uses the same kernels, and yields the same integral xa=1/3 after subtracting integral a=1/2 from5/6. It therefore has the same obstruction. Reference-measure normalization and the endpoint density zero introduce no hidden hypothesis. No mathematical correction was found.

## Exact prior-result identity and scope

The existing [version DOI](https://doi.org/10.5281/zenodo.23107180) publishes Alper Ferudun's A Negative Answer to Wolansky's Question on Mutually Dominating Multiphase Measure Spaces, version1.0, dated2026-10-02. The actual PDF's Theorem3.1(1), its proof, relevant definitions/rigidity lemma and status disclosures were inspected in text and visually. The target construction uses densities(x,1-x) on the interval and(u,1-u) on the square, the same vertical kernel/projection, and the same Borel-version graph obstruction. Its displayed source TeX agrees at the relevant theorem/proof. This is a proved full counterexample, not a generic cited background result or a merely numerical experiment.

The invertible component change(alpha,beta)->(alpha+beta,2alpha), with inverse(alpha,beta)=(sigma_2/2,sigma_1-sigma_2/2), produces the PR densities. Pushforward and kernel integration are linear, so one common transport works for one pair exactly when it works for the other. The inverse's negative coefficient is used only to recover equalities between already positive named measures. It does not require a positive inverse on all possible vectors. The PR is therefore a verification/rederivation of this exact prior result.

The prior PDF and public metadata call the paper an unrefereed, AI-assisted preprint. That status is preserved. The interval/square theorem alone resolves the original negative question. Other examples, positive fiber theorems, finite classifications and the source's broader priority discussion are outside this review. No assertion of Ferudun's historical firstness, exhaustive literature clearance, current worldwide openness or external human peer review is adopted. Those claims are unnecessary to reconcile a mathematically checked already-published full answer.

## Published record, DOI family and all payloads

Fresh native HTTP GETs authenticated the full raw Zenodo record: id23107180, published/done/submitted=true, version1.0,2026-10-02, creator Ferudun, Alper, Mercury Software GmbH, exact title and public preprint status. It is strictly identical to the supplied root raw capture, including all unknown fields; ROOT_TO_LIVE_RECORD_DIFF.json records no differences. The version DOI and concept DOI10.5281/zenodo.23107179 both resolved with HTTP200 to the exact record23107180. DataCite independently binds title, author, version, issued date and reciprocal IsVersionOf/HasVersion relations. The Zenodo versions endpoint listed one version. The selected row uses the fixed version DOI; concept and version are one publication family.

All three provider-listed files were both recovered from root by SHA256/size/recordMD5 and freshly downloaded. Every fresh payload is byte-identical to its root-authenticated copy:

| File | Bytes | SHA256 |
|---|---:|---|
| OWR-15212-005-paper.pdf |136320|ba25f8852584df11a9da23177bb17f81724e85618a5572243a5f074332b23079|
| OWR-15212-005-source.zip |56880|40ef21eb1fa8f8474d9b0015d6821733dfc928cf37c59c53d3d30194bf382b54|
| OWR-15212-005-verification-report.md |18426|aa7783f186d7a7ce820856b1bb359d6c58a62bcd401531b9e897723bab9aeecc|

The34 ZIP members were independently CRC-tested, safe-path checked and inventoried by size/SHA256. The standalone report equals the archive's verification_report.md. Relevant manuscript source and reproducibility inventory were inspected. No source-author program was executed. Historical claims of large exhaustive/random verification runs remain historical source claims, not checks rerun here. The proof audited here is analytic and does not depend on those broader computations.

## Fresh duplicate check and concrete row proposal

At09:55:59UTC the read-only GWS CLI inspected all43columns of numericgid1254632077 in both UNFORMATTED_VALUE and FORMULA views, with stable full metadata. There were191rows and strict type equality between views. Target problem IDs, both record/DOI family IDs, result phrases, original-source identifiers and labelled PR references yielded no target match. Twenty-four generic Ferudun-surname leads were semantically checked and concern other original questions and results. No private cell content is reproduced here; raw provider responses and private semantic lead data are retained privately, with only decisions/hashes in the public audit metadata.

EXISTING_PUBLICATION_ROW_PROPOSAL.json contains exactly one row, four literal strings with blank B. A binds30003386/OWR-15212-005 and the original question/source. C is the fixed existing version DOI. D gives the exact author/title/version/date/theorem, full negative scope, normalization equivalence, completion boundary, unrefereed AI-assisted status, reviewed-theorem limit, three supporting files, concept-family identity and PR reference. It credits Ferudun rather than implying Alec Kriebel authorship. The problem-source DOI is not substituted for the answer DOI.

This proposal is for root's independent scientific adoption and future operational review. It has action_ready=false and transfers no action approval. No append helper or CASE was created. Fresh live deduplication and publication-state checks remain necessary immediately before any future row write, especially if concurrent publication/ledger changes occur. No new publication is recommended.

## Checkable evidence and closure

The independent diagnostics perform1254 finite exact rational/artifact checks in each of normal, -O and -OO modes, for3762 executed PASS checks. They cover original-to-normalized rectangle integrals, projection marginals, moments, matrix inverses, strict positivity, two wrong-kernel controls, simple graph-line controls and pinned publication/artifact identities. They use explicit exceptions rather than optimization-removable assertions. Their limits are stated: they supplement the written all-Borel and measure-theoretic proof, and neither formally certify it nor reexecute the prior paper's history.

All six PR files, primary sources, complete raw record/DOI/registry responses, supporting payloads, safe ZIP inventory, independent code/results, proposal and written derivation are included in the manifest. The folder is below25MiB. Closed PR1272 and B1v04 were not modified. No Git ref/index/working-file mutation, PR action, Zenodo mutation, spreadsheet write or outside contact occurred. Overall sweep estimate80%; this bounded independent review is complete. Global completeness and a future append remain outside this audit's verdict. AI involvement is extensive; there is no external human peer review or proof-assistant certification of this review.
