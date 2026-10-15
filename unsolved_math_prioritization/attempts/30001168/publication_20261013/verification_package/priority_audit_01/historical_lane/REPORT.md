# Historical and direct-author priority lane: PR 822 / problem 30001168

Audit date: 2026-10-14 UTC. Research scope: original problem history, Morpurgo's directly relevant work, selected later author papers, and forward searches. No external communication occurred. No Git, PR, release, or spreadsheet action occurred in this lane.

## Disposition

**No explicit earlier refutation of the exact maximum-over-time comparison was located in this bounded search. No inspected theorem in this lane immediately supplies that refutation. This is neither a worldwide priority clearance nor a certificate that the problem remained open on the audit date.**

The accepted author construction is a smooth finite capped cylinder in the round conformal class of S3. This lane accepts the separate mathematical audits as its input; it does not re-certify their proof. Historical priority and mathematical ancestry are different questions. Conformal covariance and weighted realizations are already present in Morpurgo's work. The parent audit independently reports that classical long-cylinder geometry, Dirichlet min-max, and an elementary strict round maximum bound assemble into a qualitative refutation. Thus the possible contribution should be described conservatively as the exact-target assembly and its explicit finite quantitative certificate, with priority still bounded by the search.

## Exact target and source history

For the unit round sphere, put Y = Delta + n(n-2)/4 and Y_W = W^(-1/2) Y W^(-1/2), acting with the round L2 measure. The target says that every smooth positive W with integral W^(n/2) equal to the round volume satisfies

    max_(t>0) t^(n/2) Tr exp(-t Y_W)
       <= max_(t>0) t^(n/2) Tr exp(-t Y),     n >= 3.

