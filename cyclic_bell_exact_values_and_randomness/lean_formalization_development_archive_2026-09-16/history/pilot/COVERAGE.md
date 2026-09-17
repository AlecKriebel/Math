# Coverage register

**Certification status: zero kernel-checked endpoints.** No item in the table
below is called complete merely because it has a theorem declaration in a
source file. The source candidates have never been elaborated by Lean here.

## Manuscript-to-source map

| Manuscript / requested endpoint | Source candidate or exact check | Actual status |
|---|---|---|
| Tensor-product/PVM framework | `CyclicBell.State`, `PVM`, `Strategy`, `tensor`, `observable`, `born` | Definitions written; arbitrary coordinate dimensions, not just qubits. No compiler run. |
| Pure and mixed Born-rule correspondence | `expectation_eq_trace`, `pureBorn_eq_born`, `pureBorn_projectors` | Unexecuted general proof candidates. |
| `eq:Id`, `cor:first-augmented` — A | `firstReducedValue`, `firstAugmentedValue`, `FirstUpperBound` | Exact functional/target proposition defined. **No universal first-bound proof supplied.** |
| `eq:first-strategy`, `app:d4` — B | `D4.phi_normalized`, `targetState`, `aliceTargetPVM`, `bobTargetPVM` | Target state and two designated PVM candidates only. All Bell settings checked in Python, not Lean. **Full B unfinished.** |
| `eq:final-swap` | `D4.kappa_values`, `weights_are_final_swap`, `q_recurrence` | Literal `(0,1,3,2)` permutation linked to algebraic weights and target phase recurrence; uncompiled. The exponential identification is still missing. |
| Observable/outcome convention | `D4.alice_encoding`, `D4.bob_encoding` | Uncompiled encodings to algebraic swapped shift and ordinary shift. Distinguishes conventions beyond parity alone. |
| `thm:biased`, `app:d4` — C | `scripts/exact_preflight.py`, first-value checks | Exact Python attainment of `2/sin(pi/8)+1`. **No Lean attainment or maximality theorem.** |
| `eq:target-table`, `eq:d4-table` — D | `D4.targetBorn_eq_table`, `mixed_targetBorn_eq_table` | Uncompiled derivations from the physical Born definitions; also 16 exact Python Born checks. Needs compiler checking and source exponential-phase bridge. |
| Normalization, marginals, maximum | `D4.target_nonnegative`, `alice_marginal`, `bob_marginal`, `target_normalized`, `target_le_three_thirtyseconds`, `target_01` | Uncompiled theorem candidates; exact Python checks passed. |
| Trivial-Eve success gap | `D4.guessing_gap`, `target_not_uniform` | Uncompiled target-only statements. **No Bell maximality or Eve optimization is assumed or established.** |
| Combined target-only result | `D4.target_measurement_package` | Strongest combined **candidate**, not a certified theorem. Does not include a Bell value. |
| First scalar-max counterexample — E | No Lean theorem supplied | Requires A+B+C+D. **Unfinished.** |
| `eq:lambda`, `eq:second-functional` | `sourceLambda`, `bobFourier`, `secondReducedValue`, `secondAugmentedValue` | Actual source definitions written, including integer negative exponent at l=0. No coefficient-specialization proof. |
| `eq:second-sos`, `thm:second` — F | `SecondUpperBound` proposition; Python free-unitary algebra and witness SOS checks | SOS algebra/attainment checked externally, not in Lean. Requires coefficient bridge, PVM-unitarity bridge, SOS proof, positivity/mixed-state bound, full witness, and attainment. **F unfinished.** |
| Negative controls | `D4.wrong_state_normalization`; three validation files; Python altered-witness controls | Lean controls unexecuted. Exact Python wrong normalization, altered witness, phase, and SOS-prefactor controls passed. |
| All-dimensional cycle/autocorrelation results | No Lean development | Deferred. |
| `thm:support-rigidity`, divisibility, reflection-rank chain | No Lean development | Deferred in full, including support cancellation, invariance, polar kernels, and saturation bridge. |
| Arbitrary-Hilbert-space commuting-operator conclusions | No Lean development | Deferred. No inference from finite-dimensional or symbolic calculations. |

## Completed work that is not a formal theorem

The statement contract was written before the proof candidates. The source
blob and baseline branch identity were recorded. All nine dependency commits
were pinned. Six Lean files form the standard import graph: the umbrella,
Model, Functionals, D4, Statements, and AxiomAudit. There are 34 theorem
candidates plus five proof-bearing constructors queried by the axiom audit.

The exact preflight passed **392 checks** over rational cyclotomic coefficients.
It reconstructs all nine distinct witness observables' PVMs, factors their
projectors as outer products, checks both attained scalar values and the target
Born probabilities, and tests a symbolic second-family SOS with no same-party
commutation. It does not establish kernel-checked evidence or the first
universal bound. Ten reporting/scanner tests also passed.

## Conditional results and source candidates

The generic basis-to-PVM constructor explicitly takes orthonormality and
completeness, which the target candidates then try to prove; it does not take
any target table or maximality assumption. These are legitimate intermediate
hypotheses, but their unexecuted source is not a completed conditional theorem.

The external symbolic SOS checker operates under unitary-generator and
cross-party-commutation relations. Its interpretation and arithmetic have not
been verified in Lean. It must not be promoted to F or to a physical upper-bound
certificate by renaming it a theorem.

## Unresolved formal gates

1. Obtain a usable pinned compiler and run the candidates; repair any actual
   elaboration/proof errors without weakening statements.
2. Prove the correspondence between the algebraic positive-square-root phases
   and the manuscript's exponential phases.
3. Complete all Bell-setting PVMs and their observable encodings in Lean.
4. Prove a genuine arbitrary-local-dimension bound and explicit attainment
   for one actual augmented functional before asserting maximality.
5. Run the clean build, negative controls, dependency audit and an independent
   statement/dependency review.
