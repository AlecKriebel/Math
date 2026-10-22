# ODE well-posedness and continuation audit — PR 880 / problem 9700026

Decision: **PASS within the stated ODE family. No core mathematical gap or required repair was found.** The frozen author proof does not need uniqueness: its existence, continuation, and scalar inequalities apply to every classical solution. Independently, the hard weighted Voronoi cell-area vector field is locally Lipschitz on the positive orthant for fixed distinct sites. This remains true at equal weights, collinear configurations, circle-to-line limits, tangencies, and multiple-boundary coincidences.

Audit completed: 2026-10-15T09:33:44+00:00. Frozen candidate head: `fba74a301786f9648e48722e76f440097b0746c2`. Source-manifest SHA-256: `b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b` (40 members). The author proof is 5,736 bytes, SHA-256 `8b0922482116df0b6510b4d5a6c089c3478765d4fecf2c151fd04c50a6814767`.

## Independence, target, and success criteria

The primary 2007 model passage and its section 6.4 were read directly from the locally retrieved primary text, as was the 2012 model passage. `INDEPENDENT_MEMO.md` was written and saved before the author proof or either earlier report/acceptance was read. It specified the polynomial-boundary mechanism and failure scenarios in advance. Subsequently the complete author `PROOF.md`, audit A report/acceptance, and review B report/acceptance were read and their frozen bytes checked. Prior acceptance is an audited claim, not evidence substituting for the analysis below.

The exact model is hard maximum influence on Q=[0,1]^2:

    A_i(z) = area{y in Q: z_i^alpha |y-x_i|^(-beta)
                             >= z_j^alpha |y-x_j|^(-beta) for every j},
    z_i' = A_i(z)-z_i.

Assumptions: finitely many n>=2 fixed distinct interior sites, alpha,beta>0, and initially z_i>0 with sum z_i=1. Values at finitely many sites can be assigned without affecting areas. Success in this family requires (i) a well-defined area partition, (ii) adequate existence and continuation for every positive initial state, (iii) no hidden uniqueness assumption in persistence, (iv) a valid Lipschitz supplement if uniqueness is asserted, and (v) proper exclusion of boundary cases not proved.

The target conclusion is persistence for beta>2alpha, which in particular rules out a coordinate converging to 1 when alpha=2,beta=8. This audit does not claim critical-case behavior, restricted collapse, convergence, equilibrium uniqueness, stochastic-model results, novelty, or publication readiness.

## 1. The area map is well-defined and continuous

Write q=alpha/beta and p=2q. For positive populations, pairwise dominance away from the sites is equivalent to

    |y-x_i|^2 <= lambda_ij(z)|y-x_j|^2,
    lambda_ij(z)=(z_i/z_j)^p>0.

Let a=x_i, b=x_j, d=|a-b|>0, and define

    f_lambda(y)=|y-a|^2-lambda|y-b|^2.

For lambda=1 this is a nonconstant affine polynomial because a!=b, so its zero set is a line. For lambda!=1 completion of squares gives a circle with radius sqrt(lambda)d/|1-lambda|>0. Thus every pairwise tie is planar-null, including equal populations. The finite union of ties and sites is null. Every other point has exactly one strict maximizing site. The cells are measurable and partition Q up to null sets; hence A_i>=0 and sum A_i=1. There is no positive-area tie convention to resolve under the assumptions.

At a point with a strict winner, every relevant finite inequality remains strict for all sufficiently close positive states. Indicators of winning cells therefore converge almost everywhere when states converge. Dominated convergence gives continuity of each A_i on the positive orthant. No global smoothness of the singular influence scores is used.

## 2. A quantitative proof of local Lipschitz continuity

This independent derivation verifies the added uniqueness conclusions, without assuming differentiable cell areas or fixed cell combinatorics.

### Uniform gradient on a whole band

Direct expansion gives the exact identity

    |gradient f_lambda(y)|^2
        =4[lambda d^2+(1-lambda)f_lambda(y)].                 (1)

