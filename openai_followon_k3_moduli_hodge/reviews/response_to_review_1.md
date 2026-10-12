# Response and repaired-package record

First complete reviewer: `reviews/package_review_1.md`, completed
2026-10-07T04:56:53.905646Z. It requested no substantive mathematical repair
but withheld publication acceptance of V1 pending documentary/reproduction
closure and a NEW independent full review. V1 remains recoverable at
checkpoint `1884c97a7b60981f732a21bc65c5d135e920df97` and its exact hashes are
recorded in the review. No claim of human refereeing or formal certification
is made.

## R1 — completed audits reconciled

The dependency ledger, current theorem, approach table and archived validation
summary now identify the finished arithmetic/finite-locus and ordinary-HMS
checks, including their exact scopes and accepted standard inputs. The ZIP
includes the three completed reports and the historical scoped audit notes.
Early reports retain their original pending dependencies; the reconciled
ledger supplies the later status. The ordinary-HMS report checks the actual
primary theorem hypotheses and the additional graph/fullness/generation
arguments. The arithmetic report and separate finite-locus/Hecke report
check the full-tuple mechanism and complementary filtered-projector/scalar
descent. None of their favorable verdicts substitutes for the source proofs.

## R2 — supplemental reproduction completed

The ZIP includes standalone analytic and CM check scripts and expected JSON
results. The runner executes both in its own clean directory and compares
their results in addition to the earlier spin, graph and parity checks.
VALIDATION.md states their restricted scope and explicitly notes that the
placement loop counts `range(k)` only; analytic cyclic weights follow from
the source's normalized-boundary/Stokes argument, not that loop.

An ARCHIVE_MAP.json now maps archive names to the research-project locators
in the reports/ledger; the README explains that upstream paths refer to
the linked fixed-commit snapshot, which is not redistributed. This closes
a portability issue found during assembly. The original theorem, main.tex,
PDF and intended Zenodo metadata are unchanged by these repairs.

## Gate

The regenerated exact V2 artifact manifest and source hashes identify the
package for a new reviewer. Publication is withheld until that reviewer
checks the entire current package independently and finds no substantive
issue, with no known substantive concern remaining. Any material change
after that review requires renewed review.
