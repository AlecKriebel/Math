# Turn 5: rare polynomial peaks, large raw moments, and logarithmic moment control

## Results and their interpretation

This final substantive turn tests whether annealed moment bounds can bridge the remaining typical-growth gap. It obtains three rigorous facts for the finite-prefix M(D):

1. For every real q>0, with lambda=2^q,

       E M(D)^q >= Z_lambda(D)/(lambda D+1)^q,
       Z_lambda(D)=product_{i<=D}(1+(lambda−1)/i).          (1)

   Consequently, for each q>1,

       E M(D)^q >= c_q D^{2^q−1−q},                       (2)

   with a positive power. In particular,

       liminf_{D->infinity} E M(D)^2/D >= 1/96.            (3)

2. For each gamma>0, put lambda_gamma=(1+gamma)/log2 and I(lambda)=lambda log lambda−lambda+1. Then

       liminf_{D->infinity}
         log P(M(D)>=D^gamma)/log D >=−I(lambda_gamma).    (4)

3. If X_D=log M(D) log log D/log D for D>e, then for every fixed p>0,

       limsup_{D->infinity} E X_D^p <= C_*^p,
       C_*=(log3−1)(log2)^2.                              (5)

The raw moments (1)–(3) coexist with the almost-sure subpolynomial upper bounds from turns 3–4. They show why a direct fixed-q bound on E M(D)^q with q>1 cannot supply a polylogarithmic typical bound through Markov's inequality: those raw moments are genuinely polynomially large. This is an obstruction to that particular route, not a counterexample to polylogarithmic typical growth. Neither (2) nor (4) is claimed sharp. Equation (5) is a moment bound for a logarithm on a much larger normalization than the unresolved log-log exponent; it is not a convergence theorem for that exponent.

The proof uses elementary exponential tilting, pigeonhole counting, and the explicit uniform probability estimate proved in turn 4. No additional literature claim is needed.

## 1. The exact change of measure

First let D=n be a positive integer. Write

    N=|A intersect [1,n]|,   S=sum_{i in A intersect [1,n]} i.

For each fixed lambda>0 define a probability measure Q_lambda on the same finite set of indicators by

    dQ_lambda/dP=lambda^N/Z_lambda(n),
    Z_lambda(n)=E lambda^N
               =product_{i=1}^n(1+(lambda−1)/i).           (6)

This identity includes i=1: it is deterministically selected under both measures. Under Q_lambda, the indicators remain independent, with success probabilities

    p_i^(lambda)=lambda/(i+lambda−1).                     (7)

A direct multiplication of the Bernoulli probabilities proves both formulas, including the deterministic first coordinate. Thus no density is divided by the zero probability of omitting 1.

For fixed lambda>0,

    log Z_lambda(n)=(lambda−1)log n+O_lambda(1),
    E_Q N=lambda log n+O_lambda(1),
    Var_Q N<=E_Q N.                                       (8)

To prove the first estimate, discard finitely many indices depending on lambda and use log(1+(lambda−1)/i)=(lambda−1)/i+O_lambda(i^{-2}); the other estimates follow in the same way from (7) and independence. In particular there are positive constants bounding Z_lambda(n)/n^{lambda−1} above and below. For lambda>=1, also

    E_Q S=sum_{i=1}^n i lambda/(i+lambda−1)<=lambda n.      (9)

All constants here refer to a fixed lambda, not a growing one.

## 2. Pigeonhole lower bounds on raw moments

Every subset sum lies in {0,1,...,S}, and there are 2^N subsets. Hence deterministically

    M(n)>=2^N/(S+1).                                      (10)

For q>0 put lambda=2^q>1. Raise (10) to q, then use (6):

    E M(n)^q >= Z_lambda(n) E_Q (S+1)^{-q}.

The function x -> x^{-q} is convex on x>0, so Jensen's inequality and (9) give

    E_Q (S+1)^{-q} >=(E_Q S+1)^{-q}>=(lambda n+1)^{-q}.

This proves (1) for integer n. For real D, n=floor D gives the exact bound Z_lambda(D)/(lambda D+1)^q as well, since M(D)=M(n) and n<=D.

From (8), (2) follows whenever the exponent is positive. Its value f(q)=2^q−1−q is zero at q=1 and has derivative 2^q log2−1>0 for q>=1, because log2>1/2. Thus it is positive for every q>1. No positivity claim for this exponent is made for all q>0.

For q=2, lambda=4 and the product telescopes exactly:

    Z_4(n)=(n+1)(n+2)(n+3)/6.

It follows that

    E M(n)^2 >=(n+1)(n+2)(n+3)/[6(4n+1)^2].              (11)

Dividing by n and taking the liminf proves (3), also for real D by flooring. This proof does not need an asymptotic distribution of S, or a claim that its tilted mean describes its typical value sharply.

The same argument and the elementary inequality M<=2^N give only the coarse two-sided moment scales

    c_q D^{2^q−1−q} <= E M(D)^q <= C_q D^{2^q−1}.

