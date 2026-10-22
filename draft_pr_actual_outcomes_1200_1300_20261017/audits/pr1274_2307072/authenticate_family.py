"""Authenticate one explicitly selected authored-family manifest, never receipt paths."""
import datetime, hashlib, json, pathlib, sys

A=pathlib.Path(__file__).resolve().parent
family=sys.argv[1]
entries_key=sys.argv[2] if len(sys.argv)>2 else 'authored_files'
path_key=sys.argv[3] if len(sys.argv)>3 else 'path'
size_key=sys.argv[4] if len(sys.argv)>4 else 'bytes'
base=A/family
manifest=base/'MANIFEST.json'

def member(raw):
    p=pathlib.PurePosixPath(raw)
    if not isinstance(raw,str) or p.is_absolute() or str(p)!=raw or any(c in ('','.','..') for c in p.parts):
        raise ValueError('Noncanonical member')
    cur=base
    for part in p.parts:
        if part not in {x.name for x in cur.iterdir()}:
            raise ValueError('Missing or case-aliased member: '+raw)
        cur=cur/part
        if cur.is_symlink(): raise ValueError('Symlink member: '+raw)
    if not cur.is_file(): raise ValueError('Not a regular member: '+raw)
    return cur

if manifest.is_symlink(): raise ValueError('Manifest symlink')
obj=json.loads(manifest.read_text())
rows=obj[entries_key]
if not isinstance(rows,list) or not rows: raise ValueError('Empty authored membership')
seen=set()
for r in rows:
    raw=r[path_key]
    if raw in seen or raw=='MANIFEST.json': raise ValueError('Duplicate/self member')
    seen.add(raw)
    p=member(raw); b=p.read_bytes()
    if len(b)!=r[size_key] or hashlib.sha256(b).hexdigest()!=r['sha256']:
        raise ValueError('Changed member: '+raw)
print(json.dumps(dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    status='PASS',family=family,manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),
    explicit_members=len(rows),entries_key=entries_key,path_key=path_key,size_key=size_key,
    member_paths=sorted(seen),scope='Physical exact-case regular authored manifest members only. Input/source receipts were not promoted into membership. Byte authentication alone is not mathematical or provenance validation.'),indent=2))
