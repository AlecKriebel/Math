# Approach 1: recurrence in the uniform-convergence half-plane

Target: 30002507 / OWR-12866-017. This is a restricted obstruction, not a negative answer to Balazard's question. The argument is classical almost-periodicity plus Rouché, reconstructed here with its necessary convergence hypothesis explicit. No novelty is claimed.

Write H_b = {s: Re(s)>b}. An ordinary Dirichlet series is f(s)=sum_{n>=1} a_n n^{-s}, in increasing integer order. Let sigma_u be the infimum of real b for which its partial sums converge uniformly on H_b. The infimum may be infinite. The ordinary convergence abscissa sigma_c can be strictly smaller.

## Theorem 1.1

Suppose f is not identically zero and the series converges uniformly on H_b. If f(rho)=0 and Re(rho)>b, then every sufficiently narrow vertical strip around Re(rho) contains infinitely many zeros. More precisely, for every r>0 sufficiently small that the closed disk B(rho,r) lies in H_b and its boundary contains no zero, there are arbitrarily large positive tau such that B(rho+i tau,r) contains a zero, with the same total multiplicity as B(rho,r).

### Proof

Let C be that boundary and let m=min_C |f|>0. Choose a Dirichlet polynomial P(s)=sum_{n<=N} a_n n^{-s} with |f-P|<m/4 throughout H_b. Put c=Re(rho)-r. There are arbitrarily large positive tau such that all numbers exp(-i tau log n), 1<=n<=N, are as close to 1 as desired. Here is an elementary justification that does not assume rational independence. Simultaneous Dirichlet approximation of the finite real numbers log n/(2 pi) gives integers q_Q, 1<=q_Q<=Q^N, for which the distance of q_Q log n/(2 pi) to an integer is at most 1/Q. If these integers are unbounded, take an unbounded subsequence. Otherwise one positive q recurs for unbounded Q, so every q log n/(2 pi) is an integer, and its arbitrarily large multiples are exact periods.

Choose such tau so that sum_{n<=N}|a_n| n^{-c}|exp(-i tau log n)-1|<m/4. For s in C,

|f(s+i tau)-f(s)| <= |f(s+i tau)-P(s+i tau)|+|P(s+i tau)-P(s)|+|P(s)-f(s)| < 3m/4.

Both tail bounds apply because vertical translation stays in H_b. Rouché therefore gives the same number of zeros, counted with multiplicity, for s -> f(s+i tau) and f(s) inside C. This produces a zero of f in B(rho+i tau,r). Choose the shifts successively more than 2r apart. The resulting disks are disjoint, proving infinitely many distinct zeros. QED.

## Consequences and precise boundary

1. A putative single zero rho in H_alpha must satisfy alpha<Re(rho)<=sigma_u. In particular it cannot lie strictly inside the absolute-convergence half-plane, because absolute convergence at a real c gives uniform convergence on H_c by the Weierstrass test.
2. A Dirichlet polynomial with a zero in any open right half-plane has infinitely many zeros in that half-plane. Uniform convergence is automatic for a finite sum.
3. If an ordinary Dirichlet series converges at every complex s, it cannot have a finite nonempty zero set. Indeed convergence at each real c-2 bounds |a_n|n^{-(c-2)}, hence ensures absolute convergence at c; apply the theorem at any zero.
4. Entire analytic continuation alone does not justify consequence 3. The original series must converge everywhere. Local uniform convergence on compact subsets of H_alpha also does not justify the translated tail estimate.

## Additional failed construction: finite cancellation of the zeta pole

Let P be a nonzero Dirichlet polynomial and alpha<1. If P(s)zeta(s) is holomorphic in H_alpha, then P(1)=0, because zeta has a simple pole at 1. Apply Theorem 1.1 to P, with a small disk about 1 lying in H_alpha. There are infinitely many distinct zeros of P in that half-plane. At every such point except possibly 1, zeta is finite and holomorphic. Thus P zeta has infinitely many zeros. A finite Dirichlet-polynomial multiplier cannot both cancel the zeta pole and produce the requested unique zero.

For example, eta(s)=(1-2^{1-s})zeta(s) has explicitly visible zeros at 1+2 pi i k/log 2 for every nonzero integer k. The removable value at k=0 is log 2, not zero. This observation alone already rules out the standard alternating-series shortcut.

## Attempt disposition

This closes the uniform-convergence, everywhere-convergent-series, finite-polynomial, and finite-zeta-regularization subroutes. It does not control the conditional strip sigma_c<Re(s)<=sigma_u. That strip is precisely where an ordinary-series solution could occur. Estimated progress toward an unconditional full resolution: 0%; the scoped obstruction is complete.
