# Independent derivations used for the source-scope audit

These validate normalization and the already published short complex argument; they are not new proof-search turns or novel discoveries. The real analytic theorem is not certified here.

## Normalization and one-dimensional boundary

For every deterministic matrix X and positive t, ||tX||_*=t||X||_*. Therefore d^-1 E||X/sqrt(d)||_*=d^-3/2 E||X||_*. With eigenvalues x_i of XX*, ||X||_*=Σsqrt(x_i). This verifies both normalization factors separately.

Real scalar X~N(0,1) has E|X|=2(2π)^-1/2 ∫_0^∞ r exp(-r²/2)dr=sqrt(2/π). Standard circular complex Z has density exp(-|z|²)/π, radial density 2r exp(-r²), and E|Z|=2∫_0^∞r²exp(-r²)dr=Γ(3/2)=sqrt(π)/2. Its two real components are independent N(0,1/2), and E|Z|²=1. Using variance1 for each component produces sqrt(2)Z and multiplies every mean by sqrt(2). That change may preserve a monotonicity direction but does not match the requested statistic.

For continuous real shape at N=1 the χ-law yields α_R^(λ)(1)=sqrt(2)Γ((λ+2)/2)/Γ((λ+1)/2). In particular square λ=0 and one-excess-column λ=1 have different starting values sqrt(2/π) and sqrt(π/2). A shape-one result cannot substitute for the square theorem.

## Complex-square universal propagation, with imported recurrence

Let q_n=ETr(XX*)^(1/2), q_0=0. The imported input is the Cunden–Mezzadri–O'Connell–Simm finite-dimensional moment identification, Theorem4.4/formulas(4.11)–(4.12) of the final2019 paper, together with its continuous-dual-Hahn polynomial recurrence. The moment domain Re(k)>-λ-1 contains k=1/2, λ=0. A degree-in-n formula displayed for integer k must not by itself be treated as its fractional continuation; the polynomial identification supplies that continuation. The subsequent remark records the dimension recurrence, and Abreu–Patil Section2.2 explicitly specializes the dual-Hahn recurrence at this fractional order.

The square specialization is q_(n+1)=(2+3/(4n²))q_n-q_(n-1). Positivity of q_n follows from its nonnegative moment integral. Normalize c_n=q_n/n^(3/2) and D_n=c_(n+1)-c_n. For n>=2,

D_n=(A_n-B_n-1)c_n+B_nD_(n-1),
A_n=(2+3/(4n²))(n/(n+1))^(3/2),
B_n=((n-1)/(n+1))^(3/2)>=0.

Set f(x)=(1+x)^(3/2)+(1-x)^(3/2)-2-3x²/4 for 0<=x<=1. Then f(0)=f'(0)=0 and
f''(x)=(3/4)[(1+x)^(-1/2)+(1-x)^(-1/2)-2]>=0
for 0<=x<1, by convexity of t^-1/2. Continuity gives f(x)>=0 also at x=1. Multiplying by (n/(n+1))^(3/2) and taking x=1/n gives A_n-B_n-1<=0.

The exact Laguerre integral values q_1=sqrt(π)/2 and q_2=11sqrt(π)/8 give c_2/c_1=11/(8sqrt(2))<1 because121<128. Thus D_1<0. The recurrence and c_n>0 imply D_n<0 inductively for every integer n>=1. This audits the logical complex-square proof conditional only on the explicitly imported established moment theorem/recurrence. Finite383/53 receipts independently check arithmetic, but are not the universal argument.

The printed Baslingker–Dan scalar statement says x>=0; its real-valued expression is defined on0<=x<=1. Their proof only substitutes x=1/n, so the wider wording does not undermine the exact square result. The candidate source audit already states the correct required domain.

## What these derivations do not certify

No calculation above derives the real LOE one-point correction, justifies all Abel-limit interchanges, or validates the complete Abreu–Patil bound. Those remain external analytic dependencies. The all-d complex propagation cannot remove the bundled real proof hold.
