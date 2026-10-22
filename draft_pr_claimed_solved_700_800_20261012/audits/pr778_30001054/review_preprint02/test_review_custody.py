"""Physical negatives and changed-mtime relocation positives for the review seal."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,tempfile
from verify_review import identity,snapshot

scratch=Path(sys.argv[1]);script=Path(__file__).parent/'verify_review.py';rows=[]
for optimized in [False,True]:
    for case in ['baseline','mtime_relocated','hidden_extra','missing','changed','symlink','fifo','emptydir','rewrittenmanifest','wrongpin']:
        with tempfile.TemporaryDirectory(prefix='review02-custody-',dir=scratch) as td:
            r=Path(td)/'packet';r.mkdir();(r/'.hidden').write_text('authored\n');(r/'nested').mkdir();(r/'nested/evidence').write_text('test\n')
            manifest={'schema':'review02-exact-recursive-v1','sealed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'excluded':['MANIFEST.json'],'files':[{'path':n,**v} for n,v in sorted(snapshot(r).items())]}
            raw=(json.dumps(manifest,indent=2)+'\n').encode();(r/'MANIFEST.json').write_bytes(raw);pin=identity(raw)['sha256']
            if case=='mtime_relocated':
                q=Path(td)/'relocated with spaces';shutil.copytree(r,q);r=q
                for p in r.rglob('*'):
                    if p.is_file():os.utime(p,(1000000000,1000000000))
            elif case=='hidden_extra':(r/'.extra').write_text('extra')
            elif case=='missing':(r/'nested/evidence').unlink()
            elif case=='changed':(r/'nested/evidence').write_text('changed')
            elif case=='symlink':(r/'nested/evidence').unlink();(r/'nested/evidence').symlink_to(r/'.hidden')
            elif case=='fifo':os.mkfifo(r/'specialfifo')
            elif case=='emptydir':(r/'empty').mkdir()
            elif case=='rewrittenmanifest':(r/'MANIFEST.json').write_text('{}')
            elif case=='wrongpin':pin='0'*64
            cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(script),'--root',str(r),'--manifest-sha256',pin]
            p=subprocess.run(cmd,cwd='/',capture_output=True)
            expected=case in ('baseline','mtime_relocated')
            if (p.returncode==0)!=expected:raise RuntimeError(case+':'+p.stdout.decode()+p.stderr.decode())
            rows.append({'case':case,'optimized':optimized,'returncode':p.returncode,'result':json.loads(p.stdout)})
print(json.dumps({'status':'PASS','positives':4,'physical_negatives':16,'checks':rows},indent=2))
