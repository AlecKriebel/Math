# Independent theorem and proof reconstruction

This reconstruction was recorded before consulting any past mathematical or priority acceptance verdict. Its evidence is the finished `note.tex` and the primary OWR text, not accepted audits.

## Exact target

OWR 6/2009 printed pages 421–422, item (16), Conjecture 1 uses the positive round conformal Laplacian Y=Delta+n(n-2)/4, smooth strictly positive W, integral W^(n/2)=round volume, and W^(-1/2) Y W^(-1/2) on the unweighted round L2 space. The asserted maximum comparison is universal over n>=3. A single n=3 instance exceeding the round maximum refutes exactly that assertion. It says nothing about the n>=4 restriction or Conjecture 2's separate monotonicity assertion.

## Smooth finite geometry

Under stereographic radius r=e^s the unit round sphere has g0=sech(s)^2(ds^2+gS2). Put L=10000, q=|s|-L/2 and u=exp[-chi(q) log cosh(q)], where chi is the specified smooth flat-endpoint step. Then u=1 throughout the cylinder, u=sech(q) beyond either transition, and it is identically 1 near the nonsmooth coordinate |s| at s=0. Its transition jets match to all orders. Near either omitted pole, rho=e^(-|s|) and algebra gives W_L=e^L(1+rho^2)^2/(1+e^L rho^2)^2. This is a smooth positive Cartesian radial coefficient at rho=0. Every parameter is fixed and finite; e^10000 need not be numerically evaluated.

Each side's cap integral is <1+8/(3e^3)<2, since u<=1 on q in [0,1] and sech(q)^3<8 exp(-3q) after q=1. Thus 4pi L<=V_L<4pi(L+4). With a=(2pi^2/V_L)^(2/3), h=a g_L and W=a W_L have exactly round volume. All coefficients and inverses are smooth and bounded on the compact sphere.

## Correct operator and form comparison

In three dimensions the geometric operator is Delta+R/8. Conformal covariance gives Y_h=W^(-5/4)Y0 W^(1/4). The map U:f -> W^(3/4) f from L2(dV_h) to round L2 is unitary. Therefore UY_hU^(-1)=W^(-1/2)Y0W^(-1/2). Its quadratic form is the positive round Yamabe form of W^(-1/2)f, giving lambda1>=3/(4 max W)>0. This does not assume pointwise positivity of transition curvature.

On the exact cylinder R=2 and the constant-angular Dirichlet modes have Rayleigh values mu_k=1/4+(pi k/L)^2. Zero extension of each sine belongs to global H1 because its boundary trace is zero; only its derivative jumps, not its value. Its norm and form integrals are supported on the cylinder. The first k trial modes span a k-dimensional subspace with maximum quotient mu_k. Full-index min-max yields lambda_k(g_L)<=mu_k, even if nonconstant angular or cap modes intervene; no subset-index inference is used. Every finite partial heat sum dominates exp(-1) sum exp(-4pi^2k^2/L^2), and monotone limits give the infinite trace bound. A decreasing Gaussian sum is >= its integral from 1 onward, yielding L/(4sqrt(pi))-1.

Rescaling has Y_h=a^(-1)Y_gL and t*=4a. The product of t*^(3/2) and trace is (16pi^2/V_L)Tr(exp(-4Y_gL)). Substitution of the strict upper volume bound yields >sqrt(pi)/e (L-4sqrt(pi))/(L+4). Independently tracking each monotone constant replacement gives > (1772/2719)(10000000-7092)/10004000=1106714561/1700054750>13/20.

## Round all-time comparison

The j-th grouped round eigenvalue is j^2-1/4 with multiplicity j^2, j>=1. Gaussian Poisson differentiation gives the printed formula. For 0<t<=7/5, all dual corrections are negative, and sqrt(pi)/4 exp(t/4) is bounded by (1773/4000) exp(7/20). For t>=7/5 split off A=t^(3/2)exp(-3t/4). A increases through t=2. The remaining terms decrease already for t>=2/5. Their j>=3 consecutive ratio is <=(16/9)exp(-7t)<1/2; summing the geometric majorant yields D(t)=t^(3/2)[4exp(-15t/4)+18exp(-35t/4)]. On each of the six printed intervals [a,b], F0<=A(b)+D(a). Exact rational Taylor reciprocals and upper square-root bisection must still be independently replayed and matched to all seven displayed rational enclosures. For t>=2 every grouped term is nonincreasing, so the final region's bound also covers all large times. The claimed maximum bound is <321/500, below 13/20.

## Attainment and outstanding checks

For a fixed normalized smooth metric the heat coefficient limit is sqrt(pi)/4. Positivity gives t^(3/2)Tr(exp(-tY))->0 at infinity. The weighted value >13/20 lies above the zero-time limit, so continuity implies a maximum at a finite positive time. The round first mode at t=2 is 2sqrt(2)exp(-3/2)>sqrt(pi)/4 because 128>pi e^3, so its maximum is attained as well.

At this checkpoint the analytic chain has no identified gap. The remaining review obligations are exact rational replay, all seven displayed constants, executable safety/integrity controls, relocated normal and optimized portable/outer checks, original/archive/mapping identity, independent priority source inspection, metadata consistency, and all-page PDF visual QA. Mathematical novelty and firstness are not inferred from this derivation.
