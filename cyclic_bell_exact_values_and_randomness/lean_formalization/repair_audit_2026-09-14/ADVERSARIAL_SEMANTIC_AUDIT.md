# Adversarial guessing and privacy: semantic audit

Audit timestamp: 2026-09-15T03:54:02.604182+00:00

Assigned audit scope: 100% inspected. This is a semantic review of the requested adversarial modules and their contracts, not a claim that the complete package has passed its final build. Parent agent is independently repairing and compiling the final aggregate.

## Result

No semantic blocker found in the adversarial value, entropy, fixed-POVM maximum, or nested finite-q supremum routes. Their definitions match the manuscript's intended optimization domains and their conclusions preserve the distinction between an exhibited attack, the optimal attack on a fixed realization, and the supremum over all maximizing realizations. The binary privacy result retains its finite-purification scope and derives the necessary on-state relations from scalar saturation.

The audit read the actual definitions and proof dependencies in GeneralExtendedBehavior, GeneralTripartite, GeneralCommutingGuessing, GeneralAdversarialValues, GeneralAdversarialEntropy, GeneralPOVMMaximum, GeneralNestedGuessing, GeneralBinary, GeneralBinaryCertification, GeneralAdversarialRegression, AdversarialStatements and the relevant validation files. Manuscript comparison: main.tex lines 267–290 (conditional states and models), 1100–1125 (G_val and its lower bound), 1170–1185 (d=4 entropy direction), and Appendix Binary, lines 1780–1897.

## Domain and closure checks

- GuessQ ranges over unrestricted finite Alice, Bob and Eve index types, actual normalized positive joint density matrices, observed PVMs, and an arbitrary complete positive Eve POVM. Validity contains no Bell saturation, privacy or guessing-value premise.
- GuessPOVM has only effects, positivity and completeness. Neither projectivity nor rank one is required. HilbertGuessPOVM has self-adjointness, nonnegative quadratic forms and completeness, with no same-party effect-commutation requirement.
- GuessQc uses an arbitrary complete complex Hilbert space, normalized vector state and observed commuting PVMs. Every Eve effect commutes with every Alice and Bob effect; the observed cross-party commutation is carried by CommutingOn. Thus it is an actual three-party commuting model, not a renamed tensor construction.
- GuessQa is literally `closure (GuessQ d α β)` in the full real extended-correlation array type. `valueSlice` subsequently imposes the Bell equality on `forgetE r`. `GvalQa` therefore closes before slicing and does not take arbitrary extensions of an already-closed AB marginal.
- Forgetting Eve has actual marginal-realization proofs for finite and commuting strategies; continuity transfers the finite marginal inclusion to qa. The lower-bound route requires only finite→qa and finite→qc inclusions, which are proved. It does not assume a general qa→qc inclusion.

The manuscript introduces G for a purification and then S_q as finite tripartite strategies. GuessQ permits mixed tripartite states, as is conventional for that model. This does not weaken any displayed lower bound: the exhibited attack is an actual pure AB strategy with trivial Eve. If an exposition demands identifying the entire mixed-tripartite domain with a domain restricted to pure ABE states, that standard purification-and-enlarge-Eve equivalence should be explicitly cited or added; these modules do not currently expose that separate equivalence as a named theorem. The finite→qc embedding purifies the entire ABE state, which is the correct construction for its own claimed embedding.

## Optimization and entropy checks

- `guessingSuccess` sums the diagonal event g=(a,b), while `forgetE` sums all Eve labels. `valueGuessing` is the supremum of this actual success over the score equality slice.
- Normalization gives a bound by one. A concrete finite maximizing extension supplies nonemptiness before `csSup_le` is used. No potentially empty generic saturation set is silently assumed nonempty.
- `three_model_Gval_interval` receives independently proved quantum values, embeds the same complete finite extension into all three domains, and establishes only an interval from its exhibited success to one.
- Both family results use the exact displayed all-d floor with denominator d²(d−1), d≥4, and the correct target inputs 1 and `none` (the added setting d). The strict inequality is proved, not asserted in strategy validity.
- `paperGuessFloor_four=1/12` and `general_floor_not_four_peak` explicitly distinguish the general estimate from the stronger d=4 peak 3/32.
- `first_four_Gval_three32` and its second-family counterpart are lower bounds. No theorem in these routes sets G_val equal to 3/32 or claims the final-two swap is a worst attack.
- `guessingMinEntropy g=−log(g)/log(2)` is used antitonically only after positivity follows from the positive 3/32 lower bound. Therefore H_val≤5−log₂3<4 is the correct direction; this is not an exact global optimized entropy claim.

## Fixed-realization maximum and nested supremum

Every finite POVM has an exact positive square-root Gram factorization. The Gram normalization gives a finite-coordinate norm bound; the valid factors form a closed subset of a compact product of closed complex balls. The real objective is continuous. Thus the fixed finite-Eve objective has an attained maximum over all positive complete POVMs. The proof does not optimize over a restricted projector class or import a numerical solver's verdict.

`tripartiteConditionals` uses the actual measurement sandwich and partial trace. `guessingSuccess_objective` connects the discrimination objective to the actual extended Born probabilities. `withEve_marginal` preserves the entire observed behavior, not only its Bell score.

`optimizedFiniteScores` enumerates the attained fixed-realization optimum for every finite strategy whose observed Bell score equals betaQ. Replacing Eve's POVM realizes each such optimum in GuessQ with the same observed behavior. Conversely each existing strategy's success is bounded by its fixed-realization optimum. This proves the two supremums coincide. The generic theorem requires a saturating realization; both family instantiations supply their explicit maximizing strategy. The result is expressly finite-q. It neither asserts a maximum over realizations nor incorrectly promotes finite-dimensional compactness to arbitrary-Hilbert Eve.

