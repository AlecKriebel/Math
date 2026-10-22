from pathlib import Path
import json,hashlib,zipfile,stat,datetime,gzip,urllib.request,urllib.parse
P=Path(__file__).resolve().parent;S=P.parent/'publication_preparation_01'
mbytes=(S/'MANIFEST.json').read_bytes();m=json.loads(mbytes)
print('manifest schema',list(m));print('manifest digest',hashlib.sha256(mbytes).hexdigest())
print(json.dumps(m,indent=2)[:1400])
result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'package_manifest_sha256':hashlib.sha256(mbytes).hexdigest(),'pinned_expected':'aac44c2eb49dedf439702123c32e202f43b926a240651886a76b74e51152144f'}
entries=m.get('members',m.get('files',[]));entries=[dict(path=k,**v) for k,v in entries.items()] if isinstance(entries,dict) else entries;seen=[]
for e in entries:
 q=S/e['path'];b=q.read_bytes();d=hashlib.sha256(b).hexdigest()
 if d!=e['sha256'] or len(b)!=e.get('bytes',e.get('size')):raise RuntimeError('manifest mismatch '+str(q))
 seen.append(e['path'])
actual={str(q.relative_to(S)) for q in S.rglob('*') if q.is_file() and q.name!='MANIFEST.json'}
if actual!=set(seen):raise RuntimeError('closure mismatch '+str(actual^set(seen)))
result.update({'closed_members':len(entries),'bytes':sum((S/x).stat().st_size for x in seen),'closure_valid':True})
archives=[]
for q in sorted((S/'release').glob('*.zip')):
 with zipfile.ZipFile(q) as z:
  names=z.namelist()
  if len(names)!=len(set(names)) or any(Path(n).is_absolute() or '..' in Path(n).parts for n in names):raise RuntimeError('unsafe archive')
  if z.testzip():raise RuntimeError('bad zip')
  details=[]
  for n in names:
   b=z.read(n);details.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
  archives.append({'path':str(q.relative_to(S)),'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'members':details})
result['archives']=archives
(P/'PACKAGE_INTEGRITY.json').write_text(json.dumps(result,indent=2)+'\n')
print('closure',len(entries),result['bytes']);print('archives',[(x['path'],len(x['members'])) for x in archives])
