# All-dimensional proof certificates

The following files, together with their human-readable derivations in `proof_audit/`, constitute the all-dimensional certificates.

- `independent_verifier/improved_modulus_certificate.json`: 35-term homogeneous and 77-term improved-profile spatial half-plane certificates.
- `independent_verifier/pareto_all_m_certificate.json`: 34-term homogeneous and 84-term equilibrium-scaled spatial certificates.
- `independent_verifier/frontier_certificate.json`: master stable trade-off and gauge-comparison data.
- `data/certificate_tables.tex`: exact coefficient tables printed in the supplement.
- `independent_verifier/verify_symbolic_certificates.py`: aggregate exact symbolic checker.
- `independent_verifier/verify_one_bad_minor.py`: independent one-bad-minor interface and stationary-band audit.
- `independent_verifier/verify_pareto_family.py`: physical equilibrium-scaling and contrast checks.
- `independent_verifier/verify_exchange_of_stability.py` and `verify_branch_stability.py`: nonlinear stability checks.

Finite JSON instances in `data/network_instances/` and `data/exact_instances/` are regression artifacts, not substitutes for the symbolic proof.
