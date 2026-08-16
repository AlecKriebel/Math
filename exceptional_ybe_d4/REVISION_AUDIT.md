# Revision audit for version 1.1.0

> **Historical record.** This file records decisions made for version 1.1.0
> on 27 July 2026. It is not the submission-readiness assessment for version
> 1.1.1; the current declarations and validation record are in `main.tex`,
> `RELEASE_NOTES_v1.1.1.md`, and `VERIFICATION_ENVIRONMENT.md`.

Audit date: **27 July 2026** (America/Los_Angeles).

This file records the disposition of the independent review supplied after
the first public release. The review was treated as a list of proposals, not
as mathematical authority. Each substantive item was checked against the
paper, exact programs, Galindo--Hong--Rowell, and Lechner's version-1
preprint.

## Accepted mathematical revisions

1. **The \(*\)-structure and tower maps are now explicit.** The paper defines
   the conjugate-linear involution \(e_i^*=e_i\), states that each
   \(\rho_n\) is a unital \(*\)-representation, proves
   \[
   \ker\rho_n=\operatorname{Ann}_n,
   \qquad
   \iota_n^{-1}(\operatorname{Ann}_{n+1})=\operatorname{Ann}_n,
   \]
   and displays compatibility of the induced quotient injections. This
   closes the gap between levelwise faithfulness and a localization in the
   tower sense of Galindo--Hong--Rowell.

2. **The dimension-three proof is direct and symmetric.** A hypothetical
   local operator inherits the Hecke polynomial from the localization, and
   two-strand injectivity forces both eigenvalues to occur. The paper now
   prints both three-strand obstructions
   \[
   T=e_1e_2e_1-\tfrac13e_1,\qquad
   T^\perp=e_1^\perp e_2^\perp e_1^\perp-\tfrac13e_1^\perp
   \]
   and proves that each has exceptional trace norm \(1/18\).
   `verify_exact.py` independently checks both norms.

3. **The generalized form is a proposition.** The within-site flip
   \(\Sigma\), the chain unitary \(U_n=\Sigma^{\otimes n}\), the active
   representation, and the spectator-factor conjugacy are all defined.
   This makes the faithful unitary \((3,2)\)-localization statement formal.
   The dependency-free verifier now constructs the sitewise swap matrix and
   checks the \(16\times16\) factorization directly before checking the
   \(32\times32\) generalized equation.

4. **Two consequences are stated with their proper provenance.** The
   \(\mathcal C(\mathfrak{sl}_3,6)\) sequence is not the possible
   counterexample to the localization conjecture contemplated in
   Galindo--Hong--Rowell,
   Remark 6.2(2). Lechner's page-16 observation gives index \(4\) and the
   standard-braided property for the associated Yang--Baxter endomorphism.

5. **Both equation-label defects were fixed.** The review correctly found
   that `eq:cubic-family` was inside an unnumbered display. A separate audit
   found the same defect for `eq:markov`; both displays are now numbered.

## Accepted editorial revisions

- The abstract is shorter and centered on the ordinary localization theorem.
- The first partial traces are identified as unnormalized.
- The paper distinguishes the smallest unresolved member from the remaining
  family as a whole.
- The bibliographic author is Alec Kriebel. Substantial AI assistance remains
  disclosed in the title footnote, final disclosure, structured webpage
  metadata, research log, and source package.
- The related-work section is shorter. The no-contact policy remains in the
  research audit and log rather than the mathematical narrative.
- The PDF contains a version-specific source and release URL.
- The webpage links the original 2012 paper and gives runnable
  dependency-free verification commands.

## Modified or rejected proposals

- **Version:** the first public artifact already existed, so this revision is
  version 1.1.0 rather than a retroactive version 1.0.0.
- **Self-referential metadata:** a PDF cannot contain its own SHA-256 or the
  hash of the commit that contains it; inserting either changes the object.
  The PDF instead contains a predeclared release tag. The later webpage and
  release record identify the artifact commit and PDF hash.
- **Cryptographic signature:** no signing key is configured. The release uses
  an annotated tag and does not claim a cryptographic signature.
- **DOI:** no DOI has been reserved or deposited. No placeholder or invented
  DOI is printed. A future curated archive would require the human author's
  account, metadata, licensing, and publication choices.
- **Authorship responsibility wording:** the review's proposed statement that
  the author assumes responsibility was not inserted. The disclosure instead
  states the actual limitations: substantial AI assistance, lack of
  independent non-AI validation of every argument, and no specialist review.
- **Error-report invitation:** no project-specific contact or outreach request
  was added because the repository's independent-research policy prohibits
  preparing or initiating outside outreach. The existing general repository
  links remain.
- **Expert verification record:** no expert is named because no independent
  specialist review has occurred.

## Scope after revision

The theorem, formula, and priority conclusion are unchanged. Version 1.1.0
strengthens formal completeness, verification coverage, source provenance,
and presentation. Absolute novelty, uniqueness, equivalence to the older
quaternionic tower, and the dimensions \(6,10,14,\ldots\) remain unresolved.
