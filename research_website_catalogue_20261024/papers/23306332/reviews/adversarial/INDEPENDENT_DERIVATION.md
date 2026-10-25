# Independent adversarial derivation

The reviewed ambient space is real coefficient space: monic complex quadratics give four real coordinates `(x,y,u,v)=(Re a,Im a,Re b,Im b)`. All stability here is closed half-plane stability. Statements involving every metric mean every **fixed** real symmetric positive-definite matrix, with no uniform constants over metrics.

## Exact stability chart and an alternative normal calculation

Substitute `z=w−iy/2`. The roots' real parts are unchanged and the resulting polynomial is

`w²+xw+U+iV`, where `U=u+y²/4`, `V=v−xy/2`.

If `D=x²−4U−4iV`, the largest root real part is

`[−x+sqrt((|D|+Re D)/2)]/2`.

This follows from the two square roots of `D`; their largest real part is the nonnegative radical. Stability forces `x≥0`. Squaring the nonnegative quantities gives `|D|≤x²+4U`, so the right side must be nonnegative. A second squaring gives `16V²≤16x²U`. Conversely `x≥0`, `U≥0`, `V²≤x²U` give the unsquared bound with its required sign, hence stability. For `x=0`, this correctly gives `V=0` and `U≥0`, including double roots and arbitrary imaginary root pairs.

In original coefficient coordinates this simplifies substantially:

`F(x,y,u,v)=V²−x²U=v²−xyv−x²u`.

Thus `S={x≥0, u+y²/4≥0, F≤0}`. Keeping the `U≥0` inequality is essential; `F≤0` alone admits `(0,0,−1,0)`, whose polynomial has a positive real root.

At `c(t)=(t²,0,t²,t³)`, `x>0` and `U>0`; locally `F≤0` is the sole active condition. Direct polynomial differentiation gives

`∇F(c(t))=(−2t⁴,−t⁵,−t⁴,2t³)=2t³(−t,−t²/2,−t/2,1)`.

This conormal derivation does not use the manuscript's implicit root-derivative formula. The root factorization independently gives `−it` and `−t²+it`, so there is one simple active root and a strictly negative real gap for every fixed `t>0`.

## Proximal membership, all complex competitors, and every fixed metric

For fixed `t`, the polynomial `F` has bounded Hessian on a sufficiently small ball at `c(t)`, hence for every stable `z` in that ball,

`n(t)·(z−c(t))≤K(t)||z−c(t)||_G²`.

Choose `τ>0` with `2τK(t)<1` and `τ||G⁻¹n(t)||_G` less than half that ball's radius. Expanding the squared metric distance proves `c(t)` strictly beats every other stable point inside the ball as a candidate nearest point to `c(t)+τG⁻¹n(t)`. The triangle inequality proves the same against every stable point outside the ball. There is no restriction to real competitors, a parameter slice, a fixed root ordering, or local minimizers. This verifies actual proximal membership.

As `t→0+`, `n(t)→n0=(0,0,0,1)`. Therefore `G⁻¹n0` is a limiting normal. But

`n0·c(t)=t³`, `||c(t)||²=2t⁴+t⁶`.

For an arbitrary fixed SPD `G`, let `T=tr G>0`. For `0<t≤1`,

`||c(t)||_G²≤T||c(t)||²≤3Tt⁴`.

For **any fixed** `τ>0`, choosing `0<t<min(1,2τ/(3T))` yields

`||c(t)−τG⁻¹n0||_G²−||τG⁻¹n0||_G²=||c(t)||_G²−2τt³<0`.

Thus the limiting normal cannot be proximal, even locally. A second check directly violates the uniform local support condition at nearby points: `n(t)·(−c(t))=t³/2`, so the Euclidean ratio is `1/[2t(2+t²)]→∞`. The fixed-metric version follows from norm equivalence. The latter supplies a direct attack on the quantifiers in PRT Proposition 1.2 as well.

The nonproximal-normal inequality does **not** itself identify a target with two minimizing polynomials. The step from non-prox-regularity to such targets uses the actual PRT Theorem 1.3(a)⇔(k), which applies to closed sets and global nearest-point projection in finite dimensions. The continuous radical formula proves `S` closed. A minimizing sequence is bounded by comparison with the stable origin, so every global projection exists. The negation of local single-valuedness therefore gives two distinct attained global nearest points in every neighborhood. A stable input projects only to itself, so each tied input is unstable. No claim that every nearby unstable input has a tie follows.

## Varying leading coefficient and epigraph

