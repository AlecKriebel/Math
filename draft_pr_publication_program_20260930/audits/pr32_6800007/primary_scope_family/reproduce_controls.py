#!/usr/bin/env python3
"""Isolated exact-head replay and finite negative controls; no universal-proof certificate."""
import ast, hashlib, json, pathlib, shutil, subprocess, sys
from datetime import datetime, timezone

HERE=pathlib.Path(__file__).resolve().parent
SNAP=HERE.parent/'source_snapshot'
MANIFEST=json.loads((HERE.parent/'snapshot_manifest.json').read_text())
WORK=HERE/'isolated_controls'; WORK.mkdir(exist_ok=True)
OUT=HERE/'control_outputs';OUT.mkdir(exist_ok=True)
PYTHON=pathlib.Path('/Users/alec/Documents/Math/.venv/bin/python')
def sha(b):return hashlib.sha256(b).hexdigest()
def binding(directory):
    failures=[]
    for f in MANIFEST['files']:
        p=directory/f['path']
        if not p.is_file():failures.append({'path':f['path'],'reason':'missing'})
        else:
            b=p.read_bytes()
            if len(b)!=f['size'] or sha(b)!=f['sha256']: failures.append({'path':f['path'],'reason':'bytes differ'})
    return {'accepted':not failures,'failures':failures}
def copy(name):
    directory=WORK/name
    if directory.exists():shutil.rmtree(directory)
    shutil.copytree(SNAP,directory)
    return directory
def run(directory,script,label,python=PYTHON):
    started=datetime.now(timezone.utc).isoformat()
    p=subprocess.run([str(python),script],cwd=directory,capture_output=True)
    (OUT/(label+'.stdout')).write_bytes(p.stdout);(OUT/(label+'.stderr')).write_bytes(p.stderr)
    obj=None
    if p.returncode==0:obj=json.loads(p.stdout)
    expected=(SNAP/('verification.json' if script=='verify.py' else 'review/independent_results.json')).read_bytes()
    return {'label':label,'utc_started':started,'exit_code':p.returncode,'stdout_sha256':sha(p.stdout),'stdout_bytes':len(p.stdout),
            'stderr_sha256':sha(p.stderr),'stderr_bytes':len(p.stderr),'byte_equal_original_receipt':p.stdout==expected,
            'json_pass':None if obj is None else obj.get('pass'),
            'assertion_count':None if obj is None else obj.get('assertions',len(obj.get('checks',obj.get('symbolic_and_group_checks',[])))),
            'torsion_cases':None if obj is None else obj.get('torsion_cases'),
            'failure_excerpt':p.stderr.decode(errors='replace')[-1200:] if p.returncode else None}
result={'utc':datetime.now(timezone.utc).isoformat(),'python':str(PYTHON),'expected_sympy':'1.14.0',
    'boundary':'A byte-binding control and executable assertion replay are provenance/algebra checks. They cannot certify h-principle, global mapping-space proof or novelty.', 'runs':[], 'controls':[]}
base=copy('baseline')
result['baseline_binding']=binding(base)
assert result['baseline_binding']['accepted']
for script,label in [('verify.py','baseline_author'),('review/independent_checks.py','baseline_independent')]:
    replay=run(base,script,label); result['runs'].append(replay)
    assert replay['exit_code']==0 and replay['json_pass'] and replay['byte_equal_original_receipt']
for name,mutation in [('proof_deleted',lambda d:(d/'CANDIDATE.md').unlink()),
                       ('proof_false_claim',lambda d:(d/'CANDIDATE.md').write_text('False control claim: every real three-manifold admits a proper totally real immersion into the nearly Kaehler unordered flag quotient, and one class exhausts all homotopies.\n'))]:
    d=copy(name);mutation(d)
    gate=binding(d);assert not gate['accepted']
    runs=[run(d,s,name+'_'+label) for s,label in [('verify.py','author'),('review/independent_checks.py','independent')]]
    assert all(v['exit_code']==0 and v['byte_equal_original_receipt'] for v in runs)
    result['runs']+=runs
    result['controls'].append({'name':name,'frozen_binding':gate,'standalone_scripts_still_pass':True,
        'implication':'Receipt counts alone are not bound to any proof text; exact proof hash plus independent mathematical review is required.'})