When the lower power is negative, the trivial M>=1 is stronger. Neither endpoint is asserted to be the true moment exponent.

## 3. Polynomial lower tails for atypically large maxima

Fix gamma>0 and any lambda>(1+gamma)/log2. Choose delta>0 sufficiently small that

    (lambda−delta)log2>1+gamma.                           (12)

Here lambda>1. Under Q_lambda, Chebyshev's inequality using (8) shows

    Q_lambda(|N−lambda log n|<=delta log n)->1.

Markov's inequality and (9) give Q_lambda(S<=4 lambda n)>=3/4. Therefore their intersection F_n has Q_lambda-probability at least 1/2 for all large n. On F_n, (10) gives

    M(n)>= n^{(lambda−delta)log2}/(4 lambda n+1)
          >n^gamma                                      (13)

eventually, by (12). In the other direction N<=(lambda+delta)log n on F_n. Thus the likelihood ratio in (6) yields

    P(F_n)=Z_lambda(n) E_Q[lambda^{-N}1_{F_n}]
       >=(1/2)Z_lambda(n)n^{−(lambda+delta)log lambda}
       >=c_lambda n^{−I(lambda)−delta log lambda}.        (14)

This gives the claimed logarithmic probability lower bound after letting lambda decrease to lambda_gamma and delta decrease to zero subject to (12). These are fixed parameters during each n-limit.

For real D, apply the integer bound with an exponent gamma'>gamma and n=floor D. Eventually n^{gamma'}>=D^gamma. Then let gamma' decrease to gamma, using continuity of I(lambda_gamma). This proves (4) without silently replacing the event threshold during flooring.

The rate I(lambda_gamma) is positive, because lambda_gamma>1 and I is increasing from zero on (1,infinity). Thus this lower bound is fully consistent with probabilities tending to zero, and with almost-sure subpolynomial growth along dyadic scales. It does not assert a positive limiting probability of a polynomial-size maximum.

## 4. All fixed moments of the larger logarithmic normalization

We spell out how turn 4's probability estimate can be passed through expectation, rather than relying on its almost-sure assertion alone. Fix epsilon>0 and use the parameters k,t_0,u,c from turn 4, equation (13), for each sufficiently large D. Let B_D be the event that the annular multiplicity is at least k. Turn 4 proves

    P(B_D)<=2exp(−epsilon L/2)
              +2(L+3)exp(−(log L)^2/3)=:p_D, L=log D.    (15)

On B_D^c, the deterministic convolution bound gives

    X_D <= (log k)(log L)/L
              +(log2)(log L)/L * N(D^c)=:Y_D.             (16)

We need two elementary moment facts about sums N(T) of independent Bernoulli indicators. If mu_T=E N(T), then for each fixed r>0,

    E N(T)^r=O_r((1+mu_T)^r).                             (17)

For integer r this follows by expanding ordinary powers into falling factorial powers, whose expectations are at most mu_T^j. For arbitrary r use Lyapunov's inequality with an integer at least r. Also, as mu_T->infinity,

    N(T)/mu_T ->1 in every fixed L^r.                     (18)

Variance at most mu_T proves the L^2 case. Bounded higher moments from (17) give uniform integrability of every fixed power, and convergence in probability from L^2 then gives (18). Equivalently, interpolation with a strictly higher fixed moment proves it directly. The deterministic first indicator causes no difficulty in the factorial-moment bound.

Here T=D^c satisfies mu_T=cL+O(1)->infinity. Since t_0~log L/log2 and c=(a+epsilon)/t_0, (16)–(18) imply that Y_D converges in every fixed L^r to

    C_epsilon=(a+epsilon)(log2)^2.

In particular E Y_D^p ->C_epsilon^p for all p>0.

On B_D, use the unconditional bound log M(D)<=N(D)log2. Cauchy–Schwarz and (17), with mu_D=O(L), give

    E[X_D^p 1_{B_D}]
       <=[(log2)(log L)/L]^p
                  (E N(D)^{2p})^{1/2} P(B_D)^{1/2}
       <=C_p(log L)^p p_D^{1/2} ->0.                     (19)

Combine (16) and (19), then let epsilon decrease to zero. This proves (5). Applying the same result with any exponent larger than p also gives uniform integrability of X_D^p for sufficiently large D. No unidentified cutoff-dependent constant has been used to exchange limits and expectations.

## Final disposition after five substantive turns

The quantitative finite-prefix problem remains unresolved. The proved almost-sure lower bound is at least the credited exponent eta on the polylogarithmic scale. The proved upper bound is (1) of turn 4, which is substantially larger. The deterministic almost-sure liminf and limsup of log M(D)/log log D from turn 1 have not been shown finite, equal, or equal to eta; convergence in probability on that scale has not been proved.

The unrestricted infinite-set supremum is infinite almost surely by the separately credited source corollary. That literal observation does not answer the broader source growth question, and is not used to label this five-turn quantitative attempt solved. The latest threshold-identification preprint does not evaluate the prefix exponent in this packet. The rare-event results of this turn are method diagnostics, not original-question counterexamples.
