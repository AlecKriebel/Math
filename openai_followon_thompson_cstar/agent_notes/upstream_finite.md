# Independent finite-combinatorial audit of source family 248

Audit checkpoint: 2026-10-06 22:15 PDT (2026-10-07 05:15 UTC).
Auditor: internal independent AI research agent `upstream_finite`.
Source clone was read only throughout. No external individual was contacted.

## Verdict and exact scope

I independently reconstructed the pivotal argument in the pinned manuscript and
did not identify a material mathematical gap or a counterexample. The finite
correlation argument proves the displayed positive uniform boundary bound once
the displacement map is supplied. The appendix supplies that map with a valid
infinite-dimensional construction. Thus my strongest mathematically checked
result is the manuscript's nonamenability theorem for the ordinary increasing
dyadic piecewise-linear Thompson group F, by a manual proof audit. This is
verification of an attributed upstream result, not a new proof claimed by this
project and not conventional human peer review.

The actual formalization has also been inspected for semantic agreement, but
**a successful fresh Lean build has not yet been reproduced in this audit**.
Disk space initially prevented beginning the dependency preparation. Merely
finding the formalization is not being treated as a build certificate. The
remaining gap in this audit is formal-build reproduction, not a located
mathematical gap in the argument.

Best-guess completion estimates for this assigned audit at this checkpoint:
manual upstream mathematical audit 100%; formal reproduction 10%; follow-on
publication-package work is outside this agent's assignment and is not estimated.

## Pinned material actually read

Repository: `/Users/alec/Desktop/math`.
Pinned and observed HEAD: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
The tracked source checkout was clean on read-only inspection.

Read the repository README, family README and manuscript citation metadata,
all four section sources (`introduction.tex`, `finite-proof.tex`,
`auxiliary.tex`, `consequences.tex`), the mixed-pair figure source, and the
manuscript bibliography. The source consequences are near-unitary uniformly
bounded nonunitarizable representations and percolation statements; neither
contains the proposed four-group C*-simplicity application. The introduction
does discuss the older Haagerup--Olesen direction from C*-simplicity of T to
nonamenability of F. This does not establish novelty of the follow-on package.

Also read `lean/docs/248.md`, the actual solution `Main.lean`, the model and
standard group identification, finite-boundary and transport modules, the
analytic model and construction statements, the mean-to-Følner bridge, and
the comparator statement/configuration. The source's bibliography was read
as an inventory, not a claim that every cited primary paper has been audited
in full by this agent. Parent agents own the follow-on primary-source and
priority checks.

## Independent reconstruction of the finite mechanism

1. A basic cell contained in a basic interval remains basic after normalized
   affine restriction. The affine charts compose, so restricting to I and
   then J is exactly restricting to the affine copy I·J. Basic dyadic
   intervals with intersecting interiors are nested. Therefore any basic
   partition whose mesh is strictly smaller than |I| respects I.

2. An ordinary element of F has finitely many dyadic breakpoints and affine
   pieces `2^q x+b` with dyadic b. A sufficiently fine uniform source grid
   resolves breakpoints and makes each image cell basic. Its mesh tends to
   zero. This proves eventual admissibility for every prescribed finite
   family of intervals and finite family of group elements. No global
   admissibility in g is claimed or needed.

3. Two separated internal basic intervals leave three nonempty dyadic gaps.
   Each gap can be partitioned into basic cells. Repeated bisection increases
   the number of cells by exactly one, allowing the corresponding source
   and target gap counts to be equalized separately. Matching corresponding
   cells defines an increasing genuine F element: knots are dyadic and
   slopes are ratios of powers-of-two lengths. The selected intervals stay
   single corresponding cells, so they are mapped affinely. No unsupported
   arbitrary two-interval transport property is being inserted here.

4. If h maps I affinely to I', then on I the identity
   `s_(I')^{-1} h = s_I^{-1}` holds. For sufficiently admissible image
   partitions it identifies the normalized restrictions exactly. Breakpoints
   of h elsewhere have no effect on this identity inside I.

5. Each normalized parent restriction has strictly fewer cells than its
   partition, because the parent is internal and the partition has cells
   outside it. The coloring is therefore a genuine finite induction, with
   unit-ball values. Its recursive identities at parent/descendant pairs
   use only the restriction associativity in item 1.

6. Choose D, the parent/descendant interval family, and all pair transports
   before the finite test set A. The set S of transports is fixed. Given A,
   choose one n admitting all of `A ∪ SA`. The dependence of n on A is
   harmless: cancellation works for every globally bounded scalar function,
   uniformly in n. Defining nonadmissible colors to be zero makes the scalar
   functions globally bounded and removes any partial-function issue.

