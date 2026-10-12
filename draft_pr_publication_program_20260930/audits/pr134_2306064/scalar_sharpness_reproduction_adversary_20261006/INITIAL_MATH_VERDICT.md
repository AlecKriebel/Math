# Independently frozen initial mathematical verdict

Inputs read before this freeze: original CANDIDATE.md, source_record.json, readiness.json only. No original REVIEW, independent code/results, author code/results, or other-family conclusion has been inspected. The readiness metadata includes its historical verdict, but this conclusion follows from the independent derivation below.

## Exact claim and initial verdict

For normalized analytic f(z)=z+sum(n>=2) a_n z^n, real alpha, and k given by the candidate, sum n[1+k(n-1)]|a_n|<=1 implies nonvanishing of f/z and f' and Re J_alpha>0 in the open disk. This claim is valid. For 0<alpha<=1, k is minimal among nonnegative lambda in the stated universal strict weighted-sum implication, even restricting to quadratic polynomials with f/z and f' nonzero. This sharpness claim is valid. No novelty finding follows from either conclusion.

## Independent constrained optimization

Let t_n=|a_n|, X=sum(n-1)t_n, Y=sum n(n-1)t_n, B=sum n t_n, A=B-X, and D=1-B. For lambda>0 and B+lambda Y<1, let u=X/D and v=Y/D. Then u>=0, v>=2u, and v<1/lambda. The scalar majorant is

    F(u,v)=a u/(1+u)+b v,
    a=|1-alpha|, b=|alpha|.

It is increasing in both coordinates (strictly in v when b>0). Consequently

    sup F = a/(1+2lambda)+b/lambda.

This is an exact supremum, not a relaxed unsupported bound: a single n=2 coefficient, tending to t_2=1/[2(1+lambda)] from below, gives u->1/(2lambda), v->1/lambda. Solving sup F=1 gives 2lambda^2-(a+2b-1)lambda-b=0. Since b>0 for alpha!=0, its roots have opposite signs, and the positive root is exactly the candidate k. Therefore strict moment feasibility gives F<1. The algebraic branches are d=alpha on [0,1], d=-3alpha for alpha<0, and d=3alpha-2 for alpha>1.

For alpha=0, b=0 and lambda=k=0. B<1 suffices and X/(1-A)<1 follows exactly from X=B-A; no finite second moment is required. For identity, J=1. For boundary equality, f_R=f(Rz)/R has strict weighted sum for every 0<R<1 unless f is identity; every interior point and its nonvanishing expressions is recovered by selecting |w|<R<1. Thus <=1 does not entail loss of strict positivity in the open disk. Equality/possible zeros on |z|=1 are outside the claim.

## Independent analytic connection

For |z|<1, f/z=1+sum a_n z^(n-1), f'=1+sum n a_n z^(n-1), and f'-f/z=sum(n-1)a_n z^(n-1). The weighted bound makes B<1 in the strict case, A<=B/2, and (when alpha!=0) Y finite. Triangle inequalities give |zf'/f-1|<=X/(1-A), |zf''/f'|<=Y/(1-B). These, the exact scalar supremum, and absolute values of the real multipliers prove |J-1|<1. Analyticity justifies derivatives locally even at alpha=0 when Y need not be finite. The second quotient is never estimated at alpha=0.

## Quadratic sharpness independent calculation

For f=z-c z^2, x=cz,

    J=[1-(4+alpha)x+4x^2]/[(1-x)(1-2x)].

For 0<alpha<=1, the root c*=1/[2(1+k)] is in (0,1/2), and the numerator derivative 8x-(4+alpha)<0 on [0,1/2). Any lambda<k admits c*<c<min(1/2,1/[2(1+lambda)]). Then the lambda coefficient sum is strict while J<0 at any real c*/c<z<1. f/z and f' are nonzero throughout the disk because c<1/2. At alpha=0, zero is already minimal in the stipulated nonnegative parameter domain. At alpha=1, k=1 and the same argument applies.

The exact naive-interpolation witness alpha=1/2,c=8/25,z=31/32 gives x=31/100, numerator -53/5000, denominator 1311/5000, and J=-53/1311; its naive weight is 24/25.

## Distinct families and limits considered before freeze

For f=z-c z^N, N>=2, x=c z^(N-1), direct algebra gives J=[1-(2N+alpha(N-1)^2)x+N^2 x^2]/[(1-x)(1-Nx)]. For 0<alpha<=1 its positive-root obstruction to weights has lambda_N solving N lambda_N^2-alpha(N-1)lambda_N-alpha=0. The map N lambda^2/[1+(N-1)lambda] increases with N for 0<=lambda<=1, so lambda_N<=lambda_2=k, strictly for alpha<1,N>2; at alpha=1 all equal one. Higher single-degree negative coefficients do not strengthen the claimed obstruction.

For alpha<0, write q=-alpha. The numerator along x>0 is (1-Nx)^2+q(N-1)^2 x>0, so this real ray does not furnish a counterexample. Along the opposite phase x=-c it becomes (1+Nc)^2-q(N-1)^2 c, exposing a distinct potential outside-interval mechanism. The candidate makes no outside-interval minimality claim. Complex phases and multiple degrees remain covered rigorously by the scalar majorization; numerical searches can test implementation but cannot upgrade the proof or priority status.

k is continuous at 0 and 1. As alpha->0+, k~sqrt(alpha/2); as alpha->0-, k~sqrt(-alpha/2). As alpha->+infinity, k=(3/2)alpha-2/3+O(1/alpha); as alpha->-infinity, k=-(3/2)alpha+1/3+O(1/|alpha|). Large parameters tighten the bound; no division-by-zero inference is needed at alpha=0 because that case is separate.

## Remaining audit work

Reproduce complete author and independent receipts in isolated copies; inspect code scope, numerical sampling versus exact proof, negative controls, optimized assert erasure; only after this frozen initial conclusion inspect actual original reviews. Original 17 files will remain unchanged. This is a reproduction/adversarial audit, not additional central proof-search; original substantive approach accounting remains 1/5 and added central proof-search is zero.
