"""Root's fresh exact-control replay; originals remain byte-unchanged."""
from pathlib import Path
import json,hashlib,subprocess,datetime,sys,os
A=Path(__file__).resolve().parent
CHILD=r"""
from pathlib import Path
import sys,hashlib,json,io,contextlib
p=Path(sys.argv[1]);raw=p.read_bytes();saved={};original_write=Path.write_text
def capture(self,data,*args,**kw):
 if self.parent==p.parent and self.name in ['CHECK_RESULTS.json','CHECK_RESULTS_OPT.json']:
  saved[self.name]=json.loads(data);return len(data)
 raise RuntimeError('Unexpected write: '+str(self))
Path.write_text=capture
out=io.StringIO()
try:
 with contextlib.redirect_stdout(out):exec(compile(raw,str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
finally:Path.write_text=original_write
print(json.dumps({'source_sha256':hashlib.sha256(raw).hexdigest(),'optimization':sys.flags.optimize,'captured_result':saved,'stdout':out.getvalue()}))
"""
rows=[]
for opt in [False,True]:
 argv=[sys.executable,'-B']+(['-O'] if opt else [])+['-c',CHILD,str(A/'math_direct_geometry_01/verify_exact_controls.py')]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 r=subprocess.run(argv,capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr)
 item=json.loads(r.stdout);item.update(started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),returncode=r.returncode,command=argv[:3]+['<embedded CHILD>',argv[-1]],stderr=r.stderr)
 z=item['captured_result']['CHECK_RESULTS_OPT.json' if opt else 'CHECK_RESULTS.json']
 if z['checks']!=282 or z['status']!='PASS' or z['script_sha256']!='1f778585d64653a5ea4e8d3b85062053a1f0576a523b3eaab76eb79136be5633':raise RuntimeError('Unexpected control identity')
 rows.append(item)
target=A/'ROOT_EXACT_REPLAY_01.json'
body=(json.dumps({'actual_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'replays':rows,'scope':'282 finite exact geometry controls per mode; explicit exceptions survive -O. No universal theorem inferred.'},indent=2)+'\n').encode()
fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
with os.fdopen(fd,'wb') as f:f.write(body)
print(json.dumps({'receipt':str(target),'sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'checks_per_mode':282}))
