#!/usr/bin/env python3
import datetime, hashlib, json, os, pathlib, subprocess
D=pathlib.Path(__file__).resolve().parent
P=D/'private_sources'/'takagi_1105.0072v1.pdf'; R=D/'private_renders'; R.mkdir(exist_ok=True)
def ck(b,m):
    if not b: raise ValueError(m)
def pin(path):
    b=path.read_bytes(); return {'relative_path':str(path.relative_to(D)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
J={'schema':'pr117-first-prior-version-renders/v1','pid':os.getpid(),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'events':[],'source_pin':pin(P)}
ck(J['source_pin']['sha256']=='24f38aecbf9b40edfa7ec223a08694f60934c41f13e213e9549883a8111eaa7c','Version1 source pin')
for num in [18,19]:
    out=R/('takagi_1105.0072v1_physical_p'+str(num))
    argv=['/opt/homebrew/bin/pdftoppm','-f',str(num),'-l',str(num),'-singlefile','-r','180','-png',str(P),str(out)]
    res=subprocess.run(argv,capture_output=True,timeout=40,env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'})
    ck(res.returncode==0 and len(res.stderr)==0,'Version1 render must succeed')
    J['events'].append({'argv':argv,'returncode':res.returncode,'stderr_bytes':len(res.stderr),'physical_page_1_based':num,**pin(pathlib.Path(str(out)+'.png'))})
J['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat(); J['status']='PASS'
(D/'FIRST_PRIOR_VERSION_RENDER_RECEIPT.json').write_text(json.dumps(J,indent=2,sort_keys=True)+'\n')
print(json.dumps({'pid':os.getpid(),'status':J['status'],'rendered_pages':[18,19]},sort_keys=True))
