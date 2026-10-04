from pathlib import Path
import json,hashlib,datetime
root=Path(__file__).resolve().parent
files=[]
for p in sorted(root.rglob('*')):
 if not p.is_file() or 'ignoredtmp' in p.relative_to(root).parts or p.name=='FAMILY_MANIFEST.json':continue
 assert not p.is_symlink(),str(p)
 b=p.read_bytes();files.append({'path':str(p.relative_to(root)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(root/'FAMILY_MANIFEST.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':'980719c79e13ffbc3f5cfbf149c325ea2fb51df0','excluded':['FAMILY_MANIFEST.json','ignoredtmp/**'],'files':files},indent=2)+'\n')
print(len(files))
