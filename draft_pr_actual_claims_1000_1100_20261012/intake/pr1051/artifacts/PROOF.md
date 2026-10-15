# Hall coefficient-sign question: approach 1

## Status

**Partial result; the general arbitrary-complex-root problem remains unresolved in this approach.**

For positive real exponents beta_1,...,beta_n, put B = sum beta_j and

f(z) = product_j (1 - zeta_j z)^(beta_j) = 1 + sum_{k>=1} a_k z^k,

using the local branches normalized to 1 at zero. Assume all a_k are real.

This report proves:

1. If all zeta_j are real, some a_k <= 0 with k <= ceil(B) + n.
2. The same bound holds if every nonreal zeta_j lies in the closed left half-plane. Positive real zeta_j are allowed and are eliminated by a positivity-preserving operation. Repeated roots and zero zeta_j are allowed throughout.
3. For n<=2, the bound ceil(B)+n holds for every admissible complex parameter tuple. For (beta_1,beta_2)=(3/5,3/5), the sharp universal value is N=4.
4. For arbitrary complex zeta_j and rational beta_j, if q is a common positive denominator, the elementary bound N <= q B + 1 holds.
5. Two tempting stronger bounds are false. The conjectural bound 1 + sum ceil(beta_j) fails already for two negative real zeta_j. The bound ceil(B) + n fails for arbitrary complex zeta_j.

The bound is sharp even in the full complex-parameter problem for the exponent tuple (3/5,3/5). No global sharpness claim is made. No finite explicit exponent-only bound for arbitrary positive irrational exponent tuples is proved here.

## 1. Exact source and scope

The target is R. Hall's Problem 7.34 in W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, printed p.170 / PDF p.171. The source asks for a sharp or good exponent-dependent uniform bound. The minimum must be nonpositive, rather than strictly negative.

The source's explanatory paragraph has an incorrect integer/noninteger index and a missing z in one multiplier; neither defect is used to create a counterexample. Equal zeta_j must be merged when identifying genuine branch singularities. The present argument uses the coherent main statement.

The integral-exponent benchmark N = B + 1 is valid and sharp: the function is a polynomial of degree at most B, and choosing all zeta_j = -1 gives (1+z)^B with positive coefficients through degree B.

This is target 2307034 / AMR-022-7034, not the distinct unweighted pure-power-sum question 2307004 / Problem 7.4 associated with PR 659. No proof or experiment from that PR is used here.

## 2. Positive-polynomial-factor lemma

**Lemma.** Let P_1,...,P_s be nonconstant real polynomials with nonnegative coefficients and constant term 1. Write d_l = deg P_l, let gamma_l > 0, and put

F(z) = product_l P_l(z)^(gamma_l) = sum_{k>=0} c_k z^k,

with the normalized local branches and c_0=1. Define

d = sum_l d_l,  T = sum_l gamma_l d_l.

Then at least one of c_1,...,c_N is nonpositive for N = ceil(T) + d.

**Proof.** Write Q = product_l P_l = sum_{i=0}^d q_i z^i, and

R = sum_l gamma_l P_l' product_{h != l} P_h = sum_{i=1}^d r_{i-1} z^(i-1).

Then Q F' = R F and q_0=1. Expanding the products coefficientwise gives

0 <= r_{i-1} <= T q_i  for 1 <= i <= d.

Indeed, each monomial choice in the expansion of q_i has exponents e_l with 0 <= e_l <= d_l and sum e_l=i. Its corresponding contribution to r_{i-1} is the same nonnegative monomial weight multiplied by sum_l gamma_l e_l, which is at most T. This also shows that q_i=0 implies r_{i-1}=0.

Let K = ceil(T)+d. Comparing the coefficient of z^(K-1) in Q F' - R F gives

0 = K c_K + sum_{i=1}^d ((K-i)q_i - r_{i-1}) c_{K-i}.

For each i, K-i >= ceil(T) >= T, so every multiplier in the sum is nonnegative. Also K-d = ceil(T) >= 1. If c_1,...,c_K were all strictly positive, the right-hand side would be strictly positive because of K c_K. This contradiction proves the lemma. No radius bound or distinctness assumption is used. QED.

## 3. All real parameters

Suppose all zeta_j are real. Remove the factors with zeta_j=0. Multiply f by

H(z) = product_{zeta_j>0} (1-zeta_j z)^(-beta_j).

