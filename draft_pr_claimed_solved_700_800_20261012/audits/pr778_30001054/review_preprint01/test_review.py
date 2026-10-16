"""Physical, relocated corruption controls for verify_review.py, using owned scratch."""
from pathlib import Path
import tempfile,hashlib,json,sys,subprocess,os,datetime
B=Path(__file__).resolve().parent
base={p.name:p.read_bytes() for p in B.iterdir() if p.is_file() and p.name not in ['MANIFEST.json','REVIEW_GUARD_RESULTS.json']}
def need(x,m):
 if not x:raise RuntimeError(m)
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
rows=[]
for opt in [False,True]:
 for case in ['relocated','mtime_changed','extra_hidden','missing','changed','symlink','fifo','empty_directory','wrong_external_pin']:
  with tempfile.TemporaryDirectory(dir=B,prefix='owned-review-control-') as temp:
   root=Path(temp)/'relocated review with spaces';root.mkdir()
   for n,raw in base.items():(root/n).write_bytes(raw)
   manifest=json.dumps({'schema':1,'files':{n:ident(raw) for n,raw in sorted(base.items())}},indent=2).encode()+b'\n'
   (root/'MANIFEST.json').write_bytes(manifest);pin=ident(manifest)['sha256']
   q=root/'REPORT.md'
   if case=='mtime_changed':
    for p in root.iterdir():os.utime(p,(946684800,946684800))
   elif case=='extra_hidden':(root/'.extra').write_bytes(b'extra')
   elif case=='missing':q.unlink()
   elif case=='changed':q.write_bytes(q.read_bytes()+b'changed')
   elif case=='symlink':q.unlink();q.symlink_to(B/'REPORT.md')
   elif case=='fifo':os.mkfifo(root/'special')
   elif case=='empty_directory':(root/'empty').mkdir()
   elif case=='wrong_external_pin':pin='0'*64
   cmd=[sys.executable,'-E','-s','-B']+(['-O'] if opt else [])+[str(root/'verify_review.py'),'--manifest-sha256',pin]
   r=subprocess.run(cmd,cwd='/',capture_output=True,timeout=30)
   need((r.returncode==0)==(case in ['relocated','mtime_changed']),'wrong guard '+case)
   rows.append({'mode':'O' if opt else 'normal','case':case,'returncode':r.returncode,'PASS':True})
print(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','positive_controls':4,'negative_controls':14,'own_temporary_fixtures_removed':True,'rows':rows},indent=2))
