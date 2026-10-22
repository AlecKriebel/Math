from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,datetime,stat
B=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr209_5100015/preprint');O=B.parent/'whole_package_adversary_01';s=json.loads((B/'SOURCE_MANIFEST.json').read_text());prefix='k303b_outer_center_pedal_product/'
with zipfile.ZipFile(B/'k303b-source-verification.zip') as z:
 rows=[]
 for i in z.infolist():
  assert i.filename.startswith(prefix)
  p=i.filename[len(prefix):];d=z.read(i);raw=(B/p).read_bytes()
  rows.append(dict(path=p,bytes=len(d),sha256=hashlib.sha256(d).hexdigest(),byte_identical=d==raw,safe=not PurePosixPath(p).is_absolute() and '..' not in PurePosixPath(p).parts and not stat.S_ISLNK(i.external_attr>>16)))
 result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),correction='Initial literal path comparison was intentionally unresolved in scope freeze; archive has a single documented top-level prefix, not a mismatch.',prefix=prefix,entries=len(rows),membership={r['path'] for r in rows}=={r['path'] for r in s['files']}|{'SOURCE_MANIFEST.json'},all_byte_identical=all(r['byte_identical'] for r in rows),all_safe=all(r['safe'] for r in rows),crc_test=z.testzip(),rows=rows)
(O/'ZIP_NORMALIZED.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='rows'})
