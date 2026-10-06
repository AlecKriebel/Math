#!/usr/bin/env python3
"""Reproduce the NEW whole-current gate using unchanged private program copies.
Writes only tmp/reproduce/; requires existing /usr/bin/python3 + SymPy1.14.0.
Does not mutate recorded receipts, fetch sources, run Git or invoke queue helpers.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
OUT=HERE/'tmp/reproduce'
PYTHON='/usr/bin/python3'
def digest(data):return hashlib.sha256(data).hexdigest()
def read(p):return json.loads(p.read_text())
def bind(root,entries):
    for e in entries:
        p=root/e['path'];assert p.is_file() and p.stat().st_size==e.get('bytes',e.get('size')) and digest(p.read_bytes())==e['sha256'],e['path']
def protected():
    bind(BASE/'reviewed_candidate',read(BASE/'reviewed_candidate/MANIFEST.json')['files'])
    bind(BASE,read(BASE/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json')['files'])
    if (HERE/'MANIFEST.json').exists():bind(HERE,read(HERE/'MANIFEST.json')['files'])
def copy_program_tree():
    root=OUT/'audits/pr32_6800007';root.mkdir(parents=True,exist_ok=True)
    for e in read(BASE/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json')['files']:
        q=root/e['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(BASE/e['path'],q)
    packet=root/'reviewed_candidate';shutil.copytree(BASE/'reviewed_candidate',packet,dirs_exist_ok=True)
    own=root/'current_whole_adversary';own.mkdir(exist_ok=True);(own/'tmp').mkdir(exist_ok=True);shutil.copyfile(HERE/'fresh_controls.py',own/'fresh_controls.py')
    return root
runs=[]
def execute(label,path,cwd,args=()):
    p=subprocess.run([PYTHON,str(path.resolve()),*args],cwd=cwd,capture_output=True,timeout=90)
    (OUT/f'{label}.stdout').write_bytes(p.stdout);(OUT/f'{label}.stderr').write_bytes(p.stderr)
    runs.append({'label':label,'exit_code':p.returncode,'stdout_sha256':digest(p.stdout),'stderr_bytes':len(p.stderr)})
    return p
protected();OUT.mkdir(exist_ok=True);tree=copy_program_tree()
for label,code,expected in [('author','verify.py','verification.json'),('old_independent','review/independent_checks.py','review/independent_results.json')]:
    p=execute(label,tree/'source_snapshot'/code,tree/'source_snapshot');assert p.returncode==0 and not p.stderr and p.stdout==(BASE/'source_snapshot'/expected).read_bytes()
p=execute('geometry',tree/'hprinciple_family/controls.py',tree/'hprinciple_family');assert p.returncode==0 and not p.stderr and p.stdout==(BASE/'hprinciple_family/controls_results.json').read_bytes()
p=execute('integral',tree/'integral_action_family/integral_controls.py',tree/'integral_action_family');assert p.returncode==0 and not p.stderr and p.stdout==(BASE/'integral_action_family/integral_results.json').read_bytes()
p=execute('integral_expected_failure',tree/'integral_action_family/integral_controls.py',tree/'integral_action_family',('--mutant','ordinary_c2'));assert p.returncode==1 and b'EXPECTED_FAILURE' in p.stderr
p=execute('primary_all_mutants',tree/'primary_scope_family/reproduce_controls.py',tree/'primary_scope_family');assert p.returncode==0 and not p.stderr
old=read(BASE/'primary_scope_family/CONTROL_RESULTS.json');new=read(tree/'primary_scope_family/CONTROL_RESULTS.json')
for a,z in zip(old['runs'],new['runs']):
    assert a['label']==z['label'];label=a['label']
    for suffix in ['stdout','stderr']:
        original=(BASE/'primary_scope_family/control_outputs'/f'{label}.{suffix}').read_bytes();got=(tree/'primary_scope_family/control_outputs'/f'{label}.{suffix}').read_bytes()
        if suffix=='stderr':got=got.replace(str((tree/'primary_scope_family').resolve()).encode(),str((BASE/'primary_scope_family').resolve()).encode())
        assert original==got
    for value in [a,z]:
        value.pop('utc_started',None)
        if a['exit_code']:
            for key in ['stderr_sha256','stderr_bytes','failure_excerpt']:value.pop(key,None)
old.pop('utc');new.pop('utc');assert old==new
p=execute('prior_specialization',tree/'priority_topology_family/specialization_check.py',tree/'priority_topology_family');assert p.returncode==0 and not p.stderr
old=read(BASE/'priority_topology_family/SPECIALIZATION_CHECK.json');new=read(tree/'priority_topology_family/SPECIALIZATION_CHECK.json');old.pop('recorded_utc');new.pop('recorded_utc');assert old==new
# The priority closed-preservation program must read closed original families,
# not the primary copy whose generated outputs just changed in the replay above.
flagbase=OUT/'priority/audits/pr32_6800007';flag=flagbase/'priority_flag_family';flag.mkdir(parents=True,exist_ok=True)
for e in read(BASE/'priority_flag_family/MANIFEST.json')['files']:
    q=flag/e['path'];q.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(BASE/'priority_flag_family'/e['path'],q)
for name in ['sources']:
    q=flag/name
    if not q.exists():q.symlink_to((BASE/'priority_flag_family'/name).resolve(),target_is_directory=True)
for name in ['primary_scope_family','source_snapshot']:
    q=flagbase/name
    if not q.exists():q.symlink_to((BASE/name).resolve(),target_is_directory=True)
q=flagbase.parent/'pr31_10000043/primary_scope_family';q.parent.mkdir(exist_ok=True,parents=True)
if not q.exists():q.symlink_to((BASE.parent/'pr31_10000043/primary_scope_family').resolve(),target_is_directory=True)
p=execute('prior_binding',flag/'priority_binding_controls.py',flag);assert p.returncode==0 and not p.stderr
old=read(BASE/'priority_flag_family/CONTROL_RESULTS.json');new=read(flag/'CONTROL_RESULTS.json');old.pop('generated_utc');new.pop('generated_utc');assert old==new and new['closed_families_unchanged']
p=execute('new_independent_controls',tree/'current_whole_adversary/fresh_controls.py',tree/'current_whole_adversary');assert p.returncode==0 and not p.stderr
old=read(HERE/'FRESH_CONTROL_RESULTS.json');new=read(tree/'current_whole_adversary/FRESH_CONTROL_RESULTS.json')
for value in [old,new]:
    for k in ['utc','queue_observed_sha256','frozen_queue_preimage_matches_observation']:value.pop(k)
assert old==new
protected()
result={'pass':True,'actual_runs':runs,'complete_generated_results_equal_with_only_explicit_clock_and_verified_traceback_prefix_normalizations':True,'original_expected_failure_is_failure':True,'private_source_and_program_copies_only':True,'protected_current32_and186_and_own_closed_firstparty_unchanged':True,'diagnostics_not_universal_topology_or_novelty_certificate':True}
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
