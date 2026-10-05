# Rational and integral completely positive factorizations: prior resolution

UnsolvedMath 30003649 / OWR-15957-002, rank 737. Disposition: **already_solved**, one of five substantive approaches used.

Both original primary questions have credited prior resolutions:

- General rational factorability is false. Sidney Holden's public manuscript of 13 September 2026 gives an order-444 counterexample with no nonnegative rational factor of **any finite width**. The complete obstruction proof and exact finite certificate have been independently audited here.
- Unscaled integral factorability in **order two** is true, by Thomas Laffey and Helena Šmigoc (2018). The retained package also includes a complete all-input descent proof. This does not assert unscaled integral factorability in higher orders.

Read [the full independent audit](independent_audit/AUDIT.md), [proofs](authored/PROOFS.md), and [source/scope report](authored/REPORT.md). The rational source remains a public manuscript: journal publication and external human peer review were not verified. This independent nonauthor AI audit is not external human peer review. The separately reported Lean formalization was neither run nor audited here. No novel solution, minimum counterexample order, or classification of smaller orders is claimed.

## Preserved history

The 15-file authored freeze and 24-file independent audit are preserved byte for byte, both expanded and as their original ZIP archives. Pending-audit and no-remote-write statements inside the authored freeze describe its historical preparation state. The completed independent audit and CURRENT_STATUS.json provide the current publication state. The audit required no mathematical revision.

The frozen checker reports input hashes and asks the operator to validate them. The independent checker and the publication replay below enforce the same exact byte-count and SHA-256 pins before source-dependent checks. A sign typo in the 2018 preprint is recorded in the audit; the independent descent does not use the erroneous line.

## Reproduce

Python 3.10 or later, standard library only; run from any working directory:

    python3 /path/to/attempts/30003649/verify_publication.py
    python3 -OO /path/to/attempts/30003649/verify_publication.py

These commands verify strict package inventory, all content hashes, exact ZIP/member agreement, both integral controls, and the author's arithmetic self-test. They explicitly report the source-dependent certificate replay as NOT_RUN.

For the full replay, separately obtain the five public witness files at the immutable URLs in [input_pins.json](independent_audit/input_pins.json), place them together in DATA, and run:

    python3 /path/to/attempts/30003649/verify_publication.py --data /path/to/DATA
    python3 -OO /path/to/attempts/30003649/verify_publication.py --data /path/to/DATA

This adds both certificate verifiers and both source-dependent corruption suites, with stable-result comparisons. Missing inputs are NOT_RUN, never a mathematical pass; a present but mismatched witness is rejected. Recorded result files are comparison outputs, not mathematical proof inputs. Finite computation corroborates the universal written proofs; it does not replace them.

No source datasets, PDFs, extracts, third-party executable code, or private coordination files are distributed. The source pins, public retrieval/inspection metadata, and scholarly titles/URLs identify evidence without redistributing its contents. No CI, peer-review, merge, release, or journal-readiness claim follows from these local checks.
