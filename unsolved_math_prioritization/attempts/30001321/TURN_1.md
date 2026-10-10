# Turn 1: exact replica overlap and ordinary coarse-grained concentration

**30001321 / OWR-4081-005. Scoped partial, not a solution of the superpolynomial-tail conjecture.** One substantive author turn. No novelty claim; the replica-difference and quenched-mean mechanisms have established precedents cited below.

## 1. Exact model and remaining target

Let p_(s,x), s>=0 and x in Z, be i.i.d. random variables with
0<p_(s,x)<1 almost surely. Starting from X_0=0, the quenched walk
steps from x to x+1 with probability p_(s,x), and to x−1 otherwise.
The environment is resampled in time and independent across spatial
sites, as in Berger's OWR Theorem 1 and Conjecture 1, printed p.2151.
No uniform lower bound on p or 1−p is used in this partial theorem.

Put q=E p, a=q(1−q), delta=E[p(1−p)] and sigma²=Var(p)=a−delta.
Then 0<delta<=a<=1/4. The averaged walk has independent increments,
mean v=2q−1 and variance 4a per step. Its parity is retained throughout.

For a deterministic partition of Z into intervals I_j containing M
consecutive lattice points, set

    L_(N,M)=sum_j |P_omega(X_N in I_j)−P(X_N in I_j)|.

The original target asks whether, in transverse dimension one, the
universal assertion of superpolynomial decay of P_env(L_(N,M_N)>epsilon)
fails for some i.i.d. elliptic environment, diverging M_N and fixed
epsilon>0. A deterministic environment trivially has L=0, so it cannot
be asserted that every elliptic law must fail. Neither a quenched CLT
nor ordinary concentration settles this quantitative target.

### Partial theorem

There is a finite constant C, depending only on the environment law,
such that, for N>=2, integers M>=1, every deterministic interval
alignment, and R>=1,

 E_env L_(N,M)
   <= C sqrt[(R/M+1/sqrt(N))
              (1+log(1+min(M,sqrt(N))))] + C/R².             (1)

In particular, for **every** M_N→infinity, L_(N,M_N)→0 in L1 of
the environment and hence in probability, uniformly over deterministic
alignments. This is strictly weaker than the requested superpolynomial
tail bound. It does not prove or disprove Berger's failure conjecture.

## 2. The exact two-replica difference chain

Write mu_s(x)=P_omega(X_s=x). Conditional on the same environment,
run two independent walks X,Y from zero. Their annealed half-difference
D_s=(X_s−Y_s)/2 is integer valued because the walks have the same
parity. If D_s is nonzero, their current environment variables are
independent. If D_s=0, they share a variable. Therefore D is the
nearest-neighbor lazy Markov chain with transitions

    from d!=0:  d→d+1 and d→d−1 each with probability a;
                 hold with probability 1−2a;
    from 0:     0→+1 and 0→−1 each with probability delta;
                 hold with probability 1−2delta.            (2)

In particular,

    E_env sum_x mu_s(x)² = P(D_s=0) =: g_s.                 (3)

This identity has no unspecified constant and does not invoke a
quenched heat-kernel bound.

### Return generating function

For 0<=z<1 let G(z)=sum_(s>=0) g_s z^s. The hitting-time transform
from 1 to 0 for the homogeneous chain away from 0 is rho(z), the
smaller root of

    az rho²−[1−(1−2a)z]rho+az=0.

The solution bounded at spatial infinity is rho(z)^d when starting
from d>=0. The first-return decomposition at 0 gives

    G(z)=1/[1−(1−2delta)z−2delta z rho(z)]
        =1/[(1−delta/a)(1−z)
              +(delta/a)sqrt((1−z)(1−(1−4a)z))].            (4)

The square root is the nonnegative branch on [0,1). Because delta<=a
and 1−(1−4a)z>=4a,

    G(z)<=sqrt(a)/(2delta sqrt(1−z)).                       (5)

For a pointwise coefficient bound, not just an averaged estimate,
observe that (2) is reversible with weights pi(0)=a/delta and
pi(d)=1 for d!=0. Its transition operator P is a self-adjoint
contraction on l2(pi). All holding probabilities are at least 1/2,
so 2P−I is also a Markov contraction; hence the spectrum of P lies
in [0,1]. The spectral representation of g_s shows it is nonincreasing.
Consequently

    g_n (1−z^(n+1))/(1−z)<=G(z).

Take z=n/(n+1), use z^(n+1)<=exp(−1), and apply (5). This proves

    g_n<=C/sqrt(n+1).                                       (6)

No asymptotic coefficient-transfer theorem is needed for this bound.

## 3. A layer martingale and exact variance identity

For a bounded deterministic terminal function f:Z→R, let
Z_f=P_omega f(X_N), and expose entire environment layers in time
order. If F_s contains layers 0,...,s−1, then

 E_env[Z_f | F_s]=sum_x mu_s(x) T_(N−s)f(x),

where T_t is the averaged biased-walk semigroup. With t=N−s−1,
the next martingale increment is exactly

    sum_x mu_s(x) (p_(s,x)−q)
          [T_t f(x+1)−T_t f(x−1)].                         (7)

Given F_s, its summands are independent and centered. Orthogonality
of time increments therefore gives

 Var_env(Z_f)=sigma² sum_(s=0)^(N−1) sum_x E[mu_s(x)²]
                   [T_(N−s−1)f(x+1)−T_(N−s−1)f(x−1)]².   (8)

