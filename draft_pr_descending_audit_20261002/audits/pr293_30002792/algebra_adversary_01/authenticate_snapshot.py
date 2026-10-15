import hashlib,json,os,pathlib,datetime
W=pathlib.Path(__file__).resolve().parent; A=W.parent
m=json.loads((A/'snapshot_manifest.json').read_bytes())
if hashlib.sha256((A/'snapshot_manifest.json').read_bytes()).hexdigest()!='8fe845421a5802daed352e99b4903797eb7ac98c1bc88592ac639d8f20fb0d1a': raise RuntimeError('manifest pin mismatch')
pins=[]
for f in m['files']:
    p=pathlib.Path(f['snapshot']['path']); b=p.read_bytes()
    expected=f['snapshot']
    if len(b)!=expected['bytes'] or hashlib.sha256(b).hexdigest()!=expected['sha256'] or (p.stat().st_mode&0o777)!=expected['mode']: raise RuntimeError('snapshot changed: '+str(p))
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    if blob!=f['git_blob']: raise RuntimeError('Git blob mismatch')
    pins.append({'path':f['path'],'bytes':len(b),'sha256':expected['sha256'],'git_blob':blob,'mode':expected['mode']})
if m['head']!='6e717193f93c8a321cce1ce35a00eed1ecfb56e7': raise RuntimeError('wrong original head')
print(json.dumps({'status':'PASS_EXACT_ORIGINAL_SNAPSHOT_CUSTODY','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'original_head':m['head'],'snapshot_files':len(pins),'pins':pins},indent=2,sort_keys=True))
