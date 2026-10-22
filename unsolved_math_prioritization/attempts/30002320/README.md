# Random-graph coloring growth rates: audited partial result

Problem **30002320 / OWR-12481-005**, rank 503. Five substantive approaches completed; the original all-density conjecture remains **unsolved**.

## Essential statement correction

The original Oberwolfach formula is **E[Z_k(G(n,m))^(1/n)]**, with the nth root inside the expectation. The catalog's outside-root expression, **(E Z_k(G(n,m)))^(1/n)**, is different and has the elementary limit k(1−1/k)^(d/2). Proving that formula does not resolve the source conjecture.

- [Proofs, known results, and precise remaining gaps](release/RESULT.md)
- [Five approaches and outcomes](release/RESEARCH_LOG.md)
- [Primary-source audit](release/SOURCE_AUDIT.md)
- [Independent mathematical audit: PASS for partial](audit/AUDIT.md)
- [Independent audit status](audit/AUDIT_STATUS.json)
- [Author freeze](release/AUTHOR_MANIFEST.json) and [publication manifest](PUBLICATION_MANIFEST.json)

The packet proves the standard low-density limit, a strict first-moment zero region, and several model/limit controls. It credits the 2018 all-k condensation theorem and distinguishes it from all-density hard-coloring convergence. No new solution, paper, DOI, or counterexample in the prescribed random-graph ensemble is claimed.

The fresh independent audit found no required repair and verified the frozen author bytes. The retained author status and README are the immutable pre-audit snapshot; the audit records the subsequent PASS. Repository queue disposition: **unsolved, 5/5**, with an audited partial outcome in Findings.

## Reproduction

From this directory, with Python 3 and the standard library:

    python release/checks/check.py
    python audit/controls/audit_controls.py

The first program checks 1,099 small graphs; the independent program uses inclusion-exclusion and a subset zeta transform on 33,867 graphs. Both passed. Finite controls do not prove the asymptotic conjecture. The analytical arguments and their stated ranges are reviewed in the audit.

This is AI-assisted mathematical research with an independent AI audit, not external human peer review. Source PDFs, source screenshots, full extracted texts, catalog data, and private research records are excluded.
