# Independent adversarial audit: 30002507 / OWR-12866-017

Date: 2026-10-05 UTC. Target rank: 722. Scope: the frozen five-approach author packet identified in BINDING.json.

## Verdict

**PASS WITHIN THE STATED RESTRICTED SCOPE. The original target remains UNSOLVED in this attempt, with 5/5 author approaches used.** No substantive mathematical correction to the five retained arguments is required. No complete ordinary-series construction or universal impossibility theorem has been obtained. This is an independent AI-assisted audit, not independent external human refereeing or formal proof certification.

The strongest retained conclusion is valid: using the credited Broucke-Vindas general-series theorem, for each prescribed compact subset K of {Re(s)>1/2} avoiding 1, sufficiently large integer parameters q give an ordinary Dirichlet series C_q that converges throughout {Re(s)>1/2}, has an exact simple zero at 1, and is nonzero on K. The choice of q depends on K. A compact containing 1 can instead be controlled to have no zero other than 1 by combining a small Rouché disk with its compact complement. There is no single parameter established to exclude additional zeros everywhere in that half-plane.

No novelty claim, exhaustive literature certification, or assertion of global openness is supported or made. The report preserves the frozen author files, including their historical pending-audit fields; the present verdict applies through the exact byte binding rather than by rewriting those files.

## 1. Scope and immutable binding

The author manifest has SHA-256 5f892f30acb55e30ccfcf88932e933c55b76942583bca032bbc8339d95548791. The archive DIRICHLET_ZERO_30002507_AUTHOR_FREEZE.zip is 29,837 bytes with SHA-256 d3c1884b33f378a1289dcbd6eea175dd0e721964f478a6ceb6186d7990d77b1b. All 17 manifest-listed payloads match their hashes and sizes. The manifest is the eighteenth safe file. The archive contains exactly these 18 flat files, each byte-identical to the safe directory; its CRC test passes.

The 2014 publisher PDF was independently rendered again and printed p.390 was visually inspected. It asks about an ordinary Dirichlet series converging in some open half-plane and having exactly one zero there. The audit therefore does not add boundedness, reality, signs, multiplicativity, finite order, entire continuation, or whole-half-plane uniform convergence. It does not replace actual convergence with continuation or ordinary integer bases with generalized frequencies. The exact multiplicity is unspecified in the original question; a simple-zero construction is sufficient. The chosen zero must be an interior point, not merely a boundary zero. The requested half-plane need not be the maximal convergence half-plane.

The cached repository queue observation matches rank 722, numeric ID 30002507, OWR-12866-017, and the stated title. The inaccessible live problem page and missing raw imported statement/prior AI report were not inspected; no access bypass or new claim about their contents was made. Earlier repository-search observations remain bounded historical observations, not an independently rerun exhaustive absence proof.

## 2. Approach 1: almost-periodic recurrence

**Accepted.** The proof genuinely assumes uniform convergence of the original partial sums on H_b. This supplies one Dirichlet polynomial approximating f uniformly on both the original boundary circle and every vertical translate of it. Local compact convergence alone would not supply that estimate.

For the finite logarithm vector, simultaneous approximation yields arbitrarily large positive almost-periods without requiring rational independence. If the approximating integers are unbounded, an unbounded subsequence works. If they remain bounded along arbitrarily accurate approximations, one positive integer repeats infinitely often and is an exact period, whose multiples are unbounded. This handles both alternatives correctly.

The boundary error is less than 3m/4, with m the strictly positive minimum modulus of f on the chosen circle. Rouché applies to f(s+i tau) and f(s), and it puts the corresponding zeros of f in the upward-shifted disk. Choosing successive shifts farther than the disk diameter gives distinct zeros. Multiplicities are correctly counted.

The consequences use the right domain. A zero strictly to the right of sigma_u recurs. Absolute convergence at a real c gives uniform convergence on H_c by a summable majorant, so a singleton zero cannot lie inside the absolute-convergence half-plane. An everywhere-convergent ordinary series is absolutely convergent at every real c: convergence at c-2 bounds its terms and leaves a summable n^(-2) majorant. Entire analytic continuation without everywhere convergence is correctly excluded from that inference.

The finite multiplier argument is also valid. Holomorphy of P(s) zeta(s) across 1 forces P(1)=0. Recurrence produces infinitely many other zeros of P in the chosen half-plane, and zeta has no pole at any of them. The alternating-zeta example correctly excludes the removable value at 1 and retains the nonzero vertical periods. No result here covers arbitrary conditionally convergent ordinary series.

## 3. Approach 2: conditional Möbius construction

**Accepted as conditional only.** The hypothesis |M(x)| <= C x^theta with theta<1 provides the needed ordinary convergence. A nonvacuous exponent is nonnegative: differences M(p)-M(p-1)=-1 at arbitrarily large primes rule out theta<0.

