# Formal dependency audit: family 197 companion construction

Checkpoint: 2026-10-06 20:48 America/Los_Angeles (2026-10-07 UTC).
Reviewer: independent AI-assisted formal-source reviewer.
Formal-source scope completion estimate: 90%; pinned build completion: 0%.
This estimate concerns this narrowly assigned audit, not either overall target.

**Status: NOT BUILT; NOT USED as a retained theorem dependency.** The audit
does not certify any Lean theorem. It establishes the actual source statement,
its source-level dependency mechanism, and its distance from the torsion-free
manuscript. Parent expressly instructed no toolchain installation or import
changes after the storage feasibility assessment.

## Immutable sources and version coverage

All mathematical source inspection used OpenAI commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
`source_records.json` records 137 unique text files (667,176 bytes), each with
immutable raw URL, SHA-256, Git blob SHA-1, and observation timestamp. The
canonical sorted path/SHA-256 identity is
`08ba875ab2bf774a3d5b24490814bf2f0ad0c6eb6f78f5e88f6b3d49ae65455b`.
This set includes the transitive OAI imports of the theorem plus comparator,
catalogue, configuration and README evidence. Byte copies are stored only in
the effort's ignored `sources/formal_adc7f124/` directory.

The API current-history and theorem-path-history queries, recorded in
`version_and_runtime_receipt.json`, returned only the initial commit above.
Thus no subsequent public repository correction was visible in those queries
at retrieval. Commit author/committer timestamps are not authenticated public
priority dates. This audit did not search the complete literature or all
off-repository correction channels.

The [formalization catalogue](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/formalization.yaml)
lists the September 23 characteristic-two manuscript among its source papers
and the declaration below among formal declarations. It does not list the
October 4 torsion-free manuscript as a formalized source paper. A common
family number does not make these results interchangeable.

## Exact theorem and model translation

The [actual theorem](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/OAI/RingTheory/DirectFiniteness/FinitelyPresented.lean)
`OAI.KaplanskyCounterexample.finitelyPresented_counterexample` states:

There exist a field `K` with `Fintype K` and `CharP K 2`, and a group `G`
with `Group.IsFinitelyPresented G`, such that (i) there exist an odd prime
natural number `ell` and `g : G` with `orderOf g = ell`, and (ii) there exist
`a_out b_out : MonoidAlgebra K G` with `a_out * b_out = 1` and
`b_out * a_out != 1`.

`MonoidAlgebra K G` is Mathlib's finite-support group algebra, not an
unbounded-function algebra or a ring named to resemble one. The statement
does not specialize `K` to `F_2`. It explicitly requires nontrivial odd-prime
torsion, and so cannot be the claimed torsion-free theorem. The encompassing
`thm_main` adds certificates concerning prescribed data, the least successful
outer input `selectedH <= 217`, and the prescribed output group and pair.

If this finite-field theorem were independently established, it could still
supply an alternative input for the existence question in Target A: the
additive group of the finite field `K` is a finite, finitely generated Hopfian
lamp group. Its restricted direct sum over an acting group identifies with
the additive group of `K[H]`, and the same right-multiplication map applies.
That observation neither validates the imported result nor yields the more
specific `F_2` and torsion-free input. The alternate route is not retained.

## Dependency mechanism actually inspected

| Layer | Source-level mechanism | Status and exact boundary |
|---|---|---|
| Final quantified claim | `finitelyPresented_counterexample = thm_main.1`; witnesses are `Prescription.Output.Coeff`, `Output.G`, `Output.a`, `Output.b` | Statement inspected; not elaborated or kernel checked |
| Prescribed products | `Output.prescribed_products` invokes `ChosenCriterion.products`, with proved size, global matrix, local matrix and distinct-character inputs | Does not assume final `ab=1` or `ba!=1` as a field |
| Rank defect | `CharacterTwist.defect_ne_zero` pulls a zero claim back through an injective group-algebra map, applies a character evaluation and contradicts rectangular matrix rank | Actual nonvanishing lemma inspected; depends on base and HNN embeddings |
| Point-group embedding | `AssignedDevelopment.point_injective` invokes `GluedGroup.theta_injective` and `generator_ne_one` | Final point injectivity is proved in source from incidence girth and local independent direction maps |
| Actual presentation translation | `WordReduction.of_presented_eq_one` uses Mathlib `PresentedGroup`, normal closure and finite relator insertions/deletions | Presentation equality is translated to a word reduction rather than an assumed van Kampen diagram |
| Drawing translation | `OpenDiagram.initial`, `OpenDiagram.related_iff`, `deleteWordBlock`, `insertWordBlock`, and `close` convert a hypothetical generator collapse into a balanced genus-zero ribbon | Source constructors must prove diagram fields; merely listing those fields is not assumed coverage |
| Diagram obstruction | `WeakBalanced.not_genusZero` minimizes edge count then vertex count, eliminates zero weights/parallel edges and reduces to black/white/face degree and Euler inequalities | Source proof inspected; no claim of complete independent mathematical reconstruction here |
| Multiple HNN embedding | `MultipleHNN.finite_partial_realization` iterates Mathlib `HNNExtension.of_injective`; `of_injective` realizes all finite stable-letter relations | Depends on the pinned Mathlib Britton lemma; this audit did not build or fully audit that Mathlib proof |
| Finite presentation and torsion | `PrescribedPresentation` invokes the finite short-relator presentation and finite multiple-HNN/product results; `OddTorsion` retains odd-prime order | Corresponds to the torsion companion, not torsion-free root protection |
| Finite-data existence | `succeeds217`, finite-field/prime certificates, alteration estimates and slab selection prove existence; `Nat.find`/classical choice select the first successful data | Mostly noncomputable existential source proof, not an actually executed astronomical finite search |

