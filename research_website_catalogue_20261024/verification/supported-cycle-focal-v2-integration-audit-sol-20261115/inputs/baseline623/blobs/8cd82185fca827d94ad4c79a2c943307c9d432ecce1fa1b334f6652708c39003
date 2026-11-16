"""Acquire one public Zenodo paper without altering its archived bytes."""
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone
from zipfile import ZipFile
import hashlib, json, sys

ROOT = Path(__file__).resolve().parents[1]
record_id = str(int(sys.argv[1]))
folder = ROOT / 'papers' / record_id / 'sources'
folder.mkdir(parents=True, exist_ok=True)
with urlopen(Request(f'https://zenodo.org/api/records/{record_id}', headers={'User-Agent':'Research catalogue verification'}), timeout=45) as response:
    record = json.load(response)
public = {k: record[k] for k in ('id','conceptrecid','doi','metadata','files','created','updated') if k in record}
(folder/'record.json').write_text(json.dumps(public, indent=2)+'\n')
receipt = {'record_id':record_id,'retrieved_utc':datetime.now(timezone.utc).isoformat(),'files':[]}
zip_count = sum(x['key'].lower().endswith('.zip') for x in record.get('files', []))
for item in record.get('files',[]):
    name = item['key']
    if Path(name).name != name or not name.lower().endswith(('.pdf','.zip','.md','.txt','.sha256')):
        continue
    if item.get('size', 0)>50*1024*1024:
        raise RuntimeError('Inspect large archive before download')
    url = item['links'].get('self') or item['links']['content']
    with urlopen(Request(url, headers={'User-Agent':'Research catalogue verification'}), timeout=60) as response:
        data = response.read(50*1024*1024+1)
    algorithm, expected = item['checksum'].split(':',1)
    assert hashlib.new(algorithm,data).hexdigest()==expected
    assert len(data)==item['size']
    (folder/name).write_bytes(data)
    receipt['files'].append({'name':name,'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'zenodo_checksum':item['checksum']})
    if name.endswith('.zip'):
        destination=folder/'published-source'
        if zip_count > 1:
            destination=destination/Path(name).stem
        with ZipFile(folder/name) as archive:
            assert sum(x.file_size for x in archive.infolist())<100*1024*1024
            for member in archive.infolist():
                resolved=(destination/member.filename).resolve()
                assert resolved.is_relative_to(destination.resolve())
                assert (member.external_attr>>16)&0o170000 != 0o120000
            archive.extractall(destination)
(folder/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
