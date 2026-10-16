"""Final repair custody recheck and separate terminal seal; no candidate edit."""
from pathlib import Path
import datetime, hashlib, json
R=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1094_2100509/repairs/package01')
A=R.parent.parent;P=A/'preprint_v1_0';K=P/'kit'
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def writej(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def row(p,n):
    b=p.read_bytes();return {'path':n,'bytes':len(b),'sha256':sha(b)}
def main():
    baseline=json.loads((R/'FROZEN_INPUT_PINS.json').read_text())['records']
    inputs={r['path']:r for r in baseline}
    changes={r['path']:r for r in json.loads((R/'INPUT_PRESERVATION.json').read_text())['allowed_changes']}
    preserved=[]
    for r in baseline:
        p=A/r['path'];actual=row(p,r['path'])
        need({k:actual[k] for k in ('bytes','sha256')}==(changes[r['path']]['after'] if r['path'] in changes else {k:r[k] for k in ('bytes','sha256')}),'unexpected live input change '+r['path'])
        source=R/'before'/r['path'] if r['path'] in changes else p
        need(row(source,r['path'])==r,'unresolved before input '+r['path'])
        preserved.append({'path':r['path'],'resolution':'before/'+r['path'] if r['path'] in changes else 'unchanged_live','bytes':r['bytes'],'sha256':r['sha256']})
    current=json.loads((R/'CURRENT_ARTIFACT_PINS.json').read_text())['records']
    for r in current:need(row(A/r['path'],r['path'])==r,'current artifact changed '+r['path'])
    custody=json.loads((K/'CUSTODY_MAP.json').read_text())
    origins=[]
    for r in custody['copies']:
        name=r['original_path'];origins.append(name);expected=inputs[name]
        need(r['bytes']==expected['bytes'] and r['sha256']==expected['sha256'],'copy origin pin differs '+name)
        need(row(K/r['copy_path'],name)==expected,'selected historical copy differs '+name)
    for r in custody['exclusions']:
        name=r['path'];origins.append(name);expected=inputs[name]
        need(r['bytes']==expected['bytes'] and r['sha256']==expected['sha256'],'exclusion differs '+name)
    need(len(origins)==len(set(origins))==custody['exact_partition_count']==len(inputs) and set(origins)==set(inputs),'custody exact partition')
    stages=json.loads((R/'PRIOR_STAGE_RESOLUTION.json').read_text())['stages'];stage_count=0
    for stage in stages:
        need(sha((A/stage['inventory']).read_bytes())==stage['inventory_sha256'],'dated inventory changed')
        for r in stage['records']:
            need(row(A/r['resolution'],r['path'])=={k:r[k] for k in ('path','bytes','sha256')},'dated row differs')
            stage_count+=1
    metadata=json.loads((K/'.zenodo.json').read_text())
    need(json.loads((K/'metadata.json').read_text())==metadata,'bare metadata differs')
    need(json.loads((K/'metadata_api.json').read_text())=={'metadata':metadata},'API metadata differs')
    need(json.loads((P/'zenodo-deposit.json').read_text())['metadata']==metadata,'native metadata differs')
    need(json.loads((P/'DEPOSIT_BINDING.json').read_text())['metadata']==metadata==json.loads((R/'before/preprint_v1_0/DEPOSIT_BINDING.json').read_text())['metadata'],'metadata changed since before repair')
    need(sha((P/'paper.pdf').read_bytes())=='a1e2da77dd739bcc7ddc4dd8ba916c99010450e4224ae7a52d01d34c98960e72','paper changed')
    need((P/'paper.pdf').read_bytes()==(K/'paper.pdf').read_bytes(),'PDF aliases differ')
    v=json.loads((R/'VALIDATION.json').read_text());s=json.loads((R/'CASE_DIRECTION_SUPPLEMENT.json').read_text())
    need(v['status']==s['status']=='PASS' and v['command_count']==127 and s['command_count']==12,'final command evidence absent')
    need(not (R/'tmp').exists(),'own scratch remains')
    writej(R/'FINAL_CUSTODY_RECHECK.json',{'utc':now(),'status':'PASS','baseline_count':len(baseline),'allowed_existing_edits':len(changes),'unchanged_count':len(baseline)-len(changes),'resolved_before_records':preserved,'current_artifacts_rehashed':len(current),'exact_selected_copies_rehashed':len(custody['copies']),'individual_exclusions':len(custody['exclusions']),'stage_inventory_rows_resolved':stage_count,'proof_PDF_all_native_metadata_unchanged':True})
    writej(R/'FINAL_STATUS.json',{'utc':now(),'status':'BOUNDED_P3_REPAIR_COMPLETE_PENDING_ROOT_AND_NEW_COMPLETE_WHOLE02','pr':1094,'head_oid':'954dd70b49458026e29b8dae63243391249008d8','completed_new_whole_reviews':1,'minimum_new_whole_reviews':2,'new_complete_review_required':True,'publication_ready':False,'published':False,'ordered_services_hold_pr':1032,'full_result_and_method_priority':'UNKNOWN','commands':139,'expected_nonzero_outcomes':128,'proof_PDF_metadata_unchanged':True,'services_performed':False,'git_mutations':False,'new_compile_or_render':False,'assignment_completion_percent':100})
    outputs=[row(p,p.relative_to(R).as_posix()) for p in sorted(R.rglob('*')) if p.is_file() and not p.is_symlink() and p.name not in ('OUTPUT_PINS.json','SEAL.json') and 'tmp' not in p.relative_to(R).parts]
    writej(R/'OUTPUT_PINS.json',{'utc':now(),'scope':'Every retained regular repair output, including exact before bytes and own code; this inventory and separate seal excluded only to avoid self-reference. No scratch or third-party body added.','records':outputs})
    seal={'utc':now(),'status':'COMPLETE_BOUNDED_REPAIR_PENDING_ROOT_AND_NEW_COMPLETE_WHOLE_REVIEW','pr':1094,'head_oid':'954dd70b49458026e29b8dae63243391249008d8','output_count':len(outputs),'output_pins_sha256':sha((R/'OUTPUT_PINS.json').read_bytes()),'baseline_inputs':len(baseline),'unchanged_inputs':len(baseline)-len(changes),'allowed_existing_edits':len(changes),'exact_selected_copies':len(custody['copies']),'individual_exclusions':len(custody['exclusions']),'prior_stage_rows_resolved':stage_count,'commands':139,'expected_nonzero_outcomes':128,'whole_reviews_completed':1,'minimum_whole_reviews':2,'new_complete_whole_review_required':True,'publication_ready':False,'published':False,'ordered_services_hold_pr':1032,'support_zip':row(P/'pr1094_supportkit_v1.0.zip','pr1094_supportkit_v1.0.zip'),'paper_PDF_and_native_metadata_unchanged':True,'services_performed':False,'git_mutations':False,'outside_communication':False,'new_compile_or_render':False,'completion_percent_of_assigned_repair':100}
    writej(R/'SEAL.json',seal)
    for r in outputs:need(row(R/r['path'],r['path'])==r,'sealed output mismatch')
    print(json.dumps(seal,indent=2))
if __name__=='__main__':main()
