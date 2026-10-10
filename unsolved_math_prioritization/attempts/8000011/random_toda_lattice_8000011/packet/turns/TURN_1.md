# Author turn 1: deterministic all-coupling bounds

2026-10-03 06:17 UTC. Original target unresolved. This is a deterministic reduction and fixed-sample asymptotic, not an expectation theorem. Progress estimate: 10% toward a quantitative partial; 0% toward full general-n, general-epsilon resolution.

## Convention and classical input

Use the source Lax clock J'=[B,J], B=J_+−J_−, and eventual descending eigenvalue order. Let lambda_1<...<lambda_n be the spectrum and let w_j be the squared first eigenvector components, all positive, sum w_j=1. Under this clock the spectral weights are proportional to w_j exp(2 lambda_j t). The standard finite Toda moment/Hankel formula gives

 tau_k(t)=sum_(|I|=k) (prod_(j in I) w_j) Delta(lambda_I)^2 exp(2t sum_(j in I)lambda_j),
 tau_0=1,
 b_k(t)^2=tau_(k−1)(t) tau_(k+1)(t)/tau_k(t)^2.

This formula follows by Gram determinants for monic orthogonal polynomials with measure sum w_j exp(2lambda_j t) delta_lambda_j; the squared recurrence coefficient is the ratio of consecutive Hankel determinants. The weight evolution and this formula are classical inputs credited to Moser's finite Toda solution. They are not a new integrability claim.

## Explicit envelopes

Let I_k={n−k+1,...,n}, S_k=sum_(I_k)lambda_j, and A_k=(prod_(I_k) w_j) Delta(lambda_(I_k))^2. Set A_0=1, S_0=0, M_k=tau_k(0)/A_k, so M_0=M_n=1. All coefficients are positive and I_k uniquely maximizes the exponent, hence

 A_k exp(2S_k t) <= tau_k(t) <= M_k A_k exp(2S_k t), t>=0.

For 1<=k<n let
 d_k=lambda_(n−k+1)−lambda_(n−k),
 c_k=sqrt(A_(k−1) A_(k+1))/A_k,
 L_k=c_k/M_k,
 U_k=c_k sqrt(M_(k−1) M_(k+1)).

Then for every t>=0,

 L_k exp(−d_k t) <= b_k(t) <= U_k exp(−d_k t).              (1)

Consequently, with [x]_+=max(x,0),

 max_k [log(L_k/epsilon)]_+/d_k <= T_all(epsilon)
 <= max_k [log(U_k/epsilon)]_+/d_k.                         (2)

For the strict threshold, the upper endpoint is interpreted as an infimum: every time strictly larger than the displayed upper bound has all couplings strictly below epsilon. The lower bound holds for every point of the stopping set, so for its infimum. No monotonicity of b_k or of their maximum is assumed. In particular T_all is not replaced by a last exit or a maximum of individual first crossings.

Writing d=min_k d_k and H=max_k(max(|log L_k|,|log U_k|)), for 0<epsilon<=1 and ell=log(1/epsilon), (2) implies

 |T_all(epsilon)−ell/d| <= H/d.                            (3)

For the lower inequality select an index with d_k=d; for the upper use d_k>=d and log U_k<=H. Thus samplewise

 T_all(epsilon)/log(1/epsilon) -> 1/d as epsilon downarrow0. (4)

This alone does NOT justify interchanging expectation and limit. The random envelope H/d has inverse-gap and logarithmic norming-constant singularities. The next substantive step must establish its integrability under the declared GOE ensemble, rather than use qualitative almost-sure convergence as a substitute.

## Boundary and nonmonotonicity warning

For n=1, T_all=0 by the empty-maximum convention; formulas involving d apply only for n>=2. Simple spectrum and strictly positive weights hold almost surely for tridiagonal GOE. For epsilon>=max b_k(0), the first-crossing time can be zero even if a coupling later rises above epsilon. For example n=2, spectrum {0,4}, weights (99/100,1/100), initial b=4 sqrt(99)/100<1/2, but its later maximum is 2. This forbids a naive survival-probability identity P(T_all>t)=P(max b_k(t)>=epsilon).

## Remaining gap

Prove E[H/d]<infinity for every fixed n; then (3) supplies a controlled expectation asymptotic. Even that would answer only the fixed-n small-epsilon regime, not the original general request.
