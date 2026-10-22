import hashlib,json,pathlib,datetime,sys
here=pathlib.Path(__file__).resolve().parent
f=here/'INPUT_FREEZE.json'
d=json.loads(f.read_text()); out=[]
for e in d['files']+d['external_readonly_inputs']:
 p=pathlib.Path(e['path']); p=p if p.is_absolute() else pathlib.Path(d['root'])/p
 b=p.read_bytes(); actual={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 out.append({'path':str(p),'expected':{'bytes':e['bytes'],'sha256':e['sha256']},'actual':actual,'match':actual['bytes']==e['bytes'] and actual['sha256']==e['sha256']})
r={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'freeze_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'expected_freeze_sha256':'4f4ff36e81cd0e4551d099c0c3bdaba0a5cd82a6805dc83a2561ae0ac34b9cd4','count':len(out),'all_match':all(x['match'] for x in out),'entries':out}
(here/sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n')
print({k:r[k] for k in ['at_utc','freeze_sha256','count','all_match']})
if not r['all_match'] or r['freeze_sha256']!=r['expected_freeze_sha256']:sys.exit(1)
