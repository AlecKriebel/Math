# Internal notes on the scope of the PRA manuscript

| Question | Scope and evidence |
| --- | --- |
| Which equality is proved? | At two settings per party, every qubit POVM behavior is a finite shared-randomness mixture of complete qubit PVM behaviors. One selector reproduces all input pairs. The branch states can vary. |
| What happens without shared randomness? | A singlet measured with identical trine POVMs gives a joint table of rank three. A pair of single qubit PVMs, even with local stochastic processing of their labels, produces a table of rank at most two. Repeating the settings supplies a two-input example. |
| Which outputs are included? | Declared outputs can vary by input. The proof reduces a hypothetical strict separator to an extreme point of its exposed maximizing face. The binary–ternary reduction concerns that maximizer and permits arbitrary initial output counts and zero effects. |
| Why do positive multipliers follow? | Replacing a Bob input by a deterministic response gives a behavior in the projective hull. At a putative strict separator the finite score deficit is positive and the future Lorentz pairing is positive, forcing the corresponding multiplier to be positive. |
| What closes the rank-one case? | The five frame rays constrain the ranks of linear combinations of their outer products. On the real null quadric this identifies the base locus and forces projective injectivity elsewhere. The Lean proof establishes the fiber assertion through coordinate identities. |
| What is the three-setting witness? | With active outputs (2,2,3) on Alice and (2,2) on Bob, the strengthened POVM strategy scores (16 + 8√7813)/25. The SOS bound 289/10 holds for every two-qubit PVM strategy and its shared-randomness hull. |
| What is new? | The universal arbitrary-output two-setting equality supplies the lower bound on the number of settings for separation. Vértesi and Bene established the three-by-two advantage. Zhu et al. also give a rational three-by-two witness and a formal separation certificate. |
| What did verification cover? | The Lean endpoint covers the equality, common-selector simulation, minimum architecture and three-by-two witness and bounds. Independent exact computations check the supplied physics data. The manuscript describes the auxiliary mathematical statements proved in prose. |

The pre-submission review records the adversarial checks and their scope. [Review report](../../qubit_povm_pvm_pra_review_20261122/PRA_REVIEW.md) · [Verification results](../../qubit_povm_pvm_pra_review_20261122/evidence/lean_summary_20261122.json)
