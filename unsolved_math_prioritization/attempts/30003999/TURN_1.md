# Turn 1: exact equality and a positive-sum parameter reduction

**30003999 / OWR-16633-016. Partial research checkpoint, 2026-10-01.** The original polynomial-time sign question is still open in this attempt. One substantive author turn, of at most five if no complete resolution is obtained. The results below are elementary reductions, with no novelty claim.

## 1. Restored problem and input model

Olver's [original question](https://ems.press/content/serial-article-files/46772), printed p. 3015, asks whether

    sum_i (2/3)^(r_i) > 1

is decidable in time polynomial in the binary encoding of the signed integers r_i. The extracted record's 2^(r_i/3) is a different expression. The same source asks for the sign of sum_i β_i α^(r_i), with a **fixed rational** α and rational input β_i. This turn studies that original rational-base formulation. Bit complexity, including coefficient numerator and denominator lengths, is the target; a polynomial number of unit-cost operations on exponentially long integers would not suffice.

Take input size L to include n, the signs and binary lengths of r_i, and the binary lengths of the numerators and positive denominators of β_i. Zero powers have a nonzero encoding cost. α=0 with a negative exponent is undefined and is excluded; any chosen conventional 0^0 case is elementary. α=±1 is also elementary. For negative nonzero α, absorb (−1)^(r_i) into β_i. If 0<|α|<1, replace the base by its reciprocal and negate every exponent. We may consequently normalize the substantive general case to

    α=p/q>1,  p,q positive coprime integers.

Multiplying all coefficients by their common positive denominator, sorting and collecting equal exponents, then subtracting the least exponent reduces the sum's sign to the sign of

    f(p/q),  f(x)=sum_(i=0)^(m−1) a_i x^(e_i),
    0=e_0<e_1<...<e_(m−1),  a_i∈Z\{0}.

These operations have polynomial bit cost. The common denominator can be a product rather than an LCM; its bit length is at most the sum of input denominator lengths. Put A=sum |a_i|. Its logarithm is polynomially bounded by L. The exponent magnitudes themselves need not be polynomial in L.

## 2. Polynomial-time zero test by integer carries

Equality is already covered by Lenstra's polynomial-time rational-root theorem for lacunary polynomials, [1999 primary paper](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1999a/art.pdf). The following direct proof isolates that easy part without using it as a sign oracle.

Initialize c=a_0. For i=1,...,m−1 let d=e_i−e_(i−1).

- If c=0, set c=a_i and continue without evaluating either large power
- Otherwise, test whether p^d divides c. If not, return **nonzero**
- If it does, set c=(c/p^d)q^d+a_i
- At the end, return **zero** if and only if c=0

### Correctness

At each successful step, the remaining expression, after division by the positive factor α^(e_(i−1)), has the form

    c + a_i α^d + further terms with exponents at least d.

After clearing a power of q, every term except the c term is divisible by p^d. Since p and q are coprime, equality to zero therefore requires p^d|c. If divisibility holds, factoring out α^d yields exactly the stated integer update and preserves equality. Induction proves the result. The argument works for composite p: prime factorization is unnecessary.

### Bit cost

At every successful update,

    |c_new| ≤ |c| (q/p)^d + |a_i| ≤ |c|+|a_i| ≤ A.

For nonzero c, d>bitlength(|c|) guarantees p^d>|c|, so divisibility fails without constructing the power. Otherwise d=O(log A), and p^d and q^d have polynomially many bits; exact division and multiplication are polynomial-time operations. For a fixed base their bit lengths are O(log A), and even an explicitly input base would only introduce a polynomial factor in its bit length. Thus equality is decidable in polynomial bit complexity.

**Limitation:** early divisibility failure determines only that the sum is nonzero. It does not determine its real sign. Modular information is not an order comparison. This lemma does not solve the original sign problem.

## 3. Equality and pruning for the positive original example

