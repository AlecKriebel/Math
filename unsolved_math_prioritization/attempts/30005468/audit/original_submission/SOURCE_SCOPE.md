# Exact source and scope assessment

Checked 2026-10-01. Proposed disposition is a complete candidate for the literal
fixed-polynomial existence question, pending independent review. One substantive
author turn is used. No historical novelty claim is made.

## Original report

Simone Naldi, joint with Didier Henrion and Mohab Safey El Din, “On Algebraic
Certificates for the Truncated Moment Problem,” OWR 14/2023, printed pp.802–804,
DOI 10.4171/OWR/2023/14. Full publisher PDF was read, and pp.803–804 were
visually checked. The moment indices comprise every monomial of total degree
at most d. Measures are nonnegative Borel measures supported in a basic closed
semialgebraic K in real affine n-space. The report initially allows real
generators; our example satisfies the stronger rational-generator condition.

The report discusses compact K. Its certificates p have degree <=d,
are strictly positive on K, satisfy L_y(p)=0, and belong to 1+Q(g). The final
question asks whether a rational such p can require irrational SOS data in
every certificate of this fixed membership. It does not require every separator
for y to have that defect. The printed unit-ball example on p.803 is
p=1+(8/9)(1-x^2-y^2), whose minimum on the ball is exactly one. Hence
strict positivity of p is not a printed condition min p>1.

The report omits several hypotheses in its compressed general discussion.
We explicitly take y_0=1>0, a nonempty compact ball and a rational Archimedean
module. We do not rely on the report's unqualified conic-duality statements.
The constructed y is not positive semidefinite as a truncated moment matrix;
no such restriction is printed. Requiring it would be an additional problem.

## Companion preprint, stronger construction

Henrion–Naldi–Safey El Din, arXiv:2302.06927v1, 2023, full author PDF from
Henrion's publication page. Section 2.1 defines Q(g)[D] by bounding each
summand's degree, in distinction from Q(g) intersected with low-degree
polynomials. Our impossibility quantifies over all D, so it is not a failure
only at a small SDP relaxation.

Definition 3, p.9, defines a separator by strict positivity and L_y(p)=0.
Corollary 2 additionally constructs min_K p>1, arbitrarily large, under
Archimedeanity and y_0>0. Remark 2 discusses rational p and potential
irrationality of its SOS data. Our example meets Definition 3 and the OWR
question, but does not meet the extra strict-margin conclusion of Corollary 2.
That distinction is explicit rather than silently repaired. On a rational ball,
Powers's theorem rules out the stronger strict-margin version for a fixed p.
A review should judge whether the intended OWR question adds that unprinted
restriction; if so, this packet is a scoped result rather than a full answer.

## Primary inputs and current status

- Scheiderer, JEMS 18 (2016), pp.1495–1513, Theorem 2.1 / Example 2.8:
  explicit rational real-SOS but non-rational-SOS ternary quartic. Full
  publisher PDF read. The construction and its Galois obstruction are credited
  and reproduced in the proof; this is not a newly discovered quartic.
- Powers, Pacific J. Math. 251 (2011), pp.385–391, Theorem 7:
  rational strictly positive polynomials admit rational Putinar certificates
  when a rational ball generator is available. The displayed theorem includes
  the ball term separately. We use it only for the unit-ball presentation,
  where that term is already one of the original generators.
- Powers's Remark 8 asks whether real Archimedeanity descends to Q. A 2026
  IIT Bombay primary talk abstract reports a partial zero-dimensional result;
  it is not used as a theorem in this packet. Keshari–Ojha–Patra's 2025
  arXiv abstract and September 2026 publisher metadata concern natural
  univariate generators and likewise do not settle the displayed multivariate
  fixed-p example. No claim of comprehensive negative literature search.
- The original authors' current publication listings still list the moment
  manuscript as a preprint, and arXiv showed only v1. These are status checks,
  not proof of historical openness or novelty of this consequence.

The full pinned upstream statement and catalog assessment were read. The
immutable research_results.json has no OWR records or matching ID/code/title;
no separate prior AI proof report was available. Exact ID/source-code PR and
branch searches, two main attempt-directory histories, local all-ref history,
and related-target-group inspection found no prior Alec/campaign attempt.
Upstream source research does not count as an earlier campaign proof attempt.
