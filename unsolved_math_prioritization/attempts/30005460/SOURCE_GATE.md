# Exact source and prior-work gate

## Source formulation

Bruce Reznick, “The Odd Powers of the Motzkin Polynomial, etc.”, Oberwolfach Report 14/2023, printed pp.778–780, defines `F_(n,m)` as real homogeneous forms of degree m in n variables, and `P_(n,m)` and `Sigma_(n,m)` as nonnegative and sum-of-squares forms. Here m is even and n is positive. On printed p.779 (PDF39), he defines

`Sigma_(n,m)(2k+1)={f in P_(n,m): f^(2k+1) in Sigma_(n,(2k+1)m)}`.

The following question asks whether this set is a closed convex cone. The question concerns the same **fixed** odd exponent on both inputs and their sum. It is not a question about sums of odd powers of arbitrary forms, complex or Hermitian squares, convexity of each form as a function, or arbitrary rational-function denominators. Coefficients and SOS summands are real. For a homogeneous SOS of degree qm, the summands may be taken homogeneous of degree qm/2. Zero is included.

Closedness is already observed in the source: the power map is continuous in the coefficient topology and the target SOS cone is closed. Nonnegative scaling is immediate. Thus convexity is equivalent to closure under addition. The trivial cases q=1, binary forms, quadratic forms and ternary quartics already follow from the classical equality of nonnegative and SOS cones.

Official report: https://ems.press/content/serial-article-files/47007

DOI: https://doi.org/10.4171/owr/2023/14

## Current primary literature

Grigoriy Blekherman, Khazhgali Kozhasov and Bruce Reznick, “On odd powers of nonnegative polynomials that are not sums of squares,” *Forum of Mathematics, Sigma* 14 (2026), e65, published online 27 April 2026, DOI https://doi.org/10.1017/fms.2026.10221. Its author preprint is arXiv:2407.21779v1 (31 July 2024).

The exact known results relevant to the target are:

- Theorem 5.1: if p^q and s are SOS, q odd, then (p+s)^q is SOS. Each fixed-exponent set is therefore stable under adding an ordinary SOS form.
- Theorem 5.3: if p^q and r^t are SOS, with q,t odd, then (p+r)^(q+t−1) is SOS. This proves convexity of the union over odd powers, and settles the separate mixed-exponent conjecture added in the OWR report.
- Section 6 explicitly leaves convexity for a fixed odd exponent open. The closedness statement appears earlier in the same paper.

Neither the union theorem nor exponent monotonicity proves the fixed-exponent target. A bound at exponent 2q−1 is not membership at exponent q. The literature search on 1 October 2026 found no later primary resolution; that is a bounded search result, not a proof of worldwide openness.

## Prior-work gate

The complete pinned problem record was read, including its August 2026 literature assessment, which only checked the original report and retained the convexity gap. The pinned research-results dictionary contains no OWR records and no matching ID or code entry; this absence is recorded rather than replaced with an invented prior report. The individual queue desk note proposes a small SOS-root convexity test but contains no proof certificate.

The recovered campaign inventory lists no prior user/campaign work for this ID. Fresh all-state GitHub PR search for the exact ID, source code and odd-power terminology, branch search, and main attempt-path history returned no match. The related-target groups contain no exact ID match. Source-related questions are not automatically claimed as separate new results. Dedicated work starts from main commit b40fe7dacd5ca480d1de9728492434ac6b827e03.

No substantive author turn is charged for this source gate. Subsequent proof work is recorded as turns 1–5, and an unresolved original target cannot be finalized before five substantive turns. Separate full adversarial review precedes any final PR.
