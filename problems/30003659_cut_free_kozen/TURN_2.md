# Turn2: a two-induction lower bound for the pinned test sequent

30003659 / OWR-15958-006. 2026-10-02. **Original completeness question unresolved;2/5 substantive author turns.** This turn studies the exact2016 expanded Koz− as well as the conservative core C. The inaccessible2017 full-rule-table limitation and the corrected Clo literature chain remain in force. No claim about unverified alternative presentations is made.

Use the formulas A,B,R,V,U,W and Φ={U,W} of TURN_1.md. The following is an author partial-result candidate, awaiting the eventual independent packet audit.

## 1. Scoped theorem

**Any finite cut-free proof of Φ in the explicit Afshari–Leigh2016 Koz− calculus must contain at least two occurrences of ordinary greatest-fixed-point induction.** Consequently the same lower bound holds in its conservative subsystem C.

This remains only a proof-complexity lower bound. It neither proves that such a cut-free proof exists nor proves it impossible. It does not justify transplanting the known Clo-unprovability result to Kozen. Deep disjunction and generalized fixed-point identity are included in the stronger system covered by this theorem; strong induction and cut are not.

## 2. The two possible induction principals before the first induction

The only closed fixed-point subformulas in U and W are U and W themselves. Their nonclosed nested binder V(x) has free x until the outer U is unfolded; then it becomes exactly W. Unfolding either closed fixed point introduces no other closed fixed-point formula. All fixed points appearing before an ordinary-induction step are greatest fixed points.

Neither U nor W contains a **closed disjunction subformula**. Their disjunctions have a free formal variable when viewed as subformulas: in U they involve x or y, and the additional outer disjunction in W involves y. The complete2016 Figure2 deep-disjunction rule has the shape

    Γ,D(E),D(F) / Γ,D(E∨F).

If D uses its argument and D(E∨F) is closed, capture-avoiding substitution forces E and F to be closed. Hence applying this rule backward inside a closed fixed-point occurrence U or W would require a closed disjunction subformula inside that occurrence, which does not exist. A vacuous context D does not change the sequent and may be deleted. A deep-disjunction step elsewhere only removes some occurrences of a closed disjunction and replaces them by one of its existing disjuncts; it cannot introduce a new closed fixed-point formula or alter U/W inside such a step.

It follows by induction on any backward path from Φ, using only the rules other than ordinary induction, that every closed fixed-point formula eligible as an induction principal is U or W. Weakening removes formulas; propositional/modal decomposition and unfolding preserve the stated property; deep disjunction preserves it by the preceding paragraph. Initial sequents end a branch and introduce no intermediate rule premise.

In particular, if a proof of Φ had exactly one ordinary-induction occurrence, its principal would be U or W. Nothing is assumed about the more complicated formulas above that induction: the semantic argument below applies to them without a subformula restriction.

## 3. A dual-consistent swapped fixed-point interpretation

For this proof-obstruction argument, interpret every ν as the **least** fixed point and every μ as the **greatest** fixed point of its positive operator. Atoms, Boolean operations and modalities retain their ordinary Kripke interpretation. This is an auxiliary interpretation of the proof rules, not the intended μ-calculus semantics.

All2016 Koz− rules except ordinary induction remain sound under this interpretation:

- Atomic and generalized fixed-point identities remain valid. Formula duality still exchanges a fixed point with the complement of the dual fixed point, because the two choices are swapped together
- Weakening, conjunction, disjunction and modal K are ordinary sound rules
- Both fixed-point unfolding rules remain sound because either chosen fixed point satisfies its fixed-point equation
- Deep disjunction remains sound because every positive formula context is monotone under this interpretation. Monotonicity holds structurally for both least and greatest fixed points, so D(E)∨D(F) implies D(E∨F)

These are semantic preservation statements for every instance of the respective rules, not just the finite examples checked in the supplementary script.

