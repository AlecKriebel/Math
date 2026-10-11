# Independent checkpoint before decisive new-source comparison

Timestamp: 2026-10-06 18:53 UTC. Immutable PR117 head: 8163ee0dc7a0f944570925984cef2dc0fb291ad8. Source identifier 30001234 / OWR-3471-008. This record freezes this family's independent reasoning before reading the new 2013 Takagi paper pointer supplied by the root. No other new priority-family reports were read.

## Independent conclusion at this checkpoint

The candidate is a correct explicit counterexample to the exact universal singleton-fiber question. The original ideal is the generic 2-by-3 size-two determinantal ideal, with one cyclic sign reversal. Prior threshold theory already yields a negative answer once combined with the exact conditional LP theorem. At this checkpoint this family has **not located an explicitly published answer to the numbered question**. The prior-theory conclusion is a deduction made during this review, not a quotation or attribution of an explicit historical answer.

The candidate adds a short, transparent complete-face calculation to that deduction. Its ideal, threshold, and failure of the conditional LP theorem's hypothesis are direct consequences of familiar prior theory. This is a substantial priority concern for publication as a novel resolution of an original open problem; it does not prove that every sentence of the candidate has been published or that the candidate has no expository value.

## Exact implication, including the local-at-origin bridge

Let I be generated in C[x1,x2,x3,y1,y2,y3] by x1y2-x2y1, x2y3-x3y2, and x3y1-x1y3. A counterexample over C suffices for the universal characteristic-zero question. No arbitrary-field threshold extension is needed for this priority implication.

The source LP has all nine augmented rows. The last three constraints give objective at most three; z0=(0,0,0,1,1,1) and z1=(1,1,1,0,0,0) each have image 1_9 and objective three. Thus its optimum is exactly three. Saturating the last rows and using the three directed top-row comparisons forces all mu coordinates equal, and yields the candidate's full rational optimal segment.

Shibuta–Takagi Proposition 2.1, primary arXiv:0810.1278v3 pp.6–8, says the exact singleton-image-fiber hypothesis implies **lct_0(I)=LP optimum**. Question 2.2 asks the universal minimal-binomial, monomial-free version. The section heading concerns complete intersections, but Proposition 2.1 itself does not assume a regular sequence. The latter enters the separate Theorem 2.4, not this conditional implication.

Docampo's primary arXiv:1011.1930v2 Theorem 5.6, printed pp.21–22, computes the **global** threshold for rank-at-most-k matrices of size r-by-s as min_{i=0..k}(r-i)(s-i)/(k+1-i). The specialization (r,s,k)=(2,3,1) is min(3,2)=2. His introduction credits Johnson's 2003 thesis; that thesis was not retrieved or read by this family. The source arXiv history dates v2 to 2011-02-20, while the retrieved PDF's ordinary title date is June 2, 2018; both are preserved without equating them. The related journal citation is 2013. AMS journal body requests returned 403, so this family relies on the actual primary preprint body, not an assumed publisher-body identity.

A global value two alone is insufficient to conclude lct_0=2. Here the missing bridge is checkable independently. The rank-one variety Z is irreducible, four-dimensional, and contains zero. On x1 nonzero it is parametrized by free (x1,x2,x3,y1), with y2=x2*y1/x1 and y3=x3*y1/x1. Thus its dense rank-one locus is smooth of codimension two. Blowing up this smooth locus gives a divisor with ideal order one and log discrepancy two. The corresponding divisorial valuation extends on a proper birational model, its center closure is Z, and zero belongs to Z. Mustata's primary arXiv:1107.2676v1 p.5 expressly uses divisors whose centers **contain** the tested point, not only divisors centered at that point; p.8 Example 1.5 gives the codimension-r smooth-center blowup discrepancy r-1. Therefore lct_0(I)≤2.

For a stronger explicit check, blow up the origin. In the x1 chart write x1=u, x2=u*a, x3=u*b, y1=u*c, y2=u*d, y3=u*e. The three pulled-back minors are u²(d-ac), u²(ae-bd), u²(bc-e). Let D=d-ac and E=e-bc. The residual ideal is (D,E); the third residual minor is aE-bD, and the first exceptional divisor is (u=0). The chart is smooth, and u,D,E are independent coordinates, so the strict center is smooth and meets the first exceptional divisor transversely. Row and column permutations give all six entry-pivot charts and cover the first blowup.

Blow up the strict center (D,E). In the D chart let D=v, E=v*w. Then I pulls back to the principal ideal (u²v), and the direct Jacobian determinant of the composite to A6 is u^5*v up to sign. The E chart is analogous. The two divisors are coordinate normal crossings. Their ideal orders are (2,1), ordinary discrepancy coefficients (5,1), and log-discrepancy ratios (6/2,2/1)=(3,2). The second divisor maps onto Z, including zero in its center closure. This reproduces lct_0(I)=2 without substituting a global invariant for a local one.

Consequently, if the singleton-fiber condition were true for these minimal monomial-free generators, the source theorem would imply 3=lct_0(I)≤2, a contradiction. Its failure is already a direct consequence of prior threshold and discrepancy theory. Neither the LP optimum nor the discrepancy upper bound requires a new construction.

## Boundary controls

- The ideal is polynomial and its generators remain minimal at the homogeneous maximal ideal. Inverting an entry makes the third minor redundant; that is not the source hypothesis.
- This is an ideal generated by all three size-two minors of a matrix of six **independent** variables, not a specialized matrix or the determinantal ring's own threshold.
- The threshold implication uses the full augmented LP and nonstrict inequalities. It does not substitute a later modified graph LP.
- The contrapositive proves that no optimizer satisfies the exact condition. It does not confuse nonunique optimizers with a failure of a singleton image fiber.
- Threshold equality by itself would not imply the condition; the source theorem gives only a forward implication. A strict mismatch is what supports the contrapositive.
- A global threshold or a center excluding zero cannot alone establish the local contradiction.

## Actual verification and remaining gap at this checkpoint

run_checks.py actual process 70549 completed successfully. Both normal and physical Python -O runs passed 73 explicit exception checks; the deliberately false guard failed with nonzero exit in both modes. Computations reconstruct all augmented rows, exact rank/kernel/endpoints and dual certificate, all six blowup pivot charts, the two second-blowup charts, total transforms/Jacobians, formula specialization, and rejection of global-only/equal-threshold/reverse-inequality/normalization/row-dropping substitutions. They are diagnostics supporting the written unrestricted argument, not tests of literature priority.

This family estimates bounded priority-audit completion 70%. The remaining stage is to inspect the new exact-primary-source pointer from the independent original-question family. The original construction budget remains 1/5; this family used zero additional central proof-search turns. No Git/index/ref/global/shared/service/native changes or outside communication occurred.

