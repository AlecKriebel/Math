"""Own complete in-place custody audit; every production source is read as bytes only."""
from pathlib import Path,PurePosixPath
import datetime as dt,difflib,hashlib,json,math,os,re,stat,sys
F=Path(__file__).resolve().parent;A=F.parent;R=A.parents[2];S=A/'acceptance_preparation_family_v2'
checks=0;external={}
def need(x,m='custody failure'):
    global checks
    checks+=1
    if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def same(a,b):return type(a) is type(b) and (a.keys()==b.keys() and all(same(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(same(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
def parse(b):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'duplicate JSON');d[k]=v
        return d
    def floating(s):v=float(s);need(math.isfinite(v),'nonfinite JSON');return v
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def safe(p):
    need(p.is_absolute() and p.is_relative_to(R),'literal repository path')
    for ancestor in [p,*p.parents]:need(not ancestor.is_symlink(),'no symlink path/ancestor')
    need(stat.S_ISREG(p.lstat().st_mode),'regular body');return p
def observe(p,register=True):
    p=safe(p);raw=p.read_bytes();row=dict(path=p.relative_to(R).as_posix(),bytes=len(raw),sha256=sha(raw),full_mode=stat.S_IMODE(p.stat().st_mode))
    if register:
        need(row['path'] not in external or same(external[row['path']],row),'conflicting current binding');external[row['path']]=row
    return row,raw
def check_row(z,base=R,register=True,mode=True):
    need(type(z) is dict and type(z['path']) is str and type(z['sha256']) is str and len(z['sha256'])==64,'typed row')
    n=z['path'];q=PurePosixPath(n);need(not q.is_absolute() and q.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(q.parts),'canonical member')
    actual,raw=observe(base/n,register)
    count=z.get('bytes',z.get('size'));need(type(count) is int and count>=0 and actual['bytes']==count and actual['sha256']==z['sha256'],'complete full bytes: '+n)
    if mode and 'full_mode' in z:need(type(z['full_mode']) is int and actual['full_mode']==z['full_mode'],'full mode: '+n)
    return actual,raw
def clock(s):
    d=dt.datetime.fromisoformat(s.replace('Z','+00:00'));need(d.tzinfo is not None and d.utcoffset()==dt.timedelta(0),'actual UTC');return d
def root_capture(folder,expected_pid,source_basename):
    caprow,raw=observe(folder/'CAPTURE.json');cap=parse(raw)
    need(cap['schema']=='root-explicit-command-capture/v1','actual ROOT CAP4 helper schema')
    need(cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid']==expected_pid and type(cap['exit_code']) is int and cap['exit_code']==0,'genuine completed ROOT process')
    need(cap['argv'][:2]==['/usr/bin/python3','-B'] and Path(cap['argv'][2]).name==source_basename and Path(cap['argv'][2]).parent==S,'genuine current source argv')
    need(clock(cap['started_utc'])<=clock(cap['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'complete real chronology')
    for key in ['stdout','stderr']:check_row(cap[key],folder)
    need((folder/'stderr.bin').read_bytes()==b'','whole stderr empty')
    for n in ['PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py']:
        if (folder/n).exists():observe(folder/n)
    return cap
pin,closing_name,closing_pid,readback_name,readback_pid=sys.argv[1:]
manifest_row,manifest_body=observe(S/'PREPARATION_MANIFEST.json');need(manifest_row['sha256']==pin,'actual ROOT-returned manifest')
mf=parse(manifest_body);keys={'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'}
need(set(mf)==keys and mf['schema']=='pr49-acceptance-source-closure/v2' and mf['status']=='CLOSED_SOURCE_ONLY','exact nine-key V2 schema')
need(mf['source_only'] is True and mf['proposed_helpers_imported_compiled_executed'] is False and mf['future_acceptance_or_ROOT_approval_claimed'] is False,'no source self-approval')
need(same(mf['self_excluded'],['PREPARATION_MANIFEST.json']) and type(mf['files_count']) is int and mf['files_count']==len(mf['files']),'literal self exclusion typed count')
names={z['path'] for z in mf['files']};need(len(names)==len(mf['files']) and 'PREPARATION_MANIFEST.json' not in names,'no duplicate/self member')
actual_files=set();actual_dirs=set()
for p in S.rglob('*'):
    need(not p.is_symlink(),'complete symlink-free family')
    if p.is_file():actual_files.add(p.relative_to(S).as_posix())
    else:need(p.is_dir(),'no special file');actual_dirs.add(p.relative_to(S).as_posix())
need(actual_files==names|{'PREPARATION_MANIFEST.json'},'entire complete source family')
expected_dirs={q.as_posix() for n in actual_files for q in PurePosixPath(n).parents if q.as_posix()!='.'};need(actual_dirs==expected_dirs,'no extra empty directory')
for z in mf['files']:row,_=check_row(z,S);need(row['full_mode']==0o444,'every closed full mode444')
need(manifest_row['full_mode']==0o444,'manifest444')
control=parse((F/'PRIVATE_CONTROLS_RESULT.json').read_bytes())
source_read=[]
for n,expected in control['source_bindings'].items():
    row,raw=observe(S/n);need(row['bytes']==expected['bytes'] and row['sha256']==expected['sha256'],'source personally read before closure is unchanged');source_read.append(dict(**row,lines=len(raw.splitlines()),read_as_text_only=True))
old_source=A/'acceptance_preparation_family';diff=[]
for n in ['pr49_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py']:
    old_body=(old_source/n).read_bytes();new_body=(S/n).read_bytes()
    if n not in {'pr49_guards.py','capture_root_final_operation.py'}:need(old_body==new_body,'four full helper bodies unchanged')
    diff.extend(difflib.unified_diff(old_body.decode().splitlines(keepends=True),new_body.decode().splitlines(keepends=True),fromfile='original-unclosed/'+n,tofile='reviewed-V2/'+n))
def function_text(body,name):
    text=body.decode();match=re.search(r'^def '+re.escape(name)+r'\(',text,re.M);need(match is not None,'source function exists')
    tail=text[match.start():];next_function=re.search(r'^def ',tail[1:],re.M)
    return tail if next_function is None else tail[:1+next_function.start()]
for name in ['write','fresh_check','native_modes','foreign_capture','foreign_check','owned_log_append_check']:
    need(function_text((old_source/'pr49_guards.py').read_bytes(),name)==function_text((S/'pr49_guards.py').read_bytes(),name),'full reviewed function unchanged: '+name)
(F/'SOURCE_DIFF.patch').write_text(''.join(diff))
inputs=parse((S/'INPUT_BINDINGS.json').read_bytes());need(inputs['whole_binding_completed'] is True and inputs['actual_predecessor_PR48_completed'] is False,'WHOLE only supplied before future acceptance')
for z in inputs['pins'].values():check_row(z)
_,raw=check_row(inputs['root_whole_record']);root=parse(raw)
need(root['status']=='PASS_ROOT_COMPLETE_CLOSED_CURRENT_WHOLE_RECONCILIATION' and len(root['normalized_complete_fixed_bindings'])==3229,'all3229 genuine fixed WHOLE rows')
fixed_path_names=set()
for z in root['normalized_complete_fixed_bindings']:
    check_row(z,register=False);fixed_path_names.add(z['path'])
need(len(fixed_path_names)==3229,'unique whole fixed rows')
need(len(root['dated_native4'])==4,'four dated native witness count')
for z in root['dated_native4']:
    actual,body=check_row(z['whole_historical_snapshot']);old=z['original_observed_row']
    need(actual['bytes']==old['bytes'] and actual['sha256']==old['sha256'] and z['future_fresh13_ROOT_required'] is True and z['live_unchanged_required_by_review_closure'] is False,'dated bytes not native future authority')
old=parse((S/'ORIGINAL_UNCLOSED_FAMILY_BINDINGS.json').read_bytes());need(old['source_family_closed'] is False and len(old['files'])==154,'entire superseded unclosed154')
for z in old['files']:check_row(z,register=False)
design=parse((S/'PREDECESSOR_V3_DESIGN_BINDINGS.json').read_bytes())
need(design['actual48_acceptance_completed'] is False and design['actual48_ROOT_post_completed'] is False and design['new48_SOURCE_adversary_approval_transferred'] is False,'design not genuine future acceptance')
for z in design['design_source_body_bindings']:
    row,_=check_row(z,mode=False);need(row['full_mode'] in {0o644,0o444},'dated preparation-to-closure custody mode only')
for z in design['closed_history_fixed_bindings']:check_row(z,register=False)
need([z['id'] for z in design['entire_closed_M2_verdict']['mandatory_corrections']]==['M2'],'historic adverse stays adverse')
closure=root_capture(R/'draft_pr_publication_program_20260930/audits/pr45_9900007'/closing_name,int(closing_pid),'close_source_ROOT_ONLY.py')
readback=root_capture(R/'draft_pr_publication_program_20260930/audits/pr45_9900007'/readback_name,int(readback_pid),'verify_closed_source_ROOT_ONLY.py')
need(clock(closure['finished_utc'])<=clock(readback['started_utc']),'separate readback after actual close')
need(pin in (R/'draft_pr_publication_program_20260930/audits/pr45_9900007'/closing_name/'stdout.bin').read_text(),'actual closing stream returns bound hash')
need(readback['argv'][-2:]==['--expected-manifest-sha256',pin],'separate actual reader uses returned hash')
for capture_name,expected_code in [('AUTHORING_ACTUAL_CAPTURE',1),('REPAIR_AUTHOR_ACTUAL_CAPTURE',0),('AUTHORING_V2_ACTUAL_CAPTURE',0),('PRIVATE_CONTROLS_ACTUAL_CAPTURE',0),('FINAL_PRIVATE_CONTROLS_ACTUAL_CAPTURE',0),('PREDECESSOR_DESIGN_BINDING_ACTUAL_CAPTURE',0),('FINAL_SOURCE_READINESS_ACTUAL_CAPTURE',0)]:
    folder=S/capture_name;cap=parse((folder/'CAPTURE.json').read_bytes());pre=cap['prelaunch']
    need(cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid']>0 and type(cap['exit_code']) is int and cap['exit_code']==expected_code,'complete preparer capture')
    need(pre['cwd']==str(S) and cap['source_unchanged'] is True and cap['operator_unchanged'] is True,'preparer source custody')
    need(clock(pre['created_utc'])<=clock(cap['started_utc'])<=clock(cap['finished_utc']),'preparer actual chronology')
    for key in ['stdout','stderr']:check_row(cap[key],folder)
    need(sha((folder/'PRELAUNCH_SOURCE.py').read_bytes())==pre['source_sha256'] and sha((folder/'PRELAUNCH_OPERATOR.py').read_bytes())==pre['operator_sha256'],'whole preparer prelaunch source/operator')
    need((folder/'stderr.bin').read_bytes()==b'' if expected_code==0 else bool((folder/'stderr.bin').read_bytes()),'failed/success complete stderr retained')
    for z in pre.get('proposed_sources_read_as_text_only',[]):check_row(z,folder/'PRELAUNCH_PROPOSED_SOURCES')
result=dict(schema='pr49-fresh-source-complete-custody/v1',status='PASS',actual_pid=os.getpid(),utc=dt.datetime.now(dt.timezone.utc).isoformat(),assertions=checks,preparation_manifest_sha256=pin,source_payload_count=mf['files_count'],source_directories_count=len(actual_dirs),source_read_ledger=source_read,all3229_normalized_fixed_WHOLE_rows_checked=True,all154_unclosed_old_source_bodies_checked=True,all148_closed48_history_rows_checked=True,dated_native4_body_witnesses_checked_without_live_equality=True,actual_ROOT_closing_pid=int(closing_pid),actual_ROOT_separate_readback_pid=int(readback_pid),production_imported_compiled_executed=False,future_acceptance_approved=False)
(F/'CUSTODY_RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
(F/'EXTERNAL_BINDINGS.json').write_text(json.dumps(dict(schema='pr49-fresh-source-individual-inputs/v1',files=sorted(external.values(),key=lambda z:z['path']),nested_fixed_table=inputs['root_whole_record'],nested_fixed_table_count=3229,nested_old_source_table='ORIGINAL_UNCLOSED_FAMILY_BINDINGS.json',nested_closed48_history_table='PREDECESSOR_V3_DESIGN_BINDINGS.json'),sort_keys=True,separators=(',',':'))+'\n')
print(json.dumps(result,sort_keys=True,indent=2))
