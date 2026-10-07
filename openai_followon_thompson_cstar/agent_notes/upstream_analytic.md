# Independent analytic audit of family 248

Checkpoint: 2026-10-06 22:13 PDT (2026-10-07 05:13 UTC).
Pinned upstream: `/Users/alec/Desktop/math`, HEAD
`adc7f1241b42e322a6451854ab7e4b4c146bf78a` (confirmed by a read-only Git query).
Audit-family mechanism: infinite-dimensional displacement, nearest-point tube,
finite Hilbert variance, and Følner quantifiers. Estimated completion of this
specified analytic audit: 95%; no claimed percentage toward a new theorem.

## Verdict and exact limits

No mathematical gap or counterexample was found in the specified analytic
route after adversarial source review. The argument examined is internally
checkable and its analytic existence input also has a published independent
source. This is an analytic audit, not a certificate that every imported Lean
file compiles or a proof of any proposed C*-algebraic consequence. No fresh
kernel build was performed here, to keep upstream strictly read only. The
root audit must independently check standard-group semantics, dependency
closure, and the follow-on operator-algebraic theorems before promotion.

Strongest verified result in this audit: assuming the elementary dyadic
transport/covariance facts stated in the paper, the finite correlation
argument gives the asserted positive uniform boundary for ordinary finite
subsets, using a legitimately available Lipschitz displacement map. There
is no remaining analytic gap identified. No repair is required on this
route. This conclusion does not upgrade unexamined follow-on assertions.

## Sources and statement scope

The original theorem is `build/sections/introduction.tex`, Theorem
`thm:main`: ordinary Thompson F is not amenable. Its definition of amenability
is a positive normalized invariant linear functional on all bounded real
functions, with multiplication `hg = h ∘ g`.

`lean/docs/248.md` describes the same standard dyadic PL group and all bounded
real functions. It says no explicit boundary constant or prescribed generating
set is given; the current Main source does give a symbolic exact formula,
but does not evaluate the noncomputable analytic constant numerically or give
a short named generating set. This is not a change of the underlying claim.

Actual declarations inspected:

- `lean/OAI/GroupTheory/Thompson/Main.lean:16`: existential D and finite S,
  a positive `boundaryConstant`, and `∀ A`, nonempty finite A has a translation
  in S with boundary ratio at least that constant.
- `Main.lean:38`: the literal displayed boundary constant formula.
- `Main.lean:45`: `∃ S b, S.Nonempty ∧ 0 < b ∧ ∀ A`, nonempty finite A has
  `∃ h ∈ S, b * card A ≤ card(leftTranslate h A ∆ A)`.
- `Main.lean:65`: `¬ Nonempty (InvariantMean F)`, with no analytic certificate
  premise or conditional nonamenability premise.
- `Main.lean:69`: composition law and nonamenability together for the installed
  group structure.
- `AnalyticModel.lean:14–20`: actual `EuclideanSpace ℝ (Fin 2)`-valued L² for
  Lebesgue measure restricted to [0,1], and its unit ball.
- `AnalyticConstruction.lean:22–79`: concrete curve, rotation, and correction
  data instantiate every field of the generic certificates.
- `AnalyticConstruction.lean:98–127`: actual displacement map, displacement
  1/2, positive Lipschitz constant, and unconditional existence statement.

A textual scan of `lean/OAI/GroupTheory/Thompson` found no declaration of
`axiom`, `sorry`, `admit`, `unsafe`, or `opaque`. The match `admit` in a
DyadicGapPartition comment is ordinary English. The comparator challenge
has a `sorry` at its target theorem, `ComparatorChallenges/ThompsonNonamenability.lean:83`;
this is not the proof in Main and is not imported by Main. A textual scan is
not a substitute for a kernel/axiom-closure audit.

## Independent published analytic input

The paper's bibliography identifies Benyamini and Sternfeld, “Spheres in
infinite-dimensional normed spaces are Lipschitz contractible,” Proc. AMS 88
(1983), 439–445, DOI `10.1090/S0002-9939-1983-0699410-7`.
The AMS primary publisher abstract independently confirms all three results:
Lipschitz sphere contraction, a Lipschitz ball-to-sphere retraction, and a
Lipschitz ball self-map with strictly positive minimal displacement.
Verified source:
<https://www.ams.org/proc/1983-088-03/S0002-9939-1983-0699410-7/>.
The browser's direct full-PDF request was denied with HTTP 403, so this audit
does not claim to have read the complete published proof. The theorem statement
is verified through the publisher's indexed abstract and the appendix gives
an independently reviewed construction in the required Hilbert case.

