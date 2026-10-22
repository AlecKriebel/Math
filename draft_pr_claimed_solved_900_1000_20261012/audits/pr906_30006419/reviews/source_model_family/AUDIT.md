# PR906 independent source/model assessment

Audit of problem 30006419 / OWR-14299521-012, frozen candidate head
`32eaecaa8907dbf674e65b138b000cdcc49004ae`. This family read the author
artifacts and primary sources before any historical review. No historical review
was subsequently needed. This is source triage and validation, not another proof
attempt; the original 2/5 count is preserved.

**Disposition: the original-source model binding passes. Final-publisher
mathematical scope remains unverified after substantive fresh retrieval work.**
This finding does not certify either authored analytic proof or historical
priority.

## Original-source normalization

The private upstream statement matches SHA256
`f39339834d52efed151d9dd4aa4e36f9e8a4319228308fd21e4b277784a604a0`.
Its antecedent agrees with OWR Question 1, printed p. 1625. OWR fixes an energy
before asking about local harmonic spheres. The omitted energy parameter must
therefore remain explicit in the assessment. [Official OWR report](https://ems.press/content/serial-article-files/52249).

The following clauses were independently checked in the full [arXiv v1
PDF](https://arxiv.org/pdf/2503.08553v1), not inferred from the candidate:

| Locator, printed page | Verified clause |
| --- | --- |
| Section 1.2, pp. 2-3; Question 1.9, p. 4 | Fixed general energy; compact quasiconvex target, local quadratic isoperimetry, and null-homotopy of all continuous spheres with sufficiently small image diameter. |
| Definitions 2.1-2.3, pp. 7-8 | Complete-target Sobolev theory with measurable, essentially separably valued maps; approximate metric differentials; quasiconformality compares stretches in equal-length directions almost everywhere. |
| Definition 3.1, p. 9; quasiconvexity paragraph, p. 11 | Continuous, monotone, degree-two homogeneous, rotation-invariant, proper energy; quasiconvexity also required. Both Reshetnyak and KS are included. |
| Definition 6.1, p. 15 | For each point choose one open neighborhood, then every relatively compact Lipschitz subdomain and all same-trace Sobolev competitors. |
| Theorem 3.2 and Corollary 3.3, p. 10 | Global comparison under every biLipschitz sphere reparametrization, or continuous homotopy-class minimization, is stronger than the local premise. |

## Candidate-to-model checks

The negative theorem chooses one permitted fixed energy, Reshetnyak. Consequently,
if its proof passes the independent proof family, it falsifies the blanket
affirmative claim across the general-energy framework. It does not establish a
negative answer for each permitted energy separately. A KS-only reading would be
a distinct claim, and the candidate explicitly distinguishes it.

The constructed target and map are stronger than necessary: a compact smooth
Riemannian sphere and a smooth homeomorphism. The stated geodesic property gives
quasiconvexity with constant one. The uniform contractible-ball argument addresses
all continuous small-image spheres; it imposes no regularity on those test
spheres. The cone argument is directed at short Lipschitz loops with their
prescribed trace. None of the antecedent requirements is silently weakened to a
special subclass of competitors.

The local comparison arguments are written with the full competitor quantifier.
The first uses a global real Lipschitz extension to handle maps leaving the flat
patch. The second uses a global primitive and same-trace gluing; its cutoff
controls the calibration, rather than constraining competitor images. The
compact support used in its integration by parts is the support of the glued
form difference inside the source neighborhood. Whether all analytic identities
are valid is delegated to proof review; there is no source-level permission to
discard competitors of inconvenient topology, image, or energy.

No existence/attainment theorem for an auxiliary minimizer is substituted for
minimality of the displayed map. The candidate claims a pointwise lower bound for
every competitor and equality for its own map. Its explicit comparison with a
conformal degree-one map also acknowledges failure of global homotopy minimality.
It need not satisfy a global reparametrization comparison merely because it is
locally minimizing in the source sense.

Energy normalization is internally consistent: in a smooth target the two
densities used are `max(sigma_1,sigma_2)^2` and
`sigma_1^2 + sigma_2^2`. The symbol `E_+` in the candidate abbreviates the
quadratic energy, not the square root of that integral. Domain conformal factors
cancel in dimension two. The distortion constant is a stretch ratio, not its
square. The claimed failure is on positive-area bands for every finite constant;
the equator's measure-zero rank defect is not the sole evidence. Comparability
of the two energies does not equate their minimizers.

The KS companion explicitly fixes the angular-average energy and uses the same
locality quantifier. Its complete-target statement is compatible with the
standard Sobolev framework just inspected. Essential separable valuedness is
already part of `W^{1,2}`. Smooth source coordinate changes preserve the scalar
distance-function Sobolev tests; approximate metric differentials transform by
their derivatives because such changes preserve density-zero exceptional sets.
Thus its sentence about the required differential and chain rule does not, in
this framework, add an unverified geometric regularity hypothesis on `X`.
This is a framework check, not a certification of the stress calculation or its
numerical constant.

## Fresh current-version effort and exact remaining gap

The current unversioned arXiv PDF is byte-identical to v1, with SHA256
`23c2b27bf9a39649cea4dc820815c73cb983224488f66de2ccdfe0fc9254dc28`.
The abstract record lists only v1. The HTML header's August 24, 2026 date does not
establish a new mathematical version: the versioned source archive contains
literal `\date{\today}` in `main.tex`, line 26. A later rendering is an inference
consistent with this artifact, not a claim about the arXiv renderer's operation.

The author bibliography still lists volume 838 (2026), pp. 137-169 and DOI
10.1515/crelle-2026-0042. [Author publication record](https://people.math.ethz.ch/~damameier/research.html).
Fresh DOI, publisher HTML, PDF, XML, old-host PDF and German-path PDF requests
returned HTTP 202 with zero-byte bodies. The XML/PDF endpoints are additionally
identified by the DOI's Crossref metadata. A browser then successfully loaded
the actual [publisher landing page](https://www.degruyterbrill.com/document/doi/10.1515/crelle-2026-0042/html):
it displays authentication restrictions, with abstract, acknowledgments and
references accessible, and the mathematical body unavailable. Its dates are
received 2025-06-27, revised 2026-04-07, online 2026-06-06 and print 2026-09-01.
No purchase, login, outreach, or access-control bypass was attempted.

A fresh primary [ETH institutional record](https://www.research-collection.ethz.ch/items/30efd2c4-15c5-487b-a504-bb66d5162fad)
also loaded in the browser. It confirms the journal volume and pages but
explicitly marks the record metadata-only, with no full-text file.

The exact unresolved comparison is whether the revised/final mathematical body
retains Question 1.9, the general-energy convention, Definitions 2.3/3.1/6.1,
and their quantifiers unchanged. None of those final-version clauses was
inspected. The observed revision date makes byte-equivalence with the preprint
unsafe to assume. Keep the original OWR/v1 qualification and do not relabel this
as a verified resolution of the current publisher formulation. This limit does
not erase the original-source binding already checked.

Complete primary PDFs, HTML, source archive, extracted text, rendered pages and
retrieval records are retained only in ignored `private_sources/`. Public
artifacts expose metadata, hashes, locators and this checkable assessment.
