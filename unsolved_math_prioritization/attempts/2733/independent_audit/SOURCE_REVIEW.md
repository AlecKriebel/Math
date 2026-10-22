# Independent source and corpus review

## Result

PASS within the explicitly bounded scope below. Full local corpus bytes, exact record identity, complete problem/report serialization, and five source-PDF byte/page pins reproduce the frozen author metadata. Relevant mathematical claims were checked against primary sources. No raw dataset, source PDF, source extract, private source, personal data, or private coordination material is included in this audit package.

## Full-input and identity gate

The complete catalog and problems arrays each contain 15,458 records; the report mapping contains 6,701 keys. All three full files match the expected byte counts and SHA-256 values in CORPUS_VERIFICATION.json. ID 2733 occurs exactly once in each array. Its catalog rank is 907 and its number is KP-1.74. The independently computed UTF-8 statement digest is 0697193ff65093da9abc34c354a747974b2dfedc0f9db20372d79336626545b7. The complete problem record, together with reports.get(problem_number,{}) and Python's default json.dumps(...,sort_keys=True) serialization, produces 3728d6f7692daadc11b003a16e89a90a49832dd78bdeb4fe0719072b0d1e81e0. This is not a digest of a selected subset of fields or normalized text. There is no KP-1.74 report entry; the selected report is empty. The background contains dated literature triage rather than a substantive inherited proof or computation. The older triage's AIM URL was not accepted as a substitute for the actual K3 problem text.

## Primary mathematical sources

All five local PDFs were independently rehashed and passed pdfinfo page counts; exact metadata appear in PDF_VERIFICATION.json. This confirms the local inspection inputs, not an immutable claim about future bytes served at the URLs.

- K3: the 436-page author-preliminary PDF was independently opened live, and the pinned local PDF was inspected through freshly regenerated text at printed pp. 11, 67 and 69–70. Renderings of pp. 67 and 69 were visually inspected. The smooth knot-type convention does not add a nontriviality qualifier. The local statement admits arbitrary knot/link types, uses radius-one thickness, and exhibits the Hopf-link normalization. The report correctly notes the infimal/supremal wording issue and labels the PDF preliminary; no claim about a final published version is added.
- CKS02: the author PDF is pinned, but its garbled mathematical text extraction is not used to justify exact formulas. The independently pinned arXiv v3 PDF supplies readable text. Fresh extraction matched the inherited extraction byte-for-byte. Lemmas 1, 2 and 4, Theorem 7, Figure 1 and the relevant link discussion support the regularity/thickness framework and prior chain family. The theorem-level mathematics is discussed separately in MATHEMATICAL_AUDIT.md.
- CLR12: freshly regenerated text matched the inherited author-PDF extraction byte-for-byte. The abstract, pp. 3–4, Section 2.3 and Section 3.2 support the prime-factor composite domain, the approximate splicing/tightening procedure, and the absence of a general global-minimum certificate. Its arXiv abstract was also retrieved live. These observations support an intended-domain inference; they do not prove what the uninspected full 1997 article implicitly required.
- Milnor50: the pinned 11-page PDF was independently extracted; Theorem 3.4 on printed p. 254 gives the relevant total-curvature lower bound. The authored mollification argument supplies the C1,1 bridge rather than leaving it implicit.

## Current-context and access checks

On 2026-10-06 the exact UnsolvedMath page could not be read through the web tool, on either the plain or www host. A separate standard HTTPS request to the www host independently returned HTTP 403. The live statement was not inspected; its identity is established from the pinned full corpus and the actual K3 text instead.

The Nature article URL was again inaccessible through the web tool because of a redirect/fetch failure. This audit did not obtain or inspect the full original Nature article. Primary-site search results corroborate its title, DOI and bibliographic identity. A direct PubMed page open yielded no useful abstract; a separate standard HTTPS request returned status 203 with no extractable abstract. Primary PubMed search results exposed a limited abstract snippet. Thus the author's earlier full-abstract inspection remains a historical claim and is not falsely described as independently reproduced here. This limitation does not affect the proof or the intended-domain inference from CLR12.

The Cambridge publisher page was retrieved and its abstract, introduction and displayed Theorem 3.1 were inspected. It concerns a crossing-number lower bound for alternating knots. It does not furnish the connected-sum upper bound required by the present problem. The bibliographic issue/year/pages and DOI agree with the frozen report.

Klotz's arXiv version-1 HTML was retrieved. Its abstract and introduction concern bounds and constructions for T(Q,Q) torus links; the page explicitly identifies v1 dated 2 March 2026. This audit does not claim a full verification of that preprint or an exhaustive search for later work. No universal connected-sum theorem was verified in these inspected portions.

## Repository search history

The three bounded GitHub searches described by the author were repeated against AlecKriebel/Math: default-branch files for 2733 (top 10); all-state pull requests for 2733 OR "KP-1.74" OR ropelength (top 20); commit messages for ropelength (top 20). All returned empty lists without tool errors. The inherited empty responses agree. These queries cannot prove repository-wide absence, absence from every branch, or mathematical novelty. No repository state was changed.

## Limits

A digest verifies byte identity, not truth of source contents or historical execution time. This audit verifies current source observations and distinguishes them from the author's earlier retrieval/inspection attestations. It does not authenticate every historical tool call, inspect the entire K3 volume, inspect the unavailable Nature full text, formally verify every cited theorem, or prove exhaustive literature absence. The accepted conclusion remains a partial formulation issue with intended (a) and (b) unresolved.

Public URLs and source-PDF pins are recorded in PDF_VERIFICATION.json and SOURCE_INSPECTIONS.json. No source text is reproduced here.
