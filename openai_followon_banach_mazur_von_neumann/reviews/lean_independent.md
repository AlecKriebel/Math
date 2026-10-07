# Independent audit of upstream family295 Lean formalization

**Status: static semantic audit; kernel reproduction not completed.**

Upstream inspected read-only at `/Users/alec/Desktop/math`, HEAD
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The intended mathlib pin is
`d13f23b723b8a846827a245b89c10fc7d3f11612`; intended Lean is 4.34.1.

## Strongest verified result

The actual solution source declares the ordinary bounded Hochschild vanishing
claim for arbitrary abstract complex von Neumann algebras, with no separability,
factor, finiteness, normality, or complete-boundedness hypothesis in its final
theorem type. This is a verified statement about the exact source and its
semantics, **not an independently kernel-checked proof of the conjecture**.
The source is not a toy model or a quotient definition that builds in vanishing.

The actual entry point is
`lean/OAI/Analysis/BoundedHochschild/MainResult.lean:13`, declaration
`OAI.BoundedHochschild.KadisonRingrose.main_result`. The comparator JSON maps
this declaration to this solution module. The comparator's `sorry` and the
scope documentation are not proof evidence and were not used as such.

The declaration is:

```lean
theorem main_result
    {M : Type u} [CStarAlgebra M] [PartialOrder M] [StarOrderedRing M] [WStarAlgebra M]
    (n : ℕ) (f : Cochain M (n + 2))
    (hf : ∀ x : Fin (n + 3) → M, differentialValue f x = 0) :
    ∃ g : Cochain M (n + 1), ∀ x : Fin (n + 2) → M,
      differentialValue g x = f x
```

Its proof extracts the predual, rewrites the pointwise cocycle condition as
`differential f = 0`, applies `KadisonRingrose.bounded_primitive`, and rewrites
back to pointwise equality. `Main.lean:79` contains `bounded_primitive`;
`Main.lean:93` contains the stronger quotient-vanishing formulation `vanishing`.

## Semantic correspondence

1. `Cochains.lean:12` defines `Cochain M n` to be mathlib's
   `ContinuousMultilinearMap ℂ (fun _ : Fin n => M) M`. These are the ordinary
   bounded complex multilinear cochains, with their operator norm. The values
   lie in the same algebra M; no finite-dimensional surrogate occurs.
2. `Cochains.lean:16` implements `mergeInputs` by replacing adjacent entries
   with their actual product and shifting the remaining inputs.
   `Cochains.lean:23` gives the usual alternating Hochschild differential.
   For a 2-cochain the expression is
   `a*f(b,c) - f(a*b,c) + f(a,b*c) - f(a,b)*c`.
3. `CentralHomotopy.lean:132` assembles this formula as a bounded multilinear
   cochain; `differential_apply` at line 137 identifies its evaluations with
   `differentialValue`. `BarDifferential.lean:153` states and proves the
   differential-squared identity.
4. `TracialCohomology/Cohomology.lean:37` defines cocycles as the kernel.
   Lines 43 and 60 define the denominator from the actual linear-map range,
   followed by the quotient `Cohomology`. There is no closure of the image,
   selected subset of cocycles, or redefinition that makes all cocycles zero.
   `cohomology_subsingleton_iff` explicitly connects quotient vanishing with
   existence of actual bounded primitives.
5. `n = 0` is degree two; arbitrary `n` covers every degree at least two.
   Degree one is outside this selected final theorem. The zero algebra is
   allowed and is handled separately in `properlyInfinite_primitive`.

## Assumptions and the abstract/concrete boundary

The pinned mathlib `Analysis/CStarAlgebra/Classes.lean:38` defines
`CStarAlgebra` using a complete complex normed unital ring with the actual
C-star identity and compatible involution. This is an ordinary unital
complex C-star algebra structure.

The pinned `Analysis/VonNeumannAlgebra/Basic.lean:45` defines `WStarAlgebra M`
by existence of a Banach space X and a conjugate-linear isometric equivalence
`StrongDual ℂ X ≃ₗᵢ⋆[ℂ] M`. The symbol here denotes the Banach space
conjugate-linear equivalence; it is not an algebraic star-isomorphism from
a fictitious dual algebra. The definition asserts the Banach-predual property,
not cohomology vanishing, injectivity, hyperfiniteness, or a trace. It is
Sakai's abstract definition. The use of a conjugate-linear equivalence is the
library's predual convention; ordinary complex linear duality can be recovered
by conjugating the predual space.

