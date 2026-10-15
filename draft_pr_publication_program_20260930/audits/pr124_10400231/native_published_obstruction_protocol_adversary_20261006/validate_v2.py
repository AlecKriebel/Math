"""Validate corrected V2 by exact body hashes and target-only normalization.

This script never invokes native CLI or performs Git/index/service writes.
"""
from pathlib import Path
import copy, datetime, hashlib, json, os, subprocess

H=Path(__file__).resolve().parent; A=H.parent; C=A.parents[2]; R=Path('/Users/alec/Documents/Math')
D=A/'native_published_obstruction_preparation_20261006'; old='fresh_published_obstruction_disposition_adversary_20261006/REPORT.md'
new='draft_pr_publication_program_20260930/audits/pr124_10400231/'+old
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'; K='10400231'
checks=[]; inputs={}; events=[]; control_results=[]
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def require(v,label):
    if not v: raise RuntimeError(label)
    checks.append(label)
def read(p):
    require(p.is_file() and not p.is_symlink(),'Regular V2 input '+str(p))
    b=p.read_bytes(); inputs[str(p)]={'path':str(p),'bytes':len(b),'sha256':sha(b)}; return b
def load(p): return json.loads(read(p))
def dump(n,x): (H/n).write_text(json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
def git(*args,cwd=C):
    start=now();p=subprocess.Popen([GIT,*args],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));out,err=p.communicate()
    events.append({'actual_PID':p.pid,'UTC_start':start,'UTC_end':now(),'argv':[GIT,*args],'cwd':str(cwd),'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)})
    require(p.returncode==0,'Successful V2 read-only Git process');return out
def transform(x,from_value,to_value):
    if isinstance(x,dict):return {k:transform(v,from_value,to_value) for k,v in x.items()}
    if isinstance(x,list):return [transform(v,from_value,to_value) for v in x]
    return to_value if x==from_value else x
def count(x,value):
    if isinstance(x,dict):return sum(count(v,value) for v in x.values())
    if isinstance(x,list):return sum(count(v,value) for v in x)
    return int(x==value)
def negative(label,fn):
    try:fn()
    except (ValueError,RuntimeError,KeyError):control_results.append({'control':label,'rejected':True})
    else:raise RuntimeError('Accepted bad V2 control '+label)
start=now()
base=git('rev-parse','HEAD');branch=git('branch','--show-current');index=git('diff','--cached','--name-only','-z');dirty=git('diff','--name-only','-z')
require(base.strip()==b'5de48499b84f168099d0273a340f4976f841f691' and branch==b'main\n' and not index,'V2 still pinned main with empty index')
primary=git('rev-parse','HEAD',cwd=R);primaryindex=git('diff','--cached','--name-only','-z',cwd=R);primarydirty=git('diff','--name-only','-z',cwd=R)
v1body=read(D/'PREPARED_RECEIPT.json');v1=load(H/'V1_PREPARED_RECEIPT.json');require(v1body==read(H/'V1_PREPARED_RECEIPT.json'),'Original V1 prepared receipt unchanged')
v2body=read(D/'CORRECTED_PREPARED_RECEIPT_V2.json');require(sha(v2body)=='cbcc2d7ada7ccd6d08bec3a8871c42ed3bed7ed5bf5d379ce33663e2cfd747fe','Exact supplied V2 receipt pin')
v2=json.loads(v2body);correction=load(D/'LOCATOR_CORRECTION_V2.json');repair_source=read(A/'repair_native_evidence_locator_v2_20261006.py')
require(sha(read(D/'LOCATOR_CORRECTION_V2.json'))==v2['locator_correction_sha256'],'V2 locator correction body pin')
require(v2['V1_receipt_sha256']==sha(v1body) and v2['actual_locator_repair_operator_PID']==v2['actual_operator_PID']==correction['actual_operator_PID']==75162,'V2 receipt binds honest V1 and repair PID75162')
require(correction['independent_V1_finding_sha256']==sha(read(H/'V1_FINDING.json')),'V2 exact independent V1 finding binding')
require(v2['source_inputs']==v1['source_inputs'] and v2['read_only_revalidation_events']==v1['read_only_revalidation_events'],'Original baseline/continuation provenance retained')
require(v2['private_native_command_operator_PID']==68361 and v2['actual_receipt_completion_operator_PID']==70252 and not v2['native_commands_repeated'] and v2['new_native_commands_in_v2']==0 and v2['new_history_events_in_v2']==0,'No command or event repetition; three operator roles explicit')
require(v2['new_central_proof_search_turns']==0 and not v2['shared_tracked_files_exported'] and v2['native_export_pending_fresh_writer_grant'],'V2 still private; newproof0 and writer grant pending')
oldpins={x['path']:x for x in v1['proposed_native_pins']};newpins={x['path']:x for x in v2['proposed_native_pins']}
require(len(oldpins)==len(newpins)==15 and set(oldpins)==set(newpins),'V2 exact same 15 unique destination paths')
changed=[];total=0;v2objects={}; qualified_locations=[]
def locations(x,path=''):
    if isinstance(x,dict):
        for k,v in x.items():
            if v==new:qualified_locations.append({'member':member,'json_path':path+'/'+k})
            locations(v,path+'/'+k)
    elif isinstance(x,list):
        for i,v in enumerate(x):locations(v,path+'/'+str(i))
for member,pin in newpins.items():
    original=oldpins[member];p1=Path(original['prepared_local_path']);p2=Path(pin['prepared_local_path']);b1=read(p1);b2=read(p2)
    require(len(b1)==original['bytes'] and sha(b1)==original['sha256'],'V1 full body still unchanged '+member)
    require(len(b2)==pin['bytes'] and sha(b2)==pin['sha256'],'V2 full proposed body pin '+member)
    require(p1!=p2 and p2.parent.parent==D/'v2' and p2.name==p1.name and p2.parent.name==p1.parent.name,'Separate contained V2 postimage '+member)
    if p1.suffix=='.json':
        x1=json.loads(b1);x2=json.loads(b2);n=count(x1,old);total+=n
        require(transform(x2,new,old)==x1,'All V2 JSON semantics unchanged except exact locator '+member)
        require(count(x2,new)==n and count(x2,old)==0,'All target locators corrected '+member)
        expected=(json.dumps(transform(x1,old,new),indent=2,sort_keys=True)+'\n').encode() if n else b1
        require(b2==expected,'V2 deterministic full JSON serialization '+member)
        v2objects[member]=x2;locations(x2)
    elif p1.suffix=='.jsonl':
        l1=b1.splitlines(keepends=True);l2=b2.splitlines(keepends=True);require(len(l1)==len(l2),'V2 exact unchanged history event count '+member);n=0
        for i,(line1,line2) in enumerate(zip(l1,l2)):
            x1=json.loads(line1);x2=json.loads(line2);m=count(x1,old);n+=m
            require(transform(x2,new,old)==x1,'V2 event semantic/timestamp preservation '+member+':'+str(i+1))
            require(count(x2,new)==m and count(x2,old)==0,'V2 event exact locator count '+member+':'+str(i+1))
            expected=(json.dumps(transform(x1,old,new),sort_keys=True)+'\n').encode() if m else line1
            require(line2==expected,'V2 untouched prefix and deterministic changed event body '+member+':'+str(i+1));locations(x2,'line'+str(i+1))
        total+=n
    else:n=0;require(b1==b2,'Non-JSON V2 body unchanged '+member)
    if n:changed.append({'path':member,'occurrences':n,'before_sha256':sha(b1),'after_sha256':sha(b2)})
require(total==10 and len(changed)==6 and changed==correction['changes'],'Independent exact 10 replacements in 6 bodies match correction record')
require(sum('/10400231/' in x['member'] or '/10400231/' in x['json_path'] or x['member'].endswith('history.jsonl') for x in qualified_locations)==10,'All ten locator references are target-specific evidence')
ep=v2objects['unsolved_math_prioritization/attempts/10400231/PRIORITY_EVIDENCE.json'];review=read(C/ep['fresh_review'])
require(ep['fresh_review']==new and sha(review)==correction['review_report_sha256']=='c47bb56bca384c7a0e88f76e1b93e93ffaa7d7a54450d6cffacfba3ae8483412','Corrected repository-qualified review resolves to exact fresh report')
require(ep['new_central_proof_search_turns']==0 and ep['original_effort_imported']==2 and not ep['express_historical_refutation_established'],'V2 evidence still original2/5/newproof0 and scoped old mathematical content')
bad=copy.deepcopy(v2objects['unsolved_math_prioritization/state.json']);bad[K]['at']='FORGED'
negative('changed original event timestamp',lambda:require(transform(bad,new,old)==json.loads(read(Path(oldpins['unsolved_math_prioritization/state.json']['prepared_local_path']))),'Forged timestamp rejected'))
bad2=copy.deepcopy(v2objects['unsolved_math_prioritization/assessments.json']);key=next(k for k in bad2 if k!=K);bad2[key]['p_solve']=0.999
negative('unrelated assessment corruption',lambda:require(transform(bad2,new,old)==json.loads(read(Path(oldpins['unsolved_math_prioritization/assessments.json']['prepared_local_path']))),'Wrong other target rejected'))
bad3=copy.deepcopy(ep);bad3['fresh_review']=old
negative('uncorrected bare locator',lambda:require(bad3['fresh_review']==new,'Bare locator rejected'))
# Recheck every V1 input full body, allowing only the explicitly disclosed future
# preparer source expression update. Preserve both historical source versions.
v1inputs=load(H/'V1_INPUT_HASHES.json')['inputs'];source_record={}
for item in v1inputs:
    p=Path(item['path']);b=read(p)
    if p==A/'prepare_native_published_obstruction_20261006.py' and sha(b)!=item['sha256']:
        future=b"'fresh_review':str((A/ready['fresh_disposition_review']).relative_to(C))";historical=b"'fresh_review':ready['fresh_disposition_review']"
        require(b.count(future)==1,'Single disclosed future preparer locator expression')
        restored=b.replace(future,historical);require(sha(restored)==item['sha256'],'Historical corrected source reconstructed exactly from single future change')
        dest=H/'V1_CORRECTED_PREPARER_RECONSTRUCTED.py';dest.write_bytes(restored);read(dest)
        failure=load(D/'ACTUAL_INTERRUPTED_RECEIPT_PHASE.json');executed=restored.replace(b"'cache_snapshot_sha256':sha(cache.read_bytes())",b"'cache_snapshot_sha256':sha(cache)")
        require(sha(executed)==failure['actual_executed_original_script_sha256'],'Actual originally executed defective source reconstructed exact hash')
        dest2=H/'ACTUAL_EXECUTED_PREPARER_RECONSTRUCTED.py';dest2.write_bytes(executed);read(dest2)
        source_record={'future_preparer_sha256':sha(b),'historical_corrected_preparer_sha256':sha(restored),'actual_executed_defective_preparer_sha256':sha(executed),'historical_sources_explicitly_reconstructed_not_reexecuted':True}
    else:require(len(b)==item['bytes'] and sha(b)==item['sha256'],'V1 whole-body inputs still match current version '+str(p))
for item in v2['source_inputs']:
    b=git('show',item['Git_commit']+':'+item['path']);require(len(b)==item['bytes'] and sha(b)==item['sha256'],'V2 baseline exact full Git body '+item['path'])
    for root in [C,R]:
        p=root/item['path'];expected=b if root==C else git('show',primary.strip().decode()+':'+item['path'],cwd=R)
        if p.exists():require(read(p)==expected,'No shared V2 export '+str(p))
for root in [C,R]:require(not (root/'unsolved_math_prioritization/attempts'/K).exists(),'No shared V2 native attempt '+str(root))
require(git('rev-parse','HEAD')==base and git('branch','--show-current')==branch and git('diff','--cached','--name-only','-z')==index and git('diff','--name-only','-z')==dirty,'V2 audit leaves isolated main/index/tracked changes unchanged')
require(git('rev-parse','HEAD',cwd=R)==primary and git('diff','--cached','--name-only','-z',cwd=R)==primaryindex and git('diff','--name-only','-z',cwd=R)==primarydirty,'V2 audit leaves primary main/index/tracked changes unchanged')
dump('V2_INPUT_HASHES.json',{'schema':'pr124-native-protocol-v2-full-inputs/v1','UTC':now(),'inputs':list(inputs.values()),'historical_source_version_record':source_record})
dump('V2_ACTUAL_VALIDATION.json',{'schema':'pr124-native-protocol-v2-actual-validation/v1','UTC_start':start,'UTC_end':now(),'actual_operator_PID':os.getpid(),'checks_passed':len(checks),'checks':checks,'negative_controls':control_results,'read_only_events':events,'exact_V2_receipt_sha256':sha(v2body),'V1_receipt_unchanged':True,'all15_V2_full_body_pins_verified':True,'exact_target_reference_replacements':10,'bodies_with_reference_replacements':6,'qualified_locations':qualified_locations,'original_timestamps_and_event_counts_preserved':True,'V1_whole_body_inputs_revalidated_except_disclosed_future_preparer_source':True,'historical_source_version_record':source_record,'native_CLI_invocations':0,'new_history_events':0,'new_central_proof_search_turns':0,'shared_exports':False,'service_writes':False})
print(json.dumps({'UTC':now(),'actual_PID':os.getpid(),'checks_passed':len(checks),'input_count':len(inputs),'negative_controls':len(control_results),'V2_receipt_sha256':sha(v2body),'target_reference_replacements':total},sort_keys=True))
