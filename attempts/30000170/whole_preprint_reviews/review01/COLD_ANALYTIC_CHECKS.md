# Independent analytic checks, before external reviewer conclusions

Hypotheses are the numbered assertions of the frozen manuscript; no novelty assumption is used. Success requires an actual sequence of ambient proximal normals with a nonproximal limit, the exact local-to-global quantifiers for projection, and a direct neighborhood-uniform finite-subgradient support proof. Finite verifier samples cannot meet those criteria alone.

## Monic normal and all fixed metrics

The proposed roots are `-it` and `-t²+it`. Their sum is `-t²` and product is `t²+it³`, so the factorization and closed-left-half-plane inclusion hold for each real `t>0`. The abscissa-active root is unique and simple: its real part is zero, the other has real part `-t²`, and the derivative denominator is `t²-2it != 0`. The complex implicit derivative at fixed `t` is therefore `-(lambda da+db)/(t²-2it)`.

Multiplying by the conjugate denominator yields the four real gradient components:

```
Re-a: -2/(t²+4)
Im-a: -t/(t²+4)
Re-b: -1/(t²+4)
Im-b:  2/[t(t²+4)]
```

These are exactly `gamma_t n_t`; the positive imaginary-constant sign is essential. `n_t` points outwards from the sublevel set. Smoothness is used at each fixed positive `t`, so no uniform root gap is assumed.

For any fixed SPD real matrix `G`, a local Taylor support `n_t·d <= K_t d^T G d` exists. Expanding distance to `c_t+tau G^-1 n_t` gives `d^T G d - 2 tau n_t·d >= (1-2 tau K_t)d^T G d`; choose `tau` with positive coefficient. Then choose its actual metric step norm smaller than half the local support radius. Any competitor outside that radius has distance to the shifted input greater than the base distance by the triangle inequality. This establishes actual global proximal normal membership at `c_t`, not only a formal constraint gradient. The argument also works for a locally closed set after clipping in an interior neighborhood.

Thus `G^-1 n_t -> G^-1 n_0`, a nonzero limiting normal at zero. For `e=(1,0,1,0), f=(0,0,0,1)`, the path is `t²e+t³f` and the exact distance difference from the candidate base is

```
t^4 (e^TGe+2t e^TGf+t² f^TGf) - 2 tau t³.
```

For each fixed `G` and each fixed positive `tau`, this is negative for sufficiently small `t`. Cross terms, tiny eigenvalues and correlations only change the threshold; they cannot reverse the order-three versus order-four limit. This invalidates even local proximal support for the limit normal. The assertion is pointwise in the fixed metric, with no uniform threshold across all SPD matrices.

The real quadratic formula for the abscissa is continuous, including discriminant zero and the negative ray. Hence the monic stable set is globally closed and nonempty. Every global distance is attained, because a minimizing sequence is bounded by comparison with zero and any SPD norm is coercive in finite dimensions.

The primary projection characterization uses a closed set and a neighborhood of its base point, and the additional single-valued criterion is valid in finite dimensions. Its contrapositive supplies an input in every neighborhood where the projection is not a singleton. Since attainment has separately ruled out empty projection values, there are at least two distinct global nearest points. Stable inputs have exactly themselves as nearest points, so those inputs are unstable. These conclusions do not require identifying the input or its minimizers explicitly.

## Full exact degree and competitors at degree loss

At the same monic points, the additional numerator for leading coefficient differentiation is `lambda² dl=-t² dl`. Real and imaginary leading directions yield `t²/(t²+4)` and `-2t/(t²+4)`, respectively; after dividing by `gamma_t` this is `(t³/2,-t²)`. Thus all six full ambient directions agree with the manuscript, not merely the monic slice. The limit support covector is `(0,0,0,0,0,1)` and the path has zero leading displacement, again producing order-three support and order-four norm in every fixed full SPD metric.