7. For any separated pair in the family, exact covariance followed by
   cancellation over `hA ∩ A` bounds its averaged correlation's distance
   from the reference α by η, where
   `η=max_(h∈S) |hA Δ A|/|A|`. The estimate uses the symmetric difference
   itself, not half of it, since values lie in [-1,1]. Reversing a pair uses
   symmetry of a real Hilbert inner product. Nested pairs are never assigned
   this correlation comparison.

8. Put `m=D^{-1}Σ_k X_k` and `z_i=D^{-1}Σ_j Y_ij`. Off-diagonal parent
   correlations and off-diagonal sibling correlations are all separated.
   The mixed pairs `(Y_ij,X_k)` are separated exactly when `k≠i`;
   precisely D of the D² mixed pairs are own-parent nested exceptions.
   Bounds ±1 on the exceptional correlations give

   ```text
   E||m||², E||z_i||² ≤ (1-1/D)(α+η)+1/D,
   E<z_i,m> ≥ (1-1/D)(α-η)-1/D,
   E||z_i-m||² ≤ 4/D+4(1-1/D)η.
   ```

   The α terms cancel without assuming α≥0. There is no exchange of
   an infinite sum/limit and no independence assumption on the colors.

9. The exact recursion says `X_i=f(z_i)`. Convexity of squared Hilbert norm
   and the L-Lipschitz estimate imply pointwise
   `δ²≤(L²/D)Σ_i||z_i-m||²`. Averaging yields

   ```text
   max_(h∈S) |hA Δ A|/|A|
     ≥ (δ²/L²-4/D)/(4(1-1/D)) > 0
   ```

   when `D≥2` and `D>4L²/δ²`. This is a fixed-S, all-nonempty-finite-A
   estimate and contradicts the left Følner criterion.

## Attacks on the infinite-dimensional input

The Hilbert space is real `L²([0,1];R²)`, which is infinite dimensional.
Replacing it by a finite-dimensional model would invalidate the displacement
input; this audit did not make that replacement.

The piecewise formulas for a and θ have matching first derivatives at all
junctions. Direct differentiation gives
`||γ'||²=(a')²+a²(θ')²/3`. For t≤2 the first term is 1/64; for t≥2,
the second is at least 1/48. Hence the global lower speed c=1/8 is correct.
The derivative is globally Lipschitz, including the negative half-line where
the angle is constant. Normalizing a derivative bounded away from zero
makes the unit tangent Lipschitz.

The crucial bounded-tail issue was checked directly. Although γ(t) has a
bounded positive tail, `⟨v(s),v(t)⟩=sinc(θ(t)-θ(s))`. In every possible
extended-limit case, parameters separated by a fixed d>0 have curve points
separated by a positive amount. In particular on the constant-radius tail,
the required estimate is `sup_(q≥d) sinc(q)<1`, which follows from
continuity, strict inequality away from zero, and decay. This supplies the
uniform-separation property without incorrectly claiming compactness of the
bounded tail in Hilbert space.

Uniform separation confines a minimizing sequence's sufficiently late
parameters to a compact real interval, so a nearest curve point exists in
the small tube. The local tangent estimate and tangent orthogonality then
give uniqueness and `|t(x)-t(y)|≤16||x-y||` for close tube points. Taking
y=x for competing minimizers is valid because both residuals are strictly
smaller than the tube radius.

The explicit rank-two rotation formula is orthogonal, maps u(t) to v(t),
and remains Lipschitz at u=v because its denominator is 1+κ≥1. The residual
is perpendicular to v after rotation. I checked the cutoff junctions and
all three nonvanishing cases (`r≤ρ/4`, `ρ/4≤r≤ρ/2`, and `ρ/2≤r<ρ`).
The lower bound `||G||≥ρ/4` survives the transition annuli. The global
Lipschitz argument handles close tube points, separated pairs, and pairs
crossing the tube boundary, using distance-to-curve being 1-Lipschitz.

For ||x||≥1/2, the tube radius and maximal positive radius force the curve
parameter onto the negative straight portion; both correction terms vanish,
so G(x)=x. Consequently `f=-G/||G||` has norm one and displacement at least
1/2 throughout the unit ball. The normalization Lipschitz estimate 8/ρ is
consistent with the lower norm bound ρ/4. No circular use of nonamenability
occurs in this construction.

