# Reviewer guide

This is source for offline development, not a certified companion. Start with
`STATEMENT_CONTRACT.md`, `SESSION_REPORT.md`, and `progress.json`.

The most important new proof bodies to read are in `Flag/Rigidity.lean`.
`full_flag_rigidity` quantifies over an arbitrary bracket-preserving linear
bijection preserving the actual two-step flag. It does not assume connectedness,
innerness, or membership in a proposed automorphism family. The infinitesimal
proof applies to arbitrary derivations. Both close by the explicit generation
chain. The mathematical explanation is in `docs/DIRECT_FLAG_RIGIDITY.md`.

Trace the concrete Lie ring through `RawCoefficients`, `TableCertificate`,
`Ambient/Lie`, `Lattice/AdaptedBasis`, `Lattice/Integral`, and
`Finite/Coordinates`. Finite basis checks are paired with proof bodies reducing
arbitrary vector identities to those checks. `Finite/Nilpotency` uses the
actual integral embedding to avoid enumerating the finite coordinate carrier.

Inspect `Finite/LieAutomorphisms` for the full Lie-automorphism scope and
`Certificates/DerivationMatrix` for the complete derivation-kernel relation.
The 30-direction witness in `InnerRank` and its scalar extension are independent
of a finite-precision zero residual. Read `Elementary` carefully: it is a
generic operation checker, **not** an actual accepted Smith proof.

The most important limits are the unassembled arbitrary-representative lifting
argument, missing exp/log bijection and analytic estimates, missing actual
Smith acceptance, and missing finite BCH/group-automorphism theorem. These
are explicitly listed in `docs/REMAINING_OBLIGATIONS.md`. Do not infer their
existence from module names such as `BCH`, `TensorAction`, or `InnerRank`.

For every claimed result, ask two separate questions: is there a Lean proof
body with the intended hypotheses, and has it actually been accepted by Lean?
At delivery the second answer is no for every module. `reference/source_inventory.json`
helps navigation but is static, not an elaborated declaration listing. The
prepared axiom/type queries must actually run offline before their output can
be assessed.
