"""One passive four-root custody reader; never import or execute research code."""
import datetime,hashlib,json,os,re,stat
from pathlib import Path
if not __debug__:
    raise RuntimeError('Custody assertions must remain enabled')
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=P/'verification/pentagon-root-custody-sol-20261117'
BASE=P/'papers/23137834'
ROOTS={'source':BASE/'sources','root_INITIAL':BASE/'reviews/root-initial-20261117','adversarial':BASE/'reviews/adversarial-sol','scope':BASE/'reviews/scope-sol'}
EXPECTED={'source':(97,7),'root_INITIAL':(17,1),'adversarial':(47,4),'scope':(81,3)}

def allowed(path):
    assert any(path==r or path.is_relative_to(r) for r in ROOTS.values()),str(path)
    assert not path.is_symlink(),str(path)

def raw(path):
    allowed(path)
    a=path.lstat();assert stat.S_ISREG(a.st_mode),str(path)
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        b=os.fstat(fd);assert (a.st_dev,a.st_ino)==(b.st_dev,b.st_ino)
        with os.fdopen(fd,'rb',closefd=False) as f:body=f.read()
        z=os.fstat(fd)
        assert (b.st_dev,b.st_ino,b.st_mode,b.st_size,b.st_mtime_ns,b.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
        assert len(body)==z.st_size
        return body
    finally:os.close(fd)

def load(path):return json.loads(raw(path))
def sha(body):return hashlib.sha256(body).hexdigest()
def mode(path):return format(stat.S_IMODE(path.lstat().st_mode),'04o')
def relsafe(text):
    p=Path(text);assert not p.is_absolute() and '..' not in p.parts and str(p) not in ('','.'),text
    return p.as_posix()

def census(root):
    allowed(root)
    files={};dirs={};pending=[root]
    while pending:
        here=pending.pop();a=here.lstat();assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        entries=sorted(here.iterdir())
        key=here.relative_to(root).as_posix()
        dp=dict(mode=mode(here),empty=not entries,mtime_ns=a.st_mtime_ns,ctime_ns=a.st_ctime_ns)
        if key=='.':root_pin=dp
        else:dirs[key]=dp
        for path in entries:
            z=path.lstat();rel=path.relative_to(root).as_posix();assert not path.is_symlink()
            if stat.S_ISDIR(z.st_mode):pending.append(path)
            else:
                body=raw(path)
                files[rel]=dict(bytes=len(body),SHA256=sha(body),mode=mode(path),empty=not body,hidden=any(t.startswith('.') for t in Path(rel).parts),mtime_ns=z.st_mtime_ns,ctime_ns=z.st_ctime_ns)
        z=here.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
    return dict(root=str(root),root_metadata=root_pin,files=files,directories=dirs)

started=datetime.datetime.now(datetime.timezone.utc).isoformat()
before={label:census(root) for label,root in ROOTS.items()}
for label,(nf,nd) in EXPECTED.items():assert (len(before[label]['files']),len(before[label]['directories']))==(nf,nd),label
assert sum(len(x['files']) for x in before.values())==242
assert sum(len(x['directories']) for x in before.values())==15
external=[('source','SOURCE_FINAL.json',908,'14cbf430570b90574e7c28bba911e7fe2b868c164107591b1783694c30212f80'),('source','SOURCE_MANIFEST.json',20546,'7f2ec5e3f4d6fa358bc9dcc5af3ef5adb4ec3e3b2b8851ff831f8b4574dcd2ed'),('root_INITIAL','INITIAL_SEAL.json',558,'a47cd3a2b923f87c6479f17277aa3cd35e4ef3792e20a2a69a8be1623575632b'),('root_INITIAL','INITIAL_MANIFEST.json',3695,'223215551a335131ef19947432afd1d9c614353882c1ae7bdbe2a772a5efee15'),('adversarial','FINAL.json',3811,'5d02a6ed2c1c652e2c821dd3c59c61dd26e9fa039443b19ad4d5d8475565017e'),('adversarial','MANIFEST.json',8561,'53f16c689368a67a76c7a85597a2acc87abb16414767c8740fad9d14b79adc54'),('scope','FINAL.json',4840,'7b9e29236010ae962915d4477ce9c2cd44443daff94d87c418cf7847b5a3da25'),('scope','MANIFEST.sha256',7102,'39fc00aca8a8b91360625e550083424c2e03213bce378b553bcef3b70b9b3453')]
external_checked=[]
for label,rel,size,digest in external:
    pin=before[label]['files'][rel]
    assert (pin['bytes'],pin['SHA256'])==(size,digest),(label,rel)
    external_checked.append(dict(namespace=label,path=rel,**{k:pin[k] for k in ['bytes','SHA256','mode']}))

checks=[]
def rowcheck(label,rows):
    seen=set()
    for row in rows:
        rel=relsafe(row['path']);assert rel not in seen;seen.add(rel)
        p=before[label]['files'][rel]
        h=row['SHA256'] if 'SHA256' in row else row['sha256']
        assert isinstance(h,str) and re.fullmatch('[0-9a-f]{64}',h),rel
        assert p['SHA256']==h and p['bytes']==row['bytes'] and int(p['mode'],8)==int(row['mode'],8),(label,rel)
    return seen

def dircheck(label,rows,include_root=False):
    seen=set()
    for row in rows:
        rel=row['path'];assert rel not in seen;seen.add(rel)
        p=before[label]['root_metadata'] if rel=='.' else before[label]['directories'][relsafe(rel)]
        assert int(p['mode'],8)==int(row['mode'],8),(label,rel)
    assert seen==set(before[label]['directories'])|({'.'} if include_root else set())

source=load(ROOTS['source']/'SOURCE_MANIFEST.json');sf=load(ROOTS['source']/'SOURCE_FINAL.json')
sp=rowcheck('source',source['files']);term=set(source['root_controls_excluded_from_own_list'])
assert term=={'SOURCE_MANIFEST.json','SOURCE_FINAL.json'} and sp|term==set(before['source']['files']) and not sp&term
dircheck('source',source['directories'])
assert source['ordinary_files_including_controls']==97 and source['child_directory_count']==7
assert sf['extent']==dict(ordinary_files=97,child_directories=7)
assert sf['SOURCE_MANIFEST']['SHA256']==before['source']['files']['SOURCE_MANIFEST.json']['SHA256']
assert int(sf['SOURCE_MANIFEST']['mode'],8)==int(before['source']['files']['SOURCE_MANIFEST.json']['mode'],8)
rowcheck('source',[sf['SOURCE_READY']])
checks.append(dict(namespace='source',payload_rows=len(sp),exact_existing_recursion_terminals=sorted(term),directory_modes_verified=7,manifest_mode_link_verified=True,terminal_SOURCE_FINAL_mode_observed=before['source']['files']['SOURCE_FINAL.json']['mode'],source_root_mode_observed=before['source']['root_metadata']['mode'],no_undeclared_terminal_mode_invented=True))

im=load(ROOTS['root_INITIAL']/'INITIAL_MANIFEST.json');iseal=load(ROOTS['root_INITIAL']/'INITIAL_SEAL.json')
ip=rowcheck('root_INITIAL',im['payload_files']);it=set(im['exact_terminal_recursive_hash_exclusions'])
assert it=={'INITIAL_MANIFEST.json','INITIAL_SEAL.json'} and ip|it==set(before['root_INITIAL']['files']) and not ip&it
assert im['other_exclusions']==[] and im['regular_files']==17 and im['child_directories']==1
assert before['root_INITIAL']['root_metadata']['mode']==im['root_mode']=='0555'
dircheck('root_INITIAL',im['directories'],True)
for rel in it:assert before['root_INITIAL']['files'][rel]['mode']==im['terminal_modes'][rel]=='0444'
assert all(x['mode']=='0444' for x in before['root_INITIAL']['files'].values())
assert iseal['manifest_SHA256']==before['root_INITIAL']['files']['INITIAL_MANIFEST.json']['SHA256']
checks.append(dict(namespace='root_INITIAL',payload_rows=len(ip),exact_existing_recursion_terminals=sorted(it),root_and_child_directory_modes='0555',all17_regular_file_modes='0444'))

am=load(ROOTS['adversarial']/'MANIFEST.json');af=load(ROOTS['adversarial']/'FINAL.json')
ap=rowcheck('adversarial',am['payload_pins']);at={'MANIFEST.json','FINAL.json'}
assert am['self_and_FINAL_excluded'] is True and af['self_hash_excluded'] is True
assert len(ap)==am['payload_regular_files']==45 and ap|at==set(before['adversarial']['files']) and not ap&at
assert set(am['child_directories'])==set(before['adversarial']['directories'])
assert set(af['exact_extent']['files'])==set(before['adversarial']['files']) and set(af['exact_extent']['directories'])==set(before['adversarial']['directories'])
assert af['exact_extent']['regular_files']==47 and af['exact_extent']['child_directories']==4
assert af['manifest']['sha256']==before['adversarial']['files']['MANIFEST.json']['SHA256'] and int(af['manifest']['mode'],8)==int(before['adversarial']['files']['MANIFEST.json']['mode'],8)
checks.append(dict(namespace='adversarial',payload_rows=45,exact_existing_recursion_terminals=sorted(at),manifest_mode_link_verified=True,FINAL_mode_observed=before['adversarial']['files']['FINAL.json']['mode'],directory_and_root_modes_observed=before['adversarial']['root_metadata']['mode'],directory_modes_not_declared_in_original_controls=sorted(before['adversarial']['directories']),no_undeclared_mode_invented=True))

cf=load(ROOTS['scope']/'FINAL.json');extent=cf['finite_extent'];scope_rows={}
for line in raw(ROOTS['scope']/'MANIFEST.sha256').decode().splitlines():
    match=re.fullmatch(r'([0-9a-f]{64})  (.+)',line);assert match,line
    digest,rel=match.groups();rel=relsafe(rel);assert rel not in scope_rows
    assert before['scope']['files'][rel]['SHA256']==digest,rel
    scope_rows[rel]=digest
st=set(extent['exact_existing_terminal_controls_excluded'])
assert st=={'MANIFEST.sha256','FINAL.json'} and set(scope_rows)|st==set(before['scope']['files']) and not set(scope_rows)&st
assert extent['regular_files']==81 and extent['payload_files_in_manifest']==len(scope_rows)==79 and extent['future_exclusions']==[]
assert set(extent['child_directories'])==set(before['scope']['directories'])
assert all(x['mode']==extent['all_regular_file_modes'] for x in before['scope']['files'].values())
assert before['scope']['root_metadata']['mode']==extent['root_and_child_directory_modes']
assert all(x['mode']==extent['root_and_child_directory_modes'] for x in before['scope']['directories'].values())
assert cf['manifest']['SHA256']==before['scope']['files']['MANIFEST.sha256']['SHA256']
checks.append(dict(namespace='scope',manifest_format='SHA256 two-space relative-path text',payload_rows=79,exact_existing_recursion_terminals=sorted(st),each_file_mode_checked_against_own_FINAL_declaration=extent['all_regular_file_modes'],root_and_each_directory_mode_checked_against_own_FINAL_declaration=extent['root_and_child_directory_modes']))

src=ROOTS['source']/'published-source/container-001/tree'
arithmetic=raw(src/'programs/arithmetic.py');copy=raw(ROOTS['adversarial']/'native-run/arithmetic.py')
assert len(arithmetic)==8484 and sha(arithmetic)=='3c5bd223a9841719c4a51112c2d9e34cd55fc9a54a8cc4e11b55c6f8b2d6dbd1' and arithmetic==copy
geometry=raw(src/'programs/geometry.py')
assert len(geometry)==6420 and sha(geometry)=='c26a532c7d092b32a76dc204c0845fde8d7a545d4cd9127362616015efadfba4'
assert not (ROOTS['scope']/'native-run/geometry.py').exists()
ae=load(ROOTS['adversarial']/'NATIVE_EXECUTION.json');spec=load(ROOTS['adversarial']/'NATIVE_RUN_SPEC.json');inspection=load(ROOTS['adversarial']/'RESULT_INSPECTION.json')
assert ae['ordinary_invocations']==1 and ae['actual_exit']==0 and ae['reruns']==0
assert ae['source_sha256']==ae['copy_sha256']==sha(arithmetic) and ae['source_unchanged'] is True
assert spec['command']==['/Library/Developer/CommandLineTools/usr/bin/python','-B',str(ROOTS['adversarial']/'native-run/arithmetic.py')]
aout=raw(ROOTS['adversarial']/'native-run/stdout.json');aerr=raw(ROOTS['adversarial']/'native-run/stderr.txt');aexpected=raw(src/'expected/arithmetic.json')
assert len(aout)==ae['stdout_bytes']==1669 and len(aerr)==ae['stderr_bytes']==0
assert json.loads(aout)==json.loads(aexpected)==inspection['output']
rowcheck('adversarial',[inspection['literal_stdout_pin'],inspection['literal_stderr_pin']])
ac=load(ROOTS['adversarial']/'SOURCE_CUSTODY.json')
assert ac['regular_files']==97 and ac['child_directories']==7 and rowcheck('source',ac['files'])==set(before['source']['files'])
assert set(ac['directories'])==set(before['source']['directories'])
route=cf['single_native_route']
assert route['scientific_execution_history']==[0] and route['other_native_routes_variants_optimized_runs_reruns_or_dependency_installs']==0
assert route['source_relative_path']=='published-source/container-001/tree/programs/geometry.py' and route['bytes']==6420 and route['SHA256']==sha(geometry)
sout=raw(ROOTS['scope']/'native-run/stdout.txt');serr=raw(ROOTS['scope']/'native-run/stderr.txt')
assert len(sout)==3177 and len(serr)==0 and raw(ROOTS['scope']/'native-run/exit.txt')==b'0\n'
rowcheck('scope',[dict(route['stdout'],mode=extent['all_regular_file_modes']),dict(route['stderr'],mode=extent['all_regular_file_modes'])])
stamp=r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00'
lines=[];full_removed=suffix_removed=0
for line in sout.decode('utf-8').splitlines():
    if re.fullmatch(r'native_utc(?:_start|_end)? '+stamp,line):full_removed+=1;continue
    cleaned,n=re.subn(r' native_utc '+stamp+r'$','',line);suffix_removed+=n;lines.append(cleaned)
normalized=('\n'.join(lines)+'\n').encode();gexpected=raw(src/'expected/geometry.txt')
assert len(normalized)==1715 and normalized==gexpected
assert route['complete_mathematical_output']['bytes']==1715 and route['complete_mathematical_output']['SHA256']==sha(normalized)
assert raw(ROOTS['scope']/'native-run/comparison.exit')==b'0\n' and raw(ROOTS['scope']/'native-run/comparison.stderr')==b''
comparison=load(ROOTS['scope']/'native-run/comparison.stdout')
assert comparison['native_routes']==1 and comparison['raw_stdout_bytes']==3177 and comparison['normalized_bytes']==1715 and comparison['normalized_SHA256']==sha(normalized)
plan_text=raw(ROOTS['scope']/'NATIVE_PLAN.md').decode()
recorded_command='PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.11 ../../sources/published-source/container-001/tree/programs/geometry.py'
assert recorded_command in plan_text
sb=raw(ROOTS['scope']/'native-run/SOURCES.before.sha256');sa=raw(ROOTS['scope']/'native-run/SOURCES.after.sha256')
tb=raw(ROOTS['scope']/'native-run/SOURCES.before.topology');ta=raw(ROOTS['scope']/'native-run/SOURCES.after.topology')
assert sb==sa and tb==ta
source_history={}
for line in sb.decode().splitlines():
    m=re.fullmatch(r'([0-9a-f]{64})  \.\./\.\./sources/(.+)',line);assert m,line
    digest,rel=m.groups();rel=relsafe(rel);assert rel not in source_history
    assert before['source']['files'][rel]['SHA256']==digest,rel;source_history[rel]=digest
assert set(source_history)==set(before['source']['files'])
history_dirs={};history_files={}
for line in tb.decode().splitlines():
    m=re.fullmatch(r'(Directory|Regular File) ([0-7]+) (\d+) \.\./\.\./sources(?:/(.+))?',line);assert m,line
    kind,declared_mode,declared_size,rel=m.groups();rel='.' if rel is None else relsafe(rel)
    if kind=='Directory':
        p=before['source']['root_metadata'] if rel=='.' else before['source']['directories'][rel]
        assert int(p['mode'],8)==int(declared_mode,8);assert rel not in history_dirs;history_dirs[rel]=dict(mode=declared_mode,historical_storage_bytes=int(declared_size))
    else:
        p=before['source']['files'][rel];assert int(p['mode'],8)==int(declared_mode,8) and p['bytes']==int(declared_size)
        assert rel not in history_files;history_files[rel]=dict(mode=declared_mode,bytes=int(declared_size))
assert set(history_dirs)==set(before['source']['directories'])|{'.'} and set(history_files)==set(before['source']['files'])
execution=dict(adversarial=dict(route='One recorded isolated arithmetic copy invocation',recorded_argv=spec['command'],source_and_copy_bytes_equal=True,source_and_copy_SHA256=sha(arithmetic),actual_recorded_attempts=1,actual_recorded_exit=0,stdout=dict(bytes=len(aout),SHA256=sha(aout)),stderr=dict(bytes=len(aerr),SHA256=sha(aerr)),full_parsed_JSON_equal_actual_published_expectation=True,literal_bytes_equal_published_expectation=aout==aexpected,source_custody97files7dirs_actual_match=True),scope=dict(route='One recorded direct-source geometry invocation; no isolated geometry copy exists or is claimed',recorded_plan_command=recorded_command,source_program_bytes=6420,source_program_SHA256=sha(geometry),actual_recorded_attempts=1,actual_recorded_exit=0,stdout=dict(bytes=len(sout),SHA256=sha(sout)),stderr=dict(bytes=len(serr),SHA256=sha(serr)),normalized=dict(bytes=len(normalized),SHA256=sha(normalized),equal_whole_actual_published_expectation=True,removed_fully_anchored_UTC_lines=full_removed,removed_exact_trailing_UTC_suffixes=suffix_removed,other_normalization=False),historical_source_before_after_receipt_bytes_equal=True,current_source97files_and8directory_paths_modes_match_history=True,historical_checksum_receipt_SHA256=sha(sb),historical_topology_receipt_SHA256=sha(tb)),limits='These are authenticated historical receipts and saved-output comparisons, not new scientific executions or a new mathematical verdict. Other scripts, variants and all-suite reproduction are not claimed. Original lookup/dependency/reading errors remain as frozen payloads and are not relabeled as clean probes.')
after={label:census(root) for label,root in ROOTS.items()}
assert before==after
result=dict(schema='pentagon-four-root-data-custody-v1',started_UTC=started,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='FOUR_FIXED_NAMESPACES_AUTHENTICATED',fixed_extent=dict(files=242,child_directories=15,roots=4),external_control_pins=external_checked,manifest_checks=checks,historical_execution_authentication=execution,before=before,after=after,whole_before_after_equal=True,all_hidden_ignored_empty_bytes_modes_topology_included=True,no_import_AST_compile_helper_or_scientific_execution=True,no_current_root_progress_W_Git_network_Sheet_read_or_mutation=True,own_data_custody_completion_percent=100,scientific_verdict='NONE_BY_THIS_CUSTODY_TASK',programme_goal_active_incomplete=True)
with (OWN/'DATA_AUTHENTICATION.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(dict(status=result['status'],files=242,child_directories=15,external_controls=len(external_checked),manifest_payload_rows=[x['payload_rows'] for x in checks],whole_before_after_equal=True,arithmetic_full_parsed_output_equal=True,geometry_normalized_bytes=1715,geometry_full_normalized_output_equal=True,scope_route='Direct source; isolated geometry copy absent and not claimed',new_scientific_executions=0,new_scientific_verdict=False,custody_completion_percent=100)))
