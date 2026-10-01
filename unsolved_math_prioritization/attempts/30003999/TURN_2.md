# Turn 2: a unified exact gap algorithm and its denominator bottleneck

**Active partial research, 2026-10-01. Author turn 2/5.** No full solution of the variable-term polynomial-time question is claimed. The fixed rational base in the original source matters: it is not an arbitrary rational evaluation point supplied as an additional input.

## 1. Normalization and constants

Use the sign-preserving normalization of Turn 1 to write the target as

    f(α)=sum_(i=0)^(m−1) a_i α^(e_i),
    α=p/q>1 fixed, gcd(p,q)=1,
    a_i∈Z\{0}, 0=e_0<...<e_(m−1).

Let A=sum |a_i| and B=bitlength(A), so A<2^B. Set Q=ceil(log_2 q), an exact integer (Q=0 if q=1). Choose once and for all a positive integer c such that α^c≥2. Such c exists because α>1. These are constants depending on the **fixed** base, except for B. In particular, for α=3/2 one can take c=2 and Q=1.

The following deterministic algorithm gives

    time F_α(m) poly(L),

where L is the binary input length. For q=1 its bound improves to polynomial time with variable m. It therefore recovers the familiar integer and reciprocal-integer cases and identifies exactly where the present proof incurs exponential dependence on the number of terms.

## 2. Descending clusters

Read the terms from highest exponent downwards. Maintain one current cluster, with highest exponent u, lowest exponent v and width W=u−v, in the form

    cluster value = α^v R/q^W,    R∈Z.

Initially R is the leading coefficient and W=0. Suppose the next lower term is a α^e, with gap d=v−e>0.

1. If R=0, the entire processed cluster vanishes exactly. Discard it and restart at the next term: R=a, W=0, v=e
2. If R≠0 and

       d ≥ c(B+QW+1),                                  (1)

   return sign(R); all remaining terms together are too small to change it
3. Otherwise merge the next term exactly, using

       R_new = R p^d + a q^(W+d),
       W_new = W+d, v_new=e                            (2)

When there are no remaining terms, return sign(R). If the normalized polynomial was empty, return zero.

No power with the magnitude of an unaccepted binary exponent gap is ever expanded. In particular, an exact zero cluster can be discarded before crossing an arbitrarily large gap.

## 3. Correctness of a gap cut

If R≠0, then |R|≥1. The current cluster consequently has absolute value at least α^v q^(−W). Every remaining exponent is at most e, so the absolute value of their total is at most A α^e. Under (1),

    α^d ≥ 2^(B+QW+1) > A q^W,

because q≤2^Q and A<2^B. Thus the cluster strictly dominates the sum of all remaining terms in absolute value. Its sign is sign(R), since α^v/q^W is positive. This proves the early-return rule. Formula (2) is the exact common-denominator update, and a zero cluster contributes nothing. Induction proves the full algorithm.

This proof does not confuse a modular nonzero test with an order test. The order certificate is the explicit real absolute-value inequality at the gap cut.

## 4. Bit complexity

Only a failed cut leads to expansion, and then

    d < c(B+QW+1),
    W_new < (1+cQ)W+c(B+1).                            (3)

Every restart reduces W to zero. With at most m−1 merges, the maximal expanded width is bounded by

    W < c(B+1) sum_(j=0)^(m−2) (1+cQ)^j.                (4)

Moreover |R|≤A p^W: write the current numerator as a sum of terms a_i p^s q^(W−s), with 0≤s≤W, and use q≤p. All exact integer arithmetic therefore uses O(B+W log p) bits. The original exponents are only sorted, subtracted and compared in binary; a very large gap is rejected before its power is formed.

For q>1, put M=1+cQ. Since the base is fixed, a conservative grade-school bound from (4) is

    M^(2m) poly(L).

Factors polynomial in m and log W are absorbed into poly(L) and the parameter function. Thus the problem is fixed-parameter tractable in the number of distinct exponents. For each fixed m it is polynomial in the full input bit length. It is also polynomial on families with m=O(log L), with the constant in that condition fixed.

For q=1, Q=0 and (4) instead gives W<c(B+1)(m−1), hence polynomial bit complexity for arbitrary m. Reciprocating a reciprocal-integer base reduces to this same case. This is a reconstruction of the classical easy-base phenomenon stated by Olver and treated in the sparse-polynomial literature, not a novelty claim.

For the original base 2/3, normalization uses 3/2. Here M=3, so the conservative general signed-coefficient bound is 9^m poly(L). Turn 1's positive-unit-coefficient algorithm is a specialized version with an especially simple prefix-deficit argument.

## 5. What the analysis does not prove

The appearance of M^m in this upper bound is **not** a lower bound for the problem. It is only the worst recurrence permitted by the rational-denominator estimate |R/q^W|≥q^(−W). Actual clusters can be much farther from zero, and using their exact magnitude can lead to earlier cuts. No family forcing exponential work in every correct algorithm is provided.

Nor may c be silently treated as an absolute constant if α is an input rational close to one. The fixed-base hypothesis is essential to the stated parameter bound. This is why the polynomial result for a fixed number of terms does not resolve the more general variable-rational-point trinomial problem discussed by Boniface–Deng–Rojas.

An attempted improvement was to remove exact zero blocks using the bounded-carry equality test, then hope that all remaining clusters have a polynomial absolute-separation bound. Exact zero removal is valid and is used by step 1. However, it does not by itself supply that separation bound for a nonzero cluster. Replacing the factor QW in (1) by a polynomial in the input coefficient height and number of terms would require a new argument. The present derivation cannot make that replacement.

Thus this turn supplies a complete exact algorithm with a parameterized bound, but the original demand for polynomial bit complexity when m varies remains open in the attempt. Next routes should target nonzero-cluster separation or a different compressed order representation, rather than count this FPT theorem as full resolution.