Every Taylor coefficient of H is nonnegative and H(0)=1. Hence if a_1,...,a_K are strictly positive, so are the first K nonconstant coefficients of g=fH. This follows immediately by convolution, since the coefficient of a_k is 1 and all other summands are nonnegative.

Now g is the product of factors (1+t_j z)^(beta_j), where t_j=-zeta_j>0 ranges over the negative real parameters. If there are no such factors, g=1 and a_1>0 is already impossible. Otherwise apply the lemma with P_j=1+t_j z. If m is the number of retained factors and B_- the sum of their exponents, it gives

N <= ceil(B_-) + m <= ceil(B) + n.

Thus ceil(B)+n is an exponent-only bound for the complete real-parameter subcase, including positive, negative, repeated, and zero parameters.

## 4. Closed-left-half-plane extension

The reality hypothesis must not be replaced by an unsupported assumption that the original labels occur in conjugate pairs. The correct argument first merges equal nonzero parameters.

For each distinct nonzero lambda, let gamma(lambda) be the sum of beta_j over the indices with zeta_j=lambda. The logarithmic derivative is

f'/f = - sum_lambda gamma(lambda) lambda/(1-lambda z).

It is a real rational function because f has real Taylor coefficients near zero. Its distinct simple poles are 1/lambda with positive, nonzero residues gamma(lambda). Uniqueness of partial fractions therefore implies that the merged parameters occur in conjugate pairs and gamma(conjugate lambda)=gamma(lambda). Real merged parameters are unrestricted in sign.

Eliminate positive real parameters as in Section 3. A retained negative real parameter contributes P(z)=1+|lambda|z to exponent gamma(lambda). A retained nonreal conjugate pair contributes

P(z) = (1-lambda z)(1-conjugate(lambda) z)
     = 1 - 2 Re(lambda) z + |lambda|^2 z^2

to the common exponent gamma(lambda). If Re(lambda)<=0, P has nonnegative coefficients. The local identities follow by their logarithmic derivatives and value 1 at zero.

Apply the positive-polynomial-factor lemma. The sum d of the degrees is the number of retained distinct merged parameters, at most n. The weighted degree T is the sum of the original exponents at retained nonzero parameters, at most B. Therefore N <= ceil(B)+n.

This theorem covers every admissible tuple having no nonreal parameter in the open right half-plane. It does not cover the full source question.

**Corollary (at most two parameters).** If n<=2, the bound N<=ceil(B)+n holds for arbitrary admissible complex parameters. For n=1, reality of a_1=-beta_1 zeta_1 forces zeta_1 real, so Section 3 applies. For n=2, the merged-pole argument shows that either all nonzero parameters are real, or the two are a nonreal conjugate pair with beta_1=beta_2=beta. In the latter case a_1=-2 beta Re(zeta_1). If Re(zeta_1)>=0, a_1<=0 already. Otherwise the quadratic has nonnegative coefficients and Section 4 applies. Zero parameters and coincident parameters reduce to the real case. This exhausts all n<=2 configurations.

## 5. A sharp two-real-parameter example

Take beta_1=beta_2=3/5, zeta_1=-1, zeta_2=-2/5. Then

f(z)=(1+z)^(3/5)(1+(2/5)z)^(3/5),

and direct exact expansion gives

a_1 = 21/25,
a_2 = 3/625,
a_3 = 301/15625,
a_4 = -6471/390625.

Thus the first three coefficients are strictly positive. Consequently the candidate N=1+sum ceil(beta_j)=3 is false. Since ceil(6/5)+2=4, the bound is sharp for this exponent tuple even when arbitrary complex parameters are allowed, by the preceding corollary.

This is a counterexample to the proposed bound, not to Hall's existence statement.

## 6. Exact obstruction to extending ceil(B)+n to arbitrary complex roots

Take all four exponents equal to 21/10 and parameters

zeta_1, zeta_2 = 9/40 +/- (33/100)i,
zeta_3, zeta_4 = -19/40 +/- (3/25)i.

The conjugate pairing makes every Taylor coefficient real. Equivalently,

f(z) = P(z)^(21/10),

P(z) = (1-(9/20)z+(6381/40000)z^2)
       (1+(19/20)z+(9601/40000)z^2).

For a self-contained coefficient check, write P=sum_{i=0}^4 p_i z^i, where

(p_0,p_1,p_2,p_3,p_4) = (1, 1/2, -559/20000, 3483/80000, 61263981/1600000000).