The full set is not globally closed: `(epsilon,0,0)` tends to the forbidden leading-zero polynomial. This does not invalidate local closedness at `(1,0,0)`. Let `G` be fixed, let `A` project to the two leading coordinates, and choose `R` with `||A||_(G->Euclidean) R < 1/2`. Every point in the radius-`R` closed metric ball then has `|ell|>1/2`. On this ball normalization `(ell,a,b)->(a/ell,b/ell)` is smooth and the abscissa continuous. The stable intersection `C` is compact and contains the base in its interior.

For `d=||q-cfull||_G<R/3`, every stable point with distance at least `R` from the base has distance at least `R-d>2R/3` from `q`, while the stable base has distance `d<R/3`. Thus neither boundary nor outside points can minimize. Global nearest points to `C` and the exact-degree set coincide; they exist. The limiting-normal obstruction lies in the interior for all sufficiently small `t`, so clipping cannot remove it. Combining this with the primary closed-set projection theorem gives the full-degree ties. Inputs can also be chosen inside this ball, hence retain exact degree. No competitor approaching leading-zero coefficients can beat the base for these inputs.

## Epigraph and mixed coefficient/height metrics

At `(c_t,0)`, the active root remains unique and the smooth epigraph constraint is `alpha(c)-r<=0`. Its outward covector is `(gamma_t n_t,-1)`; scaling by the positive `gamma_t^-1` gives `(n_t,-1/gamma_t)`. The limit is `(n_0,0)`. In full degree replace `n_t` by `N_t`.

For any fixed joint SPD matrix `H`, `H^-1` turns that covector into its normal vector. The comparison displacement `(c_t,0)` pairs with the limiting covector to `t³`; its joint squared norm is order four with a positive leading coefficient. Therefore the same exact distance difference is negative for small `t`, even when the normal vector acquires a height component. A horizontal *covector* does not imply a horizontal representing vector under a mixed metric. Each moving normal is proximal by the local smooth-boundary argument and small-step exclusion. The monic epigraph is closed; the full epigraph is locally closed in leading-nonzero coordinates and can be clipped. Failure concerns the whole set at height zero, not a specified finite-subgradient direction.

## Stability chart and real edge cases

Substitution `z=w-iy/2` in `z²+(x+iy)z+u+iv` gives `w²+xw+U+iV` with `U=u+y²/4, V=v-xy/2`. The substitution is purely imaginary and preserves root real parts. Put `D'=x²-4U-4iV`. Stability is equivalent to `x>=0` and `sqrt((|D'|+x²-4U)/2)<=x`, hence `|D'|<=x²+4U`. The right side must be nonnegative before squaring.

The squared condition gives `16V²<=16x²U`. If `x>0` this forces `U>=0`; if `x=0`, the unsquared nonnegative-right-side condition forces `U>=0` and then `V=0`. Conversely, `x>=0, U>=0, V²<=x²U` makes the right side nonnegative and permits reversing every step. At `U=0`, `V=0`; the transformed roots are `0,-x`, stable. At `x=0`, `V=0,U>=0`; the roots are imaginary (or both zero). The path has `x=U=t²,V=t³`, which saturates the upper sheet with `x,U>0`.

In the real monic slice `y=v=0`, this reduces to `a>=0,b>=0`. This is convex and closed, so the strictly convex SPD distance objective has a unique minimizer. An arbitrary complex coefficient path cannot be used to refute a real-only problem.

## Positive function condition

Let `Phi(D)=sqrt((|D|+ReD)/2)` and `L=(-infinity,0]`. At `D` outside `L`, differentiation gives gradient components `Phi/(2|D|)` and `ImD/(4|D|Phi)`; their squared norm simplifies to `1/(4|D|)`. At fixed `D=-s<0`, rationalization gives `Phi(-s+h)=|Imh|/(2 sqrt s)+O(|h|²)`. The regular subgradients are exactly the imaginary interval with endpoint magnitude `1/(2 sqrt s)`, the same intervals have local quadratic supports, and the two off-ray gradient limits only add the already present endpoints. Thus regular, proximal and limiting subdifferentials agree there.

