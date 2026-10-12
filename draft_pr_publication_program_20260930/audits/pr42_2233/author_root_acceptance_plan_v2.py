"""Genuine ROOT V2 approval after personal reading and actual independent closure check.

V1 approval and actual failure remain immutable. This does not execute production.
"""
from pathlib import Path
import copy, datetime as dt, hashlib, json, os, stat, subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];H=A/'acceptance_preparation_family_v2';S=A/'acceptance_v2_source_adversary_family'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
    assert p.is_file() and not p.is_symlink() and all(not q.is_symlink()for q in p.parents)
    b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def check(z):assert pin(R/z['path'])=={k:z[k]for k in ['path','bytes','sha256']}
def write(name,j):
    with (A/name).open('x')as f:json.dump(j,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def main():
    assert __debug__
    (A/'ROOT_ACCEPTANCE_PLAN_PRELAUNCH_SOURCE_V2.py').write_bytes(Path(__file__).read_bytes())
    assert subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main'
    assert subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R)==b''
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
    prep=pin(H/'PREPARATION_MANIFEST.json');assert prep['sha256']=='f5cd2d41d448c97fcf160afeca63dc4c57c283deb03ffa4fe2292125db06b1a8'
    adv=pin(S/'OWN_CLOSED_MANIFEST.json');assert adv['sha256']=='7d34755d82033bd96c08083f4575406b419d1788c6a7fc3fff3f3dc0d099a5f6'
    for d,n in [(H,'PREPARATION_MANIFEST.json'),(S,'OWN_CLOSED_MANIFEST.json')]:
        m=load(d/n)
        for z in m['files']:
            q=d/z['path'];b=q.read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256'] and stat.S_IMODE(q.stat().st_mode)==0o444
        assert stat.S_IMODE((d/n).stat().st_mode)==0o444
    inspection=load(A/'ROOT_ACCEPTANCE_V2_SOURCE_INSPECTION.json')
    assert inspection['actual_pid']==23869 and inspection['status']=='PASS_ROOT_PERSONAL_V2_SOURCE_AND_CLOSED_EVIDENCE_INSPECTION'
    for k in ['personal_original_production_full_read_completed','personal_complete_V2_delta_contract_inputs_controls_read_completed','personal_new_different_report_and_verdict_full_read_completed']:assert inspection[k]is True
    verdict=load(S/'VERDICT.json');assert verdict==inspection['complete_new_VERDICT'] and verdict['mandatory_defects']==verdict['mandatory_corrections']==[]
    assert verdict['future_runtime_or_acceptance_certified']is False
    inp=load(H/'INPUT_BINDINGS.json')
    for z in inp['pins'].values():check(z)
    for k in ['closed_whole_manifest','closed_whole_result','closed_whole_report','closed_root_whole_inspection','root_capture_operator']:check(inp[k])
    assert inp['root_capture_operator']['sha256']=='48e5e5ccbd68ddbc4dc6c661a306003902dfb856a3bcdb0061278cb51749e5c2'
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    approved=copy.deepcopy(load(H/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json'))
    approved.update(status='ROOT_APPROVED_CLOSED_WHOLE_EVIDENCE',created_utc=now,root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,whole_manifest=inp['closed_whole_manifest'],root_whole_inspection=inp['closed_root_whole_inspection'],root_capture_operator=inp['root_capture_operator'])
    write('ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS_V2.json',approved);bound=pin(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS_V2.json')
    refs=list(inp['pins'].values())+[pin(A/'reviewed_candidate/MANIFEST.json'),pin(A/'reviewed_candidate/CURRENT_DEPENDENCIES.json'),inp['closed_whole_manifest'],inp['closed_whole_result'],inp['closed_whole_report'],inp['closed_root_whole_inspection'],inp['root_capture_operator'],bound]
    assert len(refs)==len(inp['pins'])+8==len({z['path']for z in refs})
    plan=copy.deepcopy(load(H/'DRAFT_FINAL_PLAN.json'))
    plan.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',partial_valid=True,preparation_manifest_sha256=prep['sha256'],root_bindings=bound['path'],root_bindings_sha256=bound['sha256'],whole_manifest_sha256=inp['closed_whole_manifest']['sha256'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,immutable_evidence_references=sorted(refs,key=lambda z:z['path']))
    write('ROOT_FINAL_PLAN_V2.json',plan)
    native=[]
    for z in load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')['files']:
        q=R/z['path'];native.append({**pin(q),'worktree_mode':stat.S_IMODE(q.stat().st_mode)})
    assert len(native)==len({z['path']for z in native})==13
    fresh={'schema':'pr42-root-fresh-acceptance-input-preimages/v1','approved_by_root':True,'created_utc':now,'reason_date_utc':now[:10],'reason':'ROOT completed the repaired V2 source reading, newly closed different adversary and genuine23869 full evidence inspection; latest-main actual native13 are fresh acceptance authority. V1 failure and c61 historical inputs remain dated evidence only.','current_head':head,'files':native}
    write('ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V2.json',fresh)
    result={'schema':'pr42-root-genuine-repaired-source-approval/v1','status':'PASS_ROOT_COMPLETED_V2_SOURCE_APPROVAL','utc':now,'actual_pid':os.getpid(),'new_different_source_manifest':adv,'entire_new_different_VERDICT':verdict,'genuine_complete_ROOT_inspection':pin(A/'ROOT_ACCEPTANCE_V2_SOURCE_INSPECTION.json'),'bindings':bound,'plan':pin(A/'ROOT_FINAL_PLAN_V2.json'),'fresh13':pin(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V2.json'),'actual_main':head,'refs':len(refs),'V1_records_unchanged':True,'future_runtime_or_merge_certified':False}
    write('ROOT_ACCEPTANCE_V2_APPROVAL.json',result)
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==head
    print(json.dumps({k:v for k,v in result.items()if k!='entire_new_different_VERDICT'}))
if __name__=='__main__':main()
