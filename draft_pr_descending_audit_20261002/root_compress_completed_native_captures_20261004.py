"""Losslessly archive only large, completed, untracked root capture streams."""
from pathlib import Path
import datetime, gzip, hashlib, json, os, subprocess
P=Path(__file__).resolve().parent; R=P.parent
tracked=set(subprocess.check_output(['git','ls-files','-z'],cwd=R).split(b'\0'))
groups={}
for a in (P/'audits').glob('pr*'):
    if a.name=='pr356_30001552': continue
    for d in a.glob('root*_private'):
        if not d.is_dir(): continue
        for f in d.rglob('*'):
            if not f.is_file() or f.is_symlink(): continue
            s=f.stat()
            if f.suffix!='.stdout' or s.st_size<10_000_000: continue
            if str(f.relative_to(R)).encode() in tracked: continue
            groups.setdefault(s.st_ino,[]).append(f)
receipt=P/'ROOT_COMPLETED_NATIVE_CAPTURE_COMPRESSION_20261004T0228.json'
assert not receipt.exists()
data={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'scope':'Completed untracked root*_private native .stdout streams above10MB; active PR356, agent namespaces, sources, tracked and foreign files excluded.',
      'restoration':'Old capture paths require gzip decompression to recorded paths/modes before legacy validators are used. Every original byte remains preserved.',
      'status':'PREPARED','groups':[]}
def save(): receipt.write_text(json.dumps(data,indent=2)+'\n')
save()
for inode,paths in sorted(groups.items(),key=lambda item:item[1][0].stat().st_size):
    first=paths[0]; s=first.stat()
    if s.st_nlink!=len(paths): continue  # Never unlink a group with an unknown owner.
    body=first.read_bytes(); digest=hashlib.sha256(body).hexdigest()
    assert all(f.read_bytes()==body and f.stat().st_ino==inode and f.stat().st_mode&0o7777==s.st_mode&0o7777 for f in paths)
    archive=first.with_name(first.name+'.rootstorage.gz'); assert not archive.exists()
    row={'state':'PREPARED','original_paths':[str(f.relative_to(R)) for f in paths],
         'bytes':len(body),'sha256':digest,'mode':s.st_mode&0o7777,'archive':str(archive.relative_to(R))}
    data['groups'].append(row); save()
    try:
        with archive.open('xb') as out:
            with gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0,compresslevel=6) as z: z.write(body)
            out.flush(); os.fsync(out.fileno())
        assert gzip.decompress(archive.read_bytes())==body
        row.update(state='VERIFIED_ARCHIVE_ORIGINALS_PRESENT',archive_bytes=archive.stat().st_size,
                   archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest()); save()
    except Exception as exc:
        assert all(f.read_bytes()==body for f in paths)
        row.update(state='FAILED_ORIGINALS_PRESERVED',error=repr(exc))
        if archive.exists(): archive.unlink()
        save(); raise
    for f in paths: f.unlink()
    assert gzip.decompress(archive.read_bytes())==body
    row['state']='COMPLETE_LOSSLESS_ORIGINAL_PATHS_REQUIRE_RESTORATION'; save()
data.update(status='COMPLETE_ALL_ARCHIVES_VERIFIED',finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
save(); print(json.dumps(data,indent=2))
