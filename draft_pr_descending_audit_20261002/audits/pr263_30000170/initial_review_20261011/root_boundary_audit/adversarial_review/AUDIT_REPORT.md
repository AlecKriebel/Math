# Independent adversarial audit of the tentative quadratic function lemma

**Verdict: GO for the stated auxiliary function lemma, with the strict-inequality constant repair below.** This is an independent verification of the limited mathematical claim, not acceptance into the preprint, a novelty verdict, or permission to change accepted results A–C. No outside person was contacted. The report was developed from the tentative statement and the primary source, without consulting another agent's conclusion.

## Exact target and conventions

Identify complex coefficient space C² with R⁴ and use the Euclidean norm and real pairing `<q,z> = Re(conjugate(q) z)`. Put

- `L = (-infinity,0]` in C;
- `D(a,b) = a² - 4b`;
- `Phi(D) = sqrt((|D| + Re D)/2) = |Re sqrt(D)|`;
- `alpha(a,b) = -Re(a)/2 + Phi(D(a,b))/2`.

The target is: **alpha is function prox-regular at (0,0) relative to each finite limiting subgradient v0.** The neighborhood and quadratic constant may depend on v0. The target does not assert one uniform constant over all subgradients, or prox-regularity of the whole epigraph at every normal. All functions in this report are finite and continuous; properness and lower semicontinuity therefore hold.

## Primary definition and its quantifiers

