from pathlib import Path, PurePosixPath
from urllib.request import Request,urlopen
from datetime import datetime, timezone
import hashlib,json,tarfile,io,zipfile
base=Path(__file__).resolve().parents[2]; out=base/'sources'; out.mkdir(parents=True,exist_ok=True)
now=lambda:datetime.now(timezone.utc).isoformat()
url='https://zenodo.org/api/records/22089807'
with urlopen(Request(url,headers={'User-Agent':'Research catalogue verification'}),timeout=60) as r: raw=r.read()
(out/'record-raw.json').write_bytes(raw); record=json.loads(raw)
public={k:record[k] for k in ('id','conceptrecid','doi','metadata','files','created','updated') if k in record}
(out/'record.json').write_text(json.dumps(public,indent=2)+'\n')
q=json.loads((base.parents[1]/'reconciliation/queue.json').read_text()); entry=next(x for x in q['queue'] if x['record_id']==22089807)
(out/'queue-entry.json').write_text(json.dumps(entry,indent=2)+'\n')
receipt={'record_id':'22089807','retrieved_utc':now(),'api_url':url,'api_sha256':hashlib.sha256(raw).hexdigest(),'files':[],'queue_check':[]}
expected={x['filename']:{'size':x.get('expected_bytes',x.get('filesize')),'md5':x.get('expected_md5',x.get('checksum'))} for x in entry['sources']+entry['supporting_files']}
for f in record['files']:
 name=f['key']; assert PurePosixPath(name).name==name
 url=f['links'].get('self') or f['links']['content']
 with urlopen(Request(url,headers={'User-Agent':'Research catalogue verification'}),timeout=120) as r: data=r.read()
 alg,check=f['checksum'].split(':',1); assert hashlib.new(alg,data).hexdigest()==check; assert len(data)==f['size']; (out/name).write_bytes(data)
 sha=hashlib.sha256(data).hexdigest(); receipt['files'].append({'name':name,'url':url,'bytes':len(data),'sha256':sha,'zenodo_checksum':f['checksum'],'retrieved_utc':now()})
 assert name in expected; assert len(data)==expected[name]['size']; assert hashlib.md5(data).hexdigest()==expected[name]['md5']
 receipt['queue_check'].append({'filename':name,'size_match':True,'md5_match':True})
assert set(expected)=={f['name'] for f in receipt['files']}
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
inventory=[]; dest=out/'published-source'; dest.mkdir(exist_ok=True)
for f in receipt['files']:
 p=out/f['name']
 if tarfile.is_tarfile(p):
  with tarfile.open(p) as arc:
   for i,m in enumerate(arc.getmembers()):
    assert not m.issym() and not m.islnk() and not m.isdev(); assert not PurePosixPath(m.name).is_absolute() and '..' not in PurePosixPath(m.name).parts
    data=arc.extractfile(m).read() if m.isfile() else b''
    inventory.append({'archive':f['name'],'index':i,'name':m.name,'type':'file' if m.isfile() else 'directory','bytes':m.size,'sha256':hashlib.sha256(data).hexdigest() if m.isfile() else None,'hidden':any(x.startswith('.') for x in PurePosixPath(m.name).parts)})
   arc.extractall(dest,filter='data')
(base/'reviews/scope/archive_inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
print(json.dumps(receipt,indent=2)); print('Archive members',len(inventory))
