# Independent mathematical interface audit

Checkpoint: 2026-09-11T01:42:50Z. Completion estimate: 100% of this bounded
interface review; this is **not** a percentage of the complete Lean build.

This review was performed independently of compilation repair. No Lean source
was edited. The inspected source was the imported September 10 audit package.
The comparison manuscript is `paper/main.tex` in this repository, rather than
the historical PDF bundled under `bell_lean/source/`.

## Finding

No false or weakened principal statement was identified in the inspected
definitions and theorem interfaces. The intended principal assertions are
present unconditionally in `Assembly.lean`, subject to successful elaboration
and a dependency audit. Source inspection does not establish that these proof
terms exist. This report must not be used as a substitute for the actual build.

## Physical model and statement correspondence

* `Quantum.lean` uses complex 2-by-2 local matrices and a positive semidefinite,
  trace-one 4-by-4 density matrix. The tensor index order is explicit. `born`
  takes the real part of the usual trace. For Hermitian positive physical
  inputs the trace is real, so taking the real part does not enlarge the model.
* A `POVM n` requires positivity of every effect and an operator sum equal to
  identity. A `PVM n` additionally requires idempotence and pairwise
  orthogonality. Zero and identity effects are retained. Empty output sets
  cannot support a normalized measurement; the one-input code explicitly
  handles that boundary rather than asserting all output counts are positive.
* The raw sets are ranges of **whole strategies**. Their hulls are ordinary
  real convex hulls. Each mixture component may choose both the state and all
  local measurements. `finite_projective_simulation` exposes one common finite
  index for the full table. There is no entrywise independent mixture hidden
  in the equality assertion.
* The equality quantifies over arbitrary input-dependent finite outputs. It is
  not restricted to ternary outputs or real effects. The final minimum-input
  statement excludes one input on either party and the 2-by-2 case, up to
  exchange of parties. No equality of the nonconvex raw images is asserted.
* The signs, three rational auxiliary coefficients, CHSH signs, and common
  three-label presentation in `Witness.lean` agree with the manuscript's
  displayed Bell functional exactly. `ProjectiveGlobalUpperBound` quantifies
  over actual physical projective strategies, rather than a scalar relaxation
  supplied as an assumed oracle.

Two representational conventions should be stated when describing coverage.
The manuscript says local dimension **at most** two; the primitive Lean model
uses dimension exactly two. A one-dimensional strategy embeds by putting its
state in one coordinate and completing each measurement on the unused
coordinate; projectivity is preserved by assigning the complementary projector
to any declared label. Thus this is not a mathematical counterexample or a
weaker optimum, but an explicit arbitrary-dimension embedding theorem was not
among the inspected statement contracts. Similarly, the manuscript explicitly
includes stochastic postprocessing: a finite stochastic map is a mixture of
deterministic maps, and deterministic merging preserves PVMs. The Lean hull is
the equivalent finite-mixture model; a general stochastic-channel equivalence
theorem was not among the inspected contracts.

## Independent separator calculations

The simple witness has the Bell-state identity
`p(M,N) = tr(M Nᵀ)/2`. The three auxiliary effects are positive rank-one matrices
with nonzero eigenvalues respectively `17/25`, `17/25`, and `16/25`; their sum
is identity. Directly multiplying against Bob's positive Z, negative Z, and
positive X projectors gives the three selected probabilities `8/25`. Alice's
first two observables are `(Z+X)/sqrt(2)` and `(Z-X)/sqrt(2)`, so the four CHSH
correlations are `1/sqrt(2), 1/sqrt(2), 1/sqrt(2), -1/sqrt(2)`.
Consequently the score is exactly `20 sqrt(2)+16/25` as claimed. The first
auxiliary effect is not idempotent, since its nonzero eigenvalue is `17/25`.

The PVM bound source uses the stronger bound `289/10`, not the paper's deficit
argument as an unproved physical reduction. A ternary qubit PVM has a zero
effect. Each of the three possible zero positions has an explicit physical
Bell-operator identity. Deterministic measurements have two zero positions
and remain covered. The CHSH observables from Alice's first two measurements
are involutions even if the third label there is nonzero: the signed sum is
`I-2 M₁`, with the other two labels sharing the positive sign.

