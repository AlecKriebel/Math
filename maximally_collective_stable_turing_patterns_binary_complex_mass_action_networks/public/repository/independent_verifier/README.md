# Independent exact verifier

The verifier reconstructs the family from the indexed reactions and keeps the all-spectrum, diffusion-design, and equilibrium-scaled implementations separate.

Core commands:

```bash
python independent_verifier/verify_family.py
python independent_verifier/verify_realization_space.py
python independent_verifier/verify_all_spectrum.py
python independent_verifier/verify_one_bad_minor.py
python independent_verifier/verify_diffusion_criterion.py
python independent_verifier/verify_contrast_bounds.py
python independent_verifier/verify_improved_profile.py
python independent_verifier/verify_pareto_family.py
python independent_verifier/verify_symbolic_certificates.py
python independent_verifier/verify_branch_stability.py
```

The all-dimensional proof objects are the source proofs in `proof_audit/`, the coefficient tables in `data/certificate_tables.tex`, and the exact JSON certificates in this directory. Finite dimensions are regression tests only.
