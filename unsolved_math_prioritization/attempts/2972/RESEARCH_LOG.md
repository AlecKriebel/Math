# Five-attempt research log: KP-4.96

Date: 2026-10-03 UTC. Target: the closed four-dimensional fixed-class uniqueness question. These are substantive mathematical attempts, not counts of searches, downloads, or algebra evaluations. No approach below resolves the full target. Percentages are rough progress estimates toward a full proof, not probability estimates or measured quantities.

## Attempt 1: exploit the Chern-class and gauge-theory conditions

Checkpoint: 20:45 UTC. Completion estimate for the full target: 2%.

**Mechanism.** Pull the forms to one smooth manifold and try to use their canonical classes or canonical Spin-c structures to separate them.

**Work.** Checked the full proof of Salamon's Corollary A, including the b⁺=1 chamber issue and the e=0 equality case, then derived the fixed-class formulation. Derived the Moser identification of identity-component diffeomorphism orbits with constant-class path components.

**Result.** The Chern hypothesis is redundant for the closed target. A successful invariant must detect different orbits under the full class stabilizer, rather than just different canonical data or different path components.

**Exact gap.** No such pair of orbits or distinguishing invariant is constructed. The reduction identifies the problem; it does not solve it.

## Attempt 2: force an affine Moser path

Checkpoint: 20:51 UTC. Completion estimate: 3%.

**Mechanism.** Try to interpolate directly between any two cohomologous forms, then integrate Moser's vector field.

**Work.** Derived a necessary and sufficient pointwise inequality B>−sqrt(AC) for an affine segment to remain symplectic. Checked the equality case, strict failure, and the common-taming sufficient condition. Constructed a compactly supported rotation inside a Darboux chart on an arbitrary closed symplectic four-manifold.

**Result.** The inequality yields a rigorous sufficient condition for uniqueness, but the rotation produces symplectomorphic cohomologous endpoints whose affine midpoint vanishes. It is therefore invalid to infer affine-path positivity from the target's invariant equalities, or nonsymplectomorphism from affine-path failure.

**Exact gap.** No general replacement path or obstruction to all possible paths modulo diffeomorphisms is found.

## Attempt 3: search a large explicit symmetric torus family

Checkpoint: 20:52 UTC. Completion estimate: 3%.

**Mechanism.** Allow arbitrary smooth periodic coefficient functions in a T³-invariant closed form on T⁴, rather than only constant forms, and attempt to vary the symplectic geometry without changing periods.

**Work.** Classified all such forms as (4.1), computed their wedge squares and all six periods, and integrated the zero-mean coefficient differences to periodic primitives. Tested large oscillatory perturbations perpendicular to the constant coefficient vector.

**Result.** The entire fixed-class family is convex through symplectic forms; all its members are symplectomorphic. This is an elementary restricted exclusion already covered by stronger circle-invariant literature, not a novelty claim.

**Exact gap.** General forms need not have the symmetry that makes the positivity condition linear. Averaging does not supply the missing symmetry while retaining nondegeneracy in general.

## Attempt 4: use mapping classes or higher-dimensional separation

Checkpoint: 20:54 UTC. Completion estimate: 2%.

**Mechanism.** Test whether recent disconnectedness constructions or inequivalent stabilized forms provide the desired pair.

**Work.** Read the explicit construction and full Theorem 1.2 proof of Lin–Wu, and the full Ning stabilization argument. Independently derived the universal pullback-family identity (f_j⁻¹∘f_i)^*ω_j=ω_i. Tracked where the stabilized construction uses a diffeomorphism of products rather than of the four-dimensional bases.

**Result.** Pullback families cannot yield the required nonsymplectomorphism, regardless of their non-isotopy. Stabilization does not provide an unstabilized smooth identification or the required Chern matching. The restricted Kähler-type results do not cover arbitrary forms.

**Exact gap.** A mechanism separating full diffeomorphism orbits in dimension four is absent.

## Attempt 5: promote relative fillings to a closed example

Checkpoint: 20:56 UTC. Completion estimate: 2%.

**Mechanism.** Examine capping as a way to import filling nonuniqueness into the closed problem.

**Work.** Proved the relative affine Moser statement with a primitive zero near the boundary. Constructed the explicit S²×D² example distinguishing absolute exactness from the existence of a relative primitive, and computed its volume obstruction. Checked the new normalized filling preprint and its explicit separation of marked/unmarked boundary data and the closed question. Also checked the literal noncompact volume example to prevent a scope-based false solution.

**Result.** Easy relative exact deformations glue to symplectomorphic closed manifolds. Other relative examples need additional proofs of smooth/cohomology-compatible capping and of an invariant surviving arbitrary global symplectomorphisms. Neither follows automatically from filling inequivalence.

**Exact gap.** No closed construction supplies all those requirements. The intended target is therefore unresolved after five attempts.

## Reproducible verification

The final algebra package performs 11,393 deterministic exact checks using only Python's standard library. It covers the affine criterion, Pfaffian identity, Darboux-chart rotation, torus wedge formula, explicit oscillatory-family positivity, pullback composition order, and relative-volume sign. This computation validates finite controls and formulas, not the global conjecture.

The first public snapshot is frozen by SHA256SUMS. Independent review is pending at this snapshot. No historical priority or human-peer-review claim is made.
