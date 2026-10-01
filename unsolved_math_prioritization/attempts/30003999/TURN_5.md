# Turn 5: sparse rational-base normalization does not yet provide order

**Final substantive author turn, 5/5, 2026-10-01. Proposed overall disposition: unsolved, with the partial results below awaiting independent review.** No polynomial-time algorithm or hardness theorem for the full original problem has been obtained.

## 1. A canonical nonnegative carry form

Let ρ=p/q with fixed coprime integers 1≤p<q. Consider a finite nonnegative integer combination

    U=sum_r a_r ρ^r,  a_r∈Z_(≥0), r∈Z,

given sparsely by binary exponents and binary coefficients. Put A=sum a_r and let m be the number of initially occupied exponents. The following rewriting preserves U:

    a_r=q c+d, 0≤d<q:
    replace a_r by d and add p c to a_(r−1).           (1)

Indeed qρ^r=pρ^(r−1). Each nontrivial carry reduces the total coefficient mass by (q−p)c, so the process terminates. Process occupied positions in decreasing exponent order and skip empty gaps. The terminal digits belong to {0,...,q−1}.

### Sparse bit complexity

Termination by coefficient mass alone would only give a bound proportional to the numerical A and would be inadequate for binary coefficients. A stronger bound follows from contraction across an interval containing no original input coefficient. If the incoming coefficient is t, the next carry is at most (p/q)t. Since all intermediate coefficients are at most A, after O_ρ(log(A+1)) consecutive positions that carry is below q and stops. There are at most m such gaps, including the tail below the least original exponent.

Thus at most O_ρ(m log(A+1)) positions are processed and emitted, regardless of the binary lengths of the empty gaps. Every coefficient has O(log(A+1)) bits. Each new index differs from an original index by at most this polynomial number of unit shifts. A sparse ordered map or priority queue therefore computes the finite digit representation in polynomial bit time for each fixed ρ. For unit-coefficient input the simpler mass argument already bounds the number of elementary carries by n.

### Uniqueness

Suppose two finite digit arrays with digits in {0,...,q−1} represented the same number. Subtract them, shift the least exponent to zero, and let R be the largest exponent at which the difference c_R is nonzero. After multiplying by q^R, reduction modulo q gives

    c_R p^R = 0 mod q.

Coprimality implies q divides c_R. But 0<|c_R|≤q−1, a contradiction. Therefore the finite digit representation is unique. This proves independence of the terminating carry order as well.

These facts belong to the general setting of classical rational-base numeration. Related integer-expansion and addition methods are developed by Akiyama–Frougny–Sakarovitch, [author manuscript](https://www.math.tsukuba.ac.jp/~akiyama/papers/3half_H65fullTH-060406.pdf), later *Israel Journal of Mathematics* 168 (2008), 53–91. The argument here states its own scaling/index convention and sparse binary-gap bound explicitly. No novelty claim is made.

## 2. A precise reformulation of the general sign task

For any fixed nonzero rational base other than ±1, absorb a negative-base parity into the coefficients and invert the base/exponents if necessary to arrange 0<ρ<1. Clear rational coefficient denominators by one positive common denominator and split the resulting integer coefficients into positive and negative parts:

    f(ρ)=U−V.

Normalize U and V separately by (1). Their sparse finite digit words have polynomial size and can be constructed in polynomial bit time. Hence the fixed-rational-base sign problem is polynomial-time reducible to **numeric comparison of two sparse canonical rational-base digit words**. The converse is immediate by subtracting the two digit lists. Equality is just identity of the normalized lists.

This is an equivalence of exact order problems, not an order algorithm. A canonical equality representation need not place numeric values in a simple lexical order.

## 3. Two exact failures of the naive order-certificate route

### Leading digits do not determine the real order

At ρ=2/3, the canonical word consisting of digit 1 at exponent zero represents 1. The canonical word consisting of digit 2 at exponent one represents 4/3. The first has the larger-place leading digit, but the second is numerically larger. Comparing the other end of the words also fails in general: a digit 1 at exponent one represents less than a digit 2 at exponent zero.

For every p>1, take d=ceil(q/p). Since p and q are coprime, 1≤d≤q−1 and

    dρ>1.

Both dρ and 1 are already canonical finite words. This shows why the usual integer-base leading-digit test is invalid here. It does not prove that every finite-state or compressed-word comparison method must fail.

### A positive difference need not have a finite nonnegative-power certificate

For the same d, write

    dρ−1=(dp−q)/q=t/q,   1≤t≤p−1.

This number lies strictly between zero and one, but it cannot be a finite nonnegative integer combination of powers ρ^r with integer exponents. Any nonzero term with r≤0 would already be at least one. If all r≥1 and R is the greatest exponent, clearing q^R makes the combination's numerator divisible by p. The numerator of t/q becomes t q^(R−1), which is not divisible by p. Contradiction.

For ρ=2/3 this is the concrete positive residual 2ρ−1=1/3. Thus exact integer coefficient-carry rewriting cannot always certify positivity by converting the signed difference into a finite expression with only nonnegative integer coefficients. This obstruction concerns that specific certificate format; it is not a lower bound for sign computation or a prohibition on other symbolic/rational certificates.

## 4. What normalization achieves for the original positive problem

Apply the carry algorithm to sum_i (2/3)^(r_i). If a terminal digit occurs at a negative exponent, the sum exceeds one. If there is a digit at exponent zero, the sum is at least one, with equality only for the single digit 1 there and no other terms. Otherwise all exponents remain positive and each has multiplicity at most two.

Consequently the original comparison reduces in polynomial time to the same question with **multiplicity at most two**. The term count does not increase for the original unit input. The example 2ρ>1 shows why this normalized positive case is still not decided by the absence of a constant digit. No polynomial comparison algorithm for its remaining sparse digit word has been proved here.

## 5. Five-turn outcome

The attempt has established and checked the following partial tools:

1. Correct original source/input model; polynomial exact equality testing; positive-sum pruning with an explicit fixed-parameter exponent cap
2. A complete exact signed-coefficient gap algorithm for each fixed rational base, with fixed-parameter rather than polynomial dependence on the variable term count; polynomial integer/reciprocal-integer branches
3. Polynomial large-gap zero-block deletion and a certified adaptive truncation algorithm with an uncontrolled separation parameter; an actual exponential-work family for one conservative implementation, handled immediately by the adaptive method
4. Degree-independent local isolation of the original positive sum's unique near-threshold root, plus a fixed-term gap bound that remains too weak for polynomial bit complexity
5. Polynomial sparse rational-base carry normalization, exact equality normal forms, an order-problem equivalence and explicit failures of lexical/nonnegative-integer-certificate shortcuts

The missing result is still a polynomial bit-time order decision for variable term count at ρ=2/3, and for the source's more general fixed rational base with rational input coefficients. Neither a polynomial nonzero-separation bound nor a different polynomial symbolic order certificate was obtained. No hardness classification follows from the failed routes. The positive original subcase and the general bundle both remain unresolved in this attempt.

**Proposed final status: unsolved, 5/5.** No sixth author research turn is taken. The frozen partial package must undergo separate adversarial review before any partial-result PR. Classical inputs, the transcription correction, bit-complexity parameters and all gaps must remain explicit; there is no novelty or priority claim.