The ribbon definition is the explicit Euler equation
`cycles(black)+cycles(white)+cycles(white*black)=edges+2*components`.
Thus the relevant drawing claim is about a specified finite combinatorial
model. Correct application to the actual presented group is supplied by the
word and drawing translations above; a valid model-definition audit and
kernel build remain necessary. Source inspection found no final injectivity
or product claim hidden as an undischarged structure assumption. It did not
independently prove every source lemma or validate every model boundary.

**No inspected declaration provides the October 4 construction's graphical
asphericity, root protection, torsion freeness or `F_2` nonvanishing.** Those
manuscript assertions must stand on their own mathematical audit.

## Axioms and placeholders

The [comparator configuration](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/KaplanskyFinitelyPresented.json)
allows only `propext`, `Quot.sound`, and `Classical.choice`; it sets
`enable_nanoda` to false. The challenge statement contains `sorry`, as does
the simpler direct-finiteness challenge. These are challenge templates, not
the actual solution module. The solution's OAI source closure has no detected
`sorry`, `axiom`, `admit`, `unsafe`, `implemented_by` or `native_decide` tokens
outside comments. The only additional scan hit is `unsafe` in Lake's
configuration-time dependency inspection, not a mathematical declaration.

`audit_formal_sources.py` performs nested-comment-aware textual scanning and
hashing. `source_scan_receipt.json` preserves all hits and the import boundary.
A clean text scan is weaker than Lean elaboration, `#print axioms`, proof-term
export, comparator checking, or independent reconstruction. Imported Mathlib
and Lean/Lake libraries are outside the recorded OAI source closure; no
absence-of-axioms claim is made about those transitive compiled dependencies.

## Build and resource receipt

The pinned environment requires Lean `v4.34.1` and Mathlib commit
`d13f23b723b8a846827a245b89c10fc7d3f11612`. Only Lean `v4.19.0` was installed.
At assessment, free space was approximately 3.3 GiB, the existing older
toolchain occupied 1.5 GiB, and an unauthenticated older/local Mathlib cache
occupied 276 MiB. The official 4.34.1 ARM macOS toolchain archive is
562,038,070 bytes compressed before expansion. Every relevant mathematical
source imports the umbrella `Mathlib`, requiring its complete pinned import
closure to reproduce the original source. Toolchain installation plus that
closure/cache risked filling the available disk. No toolchain was downloaded,
no imports were changed, and no misleading older-version build was run.
`build_feasibility_receipt.json` records the observed state and decision. Its
later final observation found approximately 7.1 GiB free after concurrent
changes elsewhere; this reviewer removed no unrelated files. That later
change was after the parent's express no-install instruction and did not lead
to a pinned build. The storage assessment is a limitation of the attempted
reproduction, not a theorem falsification.

To reopen this alternate route, provide enough storage for an isolated
original pinned environment, build
`OAI.RingTheory.DirectFiniteness.FinitelyPresented`, inspect its elaborated
statement and actual axiom dependency, and run its comparator with the exact
challenge. Then independently validate the finite-data, group-model and
presentation translations. A successful build alone would not discharge the
torsion-free manuscript or all independent mathematical scrutiny.

## Retained finding and unresolved gap

The catalogue label supplies no formal validation of the torsion-free input.
The alternate characteristic-two formal source contains substantive explicit
proof mechanisms and no detected OAI placeholders; it remains **unbuilt and
unvalidated** here. This is an exact obstruction to claiming a checked formal
route. It is not, by itself, a counterexample to or a proof gap in a separately
audited handwritten torsion-free argument. No unconditional Target A result
is inferred from these source findings.
