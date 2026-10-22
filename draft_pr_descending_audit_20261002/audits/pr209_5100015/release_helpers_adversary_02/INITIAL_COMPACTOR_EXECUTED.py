from pathlib import Path
import sys,zipfile,hashlib,json,datetime,shutil
D=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr209_5100015/release_helpers_adversary_02')
def sha(b):return hashlib.sha256(b).hexdigest()
for name in ['full_baseline','binding_negatives','wrong_get_range','partial_http','text_decode_loss','append_duplicate','append_unknown','publish_unknown','native_metadata_rejected']:
 root=D/'fixtures'/name
 assert root.parent==D/'fixtures' and root.is_dir() and not root.is_symlink()
 files=sorted(p for p in root.rglob('*') if p.is_file())
 assert all(not p.is_symlink() for p in root.rglob('*'))
 rows=[dict(path=p.relative_to(root).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in files]
 archive=D/('FIXTURE_'+name+'.zip')
 with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p,row in zip(files,rows):z.write(p,row['path'])
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None
  assert z.namelist()==[x['path'] for x in rows]
  for p,row in zip(files,rows):
   body=z.read(row['path']);assert body==p.read_bytes() and len(body)==row['bytes'] and sha(body)==row['sha256']
 receipt=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),owned_root=str(root),archive=dict(path=archive.name,bytes=archive.stat().st_size,sha256=sha(archive.read_bytes())),exact_members_all_bodies_crc_verified=True,member_count=len(rows),members=rows)
 (D/('FIXTURE_'+name+'_MANIFEST.json')).write_text(json.dumps(receipt,indent=2)+'\n')
 shutil.rmtree(root)
 print(name,len(rows),archive.stat().st_size,flush=True)
