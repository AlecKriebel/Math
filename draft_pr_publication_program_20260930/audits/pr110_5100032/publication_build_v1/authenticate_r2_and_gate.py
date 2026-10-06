#!/usr/bin/env python3
"""Root full-byte authentication of the independently sealed second review."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
A=Path(__file__).resolve().parents[1];R=A/'whole_publication_adversary_r2_20261006'
def need(v,m):
    if not v:raise RuntimeError(m)
def read(p):return json.loads(p.read_text())
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def match(p,row):
    q=pin(p);need(all(q[k]==row[k] for k in ('bytes','sha256')),'Full-byte pin mismatch: '+str(p))
def now():return datetime.now(timezone.utc).isoformat()
start=now();m=R/'OUTPUT_MANIFEST.json';seal=R/'SEAL_RECEIPT.json'
need(pin(m)['sha256']=='939a1a54205b36e283d3c56e88d8c34b6423b0ec30b97f2824006b9974abcb71','R2 fixed manifest')
need(pin(seal)['sha256']=='4bf01f2f97ac34603f01836014253656102a84ba1b563c4d5577f15c34c42696','R2 fixed seal')
rows=read(m)['files'];need(len(rows)==44 and sum(e['bytes'] for e in rows)==172975,'R2 scope')
actual={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file() and 'private_scratch' not in p.relative_to(R).parts}
need(actual=={e['path'] for e in rows}|{'OUTPUT_MANIFEST.json','SEAL_RECEIPT.json'},'Exact R2 public set')
for e in rows:
    need(not (R/e['path']).is_symlink(),'R2 symlink');match(R/e['path'],e)
match(m,read(seal)['output_manifest'])
inputs=read(R/'INPUT_PINS.json');match(Path(inputs['external_candidate_seal']['path']),inputs['external_candidate_seal'])
allpins=inputs['candidate_files']+inputs['candidate_research_inputs']+inputs['primary_and_boundary_inputs']
for e in allpins:match(Path(e['path']),e)
ex=read(R/'EXECUTION_RECEIPTS.json');negative=0
for op in ex['operations']:
    need(op['actual_PID']>0 and op['UTC_start']<=op['UTC_end'],'Genuine recorded process shape')
    for s in ('stdout','stderr'):match(R/op[s]['path'],op[s])
    if op['tag'].startswith('invalid_'):
        r=read(R/op['stderr']['path']);need(op['exit_code']==2 and op['stdout']['bytes']==0 and r['actual_verifier_PID']==op['actual_PID'] and r['status']=='rejected','Real rejected control');negative+=1
    else:need(op['exit_code']==0,'Successful review operation')
need(negative==8,'Eight additional real failures')
replays=[]
for mode in ('normal','optimized'):
    d=A/'actual_operations'/('root_whole_publication_r2_'+mode+'_20261006');e=read(d/'execution.json')
    for s in ('stdout','stderr'):match(d/e[s]['path'],e[s])
    result=read(d/'stdout.bin');need(e['exit_code']==0 and e['stderr']['bytes']==0 and result['actual_PID']==e['child_PID'],'Actual root replay identity')
    need(result['explicit_guards']==21011 and result['optimization']==(mode=='optimized') and result['status']=='passed','Root R2 replay result')
    replays.append({'mode':mode,'execution':pin(d/'execution.json'),'result':pin(d/'stdout.bin'),'actual_PID':e['child_PID']})
v=read(R/'VERDICT.json');need(v['verdict']=='PASS_EXACT_IMMUTABLE_CANDIDATE' and v['required_findings']==[] and v['earlier_R1_review_read_before_verdict'] is False,'Independent clean R2 verdict')
auth={'schema':'pr110-root-R2-authentication/v1','actual_root_PID':os.getpid(),'UTC_start':start,'UTC_end':now(),'full_public_files_authenticated':44,'full_input_pins_authenticated':len(allpins)+1,'manifest':pin(m),'seal':pin(seal),'report':pin(R/'REPORT.md'),'verdict':pin(R/'VERDICT.json'),'root_real_replays':replays,'required_findings':[],'historical_process_receipts_full_stream_hashes_verified':True,'no_claim_of_OS_lookup_of_historical_PIDs':True,'new_review_independent_of_R1':True,'publication_authorized_by_this_receipt':False}
out=A/'ROOT_WHOLE_PACKAGE_R2_AUTHENTICATION_20261006.json';need(not out.exists(),'Unique root authentication');out.write_text(json.dumps(auth,indent=2)+'\n')
evidence=['ROOT_PRIORITY_CLEARANCE_AFTER_M1_20261006.json','ROOT_WHOLE_PACKAGE_R1_AUTHENTICATION_20261006.json','ROOT_WHOLE_PACKAGE_R2_AUTHENTICATION_20261006.json','publication_ready_v1_SEAL.json']
for p in evidence:need((A/p).is_file(),'Required earlier gate evidence')
candidate=read(A/'publication_ready_v1_SEAL.json')
for e in candidate['files']:match(A/'publication_ready_v1'/e['path'],e)
need(read(A/evidence[0])['publication_ready'] is False,'Historical priority gate correctly predates package readiness')
gate={'schema':'pr110-root-publication-readiness/v1','actual_root_PID':os.getpid(),'UTC_start':start,'UTC_end':now(),'PR':110,'problem_id':5100032,'original_head':'3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35','publication_ready':True,'evidence':[pin(A/p) for p in evidence],'required_findings':[],'distinct_whole_package_reviews':['pr110_whole_publication_adversary_r1_20261006','pr110_whole_publication_adversary_r2_20261006'],'substantive_repairs_needed':False,'optional_comments_disposition':'Sparse reference page and possible future nonzero-coefficient exact closed-cycle control are optional; legible frozen candidate retained.','mathematics_completion_percent':100,'bounded_priority_completion_percent':100,'publication_preparation_completion_percent':100,'workflow_completion_percent':65,'priority_statement':'No full cover found in the inspected dated corpus; no absolute-first or exhaustive literature claim.','AI_use_and_unrefereed_disclosure':True,'Zenodo_published':False,'tracker_updated':False,'native_integration_complete':False,'overall_program_complete':False}
gp=A/'ROOT_PUBLICATION_READINESS_V1_20261006.json';need(not gp.exists(),'Unique root readiness gate');gp.write_text(json.dumps(gate,indent=2)+'\n')
print(json.dumps({'root_authentication':pin(out),'readiness_gate':pin(gp),'status':'READY_FOR_AUTHORIZED_PUBLICATION','root_PID':os.getpid()}))
