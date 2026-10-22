# Five-approach research log

Date: 2026-10-04 UTC. Numeric ID 30001988. Completion estimates below concern the full mathematical resolution, are subjective, and are separate from completion of this bounded investigation.

## Source triage, 16:32-16:37

Read repository and queue instructions; verified the live own row, absent attempt/state entry and PR duplicates. Tried the prescribed catalogue page, then inspected the official report and later primary literature. Corrected the splitting/constraint distinction and complement convention. The existing theorem does not have the target's full scope. No substantive source text or dataset extract is included in the public packet.

## Approach 1: ordinary-field splitting, 16:37

Mechanism: identify K<z> with a rational-function field in the computable algebraically independent jet sequence. Apply ordinary factorization and Gauss-type preservation under further transcendental extension.

Result: ordinary irreducibility is reduced to the base splitting oracle, but delta Y is an explicit algebraically irreducible polynomial with an unconstrained pair (delta Y,1). Roots 0 and 1 supply the distinguishing polynomial Y. The desired differential predicate is therefore not the ordinary factorization predicate.

Gap: a constraint/isolation algorithm, even after all algebraic factorizations are known. Stopped this shortcut rather than treating the title as the mathematics. Estimate: 10%.

## Approach 2: high-order specialization, 16:38

Mechanism: inspect how a high-order constrained specialization of the differential indeterminate converts a question over K<z> into one over a constrained extension of K; use the published constrained-extension reduction as the oracle step.

Result: the explicit 2014 Theorem 9.6 requires both a nonconstant base and Khat/K nonalgebraic. For algebraic Khat/K, all available specializing elements have differential order zero, so the required high-order search has no witnesses. This is a genuine absent hypothesis, not a notational technicality.

Gap: replace the specialization mechanism for the algebraic-closure branch. The later linear test in Approach 5 gives an exact counterexample to unrestricted specialization preservation. Estimate: 20%.

## Approach 3: constant-base primitive-element repair, 16:38-16:40

Mechanism: use Pogudin's later primitive-element theorem and make its existence proof effective by enumerating a generator together with rational differential recovery expressions. Handle finite extensions generated only by constrained constants using ordinary algebraic primitive elements.

Result: the direct primitive-element obstruction can be removed. The elementary argument in PROOF.md shows that constrained constants over a constant base are algebraic. However, rereading the earlier dependency reveals that Theorem 6.1's algebraic-dependence computation also has a nontrivial-derivation hypothesis. Adding t with delta t=1 is useful for primitive generation, but coefficients involving t cannot silently appear in the target field.

Gap: write and audit the entire constant-base dependence/constraint transfer, not merely swap a single theorem citation. No complete constant-base oracle reduction is claimed here. Estimate: 30%, reduced from an initially optimistic impression after the dependency check.

## Approach 4: effective quantifier elimination and ideal tests, 16:40-16:41

Mechanism: search in a computable differential closure for two solutions of a pair distinguished by some differential polynomial. In parallel, try to certify that the saturated differential ideal determines just one type; invoke effective quantifier elimination for each fixed formula.

Result: unconstrainedness is semidecidable; for a fixed candidate h, existence of distinguishing solutions is decidable via the complete decidable DCF_0 theory over the computable base diagram. But the universal claim ranges over all h, and a terminating bounded search for the positive case was not obtained. Primality is insufficient: [delta Y] is prime, yet contains many proper differential specializations [Y-c]. The quotient E[Y] with Y constant is an integral domain but not differentially simple.

Gap: an effective bound or finite complete certificate for the arbitrary-pair isolation test in the omitted base classes. No implication from decidable first-order theory to decidable principal-type recognition is assumed. Estimate: 25%.

## Approach 5: counterexample coding and exact linear test, 16:41-16:44

Mechanism: test whether a family delta Y-a z could encode undecidable information into constrainedness over an easy base. Analyze rational antiderivatives by the highest jet, exclude algebraic antiderivatives with the trace, and determine all differential polynomial relations of a solution.

Result: PROOF.md proves (delta Y-a z,1) constrained exactly when a!=0. Equality in computable K is decidable, so this family cannot encode an undecidable set through a computable list a_e. Over a differentially closed base, every specialization z->c in K destroys constrainedness, despite constrainedness over K<z>. This isolates a concrete failure of the naive specialization route.

Gap: an arbitrary-pair algorithm or an actual noncomputable constraint-set construction under the differential-transcendence promise. Altering z's derivative relations to encode a set would break that promise. No such construction was found. Estimate: 25%.

## Final checkpoint

Status: **unsolved**. Five distinct substantive approaches recorded. Full-target proof/counterexample: absent. The elementary partial proposition is proved, but no novelty claim is made. Finite exact controls exercise rational-derivative identities and scope guards; they do not prove the target. Packet preparation is complete once its manifest verifies; independent audit is still required before any remote publication.
