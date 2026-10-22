# PR 261 independent reproduction adversary

Fixed submitted head: `7b7fcd63d5ea83df3a4c29853c4ba34b93d16f07`.

**Result:** all four unchanged submitted programs reproduce byte-identical PASS receipts. A separately authored Cartesian physical-orbit mechanism supports the pinned primitive focal area-product target, including stars and both signs. No counterexample to the primitive strict elliptical target was found. There is an exact counterexample to the unrestricted repeated-list extension. These finite controls do **not** certify the universal meromorphic proof; that proof is independently audited by the root agent.

## Independence and physical construction

`PRE_EXPOSURE_PLAN.md` was saved before reading any submitted proof, script, previous review or previous reviewer script. Original physical ray and low-period programs were authored and run before exposure to the submitted computational programs. Historical verdict prose was never used as mathematical evidence.

The orbit mechanism uses no Jacobi function or proof-specific helper. For a candidate strict confocal caustic let `ac²=a²−λ`, `bc²=b²−λ`. At an outer point `p`, transform to `z=(px/ac,py/bc)`, set `r²=z·z`, and solve unit-circle tangency by

`contact_unit=(z+sqrt(r²−1) Jz)/r²`, where `Jz=(-zy,zx)`.

This independently yields `contact_unit·contact_unit=1` and `z·contact_unit=1`. Transform back and launch toward that contact. The next bounce is obtained directly from the nonzero root of the outer ellipse's ray-intersection quadratic. Reflect the velocity at the Euclidean ellipse normal. Closure parameters are found by bisection of **total physical boundary winding**, rather than by setting a Jacobi step. Direct boundary, tangency-discriminant, closure, velocity-closure and primitive-vertex checks validate the constructed trajectories.

Pedal vertices are direct Euclidean projections onto each original chord. Antipedal vertices solve the two original equations `(p−F)·(X−p)=0` and `(q−F)·(X−q)=0`. Both areas use ordered signed shoelace sums. The implementation never substitutes an inverted, outer, or inner polygon.

## Fresh physical coverage and stability

`physical_ray_audit.py` tested 14 families, 7 nonidentical phases per family, and both foci. The families `(a/b,N,τ)` were

`(1.000001,4,1), (1.5,4,1), (2,8,1), (2,8,3), (3,12,1), (3,12,5), (1.2,16,3), (1.2,16,7), (1.5,20,3), (1.5,20,9), (5,24,5), (5,24,11), (10,12,5), (1.000001,32,15)`.

All `gcd(N,τ)=1`. At 110 decimal digits the worst relative product spread is `2.294e−68`. Worst outer-boundary residual is `4.08e−110`, normalized caustic-discriminant residual `5.55e−90`, position closure `3.13e−88`, and velocity closure `1.31e−88`. Central symmetry is independently observed to `1.55e−88`. Every antipedal intersection is finite and every orbit has distinct vertices. The near-separatrix case has minimum normalized antipedal normal determinant about `5.48e−22` and minimum vertex separation about `4.43e−11`, so finite precision conditioning matters.

The initial 65-digit run passed 13 families at the `1e−35` threshold; `(5,24,11)` had a `3.10e−24` product spread despite small physical residuals. Raising precision to 110 digits reduced that spread to `2.294e−68`. Both run receipts and outputs are preserved. This was numerical cancellation, not a physical counterexample. `physical_ray_audit_65dps.py` recreates the earlier configuration. No interval certification is claimed.

After the independent construction was completed, `canonical_bridge.py` compared all vertices at a nonaxis phase and the predicted axes against the submitted/Stachel canonical parameterization for the same independently closed caustics. All 14 bridges pass the `1e−60` threshold. Thus the computational agreement is not merely repetition of the submitted Jacobi-generated vertex helper.

`boundary_diagnostics.py` independently exercises traversal reversal and translated/scaled coordinates; each signed area reverses sign, and the product scales as length to the fourth power. It also locates a primitive convex N8 zero-area family near `a/b=1.8538473043818210146`, `λ=0.25278935048914019585`; at four phases antipedal area is at most `3.10e−109` and product at most `2.21e−108`. This is a numerical root diagnostic, not a certified exact zero theorem. Negative and positive antipedal areas occur in the other physical families.

## Exact independently authored controls

