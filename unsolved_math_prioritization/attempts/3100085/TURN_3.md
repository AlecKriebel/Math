# Turn 3: a general small-prime obstruction from the classical row LCM

**Scoped partial; original question unresolved after three new/recovered author turns.** This turn tests a global prime-valuation route instead of extending the finite collision scan. It yields an exact necessary divisibility test for every n and every pair of tie lengths, and specifies why that test does not finish the problem.

## 1. Credited input and notation

Let L_n=lcm{binomial(n,k):0<=k<=n}. Farhi's classical identity is

 L_n=lcm(1,2,...,n+1)/(n+1).                                   (1)

The full five-page arXiv0906.2295v2 source was read, including its Kummer-valuation proof. This identity and the resulting maximum-valuation formula are prior results, not discoveries of this campaign. For each prime ell, write

 e_ell(n)=v_ell(L_n)=floor(log_ell(n+1))-v_ell(n+1).             (2)

For an integer R>=1 define the integer

 K_R(n)=product_ell ell^floor(e_ell(n)/R).

Equivalently, K_R(n) is the largest positive integer whose Rth power divides L_n. This is a divisibility root, not the real floor of L_n^(1/R).

## 2. The collision obstruction

Suppose a genuine two-pair collision exists with outer length r and inner length s, so r>s>=1 by Turn1. Put g=gcd(r,s), R=r/g, S=s/g. Then R>S and gcd(R,S)=1, hence R>=2. As before, q=p/(1-p)>0.

**Theorem 1.** There are coprime positive integers a!=b such that

 q^g=a/b, and a|K_R(n), b|K_R(n).                              (3)

Proof. Both q^r and q^s are rational, so Bezout gives q^g in Q. Reduce it to a/b. The outer pair satisfies

 binomial(n,k)/binomial(n,l)=a^R/b^R.

Because a and b are coprime, a^R divides the numerator binomial coefficient and b^R divides the denominator coefficient. Both coefficients divide L_n. Prime by prime, Rv_ell(a)<=e_ell(n) and Rv_ell(b)<=e_ell(n), which is exactly (3). The condition a!=b follows from q!=1.

### Consequences

1. If K_R(n)=1, these two lengths cannot collide. More coarsely, R must not exceed max_ell e_ell(n).
2. Every prime dividing the numerator or denominator of q^g is at most(n+1)^(1/R), hence at most sqrt(n+1). This follows because a nonzero exponent requires e_ell(n)>=R, which by(2) implies ell^R<=n+1.
3. Every prime larger than sqrt(n+1) has equal valuation at the two endpoints of each tied pair. Thus the squarefree product of those large primes dividing binomial(n,k) must match between endpoints. This is a necessary endpoint signature, not an asserted injective signature.
4. If q itself is rational, Turn2 gives r>=7, and the same proof with q=a/b shows a,b divide K_r(n), hence divide K_7(n). Thus K_7(n)=1 excludes all rational-odds collisions in that row, regardless of their lengths.

For example, in Mersenne rows n=2^a-1, e_2(n)=0. If n+1<3^7, then e_ell(n)<7 for every odd prime as well, so K_7(n)=1. Consequently the rows127,255,511,1023,2047 have no rational-odds collision. This is an analytic consequence of(1)-(3), not a numerical scan at those n. It makes no claim about irrational odds in those rows.

## 3. The squarefree-row boundary is already classical

If L_n is squarefree, e_ell(n)<=1 for every prime; since R>=2, K_R(n)=1 and Theorem1 excludes a collision for every real p in the source domain.

For completeness, the rows with squarefree L_n are exactly

 n in {0,1,2,3,5,7,11,23}.

This classification is known; Conrad's binomial-coefficient notes explicitly record23 as the last all-squarefree row, with a reference to OEISA048278. An elementary derivation from(2) clarifies the boundary. Put m=n+1. For m>=2 let 2^a<=m<2^(a+1). The inequality e_2(n)<=1 forces 2^(a-1)|m, so m is either2^a or3*2^(a-1). In the first case v_3(m)=0, and e_3<=1 implies m<9. In the second v_3(m)=1, and e_3<=1 implies m<27. The possible m are therefore1,2,3,4,6,8,12,24, including the separate m1 case. Each indeed satisfies(2) with all exponents at most1; primes>=5 have square exceeding24. Subtracting1 gives the list.

The classification and row-LCM identity are explicitly credited. This route does not produce an infinite family of completely excluded rows by merely invoking squarefreeness.

## 4. Why the LCM route is insufficient by itself

The divisibility criterion forgets which two coefficients realize the relevant prime exponents and whether the two ratios occur simultaneously at nested distinct endpoints. It can retain false candidates. For instance, L_8=280 and K_2(8)=2, so (3) permits q^g=1/2 for a putative length ratioR:S=2:1. But Turn1's exact n8 test excludes every genuine collision in that row. Thus no converse to(3) is valid, even at a tiny fixed n.

The precise remaining task is the joint realization of the allowed prime vectors by four coefficients. The LCM obstruction is a useful filter and a structural restriction, but it does not establish the global no-collision conclusion. It is marked blocked as a standalone completion route unless supplemented by a mechanism controlling that joint realization. Two genuine author turns remain. No historical novelty is asserted for these elementary applications of the credited identities.
