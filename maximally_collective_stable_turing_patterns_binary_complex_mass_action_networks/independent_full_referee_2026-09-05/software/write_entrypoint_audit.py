import ast, pathlib
import audit_driver as a
notes={
'frontier_verify_cubic_bound.py':('symbolic scalar inequalities','Shifted polynomial signs, harmonic bounds, tau derivatives/endpoint comparison; domain inequalities and the link to PDE stability remain human proof steps.'),
'frontier_verify_determinant_identity.py':('finite exact determinants','m=3,4 symbolic L; m=5 fixed rational L; determinant versus chain-product formula. Does not prove the chain recurrence in all dimensions.'),
'frontier_verify_exposition_identities.py':('symbolic identities and finite interfaces','Regenerates rational clearing identities, boundary determinant, 77/84 source polynomials and printed-table freshness. Uses discovery-side generators only for text freshness. Extra/duplicate-term weakness documented in SOFTWARE_REPORT.'),
'frontier_verify_family.py':('finite exact reconstruction','Default m=3,4,5,6,8,10: reaction matrices, rank, mass covector, rates, AH realization and physical H*Delta diffusion.'),
'frontier_verify_master_certificate.py':('metadata/algebra interface','Checks named factors, endpoints, contrast product and normal-form conventions; cannot independently establish their mathematical origins.'),
'frontier_verify_mode_certificates.py':('symbolic modulus and rational enclosure','Regenerates 22/84 polynomials, m=3 Routh boundary, finite characteristic connection, and exact Gaussian-rational Rouche counterexample at old m=149 endpoint. Extra/duplicate-term false acceptance documented.'),
'frontier_verify_near_threshold.py':('symbolic expansion and finite ansatz','Checks affine ansatz at listed dimensions and symbolic epsilon expansion. Supplied m=3 cubic rational function limit/sign is checked; its Hessian derivation was independently verified by the algebra referee.'),
'frontier_verify_normal_form.py':('finite exact normal form','Default m=3,4,5,6,8,10: explicit zero/second-harmonic solves, transformed left vector/mass gauge, eta/cubic contraction at L0.'),
'frontier_verify_pareto.py':('finite exact algebraic ordering','Default m=3,4,5,6,8,10; additional portable regression includes149,200. Exact positivity ordering at L0; no float/evalf ordering.'),
'frontier_verify_pareto_curve.py':('finite exact normal form','Direct vectors, gauges, contractions at L0/midpoint/L1 in listed dimensions; no all-L proof from these samples.'),
'verify_all_spectrum.py':('symbolic boundary plus finite SCC regression','Symbolic positive boundary Routh coefficients; exact SCC/Hurwitz enumeration in m=3,4,5,6,8 at two rational parameter families including b=2a. Generic SCC exhaustion remains the manuscript argument.'),
'verify_branch_stability.py':('finite floating spectral regression','NumPy eigenvalues for listed dimensions/modes and scaled endpoints; near-zero eigenvalues filtered at1e-7. No nonlinear stability proof or certified interval spectrum.'),
'verify_contrast_bounds.py':('finite exact ordering','m=3..20 extremal diffusion values and factor-eight comparison; simple all-m inequalities are in manuscript.'),
'verify_critical_profile.py':('finite exact linear residuals','m=3,4,5,6,8,10; core critical right/left vectors and pairings compared to direct matrix products.'),
'verify_cubic_sign.py':('symbolic signs plus finite contractions','Positive coefficients after m=u+3; direct contractions in six dimensions; generic recurrence bridge handled separately.'),
'verify_current_numerical_provenance.py':('independent finite exact solves','No construction-helper imports; reconstructs reactions, Hessian and constrained zero/second-harmonic solves for every current row m=3..10; checks rational vectors/pairings/eta/cubic.'),
'verify_diffusion_criterion.py':('finite exact determinant coefficients','Listed dimensions; elementary-symmetric diffusion expansion, omission factor8; symbolic m=3 flux-dependent threshold and nonzero resultants distinguish a,b dependence.'),
'verify_exchange_of_stability.py':('exact signs plus floating spectrum','Exact eta/cubic signs in six dimensions; complementary and higher-mode eigenvalues checked numerically with1e-7/1e-8 tolerances.'),
'verify_family.py':('finite exact reconstruction','Indexed reactions, nonzero maximal minor and two-step structural expansion, flux-cone basis, symbolic a,b,h realization Jacobian; six dimensions.'),
'verify_generic_cubic_recurrence.py':('standalone symbolic identity','No project helpers. Rational-function field in symbolic m and formal harmonic sum: boundary vectors, mass gauge, second-harmonic recurrence, contraction reduction and gauge contraction. Human proof supplies positive denominator/domain interpretation.'),
'verify_harmonic_corrections.py':('finite exact linear solves','Six dimensions; both Fourier factors -1/4, second-mode Laplacian factor4, and mass gauge.'),
'verify_improved_profile.py':('aggregate wrapper','Runs five child scripts with subprocess check=True. No new mathematical evidence.'),
'verify_mode_certificates.py':('aggregate wrapper','Runs unit and scaled mode-certificate children with check=True. No new mathematical evidence.'),
'verify_mode_isolation.py':('symbolic modulus plus finite determinants','35/77 exact polynomial tables, symbolic zero-derivative/telescoping bridge and denominator sign; sparse determinant checked m=3,4,5. Identical duplicate rows collapse in set comparison.'),
'verify_network_one_bad_minor.py':('finite exact interface','m=3,4,5,6 examples: determinant coefficient signs and derivative/signed-sum relation.'),
'verify_order_m_minors.py':('finite exact determinants','Six dimensions and one positive rational a,b pair; checks complete omission table.'),
'verify_pareto_family.py':('aggregate wrapper','Runs eight children, with small normal-form/curve dimensions; check=True failure propagation. No independent evidence beyond children.'),
'verify_principal_minor_diffusion_ray.py':('finite exact general-matrix interfaces','Includes lower endpoint n=2, stable singular Laplacians n=2..5 and crossing networks m=3..6; exact coefficient expansion and lambda-derivative decomposition.'),
'verify_realization_space.py':('finite exact flux interfaces','Six dimensions; rank, nullity and A=Gamma diag(v)Y^T identities. Full positive-realization classification remains rank/cone argument in source.'),
'verify_stable_contrast.py':('finite exact signs','Selected eta/cubic formulas and contrast at m=3,4,5,6,8,10,20,50.'),
'verify_symbolic_certificates.py':('aggregate wrapper','Sixteen named children with check=True, including standalone generic recurrence. Finite children retain finite evidentiary scope.'),
}
for path in (a.SOURCE/'independent_verifier').glob('dd_*.py'):
    name=path.name[3:]; notes[path.name]=('duplicate '+notes[name][0],'Substantive code duplicates '+name+' and shares common.py; does not add an independent derivation. '+notes[name][1])
assert len(notes)==39
text='# Semantic inventory of all 39 direct entrypoints\n\nEvery entrypoint was read and independently executed successfully in normal CPython3.9.6; every one was rejected under `python -O` with an assertion-mode message. This table distinguishes what those successful runs establish.\n\n| Entrypoint | Evidence | Mechanism and exact boundary |\n|---|---|---|\n'
for name,(kind,note) in sorted(notes.items()):text+=f'| `{name}` | {kind} | {note} |\n'
text+='\nThe four import-only helpers are `common.py`, `core.py`, `stable_core.py`, and `pareto_core.py`. `common.py` and `core.py` are byte-identical. All direct scripts guard assertion mode before imports/subprocesses. Exact verifiers use SymPy Rational/Integer arithmetic, except the explicitly classified NumPy spectral regressions; floating decimals in generators/figures are presentation and numerical illustration. Shell replay sets `PYTHONOPTIMIZE=0`; wrapper processes use `sys.executable` and `check=True`.\n'
(a.HERE/'ENTRYPOINT_AUDIT.md').write_text(text)