Now take the one-state frame with a self-loop (for each action, if needed). Modalities are identity on its Boolean algebra. Let p be either false or true. Under the swapped interpretation, U=W=false in both cases:

- If p=true, U's body is identically false because of its ¬p conjunct. Thus U=false; then W is the least fixed point of y↦y, also false
- If p=false, every V(X) is the least fixed point of the constant-false operator, so V(X)=false. Then U is the least fixed point of x↦x and W=false

Therefore Φ is false under either auxiliary model.

## 4. Excluding zero or one ordinary-induction occurrence

Zero inductions are impossible: every remaining rule is sound under the swapped interpretation, its initial sequents are true, and Φ is false.

Suppose there is exactly one induction.

If its principal is U, choose the self-loop model with p=true. U's body F_U(Z) is false for **every** Boolean argument Z, and U itself is false. For any side context Γ, the induction premise Γ,F_U(barΓ) and conclusion Γ,U have exactly the same truth value as Γ. This particular induction instance is therefore sound in the chosen auxiliary model, regardless of the complexity of Γ. Every other proof step is already sound there, contradicting the false endsequent.

If its principal is W, choose p=false. W's body F_W(Z) is again false for every Z because the state has a self-loop and the body is □(p∧...). The same argument shows that this sole induction is sound in the selected auxiliary model, again a contradiction.

By §2 these exhaust the possibilities for a sole ordinary induction. The claimed lower bound follows. This argument does not assert that the same auxiliary model makes an arbitrary combination of several different induction instances sound; doing so would be an invalid extension.

## 5. Exact last-rule obligations in the conservative core

C does not have ν-unfolding or deep disjunction. In a minimal finite C proof of Φ, the final effective rule must be ordinary induction on U or W. Atomic identity, propositional/modal and μ rules cannot have that endsequent. Proper weakening would require U or W alone to be provable, but each is invalid in ordinary semantics: U is false in the self-loop p=true model, and W in the self-loop p=false model. Inessential weakenings are removed by minimality.

Because sequents are sets, the principal formula may already occur in the side context. This possibility must not be omitted. There are **four**, not merely two, final ordinary-induction obligations:

1. Principal U, side context {W}: {W,F_U(¬W)}
2. Principal W, side context {U}: {U,F_W(¬U)}
3. Principal U retained in side context Φ: {U,W,F_U(¬U∧¬W)}
4. Principal W retained in side context Φ: {U,W,F_W(¬U∧¬W)}

Each would need a cut-free finite proof to complete this last step. The two self-retaining cases are legitimate set-sequent rule instances; they are not silently ruled out by a multiset intuition. Each of the U obligations is false under the swapped p=true interpretation, and each W obligation is false under swapped p=false, so none has an induction-free proof. This is consistent with, and more specific than, the two-induction lower bound.

The expanded2016 system additionally permits final ν-unfolding, so these four obligations are not claimed to exhaust its final rules. The global lower bound in §§2–4 does cover that expanded system.

## 6. Verification, corrections and remaining gap

`turn2/check_obstruction.py` checks the relevant closed-binder and closed-disjunction syntax, the self-loop valuations, all four core final-rule contexts, and duality on28 generated closed formulas. It passes85 exact assertions. These finite controls support the written structural and semantic metaproof; no bounded proof-search failure is promoted to unprovability.

During author development, the initial two-last-premise shorthand was corrected before freeze to include the two self-retaining context cases. No earlier frozen turn1 statement or certificate is changed. The final theorem and checker include all four contexts.

The turn1 one-cut proof remains a useful upper certificate in C+cut. The present result shows that replacing it by a proof with zero or one ordinary induction is impossible even in the explicitly stronger2016 cut-free system. Whether there is a proof with two or more inductions, and whether all valid formulas admit cut-free Kozen proofs, remains unresolved. The next attempt must engage that multi-induction interaction rather than repeat a semantic equivalence or cite completeness of the different cyclic/infinitary systems.
