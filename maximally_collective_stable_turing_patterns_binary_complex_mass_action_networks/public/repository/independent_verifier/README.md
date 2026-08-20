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
python independent_verifier/frontier_verify_pareto.py
python independent_verifier/frontier_verify_exposition_identities.py
python independent_verifier/verify_symbolic_certificates.py
python independent_verifier/verify_branch_stability.py
```

The all-dimensional proof objects are the source proofs in `proof_audit/`, the
modulus and signed-scalar coefficient tables in `data/`, and the exact JSON
certificates in this directory. The exposition-identity verifier reconstructs
the printed second-harmonic boundary system, clearing identities, gauge
derivatives, source polynomials, and fixed contrast product.  The family
verifier also checks the explicit maximal stoichiometric minor
`det=4(-1)^m` through the same two-step expansion used in the proof.  Finite
dimensions are regression tests only.

The exact verifiers require normal Python assertion mode. Canonical entrypoints
fail immediately under `python -O` or a nonzero `PYTHONOPTIMIZE` setting.
