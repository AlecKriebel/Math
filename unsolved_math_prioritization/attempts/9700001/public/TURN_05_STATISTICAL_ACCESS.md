# Attempt 5: finite-sample access and the need for a tolerance

Previous exact algorithms require explicit rational laws or exact moments. Here the input is instead K independent complete sample paths of a process with |X_t|<=B, where B>0 is known. Fix a finite library of m>=1 stopping rules before seeing those paths. Rules must be executable using the observed prefix; their values may be evaluated on a complete stored path by replaying them online. Training a library on the same sample without a uniform bound is not covered.

Let a_j=E[X_{T_j}-X_0], and let hat a_j be the average over the K paths. Within each path the m evaluations may be dependent; only independence between paths is used.

## Theorem 5A: a simultaneous certificate with an explicit gap

For 0<delta<1 set

r=B sqrt(8 log(2m/delta)/K).

With probability at least 1-delta, simultaneously for all j,

|hat a_j-a_j|<=r.                              (7)

Consequently, for a chosen tolerance epsilon>=0:

- if some |hat a_j|>epsilon+r, that rule is a genuine witness with |a_j|>epsilon;
- if max_j |hat a_j|<=epsilon-r, every library rule satisfies |a_j|<=epsilon;
- otherwise the data are inconclusive under this certificate.

The second branch is usually empty if epsilon<r; this is intentional. A true maximum exceeding epsilon+2r guarantees the first branch on event (7). Library evaluation is polynomial work if K, m, the path length, and the per-rule execution costs are polynomial. This gives a reliable search and certification procedure for that library at a separated tolerance, not for every efficient rule.

### Full concentration proof

For a bounded random variable Y in [a,b], put h(lambda)=log E exp(lambda(Y-EY)). Under its exponentially tilted law, h''(lambda) is the variance of Y. For any law on [a,b], (Y-a)(b-Y)>=0 implies Var(Y)<=(EY-a)(b-EY)<=(b-a)^2/4. Since h(0)=h'(0)=0, integrating this second-derivative bound in either direction gives h(lambda)<=lambda^2(b-a)^2/8.

For K independent copies, multiply the moment-generating functions and apply Markov's inequality to exp(lambda sum(Y_i-EY_i)). Optimizing lambda>0 gives

P(hat Y-EY>=r)<=exp(-2Kr^2/(b-a)^2).

Apply the same argument to -Y for the lower tail. Here Y=X_{T_j}-X_0 lies in [-2B,2B], a range of width 4B, so the two-sided bound is 2 exp(-Kr^2/(8B^2)). A union bound over m rules proves (7). The certificate conclusions follow directly from the triangle inequality. This is the classical Hoeffding argument, credited to Hoeffding (1963), not a new concentration result. QED.

## Theorem 5B: no uniform exact-zero decision from boundedly many samples

Already for n=1 consider two laws: X_0=0 always, and under P_0 let X_1=0, while under P_theta let X_1 be Bernoulli(theta), 0<theta<1. Values lie in [0,1]. The first process is a martingale; the second has the constant-time witness T=1 with expected deviation theta.

The total variation distance between their K-sample laws is exactly

1-(1-theta)^K <= K theta.                      (8)

Indeed P_0 puts all its mass on the all-zero sample; P_theta assigns that sample probability (1-theta)^K and assigns the rest elsewhere. The inequality follows either by the union bound or induction on K.

If a possibly randomized test recognizes the null with probability at least 2/3 under P_0 and recognizes the alternative with probability at least 2/3 under P_theta, the probability it reports the alternative differs by at least 1/3 between these laws. Any [0,1]-valued randomized decision function has expectation difference at most total variation (sum the positive and negative masses, or condition on its random seed). Therefore (8) implies K>=1/(3 theta). No finite uniform K works over every nonzero theta. A procedure using at most K samples, possibly adaptively, is also a function of K samples by padding, so the same conclusion holds.

This is a lower bound for reliably deciding or certifying a violation. It is not a claim that the stopping map T=1 itself is difficult to write down. The distinction is exactly why an input-access and success criterion must accompany the words 'practical to find'.

## Final outcome

A practical finite-sample notion must specify at least the accessible observations, law representation or sampling access, strategy class and resource bound, tolerance/scale of advantage, and permitted error probability. The five attempts give rigorous positive models and precise obstructions once these are fixed. They do not identify a canonical, broadly applicable MPP class, nor compress all polynomial-time stopping algorithms into one fixed polynomial-size certificate library. No general resolution of Aldous's programmatic question is claimed.
