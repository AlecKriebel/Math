# Research log

Target: **30003656 / OWR-15958-003**. Date: 2026-10-03 (UTC).

## Readiness, 17:03–17:06

- Required problem page inaccessible (HTTP 403); recovered identity from the pinned record and independently retrieved the OWR report and author preprint.
- Corrected the initial domain interpretation: redundancy concerns geometric consequences of a nongeometric sentence, not redundant operations or equations in an algebraic presentation.
- Fixed one-sorted, finitary, total-operation conventions, with logical equality and nullary operations allowed.
- Live queue: queued, 0/5. No exact previous attempt or related-target group found in the bounded checks described in `SOURCE_GATE.md`.
- Blechschmidt's primary-source warning shows that a bare excluded-middle construction is not a novelty claim.
- Estimated completion toward an independently usable resolution: **15%**. Precise scope remained the main risk.

## Substantive approach 1: classical conservativity, 17:06–17:07

Candidate mechanism: take an excluded-middle instance about equality in the empty algebraic theory. Coherent/geometric conservativity of classical over intuitionistic deduction supplies redundancy; the generic object's collapsing maps can defeat decidable equality.

Outcome: a literal-scope diagnostic, **not a new contribution**. Blechschmidt explicitly already records the general excluded-middle obstruction. This route cannot support an originality claim or evade the intended-source caveat. It also leaves unnecessary metatheoretic conservativity dependencies if used as the principal proof.

Estimated completion: **30%**. The literal statement is demonstrably suspect, but a more informative constructive example is preferable.

## Substantive approach 2: pointed objects and negative universality, 17:07–17:15

Chosen T: one sort, one constant c, no nonlogical equations. Chosen sentence α=¬∀x¬¬(x=c).

The unbounded proof is complete at author stage:

1. In the generic pointed object over finite pointed sets/all pointed maps, every element can be collapsed to c at a later stage. Consequently β=∀x¬¬(x=c) holds.
2. In the pointed-injection model, distinctness from c is persistent. Every stage embeds in one with a fresh non-basepoint element, so no stage forces β and every stage forces α.
3. Restriction from all maps to injections is conservative and preserves all geometric interpretations because the categories have identical objects and limits/colimits are objectwise. It reflects geometric sequents, proving T-redundancy of α.
4. An independent direct route establishes geometric completeness using the finite pointed quotient of a finite equality antecedent, then extracts witness terms and disjuncts. This avoids relying on a source theorem or classical completeness for the key redundancy step.

The two-constant source pitfall does not arise: a single constant adds no disjointness condition to T. The constant also removes empty-sort ambiguity. Unlike an excluded-middle tautology, α is classically false in the one-point model. The proof never uses ¬∀θ⇒∃¬θ.

Outcome: **complete candidate counterexample to the literal definition**, so the five-turn search budget is stopped early at **2/5**. The remaining planned search turns are not spent or reclassified as review. Subsequent work is validation of this fixed candidate only.

Estimated completion toward an independently usable resolution: **85%**. Mathematical, source-scope, and priority reviews remain.

## Fixed-candidate validation, 17:15–17:18

Three distinct validation routes were recorded, without extending the search budget:

- **Categorical audit:** distinguish the genuine classifier [C,Set] from the conservative model [D,Set]; check covariance, inverse-image direction, objectwise conservativity, and the geometric/nongeometric preservation boundary.
- **Syntactic audit:** normalize geometric antecedents, take the finite term quotient, and recover disjuncts/existential witnesses. Include arbitrary set-indexed disjunctions and no new language symbols.
- **Exact finite audit:** independently evaluate the forcing clauses on all pointed maps versus pointed injections among five finite objects. All 1,279 maps and 89 injections are included. All checks pass; 64 equality-premise sets yield 1,024 verified atomic-consequence comparisons. The code explicitly tests the one-point stage, where α holds in the injection model but ∃x¬(x=c) does not.

These checks support the explicit proof; none is represented as a finite proof of a universal categorical assertion. Literature checking remains bounded, and the 2019 follow-up's full text has not been verified.

## Freeze and exact remaining obligations

The public author package is frozen by `FROZEN_AUTHOR_MANIFEST.json` before independent audit. No remote mutation or publication was performed by the author-stage investigation.

The fresh reviewer must:

1. Try to falsify the forcing calculations, especially the direction of arrows and the use of fresh elements versus collapse maps.
2. Verify the pointed-object classifying topos and that α stays in the original signature.
3. Verify geometric-consequence reflection, including equality and arbitrary disjunctions, and the independent quotient proof.
4. Check the exact OWR/2018 target for any additional scope condition omitted from the extracted statement; explain any such condition rather than infer it.
5. Check whether the example or a stronger algebraic negative result is already known, especially in the 2019 Bezem–Coquand paper.

Current estimate: **85%** toward an independently usable result. The literal theorem has a complete author proof; independent correctness/scope verification and historical priority are not yet established.