Only finitely many sites influence a fixed N, so there is no infinite
filtration or conditional summation issue. Taking f(x)=x is also
legitimate on this finite reachable set and yields

 Var_env(E_omega X_N)=4sigma² sum_(s=0)^(N−1) g_s.          (9)

The resulting O(sqrt(N)) variance and N^(1/4) fluctuation scale are
consistent with the credited prior work of Balázs–Rassoul-Agha–
Seppäläinen. Equation (9) does not turn that fluctuation scale into a
fixed-epsilon coarse-L1 lower-tail certificate.

## 4. Binomial gradients, with parity included

Let b_t(k)=P(X_t=k) for the averaged walk. On its parity sublattice it
is a binomial mass function. For constants depending on q, standard
binomial estimates give, for all t>=0,

 max_k b_t(k)<=C/(t+1)^(1/2),
 max_k |b_t(k+2)−b_t(k)|<=C/(t+1),
 sum_k |b_t(k+2)−b_t(k)|<=C/(t+1)^(1/2).                  (10)

The last identity follows from unimodality: the sum is twice the
maximum binomial mass. For completeness, the middle estimate follows
from the ratio of adjacent binomial masses. Within a fixed fraction
of the mean, the relative difference is bounded by
C(|j−tq|+1)/(t+1); the binomial Gaussian bound from Stirling's formula
controls the product by C/(t+1). Outside that region the exponential
binomial tail absorbs the at-most-polynomial ratio. The finitely many
small t are absorbed into C. These are elementary estimates, not a
claim of a quenched local CLT.

For f_j=1_(I_j), write
h_j(x)=T_t f_j(x+1)−T_t f_j(x−1). Summation of the parity-lattice
mass difference over one interval telescopes to at most two endpoint
masses. Also, the interval has at most M contributing sites. Thus

 max_j |h_j(x)|<=C min((t+1)^(−1/2), M/(t+1)).

Because the I_j partition the whole lattice,

    sum_j |h_j(x)|<=sum_k |b_t(k+2)−b_t(k)|.

Multiplying these two bounds yields, uniformly in x and alignment,

 sum_j h_j(x)²
    <=C min((t+1)^(−1), M(t+1)^(−3/2)).                    (11)

## 5. Sum of interval variances

Apply (8) to each f_j, sum, and use (3), (6), and (11). Nonnegative
summation is justified directly; at fixed N only finitely many
intervals can carry mass. We obtain

 sum_j Var_env(mu_N(I_j))
  <=C sum_(s=0)^(N−1) (s+1)^(−1/2)
             min((N−s)^(−1), M(N−s)^(−3/2)).              (12)

For s<=N/2 the sum is at most C min(M/N,1/sqrt(N)). For s>N/2,
factor out C/sqrt(N) and put k=N−s. Splitting at k=M² gives

 sum_(k<=N) min(k^(−1),M k^(−3/2))
    <=C[1+log(1+min(M,sqrt(N)))].

Hence

 sum_j Var_env(mu_N(I_j))
    <= C[1+log(1+min(M,sqrt(N)))]/sqrt(N).                  (13)

This estimate controls a sum of variances, not a superpolynomial
environment tail and not independence of the interval masses.

## 6. From variances to coarse L1 convergence

The interval [vN−R sqrt(N),vN+R sqrt(N)] intersects at most
2R sqrt(N)/M+2 partition cells. On those cells Cauchy–Schwarz and
E mu_N(I_j)=P(X_N in I_j) bound the expected sum of absolute
deviations by the square root of that number times (13).

All other cells lie outside the displayed window. Their expected
absolute deviations sum to at most twice the averaged probability
outside the window, at most 8a/R² by the averaged variance 4aN.
Combining gives (1).

Fix R, then let N→infinity with M=M_N→infinity. The first term
vanishes: if M<=sqrt(N), log(1+M)/M→0; otherwise it is bounded
by constants times log(N)/sqrt(N). Then let R→infinity. This proves
the asserted L1 convergence. The bound is uniform over deterministic
partition alignments.

## 7. Exact unresolved gap and next attacks

The source asks for tails smaller than N^(−k) for **every** k at
each fixed epsilon and every diverging M_N. Bound (1) and Markov's
inequality do not provide that rate, especially when M_N diverges
arbitrarily slowly. Nor does the exact second-moment identity furnish
a polynomial lower bound on a fixed-epsilon event. Thus the original
conjecture remains unresolved after this turn.

The first route reduces the missing upper-tail input to control of
random conditional overlap sums in (7), beyond their expectations.
A genuinely different counterexample route would need an admissible
i.i.d. environment event with non-superpolynomial cost and a fixed
coarse-L1 effect; merely citing N^(1/4) quenched-mean fluctuations or
different ballistic large-deviation rate functions does not supply one.

### Credit

- Berger, OWR38/2009, pp.2151–2152, exact theorem/conjecture and
  exposure/concentration strategy:
  https://ems.press/content/serial-article-files/46239
- Balázs, Rassoul-Agha, Seppäläinen, *The random average process and
  random walk in a space-time random environment in one dimension*,
  CMP266 (2006), 499–545; full author manuscript Theorem3.1 and the
  difference-walk discussion: https://www.math.utah.edu/~firas/Papers/rap.pdf
- Yilmaz–Zeitouni, CMP300 (2010), 243–271,
  DOI10.1007/s00220-010-1119-3: differing ballistic large-deviation
  rates are related but do not by themselves decide this target.