## Binary privacy boundary

`binary_saturation_privacy` starts with actual normalized purification amplitudes, Hermitian involutions, cross-party commutation, and scalar saturation at 3 sqrt(3). It derives both residual annihilations, on-state anticommutators, vanishing operator-valued Eve moments and then the conditional-state identity rho_E/4. It does not assume global anticommutation or privacy. `binary_purified_saturation` bridges actual arbitrary finite tensor PVM strategies to this theorem. `BinaryPrivacyAt` quantifies all compatible finite purifications; explicit attainment provides nonvacuity. The q/qa/qc value identity is separate from this finite-dimensional privacy conclusion, matching the manuscript.

## Validation-contract limits

The strongest closure-order guard is the actual `rfl` contract in AdversarialStatements expanding GvalQa to a supremum over `r∈closure GuessQ ∧ score=betaQa`. The real-line `closure_before_slice_control` and its rejected companion are supplementary topological examples; by themselves they would not guard against changing the actual quantum definition.

The positive POVM control constructs a complete nonprojective sixteen-outcome POVM on C¹, then proves every effect fails idempotence. The negative control attempts the false idempotence equation. This directly detects a projective-only Eve restriction when combined with the positive construction and structural review.

AcceptAdversarial instantiates the fixed-POVM attained-maximum theorem and nonprojectivity witness, a G_val lower bound, and an entropy upper/strict bound. AdversarialStatements additionally checks instrument identity, actual finite→qc embedding, full qa domain expansion, behavior preservation and nested finite-q equality. These checks do not replace a semantic audit of the definitions.

The repaired runner explicitly treats negative files as proof-mutation smoke tests, not as proofs of falsity. It rejects resource exhaustion, missing imports/names, failed typeclass synthesis and syntax errors, and requires source-located diagnostics within the single attempted proof. The positive proven negations and mathematical source review are the evidence that these particular targets are false. A mere proof-attempt failure would not establish falsity in general.

## Supplemental audit: canonical polar identity and generic permutation extension

Supplement inspected at 2026-09-15T03:55:18.097556+00:00. Read GeneralCoveragePolarCanonical, GeneralCoveragePolarAlgebra, GeneralCoveragePermutation, GeneralPermutation, and the simple-spectrum endpoint in GeneralCoverageWitness. Compared with manuscript lem:polar and thm:permutation.

**Canonical polar identity: faithful conditional theorem, with an explicit analytic boundary.** The assumptions `C=V*sqrt(C†C)` and `(V†V)*sqrt(C†C)=sqrt(C†C)` are the decomposition and initial-support isometry properties of a canonical polar factor. The manuscript itself identifies V†V with the support of |C|. Consequently the second assumption is a legitimate polar-decomposition property, not the desired positive-factor identity or a disguised commutation/cross identity. The formal statement is actually valid for more factors than the unique canonical partial isometry: arbitrary off-support behavior of V is permitted if the two supplied equations hold.

The conclusion uses actual CFC square roots twice, so its P is literally |C†|^(1/2)−V|C|^(1/2)B. Positive-root uniqueness identifies the transported roots. `initial_isometry_sqrt` derives the half-root support equation using the C*-zero-product norm identity, requiring no inverse, lower spectral bound, closed range, or absence of a kernel. Commutation of C† and B follows from C commuting with the unitary B, then CFC derives the required modulus commutation. The mixed products and the final P†P identity are derived, not premises. Assuming C commutes with B is weaker than the paper's two commuting *-algebras and is sufficient for this identity.

This closes the literal **identity conditional on polar-decomposition data**. It does not construct a canonical polar decomposition for every bounded operator or formalize the manuscript's von Neumann bicommutant/strong-limit proof that V lies in the generated algebra and commutes with B. Those are standard analytic infrastructure/proof-route details, and this alternative proof avoids needing them, but coverage documentation should not call those separate constructions formalized. In particular, the header phrase about deriving commutation should refer to the commutation actually used for the modulus; no theorem here asserts all of the original von Neumann algebra narrative.

**Generic permutation theorem: hypotheses match the stated conditional result.** `linearScalar` is exactly sum_r |alpha_r+beta_r z|. The new arbitrary-C*-algebra/Hilbert upper bound assumes a scalar cap on the unit circle, not an operator/Bell bound. Combined with `PermutationData.equality` at unit phases (and d>0), this says precisely that M is the attained scalar maximum used in the paper. The data fields are the paper's unit-modulus phases, product-one conditions, scalar equality and `s*|g|=g` phase alignment. They do not assume quantum maximality. At zeros of g the alignment equation remains 0=0, leaving the unitary extension phase arbitrary as required.

The generalized functional factors use continuous half-polar functions with the correct zero extension. The SOS upper bound is proved on arbitrary complete complex Hilbert spaces from unitarity and observed cross-party commutation, with no finite dimension or order-d premise. The augmented alignment term needs only unitarity for its norm bound; omitting an unnecessary commutation assumption there makes the theorem stronger without changing its applicability.

The existing actual finite weighted-cycle PVM construction gives the stated observables and attainment. The new local first-moment theorem proves zero for d≥2, hence permutation invariance. The new all-harmonics theorem includes both Alice settings and the added Bob alignment setting, completing the earlier narrower some-r formula. GeneralCoverageWitness provides one-dimensional eigenspaces at every d-th root for every displayed observable; weighted cycle characteristic-polynomial/order results provide the matching order-d/spectrum facts. No claim classifying all maximizers is introduced.

No new semantic blocker found in these two additions. The remaining distinction is one of accurately naming coverage: the conditional polar identity has been formalized; existence/canonicity and the original strong-closure construction have not been supplied by these files.
