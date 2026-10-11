"""Narrow adjacent source repair of two independently reported runtime defects."""
from pathlib import Path,PurePosixPath
import hashlib,json,datetime,os,stat,difflib
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2];V1=A/'acceptance_preparation_family'
sha=lambda b:hashlib.sha256(b).hexdigest();stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def pin(p):
    b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def put(n,b):
    p=H/n;require(not p.exists(),'Absent own output '+n);p.write_bytes(b)
def dump(n,o):put(n,(json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
raw=(V1/'PREPARATION_MANIFEST.json').read_bytes();require(sha(raw)=='4161032794d175f8e0cfc3b62b3d1567f172ca93abe590f43ef81576d6cd20f9','Literal preserved V1 closure')
mf=json.loads(raw);require(mf['files_count']==len(mf['files'])==108 and mf['self_excluded']==['PREPARATION_MANIFEST.json'],'108+self V1')
names={z['path'] for z in mf['files']}|{'PREPARATION_MANIFEST.json'}
require({p.relative_to(V1).as_posix() for p in V1.rglob('*') if p.is_file()}==names,'Whole exact preserved V1 file set')
source_refs=[]
for z in mf['files']:
    p=V1/z['path'];b=p.read_bytes();require(len(b)==z['bytes'] and sha(b)==z['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'Entire preserved V1 input')
    source_refs.append({**pin(p),'historical_classification':'Preserved closed V1 source/prelaunch/control/failure evidence; not a new V2 PASS.'})
source_refs.append({**pin(V1/'PREPARATION_MANIFEST.json'),'historical_classification':'Only V1 literal manifest self; preserved immutable old closure.'})
production=['pr43_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py'];deltas=[];patch=[]
replacements={'integrate_reviewed_partial.py':("g.load(g.A/'snapshot_manifest_v2.json')","g.load(g.A/'snapshot_manifest.json')"),'state_mirror_reconciliation.py':("scope='Incremental present accepted primary PR43; source-status correction; original0/5, no new proof turn or historical reconstruction.'","scope='Incremental present accepted primary PR43 source-status correction; original0/5, no new proof turn or historical reconstruction.'")}
for n in production:
    before=(V1/n).read_bytes();after=before
    if n in replacements:
        old,new=replacements[n];require(before.decode().count(old)==1,'Unique old defect token '+n);after=before.decode().replace(old,new,1).encode()
        patch+=list(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True),fromfile='preserved_V1/'+n,tofile='adjacent_V2/'+n))
    put(n,after);deltas.append({'path':n,'before':pin(V1/n),'after':pin(H/n),'changed':before!=after})
for n in ['DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json','SCIENTIFIC_SCOPE.json','EXPECTED_CURRENT_ADMIN.json','EXPECTED_WHOLE_VERDICT.json','EXPECTED_ROOT_WHOLE_REVIEW.json']:
    put(n,(V1/n).read_bytes())
old_operator=A/'capture_root_final_operation.py';new_operator=A/'capture_root_final_operation_v2.py'
require(sha(old_operator.read_bytes())=='0da8951ebcbbe8e410e2390d838a76e95da9a1d9df7dd7f61ba39f93a86a5ecf','Actual unchanged V1 ROOT operator')
require(sha(new_operator.read_bytes())=='9376c9c2d972f3ae4950ddb6b46300c2cd1cc36db89bc6ced6627fe8801e71a4','Actual separately ROOT-authored V2 operator')
require(new_operator.read_bytes()==old_operator.read_bytes().replace(b"A / 'acceptance_preparation_family'",b"A / 'acceptance_preparation_family_v2'",1),'Only actual permitted-parent ROOT source delta')
inp=json.loads((V1/'INPUT_BINDINGS.json').read_bytes());inp['pins'].pop('capture_root_final_operation.py');inp['pins']['capture_root_final_operation_v2.py']=pin(new_operator);inp['root_capture_operator']=pin(new_operator);dump('INPUT_BINDINGS.json',inp)
status=json.loads((V1/'SOURCE_STATUS.json').read_bytes());status['source_preparation_complete']=None;status['own_control_demands']=None;status['independent_acceptance_source_verdict']=None
status.update(adjacent_V2_repairs_pending_NEW_different_source_audit=True,V1_source_review_PASS_transferred=False,future_ROOT_or_acceptance_approval_claimed=False);dump('SOURCE_STATUS.json',status)
prefix='''# V2 two-defect source repair, preserving V1\n\nThe independent V1 source audit identified two mandatory runtime defects:\nnonexistent snapshot_manifest_v2.json in the overlay phase, and a semicolon\nmismatch between the mirror writer scope and the guard's exact expected scope.\nThis separate family changes exactly those two tokens in production. All other\nproduction sources, scientific scope, expected science/whole objects and draft\nROOT approval/final plan bytes are unchanged. The original108+self closure\n4161032794d175f8e0cfc3b62b3d1567f172ca93abe590f43ef81576d6cd20f9,\nall initial failures and old controls are preserved at their original paths and\nindividually pinned in V1_SOURCE_REFERENCES.json. Their old successful finite\nchecks are not a clean acceptance-source verdict for V2. The independent V1\nsource review was still being completed when repair was requested; no unfinished\nreport or fabricated PASS is promoted. A new different V2 adversary is required.\n\nROOT separately authored the actual V2 five-member operator5113B, SHA256\n9376c9c2d972f3ae4950ddb6b46300c2cd1cc36db89bc6ced6627fe8801e71a4,\nwith only its allowed family parent changed. This is source, not ROOT approval\nor a future runtime success. INPUT_BINDINGS updates exactly its two operator\nreferences. All three required actualPR42 predecessor draft references remain\nnull, and all future ROOT read flags remain false until genuine completion.\n\n'''
contract=(V1/'CONTRACT.md').read_text().replace('A43/capture_root_final_operation.py','A43/capture_root_final_operation_v2.py').replace('0da8951ebcbbe8e410e2390d838a76e95da9a1d9df7dd7f61ba39f93a86a5ecf','9376c9c2d972f3ae4950ddb6b46300c2cd1cc36db89bc6ced6627fe8801e71a4')
put('CONTRACT.md',(prefix+contract).encode());put('SOURCE_REPAIR_DELTA.patch',''.join(patch).encode())
dump('V1_SOURCE_REFERENCES.json',{'schema':'pr43-preserved-entire-V1-source-references/v1','created_utc':stamp(),'manifest':pin(V1/'PREPARATION_MANIFEST.json'),'files_count_including_literal_self':109,'files':source_refs,'copied_foreign_primary_bodies':[],'old_source_PASS_transferred':False})
record={'schema':'pr43-adjacent-two-token-source-repair/v2','created_utc':stamp(),'actual_author_pid':os.getpid(),'original_closed_source_manifest':pin(V1/'PREPARATION_MANIFEST.json'),'production_delta':deltas,'unchanged_science_and_drafts':[pin(H/n) for n in ['DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json','SCIENTIFIC_SCOPE.json','EXPECTED_CURRENT_ADMIN.json','EXPECTED_WHOLE_VERDICT.json','EXPECTED_ROOT_WHOLE_REVIEW.json']],'actual_ROOT_V2_operator':pin(new_operator),'ROOT_source_approval_authored':False,'V1_source_PASS_transferred':False,'proposed_helpers_imported_compiled_executed':False,'future_PR42_completion_certified':False,'new_substantive_attempts':0,'audit_turns':0};dump('REPAIR_RESULT.json',record)
put('RESEARCH_LOG.md',('# PR43 adjacent acceptance source repair\n\n## '+stamp()+' — Narrow independent-audit repair\n\nPreparation65%; newdiscovery0%; original0/5,new0,audit0. Actual own author\nPID'+str(os.getpid())+' retained the complete109 V1 source file references, fixed\nexactly the two independent reported production defects, and bound the actual\nseparately authored ROOT V2 operator. All other production/science/draft bytes\nremain exact. No proposed helper import, bytecode compilation or execution; no\nnative, index, Git, branch, remote or external-human action. All future approval\nflags and PR42 predecessor references stay false/null. New different review\nremains mandatory.\n').encode())
print(json.dumps({'status':'SOURCE_ONLY_TWO_TOKEN_REPAIR_AUTHORED','actual_author_pid':os.getpid(),'changed_production_files':[z['path'] for z in deltas if z['changed']],'genuine_ROOT_operator_sha256':pin(new_operator)['sha256'],'future_approval_claimed':False}))