Partial summation includes the correct boundary term and lower endpoint. For sigma>theta the boundary term tends to zero and the integral tail is bounded by a constant times X^(theta-sigma). On a compact subset the distance sigma-theta is positive and |s| bounded, establishing local uniform convergence and holomorphy on the same H_theta. No passage to a smaller half-plane is hidden.

The convolution identity with zeta is first used only on H_1, where both series converge absolutely. Analytic continuation of the product identity then takes place on the connected punctured half-plane H_theta minus {1}. Since zeta is finite there, F cannot vanish away from 1. The local Laurent expansion with residue 1 gives F(s)=(s-1)/(1+(s-1)h(s)); hence F(1)=0 and F'(1)=1. This is a genuine simple zero of the convergent ordinary series, conditional on the stated power saving.

No such power saving is supplied. The difference between x exp(-c (log x)^a), 0<a<1, and a fixed power saving is correctly established by comparing logarithms. Boundary convergence at 1 is insufficient. The RH implication is an explicitly external classical dependency, and neither equivalence with RH nor an unconditional Möbius theorem is asserted.

## 4. Approach 3: sparse-prime perturbations

**Accepted.** The direction of the quotient is correct: primes in Q minus P contribute 1+p^(-s), and primes in P minus Q contribute its reciprocal. Positivity of delta ensures |p^(-s)|<1 throughout H_delta and prevents local-factor zeros there.

The summable prime condition makes the logarithm series normally convergent on every closed half-plane to the right of delta. Exponentiating gives a holomorphic nonvanishing multiplier and reciprocal. The local geometric expansions of both are ordinary Dirichlet series with absolutely summable coefficients at every real sigma>delta. This is the only use of an absolute Euler-product expansion; no conditionally convergent Euler product is smuggled into the proof.

The ordinary coefficient identity is established in a common absolute half-plane and is also a formal prime-factor identity. For an arbitrary fixed s with Re(s)>max(sigma_c(F_Q),delta), the partial sums S_Q(y) are bounded and converge. In the finite hyperbolic convolution sum, |u_d d^(-s) S_Q(X/d)| has a summable majorant independent of X. Dominated convergence therefore transfers ordinary, potentially conditional convergence. Applying the same argument to 1/U proves the reverse inequality. The stated equality of abscissae follows only when the original abscissa lies strictly to the right of delta; the proof does not claim equality otherwise.

The divisor statement is conditional on the existence of the indicated meromorphic continuations to the connected half-plane. A nowhere-zero holomorphic multiplier preserves every local order. Finite changes satisfy the prime sum condition for each positive delta, so they cannot improve a positive convergence abscissa. No nonsparse construction, and no repair of the withdrawn paper, follows.

## 5. Approach 4: representation obstructions

**Accepted.** Convergence at one real point bounds individual coefficients by a power of n and gives absolute convergence sufficiently far right. If m is the first nonzero index, the remaining normalized tail is bounded by a fixed multiple of (m/(m+1))^(sigma-b), uniformly in the imaginary part. Division by the nonzero leading coefficient is legitimate.

The derivative statement is not an unsupported termwise differentiation in a conditional strip. It follows by applying Cauchy's formula to the exponentially small holomorphic normalized tail on fixed-radius disks sufficiently far right. The normalized function is bounded away from zero there, so its logarithmic derivative is controlled.

For P exp(Q), the polynomial Q'+log m tends to zero along the real axis and therefore vanishes identically. Comparing P'/P=d/sigma+O(sigma^(-2)) with exponential decay forces d=0. The leading coefficient then fixes the remaining constant. For a rational target, its nonzero power asymptotic first rules out m>1; with m=1, the rational difference f-a_1 cannot decay exponentially unless it vanishes identically. Both arguments need only equality in a right half-plane.

The extension through finite-order entire factorization is explicitly dependent on Hadamard's theorem and is not used to exclude arbitrary entire infinite-order functions. General holomorphic factors remain outside the obstruction.

Seip's source defines sigma(chi) as a meromorphic-continuation abscissa. Its singleton choice at 2/3 meets the stated divisor conditions, for example with alpha=7/10<59/80; the conclusion still gives no required bound sigma_c<2/3 for the ordinary series. The audit does not turn coefficient restrictions in nearby continuation results into convergence estimates.

## 6. Approach 5: generalized-frequency rounding

**Accepted, with exactly the fixed-compact quantifier stated.** This is the principal result tested adversarially.

### Coefficients, ordering, and convergence