For the unit-coefficient base 2/3, a negative exponent makes the sum exceed one immediately. A zero exponent also makes it exceed one unless it is the only term, which gives equality. The empty sum is below one. We may therefore assume n≥2 and all r_i≥1, sorted increasingly.

For any nonempty prefix ending at R, its sum has denominator 3^R and an even numerator. Hence it cannot equal one. If the prefix is below one, its deficit is at least 3^(−R). For the empty prefix use R=0 and deficit one.

Let k=ceil(log_2 n), computed as the bit length of n−1. Suppose the next exponent e satisfies

    e ≥ 3(R+k).                                      (1)

Every remaining term is at most (2/3)^e, so the entire tail is at most

    n (2/3)^e ≤ n (8/27)^(R+k)
              = 3^(−R) (8/9)^R n (8/27)^k
              < 3^(−R).

The strict inequality follows from k≥1, n≤2^k and 8/27<1/2. Thus condition (1) certifies that a below-one prefix cannot be brought up to one by the remaining tail. Return **below one**, without expanding those exponents.

If (1) fails, evaluate the next term and updated prefix exactly. If the prefix exceeds one, return **above one**. Otherwise continue. The parity argument excludes equality at every nonempty positive-exponent prefix.

### Parameterized complexity

Every exponent actually expanded by this algorithm satisfies

    R_j < 3(R_(j−1)+k),  R_0=0,
    R_j < (3k/2)(3^j−1).

Thus all expanded integers have O(3^n log n) bits, independently of the largest exponent supplied in binary. Sorting and comparing the original exponents has polynomial cost in L. Grade-school integer arithmetic gives a conservative running-time bound

    poly(L) + 9^n poly(n).

This is fixed-parameter tractability in the number of terms, with an explicit exponent cap for all non-pruned work. It is **not polynomial in total input length when n varies**, as the original question allows. No assertion is made that the exponential cap is optimal or that instances attain it.

## 4. Why raw precision bounds do not close the general case

The sparse family

    f_N(x)=(3x−2)^2−x^N,  N>2,

has constant-size coefficients and binary input length O(log N), but

    f_N(2/3)=−(2/3)^N.

Absolute-error interval evaluation that ignores exact cancellation may therefore require Ω(N) bits just to separate the value from zero. This is **not a complexity lower bound**: recognizing the exact vanishing quadratic block gives the sign immediately. It invalidates the naive argument that a universal polynomial absolute-separation bound follows merely from sparse input, while illustrating why structural cancellation must be handled first.

The zero algorithm above handles equality, but does not yet turn such structural information into a general polynomial-time real sign algorithm. A proposed gap-splitting strategy based only on denominator bounds leads to a prefix-width recurrence of the same exponential type as Section 3. No polynomial gap bound is proved here.

## 5. Literature boundary and next route

The exact target's general rational sign task is closely related to sparse polynomial sign evaluation. Boniface–Deng–Rojas, [arXiv:2202.06115v2](https://arxiv.org/abs/2202.06115v2), 2025, discuss the rational-point trinomial sign problem and prove a positive result away from their ill-conditioned family (Corollary 1.4). That is not a worst-case result for arbitrary input terms at the fixed base 2/3, nor does the more general variable-rational-point question immediately prove hardness of the fixed-base case.

Jindal–Sagraloff, [arXiv:1704.06979](https://arxiv.org/abs/1704.06979), Theorems 3–4, give sparse root covering with explicit precision dependence and isolation with separation dependence. Those parameters must not be suppressed. The earlier sparse-root result [arXiv:1401.6011](https://arxiv.org/abs/1401.6011) has a polynomial number of rational arithmetic operations but bit complexity linear in the numerical degree, up to other factors and logarithms. None is used here as a polynomial-bit-complexity solution of Olver's question.

Next substantive route: examine whether exact zero-block removal plus an order-preserving compressed rational-base representation yields a polynomial sign algorithm, or derive a sharper structural obstruction. The general sign task and the original positive-unit-coefficient task both remain unresolved in this attempt. No final unsolved disposition is made before the remaining author turns.
