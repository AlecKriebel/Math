"""Own adjacent source authoring only; preserve V1 and all production inputs."""
from pathlib import Path
import json,hashlib,difflib,os,datetime as dt
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2];OLD=A/'acceptance_preparation_family'
def put(n,raw):
    p=H/n
    if p.exists():raise ValueError('Absent own output required: '+n)
    p.write_bytes(raw)
def obj(n,o):put(n,(json.dumps(o,indent=2,ensure_ascii=False)+'\n').encode())
def pin(p):
    raw=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def verify_closed(root,name):
    o=json.loads((root/name).read_bytes())
    for z in o['files']:
        p=root/z['path'];raw=p.read_bytes()
        if len(raw)!=z['bytes'] or hashlib.sha256(raw).hexdigest()!=z['sha256']:raise ValueError('Preserved old closure mismatch')
    if {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}!={z['path'] for z in o['files']}|{name}:raise ValueError('Preserved exact old closure mismatch')
    return o
old=verify_closed(OLD,'PREPARATION_MANIFEST.json');advroot=A/'acceptance_source_adversary_family';oldadv=verify_closed(advroot,'OWN_CLOSED_MANIFEST.json')
guard=(OLD/'pr42_guards.py').read_text()
old_loop="""    names=set()
    for z in foreign:
        keyset(z,{'path','bytes','sha256','classification'},'Whole individual foreign reference')
        require(type(z['path']) is str and z['path'].startswith(str(R)+'/'),'Whole foreign path must be exact absolute repository path')
        n=Path(z['path']).relative_to(R).as_posix();relative(n);require(n not in names,'Duplicate foreign row');names.add(n)
        p=regular(A,historical[n]) if n in historical and (A/'integration_preflight.json').exists() else regular(R,n)
        raw=p.read_bytes();require(type(z['bytes']) is int and len(raw)==z['bytes'] and sha(raw)==digest(z['sha256']),'Entire individually bound historical/current foreign input differs: '+n)
    require(NATIVE<=names,'Whole foreign native13 explicit rows required')"""
new_loop="""    literal_names=set();canonical_names=set()
    for z in foreign:
        keyset(z,{'path','bytes','sha256','classification'},'Whole individual foreign reference')
        require(type(z['path']) is str and z['path'] not in literal_names,'Duplicate literal foreign row identity')
        literal_names.add(z['path'])
        canonical=resolve_foreign_literal(z['path'])
        n=canonical.relative_to(R).as_posix();canonical_names.add(n)
        p=regular(A,historical[n]) if n in historical and (A/'integration_preflight.json').exists() else canonical
        raw=p.read_bytes();require(type(z['bytes']) is int and len(raw)==z['bytes'] and sha(raw)==digest(z['sha256']),'Entire individually bound historical/current foreign input differs: '+z['path'])
    require(len(literal_names)==925 and NATIVE<=canonical_names,'Exact925 literal identities and explicit canonical native13 required')"""
