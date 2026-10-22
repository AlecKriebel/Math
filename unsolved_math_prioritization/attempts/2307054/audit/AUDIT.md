# Adversarial audit: Rippon's iterated-exponential coefficients

## Verdict

**PASS for the explicitly stated partial theorem. The universal coefficient question remains unresolved.**

No substantive mathematical, indexing, arithmetic, source-transcription, or finite-to-infinite coverage defect was found. No correction to the frozen package is required. This verdict does not establish novelty, priority, or the current literature's global status.

The accepted partial coverage is the union of:

1. Every iterate n >= 1 at degrees 0 <= k <= 200.
2. Every iterate n >= 1 at offsets 0 <= k - n <= 100.
3. Every degree k >= 0 for iterates 1 <= n <= 4.
4. The vanishing coefficients k < n.

The exact complement of this coverage is n >= 5, k >= 201, k - n >= 101. The package does not solve that region. Its five documented approaches must not be counted as five universal proofs or as a resolution of the problem.

## Scope and integrity

Audit date: 2026-10-03. All six entries of the frozen `public/SHA256SUMS` verified both before and after the review. The manifest's SHA-256 is:

`bc440603567a5e83bcfb91466bb3196e741bb5d57cabca2726585174d6f47f6d`

The reviewed public files are `README.md`, `SOURCE_GATE.md`, `ATTEMPTS.md`, `proof.md`, `verify.py`, and `verification_output.json`. Every mathematical argument and all verifier code were read. The submitted verifier ran successfully with normal Python assertions enabled and reproduced `verification_output.json` byte-for-byte. No frozen input was modified. The audit is a local, additive deliverable; it makes no publication or repository change.

The exact primary question and adjacent update were independently read in text and in the rendered PDF page. See `PRIMARY_SOURCE_CHECK.md`. The recurrence agrees with the original problem, and the reported missing exponent in t/2! is actually present in the printed source.

## 1. Integer recurrence, valuation, and finite coverage

Let A_(n,k) = k! [t^k]F_n and E = exp(t F_n). The EGF coefficient of degree j in t F_n is j A_(n,j-1). Thus differentiating E and multiplying exponential generating functions gives exactly

B_k = sum over 1 <= j <= k of binom(k-1,j-1) j A_(n,j-1) B_(k-j), with B_0 = 1.

Replacing the output constant coefficient by zero correctly subtracts 1 only after the exponential recurrence has used B_0 = 1. The implementation does this at the correct time. All arithmetic uses arbitrary-precision integers or exact rational numbers.

Starting with F_0 = -1, induction gives F_n = -t^n + O(t^(n+1)). In the step to F_(n+1), the linear exponential term has order n+1, whereas every nonlinear term has order at least 2(n+1) > n+1. This also works at n = 0. Consequently, when computing row n in the code, the first possible nonzero input to its exponential is at degree n; the skipped j < n and k < n entries are genuinely zero. No circular estimate is hidden in this optimization.

The recurrence is degree-triangular, so coefficients above 200 cannot affect those through 200. The 200 rows and 201 degrees give exactly 40,200 tested pairs; many are zero, but the count is accurate. Every n > 200 contributes only zeros in this degree range, proving the asserted all-iterate extension. The reported maximum is expressly confined to the finite rectangle.

## 2. Stabilization and its boundary

Substitution of F_n = -t^n H_n gives

H_(n+1) = H_n + sum over m >= 2 of (-1)^(m+1) t^((m-1)(n+1)) H_n^m / m!.

Thus H_(n+1) - H_n has order at least n+1. For offset j, the transition from n to n+1 is unchanged whenever n+1 > j, equivalently n >= j. Therefore the coefficient is constant from H_j onward, not merely from H_(j+1), and there is no off-by-one error. Offset zero is constant starting at H_0.

The finite bridge covers all transient cases: if n <= 100 and j <= 100 then n+j <= 200. If n > 100, all these offsets agree with row 100 because each intervening transition has order at least 101. The possible equality j = 100 is included. The independent checker also confirms 10,099 adjacent stability comparisons within the available rectangle. As a boundary sanity check, the offset-2 coefficients at n = 1 and n = 2 differ: -1/6 versus 1/3. Stabilization is not improperly claimed before its valid start.

The formal limit exists coefficientwise, but gives no estimate at all offsets and does not control transients n < j. The package correctly retains both limitations.

## 3. Analytic tails and exact constants

Every fixed iterate is entire by composition. Cauchy's coefficient estimate is therefore applicable at each positive radius used, and |exp(z)-1| <= exp(|z|)-1 follows directly from the absolutely convergent exponential series.

The bound e < 87/32 is valid: terms through degree 3 sum to 8/3; the remaining tail is strictly less than (1/24)/(1-1/5) = 5/96 because later successive ratios decrease below 1/5. Also exp(x) <= 1/(1-x) for 0 <= x < 1 follows termwise, so no floating-point approximation is needed.