Near `ell=1`, normalization is `(ell,a,b)↦(a/ell,b/ell)`. At the path, the two leading coefficient derivatives of normalized coefficients are `(-a,-b)` and `(-ia,-ib)`. Pairing with the independently derived `n(t)` gives `t³/2` and `−t²`, respectively, exactly the two leading entries of the manuscript's `N(t)`. All six real directions are accounted for. The same support-versus-squared-distance comparison applies to the zero-leading-displacement path in dimension six.

The exact-degree set is not globally closed: `(ell,0,0)` with positive `ell→0` is a stable sequence with an excluded limit. Hence direct application of the closed-set theorem to that global set would fail. The manuscript avoids this. A closed metric ball of radius `R` at `(1,0,0)` can be chosen wholly inside `ell≠0`; the clipped stable set is compact and agrees locally with the original. For inputs less than `R/3` from the base, all stable points on or outside the ball have distance greater than `2R/3`, while the base has distance less than `R/3`. Therefore all clipped minimizers are interior and are exactly the global minimizers in the original exact-degree set. This checks both attainment and globality.

At the epigraph boundary, `(n(t),−1/gamma(t))` is a positive scalar multiple of the smooth outward constraint differential `(∇alpha,−1)`. Its limit is `(n0,0)`. In any fixed mixed coefficient/height metric `H`, the normal vector is `H⁻¹(n0,0)`, not the covector itself. The same epigraph competitors `(c(t),0)` give cubic support and quartic squared distance. Full degree again requires local clipping. These are set statements about a horizontal **covector**; an arbitrary mixed metric may give that covector a vector representative with a height component.

## Finite limiting subgradients: an independent quantifier check

Write `Phi(D)=sqrt((|D|+Re D)/2)` and `L=(−∞,0]`. Off `L`, differentiation gives `||∇Phi(D)||=1/(2sqrt(|D|))`. At `D=−s<0`, rationalization gives `Phi(D+h)=|Im h|/(2sqrt s)+O(|h|²)`. Hence regular and proximal subgradients form the imaginary interval `iq`, `|q|≤1/(2sqrt s)`; off-ray limits at the fixed base give its endpoints, and on-ray subgradients give the rest. At zero the distance-to-ray bound

`Phi(D)≥dist(D,L)/(2sqrt delta)`, for `|D|≤delta`,

implies local linear lower support for every finite vector in `N_L(0)={q:Re q≥0}`. Negative real increments exclude every vector with negative real part. Bounded off-ray gradient sequences cannot approach zero. Together these facts prove the regular/proximal/limiting subdifferential claims, rather than just a lower inclusion.

The map `(a,b)↦(a,D=a²−4b)` is a smooth global real diffeomorphism. Transport of regular and proximal lower supports in both directions proves the exact subgradient rule, including the limiting version; no unconditional general chain-rule equality is being assumed. In complex notation,

`v_a=−1/2+conj(a)q`, `v_b=−2q`.

Fixing a finite `v0` first bounds `|q|≤M` for subgradients `v` sufficiently close to it. With `|D|<1/(16M²)`, an off-ray gradient has norm greater than `2M`, so every allowed base lies on `L`. For any comparison `Dy`, a nearest ray point `z` and convex normality give

`q·(Dy−Dx)≤|q|dist(Dy,L)≤Phi(Dy)`.

The identity `Dy−Dx=J_D(x)(y−x)+(Delta a)²` then gives

`alpha(y)≥alpha(x)+v·(y−x)−(M/2)||y−x||²`.

Taking curvature `M+1` makes the PR Definition 1.1 inequality strict whenever the comparison point differs from the base. This bound holds without any extra function-value condition, hence also on the function-attentive neighborhood the definition requires. Constants depend on `v0`.

The subgradient localization cannot be deleted. With `a=0`, `Dx=t²`, `Dy=4t²`, one has `b_x=−t²/4`, `b_y=−t²`, `q=1/(2t)`, and `v_b=−1/t`. The actual support deficit is `−t/4`, while squared displacement is `9t⁴/16`, requiring curvature at least `8/(9t³)→∞`. This checks why unbounded gradients and a horizontal epigraph normal cannot refute the stated finite-relative-subgradient condition.

## Evidence limits

The code `evidence/independent_controls.py` uses exact fractions and encodes discriminants as squares of rational complex numbers, making all radicals used in its support controls exact. It tests the polynomial chart against root-constructed stable and unstable quadratics, normal signs, all leading directions, dense mixed SPD metrics, ray-bound/gradient identities, full coefficient supports, sharp adverse-curvature cases, and deliberately false mutants. These finite checks supplement the arguments above. They do not independently construct an explicit pair of global nearest points; that existential conclusion rests on the verified closed-set projection theorem.