Set a_0=1 and a_j=0 for j<0. The identity P f'=(21/10)P' f gives the exact recurrence

k a_k = sum_{i=1}^4 (((31/10)i-k) p_i a_(k-i))  for k>=1.

Thus every entry below can be checked using just four preceding rational coefficients. Exact arithmetic gives a_1,...,a_13>0 and a_14<0. The following fractions make the sign certificate self-contained:

| k | a_k |
|---|---|
|1|21/20|
|2|46011/200000|
|3|63959/1000000|
|4|2604972279/20000000000|
|5|17176057899/400000000000|
|6|1716180224143/4000000000000000|
|7|18850467170403/5000000000000000|
|8|378974338478734383/200000000000000000000|
|9|267541186415691881/8000000000000000000000|
|10|416255521145722785681/400000000000000000000000000|
|11|45257562655633678288701/8000000000000000000000000000|
|12|1130659439881192077002447/160000000000000000000000000000000|
|13|25669021687283962042020147/3200000000000000000000000000000000|
|14|-2888094401257003768564291271949/32000000000000000000000000000000000000|

Here B=42/5, so ceil(B)+n=9+4=13. Any bound for this exponent tuple in the full complex-parameter problem must therefore be at least 14. The source has no half-plane restriction, so the counterexample is admissible.

## 7. Elementary rational-exponent bound

Suppose q is a positive integer and q beta_j are all positive integers. Then f^q is a polynomial of degree at most D=qB. If a_1,...,a_(D+1) were all positive, the coefficient of z^(D+1) in f^q would be strictly positive: its expansion is a sum of nonnegative products of a_0,...,a_(D+1), including the term q a_(D+1). But that coefficient of a degree-at-most-D polynomial is zero. Therefore N<=qB+1.

This is explicit and uniform over arbitrary complex parameters, and includes the integer benchmark with q=1. Its potentially large common-denominator dependence is not claimed to be a sharp or good answer to the general question. For the example in Section 6 it gives N<=85, while that example shows N>=14.

## 8. Why the general compactness argument still needs work

A useful pointwise fact is straightforward. If all coefficients of f are nonnegative and f is not a polynomial, merge equal nonzero parameters. The radius of convergence R is finite and is the distance to a genuine branch singularity. Pringsheim's theorem places such a singularity at positive real R. Its merged exponent is positive. Along t increasing to R from below, the modulus of the product therefore tends to zero: the positive exponent at R forces a zero and every other factor remains bounded. But a power series with constant term 1 and nonnegative coefficients has f(t)>=1. This contradiction proves that a member of the family with all coefficients nonnegative must be a polynomial.

Such polynomial limits do exist, including after nonintegral exponents merge to integer sums. If max |zeta_j|=1 is used to normalize a hypothetical sequence of increasingly long positive prefixes, its limit may be a nonnegative-coefficient polynomial, so plain compactness does not finish the argument.

A log-derivative positive-multiplier argument can control neighborhoods of polynomial limits when every original parameter stays nonzero: a real denominator with no positive real zero has a polynomial multiple with strictly positive coefficients, and then sufficiently high coefficient equations give an obstruction. One can symmetrize the denominator to avoid assuming that the original labels pair under conjugation. This observation does not handle degree drop.

In particular, if some original zeta_j tends to zero, its nearby value can be small and positive real. This introduces a distant positive real zero of the denominator, hence a pole of the logarithmic derivative; it is a branch singularity of f when the corresponding merged exponent is nonintegral. Therefore the nearby denominator need not have any polynomial multiple with nonnegative coefficients. Its highest limiting coefficients are zero, and strict positivity cannot be extended by continuity. Thus this attempted neighborhood argument does not establish uniformity in the full normalized parameter space.

The theorem in Sections 2-4 avoids this issue entirely in its stated domain. The arbitrary-complex problem remains open in this report, and the unresolved degree-drop/merger analysis is not presented as a proof.

## 9. Approach accounting

This is one substantive coefficient-recurrence approach, approach 1 of the allocated five. The numerical exploration and exact counterexample checks are diagnostic parts of that approach, not additional completed approaches. No other queue row's budget is imported or reset.

The partial results have received the independent mathematical review in [AUDIT.md](AUDIT.md). This edition incorporates its explanatory Section 8 clarification. [ACCEPTANCE.json](ACCEPTANCE.json) distinguishes the original reviewed report from this edited edition and retains the unresolved general-case limitation.