if guard.count(old_loop)!=1:raise ValueError('Unique exact old resolution source required')
guard=guard.replace(old_loop,new_loop)
resolver='''def resolve_foreign_literal(literal):
    """Preserve a literal archived row; resolve traversal with no symlink hops."""
    require(type(literal) is str and literal.startswith(str(R)+'/') and '\\\\' not in literal and '\\0' not in literal,'Exact absolute foreign reference inside repository required')
    require(R.is_dir() and not R.is_symlink() and R.resolve(strict=True)==R,'Regular canonical repository root required')
    for ancestor in R.parents:require(ancestor.is_dir() and not ancestor.is_symlink(),'Symlink repository ancestor prohibited')
    parts=literal[len(str(R))+1:].split('/')
    require(parts and all(part and part not in {'.git','__pycache__'} for part in parts),'Empty or private foreign reference component prohibited')
    current=R
    for i,part in enumerate(parts):
        require(current.is_dir() and not current.is_symlink(),'Every traversed foreign ancestor must be a real directory')
        if part=='.':continue
        if part=='..':
            require(current!=R,'Foreign traversal outside repository prohibited')
            current=current.parent
        else:current=current/part
        require(current.exists() and not current.is_symlink(),'Missing/symlink foreign traversal component prohibited')
        require(current==R or current.is_relative_to(R),'Every foreign traversal prefix must stay inside repository')
        if i<len(parts)-1:require(current.is_dir(),'Non-directory foreign traversal component')
    canonical=current.resolve(strict=True)
    require(canonical!=R and canonical.is_relative_to(R) and canonical==current,'Foreign canonical path must stay strictly inside repository')
    return regular(R,canonical.relative_to(R).as_posix())


'''
if guard.count('def basis(')!=1:raise ValueError('Unique common basis source required')
guard=guard.replace('def basis(',resolver+'def basis(',1)
put('pr42_guards.py',guard.encode())
for n in ['seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','SCIENTIFIC_SCOPE.json','CLOSED_WHOLE_RESULT_KEYS.json']:
    put(n,(OLD/n).read_bytes())
inputs=json.loads((OLD/'INPUT_BINDINGS.json').read_bytes())
inputs['root_capture_operator']=pin(A/'capture_root_final_operation_v2.py')
for root,mname,tag in [(OLD,'PREPARATION_MANIFEST.json','preserved_V1_preparation'),(advroot,'OWN_CLOSED_MANIFEST.json','preserved_V1_adversary')]:
    for p in sorted(x for x in root.rglob('*') if x.is_file()):inputs['pins'][tag+'/'+p.relative_to(root).as_posix()]=pin(p)
for n in ['ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json','ROOT_FINAL_PLAN.json','ROOT_ACCEPTANCE_PLAN_PRELAUNCH_SOURCE.py']:
    inputs['pins']['preserved_V1_actual_approval/'+n]=pin(A/n)
for p in sorted((A/'root_final_reconciliation_actual_capture').iterdir()):
    if p.is_file():inputs['pins']['preserved_V1_actual_failed_sealer/'+p.name]=pin(p)
obj('INPUT_BINDINGS.json',inputs)
obj('REPAIR_INPUTS.json',{'schema':'pr42-adjacent-foreign-reference-source-repair/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_author_pid':os.getpid(),'old_preparation_manifest':pin(OLD/'PREPARATION_MANIFEST.json'),'old_adversary_manifest':pin(advroot/'OWN_CLOSED_MANIFEST.json'),'retained_failed_capture':pin(A/'root_final_reconciliation_actual_capture/CAPTURE.json'),'new_ROOT_capture_operator':pin(A/'capture_root_final_operation_v2.py'),'repair':'Resolve each literal foreign row safely to canonical repository regular file; reject symlink traversal and escapes, retain literal duplicate identity guard, canonical native4 preimage selection, all925 individual hashes/count.','old_PASS_transferred_to_new_source_gate':False,'proposed_sources_imported_compiled_executed':False,'ROOT_v2_approval_authored':False,'current385_dependency517_whole25_925_unchanged':True})
delta=''.join(difflib.unified_diff((OLD/'pr42_guards.py').read_text().splitlines(True),guard.splitlines(True),fromfile='preserved_V1/pr42_guards.py',tofile='adjacent_V2/pr42_guards.py'))
put('SOURCE_REPAIR_DELTA.patch',delta.encode())
old_status=json.loads((OLD/'SOURCE_STATUS.json').read_bytes());old_status['source_preparation_complete']=None
obj('SOURCE_STATUS.json',old_status)
print(json.dumps({'status':'SOURCE_ONLY_ADJACENT_REPAIR_AUTHORED','actual_pid':os.getpid(),'preserved_V1_members':len(old['files']),'preserved_V1_adversary_members':len(oldadv['files']),'root_operator':inputs['root_capture_operator'],'proposed_sources_imported_compiled_executed':False,'native_Git_remote_people_mutations':False}))
