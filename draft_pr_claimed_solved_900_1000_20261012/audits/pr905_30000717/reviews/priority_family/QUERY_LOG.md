# Priority audit query and access log

Local date: 12 October 2026; literature cutoff: 2026-10-12. Queries below were actually issued in the audit, grouped by purpose. UTC research checkpoints are recorded separately. This log does not pretend to retain per-query wall-clock times that were not captured. Web index results, including unrelated hits, served only to discover sources; mathematical conclusions use inspected primary material.

## Exact target and counterexample search

- `"tangency variety" "sum of squares" counterexample`
- `"10.4171/owr/2007/14"`
- `"tangency ideal" "counterexample"`
- `"Robinson" "tangency" polynomial`
- `"truncated tangency" "counterexample"`
- `"Schweighofer" "Conjecture 2" tangency`
- `"tangency variety" "Schweighofer" "conjecture"`
- `"Schweighofer" "conjecture" "tangency"`
- `"tangency variety" "not" "sum of squares"`
- `"truncated tangency" "Conjecture" -site:researchgate.net`
- `"tangency" "ideal" "Schweighofer"`
- `"tangency ideal" polynomial sos`
- `"tangency" "Robinson form"`
- `"tangency variety" "sum of squares modulo"`
- `"tangency" "sum of squares" "false"`
- `"tangency variety" "counter-example"`
- `"gradient ideal" "Conjecture 2" "Schweighofer"`
- `"tangency" "Robinson" "sos"`
- `"tangency variety" Robinson sextic sums squares epsilon`
- `"Robinson" "real vanishing ideal" sum squares`
- `"OWR-1465-011"`
- `"tangency certificates" counterexample polynomial`
- `"tangency variety" "ideal" "counterexample" sums`
- `"Robinson" "tangency" "epsilon"`
- `"Conjecture 2" "Reelle Algebraische Geometrie"`

Outcome: original report, truncated-tangency literature and classical SOS sources were identified. No earlier **exact** target obstruction was authenticated. Many broad queries produced unrelated results, which were discarded. No historical conclusion follows from those null or irrelevant results.

## Truncated-tangency literature and full-text access

- `"Ha" "Pham" "truncated tangency variety" 2008`
- `"Global Optimization of Polynomials Using the Truncated Tangency Variety" pdf`
- `"Global Optimization of Polynomials Using" "941" filetype:pdf`
- `"Solving polynomial optimization problems via" filetype:pdf`
- `"080719212" pdf`
- `"GLOBAL OPTIMIZATION OF POLYNOMIALS" "HÀ HUY" "pdf"`
- `"truncated tangency variety" "Robinson"`
- `"truncated tangency variety" pdf -site:researchgate.net -site:doczz.net -site:scribd.com`
- `"Global Optimization of Polynomials" "Huy" "Son" filetype:pdf -site:researchgate.net -site:scispace.com`
- `Hà Pham truncated tangency 2008 PDF`
- `"global optimization" "truncated" "tangency" "pdf" -site:researchgate.net -site:doczz.net -site:scispace.com -site:citeseerx.ist.psu.edu`
- `"Representations of Positive Polynomials" "Pham" pdf`
- `"truncated tangency" "Robinson" "2008"`
- `"Pham Tien Son" "publications" "2008" optimization`
- `"tangency" "Ha" "Pham" site:ictp.it`
- `"truncated tangency variety" "941" -site:researchgate.net -site:scispace.com -site:scribd.com -site:doczz.net -site:citeseerx.ist.psu.edu -site:epubs.siam.org -site:math.ac.vn -site:hdgsnn.gov.vn`
- `"Global Optimization of Polynomials" "truncated" "full text"`

Primary access attempts:

| URL or route | Observed outcome |
|---|---|
| `https://epubs.siam.org/doi/10.1137/080719212` | Bibliographic record, abstract, references and citing list read. |
| Publisher's “View PDF” link `/doi/epdf/10.1137/080719212` | Redirected to abstract/purchase page. |
| `https://epubs.siam.org/doi/pdf/10.1137/080719212` | HTTP403; no complete article. |
| Crossref record for DOI10.1137/080719212 | Publisher PDF URL authenticated; raw metadata kept private. |
| OpenAlex work W1984903186 | Reported closed access, no repository full text. Index report alone does not prove no copy exists. |
| Publisher-provided preview discovered via ResearchGate | First-page preview only; not used to infer later contents. No author-copy request or contact was initiated. |
| `https://www.sciencedirect.com/science/article/pii/S002240490900070X` | Publisher abstract/index visible; subsequent direct access returned403. |
| Publisher `/pdf` for that PII | HTTP403 despite open-archive metadata. |
| Elsevier content API for PII, `httpAccept=text/xml` | Returned a 1986-byte metadata-only response, not article body. |
| Crossref/OpenAlex for DOI10.1016/j.jpaa.2009.03.014 | Bibliographic and open-archive metadata checked. |
| Author-hosted Guo et al. `gcv_sos.pdf` | Complete eight-page PDF retrieved, with candidate-matching hash. Relevant statements and examples read. |
| Laurent author `moment-ima-update-new.pdf` | Complete PDF retrieved; §7.2.3 read. |
| Pham arXiv1902.06041 | Complete v2(2019) manuscript retrieved and targeted reading performed. Later journal version identified, not fully read. |

