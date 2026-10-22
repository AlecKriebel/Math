# Turn5: μ-bearing premise attempts and the exact unresolved boundary

30003659 / OWR-15958-006. 2026-10-02. **Unresolved after5/5 substantive author turns.** No sixth author search is undertaken. The final attempt permits the μ-bearing invariants required by turn4 and examines all four possible final-induction contexts in the conservative core. The fully available2016 system, common core,2017 version gap and corrected literature chain remain as stated in RULE_COMPARISON.md.

## 1. All four final-induction premises are semantically valid

There is no semantic countermodel to the four exact premises listed in turn2. This can be proved on arbitrary Kripke frames, rather than inferred from a finite model scan.

Write A=◇¬p, B=□p, so B=¬A. Recall

    V(X)=νy.□(p∧(□X∨◇y)),
    F_U(X)=◇(¬p∧(□X∨◇V(X))),
    U=νx.F_U(x),    W=V(U),
    F_W(Y)=□(p∧(□U∨◇Y)).

First, □A∨◇B is valid because B=¬A. Therefore B is an exact fixed point of the operator defining V(A):

    □(p∧(□A∨◇B)) = □p = B.

Every fixed point of that operator is contained in B, since its output is always contained in □p. The greatest fixed point is consequently **V(A)=B**.

It follows that F_U(A)=◇¬p=A. Every fixed point of F_U is contained in A because its output is always contained in ◇¬p. Hence its greatest fixed point is **U=A**, and then **W=V(U)=V(A)=B**. In particular F_W(B)=B. These standard-semantic identities agree with turn1's separately supplied cut-free implication certificates.

For principal U with side context {W}, the invariant ¬W is therefore A and the premise W∨F_U(¬W) is B∨A. For principal W with side context {U}, the premise U∨F_W(¬U) is A∨B. The two retained-principal premises already contain the valid disjunction U∨W. All four premises are thus valid over every Kripke frame.

This removes one possible route to an obstruction: none of those exact premises can be dismissed as invalid. It does **not** give a cut-free derivation of them. Replacing their μ-bearing syntactic invariants by semantically equivalent A or B inside a proof requires a justified syntactic transformation, not merely equality of denotations.

## 2. A targeted finite backward attempt

The program `turn5/targeted_search.py` attempts those four premises directly in the conservative core. It allows μ-bearing intermediate formulas, ordinary induction with either minimal or retained-principal context, and μ unfolding. It uses no cut, strong induction, deep disjunction, ν unfolding or cyclic closing rule.

This is explicitly **not an exhaustive search** of core proofs, much less of2016 Koz−. It uses:

- The first eager top-level Boolean decomposition, rather than all possible proof arrangements
- One boxed principal for modal K, all available diamond formulas, and explicit weakening of other side formulas after a successful step
- No general branching over weakening choices
- At most two additional ordinary inductions per branch below the forced final induction, three μ unfoldings per branch, depth22, and600 formula-symbol occurrences per explored sequent
- A cap of300 expanded states per target premise

These restrictions are search choices, not assumed normalization theorems for the calculus. In particular the earlier context-permutation obstruction warns against assuming such a normalization without proof.

The method first finds and syntactically verifies the known positive control {B,U}. The recovered proof has16 nodes and uses ordinary induction twice. It therefore tests the actual induction/context/substitution implementation rather than merely accepting atomic tautologies.

The four target attempts explored78,89,56 and115 states respectively, for338 target states. Of these321 contain μ-bearing formulas. Seventeen μ-unfolding attempts were made. None of the four target proofs was found. Including the15-state positive-control run,353 states were explored. The retained-principal runs encountered18 size prunes in total, and the two W-principal runs encountered four depth prunes. Remaining failures also depend on the induction/unfolding budgets and the non-exhaustive focusing choices; absence of a state-cap hit does not make a run complete.

`found_certificates.json` contains the actual recovered positive-control proof, with every inference checked. It contains no purported proof of Φ. The search report records representative unfinished sequents and the precise limits. Failure has no unprovability meaning.

## 3. What the attempt establishes and what it does not

This fifth turn does not close the exact test-case gap. It establishes the universal semantic validity of all four final-induction premises and carries out a reproducible μ-bearing syntactic attempt with a checked positive control. It does not infer:

- That Φ lacks a finite cut-free proof
- That ordinary induction is incomplete
- That deep disjunction or ν unfolding could not help
- That a larger or differently organized search would fail
- That the unavailable2017 presentation has been pinned by these experiments

The semantic identities are particularly easy to misuse. Both components are equivalent to complementary modal formulas, but the problem is to compose or transport their separate proofs without cut and without an unproved contextual replacement principle. Turn1 displays a single fixed-point-free cut accomplishing that composition. Turns2–4 restrict the shape and intermediate content of a cut-free alternative. None eliminates every unrestricted alternative.

## 4. Exact controls and final disposition

`turn5/check_semantic_premises.py` checks the identities and all four premises in68 one- and two-state models, with680 exact assertions. The preceding Knaster–Tarski argument, not those finite checks, proves their validity on arbitrary frames.

The original completeness question remains **unresolved5/5 in this attempt**. The final packet retains:

1. Four cut-free component-equivalence certificates and an explicit one-cut proof of the test sequent
2. A two-ordinary-induction lower bound in the pinned2016 cut-free system
3. An exact obstruction to one naive irredundant-context permutation, together with a cut-free proof of the example's actual weakened conclusion
4. A proof that every cut-free2016 proof of the test sequent must introduce a μ-bearing intermediate formula
5. Universal validity of the four core final-induction premises and a precisely limited μ-bearing backward attempt, with no full proof found

The complete packet now needs separate independent source/proof review. Its proposed disposition is unsolved5/5 with the exact system caveat and credited partial results, not a claim of general incompleteness or a resolution imported from another calculus. No historical novelty is certified.
