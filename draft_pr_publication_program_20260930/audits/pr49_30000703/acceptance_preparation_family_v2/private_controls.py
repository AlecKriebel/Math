"""Independent bounded path/schema/full-mode models; read production text, never execute it."""
from pathlib import Path
import copy,datetime as dt,hashlib,json,os,stat
F=Path(__file__).absolute().parent;A=F.parent;OLD=A/'acceptance_preparation_family'
SOURCES=['pr49_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py']
def need(q,m):
    if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def eq(a,b):return type(a) is type(b) and (a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
checks=[];neg=[]
def positive(label,p):need(p,label);checks.append(label)
def negative(label,f):
    try:f()
    except (ValueError,OSError):neg.append(label)
    else:raise ValueError('Accepted mutant '+label)
def block(s,name):
    p=s.index('\ndef '+name+'(');q=s.find('\ndef ',p+1);return s[p:q if q>=0 else len(s)]
texts={n:(F/n).read_text() for n in SOURCES};old={n:(OLD/n).read_text() for n in SOURCES}
for n in SOURCES[1:5]:positive('unchanged_full_helper_'+n,texts[n]==old[n])
for n in ['write','fresh_check','native_modes','foreign_capture','foreign_check','owned_log_append_check']:
    positive('unchanged_guard_function_'+n,block(texts[SOURCES[0]],n)==block(old[SOURCES[0]],n))
guard=texts['pr49_guards.py'];operator=texts['capture_root_final_operation.py']
positive('registered49V2_exact9key',"'pr49-acceptance-source-closure/v2':{'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'}" in guard)
positive('registered48V3_exact9key',"'pr48-acceptance-source-closure/v3':{'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'}" in guard)
positive('required_literal48V3',"require(load(sm)['schema']=='pr48-acceptance-source-closure/v3'" in guard)
positive('exact_future48V3_contract_path',"cp==p48/'acceptance_preparation_family_v3/ROOT_POST_CONTRACT.json'" in guard)
positive('own49V2_final_operator_path',"script.parent == A / 'acceptance_preparation_family_v2' and script.name == 'seal_final_evidence.py'" in operator)
positive('ancestors_checked_before_destination_mutation',operator.index('assert not ancestor.is_symlink()')<operator.index('dest.mkdir('))
q=json.loads((F/'ROOT_POST_CONTRACT.json').read_bytes());positive('22_future_ROOT_keys',len(q['future49_required_ROOT_complete_keyset'])==22)
positive('future_ROOT_post_false',q['future_ROOT_post_completed'] is False and q['predecessor']['actually_completed'] is False)
for n in ['SCIENTIFIC_SCOPE.json','EXPECTED_ORIGINAL_LEDGER.json','EXPECTED_CURRENT_ADMIN.json','EXPECTED_NATIVE_TRANSITION.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json']:
    positive('unchanged_metadata_'+n,(F/n).read_bytes()==(OLD/n).read_bytes())
# Genuine private files; these are not native or final publication directories.
base=F/'private_model_fixtures_v2';base.mkdir();right=base/'acceptance_preparation_family_v2';right.mkdir();candidate=right/'seal_final_evidence.py';candidate.write_bytes(b'PRIVATE TEXT ONLY\n')
wrong=base/'acceptance_preparation_family';wrong.mkdir();(wrong/'seal_final_evidence.py').write_bytes(b'PRIVATE TEXT ONLY\n')
def path_gate(p,root):
    need(p.is_absolute() and p.parent==root/'acceptance_preparation_family_v2' and p.name=='seal_final_evidence.py','Exact own V2 sealer')
    need(p.is_file() and not p.is_symlink(),'Regular literal sealer')
    for v in [p.parent,*p.parent.parents]:
        need(not v.is_symlink(),'Nonsymlink ancestor')
        if v==root:break
    need(p.is_relative_to(root),'Under root')
path_gate(candidate,base);positive('actual_private_ownV2_path_model',True)
negative('old49_family_rejected',lambda:path_gate(wrong/'seal_final_evidence.py',base))
negative('wrong_name_rejected',lambda:path_gate(right/'verify_post_acceptance.py',base))
saved=right/'regular_source_retained.py';candidate.rename(saved);candidate.symlink_to(saved)
negative('symlink_leaf_rejected',lambda:path_gate(candidate,base));candidate.unlink();saved.rename(candidate)
alternate_root=base/'alternate_root';alternate_root.mkdir();ancestor_alias=alternate_root/'acceptance_preparation_family_v2';ancestor_alias.symlink_to(right,target_is_directory=True)
negative('symlink_ancestor_rejected',lambda:path_gate(ancestor_alias/'seal_final_evidence.py',alternate_root));ancestor_alias.unlink();(alternate_root/'retained_control.bin').write_bytes(b'PRIVATE ANCESTOR CONTROL COMPLETED\n')
negative('relative_path_rejected',lambda:path_gate(Path('seal_final_evidence.py'),base))
K={'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'}
model=dict(schema='pr48-acceptance-source-closure/v3',status='CLOSED_SOURCE_ONLY',utc='2026-10-03T00:00:00+00:00',self_excluded=['PREPARATION_MANIFEST.json'],files_count=0,files=[],source_only=True,proposed_helpers_imported_compiled_executed=False,future_acceptance_or_ROOT_approval_claimed=False)
def schema_gate(o):
    need(type(o) is dict and set(o)==K,'Exact9key closure');need(o['schema']=='pr48-acceptance-source-closure/v3' and o['status']=='CLOSED_SOURCE_ONLY','Exact48V3 literal')
    need(type(o['files_count']) is int and o['files_count']==len(o['files']),'Typed count');need(o['source_only'] is True and o['proposed_helpers_imported_compiled_executed'] is False and o['future_acceptance_or_ROOT_approval_claimed'] is False,'No future authority');need(eq(o['self_excluded'],['PREPARATION_MANIFEST.json']),'Self only')
schema_gate(model);positive('independent48V3_schema_model',True)
for label,key,val in [('oldV1_schema','schema','pr48-acceptance-source-closure/v1'),('oldV2_schema','schema','pr48-acceptance-source-closure/v2'),('bool_count','files_count',False),('future_approval','future_acceptance_or_ROOT_approval_claimed',True),('numeric_false','proposed_helpers_imported_compiled_executed',0),('extra_exclusion','self_excluded',['PREPARATION_MANIFEST.json','other'])]:
    m=copy.deepcopy(model);m[key]=val;negative(label,lambda m=m:schema_gate(m))
m=copy.deepcopy(model);m['extra']=False;negative('extra_schema_key',lambda:schema_gate(m))
# Descriptor based independent write model; source guard itself remains unexecuted.
modes=[]
for mode in [0o600,0o644,0o1600,0o2600,0o4600]:
    p=base/('mode_'+oct(mode)+'.bin');p.write_bytes(b'before\n');p.chmod(mode);before=stat.S_IMODE(p.lstat().st_mode);t=base/(p.name+'.tmp')
    fd=os.open(t,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    try:os.write(fd,b'after\n');os.fchmod(fd,before);os.fsync(fd)
    finally:os.close(fd)
    os.replace(t,p);after=stat.S_IMODE(p.lstat().st_mode);positive('independent_actual_mode_'+oct(mode),before==mode==after and p.read_bytes()==b'after\n');modes.append(dict(path=str(p.relative_to(F)),requested_mode=mode,before_mode=before,after_mode=after))
rows=[dict(path='native'+str(i),body='before',mode=0o600 if i<4 else 0o644) for i in range(13)];allowed={'native'+str(i) for i in range(4)}
def mode_gate(observed):
    need(len(observed)==13 and {z['path'] for z in observed}=={z['path'] for z in rows},'Exact13paths')
    for expected,z in zip(rows,observed):
        need(type(z['mode']) is int and z['mode']==expected['mode'],'All13 modes always')
        if z['path'] not in allowed:need(z['body']==expected['body'],'Protected bytes')
o=copy.deepcopy(rows)
for z in o:
    if z['path'] in allowed:z['body']='allowed-after'
mode_gate(o);positive('13mode_model_allowed_body_paths',True)
for i in range(13):
    m=copy.deepcopy(o);m[i]['mode']^=0o100;negative('changed_full_mode_'+str(i),lambda m=m:mode_gate(m))
m=copy.deepcopy(o);m[0]['mode']=False;negative('bool_mode_rejected',lambda:mode_gate(m))
out=dict(schema='pr49-v2-private-bounded-controls/v1',status='PASS_PRIVATE_SOURCE_ONLY',actual_pid=os.getpid(),utc=dt.datetime.now(dt.timezone.utc).isoformat(),checks=checks,expected_negative_controls=neg,selected_actual_mode_controls=modes,six_source_bindings={n:dict(bytes=len((F/n).read_bytes()),sha256=sha((F/n).read_bytes())) for n in SOURCES},production_imported_compiled_executed=False,formal_or_mathematical_certificate=False,native_index_remote_write=False,ROOT_approval_created=False,future_acceptance_approved=False)
with (F/'FINAL_PRIVATE_CONTROLS_RESULT.json').open('x') as q:json.dump(out,q,indent=2,sort_keys=True);q.write('\n')
print(json.dumps(out))
