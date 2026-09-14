# Formalization design — 2026-09-14

The full 1,671-line local manuscript was read before implementation. Its statements and previous reviews are evidence, not axioms. No theorem about the original-process amplifier is currently established here.

## Exact target and representation

Use a finite vertex type, a symmetric nonnegative real weight function with zero diagonal, positive weighted degree, and connected positive-edge support. Mutant states are finite vertex subsets. For fitness r>0, a labelled event replaces target v by parent u's type. Bd event probability is f(S,u)/sum_x f(S,x) times w(u,v)/degree(u). dB event probability is 1/|V| times f(S,u)w(u,v)/sum_x f(S,x)w(x,v). Aggregate all events, including unchanged states. Prove nonnegativity, row sums, and the two absorbing boundaries.

Define finite-horizon fixation recursively by the probability of hitting the all-mutant state within k steps, and eventual fixation by its supremum. This gives a definition without presupposing absorption or invertibility. Prove boundedness, monotonicity, the harmonic equation, and equality with the unique absorbing boundary-value solution; prove finite connected Moran absorption separately. Uniform singleton initialization is the arithmetic mean. Complete-graph comparators use exactly the same kernels and initialization; closed formulas are derived lemmas, never definitions substituted for the process.

The final proposition will quantify a sequence of positive couplings before r. Each graph is the exact hybrid with C=t^4, q=t, m=floor(lambda*t), W=C/sigma, unit clique/pendants and all satellite–clique edges of weight epsilon_t. To avoid degenerate t=0,1 graphs, use index t with construction parameter t+2 (equivalently extend the sequence finitely). Include order divergence and both strict comparisons for every fixed 1<r<Rhyb with a common eventual index depending on r. Define the isolated sextic root only after proving unique existence. A typed `def ... : Prop` will record the unproved target; do not insert a theorem with a placeholder proof.

## Dependency map and gain budget

| Node | Manuscript | Inputs and required precision | Formal status at design |
|---|---|---|---|
| M0 | Model §2 | labelled events, absorption, singleton average | missing |
| M1 | §2 baseline formulas | count lumping + gambler's ruin; dB n≥2 | missing |
| G | §3 construction | positive sigma, lambda, coupling; connectedness, order | missing |
| L | strong orbit lumping | kernel equivariance + transitivity on every fibre, all sizes | missing |
| W | finite weak-cut trace | fast-block inverse and scaled interior Schur inverse; uniform on fitness compacts | missing |
| E | early establishment | O(log C/C)+O(r^-K), smaller than q/C | missing |
| C | confinement and cleanup | O(C^-B) for any B plus polynomial times exp(-gamma C); hidden coordinates allowed | missing, audit repair |
| I | pendant initialization | Bd 1-o(1), dB O(1/C), multiplied by m/C | missing |
| R | reciprocal renewal | ordinary fixation and dB portal o(1/C), compact-uniform | missing |
| H | center proposition | core p+o(q/C), center average expansions | depends E,C,I,R |
| A | gate + sweep | mutant center 1-o(q/C), pair gate o(1) error | depends W,H,R |
| F | response functions | normalized error o(q/C); baseline error O(1/C) | depends M1,W,H,A |
| P | exact root and positivity | unique root (3/2,151/100), positive responses on open interval | missing |
| D | diagonal | finite-t uniform convergence selects epsilon_t; scaled perturbation ≤1/t | depends W |
| MAIN | main theorem | G,M0,M1,F,P,D; exists family before forall fitness | missing |

The gain is q/C=t^-3. Multiplying an O(1) center mass requires an o(t^-3) error, while an O(t^-3) satellite/pendant mass needs only o(1). Reverse-center rate must be o(C^-1), so q reversals remain o(q/C). Floors cost O(1/t) in the scaled responses. No uniform threshold over the entire open interval or endpoint gain is inferred.

## Reusable infrastructure and gaps

The repository has two Lean projects, Bell and symmetric_sector_lean, pinned to Lean 4.19.0 and mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b. The latter formalizes a different symmetric-sector matrix calculation; it does not supply general Moran, absorption, lumpability, or asymptotic center lemmas. Reuse the pin and build conventions, not their domain results. The local dependency cache is reused through an ignored symlink to avoid duplicating gigabytes, with no dependency update.

Mathlib supplies finite sums/matrices, simple-graph reachability, conditionally complete real suprema, finite Markov/PMF kernels, matrix inverse and Schur complements, topology on finite-dimensional spaces, compact uniform continuity, asymptotics and real limits, polynomial differentiation and intermediate value theorems, rational normalization, and discrete martingale optional stopping. Exact APIs will be checked against the pinned source. Missing domain infrastructure is substantial: graph-event kernels, finite absorption bounds, orbit quotient semantics, singular perturbation trace identification, adapted embedded-chain comparison and regenerative estimates, and all center asymptotics.

Preferred route: finite substochastic matrices and harmonic/subharmonic functions. Uniformize finite continuous-time rate tables using a state-independent rate bound and prove invariance of absorption under holding/time changes. Resolvent identities can replace path-measure machinery for finite expected occupation/hitting estimates. Discrete repeated-attempt inequalities can replace continuous-time strong Markov arguments. This route must prove the bridge to the original kernels; it cannot merely define fixation as a guessed harmonic expression.

## Trust and validation

Use Lean kernel checked proof terms, with disclosed standard foundations (`propext`, `Classical.choice`, `Quot.sound` as actually reported). No custom axioms, sorry/admit, sorryAx, native_decide, or externally accepted numerical answers. `ring`, `norm_num`, and `nlinarith` may generate kernel-checkable certificates. Source checksum scripts and existing Python/SymPy certificates provide provenance/discovery evidence only, outside the theorem trust boundary. Pin dependencies in the manifest and inspect transitive theorem axioms with `#print axioms`; audit signatures separately because absence of axioms does not rule out inappropriate hypotheses.

Independent tasks started with distinct scopes: source/statement correspondence, stochastic repair and center estimates, and finite weak-cut/macro analysis. Formal algebra and generic finite-chain work will be reviewed against definitions before inclusion. Every promotion reports proved declarations and unproved obligations. Effective least-dyadic computability and architecture optimality are supplementary, not prerequisites to the main nonconstructive existence proof.