For auxiliary support `{0,1}`, the short square certificate can be verified
without any optimization argument. Put `r=7/5`,
`S₀=r A₀-B₀-B₁`, `S₁=r A₁-B₀+B₁`, and `S₂=I-A₂B₀`, with tensor identities
suppressed. Hermitian involutions and interparty commutation give

```
S₀²+S₁² = (198/25) I - (14/5) CHSH,
S₂²      = 2 I - 2 A₂B₀.
```

Multiplying by `25/7` and `3/20`, then adding `I/70`, yields
`(143/5)I - 10 CHSH - (3/10)A₂B₀`, exactly
`(289/10)I - bell01`. Every square has nonnegative state expectation.
The `{1,2}` switch sends `(A₀,A₁,B₀,B₁)` to
`(-A₁,-A₀,-B₀,B₁)` and preserves CHSH, so it correctly reduces to `{0,2}`.
The large rational Gram certificate for `{0,2}` requires the separate exact
coefficient/factorization and compiler checks; this review does not claim to
have independently expanded that entire matrix.

## Residual proof interfaces and exceptional cases

`full_pure_of_not_mem_convexPVM` may initially look suspicious because it does
not require an extreme behavior. Its mechanism is legitimate: retain Alice's
POVMs, convert the mixed strategy into a qubit assemblage, and purify that
assemblage with changed Bob POVMs. This is not a claim that a mixed state itself
is pure. Singular reduced states are treated as product behaviors before the
inverse is used.

`ResidualStrategy.lean` derives its invertible frames and active rank-one effects
from the physical strategy and extreme-point reductions. It pulls the entire
Bell functional back through a whole-strategy label map. In particular, padded
outcomes do not receive free zero Bell coefficients that would invalidate the
maximum comparison for a negative functional.

`ResidualClosure.lean` starts with a maximum over the raw physical strategy
image and a strict comparison with the full PVM hull. It derives incidence
local maximality through `GramLift.lean`, whose stated Gram derivative has the
right inverse `H ↦ (1/2) J E⁻ᵀ H`. This formula is correct:
`Eᵀ J D=H/2`, and the transpose gives the other half for symmetric H.
Strict positivity is retained on an open neighborhood. Thus physical local
realizability is not silently assumed as a field of a chart object.

The rank-one projective fiber proof has a complete case split, including
`x₂=0`, `x₃=0`, `x₀=x₁`, and `x₂=x₃`, before applying the generic inverse.
The generic reconstruction factor is
`x₂ x₃ (x₂-x₃) (x₀-x₁)²`; the guards make it nonzero. Each exceptional inverse
has a separately established nonzero weight, using the strict metric
inequalities. The proof transfers the relevant target equations to the second
source before applying the same inverse. Intersections of exceptional planes
are included by the ordered case split. `SameRay` alone permits zero vectors,
but the relevant arguments separately require a nonzero projective image.
No division by an unchecked zero representative was found.

The final closure obtains multiplier positivity and stationarity before its
rank split. Rank zero uses an explicit PVM-hull reconstruction; rank one invokes
the fiber obstruction; rank at least two uses an uphill feasible curve. The
curve argument requires only first differentiability because an exact finite
score-gap identity supplies the quadratic limit. No state-only or one-block
maximum is substituted for the required coupled maximum.

## Trust boundary and remaining verification

A source scan of the mathematical module tree found no `sorry`, `admit`,
`native_decide`, `unsafe`, or explicit mathematical `axiom` declarations.
Occurrences of the word “axiom” in comments are not declarations. The actual
transitive axiom dependencies still require the compiler's declaration audit.

This was not a line-by-line independent reproof of all 58 modules. In
particular, the general compactness/convex-extreme reductions, every cone
decomposition lemma, the complete rank-zero transportation reconstruction,
the large SOS Gram matrix, and the strengthened Appendix B attainment require
their own validation in addition to the build. No new counterexample was found
in this review. Successful kernel checking of unchanged principal definitions
and the independent statement contracts remains the decisive formal boundary.
