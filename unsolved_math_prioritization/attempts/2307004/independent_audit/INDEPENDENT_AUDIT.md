# Independent audit: Function Theory 7.4 / 2307004

Date: 2026-10-05 UTC. Rank: 688. Catalog code: AMR-022-7004.

## Verdict

**PASS for the stated scoped partial results and the unsolved, five-approach disposition. No blocking mathematical defect found. This is not a solution of the sharp-constant problem, a novelty finding, a proof-assistant verification, or human peer review.**

The audit is bound to the 16-file frozen packet whose `FREEZE_MANIFEST.json` has SHA-256 `cd89e252a6d2e0ad4eeaa9696e361c99f68c4fb89419f94c6f78e66402a16dac`. Its 15 manifest entries and the manifest itself were checked; no frozen file was edited. The audit made no remote write and used no helper researcher.

The strongest finite certificate independently confirms existence of 32 complex numbers, one equal to 1, with every first-32 power sum strictly below 29/40 in modulus. This upper example does not identify the optimum or establish a best published bound.

## 1. Exact claim and scope

The governing primary statement is Hayman–Lingham, Problem 7.4, printed page 161 / PDF page 162. It fixes one complex number at 1, allows arbitrary complex values for the other entries, takes the first n positive exponents, and asks for the best universal constant in a strict inequality. The audit inspected the page visually and in text. The restrictions and shifted window of adjacent Problem 7.3 must not be carried into 7.4. [Primary collection](https://arxiv.org/pdf/1809.07200v2).

Let M_n be the maximum of the moduli of these n sums. The supremum of constants c satisfying M_n>c for all allowed tuples and all n is the infimum of all objective values. Whether the infimum itself is admissible for the strict inequality is a separate attainment question. The packet makes this distinction correctly.

For each fixed n, division by an entry of maximum modulus R>=1 multiplies the k-th sum by a complex factor of modulus R^(-k). Reordering makes the resulting maximal entry 1, and all new entries lie in the unit disc. Conversely, a unit-maximum tuple can be rotated and reordered to give an entry 1 without changing any power-sum modulus. Thus the fixed-root infimum equals the compact normalized minimum R_n. This also proves fixed-n attainment; it does not prove attainment of the infimum over all n.

The all-n target is inf_n R_n. It is not automatically limsup R_n, and no such identification is used. Adding a zero lengthens the exponent window; the packet supplies a valid exact example where that worsens the objective. Restricted real or unit-modulus problems cannot replace the general complex problem.

## 2. Full complex n=2 result

**Accepted:** R_2=sqrt(3-sqrt(5)).

I independently expanded the completed-square identity in the real and imaginary coordinates of w=1+z_2, rather than accepting the author's polynomial coefficient table. Write t=|w|^2 and x=Re(w). The identity is

|w^2-2w+2|^2=(t-2)^2/2+8(x-(t+2)/4)^2.

The smaller root t_0 of t^2-6t+4=0 is 3-sqrt(5), and it lies between 3/4 and 4/5. If t<t_0, then (2-t)^2/2>t_0, so the second moment already exceeds sqrt(t_0). If t>=t_0, the first moment meets that bound. At t=t_0 and x=(t_0+2)/4 the radicand for Im(w) is positive, the completed square vanishes, and both moment moduli equal sqrt(t_0). The remaining root has squared modulus t_0/2<1. Thus the proposed witness is genuinely complex and admissible in the normalized problem.

This is a global proof for the two-variable complex case, not a numerical optimizer result or a proof for unbounded n. The checker independently verifies the identity and exact endpoint isolation; the global minimax conclusion is the prose argument above.

## 3. Strict one-half lower bound and its limitation

**Accepted:** every allowed finite tuple has M_n>1/2.

The fixed-root recurrence follows by logarithmic differentiation of the product over all roots except 1. Assuming all moment moduli are at most 1/2 gives

|C_(j-1)-j b_j|<=B_(j-1)/2,

where C_j is a coefficient partial sum and B_j is the corresponding sum of moduli. If |C_(j-1)|>=B_(j-1)/sqrt(2), the disc for j b_j avoids zero and lies within angle pi/4 of C_(j-1). Projection therefore propagates |C_j|>=B_j/sqrt(2). The nonzero-center requirement is valid because B_j>=1. The terminal identity has b_n=0 and forces |C_(n-1)|<=B_(n-1)/2, a contradiction. The case n=1 is immediate.

The scalar-cone obstruction is scoped correctly: demanding the same uniform projection estimate for an invariant with factor gamma gives q^2<=gamma^2(1-gamma^2)<=1/4. This excludes improvements using that particular estimate alone, not every stronger recurrence argument or the true extremal constant.

A logical distinction matters: proving M_n>1/2 for every tuple, or even R_n>1/2 for every n, alone gives only inf_n R_n>=1/2. A uniform positive improvement requires additional work. The packet does not claim its short proof provides that improvement; it separately cites Biró's stronger published theorem.

## 4. Coefficient bounds and restricted classes

**Accepted:** the coefficient majorant, the degree-dependent rho_n bound, and the sharp restricted-class constant 1.

For nonnegative M, the coefficient majorant d_j(M)=(M)_j/j! follows by the positive triangular recurrence. Evaluation at the forced root yields 1<=sum_{j=1}^n d_j(M), and the partial sum is product_{k=1}^n(1+M/k)-1. The unique positive crossing at 2 is well defined, and its parameter tends to zero by divergence of the harmonic series. It is not a uniform positive lower-bound solution.

If every root has modulus at least 1, the top coefficient has modulus at least 1. For M<1, every factor in d_n(M) is below 1, which is a contradiction. The construction using all but one of the (n+1)-st roots of unity gives equality in every measured modulus; rotation makes an entry 1. Hence 1 is sharp in this exterior class, including its unit-circle subclass. For real tuples, the second sum is at least 1 when n>=2, and the tuple (1,0,...,0) gives equality. Neither restriction is imposed in the original target.

## 5. Inverse moments and constant-moment obstruction

**Accepted:** arbitrary proposed complex moments s_1,...,s_n are realizable by n complex roots including 1 if and only if the specified coefficient b_n vanishes.

For sufficiency, take the degree-at-most-n polynomial P(t) represented to order n by exp(-sum s_k t^k/k). The condition b_n=0 is exactly P(1)=0 after division by 1-t. The reciprocal F(X)=X^n P(1/X) is monic of degree n because P(0)=1. The fundamental theorem of algebra gives n complex roots counted with multiplicity; any degree deficit in P produces zero roots of F. The equation F(1)=0 supplies the required distinguished root, and the logarithmic derivative or Newton identities recover precisely the first n moments.

No modulus, distinctness, realness, or conjugate-symmetry condition is needed. In particular, an algebraic certificate for the moments does not need decimal root approximations. Normalizing the realized tuple if desired preserves the upper bound, although it need not preserve the original moments.

When all moments equal u, b_n=(1-u)_n/n!, whose zero set is exactly {1,...,n}. This correctly rejects the constant-moment construction below 1; it does not rule out multiple blocks or varying phases.

## 6. Two-block construction and independent rational replay

**Accepted:** the two-block linear constraint and the exact n=32 strict upper certificate.

With m=floor(n/2), all perturbation terms have degree at least m+1, so products of two such terms exceed degree n. The coefficient-n constraint is consequently linear in the high moments. Its coefficients and right-hand side agree with the packet's formula. The image of a product of complex discs under that linear map is the disc with summed radii; the proposed phase alignment realizes every point in it. The coefficient v_n=1/n prevents a zero denominator.

The independent checker imports no code from the frozen packet. It uses pairs of exact rational numbers and constructs P by multiplying the truncated factors exp(-s_k t^k/k). It then inverts P as a formal series and recovers the moment sequence from -tP'/P. This independently checks the author's recurrence-based certificate with a different computational construction.

Results:

- The input manifest and every frozen file match their specified hashes and lengths.
- The original standard-library verifier exits successfully and reproduces its stored output.
- All 32 strict squared-norm inequalities hold exactly.
- Every squared-norm gap from (29/40)^2 exceeds the rational number 3/1000; the smallest gap occurs at moment 19.
- P(0)=1, P(1)=0, the reciprocal polynomial is monic of degree 32, and all logarithmic moments are recovered exactly.
- Division by 1-t and the two-block affine constraint both hold exactly.
- Known-root fixtures include repeated roots, zero roots, and roots outside the unit disc.
- A final-moment perturbation is rejected by the root constraint; a separate enlarged moment is rejected by the radius constraint.
- The independent checker produces identical output with and without Python optimization. The original checker correctly refuses optimization because it uses assertions.

The optional floating exploration and phase generator are not the acceptance mechanism. Their output is not evidence of global optimization, monotonicity, convergence, or sharpness. No sampled search was used as a proof in this audit.

## 7. Literature reconciliation

The three source PDFs were freshly fetched independently with HTTP 200. Their exact byte counts and SHA-256 values agree with the frozen provenance. Source PDFs, rendered pages and extracted text remain outside the authored audit deliverable. Details are recorded in `SOURCE_AUDIT.json`.

Biró's lower-bound paper, printed page 344, explicitly states an effectively computable uniform q>1/2 for arbitrary complex roots with the first root 1 and says a numerical value is not computed. I checked that statement visually and examined the recurrence/proof outline. This audit does not independently certify every estimate in that published proof or extract q. [Primary lower-bound paper](https://users.renyi.hu/~biroand/pdfs/Turan1.pdf).

Biró's upper-bound paper defines the same normalized finite quantities. Its theorem concerns limsup R_n. The displayed choice on page 507 gives limsup R_n<=sqrt(17/25)<5/6; its addendum reports Harcos's computation giving limsup R_n<0.69368. The latter remains a source-verified numerical report, not an interval calculation re-certified here. The packet's qualifications are accurate. [Primary upper-bound paper](https://users.renyi.hu/~biroand/pdfs/AnUpperEstimateinTuran.pdf).

Griego's version-v1.0.0 README explicitly describes 0.6906538 as a proposed asymptotic upper certificate, supplies no finite threshold, and separates exact verification of a limiting inequality from the analytic reduction. The independent audit read that public description, not the complete proof or executable verifier. Absence of a finite threshold is not by itself a defect in a valid asymptotic proof; the relevant limit is that checking the limiting numerical inequalities alone does not verify the reduction. No result here adopts the proposal as a proved sharp constant. [Primary public proposal](https://github.com/sebastian-griego/turan-c42-certificate/tree/v1.0.0).

A current constants registry likewise defines C_42 using limsup R_n and labels the recent value as proposed. It is useful corroboration of scope, not a replacement for the primary proofs. [Registry entry](https://teorth.github.io/optimizationproblems/constants/42a.html).

Two nonblocking attribution cautions:

1. The collection's historical attribution associates 1/3 with Atkinson [35]; modern summaries distinguish the 1961 published 1/6 estimate from later improvements. The packet says what the collection records and discloses that the original Atkinson proof was not inspected. It should not be tightened into a claim that this audit verified 1/3 in the 1961 paper.
2. Erdős problem 519 asks for existence of a positive universal constant and is already solved. That is weaker than determining the best constant in Function Theory 7.4. A solved flag for the existence problem would not resolve this target.

Neither caveat changes any authored mathematical result or requires editing the frozen packet.

## 8. Disposition and limits

The five approaches are substantively distinct as recorded: exact finite-dimensional minimax, phase geometry, coefficient majorants and restricted classes, inverse-moment algebra with a rejected ansatz, and two-block finite construction. Treating these as the five exhausted approaches is consistent with the supplied record; no additional budget or full solution is implied by this audit.

The necessary unresolved work remains a sharp all-n lower bound, a matching construction or extremizing sequence, and strict-endpoint analysis. None of the finite checks or cited asymptotic upper claims provides that.

This review checked mathematical validity, finite certificate replay, freeze integrity, and the main source-scope claims. It did not repeat the original repository duplicate survey, independently reproduce the dataset corpus, examine an unavailable prior AI report, or exhaust the mathematical literature. The catalog and source metadata are not being promoted into proof. All remote publication decisions remain separate.

## Replay

From this audit directory, with the frozen packet in the sibling `safe_output` directory:

    python3 -B check_certificate_independent.py

Alternatively supply its directory explicitly. The script prints `INDEPENDENT_REPLAY.json` deterministically and never writes to the input. `AUDIT_BINDING.json` records the audited input manifest, all original file bindings, and the hashes of the audit artifacts.
