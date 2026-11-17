"""Data-only finite D4 custody; no target code import, parse or execution."""
from pathlib import Path
import datetime,hashlib,json,os,stat
if not __debug__:
    raise RuntimeError('Custody assertions require unoptimized Python')
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/d4-root-custody-sol-20261117')
BASE=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23439776')
SPECS=[('sources',72,7,'SOURCE_MANIFEST.json','SOURCE_FINAL.json','files','directories'),('reviews/root',17,1,'INITIAL_MANIFEST.json','INITIAL_SEAL.json','files','directories'),('reviews/adversarial-sol',53,3,'OWNED_MANIFEST.json','FINAL.json','payloads','directories'),('reviews/scope-sol',95,3,'OWNED_MANIFEST.json','FINAL.json','payloads','directory_modes')]
EXTERNAL={'sources/SOURCE_FINAL.json':'e95d8717aee6b39ba23b73d85462a20340c823ff3ee5a09bc66470775a5b5a03','reviews/root/INITIAL_SEAL.json':'41fba8e0dc837a244f739dae50d9fe552335e360bb9e4003819b46ba5c997228','reviews/adversarial-sol/FINAL.json':'6f781d8334c1e5b3a17c87128653b3301274104159c70d8d550c3e80b3d20bce','reviews/adversarial-sol/OWNED_MANIFEST.json':'e7c5ea3a64cf6c8079d127699955a8060e49a7685a2e0d5b5c598f6a1e6b411a','reviews/scope-sol/FINAL.json':'4158336e8ea7b0322e1d387f2f84f508887a911dc64c33fd9a70686d9cd302fa','reviews/scope-sol/OWNED_MANIFEST.json':'5d9a0b188d397fefe744f7451aba032586625c09e095834f19353b573ab28e6c'}
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def mode(value):return stat.S_IMODE(value if isinstance(value,int) else int(value,8))
def stable_bytes(path):
    a=path.lstat();assert stat.S_ISREG(a.st_mode) and not path.is_symlink(),str(path)
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        first=os.fstat(fd);assert (a.st_dev,a.st_ino)==(first.st_dev,first.st_ino)
        blocks=[]
        while True:
            block=os.read(fd,1048576)
            if not block:break
            blocks.append(block)
        end=os.fstat(fd)
        fields=lambda x:(x.st_dev,x.st_ino,x.st_size,x.st_mode,x.st_mtime_ns,x.st_ctime_ns)
        assert fields(first)==fields(end)==fields(path.lstat()),str(path)
        raw=b''.join(blocks);assert len(raw)==end.st_size
        return raw,dict(bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),mode=oct(stat.S_IMODE(end.st_mode)),mtime_ns=end.st_mtime_ns,ctime_ns=end.st_ctime_ns)
    finally:os.close(fd)
def census(root):
    files={};directories={};pending=[root]
    while pending:
        here=pending.pop();a=here.lstat();assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        children=sorted(here.iterdir())
        for p in children:
            rel=p.relative_to(root).as_posix();z=p.lstat();assert not p.is_symlink()
            if stat.S_ISDIR(z.st_mode):
                directories[rel]=dict(mode=oct(stat.S_IMODE(z.st_mode)),empty=not any(p.iterdir()),mtime_ns=z.st_mtime_ns,ctime_ns=z.st_ctime_ns);pending.append(p)
            else:
                raw,pin=stable_bytes(p);files[rel]=dict(**pin,hidden=any(x.startswith('.') for x in Path(rel).parts),empty=not raw)
        z=here.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
    z=root.lstat()
    return dict(root=str(root),root_mode=oct(stat.S_IMODE(z.st_mode)),root_mtime_ns=z.st_mtime_ns,root_ctime_ns=z.st_ctime_ns,files=files,directories=directories)
def metadata(root,relative):
    rel=Path(relative);assert not rel.is_absolute() and '..' not in rel.parts
    return json.loads(stable_bytes(root/rel)[0])