For radius 11/10, the submitted rational inequalities yield M_1 < 21/10, M_2 < 10, and M_3 < 3^11. The first two maxima also lie below 3^11. The exact inequality (11/10)^128 > 3^11 then covers every k >= 128 for n = 1,2,3, because the radius exceeds 1. All smaller degrees are in the exact rectangle.

For radius 23/20, the bounds yield M_1 < 11/5 and M_2 < 12. The split exp(253/100) = e^2 exp(1/2) exp(3/100) is correct, and exp(1/2) < 5/3 follows by squaring positive quantities and using e < 11/4 < 25/9. Next M_3 < exp(69/5) < (11/4)^14. These inequalities are checked independently.

For r = 21/20 and q = 21/23, Cauchy's bound at the larger radius controls each coefficient in the absolute tail. Summing from degree 201 gives exactly (11/4)^14 q^201/(1-q), with the correct tail start and geometric denominator. The degree-200 polynomial uses absolute values, so its addition to this tail dominates the full weighted absolute coefficient sum and hence the supremum of |F_3| on |t| = r. There is no assumption of cancellation at this step.

The independent exact replay gives rational enclosures corresponding to:

- Polynomial contribution: strictly between 4.434445700943 and 4.434445700944.
- Tail bound: strictly between 0.186268216371 and 0.186268216372.
- Their sum: strictly between 4.620713917315 and 4.620713917316.

These decimal strings describe exact rational endpoints, not floating-point evidence. They confirm the claimed interval (4.620, 4.621), and in particular the required upper bound 5. Hence M_4(21/20) < exp(21/4) < 3^6. The exact inequality (21/20)^136 > 3^6 proves the fourth-iterate tail for all k >= 136; all lower degrees were checked. Both infinite-tail arguments are complete for their asserted ranges.

## 4. Failed approaches and signed profiles

The positive-start iteration is a valid coefficientwise majorant, but its coefficient at (n,k) = (3,6) is 25/24 while the signed coefficient is 1/24. Thus its failure cannot be mistaken for a counterexample to the original problem.

For the small-disc approach, q = exp(r)-1 is greater than r for r > 0. Because 0 < r <= log(2) < 1, the proposed Cauchy bound q^n r^(-k) is greater than 1 throughout k >= n >= 1. The stated obstruction is correct and does not rule out other analytic estimates.

The level-profile expression has the correct sign and factorial divisor. Each vertex above the last level must have a nonempty collection of children. For fixed positive nondecreasing level sizes, surjective parent maps give the Stirling factors. Independent labeling and division by level factorials leave the final 1/l_n! factor. The first level introduces S(l_1,1) = 1, so there is no missing root factor. The elementary exponential expansion provides an equivalent formal derivation.

An independent enumeration of all 215,307 nonempty nondecreasing profiles with total size at most 40 matches all 1,681 coefficients for 0 <= n,k <= 40. The specific single-profile value S(6,3) S(9,6) S(12,9)/12! = 2835/256 is also exact. This supports the formula and the stated obstruction to termwise bounds; it supplies no uniform cancellation theorem.

## 5. Independent computation

`independent_verify.py` does not import or execute the submitted verifier. It computes exp(g)-1 as the sum of divided powers g^m/m! using EGF polynomial convolution, rather than the submitted exponential derivative recurrence. Each division by m has its zero remainder checked. The algorithm discovers actual nonzero supports and terminates a power sequence only when its truncated product vanishes. It performs 220,698 checked integer divisions and uses no floating-point arithmetic.

It independently validates every rectangle inequality and finds the unique off-leading maximum 2663/4480 at (6,13), with negative coefficient. It checks the analytic rational inequalities and weighted norm, the profile formula, the majorant example, and the stability comparisons.

The companion `replay_comparison.py` separately runs the package verifier, directly compares every entry of the full 201-by-201 integer coefficient matrix against a fresh independent calculation, and checks the canonical matrix SHA-256 against the independently saved output. All 40,401 entries, including the initial row, agree. Matrix digest:

`0a8789537983c65c4cd6f452fd9eaeee60468d1ba0531a031a24cae17ed29bb5`

## Reproduction

From the audit directory, run:

```sh
python3 independent_verify.py > independent_output.json
python3 replay_comparison.py > matrix_comparison.json
sha256sum -c SHA256SUMS
(cd ../public && sha256sum -c SHA256SUMS)
```

`package_replay.json` is generated by the comparison script and equals the frozen expected output byte-for-byte. The audit manifest covers the public audit deliverables, excluding itself. The submitted package's separate manifest remains unchanged.

## Limits

This is a mathematical and reproducibility audit of bounded claims and their proved infinite extensions. It does not independently authenticate the historical repository-search account or establish absence of later literature. All five documented approaches are substantive descriptions with correctly limited outcomes. Their number does not change the verdict: **partial results accepted; universal problem unresolved in this work**.
