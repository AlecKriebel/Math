"""Copy selected literal SOURCE bodies and perform only the reviewed V2 path/schema edits."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat
F=Path(__file__).absolute().parent;A=F.parent;R=A.parents[2];OLD=A/'acceptance_preparation_family'
SOURCES=['pr49_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py']
METADATA=['SCIENTIFIC_SCOPE.json','EXPECTED_ORIGINAL_LEDGER.json','EXPECTED_CURRENT_ADMIN.json','EXPECTED_NATIVE_TRANSITION.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json']
def need(q,m):
    if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(q):return (json.dumps(q,sort_keys=True,indent=2)+'\n').encode()
def put(n,b):
    with (F/n).open('xb') as q:q.write(b);q.flush();os.fsync(q.fileno())
def pin(p):
    need(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode),'Old regular file');b=p.read_bytes();return dict(path=str(p.relative_to(R)),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.lstat().st_mode))
def replace1(s,a,b):need(s.count(a)==1,'Unique reviewed edit: '+a[:60]);return s.replace(a,b,1)
now=dt.datetime.now(dt.timezone.utc).isoformat();oldrows=[]
for n in SOURCES+METADATA+['INPUT_BINDINGS.json','ROOT_POST_CONTRACT.json','SOURCE_CONTRACT.md','REPORT.md','READY.json','READINESS_CHECK.json','source_package_checks.py','close_source_ROOT_ONLY.py','verify_closed_source_ROOT_ONLY.py']:
    oldrows.append(pin(OLD/n))
# Preserve every original own payload in place with compact full-byte/full-mode rows, no body copies.
allold=[]
for p in sorted(OLD.rglob('*')):
    need(not p.is_symlink(),'Old symlink forbidden')
    if p.is_file():allold.append(pin(p))
put('ORIGINAL_UNCLOSED_FAMILY_BINDINGS.json',enc(dict(schema='pr49-v2-original-unclosed-family-bindings/v1',utc=now,source_family_closed=False,historical_READY_not_SOURCE_approval=True,modes_are_actual_unclosed_observations=True,files=allold,selected_source_and_contract_rows=oldrows)))
for n in METADATA:put(n,(OLD/n).read_bytes())
changes=[]
for n in SOURCES:
    raw=(OLD/n).read_bytes();s=raw.decode();edits=[]
    if n=='pr49_guards.py':
        for v in ['pr48','pr49']:
            base='v2' if v=='pr48' else 'v1';row="        '"+v+'-acceptance-source-closure/'+base+"':{'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'},"
            add=row.replace('/'+base,"/v3" if v=='pr48' else '/v2');s=replace1(s,row,row+'\n'+add);edits.append('Register '+v+('V3' if v=='pr48' else 'V2')+' exact nine-key closure schema')
        s=replace1(s,"if obj['schema'] in {'pr49-acceptance-source-closure/v1',","if obj['schema'] in {'pr49-acceptance-source-closure/v2','pr48-acceptance-source-closure/v3','pr49-acceptance-source-closure/v1',")
        s=replace1(s,"acceptance_preparation_family_v2/ROOT_POST_CONTRACT.json","acceptance_preparation_family_v3/ROOT_POST_CONTRACT.json")
        s=replace1(s,'Actual repaired48 V2 closure/contract required','Actual repaired48 V3 closure/contract required');s=replace1(s,'unfinished V2 never pins or readiness','unfinished V3 never pins or readiness')
        line="    manifest(cp.parent,'PREPARATION_MANIFEST.json',o['previous_preparation_manifest']['sha256'],frozen=True)"
        s=replace1(s,line,line+"\n    require(load(sm)['schema']=='pr48-acceptance-source-closure/v3','Exact repaired48 V3 predecessor schema; V1/V2 never transfer')")
        edits.append('Exact future48 V3 path and literal schema; future48 actual manifest and ROOT post remain required')
    if n=='capture_root_final_operation.py':
        s=replace1(s,"script.parent == A / 'acceptance_preparation_family'","script.parent == A / 'acceptance_preparation_family_v2'")
        old="    assert script.is_absolute() and script.is_file() and not script.is_symlink()"
        new=old+"\n    for ancestor in [script.parent,*script.parent.parents]:\n        assert not ancestor.is_symlink()\n        if ancestor==R:break\n    assert script.is_relative_to(R)"
        s=replace1(s,old,new);edits.append('Exact own V2 final sealer parent and nonsymlink ancestor chain before capture mutation')
    put(n,s.encode());changes.append(dict(path=n,before=pin(OLD/n),after=pin(F/n),edits=edits,identical=raw==s.encode()))
inputs=json.loads((OLD/'INPUT_BINDINGS.json').read_bytes());inputs['schema']='pr49-source-only-input-bindings/v2';inputs['known_predecessor_source_contract_design_only']['path']=inputs['known_predecessor_source_contract_design_only']['path'].replace('family_v2/','family_v3/');inputs['known_predecessor_source_contract_design_only']['readiness_transferred']=False;inputs['existing48SOURCE_M2_adverse_preserved_by_reference']=True;inputs['original49_unclosed_family']=pin(F/'ORIGINAL_UNCLOSED_FAMILY_BINDINGS.json');inputs['future48_V3_design_final_read_completed']=False;put('INPUT_BINDINGS.json',enc(inputs))
post=(OLD/'ROOT_POST_CONTRACT.json').read_text();post=replace1(post,'Actual repaired PR48 V2 closed SOURCE','Actual repaired PR48 V3 closed SOURCE');put('ROOT_POST_CONTRACT.json',post.encode())
contract=(OLD/'SOURCE_CONTRACT.md').read_text();contract=contract.replace('acceptance_preparation_family_v2/ROOT_POST_CONTRACT.json','acceptance_preparation_family_v3/ROOT_POST_CONTRACT.json').replace('PR48 V2','PR48 V3').replace('repaired48 V2','repaired48 V3').replace('PR49 SOURCE preparation','PR49 SOURCE V2 preparation');contract+='\n\nV2 custody correction: this family supersedes only the pending design of the original unclosed49 family. Exact future48 V3 nine-key closure schema and path are required; both current49 V2 and future48 V3 source closures remain separate actual ROOT operations. The final operator requires its sealer in acceptance_preparation_family_v2, with nonsymlink ancestors. Original49 whole approval stays WHOLE-only. No future48 acceptance or repaired49 SOURCE approval is supplied here. All six bodies are read only as text during this preparation.\n';put('SOURCE_CONTRACT.md',contract.encode())
put('CHANGE_MAP.json',enc(dict(schema='pr49-narrow-source-v2-change-map/v1',utc=now,changes=changes,unchanged_four_helpers=[q['path'] for q in changes if q['identical']],write_and_fresh_check_preserved_identically=True,scientific_metadata_unchanged=True,future48_approval_created=False,production_imported_compiled_executed=False)))
put('RESEARCH_LOG.md',('# PR49 SOURCE V2 preparation\n\n'+now+' — Narrow source path/schema repair. Original unclosed49 preserved with complete body/mode rows in place. Four helpers and all scientific/draft/native-transition bodies copied unchanged. Guard edits only register49V2/48V3 and require exact future48V3; final operator uses exact ownV2 parent and nonsymlink ancestors. Production source read only as text. Mechanism: literal replacements; evidence: actual author capture plus CHANGE_MAP; status: awaiting final48V3 design read and independent private controls. Gap: actual48 acceptance and all49 SOURCE/ROOT/fresh native13/acceptance gates remain future. SOURCE preparation estimate75%; mathematical discovery0%; actual49 acceptance0%.\n').encode())
print(json.dumps(dict(status='AUTHORED_SOURCE_V2_ONLY',actual_pid=os.getpid(),six_source_changes=changes,original_unclosed_family_files_bound=len(allold),production_imported_compiled_executed=False,future_acceptance_approved=False)))