def check_pin(row,actual):
    assert row['bytes']==actual['bytes'] and row['SHA256']==actual['SHA256']
    if 'mode' in row:assert mode(row['mode'])==mode(actual['mode'])
def validate_manifest(spec,snapshot):
    rel,nfiles,ndirs,manifest_name,final_name,file_key,dir_key=spec;root=BASE/rel
    manifest=metadata(root,manifest_name);final=metadata(root,final_name)
    assert len(snapshot['files'])==nfiles and len(snapshot['directories'])==ndirs
    assert mode(manifest['root_mode'])==mode(snapshot['root_mode'])
    if 'root' in manifest:assert Path(manifest['root'])==root
    payloads=manifest[file_key];names=[x['path'] for x in payloads]
    assert len(names)==len(set(names))
    terminals={manifest_name,final_name}
    assert set(names)|terminals==set(snapshot['files']) and not set(names)&terminals
    for item in payloads:
        path=Path(item['path']);assert not path.is_absolute() and '..' not in path.parts
        check_pin(item,snapshot['files'][item['path']])
        if 'hidden' in item:assert item['hidden']==snapshot['files'][item['path']]['hidden']
        if 'empty' in item:assert item['empty']==snapshot['files'][item['path']]['empty']
    rows=manifest[dir_key];dirnames=[x['path'] for x in rows]
    assert len(dirnames)==len(set(dirnames)) and set(dirnames)==set(snapshot['directories'])
    for item in rows:
        actual=snapshot['directories'][item['path']];assert mode(item['mode'])==mode(actual['mode'])
        if 'empty' in item:assert item['empty']==actual['empty']
    for key in ['root_controls_excluded_from_own_list','exact_existing_root_terminal_controls_excluded','exact_existing_terminal_controls_excluded']:
        if key in manifest:assert set(manifest[key])==terminals
    if 'actual_file_paths_including_controls' in manifest:assert set(manifest['actual_file_paths_including_controls'])==set(snapshot['files'])
    if rel=='sources':
        assert manifest['schema']=='opaque-native-source-manifest-v1'
        assert final['extent']==dict(ordinary_files=nfiles,child_directories=ndirs)
        check_pin(final['SOURCE_MANIFEST'],snapshot['files'][manifest_name]);check_pin(final['SOURCE_READY'],snapshot['files']['SOURCE_READY.json'])
    elif rel=='reviews/root':
        assert final['manifest_SHA256']==snapshot['files'][manifest_name]['SHA256']
        assert final['INITIAL_SHA256']==snapshot['files']['INITIAL.md']['SHA256']
        assert final['files_including_exact_controls']==nfiles and final['child_directories']==ndirs
    elif rel=='reviews/adversarial-sol':
        assert manifest['schema']=='finite-whole-owned-scientific-review-v1'
        assert manifest['extent_including_controls']==dict(files=nfiles,child_directories=ndirs)
        assert final['extent']==dict(files=nfiles,child_directories=ndirs)
        check_pin(final['manifest'],snapshot['files'][manifest_name]);check_pin(final['report'],snapshot['files']['REPORT.md']);check_pin(final['native_result'],snapshot['files']['native-route/results.json'])
    else:
        assert manifest['schema']=='finite-scientific-scope-manifest-v1'
        assert manifest['extent']==dict(ordinary_files=nfiles,child_directories=ndirs)
        assert final['extent']==dict(ordinary_files=nfiles,child_directories=ndirs)
        assert manifest['ignored_empty_failure_or_future_subtree_exclusions']==[]
        for value in final.values():
            if isinstance(value,dict) and {'path','bytes','SHA256'}<=set(value):check_pin(value,snapshot['files'][value['path']])
    return dict(path=rel,files=nfiles,child_directories=ndirs,manifest=dict(path=manifest_name,**snapshot['files'][manifest_name]),terminal=dict(path=final_name,**snapshot['files'][final_name]),payload_rows=len(payloads),complete_actual_file_set_authenticated=True,complete_directory_set_and_modes_authenticated=True)
