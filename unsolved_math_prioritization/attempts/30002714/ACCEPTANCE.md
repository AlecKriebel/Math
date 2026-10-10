# Acceptance of a prior negative resolution

Decision: PASS_PRIOR_NEGATIVE_RESOLUTION for problem 30002714 / OWR-13351-013.

The original unrestricted question asks whether the complete integral closure, in the original fraction field, of a total blow-up ring along a centered valuation is always a valuation ring. The answer is negative. AUDIT.md contains the complete elementary proof and substantive independent internal audit of an explicit instance of published Example 7.2.

For any field k, take R = k[x,y,z]_(x,y,z) and K = k(x,y,z). Use the rank-three lexicographic valuation with v(x) = (0,0,1), v(y) = (0,1,0), and v(z) = (1,0,0). Its exact successive local quadratic transforms are R_i = k[x,y/x^i,z/x^i]_(x,y/x^i,z/x^i). They form a strict infinite chain inside K. Their union S is nonarchimedean and has maximal ideal xS.

The accepted calculation is S* = S[1/x] = T = R_(y,z) = k(x)[y,z]_(y,z). Every denominator of T is normalized to x^e times a unit at a sufficiently late stage. The fixed nonzero witness y gives yT contained in S and proves every element of T almost integral over S. Prime exponents in the UFD T prove T completely integrally closed and force S* contained in T. Neither y/z nor z/y belongs to T, so T is not a valuation ring.

Credit remains with Heinzer, Loper, Olberding, Schoutens and Toeniskoetter, Ideal theory of infinite directed unions of local quadratic transforms, Example 7.2 and Theorem 6.9, arXiv:1505.06445v3; Journal of Algebra 474 (2017), 213–239. Shannon's 1973 Example 4.7 is the antecedent explicitly credited there. No new theorem, novelty, or historical-priority claim is made.

The accepted scope excludes a rank-one or archimedean extension, certification of every general theorem or arbitrary-ring example in the source, and acceptance of the separate stronger arXiv:1509.07545 example by proxy. The inspected body is arXiv v3, submitted 1 October 2016, with retrieved-PDF internal typesetting date 28 October 2021. Journal metadata is verified; the journal-final PDF and Shannon's original article were not independently inspected. No arXiv/journal text or byte identity is claimed.

This is acceptance by an independent internal AI mathematical audit of AI-assisted authored mathematics. The reconstruction and audit are unrefereed; no external human peer review or formal proof-assistant certification is claimed. No mathematical correction was required. Finite computational diagnostics and file-integrity checks are supplementary and do not establish universal mathematical steps.

ACCEPTANCE.json preserves the exact mathematical acceptance, exclusions, and original/distributed document identities. Editorial changes add review-status framing, remove private accounting, and clarify source dates. The complete mathematical body and substantive source limitations remain unchanged.
