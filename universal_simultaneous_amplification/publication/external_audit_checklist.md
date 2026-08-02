# External specialist-audit checklist

> **DRAFT — NOT SUBMITTED. NO EXTERNAL AUDIT HAS BEEN REQUESTED OR ARRANGED BY
> THIS WORK.** Under the independent-research policy, only the human user may
> contact a specialist. This file is a scope and acceptance checklist, not an
> invitation, email, reviewer suggestion, or outreach template.

## Current status

- [x] The repository contains internal adversarial/hostile audits of the
      directed theorem, triangle certificate, symmetric K4 certificates, and
      asymptotic continuation.
- [x] Independent exact programs rebuild important chains and certificates.
- [x] `paper/main.tex` explicitly says that the preprint has not undergone
      external specialist peer review.
- [ ] An external human specialist has audited the final frozen manuscript.
- [ ] Any external audit report has been incorporated or answered.

Internal AI-assisted hostile audits are valuable verification artifacts, but
they must not be represented as external specialist peer review.

## A. Freeze the object being audited

- [ ] Human creates a clean commit containing the exact proposed submission.
- [ ] Record commit: **[HUMAN: commit SHA]**.
- [ ] Record manuscript SHA-256: **[HUMAN: hash]**.
- [ ] Record PDF SHA-256: **[HUMAN: hash]**.
- [ ] Record code-release version/DOI: **[HUMAN: identifier]**.
- [ ] Confirm the source and PDF correspond to one another.
- [ ] Confirm subsequent edits trigger a new audit or a documented diff audit.

For orientation only, the released source hashes checked on 2026-08-01 are:

```text
paper/main.tex  b0e066fa5c9db3b255b86ef8bd8f7330d071e2f0876b5e155e9f3b339e14a1f0
paper/n4_certificate.tex  c27538ccc00ae6816020e39599a3a81ea7f81df58f1b0df543c1c14ff9e9d69b
paper/main.pdf  1572d2fd4abd495c4eed61075afdc1dbd74a7d90fb0fe1f379bfa12c50fbf69b
```

These hashes identify the v1.0.0 manuscript files but are not substitutes for
the release tag or an archival DOI. They must be refreshed after any edit.
The corresponding version DOI is `10.5281/zenodo.21753405`.

## B. Model and baseline audit

- [ ] Verify the source-to-target convention for directed weights is used
      consistently in every transition and theorem.
- [ ] Re-derive the complete-graph Bd and dB fixation formulas from the
      one-dimensional count chain.
- [ ] Check looplessness, positive incoming-degree assumptions, initialization,
      and fitness domain in every theorem.
- [ ] Check the (n=2) exception separately.
- [ ] Confirm that target-column scaling leaves dB dynamics unchanged.

## C. Main fixed-graph obstruction

- [ ] Re-derive the complete-directed-support (1/r) coefficient.
- [ ] Check the factor (n^2(n-2)), the comparison direction, and the
      (O(r^{-2})) quantifier for fixed (G).
- [ ] Verify the incoming-column sum-of-squares identity term by term.
- [ ] Verify equality means constant incoming columns and gives the full K-n
      chain, not merely equality of one asymptotic coefficient.
- [ ] Audit the source-component argument for non-strong supports, including
      edge direction and uniform-initialization averaging.
- [ ] Compare the strongly connected noncomplete branch against the exact
      hypotheses of the cited prior theorem.
- [ ] Confirm the three directed support cases are disjoint and exhaustive.

## D. Undirected and finite-size exact results

- [ ] Check the incomplete-support limit
      ((1/n)\sum_i s_i/(s_i+1)) and its explicit deficit.
- [ ] Check the perturbation/leakage argument justifying the infinite-fitness
      limiting chain.
- [ ] Rebuild the six-state weighted-triangle chain without importing the
      expected formula; verify denominator positivity and the homogeneous SOS.
- [ ] Rebuild the 1+3 and 2+2 K4 orbit chains; verify strong lumpability,
      rational comparisons, denominator signs, and equality cases.
- [ ] Confirm unrestricted six-edge weighted K4 suppression remains labeled
      **OPEN**, despite the exact finite search.

## E. Quantifiers and scope

- [ ] Check that the paper resolves
      `exists N0, forall N>=N0, forall r>1` negatively.
- [ ] Check that it does not claim to resolve
      `forall r>1, exists N0(r), forall N>=N0(r)`.
- [ ] Verify the necessary support-degree condition for the open asymptotic
      order and the regimes explicitly left open.
- [ ] Search the manuscript for words such as “universal,” “all fitness,” and
      “asymptotic” and confirm each occurrence has the intended quantifier.

## F. Exact-code and build audit

- [ ] Run from a clean archive with no developer environment inherited.
- [ ] Install the pinned dependency and document the Python and SymPy versions.
- [ ] Run `make paper1` and save the complete output.
- [ ] Run the directed, triangle, K4, and phase-three checks individually.
- [ ] Confirm all transition rows sum exactly to one.
- [ ] Confirm claimed symbolic identities reduce exactly to zero.
- [ ] Confirm numerical or finite-search observations are never used as
      universal proof.
- [ ] Rebuild the PDF and scan for compilation warnings, missing references,
      clipping, and unreadable equations or figures.

## G. Attribution and publication integrity

- [ ] Check all three cited papers against the claims attributed to them.
- [ ] Retain the qualified novelty language justified by the narrow literature
      audit; do not convert it into an exhaustive priority claim.
- [ ] Check title, abstract, author summary, cover letter, and portal text for
      claim consistency.
- [ ] Confirm the data/code archive named in the paper actually exists and is
      immutable.
- [ ] Confirm AI assistance is disclosed and no AI system is listed as an
      author.
- [ ] Confirm competing-interest, funding, preprint, and authorship declarations
      are supplied by the human and agree across all files.

## H. Required audit output

- [ ] State **PASS**, **PASS WITH REQUIRED REVISIONS**, or **FAIL**.
- [ ] Identify the exact source commit and hashes audited.
- [ ] Separate theorem-level errors, reproducibility failures, wording issues,
      and optional suggestions.
- [ ] Give exact file/line references for every required correction.
- [ ] State whether calculations were independently rebuilt or only replayed.
- [ ] List any scope not audited.

## Exit criterion

An external audit is complete only when the human has a written verdict tied
to a frozen source version and has resolved every required correction. If no
external audit occurs, the submission materials must continue to say so
plainly; internal agent audits cannot replace that disclosure.
