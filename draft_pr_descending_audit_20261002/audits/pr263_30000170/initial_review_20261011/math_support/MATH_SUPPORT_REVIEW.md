# Independent mathematical support review of frozen PR 263 / problem 30000170

Frozen submission: `c4eff3253932a504f8e558c8b5f5b1b5e155de0f`.

Reviewer family: direct complex root differentiation, exact stability chart, limiting versus proximal normals, and support asymptotics. The initial derivation was performed without consulting the frozen independent-review verdict or comparing with the separate projection-family reviewer.

**Mathematical disposition: GO for the precisely scoped complex coefficient Theorems A–C.** No mathematical counterexample or proof gap was found in those statements. Source coverage, campaign completion, and priority/novelty are outside this disposition. The construction gives neither an identified pair of nearest points nor a counterexample to prox-regularity of the abscissa at a fixed finite subgradient. No author research turn was consumed.

## Exact hypotheses and success criterion

The ambient monic space is `(a,b) in C^2`, identified with `R^4` in order `(Re a, Im a, Re b, Im b)`. The full space is `(l,a,b) in C^3`, with `l != 0`; the base is `(1,0,0)`. Stability means every root has real part **at most zero**. Distances use an arbitrary **fixed** symmetric positive-definite real coefficient matrix `G`. The standard metric is `G=I`.

The claims checked are: failure of stable-set prox-regularity at `z^2`; existence of unstable inputs arbitrarily close to `z^2` with at least two nearest stable polynomials; the same conclusion in full exact-degree coefficient space; failure of whole-epigraph set prox-regularity at `(z^2,0)`. The full exact-degree assertions must establish their own ambient normals and ensure that nearby global projections exist despite the globally nonclosed degree restriction.

