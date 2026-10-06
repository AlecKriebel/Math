# PR97 / 10300055: independent question-history priority audit

Completed bounded history-family audit at 2026-10-06 00:17:30 UTC. This report is independent of the other fresh priority family's conclusions: hypotheses were recorded before new searches and OWN_ANALYSIS.md before any exchange of conclusions. Mathematical proof-search turns added: **0**. No PR, queue, publication, Git, or external-service mutation was performed.

## Result and exact scope

**No exact earlier or later resolution of Calegari's conditional Question 13.2 was authenticated in the sources and passages checked. Historical firstness and present-day open status remain unestablished. This family alone does not clear the strict priority gate.** This conclusion neither retracts ROOT's passed mathematical gate nor establishes that the theorem is novel.

The pinned candidate is `repaired_verification_candidate_v1/CANDIDATE.md`, SHA256 `393241cc6299a7a8e7b9a2d72c22e48f574702e0f3c822e0310647a16e0ff4c7`, on PR head `fb50facb2a7389bb272bbf0b5cbd80c24c79b992`. Its main claim concerns a closed oriented smooth three-manifold with a cooriented taut C2 foliation, no spherical leaves, a global nowhere-zero C1 defining form alpha, and a **smooth** contact form omega satisfying d alpha = alpha wedge omega: ker omega is tight in the usual smooth sense. Its separate C1 assertions are exclusion of embedded C2 disks satisfying the stated boundary criterion and tightness of sufficiently C1-close smooth approximations. No equivalence between this disk criterion and every possible low-regularity definition is asserted.

The question-history audit targets the source, attribution, subsequent problem-list history, explicit solutions, and possible nonexistence/existence issues. It does not independently re-prove the candidate or decide whether its classical contact-pencil mechanism already occurs in literature. That is the distinct theorem/mechanism family's remit.

## 1. Authenticate the original question and publication

The actual arXiv author PDF, reused read-only from the shared cache, identifies itself on printed page 1 as September 8, 2002, Version 0.78. Printed page 29 was read in text and **visually inspected** in `calegari2002_page29.png`.

