# Turn 3: adaptive truncation, exact zero blocks, and an actual failure family

**Active partial research, author turn 3/5, 2026-10-01.** The requested polynomial dependence on the variable number of terms is still unproved. This turn studies a different computational route: approximate a bounded normalized sum with exact error bars, while eliminating structurally zero high-degree blocks first.

## 1. A polynomial-time large-gap zero decomposition

Normalize as in the previous turns to a fixed α=p/q>1 and an integer sparse polynomial f. Let A be the coefficient l1 norm and B=bitlength(A). Partition its ascending exponent list into blocks, cutting whenever consecutive exponents differ by more than B. Each block has width at most (m−1)B, so its value after factoring out its lowest power of α can be evaluated exactly with polynomially many bits.

**Lemma. f(α)=0 if and only if every block vanishes at α.**

To see the nontrivial direction, run the bounded-carry zero argument from Turn 1. For a globally zero expression every divisibility test must succeed. At a gap d>B, its current integer carry c satisfies |c|≤A<2^B<p^d. Hence p^d|c forces c=0 before crossing that gap. The already processed blocks therefore contribute zero, and induction gives the assertion for each block. The converse is immediate.

Thus all exactly zero blocks in this fixed partition can be removed in polynomial bit time. If no terms remain, the answer is zero; otherwise the remaining sum is nonzero. This is another direct realization of a classical rational-root/equality subproblem, not a new solution of the sign problem. It removes exactly the blocks in the stated partition, not every conceivable vanishing subexpression.

## 2. Certified truncation after scaling the largest power

For the remaining polynomial, let E be its largest exponent and put ρ=q/p∈(0,1). Its sign is the sign of

    F = α^(−E) f(α) = sum_i a_i ρ^(E−e_i).

The common factor removed is positive. Recompute A and B for the retained coefficients. Choose a fixed c with ρ^c≤1/2. For a requested precision parameter P≥1, set

    D=c(P+B+2).

Retain only terms whose gap E−e_i is less than D, and evaluate their sum S exactly. The omitted terms have total absolute value at most

    epsilon = A ρ^D < 2^(−P−2).

Therefore F lies in [S−epsilon,S+epsilon]. If this interval is strictly positive or strictly negative, return that sign. Otherwise double P and repeat. All powers expanded at that stage have exponent at most D, so each stage uses poly(L+P) bit operations. The exponent gaps are only compared in binary before deciding which ones to expand.

Since exact zero blocks have already been dealt with, F≠0. Hence the adaptive algorithm terminates. Its bit cost is polynomial in L plus the normalized separation parameter

    T = max(1, ceil(log_2(A/|F|))).

This statement is an **instance-dependent** bound. No polynomial upper bound on T in terms of the input length is established for a general noninteger rational base. Defining T does not solve the original complexity question.

## 3. Exact cancellation defeats raw normalized interval evaluation

For α=3/2 and a huge binary exponent E, consider

    f_E(x)=x^E(2x−3)^2−1
          =4x^(E+2)−12x^(E+1)+9x^E−1.

Its value at α is −1, but its raw largest-power normalization is

    α^(−E−2) f_E(α)=−α^(−E−2).

A truncation method that does not recognize the zero leading block sees a zero retained sum until it reaches the remote constant term. The block decomposition above immediately deletes the three-term zero block and leaves −1. This is an exact structural improvement; it is not a complexity lower bound.

For the original positive unit-coefficient example with every r_i≥1, there is no comparable exactly zero block involving the −1 threshold: the common-denominator numerator of a positive prefix is even and cannot equal the odd denominator. Thus this cancellation preprocessing alone does not resolve the most important original subcase.

## 4. A genuine exponential-work family for Turn 2's conservative algorithm

The exponential recurrence in Turn 2 is not merely a loose formal possibility for that particular implementation. Let m≥3, B=bitlength(m), and define

    W_0=0,
    d_j=2(B+W_(j−1)+1)−1,
    W_j=W_(j−1)+d_j=3W_(j−1)+2B+1,

for 1≤j≤m−1. Set E=W_(m−1), choose descending exponents e_j=E−W_j, and take coefficients a_0=1 and a_j=−1 for j≥1. All exponents have O(m+log B) bits, so the sparse input has O(m²) bits.

At α=3/2, the first gap is d_1=2B+1. The sum of all negative terms, divided by the leading term, is at most

    m α^(−d_1) < (2/3)(8/9)^B < 2/3.

Thus the polynomial is positive with normalized margin greater than 1/3, and every processed prefix is positive. There are no zero-cluster restarts. Yet each d_j is exactly one less than the conservative cut threshold in Turn 2 (where c=2 and Q=1), so that algorithm merges every term. Its final expanded width is

    W_(m−1)=((2B+1)/2)(3^(m−1)−1).

Its final numerator has at least α^E q^E/3=p^E/3 in magnitude, so it genuinely constructs exponentially many bits in m. This is a lower bound only for the specified conservative implementation, not for the mathematical sign problem.

The adaptive truncation algorithm resolves this family already at P=1: the full normalized value exceeds 1/3, and epsilon<1/8. Omitting negative tail terms only increases the retained sum, so the interval is positive. The test program checks this for families with hundreds of terms and enormous binary exponents without expanding those exponents.

## 5. Why integer bases avoid the remaining denominator difficulty

For q=1, every nonzero leading block, after factoring its lowest exponent, has nonzero integer value and hence absolute value at least one. The next lower block is separated by a gap greater than B. Its entire remaining tail is at most A α^(−gap)<1/2 relative to that lowest power, since α is an integer at least two. Thus the leading nonzero block determines the sign.

Its width is at most (m−1)B, and so its largest-power-normalized margin is at least α^(−(m−1)B)/2. This yields a polynomial precision bound and recovers the classical polynomial integer-base sign algorithm. For q>1 the corresponding leading-block lower bound has the extra denominator q^width, which prevents this same argument from closing.

## 6. Remaining issue and next route

The current work now separates three phenomena:

- Equality and exact zero-block removal are polynomial-time, credited classical territory
- Conservative denominator-based expansion can be exponentially wasteful even on easy sign instances
- Adaptive truncation removes that waste but still requires an uncontrolled normalized nonzero-separation parameter in the general rational-base case

The original positive (2/3)^r comparison is not solved by any of these facts. A polynomial nonzero-separation theorem after suitable structural simplification would be sufficient for this route, but has not been proved. Nor is such a separation theorem necessary for every conceivable exact symbolic algorithm. The next turn should investigate that number-theoretic/positive-sum structure rather than relabeling a precision-dependent algorithm as polynomial-time.
