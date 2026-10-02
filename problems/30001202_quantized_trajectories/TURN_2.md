# Turn2: continuous dynamics with unique infinite codes but no uniform finite-window localization

AI-assisted proof attempt; independent review pending. Original quantitative question unresolved.

This turn checks a tempting compactness shortcut. Compact X and continuous f do NOT suffice to turn injectivity of the complete forward quantized itinerary into uniform shrinking finite-horizon feasible sets when partition cells need not be closed.

Set p=0,q=2, a_n=1/(n+2), b_n=2+1/(n+2), n≥0, and
X={p,q} union {a_n,b_n:n≥0} subset R.
This set is compact. Define f(p)=p,f(q)=q,f(a_0)=p,f(b_0)=q, and f(a_n)=a_(n−1),f(b_n)=b_(n−1) for n≥1. It is continuous on X: all nonlimit points are isolated and f(a_n)→p,f(b_n)→q. It extends to a continuous map R→R, for example by the following formulas on consecutive intervals:
- x≤0:0;
- 0≤x≤1/3:x/(1−x);
- 1/3≤x≤1/2:3/2−3x;
- 1/2≤x≤2:(4/3)(x−1/2);
- 2≤x≤7/3:2+(x−2)/(3−x);
- 7/3≤x≤5/2:19/2−3x;
- x≥5/2:2.
The endpoint values agree and all stated orbit values are exact.

Partition X into five disjoint cells:
P_0={a_n,b_n:n≥1}, P_1={a_0}, P_2={p}, P_3={b_0}, P_4={q}.
Every infinite itinerary is unique. The code of a_n is n zeros, then1, then infinitely many2s; the code of b_n is n zeros, then3, then infinitely many4s. The two limit points have constant2 and constant4 codes. This includes n=0 correctly.

Yet for every finite T the observed all-zero word of lengthT+1 is realizable. At time t its exact feasible set is
Q_t={a_m,b_m:m≥T+1−t}.
Proof: precisely the initial indices n≥T+1 remain in P_0 at every observed time; at time t their index is n−t. In particular Q_t contains a_m and b_m with distance exactly2. Thus diam(Q_t)≥2 for EVERY t in EVERY such observation window, however large T is. The sets can be proper subsets of P_0 while retaining macroscopic diameter. Neither unique infinite observability nor the turn1 strict-containment test guarantees uniform finite-window accuracy.

There is no contradiction with pointwise reconstruction: for each fixed initial point its own distinguishing nonzero symbol eventually appears. The bad initial points depend on T. The all-zero infinite word has no realization, although every finite prefix does. The failure of the compactness argument is exactly that P_0 is not closed; its closure contains p and q, both fixed and differently labelled.

This is a counterexample to the proposed sufficient conditions, not to the source's exact forward/backward optimality or to a theorem imposing a closed observation relation, expansivity, or a specified hyperbolic neighborhood. It satisfies the source's actual compact-X/finite-partition/known-continuous-map setting. No smoothness assertion is made for the piecewise extension.
