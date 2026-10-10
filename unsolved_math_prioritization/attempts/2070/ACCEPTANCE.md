# Acceptance report: EP-354 / problem 2070

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the variable-base counterexample, with no external human peer review, journal acceptance, or formal proof-assistant certification claimed. The complete substantive mathematical proof and audit are retained. No mathematical correction was required. The fixed-base-2 irrational-ratio question remains unresolved by this work. The exact quartic family and positive-multiplier mechanism are prior work of Dubickas (2006); no novelty of the application is claimed. Executable programs, raw datasets, detailed execution receipts, full computational certificates, and copied source documents are omitted. This is not an executable reproduction package. Edition preparation performed byte-integrity and publication-structure checks, with no new mathematical test execution or scholarly-source retrieval or inspection.

## Decision and exact scope

ACCEPTED: the universal variable-base extension is false. No mathematical correction was required. The original fixed-base-2 irrational-ratio question remains unresolved by this work, so the combined problem is not declared solved.

Let P(X)=X^4-X^3-X^2-X-1 and let gamma be its unique positive root. Define c=1/((gamma-1)P'(gamma)), alpha=2c gamma^20, and beta=gamma alpha. Then 1.92<gamma<1.93, c>0, alpha,beta>0, and alpha/beta=1/gamma is irrational. Every indexed term floor(alpha gamma^n) and floor(beta gamma^n), for n>=0, is even. Every positive odd integer is therefore absent from finite sums of distinct positions, including when coincident values occupy different positions.

The all-future proof uses the exact recurrence with constant residue 1/3, bounds all three nonleading roots by 5/6 and their coefficients by 1, and proves |E_m|<3(5/6)^m<1/6 for every m>=20. Strict floor endpoints cover both exponent-zero terms. The shift is justified rather than inferred from sampling; the unshifted m=3 floor is odd.

The independent audit confirmed the original quantifiers, indexed multiplicity, rational endpoint calculations, trace sign and recurrence, all-future bound, floor endpoints, and attribution. Historically recorded independent exact arithmetic passed 1,573 checks, including 1,024 trace values and 512 consecutive floor values, with byte-identical normal/-O/-OO results and exception-based failure controls. Finite tests supplement the written infinite-range proof.

## Attribution and limits

[Dubickas, On the limit points of the fractional parts of powers of Pisot numbers (2006)](https://dml.cz/handle/10338.dmlcz/107991), Theorem 4 and its proof, supplies the positive multiplier and fractional-part mechanism. [Dubickas, Even and odd integral parts of powers of a real number (2006)](https://doi.org/10.1017/S0017089506003090), Theorem 1(iv), supplies the all-even mechanism, and printed page 332 explicitly contains the exact quartic in the multinacci family at d=5. This edition credits that prior work. No novelty or priority of the application to EP-354 is claimed.

The result is one counterexample in (1,2), not a classification of all bases. At gamma=2 the analogous beta=gamma alpha choice has rational ratio and is inadmissible; that fixed-base exclusion does not exclude the present irrational-base example. The reported individual base-2 pair (10 sqrt(2),10 sqrt(3)) is not used or independently re-certified here.

## Exact edition identities

- PROOF.md: 9,813 bytes; SHA-256 d1763e7b4b40f59f69c00f18e75f283a0692db29fb9835f1af66ab5197554207.
- AUDIT.md: 12,889 bytes; SHA-256 d92bf24c643a88a57984c4ffa93f57dac06aba0120e5235a41a1a61b17fea917.

The original candidate and audit are unchanged. Tracked editorial changes clarify review and distribution status and describe omitted verification historically. All substantive mathematics and original acceptance qualifications are preserved.