The whole relevant [OWR pages 421-422](https://ems.press/content/serial-article-files/46205) were text-inspected and visually inspected. Item (16), Conjecture 1, has exactly this scope. Its separate Conjecture 2 concerns monotonicity for n >= 4. The observation that monotonicity fails at small time in n = 3 does not refute Conjecture 1: the round scaled trace also initially rises.

The [AIM problem list](https://aimath.org/WWN/loweigenvalues/loweigenvalues.pdf) is explicitly version 6, April 2009. Pages 1 and 10-11 were inspected completely. Its target matches OWR, with different equation numbering. Its title and introduction combine the May 22-26, 2006 AIM workshop and the February 2009 MFO workshop; they do not establish which meeting first introduced this particular formula. The [2006 workshop report](https://aimath.org/pastworkshops/loweigenvaluesrep.pdf), inspected in full, records Morpurgo's ideas for improving CLR constants on page 2 but gives no exact target formula or resolution. OWR's event span is February 8-14, 2009; Crossref's deposited publication date is December 23, 2009. Those dates describe distinct events.

## Morpurgo's direct trace results

The [Missouri institutional bibliography](https://math.missouri.edu/people/faculty/morpurgo) identifies *Sharp inequalities for functional integrals and traces of conformally invariant operators*, Duke Mathematical Journal 114(3), 477-553 (2002), DOI [10.1215/S0012-7094-02-11433-1](https://doi.org/10.1215/S0012-7094-02-11433-1). Crossref supplies September 15, 2002. An [author-uploaded manuscript](https://www.researchgate.net/publication/38337286_Sharp_inequalities_for_functional_integrals_and_traces_of_conformally_invariant_operators) was inspected at full relevant statements and surrounding definitions: manuscript pages 12-14, 44-48, 61, 69-71, and 73-74. The upload date is June 18, 2019; this is not the research publication date. No manuscript creation/revision date was visible. The official version of record could not be retrieved: Euclid returned challenge HTML. Theorem 4.1/Corollary 4.2 concern zeta functions and transformed traces under convex continuous Psi and integrability hypotheses. Theorem 5.6/5.10 and Corollary 5.12 concern regularized zeta values, including restrictions and reversed signs for s < 1.

The following is the lane's mathematical relevance check, not a new literature claim. The transform is

    L_Psi(1/lambda) = integral_0^infinity exp(-t lambda) Psi(t) dt/t.

Selecting a single heat time would require a point mass at that time, outside the stated continuous convex function class. A maximum over time is a nonlinear operation, not an allowed transform. Therefore neither the fixed-time comparison nor its maximum follows by simply substituting a heat exponential into these theorems. The sharp first-eigenvalue lower bound likewise does not compare full heat traces; multiplicities and the rest of the spectrum matter.

A source-version sign issue remains: [Branson's 2007 primary exposition](https://www.maths.tcd.ie/EMIS/journals/SIGMA/2007/090/sigma07-090.pdf), pages 26-27, describes a nonnegative regularized zeta difference for even n between the first two poles, whereas the inspected author manuscript's Corollary 5.12 states the opposite direction for s > 1. The exposition labels the determinant extension inconclusive and identifies the missing step. No sign reconciliation or identification of the author manuscript with the final Duke text is claimed here. Both discuss zeta/determinant quantities, not this maximum heat-trace statement.

## Earlier work and unavailable primary texts

The 2002 bibliography's actual direct precursor is Morpurgo's [1996 GAFA paper](https://link.springer.com/article/10.1007/BF02246771), volume 6, 146-171, DOI 10.1007/BF02246771. Publisher metadata says received December 15, 1994, revised July 15, 1995, issue January 1996. The publisher abstract concerns logarithmic HLS, even dimensions, and Paneitz-type operators. Full text was unavailable; no theorem-level exclusion is asserted from the abstract.

Morpurgo's [1999 IMRN paper](https://academic.oup.com/imrn/article-abstract/1999/20/1101/657500), *Sharp trace inequalities for intertwining operators on Sn and Rn*, pages 1101-1117, DOI 10.1155/S1073792899000616, was identified in publisher metadata and later primary bibliographies. OUP's exact PDF returned 403. It remains a full-text gap, rather than a paper silently counted as checked.

The official abstract of [*Conformal Perturbation of Heat Kernels and Their Traces*](https://www.sciencedirect.com/science/article/pii/S0022123696901317), JFA 141(2), 319-334, November 1, 1996, DOI 10.1006/jfan.1996.0131, specifies w^(-1) Delta on L2(M,w dx), whose direct conformal interpretation is dimension two. This is not the stated positive Yamabe operator in dimension three. Full text could not be retrieved. *Local Extrema of Traces of Heat Kernels on S2*, JFA 141(2), 335-364, November 1996, DOI 10.1006/jfan.1996.0132, was identified; [its public entry](https://www.researchgate.net/publication/243023223_Local_Extrema_of_Traces_of_Heat_Kernels_on_S_2) explicitly has no full text. The abstract concerns local minima on S2 with fixed area and fixed time. This dimension/function distinction is preliminary screening, not full theorem inspection.

## Later author and forward-citation coverage

Coverage is deliberately counted: the Missouri page has eight selected publication entries, ending with a 2015 preprint; it is not a current complete bibliography. Four distinct recent author works were retrieved and their complete main theorem statements inspected, with one work checked in both arXiv and final journal forms:

| Work and current version inspected | Complete main statements inspected | Relevance boundary |
| --- | --- | --- |
| [Morpurgo-Qin, arXiv 2211.02991v2](https://arxiv.org/abs/2211.02991), first November 5, 2022; v2 December 21, 2023 | Theorem 1, p. 8; Theorem 2, p. 10; kernel assumptions pp. 5-9 | Adams bounds for Riesz-like integral potentials; no Yamabe maximum comparison. |
| [Fontana-Morpurgo-Qin, arXiv 2412.05638v2](https://arxiv.org/abs/2412.05638), first December 7, 2024; v2 October 6, 2025; [JGA version of record](https://link.springer.com/article/10.1007/s12220-026-02364-6), March 31, 2026 | Theorems 1-2, arXiv pp. 2-3 and journal pp. 4-5, with preceding definitions | Complete noncompact manifolds, nonnegative Ricci, Euclidean volume growth; Sobolev exponential bounds. |
| [Morpurgo-Nardulli-Qin, arXiv 2602.06648v1](https://arxiv.org/abs/2602.06648), February 6, 2026 | Theorem 1, p. 1, definitions/context pp. 1-3 | Sharp Sobolev inequality with a geometry-dependent lower-order constant B. |
| [Morpurgo-Qin, arXiv 2602.09677v1](https://arxiv.org/abs/2602.09677), February 10, 2026 | Theorems 1-2, p. 2, definitions/context pp. 1-4 | Sobolev/Moser-Trudinger bounds under Ricci and injectivity assumptions; no sharp round Yamabe trace maximum. |

The complete primary statements for two plausible forward leads were also inspected. [Pascu-Gageonea 0807.4726v2](https://arxiv.org/abs/0807.4726), both versions July 29, 2008, Theorem 3.8 p. 8 and Theorem 4.3 p. 12, settle radial monotonicity of the Neumann heat-kernel diagonal on a disk/ball. This is a different Morpurgo conjecture. [Moller-Orsted 0902.4067v1](https://arxiv.org/abs/0902.4067), February 24, 2009; journal online August 26, 2013, requires full conformal invariance in Assumption 2.2 (p. 3), and proves universal Hessian and determinant statements (Theorems 5.1 p. 12 and 7.3 p. 17). It supplies no missing target inequality. These are full relevant statement inspections, not conclusions drawn from search-result snippets.

Exact-title, exact-DOI, source-URL, author/operator, and resolution/counterexample searches were performed through October 14, 2026 UTC. The query and retrieval ledgers record the bounded scope and failures. Search-result crawl ages were not treated as publication dates. Parent lanes inspect Frank's CLR review and the classical cylinder ancestry; this report does not count those as independently inspected here.

## Remaining gaps and promotion boundary

- Obtain the final 2002 Duke text and compare the manuscript's statements, numbering, and sign conventions; reconcile the Branson exposition only if relevant to a claimed corollary.
- Inspect the unavailable 1999 and 1996 primaries in full before any stronger direct-author clearance.
- A full current author bibliography and exhaustive forward-citation census were not established. Four recent primary works were checked, not every later publication.
- Earlier AIM problem-list versions were not obtained; the precise first appearance of the formula is unresolved.
- No finite search proves absence of a published exact-target corollary. Classical ancestry must be credited even if no earlier paper explicitly refuted this particular conjecture.

The appropriate publishable wording is that the construction refutes the stated 2009 universal comparison, with the classical ingredients credited and without a claim to worldwide firstness or present-day openness. Checkpoint estimate: **80% toward the bounded historical/direct audit objective**, with the above primary-text and completeness gaps preserved.

Artifacts: `SOURCE_LEDGER.json`, `SEARCH_LEDGER.json`, `DECISION.json`, `RESEARCH_LOG.jsonl`, and `downloaded_hashes.json`. Copyrighted primary files and extracted text are stored only in the ignored sibling `private_sources/historical` directory; the public report contains original summaries and bibliographic locators.
