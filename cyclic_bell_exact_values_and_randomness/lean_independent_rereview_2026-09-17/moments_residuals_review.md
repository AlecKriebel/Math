# Independent revised-source review: second-family moments and residuals

Checkpoint: 2026-09-17T14:59:47Z. Completion estimate: 100% of this bounded source/statement review. This reviewer did not build Lean or edit the submitted snapshot. Fresh build and dependency-axiom verification are the coordinating reviewer's responsibility.

Reviewed snapshot: `snapshot/lean_formalization`. All paths and line numbers below are relative to that directory. The reference is the submitted `reference/manuscript/main.tex`, specifically Theorem `thm:second` and its proof at lines 991–1087. Package self-reports and recorded successful logs were not used as evidence.

## Verdict

**Both assigned previous gaps are closed at the level of actual source definitions and theorem statements, subject to successful fresh compilation. No new mathematical, semantic, or scope blocker was found.**

1. `GeneralSecondMoments.lean` proves the complete d-by-(d+1) complex first-harmonic matrix, including every Alice row, the extra Bob column, and every local first moment. It connects these formulas to actual Born probabilities and proves permutation independence of that probability-derived array.
2. `GeneralSecondResiduals.lean` proves literal vector annihilation of every second-family SOS residual in every d>=2 and for every phase permutation, plus the additional alignment residual. It uses explicit operator compression and unitarity, not an assumption of maximality or even the already-proved scalar attainment theorem.

The earlier alternate Bob-adjoint convention gap is outside this assigned subreview; the new `GeneralOutcomeRelabeling` module is being reviewed separately. This report does not infer a verdict on that module from its presence.

## First-harmonic coverage and scope

`CyclicBell/GeneralSecondMoments.lean:15–42` proves, for arbitrary `l y : Ix d` and `κ : Equiv.Perm (Ix d)`,

    <A_l B_y> = generalLambda l * chi (-(l*y)).

Both sides have type complex, not real. The proof expands the actual Alice/Bob encodings, uses `phi_weighted`, removes κ with a finite permutation sum identity, and evaluates the remaining Fourier sum. The complex phase is retained through `polarTransform_compression`; multiplication by the conjugate prefactor cancels its unit-modulus phase. This matches manuscript lines 1066–1078, including the minus sign in omega^(-l y).

`GeneralSecondMoments.lean:45–60` proves the extra-input column for **every** Alice row:

    <A_l B_none> = if l=0 then 1 else 0.

Here `none` is the added Bob setting d. It does not merely reprove the alignment entry l=0. Character orthogonality treats nonzero l uniformly, including composite d; no coprimality or prime-dimensional premise appears.

`GeneralSecondMoments.lean:63–77` proves all Alice and all Bob local complex first moments vanish. The Bob quantifier is `AugmentedInputs d`, including `none` and every reduced input. The proof uses the actual weighted-cycle trace-zero property and correctly assumes d>=2. The physical density trace version is stated and proved at lines 128–139.

The complete matrix formula appears at lines 80–90, and equality of entire expectation arrays for arbitrary κ and τ appears at lines 94–103. More importantly, lines 106–125 prove the same formula and permutation independence for

    probabilityCorrelator (behavior (secondPermutationStrategy hd κ)).

This is not a synthetic array filled with the desired coefficients. `GeneralBehavior.lean:17–18` defines `probabilityCorrelator` as the actual sum

    sum_a sum_b chi(a+b) * p(x,y,a,b).

`GeneralBehavior.lean:82–87` proves its equality to the density-matrix expectation for an arbitrary physical strategy, using `GeneralModel.lean:272–278` and the Born rule. The new proof applies that bridge at `GeneralSecondMoments.lean:112–116`, then explicitly rewrites the density as the projector of the maximally entangled vector.

The combined endpoint `secondPermutation_complete_first_moments` at lines 143–155 supplies both kinds of pair correlators and both parties' local moments. It therefore closes the previous literal coverage omission in manuscript lines 1012–1013 and 1080–1087.

**No higher-harmonic overclaim:** the row index l labels Alice's measurement setting. `probabilityCorrelator` has no Fourier-order arguments and uses only chi(a+b), corresponding to first powers on each side. The theorem does not assert equality of the entire behavior or of arbitrary moments A_l^k B_y^m. The module's opening scope statement at lines 4–7 correctly makes this distinction. The first-harmonic invariance can coexist with the manuscript's nonuniform target table.

## Literal residual coverage and absence of circularity

`CyclicBell/GeneralSecondResiduals.lean:14–22` proves the full vector identity

    (A tensor conjugate(A)) Phi_d = Phi_d

from ordinary matrix unitarity. It uses the vectorization identity to reduce the left side to A A†, so the required operation is entrywise conjugation, not adjoint. This is the correct maximally entangled invariance.