An additional exact deduction independently cross-checks the displacement
mechanism. If r:B→S is a K-Lipschitz retraction, let f(x)=-r(x). Then f(x)∈S
and r(f(x))=f(x), hence

    2 = ||r(x) - r(f(x))|| ≤ K ||x - f(x)||.

Thus `inf_B ||x-f(x)|| ≥ 2/K > 0`. Consequently an appendix-specific defect,
if later found, would not invalidate the published analytic existence input
without a separate objection to Benyamini–Sternfeld itself.

## Checkable tube/correction verification

Source locations below are in `build/sections/auxiliary.tex`.

1. **Speed and regularity (lines 22–84).** The piecewise a and θ are C¹ at
   1,2,3. For t≤2, a′=1/8; for t≥2, a≥1/4 and θ′=1. Since
   `||γ′||² = (a′)² + a²(θ′)²/3`, the speed is at least 1/8 and equals it on
   t≤1. Angular derivatives vanish on the unbounded negative ray, where a
   itself is unbounded; this is why that unbounded a does not destroy bounded
   velocity or globally Lipschitz velocity. The concrete Lean bounds are
   `Lip γ′ ≤ 1`, `Lip u ≤ 16`, `Lip v ≤ 1`, `Lip γ ≤ 7/16`.

2. **Uniform separation (lines 86–118).** The identity
   `⟨v(s),v(t)⟩ = sinc(θ(t)-θ(s))` is correct for the interval [0,1].
   Nonzero angular gaps have absolute sinc strictly below 1. The five extended
   parameter-limit cases exhaust s<t: both finite; both −∞; only s→−∞;
   finite s and t→+∞; both +∞. In the last case the squared distance is
   `2(5/16)²(1-sinc(t-s))`, whose infimum for t-s≥d>0 is positive by continuity
   plus sinc decay. No compactness of the Hilbert ball is used.

3. **Nearest point attainment (lines 120–144).** For a tube point a minimizing
   sequence eventually has residual below 2ρ. Its curve points then differ
   by less than 4ρ<σ(d), confining their real parameters to one compact
   interval. A convergent subsequence gives attainment. This explicitly fixes
   the possible nonproperness issue in an infinite-dimensional ambient space.

4. **Uniqueness and parameter Lipschitz bound (lines 146–158).** Nearby tube
   points have curve-point distance below 3ρ and hence parameter gap below d.
   The tangent Taylor estimate gives projected curve displacement at least
   `(3c/4)|t-s|`. The normal residual error is at most `ρ K_u |t-s|`.
   Choosing `ρ K_u < c/4` yields

       ||x-y|| ≥ (c/2)|t-s| = |t-s|/16.

   Applying this with y=x proves uniqueness before a parameter is selected.
   Lean `TubeNearest`, `TubeComparison`, and `AnalyticTube` preserve this
   dependency order. The concrete radius `min(1/1024, separation/8)` has
   strict slack at the fixed scale d=1/32.

5. **Rotations (lines 165–185).** A is skew-adjoint, sends u to v−κu, and
   `R=Id+A+A²/(1+κ)` is the plane rotation sending u to v, extended by the
   identity. On the span it is `κ Id+A`. κ≥0 excludes the antipodal singular
   case and makes the denominator ≥1; u=v gives A=0. The same polynomial
   formula handles the transition uniformly. Actual Lean operator norm
   Lipschitz bound is 238 (`AnalyticCurveRotation.lean:39–51`).

6. **Global gluing (lines 222–247).** With local parameter constant 16 and
   `Lip γ ≤ 7/16`, the residual is locally 8-Lipschitz. The radial correction
   β q v has a local bound `9+7/(4ρ)`, because qv is 9/16-Lipschitz in t.
   The residual correction χ(R−Id)e contributes at most
   `4 + 16 + 16·238ρ`. Including identity gives

       C_local = 30 + 7/(4ρ) + 3808ρ.

   Across the tube boundary, both cutoffs are ≤`2(ρ-r)/ρ`, so correction norm
   is at most `(7/(8ρ)+4)(ρ-r)`; distance to the curve is 1-Lipschitz and an
   outside point has distance at least ρ. Thus cross-boundary Lipschitz
   constant is `5+7/(8ρ)`. Distant pairs also obey this constant when the
   bounded additive correction is used. This is an independent reconstruction
   of the constants actually used in `AnalyticCorrection.lean`, and covers
   boundary points r=ρ as well as the inside/outside cases.

