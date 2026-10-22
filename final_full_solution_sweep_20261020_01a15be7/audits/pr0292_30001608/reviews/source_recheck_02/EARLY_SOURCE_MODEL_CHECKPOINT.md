# Independent checkpoint before candidate-proof access

Recorded: 2026-10-21T03:22:01.337913+00:00
Review completion estimate: 35%. This is progress toward this bounded source/model and distinct stochastic review, not toward proving the conjecture.

## Exact claim fixed independently

For every fixed real lambda > 0, on nonnegative integer states s=(a,b,x,y), D=x+y+1, the chain has these six off-diagonal transitions:

| increment (a,b,x,y) | rate |
|---|---|
| (1,0,0,0) | lambda/2 |
| (0,1,0,0) | lambda/2 |
| (-1,0,1,0) | a(x+1)/D |
| (0,-1,0,1) | b(y+1)/D |
| (0,0,-1,0) | x(y+1)/D |
| (0,0,0,-1) | y(x+1)/D |

The target is irreducibility plus positive recurrence (not only almost-sure return or bounded finite trajectories). A and B contain empty peers that have independently committed to chunk 0 or chunk 1; X and Y contain peers with their respective first chunk. A completed peer leaves immediately. One permanent seed supplies the +1 terms. Empty peers are invisible to contacts, giving D=x+y+1 rather than a+b+x+y+1. Figure 2 is authoritative for the count-chain intensities. Counts are Markov because rates depend only on these counts and the source uses exponential/Poisson clocks; failed contacts are null events, not additional state transitions.

For lambda>0, finite prescribed sequences of arrivals, first downloads, and completions have positive probability; every state communicates with zero and conversely, so irreducibility is straightforward. Total N=a+b+x+y satisfies N_t <= N_0 + Poisson(lambda t) pathwise, while total effective rate <= lambda+N. This gives nonexplosion. Boundary states are meaningful: at x=y=0 the first-download rates are a and b, and all completion rates vanish.

## Primary-source findings and limits

- EMS, Oberwolfach Report 48/2010, printed pp. 2782-2783 (PDF pp. 38-39), https://ems.press/content/serial-article-files/46306: one permanent seed, Exp(1) contacts, Poisson(lambda) arrivals, immediate completion departures. The DFC paragraph on p.2782 conjectures stochastic stability despite instability of the large-system limit; the stated objective is stability for any input rate. The subsequent Enforced Friedman question on p.2783 is a different algorithm, not this DFC model.
- arXiv:0910.5577v1, https://arxiv.org/pdf/0910.5577v1, printed/PDF pp.7-9: Figure 2 on p.8 has exactly the six rates above. The 2009 Conjecture 3.4 on p.9 instead conjectures instability for sufficiently large lambda. This historical reversal must not be erased or attributed to the 2011 wording. The arXiv page currently lists only v1 (29 October 2009) and the 2011 journal reference; it does not make its unchanged PDF a 2011 text.
- HAL hal-00781341, https://hal.science/hal-00781341/document: a deposited author-proof PDF, with cover page and QUES9209_source.tex; 5/01/2011 headers. Section 2, proof p.5 (PDF p.6), defines stable as irreducible and positively recurrent. Section 3.2, proof p.10 (PDF p.11), gives Figure 2 and explicitly explains the invisible waiting rooms. Conjecture 3.6 on proof p.12 (PDF p.13) states stability without a load restriction. The surrounding goal of any input rate supports the all-fixed-positive-lambda reading. The footnote records fixed holding times in their simulations; those simulations are evidence only and do not change the continuous-time generator definition.
- Actual publisher landing page https://link.springer.com/article/10.1007/s11134-011-9209-2 confirms authors, publication 26 January 2011, Queueing Systems 67 pp.183-206, but currently exposes subscription preview rather than Section 3.2. A cached purported final-PDF response at the /content/pdf/ DOI URL begins <!DOCTYPE html>, so it is not an independently inspected final publisher PDF. Do not claim publisher-edition body equality from metadata. The inspected 2011 operative body is an author proof, with this precise version limitation.

Primary body hashes and retained retrieval provenance are in PRIMARY_INVENTORY.json. No previous review or candidate proof/checker was read before this checkpoint. Directory filenames and source response records were used only to locate primary bodies.

## Exact generator deductions and a distinct limiting mechanism

Write alpha=lambda/2, u=a(x+1)/D, v=b(y+1)/D, r=x(y+1)/D, s=y(x+1)/D. Then
L a=alpha-u, L b=alpha-v, L x=u-r, L y=v-s, and L N=lambda-r-s.

For initial (a,b,x,y)=(R,b0,n,R), fixed n,b0 and fixed finite time T, as R tends to infinity the locally convergent generator has X births k+1 and deaths k, and B immigration alpha and deaths j. These processes are independent in the limit. Centered A and Y jump by order one on this horizon. Their limiting drift equations give
E X(t)=n+t,
E B(t)=alpha+(b0-alpha)e^(-t),
E[A(t)-R]=(alpha-n-1)t-t^2/2,
E[Y(t)-R]=(alpha-n-1)t-t^2/2+(b0-alpha)(1-e^(-t)),
E[N(t)-N(0)]=(lambda-2n-1)t-t^2.

This rederivation confirms the earlier assigned observation. It identifies the +1 seed immigration as the mechanism absent from the zero-seed fluid boundary. A proof of fixed-horizon moment convergence can use stopping while A,Y remain between R/2 and 2R: there X has a linear pure-birth upper bound, B has a Poisson arrival bound, and their finite-horizon counting processes have moments of every fixed order. Exiting requires order R jumps; high-moment bounds make its contribution vanish. This route is local-in-horizon and local-in-regime. It does not establish a Foster inequality uniform over all imbalanced ratios, n growing with R, b growing with R, or lambda growing with R.

Negative diagnostic: for lambda=10,n=0,b0=5, the limiting expected Y increment is 4t-t^2/2 and total-population increment is 9t-t^2. Both are positive at t=1 and negative at t=10. Thus the boundary mechanism supports eventual restoration over suitable horizons but does not give negative short-horizon total-population drift or recurrence by itself. For A= rho R,Y=R the limiting X births are rho(k+1), deaths k; rho<1 and rho>1 are materially different from the critical rho=1 family. A proof must cover those regimes as well.

## Outstanding obligations

Read the frozen candidate proof only after this checkpoint; test exact generator substitutions and meaningful negative controls; determine whether the full proof supplies a coercive Lyapunov function and uniform finite exception set for each fixed real lambda>0. Source identity alone is not a novelty certificate. External expert input could help resolve any surviving gap, but this project forbids outreach and none is prepared or initiated.
