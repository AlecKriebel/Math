"""Hash every authored public payload; keep third-party reading aids private."""
from pathlib import Path
import datetime,hashlib,json
base=Path(__file__).resolve().parent
manifest=base/'AUTHORED_MANIFEST.json'
rows=[]
for path in sorted(base.rglob('*')):
    if not path.is_file() or path==manifest or 'private_reading' in path.relative_to(base).parts:
        continue
    data=path.read_bytes()
    rows.append({'path':str(path.relative_to(base)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
manifest.write_text(json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Every public authored payload under the assigned folder; this manifest is self-excluded. Third-party PDFs, full texts, source archives and renderings remain private_reading and are excluded.',
 'payloads':rows,'payload_count':len(rows),'total_payload_bytes':sum(r['bytes'] for r in rows),
 'release_authority':False},indent=2)+'\n')
check=json.loads(manifest.read_text())
for row in check['payloads']:
    data=(base/row['path']).read_bytes()
    assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
print(json.dumps({'payload_count':len(rows),'total_payload_bytes':check['total_payload_bytes'],'all_hashes_match':True}))
