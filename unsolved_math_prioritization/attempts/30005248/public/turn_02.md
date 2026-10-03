# Attempt 2: sharp discrete rates and the failed unrestricted formula

## Existing theorem, with its hypotheses

[Jiao, Han and Weissman (2018)](https://arxiv.org/abs/1705.00807), Theorem 4, concerns independent Poisson counts of means n p_i and known Q. Put

A_n(Q)=sum_i min(q_i,sqrt(q_i/(n log n))),
B_n(Q)=sum_i min(sqrt(q_i),q_i sqrt(n log n)).

For S>=2, under c log S <= log n <= C log B_n(Q), with fixed positive c,C, the minimax squared-error risk is comparable to A_n(Q)^2. Constants depend on c,C. These restrictions matter; this is not an unrestricted all-Q, all-n expression.

For Q=u_S and n comparable to S, B_n(Q)=sqrt(S), and the condition holds with fixed constants for large S. Consequently the Poisson risk has order 1/log S. For Q=e_1, B_n(Q)=1: the theorem does not apply. Attempt 1 instead gives the parametric risk 1/n.

This sharpens the earlier example and predates the 2022 report. It is a credited existing result, not a new resolution.

## Fixed-size transfer, proved explicitly

Write R^F_m and R^P_t for the fixed-m and Poisson-mean-t risks with the same Q. Clip all estimators to [0,2], which cannot increase risk, so squared loss is at most 4.

A Poisson-mean-2m experiment has N~Pois(2m) draws. On N>=m run a nearly minimax fixed-m estimator on the first m observations; otherwise output zero. Therefore

R^P_{2m} <= R^F_m +4 Pr{Pois(2m)<m}.

Conversely, given m draws, generate N~Pois(m/2) independently. On N<=m use the first N observations in a Poisson estimator; otherwise output zero. Thus

R^F_m <= R^P_{m/2}+4 Pr{Pois(m/2)>m}.

Both tails decay exponentially by the Poisson Chernoff bound. If randomized estimators are excluded, conditional averaging reduces squared loss. Applying these inequalities with m=S proves R^F_S(u_S) of order 1/log S. Compared with R^F_S(e_1) of order 1/S, the sharp ratio is of order S/log S.

## Failed extension and obstruction

Blindly asserting R_n(Q) comparable to A_n(Q)^2 for all Q would give R_n(e_1) of order 1/(n log n), contradicting the two-point lower bound. An additional parametric term or a restricted regime is indispensable. Likewise fixed-S, n-to-infinity extrapolation of the large-alphabet formula is invalid.

This route settles a concrete discrete L1 reference-dependence example. It does not provide a theorem covering arbitrary divergences, smooth density classes, or all tolerance levels. The broad source question therefore cannot be closed merely by citing Theorem 4.
