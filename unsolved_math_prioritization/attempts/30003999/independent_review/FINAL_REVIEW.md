# Independent full partial-package review: 30003999

**Verdict: PASS for the frozen partial results, with no mandatory mathematical correction. The original positive and general fixed-rational-base sign questions remain unsolved after five substantive author turns.** No polynomial-time solution or hardness result is certified. This is separate adversarial AI review, not human peer review or a novelty assessment.

## Frozen version and independent checks

- `RESULT.md`: SHA-256 `5ac893fd4f3eb1e7fe6feb66b17aaf73ec99b6de3b82fc8e563f34ab86e9d3f7`
- `FROZEN_MANIFEST.json`: SHA-256 `166ed4af90ce10be5e2d0e6c7b674f55432b0a39286b019ab260f5fbc69be582`
- All 29 public-file hashes and all six source-PDF hashes matched
- All five author checker outputs reproduced byte-for-byte, totaling 204,056 recorded exact controls/cases
- A separately authored checker passed 161,319 exact assertions without importing author functions

I had no role in this candidate's derivation. I read all five mathematical turn files, the result, source audit, complete recovered source record, checker code and receipts. The finite tests supplement the universal proofs below; they do not establish bit-complexity bounds by sampling. No author file was changed.

## 1. Exact primary question and encoding

