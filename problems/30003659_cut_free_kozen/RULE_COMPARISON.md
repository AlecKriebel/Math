# Pinned finite systems and scope of turn1

2026-10-02. This formal comparison permits scoped proof work despite the unavailable full LICS2017 rule table. It supersedes only the initial gate's decision to postpone all author work; the source-version and literature limitations remain.

## Syntax

Formulas are positive modal μ-formulas in negation normal form, as in Afshari–Leigh2016 §2. Formal fixed-point variables occur positively; propositional atoms have positive/negative literals. Substitution is capture-avoiding. Sequents are finite sets of **closed** formulas and mean their disjunction. Write barΓ for the conjunction of the negations of its elements. Proofs are finite, well-founded trees with no undischarged assumptions; shared subtrees may be encoded as a finite DAG with edges to earlier nodes.

## Conservative core C

The following rules alone define C:

- Atomic initial sequent {p,¬p}
- Weakening Γ / Γ,A
- Disjunction Γ,A,B / Γ,A∨B
- Conjunction with premises Γ,A and Γ,B, conclusion Γ,A∧B
- Modal K: Γ,A / ◇Γ,□A (one modality suffices here)
- Least-fixed-point unfolding: Γ,F(μxF(x)) / Γ,μxF(x)
- Ordinary greatest-fixed-point induction: Γ,F(barΓ) / Γ,νxF(x)

C has **no cut**, no deep-disjunction rule, no strong induction, no cyclic discharge, no infinitary rule, no arbitrary-formula identity axiom and no greatest-fixed-point unfolding rule. This deliberately conservative choice avoids every disputed extra inference. Γ is retained literally by induction; no arbitrary invariant is silently inserted.

Let C+cut add the standard shared-context one-sided cut rule, with premises Γ,D and Γ,¬D and conclusion Γ.

## Formal containment

The fully available2016 preprint explicitly defines Fix in Figure1 and Koz− in Figures1–2 / §3.1. Every rule of C is literally one of those rules: atomic identity, weakening, disjunction, conjunction, modal K and μ-unfolding are in Fix; ordinary induction is in Figure2. Thus the identity mapping on sequents and each labeled proof node embeds C into that fully specified2016 Koz−. The latter additionally includes ν-unfolding, generalized fixed-point identity and deep disjunction. Adding cut gives the analogous containment C+cut into2016 Koz.

The OWR source itself prints the same ordinary induction and identifies the surrounding system as the natural sequent version of modal K with fixed-point rules. C uses only this explicitly common conservative collection. Nevertheless, the exact conference2017 full rule list is not claimed recovered, and completeness of C is not asserted equivalent to completeness of either fuller presentation.

Transfer directions are asymmetric:

1. A completeness proof for C would prove completeness of any sound target calculus containing these rules
2. A proof of incompleteness for a demonstrably stronger calculus would imply incompleteness of its weaker targets
3. Incompleteness of C alone would not settle the original or2016 expanded target
4. A proof using an additional strong-induction/cyclic/deep-disjunction rule must not be called a C proof
5. Cut-equivalence of two presentations is insufficient to transfer a no-cut claim

The turn1 certificate's four cut-free roots use only C. Its fifth root is explicitly in C+cut and has exactly one cut on □p. It is not presented as a cut-free proof of the final sequent.

## Literature dependency boundary

Kloibhofer2023's counterexample is to the distinct cyclic system Clo. His valid sequent supplies a test case, not an unprovability claim in C or Kozen. The invalidated2016/2017 chain through Clo and its claimed completeness of the strong-induction system are not used. Demystifying μ2025 proves completeness with cut; Bauer–Saurin2025 concerns non-wellfounded cut elimination. Neither is substituted for the exact finite no-cut question.
