# Independent exact verifier

The verifier reconstructs the family from the indexed reactions and keeps the all-spectrum, diffusion-design, and equilibrium-scaled implementations separate.

Core commands:

```bash
python independent_verifier/verify_family.py
python independent_verifier/verify_realization_space.py
python independent_verifier/verify_all_spectrum.py
python independent_verifier/verify_principal_minor_diffusion_ray.py
python independent_verifier/verify_network_one_bad_minor.py
python independent_verifier/verify_diffusion_criterion.py
python independent_verifier/verify_contrast_bounds.py
python independent_verifier/verify_improved_profile.py
python independent_verifier/verify_generic_cubic_recurrence.py
python independent_verifier/frontier_verify_pareto.py
python independent_verifier/frontier_verify_near_threshold.py
python independent_verifier/frontier_verify_exposition_identities.py
python independent_verifier/verify_symbolic_certificates.py
python independent_verifier/verify_branch_stability.py
```

## Evidence classification

The all-dimensional proof objects are the source proofs in `proof_audit/`, the
modulus and signed-scalar coefficient tables in `data/`, and the exact JSON
certificates in this directory. The executable layers have deliberately
different evidentiary roles:

- `verify_generic_cubic_recurrence.py` is a standalone symbolic bridge. It
  imports no project construction helper and proves, with symbolic `m` and a
  formal harmonic sum, that the printed zero/second-harmonic recurrences reduce
  the cubic contraction to `R_m+C_m*hfrak`; it also checks the boundary
  determinant and gauge contraction.
- `frontier_verify_exposition_identities.py`, the modulus-certificate scripts,
  and the scalar-bound scripts regenerate exact algebraic certificate objects.
  They support the printed identities but do not replace the human domain and
  functional-analytic arguments.
- Scripts whose substantive matrix loops use listed dimensions are finite
  exact regression tests. They are mutation-sensitive checks, not
  all-dimensional proofs. In particular, `verify_cubic_sign.py` checks full
  contractions only in representative dimensions; the generic bridge above
  supplies the missing recurrence-to-closed-form identity.
- The `dd_*.py` scripts share `common.py` with their corresponding regression
  layer. They are duplicate replay checks, not independent implementations and
  must not be counted as additional mathematical evidence.
- `verify_branch_stability.py` is a finite floating-point complementary-spectrum
  regression. It is counterexample/provenance evidence only, not a proof of the
  nonlinear branch-stability theorem.
- Aggregate entrypoints such as `verify_improved_profile.py`,
  `verify_pareto_family.py`, and `verify_symbolic_certificates.py` only run
  child scripts; a wrapper `PASS` adds no evidence beyond those children.

The exposition-identity verifier reconstructs the printed second-harmonic
boundary system, clearing identities, gauge derivatives, source polynomials,
and fixed contrast product. The family verifier also checks the explicit
maximal stoichiometric minor `det=4(-1)^m` through the same two-step expansion
used in the proof.

The exact verifiers require normal Python assertion mode. Every direct
entrypoint fails immediately under `python -O` or a nonzero `PYTHONOPTIMIZE`
setting; `common.py`, `core.py`, `pareto_core.py`, and `stable_core.py` are
import-only support modules. The test suite executes every direct entrypoint
under `-O` to keep this fail-closed property from regressing.
