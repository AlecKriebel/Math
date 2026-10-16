#!/usr/bin/env python3
"""Read-only authentication; writes metadata solely beside this file."""
from pathlib import Path
import datetime, hashlib, json, os

D=Path(__file__).resolve().parent
A=D.parent
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def check(ok,msg):
    if not ok: raise RuntimeError(msg)
def pin(p):
    b=p.read_bytes()
    return {'path':str(p.relative_to(A)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify_entry(folder,entry):
    p=folder/entry['path']
    check(p.is_file() and not p.is_symlink(),'missing/linked payload '+str(p))
    actual=pin(p)
    check(actual['bytes']==entry['bytes'] and actual['sha256']==entry['sha256'],'pin mismatch '+str(p))
    return actual
def operation(folder,label):
    e=folder/'actual_operations'/label
    start=json.loads((e/'started.json').read_text())
    record=json.loads((e/'execution.json').read_text())
    check(record['argv']==start['argv'] and record['cwd']==start['cwd'],'argv/cwd '+label)
    check(record['UTC_start']==start['UTC_start'],'UTC start '+label)
    check(record['recorder_PID']==start['recorder_PID'],'recorder PID '+label)
    check(isinstance(record['child_PID'],int) and record['child_PID']>0,'actual child '+label)
    check(record['child_PID']!=record['recorder_PID'],'PID separation '+label)
    check(datetime.datetime.fromisoformat(record['UTC_end'])>=datetime.datetime.fromisoformat(record['UTC_start']),'timestamps '+label)
    for stream in ['stdout','stderr']:
        q=e/record[stream]['path']; actual=pin(q)
        check(actual['bytes']==record[stream]['bytes'] and actual['sha256']==record[stream]['sha256'],'stream '+label)
    return {'label':label,'child_PID':record['child_PID'],'recorder_PID':record['recorder_PID'],'exit_code':record['exit_code'],'argv':record['argv'],'receipt':pin(e/'execution.json')}

families=[
 ('exact','priority_exact_invariant_history_20261006','56a7a95b53a97916dc83ee9fce02b7034ef5ce37ba12781a7b49a385892a7122','payload','seal_public_audit_final'),
 ('classical','priority_classical_confocal_mechanism_20261006','c31ff3476ba625f91b7d15bea8a2097ec8d9c7aaf26f449fecafe0e7c6ce7869','payload','final_seal'),
 ('modern','priority_modern_invariant_mechanism_20261006','070552d43ff08757eb0275ee952f5c49e235efeb0c7f6a6e6f951ca8841e3e6e','public_payload_bodies','seal_public_payload')]
out={'schema':'pr110-cross-family-input-authentication/v1','UTC':now(),'actual_authenticator_PID':os.getpid(),'families':[],'original_and_policy_inputs':[]}
for name,foldername,expected,listkey,closing in families:
    F=A/foldername; mp=pin(F/'OUTPUT_MANIFEST.json'); check(mp['sha256']==expected,'manifest '+name)
    m=json.loads((F/'OUTPUT_MANIFEST.json').read_text()); s=json.loads((F/'SEAL_RECEIPT.json').read_text())
    entries=m[listkey]
    if isinstance(entries,dict): entries=[dict(v,path=k) for k,v in entries.items()]
    for ent in entries: verify_entry(F,ent)
    closing_record=operation(F,closing)
    check(closing_record['exit_code']==0,'seal failed '+name)
    check(m['actual_sealer_PID']==s['actual_sealer_PID']==closing_record['child_PID'],'sealer mismatch '+name)
    actual_ops=[operation(F,p.parent.name) for p in sorted((F/'actual_operations').glob('*/execution.json'))]
    item={'family':name,'folder':foldername,'manifest':mp,'receipt':pin(F/'SEAL_RECEIPT.json'),'report':pin(F/'REPORT.md'),'verdict':pin(F/'VERDICT.json'),'full_public_payload_bodies_authenticated':len(entries),'actual_operations_authenticated':actual_ops,'closing_envelope_authenticated':True}
    for p in [F/'INPUT_PINS.json',F/'INPUT_AUTHENTICATION.json',F/'ACTUAL_PROCESS_AUTHENTICATION.json']:
        if p.exists(): item.setdefault('additional_input_metadata_pins',[]).append(pin(p))
    out['families'].append(item)
paths=[
 'original_head_authentication_20261006/POLICY_AGENTS.md',
 'original_head_authentication_20261006/POLICY_unsolved_math_prioritization_AGENTS.md',
 'original_head_authentication_20261006/original_attempt/PROOF.md',
 'original_head_authentication_20261006/original_attempt/source_record.json',
 'original_head_authentication_20261006/original_attempt/prior_imported_report.json',
 'ROOT_MATHEMATICAL_GATE_20261006.json',
 'ROOT_EXACT_PRIORITY_FAMILY_AUTHENTICATION_20261006.json',
 'ROOT_CLASSICAL_PRIORITY_FAMILY_AUTHENTICATION_20261006.json',
 'ROOT_MODERN_PRIORITY_FAMILY_AUTHENTICATION_20261006.json']
for path in paths: out['original_and_policy_inputs'].append(pin(A/path))
proof=out['original_and_policy_inputs'][2]
check(proof['sha256']=='8478d2a792944c5fb9e8a53324e0c6bce8eba317de29c31a6fcbd6ca0205709d','original proof pin')
prior=json.loads((A/paths[4]).read_text());check(prior and prior['result'],'nonempty prior')
gate=json.loads((A/paths[5]).read_text())
check(gate['original_head']=='3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35','head')
check(gate['mathematical_clearance'] and gate['original_effort']=='2/5' and gate['new_central_proof_search_turns']==0,'gate scope')
out['public_payload_bodies_authenticated']=sum(f['full_public_payload_bodies_authenticated'] for f in out['families'])
out['preserved_original_prior_nonempty']=True
out['new_central_proof_search_turns']=0
out['shared_input_mutations']=False
(D/'INPUT_AUTHENTICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'authenticated_public_bodies':out['public_payload_bodies_authenticated'],'closing_envelopes':3,'actual_PID':os.getpid(),'output':'INPUT_AUTHENTICATION.json'}))
