# Qubit Bell-setting formalization — end-to-end source draft

**Uncompiled and not kernel-verified.** Start with [SEMANTIC_AUDIT.md](SEMANTIC_AUDIT.md),
[PREFLIGHT_STATUS.md](PREFLIGHT_STATUS.md), and [OFFLINE_RUN.md](OFFLINE_RUN.md). The earlier [SOURCE_STATUS.md](SOURCE_STATUS.md)
is retained as historical source-writing status, not a successful build receipt.

This project targets Alec Kriebel's *Minimum Bell-Setting Complexity for Qubit
POVM–PVM Separation*, DOI `10.5281/zenodo.21699161`. The new source route includes
the main arbitrary-output two-input equality, the minimum-setting classification,
the explicit 3×2 separation, and the strengthened Appendix B attainment.

## Main entry points

| Source | Purpose |
|---|---|
| `Bell/Assembly.lean` | Unconditional main-theorem proof attempts and minimum settings |
| `Bell/SimulationCorollaries.lean` | Finite common-randomness mixtures of complete PVM strategies |
| `Bell/StrengthenedWitness.lean` | Actual state and POVMs attaining `(16+8√7813)/25` |
| `Bell/Quantum.lean` | Complex qubits, density matrices, measurements, raw/hull behavior sets |
| `docs/SOURCE_COVERAGE.md` | Claim-to-source map and validation boundaries |
| `docs/SOURCE_PROOF_ROUTE.md` | The alternative proof architecture and normalization conventions |
| `reports/source_completion/` | Fresh static and exact-algebra evidence for this phase |

## Additional mathematical-interface audit

The newest compiler-free pass adds an independent exact physical checker,
including complex state/measurement conventions, common-span filters, finite
cone degeneracies, complete-strategy relabeling, and a coupled rank-three saddle
with an explicit increasing physical path. The saddle is **not** a POVM/PVM
separation. All 58 mathematical source modules and the 14 statement contracts
are unchanged from the incoming preflight package.

See [SEMANTIC_AUDIT.md](SEMANTIC_AUDIT.md) for executed evidence and limitations,
and [the exact rank-three test](docs/RANK_THREE_STRESS_TEST.md) for its formulas.

```bash
# Requires the Python test dependencies; never invokes Lean or Lake.
python3 scripts/preflight_all.py
```

## Deferred Lean run

The toolchain pin is `leanprover/lean4:v4.19.0`. Mathlib is pinned to
`c44e0c8ee63ca166450922a373c7409c5d26b00b` with the dependency manifest retained.

```bash
bash scripts/check.sh --bootstrap
```

This command has **not** been run for the new draft. It is intended to compile all
imports and then check public theorem axiom dependencies, including the named
main claims. No claim is made that the first run will succeed without repairs.

For the separate exact finite-algebra checks:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/source_completion_checks.py --suite all
```

For static source and audit-parser checks only:

```bash
python3 scripts/source_audit.py
python3 scripts/source_completion_inventory.py
python3 scripts/test_axiom_audit.py
```

The last commands do not invoke Lean. The parser tests use mock dependency text.

## Mathematical scope

The models use actual complex two-dimensional local Hilbert spaces, finite
input-dependent output alphabets, and shared randomness selecting entire
state-and-measurement strategies. Identity/zero projectors, unused labels, and
mixed-state inputs are retained. The conclusion is hull equality, **not**
raw-image equality, same-state simulation, or projective simulability of each
individual POVM. The Bell values are attained lower bounds and certified-bound
source attempts, not claims of exact global optima.

## Preservation

The complete incoming continuation archive is in
`preservation/input_before_source_completion.zip`. Earlier recovery archives,
reports, and supplied paper PDF are retained. Root status documents point to the
current source status; historical documents are marked separately.

`SHA256SUMS.txt` and the archive receipt certify byte integrity only. Build
products and toolchain caches are not included. The retained environment-export
helpers are optional historical infrastructure; they were not used or rerun
while writing this source.
