"""Preserve history, pin current bytes, capture a real closer, finish and seal."""
import datetime, hashlib, importlib, json, os, pathlib, shutil, stat, subprocess, sys
root=pathlib.Path(__file__).resolve().parent
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(path):
    h=hashlib.sha256()
    with pathlib.Path(path).open('rb') as inp:
        for data in iter(lambda:inp.read(1024*1024),b''): h.update(data)
    return h.hexdigest()
def body(path):
    p=pathlib.Path(path)
    return dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=sha(p))
def dump(path,value):
    pathlib.Path(path).write_text(json.dumps(value,indent=2)+'\n')
if sys.flags.optimize: raise RuntimeError('optimization is not allowed')
old_manifest=root/'NAMESPACE_CLOSURE.json'
old_checksum=root/'NAMESPACE_CLOSURE.sha256'
old_manifest_bytes=old_manifest.read_bytes()
old_checksum_bytes=old_checksum.read_bytes()
old_digest=hashlib.sha256(old_manifest_bytes).hexdigest()
if old_digest!='5636d9b9da40879683ea4d7a83ac0d0c949c4012ab8e8dd2cde303cd6c54ba35':
    raise RuntimeError('unexpected original manifest')
if not old_checksum_bytes.decode().startswith(old_digest+'  '):
    raise RuntimeError('original checksum mismatch')
original=json.loads(old_manifest_bytes)
for row in original['payload_files']:
    p=root/row['path']
    if p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:
        raise RuntimeError('original payload changed: '+row['path'])
# Preserve exact old bytes before generating any new manifest or custody pins.
history=root/'historical_closure_20261005_053158'
history.mkdir(exist_ok=False)
(history/'NAMESPACE_CLOSURE.json').write_bytes(old_manifest_bytes)
(history/'NAMESPACE_CLOSURE.sha256').write_bytes(old_checksum_bytes)
dump(history/'PRESERVATION.json',dict(preserved_utc=utc(),original_manifest_sha256=old_digest,
     original_checksum_sha256=hashlib.sha256(old_checksum_bytes).hexdigest(),
     original_payload_count=len(original['payload_files']),original_payload_hashes_verified=True,
     original_paths_retained_unchanged=True,history_copies_exact=True))

exe=pathlib.Path(sys.executable).resolve()
program_specs=[('actual_closer_python_executable',exe)]
framework=exe.parent.parent/'Python'
if framework.is_file(): program_specs.append(('python_framework_runtime_library',framework))
for record in sorted((root/'process_evidence').glob('*/execution.json')):
    r=json.loads(record.read_text())
    current=shutil.which(r['argv'][0]) if not pathlib.Path(r['argv'][0]).is_absolute() else r['argv'][0]
    if current: program_specs.append(('current_resolution_of_historical_argv0',pathlib.Path(current).resolve()))
for name in ('subprocess','hashlib','json','pathlib','shutil','stat','sysconfig','datetime','_hashlib','_posixsubprocess','_json','_datetime'):
    module=importlib.import_module(name)
    path=getattr(module,'__file__',None)
    if path and pathlib.Path(path).is_file():
        program_specs.append(('selected_current_runtime_module:'+name,pathlib.Path(path).resolve()))
for p in sorted(root.glob('*.py')):
    program_specs.append(('current_recorder_or_child_program',p.resolve()))
seen={}
for role,p in program_specs:
    key=str(p)
    if key in seen:
        seen[key]['roles'].append(role); continue
    before=p.stat(); digest=sha(p); after=p.stat()
    if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
        raise RuntimeError('file changed during current-time pin: '+key)
    seen[key]=dict(resolved_path=key,roles=[role],bytes=after.st_size,sha256=digest,
                   current_stat_mtime_ns=after.st_mtime_ns,pinned_utc=utc(),copied=False)
dump(root/'CURRENT_CLOSURE_CUSTODY.json',dict(pinned_utc=utc(),python_version=sys.version,
     python_optimization_level=sys.flags.optimize,observed_files=list(seen.values()),
     scope='Current-time full-file pins of the specifically listed executables/runtime files/scripts only; not a retrospective historical launch capture or exhaustive transitive runtime manifest.',
     historical_capture_scope='Actual child PID/argv/cwd/UTC/full stdout/stderr/exit and recorder SHA; no whole executable/runtime or child-program byte pins at each old launch. Historical records untouched.'))
dump(root/'SEAL_CHECKPOINT.json',dict(utc=utc(),validation_completion_percent=100,
     work='Additive custody checkpoint and physical seal only; no substantive report/source or original body changes.',
     original_manifest_sha256=old_digest,original_payload_count=95,original_payload_hashes_verified=True))