I visually inspected the original printed p.3015 of [OWR50/2018](https://ems.press/content/serial-article-files/46772). The base is the rational number 2/3 with exponent r_i. It is not the cube-root expression in the imported record. The same page fixes the rational base in the generalized question and makes the rational coefficients part of the input. The paper's remarks about integer and reciprocal-integer bases agree with the package's distinctions.

The stated normalization is sign preserving: absorb negative-base parity in coefficients, invert a positive base below one by negating exponents, clear denominators with a positive common multiple, collect equal exponents, and shift all exponents by the least one. None requires constructing the potentially huge power removed as a positive factor. Coefficient-denominator products have bit length bounded by the sum of the denominator lengths. Signed binary exponents, term delimiters, zero exponents and rational coefficient heights are included. Bases ±1 and the defined cases of base zero are treated separately; negative exponents at zero are not assigned a fictitious value.

## 2. Turn 1: equality and positive pruning

For normalized alpha=p/q>1, every successful ascending carry represents the exact remaining expression after removal of a positive power. Clearing q denominators forces p^d to divide the current integer carry if the full sum is zero; coprimality is sufficient, including composite p. The update c↦(c/p^d)q^d+a preserves equality. It is correct to stop with nonzero when the divisibility test fails, but this supplies no real sign information, exactly as the author warns.

The height bound |c|≤A is inductive because q/p<1. If a nonzero carry faces a gap larger than its bit length, p^d>|c| and the algorithm can reject without expanding either power. Otherwise all constructed integers have polynomial bit length. Zero carries reset before large gaps. The equality procedure therefore has polynomial bit cost, not just polynomial arithmetic-operation count.

For the positive 2/3 instance, negative and zero exponents are correctly separated first. Any nonempty positive-exponent prefix has an even numerator over an odd power-of-three denominator, so it cannot equal one. Its deficit, when positive, is at least 3^(-R). The proposed large-gap cutoff makes the entire remaining tail strictly smaller than that deficit. The exponent recurrence and its geometric bound are correct. This is fixed-parameter tractability in the number of terms; it is not polynomial when that number varies.

The cancellation family with a vanishing quadratic block really has exponentially small absolute value in its binary exponent length, but its sign is symbolically immediate. The package correctly uses it only against an unqualified raw-separation argument.

## 3. Turn 2: signed clusters and bit bounds

The maintained invariant alpha^v R/q^W is exact. Merging a lower term across gap d gives R_new=R*p^d+a*q^(W+d), as stated. A vanishing processed cluster can be discarded entirely because no earlier nonzero cluster remains outside it. At a cut, |R|≥1 and alpha^d>A*q^W give strict domination over all lower terms, regardless of coefficient signs.

Only gaps below c(B+QW+1) are expanded. The width recurrence, numerator bound |R|≤A*p^W, and fixed-base running-time estimate follow. Sorting and gap arithmetic use binary exponents; they do not cost time proportional to their numerical magnitudes. For q=1 the width grows only linearly in the number of merges and coefficient height. For q>1 the stated dependence is F_alpha(m) times a polynomial in input length. The assertion for m=O(log L) is valid with the base and implied constant fixed. Treating c as constant for a variable rational base near one would be invalid, and the package explicitly does not do that.

## 4. Turn 3: zero-block removal, adaptive precision, and the implementation lower bound

At every ascending gap exceeding B, a globally zero polynomial must have zero carry before the gap, because a nonzero carry of magnitude at most A cannot be divisible by p^d. Thus the fixed large-gap partition is zero exactly when each block is zero. Each block has polynomial width and can be evaluated with polynomially many bits. Removing its exactly vanishing blocks preserves the full value and guarantees a nonzero remainder whenever any block remains. It does not purport to find all possible vanishing subexpressions.

For the largest-power normalization, omitted terms have total absolute value at most A*rho^D, below 2^(-P-2). Evaluating only gaps below D and doubling P gives a certified, terminating algorithm on a nonzero remainder. Stage cost is polynomial in input length plus P. The unknown separation parameter T is explicitly retained; the proof does not convert an instance-dependent bound into a uniform polynomial-time algorithm.

The constructed conservative-algorithm family is internally consistent. Each gap is one below its cut threshold, each processed prefix is positive, and no zero reset occurs. The final expanded width grows as 3^(m-1) and the algorithm actually constructs an integer with order that many bits. Its sparse input length is O(m²). Thus it exhibits exponential work in the term parameter m, and in particular superpolynomial work in that input length for this specific implementation. It is not a hardness result for the sign problem. The adaptive algorithm correctly resolves the same family at P=1 because the true normalized margin exceeds one third and omitted terms are negative.

The q=1 leading-block argument properly removes the rational-denominator difficulty. The next lower block's total contribution is less than one half relative to the leading block's lowest power. This yields the stated polynomial precision bound for integer and reciprocal-integer bases only.

## 5. Turn 4: root conditioning is not rational-point separation

For n≥2 positive exponents, f(x)=sum x^r-1 has exactly one positive root, in (0,1), with derivative at least 1/x at that root. The near-threshold hypothesis correctly places it between one half and three quarters. The lower derivative estimate 5/4 and upper estimate 27n/16 hold on the entire intervening real interval. The stated mean-value comparison is consequently correct.

The complex derivative bound follows by dominating each monomial derivative by the full positive binomial generating series. On the larger disk, the second derivative bound is 1024n. The Taylor remainder on radius 1/(1024n) is at most half the radius, strictly below the linear term. Rouché therefore certifies one root in that disk. This is a valid local complex-isolation result independent of the numerical degree. It does not bound the distance from the fixed rational comparison point.

The reciprocal-integer and signed examples correctly show why an isolated simple root can still lie extraordinarily close to a rational point. They are not misidentified as parity-protected positive-unit 2/3 instances, or as lower bounds for symbolic sign decisions.

The compactification argument for a positive fixed-term gap is valid: append infinite exponents as zero terms; any limiting equality would be a finite sum of at most n positive powers equaling one, which parity excludes. The quantitative pruning estimate gives the displayed doubly exponential reciprocal-gap bound. It does not imply that the actual minimum gap has this size, nor that a stronger separation estimate is necessary for every possible symbolic algorithm.

## 6. Turn 5: sparse canonical forms and their precise limitation

The rewrite q*rho^r=p*rho^(r-1) is exact, and each nontrivial carry decreases total nonnegative coefficient mass. A mass-only termination estimate would indeed be inadequate for binary coefficients. The stronger descending-order bound is sound: between original occupied positions, each outgoing carry contracts by at least the fixed factor p/q, starting below A. Thus each such gap requires only O_rho(log(A+1)) processed positions before the carry dies, unless the next original input position arrives first. There are at most m such intervals, including the final tail. All coefficient heights and the bit lengths of shifted indices remain polynomial. It is crucial that the base is fixed.

Finite digit uniqueness follows from the largest differing exponent after a common shift: reducing the cleared equality modulo q forces a nonzero digit difference of magnitude at most q-1 to be divisible by q. The argument works for composite denominators and signed exponent positions. It establishes uniqueness of the terminating normal form, not a lexical order rule.

Splitting a general integer-coefficient sum into positive and negative parts and normalizing them is a polynomial reduction to numeric comparison of sparse canonical words; subtraction gives the reverse reduction. This is only an order-problem equivalence. The explicit leading-place failure and positive residual t/q obstruction are correct. The latter uses 0<t<p and gcd(p,q)=1, not an assumption that p is prime, and excludes only the specified finite nonnegative-integer power-sum certificate format. It does not exclude rational certificates or other algorithms.

For the original positive unit input, coefficient mass does not increase, so the resulting positive-exponent digit multiplicities are at most two without increasing term count. The remaining order comparison is still not solved.

## 7. Primary literature and attribution boundary

I inspected Lenstra's primary first page visually, including its explicit polynomial bit-time rational-root consequence for sparse polynomials. The package's classical equality credit is appropriate. I also checked the relevant Jindal–Sagraloff theorem statements, whose precision/separation parameters remain visible; Boniface–Deng–Rojas's non-ill-conditioned trinomial corollary and variable evaluation-point setup; and the Akiyama–Frougny–Sakarovitch rational-base introduction and its different digit scaling convention. Sagraloff 2014 was checked at abstract level only, matching the author's access qualification. Its arithmetic-operation bound is correctly distinguished from degree-dependent bit complexity.

These cited sources are context and attribution, not unproved or overextended premises for the package's elementary arguments. No exhaustive literature search or historical novelty certification is implied.

## 8. Independent controls and final disposition

The independent program uses exact rational ground truth for 6,400 signed instances over eight bases, separate implementations of equality, rational-valued clusters and adaptive truncation, canonical normalization tests over 27 reduced bases, and analytic-constant controls. It includes exponent gaps of bit length 4,097 and coefficients of bit length 2,049; those gaps are never expanded. A 200-term conservative-family fixture is resolved adaptively at P=1. These tests check implementation consistency and boundary cases, while the written audit above verifies the universal bounds.

No substantive correction is required. Preserve the source transcription correction, all fixed-parameter and precision-dependent qualifiers, classical credit and explicit lack of a hardness claim. Recommend **unsolved, 5/5**, with the scoped partials reviewed. Both the positive original example and the general rational-coefficient sign task remain unresolved; this review is not a sixth author search turn.
