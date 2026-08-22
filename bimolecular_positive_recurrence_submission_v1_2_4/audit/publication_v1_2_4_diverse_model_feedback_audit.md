# Adjudication of diverse-model feedback

**Feedback received and adjudicated:** 22 August 2026

A differently trained generative-AI model reviewed four manuscript artifacts
from an earlier snapshot and returned an accept-with-minor-revisions verdict on
the mathematics. Its section numbering and quoted PDF subject do not match the
current Version 1.2.4 tree, so every suggestion was rechecked against the
current source and, where relevant, primary records. This is an AI-feedback
audit, not independent expert human peer review.

## Mathematical findings

- **Core proof checks:** consistent with the current proof and earlier audits;
  no theorem-breaking defect or counterexample was identified. The reviewer's
  unretained numerical counts are not treated as reproducible release evidence.
- **Nonempty divergent set:** valid exposition point. The compactification now
  states explicitly that leaving every finite set with fixed carried target
  forces $I\ne\varnothing$ and $R_n\to\infty$.
- **Unit-rate attenuation:** the reviewer's underlying coefficient is real,
  but its table is not publication-ready. It did not specify the complexes,
  ordering, divergent ray, parity class, or diameter metric, and its displayed
  “smallest” thresholds are leading asymptotic estimates rather than certified
  exact minima. A three-species table also has at most six distinct quadratic
  complexes and cannot by itself support an asymptotic claim as network size
  grows. The manuscript instead records the fully specified unit-rate family
  $0\to2S_1\to\cdots\to2S_d\to0$, for which exact recursion gives
  $D_0=-(2/d^d)\log N+O_d((\log N)/N)$ on one augmented class and positive
  drift for all nonzero terminals. The text labels this as a limitation of the
  present episode/Foster construction, not a lower bound on the CTMC's true
  return or mixing rate. The original fixed-network, rate-degeneration example
  is retained because it proves a distinct statement.

## Prior art, bibliography, and exposition

- **Anderson--Cappelletti--Kim condition:** the reviewer's wording distinction
  is only partial. Their abstract and introduction use “a multiple of that
  species,” but published Theorem 4.1 literally states the manuscript's
  displayed condition
  \(\{S_i,2S_i\}\cap\mathcal C\ne\varnothing\). The manuscript now notes the
  equivalence under binaryity; the displayed condition remains unchanged.
- **Abstract attribution:** accepted. The non-journal abstract now attributes
  the conjecture directly to Anderson and Kim before stating the proved
  subclass; the corresponding bioRxiv, arXiv, and public-page metadata were
  updated consistently.
- **Stationary corollary:** no change. Its statement already has an immediate
  forward proof pointer, and the end of the recurrence section explicitly
  invokes it and displays the regenerative formula.
- **Xu record:** no change. The official record remains arXiv:2409.05340v2,
  submitted in 2024 and revised 9 May 2026, under the displayed title *On the
  Regulary of Reaction Systems*. It has no journal-reference field, and no
  matching journal article was located. The internal BibTeX key does not
  render; adding editorial “[sic]” would make the bibliography less canonical.
- **Title:** no change. “Single-linkage” is intelligible in the reaction-network
  context; replacing it with the longer “with a single linkage class” would be
  stylistic package-wide churn, not a correction.
- **Conditional JAP source:** no change. The wrappers intentionally select
  venue-appropriate abstracts from one canonical source, and initial Applied
  Probability submission uses the PDF rather than a TeX archive.
- **AI disclosure:** no change to the reader-facing declaration. The rejected-
  approaches sentence is specific and transparent, while the full statement
  supplies the detailed record required for later audit.

## Venue and priority suggestions

- The categorical bioRxiv warning was rejected. bioRxiv expressly permits
  mathematics with direct life-science relevance and lists Systems Biology,
  although its biological-research and new-data screening language creates a
  real discretionary risk. The present abstract, introduction, secondary MSC
  92C42, screening note, and chemical-master-equation framing already make the
  direct relevance explicit. A nominal biological label or simulated histogram
  added only to influence screening would not strengthen the theorem and could
  misrepresent the contribution. The PDF subject is topical metadata and does
  not conflict with primary MSC 60J27.
- arXiv q-bio.MN/math.PR remains the documented fallback. No primary guidance
  supports the reviewer's comparative claim that one endorsement route is
  usually easier.
- A Zenodo DOI remains optional after the exact public tag replay. It cannot
  predate the public 2022 announcement and is not required for bioRxiv.
- The ConStRAINeD page was rechecked. It still describes the two-dimensional
  proof as complete while listing the five-author manuscript as in preparation;
  no public manuscript was located. The dated, incomparable-scope wording is
  retained.

## Result

The retained edits sharpen attribution, close one compactification sentence,
and add a rigorously specified method-specific unit-rate limitation. They do
not change the theorem, its proof mechanism, or its scope. Best-guess
completion is **100% of mathematical and local release-content work**. The
annotated public tag and hosted detached-checkout replay remain the external
release gate.

A final independent read-only pass rederived the unit-rate formulas and found
no mathematical defect. Its polish findings were retained: the family uses the
global species-count symbol $d$ rather than the reaction-channel index $r$;
the abstract attributes the conjecture directly without coining an eponym; and
copy-ready metadata uses rendered en dashes.
