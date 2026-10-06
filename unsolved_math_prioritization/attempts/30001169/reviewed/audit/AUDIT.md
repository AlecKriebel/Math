# Independent adversarial audit: weighted Yamabe heat-trace monotonicity

## Verdict

**Accept the stated partial results; the original arbitrary-weight, all-time problem remains unresolved in this attempt.** No material mathematical error was found in the audited author packet. No correction to its claims is necessary. A separate derivative-remainder clarification makes one standard analytic step explicit. This is an independent mathematical and computational audit, not a formal proof assistant verification and not a certification of the global literature's current status.

Target: ID 30001169, rank 822, OWR-3389-022; dimension n>=4. The frozen author's five approaches are exhausted. The neighboring dimension-three comparison investigation, ID 30001168, is not a solution or counterexample for this target.

The accepted author public derivative ZIP is pinned externally by SHA-256 3f73854c0fb2b1aaaa1b807f903e681efb31be5c980feb071ca90b29c969b821, 16017 bytes. Its ten files are reproduced byte-for-byte under author/. Only an editorial paragraph and its manifest entry differ from the previously audited packet; the mathematics, code, claims and results are unchanged. This separate audit derivative updates the author identity pin and reruns the exact and mutation checks against the accepted public files. Audit additions remain separate under audit/. The original audit is preserved.

## Source identity and scope

All three complete supplied corpora were hashed afresh, then the target was found uniquely in both catalog and problems. The complete record together with its empty report entry was reconstructed using the stated serialization. Its 3832 bytes match the reviewed complete-record file exactly and produce b85a5eda1e0fa5cf3ce3f07b5919c7ad445a349a8ac382b5e1bf68b1c1f77ba3. The raw statement hash also matches the catalog. No excerpt-only substitution was used for this comparison.

The official EMS report was opened on the web, and locally hashed official PDF bytes were rendered and visually inspected at printed pp. 421–422 (one-based PDF pp. 67–68). They specify the weighted operator, volume normalization and n>=4 monotonicity question. They separately record the round case and large-time bound. Juhl's primary PDF was opened, its locally available bytes hashed, and p. 74 visually inspected for the dimension-four coefficient. Source metadata and retrieval limitations appear in PUBLIC_SOURCE_REVIEW.json. No corpus content, PDF, extract or screenshot is in this deliverable.