The primary PRT definition makes set prox-regularity relative to a limiting normal a uniform local nearest-point condition for nearby normals. Its Theorem 1.3(a),(k) equates set prox-regularity and local single-valued nearest projection for closed sets in finite dimension. These are the only projection results imported here; existence and localization are checked below. [Poliquin–Rockafellar–Thibault, 2000, pp. 5233–5234](https://sites.math.washington.edu/~rtr/papers/rtr170-LocalDiffDistance.pdf).

## Independent stability chart and boundary checks

For `a=x+iy`, `b=u+iv`, put `z=w-iy/2`. The resulting polynomial is

    w^2+xw+U+iV,  U=u+y^2/4,  V=v-xy/2.

This translation changes no root real part. Put `A=x^2-4U` and choose a square root of `A-4iV` with nonnegative real part `s`. Independently of the square-root sign,

    s^2 = (sqrt(A^2+16V^2)+A)/2,
    alpha = (-x+s)/2.

Thus stability is exactly

    x >= 0,  U >= 0,  V^2 <= x^2 U.

Proof: `s<=x` forces `x>=0`. Squaring `s<=x` first gives `sqrt(A^2+16V^2)<=x^2+4U`; its right side must be nonnegative. A second squaring gives `V^2<=x^2 U`. If `x>0`, this implies `U>=0`; for `x=0`, the first inequality instead requires `U>=0` and `V=0`. Conversely, the three displayed conditions make the right side nonnegative and both squaring steps reversible. This checks the otherwise delicate `x=0` boundary. If `U=0` and `x>=0`, stability requires `V=0`, also consistent with roots `0,-x`.

In the smooth chart `x>0,U>0`, this is `|V|<=x sqrt(U)`. For

    p_t(z)=z^2+t^2 z+t^2+i t^3=(z+it)(z+t^2-it),  t>0,

the roots are `-it` and `-t^2+it`. The active root is simple, and its strict dominance gap is `t^2`. A sufficiently small neighborhood may depend on `t`; no uniform root gap is assumed. The upper chart constraint is active, and the lower constraint has positive slack `2t^3`.

The upper defining function `phi=v-xy/2-x sqrt(u+y^2/4)` has, at `p_t`, the full gradient

    n_t=(-t,-t^2/2,-t/2,1).

Its sign is outward because increasing `v` violates the active upper inequality. In particular the imaginary linear-coefficient direction is present and has not been silently frozen.

## Independent monic and nonmonic derivatives

At the active root `lambda=-it`, `D=2lambda+t^2=t^2-2it`. Implicit differentiation gives

    d lambda = -(lambda da+db)/D

in the monic space. Taking real parts independently in all four real coefficient directions yields

    grad alpha = (-2/(t^2+4), -t/(t^2+4),
                  -1/(t^2+4), 2/[t(t^2+4)])
               = gamma n_t,
    gamma = 2/[t(t^2+4)] > 0.

For the full polynomial `l z^2+a z+b`, the extra term is `lambda^2 dl`. Its real and imaginary leading-coefficient derivatives are respectively `t^2/(t^2+4)` and `-2t/(t^2+4)`. Therefore

    grad alpha = gamma N_t,
    N_t=(t^3/2,-t^2,-t,-t^2/2,-t/2,1).

These six entries are derived in the full ambient space. The theorem does not infer full non-prox-regularity from a monic slice. The smooth normalization `(l,a,b)->(a/l,b/l)` independently produces the same derivatives.

## Why these are actual proximal normals

At each fixed `t>0`, the stable set agrees locally with a smooth sublevel constraint whose gradient is nonzero. A local Taylor bound gives, for nearby stable `y`,

    <n_t,y-p_t> <= K_t ||y-p_t||^2.

Choose `tau>0` with `2tau K_t<1`. Expanding the squared distance from `p_t+tau n_t` shows that every distinct nearby stable `y` is farther than `p_t`. For competitors outside a chosen radius `r` about `p_t`, choose also `tau||n_t||<r/2`; the triangle inequality rules them out. Hence `p_t` is a nearest point to `p_t+tau n_t`, and `n_t` is genuinely proximal. The same proof applies to `N_t`, to the epigraph normals, and to a closed local truncation in the exact-degree space. There is no assumed uniform bound on `K_t`.

The vectors converge to `n0=(0,0,0,1)` in the monic space and `N0=(0,0,0,0,0,1)` in the full space. Because the base points converge to `z^2` and these are proximal normals, the limit vectors are limiting normals at the base by the limiting-normal definition. Boundedness alone would not have established this membership; the proximal sequence does.

## Support asymptotics and an additional simpler witness

For a fixed scale `c>0`, `c!=1`, comparison with `p_(ct)` gives

    Delta=((c^2-1)t^2,0,(c^2-1)t^2,(c^3-1)t^3),
    <n_t,Delta>=(c-1)^2(c+1/2)t^3 > 0,
    ||Delta||^2=2(c^2-1)^2t^4+(c^3-1)^2t^6.

For the submitted `c=sqrt(2)`, the support coefficient is `2sqrt(2)-5/2>0`, and

    lim_(t->0+) t <n_t,Delta>/||Delta||^2
      = (2sqrt(2)-5/2)/2 > 0.

This analytically proves divergence, rather than extrapolating from a finite list of successful checks.

A still simpler independent check uses the base itself:

    w_t=p_t-p0=(t^2,0,t^2,t^3),
    <n_t,-w_t>=t^3/2,
    <n0,w_t>=t^3,
    ||w_t||^2=2t^4+t^6.

In particular, `n0` is a limiting normal that is **not proximal** at `p0`. For any `tau>0`, compare distances to `p0+tau n0`: the difference between the squared distance of `p_t` and that of `p0` is

    2t^4+t^6-2tau t^3 < 0

for sufficiently small `t`. These competitors approach the base arbitrarily closely. Consequently the fixed-normal local projection condition fails already for `x=p0,v=n0`; this is a direct disproof of set prox-regularity relative to that normal. Alternatively, using `x=p_t,y=p0` violates the uniform quadratic support inequality with a quotient asymptotic to `1/(4t)`. Both checks reinforce the original two-moving-point calculation.

## Universal fixed positive-definite metrics

For any fixed SPD `G`, the covector `n_t` corresponds to the metric normal vector `G^-1 n_t`. The local Taylor and remote-competitor arguments remain valid after replacing Euclidean squared norm by the metric norm, using the positive minimum eigenvalue of `G`. Thus these are metric proximal normals, and their limits are `G^-1 n0`. Pairing with displacement gives exactly

    <G^-1 n_t,Delta>_G = n_t^T Delta.

Write the base displacement as `w_t=t^2 e+t^3 f`, where `e=(1,0,1,0)` and `f=(0,0,0,1)`. Then

    ||w_t||_G^2=t^4(e^TGe+2t e^TGf+t^2 f^TGf),
    lim_(t->0+) ||w_t||_G^2/t^4=e^TGe>0.

Since the support numerator is exactly `t^3`, the quotient still diverges. The same argument uses the zero-leading-coordinate embeddings of `e,f` in dimensions six and seven. This proves the claim for **every** fixed SPD real coefficient metric, including nondiagonal matrices; no inference from mere equivalence of arbitrary norms and no finite metric sampling is used. The argument does not extend to a metric varying with `t`, a semidefinite metric, or a root-matching metric.

For the epigraph with coefficient metric `G` and the ordinary height metric, the limiting metric normal stays horizontal. If one additionally permits SPD matrices mixing coefficient and height coordinates, non-prox-regularity still follows from the same covector argument, but the vector `H^-1(n0,0)` need not be horizontal. Thus the geometric word "horizontal" refers to the usual product metric, or equivalently to the limiting horizontal covector under a general ambient metric.

## Closedness, existence, and full-degree localization

An explicit continuous formula avoids any unexamined root-labeling assumption:

    alpha(a,b)=[-Re a+sqrt((|a^2-4b|+Re(a^2-4b))/2)]/2.

The formula is continuous even at the discriminant zero. Hence the monic stable set is the nonempty closed sublevel `alpha<=0`. Every point has a nearest point: a minimizing sequence is bounded because `p0` is an available finite-distance competitor, and a convergent subsequence realizes the infimum. PRT then turns failure of local prox-regularity into failure of local single-valued projection. Because projections exist, the failure yields at least two points, not an empty projection. An input in the stable set has exactly itself as its distance-zero projection, so the nonunique inputs are necessarily unstable.

For full degree, `alpha(l,a,b)=alpha(a/l,b/l)` is continuous where `l!=0`, so stability is relatively closed there, though generally not closed in all of `R^6`. Choose a **closed metric ball** of radius `R` about `(1,0,0)` small enough that every leading coefficient in the ball is nonzero. Its intersection `C` with the stable set is nonempty and compact. All the normal points and comparison points used above are eventually in the interior of the ball, and their local geometry is unchanged. The same obstruction proves that `C` is not prox-regular at the base.

If `||q-p0||_G<R/3`, any full-degree stable polynomial `s` outside that ball satisfies

    ||s-q||_G >= ||s-p0||_G-||q-p0||_G
                > R-||q-p0||_G > 2R/3.

The competitor `p0` has distance below `R/3`. Thus no point outside the ball can improve the compact-set minimum. Boundary points likewise cannot minimize, and nearest points in `C` and the entire full-degree stable set agree. This proves existence as well as locality for nearby `q`. PRT applied to `C` supplies nonunique projections arbitrarily close to the base, which are therefore nonunique **global** nearest full-degree stable polynomials. The proof works for every fixed SPD coefficient metric, with the localization radius chosen for that metric.

## Epigraph and finite-subgradient boundary

At `(p_t,0)` the monic epigraph is locally `alpha(p)-r<=0`. Its scaled outward gradient is

    v_t=(n_t,-1/gamma)=(n_t,-t(t^2+4)/2),

and in the full space it is `(N_t,-1/gamma)`. Both are proximal at each smooth boundary point and converge to horizontal limiting normals. The comparisons have height displacement zero, so all preceding support calculations are unchanged. In fact the horizontal limit normal at `(p0,0)` is itself nonproximal, by comparison with `(p_t,0)`. The monic epigraph is closed by continuity. The full-degree epigraph is locally closed and can be intersected with a small closed ball whose coefficient component remains in `l!=0`; the obstruction occurs in the interior of that localization.

The unscaled gradient's imaginary-constant component is `gamma`, which diverges. Hence the sequence does not remain near any fixed finite subgradient. Function prox-regularity relative to a finite subgradient concerns the epigraph normal `(v,-1)`, rather than all epigraph normals; the horizontal limiting normal here does not have that form. [Poliquin–Rockafellar, 2010, Definition 1.1 and p. 205](https://www.heldermann-verlag.de/jca/jca17/jca0849_b.pdf). No finite-subgradient conclusion follows from this construction.

## Adversarial boundary findings and remaining limits

- **Closed versus strict stability:** every `p_t` has an imaginary-axis root and belongs to the closed stable set. For a strict `<0` convention it is not in the set, and the open stable set can have unattained distance infima. The proof must retain `<=0`.
- **Real restriction:** for real monic quadratics, stability is exactly `a>=0,b>=0`, a closed convex orthant. Its nearest projection is unique under every SPD metric. The imaginary-constant witness is outside this space. Near a real nonzero leading coefficient, the full real quadratic stable set is also locally an orthant times the leading-coordinate interval. Higher-degree real questions remain separate.
- **Root dominance:** simple-root smoothness is only used at each fixed positive `t`; the shrinking gap does not violate a hypothesis. The desired uniformity at the singular base is precisely what the support calculation disproves.
- **Projection quantifiers:** the two submitted stable comparison points are not asserted to be nearest points of a common input. Nonuniqueness is an analytic existence consequence of the verified closed-set projection theorem and existence/locality argument.
- **Metric and units:** all coordinates are coefficient coordinates in one fixed quadratic coefficient space. If physical coefficient units are rescaled by fixed positive factors, that is an SPD coefficient metric covered above. Degree, coefficient ordering, and the height coordinate are not interchanged.
- **Target coverage:** determining whether the original campaign also demands a real-only or finite-subgradient statement is left to the independent source reviewer. No priority, historical-openness, or paper-level verdict is prepared.

The strongest independently verified result is a horizontal limiting normal at `z^2` that is not proximal, in both monic and full complex quadratic spaces and in the abscissa epigraph; together with closedness/localization, this proves the submitted nearby nonunique stable projections for all fixed SPD coefficient metrics. There is no remaining mathematical gap for that scoped result. The exact unproved extensions are the real-only general problem, fixed-finite-subgradient function prox-regularity, and identification of an explicit nearest-point pair.

## Reproduction evidence

The inspected frozen control scripts were copied byte-for-byte before execution. They contain only imports, exact symbolic/algebraic computations, assertions, and JSON printing. Replays use an existing read-only Python 3.14.6 / SymPy 1.14.0 environment, with bytecode writing disabled. The receipt records source/copy hashes, return codes, expected counts, full JSON outputs, and source hashes after execution.

| Run | Exact assertions | Outcome |
| --- | ---: | --- |
| Frozen author controls, own copy | 533 | PASS |
| Frozen previous independent controls, own copy | 801 | PASS |
| Fresh independent support/chart/metric controls | 90 | PASS |

These finite controls corroborate exact identities; the infinite conclusions and universal metric/projection assertions depend on the analytic arguments above. Artifacts: `support_checks.py`, `run_replays.py`, `replay/REPLAY_RECEIPT.json`, individual stdout JSON and stderr receipts, and `FROZEN_INPUT_HASH_CHECK.json`.

Final UTC and completion estimate are recorded in `RESEARCH_LOG.md`. Completion is 100% of this assigned mathematical-support audit; this is not an assertion of complete resolution of the original campaign.