At lines 26–50, `secondPermutation_residual_zero` states the actual residual with actual encoded physical measurements:

    [d lambda_l I - A_l tensor Bhat_l] Phi_d = 0.

Its quantifiers cover every d>=2, every permutation κ, and every l in `ZMod d`. The residual uses the **unconjugated** lambda_l, matching `P_l` in the manuscript and `GeneralSecondSOS.lean:63–64`; conjugate(lambda_l) belongs in the Bell score, not in this residual. `secondFourier` is the actual positive-character sum over all reduced Bob inputs. There is no precomputed residual field in the strategy and no residual-zero hypothesis.

The proof obtains unitarity from `encoded_unitary` for the constructed PVM, expands `secondAlice_encoding`, cancels double entrywise conjugation, and applies `secondPermutation_compression` (line 43). It then distributes the matrix action and subtracts identical vectors. Neither `secondPermutation_attains`, `secondPermutation_maximal`, nor an equality assumption is invoked. Although the imported witness module contains attainment theorems, this proof's dependency mechanism does not use them.

The residual is written explicitly rather than using the helper `secondResidual` with lifted operators. It is mathematically the identical tensor-product residual: the helper defines d lambda I minus A_l times the Bob Fourier operator, and Alice/Bob lifts multiply to the displayed Kronecker product. There is no omission caused by this spelling difference.

At lines 54–75, `secondPermutation_aligned_residual_zero` similarly proves

    [I - A_0 tensor B_none] Phi_d = 0.

The proof derives A_0=B_none=X from the actual strategy, proves X has real entries, and uses the same unitary invariance. This matches the aligned augmentation in the manuscript. Together these additions close the previous residual-annihilation packaging omission without using circular maximality assumptions.

## Actual dependency checks

I re-read the relevant physical and coefficient definitions in this snapshot, rather than relying on theorem names or comments:

- `GeneralModel.lean:14–24,40–48`: density positivity/trace normalization and complete orthogonal projective measurement effects; strategy has no Bell-value or moment assumptions.
- `GeneralWitness.lean:25–26,35–40,42–53`: normalized maximally entangled vector, X diag(weight) orientation, actual entrywise conjugation, and projector density.
- `GeneralSecondWitness.lean:59–74`: Alice PVMs and the physical second-family strategy, with the encoded Alice observable equal to the entrywise conjugate of the weighted D_l.
- `GeneralSecondWitness.lean:82–111`: exact scalar transform shift and operator compression, including its complex coefficient.
- `GeneralSecondCoefficients.lean:14–19,24–40`: the literal source lambda and r_l definitions, including a proved integer-exponent bridge at l=0.
- `GeneralModel.lean:133–141`: encoded unitarity is derived from the PVM laws.
- `GeneralCycles.lean:55`: maximally entangled weighted-cycle expectation is a sum of the product of the two weights; no hidden conjugation changes the sign calculation.

A byte-for-byte read comparison against the earlier delivered snapshot found the following dependencies unchanged: `GeneralSecondWitness`, `GeneralSecondCoefficients`, `GeneralFirstWitness`, `GeneralWitness`, `GeneralCycles`, `GeneralFourier`, `GeneralBehavior`, `GeneralModel`, `GeneralSecondSOS`, `GeneralSecondBound`, `Model`, and `MatrixAlgebra`. Thus these repairs did not obtain stronger endpoints by silently weakening those physical definitions or changing the paper's coefficients.

## Contracts, import exposure, and verification boundary

`GeneralSecondCompletionStatements.lean:13–30` restates the new correlator results as explicit sums over Born probabilities, including equality of the complete first-harmonic arrays. Lines 32–37 expose the physical local trace moments; lines 39–51 expose both literal residuals. These contracts preserve the intended quantifiers and do not add hidden hypotheses. `CyclicBell.lean:1` imports this contract module, which imports both new proof modules at its lines 1–2. The new results are therefore exposed through the library target, not isolated unimported files.

`AxiomAudit.lean:84–85,1520–1531` imports the new modules and contains queries for their public results. This inspection establishes the presence of queries, **not** their successful execution or output. `validation/AcceptGeneral.lean:20–23` contains a d=2 extra-input positive control; that is supplementary and does not replace the universally quantified theorem statements.

No `sorry`, `admit`, top-level `axiom`, `native_decide`, or `unsafe` appeared in the two assigned new proof modules or their completion-statement module in a source search. Full dependency trust and actual elaboration remain subject to the independent root build/axiom review. No build-success claim is made here.

Recommended disposition: **accept these two repairs after the fresh build succeeds; mark the previous second-family complete-first-moment gap and explicit all-dimensional residual gap closed.** There is no further source-level repair requested in this assigned scope.
