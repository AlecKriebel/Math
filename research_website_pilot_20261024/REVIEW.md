# First-paper review decision

Date: 24 October 2026. Mathematical review completion: 100% of the defined
pilot review. Website deployment is recorded separately in RESEARCH_LOG.md.

**PASS for the stated result. No substantive mathematical error or required
correction was found in the published preprint.** This is internal AI-assisted
review and exact computational verification, not independent human refereeing
or proof-assistant certification.

Paper: *Free spanning-forest degree can decrease under squaring*, Alec Kriebel,
version 1.0.0, published 22 October 2026,
[DOI 10.5281/zenodo.23575190](https://doi.org/10.5281/zenodo.23575190).

## Strongest verified claim

The degree-8 binary grandparent graph G is infinite, connected, locally finite,
simple, vertex-transitive, and nonunimodular. Its expected free uniform spanning
forest root degree is exactly (24−√2)/7, exceeding 3.22. Its simple square has
degree 40 and expected FUSF root degree at most 3.208526010913748780, below 3.21.
The square value is an upper bound. The conventional normalized b_F gap is
strictly greater than 1/200. No negative claim about the unimodular/Cayley
subclasses or an unspecified nonunimodular L² invariant is made.

## Evidence and independent review families

- Source identity: fresh Zenodo download sizes and MD5 checks pass; PDF SHA-256
  dc0126e8f3da1baf7743b462ac3e6962f5969b5fec4d7451e225a19d9762ef08.
  The PDF and its source were reconciled; all seven PDF pages were inspected.
- Analytic: both finite free exhaustions, local recurrences, cofinality,
  uniform convergence, edge probabilities/counts and full-group symmetry
  were reconstructed. Exact elimination checks and an additional independent
  adversary found no missing boundary condition or unsupported limit.
- Computational: a distinct word-tree implementation checked 3,070 vertices,
  19,931 edges, all 40 root neighbors, 797,240 integer currents and 122,800
  divergence equations. The exact total energy agrees with the paper.
  All 161 adversarial checker outcomes matched expectations. Deposited
  verifier replay also passes with optimization enabled.
- Scope: the actual Abért source is unrestricted; the paper's explicit b_F
  convention is retained. Established grandparent graphs, electrical facts,
  free/wired distinctions and Cayley context are credited. Additional book
  and lecture-note passages were checked. No exhaustive firstness claim is
  warranted by the bounded search.

Detailed evidence is in reviews/analytic/ANALYTIC_REVIEW.md,
reviews/certificate/REPORT.md, and reviews/scope/SCOPE_ATTRIBUTION_REVIEW.md.
The exact computations and review receipts accompany those reports. Their
mechanisms, scope and remaining limits are recorded separately rather than
treated as confidence votes. External reference PDF/text bodies are local-only.

## Remaining gaps and qualifications

No central proof or certificate gap remains in this review. Historical
firstness, all unindexed literature, some final journal editions, and human
peer review remain unestablished. The finite code checks do not replace the
written infinite-limit arguments. Noncritical direct-API parser leniencies
are documented; they do not affect the genuine file pinned by SHA-256.

## Website gate

The public explanation must preserve the upper-bound sign, nonunimodular
scope, version dates, AI disclosure and unrefereed status. The public PDF/ZIP
are byte-identical to Zenodo. Website source lives in the user's existing
personal-site repository. The first preview was redesigned on the user's
instruction to closely follow the plain blog template. No GitHub Pages
redirect is authorized until the user approves the pilot, and no old page
for this particular paper was found. No individual was contacted.
