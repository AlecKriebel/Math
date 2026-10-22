# Turn4: least-fixed-point detours are unavoidable in a cut-free proof of the test case

30003659 / OWR-15958-006. 2026-10-02. **Original completeness question unresolved;4/5 substantive author turns.** The theorem below concerns the explicit2016 Koz− rule set, including deep disjunction, not an unverified2017 variant. It is a restriction on the intermediate formulas of a possible proof, not a claim that no unrestricted cut-free proof exists. The source/literature caveats from RULE_COMPARISON.md remain.

Use U,W,Φ={U,W} from turn1. Call a proof **μ-free throughout** if no formula in any of its sequents contains a least-fixed-point binder μ. This is a syntactic condition; it is not a statement about semantic alternation depth or about the formulas merely in the endsequent.

## 1. Scoped theorem

**Φ has no finite cut-free2016 Koz− proof that is μ-free throughout.**

On the other hand, turn1 supplies a finite proof of Φ with one fixed-point-free cut on □p that is μ-free throughout. Thus, if this cut can be eliminated in the pinned system, the resulting proof must introduce at least one μ-bearing intermediate formula even though the endsequent contains only ν binders.

This does not prove cut nonadmissibility or incompleteness of the full system: ordinary induction is expressly allowed to create μ-bearing formulas through its negated side context. Such proofs remain a live possibility. The claim is also not automatically transferred to a presentation with additional unverified rules.

## 2. A19-formula predecessor invariant

Let

    X=□U,    Y=◇W,    H=X∨Y.

Define the finite set S to comprise

    p, ¬p, U, W, X, Y, H,

and, for each h∈{X,Y,H}, the four formulas

    p∧h,    ¬p∧h,    □(p∧h),    ◇(¬p∧h).

There are19 distinct formulas. The only fixed-point-free members of S are p and ¬p. The only closed fixed-point formulas occurring as subformulas of its members are U and W.

Every backward proof step from a sequent of formulas in S, using no ordinary induction and no cut, again has all its premise formulas in S:

- Weakening removes a formula
- Propositional rules select the displayed children, which are in S
- Modal K strips a box/diamond, again producing a listed formula
- Unfolding U produces ◇(¬p∧H); unfolding W produces □(p∧H)
- No μ-unfolding is applicable to S
- Generalized fixed-point identity can only terminate a branch, and contains a μ formula, so it is unavailable in an entirely μ-free proof

It remains to verify deep disjunction, rather than silently omitting it. As in turn2, capture-avoiding insertion into a closed formula forces the disjuncts inserted by a nonvacuous deep-disjunction instance to be closed. Each S formula has at most one closed disjunction occurrence, namely H, and there is no such occurrence inside U or W. Therefore any effective backward deep-disjunction step replaces H by X or Y in its displayed surrounding context. The resulting formulas are precisely the listed S variants. A vacuous context yields the same sequent and is inessential.

This verifies closure for every rule of the pinned2016 system prior to the first ordinary induction. It is not a bounded-depth approximation: S is an exact invariant for the stated backward fragment.

## 3. What a first ordinary induction would require in a μ-free proof

Assume for contradiction that a μ-free finite cut-free proof of Φ exists, and choose one with the smallest total number of ordinary-induction occurrences. If the number is zero, turn2's dual-consistent swapped fixed-point interpretation refutes it. Thus choose an ordinary-induction occurrence nearest the root along a branch, so no induction lies between its conclusion and Φ.

By §2, its principal formula is U or W and its side context Γ consists of S formulas. Each corresponding positive body genuinely uses its formal variable. If Γ contains any formula with a fixed point, that formula has a ν binder, so its dual in barΓ has a μ binder. Substituting barΓ into either body therefore creates an actual μ occurrence in the induction premise. No formula simplification modulo semantic equivalence is part of the syntax. This would violate the assumption that every sequent in the proof is μ-free.

Hence Γ can contain only p and ¬p. Retaining the principal U or W in Γ is specifically excluded by this same μ-creation argument, not by an incorrect assumption that principal repetition is forbidden in a set-sequent rule.

## 4. Eliminating the finitely many possible contexts

If Γ does not contain both p and ¬p, the conclusion Γ,U or Γ,W is invalid in standard semantics. This follows from turn1's separately cut-free proved equivalences

    U↔◇¬p,   W↔□p,

or directly from the following small countermodels:

- U alone: one state with a self-loop and p=true
- W alone: one state with a self-loop and p=false
- p,U: a dead-end state with p=false
- p,W: one state with a self-loop and p=false
- ¬p,U: one state with a self-loop and p=true
- ¬p,W: a state with p=true pointing to a self-loop state with p=false

Each indicated endsequent fails at the first state. Soundness of the ordinary2016 rules therefore excludes a closed proof above such an induction node.

The only remaining context is Γ={p,¬p}. Its conclusion with U or W is already provable from atomic identity by weakening. Replace the entire subproof ending at the selected induction node by that induction-free proof. This preserves the sequent, μ-freeness and all inferences below the node, while strictly reducing the number of ordinary inductions. It contradicts minimality.

Both cases are impossible. The theorem follows.

## 5. Why this does not settle the original problem

The conclusion is about a **syntactically restricted proof fragment**, not the full class of finite cut-free Kozen proofs. In an unrestricted proof, negating a ν-bearing side context during ordinary induction produces μ-bearing invariants. The four final contexts of turn2 make exactly this feature visible in the conservative core.

This turn explains why a proof search confined to the ν-only endsequent closure, or a direct conversion of its greatest-fixed-point cyclic proof without adding least-fixed-point intermediates, cannot succeed in the pinned2016 calculus. It does not show those intermediates can never suffice. No result for a weaker fragment is mislabeled as an incompleteness theorem for a stronger one.

The contrast with turn1 is exact: its final one-cut root uses26 ancestral DAG nodes and no μ-bearing formula. The separate reverse-implication roots in that file do contain μ; they are not part of the26-node proof of Φ. Removing the cut while insisting on retaining μ-freeness is impossible. Removing the cut with a different intermediate language remains unresolved.

## 6. Checks and next step

`turn4/check_mu_free_boundary.py` verifies all19 formulas, their logical/unfolding/deep-disjunction predecessors, the absence of closed disjunctions inside U/W, literal μ creation for ν-bearing side formulas, the six ordinary-semantic countermodels, and μ-freeness of the actual turn1 one-cut proof. It passes198 exact assertions. The universal conclusion rests on the closure and minimality proof above, not a search cutoff.

The fifth attempt should therefore allow the required μ-bearing invariant detours. If it fails, the final packet must retain this precise restricted obstruction and an explicit gap, rather than claim full Kozen incompleteness. No historical novelty certification is made for the partial result.
