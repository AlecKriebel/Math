#!/usr/bin/env python3
"""Seal original public analysis/metadata only, excluding closing envelopes."""
from pathlib import Path
import json,hashlib,datetime,os
D=Path(__file__).resolve().parent
def check(v,msg):
    if not v: raise RuntimeError(msg)
def pin(p):
    b=p.read_bytes();return {'path':str(p.relative_to(D)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
v=json.loads((D/'VERDICT.json').read_text());a=json.loads((D/'INPUT_AUTHENTICATION.json').read_text());c=json.loads((D/'CUSTODY_AND_READ_SCOPE.json').read_text())
check(v['recommended_state']=='HOLD_FOR_ESSENTIAL_IDENTIFIED_VERSION_GAP' and v['bounded_substantive_novelty_supported'] and not v['already_solved_supported'],'verdict state')
check(not v['priority_clearance'] and not v['publication_clearance'] and v['new_central_proof_search_turns']==0,'clearance scope')
check(a['public_payload_bodies_authenticated']==514 and c['private_body_pins_authenticated']==256 and c['author_book_Git_bodies_authenticated']==145,'custody counts')
for k,name in [('input_authentication_pin','INPUT_AUTHENTICATION.json'),('custody_read_scope_pin','CUSTODY_AND_READ_SCOPE.json')]:
    pp=v['authentication'][k];b=(D/name).read_bytes();check(pp['bytes']==len(b) and pp['sha256']==hashlib.sha256(b).hexdigest(),'verdict metadata pin '+name)
operations=[]
for ep in sorted((D/'actual_operations').glob('*/execution.json')):
    r=json.loads(ep.read_text());s=json.loads((ep.parent/'started.json').read_text())
    check(r['child_PID']!=r['recorder_PID'] and r['argv']==s['argv'] and r['UTC_start']==s['UTC_start'] and r['recorder_PID']==s['recorder_PID'],'process consistency')
    for stream in ['stdout','stderr']:
        pp=r[stream];b=(ep.parent/pp['path']).read_bytes();check(len(b)==pp['bytes'] and hashlib.sha256(b).hexdigest()==pp['sha256'],'stream hash')
    operations.append({'label':ep.parent.name,'child_PID':r['child_PID'],'recorder_PID':r['recorder_PID'],'exit_code':r['exit_code']})
excluded_files={'OUTPUT_MANIFEST.json','SEAL_RECEIPT.json','CLOSING_AUTHENTICATION.json'}
excluded_prefixes=('actual_operations/final_seal/','actual_operations/verify_closing_envelope/','private_sources/','private_review_materials/')
rows=[]
for p in sorted(D.rglob('*')):
    if not p.is_file():continue
    rel=str(p.relative_to(D))
    if rel in excluded_files or rel.startswith(excluded_prefixes):continue
    check(not p.is_symlink(),'linked public payload')
    rows.append(pin(p))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
m={'schema':'pr110-cross-family-public-full-body-manifest/v1','UTC':now,'actual_sealer_PID':os.getpid(),'public_payload_count':len(rows),'public_payload_bytes':sum(r['bytes'] for r in rows),'payload':rows,'excluded_files':sorted(excluded_files),'excluded_prefixes':list(excluded_prefixes),'closing_rule':'Actual recorder final_seal/execution.json is written after child exits and authenticated separately. Manifest, seal receipt and closing verification cannot hash themselves.','copyrighted_body_extract_render_raw_results_redistributed':False,'priority_clearance':False,'publication_clearance':False,'recommended_state':v['recommended_state']}
dump(D/'OUTPUT_MANIFEST.json',m)
for r in rows:
    p=D/r['path'];b=p.read_bytes();check(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'payload changed during seal')
s={'schema':'pr110-cross-family-public-seal-receipt/v1','UTC':now,'actual_sealer_PID':os.getpid(),'manifest':pin(D/'OUTPUT_MANIFEST.json'),'report':pin(D/'REPORT.md'),'verdict':pin(D/'VERDICT.json'),'public_payload_count':len(rows),'all_public_payload_full_bodies_rechecked':True,'completed_actual_operations_authenticated':operations,'closing_recorder_receipt':'actual_operations/final_seal/execution.json','closing_record_will_be_created_after_this_child_exits':True,'sealer_and_recorder_separate':True,'required_priority_gap':'M1','priority_clearance':False,'publication_clearance':False,'private_material_redistributed':False}
dump(D/'SEAL_RECEIPT.json',s)
print(json.dumps({'actual_sealer_PID':os.getpid(),'manifest_sha256':s['manifest']['sha256'],'report_sha256':s['report']['sha256'],'verdict_sha256':s['verdict']['sha256'],'payload_count':len(rows)}))
