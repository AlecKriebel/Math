# Public source and inspection ledger

Audit date: 10 October 2026 UTC. This ledger records public citations, source byte identities, inspection history, and limits. Source documents, extracted source text, rendered source images, dataset contents, and private coordination are excluded from the authored public packet.

## Original problem source

- Author and contribution: Pierre Tarrès, joint work with Vlada Limic, *What is the difference between a square and a triangle?*
- Container: *Non-Classical Interacting Random Walks*, Oberwolfach Report 27/2007, contribution beginning p.1553.
- Official report URL: https://ems.press/content/serial-article-files/46113?nt=1
- DOI: https://doi.org/10.4171/owr/2007/27
- Recorded retrieval: 2026-10-10T00:45:45.746125+00:00, HTTP 200.
- Exact retained report PDF: 468475 bytes; SHA-256 `f29794c485fab9b8e11a8618e1f34e6b6929b1eac04a269b703edd47e9c6a13a`.
- This audit: hash recomputed; the full contribution's model, scope, question, and prior-result discussion read; rendered PDF p.33, printed p.1553, viewed again.
- Evidentiary role: confirms edge rather than vertex reinforcement; the reciprocal-summability residual; bounded-degree context; the explicit triangle case; and already-known nondecreasing-weight work.

## Decisive prior manuscript

- Authors: Codina Cotar and Debleena Thacker.
- Title: *Edge- and vertex-reinforced random walks with super-linear reinforcement on infinite graphs*.
- Version: arXiv:1509.00807v3, 2 June 2016. Current arXiv version record read again during this audit; v1 was submitted 2 September 2015.
- Version record: https://arxiv.org/abs/1509.00807v3
- Recorded PDF retrieval URL: https://arxiv.org/pdf/1509.00807
- Prior retrieval: 2026-10-10T00:47:13.822854+00:00, HTTP 200.
- Exact retained PDF: 448416 bytes; SHA-256 `ebde6b71d3618210ada7c79f2f6b0000df8f6b97718113d53cdf8a77dee0b574`.
- Format: 38-page arXiv manuscript. Its first page explicitly identifies v3 and its revision date. A later PDF-generation timestamp is not represented as the mathematical version date.
- This audit: hash recomputed; ERRW definitions on p.2, conditions (6),(8), Theorem 1.1 on p.3, complete edge-reinforcement Section 2 on pp.7–19, and auxiliary summability statements on pp.36–37 read. The theorem pages p.3 and p.9 and formula (36) on p.15 were viewed as rendered pages; the original question page was also viewed.
- Scope of audit: full verification of the finite theorem by count-vector induction and a summability test function; explicit finite-offset repair of the infinite-range estimate; rigorous confinement comparison. This does not certify the entire real-offset generality of the manuscript's infinite theorem or any vertex-reinforcement theorem.
- Material discrepancy: the inspected p.15 estimate (36) omits the increment of the arrival edge in competing reinforcement and loses a zero-index product factor. PROOF_AUDIT.md gives a concrete exact counterexample to that estimate and a scoped repair. This is not a counterexample to the attracting-edge conclusion.

## Publication status and journal access

- Published citation: Cotar–Thacker, Annals of Probability 45(4) (2017), 2655–2706.
- DOI: https://doi.org/10.1214/16-AOP1122
- Institutional publication record: https://discovery.ucl.ac.uk/id/eprint/1482663/
- The UCL record was read through the web tool on 10 October 2026; it identifies the article, journal, year, volume, pages, DOI, and a deposited item described as the published version.
- A DOI open and the UCL PDF-download click returned tool errors. A subsequent UCL page retrieval returned HTTP 403; no further retrieval was attempted from that denied endpoint.
- The public IMS issue URL https://www.imstat.org/publications/aop/aop_45_4/aop_45_4.pdf was also checked. The web tool reported 502; a permitted retry returned an HTML bot-check response instead of a PDF. The response did not supply the journal article. No CAPTCHA was solved or access restriction bypassed.
- Consequently, **no journal proof PDF was obtained or compared**, and no claim of manuscript/journal byte identity or a defect in the uninspected journal proof is made. Published status is supported by institutional bibliographic metadata and the official IMS indexed issue listing.
- A bounded exact-title/author/DOI search for corrections found no relevant correction record. This is not a certification that no correction exists. No additional unrefereed result is needed for the credited conclusion.

## Earlier count-vector method

The manuscript credits Cotar–Limic, *Attraction time for strongly reinforced walks*, Annals of Applied Probability 19(5) (2009), 1972–2007, for the estimate recalled as Proposition 2.1. The citation was checked in the inspected manuscript's bibliography. Its separate full text was not obtained. The necessary estimate is explicitly proved in the authored audit, so no unchecked external lemma is a logical gap in the accepted scoped proof.

## Target identity and audit status

- Exact target: integer problem ID 30000773; source alias OWR-1543-004; queue rank 1226.
- The historical triangle question is covered in the accepted ordinary-initialization scope by the Cotar–Thacker result and the scoped proof audit.
- New proof-search turns: 0. Verification and correction of an estimate in an existing argument are distinguished from a new attempt at an open problem.
- The authored reports are AI-assisted and unrefereed. They do not claim journal peer review, proof-assistant certification, a new solution, or exhaustive historical priority verification.