As an external cross-check, the original Benyamini--Sternfeld abstract
explicitly states that every infinite-dimensional normed-space unit ball has
a Lipschitz self-map with positive minimum displacement:
https://www.jstor.org/stable/2044990 ; the primary journal record is
https://www.ams.org/proc/1983-088-03/S0002-9939-1983-0699410-7/ .
This confirms the type of input, independently of the appendix construction;
the full historical proof was not used as a substitute for auditing the
appendix.

## Checkable independent finite experiment

`../upstream_finite_checks.py` uses exact Python rational arithmetic and
independent dyadic PL code. It constructs the three-gap transports rather
than assuming their existence. It checks all separated pairs for D=2,3,5,7,
affine covariance on refined cells, actual normalized restriction
associativity, well-founded recursive identities under a nonconstant bounded
scalar Lipschitz coloring, and one fully enumerated nontrivial image
partition. The scalar coloring intentionally has a fixed point; it tests
only the combinatorial identities and is not a displacement witness.

Reproduce with `python3 upstream_finite_checks.py` from the project folder.
Observed result:

```json
{
  "status": "pass",
  "transport_pairs": 1969,
  "local_covariance_cells": 31504,
  "recursive_identities": 17,
  "fully_enumerated_image_level": 10,
  "fully_enumerated_image_cells": 1024,
  "scope": "Exact finite dyadic checks, not a theorem/formal build certificate"
}
```

These checks exercise likely failure points. They are not evidence for an
arbitrary infinite-dimensional displacement construction and do not replace
the all-A mathematical argument.

## Actual Lean scope and semantic agreement

The scope document `lean/docs/248.md` exists. The comparator statement's
intentional `sorry` is a challenge target, not the solution. The actual
solution declaration is
`OAI.ThompsonNonamenability.thompson_F_nonamenable_composition` in
`lean/OAI/GroupTheory/Thompson/Main.lean`.

The F carrier is the subtype of actual increasing homeomorphisms of [0,1]
with finite dyadic knots and affine pieces of slopes `2^q`, q∈Z. The
`DyadicPLWitness` does not assume amenability, boundary expansion, transport
existence, or the theorem to be proved. `StandardCharacterization.lean`
removes even the explicit subdivision-cover field from the standard
condition, deriving coverage from ordered endpoints. `StandardF.lean`
derives the subgroup/group structure by genuine PL closure and proves
`F.mul_apply` definitionally agrees with h∘g.

`InvariantMean` is a positive normalized real linear map on bounded real
functions, invariant under g↦h*g. Positivity supplies norm control; the
formal mean-to-Følner bridge has no countability/finitely-generated premise.
The analytic Hilbert model is `Lp (EuclideanSpace R (Fin 2)) 2` for Lebesgue
measure restricted to [0,1], agreeing with the paper's real Hilbert space.
The actual displacement declaration is not assumed as an axiom: it is
supplied by the analytic construction and its preceding curve/tube modules.
The fixed transport set and all-A boundary theorem are also supplied by
actual constructions, not an abstract input property of a fabricated group.

Main additionally proves `thompson_F_boundary_with_exact_constant`,
`thompson_F_uniform_boundary`, and `thompson_F_not_amenable`. The symbolic
constant is exactly the displayed manuscript formula. The scope document's
statement that it does not give an explicit boundary constant is a conservative
or stale description; Main does give a symbolic constant depending on its
constructed Lipschitz constant, while no small numerical bound or prescribed
generating set is supplied.

A recursive import scan from the actual solution Main finds 68 OAI modules,
9,457 lines, 372,798 bytes, and 71 distinct direct external imports in the
Lean and Mathlib namespaces. Every module's checked-out bytes equal the
pinned Git object's bytes. No `sorry`, `admit`, `axiom`, or `unsafe`
declaration was found in the Thompson solution folder (word occurrences in
ordinary comments do not introduce assumptions). The only required external
library for this import closure is Mathlib and Lean's own tactic support;
the release's unrelated external packages need not be downloaded to check it.

Pinned versions: Lean `leanprover/lean4:v4.34.1`; Mathlib commit
`d13f23b723b8a846827a245b89c10fc7d3f11612`. The v4.34.1 toolchain is locally
installed, but the existing shared Mathlib cache was not assumed to match
this pin. Source clone and shared cache remain unmodified. A fresh build and
`#print axioms` inspection of the final theorem are the remaining formal
verification operations.

## Repairs and disposition

No mathematical repair is proposed because no defect was found. Do not
weaken the upstream result to an unjustified assumption solely because the
problem was historically open, and do not promote a code-presence check
into formal verification. Parent agents still must verify the precise
Le Boudec--Matte Bon implication, trace theorem, action models, countability,
priority, attribution, and final publication package. This audit alone
does not resolve those follow-on obligations.
