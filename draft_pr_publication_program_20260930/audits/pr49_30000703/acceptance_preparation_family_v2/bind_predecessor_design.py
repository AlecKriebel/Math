"""Bind completed48V3 SOURCE design only; real48 native acceptance remains future."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat
F=Path(__file__).absolute().parent;A=F.parent;R=A.parents[2];V3=A.parent/'pr48_2961/acceptance_preparation_family_v3'
def need(q,m):
    if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def enc(q):return (json.dumps(q,sort_keys=True,indent=2)+'\n').encode()
def observed(p):
    need(not p.is_symlink() and all(not x.is_symlink() for x in p.parents) and stat.S_ISREG(p.lstat().st_mode),'Regular nonsymlink design file');b=p.read_bytes();return dict(path=str(p.relative_to(R)),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.lstat().st_mode))
def check(z):need(observed(R/z['path'])==z,'Complete fixed history member '+z['path'])
ready=load(V3/'FINAL_READY_CHECK.json');need(ready['status']=='READY_SOURCE_ONLY_WAIT_ROOT_CLOSURE_AND_NEW_ADVERSARY' and ready['production_imported_compiled_executed'] is False and ready['future_acceptance_approved'] is False and ready['actual_PR47_predecessor_completed'] is True,'Completed V3 design, no48 authority')
names=['capture_root_final_operation.py','close_source.py','verify_closed_source.py','ROOT_POST_CONTRACT.json','FINAL_READY_CHECK.json','REPORT.md','CHANGE_MAP.json','V2_M2_HISTORY_BINDINGS.json','ACTUAL47_PREDECESSOR_BINDINGS.json','pr48_guards.py','seal_final_evidence.py']
observations=[observed(V3/n) for n in names]
for n,z in ready['source_files'].items():
    row=observed(V3/n);need(row['bytes']==z['bytes'] and row['sha256']==z['sha256'],'Final V3 READY source anchors')
op=(V3/'capture_root_final_operation.py').read_text();close=(V3/'close_source.py').read_text();contract=load(V3/'ROOT_POST_CONTRACT.json')
need("script.parent == A / 'acceptance_preparation_family_v3' and script.name == 'seal_final_evidence.py'" in op and op.index('assert all(not parent.is_symlink()')<op.index('dest.mkdir('),'Exact completed V3 path before mutation')
need("'schema':'pr48-acceptance-source-closure/v3'" in close and "'self_excluded':[NAME]" in close and "'source_only':True,'proposed_helpers_imported_compiled_executed':False,'future_acceptance_or_ROOT_approval_claimed':False" in close,'Literal9key V3 source-only closer')
need(sha((V3/'ROOT_POST_CONTRACT.json').read_bytes())=='26f89f5ebf8444f96394ca5050c503920de1b9adb7417489241fcbe04885b410' and contract['schema']=='pr48-future-ROOT-whole-post-contract/v1' and len(contract['future48_required_ROOT_complete_keyset'])==22 and contract['source_only'] is True and contract['future_ROOT_post_completed'] is False,'Exact known future ROOT22 contract')
h=load(V3/'V2_M2_HISTORY_BINDINGS.json');need(h['previous_PASS_transferred'] is False and h['status']=='CLOSED_V2_AND_CLOSED_M2_ADVERSE_UNPROMOTED','Original history not promoted')
closed=[]
for n in ['superseded_V2','closed_M2_adverse']:
    closed.extend(h[n]['individual_closed_members']);closed.append(h[n]['manifest'])
closed.extend([h['report'],h['verdict']])
for q in h['actual_closure_and_readback_captures']:closed.extend(q['complete_members'])
unique={z['path']:z for z in closed}
for z in unique.values():check(z)
verdict=load(R/h['verdict']['path']);need(verdict==h['entire_M2_verdict'] and [x['id'] for x in verdict['mandatory_corrections']]==['M2'],'Entire closed adverse M2, no repaired-source approval')
result=dict(schema='pr49-v2-future48-completed-source-design-bindings/v1',utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_private_pid=os.getpid(),source_design_ready=True,design_source_body_bindings=[{k:v for k,v in z.items() if k!='full_mode'} for z in observations],dated_source_mode_observations=observations,source_modes_are_dated_preparation_or_ROOT_closure_epochs=True,allowed_later_literal_source_closure_mode=0o444,closed_history_fixed_bindings=list(unique.values()),entire_closed_M2_verdict=verdict,entire_future48_ROOT_contract=contract,expected48V3_closure_schema='pr48-acceptance-source-closure/v3',expected48V3_closure_exact_keys=['schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'],final48_source_ready_record={k:v for k,v in observed(V3/'FINAL_READY_CHECK.json').items() if k!='full_mode'},actual47_predecessor_completed_in_V3=True,actual48_acceptance_completed=False,actual48_ROOT_post_completed=False,new48_SOURCE_adversary_approval_transferred=False,production_imported_compiled_executed=False,future_acceptance_approved=False)
with (F/'PREDECESSOR_V3_DESIGN_BINDINGS.json').open('xb') as q:q.write(enc(result));q.flush();os.fsync(q.fileno())
ip=F/'INPUT_BINDINGS.json';before=ip.read_bytes()
with (F/'INPUT_BINDINGS_INITIAL_BEFORE_COMPLETED_DESIGN.json').open('xb') as q:q.write(before)
i=json.loads(before);i['future48_V3_design_final_read_completed']=True;i['completed_predecessor_source_design']=observed(F/'PREDECESSOR_V3_DESIGN_BINDINGS.json');i['known_predecessor_source_contract_design_only']['source_design_ready']=True
for z in unique.values():i['pins'][z['path']]=z
ip.write_bytes(enc(i))
with (F/'RESEARCH_LOG.md').open('ab') as q:q.write((result['utc']+' — Completed48V3 operator, literal9-key closer, ROOT22 contract and final SOURCE readiness read as text and bound by whole bytes. Closed48V2/M2 members and captures preserved in place; earlier source mode observations are dated, not immutable future permissions. Actual47 predecessor is recorded in48V3; actual48 acceptance/ROOTpost and new49 SOURCE/ROOT/fresh13 remain future. Narrow source controls35 positive/26 expected negatives/5 selected real mode replacements; final exact-parent symlink controls passed86740. Failure84412 and repair84652/author84655 retained. SOURCE preparation95%; discovery0%;49 acceptance0%.\n').encode())
print(json.dumps(dict(status='BOUND_COMPLETED_V3_SOURCE_DESIGN_ONLY',actual_pid=os.getpid(),design_members=len(observations),closed_history_fixed_members=len(unique),actual48_acceptance_completed=False,actual48_ROOT_post_completed=False,production_imported_compiled_executed=False)))
