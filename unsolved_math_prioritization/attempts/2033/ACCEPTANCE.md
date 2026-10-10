# Acceptance report: EP-291 / problem 2033

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the explicitly stated partial theorems; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The complete substantive proof and independent mathematical audit are retained. No mathematical correction was required. Historical finite tests and rigorous arithmetic bounds are described, but executable programs, detailed receipts, full computational certificates, raw datasets, and copied source documents are omitted. This edition is not an executable reproduction package. Edition preparation did not rerun mathematical tests or newly inspect scholarly sources.

## Decision and accepted scope

ACCEPTED AS AN UNCONDITIONAL PARTIAL RESULT. The independent mathematical audit required no correction. The full coprimality-infinitude question remains unresolved by this work.

- For q_n = gcd(L_n H_n,L_n), the exact local leading-digit criterion holds only for p <= n and positive exponents. The invertible multiplier L_n/p^e is retained; q_n is always odd.
- Every fixed finite prime set can be avoided on arbitrarily long intervals with endpoint ratio 6/5, or relative length 1/5. The constructive exponent satisfies j <= Q^r for Q >= log(P)/log(6/5), as precisely quantified in Theorem A.
- Every fixed finite-prime survivor set has positive lower natural density. The proof uses recurrence on the actual compact orbit closure and assumes no higher-dimensional reciprocal-logarithm independence.
- The set U avoiding only the universal leading digits p-1 for every odd prime has lower logarithmic density strictly greater than 283/2000 = 0.1415 > 7/50. Pairwise prime-logarithm irrationality, a uniform infinite-prime tail bound, and independently verified finite rational bounds suffice.
- Historical finite rational bounds, direct local-criterion comparisons through 2,000, and complete sieves through 1,000,000 were independently reproduced. They are finite checks, not an infinitude proof.

The distinction n=33 is essential: 33 belongs to U, but q_33=11, because its base-11 leading digit is 3 and H_3=11/6. Non-universal zero digits over a growing prime family remain uncontrolled. Fixed finite-prime density and pairwise independence do not justify an all-prime coprimality conclusion. No novelty, priority, exhaustive literature coverage, world-record computation, or full solution is claimed.

## Verification limitation

The original candidate arithmetic and integrity checkers use Python assert statements, whose checks disappear under -O and -OO. Their optimized runs must not be relied on as verification. The independent auditor used exception-based checks and recorded matching normal/-O/-OO mathematical results and successful rejection controls. These programs and full detailed receipts are not distributed in this prose-only edition.

## Exact edition identities

- PROOF.md: 14,111 bytes; SHA-256 5dcc6e428f500a35004a7dff08e37af1f2239b5b676ec9669ad47b447b38e7c8.
- AUDIT.md: 17,838 bytes; SHA-256 71cd4b79b8af19d95677ecfdf63d2c179691f0a002cfa1fd91c44f2dce1ab4a6.

The original candidate and audit remain unchanged. Editorial differences add review/distribution framing, describe omitted computation and source inspection historically, and remove nonmathematical coordination references. All substantive proof arguments, audit reasoning, accepted qualifications, and unresolved limitations are preserved.
