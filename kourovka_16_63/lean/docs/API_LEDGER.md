# Source/API consultation ledger

Toolchain target: Lean 4.19.0, Mathlib
`c44e0c8ee63ca166450922a373c7409c5d26b00b`.

Actual upstream source was consulted for selected interfaces during source
writing. This is an API-reading record, not evidence of compilation. Raw source
consultation is not a complete audit of every signature used in the draft.

| Primary source at the pin | Interfaces or issues inspected |
| --- | --- |
| `Mathlib/Algebra/Lie/Basic.lean` | `LieRing`, `LieAlgebra`, bilinearity/Jacobi conventions, `LieEquiv`, `LieHom.map_lie'`, `toLinearEquiv`, `lie_skew`, integer Lie-algebra structure |
| `Mathlib/Algebra/Lie/Nilpotent.lean` and its imports | `LieModule.lowerCentralSeries`, zero-index convention, successor/span route |
| `Mathlib/Data/ZMod/Defs.lean`, `Basic.lean` | finite cardinality, coordinate representatives, composite-modulus structure and casts |
| Pinned padic ring-hom sources | `PadicInt.toZModPow` and its kernel, rather than an assumed residue-field argument |
| Pinned quotient-group sources | additive quotient/kernel equivalence via the library's additive counterpart |
| Pinned finite-dimensional and matrix linear-map sources | rank-nullity and function-space dimension; avoided a guessed sum formula for `Module.finrank_pi` |
| Lean 4.19 `Init/Data/Nat/Div/Basic.lean` | `Nat.mul_div_right` with its positive denominator hypothesis; divisibility inequalities |
| Pinned finite-product source | `Finset.prod_pow_eq_pow_sum` |
| `leanprover/lean4checker` at `e11f65c651edd58d68ba260015d2bfde5102cd7f` | compatible toolchain and documented `--fresh` same-kernel replay |

The exact-version primary-source base is
`https://github.com/leanprover-community/mathlib4/tree/c44e0c8ee63ca166450922a373c7409c5d26b00b`.
The Lean source base is
`https://github.com/leanprover/lean4/tree/v4.19.0`.

Some candidate logarithm/power-series source paths could not be retrieved.
That is not a proof that a needed theorem is absent from Mathlib. No nonexistent
BCH or Lazard API was imported as a substitute. The current BCH and tensor
modules contain local algebraic helpers, not a presumed upstream correspondence.

All imports, coercions, implicit arguments, tactic invocations, instance paths,
and generated finite checks still require real elaboration. Offline repairs
may involve mathematical changes as well as API names; preserve that distinction.
