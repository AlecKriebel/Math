# Acquisition and scope review — Zenodo23180194

**Scope result: acquisition complete and exact claim mapped. Mathematical clearance remains pending the separate analytic and adversarial reviews.** No finite mathematical verifier was run in this assignment, and this report is not a proof-validity or novelty verdict.

## Published edition and custody

Title: *Measure-only preserving Markov transports characterize mass-stationarity*. Author: Alec Kriebel, ORCID0009-0001-9320-500X. Zenodo version1.0, publication date6October2026, DOI10.5281/zenodo.23180194; concept record23180193. The manuscript itself is dated6October2026 and labelled an unrefereed research note. Inventory row47.

Fresh public metadata and both public assets were retrieved from <https://zenodo.org/records/23180194>. Original bytes, resolved URLs, retrieval times, MD5, SHA-256 and byte lengths are in `sources/receipt.json`.

| File | Bytes | SHA-256 |
|---|---:|---|
| `mass_stationarity_markov.pdf` |103603|`3503e9351da854e882cd8ce26f1450482b44e1f5e547b06224875c3b55b391f3`|
| `mass_stationarity_verification.zip` |35774|`6007977e60dd4464e0c62309ad694697d4f927bae407531b0bee5285e80fa8a9`|

Both match live Zenodo MD5 and size; the manuscript also matches the queue-bound PDF hash. The verification ZIP has19 members. Every member passed path/symlink safety checks and ZIP CRC verification, and its original extracted bytes were SHA-256 inventoried. There are **no additional reader PDFs**. `sources/reader-pdf-map.json` maps the seven-page manuscript, standalone `paper.tex`, and source/verification archive.

An independent size/hash comparison checked all18 declared outer-bundle files, all11 declared verification files, and the archive's external-PDF binding. All matched. This was byte integrity checking only; the published verifier and its mathematical controls were not executed. The evidence is `package-integrity.json`.

## Full claim and proof interfaces

Read all seven manuscript pages, the relevant source definitions/abstract, both required `CLAIM_SCOPE.md` files, the bibliography/credit file, the verifier's program logic and the control-program structure. The proof's two constructions and completion are entirely in the seven-page manuscript; no external reader supplement is silently omitted.

The exact model is:

- A locally compact second countable Hausdorff **Abelian** group G.
- An arbitrary measurable ambient space Ω with a **jointly measurable** G-action.
- A sigma-finite measure Q on Ω and a measurable, covariant, nonnegative locally finite Radon random measure ξ, nonzero Q-almost everywhere.
- Every admissible test kernel is Markov (row mass exactly one), invariant under joint translation, pointwise ξ-preserving, and measurable with respect to σ(ξ) times the spatial Borel sigma-field.
- The invariance hypothesis tests **every nonnegative measurable function of the full ambient state**, not merely functions of ξ.

The claimed conclusion is equivalence with **joint mass-stationarity** and, in the sufficient direction, full joint Campbell/Mecke reversal for every nonnegative measurable function on Ω×G. The source's standard Borel measure space is the canonical space of locally finite Radon measures, not Ω. No standard Borel Ω, sigma-finite marginal law of ξ, finite intensity, finite Q(Ω), or finite ξ(G) is assumed.

The purported new deduction is the implication from these restricted measure-only **Markov** tests to the joint Mecke identity. It uses oriented local symmetric transports off the measure-period set, then normalized transports on the closed period subgroup to recover the residual ambient reversal. The use of all ambient test functions matters: a period of ξ may still move hidden information in Ω. Finite-Q test functions and countable finite product covers are used to avoid subtracting infinite integrals or assuming disintegration over ξ.

The claimed argument subsequently invokes credited classical equivalences. It does not present the Mecke/Palm equivalence, Palm/mass-stationarity equivalence, or necessity of transport invariance as new.

The hypothesis quantifies over **all** admissible measure-only Markov kernels; it is not an effective finite algorithm or a claim that a finite sample of transport tests proves mass-stationarity. The paper includes atoms, diffuse/mixed mass, periodic measures and the zero period-restriction case. It excludes the zero random measure under its nonzeroness convention, non-Abelian groups, and measures without local finiteness. Origin-in-support is a derived claim, not an extra assumption.

## Primary-source interfaces checked

Fresh primary PDFs and text are in `reviews/scope/cache/primary-sources/`; their URLs, hashes, bytes and access outcomes are preserved separately in `primary-references.json` so the evidence remains meaningful even if ignored caches are not retained.

