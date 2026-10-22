# Independent analytic acceptance: height three and size-weight threshold

Final shared PASS5, 14 October 2026.

Reviewed: `pass5_pair_counts/HEIGHT_THREE_SIZE_WEIGHT_BARRIER.md`, SHA-256 `4423d6d5870b46781004ee7642a26fde62e7b03d0c619fd74487cdd22abdbf59`.

**Accepted.** The actual restricted-path growth is at most 6+2sqrt(5), and the stated pure exponential size-weight boundedness threshold is exact. The latter is not a lower bound on the restricted-path growth.

The minimum decomposition gives F_h=1/(1-xF_(h-1)) with F_0=1, including the empty permutation. The displayed F_3 and its two positive partial-fraction coefficients are correct. A*kappa+B*sigma=1 implies the coefficient majorant s_c<=kappa^(c-1) for c>=1; the empty coefficient is not inserted into the transition.

For z<=1/(4*kappa), t=C(kappa*z) lies in (1,2]. The same absolutely convergent row sum as in the height-two theorem gives T_z f<=t*f/kappa. Since kappa>2, this is a strict weighted-supremum contraction even at the endpoint. The starting sum z*t^2 is finite there, so the full restricted-path generating function is finite at that endpoint. Growth at most4*kappa follows. No compactness or asymptotic extrapolation from finite coefficients is used.

For the exact row formula, the first skew block of C starts at its minimum, whose global rank is |C|-d(C)+1. Under S its maximum is therefore at position d(C). Starting U is necessary by the greedy witness and 1324 avoidance; after that first U, the only remaining condition is that an upper point follows the lower maximum. The nongreedy words interleave p-1 upper points and d(C)-1 lower points before that maximum, giving exactly the stated subtraction. It is valid for singleton C and d(C)=1 as well.

A first skew block in H_3 is 1 followed by an arbitrary H_2 state; its remaining skew suffix is any H_3 state. Hence the subtracted row sum factors as x*F_3(x) times the binomial transform of F_2's coefficient sequence. Its coefficients are one at degree zero and 2^(r-1) at positive degree, yielding [1+(1-2x)^(-p)]/2. The first row term follows from the partial fractions and the identity sum_q binom(p+q-1,q)y^q=(1-y)^(-p). Subtracting the empty term gives the exact W_p identity.

For 0<x<1/kappa, the positive term with base (1-kappa*x)^(-1) strictly dominates the base (1-2x)^(-1), the sigma term and all constants. Its coefficient is positive. Therefore W_p(x)^(1/p) has the claimed limit without a hidden cancellation.

For any t>0, applying T_z to its own positive weight vector gives the lower operator-norm test W_p(zt)/t^p. If zt>=1/kappa, a row already diverges, because K(A_p,C)>=1 for every nonempty C. Otherwise its root limit is 1/[t(1-kappa*z*t)]. Above z=1/(4*kappa), the quadratic kappa*z*t^2-t+1 is positive for every t. The root limit exceeds one, so the supremum over p is infinite. This establishes unboundedness on each of these pure-size weighted spaces, using genuine actual-kernel rows rather than a failed upper bound.

The comparison with the inspected BBEPP lower bound does not prove a strict gap. A separate source-status check also rejects a stale newer 10.617 claim, because that claim was explicitly withdrawn. The surviving newer preprint statement remains below 6+2sqrt(5), and its proof has not been independently audited here; see `NEW_LOWER_BOUND_STATUS.md`.

Shape-dependent weights, other function spaces and direct path estimates remain outside the obstruction. No claim about the full uniform-law pair coefficient follows.
