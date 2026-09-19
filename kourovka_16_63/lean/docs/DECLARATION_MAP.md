> **Historical delivery record — 17 September 2026.** The uncompiled status below describes the original cloud delivery. See the current root README, `progress.json`, and accompanying local verification report for the repaired source and actual compiler results.

# Paper-to-Lean declaration map — source revision 0.1.0

## Status vocabulary

**Fully proved and kernel-checked declarations: none.** All source in this
package is uncompiled. A written tactic proof is not an accepted theorem.

A conditional helper is a theorem for its explicitly stated hypotheses, not an
axiom; its proof body also remains uncompiled. The concrete final argument must
supply those hypotheses. External executed tests have no formal soundness merely
because they pass. The static inventory lists actual source command names and
locations but is not an elaborated declaration list.

## Coverage by mathematical obligation

| Obligation | Source under `Kourovka/` | Principal content | Status |
| --- | --- | --- | --- |
| Raw integral formula and original table | RawCoefficients; TableCertificate | raw/table coefficient equality and signs | proof_body_written_uncompiled |
| Ambient Lie ring | Ambient/Lie; Linear/Basis | basis-to-arbitrary Jacobi, alternating bilinear bracket, structure values | proof_body_written_uncompiled |
| Concrete finite-field generation | Flag/Generation | 88 DAG nodes and all 31 targets; automorphism/derivation generation induction | proof_body_written_uncompiled |
| Full finite-field flag stabilizer | Flag/Rigidity | full_flag_rigidity; lieEquiv_flag_rigidity | proof_body_written_uncompiled |
| Infinitesimal flag stabilizer | Flag/Rigidity | infinitesimal_flag_rigidity | proof_body_written_uncompiled |
| Adapted basis and scaled bracket | Lattice/AdaptedBasis; Lattice/Integral | P; embed; embed_bracket; scaled Jacobi and structure values | proof_body_written_uncompiled |
| Generation over p-adic integers | Lattice/IntegralGeneration | generator_value_ring; denominator_unit_padic; padic_generation | proof_body_written_uncompiled |
| Finite quotient coordinates | Finite/Coordinates; Finite/PadicQuotient | reduction kernel; quotientEquiv; cardinality_at_depth | proof_body_written_uncompiled |
| Nilpotency bound | Finite/Nilpotency | monomial_vanishes; target_lowerCentralSeries | proof_body_written_uncompiled |
| All additive endomorphisms are scalar-linear | Finite/AdditiveLinear | additive maps/equivalences to residue-ring linear maps/equivalences | proof_body_written_uncompiled |
| Full Lie-ring automorphisms are full matrix automorphisms | Finite/LieAutomorphisms | ringAutEquivEntries; full_lie_aut_card_eq_matrix_card | proof_body_written_uncompiled |
| Arbitrary representative lifting | Lattice/Precision; WeightedFlags; NearIdentity | i-6 error bound, word induction, weighted flags, power gains; assembly absent | conditional_helpers_uncompiled |
| Derivation matrix | Certificates/DerivationMatrix; Indexing | actual K formula, full kernel equivalence, lexicographic index relation | proof_body_written_uncompiled |
| No hidden higher-valuation rank | Certificates/InnerRank; InnerScalarExtension | 30-direction left inverse; characteristic_zero_rank_upper | proof_body_written_uncompiled |
| Elementary coordinate operations | Certificates/Elementary | decode/decodeCircuit; check_sound; composite-ring controls | generic_checker_uncompiled_not_actual_smith |
| Scalar/diagonal kernels | Certificates/ScalarKernel; DiagonalKernel; KernelTransport | exact scalar count and equivalences; actual K application absent | general_proofs_uncompiled |
| Tensor and exp/log ingredients | Analytic/TensorAction; NilpotentUnit; Lattice/NearIdentity | three commuting actions; factor equivalence; finite inverse; series missing | conditional_helpers_uncompiled |
| BCH ingredients | BCH/Dynkin; CoefficientSoundness | dynkin_expand; eval_zero_of_coeff_zero with explicit degree hypothesis | general_proofs_uncompiled_not_lazard |
| Actual Smith acceptance | data/smith_pivot_plan.txt | actual 931-pivot local Smith proof and acceptance | absent_external_historical_evidence_only |
| Full exp/log bijection | no completed declaration | actual integrality, inverse, precision and set bijection | absent |
| BCH group and full group/Lie correspondence | no completed declaration | group law plus every ordinary group automorphism | absent |
| Final cardinalities and notebook corollary | Challenge (targets only) | no actual G, no closed exact orders or notebook theorem | absent |

## Executed tests without formal proof

`source_evidence.py`, `generate_certificates.py`, `direct_flag.py`, and the literal
check ran this session. The original C++ Smith verification log is from the
previous session. Neither is counted as a Lean theorem. The new operation
checker soundness attempt does not change this until it is compiled and its
actual input acceptance is established.

## Unformalized paper material and alternative organization

The full finite-field automorphism classification, cohomology calculations,
separate perfectness theorem, and exact centre theorem are not formalized here.
The direct flag proof and explicit inner-direction witness replace their roles
in the selected dependency path. The remaining exp/log and Lazard claims are
not replaced; they remain outstanding.

For every individual named source command, use
`reference/source_inventory.json`. Its entries are all marked `uncompiled`.
The generated `validation/AxiomAudit.lean` and `Statements.lean` are requests
for future real output, not retained successful output.
