#!/usr/bin/python3
import pathlib,hashlib,json,datetime
root=pathlib.Path(__file__).resolve().parent
files=[]
for p in sorted(root.rglob('*')):
    rel=p.relative_to(root).as_posix()
    if rel=='authored_manifest.json' or rel.startswith('tmp/'):continue
    assert not p.is_symlink()
    if p.is_file():
        raw=p.read_bytes();files.append({'path':rel,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
(root/'authored_manifest.json').write_text(json.dumps({'schema':'strict-self-excluded-authored-manifest-v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'excluded':['authored_manifest.json','tmp/'],'files':files},indent=2)+'\n')
print(len(files))