The assumptions x_k increasing with multiplicity and tending to infinity make every bounded frequency interval finite. Thus each set of equal ceil(q x_k) values is a finite consecutive block, and the coefficients b_m,q are finite well-defined sums. Grouping uses consecutive blocks; it is not an arbitrary rearrangement of a conditional series. Ordinary partial sums over m correspond to endpoints of these blocks, including zero coefficients at unused integers.

The counting condition A(X)=O(X) implies S_epsilon=sum |a_k| x_k^(-1-epsilon)<infinity by dyadic summation. For y_k=ceil(q x_k)/q, one has x_k<=y_k<x_k+1/q. Integrating the derivative of u^(-s), with real positive u, yields

|y_k^(-s)-x_k^(-s)| <= (|s|/q) x_k^(-1-epsilon)

whenever Re(s)>=epsilon>0. The bound is valid for complex s because |u^(-s-1)|=u^(-Re(s)-1). Absolute summability of the difference proves normal convergence of E_q and holomorphy on H_0. It does not prove absolute convergence of either original series.

At a fixed point of H_beta, adding the absolutely convergent difference to the given convergent general series preserves convergence in its original order. Consecutive finite grouping then proves convergence of the ordinary series B_q and the identity q^s B_q=D+E_q. Because beta>=0, the entire claimed domain lies in H_0. The proof uses no value of E_q outside its domain.

For the published input, coefficients have modulus at most 1 and the generalized-integer counting estimate gives A(X)<=N(X)=O(X). The ordinary output therefore converges on H_(1/2). This establishes sigma_c(C_q)<=1/2, not equality of its convergence abscissa with that of D. The packet does not falsely claim equality.

### Exact zero correction, holomorphic derivatives, and Rouché

Subtracting q^(-s) E_q(rho) changes precisely the ordinary coefficient with integer index q. The scalar is defined by an absolutely convergent difference series. The identity becomes q^s C_q=D+E_q-E_q(rho), so the target zero is exact, not numerically fitted or merely nearby.

On a fixed small boundary circle around the simple zero, the error tends uniformly to zero and is eventually strictly smaller than the positive minimum of |D|. Rouché gives exactly one zero counted with multiplicity; the forced zero is therefore simple. Independently, normal convergence and Cauchy's formula give E_q'(rho)->0, and differentiation at the forced zero gives

C_q'(rho)=q^(-rho) [D'(rho)+E_q'(rho)],

which is nonzero for sufficiently large q. The q^s factor is entire and nonvanishing, so it changes neither zero locations nor multiplicities.

For a fixed compact zero-free K, min_K|D|>0. The estimate O_K(1/q), also controlling E_q(rho), gives nonvanishing there for all sufficiently large q. It is important that K avoid rho when the conclusion is called nonvanishing. To control an arbitrary compact containing rho, combine the local disk result with its closed complement in that compact.

### Absolute convergence and abscissa safeguards

The proof does not establish uniform convergence or absolute convergence throughout H_(1/2). Directly from the counting estimate, absolute convergence is assured only to the right of 1. The forced zero at 1 is not inside that guaranteed absolute-convergence half-plane. There is consequently no contradiction with Approach 1 and no hidden replacement of conditional convergence by absolute convergence.

A simple analytic stress test is D(s)=sum from n=1 to infinity of (-1)^(n-1)(n+1/2)^(-s). It converges on H_0 by summation by parts, while at s=1 its absolute series diverges. With q=1 the rounded ordinary series uses n+1 and retains conditional convergence at 1. Thus the rounding mechanism itself demonstrably does not require absolute convergence of the underlying series.

Exact preservation of the convergence abscissa cannot be inferred merely from grouping. For each k>=1, take frequencies k+1/4 and k+1/2 with coefficients +1 and -1. The weighted counting function is O(X). The original series converges for Re(s)>0 because its paired differences are absolutely summable there and the individual terms tend to zero; it fails at s=0 because its individual terms do not tend to zero. Thus its abscissa is 0. Rounding with q=1 groups each pair at k+1 and yields the identically zero ordinary series, whose abscissa is minus infinity. This is a verification counterexample to an unstated strengthening, not a sixth target-solving approach or a defect in the packet.

### The actual remaining gap

The quantifiers cannot be exchanged: for each K, there exists q(K) does not imply there exists q valid on every K. The normalized approximants q^s C_q have locally uniform limit D, whose frequencies need not be integers. Multiplication by q^s is not generally an ordinary-series-preserving operation. Neither taking that limit nor noting that zeros escape compact sets produces one ordinary coefficient sequence with a singleton global zero set.

The escaping-root polynomial control is correct: h_N(s)=(s-1)(1-s/(2+iN)) tends locally uniformly to s-1, but each h_N has the extra zero 2+iN inside H_(1/2). The stated compact error estimate follows from |s-1|<=R+1. This is a counterexample to a general inference, not an asserted ordinary-Dirichlet-series counterexample.