`low_period_symbolic.py` checks `a=5,b=3,λ=225/34`, both foci `(±4,0)`, at the axis diamond and an algebraic nonaxis primitive quadrilateral. It proves exact outer incidence, strict-caustic tangency, reflected-ray direction and direct original constructions. Both products are `202500/289`, agreeing with `16a⁴b⁴/(a²+b²)²`. The two individual factors vary. This is a check of two phases, not a proof of every quadrilateral phase.

`exact_repeated_period.py` independently proves that two primitive N6 phases at `a=3/2,b=1,λ=9/25`, each repeated twice as a listed N12 walk, have products `27648/625` and `27783/625`. All vertices, exact physical checks, areas and the nonzero difference `−27/125` are recorded in `EXACT_REPEATED_PERIOD.json`. This precisely isolates why a least-period convention is needed; it does not violate the pinned primitive target.

## Safe unchanged replay and actual coverage

The four programs were inspected statically before execution. Imports are limited to standard library and mpmath/SymPy; none contains network, shell, Git, provider mutation or writes to submitted files. Each was copied unchanged into its own `replays/` directory and run with its output redirected there. `REPLAY_INPUTS.json` binds each copy to its submitted hash. `SUBMITTED_BODY_HASH_RECHECK.json` confirms all 26 submitted bodies still match the intake hashes.

| Program | Replayed assertions | Meaningful scope |
|---|---:|---|
| Author exact | 12,029 | Symbolic direct-line incidence/confocality/projections and pole-factor identities; 1,695 finite `(N,τ)` lattice controls for N≤256; finite central-pair polygon controls; two actual N4 billiards. Most count is repeated arithmetic conditions, not independent full-period proofs. |
| Author numeric | 10,284 | 33 canonical/Jacobi-generated families for N=4,8,12,20,28 and k=.25,.63,.96; 4 real phases each including baseline, 4 complex phases, direct feet/intersections and formula comparisons. 9,024 assertions compare individual coordinates. No independent physical closure construction is present. |
| Prior reviewer exact | 6,469 | Independent midpoint/halfedge solve and actual projection identities; two generic-aspect N4 shapes and both foci; 1,069 finite lattice controls for N≤204. Laurent-germ and divisor controls are algebraic/finite checks, not universal analytic pole certification. |
| Prior reviewer numeric | 14,932 | 39 families for N=4,8,12,16,20, all admissible coprime windings, k=.2,.6,.96 and 3 real phases; rays are independently propagated, but axes and closure candidates originate from the canonical formula. Both foci, signs, reversal/scaling and selected complex/pole controls are covered. |

All four replay stdout files are byte-identical to the submitted recorded receipts, with empty stderr. `REPLAY_COMPARISON.json` records hashes and semantic equality. The old reviewers' numeric ray propagation is meaningful independent geometry; its remaining dependence on canonical axis generation is why this audit adds physical-winding root closure.

## Reproduction instructions

Dependencies are pinned in `requirements.txt` (`mpmath==1.3.0`, `sympy==1.14.0`). Successful runs used the bundled Python 3.12.14 runtime. Install into a local environment and run the five owned programs `physical_ray_audit.py`, `low_period_symbolic.py`, `canonical_bridge.py`, `boundary_diagnostics.py`, `exact_repeated_period.py` in that order. Each writes only within this directory. For unchanged submitted replays, run each copied `replays/<name>/program.py` with stdout redirected locally. Do not run against writable submitted source paths.

## Strongest verified result and exact gap

The strongest fully exact fresh result is physical agreement of the two N4 algebraic phases and the padded-list counterexample. The strongest higher-period evidence is independent ray-closure invariance in 14 primitive families with nonaxis phases, both foci, strong physical residuals and zero/sign/conditioning controls. All submitted computational receipts are reproducible and correctly label themselves finite/non-interval.

Remaining gap for this agent: finite controls cannot establish complete pole classification, cancellation at every complex point, or all-period torus constancy. Those require the written proof audit. The source also needs a transparent least-period qualification: Table 5 does not state it explicitly. Current primary search found a same-target external unrefereed 2026-10-01 claim; novelty and priority are not certified. No claim of a general hyperbolic, circular, degenerate or repeated-walk extension is supported.

Fresh source details and links are in `SOURCE_AUDIT.md`. Audit completion: 100% of this agent's source/reproduction assignment, not 100% acceptance of the universal mathematical result.
