"""Freeze every completed payload; explicit administrative self-hash exclusions."""
import datetime, hashlib, json, os, pathlib, sys
root=pathlib.Path(__file__).resolve().parent
admin={'NAMESPACE_CLOSURE.json','NAMESPACE_CLOSURE.sha256'}
files=[]
for p in sorted(root.rglob('*')):
 if p.is_file() and str(p.relative_to(root)) not in admin:
  data=p.read_bytes()
  files.append(dict(path=str(p.relative_to(root)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
dirs=sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_dir())
result=dict(frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            root=str(root),freeze_process=dict(actual_pid=os.getpid(),argv=sys.argv,cwd=os.getcwd()),
            payload_file_count=len(files),payload_bytes=sum(r['bytes'] for r in files),
            directories=dirs,payload_files=files,
            administrative_files=[dict(path=p,sha256=None,reason='Self-reference excluded; manifest digest emitted by builder and stored in NAMESPACE_CLOSURE.sha256.') for p in sorted(admin)],
            closed_namespace_rule='Exactly the listed payload files, directories, and two administrative files. No other file is admitted.',
            capture_scope='All primary-source retrieval/extraction/OCR and numerical/final control procedures have recorded child process custody. Initial informal reads/web searches and this administrative namespace build use tool transport; no invented subprocess exit record.')
data=(json.dumps(result,indent=2)+'\n').encode()
(root/'NAMESPACE_CLOSURE.json').write_bytes(data)
digest=hashlib.sha256(data).hexdigest()
(root/'NAMESPACE_CLOSURE.sha256').write_text(digest+'  NAMESPACE_CLOSURE.json\n')
expected={r['path'] for r in files}|admin
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
assert actual==expected
assert not any(p.is_symlink() for p in root.rglob('*'))
print(json.dumps(dict(namespace_sha256=digest,payload_files=len(files),payload_bytes=result['payload_bytes'],actual_freeze_pid=os.getpid(),namespace_verified=True)))