The phase-separation control is also exact. For distinct positive x and y, the chosen odd multiples of pi/log(y/x) make the two unit-modulus phases opposite. Hence a small frequency displacement gives no uniform-in-height smallness. The two-term rounding/correction example retains infinitely many periodically spaced zeros after restoring the real zero. All three controls point to the same missing all-height exclusion.

## 7. Source dependencies and inspection limits

- Original target: [2014 publisher report](https://ems.press/content/serial-article-files/46499), printed p.390. Independently rendered and visually inspected from the hash-bound PDF.
- Invalid solution dependency: the live [Hilberdink-Saias arXiv record](https://arxiv.org/abs/1812.11880) was rechecked. It records withdrawal on 2024-04-26 and an irreparable error in the main proof. The old successful abstract does not override this notice. No particular erroneous lemma is identified here.
- Valid external input: [Broucke-Vindas v2](https://arxiv.org/abs/2102.08478v2), Proposition 1.4 and Theorem 3.1, with published reference Math. Z. 307 (2024), article 62. The statements and relevant Section 3 were read; pages 3 and 11 were independently rendered and visually inspected. The source provides a general series and an O(X) integer count. Its representation zeta_P(s)=s/(s-1) exp(Z(s)), with Z holomorphic near 1, proves the reciprocal has a simple zero. The underlying probabilistic approximation theorem is credited, not independently reproved in this audit.
- Continuation boundary: [Seip v2](https://arxiv.org/abs/1812.11729v2), definition of sigma(chi) and Theorem 1.1, were read. The continuation/convergence distinction is verified directly.
- Eight local public-source PDF/HTML objects were matched to the author's published size/hash metadata. Hash equality establishes byte identity, not theorem correctness. The 2023 finite-value refinement remains abstract-only in the author inspection record; no stronger inspection claim is added.

The exact inaccessible target page was not retried. Missing raw imported records remain uninspected. No source PDF, extraction, page image, raw imported record, or private coordination material is included in the audit payload.

## 8. Reproduction and finite-control limits

The author controls were independently rerun from a relocated temporary directory and unrelated working directory. The 67,207 exact predicates reproduced byte-for-byte in direct normal and direct optimized Python runs. Both author manifest replay modes passed. All 12 author damaged-package cases were rejected and their output reproduced exactly. Direct optimized runs were used because an optimized parent Python process does not automatically propagate optimization to a separately launched child interpreter.

The independently written controls import no author code. They use a sieve-based factor table and direct prime-exponent formulas for the two multiplier directions, explicit divisor convolutions, rational frequencies with repeated values and collisions, exact target-zero fixtures at rho=1,2,3, q up to 25, corrected identities away from rho, and Gaussian-rational escaping zeros. All 192,572 positive finite predicates and 6 mathematical negative controls pass, byte-identically in normal and optimized Python.

The author correction fixtures test the generalized identity obtained by subtracting D(1)+E_q(1); when D(1) is not zero, those fixtures do not directly instantiate the exact stated corollary. This is a coverage limitation only. The independent fixtures enforce D(rho)=0 first and then subtract only E_q(rho), directly checking the stated correction.

The independent binding checker pins both handoff digests rather than merely checking a manifest's internal consistency. All 18 independent corruptions are rejected in both normal and optimized modes, including a self-consistently rehashed payload, archive corruption, duplicate JSON keys, added source-like content, and symlinks. A manifest checker without an external digest cannot authenticate a newly rehashed alternative package; this is why BINDING.json and the frozen values matter.

Reproduce with Python 3:

1. Run independent_controls.py and compare its stdout with INDEPENDENT_CONTROL_RESULTS.json; repeat with -O.
2. Run verify_frozen_binding.py with --author pointing to the directory containing the frozen safe directory and author archive.
3. Add --negative-controls and compare stdout with INDEPENDENT_NEGATIVE_RESULTS.json; repeat with -O.
4. Verify every audit payload against AUDIT_MANIFEST.json and pin the audit manifest's separately reported digest.

None of these finite controls is an analytic proof, a zero search covering an unbounded domain, or evidence that the original target has been solved. The analytic verdict above rests on the explicit proof review and its credited dependencies.

## 9. Final disposition

The frozen author packet is accepted as an honest unresolved five-approach checkpoint. Its restricted theorems, conditional result, and fixed-compact rounding deduction are sound under their stated hypotheses and external dependencies. No mandatory mathematical correction was found. Preserve the unresolved status and five-approach count. Do not promote local nonvanishing to global uniqueness, continuation to convergence, or the generalized example to an ordinary-series solution. No remote writes were performed.