for name,script,old,new in [
    ('ordinary_c2_substitution','verify.py','virtual_c2=c2(ar)-sum(ar)*delta+delta**2-c2(rs)','virtual_c2=c2(ar)-c2(rs)'),
    ('cochain_torsion_corruption','review/independent_checks.py','K_d2 = s.Matrix([[0, 0, 2]])','K_d2 = s.Matrix([[0, 0, 4]])')]:
    d=copy(name);p=d/script;code=p.read_text();assert old in code;p.write_text(code.replace(old,new))
    replay=run(d,script,name);result['runs'].append(replay)
    assert replay['exit_code']!=0 and not binding(d)['accepted']
    result['controls'].append({'name':name,'frozen_binding':binding(d),'algebra_script_rejected':True})

source=json.loads((HERE/'SOURCE_IDENTITY_AUDIT.json').read_text())
assert all(source['identity_controls'].values())
result['controls'].append({'name':'source_identity_and_serialization','checks':source['identity_controls'],'all_detected':True})
inputs=json.loads((HERE/'EXACT_INPUT_AUDIT.json').read_text())
paths=inputs['diff']['paths'];attempt_prefix='unsolved_math_prioritization/attempts/6800007/'
folder_only=all(p.startswith(attempt_prefix) for p in paths)
approved_scope=all(p.startswith(attempt_prefix) or p=='unsolved_math_prioritization/QUEUE.md' for p in paths)
assert not folder_only and approved_scope
result['controls'].append({'name':'actual_action_scope','folder_only_denial_rejected':not folder_only,
    'queue_plus_target_folder_scope_accepted':approved_scope,'queue_path':'unsolved_math_prioritization/QUEUE.md',
    'not_permission_gate':'Historical draft/no-merge prose does not override current human authorization; this family performs no Git/GH mutation.'})
queue=inputs['queue']['current'][0];cells=[c.strip() for c in queue.split('|')[1:-1]]
legacy_cells=cells[:4]+cells[5:9]
assert len(cells)==12 and len(legacy_cells)==8
result['controls'].append({'name':'legacy_eight_column_generator','current_columns':len(cells),'mutant_columns':len(legacy_cells),
    'schema_rejected':len(legacy_cells)!=12,'protected_cell_indices_one_based':[5,10,11,12],
    'current_protected_values':[cells[i-1] for i in [5,10,11,12]],'live_queue_mutated':False})
candidate=(SNAP/'CANDIDATE.md').read_text()
result['scope_controls']=[{'change':change,'not_covered_by_candidate':True,'reason':reason} for change,reason in [
    ('Replace ordered SL3C/B complex structure with nearly Kaehler or unordered quotient','Root bundles, c1 and source target differ.'),
    ('Interpret target as neighboring real-form uniformization question','Source TeX gives a separate question; this formula classifies TR regular homotopies.'),
    ('Require proper immersion/homotopy for noncompact source','Target flag is compact; a proper map into it would force source compact.'),
    ('Replace regular TR homotopy with ordinary map homotopy','Formal derivative isomorphism data is discarded; S3 has Z map components and Z additional formal frame components.'),
    ('Set orientation Bockstein to zero for all real3 sources','RP2 x S1 has nonzero beta w1 and empty index set.'),
    ('Discard nonorientable H3 torsion using deRham cohomology','Klein x S1 and RP2 x S1 have integral H3=Z/2.')]]
result['script_ast']={name:{'imports':sorted({n.name for node in ast.walk(ast.parse((SNAP/name).read_text())) if isinstance(node,ast.Import) for n in node.names}),
    'reads_candidate_literal':'CANDIDATE.md' in (SNAP/name).read_text(),'has_open_calls':any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='open' for n in ast.walk(ast.parse((SNAP/name).read_text())))} for name in ['verify.py','review/independent_checks.py']}
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'runs':len(result['runs']),'controls':len(result['controls']),'baseline_byte_equal':True,
    'proof_mutations_still_pass':True,'arithmetic_mutations_rejected':True},indent=2))