Fix any compact positive parameter range lambda in [m,M], with m>0, and set

    H=max(1,|1-m|,|1-M|),
    epsilon_0=m d^2/(2H),
    g=sqrt(2m)d.

For |f_lambda|<=epsilon<=epsilon_0, formula (1) implies

    |gradient f_lambda|^2 >= 2m d^2,
    |gradient f_lambda| >= g>0.                              (2)

This bound holds throughout the band. It does not merely hold at the moving zero boundary. In particular it is uniform as lambda approaches or equals 1.

### Uniform level-length bound and coarea

Every nonempty regular level f_lambda=u is a circle or a line. The total length of its intersection with Q is at most 8. For a circle, split it into the four arcs between its horizontal and vertical extrema. Both coordinates are monotone on each arc. Intersection with the square is an interval of that arc (possibly empty); along it, ds<=|dx|+|dy| and each coordinate varies by at most 1. Each contribution is at most 2, and the four contributions total at most 8. A line contributes at most sqrt(2). Degenerate point levels have length zero and, by (2), do not occur inside the chosen band if nonempty.

Coarea for the polynomial f_lambda, followed by (2), gives

    area{y in Q: |f_lambda(y)|<=epsilon}
      = integral[-epsilon,epsilon]
          integral[Q intersect {f_lambda=u}] 1/|gradient f_lambda| dH^1 du
      <=16 epsilon/g,     0<epsilon<=epsilon_0.             (3)

Thus boundary length cannot blow up in the circle-to-line limit. Neither circle crossings with the square nor intersections with other pairwise boundaries enter this estimate.

### From pairwise motion to cell-area motion

For any lambda,mu>0 and y in Q,

    |f_lambda(y)-f_mu(y)|
      =|lambda-mu||y-b|^2 <=2|lambda-mu|.                    (4)

If the pairwise dominance indicator changes, |f_lambda(y)|<=2|lambda-mu|. Equations (3)–(4) imply, for sufficiently close lambda,mu in [m,M],

    area({f_lambda<=0} symmetric-difference {f_mu<=0})
        <=32|lambda-mu|/g.                                  (5)

Every full i-cell is the intersection of its n-1 pairwise dominance regions. The symmetric difference of two such intersections is contained in the union of the pairwise symmetric differences. Each function z -> (z_i/z_j)^p is smooth, and hence Lipschitz with bounded derivative, on a compact positive neighborhood of any fixed positive state. Shrink that neighborhood so the finitely many parameter differences satisfy the band-size condition in (5). A finite sum of (5) proves local Lipschitz continuity of A_i, and therefore of A(z)-z, on the positive orthant.

There is no generic-position assumption in this argument beyond distinctness of sites. Close sites, large weight ratios, or small positive populations may make the local constants large. Local finiteness is all that existence and uniqueness require. No uniform bound as populations tend to zero is asserted.

## 3. Positive global forward solutions

Continuity on the open positive orthant supplies local C^1 solutions by Peano's theorem. Along every such solution, s=sum_i z_i satisfies

    s'=sum_i A_i-s=1-s.

Therefore s(0)=1 implies s(t)=1. Also

    (e^t z_i(t))'=e^t A_i(z(t))>=0,
    z_i(t)>=z_i(0)e^(-t)>0.                                 (6)

If a maximal forward interval had a finite endpoint T, then on [0,T) each coordinate would lie in [z_i(0)e^(-T),1]. This is a compact subset of the positive orthant, where the vector field is continuous and bounded; in fact |z_i'|<=1 on the simplex. Bounded derivative makes the trajectory Cauchy as t increases to T, giving a positive limiting state. Local existence at that state extends the solution beyond T, a contradiction. This proves global forward existence for every maximal positive solution and every alpha,beta>0.

The quantitative Lipschitz proof additionally gives local uniqueness by Picard–Lindelof, which combines with continuation to give a unique positive global forward solution. These arguments do not confuse continuity with uniqueness, and they do not assume finite-time positivity while attempting to prove it: inequality (6) supplies the required positive compactness bound first.