Question 13.1 asks for a defining-form choice with a Godbillon–Vey form of one weak sign, under minimal taut C2, atoroidal, and nonzero evaluated Godbillon–Vey hypotheses. Question 13.2 then assumes that such a choice makes the associated connection form contact and asks about tightness. Thus 13.2 is conditional; proving it does not establish the existence demanded by 13.1. The section immediately below is also numbered 13.2, but is about foliated Gromov norms. Search matches for a bare number therefore require the full statement. [Calegari author version, printed p.29](https://arxiv.org/pdf/math/0209081v1).

The current arXiv record has **one submitted version**, v1 at 2002-09-08 04:30:36 UTC, and supplies the journal reference *Proceedings of Symposia in Pure Mathematics* 71 (2003), 297–335. The publisher DOI resolves to the AMS volume catalog, whose contents identify Calegari's chapter. Crossref's publisher-deposited record agrees on title, author, year, and page range: **DOI 10.1090/pspum/071/2024640**. [arXiv version record](https://arxiv.org/abs/math/0209081), [AMS chapter DOI](https://doi.org/10.1090/pspum/071/2024640).

These records authenticate publication, **not equality of the author and final published texts**. The actual advertised chapter PDF link, its filename found in the returned page, and the advertised full-volume PDF all returned HTTP 200 with access-selection HTML. The chapter access page itself was saved and read. No credential use or access bypass was attempted. The final 2003 chapter remains unread, so its question numbering, exact wording, added answers, and corrections cannot be certified. No final-edition page number for Question 13.2 is inferred from the 2002 pagination.

## 2. Later author sources and correction history

The author's book *Foliations and the Geometry of 3-Manifolds* is a **2007 Oxford University Press book**, with the author's page dating publication to May 2007 and hosting its PDF with publisher permission. It is a separate work from the 2003 AMS chapter. The PDF title page and preface were checked. The book's relevant Godbillon–Vey cocycle material is on printed pp.110–112; Example 4.33 on pp.160–161 discusses symplectic filling of taut-foliation plane fields; Corollary 5.42 on p.208 concerns fibered links; pp.217–218 and 279 use “disk of contact” for branched surfaces; p.316 recalls a Godbillon–Vey cocycle in a Hilbert-space discussion. None of those actual passages states the candidate's conditional conclusion or labels Question 13.2 solved. The book was searched throughout but **not read cover to cover**. [Author's book page](https://math.uchicago.edu/~dannyc/books/foliations/foliations.html), [authorized book PDF](https://math.uchicago.edu/~dannyc/books/foliations/oupbook.pdf).

The author's Spring 2016 course path currently contains a document dated **January 20, 2024**, not an authenticated 2016 publication. The current book-work-in-progress Chapter 4 is dated **December 3, 2024** and follows both 2016 and 2023 courses. Their titles, dates, contents, references, and relevant full-text keywords were checked; neither returned a substantive contact/Godbillon–Vey tightness passage. Chapter 5 is dated **November 28, 2023**; its Theorem 2.13 and Corollary 2.19, printed pp.13–16, discuss Eliashberg–Thurston contact approximation and symplectic thickening. No Godbillon–Vey connection-form conclusion was located. These notes have the author's work-in-progress disclaimer, so they are not a certified complete list of resolved problems. [Current chapter index](https://math.uchicago.edu/~dannyc/books/3manifolds/3manifolds.html).

Calegari's October 9, 2009 article *Harmonic measure* was read in its actual main text. Its leafwise Godbillon class and averaged circle-bundle connection are relevant terminology, but the article does not give the contact-tightness conclusion. Its omega denotes a different connection construction. [Author article](https://lamington.wordpress.com/2009/10/09/harmonic-measure/).

No correction or explicit resolution of this question was authenticated through the checked author pages, exact-title/DOI searches, or question-number searches. This is not a claim that no such correction exists. Crossref reports nine incoming citations, but this audit does **not** represent that count as a checked inventory of all citing papers.

## 3. Subsequent problem collections and related source text

| Primary source | Actual material checked | Relevance to the exact conditional question |
|---|---|---|
| Hurder, *Foliation Geometry/Topology Problem Set*, September 2003, updated October 28, 2003 | Introduction pp.1–3; Godbillon–Vey section pp.20–21; reference 68 | Explicitly excludes 3-manifold problems and confoliations/contact structures, pointing to Calegari's list. Its silence cannot support an unresolved-status claim. |
| Hurder, *Problem Session – Foliations 2012*, version January 10, 2013 | Problem 7.2 p.5; Problem 13.2 and nearby text pp.9–10; relevant references | Problem 7.2 concerns a conformal-geometric interpretation of GV. Its Problem 13.2 concerns contractibility of spaces of compact foliations and is unrelated to Calegari 13.2. |
| Nariman–Yazdi, *Problem list on Foliations and Diffeomorphism groups*, arXiv2503.18274 | v1 March 24, 2025 and **current v2 September 14, 2025**; entire section 2 pp.2–8; GV/Calegari contexts and references | Theorem 2.5 constructs a taut foliation from contact pairs and a volume-preserving transverse field. Questions 2.6–2.9 assume tightness or contact-invariant conditions and ask for foliations. These reverse-direction statements are not the candidate. Other GV questions concern Euler classes or cobordism. |
| Gabai, *Commentary on Foliations*, author PDF with May 2021 file metadata | GV discussion p.4; related atoroidal results pp.6–7; Theorem 0.28 and references | Theorem 0.28 restates tightness near taut foliations, credited to Eliashberg–Thurston and subsequent low-regularity authors. It does not state that the given connection form is tight or announce a solution of 13.2. |
| Dathe–Nkunzimana–Saidou, 2026 publisher article | Actual publisher theorem passages and surrounding text, including Theorems 2–3 | Measured taut/R-covered foliation and fibration results use different assumptions and conclusions; no exact connection-form tightness claim occurs in the checked passages. Whole paper not read. |

[Hurder 2003 source](http://www.foliations.org/surveys/FoliationProblems2003.pdf), [Hurder 2013 version](https://homepages.math.uic.edu/~hurder/papers/78manuscript.pdf), [Nariman–Yazdi current version](https://arxiv.org/pdf/2503.18274v2), [Gabai author PDF](https://web.math.princeton.edu/facultypapers/Gabai/Commentary-Thurston-Foliations.pdf), [Dathe et al. publisher article](https://doi.org/10.1155/jom/8818157).

The later collections were not intended to catalog every Calegari question. None provides authoritative present-day open status for this specific conditional question. Related unanswered Godbillon–Vey questions must not be imported as evidence that 13.2 remains open.

## 4. Existence, nonexistence, and vacuity

No authenticated theorem proving **nonexistence of the full original antecedent** was found in the checked history passages. Conversely, this audit does not supply an example meeting every original hypothesis and the contact-connection equation. The conditional tightness theorem requires neither claim, but a historical interpretation should distinguish them.

The 2007 book's pp.180–182 discuss taut foliations of small Seifert fibered spaces. This is a useful guard against casually replacing “atoroidal” by “hyperbolic” or ignoring geometric conventions; those pages alone do not authenticate all hypotheses of the original question.

Mitsumatsu's eight-page *Ansov Flows and 3D Contact Structures* in the Hayama 2002 archive was read in its extracted substantive text. It discusses Anosov/bicontact constructions, the leafwise Reeb class, and the Godbillon–Vey form. Theorem 3.20 concerns leafwise cohomology for algebraic Anosov foliations. The ending proposed analytic-torsion tightness route explicitly asks for an analytic framework to justify it. It is not a proved exact general result with the candidate's hypotheses. The archive path establishes the source's location, not a independently verified publication date. [Mitsumatsu proceedings source](https://www.ms.u-tokyo.ac.jp/~hirachi/scv/hayama-archive/2002/proceedings/Mitsumatsu.pdf).

That source's reference Mi2 points to *Foliations and contact structures on 3-manifolds* in the Warsaw proceedings and to related minicourse/Japanese material. Those full texts were not read by this family. They are a concrete mechanism-literature follow-up, not a demonstrated earlier answer or reason to infer vacuity. Likewise, an Anosov-derived contact pair is not automatically the specific Godbillon–Vey connection form.

## 5. Search coverage, remaining gaps, and disposition

The evidence contains **52 exact recorded search queries in 19 web batches**, plus 14 successful primary retrievals and six failed retrieval attempts. Search families include exact question numbers with contact/Godbillon–Vey terms, exact title and DOI, “monotone wobble,” author sites and book versions, later problem lists, contact/connection-form terminology, and atoroidal/minimal/nonzero-GV antecedents. Generic results from mirrors, aggregators, booksellers, and social research pages were discovery leads only; none carries a substantive priority conclusion.

The material gaps are:

1. **Final AMS 2003 chapter:** compare the actual published Question 13.2 and nearby remarks against the authenticated 2002 version; check any final-edition answer or reference addition. Bibliographic identity is already established; the gap is full text.
2. **Explicit current status:** no authoritative later author source was found that specifically declares this conditional question open or solved. No status is inferred from an old question or omitted later list.
3. **Theorem/mechanism priority:** the full Eliashberg–Thurston book, the Mi2 materials, and any broader classical corollaries need the distinct family's assessment. A result can be sound yet already follow from earlier work even when no paper cites this question by number.
4. **Complete citation coverage and vacuity:** all citing papers and all possible existence/nonexistence sources were not read. Bounded search absence is not exhaustive novelty or a complete nonexistence theorem.

Recommended parent disposition: **historical priority unresolved, mathematical gate retained**. No historical contradiction or authenticated prior exact answer was found, but this family alone does not support saying “first solution of a previously unsolved open problem.” There is no inherited authorization to waive priority for PR97. Any qualified-research-note exception would need to be separately authorized; this subagent does not request or exercise one.

## 6. Checkable evidence

- `SEARCH_HYPOTHESES.md`: prior hypotheses and stopping criteria.
- `OWN_ANALYSIS.md`: independent substantive conclusion recorded before other fresh-family results.
- `SOURCE_REGISTER.json`: exact paths, SHA256 hashes, actual HTTP results, timestamps, process IDs, extraction hashes, editions, passages read, and unread boundaries.
- `SEARCH_EVENT_INDEX.json` and `WEB_01.json` through `WEB_19.json`: recorded requests and results. Filesystem mtimes are labeled as artifact-capture evidence, not invented HTTP retrieval times.
- `new_primary_sources/*.receipt.json`: actual retrieval receipts; failed attempts preserve errors and status. Non-PDF failure bodies were not silently treated as PDFs. HTTPS certificate failures for the Hurder host were recorded; the public HTTP source was then actually retrieved without disabling certificate validation.
- `calegari2002_page29.png`: rendered, visually inspected question page, from the unchanged shared source PDF.
- `CLOSED_MANIFEST.json`: closed SHA256 manifest covering this folder's files and pinning borrowed read-only inputs separately. Source PDFs remain research cache material, with no redistribution claim.

Final best-guess completion: **100% of this bounded assigned history-family audit**, with historical-priority acceptance still pending the specified evidence and parent adjudication.

