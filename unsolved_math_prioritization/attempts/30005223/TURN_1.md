# Substantive turn 1: residual zeros beyond all three standard tests

## Aim and result

The March2026 Peluse–Soundararajan theorem counts typesI–III, not all zeros. The first author route tested whether the uncounted zeros can be eliminated by a stronger deterministic Murnaghan–Nakayama support argument. The result is an exact infinite family outside all three tests and a quantitative classification within two character rows. It exposes a genuine missing case in a direct transfer of the known asymptotic, but its own density is exponentially small. The original total-density limit is not determined.

All character identities and partition asymptotic inputs used here are classical; this is an independently reconstructed scoped deduction and route test, not a novelty assertion.

## 1. An exact family and its precise typeIII classification

Let n=m+1>=3, lambda=(n-1,1), and let mu be the partition (nu,1), where nu is a partition of m with all parts at least2. The standard permutation representation minus its invariant line has character

chi_(n-1,1)(mu) = number_of_parts_equal_to_1(mu)-1 = 0.       (1)

The hook multiset of lambda is {n, n-2,n-3,...,1,1}. Consequently, for every integer t>=2,

H_t(lambda)=floor(n/t)-1_(t divides n-1).                    (2)

If t does not divide m, the weighted part statistic P_t(mu) cannot exceed H_t(lambda), since the total size is n. If t divides m, then

H_t(lambda)=m/t-1,
P_t(mu)<=m/t,

and strict inequality P_t>H_t holds exactly when every part of nu is divisible by t. Therefore

(lambda,mu) is of typeIII if and only if gcd(parts of nu)>1. (3)

Here the unavoidable single part1 of mu contributes nothing to P_t for t>=2. For t=1 both statistics equal n. Thus (3) checks every possible integer in the criterion, not just primes or part sizes.

Furthermore H_t(lambda)=0 for an available part t of mu exactly when t=n-1. Thus typeII, and hence typeI in this family, occurs exactly when nu=(m). In particular every nu with gcd1 supplies a zero outside typesI,II,III. Conjugating lambda preserves hook lengths and multiplies character values by the sign of mu, so the same family exists in the distinct conjugate row (2,1^(n-2)) when n>=4.

Example: n=6, lambda=(5,1), mu=(3,2,1). The character vanishes, gcd(3,2)=1, and none of the three standard tests detects it.

## 2. These can be support-extinction zeros, not necessarily signed cancellations

Use the Murnaghan–Nakayama rule with all nonunit parts of mu removed before its final1. For a standard shape (r-1,1), a rim hook of size t with 2<=t<=r-2 is unique: it removes the end of the long first row, leaving (r-t-1,1), with positive sign. This follows directly from the beta set {r,1}. A rim hook of size r-1 does not exist, because moving r to1 collides with the other beta number.

Follow any order of the parts of nu. Until the last part, only the unique horizontal removal occurs. At the last part t, the remaining shape is (t,1), and the required rim hook of size t is absent. There is no complete rim-hook chain in this removal order. Hence the zeros in (1), including the ones outside typeIII, have a deterministic sequential support-extinction certificate.

The unsigned number of chains depends on removal order. For the example (5,1),(3,2,1), removing 3,2,1 gives no chain, whereas removing 1,3,2 gives two chains with opposite total signs. This is why replacing character vanishing by a single order-independent condition that “there are no chains” would be wrong. The character sum itself is order independent.

There are also genuine signed cancellations in the canonical decreasing order outside typeIII: lambda=(2,2), mu=(2,1,1) has two opposite-sign chains, character0, and no typeIII obstruction. Neither all residual zeros as chain extinction nor all residual zeros as signed cancellation can be assumed without proof.

## 3. Exact count and asymptotic size of this residual family

Let C(m) count partitions nu of m with no part1 and gcd(parts)=1. Mobius inversion gives the exact formula

C(m)=p(m)-p(m-1)+sum_(d|m,d>=2) mobius(d) p(m/d).           (4)

To prove it, sum the identity 1_(gcd(nu)=1)=sum_(d|all_parts(nu)) mobius(d) over the partitions without1. For d=1 their count is p(m)-p(m-1). For d>=2 dividing all parts by d gives every partition of m/d; the original parts are automatically at least2. This establishes (4) without an independence assumption on the parts.

The divisor correction in (4) has absolute value at most m p(floor(m/2)). The Hardy–Ramanujan estimate makes this exponentially smaller than p(m)/sqrt(m). Proposition3 of Peluse–Soundararajan2026, at t=1, gives

p(m-1)/p(m)=exp(-pi/sqrt(6m))(1+O(m^(-3/4))).

It follows that

C(m) ~ pi p(m)/sqrt(6m).                                   (5)

Thus, for n>=4, the two conjugate rows supply exactly 2C(n-1) distinct pairs outside typeIII, of total table density

2C(n-1)/p(n)^2 ~ 2pi/[sqrt(6n) p(n)].                      (6)

This is strictly a lower bound on the residual-zero density, not an asymptotic for all residual zeros. It is exponentially smaller than the known leading scale 1/log n. More generally, even a complete treatment of all hook character rows covers at most n/p(n) of the whole table, because there are n hook partitions. Such a route alone cannot control the bulk of uniformly sampled lambda.

## 4. Finite independent implementation and surviving gap

The locally authored checker uses beta-number rim-hook removal and integer arithmetic. It verifies character dimensions by the hook-length formula, column norms and off-diagonal character orthogonality, the sufficient typeIII criterion, the exact gcd characterization and Mobius count through m=31, and both order/cancellation examples. It computes small complete tables through n=12 as diagnostics only. It correctly distinguishes uniform class sampling from uniform element sampling; their S4 values are 4/25 and 7/30 respectively. The source's numerical decimal next to 28/120 is not used as a mathematical input.

The surviving obstacle is a uniform upper bound for zeros outside typeIII in the bulk of partition shapes. Equation (6) shows this residual set is not empty or exactly characterized by the three known tests, while the hook-row mass bound explains why the present exact family cannot settle the limiting probability. A next substantive route must analyze a genuinely bulk family or a valid anti-concentration reduction, without changing the sampling distribution.
