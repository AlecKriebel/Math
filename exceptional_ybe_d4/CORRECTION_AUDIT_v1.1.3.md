# Correction audit for version 1.1.3

Audit date: **16 August 2026** (America/Los_Angeles).

A further model review was treated as a set of proposals rather than as
evidence. Each proposed correction was checked against the immutable Lechner
v1 PDF, the published Rowell--Wang and Galindo--Hong--Rowell articles, current
official OpenAI documentation, the manuscript, and the exact verification
package. No mathematical error or scope-changing issue was found.

## 1. Lechner equation number

**The review's factual premise was rejected; its wording improvement was
accepted.** In the immutable arXiv:2603.20158v1 PDF, the projection-form Hecke
relation is Equation (3.1) on page 11. Equation (3.2) is Wenzl's Markov
parameter in Theorem 3.3. The manuscript's old number was therefore correct.

Nevertheless, the proof already displays the relation it uses. Version 1.1.3
now says to multiply “the displayed projection-form Hecke relation” by
\(e_2\), removing an unnecessary external equation-number dependency.

Primary source:

- <https://arxiv.org/pdf/2603.20158v1>

## 2. Localization-conjecture credit

**Accepted and propagated, with version-sensitive locators corrected.**
Rowell and Wang introduced the localization framework. Their arXiv v2 states
the relevant assertion as Conjecture 4.1, but the final published article
renumbers it as Conjecture 3.1 on page 601. Because the manuscript cites the
published article, it uses the published locator. The published GHR article
explicitly calls this the main conjecture of Rowell--Wang and restates it as
GHR Conjecture 1.5. The abstract, introduction, corollary, related-work
section, README, project page, and priority audit now credit the Rowell--Wang
localization conjecture.

The numbering is version-sensitive: the early GHR arXiv version numbers this
restatement as Conjecture 1.4, while the published article cited in the
manuscript numbers it Conjecture 1.5. The latter is the applicable locator.

Primary sources:

- Rowell--Wang, published Conjecture 3.1 (p. 601), author-hosted journal PDF:
  <https://web.math.ucsb.edu/~zhenghwa/data/research/pub/Localization-12.pdf>
- Rowell--Wang, arXiv-v2 Conjecture 4.1:
  <https://arxiv.org/abs/1009.0241v2>
- Published GHR, Conjecture 1.5:
  <https://doi.org/10.1093/imrn/rnr269>

The checked journal PDFs have SHA-256 values
`4049ea09174d55596278dc7694b0955f887a07b94cb34f88d7f170e97516adef`
(Rowell--Wang) and
`ce68f021303048dffb4badd498291865e56c860a309901d6463a18b5d938cdf7`
(GHR).

## 3. OpenAI product terminology

**The proposed separate “GPT-5.6 Sol Pro” model name was rejected.** Current
official OpenAI guidance identifies GPT-5.6 Sol as the selected model, describes
Pro as a mode, and expressly says not to switch to a separate Pro model slug.
The same guidance calls Ultra a Codex mode. Version 1.1.3 therefore retains
the single model name and uses parallel wording: GPT-5.6 Sol in Pro mode
through ChatGPT and GPT-5.6 Sol in Ultra mode through Codex. Anthropic remains
identified generically because the available record does not independently
establish a more precise model label.

Official sources checked on 16 August 2026:

- <https://developers.openai.com/api/docs/guides/latest-model>
- <https://developers.openai.com/api/docs/models/gpt-5.6-sol>

## 4. Optional presentation proposals

**Accepted.** The two Lechner page citations now also identify the discussion
following Proposition 3.6. The dense GHR normalization footnote is promoted to
a visible remark, with the \(\eta\)-formula correctly located in the proof of
GHR Theorem 5.28. A final editorial audit also added Lechner's arXiv-issued
DOI, `10.48550/arXiv.2603.20158`, to the bibliography while retaining the
immutable version-1 URL used for the theorem and page locators.

## 5. Final editorial and archival freeze

**Accepted and completed.** A final review found three small presentation
issues but no mathematical defect. The abstract now has an unambiguous
antecedent, the public sole-author block omits the redundant “Corresponding
author” label and unnecessary location, and the GHR convention remark follows
rather than interrupts the proof of Proposition 5.1.

The human author supplied the fresh manual Zenodo draft's reserved version DOI,
`10.5281/zenodo.21971507`. The DOI was inserted in every current manuscript,
citation, metadata, and project-page surface, after which the PDF, manifests,
verifiers, and deterministic archives were rebuilt and rechecked. The draft
remains unpublished. The separate journal-only full postal address and portal
phone gate also remains. No Zenodo publication, arXiv submission, journal
submission, GitHub release, or outside contact occurred in this freeze.

## Conclusion

The operator, theorem, proof scope, exact verifier results, and qualified
priority claim are unchanged. Version 1.1.3 corrects attribution, removes a
fragile external locator, improves convention visibility, clarifies product
terminology, and supplies a single DOI-bearing deterministic submission
package.
