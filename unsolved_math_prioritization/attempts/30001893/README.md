# Convex partition dimensions: audited partial results

Problem 30001893 / OWR-11136-024. Queue status: **unsolved, 5/5 approaches**.
The independent verdict is **PASS_PARTIAL_ONLY**. The full source question is not solved.

For n >= 4 labeled, nonempty, open, convex pieces in R^3, using the standard canonical semialgebraic dimension, the retained global interval is

    4n - 5 <= dim C(R^3,n) <= 3 * binomial(n,2).

The five completed routes provide supporting-plane coordinates for the quadratic upper bound; an exact affine-function gauge/fiber argument for the regular family; pointed central fans of dimension 4n-8 with fixed apex and 4n-5 with moving apex; a cylindrical 4n-5 family including nonregular examples; and an exact five-cell incidence example with rank five and local dimension 15. The audit's weighted polynomial identity strengthens that local example only. No upper bound of 4n-5 for every affine realization stratum is proved.

Canonical coordinates, open valid strata, recoverable geometry, and exact fibers are essential. Raw parameter or equation counts are insufficient. The central-fan theorem requires pointedness; the cylindrical argument requires recoverable lineality and a transverse slice.

## Start here

- [Frozen authored proof](release/PROOF.md)
- [Independent mathematical audit](audit_release/AUDIT.md)
- [Five-route research log](release/RESEARCH_LOG.md)
- [Public source-verification metadata](release/SOURCE_VERIFICATION.json)
- [Present publication status](PUBLICATION_STATUS.json)

The untouched author snapshot predates its independent audit. Its historical `pending` and `remote_publication_performed: false` fields describe the freeze, not the current audit or this proposed publication. The separate audit is bound to all eight original files and the original ZIP. No mathematical correction to the author freeze was required. Audit files also retain their historical no-remote-writes statement.

## Sources and limits

The [2011 OWR report](https://publications.mfo.de/bitstream/handle/mfo/3259/OWR_2011_44.pdf?isAllowed=y&sequence=1), printed p.2539, actually prints 4n-1 for the regular-family count. The inspected [2015 Leon-Ziegler preprint](https://arxiv.org/pdf/1511.02904) gives 4n-5 for the regular family and states the full-space conjecture separately. No official erratum was verified. The 2015 dissertation was also inspected; the 2018 chapter is bibliographically verified only, with its full text uninspected. The live catalog and raw upstream records remain uninspected after access failures. Descriptor-observed hashes were not recomputed from raw records. No novelty, priority, exhaustive literature coverage, or present-day global-openness claim is made.

## Portable replay

Requires only Python 3 and its standard library. From this directory, run:

    python3 -B verify_publication.py
    python3 -O -B verify_publication.py

The wrapper first checks its explicit inventory, both immutable manifests, both exact ZIPs and their member bytes, then runs all six original author/audit commands. It requires exact output-byte matches. Author freeze runs reject 20 negative controls; the independent script rejects 22. Ordinary and optimized runs must agree. These exact computations and corruption checks supplement the analytic proofs; they do not resolve the conjecture.

The original commands remain available in each frozen README. Both ZIPs contain only the same safe authored mathematics, code, audit, results, and public verification metadata as their matching directories. Scholarly PDFs, extracts, images, raw catalog/dataset records, and private coordination are excluded.

This proposal changes only this row's Status and Turns in QUEUE.md, preserving Findings, Chat, DOI, and every other byte, including the pre-existing header. No queue regeneration, merge, release, DOI, or external outreach is part of this publication.
