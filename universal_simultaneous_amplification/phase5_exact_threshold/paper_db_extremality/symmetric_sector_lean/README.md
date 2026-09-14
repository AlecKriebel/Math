# Formalized symmetric-sector component

Lean proofs for the symmetric-balanced component of *Local Complete-Graph Optimality at Fitness Two and Strong-Selection Rigidity under Death–Birth Updating*, by Alec Kriebel ([ORCID](https://orcid.org/0009-0001-9320-500X)). The manuscript sources are in the parent directory.

The principal results prove, for the actual definitions in Appendix A:

- `reducedScalar_pos`: `S_N > 0` for every integer `N ≥ 3`.
- `R2_eq_frobeniusSq_mul_reducedScalar`: for every `n ≥ 4` and real symmetric, zero-diagonal, zero-row-sum matrix `δ`, `R2 δ = frobeniusSq δ * S_(n−1)`. Zero column sums follow from symmetry. The identity includes `δ = 0`.
- `R2_symmetricBalanced_pos`: the genuine active-chain quadratic form is strictly positive for every such nonzero `δ`. Nonnegativity and the exact zero case hold for every `n ≥ 3`; the symmetric-balanced sector at `n = 3` is proved to contain only zero.

`R2` is defined from the labeled chain as `ν₀ Δ G Δ G q`, independently of `S_N`. Both actual matrix inverses, the stationary law, feature identities, orbit averages, source, reward, and normalization factors are proved. `S_N` is the rational inverse expression `gᵀ(I−K)⁻¹s`, with `K = Hᵀ` for the printed Appendix A matrix. Good ranks are `1,…,N−1`, bad ranks `2,…,N−1`, and `N = n−1`. Features are not assumed linearly independent.

The complete finite statements include all `N = 3,…,39`, all phase margins for `N = 40,…,287`, and the exact unique minimum at `N = 40`:

```
1 − beta 40 − epsilon 40 = 639304267467075678841 / 115369588296792467144716.
```

The consistency checks `S_3 = 3/208` and `S_4 = 359/26660` are also transported to the physical forms at `n = 4` and `n = 5`.

## Pinned environment and verification

Lean is pinned to `leanprover/lean4:v4.19.0`; mathlib is pinned to `c44e0c8ee63ca166450922a373c7409c5d26b00b`. The committed manifest pins all transitive packages. With [elan](https://github.com/leanprover/elan) installed, run from this directory:

```sh
lake exe cache get
lake build
python3 tools/audit.py --targets principal_theorems.txt --clean
```

The last command removes only this project's `.lake/build`, rebuilds all production proofs, prints the exact statements and transitive axioms of every listed principal theorem, and writes a dated receipt beneath `reports/audit/`. Do not run it alongside another build. `lake exe cache get` downloads the pinned mathlib build cache; it is not a certificate checker. No `lake update` is needed for checking the committed package versions.

The two generated certificate families use sequential imports to bound peak memory during a clean build. Allow several minutes for the exact kernel reductions. Ordinary `lake build` checks the entire principal import closure. Python and external algebra packages are unnecessary for that build.

Development reused an ignored `.lake/packages` symlink to an already downloaded, revision-matched dependency cache. No theorem or assumption from the sibling Bell project is imported. A fresh checkout obtains the committed dependencies normally. The audit records the actual Lean version and mathlib checkout; the independent trust review also checks every dependency checkout against the manifest.

## Proof method and correction

Small systems have explicit exact rational solution witnesses. Lean checks every specified equation, identifies the witness with the inverse using the independently proved invertibility theorem, and checks the actual reward pairing and sign. The phase range uses one-sided integer-grid witnesses propagated to the actual radial recurrence and finite maximum. The infinite tail proves the rational comparisons on their stated domains using exact algebra and sum-of-squares identities.

The all-order proof combines true Schur elimination, nonnegative inverses, radial and bad-channel barriers, a weighted contraction bound, and the actual debt estimate. It repairs a missing implication in the printed A.31 derivation: directly pairing the printed `Y` barrier gives a differently indexed sum. At `N = 4` the discrepancy is exactly `1/360`. A sharper supersolution `Z_k = 2/[3(k−1)]`, followed by binomial reflection, proves the same printed debt bound and preserves the manuscript's `beta`. See [the independent repair review](reviews/debt_repair_independent.md). This is a repaired proof step, not a counterexample to the scalar theorem.

All mathematical certificates use ordinary proof terms, `norm_num`, or `decide +kernel`. The latter performs kernel reduction; it does not use native evaluation. No `sorry`, unproved project axiom, compiler-backed decision procedure, or external solver assertion is on the certification path. The foundational axioms are `propext`, `Classical.choice`, and `Quot.sound`; per-theorem dependencies are recorded by the audit.

## Discovery tools and records

Certificate generation is optional and untrusted. To regenerate the committed small-system witnesses:

```sh
python3 -m venv .venv
.venv/bin/pip install python-flint==0.9.0 sympy==1.14.0
.venv/bin/python tools/generate_small.py
python3 tools/generate_margins.py
```

Lean checks the generated witnesses independently. See [CORRESPONDENCE.md](CORRESPONDENCE.md), [DEPENDENCIES.md](DEPENDENCIES.md), [RESEARCH_LOG.md](RESEARCH_LOG.md), and the independent [model](reviews/model_translation_final.md), [arithmetic](reviews/finite_arithmetic_final.md), and [trust](reviews/final_trust.md) reviews. Earlier checkpoint reports retain their historical completion estimates; the final audit is authoritative for the released source hashes.

## Exact scope boundary

This is a formalized symmetric-sector component of the local-optimality proof. It does not formalize the coverage/collision identification with fixation, the stationary perturbation expansion and its analyticity, the full tangent-space decomposition, or the signs of the other two sectors. Therefore it does not certify the complete fixation Hessian theorem, local-optimality theorem, biological interpretation, or entire paper. It asserts no global fitness-two conjecture, no neighborhood uniform in population size, no exchange of fixed-graph and growing-family quantifiers, and no strong-selection result.
