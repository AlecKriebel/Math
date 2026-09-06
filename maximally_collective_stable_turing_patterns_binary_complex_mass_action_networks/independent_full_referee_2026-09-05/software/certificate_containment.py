"""Reproduce malformed-certificate acceptance and trace enclosing gates."""
import copy,json,shutil
import audit_driver as a

full=a.SCRATCH/'full'; src=a.SOURCE/'independent_verifier/pareto_all_m_certificate.json'
original=json.loads(src.read_text())
mutant=copy.deepcopy(original)
mutant['modulus']['homogeneous']['terms'].append({'powers':[99,99],'coefficient_in_U_ascending':['-1']})
mutant['modulus']['spatial']['terms'].append({'powers':[99,99,99],'coefficient_in_A_ascending':['-1']})
variants={'extra_negative_terms':mutant}
for where in ('first','last'):
    obj=copy.deepcopy(original)
    for block,field in [('homogeneous','coefficient_in_U_ascending'),('spatial','coefficient_in_A_ascending')]:
        term=copy.deepcopy(obj['modulus'][block]['terms'][0]);term[field]=[str(-__import__('fractions').Fraction(v)) for v in term[field]]
        if where=='first':obj['modulus'][block]['terms'].insert(0,term)
        else:obj['modulus'][block]['terms'].append(term)
    variants['opposite_duplicate_'+where]=obj
obj=copy.deepcopy(original);obj['modulus']['homogeneous']['term_count']=23;obj['modulus']['spatial']['term_count']=85
variants['declared_counts_changed']=obj
obj=copy.deepcopy(original);obj['modulus']['unrecognized_referee_block']={'terms':[{'powers':[99],'coefficient':'-1'}]}
variants['unknown_block_metadata']=obj

# The unit-profile verifier uses a set, so identical positive duplicates
# collapse too. Preserve the list exactly as the malformed input presents it.
unit_path=full/'independent_verifier/improved_modulus_certificate.json'
unit_bytes=unit_path.read_bytes();unit_obj=json.loads(unit_bytes)
for block in ('homogeneous','improved_mode'):
    unit_obj[block]['terms'].append(copy.deepcopy(unit_obj[block]['terms'][0]))
unit_artifact=a.HERE/'mutation_artifacts/unit_identical_duplicates.json'
unit_artifact.parent.mkdir(exist_ok=True)
unit_artifact.write_text(json.dumps(unit_obj,indent=2)+'\n')
unit_path.write_bytes(unit_artifact.read_bytes())
try:
    a.run('containment_unit_identical_duplicates',['python','independent_verifier/verify_mode_isolation.py'],full,expected=1)
finally:unit_path.write_bytes(unit_bytes)

for name,obj in variants.items():
    path=a.HERE/'mutation_artifacts'/(name+'.json');path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n')
    a.run('containment_'+name,['python',str(full/'independent_verifier/frontier_verify_mode_certificates.py'),str(path)],full,expected=1 if name!='unknown_block_metadata' else 0)

# Same modified JSON, through the printed-table checks in the portable package.
path=full/'independent_verifier/pareto_all_m_certificate.json';baseline=path.read_bytes();path.write_text(json.dumps(mutant,indent=2)+'\n')
try:
    a.run('containment_full_exposition',['python','independent_verifier/frontier_verify_exposition_identities.py'],full,expected=1)
    a.run('containment_full_symbolic_aggregate',['python','independent_verifier/verify_symbolic_certificates.py'],full,expected=1)
finally:path.write_bytes(baseline)

# The minimal packet deliberately has no printed tables or generators.
minimal=a.SCRATCH/'minimal_containment';shutil.copytree(a.SOURCE/'external_audit/minimal_verifier',minimal,dirs_exist_ok=True)
(minimal/'pareto_all_m_certificate.json').write_text(json.dumps(mutant,indent=2)+'\n')
a.run('containment_minimal_symbolic_aggregate',['python','verify_symbolic_certificates.py'],minimal,expected=1)

# Isolate the real fixed-manifest gate after a controlled, synthetic TeX
# protocol preflight. No PDF build is attempted or claimed in this control.
public=a.SCRATCH/'public_containment';shutil.copytree(a.SOURCE/'public/repository',public,dirs_exist_ok=True)
(public/'independent_verifier/pareto_all_m_certificate.json').write_text(json.dumps(mutant,indent=2)+'\n')
env=a.ENV.copy();env['PATH']=str(a.SCRATCH/'lock_stubs')+':'+env['PATH']
a.run('containment_portable_manifest_gate',['bash','replay.sh'],public,expected=1,env=env)
log=(a.LOGS/'containment_portable_manifest_gate.log').read_text()
assert 'TOOLCHAIN_LOCK_PASS' in log and '[1/8]' not in log and 'PUBLIC_REPLAY_PASS' not in log
print('CONTAINMENT_AUDIT_COMPLETE; ACTUAL_PINNED_TEX_NOT_CLAIMED')
