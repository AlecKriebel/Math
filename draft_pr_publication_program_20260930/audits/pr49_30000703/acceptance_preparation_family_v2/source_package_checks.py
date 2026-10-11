"""Own SOURCE read/closure predicates. Proposed production files are always read as bytes only."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,math,os,stat
F=Path(__file__).absolute().parent;A=F.parent;R=A.parents[2];NAME='PREPARATION_MANIFEST.json'
SOURCES=['pr49_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py']
def need(q,m):
    if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(v):
        d={}
        for k,x in v:need(k not in d,'Duplicate JSON key');d[k]=x
        return d
    def floating(s):v=float(s);need(math.isfinite(v),'Nonfinite JSON number');return v
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def load(p):return parse(Path(p).read_bytes())
def eq(a,b):return type(a) is type(b) and (a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
def regular(p):
    p=Path(p);need(p.is_relative_to(R),'Repository bound regular path')
    for x in [p,*p.parents]:need(not x.is_symlink(),'No symlink path or ancestor')
    need(stat.S_ISREG(p.lstat().st_mode),'Regular file');return p
def observed(p):
    p=regular(p);b=p.read_bytes();return dict(path=str(p.relative_to(R)),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.lstat().st_mode))
def check(z):need(eq(observed(R/z['path']),z),'Full fixed body/mode changed: '+z['path'])
def body_check(z):
    q=observed(R/z['path']);need(eq({k:v for k,v in q.items() if k!='full_mode'},z),'Full design body changed: '+z['path'])
def topology():
    need(F.is_dir() and not F.is_symlink(),'Regular family root');files={};dirs=set()
    for root,ds,fs in os.walk(F,followlinks=False):
        for n in ds:
            p=Path(root)/n;need(not p.is_symlink() and stat.S_ISDIR(p.lstat().st_mode),'No special/symlink directory');dirs.add(p.relative_to(F).as_posix())
        for n in fs:
            p=Path(root)/n;regular(p);name=p.relative_to(F).as_posix();need(name not in files and '__pycache__' not in p.parts,'No duplicate/pycache payload');files[name]=observed(p)
    need(dirs=={q.as_posix() for n in files for q in PurePosixPath(n).parents if q.as_posix()!='.'},'Exact topology, no extra empty directories');return files,dirs
def external():
    inputs=load(F/'INPUT_BINDINGS.json');need(inputs['schema']=='pr49-source-only-input-bindings/v2' and inputs['whole_binding_completed'] is True and inputs['actual_predecessor_PR48_completed'] is False and inputs['future48_V3_design_final_read_completed'] is True,'Actual WHOLE and completed V3 design, future48 acceptance false')
    for z in inputs['pins'].values():check(z)
    check(inputs['root_whole_record']);root=load(R/inputs['root_whole_record']['path']);need(root['approved_by_root'] is True and root['status']=='PASS_ROOT_COMPLETE_CLOSED_CURRENT_WHOLE_RECONCILIATION' and len(root['normalized_complete_fixed_bindings'])==3229,'Genuine complete3229-row ROOT WHOLE')
    for z in root['normalized_complete_fixed_bindings']:check(z)
    need(root['future_acceptance_approved'] is False and root['current_native_acceptance_approved'] is False and root['future_PR48_acceptance_approved'] is False and len(root['dated_native4'])==4,'No future acceptance authority')
    for z in root['dated_native4']:
        check(z['whole_historical_snapshot']);need(z['original_observed_row']['bytes']==z['whole_historical_snapshot']['bytes'] and z['original_observed_row']['sha256']==z['whole_historical_snapshot']['sha256'] and z['future_fresh13_ROOT_required'] is True and z['live_unchanged_required_by_review_closure'] is False,'Four dated fullbody witnesses, no live freshness')
    old=load(F/'ORIGINAL_UNCLOSED_FAMILY_BINDINGS.json');need(old['source_family_closed'] is False and old['historical_READY_not_SOURCE_approval'] is True and len(old['files'])==154,'Original49 unclosed154 preserved')
    for z in old['files']:check(z)
    design=load(F/'PREDECESSOR_V3_DESIGN_BINDINGS.json');need(design['source_design_ready'] is True and design['actual48_acceptance_completed'] is False and design['actual48_ROOT_post_completed'] is False and design['new48_SOURCE_adversary_approval_transferred'] is False and design['expected48V3_closure_schema']=='pr48-acceptance-source-closure/v3','No48 readiness/ROOT approval transfer')
    need(len(design['expected48V3_closure_exact_keys'])==9 and len(design['design_source_body_bindings'])==11 and len(design['closed_history_fixed_bindings'])==148,'Bounded exact design/history member counts')
    for z in design['design_source_body_bindings']:
        body_check(z);need(stat.S_IMODE(regular(R/z['path']).lstat().st_mode) in {0o644,0o444},'SOURCE mode is dated644 or later literal444 ROOT custody, not permissions authority')
    for z in design['closed_history_fixed_bindings']:check(z)
    need([z['id'] for z in design['entire_closed_M2_verdict']['mandatory_corrections']]==['M2'],'Closed adverse history stays adverse')
    c=design['entire_future48_ROOT_contract'];need(len(c['future48_required_ROOT_complete_keyset'])==22 and c['source_only'] is True and c['future_ROOT_post_completed'] is False,'Future48 ROOT22 contract only')
    return inputs,root,design
def clock(s):
    t=dt.datetime.fromisoformat(s);need(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0),'Aware UTC');return t
def actual_capture(folder,code):
    c=load(folder/'CAPTURE.json');p=c['prelaunch'];need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==code and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['status']==('PASS' if code==0 else 'FAIL'),'Complete typed actual private child')
    need(eq(load(folder/'PRELAUNCH.json'),p) and p['stdin_supplied'] is False and p['cwd']==str(F) and p['argv'][1]=='-B' and Path(p['argv'][2]).parent==F,'Actual private argv/cwd/prelaunch')
    need(sha(regular(folder/'PRELAUNCH_SOURCE.py').read_bytes())==p['source_sha256'] and sha(regular(folder/'PRELAUNCH_OPERATOR.py').read_bytes())==p['operator_sha256'],'Complete captured prelaunch sources')
    need(clock(p['created_utc'])<=clock(c['started_utc'])<clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual UTC chronology')
    for k in ['stdout','stderr']:
        z=c[k];b=regular(folder/z['path']).read_bytes();need(len(b)==z['bytes'] and sha(b)==z['sha256'],'Complete actual private stream')
    need((folder/'stderr.bin').read_bytes()==b'' if code==0 else bool((folder/'stderr.bin').read_bytes()),'Success/failure stream retained')
    for z in p.get('proposed_sources_read_as_text_only',[]):
        b=regular(folder/'PRELAUNCH_PROPOSED_SOURCES'/z['path']).read_bytes();need(len(b)==z['bytes'] and sha(b)==z['sha256'],'Entire proposed body read as text before child')
    return c
def captures():
    names={'AUTHORING_ACTUAL_CAPTURE':1,'REPAIR_AUTHOR_ACTUAL_CAPTURE':0,'AUTHORING_V2_ACTUAL_CAPTURE':0,'PRIVATE_CONTROLS_ACTUAL_CAPTURE':0,'FINAL_PRIVATE_CONTROLS_ACTUAL_CAPTURE':0,'PREDECESSOR_DESIGN_BINDING_ACTUAL_CAPTURE':0}
    return [dict(name=n,complete_capture=actual_capture(F/n,code)) for n,code in names.items()]
def science_and_sources():
    q=load(F/'FINAL_PRIVATE_CONTROLS_RESULT.json');need(q['status']=='PASS_PRIVATE_SOURCE_ONLY' and len(q['checks'])==35 and len(q['expected_negative_controls'])==26 and len(q['selected_actual_mode_controls'])==5,'Final bounded controls35/26/5')
    for n in SOURCES:
        b=regular(F/n).read_bytes();need(eq(q['six_source_bindings'][n],dict(bytes=len(b),sha256=sha(b))),'Current six source anchors')
    need(all(q[k] is False for k in ['production_imported_compiled_executed','formal_or_mathematical_certificate','native_index_remote_write','ROOT_approval_created','future_acceptance_approved']),'Private evidence is no production/math/ROOT approval')
    change=load(F/'CHANGE_MAP.json');need(change['scientific_metadata_unchanged'] is True and change['write_and_fresh_check_preserved_identically'] is True and len(change['unchanged_four_helpers'])==4,'Narrow repair map')
    for z in change['changes']:
        check(z['before']);now=observed(F/z['path']);need(now['bytes']==z['after']['bytes'] and now['sha256']==z['after']['sha256'],'Current changed source body matches author map')
    for n in ['SCIENTIFIC_SCOPE.json','EXPECTED_ORIGINAL_LEDGER.json','EXPECTED_CURRENT_ADMIN.json','EXPECTED_NATIVE_TRANSITION.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json']:need((F/n).read_bytes()==(A/'acceptance_preparation_family'/n).read_bytes(),'Unchanged exact metadata '+n)
    c=load(F/'ROOT_POST_CONTRACT.json');need(len(c['future49_required_ROOT_complete_keyset'])==22 and c['future_ROOT_post_completed'] is False and c['predecessor']['actually_completed'] is False,'Future49 ROOT22 still pending')
    for n in ['DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json']:
        d=load(F/n);need(d.get('created_utc') is None and d.get('preparation_manifest_sha256') is None and d.get('root_completed',False) is False and d.get('root_full_current_read_completed',False) is False,'False/null authority drafts')
    return q
def inspect():
    inputs,root,design=external();cs=captures();p=science_and_sources();files,dirs=topology()
    return dict(schema='pr49-source-v2-complete-readiness/v1',status='READY_SOURCE_ONLY_FOR_ROOT_CLOSURE',actual_private_pid=os.getpid(),utc=dt.datetime.now(dt.timezone.utc).isoformat(),own_files_before_readiness=len(files),own_relative_directories_before_readiness=len(dirs),six_source_bindings={n:observed(F/n) for n in SOURCES},root_whole_record=inputs['root_whole_record'],all3229_fixed_rows_and4dated_witnesses_checked=True,original_unclosed49_all154_files_unchanged=True,completed48V3_design_body_members=11,closed48V2_M2_fixed_members=148,complete_private_captures=cs,final_private_control_pid=p['actual_pid'],production_imported_compiled_executed=False,actual48_predecessor_completed=False,future_acceptance_approved=False,ROOT_approval_created=False,native_index_ref_remote_write=False)
def readiness_capture():
    folder=F/'FINAL_SOURCE_READINESS_ACTUAL_CAPTURE';c=actual_capture(folder,0);pre=c['prelaunch'];saved=load(F/'READINESS_CHECK.json');need(saved['actual_private_pid']==c['pid'] and saved['status']=='READY_SOURCE_ONLY_FOR_ROOT_CLOSURE' and load(folder/'stdout.bin')['actual_private_pid']==c['pid'],'Genuine actual final readiness child')
    common=pre['own_common'];b=regular(folder/common['path']).read_bytes();need(b==(F/'source_package_checks.py').read_bytes() and len(b)==common['bytes'] and sha(b)==common['sha256'],'Entire exact prelaunch own reader dependency')
    return c
