# Checkable implication, independently reconstructed

This derivation was begun before reading any inherited priority verdict. It uses the pinned candidate only to identify the claim, then specializes primary published statements. Let S be the primes p congruent to 3 modulo 4, N=p-1, and theta_p=phi(N)/N.

## 1. The dynamical reduction

For p in S, u^2+1 is nonzero for every u in F_p. On a vertical fiber, the map multiplies v by u^2+1. Thus v=0 has period 1 and every v nonzero has period ord_p(u^2+1). The map is birational over Q and permutes all p^2 affine points for every p in S.

Fix x in [1/2,1). Every proper divisor of N is at most N/2 < px, whereas N>px once p>1/(1-x). If

    P_p = #{u in F_p : u^2+1 has order N},

then exactly (p-1)P_p points are excluded from the point-weighted CDF. Consequently

    D_p(x) = 1 - (p-1)P_p/p^2.                              (D1)

This uses the p^2 point normalization and threshold px verbatim as mathematical conventions; it does not average over primes or count cycles with equal weights.

## 2. Existing quadratic primitive-value estimate

In Booker-Cohen-Sutherland-Trudgian (BCST), arXiv:1803.01435v2, section 2 equations (5)-(6) and Lemma 1, take q=p, Q(t)=t^2+1, e1=1, e2=N. The hypotheses a nonzero and b^2-4ac nonzero hold because p is odd. Their N(1,N) counts nonzero inputs whose Q-value is primitive. The omitted input u=0 has Q(0)=1, which is nonprimitive because N>=2. Hence their count equals P_p exactly.

The principal-principal character sum is exactly p-1 in this class, since Q has no zero. The d1=1,d2>1 case of Lemma 1 and the character coefficients give

    |P_p - theta_p(p-1)|
      <= theta_p (2^omega(N)-1)(sqrt(p)+1).                 (D2)

In particular P_p=p theta_p+o(p): for example 2^omega(N)<=64 N^(1/4), separating the six primes below 16 from primes at least 17. Combining (D1)-(D2),

    D_p(x) = 1-theta_p+o(1)                               (D3)

for each fixed x in [1/2,1). This is a direct specialization of an existing count, with only elementary bookkeeping. The pinned proof's Jacobi-sum estimate is a slightly sharper elementary proof of the same asymptotic, not a new primitive-value theorem.

Ostafe-Shparlinski (O&S), arXiv:0902.3884v3, section 2.1 equations (1)-(4), already has the generic triangular family. Set m=1, g0(t)=t^2+1, h0=0, a=1, b=0. Its coordinate order gives ((X1^2+1)X0,X1). Conjugacy by coordinate exchange yields exactly the candidate map. This is inclusion as a parameter specialization of an earlier family, not an earlier explicit statement of the target counterexample. O&S is unnecessary to prove (D3).

## 3. Existing continuous scalar law and the subset lemma

Deshouillers-Hassani (DH), J. Aust. Math. Soc. 93 (2012), printed pp.78-79, Proposition 2.1 and equation (2.1), applies to g(n)=phi(n)/n. At a prime ell,

    log g(ell) = log(1-1/ell) = O(1/ell).

Therefore its first two required series converge absolutely; the third is empty because |log(1-1/ell)|<=log 2<1. For m=2, the reciprocal sum in the continuity criterion runs over all odd primes and diverges. Their explicit specialization thus gives a continuous CDF G2 for theta_p over odd primes. Its empirical probability measures converge weakly to an atomless law mu on [0,1/2]. No GRH or fixed-base Artin conjecture is involved.

**Subset lemma.** Suppose a bounded scalar sequence indexed by primes has an atomless limiting empirical law mu. It cannot converge along any prime subset A of positive relative prime upper density. To check this, suppose values converge to a along A and delta=limsup pi_A(X)/pi(X)>0. For every epsilon>0, all but finitely many A-values lie in the closed interval I_epsilon=[a-epsilon,a+epsilon]. Hence

    limsup_X mu_X(I_epsilon) >= delta.

The closed-set inequality for weak convergence gives mu(I_epsilon)>=delta. Let epsilon decrease to zero. Continuity of measures from above gives mu({a})>=delta, a contradiction.

The class S has relative prime density 1/2. Thus theta_p does not converge on S. In fact theta cannot converge on any positive-density prime subset of S. Formula (D3) transfers the failure of convergence to D_p(x), for every fixed x in [1/2,1). No independence between theta_p and the residue class is assumed or needed.

If the period/p measures had a weak limit along any such positive-density subset, their CDFs would converge at every continuity point of that limit. A probability CDF has at most countably many discontinuities, so some x in (1/2,1) is a continuity point; this contradicts (D3) and the subset lemma. This proves the qualitative no-weak-limit assertion, even allowing positive-density thinning of S.

## 4. The numerical gap is a separate elementary consequence

Continuity alone does not quantify 23/24, nor does it establish limsup D=1. The old arithmetic inputs already used in the pinned proof do supply both.

For limsup, let Q_j be the product of the first j odd primes. The conditions p=3 modulo 4 and p=1 modulo Q_j define a reduced class modulo 4Q_j. Dirichlet's theorem allows an increasing selection p_j from these classes. Then

    0 <= theta_(p_j) <= (1/2) product_(ell|Q_j)(1-1/ell) -> 0.

Euler's vanishing prime product gives the last step. By (D3) and D_p<=1, limsup_(p in S) D_p(x)=1.

For the explicit second subsequence, Menici-Pehlivan (MP), Acta Arith. 174 (2016), equation (1), or Lemma 2 with r=m=1, gives unconditionally

    (1/pi(X)) sum_(p<=X) theta_p -> A,
    A=product_(ell prime)(1-1/(ell(ell-1))).

Let b=limsup_(p in S) theta_p. For all odd primes theta_p<=1/2. By the prime number theorem in the two classes modulo 4, and the definition of limsup,

    A <= (1/2)(1/2) + (1/2)b,
    b >= 2A-1/2.                                         (D4)

An exact elementary lower bound is A>=7/24: the factor at 2 is 1/2, and the sum of 1/(ell(ell-1)) over odd primes is at most sum_(n>=3,n!=4)1/(n(n-1))=5/12. Apply product(1-a_i)>=1-sum(a_i) and pass to the limit. Hence b>=1/12. Since (D3) implies liminf D=1-limsup theta,

    liminf_(p in S) D_p(x) <= 3/2-2A <= 11/12 < 23/24.    (D5)

Thus even a stronger coarse gap follows from the published mean and an elementary class split. This does not require a new quantitative consequence of DH. The exact claimed gap is not supplied by continuity *alone*, but there is no substantive new analytic-number-theory gap once the credited mean is included.

## 5. Boundary cases and precise scope

- p=2 is outside S. For p=3, Q(0)=1 is still nonprimitive; asymptotic threshold arguments only require sufficiently large p.
- x=1/2 is covered by the proper-divisor bound. x=1 is excluded for a reason: D_p(1)=1. No assertion for fixed x<1/2 is needed.
- S is fixed before taking limits. The Dirichlet subsequence used for limsup is sparse and is not substituted for S.
- The observable is point-weighted on all affine points. The inverse is rational rather than globally polynomial over C; it is defined everywhere over F_p for p in S.
- The conclusion addresses the literal broad birational assertion in the original two-page Vivaldi contribution. It does not decide a narrower conjecture restricted to polynomial automorphisms, area-preserving maps, or genus-one foliations.
