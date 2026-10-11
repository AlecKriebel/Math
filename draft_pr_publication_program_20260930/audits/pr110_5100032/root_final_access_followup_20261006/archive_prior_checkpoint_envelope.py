from pathlib import Path
import datetime,hashlib,json,os,zipfile
D=Path(__file__).resolve().parent;A=D.parent;C=A.parents[2];P=A.parents[1]
source=P/'audits/pr108_30003996/actual_checkpoints/PR110_priority_hold_20261006'
receipt=json.loads((source/'RECEIPT.json').read_text())
if receipt['commit']!='a54913a3c2330a2f9fe31763000cd047df84cd3b' or not receipt['remote_verified']:raise RuntimeError('completed checkpoint')
archive=D/'PR110_priority_hold_completed_operational_envelope.zip'
rows=[]
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in sorted(source.iterdir()):
        if not f.is_file() or f.is_symlink():raise RuntimeError('regular file')
        body=f.read_bytes();name='completed_checkpoint/'+f.name;z.writestr(name,body)
        rows.append({'member':name,'original_path':f.relative_to(C).as_posix(),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
    for f in sorted((A/'actual_operations/priority_hold_scoped_main_checkpoint').iterdir()):
        if not f.is_file() or f.is_symlink():raise RuntimeError('regular outer file')
        body=f.read_bytes();name='completed_outer_execution/'+f.name;z.writestr(name,body)
        rows.append({'member':name,'original_path':f.relative_to(C).as_posix(),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
with zipfile.ZipFile(archive) as z:
    if set(z.namelist())!={r['member'] for r in rows}:raise RuntimeError('members')
    for r in rows:
        b=z.read(r['member'])
        if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256'] or b!=(C/r['original_path']).read_bytes():raise RuntimeError('roundtrip')
body=archive.read_bytes()
r={'schema':'pr110-completed-priority-hold-operation-archive/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'completed_checkpoint':receipt['commit'],'archive':{'path':archive.relative_to(A).as_posix(),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()},'member_count':len(rows),'uncompressed_bytes':sum(r['bytes'] for r in rows),'every_full_member_roundtrip_and_original_equal':True,'original_files_removed':False,'scientific_and_primary_source_files_not_added':True,'reason':'Store completed redundant Git/process prefix streams compactly while preserving every actual envelope byte. Source/proof/audit bodies are already public in their original checkpoint.','members':rows,'workflow_percent':30,'priority_or_publication_clearance':False}
(D/'COMPLETED_PRIOR_CHECKPOINT_ARCHIVE.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='members'}))