capture=root/'process_evidence/physical_seal'
capture.mkdir(exist_ok=False)
final_manifest=root/'FINAL_SEALED_NAMESPACE.json'
final_checksum=root/'FINAL_SEALED_NAMESPACE.sha256'
prepared=[capture/'stdout.bin',capture/'stderr.bin',capture/'execution.json',final_manifest,final_checksum]
(root/'PHYSICAL_SEAL_RESULT.json').write_bytes(b'')
fds={p:p.open('wb') for p in prepared}
argv=[str(exe),str(root/'physical_seal.py')]
started=utc()
try:
    child=subprocess.Popen(argv,cwd=str(root),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    actual_pid=child.pid
    stdout,stderr=child.communicate()
    finished=utc()
    for p,data in ((capture/'stdout.bin',stdout),(capture/'stderr.bin',stderr)):
        fds[p].write(data); fds[p].flush(); os.fsync(fds[p].fileno())
    execution=dict(recorder_actual_pid=os.getpid(),recorder_argv=sys.argv,actual_child_pid=actual_pid,
        argv=argv,cwd=str(root),started_utc=started,finished_utc=finished,exit_code=child.returncode,
        recorder_current_sha256=sha(root/'capture_and_seal.py'),child_program_current_sha256=sha(root/'physical_seal.py'),
        current_executable_sha256=sha(exe),current_time_pins='CURRENT_CLOSURE_CUSTODY.json',
        historical_pin_claim=False,
        stdout=dict(bytes=len(stdout),sha256=hashlib.sha256(stdout).hexdigest()),
        stderr=dict(bytes=len(stderr),sha256=hashlib.sha256(stderr).hexdigest()))
    fds[capture/'execution.json'].write((json.dumps(execution,indent=2)+'\n').encode())
    fds[capture/'execution.json'].flush(); os.fsync(fds[capture/'execution.json'].fileno())
    if child.returncode: raise RuntimeError('closer failed; exact streams and exit are retained')
    for row in original['payload_files']:
        if sha(root/row['path'])!=row['sha256']: raise RuntimeError('historical body changed during seal')
    if old_manifest.read_bytes()!=old_manifest_bytes or old_checksum.read_bytes()!=old_checksum_bytes:
        raise RuntimeError('original closure changed')
    admins={'FINAL_SEALED_NAMESPACE.json','FINAL_SEALED_NAMESPACE.sha256'}
    rows=[]
    directories=[]
    for p in sorted(root.rglob('*')):
        if p.is_symlink(): raise RuntimeError('unexpected symlink')
        mode=format(stat.S_IMODE(p.stat().st_mode),'04o')
        rel=str(p.relative_to(root))
        if p.is_file():
            if mode!='0444': raise RuntimeError('file mode incorrect: '+rel)
            if rel not in admins: rows.append(dict(**body(p),mode=mode))
        elif p.is_dir():
            if mode!='0555': raise RuntimeError('directory mode incorrect: '+rel)
            directories.append(dict(path=rel,mode=mode))
        else: raise RuntimeError('unexpected filesystem object')
    root_mode=format(stat.S_IMODE(root.stat().st_mode),'04o')
    if root_mode!='0555': raise RuntimeError('root mode incorrect')
    manifest=dict(frozen_utc=utc(),root=str(root),root_mode=root_mode,
        payload_file_count=len(rows),total_file_count=len(rows)+2,payload_bytes=sum(r['bytes'] for r in rows),
        directory_count_excluding_root=len(directories),directories=directories,payload_files=rows,
        administrative_files=[dict(path=p,mode='0444',bytes=None,sha256=None,
            reason='Administrative self-reference exclusion; final manifest SHA emitted by closer wrapper and stored in FINAL_SEALED_NAMESPACE.sha256.') for p in sorted(admins)],
        physical_seal=dict(actual_child_pid=actual_pid,capture='process_evidence/physical_seal',exit_code=child.returncode,
            files_mode='0444',directories_mode='0555',all_actual_modes_verified=True,
            write_descriptor_completion='All opened administrative write descriptors are closed before success is reported.'),
        preserved_history=dict(original_manifest_sha256=old_digest,original_payload_count=95,
            original_payload_hashes_unchanged=True,original_manifest_paths_unchanged=True,
            copies='historical_closure_20261005_053158'),
        custody_scope='See FINAL_CUSTODY_SCOPE.md and CURRENT_CLOSURE_CUSTODY.json. Historical launch binaries/runtime bytes are not retrospectively authenticated.',
        exact_namespace_rule='Exactly listed payload files, two administrative files, and listed directories plus root; no unlisted objects admitted.')
    data=(json.dumps(manifest,indent=2)+'\n').encode()
    digest=hashlib.sha256(data).hexdigest()
    fds[final_manifest].write(data); fds[final_manifest].flush(); os.fsync(fds[final_manifest].fileno())
    fds[final_checksum].write((digest+'  FINAL_SEALED_NAMESPACE.json\n').encode())
    fds[final_checksum].flush(); os.fsync(fds[final_checksum].fileno())
finally:
    for handle in fds.values(): handle.close()
# Independent last verification occurs after all administrative write handles close.
actual_files={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
if actual_files!={r['path'] for r in rows}|admins: raise RuntimeError('namespace membership changed')
for p in root.rglob('*'):
    expected=0o444 if p.is_file() else 0o555
    if stat.S_IMODE(p.stat().st_mode)!=expected: raise RuntimeError('post-close mode mismatch')
if stat.S_IMODE(root.stat().st_mode)!=0o555: raise RuntimeError('post-close root mode mismatch')
if sha(final_manifest)!=digest: raise RuntimeError('final manifest checksum mismatch')
print(json.dumps(dict(final_namespace_sha256=digest,total_files=len(actual_files),
    directories_excluding_root=len(directories),payload_files=len(rows),payload_bytes=manifest['payload_bytes'],
    file_modes='0444',directory_modes='0555',root_mode='0555',captured_closer_pid=actual_pid,
    capture_execution_sha256=sha(capture/'execution.json'),current_custody_sha256=sha(root/'CURRENT_CLOSURE_CUSTODY.json'),
    physical_result_sha256=sha(root/'PHYSICAL_SEAL_RESULT.json'),original_namespace_sha256=old_digest,
    historical_95_payload_pins_unchanged=True,all_administrative_write_descriptors_closed=True,
    final_namespace_and_modes_verified=True)))
