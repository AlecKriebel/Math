# Research log: hostile exact endpoint branch

## 2026-08-07 — branch opened

The product inequality and the weaker disjunctive endpoint separator are
both open.  Earlier broad random searches did not directly optimize the
nonsmooth minimum objective.  This branch therefore targets the Pareto
frontier: constrained minimum optimization, normalized arithmetic
scalarization, product optimization, and extreme fixed supports.  Every
apparent positive gap will be rationalized and replayed by an independent
exact subset-chain implementation.

## 2026-08-07 — finite optimization cycle

- [NUMERICALLY OBSERVED] All 38 connected labelled supports on four vertices
  were optimized separately for `P`, `M`, and the normalized arithmetic
  mean over logarithmic weights.  Complete support returned the complete
  graph.  The nearest proper-support product point had approximately
  `x=1.000430008`, `y=0.993798413`, `P=0.994225754`.
- [NUMERICALLY OBSERVED] Complete, path, cycle, star, core-periphery, and
  random irregular supports on orders five through seven were optimized for
  the same endpoint objectives, with log spans through 22.  No resolved
  `P>1` or `M>1` candidate appeared.  Values above one by at most about
  `10^-14` occurred at the complete graph and are roundoff.
- [NUMERICALLY OBSERVED] On the three-blade windmill support, direct
  nonsmooth `M` optimization found a crossing `x=y~0.965253`, still below
  one.  Product and arithmetic optimization also remained below one.
- [INFERENCE, NOT PROOF] The only stable graph-independent linear separator
  in these optimizations is the balanced normalized arithmetic target
  `(x+y)/2<=1`.  Unbalanced scalarizations are genuinely false, so a dual
  proof cannot choose its Bd/dB multipliers freely.

## 2026-08-07 — exactification and affine-dual constraints

- [EXACTLY REFUTED NUMERICAL ARTIFACT] Before residual/range guards were
  added, a seven-vertex star with edge scales separated by roughly `10^17`
  produced an impossible floating Bd ratio near `4.8*10^5`.  The rational
  reconstruction in the verifier has
  `x~0.665749707`, `y~0.456174703`.  The search now rejects any absorption
  solve with a bad residual or a harmonic value outside `[0,1]`.
- [PROVED CLASS CERTIFICATE] Let every edge of `K_{2,2}` have weight one,
  add a chord of weight `a>=0` in one part, and leave the other chord absent.
  Direct solution of the seven-state orbit chain gives exact rational Bd and
  dB formulas.  The numerators of `2-x-y`, `1-xy`, and `1-y` have strictly
  positive coefficients in `a`.  Thus this entire boundary family is
  dB-suppressing and satisfies both candidate separators strictly.
- [EXACTLY COMPUTED] Ten rational hostile graphs were independently solved,
  including a true dB-amplifying windmill, a true Bd-amplifying weakly
  completed star, the closest rationalized five-edge point, and the resolved
  floating artifact.  None violates `P`, `M`, or `(x+y)/2`.
- [EXACT DUAL GUIDANCE] A new rational seven-vertex windmill-like graph has
  `x~0.827701010`, `y~1.016737744` and exactly violates
  `(177/2000)x+(1823/2000)y<=1`.  The unit star on ten vertices exactly
  violates `(7/12)x+(5/12)y<=1`.  Consequently any universal separator of
  the fixed affine form `lambda*x+(1-lambda)*y<=1` must obey

      177/2000 < lambda < 7/12.

  The actual witness crossings are approximately `0.088542284` and
  `0.582602656`.  This narrows the admissible dual multiplier but leaves
  `lambda=1/2` viable.

## Gate-2 status

The endpoint product conjecture is **STILL OPEN**.  It has not been exactly
refuted.  The weaker no-simultaneous-amplification statement is also
**STILL OPEN**.  The specific surviving proof target suggested by this
branch is the normalized arithmetic separator with the balanced multiplier;
an unbalanced graph-independent affine certificate must at least respect the
exact interval above and still needs graph-sensitive within-rank terms to
overcome the previously recorded product-chain Farkas obstruction.

## 2026-08-07 — balanced-separator Poisson cycle

- [PROVED REFORMULATION] For the exact continuous type-changing Green
  occupations `z_B,z_D`, normalized endpoint excess has the identity

      e_B+e_D = T + C - E,

  where `T` is the Bd/dB occupation mismatch paired with temperature
  imbalance, `C` is the signed complete-cut deviation, and `E>=0` is the
  exact tangent-square dispersion.  The balanced separator is equivalent to
  `T+C<=E`.
- [EXACTLY VERIFIED] FLINT rational solves check this identity on all ten
  hostile rational witnesses.  The implementation checks the complete
  harmonic drifts and the tangent-square bridge state by state.
- [EXACT ROUTE CLOSURES] `T` and `C-E` both have positive state atoms;
  complete fixed-rank contributions can be positive; and neither aggregate
  term has a universal sign.  The integer-weight path
  `4--1033--0--1--3--6--1--1269--2` (read with the vertex labels in the
  reduction note) has exact `T=3.452073...>0`, compensated by
  `C-E=-3.983685...`.
- [EXACTLY REFUTED GRAPH-SENSITIVE COEFFICIENT] Choosing `lambda(G)` to
  balance the two exact singleton reach-two deviations fails on the nearest
  five-edge witness: `lambda~0.9654023` but the affine fixation score is
  `1.000200636...>1` exactly.
- [SPECIFIC MINIMAL OBSTRUCTION / OPEN] Any proof must couple within-rank
  graph geometry to cross-rank Green flow conservation.  Statewise,
  fixed-rank, separately averaged mismatch, and establishment-only
  certificates cannot close the sign.

## 2026-08-07 — exact vertex-bilinear Farkas barrier

- [EXACTLY REFUTED PROOF ANSATZ] On the weighted three-path with leaf-center
  weights `1,17`, no correction
  `sum_ij C_ij 1(i in A)1(j in B)` to the complete radial product-chain
  Poisson potential can make the desired balanced drift inequality hold
  pointwise.  A ten-atom nonnegative rational Farkas law annihilates all nine
  coefficient columns and has expected defect
  `-2914284766335459263489/11053845274742764346205<0`.
- [EXACTLY CHECKED NON-COUNTEREXAMPLE] The same graph has normalized balanced
  slack `2-x-y=236336950/700859439>0`; the certificate closes a proof route,
  not the endpoint conjecture.
- [REFINED MINIMAL OBSTRUCTION] The remaining global proof must be
  nonpointwise or use nonlinear/higher-order vertex data in addition to the
  cross-rule, cross-rank Green-flow coupling already isolated above.
