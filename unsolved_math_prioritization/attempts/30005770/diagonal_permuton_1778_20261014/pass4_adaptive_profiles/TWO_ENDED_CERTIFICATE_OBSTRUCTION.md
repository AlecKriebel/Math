# The strongest two-ended local certificate is also defeated by canonical mountains

Shared PASS4, row 1778 / 30005770, 14 October 2026. This upgrades the frozen single-ended certificate obstruction after the independent gap lane added terminal-cell rerooting. It leaves the original proofs unchanged.

## The two-ended quantity

With e(x,y) and gamma as in EXACT_CANONICAL_WINDOW_OBSTRUCTION.md, define

    V_K^pm=min_{x_j>=0, sum x_j=1}
        max_(1<=j<=K) max{
          gamma*x_j-e(x_(j-1),x_j),
          gamma*x_j-e(x_j,x_(j+1))},
    x_0=x_(K+1)=0.                                         (1)

The independent TWO_ENDED_WINDOW_GAPS.md proves that this exact minimax is a positive lower certificate for delta_K=log(lambda/g_K), using both endpoint tails and exact rerooting counts. Here we need only its definition in(1). No equality with the true delta_K is assumed.

For K>=1 put

    T_(2h)=2(2^h-1),        h>=1,
    T_(2h+1)=3*2^h-2,      h>=0.                            (2)

## An explicit upper envelope for the certificate

For every K,

    V_K^pm<=gamma/T_K.                                     (3)

Proof. Take z_j=2^(min(j,K+1-j)-1) for1<=j<=K, and normalize x_j=z_j/T_K. The sum of the z_j is exactly T_K. At an endpoint the outward-neighbor penalty is gamma/T_K. At every non-endpoint the smaller neighboring mass is half the current mass; the other is at least half. Thus each of its two penalties is at most

    x_j[gamma-H(1/2)]<0.

For K=2 only the endpoints exist, and the penalty using the other endpoint is negative. For K=1 the only mass is1 and the maximum is gamma, consistent with T_1=1. The maximum for this test vector is gamma/T_K, proving(3). QED.

## Exact minimum boundary ratio for center-containing mountain windows

For the normalized symmetric geometric profile p_j=(1/3)2^(-|j|), let a window be[-u,v], with u,v>=0 and K=u+v+1. Put H=H(1/2). Its exact boundary ratio is

    E/M=H [2^(-u)+2^(-v)]/[3-2^(-u)-2^(-v)].                (4)

For fixed u+v=K-1, the sum s=2^(-u)+2^(-v) is minimized when u and v differ by at most1. This follows by transferring one unit from the larger index to the smaller whenever they differ by at least2: the sum strictly decreases. The function s/(3-s) is increasing for0<s<3. Substitution of the balanced values into(4) therefore gives the exact lower bound

    E/M>=H/(2^h-1)=2H/T_K,       K=2h,
    E/M>=2H/(3*2^h-2)=2H/T_K,    K=2h+1.                   (5)

The odd formula includes K=1. Equality is attained by the balanced choices of u and v. Since2H>gamma, equations(3)-(5) yield

    E/M>V_K^pm                                              (6)

for every center-containing finite window.

## Finite canonical witnesses and all locations

Use the actual canonical increasing-cell mountains pi_m established in the main obstruction note. For every fixed B>=1 and m>B, each center-containing window of width K<=B has its two outside neighbors present and exactly the ratios in(4), so(6) holds without a limiting argument.

A window wholly on one side has total mass M<2a, where a is its inward endpoint mass, and an outside inward neighbor of mass2a. Consequently

    E/M>H(1/2)>gamma>=V_K^pm,                               (7)

including when the outer endpoint is the end of the finite chain. Thus every nonempty window of width at most B in pi_m has strictly negative score M V_K^pm-E.

The obstruction also holds when a window of actual width K is counted under a larger cap L>=K: V_L^pm is nonincreasing in L, by appending a zero coordinate in(1). Hence a cap's certified score cannot be larger. The all-location statement includes the central cell of mass greater than1/3.

## Combined conclusion and remaining scope

The actual canonical mountains defeat every bounded adaptive-window rule based on the strongest two-ended profile-minimax certificate supplied in this pass. The exact one- and two-cell true-gap comparisons in SMALL_WINDOW_TRUE_GAPS.md still apply, so improving those two widths to their true gaps does not repair the criterion either.

This is a stronger obstruction than the single-ended certificate result, because both incoming- and outgoing-edge reroot losses are now optimized jointly over the size profile. It still concerns this specified collection of local penalties. Better estimates for the actual delta_K, or joint counting information not represented by these penalties, may overcome the boundary entropy. No upper bound on the true delta_K for all K is proved, and no positive uniform probability for the witness family follows.

The conditional theorem based on divergence of sum_K delta_K is unaffected. The universal target and its1324 case remain unresolved.