Outcome: multiplier/inequality distinctions verified from complete independent primary texts. The complete 2008 and 2009 articles remain access gaps; their unavailable sections were not treated as inspected.

## Classical attribution and general varieties

- `"Robinson" "ten" "cubic" Reznick`
- `"sums of squares" "union of lines" Robinson`
- `"Some concrete aspects of Hilbert" Reznick pdf`
- `"reznick" "paper34.pdf"`
- `"Some concrete aspects" "253" "ten"`
- `"Some concrete aspects" "2000" "pdf"`
- `"Some concrete aspects" Reznick arxiv`
- `"positive polynomials" "real curves" "Scheiderer" pdf`
- `"tangency" "sums of squares" "counterexamples"`
- `"Sums of squares on reducible real curves" Plaumann`
- `site:illinois.edu "~reznick" "hil17"`
- `site:illinois.edu "Some concrete aspects" pdf`
- `site:ams.org "Some concrete aspects"`

Access and authentication:

- Retrieved the original report and Schweighofer2006 author PDF, with exact hashes agreeing with the candidate's source manifest. Relevant source formulas were rendered locally.
- Reznick's old UIUC/Illinois `Paper34.pdf`/`hil17.pdf` links timed out or404ed; clicking the author's old link exposed a broken domain redirect. The current migrated author domain `https://reznick.web.illinois.edu/Paper34.pdf` supplied the complete 22-page publisher reprint. Printed p259 was visually verified.
- The UC Davis `Reznick9.pdf` scan supplied the earlier 20-page seminar version; pp7–8 were rendered. `Reznick1.pdf` was also downloaded during discovery but not used for conclusions. Earlier-version and publisher pagination were kept distinct.
- Crossref DOI10.1090/conm/253/03936 plus the Illinois institutional bibliography authenticated the2000 publication. AMS direct record/endmatter access returned403; the authenticated author-hosted publisher reprint resolved the relevant content gap.
- Publisher and Crossref authenticated Laurent's chapter DOI10.1007/978-0-387-09686-5_7 and publication pp157–270. The accessible manuscript locator remains pp117–118.
- Retrieved Plaumann arXiv0808.0460v4 and inspected the general curve-obstruction/classification locations in the evidence table. This does not identify the candidate's exact polynomial family.

## Citation graph screen

Fetched these indexing-service endpoints as discovery metadata:

- `https://api.openalex.org/works?filter=cites:W1984903186&per-page=100`
- `https://api.openalex.org/works?filter=cites:W2070850517&per-page=100`

The responses contain55 and31 records. Deduplication by OpenAlex work ID, restricted to publication date at or before2026-10-12, gives66 distinct records. Titles, dates, DOIs and seed edges are sanitized in `CITATION_GRAPH.json`; abstracts, author/contact information and raw responses are not redistributed. The SIAM2008 publisher citing list was also inspected through its September2026 entries.

Selected graph nodes were followed to primary texts or publisher descriptions: Laurent2009; Guo et al.2010; Hà–Pham2010; Pham2019/2022; the2009 truncated paper. Other titles involving Jacobian/KKT certificates, genericity, homogenization, noncompact optimization, strips, coercivity and attainment were screened at metadata level. No claim is made that all66 complete texts were read. Bibliographic dates may differ among publication-online, print and indexing records.

## Stopping rule and retained gap

The bounded priority task is complete when exact source identity, classical attribution, nearby-result boundaries, attempted access routes and residual coverage gaps have checkable records. A search-absence inference is explicitly rejected. Reopen historical priority only with materially new accessible text, an exact earlier theorem/counterexample, or an authenticated correction/status source. No external communication was prepared or initiated, and no Git mutation was made.

## Root-reported supplementary access follow-up

During sealing, root reported a separate six-query follow-up using the exact2008 title with `filetype:pdf`, DOI080719212, Hà/Pham names plus tangency, and domains `scholar.dlu.edu.vn`, `publications.ictp.it` and `arxiv.org`. Root found institutional bibliographic listings but no full2008 article. This supplement was reported by root, not independently re-executed by this family; its exact six query strings were not supplied and are not reconstructed here.

Root reported that the web tool marked `scholar.dlu.edu.vn` robots-blocked, without retry. Two bibliographic sources were identified: [Dalat institutional CV](https://ktt.dlu.edu.vn/Resources/Docs/SubDomain/ktt/Li%20lich%20khoa%20hoc/LLKH_PhamTienSOn.pdf) and [Institute of Mathematics2008 annual report](https://math.ac.vn/uploads_manager/Baocaotongket/2008_HDKH.pdf). These do not close the full-text gap. No external contact was initiated.