For `|D|<=delta`, if `ReD>=0`, `Phi>=sqrt(|D|/2)>=|D|/(2sqrt delta)=dist(D,L)/(2sqrt delta)`. If `ReD<0`, rationalization and `|D|-ReD<=2delta` give that same bound. No division by zero occurs when the rationalized expression is used off zero on this side. For any `q` with `Req>=0`, convex normal support gives `q·D<=|q| dist(D,L)`. Taking `delta` small enough therefore makes `Phi(D)>=q·D`, an actual local linear lower support at zero. Negative-real increments exclude `Req<0`. All finite regular subgradients at zero are proximal. A finite limiting sequence approaching zero cannot come from off-ray gradients (their norm diverges); on-ray intervals have real part zero, and zero-point subgradients have nonnegative real part. This proves all three subdifferentials at zero equal the closed half-plane `Req>=0`, for both proximal-limit and regular-limit conventions.

The smooth coordinate map `T(a,b)=(a,a²-4b)` is globally invertible with inverse `(a,D)->(a,(a²-D)/4)`. Under this diffeomorphism, first-order supports transform via its invertible real Jacobian. Local quadratic supports transform both ways because the maps are C² and locally Lipschitz with bounded second derivatives. Limits transform by continuity of the inverse transpose Jacobian; function attentiveness transfers because the function values are unchanged. This gives exactly

```
v_a=-1/2 + conjugate(a) q,
v_b=-2q,
q in partial Phi(D).
```

At the origin, finite subgradients have `v_a=-1/2` real and `v_b=-2q` with `Req>=0`. In particular the constant component directly prevents cancellation hiding a diverging `q`.

Fix a finite reference `v0`. On any sufficiently small fixed Euclidean neighborhood of it, `|q|=|v_b|/2` is bounded by some `M>=1`. Choose the coefficient neighborhood with `|D|<delta=1/(16M²)`. Any off-ray limiting subgradient is the ordinary gradient and has `|q|=1/(2sqrt|D|)>2M`; therefore every relevant base has `Dx in L`. Its scalar base value is zero and `q in N_L(Dx)`; at a negative-ray point its interval is a subset of that normal line. For arbitrary comparison `Dy` in the same neighborhood, choose the actual convex-ray projection `z`. Then

```
q·(Dy-Dx) = q·(z-Dx)+q·(Dy-z)
          <= M dist(Dy,L) <= Phi(Dy).
```

No comparison subgradient is restricted; this is the required stronger inequality. With `Delta=y-x`, the discriminant identity is exact: `Dy-Dx=JD(x)Delta+(Delta a)²`. Consequently

```
alpha(y)-alpha(x)-v·Delta
 >= (1/2) q·(Delta a)²
 >= -(M/2)|Delta a|² >= -(M/2)||Delta||².
```

Adding curvature `M+1` gives strictly positive slack at least `||Delta||²/2` whenever `y!=x`, as the primary strict definition requires. The coefficient neighborhood and subgradient neighborhood can be shrunk to a common epsilon, and continuity gives the locally l.s.c. requirement. The estimate does not need the base function-value restriction, so it holds in every required attentive sub-neighborhood. Constants depend on `v0`; demanding one bound for all unbounded finite subgradients would be a stronger, unproved statement.

Independent adversarial check on the curvature sign: take `q=M` real, `a_x=D_x=0`, `a_y=i tau,D_y=0`, so `b_y=-tau²/4`. Both scalar Phi values vanish and `alpha` is zero at both points, but `v_b=-2M` gives a deficit `-M tau²/2`. Squared coefficient displacement is `tau²+tau^4/16`; required curvature tends to `M`, showing that reference dependence and the sign of the quadratic remainder matter. The manuscript uses the correct sign.

The normal witness in the set proof comes from gradients whose imaginary-constant component is `gamma_t`, diverging as `1/(2t)`. It cannot remain in a neighborhood of one finite `v0`. A whole-epigraph failure through the horizontal covector is therefore compatible with the positive function condition at every finite limiting subgradient; there is no circular inference from one to the other.

Cold analytic verdict at this checkpoint: no mathematical defect found in Theorem 1, Remark 2, or Proposition 3. Publication/source consistency and literature bounds still require separate inspection.
