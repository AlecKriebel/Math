#!/usr/bin/env python3
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,stat,subprocess,sys,datetime
B=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
S=B/'sources';P=S/'published-source/deep-derived-pure-braids-source-verification-v1.0'
def sha(x):return hashlib.sha256(x).hexdigest()
r=json.loads((S/'receipt.json').read_text());top=[]
for f in r['files']:
 raw=(S/f['name']).read_bytes()
 assert len(raw)==f['bytes'] and sha(raw)==f['sha256'] and hashlib.md5(raw).hexdigest()==f['md5']
 top.append({k:f[k] for k in ['name','bytes','sha256','md5','url']})
archive=S/'deep-derived-pure-braids-source-verification-v1.0.zip'
members=[];names=set()
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for i in z.infolist():
  q=PurePosixPath(i.filename)
  assert not q.is_absolute() and '..' not in q.parts and '\\' not in i.filename
  assert i.filename not in names;names.add(i.filename)
  if i.is_dir():continue
  mode=i.external_attr>>16
  assert not stat.S_ISLNK(mode)
  raw=z.read(i);ex=(P/i.filename).read_bytes()
  assert raw==ex
  members.append({'member':i.filename,'bytes':len(raw),'sha256':sha(raw),'crc32':f'{i.CRC:08x}'})
assert len(members)==213
assert (P/'note.pdf').read_bytes()==(S/'deep-derived-pure-braids-v1.0.pdf').read_bytes()
prim=[]
for row in json.loads((B/'reviews/scope/primary-source-receipts.json').read_text()):
 raw=(B/'reviews/scope/cache/primary-sources'/row['name']).read_bytes()
 assert sha(raw)==row['sha256'] and len(raw)==row['bytes']
 prim.append({k:row[k] for k in ['name','url','version','bytes','sha256']})
record=json.loads((S/'record.json').read_text())
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'record_sha256':sha((S/'record.json').read_bytes()),'receipt_sha256':sha((S/'receipt.json').read_bytes()),'metadata':{'id':record['id'],'version':record['metadata']['version'],'publication_date':record['metadata']['publication_date'],'created':record['created'],'updated':record['updated']},'public_assets':top,'archive_crc_ok':True,'member_count':len(members),'members_match_extraction':True,'members':members,'primary_sources':prim,'embedded_note_pdf_matches_public_pdf':True,'historical_files_handling':'Names, sizes, raw bytes and hashes only; no historical assessment contents interpreted.'}
(O/'custody.json').write_text(json.dumps(result,indent=2)+'\n')
manifest_sha=sha((P/'PACKAGE_MANIFEST.json').read_bytes())
cmd=[sys.executable,'-I','-B',str(P/'verify_package.py'),'--expected-manifest',manifest_sha,'--pdf',str(S/'deep-derived-pure-braids-v1.0.pdf'),'--workdir',str(B/'reviews/adversarial/replay-work')]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.run(cmd,capture_output=True,text=True,timeout=600)
(O/'package-replay.stdout.json').write_text(p.stdout)
(O/'package-replay.stderr.log').write_text(p.stderr)
receipt={'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'returncode':p.returncode,'manifest_sha256':manifest_sha,'stdout_sha256':sha(p.stdout.encode()),'stderr_sha256':sha(p.stderr.encode())}
for f in r['files']:assert sha((S/f['name']).read_bytes())==f['sha256']
for m in members:assert sha((P/m['member']).read_bytes())==m['sha256']
receipt['all_source_bytes_unchanged_after_replay']=True
(O/'package-replay-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
assert p.returncode==0
