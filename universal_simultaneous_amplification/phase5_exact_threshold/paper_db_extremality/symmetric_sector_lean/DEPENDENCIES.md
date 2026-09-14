# Dependency and axiom boundary

`principal_theorems.txt` lists the exact declarations selected for statement and transitive-axiom auditing. The dated final receipt beneath `reports/audit/` records every audited statement, its axioms, source hashes, configuration hashes, actual toolchain and mathlib checkout, and the clean-build output. `reviews/final_trust.md` independently assesses target coverage and the trust boundary.

## Principal dependency paths

1. **Finite scalar positivity:** actual rational coefficient matrix/source/reward → strict absolute row contraction → true matrix inverse and unique solution → explicit rational witness satisfying all equations → exact actual reward pairing → positivity, for all N=3…39.
2. **Finite phase margins:** integer floor-grid certificates → proved subsolution inequalities for the actual recurrence `t` → positive denominators and actual finite maximum `beta` → all N=40…287. Exact reduction of the actual N40 maximum yields the printed fraction; all later orders have margin at least 1/100, proving uniqueness of the minimum.
3. **All-order scalar positivity:** actual dual block equations → true Schur identity → nonnegative inverses → actual radial positive vector → bad forcing and contraction barriers → sharper left-occupation bound and printed debt estimate → beta debt budget. Finite phase margins and the analytic tail imply beta+epsilon<1; the proved alternating inverse inequality gives S_N>0. The finite direct solves join this proof at N=40.
4. **Physical identity:** actual two labeled transition moves → stationary law and normalization → positive-move connectivity and centered inverse → rank Poisson solution and actual ΔGq → concrete two-feature action → coefficient solution lifted to the actual second Green solution → exact incoming current and orbit averages → the actual ν₀ΔGΔGq equals FrobeniusSq times S_(n−1).
5. **Final symmetric component:** physical identity + all-order scalar positivity + positivity of the squared Frobenius norm. The n=3 zero-sector theorem supplies the boundary for nonnegativity and the zero characterization.

No arrow above is an assumed project-specific theorem. The final strict result has only population-size, symmetry, zero-diagonal, zero-row-sum, and nonzero-perturbation hypotheses. Column balance is proved from symmetry. The identity itself does not require the perturbation to be nonzero.

## Foundational axioms and computation

The permitted axiom set is exactly:

- `propext`: propositional extensionality.
- `Classical.choice`: classical choice.
- `Quot.sound`: soundness of quotient equality.

Some finite certificate declarations use fewer; the per-theorem report is authoritative. No principal theorem may depend on `sorryAx`, a project-specific axiom, or compiler-evaluation axioms. The audit fails if any other dependency occurs.

Generated rational and integer data are untrusted witnesses. Lean validates their equations and inequalities with ordinary kernel-checked proof terms. `decide +kernel` uses kernel reduction, not a compiled decision procedure. External Python, python-flint and SymPy never assert a Lean theorem and are not needed for verification of the committed proofs.

The ordinary implementation trust boundary includes Lean's kernel implementation and binary, the package retrieval/build infrastructure and imported pinned mathlib `.olean` artifacts, operating system and hardware. The clean audit deletes and rebuilds this project's artifacts, retaining pinned dependency caches; it does not claim to rebootstrap Lean or rebuild all of mathlib from source. The independent review checks that all package source checkouts match the committed manifest, are clean, and introduce no unrelated project imports.

Source scanning is supplemental. The decisive mathematical evidence is a successful build plus the transitive `#print axioms` output for every selected theorem. The audit also prints theorem types, and the independent model/arithmetic reviewers inspect their translation and domain restrictions; dependency cleanliness alone is not treated as semantic correctness.

## Dependencies not formalized here

Connecting this active-chain symmetric component to the full fixation local-optimality theorem still requires the coverage/collision representation, stationary perturbation expansion and analyticity, full tangent-space decomposition, and signs of the standard and skew sectors. Actual stationarity and actual centered-chain invertibility **are** proved here; they do not by themselves formalize the entire perturbation expansion or fixation interpretation.

There is no claim about the global fitness-two conjecture, a neighborhood uniform in n, interchange of fixed-graph/growing-family quantifiers, the standalone strong-selection theorem, or biological applicability. These absent results are not imported as axioms and are not conclusions of the principal theorem.
