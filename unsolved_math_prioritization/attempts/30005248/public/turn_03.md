# Attempt 3: symmetry and the meaning of local minimax

## Exact obstruction to reference heterogeneity

Suppose a group acts by measurable bijections g on the sample space, preserves the model class P, and satisfies rho(gP,gQ)=rho(P,Q). Transform each of the n observations by g. The transformed experiment under P is exactly the experiment under gP. For any estimator T_Q, define T_{gQ}(x)=T_Q(g^{-1}x). For every loss depending only on estimation error, its risk at gP with reference gQ equals the original risk at P with reference Q. Taking suprema and infima in both directions proves R_n(gQ)=R_n(Q).

The identical argument transports tolerant tests with thresholds nu and epsilon. If the action is transitive on admissible reference laws, both minimax estimation and tolerant testing are exactly reference-independent.

Example: unrestricted N(theta,I_d) location models and rho(N(theta,I_d),N(theta_0,I_d))=||theta-theta_0||_p. Translation makes every reference equivalent, for every p for which the norm is defined. This does not compute the rate, but prevents reference heterogeneity in this model. A bounded or non-translation-invariant parameter class would invalidate this argument.

## Shrinking neighborhoods produce a different question

For iid Bernoulli(p), define

L_n(q,r)=inf_T sup_{|p-q|<=r, 0<=p<=1} E_p |T-|p-q||.

For 0<r<=1/4, elementary bounds give

L_n(0,r) comparable to min(r,sqrt(r/n)),
L_n(1/2,r) comparable to min(r,1/sqrt(n)).

Upper bounds: use either the zero estimator or the empirical plug-in. At q=0 its expected error is at most sqrt(r/n); at q=1/2, the reverse triangle inequality bounds error by |p_hat-p|, with expectation at most 1/(2sqrt(n)).

Boundary lower bound: take p_0=r/2 and p_1=p_0+h, where h=(1/8)min(r,sqrt(r/n)). Both parameters are in [0,r], and their functional values differ by h. The Bernoulli inequality

KL(Ber(p_1)||Ber(p_0)) <= h^2/[p_0(1-p_0)] <= (8/3)h^2/r

gives product KL at most 1/24. Hence TV<=sqrt(1/48), and the nearest-value testing argument gives maximum absolute-error risk at least h(1-sqrt(1/48))/4.

Interior lower bound: take p_0=1/2 and p_1=1/2+h with h=(1/8)min(r,n^{-1/2}). Product KL<=4nh^2<=1/16. The same argument gives risk at least h(1-sqrt(1/32))/4.

For r=n^{-1/2} and n>=16, the rates are n^{-3/4} and n^{-1/2}, respectively. This is a second rigorous example of heterogeneity, now under an explicitly neighborhood-local criterion.

## Outcome

Symmetry gives a sufficient criterion for absence of reference dependence; boundaries can yield it. These are elementary demonstrations, with no novelty assertion. They do not identify all causes of heterogeneity or solve the high-dimensional density problem. Importantly, the Bernoulli neighborhood risk above must not be substituted for the fixed-reference, global-over-P risk in Attempts 1–2.
