# Literal earlier positive-chain formula and chronology check

Recorded 2026-10-15 after independent root primary retrieval and reading.
This supplements, rather than silently revises, the provisional coverage
reconstruction. Five distinct priority/equivalence reviews are still pending.

Mihai Nica, *Decorated Young Tableaux and the Poissonized Robinson-Schensted
Process*, arXiv1404.4015, contains the complete positive finite-dimensional
shape weight in Theorem 3.2. In v4, Remark 3.3 expresses it as a product of
exponentially specialized skew Schur functions; in v1 the theorem already
states that Schur product and Remark 3.3 supplies the skew-tableau identity.
Root read the relevant definitions, theorem/remark and counting proof and
visually inspected v4 PDF pages 5–6, including the actual printed formula.

For a query with maximal threshold X, put theta=sqrt(X) and map the Poisson
rectangle `[0,X]x[0,1]` to the square `[0,theta]^2` by
`(u,v)->(u/theta,theta*v)`. Its Jacobian is one and coordinate order is
preserved. The nested x-threshold rectangles correspond to the right tableau's
restriction at `theta-s=x/theta`. Thus its positive times
`s=theta-x/theta` reverse the increasing query thresholds. The final query
threshold X corresponds to central time zero. The earlier theorem with no
sampled negative times gives exactly the joint shape weight

`exp(-theta^2) D_theta(lambda^m) product_j D_(Delta_j/theta)(lambda^j/lambda^(j-1))`.

Each skew determinant is homogeneous of degree the skew size. The terminal
factor contributes `theta^n`, the increment factors `theta^(-sum d_j)`,
and `sum d_j=n`. They cancel exactly, yielding the candidate's
`exp(-X) D_1(lambda^m) product_j D_Delta_j(lambda^j/lambda^(j-1))`.
Summing the shapes subject to each first-row constraint gives the full
candidate event, not only a one-point marginal. This is an explicit exact
specialization of the earlier stated theorem. The stationary identification
is separately tied to the earlier Gamma(B) representation and RSK rank law;
this note does not pretend that Nica names the later drift-jump question.

The current v4 PDF's title date is September 15, 2021, although its arXiv
version strip and primary version page give March 29, 2017, and the journal
reference is February 2017. Root did not silently use that displayed date as
proof of earlier content. Directly retrieved version URLs v1
(canonical April 15, 2014) and v3 (canonical April 29, 2015) already contain the same full shape
weight, relevant specialization and proof. Their separate bytes are pinned in
`NICA_EARLIER_VERSION_RETRIEVAL.json`; no unexplained title-date inference is
needed for the canonical-version content claim. Their PDF title dates also
show later dates (December 3, 2024 and May 15, 2022). Root independently
retrieved the v3 source archive and checked the actual theorem and remark in
the source. The article source has no explicit date command, so its default
title date changes on recompilation. Its TeX member has archive timestamp
April 29, 2015 and SHA256
`1805f98c486da8a3454c4bcde8607f0d0ddaa52063dca146a633f8832db51f90`.
`NICA_SOURCE_ARCHIVE_RETRIEVAL.json` pins the entire separate archive and its
member identities. The canonical version history and source content support
the pre-2018 formula; the title dates are not used as content chronology.
The mechanism is also independently supported by the 2004 ascending-process
transition theorem.

The v4 Theorem 3.2 right-product exponent prints a lambda where the surrounding
mu sequence is required. Root visually confirmed the typo, which can refer to
an undefined lambda for some list lengths. The denominator, Remark 3.3,
the full counting proof and the v1 theorem supply the consistent mu/mu
formula. The coverage argument uses those correct identities with an
independent derivation; it does not quote the erroneous display as written.

This strengthens complete automatic prior coverage substantially. It still
does not establish that anyone previously announced an answer to the exact
February 2018 page, that the proposer endorsed a particular explicitness
standard, or that no useful exposition or software contribution is possible.