## 4. The author's all-solutions persistence mechanism is sound

Although uniqueness has now been independently established, it is unnecessary for the submitted proof. For fixed i choose h_i>0 so the square of halfwidth h_i around x_i lies in Q and |x_i-x_j|>=2sqrt(2)h_i for every j!=i. For any positive simplex state, the smaller square of halfwidth h_i z_i^q lies in Q. For y in that square,

    |y-x_i|<=sqrt(2)h_i z_i^q,
    |y-x_j|>=|x_i-x_j|-|y-x_i|>=sqrt(2)h_i.

Since z_j<=1,

    |y-x_i|<=z_i^q |y-x_j|<=(z_i/z_j)^q |y-x_j|.

Thus this whole square belongs to cell i, and

    A_i(z)>=K_i z_i^p,  K_i=4h_i^2>0.                       (7)

This estimate is uniform over positive simplex states and does not assume smooth area derivatives, a basin of attraction, or a well-behaved cell topology. Distinct interior sites are precisely what guarantees usable h_i.

If beta>2alpha then 0<p<1. Along any positive classical solution, (7) gives z_i'>=K_i z_i^p-z_i. The differentiable transformation u_i=z_i^(1-p) and multiplication by its positive derivative give

    u_i'>=(1-p)(K_i-u_i).

An integrating factor yields, for every t>=0,

    z_i(t)>=[K_i+(z_i(0)^(1-p)-K_i)e^(-(1-p)t)]^(1/(1-p)). (8)

The bracket is a positive convex combination. Hence all-time lower bounds depend on both the starting state and geometry, while the asymptotic bound does not depend on the starting state:

    inf[t>=0] z_i(t)>=min(z_i(0),K_i^(1/(1-p)))>0,
    liminf[t->infinity] z_i(t)>=K_i^(1/(1-p))>0.             (9)

Every other coordinate has a positive all-time lower bound, so no coordinate can tend to 1. This is an integrating-factor deduction for every solution, not an invariant-region argument depending on prior uniqueness. Equivalently, any level delta with K_i delta^(p-1)>1 is a strict inward barrier for every solution. The argument uses the displayed ODE time without rescaling it.

The exact alpha=2,beta=8 witness has q=1/4,p=1/2,K_i=1/64 and lower bound 1/4096. The exact sites and initial vector satisfy the required strict inequalities. Therefore 1/4096<=z_i(t)<=2047/2048 for every i and t>=0. Independent rational calculations reproduce these constants.

## 5. Adversarial geometry and excluded cases

| Scenario | Assessment |
|---|---|
| Equal populations / lambda=1 | Tie is a nonconstant line; (1)–(5) remain valid. |
| Lambda near 1 / circle radius diverges | Gradient is uniformly positive on a whole band; level length inside Q is uniformly bounded. |
| Collinear or many sites | Each pair is treated separately; finite union/intersection bounds suffice. |
| Multiple ties, tangent arcs, changing cell combinatorics | No differentiability of cell combinatorics is invoked. Pairwise band bounds still control changed area. |
| Highly imbalanced positive populations | Every positive state has a compact positive neighborhood; constants may grow near the boundary. |
| Very close but distinct sites | d>0 gives finite constants; there is no claim of uniformity as d decreases to zero. |
| Distinct sites near the boundary | Regularity is unaffected; h_i can be small but positive. |
| Coincident sites | Excluded. Equal coincident weighted sites can tie on positive area, invalidating the null-tie partition argument. |
| Zero initial weights | Excluded. Formulae using ratios and positive powers cannot simply be carried over; uniqueness at the closed simplex boundary can fail. |
| beta=0 or nonpositive exponents | Excluded; the dominance equivalence and threshold proof use positive alpha,beta. |
| beta=2alpha or beta<2alpha | Global positive finite-time solutions still follow; (8)–(9) require p<1 and do not establish the desired asymptotics there. |