`PartialOrder` plus `StarOrderedRing` is the ordinary positive order:
`Algebra/Order/Star/Basic.lean:79` requires the positive cone to be generated
by `star s * s`. It does not impose a finite or commutative model.
Mathlib explicitly constructs `CStarAlgebra.spectralOrder` and proves
`CStarAlgebra.spectralOrderedRing` in
`ContinuousFunctionalCalculus/Basic.lean:376,397`, so these order hypotheses
can be supplied canonically for a C-star algebra.

**Exact formal semantic gap:** the pinned mathlib file explicitly says the
equivalence between its abstract `WStarAlgebra` and concrete
`VonNeumannAlgebra H` is unfinished. The audited final theorem quantifies over
the abstract Banach-predual class. It does not itself construct the
`WStarAlgebra` instance for every arbitrary concrete weakly closed operator
algebra, and the examined import closure supplies no universal concrete-to-
abstract bridge. Mathematically the abstract definition is the standard
von Neumann algebra characterization, so this is not evidence of a toy model;
it is a limitation of what the final formal theorem directly covers inside
Lean. Any claim of a fully formal concrete-operator-algebra corollary needs
that bridge or an explicit assumption of the relevant predual instance.

## Hidden-assumption and source-integrity checks

The exact transitive OAI source import closure from `MainResult` comprises
372 modules and 62,822 lines. Every OAI import resolves to an upstream source.
`research/lean_audit/import_closure.json` records the paths and SHA256 hashes.
The closure uses only Mathlib as an external import family.

A token scan of the closure found no `sorry`, `axiom`, `unsafe`, `extern`,
`implemented_by`, `native_decide`, `run_cmd`, or elaborator command. Five
matches for the word `admit` occur only in explanatory comments. The reproducible
comment/string-aware `research/lean_audit/static_audit.py` scan also found zero
forbidden code-token hits, including `opaque` and declaration-form `constant`.
Its result is saved as `code_token_scan.json`. An ordinary function named
`constant` in `Ultrapowers.lean` denotes the constant-sequence embedding; it
is defined explicitly and is not an axiom declaration. Neither scan is a
kernel axiom dependency print.

Intermediate names `ProperlyInfiniteVanishingInput` and
`ClassicalVanishingInput` do encode conditional vanishing propositions, but
they are not assumptions of the final theorem: the source supplies
`properlyInfiniteVanishingInput` and `classicalVanishingInput` as theorems in
`ProperlyInfinitePrimitives.lean:35,44`. `bounded_primitive` consumes that
proved source declaration. The central type decomposition is also obtained
from a source theorem rather than an extra final input. No tautological
external cohomology assumption appears in the final declaration.

This is a static audit of declared proofs. It does not establish that all
372 files elaborate or that their proof terms depend only on the permitted
axioms. The comparator JSON lists `propext`, `Quot.sound`, and
`Classical.choice` as permitted; that list is a policy statement, not an
actual `#print axioms` result.

## Reproduction attempt and exact remaining gap

An isolated minimal build was prepared in `research/lean_audit/build`, with
exact copied OAI sources and Lean 4.34.1. There were no compiled upstream
artifacts and no usable compiled pinned mathlib cache already present.
The full upstream `Mathlib` umbrella is imported in 123 modules, so the exact
build cannot be reduced to a few selected mathlib modules without changing
an input. The volume initially had only about 755 MiB available and ran out
of space during dependency setup; the attempt was stopped and its own
disposable partial downloads were removed. The child `research/lean_audit/kernel_build_report.md` and
`build/dependency_update.log` preserve the precise dependency failure: Lake
update exited 1 after Git fetch reported “No space left on device”. No upstream file was changed.

**Not reproduced:** a successful clean build/import of MainResult;
`#print axioms` for `main_result`, `bounded_primitive`, `vanishing`, and
`normal_tracial_primitive`; proof-term consistency of all dependencies.
No formal-verified theorem should be advertised on this audit alone.

The strongest justified promotion is: “the pinned source contains a
semantically faithful, apparently axiom-free proposed Lean formalization of
ordinary bounded higher Hochschild vanishing for abstract complex von Neumann
algebras; clean kernel reproduction remains outstanding.”

## Checkpoint

At 2026-10-06T22:16:40.074235-07:00, the static semantic/source audit is estimated 90% complete; the overall formal validation is estimated 45% complete because the central independent kernel reproduction remains undone. The exact gap is environmental reproduction, not a discovered counterexample or a proved theorem.
