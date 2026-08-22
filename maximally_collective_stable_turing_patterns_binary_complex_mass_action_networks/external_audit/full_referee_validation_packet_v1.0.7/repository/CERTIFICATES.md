# All-dimensional proof certificates

The all-dimensional arguments are human-readable in `proof_audit/` and checked by these exact commands:

- `python independent_verifier/verify_all_spectrum.py`
- `python independent_verifier/verify_principal_minor_diffusion_ray.py`
- `python independent_verifier/verify_network_one_bad_minor.py`
- `python independent_verifier/dd_verify_order_m_minors.py`
- `python independent_verifier/dd_verify_diffusion_criterion.py`
- `python independent_verifier/dd_verify_contrast_bounds.py`
- `python independent_verifier/dd_verify_mode_isolation.py`
- `python independent_verifier/dd_verify_harmonic_corrections.py`
- `python independent_verifier/dd_verify_cubic_sign.py`
- `python independent_verifier/frontier_verify_mode_certificates.py`
- `python independent_verifier/frontier_verify_master_certificate.py`
- `python independent_verifier/frontier_verify_near_threshold.py`
- `python independent_verifier/frontier_verify_cubic_bound.py`
- `python independent_verifier/frontier_verify_determinant_identity.py`
- `python independent_verifier/frontier_verify_exposition_identities.py`
- `python independent_verifier/verify_symbolic_certificates.py`

Printed coefficient tables are `data/certificate_tables.tex`, `data/sign_certificate_tables.tex`, and `data/triad_routh_gap.tex`. The single exact source for all displayed finite values is `data/current_profile_exact.json`. Finite instances are regression checks, not replacements for the symbolic proof.
