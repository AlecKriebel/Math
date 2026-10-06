# SIRSN subnetworks cannot be trees

Problem 9700036 / AMR-096-0036, queue rank 936. Disposition: **already_solved**, 0/5 original proof-search approaches.

Under the published SIRSN axioms, almost surely S(1) contains a finite route circuit and cannot be a tree, including when Steiner junctions are allowed. This is an explicit application of David Aldous, *Route lengths in invariant spatial tree networks*, ECP 26 (2021), article 31, Theorem 1.2, [DOI 10.1214/21-ECP401](https://doi.org/10.1214/21-ECP401), with the necessary source-proof clarifications below. The theorem's credit is unchanged; no new obstruction theorem is claimed.

## Read the accepted combination

1. [Clarified application](clarified/RESULT.md).
2. [Source-proof repair](audit/SOURCE_PROOF_REPAIR.md). This is essential, not optional.
3. [First mathematical audit](audit/AUDIT_REPORT.md) and [exact first acceptance](audit/ACCEPTANCE.json).
4. [Second mathematical/source review](second_review/SECOND_REVIEW.md) and [exact second acceptance](second_review/ACCEPTANCE.json).

The first audit's repair and the second review's `SOURCE_PROOF_REPAIR_V1.md` are identical: 12,374 bytes, SHA-256 `5d6598108c9fc3aacc7d127eb16da1af1f2ca3a4654222864036963df6ceddeb`. Both reviews accept the clarified application **together with** that repair. The historical original archive is preserved verbatim in `author/` and `archives/`, but is not accepted alone. The actual [CLARIFICATION.patch](audit/CLARIFICATION.patch) is preserved and must reproduce the five exact clarified files.

## What needed clarification

The source proof contains a balanced-strip definition typo and a color-fraction arithmetic issue. The supplied authored repair states a sufficient obstruction with explicit constants, repairs the red-fraction margin (39/178 rather than the unsupported one-quarter claim), and makes the contour and finite-tree arguments checkable. These changes are disclosed, not silently attributed as the literal printed proof. The application also explicitly treats finite-hull measurability, countable endpoint-accumulating routes, and conditioning on an invariant network event while retaining the Poisson marginal. See the full reports for exact hypotheses and the distinction between a triple-route event and a global tree event.

The original 2012 manuscript labels the question Open Problem 36; its 2014 published version labels it Open Problem 10. The later theorem does not itself name this numbered item as solved. The application is the inference documented here. These files do not resolve distinct problems 9700033 or 9700034.

## Review and verification limits

These are independent AI mathematical reviews, not human peer review, a proof-assistant certificate, or exhaustive priority certification. The executable checks certify byte bindings and finite diagnostics only. Publication preserves the original historical reports, including their time-specific statements about publication and pending review; the present combined status is recorded here and in both acceptance files.

[Verification instructions and results](PUBLICATION_VERIFICATION.md) describe externally anchored replay with all three complete corpora and all four PDF byte pins. Source PDFs, copied source text, corpus contents, exact private corpus records, and private coordination files are excluded. No release, DOI, merger, or external outreach is part of this draft publication.