Primary links: [OWR 06/2009](https://ems.press/content/serial-article-files/46205), [Juhl](https://arxiv.org/pdf/1411.7851).

## Analytic checks

1. **Operator and Hilbert space.** With the positive Laplacian, c_n=(n-2)/(4(n-1)) and Y=Delta+n(n-2)/4. For h=Wg, dv_h=W^{n/2}dv_g. Multiplication by W^{n/4} is unitary from L^2(dv_h) to L^2(dv_g). Conformal covariance gives conjugation exponents n/4-(n+2)/4=-1/2 on the left and (n-2)/4-n/4=-1/2 on the right. The resulting operator is exactly Y_W. Positivity follows from its positive quadratic form. Smooth positive W on a compact sphere gives a self-adjoint elliptic operator with discrete positive spectrum and the applicable heat expansion.

2. **Normalization and scaling.** Replacing W by aW divides every eigenvalue by a and sends f(t) to a^{n/2}f(t/a). Derivative sign is preserved; the time coordinates change. The normalized leading n=4 coefficient is Vol(S^4)/(4pi)^2=1/6. No normalized trace convention was silently substituted.

3. **Small times.** The first coefficient is (4-n)/(12(n-1)) times the positive total scalar curvature, including the common heat normalization. The total curvature is positive by conformal covariance and the round energy identity, even when scalar curvature is not pointwise positive. In dimension four, the integrated potential terms cancel to leave (1/180) integral(|Rm|^2-|Ric|^2). Conformal flatness and Gauss–Bonnet on S^4 give the integral -32pi^2 and normalized coefficient -1/90. Thus f=1/6-t^2/90+O_W(t^3). The derivative conclusion is valid, but cannot follow by naively differentiating that displayed O-term. DERIVATIVE_REMAINDER.md gives a complete finite-difference justification using a longer standard expansion. It establishes f'=-t/45+O_W(t^2), hence strict decrease for every fixed W near zero. It supplies no common epsilon over all W.

4. **Large times.** The generalized Rayleigh quotient has denominator integral(W v^2), which Hölder bounds by Vol(S^n)^{2/n} times the critical L^q norm squared. The sharp round Sobolev inequality supplies the matching lower bound in the numerator. Therefore lambda_0(W)>=n(n-2)/4. The differentiated trace equals t^{p-1} sum_j (p-t lambda_j)e^{-t lambda_j}. For t>=2/(n-2) every summand is nonpositive, and sufficiently high eigenvalues make at least one summand strictly negative. Absolute convergence makes the entire sum strictly negative, including the endpoint.

5. **Near-round interval.** Ordered min–max bounds compare each eigenvalue with the corresponding ordered round eigenvalue divided by M and m; eigenvalue crossings do not invalidate the multiplicities. For n=4 the first nine blocks have multiplicities 1,5,14,30,55,91,140,204,285 and eigenvalues (ell+1)(ell+2). Because q'(x)=(x-3)e^{-x}, q has a minimum, not a maximum, at 3. Taking the larger endpoint value over each full time/eigenvalue interval is the correct upper bound, including intervals straddling 3. The first omitted degree is 9, eigenvalue 110; at t>=1/4 its weighted lower bound already has t lambda>2. Every omitted contribution is negative. Discarding that entire convergent tail therefore preserves an upper bound without a tail-size estimate.

## Independent exact computation

The author's alternating-series exponential implementation is correct: the odd and even Taylor truncations enclose exp(-z) on [0,1], integer floor/ceiling are outward, squaring is monotone on its nonnegative enclosure, and multiplication by a negative q prefactor correctly selects the lower exponential endpoint.

To avoid merely replaying the same implementation, independent_check.py uses a different elementary enclosure. Put N=2^96 and y=x/N. For 0<=y<1,

(1-y)^N <= exp(-x) <= (1+y)^(-N).

Start with the exact rational endpoints and perform 96 outward-rounded squarings at scale 10^70. The exponential bounds follow from log(1-y)<=-y<=-log(1+y), or equivalent elementary exponential inequalities. No floating-point arithmetic or removable Python assertions enter this computation.

All 750 time intervals and 13500 exponential evaluations pass. The worst interval is index 0, [1/4,251/1000]; its exact rational upper bound lies between -0.006347226344246828861225 and -0.006347226344246828861224, strictly below -3/500. Thus the frozen quantitative partial theorem holds for normalized smooth W with 999/1000<=W<=1001/1000 and every t>=1/4. INDEPENDENT_RESULTS.json records exact fractions. The interval between a weight-dependent small-time neighborhood and 1/4 remains unfilled.

The normal, optimized and relocated replays and rejection mutations are recorded in MUTATION_RESULTS.json. These tests check exactly the pinned source and the listed mutations; a rewritable manifest alone is not an authenticity mechanism. The outer ZIP hash must be independently pinned. The verifier's success does not formalize the analytic arguments.

## Remaining approaches

- **Infinite cylinder.** The density is (4pi)^{-1/2}t^{(n-1)/2} times the shifted sphere trace. For n>=5 the shift above the round Yamabe operator in dimension n-1 is exactly 1/4; the argument uses the round-case theorem recorded in the primary report, rather than independently reproving that theorem. Multiplication by e^{-t/4} makes the positive nonincreasing round trace strictly decreasing. For n=4, the Poisson identity for t^{3/2}sum_{j>=1}j^2e^{-tj^2} has the stated coefficients. The spectral derivative is negative at and above 3/2, with j>=2 providing strictness at the endpoint. The dual derivative has sign 3-2pi^2 k^2/t and is negative below 2pi^2/3. The ranges overlap because pi>3. Local uniform convergence justifies both differentiations. This proves the infinite density's result only; compact capped-cylinder end effects remain uncontrolled.

- **Exploration.** The radial Jacobi parameter q+1, round eigenvalues and S^3 harmonic multiplicity (q+1)^2 are correct. The complete 42-record scan was rerun with one BLAS thread and reproduced the frozen JSON byte-for-byte. Exactly six coarse scans have positive maxima; all six refined scans have negative maxima. These observations have no certified quadrature, eigenvalue or omitted-tail enclosure and are not counterexamples or proofs. A negative omitted tail specifically defeats interpreting a positive truncated sum as a lower bound.

- **Abstract spectral model.** Moving five eigenvalues from 6 to 100 preserves the leading small-time coefficients through t^2 and the lowest eigenvalue. It lowers the trace at every time but produces an intermediate positive derivative. The tail polynomial ratio at ell=2 is 25/7<4, the exponent gap is at least 4, and the exact lower bound 15860455230626365/199073177278611456 exceeds 1/20. The model is not claimed to be a weighted Yamabe spectrum. It correctly refutes only the proposed use of endpoint information alone.

## Acceptance boundary

Accepted: the fixed-weight small-time theorem including n=4; the known large-time range; the exact near-round n=4 theorem for t>=1/4; the infinite-cylinder density calculation with its stated round-case dependency; and the nongeometric obstruction to an endpoint-only argument.

Not established: monotonicity for every admissible W and every positive t; a geometric counterexample; any transfer from the neighboring n=3 problem; rigorous signs for the scans; a uniform small-time interval under pointwise closeness; novelty, priority, or a complete current literature search.

The independent audit made no remote mutation, publication or external outreach. The accepted mathematical scope remains intact.
