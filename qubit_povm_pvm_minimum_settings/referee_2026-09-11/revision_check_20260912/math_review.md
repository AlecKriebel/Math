# Independent mathematical re-review of the referee response

Checkpoint: 2026-09-12 04:20:50 UTC (2026-09-11 21:20:50 PDT). Completion estimate: 100% of this bounded revision review. This is not a new complete Lean audit or whole-paper mathematical certification.

Scope: the manuscript and coverage-document changes from `08c208e90` to `53b1570d6`, the revised strict residual definition and relevant downstream arguments, and the physical frame premises in the production Lean closure. Existing production and response files were read only. No outside communication occurred.

## Verdict

**R1 is resolved by the revision. R2 is accurately clarified rather than filled in by new formal proofs.** I found no new mathematical defect in the changed definition or its inspected downstream uses. The correction leaves the physical theorem and its intended convex-hull equality unchanged. The manuscript still contains auxiliary mathematical claims not separately formalized in Lean; the revised coverage statement now makes that limitation explicit.

## R1: independent check

For a real symmetric form of signature `(1,3)` and a unit timelike vector `u`, its orthogonal complement is negative definite. Write any null vector as `x=t u+z`, with `g(u,z)=0`; nullness gives `||z||=|t|` for the norm induced by `-g`. Hence two nonproportional null vectors have positive pairing exactly when their time components have the same sign. This follows from strict Cauchy–Schwarz; equality would imply proportionality. The fixed five coefficient rays are nonzero and pairwise nonproportional.

Consequently positivity of all distinct-ray products forces all five rays into one common causal cone. The circuit `u=r1+r2`, with `g(r1,r2)=1/2`, forces that same cone to contain `u`. Conversely, the five rays in the common cone containing `u` have positive distinct-ray products. Thus the corrected equivalence is valid with the independently retained signature hypothesis. Here “future cone” includes its timelike interior; it does not assert that `u` is null.

The ten distinct-ray pairings in the normal form are exactly

```
1/2, a, b, c, d, e,
1/2-a-b, 1/2-c-d, 1/2-b-d, 1/2-a-c.
```

These reproduce the listed scalar inequalities. The products with `u` are `1/2`, `1/2`, `a+c`, `b+d`, and `1-a-b-c-d`, all positive under those inequalities. None of this supplies signature by itself.

I independently recomputed the rational counterexample using Python `fractions.Fraction`: `a=d=6/25`, `b=c=3/100`, `e=1/25`. All five nullness identities, all ten strictly positive pairings, all five positive products with `u`, and

```
g(u,u)=1, g(u,v)=0, g(v,v)=12/5,
v=(2,-2,5,-5)
```

passed exact assertions. With columns

```
u,
(-27/50,-27/50,1,1),
(1,-1,0,0),
(21/50,-21/50,1,-1),
```

the congruent form is exactly `diag(1,-529/2500,-1,241/2500)`. This confirms signature `(2,2)`, excluding the example from the corrected domain.

## Downstream boundary

- The manuscript constructs the residual metric as `g=E_Aᵀ J E_A` with an invertible effect frame. Congruence already supplies signature `(1,3)`. Physical residual strategies are therefore not removed by the correction.
- Local physical completeness explicitly assumes Lorentz signature and orientation. Its negative orthonormal frame construction on `u`'s orthogonal complement remains justified. The smooth-incidence proposition also explicitly restricts to that open domain.
- The weighted second-form argument uses `S=Pᵀg⁻¹P`. With invertible `P` and retained Lorentz signature, its asserted ambient inertia `(4,12)` remains justified. It was not extended to arbitrary scalar tuples by this revision.
- `Bell/ResidualCoordinates.lean` retains invertible Alice and steering frames, `alice * u = timeUnit`, future-null rays and a timelike reduced state. Its scalar parameters are derived from those physical data and linked back by `parameters_gram`.
- `Bell/ResidualClosure.lean:no_strict_residual_maximum` separately takes invertible `E`, `frameGram E = metric ...`, `E*u=timeUnit`, and `FramePositive E Y`. `frame_timeFunctional_positive` obtains the rank-zero orientation from precisely those premises. A scalar metric of signature `(2,2)` cannot satisfy the invertible Gram premise.

Thus no inspected physical closure step assumes that `StrictParameters` by itself proves Lorentz signature. The purely algebraic projective-fiber statements may legitimately hold on a larger scalar domain.

## R2: coverage wording

The added auxiliary-coverage section agrees with the original declaration-level referee matrix. It explicitly identifies the absent or replaced general SDP/KKT results, full manifold and Hessian/inertia assertions, general cone/filter/rank results, the original projective-bound route, auxiliary discrimination and Appendix B optimization details, and generic representation bridges. Its principal endpoint table continues to distinguish attained values from global optima and whole-strategy finite convexification from equality of raw sets.

“Specializations needed for the qubit reduction” should be read as the specialized consequences or replacement arguments described in the linked detailed matrix, not as a claim that the arbitrary rank-square inequality itself was added. In context the present wording is adequate. No mathematical repair to the production endpoint follows from R1, and no claim of literal whole-paper formalization is now made by this coverage document.

Build provenance, source fingerprint preservation, archive/PDF validation, and the full dependency-audit trust boundary are outside this bounded review and are checked separately by the coordinating referee.