started=utc();before={spec[0]:census(BASE/spec[0]) for spec in SPECS}
assert sum(len(x['files']) for x in before.values())==237 and sum(len(x['directories']) for x in before.values())==14
external=[]
for path,sha in EXTERNAL.items():
    raw,pin=stable_bytes(BASE/path);assert pin['SHA256']==sha,path;external.append(dict(path=path,**pin))
packets=[validate_manifest(spec,before[spec[0]]) for spec in SPECS]
code=BASE/'sources/published-source/container-001/tree/verify.py';data=code.parent/'certificate.json'
source_code,code_pin=stable_bytes(code);source_data,data_pin=stable_bytes(data)
assert (code_pin['bytes'],code_pin['SHA256'])==(16269,'a0defbc066b45586e8b3456504167db9d14a6d82023f04b566d3f90e412e5006')
assert (data_pin['bytes'],data_pin['SHA256'])==(16389,'4730fdf08a063a7e069619a75e390b45c317751e421ad08064844b7fd68549a4')
copies=[];receipts=[];result_bytes=[]
for family,native in [('reviews/adversarial-sol','native-route'),('reviews/scope-sol','native')]:
    root=BASE/family;snapshot=before[family]
    actual_code,cp=stable_bytes(root/native/'verify.py');actual_data,dp=stable_bytes(root/native/'certificate.json')
    assert actual_code==source_code and actual_data==source_data
    result,rp=stable_bytes(root/native/'results.json');assert (rp['bytes'],rp['SHA256'])==(24946,'ed99482136e58761f0df9ad6f59e3fa3a57ef0b1053e10326c1c3ea8de0f27a1')
    result_bytes.append(result)
    if family.endswith('adversarial-sol'):
        receipt=metadata(root,'NATIVE_RECEIPT.json');invocation=metadata(root,'NATIVE_INVOCATION.json')
        assert receipt['exit_code']==0 and receipt['exception'] is None and receipt['ordinary_native_invocations']==receipt['process_launch_attempts']==1
        assert receipt['command']==invocation['command'] and receipt['command'][-1]==str(root/native/'verify.py')
        for item in invocation['exact_relocated_inputs']:check_pin(item,snapshot['files'][item['path']])
        for key in ('stdout','stderr','result'):check_pin(receipt[key],snapshot['files'][receipt[key]['path']])
        stdout_name='native.stdout.txt';stderr_name='native.stderr.txt';receipt_name='NATIVE_RECEIPT.json'
    else:
        receipt=metadata(root,'NATIVE_EXECUTION.json');assert receipt['exit_code']==0 and receipt['native_invocation_count']==1
        assert receipt['command'][-1]==str(root/native/'verify.py')
        stdout_name='NATIVE.stdout.txt';stderr_name='NATIVE.stderr.txt';receipt_name='NATIVE_EXECUTION.json'
        assert receipt['stdout_bytes']==snapshot['files'][stdout_name]['bytes'] and receipt['stderr_bytes']==snapshot['files'][stderr_name]['bytes']
        assert receipt['code_read']['code_SHA256']==cp['SHA256'] and receipt['code_read']['data_SHA256']==dp['SHA256']
    copies.append(dict(family=family,code=dict(path=native+'/verify.py',**cp),certificate=dict(path=native+'/certificate.json',**dp),whole_code_and_certificate_bytes_equal_source=True,result=dict(path=native+'/results.json',**rp)))
    receipts.append(dict(family=family,receipt=dict(path=receipt_name,**snapshot['files'][receipt_name]),historical_reported_exit_code=receipt['exit_code'],historical_started_UTC=receipt['started_UTC'],historical_finished_UTC=receipt['finished_UTC'],stdout=dict(path=stdout_name,**snapshot['files'][stdout_name]),stderr=dict(path=stderr_name,**snapshot['files'][stderr_name]),streams_authenticated_by_current_external_bound_manifest=True,historical_scientific_execution_not_repeated=True))
