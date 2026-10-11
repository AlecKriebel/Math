# Acceptance report for the finite temporal unimodality witness

Date: 11 October 2026 UTC.

## Accepted conclusion

For the discrete-time simple symmetric nearest-neighbour random walk in dimension 26, started at the origin, the occupation probability at (17,0,...,0) satisfies p65 > p67 < p69. This is a counterexample to the universal parity-restricted temporal-unimodality conjecture identified as Cooper–Spencer Conjecture 3, database 3100082 / AMR-030-0082.

The finite mathematical argument passes this audit without a mathematical correction.

## Acceptance grounds

1. The original author manuscript's exact target and parity notation were checked in text and rendered pages. The event is occupation at the stated time, not first passage.
2. The counting recurrences are bijective, exhaustive, and exact with coefficient index bounded by 26. The three times are reachable and consecutive in the supported odd parity class.
3. An independently authored histogram enumeration, squared-multinomial recurrence, and time-slot recurrence reproduce every essential count and difference exactly.
4. The probability denominator is 52^n; the correct two-time-step multiplier is 2704. Both signed comparisons are strict and therefore defeat unimodality even with plateaus or monotone limiting cases.
5. Normal, -O, and -OO checker runs pass 810 direct low-dimensional comparisons and all 11 discriminating negative controls in each mode. Counts, normalization, parity, parameter identity, sign, inadequate truncation, and occupation/first-passage confusion are tested. The controls use explicit exceptions and remain active under optimization.
6. The previously published candidate witness is explicitly credited to Anonymous, version 1.0.0-candidate, 19 September 2026. Its PDF was inspected and freshly retrieved; frozen, current-tag, and immutable-commit PDF bytes agree. The annotated tag resolves to commit 95678898ede180f04d6b416e605faa73aed58196. The source remains an unrefereed AI-assisted preprint.

## Limits

This acceptance concerns the finite discrete-time witness and its logical consequence for the universal conjecture. It does not certify minimal dimension, a full mode count, endpoint classification, continuous time, an infinite family, Bessel-function claims, historical priority, unaffiliated endorsement, external journal peer review, or machine formalization. No source-author code was executed. No conclusion about the other Cooper–Spencer conjectures or deterministic-simulation theorem is made.

The standalone proof needs only the recurrences and the three essential integers with their differences. PROOF.md, AUDIT.md, this report, and SOURCE_PINS.json contain the authored mathematical report and public verification metadata. Source PDFs, extracted text, source-author software, checker source, and raw exhaustive tables are not redistributed.
