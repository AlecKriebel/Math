#!/usr/bin/env python3
"""Source-free, nonroot replay and rejection tests; all mutations are temporary."""
from pathlib import Path
import hashlib,json,os,shutil,stat,subprocess,sys,tempfile

class Failure(Exception):pass
def need(ok,msg):
    if not ok:raise Failure(msg)
def sha(x):return hashlib.sha256(x).hexdigest()
def snapshot(root):
    return {str(p.relative_to(root)):sha(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()}
def writable(root):
    root.chmod(0o755)
    for p in root.rglob('*'):
        if not p.is_symlink():p.chmod(0o755 if p.is_dir() else 0o644)
def copy(base,dest):
    shutil.copytree(base,dest);writable(dest)
def call(base,mode,args=(),direct=False,cwd=None,env=None):
    script=base/'packet/verify_math.py' if direct else base/'bootstrap.py'
    flags=[] if mode=='normal' else [mode]
    return subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*map(str,args)],cwd=cwd or base,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
def main():
    need(len(sys.argv)==1,'no arguments');need(os.geteuid()!=0 and os.getuid()!=0,'must run genuinely nonroot')
    base=Path(__file__).resolve().parent.parent;original=snapshot(base)
    modes=('normal','-O','-OO');positives=[];negatives=[];semantics=[];probes=[]
    with tempfile.TemporaryDirectory(prefix='mesh-preserver-controls-') as td:
        tmp=Path(td);expected=None
        for mode in modes:
            r=call(base,mode,cwd=tmp);need(r.returncode==0,'original '+mode+': '+r.stderr.decode())
            expected=expected or r.stdout;need(r.stdout==expected,'mode-dependent output');positives.append('original '+mode)
        ro=tmp/'relocated';copy(base,ro)
        for p in ro.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
        ro.chmod(0o555);before=snapshot(ro)
        # Both directory creation and mutation of an existing regular file must fail.
        for label,fn in [('create-in-root',lambda:(ro/'forbidden').write_text('no')),('create-in-packet',lambda:(ro/'packet/forbidden').write_text('no')),('write-existing',lambda:(ro/'packet/REPORT.md').open('wb'))]:
            try:handle=fn()
            except PermissionError:probes.append(label);continue
            if hasattr(handle,'close'):handle.close()
            raise Failure('read-only probe unexpectedly succeeded: '+label)
        for mode in modes:
            r=call(ro,mode,cwd=tmp);need(r.returncode==0 and r.stdout==expected,'read-only replay '+mode);positives.append('read-only '+mode)
        need(snapshot(ro)==before,'read-only bytes changed');writable(ro)
        names=sorted(p.name for p in (base/'packet').iterdir());cases=[]
        for name in names:
            cases.append(('byte-drift-'+name,lambda d,n=name:(d/'packet'/n).write_bytes((d/'packet'/n).read_bytes()+b'!')))
            cases.append(('missing-'+name,lambda d,n=name:(d/'packet'/n).unlink()))
        cases += [('extra-file',lambda d:(d/'packet/extra').write_text('x')),('extra-directory',lambda d:(d/'packet/extra').mkdir()),('missing-manifest',lambda d:(d/'AUTHOR_MANIFEST.json').unlink()),('malformed-manifest',lambda d:(d/'AUTHOR_MANIFEST.json').write_text('{bad')),('truncated-manifest',lambda d:(d/'AUTHOR_MANIFEST.json').write_bytes(b''))]
        def mutate_manifest(d,key,value):
            p=d/'AUTHOR_MANIFEST.json';m=json.loads(p.read_text());m[key]=value;p.write_text(json.dumps(m))
        for key,val in [('problem_id',True),('new_mathematical_approaches',False),('files',{}),('schema',1.0)]:cases.append(('forged-manifest-'+key,lambda d,k=key,v=val:mutate_manifest(d,k,v)))
        def forged(d):
            p=d/'packet/verify_math.py';p.write_text("from pathlib import Path\nPath('../EXECUTED').write_text('bad')\n")
            mp=d/'AUTHOR_MANIFEST.json';m=json.loads(mp.read_text())
            for e in m['files']:
                if e['path']=='verify_math.py':b=p.read_bytes();e.update(bytes=len(b),sha256=sha(b))
            mp.write_text(json.dumps(m))
        cases.append(('self-consistent-hostile-manifest',forged))
        def hostile(d):(d/'packet/verify_math.py').write_text("from pathlib import Path\nPath('../EXECUTED').write_text('bad')\n")
        cases.append(('unauthenticated-execution',hostile))
        def link(d,name):
            p=d/name;b=p.read_bytes();p.unlink();outside=d/('outside-'+p.name);outside.write_bytes(b);p.symlink_to(outside)
        cases.append(('symlink-payload',lambda d:link(d,'packet/REPORT.md')))
        cases.append(('symlink-manifest',lambda d:link(d,'AUTHOR_MANIFEST.json')))
        def linkroot(d):
            (d/'packet').rename(d/'elsewhere');(d/'packet').symlink_to(d/'elsewhere',target_is_directory=True)
        cases.append(('symlink-packet',linkroot))
        def directory(d):p=d/'packet/REPORT.md';p.unlink();p.mkdir()
        def fifo(d):p=d/'packet/REPORT.md';p.unlink();os.mkfifo(p)
        cases.append(('directory-payload',directory));cases.append(('fifo-payload',fifo))
        def imports(d):
            (d/'packet/fractions.py').write_text("from pathlib import Path\nPath('../EXECUTED').write_text('bad')\n")
        cases.append(('hostile-extra-import',imports))
        for i,(label,change) in enumerate(cases):
            d=tmp/('bad-'+str(i));copy(base,d);change(d)
            for mode in modes:
                r=call(d,mode,cwd=tmp);need(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'bad case accepted: '+label+' '+mode)
                need(not (d/'EXECUTED').exists(),'hostile code executed');negatives.append(label+' '+mode)
        # Ambient untrusted modules must be ignored even when packet validation succeeds.
        poison=tmp/'poison';poison.mkdir();marker=tmp/'IMPORT_EXECUTED'
        for module in ['fractions.py','sitecustomize.py','json.py']:(poison/module).write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("bad")\n')
        env=dict(os.environ);env['PYTHONPATH']=str(poison)
        for mode in modes:
            r=call(base,mode,cwd=poison,env=env);need(r.returncode==0 and r.stdout==expected and not marker.exists(),'ambient import attack '+mode);positives.append('isolated-import '+mode)
        valid=json.loads((base/'packet/CLAIMS.json').read_text());bad=[]
        for key in ['problem_id','rank','new_mathematical_approaches']:
            for val in [True,False,float(valid[key]),str(valid[key]),None]:
                c=dict(valid);c[key]=val;bad.append((key+'-'+repr(val),json.dumps(c)))
        for key in ['zero_output_allowed','finite_checks_are_proof','novelty_claimed']:
            for val in [int(valid[key]),not valid[key],'false',None]:
                c=dict(valid);c[key]=val;bad.append((key+'-'+repr(val),json.dumps(c)))
        for key,val in [('disposition','claimed_solved'),('solution_credit','this report'),('independent_review','passed'),('universal_theorem_dependency','none')]:
            c=dict(valid);c[key]=val;bad.append((key,json.dumps(c)))
        c=dict(valid);c['extra']=0;bad.append(('extra-key',json.dumps(c)))
        c=dict(valid);del c['rank'];bad.append(('missing-key',json.dumps(c)))
        bad += [('duplicate-key','{"rank":1030,"rank":1030}'),('nonfinite','{"rank":NaN}'),('malformed','{bad'),('top-level-list','[]')]
        for i,(label,body) in enumerate(bad):
            path=tmp/('claims-'+str(i)+'.json');path.write_text(body)
            for mode in modes:
                r=call(base,mode,('--claims',path),direct=True,cwd=tmp)
                need(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'semantic acceptance: '+label);semantics.append(label+' '+mode)
        need(snapshot(base)==original,'original distribution bytes changed')
    return {'schema':'mesh-preserver-controls-v1','status':'PASS','uid':os.getuid(),'euid':os.geteuid(),'modes':list(modes),'positive_replays':len(positives),'integrity_rejections':len(negatives),'integrity_cases':len(cases),'semantic_rejections':len(semantics),'semantic_cases':len(bad),'read_only_write_denials':probes,'bytes_unchanged':True,'positives':positives,'negatives':negatives,'semantic_negatives':semantics,'scope':'Authenticates and tests finite diagnostics; not an independent mathematical audit or hosted CI.'}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,indent=2))
    except (Failure,OSError,ValueError,TypeError,KeyError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