assert result_bytes[0]==result_bytes[1]
after={spec[0]:census(BASE/spec[0]) for spec in SPECS};assert before==after
result=dict(schema='d4-root-data-only-finite-custody-v1',started_UTC=started,finished_UTC=utc(),status='FOUR_D4_NAMESPACES_DATA_AUTHENTICATED_NO_NEW_SCIENTIFIC_VERDICT',regular_files=237,child_directories=14,packets=packets,external_control_pins=external,source_native_code=dict(path=str(code.relative_to(BASE)),**code_pin),source_native_certificate=dict(path=str(data.relative_to(BASE)),**data_pin),actual_isolated_copies=copies,historical_execution_receipts=receipts,both_actual_result_whole_bytes_equal=True,scope_result_read_as_actual_bytes_not_assumed=True,protected_before_after_whole_metadata_equal=True,complete_actual_objects=before,hidden_regular_files=sum(v['hidden'] for x in before.values() for v in x['files'].values()),empty_regular_files=sum(v['empty'] for x in before.values() for v in x['files'].values()),empty_directories=sum(v['empty'] for x in before.values() for v in x['directories'].values()),ignore_filtering_applied=False,target_code_import_parse_AST_compile_help_execution=False,mathematical_reports_or_result_claims_interpreted=False,W_nativeGit_PROGRESS_or_root_continuation_read=False,mutation_outside_own=False,new_mathematical_verdict=None,custody_task_completion_percent=100)
with (OWN/'DATA_AUTHENTICATION.json').open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
report='# D4 data-only custody authenticated\n\nAll four authorized current namespaces match their actual heterogeneous manifests and supplied external controls: source72/7, frozen rootINITIAL17/1, adversarial53/3 and scope95/3; total237regularfiles/14childdirectories. Every actual file, hidden/ignored/empty object, directory and mode was included without Git ignore filtering. Fresh before/after whole metadata is equal.\n\nThe16269Bnative code and16389Bcertificate match the supplied hashes in source and both isolated copies, with direct whole-byte equality. Both actual24946Bresult blobs were freshly read, match ed99482136e58761f0df9ad6f59e3fa3a57ef0b1053e10326c1c3ea8de0f27a1 and equal each other. Historical family execution receipts report exit0; stdout/stderr hashes and lengths were authenticated independently (stdout251B adversarial versus239B scope).\n\nThis reader ran no scientific program and imported/parsed/compiled no target code. Mathematical reports and result claims were not interpreted. W/nativeGit/PROGRESS and unfinished root continuation were not read. Only this own directory was written. No scientific verdict or disposition is supplied. Data-custody task100%complete; the research programme remains active/incomplete.\n'
with (OWN/'REPORT.md').open('x') as stream:stream.write(report)
with (OWN/'RESEARCH_LOG.md').open('a') as stream:stream.write('\n'+utc()+' — One data-reader route authenticated all237files14dirs against actual heterogeneous schemas/externalcontrols, exact source+bothcopies code/certificate identities, both actualresults and historicalreceipt streams. Before/after complete metadata equal. Custody100%; no scientific program run or mathematical verdict.\n')
print(json.dumps(dict(status=result['status'],regular_files=237,child_directories=14,hidden_files=result['hidden_regular_files'],empty_files=result['empty_regular_files'],empty_directories=result['empty_directories'],source_code_SHA256=code_pin['SHA256'],source_certificate_SHA256=data_pin['SHA256'],actual_result_SHA256=copies[0]['result']['SHA256'],historical_execution_receipts=receipts,all_source_and_frozen_namespaces_unchanged=True,custody_task_completion_percent=100)))
