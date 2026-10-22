# Turn3: why direct context permutation across induction fails

30003659 / OWR-15958-006. 2026-10-02. **Unresolved,3/5 substantive author turns.** This attempt addresses a natural way to remove turn1's fixed-point-free cut. It obtains a precise obstruction to that local transformation, not an obstruction to cut elimination by every possible method.

The finite ordinary-induction core C and the explicit2016 extension remain as pinned in RULE_COMPARISON.md. The2017 full rule-version gap, extra deep-disjunction distinction, and corrected Clo literature chain remain attached. No result for a different cyclic, strong-induction or infinitary system is substituted.

## 1. The attempted permutation and its exact limit

Ordinary induction has premise Γ,F(barΓ) and conclusion Γ,νxF(x). Enlarging Γ by a new side formula H changes the invariant from barΓ to barΓ∧¬H. Thus one cannot merely add H to an existing induction premise and call it an instance of the same induction rule.

This can fail even when there is a trivial cut-free proof of the weakened conclusion. More precisely, there is no general transformation that, after adding H, retains the same principal ν-formula and ends with ordinary induction with the **natural enlarged side context Γ,H**, excluding a duplicate retained principal formula from that side context.

The qualification is essential. Set-sequent rules also permit retaining the principal in the side context, as recorded in turn2. The example below rejects one specific direct permutation; it does not assert that every proof ending with some induction instance is impossible.

## 2. An exact finite proof example

Choose distinct atoms p,q, and use the source's Boolean abbreviations

    T=q∨¬q,       D=¬T=¬q∧q,       Z=νx□x.

There is a cut-free C proof of Z:

1. Atomic identity gives {q,¬q}
2. Disjunction gives {T}
3. Modal K gives {□T}
4. Ordinary induction with empty side context, whose complement is T, gives {Z}

Weakening now gives {p,Z}. This is a five-node cut-free derivation. The use of T as the empty conjunction is the explicit convention of the source; it is not a new truth axiom.

The same endsequent also has a proof with one fixed-point-free cut:

- Weaken {□T} by D, then apply ordinary induction with side context {D}. Since ¬D=T, this gives {D,Z}
- The earlier proof of {T} weakens to {p,T}
- Add p to the first premise and Z to the second, then use the shared-context cut on D to obtain {p,Z}

All these inferences are explicitly checked. The final endsequent is therefore not a counterexample to cut-free completeness; its direct cut-free proof is already supplied.

## 3. The proposed last induction has an invalid premise

If the weakened conclusion {p,Z} is forced to end with ordinary induction on Z using side context exactly {p}, its required premise is

    {p,□¬p}.                                             (1)

This is invalid over ordinary Kripke frames. Let the states be0,1, with edges0→1 and1→1, and let p hold only at1. At0, p is false and □¬p is false because its successor satisfies p. Both states have a successor, so the example does not exploit a dead end.

Soundness alone precludes a closed proof of(1), even in sound extensions of C. Hence the displayed direct permutation cannot work. In contrast, {p,Z} is valid and has the five-node cut-free proof in §2. The error would be to interpret failure of a prescribed final-rule shape as nonexistence of every cut-free proof.

## 4. Exact semantic characterization of this local obstruction

For a fixed formula H and a Kripke model, H∨□¬H holds everywhere precisely when the truth set of ¬H is forward-closed under the transition relation. The necessity and sufficiency follow directly from the □ semantics.

For H a freely valued propositional atom p, the schema p∨□¬p holds under **every** valuation on a frame if and only if its accessibility relation is a subset of the identity relation:

- If every edge is a self-loop, a state not satisfying p has only successors equal to itself, so □¬p holds (also vacuously if it has none)
- If u→v with u≠v, choose p false at u and true at v. Then the schema fails at u

Thus the direct context permutation accidentally asks for a restrictive frame property absent from modal K. The two-world counterexample is minimal in number of states; every one-state frame satisfies the schema under all valuations.

This characterization concerns only the local premise shape. It is not a modal-frame characterization of cut-free Kozen completeness.

## 5. Relevance to the multi-induction test

In a usual attempted cut permutation past ordinary induction, the surviving side context changes. The associated invariant changes with it. Monotonicity alone is insufficient: the new invariant is generally smaller, and a subset of a post-fixed point need not itself be post-fixed. One must either construct a new invariant proof, change the arrangement of final rules, exploit a correctly justified retained-principal case, or use another admissible transformation.

The turn1 proof of Kloibhofer's sequent cannot therefore be turned into a cut-free proof merely by moving its cut above the induction nodes and relabeling their side contexts. This turn rules out that proposed generic transformation strategy. It does not show that the specific turn1 cut cannot be removed by a more substantial proof transformation.

In particular, retaining Z inside the side context of a final induction produces a different premise {p,Z,□(¬p∧¬Z)}, not(1). That may be proved using an already available proof of Z and weakening. It neither rescues the rejected irredundant-context permutation nor proves an unproved target by circular reuse of its own desired conclusion.

## 6. Exact checks and remaining work

`turn3/verify_context_obstruction.py` validates11 stored proof nodes, including the cut-free and one-cut proofs of the same endsequent. It checks the concrete serial countermodel and all18 one- and two-state frames under all their propositional valuations, matching the universal frame characterization above. There are118 exact assertions. These finite checks supplement the written proof and do not replace it.

The original problem remains unresolved. The turn2 lower bound and the turn3 obstruction leave multi-induction proof transformations, retained-principal contexts and genuinely new invariants as the live avenues. No bounded search or failed local derivation is treated as an incompleteness theorem.
