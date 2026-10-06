from pathlib import Path
import datetime, hashlib, json, os, subprocess
A=Path(__file__).resolve().parent
D=A/'fresh_disposition_adversary_20261006'
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
def require(value,label):
    if not value:raise ValueError(label)
def pin(path):
    require(path.is_file() and not path.is_symlink(),'regular file')
    body=path.read_bytes()
    return {'path':str(path.relative_to(A)),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
manifest_pin=pin(D/'OUTPUT_MANIFEST.json')
require(manifest_pin['sha256']=='9050b75dfd4a93cc9387c9d0f48312a795a2d6f39a39c116ec0c35f45d7589fb','fresh manifest')
members=[]
for item in json.loads((D/'OUTPUT_MANIFEST.json').read_text())['members']:
    require(Path(item['path']).name==item['path'],'flat member')
    actual=pin(D/item['path'])
    require(actual['bytes']==item['bytes'] and actual['sha256']==item['sha256'],'member mismatch')
    members.append(actual)
require(len(members)==10,'member count')
result=json.loads((D/'RESULT.json').read_text())
require(result['verdict'].startswith('PASS') and not result['mandatory_corrections_remaining']
    and result['closure_without_merge_or_solved_problem_publication_defensible']
    and not result['exact_prior_entire_R5_theorem_authenticated']
    and not result['substantive_research_novelty_established'],'fresh narrow clearance')
comment=pin(A/'PROPOSED_CLOSURE_COMMENT_20261006.md')
reasoning=pin(A/'ROOT_PRIORITY_DISPOSITION_20261006.md')
require(comment['sha256']=='6e61de512e9d00c125dfbd81888d67d1ccf72cd6702798ca0c384af8f1b905b0','reviewed comment changed')
require(reasoning['sha256']=='8cdaca5631650dde1ee47896c61563ba39d6f01760555f13c19cc25c74261137','reviewed disposition changed')
replays=[]
for optimized in (False,True):
    argv=[PY,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(D/'verify_disposition_controls.py')]
    child=subprocess.Popen(argv,cwd=A,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    require(child.returncode==0 and not err,'fresh control replay failure')
    replays.append({'PID':child.pid,'argv':argv,'exit_code':child.returncode,'stdout_sha256':hashlib.sha256(out).hexdigest(),'result':json.loads(out)})
record={'schema':'pr111-root-fresh-disposition-authentication/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'actual_operator_PID':os.getpid(),'manifest':manifest_pin,'members':members,'replays':replays,'result':result,
    'comment':comment,'reasoning':reasoning,'all_originals_and_priority_input_gate':'ROOT_PRIORITY_FAMILY_AUTHENTICATION_20261006.json',
    'PR_or_native_mutation':False}
(A/'ROOT_FRESH_DISPOSITION_AUTHENTICATION_20261006.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
ready={'schema':'pr111-root-source-scope-disposition-ready/v1','UTC':record['UTC'],'actual_operator_PID':os.getpid(),
    'PR':111,'problem_id':4900006,'original_head':'8a7270989d7064a4b97badecaa4b311db5e6d49f',
    'original_literal_status':'claimed_solved','original_budget':'2/5','new_central_proof_search_turns':0,
    'mathematical_clearance':True,'three_priority_families_authenticated':True,'fresh_cross_family_review_PASS':True,
    'fresh_disposition_review_PASS':True,'fresh_disposition_review':'draft_pr_publication_program_20260930/audits/pr111_4900006/fresh_disposition_adversary_20261006/REPORT.md',
    'fresh_disposition_review_sha256':pin(D/'REPORT.md')['sha256'],
    'narrow_classical_target_disposition_supported':True,'native_status_correction_supported':True,
    'proposed_native_status':'already_solved','classification_scope':result['already_solved_scope'],
    'stronger_R5_mathematics_valid':True,'stronger_R5_identical_prior_authenticated':False,
    'stronger_R5_substantive_novelty_established':False,'publication_authorization':False,
    'closing_comment_file':'PROPOSED_CLOSURE_COMMENT_20261006.md','closing_comment_sha256':comment['sha256'],
    'same_head_closure_pending':True,'native_correction_pending':True,'DOI':None,'Zenodo_actions':False,'tracker_actions':False,
    'PR_workflow_estimate_percent':75,'program_completed':18,'program_estimate_percent':18/99*100,'persistent_goal_status':'active'}
(A/'ROOT_DISPOSITION_READY_20261006.json').write_text(json.dumps(ready,indent=2,sort_keys=True)+'\n')
print(json.dumps(ready,sort_keys=True))