Poliquin–Rockafellar, *A Calculus of Prox-Regularity*, Journal of Convex Analysis 17 (2010), 203–210, [primary PDF](https://www.heldermann-verlag.de/jca/jca17/jca0849_b.pdf), Definition 1.1, p. 203, defines the property using limiting proximal subgradients and positive constants epsilon,r. In addition to nearby base and comparison points, the definition restricts the base function value and subgradient to neighborhoods of the reference value and subgradient. It prints a **strict** quadratic lower-support inequality for distinct points. The direct estimate below is non-strict with constant M; taking `r=M+1` gives the printed strict inequality. Thus the tentative proof's final sentence needs this explicit repair, but its target survives.

The same source's p. 205 describes the correspondence with epigraph prox-regularity **relative to the normal (v0,-1)**. This is a correspondence at a specified nonhorizontal normal. It does not equate function prox-regularity at all finite subgradients with set prox-regularity at all epigraph normals. Section 3, Theorem 3.1, gives the standard smooth-composition rule under a horizon-subgradient constraint qualification.

No other chain-rule source is required here: the exact transformations and the limiting-proximal convention are verified below directly.

## 1. Scalar geometry and subdifferentials

Write `D=x+iy`, `r=|D|`.

### 1.1 Away from L

For `D not in L`, `Phi>0` and Phi is smooth, with

    grad Phi(D) = (Phi/(2r), y/(4r Phi)),
    |grad Phi(D)|² = 1/(4r).

The second identity follows directly from `Phi²=(r+x)/2`; it is valid for either sign of y and for the positive real axis. The Fréchet, proximal, and limiting subdifferentials at a fixed smooth point are the singleton containing this gradient. Smooth gradients have unbounded norm as D approaches zero through the complement of L. A bounded limiting subgradient at zero therefore cannot arise from such points. The divergence is a norm statement and cannot be defeated by a direction-dependent component cancellation.

### 1.2 Negative-ray interior

At `D0=-s`, `s>0`, a neighborhood has negative real part. There

    Phi(D) = |Im D| / sqrt(2(|D| - Re D)).

The denominator is smooth and nonzero near D0. Hence, for real increments `h=(h1,h2)`,

    Phi(D0+h) = |h2|/(2 sqrt(s)) + O(|h|²).

Restricting to positive and negative real increments forces `q1=0`; restricting to positive and negative imaginary increments forces `|q2| <= 1/(2 sqrt(s))`. Conversely, each such q has a quadratic lower support by the displayed expansion. Consequently,

    regular Phi(-s) = proximal Phi(-s)
                    = { (0,q2) : |q2| <= 1/(2 sqrt(s)) }.

The limiting subdifferential is the same interval. Indeed, sequences on the ray yield its closed interval limit, and off-ray gradients have the two endpoint limits as they approach the fixed negative point. This covers both imaginary signs and the endpoints, without using the desired coefficient support inequality.

### 1.3 The origin and the sharp distance bound

For any `delta>0` and `|D|<=delta`,

    Phi(D) >= dist(D,L)/(2 sqrt(delta)).                 (S)

Proof: for `x>=0`, the distance is r and `Phi>=sqrt(r/2)>=r/(2sqrt(delta))`. For `x<0`, the distance is `|y|`, and

    Phi(D) = |y|/sqrt(2(r-x)) >= |y|/(2sqrt(delta)).

The identity on L is interpreted directly as Phi=distance=0, including D=0.

The convex normal cone is

    N_L(0) = { (q1,q2) : q1>=0 }.

If `q in N_L(0)` is finite, choose delta so `|q|<=1/(2sqrt(delta))`. Let z be the nearest point of D on L. Convex normal support gives `<q,z><=0`, so

    <q,D> <= <q,D-z> <= |q| dist(D,L) <= Phi(D)

on that disk. Thus every finite normal is a proximal subgradient at zero, with an exact linear lower support. Conversely, `D=-t`, `t>0`, forces `q1>=0` for every regular subgradient. Therefore

    regular Phi(0) = proximal Phi(0) = N_L(0).

For the limiting subdifferential, consider any convergent finite sequence of proximal or regular subgradients at points approaching zero. Off-ray points are impossible eventually along any convergent subsequence, because their gradient norms diverge. Points at zero have `q1>=0`; negative-ray interior points have `q1=0`. Hence every finite limit has `q1>=0`, and all such limits already occur as proximal subgradients at zero. Thus

    limiting-regular Phi(0) = limiting-proximal Phi(0) = N_L(0).

The scalar subdifferential formulas in the tentative lemma are therefore correct under both conventions. The above reasoning also shows their equality everywhere, not just at zero.

## 2. Exact coordinate transformation, with no general chain-rule assumption

The mapping

    F(a,b)=(a,a²-4b)

is a global real C-infinity diffeomorphism, with inverse `(a,D) -> (a,(a²-D)/4)`. Its real Jacobian has block form

    [ I       0  ]
    [ 2A(a)  -4I ],

where A(a) is real multiplication by a. Its determinant is 16. The discriminant map alone has rank two everywhere because its b-block is -4I.

Set `h(a,D)=-Re(a)/2+Phi(D)/2`. The Fréchet subdifferential of h is exactly `{(-(1/2)e_Re a, q/2): q in regular Phi(D)}`: the a part is forced by increments with fixed D, and the D part is the scaled scalar definition. Smoothness of F and its inverse transports first-order lower supports in both directions. It also transports quadratic proximal lower supports in both directions, since the Taylor remainder of each coordinate map is quadratic and the multiplier is finite. Consequently the same exact identity holds for proximal subgradients.

Taking convergent sequences proves the identity for limiting subgradients. In particular, any convergent coefficient subgradient determines a convergent multiplier through the b-component; inverse-Jacobian boundedness also gives this generally. Function-value convergence is preserved since `Phi(D)=2alpha(a,b)+Re(a)` and all functions here are continuous.

Thus for either limiting convention,

    v_a = -(1/2)e_Re a + conjugate(a) q,
    v_b = -2q,                  q in limiting Phi(D).    (C)

There is exactly one q for each v. At zero,

    limiting alpha(0,0)
      = {(-1/2,0,-2q1,-2q2) : q1>=0, q2 real}.

There is no missing finite subgradient and no unbounded q that can be masked by the a-block. Positive scaling and addition of the smooth linear term are included in this direct calculation.

## 3. Uniform finite-subgradient support in coefficient space

Fix any finite `v0 in limiting alpha(0,0)`. Choose `M>=1` large enough that `(|v0_b|+1)/2<M`, and restrict subgradients to `|v-v0|<epsilon<=1`. Equation (C) gives `|q|<=M`.

Take `delta=1/(16M²)` and choose a sufficiently small coefficient ball so every point x in that ball has `|D_x|<delta`. For example, `epsilon<=delta/8` suffices, because `|a|²+4|b|<=epsilon²+4epsilon<delta` there. All comparisons below use this one ball.

If a nearby x with such a v had `D_x not in L`, its scalar gradient norm would exceed `1/(2sqrt(delta))=2M`, contradicting the multiplier bound. Thus `D_x in L`, `Phi(D_x)=0`, and `q in N_L(D_x)`.

For arbitrary y in the same ball, let z be the nearest point of D_y on L. Convex normal support, Cauchy–Schwarz, and (S) give

    <q,D_y-D_x>
      = <q,D_y-z> + <q,z-D_x>
      <= M dist(D_y,L)
      <= Phi(D_y).                                     (U)

No regularity or continuity of a choice of q is needed. This includes x with zero discriminant, ray-interior x, either side of the ray for y, y on the ray, and y=0.

For `Delta=(Delta a,Delta b)=y-x`, the exact identity is

    D_y-D_x = 2a_x Delta a - 4Delta b + (Delta a)².

Substitution of (C) and (U) gives

    alpha(y) >= alpha(x) + <v,Delta>
                           + (1/2)<q,(Delta a)²>
             >= alpha(x) + <v,Delta> - (M/2)|Delta|².     (Q)

The last step uses `|(Delta a)²|=|Delta a|²<=|Delta|²`, in the specified real Euclidean coefficient metric. All factors and signs agree with the tentative derivation.

If `y!=x`, (Q) is strictly larger than the same right side with `r=M+1` replacing M. This meets Definition 1.1, including its positive-r and strict-inequality requirements. The estimate holds for all nearby y and all nearby x with actual limiting subgradients near v0. Since it holds without the base-value restriction, it also holds on the source's smaller function-attentive neighborhood. This completes the target proof.

## 4. Independent horizontal-normal epigraph falsification control

This separate control verifies that the function result cannot be promoted to a whole-epigraph result. It is not needed for Section 3.

Let `E=epi alpha` in R⁵ ordered as `(Re a,Im a,Re b,Im b,z)`. For `t>0`, `s>0`, put

    rho²=t²+s²,
    X(t,s) = (a=0, b=-(t+is)²/4, z=t/2).

The discriminant at X is `(t+is)²`, so `Phi=t`. E is a smooth epigraph near X. A proximal outward normal is

    N(t,s)=(-2rho², 0, -4t, -4s, -4rho²),
    |N|=4rho sqrt(1+5rho²/4).

For positive sigma tending to zero, take

    t=sigma³,  s=sigma,
    h=sigma⁴,  k=sigma³/2,
    X_sigma=X(t,s),
    Y_sigma=X(t+h,s+k),
    n_sigma=N(t,s)/|N(t,s)|.

Both points approach the epigraph origin, and `n_sigma -> n0=(0,0,0,-1,0)`. Thus n0 is a limiting horizontal normal at the origin. First-order terms cancel exactly, leaving

    <N(t,s),Y_sigma-X_sigma>
        = t(h²-k²)+2s h k
        = sigma⁸ - sigma⁹/4 + sigma¹¹.

Moreover,

    |Y_sigma-X_sigma|²
      = |(t+h+i(s+k))²-(t+is)²|²/16 + h²/4
      = (5/16)sigma⁸ (1+o(1)).

It follows that

    <n_sigma,Y_sigma-X_sigma>/|Y_sigma-X_sigma|²
        = (4/(5sigma))(1+o(1)) -> +infinity.

No fixed quadratic upper-support constant can hold at all nearby base points and normals near n0. The indicator-function definition therefore shows that E is **not** set prox-regular at the origin relative to this horizontal normal. The finite-subgradient claim is consistent: the corresponding smooth function subgradient norms diverge, so these normals do not belong to any finite-v0 localization used in Section 3.

## 5. What is elementary and what remains unproved

The scalar mechanism is an elementary sharp distance estimate plus the divergent off-ray gradient norm. Once scalar Phi prox-regularity is established, preservation under this smooth diffeomorphism is covered by Poliquin–Rockafellar 2010, Theorem 3.1: a diffeomorphism has an invertible adjoint Jacobian, so its horizon-subgradient qualification is automatic. Product with a smooth linear coordinate and positive scaling can also be checked directly, as above. Thus this audit does not support novelty for the coordinate pullback step, or any source-intent or historical conclusion. The report independently proves the needed special case instead of importing an unverified calculus assumption.

**Strongest verified result:** the exact quadratic function is prox-regular at the coefficient origin relative to every finite limiting subgradient, with both standard limiting conventions checked and a uniform local support for each fixed finite subgradient. Its whole epigraph fails the corresponding set property at the displayed horizontal normal.

**Remaining mathematical gap for the exact target:** none found. **Remaining promotion gap:** independent broader source/priority review and a human decision are outside this audit. No all-degree, all-polynomial, root-configuration, source-author-intent, or preprint-extension claim follows. In particular, the fixed finite-v0 neighborhood and curvature constant must not be advertised as uniform over unbounded subgradients.

The companion deterministic computation is a reproducibility control, not a proof substitute; every conclusion above follows from the displayed exact identities and inequalities.

## Reproducibility result

`python3 check_controls.py` passes using only Python standard-library Decimal arithmetic at 90-digit precision and seed 26330000170. The saved CONTROL_RESULTS.json records 45 scalar boundary cases, 1,200 coefficient supports, six adverse-curvature zero-set cases, and eight horizontal-normal witnesses. The scalar gradient identity has maximum error 1e-89. The last sigma-scaled horizontal support ratio is 0.799999997999999878 at sigma=1e-8, consistent with the exact asymptotic constant 4/5. Private source reading copies and page images are ignored under tmp/.