The zero-weight exclusion is substantive. Under the natural null-site convention, take two sites a=(1/4,1/2), b=(3/4,1/2), let z_1=z, z_2=1-z, and use any p in (0,1). Put lambda=(z/(1-z))^p. For small positive z, lambda<1, and cell 1 is the disk with center (a-lambda b)/(1-lambda) and radius sqrt(lambda)|a-b|/(1-lambda). For lambda<=1/64 it is strictly inside Q, so exactly

    A_1(z)=pi |a-b|^2 lambda/(1-lambda)^2
          ~ (pi/4) z^p as z decreases to zero.

With the natural definition A_1(0)=0, the scalar vector field f(z)=A_1(z)-z is zero at zero, positive near zero, and asymptotic to (pi/4)z^p. Consequently the integral of 1/f(z) from zero to a sufficiently small positive value is finite. Its inverse defines a positive departing trajectory from zero, while z=0 is also a trajectory; arbitrary waiting times can be inserted. Thus one must not silently extend the positive-state uniqueness conclusion to all of the closed simplex. This excluded failure scenario does not affect the candidate's strictly positive initial conditions.

## 6. Evaluation of prior regularity additions

Audit A's supplementary argument is valid. Its gradient identity is (1). Its choice H=max(1,|1-m|,|1-M|) produces the stated band bound. On that band, at least one partial derivative has magnitude >=sqrt(m)d. A quadratic slice has at most two components with that derivative magnitude. Each component contributes length <=2epsilon/(sqrt(m)d). Fubini in each coordinate and a union bound therefore give its stated strip-area bound 8epsilon/(sqrt(m)d). The parameter perturbation and finite-intersection steps are valid. This argument already handles straight lines at equal weights; it need not invoke coarea or arc-length bounds.

Review B's finite-cover argument is also valid as a local argument. At any fixed positive parameter, compactness of the zero set in Q and its nonzero spatial gradient give a finite collection of coordinate rectangles with a nonvanishing selected partial derivative. The rectangles and derivative bounds persist over a sufficiently small common closed positive parameter interval. On the compact complement no sufficiently small zero band exists, uniformly after shrinking the parameter interval. Monotone slices then give O(epsilon) area. This supplies the claimed local Lipschitz result. The report's phrase about uniform constants is justified in this sufficiently small interval; it is not evidence for an unbounded parameter range.

Both prior reports correctly distinguish this additional uniqueness proof from what is needed by the author's all-solutions argument. Neither added proof reveals or repairs a required central gap.

## 7. Checkable evidence, findings, and exact remaining gap

`check_auxiliary.py` uses rational arithmetic and explicit failures rather than optimization-sensitive assertions. The fresh run passed 900 gradient-identity cases, 108 whole-strip gradient inequalities, and 3,144 changed-sign strip inclusions across ordinary, collinear, close-site, and near-boundary examples. Lambda values include equality, values immediately to either side, and 10^(-12) to 10^(12). It separately checks the exact witness constants and containment bounds for the small-disk boundary control. Five inspected proof/report/acceptance files match their 40-member source-manifest pins. `AUXILIARY_RESULTS.json` records these receipts.

These finite calculations corroborate algebra and constants. They do not prove an area theorem by sampling, establish an ODE trajectory numerically, or formally verify the mathematical argument. The analytic estimates in this report and the independently checked submitted reasoning establish the claimed conclusions. No floating-point simulation is used.

**Core gap:** none in the ODE regularity, forward continuation, positive-simplex invariance, or all-solutions comparison steps required for the literal counterexample. **Optional routine completion:** the author could add a positive-orthant Lipschitz/uniqueness lemma for completeness, but the unchanged proof is already sufficient and neither earlier audit makes it a repair condition. **Exact unresolved scope:** critical p=1 behavior, collapse for p>1, convergence and equilibrium properties, boundary-start uniqueness, the stochastic model, and wider priority/publication questions.

No candidate file was edited. No Git write, PR action, sheet write, release, publication, outreach, or contact occurred. All authored outputs for this family are confined to its dedicated folder. The research log records checkpoints and their completion estimates. The public manifest lists only newly authored audit files; no source PDFs, extracted source text, renders, or corpora are included.
