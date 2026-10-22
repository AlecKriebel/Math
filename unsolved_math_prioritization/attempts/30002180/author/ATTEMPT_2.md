# Attempt 2: restrict the metric to compact curves

## Objective
Turn directed positivity into a Chern number on curves and seek a contradiction under c1(T_X)_R=0.

## Retained proposition
Under the exact jet hypothesis, there is a constant a>0 such that every holomorphic immersion f:C→X from a smooth connected compact curve satisfies

2g(C)-2 >= a integral_C f^*omega_0 >0,

where omega_0 is a fixed Kähler form on X. In particular the original question has an affirmative answer in dimension one.

## Proof
Because f is an immersion, each jet lift f_j:C→X_j is an immersion: its composite with pi_{j,0} is f. Its image lies in X_j^reg, and df_j(T_C)⊂V_j. Differentiation at level k-1 identifies T_C with f_k^*L_k: it is a nowhere-zero homomorphism of lines, whose image is the tautological line by construction. Dualizing gives f_k^*L_k^*=K_C.

The metric is locally bounded along f_k(C), because this compact image misses Sigma_h. Pulling back its local quasi-psh potentials therefore gives a well-defined curvature current representing c1(K_C). Restriction to holomorphic discs tangent to V_k preserves the curvature inequality. This can also be checked by local convolution of the restricted bounded subharmonic potentials and passing to distributions. Thus

f_k^*alpha >= epsilon f_k^*omega_k.

There is a constant B>0 such that omega_0(d pi_{k,0}(xi),overline{d pi_{k,0}(xi)})<=B omega_k(xi,bar xi) on the compact tower. Applying this to df_k and integrating gives deg K_C >= (epsilon/B) integral_C f^*omega_0. The right side is positive for an immersion. This proves the inequality with a=epsilon/B.

If dim X=1, take f=id_X. Then integral_X c1(T_X)=2-2g(X)<0, so the real class is nonzero. No smoothness or base-induced assumption on the jet metric was added.

## Adjunction obstruction to extending the proof
For an immersed curve, 0→T_C→f^*T_X→N_f→0 is exact. If c1(T_X)_R=0, taking degrees gives deg N_f=2g(C)-2. Positivity of genus is thus compatible with a positive normal degree; it does not force a nonzero ambient first Chern class.

More concretely, suppose n>=2 and c1(K_X)_R=0. Let H be very ample and C a smooth intersection of n-1 general members of |dH|. Adjunction gives

2g(C)-2=(n-1)d^n H^n,
H.C=d^(n-1)H^n,
(2g(C)-2)/(H.C)=(n-1)d.

The ratio grows with d. Consequently testing only these high-degree curves cannot violate a fixed positive lower bound of the type just proved. These calculations are conditional geometric identities, not construction of a jet-negative c1=0 counterexample. The verifier checks their exact arithmetic on an explicit finite grid.

## Exact gap
The hypothesis rules out immersed rational and elliptic curves and, by the independently established entire-curve theorem of Demailly, rules out all nonconstant entire curves. This attempt does not construct a low-genus curve or an entire curve on every compact projective manifold with c1(T_X)_R=0. Neither the normal-bundle identity nor complete-intersection adjunction does so. No blanket assertion about rational curves on all Calabi–Yau manifolds is used.