1. **Last–Thorisson2009, official electronic reprint, arXiv0906.2062v1.** Independently read the ambient setup in §2, the transport versus weighted-transport definitions in §3, Mecke/Palm statement(2.7), Theorem4.1, Definition6.1, Theorem6.3, Theorem7.2 and Problem7.3. The original uses arbitrary measurable Ω with a jointly measurable flow and sigma-finite measures. “Transport-kernel” is explicitly Markovian; weighted kernels are separately defined. Thus the formal problem has the test-class distinction used in this note. Equation(2.7) supplies the stated ambient Mecke implication; the source expressly explains its extension beyond Mecke's original canonical setting. Theorems4.1 and6.3 have the required roles. This supports the source-interface mapping, not the new deduction itself. Primary: <https://arxiv.org/abs/0906.2062v1>.
2. **Last–Thorisson2015, pinned author version arXiv1405.7566v2.** Read Theorem6 and its surrounding definition. It concerns the joint pair((X,Z),ξ), density Z positive at the origin, local integrability along every line and infinite integrals on every half-line. It is explicitly described there as a partial solution to Problem7.3. The density-field observations must not be silently replaced by ξ-only observations. This downloaded v2 is listed as revised17July2015 and carries the internal date24April2019. The final SPA full text was not read: the publisher endpoint returned403. No equivalence of author/final editions is asserted. Primary: <https://arxiv.org/abs/1405.7566v2>; journal record: <https://www.sciencedirect.com/science/article/pii/S0304414915001635>.
3. **Original Oberwolfach Report47/2008.** Read Last's p2673 and Thorisson's pp2692–2694. Thorisson explicitly defines transport kernels as Markovian and discusses the general all-kernel converse. Last's closing question is specifically about applying allocations to an inserted Cox process. These are different test classes, so proving the all-Markov statement does not settle the narrower Cox-allocation converse. Primary PDF: <https://ems.press/content/serial-article-files/46189>; publication record: <https://ems.press/journals/owr/articles/2093>.
4. **Last–Thorisson2011, COSA.** The official LSU bibliographic record was checked, but its public PDF endpoint returned403. An author-hosted March2010 precursor was located, but direct retrieval did not yield PDF bytes and the web fulltext request timed out. Accordingly, this review does **not** claim fresh authentication of the exact final-body Proposition3.6/3.8 and Remark3.11 numbering or all the discrete-case qualifications. They remain explicit manuscript credit, and the final-body verification limitation is retained. This is background attribution rather than the logical Mecke/Palm import used by Theorem1. Primary record: <https://repository.lsu.edu/cosa/vol5/iss2/1/>.

Mecke1967's original body was not separately authenticated; the precise ambient formulation used here was checked in the credited2009 primary source. No exhaustive later-literature search or current-openness certification was performed.

## Candidate content and attribution boundaries

`candidate-content.json` contains the full113-word abstract transcribed from the published source, precise metadata, all public download links, a plain-language draft, exact-result draft, attribution, limits and an interesting-result explanation. `abstract-source.tex` preserves the literal source and `abstract.txt` its plain-text version. This is only an editorial candidate; no publication or promotion record and no website page were created.

The genuinely interesting claim to explain, if the mathematical reviews clear it, is that tests whose rules observe only the mass measure can constrain the **entire** ambient state, even through measure-periodic shifts. The arbitrary-ambient/no-disintegration feature is part of that precise claim, not a blanket claim of identifying hidden variables from data.

Crediting Last and Thorisson's formal Problem7.3 as the target is supported by the source. “Affirmative answer in the stated setting” may be used only after proof clearance; “first solution,” “still open until this paper,” blanket resolution of Oberwolfach questions, and worldwide priority must not be asserted. The manuscript's own bounded historical priority reviews are not evidence of those stronger claims.

Status should remain **unrefereed, extensively AI-assisted preprint**, with no human peer-review or formal machine-proof claim. The source/verification archive can be linked as supporting material, but a control count is not proof of the general analytic theorem. The legacy background-intensity Cox controls do not establish the intensity-erased deterministic-allocation question.

**Follow-up: null.** No independently supported, paper-worthy follow-up meeting the user's high bar was established in this scope assignment. Merely repeating the explicitly excluded Cox question without confirming its current status would not meet that bar.

## Independence and disposition

The required record description, scope and bibliography files contain historical internal-acceptance and literature-review status claims; those were incidentally exposed while reading necessary mathematical scope/credit text. They were not adopted as verification. `PRIORITY_NOTE.md`, expected historical review outputs, and historical dedicated reviewer narratives were acquired and hashed without reading their opinion bodies. No sibling report was consulted. No mathematical program execution or analytic/adversarial PASS is claimed.

This assignment is100% complete for acquisition, source mapping and scope. Separate independent analytic and adversarial gates remain required. No repair, outreach, website, spreadsheet, Git, deployment, publication or promotion action was performed.
