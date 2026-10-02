# 30005936: negative mean-square subquestion and positive bounded-test convergence

**Original broad source bundle: unresolved, five of five author turns completed.** For the exact source's space-time-white-noise LT scheme with g(v)=v_+^(5/4), the packet proves a fixed-midpoint obstruction to continuum mean-square convergence. It also proves same-noise convergence in probability and a logarithmic bounded-Lipschitz path-law rate under balanced refinement. These conclusions have different test/moment scopes and are compatible.

## Negative result for the explicit source example

Use u0(x)=sin(πx), homogeneous Dirichlet boundary, T=1, and the original frozen-coefficient geometric-Brownian LT recursion. There is an explicit δ_*>0 independent of the discretization such that, for every even N and every M,

 E U_(M,N/2)−E u(1,1/2)>=δ_*,
 (E|U_(M,N/2)−u(1,1/2)|²)^(1/2)>=δ_*.

Both first moments are finite; no finite second moment is asserted or needed. In particular the balanced sequence M=N², τ=h², rules out continuum mean-square convergence and the proposed quarter-order extension for this superlinear coefficient. TURN_5.md proves the white-noise bracket estimate, the concave Itô barrier with all localization/Fatou passages, and the positive heat-kernel transfer to the fixed midpoint. A random quadratic-variation lower bound alone is not used as proof of strict expectation loss.

## Positive results and their exact hypotheses

1. **Globally Lipschitz, not necessarily differentiable g**, with g(0)=0: positivity and the credited Bréhier–Cohen–Ulander strong estimates extend by a controlled coefficient approximation. Temporal error is C sqrt(τ/h), hence Cτ^(1/4) under τ<=γh², against the spatially semidiscrete solution. Full continuum error is Ch^(1/2) under that condition. Its replacement by Cτ^(1/4) additionally needs balanced refinement.
2. High-p moment/error estimates track the global Lipschitz constant through C exp(C(1+L^4)), subject to NL²τ<=1 for the frozen numerical substep. The cap g_R=min(v_+,R)^(5/4) has L_R=(5/4)R^(1/4), yielding an explicit C exp(CR) bound. Finite grid cardinality is retained before balanced refinement is imposed.
3. The nonnegative exact power5/4 equation has a global solution and a quantified supremum exit tail P(sup u>=R)<=C_qR^(−q) for every0<q<1/2. Subcritical nonexplosion is credited to Mueller; the mass/chaining argument supplies the displayed quantitative input, including boundary excursions and cutoff dependence.
4. For that power coefficient, smooth nonnegative zero-boundary initial data, and fixed 0<c<=γ with c h²<=τ<=γh², the bilinear interpolation of the unmodified scheme converges uniformly on space-time in probability under the same noise. Its law on C([0,T]×[0,1]) has bounded-Lipschitz error O([log(e/h)]^(−q)) for every0<q<1/2. Tests have absolute value and sup-norm Lipschitz constant at most1. No algebraic order or optimality is claimed.

The unbounded 1-Lipschitz point observable w↦w(1,1/2) has a nonvanishing weak error by the negative result. It lies outside the bounded class in item4. These results explicitly expose a failure of uniform integrability rather than a contradiction.

## Source, prior work and unresolved scope

The primary question is David Cohen's second setting in OWR26/2024, printed1497, within the complete contribution1495–1498. It is distinct from the common time-only driver of target30005935/[PR317](https://github.com/AlecKriebel/Math/pull/317). That related prior supplies credited mass-obstruction ideas, not a theorem automatically transferable to white noise. The present bracket and fixed-midpoint transfer are written out.

The OWR continuum τ-only display differs from the detailed cited BCU temporal-versus-full theorem. That discrepancy is recorded in SOURCE_SCOPE.md; it is not presented as the rough-coefficient resolution. The negative result survives on balanced meshes, where the two orders coincide. Ulander's later LTE result concerns a different exact-simulation integrator and bounded invariant state intervals.

The source does not state a precise entire rough-coefficient class or weak-test class. We have not established every such extension, an optimal bounded-test weak rate, a rate under arbitrary one-sided temporal refinement, or a theorem about other integrators. The packet therefore remains an **unresolved5/5 scoped research result**, with a complete negative answer to its specified superlinear mean-square subquestion, rather than a claim to solve the entire source bundle. Classical stochastic calculus, the credited published spatial/strong theorems, Mueller's historical result and inverse-Bessel tools are acknowledged. There is no novelty certification.

Computational receipts contain only finite exact algebraic controls. They do not certify SPDE stochastic-calculus or limiting arguments. Full independent analytic review is required before publication.
