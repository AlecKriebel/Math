"""Publication gate negative controls; mutations exist only in temporary trees."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('REJECT: controls require -I -S -B')
import hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path
LAUNCHER="""import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode): raise SystemExit('REJECT: require -I -S -B')
import hashlib,pathlib,stat
r=pathlib.Path(sys.argv[1]); p=r/'bootstrap.py'
for q in (r,*r.parents):
    if not stat.S_ISDIR(q.lstat().st_mode): raise SystemExit('REJECT: root ancestry')
s=p.lstat()
if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1: raise SystemExit('REJECT: bootstrap type')
b=p.read_bytes()
if hashlib.sha256(b).hexdigest()!=sys.argv[3]: raise SystemExit('REJECT: bootstrap anchor')
sys.argv=[str(p),str(r),sys.argv[2],*sys.argv[4:]]
exec(compile(b,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
"""
def need(ok,msg):
    if not ok:raise ValueError(msg)
root=Path(__file__).parent;pin=sys.argv[2];bp=hashlib.sha256((root/'bootstrap.py').read_bytes()).hexdigest();LOG=[]
with tempfile.TemporaryDirectory(prefix='hodge publication tests ') as td:
    temp=Path(td);marker=temp/'executed';payload='from pathlib import Path\nPath('+repr(str(marker))+').write_text("EXECUTED")\n'
    hostile=temp/'hostile';hostile.mkdir()
    for name in ['hashlib','json','pathlib','stat','os','io','zipfile','tempfile','sitecustomize','usercustomize']:(hostile/(name+'.py')).write_text(payload)
    env=os.environ.copy();env.update({'PYTHONPATH':str(hostile),'PYTHONHOME':str(hostile),'PYTHONSTARTUP':str(hostile/'sitecustomize.py')})
    def run(name,r,opt,diagnostic=None,flags=None,entry='integrity',hostile_env=False):
        f=['-I','-S','-B'] if flags is None else flags
        p=subprocess.run([sys.executable,*f,*(['-O'] if opt else []),'-c',LAUNCHER,str(r),pin,bp,entry],capture_output=True,text=True,cwd=hostile if hostile_env else temp,env=env if hostile_env else None,timeout=120)
        if diagnostic:need(p.returncode!=0 and not p.stdout and diagnostic in p.stderr,name+': expected rejection; '+p.stderr)
        else:need(p.returncode==0 and not p.stderr and json.loads(p.stdout)['status']=='PASS',name+': '+p.stderr)
        need(not marker.exists(),name+': marker executed')
        LOG.append({'case':name,'optimized':opt,'result':'rejected_before_payload' if diagnostic else 'passed','diagnostic':diagnostic})
    mutations={
      'proof byte':'payload hash mismatch: author/RESULTS.md','audit proof byte':'payload hash mismatch: audit/AUDIT.md',
      'author entrypoint':'payload hash mismatch: author/verify.py','audit entrypoint':'payload hash mismatch: audit/replay_audit.py','math entrypoint':'payload hash mismatch: audit/independent_math.py','publication entrypoint':'payload hash mismatch: verify_publication.py','test entrypoint':'payload hash mismatch: test_publication.py','bootstrap entrypoint':'REJECT: bootstrap anchor',
      'extra file':'strict inventory mismatch','missing proof':'strict inventory mismatch','empty directory':'strict inventory mismatch','nested manifest':'strict inventory mismatch','json shadow':'strict inventory mismatch','startup shadow':'strict inventory mismatch','legacy bytecode':'strict inventory mismatch','root cache':'strict inventory mismatch','author cache':'strict inventory mismatch','audit cache':'strict inventory mismatch',
      'proof symlink':'nonregular payload: author/RESULTS.md','manifest symlink':'nonregular payload: PUBLICATION_MANIFEST.json','bootstrap symlink':'REJECT: bootstrap type','FIFO':'nonregular payload: author/RESULTS.md','hardlink':'nonregular or hardlinked payload','root symlink':'REJECT: root ancestry','parent symlink':'REJECT: root ancestry','manifest byte':'external publication manifest pin mismatch','selfconsistent solved':'external publication manifest pin mismatch','archive byte':'payload hash mismatch: archives/HODGE_EXTREMALITY_30001913_AUTHOR_SAFE_FREEZE.zip'}
    for opt in (False,True):
        run('pristine',root,opt);run('hostile cwd and environment',root,opt,hostile_env=True)
        relocated=temp/('relocated with spaces '+str(opt));shutil.copytree(root,relocated);run('relocation',relocated,opt)
        for i,(name,diagnostic) in enumerate(mutations.items()):
            box=temp/(str(opt)+'-'+str(i));box.mkdir();r=box/'package';shutil.copytree(root,r)
            edits={'proof byte':'author/RESULTS.md','audit proof byte':'audit/AUDIT.md','author entrypoint':'author/verify.py','audit entrypoint':'audit/replay_audit.py','math entrypoint':'audit/independent_math.py','publication entrypoint':'verify_publication.py','test entrypoint':'test_publication.py','bootstrap entrypoint':'bootstrap.py'}
            if name in edits:(r/edits[name]).write_text(payload)
            elif name=='extra file':(r/'extra').write_text(payload)
            elif name=='missing proof':(r/'author/RESULTS.md').unlink()
            elif name=='empty directory':(r/'empty').mkdir()
            elif name=='nested manifest':(r/'nested').mkdir();(r/'nested/MANIFEST.json').write_text('{}')
            elif name=='json shadow':(r/'json.py').write_text(payload)
            elif name=='startup shadow':(r/'sitecustomize.py').write_text(payload)
            elif name=='legacy bytecode':(r/'bootstrap.pyc').write_bytes(b'untrusted')
            elif name.endswith('cache'):(r/({'root cache':'__pycache__','author cache':'author/__pycache__','audit cache':'audit/__pycache__'}[name])).mkdir()
            elif name in ['proof symlink','manifest symlink','bootstrap symlink']:
                target={'proof symlink':'author/RESULTS.md','manifest symlink':'PUBLICATION_MANIFEST.json','bootstrap symlink':'bootstrap.py'}[name];(r/target).unlink();(r/target).symlink_to(root/target)
            elif name=='FIFO':(r/'author/RESULTS.md').unlink();os.mkfifo(r/'author/RESULTS.md')
            elif name=='hardlink':outside=box/'linked';outside.write_bytes((r/'author/RESULTS.md').read_bytes());(r/'author/RESULTS.md').unlink();os.link(outside,r/'author/RESULTS.md')
            elif name=='root symlink':link=box/'link';link.symlink_to(r,target_is_directory=True);r=link
            elif name=='parent symlink':link=temp/('parentlink'+str(opt));link.symlink_to(box,target_is_directory=True);r=link/'package'
            elif name=='manifest byte':(r/'PUBLICATION_MANIFEST.json').write_text('{}')
            elif name=='selfconsistent solved':
                p=r/'PUBLICATION_METADATA.json';o=json.loads(p.read_text());o['status']='solved';p.write_text(json.dumps(o));m=r/'PUBLICATION_MANIFEST.json';v=json.loads(m.read_text());v['files']['PUBLICATION_METADATA.json']={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};m.write_text(json.dumps(v))
            elif name=='archive byte':p=r/'archives/HODGE_EXTREMALITY_30001913_AUTHOR_SAFE_FREEZE.zip';p.write_bytes(p.read_bytes()+b'x')
            run(name,r,opt,diagnostic)
        run('unsupported entrypoint',root,opt,'unsupported entrypoint',entry='author/verify.py')
        for missing in ('-I','-S','-B'):run('missing '+missing,root,opt,'REJECT: require -I -S -B',flags=[f for f in ('-I','-S','-B') if f!=missing])
print(json.dumps({'problem_id':30001913,'status':'PASS','controls':len(LOG),'normal_controls':sum(not r['optimized'] for r in LOG),'optimized_controls':sum(r['optimized'] for r in LOG),'all_markers_unexecuted':True,'cases':LOG},sort_keys=True,indent=2))
