"""Explicitly partial replay of every non-TeX portable stage."""
import hashlib
import audit_driver as a

root=a.SCRATCH/'portable'
exact=['data/current_profile_exact.json','data/contrast_table.tex','data/certificate_tables.tex','data/sign_certificate_tables.tex','data/triad_routh_gap.tex']+[f'data/network_instances/Nhat_m{m}.json' for m in [3,4,5,6,8,10]]+[f'data/exact_instances/pareto_m{m}_L0.json' for m in [3,4]]
expected={x:hashlib.sha256((a.SOURCE/'public/repository'/x).read_bytes()).hexdigest() for x in exact}
commands=[
('regenerate_profile',['python','computation/generate_current_profile_data.py']),
('regenerate_tables',['python','computation/generate_tables.py']),
('regenerate_sign_tables',['python','computation/generate_sign_certificate_tables.py']),
('portable_source_audit',['python','computation/audit_manuscript.py']),
('portable_detached_provenance',['python','independent_verifier/verify_current_numerical_provenance.py']),
('portable_symbolic_aggregate',['python','independent_verifier/verify_symbolic_certificates.py']),
('portable_integrated_improved',['python','independent_verifier/verify_improved_profile.py']),
('portable_integrated_family',['python','independent_verifier/frontier_verify_family.py','3','4','5','6','8','10']),
('portable_integrated_normal_form',['python','independent_verifier/frontier_verify_normal_form.py','3']),
('portable_integrated_pareto',['python','independent_verifier/frontier_verify_pareto.py','3','4','5','6','8','10','149','200']),
('portable_integrated_exchange',['python','independent_verifier/verify_exchange_of_stability.py']),
('portable_integrated_branch',['python','independent_verifier/verify_branch_stability.py']),
]
commands += [(f'export_m{m}',['python','computation/export_instance.py',str(m),'--out',f'data/network_instances/Nhat_m{m}.json']) for m in [3,4,5,6,8,10]]
commands += [(f'export_pareto_m{m}',['python','computation/export_pareto_instance.py',str(m),'--out',f'data/exact_instances/pareto_m{m}_L0.json']) for m in [3,4]]
commands += [
('full_15_simulations',['python','computation/simulations.py','--outdir','data/simulations','--jobs','3']),
('regenerated_numerical_provenance',['python','computation/audit_numerical_provenance.py']),
('figure_stable_tradeoff',['python','figures/stable_tradeoff.py']),
('figure_stable_profiles',['python','figures/stable_profiles.py']),
('figure_amplitude_scaling',['python','figures/amplitude_scaling.py']),
('portable_stale_claim_audit',['python','computation/audit_stale_claims.py']),
]
for name,command in commands:
    if a.run(name,command,root)!=0: raise SystemExit('PARTIAL_REPLAY_FAILED '+name)
assert all(hashlib.sha256((root/x).read_bytes()).hexdigest()==expected[x] for x in exact)
print('THIRTEEN_EXACT_BASELINE_ARTIFACTS_MATCH')
print('NON_TEX_PORTABLE_STAGES_PASS; FULL_PORTABLE_REPLAY_AND_DETACHED_TEX_BUILDS_NOT_CLAIMED')
