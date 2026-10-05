# Approach 2: reciprocal zeta and a quantitative convergence condition

This is a conditional construction, not an unconditional solution. The classical reciprocal-zeta route is explicitly mentioned in the later 2017 Oberwolfach problem session and in Broucke–Vindas. The proof below isolates an exact sufficient arithmetic hypothesis instead of silently identifying analytic continuation with convergence.

Let mu be the ordinary Möbius function and M(x)=sum_{n<=x} mu(n).

## Theorem 2.1

If there exist real theta<1 and C>0 such that |M(x)|<=C x^theta for all x>=1, then the ordinary Dirichlet series

F(s)=sum_{n>=1} mu(n)n^{-s}

converges in H_theta and has exactly one zero there, at s=1, of multiplicity one.

### Proof

First theta cannot be negative under this hypothesis: M(n)-M(n-1)=mu(n) and infinitely many primes have mu(p)=-1, whereas both bounding terms would tend to zero. Thus any nonvacuous instance has 0<=theta<1. No change of half-plane is made.

Partial summation, for real X>=1, gives

sum_{n<=X} mu(n)n^{-s}=M(X)X^{-s}+s integral_1^X M(x)x^{-s-1} dx.

For Re(s)>theta the boundary term tends to zero and the integral converges absolutely. On each compact subset of H_theta, its tail is uniformly bounded by a constant times X^{theta-Re(s)}, so F is holomorphic there and the Dirichlet series itself converges there in increasing order.

On H_1 both series F and zeta converge absolutely. Their Dirichlet convolution is the identity because sum_{d|n}mu(d) is 1 for n=1 and 0 otherwise. Hence F(s)zeta(s)=1 on H_1. The classical meromorphic zeta function has only one pole, a simple pole of residue 1 at s=1. The identity theorem extends F zeta=1 throughout H_theta minus {1}; this punctured half-plane is connected. Consequently F(s) cannot vanish at any s other than 1 in H_theta, since zeta(s) is finite at every such point.

Near 1, write zeta(s)=(s-1)^{-1}+h(s) with h holomorphic. On a punctured neighborhood,

F(s)=(s-1)/(1+(s-1)h(s)).

Thus F(1)=0 and F'(1)=1. The zero is simple. QED.

## What is and is not proved

The theorem assumes an ordinary Möbius power saving with an exponent strictly below 1. This attempt supplies no such bound. It is not enough to cite convergence of sum mu(n)/n at the boundary s=1: the required open half-plane must contain that point in its interior.

The familiar Riemann-hypothesis conditional example is consistent with the theorem: the classical implication RH => M(x)=O_epsilon(x^{1/2+epsilon}) supplies a suitable theta. That implication is a credited external theorem, not established by the finite controls in this packet. The result does not assert that Balazard's existence question is equivalent to RH. It concerns one chosen coefficient sequence only.

## Why a subpower saving of the wrong shape does not close this proof

For fixed c>0 and 0<a<1, the expression x exp(-c(log x)^a) is not O(x^theta) for any fixed theta<1. Indeed its ratio to x^theta has logarithm (1-theta)log x-c(log x)^a, which tends to +infinity. Thus an estimate of that form cannot be substituted for the power-saving hypothesis above. This is an exact asymptotic obstruction to this substitution, not a claim about the best available Möbius estimate.

The unresolved step is genuinely arithmetic: prove sufficient cancellation of this fixed coefficient sequence, or change to an unconditional construction whose convergence can be proved. Estimated progress toward unconditional full resolution remains 0%; the conditional implication and simple-zero verification are complete.
