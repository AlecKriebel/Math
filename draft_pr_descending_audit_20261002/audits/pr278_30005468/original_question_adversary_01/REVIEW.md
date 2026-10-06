# Original-question source adversary: PR 278 / problem 30005468

Verdict: **PASS_LITERAL_OWR_FIXED_P_RATIONAL_SQUARE_SOURCE_SCOPE**.
The frozen candidate covers the actual OWR question under its explicitly stated
rational-square meaning, subject to the mathematical families' independent
verification. It does not cover the stronger strict-margin companion variant.
No source incompatibility requiring a mathematical repair was found.

The inspected input is the original PR head
`deb9d7491a0bf887f7615717a5b484caf212cfd6`; the frozen proof body is pinned in
INPUT_PINS.json. I read PROOF.md, SOURCE_SCOPE.md, and SOURCES.md initially, then
independently extracted the exact imported record and retrieved the primary
sources. I sealed `sealed_independent_checkpoint_01` before reading either
original independent-review file. Subsequent comparison agrees with that sealed
assessment. SOURCE_CONTROLS.json checks those frozen bodies and the seal.

## Actual question and boundary

The whole immutable local cache bodies match revision
`37e53eabe540fb458758e198be61634bd02ee008`. Exactly one target has ID 30005468
and code OWR-12697710-015. Its clean question asks whether a rational fixed
separator can lack every rational SOS membership certificate. It does not ask
that every separator for the same input vector have that defect. Its imported
original_statement is a short source-dependent sentence; the complete question
must therefore be read in the original report.

Fresh publisher [OWR 14/2023](https://ems.press/content/serial-article-files/47007),
printed pp.802-804, supplies all moment indices of total degree at most d,
nonnegative Borel representing measures, compact support context, and
L_y(p)=0 with p in 1+Q(g). Its displayed disk example is
p=1+(8/9)(1-x^2-y^2). Visual inspection and exact arithmetic confirm minimum
one and L_y(p)=0. Strict positivity of p consequently permits p-1 to vanish.
No PSD-input requirement or restriction to a minimum relaxation degree appears.

The [companion arXiv v1](https://arxiv.org/pdf/2302.06927v1) Definition 3, p.9,
requires a positive separator in the Riesz kernel. Corollary 2 separately
constructs minimum strictly greater than one; Remark 2 follows that stronger
construction. Example 5, p.16, nevertheless uses the same minimum-one disk
example. The author-hosted PDF agrees on these statements. The candidate is
compatible with the broad definition and OWR example, but not the stronger
Corollary 2 normalization.

## What rational certificate means

The companion p.4 names the list of SOS multiplier polynomials a certificate.
Its p.9 and [Scheiderer's introduction](https://ems.press/content/serial-article-files/32129)
distinguish squares of real polynomials from squares of rational polynomials.
That context supports the candidate's rational-square definition. The field of
the squared polynomials must remain explicit: it is an interpretation supported
by the cited source context, not a formal Q-module definition printed in OWR.

Under the weaker reading that merely requires rational coefficients in the
multiplier polynomials, the candidate already has sigma_0=f and sigma_1=0.
It would fail that weaker target. This is not a hidden discrepancy: PROOF.md and
SOURCE_SCOPE.md prominently exclude that meaning. A publication or claimed-solved
summary must preserve the rational-square qualifier.

## Candidate assumptions and exact exclusions

The candidate's y_0=1 satisfies the companion Proposition 1's positive-mass
assumption. Its negative fourth moment proves nonrepresentability directly,
without relying on the compressed report's general conic-duality statements.
It violates PSD because the moment-matrix diagonal indexed by x^2 is -1.
That excludes a PSD-input variant; the original question does not impose one.

The candidate's rational ball generator proves rational Archimedeanity
immediately. That stronger assumption is admissible for an existential example.
It cannot support a counterexample to general Archimedean descent.
[Powers Theorem 7](https://msp.org/pjm/2011/251-2/pjm-v251-n2-p08-s.pdf), printed
p.389, provides a rational-square certificate for a strictly positive rational
polynomial with an additional ball term. Here that term is already the sole
generator. Therefore rational strict rescalings cp, c>1, have rational membership
certificates, while p-1=f is outside that theorem's strict-positivity premise.
The fixed boundary normalization is essential.

The other separator q=1+x^4 also has L_y(q)=0 and rational-square membership.
Hence universal irrationality over all separators is false for these data.
All-degree impossibility for the chosen p remains a mathematical proof claim
assigned to the other independent families; this report accepts source scope
only. No algorithm-output, priority, novelty, or comprehensive-history claim is
made. No person was contacted and no source, database, Git, or provider state was
mutated. Private PDFs, extracts, and renders are ignored reading copies.

## Evidence and remaining gap

SOURCE_RECEIPTS.json and SOURCE_SEMANTICS_RECEIPT.json preserve HTTP timestamps,
URLs, response headers, full body hashes, and extraction hashes. All four PDFs
named in the old manifest were retrieved afresh and match its full bytes and
hashes; the independently fetched arXiv v1 is also pinned. The initial seal
records the actual visual inspection of OWR pp.802-804 and companion pp.4,5,8,9,16.
Powers pp.388-390 were visually checked. Exact source controls independently
validate the printed example's normalization and the candidate's moment controls.

Assigned original-source audit: 100% complete (best guess). Exact remaining
gaps are full mathematical proof acceptance by the mathematical families,
historical priority assessment, and any stronger or different target listed
above. Author intent beyond the actual printed context is not certified.
