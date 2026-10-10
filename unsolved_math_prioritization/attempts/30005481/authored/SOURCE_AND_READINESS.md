# Source and readiness record

Problem: 30005481, OWR-12697711-017. Queue rank supplied for this task: 951. Checked 7 October 2026. No repository files or queue cells were changed by this work.

## Exact target

The question asks whether, for every hook-shaped symmetric polynomial hyperbolic in the all-ones direction, diagonal extendability of its associated univariate operator is equivalent to weak sum-of-squares hyperbolicity. The latter condition quantifies over every pair of directions in its hyperbolicity cone. The original target is not merely the SOS property of the all-ones/all-ones Wronskian.

The original primary source is Kevin Shu, joint work with Grigoriy Blekherman and Julia Lindberg, “Symmetrically Hyperbolic Polynomials,” in *New Directions in Real Algebraic Geometry*, Oberwolfach Report 15/2023, printed pp.865–868. Conjecture 3 is on printed p.868 (PDF page index 55). The actual official publisher PDF was downloaded, text-inspected, and that page was visually inspected. Definitions and the quintic example on the preceding pages were also read.

- Report DOI: https://doi.org/10.4171/owr/2023/15
- Official PDF: https://ems.press/content/serial-article-files/47009?nt=1

The fuller source is G. Blekherman, J. Lindberg and K. Shu, “Symmetric Hyperbolic Polynomials.” Its arXiv v1 has the same target as Conjecture 2.3, printed p.4. The published version is *Journal of Pure and Applied Algebra* 229(2) (2025), article 107869. The publisher's full-text Section 2 still explicitly presents this exact assertion as Conjecture 2.3.

- Preprint landing page: https://arxiv.org/abs/2308.09653
- Inspected PDF: https://arxiv.org/pdf/2308.09653
- Published DOI: https://doi.org/10.1016/j.jpaa.2025.107869
- Inspected publisher full-text page: https://www.sciencedirect.com/science/article/am/pii/S0022404925000088

The preprint's Theorem 1.8 gives extendability in degrees at most four, not the full weak-SOS equivalence. Theorem 1.12 and Lemma 4.2 supply the five-variable hyperbolic quintic used here. Section 5.2 gives the inverse-symbol characterization. The computational non-SOS assertion for one quintic Wronskian is reported as a source result; this work has not reconstructed its full-space rational dual certificate.

Kevin Shu's March 2024 dissertation, *Algebraic Methods in Optimization*, was inspected for its alternative presentation of the inverse-symbol and quintic arguments. It is supporting background, not a later resolution:

- https://kevinshu.me/thesis.pdf

## Dated literature check

Targeted searches covered the exact conjecture phrase, the paper title, weak SOS-hyperbolicity with extendability, hook-shaped hyperbolicity, and the authors' current publication listings. No primary theorem resolving this equivalence was located. The 2025 published paper itself retains the conjecture. This is a bounded literature-search conclusion, not a proof of worldwide openness.

Additional current primary context inspected in search-indexed publisher text was H. L. Brian Ng and James Saunderson, “Non-negative polynomials without hyperbolic certificates of non-negativity,” *Advances in Geometry* 26(2) (2026), 197–227, DOI 10.1515/advgeom-2026-0005. Its discussion of general weak-SOS obstructions does not establish the required hook-shaped equivalence. The full publisher PDF download returned no PDF body, so no full-paper proof inspection is claimed.

- https://www.degruyterbrill.com/de/document/doi/10.1515/advgeom-2026-0005/pdf?licenseType=open-access

A later general Schur–Horn inequality paper for symmetric hyperbolic polynomials was also located; its stated theorem concerns a different question, not extension versus SOS. It was not used as a theorem input here.

## Prior-work and semantic-duplicate gate

The complete retained problems and research-results corpora were parsed, with SHA-256 and byte counts independently recomputed. They agree with the supplied recovery evidence:

- problems.json: 68,931,837 bytes; SHA-256 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf
- research_results.json: 80,334,822 bytes; SHA-256 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b

The exact target has no retained research-results entry. Searching all retained entries for hook-shaped, zero-sum hyperbolicity, weak-SOS terminology, the numerical ID, and the source code found no substantive inherited solution to this problem. Loose “extendable” hits were unrelated. The adjacent record 30005480 / OWR-12697711-016 asks two different conjectures: the one-sign-root criterion for zero-sum preservation, and the all-ones Wronskian SOS criterion. It is not interchangeable with this target.

Read-only repository checks covered exact target and neighboring attempt directories (both absent on the default branch), code search for hook/SOS-hyperbolic/target ID, draft and historical PR searches for exact ID, hook, symmetric hyperbolic, zero-sum and SOS-hyperbolic terminology, and branch searches for the exact ID, hook and hyperbolic. No substantive authored semantic duplicate was identified. Searches are not an exhaustive line-by-line read of every repository branch; a whole recursive-tree request failed with a transport error, and that failure is not a negative result.

The source gate therefore permits new mathematical work, while retaining the stated coverage limits. No existing mathematical attempt was reset, overwritten, or silently discarded.

## Sign and notation audit

The exact operator definition p(r-t e), rather than p(r+t e), determines the sign. For the quintic and g_0=(t-1)^4(t+4), direct substitution gives

    T_p(g_0)=-750(t-1)^2(t-2)^2(t+6).

Some source displays suppress or reverse this overall sign. Extendability and the root obstruction are unaffected by a nonzero scalar, but the derivations and checker here retain the definition's sign.

Likewise delta_d is unambiguously t f'-(d-1)f, and g_0 has coefficient (-1)^k(1-k) binomial(n,k) at t^(n-k). We use these identities directly rather than copying sign-damaged extracted formulas.

The authored results concern the usual operator range d<=n. They make no claimed resolution for omitted degenerate conventions or d>n, and the original target remains unresolved without replacing its statement by a narrower one.

## Separation and permissions

The authored directory contains only original explanatory/proof text, public bibliographic/provenance metadata, exact computational certificates, and their checker. Downloaded PDFs, extracted source text, selected corpus records, source-page images, exploratory numerical scripts and coordination material are retained separately and are not part of this deliverable. No source text, corpus contents, copied paper, or private coordination file is cleared for publication by this package.
