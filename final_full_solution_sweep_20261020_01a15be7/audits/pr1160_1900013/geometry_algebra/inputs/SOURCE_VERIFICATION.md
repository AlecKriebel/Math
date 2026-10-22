# Independent primary-source verification

All four complete PDFs were independently fetched from the listed public URLs during this audit. Every byte count and SHA-256 matched the sealed candidate. A fresh pdftotext -layout extraction of every PDF exactly matched the candidate's extracted text. Source text and PDF bodies are not reproduced in this report.

## Historical model

Oleg Karpenkov, *On examples of two-dimensional periodic continued fractions* (2004).

URL: https://arxiv.org/pdf/math/0411054

- Complete PDF: 185536 bytes
- SHA-256: 884c9adaed650a9b40837b5698c00653cd8e81bac5de6932ca3102b2d6da1d13
- Read: PDF pages 3, 4, 15, 16
- Visually inspected: PDF pages 4 and 16
- Verified interface: Definition 1.1, full sail union and lattice equivalence; Definition 1.2, real irreducible unimodular operator; Statement 1.2, separately stated determinant-one commuting criterion; Problem 3, fixed cubic-field question and the historical finiteness remark.
- Use: source scope only. The candidate gives its own geometric argument rather than depending on Statement 1.2.

Oleg Karpenkov, *Open Problems in Geometry of Continued Fractions* (2017), arXiv v1 as returned by the cited URL.

URL: https://arxiv.org/pdf/1712.01450

- Complete PDF: 137819 bytes
- SHA-256: 262e3ebd5e6e8a4966587f5ecfeae3e3f7699c682eab26537b00611ae094028e
- Read for context: PDF pages 3-5 and 7-9
- Visually inspected: PDF page 8
- Verified interface: Problem 13 is the fixed cubic-field classification question; nearby geometric problems and the survey's generalized models require the candidate's historical Klein-only qualification.
- Use: historical restatement and scope. This is not evidence that all current literature has been searched or that the result is novel.

## Unit dependency

Keith Conrad, *Dirichlet's Unit Theorem*.

URL: https://kconrad.math.uconn.edu/blurbs/gradnumthy/unittheorem.pdf

- Complete PDF: 468600 bytes
- SHA-256: db1baeeaa0a535c19c90891deb34f172fa9fd482191bbbd64cfd9e505aa72c97
- Read and visually inspected: PDF page 1
- Verified dependency: Theorem 1.1 is explicitly for arbitrary orders, with rank r1+r2-1. It supplies an infinite-order unit in every totally real cubic multiplier order. Squaring, primitivity in prime degree, and the lattice realization are proved in the candidate, rather than imported from this source.

## Integral-basis and ideal dependencies

Tom Weston, *Algebraic Number Theory*.

URL: https://kconrad.math.uconn.edu/math5230f08/weston.pdf

- Complete PDF: 879873 bytes
- SHA-256: 16933ef3c84f0703ac727b89df612d8ec692a5d772e21682c9eaa859e88729e6
- Read: PDF pages 39, 43-46, 82-83
- Visually inspected: PDF page 83
- Verified dependency map: II.2.22 on page 39 gives a free integral basis of the field degree. II.3.3 on pages 43-44 gives Dedekindness. II.3.6 on pages 45-46 yields ideal invertibility after scalar normalization. IV.2.3 on page 83 gives finite class number, with the preceding norm argument on pages 82-83 providing its context.
- Use: only maximal-order ideal theory. The candidate never assumes the original full lattice is invertible over a nonmaximal order. The finite conductor sandwich is proved directly in the candidate.

## Exclusions and limits

The earlier mistaken arXiv identifier math/0411033 is not a source for any accepted claim. The unsuccessful earlier direct retrieval of a Milne text is not a proof dependency. No new literature-priority search is being claimed by this verification.