7. **Nonzero bound and outer identity (lines 249–283).** Four regions exhaust
   the tube: r≤ρ/4 gives radial coefficient b≤−1/8 and an orthogonal residual;
   ρ/4≤r≤ρ/2 gives a rotated orthogonal residual of norm ≥ρ/4;
   ρ/2≤r<ρ with t>1 gives norm ≥1/8−ρ>ρ/4;
   that same outer tube region with t≤1 has identity rotation and perpendicular
   residual ≥ρ/2. Outside the tube, γ(0)=0 forces norm x≥ρ.
   If norm x≥1/2 inside the tube then `|a(t)|>1/2−ρ>5/16`, so a is on the
   unchanged negative ray, q=0 and R=Id. Thus G=x there. Normalization is
   2/(ρ/4)-Lipschitz, norm f=1, and displacement is >1/2 for norm x<1/2 or
   at least 3/2 for norm x≥1/2. Junction equalities r=ρ/4, ρ/2 and norm x=1/2
   are correctly covered.

Adversarial checks rejected as nonissues: the curve has a bounded noncompact
tail (not a bounded proper embedding); no globally Lipschitz inverse parameter
is asserted; only close pairs use the parameter estimate; global normalization
uses a verified positive norm bound. A finite-dimensional numerical truncation
would destroy the required uniform tail separation and cannot falsify this
construction or contradict Brouwer's theorem.

## Independent finite-correlation derivation

Locations are in `build/sections/finite-proof.tex`.

The recursion (lines 124–138) is well founded by the strictly smaller cell
count in each internal restriction. The descendant-respecting assumption
gives `X_i=f(z_i)` exactly (lines 249–254). No averaging commutes with f.
Instead the correct pointwise identity is

    m - f(m) = D⁻¹ ∑_i [f(z_i)-f(m)].

Jensen for squared Hilbert norm and the Lipschitz bound yield
`δ² ≤ (L²/D)∑_i ||z_i-m||²` (lines 255–266). This is not an illicit linearity
or weak-continuity assumption on f.

For fixed i let c=1−1/D. Each parent and sibling squared-norm expansion has
D diagonal and D(D−1) separated off-diagonal terms. Their averaged upper
bounds are both `c(α+η)+1/D`. In the mixed product, every child in parent i
is strictly separated from every other parent k≠i. There are D(D−1) such
ordered terms and exactly D nested exceptions. Thus the mixed averaged lower
bound is `c(α−η)−1/D` (lines 268–296). Substituting in the squared-distance
expansion gives, with no sign restriction on α,

    2[c(α+η)+1/D] − 2[c(α−η)−1/D]
        = 4/D + 4cη.

The coefficient α cancels identically. Averaging the pointwise displacement
bound and dividing by L² yields

    η ≥ (δ²/L² − 4/D)/(4(1−1/D)).

D≥2 keeps the denominator positive; D>4L²/δ² makes the numerator positive.
The exact formulas, signed correlation hypotheses, and exceptional-column
count are present in `CorrelationVariance.lean`, `DisplacementEstimate.lean`,
and `FiniteCorrelationBoundary.lean`. No independence, exchangeability,
probability limit, or positivity of α is used.

## Quantifier and amenability checks

The operative order is

    ∃ f,L,δ,D,{I_i},S,b>0  ∀ finite nonempty A  ∃ n(A)
        [admissible on A∪SA and max_{h∈S} boundaryRatio(A,h)≥b].

All transports and b are fixed before A (lines 177–182). A∪SA is finite,
so one sufficiently fine n exists (lines 207–213). Correlation functions at
that n are defined on *all* F, bounded by 1, with zero on inadmissible inputs
(lines 154–173). The finite translation estimate applies to any such bounded
function and therefore uniformly to the A-dependent choice of n. This is a
finite sum identity, not a limiting invariant mean evaluated at an A-dependent
function. h need not preserve the other intervals because both g and hg are
separately admissible (lines 219–239). The reference-pair comparison is exact
on A, and comparison of sums cancels on hA∩A.

An amenable discrete group supplies, for this fixed finite S and any ε>0,
a nonempty finite A with every ratio below ε. Taking ε=b contradicts the
lower bound. Thus dependence n=n(A) does not swap an invalid ∀/∃ pair or
weaken the resulting boundary conclusion.

## Remaining work and release gate

This analytic route is not blocked. A material gap, if another independent
audit finds one, must be recorded with its precise lemma and not overwritten
by this favorable limited audit. No unconditional C*-simplicity or unique
trace theorem has been audited or certified here. The outstanding root-level
release gate is the independent standard-F/kernel/dependency audit plus the
distinct follow-on theorem hypotheses. No communication with any external
individual and no upstream or project Git mutations were performed by this
agent.
