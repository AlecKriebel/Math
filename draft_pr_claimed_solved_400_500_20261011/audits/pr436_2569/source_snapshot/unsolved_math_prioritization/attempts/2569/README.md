# A central-double-cover obstruction to rational projective lifting

Kourovka Notebook 21.60 · Catalogue ID 2569

This package proposes a **negative answer**, with `G=SL(2,5)` and `p=2`.

Every projective indecomposable over `F_2G` meets the requested positive Grothendieck-group condition. Explicit rational witnesses cover all three `F_2`-module types. Yet an eight-dimensional projective forces an odd multiplicity of a quaternionic ordinary constituent, so it cannot lift to `Z_(2)G`; that ring is not semiperfect.

The complete proof is in [COUNTEREXAMPLE.md](COUNTEREXAMPLE.md). It separates the elementary central-square-zero argument, the credited `A_5` modular data, and the Frobenius–Schur obstruction. The source statement is the October 2026 Notebook, printed page 186.

## Validation status

This is a complete candidate proof with exact computational checks, a contributing mathematical check, and a separate fresh adversarial audit with verdict PASS. These checks were AI-assisted; they are **not specialist human verification** or formal proof-assistant certification. No priority claim or claim of an established literature solution is made.

The source's general extension-lifting assertion is not used in the proof. The fifth research attempt records a precise elementary obstruction to that step. The remaining established `A_5` data are explicitly credited and checked against an independent decomposition calculation.

## Files

- `COUNTEREXAMPLE.md`: complete candidate proof and references
- `SOURCE_GATE.md`: exact statement, source provenance, and retrieval limitations
- `RESEARCH_LOG.md`: five substantive attempts, with outcomes and counting rules
- `turn_01.md` through `turn_05.md`: the full mathematical attempt record
- `verify_counterexample.py` and `counterexample_results.json`: standard-library exact verifier and results
- `verify_controls.py` and `control_results.json`: small controls for the failed direct-lifting route and quaternionic padding
- `contributor_checks/`: separate character/decomposition calculation and contributor report, not the final audit
- `independent_audit/`: fresh final audit, independently written verifier, exact mathematical coefficient input, and results
- `PUBLICATION.md`: attribution, audit scope, and publication limitations
- `status.json`: machine-readable status and scope

## Reproduce

Run `python verify_counterexample.py` and `python verify_controls.py` with Python 3. The main checker uses only the standard library and checks all 14,400 quaternion products, constructs an actual symmetric-cube character, computes its norm and Frobenius–Schur indicator, enumerates `SL(2,5)`, verifies the augmentation module's absolute irreducibility and Sylow restriction, and checks all positive witness equations.

The additional `python contributor_checks/check_character_data.py` and `python independent_audit/independent_audit.py` use SymPy. It reconstructs the full ordinary character table, a splitting-field decomposition matrix, Cartan data, and the fused `F_2` projective characters. The associated report identifies which inputs are mathematical source facts rather than computed consequences.

The proof supplies the theoretical bridge to nonsemiperfectness; finite arithmetic alone does not prove that bridge. Source PDFs, screenshots, raw catalogue data, and private context are not part of this package.
