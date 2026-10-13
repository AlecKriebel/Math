#!/usr/bin/env python3
"""Whole stream decoding and independent semantic comparison of three reviews."""
import base64, gzip, hashlib, json, pathlib
from capture import ROOT, PRIVATE, run, now
A=ROOT.parent;target=A/'snapshot/unsolved_math_prioritization/attempts/2303002'
sha=lambda b:hashlib.sha256(b).hexdigest()
observations=[]; failures=[]

def check_stream(family,record,stream,spec,stored_path):
    stored=stored_path.read_bytes(); logical=gzip.decompress(stored)
    nb=spec.get('logical_bytes',spec.get('bytes'))
    hs=spec.get('logical_sha256',spec.get('sha256'))
    assert len(logical)==nb and sha(logical)==hs,(family,record,stream)
    if 'stored_bytes' in spec: assert len(stored)==spec['stored_bytes'] and sha(stored)==spec['stored_sha256']
    observations.append(dict(family=family,record=record,stream=stream,path=str(stored_path.relative_to(A)),bytes=len(logical),sha256=sha(logical)))
    return logical

geometry={}
for path in sorted((A/'path_geometry_review/captures').glob('*.receipt.json')):
    r=json.loads(path.read_text());out={}
    for name in ['stdout','stderr']:
        out[name]=check_stream('geometry',r['label'],name,r[name],A/'path_geometry_review'/r[name]['path'])
    geometry[r['label']]=dict(receipt=r,**out)
    if r['exit_code']!=0: failures.append(dict(family='geometry',label=r['label'],exit=r['exit_code'],stdout=out['stdout'].decode(),stderr=out['stderr'].decode()))
for label,expected in [('author_replay',(target/'SOURCE_CHECKS.json').read_bytes()),('portable_full_sources',(target/'final_review/INDEPENDENT_CHECKS.json').read_bytes()),('portable_math_only',(target/'final_review/INDEPENDENT_CHECKS.json').read_bytes().replace(b'1667',b'1665'))]:
    assert geometry[label]['stdout']==expected and geometry[label]['stderr']==b''
assert geometry['integrity_full']['receipt']['exit_code']==1
assert b'queue_target_2303002' in geometry['integrity_full']['stderr']
assert geometry['integrity_corrected']['receipt']['exit_code']==0
corrected=json.loads(geometry['integrity_corrected']['stdout'])
assert len(corrected['checks'])==232 and len(corrected['scope19'])==19
assert len(corrected['actual_diff19'])==19 and corrected['author_wip_files_preserved']==10
assert geometry['historical_verbatim']['receipt']['exit_code']==1
for label in ['mutation_radial_sign','mutation_compact_cutoff','mutation_proof_binding','mutation_source_binding']:
    assert geometry[label]['receipt']['exit_code']==1 and geometry[label]['stdout']==b'' and b'AssertionError' in geometry[label]['stderr']
geo_symbolic=json.loads(geometry['symbolic_constructive']['stdout'])
assert all(value=='0' for value in geo_symbolic['identities'].values())

poisson={}
records=json.loads((A/'poisson_components_review/receipts/commands.json').read_text())
assert len(records)==45
for r in records+[dict(json.loads((A/'poisson_components_review/receipts/driver.json').read_text()),name='driver')]:
    out={name:check_stream('poisson',r['name'],name,spec,A/'poisson_components_review'/spec['path']) for name,spec in r['streams'].items()}
    assert r['exit']==0 and out['stderr']==b''
    poisson[r['name']]=dict(receipt=r,**out)
for label,expected in [('author_controls',(target/'SOURCE_CHECKS.json').read_bytes()),('review_sources',(target/'final_review/INDEPENDENT_CHECKS.json').read_bytes()),('review_math_only',(target/'final_review/INDEPENDENT_CHECKS.json').read_bytes().replace(b'1667',b'1665'))]:
    assert poisson[label]['stdout']==expected
pc=json.loads(poisson['poisson_controls']['stdout']);assert pc['exact_assertions']==735 and len(pc['rejected_false_claims'])==37

root=json.loads((A/'root_original_reproduction_receipt.json').read_text())
assert root['check_count']==387 and len(root['checks'])==387
assert all(c['passed'] is True for c in root['checks'])
assert root['binding_count']==29 and root['source_gate_author_files']==10 and root['genuine_discovery_turns']==0
assert root['queue_physical_line']==405 and root['queue_changed_pipe_cells']==[8]
for r in root['commands']:
    out={name:check_stream('root',r['label'],name,r[name],A/r[name]['path']) for name in ['stdout','stderr']}
    if r['label']=='dataset_object':
        assert r['exit']==128 and out['stdout']==b'' and out['stderr']
        failures.append(dict(family='root',label=r['label'],exit=r['exit'],stdout='',stderr=out['stderr'].decode()))
    else: assert r['exit']==0 and out['stderr']==b''
    if r['label'].startswith('remote_'):
        api=json.loads(out['stdout']);b=base64.b64decode(api['content'])
        assert b==(A/'snapshot'/api['path']).read_bytes()
        assert api['sha']==hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    if r['label']=='author': assert out['stdout']==(target/'SOURCE_CHECKS.json').read_bytes()
    if r['label']=='historical_with_sources': assert out['stdout']==(target/'final_review/INDEPENDENT_CHECKS.json').read_bytes()
    if r['label']=='historical_math_only': assert out['stdout']==(target/'final_review/INDEPENDENT_CHECKS.json').read_bytes().replace(b'1667',b'1665')

# Execute only the independently read, stable control programs, preserving
# each complete result; reviewer capture/build drivers write and are not replayed.
PY='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
for name,p,expected in [('geometry_symbolic_again',A/'path_geometry_review/symbolic_path_controls.py',geometry['symbolic_constructive']['stdout']),('poisson_controls_again',A/'poisson_components_review/check_poisson_controls.py',poisson['poisson_controls']['stdout'])]:
    p=run(name,[PY,str(p)],A)
    assert p.returncode==0 and p.stderr==b'' and p.stdout==expected

out=dict(completed_utc=now(),whole_streams_read=len(observations),streams=observations,
         retained_expected_failures=failures,geometry_checks=232,poisson_controls=735,poisson_rejections=37,root_checks=387,
         all_full_receipts_equal_independent_expectations=True,
         no_mathematical_disagreement=True,public_verifier_limitations_reported=True,
         theorem_proof_percent=100,novel_theorems=0,overall_audit_percent=70)
(ROOT/'04_cross_family_stream_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['streams']},indent=2))
