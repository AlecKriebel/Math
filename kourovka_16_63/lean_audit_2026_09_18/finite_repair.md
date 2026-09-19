# Finite-coordinate repair audit

Scope: `Kourovka/Finite/*.lean` and the initial inspection of `Kourovka/Lattice/NearIdentity.lean`.

## Scope of mathematics

These modules formalize the finite additive coordinate carrier, its Lie bracket, p-adic reduction, nilpotency of bracket monomials, full Lie-ring automorphism **sets**, and a conditional small-endomorphism power estimate. They do not construct the BCH group or prove the automorphism cardinality. In particular, `full_lie_aut_card_eq_matrix_card` identifies an automorphism set with a matrix set but does not evaluate either cardinality. `finite_power_zero` requires an actual ambient integral endomorphism and compatibility with reduction as hypotheses; it does not supply that lift for arbitrary automorphisms.

## Repairs

- Repaired additive-to-residue-linear scalar transport via integer scalar multiplication, preserving the original statements.
- Fixed natural-to-integer cast normalization in `reduce_eq_zero_iff`.
- Marked p-adic reduction and its integer section `noncomputable`, as required by mathlib's p-adic definitions. This affects code generation, not the propositions or proof checking.
- Normalized the natural/integer numeral cast in the exact p-adic reduction kernel proof.
- Added missing `AdaptedBasis` imports to `Nilpotency` and `NearIdentity`, which use concrete embedding divisibility lemmas.
- Factored the Lie-equivalence construction through a private helper on an abstract linear map. The matrix map `fromEntries` is locally marked irreducible to prevent elaboration from expanding its 961-term sum. This leaves its definition and all coordinate identities intact. The helper uses the original bijectivity and bracket-preservation hypotheses, and the full automorphism-set equivalences retain their original statements and inverse proofs.

## Actual production acceptance

All checks below used Lean 4.19.0 and the project's pinned mathlib, actual production imports, and `lake env lean -j1 ... -o ...`.

| Module | Result | Log |
|---|---|---|
| `Finite/AdditiveLinear` | exit 0 | `finite_AdditiveLinear.log` |
| `Finite/BracketTrees` | exit 0 (unused-section-variable linter warnings only) | `finite_BracketTrees.log` |
| `Finite/Coordinates` | exit 0 | `finite_Coordinates.log` |
| `Finite/LieAutomorphisms` | exit 0 | `finite_LieAutomorphisms_final.log` |
| `Finite/PadicQuotient` | exit 0 | `finite_PadicQuotient_final.log` |

The earlier unsuccessful LieAutomorphisms run is preserved separately in `finite_LieAutomorphisms.log`; `finite_compile_results.json` records that initial run and must not be mistaken for the final status. `finite_final_results.json` records both subsequent successful modules.

The parent took ownership of final production checking and any further repair of `Finite/Nilpotency` and `Lattice/NearIdentity`; consult the parent final build log for those two results. Earlier isolated checks had validated their generic bracket-span and power-naturality arguments, but those isolated checks are not substitutes for production acceptance.

No theorem statement was weakened; no axiom, admission, `sorry`, `native_decide`, or unsafe implementation was added in this repair scope. No commits were made by this reviewer.

## Final parent-owned checks

`Nilpotency` and `NearIdentity` both compiled successfully with exit zero and empty final logs. `finite_parent_final_results.json` binds their source/object hashes.

Nilpotency needed an increased elaboration recursion limit and exponentiation threshold to handle the actual modulus 1009^1689. Its integer-power divisibility proof is transported explicitly through the residue-ring cast; the final zero-scalar rewrite avoids broad simplification that searched for a no-zero-divisors property unavailable for this composite residue ring. No such property is assumed. The original length-847 and lower-central-series statements are unchanged.

NearIdentity now specifies the exact exponent in the successor-power rewrite, preventing the rewrite from acting on the wrong inner power. The two-power loss in the ell coordinates and every lifting/compatibility hypothesis are unchanged.

All seven assigned production modules now pass. These remain finite Lie-ring/conditional near-identity results, not the BCH group or final automorphism count. Earlier failure logs are retained separately; final logs are `finite_Nilpotency_final.log` and `finite_NearIdentity_final.log`.
