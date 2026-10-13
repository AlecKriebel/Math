from pathlib import Path, PurePosixPath
import json, hashlib, zipfile, sys, datetime
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
names=['outer_pedal_centroid.tex','outer_pedal_centroid.pdf','metadata.json','zenodo-deposit.json','README.md','outer-pedal-centroid-verification.zip']
pins={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[]}
for name in names:
 p=BASE/name
 data=p.read_bytes()
 pins['files'].append({'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(HERE/'REVIEWED_HASHES.json').write_text(json.dumps(pins,indent=2)+'\n')
with zipfile.ZipFile(BASE/names[-1]) as z:
 assert z.testzip() is None
 for zi in z.infolist():
  parts=PurePosixPath(zi.filename).parts
  assert not zi.filename.startswith('/') and '..' not in parts
  assert (zi.external_attr>>16)&0o170000 != 0o120000, 'symlink'
 z.extractall(HERE/'extracted')
PACKAGE=HERE/'extracted/outer-pedal-centroid-verification'
manifest=json.loads((PACKAGE/'MANIFEST.json').read_text())
paths=set()
for row in manifest['files']:
 data=(PACKAGE/row['path']).read_bytes()
 assert len(data)==row['bytes']
 assert hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
 paths.add(row['path'])
actual={str(p.relative_to(PACKAGE)) for p in PACKAGE.rglob('*') if p.is_file()}
assert actual==paths|{'MANIFEST.json'},(actual-paths,paths-actual)
assert (PACKAGE/'paper/outer_pedal_centroid.tex').read_bytes()==(BASE/names[0]).read_bytes()
for n in ['metadata.json','README.md','requirements.txt','LICENSE','run_verification.py']:
 assert (PACKAGE/n).read_bytes()==(BASE/n).read_bytes()
md=json.loads((BASE/'metadata.json').read_text())
dep=json.loads((BASE/'zenodo-deposit.json').read_text())
assert dep['metadata']==md
assert [r['path'] for r in dep['files']]==['outer_pedal_centroid.pdf','outer-pedal-centroid-verification.zip']
receipt={'zip_crc':'PASS','path_safety':'PASS','manifest_entries':len(paths),'complete_manifest':'PASS','paper_source_identical':'PASS','metadata_identical':'PASS','deposit_metadata_consistent':'PASS','runtime':sys.version,'executable':sys.executable}
(HERE/'EXTRACTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
